"""Refine the georeference with local patch matching against Bing.

Global matching failed repeatedly because the generative upscale changed the
image texture and every global objective had a degenerate optimum. Local
matching does not have that problem: given a prior good to a few hundred
metres, each patch only has to be found inside a small search window, and a
wrong match is easy to reject on peak sharpness.

Prior comes from reading landmarks off the two images by hand:
Puerto Viejo town at 0.25 of the width is -82.7545, the Punta Uva point at
0.645 is -82.695.

Output is a similarity transform plus per-point residuals in metres, so the
accuracy is stated rather than assumed.
"""
import glob, json, math, os
import numpy as np, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:\Users\danie\Downloads\caribbean-guard-cuts\Complete Mapping.jpg"
Z, TS = 17, 256

# --- prior, from hand-read landmarks ---
LON_W, LON_E = -82.79215, -82.64155
LAT_N, LAT_S = 9.66670, 9.62400


def tile2deg(x, y, z):
    n = 2 ** z
    return (math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))),
            x / n * 360.0 - 180.0)


def deg2tile(lat, lon, z):
    n = 2 ** z
    return ((lon + 180.0) / 360.0 * n,
            (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n)


def load_ref():
    files = glob.glob(os.path.join(HERE, "tilecache", f"{Z}_*.jpg"))
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
    return np.asarray(mos), x0, y0


def prep(img):
    g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    g = cv2.createCLAHE(3.0, (8, 8)).apply(g)
    return cv2.GaussianBlur(g, (0, 0), 1.0).astype(np.float32)


def main():
    ref, tx0, ty0 = load_ref()
    RH, RW = ref.shape[:2]
    nlat, _ = tile2deg(tx0, ty0, Z)
    MPP = 156543.03392 * math.cos(math.radians(nlat)) / (2 ** Z)      # m per ref px
    print(f"reference {RW}x{RH}, {MPP:.3f} m/px")

    base = np.asarray(Image.open(BASE).convert("RGB"))
    BH, BW = base.shape[:2]
    base_mpp = (LON_E - LON_W) * 111320 * math.cos(math.radians(9.645)) / BW
    k = base_mpp / MPP        # resample base by this to reach reference scale
    print(f"base {BW}x{BH}, prior {base_mpp*100:.1f} cm/px, resample x{k:.4f}")

    def prior_ll(px, py):
        return (LAT_N + (LAT_S - LAT_N) * (py / BH),
                LON_W + (LON_E - LON_W) * (px / BW))

    def ll_to_refpx(lat, lon):
        tx, ty = deg2tile(lat, lon, Z)
        return (tx - tx0) * TS, (ty - ty0) * TS

    P = 420                    # base patch half-size, px  (~470 m)
    SEARCH_M = 900             # +/- window in the reference
    pts_b, pts_r, quality = [], [], []

    ys_frac = [0.24, 0.30, 0.36, 0.42, 0.48, 0.55, 0.62]
    peaks = []
    for xf in np.arange(0.04, 0.97, 0.02):
        for yf in ys_frac:
            bx, by = xf * BW, yf * BH
            if bx - P < 0 or bx + P > BW or by - P < 0 or by + P > BH:
                continue
            patch = base[int(by-P):int(by+P), int(bx-P):int(bx+P)]
            if patch.std() < 12:
                continue
            tw = max(24, int(2 * P * k))
            tmpl = prep(cv2.resize(patch, (tw, tw), interpolation=cv2.INTER_AREA))
            if tmpl.std() < 6:
                continue

            la, lo = prior_ll(bx, by)
            rx, ry = ll_to_refpx(la, lo)
            pad = int(SEARCH_M / MPP) + tw // 2
            x0, y0 = int(rx - pad), int(ry - pad)
            x1, y1 = int(rx + pad), int(ry + pad)
            if x0 < 0 or y0 < 0 or x1 > RW or y1 > RH:
                continue
            win = prep(ref[y0:y1, x0:x1])
            if win.shape[0] <= tw or win.shape[1] <= tw:
                continue

            res = cv2.matchTemplate(win, tmpl, cv2.TM_CCOEFF_NORMED)
            _, peak, _, loc = cv2.minMaxLoc(res)
            # reject unless the peak clearly beats the rest of the surface
            m = res.copy()
            cv2.circle(m, loc, max(3, tw // 6), float(res.min()), -1)
            second = float(m.max())
            peaks.append((peak, peak - second))
            if peak < 0.22 or peak - second < 0.03:
                continue
            pts_b.append([bx, by])
            pts_r.append([x0 + loc[0] + tw / 2, y0 + loc[1] + tw / 2])
            quality.append(peak - second)

    pts_b = np.array(pts_b, np.float32); pts_r = np.array(pts_r, np.float32)
    if peaks:
        pk = np.array(peaks)
        print(f"windows tried {len(pk)}, peak corr median {np.median(pk[:,0]):.3f}, "
              f"max {pk[:,0].max():.3f}; distinctness median {np.median(pk[:,1]):.3f}")
    print(f"accepted control points: {len(pts_b)}")
    if len(pts_b) < 8:
        raise SystemExit("too few control points; widen the search or lower the threshold")

    M, inl = cv2.estimateAffinePartial2D(pts_b.reshape(-1, 1, 2), pts_r.reshape(-1, 1, 2),
                                         method=cv2.RANSAC, ransacReprojThreshold=6.0,
                                         maxIters=50000, confidence=0.9999)
    inl = inl.ravel().astype(bool)
    proj = cv2.transform(pts_b.reshape(-1, 1, 2), M).reshape(-1, 2)
    err = np.linalg.norm(proj - pts_r, axis=1) * MPP
    print(f"inliers {inl.sum()}/{len(pts_b)}")
    print(f"residual on inliers: median {np.median(err[inl]):.1f} m, "
          f"p90 {np.percentile(err[inl],90):.1f} m, max {err[inl].max():.1f} m")

    rot = math.degrees(math.atan2(M[1, 0], M[0, 0]))
    sc = math.hypot(M[0, 0], M[1, 0])       # base px -> reference px
    # metres per SOURCE pixel is MPP * sc, not MPP / sc. Inverted, this read
    # 126.7 cm and disagreed with the corners it was printed next to.
    cmpx = MPP * sc * 100
    print(f"rotation {rot:+.3f} deg, {cmpx:.1f} cm per source px")

    corners = np.array([[[0, 0]], [[BW, 0]], [[BW, BH]], [[0, BH]]], np.float32)
    rc = cv2.transform(corners, M).reshape(-1, 2)
    # float() because tile2deg inherits float32 from the transform and json refuses it
    lls = [tuple(map(float, tile2deg(tx0 + px / TS, ty0 + py / TS, Z))) for px, py in rc]
    for nm, (la, lo) in zip(["NW", "NE", "SE", "SW"], lls):
        print(f"  {nm}  {la:.6f}, {lo:.6f}")

    lats = [p[0] for p in lls]; lons = [p[1] for p in lls]
    span = (max(lons)-min(lons)) * 111320 * math.cos(math.radians(np.mean(lats)))
    print(f"\ncoverage {span/1000:.2f} km east-west")
    print(f"IMG_BOUNDS = [[{min(lats):.6f}, {min(lons):.6f}], "
          f"[{max(lats):.6f}, {max(lons):.6f}]];")

    json.dump({"corners": dict(zip(["NW", "NE", "SE", "SW"], lls)),
               "rotation_deg": rot, "cm_per_px": cmpx,
               "control_points": int(len(pts_b)), "inliers": int(inl.sum()),
               "residual_median_m": float(np.median(err[inl])),
               "residual_p90_m": float(np.percentile(err[inl], 90)),
               "bounds": [[min(lats), min(lons)], [max(lats), max(lons)]],
               "span_km": span/1000, "zoom": Z, "ref_origin_tile": [tx0, ty0],
               "affine_base_to_refpx": M.tolist()},
              open(os.path.join(HERE, "georef.json"), "w"), indent=2)
    np.save(os.path.join(HERE, "cp_base.npy"), pts_b[inl])
    np.save(os.path.join(HERE, "cp_ref.npy"), pts_r[inl])
    print("wrote georef.json")


if __name__ == "__main__":
    main()
