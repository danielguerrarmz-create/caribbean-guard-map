"""Georeference the stitched base image by chamfer matching the coastline.

Correlation kept returning spurious perfect scores: TM_CCOEFF_NORMED divides by
the local standard deviation, and an edge map is mostly empty, so wherever the
reference patch is flat the denominator collapses and any template "matches".

Chamfer matching avoids that entirely. Build a distance transform of the true
coastline, then for a candidate placement measure the mean distance from your
coastline to the nearest true coastline. Because sum-of-distances over a
translated point set is a convolution, every translation is evaluated at once
with a single correlation against the distance field.

The score is a real quantity: mean coastline error in metres. Lower is better.
"""
import glob, json, math, os, sys
import numpy as np, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:\Users\danie\Downloads\caribbean-guard-cuts\Complete Mapping.jpg"
Z, TS, GW = 17, 256, 1600


def tile2deg(x, y, z):
    n = 2 ** z
    return (math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))),
            x / n * 360.0 - 180.0)


def load_ref():
    files = glob.glob(os.path.join(HERE, "tilecache", f"{Z}_*.jpg"))
    if not files:
        sys.exit("no tile cache")
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
    return mos, x0, y0


def coast_binary(a, pct=45):
    """float32 HxWx3 in [0,1] -> uint8 coastline curve (1 px wide-ish)."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    idx = (b - g) + 0.35 * (b - r)
    idx = (idx - idx.min()) / (np.ptp(idx) + 1e-6)
    m = (idx > np.percentile(idx, pct)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    if n > 1:                       # keep the sea, drop lagoons and dark roofs
        m = (lab == 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
    return cv2.morphologyEx(m, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))


def resize_rgb(arr, w):
    return cv2.resize(arr, (w, max(1, int(round(w * arr.shape[0] / arr.shape[1])))),
                      interpolation=cv2.INTER_AREA)


def main():
    ref, tx0, ty0 = load_ref()
    RW, RH = ref.size
    nlat, _ = tile2deg(tx0, ty0, Z)
    rs = GW / RW
    ref_mpp = (156543.03392 * math.cos(math.radians(nlat)) / (2 ** Z)) / rs
    print(f"reference {RW}x{RH}px, {ref_mpp:.3f} m per working px")

    ref_arr = np.asarray(ref.convert("RGB")).astype(np.float32) / 255.0
    ref_c = coast_binary(resize_rgb(ref_arr, GW))
    cv2.imwrite(os.path.join(HERE, "dbg_ref_coast.png"), ref_c * 255)
    print(f"reference coastline pixels: {int(ref_c.sum())}")

    # distance (in working px) from every pixel to the nearest true coastline
    D = cv2.distanceTransform((1 - ref_c).astype(np.uint8), cv2.DIST_L2, 5).astype(np.float32)

    base_pil = Image.open(BASE); BW, BH = base_pil.size
    small = np.asarray(base_pil.resize((3000, int(3000 * BH / BW)), Image.LANCZOS)
                       ).astype(np.float32) / 255.0
    base_c = coast_binary(resize_rgb(small, 3000))
    cv2.imwrite(os.path.join(HERE, "dbg_base_coast.png"), base_c * 255)
    BEH, BEW = base_c.shape
    print(f"base coastline pixels: {int(base_c.sum())}")

    rows = []
    for km in np.arange(5.0, 18.01, 0.25):
        bw = int(km * 1000 / ref_mpp)
        bh = max(1, int(round(bw * BEH / BEW)))
        if bw < 150:
            continue
        be = (cv2.resize(base_c.astype(np.float32), (bw, bh),
                         interpolation=cv2.INTER_AREA) > 0.15).astype(np.float32)
        if be.sum() < 200:
            continue
        best_km = None
        for deg in np.arange(-8.0, 8.01, 0.5):
            R = cv2.getRotationMatrix2D((bw / 2, bh / 2), deg, 1.0)
            cos, sin = abs(R[0, 0]), abs(R[0, 1])
            nw, nh = int(bh * sin + bw * cos), int(bh * cos + bw * sin)
            R[0, 2] += nw / 2 - bw / 2; R[1, 2] += nh / 2 - bh / 2
            rot = (cv2.warpAffine(be, R, (nw, nh)) > 0.3).astype(np.float32)
            if nh + 2 >= D.shape[0] or nw + 2 >= D.shape[1] or rot.sum() < 200:
                continue
            # sum of D over the placed coastline, for every translation at once
            tot = cv2.matchTemplate(D, rot, cv2.TM_CCORR)
            mean_px = tot / rot.sum()
            mn, _, loc, _ = cv2.minMaxLoc(mean_px)
            if best_km is None or mn < best_km[0]:
                best_km = (mn, deg, bw, loc, R.copy())
        if best_km:
            rows.append((best_km[0] * ref_mpp, km) + best_km[1:])

    if not rows:
        sys.exit("no candidates")
    rows.sort()
    print("\nmean coastline error, best 10 (metres):")
    for err, km, deg, bw, loc, _ in rows[:10]:
        print(f"  {km:5.2f} km  {deg:+5.1f} deg  ->  {err:7.1f} m")

    # the profile matters as much as the winner: a real solution is a clear dip
    prof = sorted(((km, err) for err, km, *_ in rows))
    print("\nerror vs assumed span (m):")
    print("  " + "  ".join(f"{k:.0f}:{e:.0f}" for k, e in prof[::4]))

    err, km, deg, bw, loc, R = rows[0]
    ks = [k for k, _ in prof]
    interior = ks[0] < km < ks[-1]
    print(f"\nBEST {km:.2f} km, {deg:+.1f} deg, mean coastline error {err:.1f} m "
          f"({'interior minimum' if interior else 'AT SWEEP EDGE, suspect'})")

    S = np.array([[bw / BW, 0, 0], [0, bw / BW, 0], [0, 0, 1]], float)
    A = (np.array([[1, 0, loc[0]], [0, 1, loc[1]], [0, 0, 1]], float)
         @ np.vstack([R, [0, 0, 1]]).astype(float) @ S)

    corners = np.array([[0, 0, 1], [BW, 0, 1], [BW, BH, 1], [0, BH, 1]], float).T
    rc = (A @ corners).T[:, :2] / rs
    lls = [tile2deg(tx0 + px / TS, ty0 + py / TS, Z) for px, py in rc]
    for nm, (la, lo) in zip(["NW", "NE", "SE", "SW"], lls):
        print(f"  {nm}  {la:.6f}, {lo:.6f}")

    lats = [p[0] for p in lls]; lons = [p[1] for p in lls]
    span_m = (max(lons) - min(lons)) * 111320 * math.cos(math.radians(np.mean(lats)))
    print(f"\ncoverage {span_m/1000:.2f} km east-west, {span_m/BW*100:.1f} cm per source px")
    print(f"IMG_BOUNDS = [[{min(lats):.6f}, {min(lons):.6f}], [{max(lats):.6f}, {max(lons):.6f}]];")

    json.dump({"corners": dict(zip(["NW", "NE", "SE", "SW"], lls)),
               "rotation_deg": float(deg), "mean_coastline_error_m": float(err),
               "bounds": [[min(lats), min(lons)], [max(lats), max(lons)]],
               "span_km": span_m / 1000, "cm_per_px": span_m / BW * 100,
               "zoom": Z, "ref_origin_tile": [tx0, ty0], "interior_minimum": bool(interior)},
              open(os.path.join(HERE, "georef.json"), "w"), indent=2)

    bh = max(1, int(round(bw * BEH / BEW)))
    be = (cv2.resize(base_c.astype(np.float32), (bw, bh), interpolation=cv2.INTER_AREA) > .15).astype(np.float32)
    nw, nh = int(bh*abs(R[0,1]) + bw*abs(R[0,0])), int(bh*abs(R[0,0]) + bw*abs(R[0,1]))
    rot = cv2.warpAffine(be, R, (nw, nh))
    canvas = np.zeros_like(D)
    h = min(canvas.shape[0]-loc[1], rot.shape[0]); w = min(canvas.shape[1]-loc[0], rot.shape[1])
    canvas[loc[1]:loc[1]+h, loc[0]:loc[0]+w] = rot[:h, :w]
    ov = np.zeros((*D.shape, 3), np.uint8)
    ov[..., 1] = (cv2.dilate(ref_c, np.ones((2, 2), np.uint8)) * 255)      # green = Bing truth
    ov[..., 2] = (cv2.dilate(canvas, np.ones((2, 2), np.uint8)) * 255)     # red   = yours
    cv2.imwrite(os.path.join(HERE, "align_overlay.png"), ov)
    print("overlay: align_overlay.png (yellow = agreement)")


if __name__ == "__main__":
    main()
