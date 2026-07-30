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
# Lossless source. The previous working base came from a JPEG that had already
# been through the generative upscale and then a quality-80 encode, so it was
# compressed twice before anyone looked at it. Same 15000x4219 framing, verified
# by phase correlation at 0.1 px with a mean difference of 0.9/255, so the solved
# georeference applies to it unchanged and nothing needs re-solving.
SRC = r"C:\Users\danie\Downloads\caribbean-guard-cuts\FULL RESOLUTION MAPPING.png"
Z, TS = 17, 256

# WebP carries the alpha we need for the rotated corners at a fraction of PNG's
# weight (the same content as PNG at 5000 px is 13 MB, which is indefensible on a
# phone with one bar of signal, and that phone is the whole point of this map).
#
# 9000 px, not 5000 and not 15000. Measured on the lossless source:
#     5000  3.33 m/px  1.07 MB
#     7000  2.38 m/px  1.63 MB
#     9000  1.85 m/px  2.29 MB
#    11000  1.51 m/px  3.17 MB
# The source went through a generative upscale, so detail finer than roughly
# 2 m/px is largely invented. Paying another 2 MB for fabricated sharpness is the
# same bad trade the tile pyramid was rejected for. 9000 sits just past that line
# and is about 3x upsampled at the map's maximum zoom, which is honest.
#
# The overview is what actually loads on arrival; the full base is deferred until
# somebody zooms, so its weight is paid only by people who ask for it.
# The overview is 1200 px, not 1400. It is what loads on arrival, so its weight is
# the number that matters: 63 KB against 86 KB. At the default contain fit the
# overlay is about 1100 device px on a phone and 1400 on a desktop window, so 1200
# is at parity on the device this map is for and only briefly soft on the other,
# until the full base swaps in behind it.
OUTS = [("base.webp", 9000, 82), ("base-lo.webp", 1200, 78)]


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
