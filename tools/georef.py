"""Georeference the stitched Caribbean Guard base image.

Method: build a Bing Aerial mosaic whose geographic bounds are exact by
construction (XYZ tile maths), then feature-match the hand-stitched base
image against it and solve for the transform. Residuals are reported in
metres so the error is measured, not assumed.
"""
import io, math, os, sys, concurrent.futures as cf
import numpy as np, requests, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

OUT = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:\Users\danie\Downloads\caribbean-guard-cuts\Complete Mapping.jpg"

Z = 17
W, E = -82.800, -82.650          # generous, we crop by matching
S, N = 9.615, 9.685
TS = 256


def deg2tile(lat, lon, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    la = math.radians(lat)
    y = (1.0 - math.asinh(math.tan(la)) / math.pi) / 2.0 * n
    return x, y


def tile2deg(x, y, z):
    n = 2 ** z
    lon = x / n * 360.0 - 180.0
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    return lat, lon


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
    url = f"http://ecn.t{(x + y) % 4}.tiles.virtualearth.net/tiles/a{quadkey(x, y, Z)}.jpeg?g=1"
    for _ in range(3):
        try:
            r = requests.get(url, timeout=20,
                             headers={"User-Agent": "Mozilla/5.0 CaribbeanGuard/1.0"})
            if r.status_code == 200 and len(r.content) > 2000:
                return x, y, Image.open(io.BytesIO(r.content)).convert("RGB")
        except Exception:
            pass
    return x, y, None


def build_reference():
    x0f, y0f = deg2tile(N, W, Z)
    x1f, y1f = deg2tile(S, E, Z)
    x0, x1 = int(math.floor(x0f)), int(math.floor(x1f))
    y0, y1 = int(math.floor(y0f)), int(math.floor(y1f))
    jobs = [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
    print(f"reference: z{Z}, {x1-x0+1} x {y1-y0+1} = {len(jobs)} tiles")
    mos = Image.new("RGB", ((x1 - x0 + 1) * TS, (y1 - y0 + 1) * TS))
    ok = 0
    with cf.ThreadPoolExecutor(16) as ex:
        for x, y, im in ex.map(fetch, jobs):
            if im is not None:
                mos.paste(im, ((x - x0) * TS, (y - y0) * TS)); ok += 1
    print(f"  fetched {ok}/{len(jobs)}")
    nlat, wlon = tile2deg(x0, y0, Z)
    slat, elon = tile2deg(x1 + 1, y1 + 1, Z)
    return mos, (nlat, wlon, slat, elon)


def to_gray(pil, width):
    im = pil.convert("RGB")
    im = im.resize((width, int(width * im.size[1] / im.size[0])), Image.LANCZOS)
    g = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    # The base is AI-upscaled and colour shifted. Normalise aggressively so the
    # matcher keys on structure (coastline, roads, clearings) not tone.
    return cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(g)


def main():
    ref_pil, (nlat, wlon, slat, elon) = build_reference()
    ref_pil.save(os.path.join(OUT, "ref_mosaic.jpg"), quality=88)
    RW, RH = ref_pil.size
    print(f"  mosaic {RW}x{RH}px  N{nlat:.6f} W{wlon:.6f} S{slat:.6f} E{elon:.6f}")

    base_pil = Image.open(BASE)
    BW, BH = base_pil.size

    GW = 2400
    ref_g = to_gray(ref_pil, GW)
    base_g = to_gray(base_pil, GW)
    rs = GW / RW              # ref  gray px  per ref  full px
    bs = GW / BW              # base gray px per base full px

    det = cv2.SIFT_create(nfeatures=24000)
    k1, d1 = det.detectAndCompute(base_g, None)
    k2, d2 = det.detectAndCompute(ref_g, None)
    print(f"features: base {len(k1)}, ref {len(k2)}")

    matcher = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=64))
    raw = matcher.knnMatch(d1, d2, k=2)
    good = [m for m, n in raw if m.distance < 0.75 * n.distance]
    print(f"matches: {len(raw)} raw, {len(good)} after ratio test")
    if len(good) < 12:
        print("NOT ENOUGH MATCHES"); sys.exit(1)

    src = np.float32([k1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst = np.float32([k2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    # Partial affine = scale + rotation + translation. The right model for a
    # north-up screen capture. A full homography would happily absorb the
    # hand-stitch error into a fake perspective and hide the problem.
    M, inl = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC,
                                         ransacReprojThreshold=3.0,
                                         maxIters=20000, confidence=0.999)
    inl = inl.ravel().astype(bool)
    print(f"inliers: {inl.sum()}/{len(good)}")

    proj = cv2.transform(src, M).reshape(-1, 2)
    err = np.linalg.norm(proj - dst.reshape(-1, 2), axis=1)[inl]

    # metres per gray pixel of the reference
    mpp_ref = (156543.03392 * math.cos(math.radians((nlat + slat) / 2)) / (2 ** Z)) / rs
    print(f"\nresidual (inliers): median {np.median(err)*mpp_ref:6.1f} m   "
          f"p90 {np.percentile(err,90)*mpp_ref:6.1f} m   max {err.max()*mpp_ref:6.1f} m")

    scale = math.hypot(M[0, 0], M[0, 1])
    rot = math.degrees(math.atan2(M[0, 1], M[0, 0]))
    print(f"rotation {rot:+.3f} deg   scale {scale:.5f}")

    # corners of the base image -> reference gray px -> reference full px -> lat/lon
    corners = np.float32([[0, 0], [BW, 0], [BW, BH], [0, BH]]).reshape(-1, 1, 2) * bs
    rc = cv2.transform(corners, M).reshape(-1, 2) / rs

    x0f, y0f = deg2tile(nlat, wlon, Z)
    def px2ll(px, py):
        return tile2deg(x0f + px / TS, y0f + py / TS, Z)

    names = ["NW", "NE", "SE", "SW"]
    lls = []
    print("\ncorners of the stitched image:")
    for nm, (px, py) in zip(names, rc):
        la, lo = px2ll(px, py); lls.append((la, lo))
        print(f"  {nm}  {la:.6f}, {lo:.6f}")

    lats = [p[0] for p in lls]; lons = [p[1] for p in lls]
    print(f"\nIMG_BOUNDS = [[{min(lats):.6f}, {min(lons):.6f}], "
          f"[{max(lats):.6f}, {max(lons):.6f}]];")

    span_m = (max(lons)-min(lons)) * 111320 * math.cos(math.radians(np.mean(lats)))
    print(f"\ncoverage {span_m/1000:.2f} km east to west, "
          f"{BW/span_m:.3f} px/m  ({span_m/BW*100:.1f} cm per pixel)")

    vis = cv2.drawMatches(base_g, k1, ref_g, k2,
                          [g for g, i in zip(good, inl) if i][:80], None,
                          matchColor=(0, 255, 0), singlePointColor=None, flags=2)
    cv2.imwrite(os.path.join(OUT, "match_check.jpg"), vis)
    np.save(os.path.join(OUT, "affine.npy"), M)


if __name__ == "__main__":
    main()
