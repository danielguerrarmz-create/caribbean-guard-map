"""Georeference Caribbean Guard's own annotated hazard map.

This sheet is already published on caribbeanguard.org and carries the real work:
rip current arrows, rescue stations, and a shaded hazard bay, authored by the
organization rather than guessed by me. If it can be tied to real coordinates,
those annotations become map data instead of a picture.

Feature matching is worth trying HERE even though it failed badly on the main
base image, and the reason is specific: the base was put through a generative
upscaler that invented texture, so its descriptors matched nothing real. This
sheet looks like untouched satellite imagery, so its descriptors should still
correspond to the ground.

The overlays are masked out first. Saturated pure-hue graphics (red arrows, blue
roads, yellow stars, the white legend panel) are drawn ON TOP of the terrain and
would otherwise contribute keypoints that exist in no other image.
"""
import glob, json, math, os
import numpy as np, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ANNOT = os.path.join(ROOT, "reference", "cg-existing-maps", "annotated-base-map-v5.png")
Z, TS = 17, 256


def tile2deg(x, y, z):
    n = 2 ** z
    return (math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))),
            x / n * 360.0 - 180.0)


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


def overlay_mask(rgb):
    """255 where the pixel is terrain, 0 where it is an annotation.

    Terrain here is jungle, sand, surf and water: greens, tans, teals and near
    whites. The annotations are deliberately loud, which is what makes them
    separable. Saturation alone is not enough because tropical water is very
    saturated teal, so hue is checked too.
    """
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h, s, v = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)
    ann = np.zeros(h.shape, bool)
    # red arrows and the shaded hazard bay (OpenCV hue is 0..179, red wraps)
    ann |= ((h < 12) | (h > 168)) & (s > 90) & (v > 90)
    # the blue and light blue road lines
    ann |= (h > 100) & (h < 135) & (s > 110) & (v > 110)
    # yellow stars, orange rescue hexagons, and the yellow place labels
    ann |= (h >= 12) & (h <= 40) & (s > 130) & (v > 150)
    # the white legend panel: bright and colourless
    ann |= (s < 25) & (v > 225)
    ann = cv2.dilate(ann.astype(np.uint8), np.ones((9, 9), np.uint8), 1)
    return (1 - ann) * 255


def main():
    ref, tx0, ty0 = load_ref()
    nlat, _ = tile2deg(tx0, ty0, Z)
    MPP = 156543.03392 * math.cos(math.radians(nlat)) / (2 ** Z)

    a = np.asarray(Image.open(ANNOT).convert("RGB"))
    AH, AW = a.shape[:2]
    mask = overlay_mask(a)
    kept = mask.mean() / 255
    print(f"annotated sheet {AW}x{AH}, {kept*100:.1f}% of pixels are terrain")
    print(f"reference {ref.shape[1]}x{ref.shape[0]}, {MPP:.3f} m/px")

    def prep(img):
        g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return cv2.createCLAHE(3.0, (8, 8)).apply(g)

    ga, gr = prep(a), prep(ref)
    sift = cv2.SIFT_create(nfeatures=40000, contrastThreshold=0.02)
    ka, da = sift.detectAndCompute(ga, mask.astype(np.uint8))
    kr, dr = sift.detectAndCompute(gr, None)
    print(f"keypoints: sheet {len(ka)}, reference {len(kr)}")

    idx = cv2.FlannBasedMatcher({"algorithm": 1, "trees": 5}, {"checks": 64})
    good = [m for m, n in idx.knnMatch(da, dr, k=2) if m.distance < 0.72 * n.distance]
    print(f"ratio-test survivors: {len(good)}")
    if len(good) < 12:
        raise SystemExit("not enough matches; the sheet may not be real imagery either")

    src = np.float32([ka[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst = np.float32([kr[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    M, inl = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC,
                                         ransacReprojThreshold=4.0,
                                         maxIters=200000, confidence=0.9999)
    if M is None or inl is None:
        raise SystemExit("alignment not credible")
    inl = inl.ravel().astype(bool)
    n_in = int(inl.sum())
    print(f"RANSAC inliers: {n_in}/{len(good)}")
    if n_in < 12:
        raise SystemExit("alignment not credible")

    proj = cv2.transform(src, M).reshape(-1, 2)
    err = np.linalg.norm(proj - dst.reshape(-1, 2), axis=1) * MPP
    print(f"residual on inliers: median {np.median(err[inl]):.1f} m, "
          f"p90 {np.percentile(err[inl],90):.1f} m")

    rot = math.degrees(math.atan2(M[1, 0], M[0, 0]))
    sc = math.hypot(M[0, 0], M[1, 0])
    print(f"rotation {rot:+.3f} deg, {MPP*sc*100:.1f} cm per sheet px")

    corners = np.array([[[0, 0]], [[AW, 0]], [[AW, AH]], [[0, AH]]], np.float32)
    rc = cv2.transform(corners, M).reshape(-1, 2)
    lls = [tuple(map(float, tile2deg(tx0 + px/TS, ty0 + py/TS, Z))) for px, py in rc]
    for nm, (la, lo) in zip(["NW", "NE", "SE", "SW"], lls):
        print(f"  {nm}  {la:.6f}, {lo:.6f}")
    lats = [p[0] for p in lls]; lons = [p[1] for p in lls]
    span = (max(lons)-min(lons)) * 111320 * math.cos(math.radians(np.mean(lats)))
    print(f"\ncovers {span/1000:.2f} km east-west")

    json.dump({"corners": dict(zip(["NW", "NE", "SE", "SW"], lls)),
               "rotation_deg": rot, "cm_per_px": MPP*sc*100,
               "matches": len(good), "inliers": n_in,
               "residual_median_m": float(np.median(err[inl])),
               "sheet_size": [AW, AH], "span_km": span/1000,
               "zoom": Z, "ref_origin_tile": [tx0, ty0],
               "affine_sheet_to_refpx": M.tolist()},
              open(os.path.join(HERE, "georef_annot.json"), "w"), indent=2)
    print("wrote georef_annot.json")


if __name__ == "__main__":
    main()
