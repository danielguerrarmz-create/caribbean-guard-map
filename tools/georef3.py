"""Georeference the stitched base image against Bing (known coordinates).

Two stage, because the expensive parts should run once each:
  1. Coarse: sweep candidate ground scales, score each with a single normalised
     cross-correlation of the land/water mask. Cheap, and it finds roughly where
     and how big the image is.
  2. Fine: run ECC (which solves rotation as well) on only the best few.

Everything is derived from the coastline rather than from image texture,
because the base has been through a generative upscaler and its fine detail no
longer corresponds to any real imagery.
"""
import glob, json, math, os, sys
import numpy as np, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:\Users\danie\Downloads\caribbean-guard-cuts\Complete Mapping.jpg"
Z, TS = 17, 256
GW = 1600


def tile2deg(x, y, z):
    n = 2 ** z
    return (math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))),
            x / n * 360.0 - 180.0)


def load_ref():
    files = glob.glob(os.path.join(HERE, "tilecache", f"{Z}_*.jpg"))
    if not files:
        sys.exit("no tile cache; run georef2.py first")
    xs = sorted({int(os.path.basename(f).split("_")[1]) for f in files})
    ys = sorted({int(os.path.basename(f).split("_")[2].split(".")[0]) for f in files})
    x0, y0 = xs[0], ys[0]
    mos = Image.new("RGB", ((xs[-1]-x0+1)*TS, (ys[-1]-y0+1)*TS))
    for f in files:
        _, x, y = os.path.basename(f).replace(".jpg", "").split("_")
        try:
            mos.paste(Image.open(f).convert("RGB"), ((int(x)-x0)*TS, (int(y)-y0)*TS))
        except Exception:
            pass
    print(f"reference: {len(files)} tiles, {mos.size[0]}x{mos.size[1]}px, origin tile {x0},{y0}")
    return mos, x0, y0


def mask_from_array(a, blur_div=90.0):
    """a: float32 HxWx3 in [0,1]. Returns smooth [0,1] field, high on water."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    idx = (b - g) + 0.35 * (b - r)
    idx = (idx - idx.min()) / (np.ptp(idx) + 1e-6)
    m = (idx > np.percentile(idx, 45)).astype(np.float32)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return cv2.GaussianBlur(m, (0, 0), max(1.0, m.shape[1] / blur_div))


def field(pil_or_arr, width):
    if isinstance(pil_or_arr, Image.Image):
        im = pil_or_arr.convert("RGB")
        im = im.resize((width, max(1, int(width * im.size[1] / im.size[0]))), Image.LANCZOS)
        a = np.asarray(im).astype(np.float32) / 255.0
    else:
        h = max(1, int(width * pil_or_arr.shape[0] / pil_or_arr.shape[1]))
        a = cv2.resize(pil_or_arr, (width, h), interpolation=cv2.INTER_AREA)
    return mask_from_array(a)


def main():
    ref, tx0, ty0 = load_ref()
    RW, RH = ref.size
    nlat, wlon = tile2deg(tx0, ty0, Z)

    ref_f = field(ref, GW)
    rs = GW / RW
    mpp_px = 156543.03392 * math.cos(math.radians(nlat)) / (2 ** Z)   # m per full-res ref px
    ref_mpp = mpp_px / rs                                             # m per working px
    print(f"reference {mpp_px:.3f} m/px full, {ref_mpp:.3f} m per working px")
    cv2.imwrite(os.path.join(HERE, "mask_ref.png"), (ref_f * 255).astype(np.uint8))

    # Downsample the 63 MP source ONCE, then rescale from this cheap copy.
    base_pil = Image.open(BASE); BW, BH = base_pil.size
    small = np.asarray(base_pil.resize((3000, int(3000 * BH / BW)), Image.LANCZOS)
                       ).astype(np.float32) / 255.0
    print(f"base {BW}x{BH}, working copy {small.shape[1]}x{small.shape[0]}")

    # ---- stage 1: coarse scale + translation by cross-correlation ----
    cands = []
    for km in np.arange(6.0, 18.01, 0.2):
        bw = int(km * 1000 / ref_mpp)
        bf = field(small, bw)
        if bf.shape[0] + 4 >= ref_f.shape[0] or bf.shape[1] + 4 >= ref_f.shape[1]:
            continue
        res = cv2.matchTemplate(ref_f, bf, cv2.TM_CCOEFF_NORMED)
        _, peak, _, loc = cv2.minMaxLoc(res)
        cands.append((peak, km, bw, loc))
    cands.sort(reverse=True)
    print("\ncoarse, best 5 by correlation:")
    for p, km, bw, loc in cands[:5]:
        print(f"  {km:5.2f} km  ncc {p:.4f}  at {loc}")

    # ---- stage 2: ECC refine the top few (this also solves rotation) ----
    best = None
    for peak, km, bw, loc in cands[:5]:
        bf = field(small, bw)
        pre = np.eye(2, 3, dtype=np.float32); pre[0, 2], pre[1, 2] = loc
        canvas = cv2.warpAffine(bf, pre, (ref_f.shape[1], ref_f.shape[0]))
        try:
            cc, wm = cv2.findTransformECC(
                ref_f, canvas, np.eye(2, 3, dtype=np.float32), cv2.MOTION_EUCLIDEAN,
                (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), None, 5)
        except cv2.error:
            continue
        print(f"  ECC {km:5.2f} km: {peak:.4f} -> {cc:.4f}")
        if best is None or cc > best[0]:
            best = (cc, km, bw, wm.copy(), pre.copy())

    if best is None:
        sys.exit("alignment failed")
    cc, km, bw, wm, pre = best
    print(f"\nBEST span {km:.2f} km, ECC {cc:.4f}")

    # base full px -> working px -> placed canvas -> reference working px -> ref full px
    s = bw / BW
    A = np.linalg.inv(np.vstack([wm, [0, 0, 1]]).astype(np.float64)) @ \
        np.array([[s, 0, pre[0, 2]], [0, s, pre[1, 2]], [0, 0, 1]], float)
    rot = math.degrees(math.atan2(A[1, 0], A[0, 0]))
    sc = math.hypot(A[0, 0], A[1, 0])
    print(f"rotation {rot:+.3f} deg, {ref_mpp/sc*100:.1f} cm per source pixel")

    corners = np.array([[0, 0, 1], [BW, 0, 1], [BW, BH, 1], [0, BH, 1]], float).T
    rc = (A @ corners).T[:, :2] / rs
    lls = [tile2deg(tx0 + px / TS, ty0 + py / TS, Z) for px, py in rc]
    for nm, (la, lo) in zip(["NW", "NE", "SE", "SW"], lls):
        print(f"  {nm}  {la:.6f}, {lo:.6f}")

    lats = [p[0] for p in lls]; lons = [p[1] for p in lls]
    span_m = (max(lons) - min(lons)) * 111320 * math.cos(math.radians(np.mean(lats)))
    print(f"\ncoverage {span_m/1000:.2f} km east-west")
    print(f"IMG_BOUNDS = [[{min(lats):.6f}, {min(lons):.6f}], [{max(lats):.6f}, {max(lons):.6f}]];")

    json.dump({"corners": dict(zip(["NW", "NE", "SE", "SW"], lls)),
               "rotation_deg": rot, "ecc": float(cc),
               "bounds": [[min(lats), min(lons)], [max(lats), max(lons)]],
               "span_km": span_m / 1000, "zoom": Z,
               "ref_origin_tile": [tx0, ty0]},
              open(os.path.join(HERE, "georef.json"), "w"), indent=2)

    bf = field(small, bw)
    canvas = cv2.warpAffine(bf, pre, (ref_f.shape[1], ref_f.shape[0]))
    aligned = cv2.warpAffine(canvas, wm, (ref_f.shape[1], ref_f.shape[0]),
                             flags=cv2.WARP_INVERSE_MAP)
    ov = np.zeros((*ref_f.shape, 3), np.uint8)
    ov[..., 1] = (ref_f * 255).astype(np.uint8)      # green = Bing truth
    ov[..., 2] = (aligned * 255).astype(np.uint8)    # red   = your image (BGR)
    cv2.imwrite(os.path.join(HERE, "align_overlay.png"), ov)
    print("overlay: align_overlay.png (green = Bing, red = yours, yellow = agreement)")


if __name__ == "__main__":
    main()
