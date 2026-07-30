"""Redraw the zone polylines so they follow the actual coastline.

The zone geometry in index.html was hand-placed against the old, wrong bounds.
With the georeference corrected the lines are visibly off: they run across jungle
and sit out in open water.

Shoreline comes from the **Bing mosaic**, not from the rectified base. That is the
important choice. Bing is untouched satellite imagery already in true coordinates,
so its shoreline is ground truth. The base image is generatively upscaled and
carries 5 to 75 m of registration error in the west and none that can be verified
in the east, so tracing it would bake both problems into the geometry.

This fixes where the lines ARE. It says nothing about whether the swim status
attached to each one is correct: that still needs Caribbean Guard.
"""
import glob, json, math, os, re
import numpy as np, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
Z, TS = 17, 256

# Longitude span of each named beach, from the landmarks established by
# tools/residual.py and the extent of Caribbean Guard's own annotated sheet.
# Ordered west to east, matching the picker.
ZONES = [
    ("playa-negra",  -82.7700, -82.7580),
    ("salsa-brava",  -82.7556, -82.7505),
    ("cocles",       -82.7480, -82.7270),
    ("chiquita",     -82.7265, -82.7060),
    ("punta-uva",    -82.7055, -82.6880),
]
SEAWARD_M = 30      # nudge the line off the sand into the water it describes
MAX_POINTS = 9      # enough to follow a bay, few enough to stay legible


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
    if not files:
        raise SystemExit("no tile cache; run tools/georef2.py first")
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


def water_mask(rgb):
    """Flood fill the sea inward from the top edge.

    A plain colour threshold gets this wrong twice: dark reef inside the sea reads
    as land, and wet sand and shallow lagoons read as sea. Filling from the top,
    where every column is open ocean, keeps the sea connected and leaves inland
    ponds and reef out of it.
    """
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h, s, v = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)
    # sea here is blue-green and never bright: jungle is greener, sand is brighter
    seaish = ((h > 70) & (h < 115) & (v < 190)) | (v < 60)
    seaish = cv2.morphologyEx(seaish.astype(np.uint8), cv2.MORPH_CLOSE,
                              np.ones((9, 9), np.uint8))
    H, W = seaish.shape
    ff = np.zeros((H + 2, W + 2), np.uint8)
    m = seaish.copy()
    for x in range(0, W, 40):
        if m[0, x]:
            cv2.floodFill(m, ff, (x, 0), 2)
    return (m == 2).astype(np.uint8)


def main():
    ref, tx0, ty0 = load_ref()
    RH, RW = ref.shape[:2]
    nlat, wlon = tile2deg(tx0, ty0, Z)
    mpp = 156543.03392 * math.cos(math.radians(nlat)) / (2 ** Z)
    print(f"reference {RW}x{RH}, {mpp:.3f} m/px")

    sea = water_mask(ref)
    print(f"water is {sea.mean()*100:.1f}% of the mosaic")

    # first land pixel from the top, per column: the waterline
    land = 1 - sea
    shore_y = np.full(RW, -1, np.int32)
    for x in range(RW):
        col = np.nonzero(land[:, x])[0]
        if col.size:
            shore_y[x] = col[0]
    valid = shore_y >= 0
    print(f"shoreline found in {valid.mean()*100:.1f}% of columns")

    # smooth along the coast: per-column detection is noisy at surf and river mouths
    k = 81
    sm = shore_y.astype(np.float64).copy()
    sm[~valid] = np.nan
    ser = np.convolve(np.nan_to_num(sm), np.ones(k) / k, mode="same")
    cnt = np.convolve(valid.astype(float), np.ones(k) / k, mode="same")
    smooth = np.where(cnt > 0.25, ser / np.maximum(cnt, 1e-6), np.nan)

    def px_to_ll(x, y):
        return tile2deg(tx0 + x / TS, ty0 + y / TS, Z)

    def lon_to_px(lon):
        tx, _ = deg2tile(9.65, lon, Z)
        return (tx - tx0) * TS

    out = {}
    for zid, w, e in ZONES:
        x_from, x_to = int(lon_to_px(w)), int(lon_to_px(e))
        x_from, x_to = max(0, min(x_from, x_to)), min(RW - 1, max(x_from, x_to))
        xs = np.arange(x_from, x_to)
        ys = smooth[x_from:x_to]
        ok = np.isfinite(ys)
        if ok.sum() < 20:
            print(f"  {zid:14} no shoreline found in range")
            continue
        xs, ys = xs[ok], ys[ok]
        # sample evenly along the span, then push seaward (north) off the sand
        idx = np.linspace(0, len(xs) - 1, MAX_POINTS).astype(int)
        pts = []
        for i in idx:
            la, lo = px_to_ll(float(xs[i]), float(ys[i]) - SEAWARD_M / mpp)
            pts.append([round(la, 5), round(lo, 5)])
        span = (pts[-1][1] - pts[0][1]) * 111320 * math.cos(math.radians(9.645))
        out[zid] = pts
        print(f"  {zid:14} {len(pts)} pts, {span/1000:.2f} km, "
              f"lat {min(p[0] for p in pts):.4f}..{max(p[0] for p in pts):.4f}")

    # ---- write straight into index.html, replacing each line: [...] ----
    p = os.path.join(ROOT, "web", "index.html")
    src = open(p, encoding="utf-8").read()
    n = 0
    for zid, pts in out.items():
        arr = "[" + ",".join(f"[{a},{b}]" for a, b in pts) + "]"
        # The array is NESTED, so [^\]]* stops at the first inner bracket and
        # leaves the tail of the old polyline behind, producing valid-looking but
        # broken JS. Match to the closing ']]' instead.
        pat = re.compile(r'(id:"' + re.escape(zid) + r'".*?\n\s*line:)\[\[.*?\]\]',
                         re.S)
        src, c = pat.subn(lambda m: m.group(1) + arr, src, count=1)
        n += c
        if not c:
            print(f"  WARNING: could not find line: for {zid}")
    open(p, "w", encoding="utf-8").write(src)
    print(f"\nrewrote {n} zone polylines in web/index.html")

    json.dump(out, open(os.path.join(HERE, "zone_lines.json"), "w"), indent=1)

    # Also export the DENSE waterline, every 10 reference pixels. zone_lines.json
    # is nine points per beach, which is fine for drawing and useless for geometry:
    # one point per 370 m cannot tell you how far a pixel is from the water. Other
    # tools need the real thing (tools/extract_annotations.py orients rip arrows by
    # distance from it), so write it once here where it is already computed.
    dense = []
    for x in range(0, RW, 10):
        y = smooth[x]
        if np.isfinite(y):
            la, lo = px_to_ll(float(x), float(y))
            dense.append([round(la, 6), round(lo, 6)])
    json.dump(dense, open(os.path.join(HERE, "shoreline.json"), "w"))
    print(f"dense shoreline: {len(dense)} points, one per "
          f"{10 * mpp:.0f} m -> tools/shoreline.json")


if __name__ == "__main__":
    main()
