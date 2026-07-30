"""Warp the stitched base into north-up Web Mercator so Leaflet can place it.

Leaflet's L.imageOverlay stretches an image across an axis-aligned lat/lon
rectangle. It cannot rotate. Our base sits at +3.37 degrees to north, so handing
Leaflet the solved bounds directly would smear the ends by up to half a
kilometre, which is worse than shipping no georeference at all.

So resample once, here, into the map's own projection. After this the image is
north-up, its bounds are exact, and every downstream step (the web overlay, the
tile pyramid, any QR coordinate) inherits a correct geometry instead of
re-deriving it.

Output has an alpha channel because rotating a rectangle leaves empty wedges at
the corners. Those render as the page background rather than as black triangles.
"""
import json, math, os
import numpy as np, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = r"C:\Users\danie\Downloads\caribbean-guard-cuts\Complete Mapping.jpg"
Z, TS = 17, 256

# PNG at 5000 px is 13 MB, which is indefensible on a phone with one bar of
# signal, and that phone is the whole point of this map. WebP carries the alpha
# channel we need for the rotated corners at a fraction of the weight.
OUTS = [("base.webp", 5000, 82), ("base-lo.webp", 1400, 78)]


def tile2deg(x, y, z):
    n = 2 ** z
    return (math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))),
            x / n * 360.0 - 180.0)


def main():
    gj = json.load(open(os.path.join(HERE, "georef.json")))
    M = np.array(gj["affine_base_to_refpx"], np.float64)   # base px -> ref px
    tx0, ty0 = gj["ref_origin_tile"]

    src = np.asarray(Image.open(SRC).convert("RGB"))
    BH, BW = src.shape[:2]

    # where the four source corners land in reference pixel space
    corners = np.array([[[0, 0]], [[BW, 0]], [[BW, BH]], [[0, BH]]], np.float32)
    rc = cv2.transform(corners, M.astype(np.float32)).reshape(-1, 2)
    minx, miny = rc.min(axis=0)
    maxx, maxy = rc.max(axis=0)

    # exact bounds of the output rectangle, in the projection Leaflet uses
    nlat, wlon = tile2deg(tx0 + minx / TS, ty0 + miny / TS, Z)
    slat, elon = tile2deg(tx0 + maxx / TS, ty0 + maxy / TS, Z)

    full_w = maxx - minx
    aspect = (maxy - miny) / full_w

    # shift the solved transform so the bounding box starts at the origin
    T = np.array([[1, 0, -minx], [0, 1, -miny]], np.float64)
    base_to_box = np.vstack([M, [0, 0, 1]])
    base_to_box = (np.vstack([T, [0, 0, 1]]) @ base_to_box)[:2]

    rgba = np.dstack([src, np.full(src.shape[:2], 255, np.uint8)])

    for name, width, q in OUTS:
        k = width / full_w
        S = np.array([[k, 0, 0], [0, k, 0]], np.float64)
        A = (np.vstack([S, [0, 0, 1]]) @ np.vstack([base_to_box, [0, 0, 1]]))[:2]
        h = int(round(width * aspect))
        out = cv2.warpAffine(rgba, A, (width, h), flags=cv2.INTER_AREA,
                             borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        p = os.path.join(ROOT, "web", "img", name)
        Image.fromarray(out).save(p, quality=q, method=6)
        mb = os.path.getsize(p) / 1e6
        print(f"{name:14} {width}x{h}  {mb:.2f} MB")

    span = (elon - wlon) * 111320 * math.cos(math.radians((nlat + slat) / 2))
    print(f"\nnorth-up, {span/1000:.2f} km wide, "
          f"{span/OUTS[0][1]*100:.0f} cm per pixel at {OUTS[0][1]} px")
    print("\nIMG_BOUNDS in index.html should be exactly:")
    print(f"const IMG_BOUNDS = [[{slat:.6f}, {wlon:.6f}], [{nlat:.6f}, {elon:.6f}]];")

    gj["rectified_bounds"] = [[float(slat), float(wlon)], [float(nlat), float(elon)]]
    gj["rectified"] = True
    json.dump(gj, open(os.path.join(HERE, "georef.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
