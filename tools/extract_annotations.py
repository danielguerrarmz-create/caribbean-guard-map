"""Lift Caribbean Guard's hazard annotations off their sheet as real coordinates.

georef_annot.py tied the sheet to the ground at 1.2 m. This reads the graphics
back off it: rip current arrows, rescue stations, and the shaded hazard bay,
and writes them as GeoJSON in WGS84.

This is deliberately a colour-and-shape extraction rather than anything clever.
The legend defines the visual language exactly (red dashed arrow = rip current,
orange = rescue station, yellow star = location), the sheet was drawn to that
legend, and so the graphics are separable by hue. Anything ambiguous is left out
and reported rather than guessed at, because a rip current in the wrong place is
worse than a rip current missing.

Output is a proposal for Caribbean Guard to confirm, not a published fact. Every
feature carries source and needs_confirmation so that never gets lost downstream.
"""
import json, math, os
import numpy as np, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ANNOT = os.path.join(ROOT, "reference", "cg-existing-maps", "annotated-base-map-v5.png")
SRC_URL = ("https://www.caribbeanguard.org/programa-playa-organizada "
           "(Annotated Base Map V5.png)")
Z, TS = 17, 256

# The legend panel uses the same colours as the map. Exclude it or every legend
# swatch is read as a feature.
LEGEND = (1960, 0, 2500, 240)      # x0, y0, x1, y1


def tile2deg(x, y, z):
    n = 2 ** z
    return (math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))),
            x / n * 360.0 - 180.0)


def main():
    gj = json.load(open(os.path.join(HERE, "georef_annot.json")))
    M = np.array(gj["affine_sheet_to_refpx"], np.float32)
    tx0, ty0 = gj["ref_origin_tile"]
    mpp = gj["cm_per_px"] / 100.0

    def to_ll(pts):
        """sheet pixels -> [lon, lat] pairs, GeoJSON axis order"""
        p = np.array(pts, np.float32).reshape(-1, 1, 2)
        r = cv2.transform(p, M).reshape(-1, 2)
        out = []
        for px, py in r:
            la, lo = tile2deg(tx0 + px/TS, ty0 + py/TS, Z)
            out.append([round(float(lo), 6), round(float(la), 6)])
        return out

    a = np.asarray(Image.open(ANNOT).convert("RGB"))
    H, W = a.shape[:2]
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    h, s, v = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)

    keep = np.ones((H, W), bool)
    keep[LEGEND[1]:LEGEND[3], LEGEND[0]:LEGEND[2]] = False

    # Thresholds below are measured off the sheet's own histogram, not guessed.
    # Saturation alone does not separate anything here: tropical jungle and reef
    # water are both highly saturated, and together they are 10% of the image.
    # Hue is what actually separates the drawn layer from the photograph.
    #   blue road    h 110-115  RGB  25  93 244
    #   orange stn   h  15- 20  RGB 212 140  44
    #   yellow star  h  25- 30  RGB 205 187  65
    #   jungle       h  40- 70
    #   reef water   h  75- 95

    # --- rip current arrows: vivid red, drawn dashed so the dashes need joining
    arrows = ((h < 6) | (h > 174)) & (s > 170) & (v > 150) & keep
    arrows = cv2.morphologyEx(arrows.astype(np.uint8), cv2.MORPH_CLOSE,
                              np.ones((25, 25), np.uint8))

    # --- shaded hazard bay: same hue family but washed out, it is a translucent fill
    bay = ((h < 12) | (h > 168)) & (s > 60) & (s < 150) & (v > 130) & keep
    bay = cv2.morphologyEx(bay.astype(np.uint8), cv2.MORPH_CLOSE,
                           np.ones((15, 15), np.uint8))

    # --- rescue stations: orange hexagons. The window stops at hue 22 because the
    # yellow location stars start at 24, and there are 42 of those.
    stations = (h >= 13) & (h <= 22) & (s > 150) & (v > 170) & keep
    stations = cv2.morphologyEx(stations.astype(np.uint8), cv2.MORPH_CLOSE,
                                np.ones((5, 5), np.uint8))

    features, skipped = [], []

    def components(mask, min_px):
        n, lab, stats, cent = cv2.connectedComponentsWithStats(mask, 8)
        out = []
        for i in range(1, n):
            if stats[i, cv2.CC_STAT_AREA] >= min_px:
                out.append((lab == i, stats[i], cent[i]))
        return out

    # ---- rip currents -------------------------------------------------------
    for blob, st, cen in components(arrows, 150):
        ys, xs = np.nonzero(blob)
        pts = np.column_stack([xs, ys]).astype(np.float32)
        mean = pts.mean(0)
        # principal axis gives the line the arrow runs along
        _, eig = np.linalg.eigh(np.cov((pts - mean).T))
        axis = eig[:, -1]
        t = (pts - mean) @ axis
        p0, p1 = mean + axis * t.min(), mean + axis * t.max()
        length_m = float(np.linalg.norm(p1 - p0) * mpp)
        if length_m < 25 or length_m > 400:
            skipped.append(f"red blob at {cen[0]:.0f},{cen[1]:.0f} length {length_m:.0f} m")
            continue
        # A rip pulls seaward, and on this coast the sea is north, so orient the
        # arrow towards lower y. This is a real assumption; it is recorded as one.
        if p0[1] < p1[1]:
            p0, p1 = p1, p0
        features.append({
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": to_ll([p0, p1])},
            "properties": {"kind": "rip_current", "length_m": round(length_m),
                           "direction": "seaward, inferred from sheet orientation",
                           "source": SRC_URL, "needs_confirmation": True}})

    # ---- rescue stations ----------------------------------------------------
    for blob, st, cen in components(stations, 200):
        w_m = st[cv2.CC_STAT_WIDTH] * mpp
        if w_m > 90:
            skipped.append(f"orange blob at {cen[0]:.0f},{cen[1]:.0f} width {w_m:.0f} m")
            continue
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": to_ll([cen])[0]},
            "properties": {"kind": "rescue_station", "source": SRC_URL,
                           "needs_confirmation": True}})

    # ---- shaded hazard area -------------------------------------------------
    for blob, st, cen in components(bay, 6000):
        cnts, _ = cv2.findContours(blob.astype(np.uint8), cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
        c = max(cnts, key=cv2.contourArea)
        c = cv2.approxPolyDP(c, 0.004 * cv2.arcLength(c, True), True).reshape(-1, 2)
        if len(c) < 4:
            continue
        ring = to_ll(c)
        ring.append(ring[0])
        # NOT called a hazard area. The sheet's legend defines six things and this
        # shaded polygon is not one of them, so its meaning is genuinely unknown:
        # red reads as danger, but Caribbean Guard's own programme text describes a
        # "zona segura de bañado", a designated safe swimming zone, and that would
        # sit in exactly this kind of sheltered bay. Guessing wrong here inverts a
        # safety message. It stays unlabelled until Caribbean Guard says which it is.
        features.append({
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": [ring]},
            "properties": {"kind": "shaded_area_meaning_unknown",
                           "area_m2": round(cv2.contourArea(c) * mpp * mpp),
                           "note": ("Red shaded polygon with no legend entry. Could be "
                                    "a hazard zone or a designated safe swimming zone. "
                                    "MUST NOT be rendered with a status until confirmed."),
                           "source": SRC_URL, "needs_confirmation": True}})

    counts = {}
    for f in features:
        counts[f["properties"]["kind"]] = counts.get(f["properties"]["kind"], 0) + 1
    print("extracted:", counts or "nothing")
    for sk in skipped:
        print("  skipped:", sk)

    out = {"type": "FeatureCollection",
           "properties": {
               "source": SRC_URL,
               "extracted_by": "tools/extract_annotations.py",
               "georeference_residual_m": gj["residual_median_m"],
               "warning": ("Machine-read off a published graphic. Every feature "
                           "must be confirmed and dated by Caribbean Guard before "
                           "it is shown to the public as safety guidance.")},
           "features": features}
    p = os.path.join(ROOT, "web", "data", "cg-hazards.geojson")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(out, open(p, "w"), indent=1)
    print("wrote", p)

    # ---- proof render: draw what was extracted back onto the sheet ----------
    chk = a.copy()
    for f in features:
        k = f["properties"]["kind"]
        g = f["geometry"]
        inv = cv2.invertAffineTransform(M)

        def back(lonlat):
            lo, la = lonlat
            n = 2 ** Z
            tx = (lo + 180.0) / 360.0 * n
            ty = (1.0 - math.asinh(math.tan(math.radians(la))) / math.pi) / 2.0 * n
            p = np.array([[[(tx - tx0) * TS, (ty - ty0) * TS]]], np.float32)
            return cv2.transform(p, inv).reshape(2)

        if k == "rip_current":
            p0, p1 = [back(c) for c in g["coordinates"]]
            cv2.arrowedLine(chk, tuple(p0.astype(int)), tuple(p1.astype(int)),
                            (0, 255, 255), 5, tipLength=0.3)
        elif k == "rescue_station":
            c = back(g["coordinates"]).astype(int)
            cv2.circle(chk, tuple(c), 26, (0, 255, 255), 5)
        else:
            ring = np.array([back(c) for c in g["coordinates"][0]], np.int32)
            cv2.polylines(chk, [ring], True, (0, 255, 255), 5)
    q = os.path.join(HERE, "annot_check.jpg")
    Image.fromarray(chk).save(q, quality=88)
    print("wrote", q, "- cyan overlay must sit on the original graphics")


if __name__ == "__main__":
    main()
