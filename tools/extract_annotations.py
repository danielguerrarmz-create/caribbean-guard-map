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
feature carries its source, what authored it, and an empty `reviewed`, so none of
that gets lost downstream.
"""
import hashlib, json, math, os
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
# Fragments of one dashed arrow sit well inside this; separate arrows on the
# sheet are never this close. Measured off the sheet, not guessed.
# Dashes within one arrow are closed at 25 px, so fragments of the same arrow
# sit inside ~50 px. Distinct arrows on this sheet are never closer than about
# 100 px. 150 was over-merging: it joined separate arrows into one path that
# crossed the bay.
CLUSTER_PX = 55


def feature_id(kind, coords):
    """A stable id, derived from the geometry rather than from loop order.

    Every feature needs an id or there is nothing for a guard's confirmation to
    attach to that survives the sheet being re-extracted. An index would not do:
    connected-component order shifts when anything upstream changes, so review #3
    would silently become a different rip current.

    Hashing the rounded position instead means the id changes when, and only
    when, the feature moves. That is the correct trigger: a rip current that has
    moved is a different claim and its old confirmation should not follow it.

    Six decimal places is about 0.1 m, well under the 1.2 m georeference residual,
    so re-extracting an unchanged sheet reproduces the same ids exactly.

    Namespaced `cg:` because ids are also the join key for provenance records,
    and Caribbean Guard is not the only lifeguard organisation this project could
    ever hold. See the id convention comment in web/index.html.
    """
    flat = ";".join(f"{lon:.6f},{lat:.6f}" for lon, lat in coords)
    return "cg:%s/%s" % (kind, hashlib.sha1(flat.encode()).hexdigest()[:8])


def tile2deg(x, y, z):
    n = 2 ** z
    return (math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))),
            x / n * 360.0 - 180.0)


def load_shore():
    """Shoreline as sheet-pixel points, from the polylines traced off Bing."""
    # the DENSE waterline (one point per ~12 m), not zone_lines.json, which is
    # nine points per beach and far too coarse to measure distance against
    q = os.path.join(HERE, "shoreline.json")
    if not os.path.exists(q):
        return None
    gj = json.load(open(os.path.join(HERE, "georef_annot.json")))
    M = np.array(gj["affine_sheet_to_refpx"], np.float32)
    inv = cv2.invertAffineTransform(M)
    tx0, ty0 = gj["ref_origin_tile"]
    pts = []
    for la, lo in json.load(open(q)):
        if True:
            n = 2 ** Z
            tx = (lo + 180.0) / 360.0 * n
            ty = (1.0 - math.asinh(math.tan(math.radians(la))) / math.pi) / 2.0 * n
            r = np.array([[[(tx - tx0) * TS, (ty - ty0) * TS]]], np.float32)
            pts.append(cv2.transform(r, inv).reshape(2))
    return np.array(pts, float) if pts else None


SHORE = None


def seaward_normal(cx, cy):
    """Unit vector pointing from the shore towards open water, in sheet pixels.

    Land is south of the waterline along this whole coast, so the normal is the
    local coast tangent rotated towards decreasing y. Returns None when there is
    no shoreline nearby, in which case the caller leaves the arrow as drawn.
    """
    global SHORE
    if SHORE is None:
        SHORE = load_shore()
    if SHORE is None or len(SHORE) < 2:
        return None
    d = np.hypot(SHORE[:, 0] - cx, SHORE[:, 1] - cy)
    i = int(np.argmin(d))
    j = i + 1 if i + 1 < len(SHORE) else i - 1
    t = SHORE[j] - SHORE[i]
    if not np.any(t):
        return None
    t = t / np.linalg.norm(t)
    n = np.array([t[1], -t[0]])          # rotate the tangent 90 degrees
    if n[1] > 0:                          # keep the one heading to lower y, the sea
        n = -n
    return n


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
    # The arrows on the sheet are dashed AND curved, and a curve defeats the
    # obvious approach twice over. Closing the dashes leaves several components
    # per arrow, and fitting a principal axis to a curved blob returns the chord
    # of the curve, which for the hooked arrows is close to perpendicular to where
    # the current actually goes. Read together those two faults turned one arrow
    # at Chiquita into three "rip currents", one of them pointing along the beach.
    #
    # So: cluster the fragments that belong to one arrow, then order each cluster
    # by DISTANCE FROM THE SHORELINE rather than along an axis. Tail is the end
    # nearest the beach, head is the end furthest out. That follows a curve, gets
    # the direction right by construction rather than by a rule about north, and
    # counts arrows instead of fragments.
    blobs = components(arrows, 120)
    clusters = []
    for blob, st, cen in blobs:
        for c in clusters:
            if min(math.hypot(cen[0] - o[0], cen[1] - o[1]) for o in c["cents"]) < CLUSTER_PX:
                c["mask"] |= blob
                c["cents"].append(cen)
                break
        else:
            clusters.append({"mask": blob.copy(), "cents": [cen]})
    print(f"{len(blobs)} red fragments -> {len(clusters)} arrows")

    shore = load_shore()
    for c in clusters:
        ys, xs = np.nonzero(c["mask"])
        pts = np.column_stack([xs, ys]).astype(np.float64)
        if shore is None or len(shore) < 2:
            skipped.append("no shoreline available to orient an arrow")
            continue
        # DIRECTION IS NOT READ FROM THE PIXELS. Position is; bearing is not.
        #
        # Recovering a bearing from a dashed, curved, hand-drawn arrow needs the
        # arrowhead identified, and at this resolution the head is a few pixels
        # wider than the shaft. Every proxy tried instead was wrong somewhere on
        # the sheet: a principal axis returns the chord of a hooked arrow, and
        # ordering by distance from the waterline inverts wherever the coast bends
        # back on itself. Two arrows came out pointing along the beach and one
        # pointing inland. On a map whose job is telling somebody which way a
        # current drags them, a confidently wrong bearing is worse than no bearing.
        #
        # So the arrow is drawn along the local SEAWARD NORMAL of the coastline,
        # anchored at the position Caribbean Guard marked. That is true of rip
        # currents in general, it cannot come out pointing inland or along the
        # beach, and it claims only what is actually known: this is where they
        # marked a rip, and a rip pulls away from the beach. The sheet's exact
        # bearing stays a question for Caribbean Guard.
        d = np.min(np.hypot(pts[:, None, 0] - shore[None, :, 0],
                            pts[:, None, 1] - shore[None, :, 1]), axis=1)
        order = np.argsort(d)
        tail = pts[order[:max(3, len(order) // 20)]].mean(0)
        far = pts[order[-max(3, len(order) // 20):]].mean(0)
        length_m = float(np.linalg.norm(far - tail) * mpp)
        if length_m < 25 or length_m > 400:
            skipped.append(f"arrow at {tail[0]:.0f},{tail[1]:.0f} length {length_m:.0f} m")
            continue
        n = seaward_normal(*tail)
        if n is None:
            skipped.append("no shoreline near an arrow; direction unknown")
            continue
        head = tail + n * (length_m / mpp)
        path = [tail, head]
        coords = to_ll(path)
        features.append({
            "type": "Feature",
            "id": feature_id("rip", coords),
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": {"kind": "rip_current", "length_m": round(length_m),
                           "direction": "perpendicular to the beach, seaward. Position is Caribbean Guard's; the exact bearing on their sheet was not machine-readable and is not claimed here.",
                           "source": SRC_URL,
                           "authored": "sheet", "reviewed": None}})

    # ---- rescue stations ----------------------------------------------------
    # These four points had a twin in POSTS in web/index.html, matching to five
    # decimal places, and nothing read the copy here: drawAnnotations() handled rip
    # currents and the shaded polygon, and the string `rescue_station` did not
    # appear in that file at all. So the same four objects had two sources of truth
    # and the dead one lived in the file called "the data file". Anybody who moved
    # a station here, which is the obvious place to move it, changed nothing.
    #
    # Resolved by joining rather than by deleting either copy. THIS IS THE
    # AUTHORITATIVE GEOMETRY. POSTS keeps the name, the hours and the equipment
    # copy, which a machine reading a graphic cannot produce, plus a fallback
    # coordinate used only when this file fails to load, because stations still
    # have to draw with no signal. The map joins on `id` and warns in the console
    # if the fallback and the real position have drifted apart.
    #
    # Station ids are POSITIONAL, west to east, not hashed like the rips. The
    # numbering is already published on the markers and inside QR codes (?p=est2),
    # so it has to survive a re-extraction even when a station moves. A fifth
    # station appearing on a re-issued sheet is a renumbering decision for a human,
    # and the count printed below is where it surfaces: Caribbean Guard's own press
    # says nine along the whole coast and this sheet yields four.
    stations_out = []
    for blob, st, cen in components(stations, 200):
        w_m = st[cv2.CC_STAT_WIDTH] * mpp
        if w_m > 90:
            skipped.append(f"orange blob at {cen[0]:.0f},{cen[1]:.0f} width {w_m:.0f} m")
            continue
        stations_out.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": to_ll([cen])[0]},
            "properties": {"kind": "rescue_station", "source": SRC_URL,
                           "authored": "sheet", "reviewed": None}})
    stations_out.sort(key=lambda f: f["geometry"]["coordinates"][0])
    for i, f in enumerate(stations_out, 1):
        f["id"] = f"cg:station/est{i}"
    features += stations_out

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
            "id": feature_id("area", ring),
            "geometry": {"type": "Polygon", "coordinates": [ring]},
            "properties": {"kind": "shaded_area_meaning_unknown",
                           "area_m2": round(cv2.contourArea(c) * mpp * mpp),
                           "note": ("Red shaded polygon with no legend entry. Could be "
                                    "a hazard zone or a designated safe swimming zone. "
                                    "MUST NOT be rendered with a status until confirmed."),
                           "source": SRC_URL,
                           "authored": "sheet", "reviewed": None}})

    counts = {}
    for f in features:
        counts[f["properties"]["kind"]] = counts.get(f["properties"]["kind"], 0) + 1
    print("extracted:", counts or "nothing")
    for sk in skipped:
        print("  skipped:", sk)
    if counts.get("rescue_station", 0) != 4:
        print("  NOTE: station count changed. web/index.html POSTS numbers its "
              "markers est1..est4 west to east and QR codes carry those ids. "
              "Renumbering is a human decision, not an automatic one.")

    out = {"type": "FeatureCollection",
           "properties": {
               "source": SRC_URL,
               "extracted_by": "tools/extract_annotations.py",
               "georeference_residual_m": gj["residual_median_m"],
               "station_layer": ("Rescue stations are the ONE feature class with a "
                                 "second record elsewhere: POSTS in web/index.html "
                                 "carries their names, hours and equipment copy, "
                                 "which a machine reading a graphic cannot produce. "
                                 "The GEOMETRY HERE IS AUTHORITATIVE and the map "
                                 "joins on `id`; the coordinates in POSTS are a "
                                 "fallback used only when this fetch fails, and the "
                                 "map logs a warning if the two disagree. Move a "
                                 "station here, not there."),
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
            # two or three points now: a hooked arrow keeps its bend
            pp = [back(c) for c in g["coordinates"]]
            for a2, b2 in zip(pp, pp[1:-1]):
                cv2.line(chk, tuple(a2.astype(int)), tuple(b2.astype(int)),
                         (0, 255, 255), 5)
            cv2.arrowedLine(chk, tuple(pp[-2].astype(int)), tuple(pp[-1].astype(int)),
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
