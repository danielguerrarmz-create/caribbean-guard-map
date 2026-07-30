"""Prove the georeference visually.

A transform with a good correlation score can still be wrong. This renders the
same three landmarks from the Bing reference (known coordinates) and from the
georeferenced base image, side by side. If the coastline lines up in all three,
the georeference holds. If it drifts at the ends, the hand stitch introduced
scale error and we need a piecewise fit rather than one global transform.
"""
import json, math, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:\Users\danie\Downloads\caribbean-guard-cuts\Complete Mapping.jpg"
Z, TS = 17, 256

# Unambiguous, well separated along the coast: west end, middle, east end.
WEST = [
    ("Puerto Viejo point", 9.6553, -82.7540),
    ("Playa Cocles",       9.6480, -82.7330),
    ("Punta Uva hook",     9.6400, -82.6930),
]
# The east end is where the residual sweep loses confidence. Render it too, so
# the cause is seen rather than guessed: bad transform, or bad source imagery.
EAST = [
    ("Punta Uva east",   9.6370, -82.6834),
    ("Manzanillo apr",   9.6350, -82.6677),
    ("Manzanillo town",  9.6335, -82.6598),
]
CHECKS = EAST if os.environ.get("EAST") else WEST
OUT = "georef_check_east.jpg" if os.environ.get("EAST") else "georef_check.jpg"
HALF_M = 700  # metres each side of the check point


def deg2tile(lat, lon, z):
    n = 2 ** z
    return ((lon + 180.0) / 360.0 * n,
            (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n)


def load_ref():
    import glob
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
    return mos, x0, y0


def main():
    gj = json.load(open(os.path.join(HERE, "georef.json")))
    c = gj["corners"]
    NW, NE, SE, SW = (np.array(c[k], float) for k in ["NW", "NE", "SE", "SW"])

    base = Image.open(BASE); BW, BH = base.size
    ref, tx0, ty0 = load_ref()

    # bilinear map from base pixel -> lat/lon using the four solved corners
    def base_px_to_ll(px, py):
        u, v = px / BW, py / BH
        top = NW + (NE - NW) * u
        bot = SW + (SE - SW) * u
        return top + (bot - top) * v

    # invert numerically: lat/lon -> base px (the map is near affine, so 2 steps converge)
    def ll_to_base_px(lat, lon):
        target = np.array([lat, lon])
        p = np.array([BW / 2.0, BH / 2.0])
        for _ in range(40):
            f = base_px_to_ll(*p) - target
            e = 1.0
            J = np.column_stack([
                (base_px_to_ll(p[0] + e, p[1]) - base_px_to_ll(p[0] - e, p[1])) / (2 * e),
                (base_px_to_ll(p[0], p[1] + e) - base_px_to_ll(p[0], p[1] - e)) / (2 * e)])
            try:
                p = p - np.linalg.solve(J, f)
            except np.linalg.LinAlgError:
                break
        return p

    mlat = 111320.0
    panels = []
    for name, la, lo in CHECKS:
        dlat = HALF_M / mlat
        dlon = HALF_M / (mlat * math.cos(math.radians(la)))

        # --- reference crop, exact by construction ---
        x0, y0 = deg2tile(la + dlat, lo - dlon, Z)
        x1, y1 = deg2tile(la - dlat, lo + dlon, Z)
        rc = ref.crop((int((x0-tx0)*TS), int((y0-ty0)*TS),
                       int((x1-tx0)*TS), int((y1-ty0)*TS))).resize((420, 420), Image.LANCZOS)

        # --- base crop, via the solved georeference ---
        pts = np.array([ll_to_base_px(la + dlat, lo - dlon),
                        ll_to_base_px(la + dlat, lo + dlon),
                        ll_to_base_px(la - dlat, lo + dlon),
                        ll_to_base_px(la - dlat, lo - dlon)], np.float32)
        dstq = np.array([[0, 0], [420, 0], [420, 420], [0, 420]], np.float32)
        M = cv2.getPerspectiveTransform(pts, dstq)
        bc = cv2.warpPerspective(np.asarray(base.convert("RGB")), M, (420, 420))
        bc = Image.fromarray(bc)

        panels.append((name, rc, bc))

    sheet = Image.new("RGB", (420 * len(panels), 420 * 2 + 56), "white")
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arialbd.ttf", 16)
        small = ImageFont.truetype("arial.ttf", 13)
    except Exception:
        font = small = ImageFont.load_default()
    for i, (name, rc, bc) in enumerate(panels):
        d.text((i*420 + 10, 8), name, fill="black", font=font)
        sheet.paste(rc, (i*420, 28))
        sheet.paste(bc, (i*420, 28 + 420 + 28))
        d.text((i*420 + 10, 28 + 420 + 6), "Bing (true coordinates)", fill="#1f6fb5", font=small)
        d.text((i*420 + 10, 28 + 840 + 30), "your stitched image, georeferenced",
               fill="#b53d1f", font=small)
    out = os.path.join(HERE, OUT)
    sheet.save(out, quality=92)
    print("wrote", out)
    print(f"rotation {gj['rotation_deg']:+.3f} deg  span {gj['span_km']:.2f} km  "
          f"{gj['inliers']}/{gj['control_points']} inliers  "
          f"median residual {gj['residual_median_m']:.1f} m")


if __name__ == "__main__":
    main()
