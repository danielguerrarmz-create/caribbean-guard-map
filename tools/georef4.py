"""Georeference the stitched base image by matching the coastline EDGE.

Why this and not the previous attempts:
  georef.py  sparse SIFT     -> 5 inliers. The generative upscale destroyed the
                                fine texture, so there is nothing to match.
  georef3.py filled land mask -> degenerate. Correlating filled regions lets big
                                uniform areas of ocean and jungle dominate the
                                score, which just rewards the smallest template.

The shape information is in the boundary, so reduce both images to a thin
coastline curve and brute force scale x rotation. A correct alignment produces
a single sharp peak; a degenerate one does not, and we check for that.
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


def coast_edge(a, pct=45):
    """a: float32 HxWx3 in [0,1] -> thin, lightly blurred coastline curve."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    idx = (b - g) + 0.35 * (b - r)
    idx = (idx - idx.min()) / (np.ptp(idx) + 1e-6)
    m = (idx > np.percentile(idx, pct)).astype(np.uint8)
    k = np.ones((7, 7), np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, k)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((13, 13), np.uint8))
    # keep only the largest water body, so lagoons and dark roofs drop out
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    if n > 1:
        big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        m = (lab == big).astype(np.uint8)
    edge = cv2.morphologyEx(m, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(np.float32)
    return cv2.GaussianBlur(edge, (0, 0), 2.5)


def resize_rgb(arr, w):
    h = max(1, int(round(w * arr.shape[0] / arr.shape[1])))
    return cv2.resize(arr, (w, h), interpolation=cv2.INTER_AREA)


def main():
    ref, tx0, ty0 = load_ref()
    RW, RH = ref.size
    nlat, _ = tile2deg(tx0, ty0, Z)
    rs = GW / RW
    mpp_px = 156543.03392 * math.cos(math.radians(nlat)) / (2 ** Z)
    ref_mpp = mpp_px / rs
    print(f"reference {RW}x{RH}, {ref_mpp:.3f} m per working px")

    ref_arr = np.asarray(ref.convert("RGB")).astype(np.float32) / 255.0
    ref_e = coast_edge(resize_rgb(ref_arr, GW))
    cv2.imwrite(os.path.join(HERE, "dbg_ref_edge.png"), (ref_e * 255).astype(np.uint8))

    base_pil = Image.open(BASE); BW, BH = base_pil.size
    small = np.asarray(base_pil.resize((3000, int(3000 * BH / BW)), Image.LANCZOS)
                       ).astype(np.float32) / 255.0

    # Extract each coastline ONCE at good resolution. Rescaling the edge map is
    # safe; re-running morphology at every candidate size was not, because at the
    # small end the kernels erased the curve and matchTemplate then returned a
    # meaningless 1.0 against an empty template.
    base_e_full = coast_edge(resize_rgb(small, 3000))
    cv2.imwrite(os.path.join(HERE, "dbg_base_edge.png"), (base_e_full*255).astype(np.uint8))
    BEH, BEW = base_e_full.shape

    results, skipped = [], 0
    for km in np.arange(6.0, 18.01, 0.25):
        bw = int(km * 1000 / ref_mpp)
        if bw < 200:
            continue
        be = cv2.resize(base_e_full, (bw, max(1, int(round(bw * BEH / BEW)))),
                        interpolation=cv2.INTER_AREA)
        be = cv2.GaussianBlur(be, (0, 0), 1.6)
        th, tw = be.shape
        # A template with almost no variance correlates perfectly with anything.
        if be.std() < 0.01 or (be > 0.05).sum() < 0.02 * be.size:
            skipped += 1
            continue
        for deg in np.arange(-6.0, 6.01, 0.5):
            R = cv2.getRotationMatrix2D((tw / 2, th / 2), deg, 1.0)
            cos, sin = abs(R[0, 0]), abs(R[0, 1])
            nw, nh = int(th * sin + tw * cos), int(th * cos + tw * sin)
            R[0, 2] += nw / 2 - tw / 2; R[1, 2] += nh / 2 - th / 2
            rot = cv2.warpAffine(be, R, (nw, nh))
            if nh + 2 >= ref_e.shape[0] or nw + 2 >= ref_e.shape[1] or rot.std() < 0.01:
                continue
            res = cv2.matchTemplate(ref_e, rot, cv2.TM_CCOEFF_NORMED)
            _, peak, _, loc = cv2.minMaxLoc(res)
            results.append((peak, km, deg, bw, loc, R.copy()))
    print(f"candidates {len(results)}, scales skipped as degenerate {skipped}")

    if not results:
        sys.exit("no candidates")
    results.sort(key=lambda r: -r[0])
    print("\ntop 8 (scale x rotation):")
    for p, km, deg, bw, loc, _ in results[:8]:
        print(f"  {km:5.2f} km  {deg:+5.1f} deg  corr {p:.4f}  at {loc}")

    peak, km, deg, bw, loc, R = results[0]

    # Is the peak actually distinctive, or is everything equally good?
    scores = np.array([r[0] for r in results])
    print(f"\npeak {peak:.4f}, field mean {scores.mean():.4f}, sd {scores.std():.4f}, "
          f"z = {(peak - scores.mean())/(scores.std()+1e-9):.1f}")
    # and is the best scale a genuine interior maximum rather than a sweep edge?
    by_km = {}
    for p, k, d, *_ in results:
        by_km[k] = max(by_km.get(k, 0), p)
        ks = sorted(by_km)
    best_km = max(by_km, key=by_km.get)
    print(f"best scale {best_km:.2f} km "
          f"({'interior maximum, good' if ks[0] < best_km < ks[-1] else 'AT SWEEP EDGE, suspect'})")

    # ---- compose base full px -> reference working px ----
    S = np.array([[bw / BW, 0, 0], [0, bw / BW, 0], [0, 0, 1]], float)
    Rh = np.vstack([R, [0, 0, 1]]).astype(float)
    T = np.array([[1, 0, loc[0]], [0, 1, loc[1]], [0, 0, 1]], float)
    A = T @ Rh @ S

    corners = np.array([[0, 0, 1], [BW, 0, 1], [BW, BH, 1], [0, BH, 1]], float).T
    rc = (A @ corners).T[:, :2] / rs
    lls = [tile2deg(tx0 + px / TS, ty0 + py / TS, Z) for px, py in rc]
    for nm, (la, lo) in zip(["NW", "NE", "SE", "SW"], lls):
        print(f"  {nm}  {la:.6f}, {lo:.6f}")

    lats = [p[0] for p in lls]; lons = [p[1] for p in lls]
    span_m = (max(lons) - min(lons)) * 111320 * math.cos(math.radians(np.mean(lats)))
    print(f"\ncoverage {span_m/1000:.2f} km east-west, "
          f"{span_m/BW*100:.1f} cm per source pixel, rotation {deg:+.1f} deg")
    print(f"IMG_BOUNDS = [[{min(lats):.6f}, {min(lons):.6f}], [{max(lats):.6f}, {max(lons):.6f}]];")

    json.dump({"corners": dict(zip(["NW", "NE", "SE", "SW"], lls)),
               "rotation_deg": float(deg), "corr": float(peak),
               "bounds": [[min(lats), min(lons)], [max(lats), max(lons)]],
               "span_km": span_m / 1000, "cm_per_px": span_m / BW * 100,
               "zoom": Z, "ref_origin_tile": [tx0, ty0]},
              open(os.path.join(HERE, "georef.json"), "w"), indent=2)

    be = cv2.resize(base_e_full, (bw, max(1, int(round(bw*BEH/BEW)))), interpolation=cv2.INTER_AREA)
    rot = cv2.warpAffine(be, R, (int(A[0, 2] * 0 + ref_e.shape[1]), ref_e.shape[0]))
    canvas = np.zeros_like(ref_e)
    rr = cv2.warpAffine(be, R, (rot.shape[1], rot.shape[0]))
    h = min(canvas.shape[0] - loc[1], rr.shape[0]); w = min(canvas.shape[1] - loc[0], rr.shape[1])
    canvas[loc[1]:loc[1]+h, loc[0]:loc[0]+w] = rr[:h, :w]
    ov = np.zeros((*ref_e.shape, 3), np.uint8)
    ov[..., 1] = np.clip(ref_e * 700, 0, 255).astype(np.uint8)   # green = Bing truth
    ov[..., 2] = np.clip(canvas * 700, 0, 255).astype(np.uint8)  # red   = yours
    cv2.imwrite(os.path.join(HERE, "align_overlay.png"), ov)
    print("overlay: align_overlay.png  (yellow where they agree)")


if __name__ == "__main__":
    main()
