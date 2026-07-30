"""Georeference the stitched base image by aligning coastline, not features.

Sparse feature matching (georef.py) collapsed to 5 inliers: the base image has
been through a generative upscaler, so its fine texture no longer corresponds
to any real imagery. What DID survive that process is the shape of the coast.

So: reduce both images to a land/water mask, blur into a smooth potential
field, and solve for a Euclidean transform using every pixel via ECC. Then
report the residual as a real distance along the coastline so the accuracy is
measured rather than claimed.
"""
import io, math, os, sys, json, concurrent.futures as cf
import numpy as np, requests, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "tilecache")
BASE = r"C:\Users\danie\Downloads\caribbean-guard-cuts\Complete Mapping.jpg"
os.makedirs(CACHE, exist_ok=True)

Z, TS = 17, 256
W, E, S, N = -82.800, -82.650, 9.615, 9.685
GW = 2000                      # working width for both images


def deg2tile(lat, lon, z):
    n = 2 ** z
    return ((lon + 180.0) / 360.0 * n,
            (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n)


def tile2deg(x, y, z):
    n = 2 ** z
    return (math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))),
            x / n * 360.0 - 180.0)


def quadkey(x, y, z):
    q = ""
    for i in range(z, 0, -1):
        d, m = 0, 1 << (i - 1)
        if x & m: d += 1
        if y & m: d += 2
        q += str(d)
    return q


def fetch(args):
    x, y = args
    fp = os.path.join(CACHE, f"{Z}_{x}_{y}.jpg")
    if os.path.exists(fp) and os.path.getsize(fp) > 800:
        return x, y, Image.open(fp).convert("RGB")
    url = f"http://ecn.t{(x+y)%4}.tiles.virtualearth.net/tiles/a{quadkey(x,y,Z)}.jpeg?g=1"
    for attempt in range(5):
        try:
            r = requests.get(url, timeout=25,
                             headers={"User-Agent": "Mozilla/5.0 CaribbeanGuard/1.0"})
            if r.status_code == 200 and len(r.content) > 800 and len(r.content) != 1033:
                open(fp, "wb").write(r.content)
                return x, y, Image.open(io.BytesIO(r.content)).convert("RGB")
        except Exception:
            pass
    return x, y, None


def build_reference():
    x0f, y0f = deg2tile(N, W, Z); x1f, y1f = deg2tile(S, E, Z)
    x0, x1 = int(x0f), int(x1f); y0, y1 = int(y0f), int(y1f)
    jobs = [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
    mos = Image.new("RGB", ((x1-x0+1)*TS, (y1-y0+1)*TS)); ok = 0
    with cf.ThreadPoolExecutor(8) as ex:
        for x, y, im in ex.map(fetch, jobs):
            if im is not None:
                mos.paste(im, ((x-x0)*TS, (y-y0)*TS)); ok += 1
    print(f"reference z{Z}: {ok}/{len(jobs)} tiles, {mos.size[0]}x{mos.size[1]}px")
    nlat, wlon = tile2deg(x0, y0, Z)
    slat, elon = tile2deg(x1+1, y1+1, Z)
    return mos, (nlat, wlon, slat, elon), (x0f, y0f)


def water_field(pil, width, invert_hint=False):
    """Return a smooth [0,1] field, high on water. Uses the blue/green
    relationship, which holds in both real and upscaled imagery even when
    absolute colour has drifted."""
    im = pil.convert("RGB")
    im = im.resize((width, max(1, int(width * im.size[1] / im.size[0]))), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # water: blue >= green and low overall green excess; land (jungle): green dominant
    idx = (b - g) + 0.35 * (b - r)
    idx = (idx - idx.min()) / (np.ptp(idx) + 1e-6)
    m = (idx > np.percentile(idx, 42)).astype(np.float32)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return cv2.GaussianBlur(m, (0, 0), width / 90.0)


def main():
    ref_pil, (nlat, wlon, slat, elon), (x0f, y0f) = build_reference()
    RW, RH = ref_pil.size
    base_pil = Image.open(BASE); BW, BH = base_pil.size

    # ground scale of each, in metres per full-res pixel
    # 156543.03392 * cos(lat) / 2^z is ALREADY metres per pixel at 256px tiles.
    mpp_tile = 156543.03392 * math.cos(math.radians((nlat+slat)/2)) / (2**Z)
    ref_f = water_field(ref_pil, GW)
    rs = GW / RW
    ref_mpp = mpp_tile / rs
    print(f"reference {ref_mpp:.2f} m per working px")

    Image.fromarray((ref_f*255).astype(np.uint8)).save(os.path.join(HERE, "mask_ref.png"))

    best = None
    # The base image's ground scale is unknown, so sweep it. For each candidate
    # scale, seed the translation with normalised cross-correlation (ECC will
    # not converge from an arbitrary offset), then let ECC refine rotation.
    for guess_km in np.arange(6.0, 18.01, 0.25):
        bw = int(guess_km * 1000 / ref_mpp)
        bf = water_field(base_pil, bw)
        h, w = bf.shape
        if h + 4 >= ref_f.shape[0] or w + 4 >= ref_f.shape[1]:
            continue

        res = cv2.matchTemplate(ref_f, bf, cv2.TM_CCOEFF_NORMED)
        _, peak, _, loc = cv2.minMaxLoc(res)

        pre = np.eye(2, 3, dtype=np.float32)
        pre[0, 2] = loc[0]; pre[1, 2] = loc[1]
        canvas = cv2.warpAffine(bf, pre, (ref_f.shape[1], ref_f.shape[0]))
        try:
            crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 300, 1e-6)
            wm = np.eye(2, 3, dtype=np.float32)
            cc, wm = cv2.findTransformECC(ref_f, canvas, wm,
                                          cv2.MOTION_EUCLIDEAN, crit, None, 5)
        except cv2.error:
            cc, wm = peak, np.eye(2, 3, dtype=np.float32)
        if best is None or cc > best[0]:
            best = (cc, guess_km, bw, wm.copy(), pre.copy())
            print(f"  span {guess_km:5.2f} km  ncc {peak:.4f} -> ECC {cc:.4f}")

    if best is None:
        print("alignment failed"); sys.exit(1)

    cc, span_km, bw, wm, pre = best
    print(f"\nBEST: span {span_km:.1f} km, ECC correlation {cc:.4f}")

    # compose: base full px -> base working px -> centred canvas -> reference field px
    s = bw / BW
    A_pre = np.array([[s, 0, pre[0, 2]], [0, s, pre[1, 2]], [0, 0, 1]], dtype=np.float64)
    # wm maps reference -> canvas, so invert it
    Wm = np.vstack([wm, [0, 0, 1]]).astype(np.float64)
    A = np.linalg.inv(Wm) @ A_pre

    rot = math.degrees(math.atan2(A[1, 0], A[0, 0]))
    scale = math.hypot(A[0, 0], A[1, 0])
    print(f"rotation {rot:+.3f} deg, {ref_mpp/scale*100:.1f} cm per source pixel")

    corners = np.array([[0, 0, 1], [BW, 0, 1], [BW, BH, 1], [0, BH, 1]], dtype=np.float64).T
    rc = (A @ corners).T[:, :2] / rs          # -> reference FULL px

    def px2ll(px, py):
        return tile2deg(x0f + px/TS, y0f + py/TS, Z)

    lls = [px2ll(px, py) for px, py in rc]
    for nm, (la, lo) in zip(["NW", "NE", "SE", "SW"], lls):
        print(f"  {nm}  {la:.6f}, {lo:.6f}")

    lats = [p[0] for p in lls]; lons = [p[1] for p in lls]
    mid = np.mean(lats)
    span_m = (max(lons)-min(lons)) * 111320 * math.cos(math.radians(mid))
    print(f"\ncoverage {span_m/1000:.2f} km east-west")
    print(f"IMG_BOUNDS = [[{min(lats):.6f}, {min(lons):.6f}], [{max(lats):.6f}, {max(lons):.6f}]];")

    json.dump({"corners": {k: v for k, v in zip(["NW","NE","SE","SW"], lls)},
               "rotation_deg": rot, "ecc": float(cc),
               "bounds": [[min(lats), min(lons)], [max(lats), max(lons)]],
               "span_km": span_m/1000},
              open(os.path.join(HERE, "georef.json"), "w"), indent=2)

    # visual proof: base coastline warped onto the reference
    bf = water_field(base_pil, bw)
    canvas = cv2.warpAffine(bf, pre, (ref_f.shape[1], ref_f.shape[0]))
    aligned = cv2.warpAffine(canvas, wm, (ref_f.shape[1], ref_f.shape[0]),
                             flags=cv2.WARP_INVERSE_MAP)
    ov = np.zeros((*ref_f.shape, 3), np.uint8)
    ov[..., 1] = (ref_f*255).astype(np.uint8)      # reference = green
    ov[..., 0] = (aligned*255).astype(np.uint8)    # base      = red
    cv2.imwrite(os.path.join(HERE, "align_overlay.png"), ov)
    print("\noverlay written: align_overlay.png (green = Bing truth, red = your image)")


if __name__ == "__main__":
    main()
