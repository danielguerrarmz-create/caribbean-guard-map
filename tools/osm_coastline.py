"""Build web/data/zones-geometry.json from the OpenStreetMap coastline.

WHY THIS REPLACES tools/export_zones.py AND tools/coastline.json
----------------------------------------------------------------
`trace_coastline.py` found the shore by flood-filling a water mask out of the
z17 satellite mosaic and contouring the sea/land boundary. On a coast with no
reef that works. This coast is a reef coast.

The mask thresholds on brightness (`v < 60` is sea). Shallow water over live
coral at Salsa Brava, over the rock shelf west of Puerto Viejo and over every
sand cay off Punta Uva is BRIGHT, so the mask read all of it as land and the
contour walked around each reef patch instead of along the beach. The result
was a hazard line drawn 20 to 130 m out to sea, looping seaward around rock and
back, and Daniel marked it against the real shore on 2026-09-17.

The arithmetic that proves it, per zone, before this script ran:

    zone           traced length      true coast      excess
    playa-negra         1618 m          1625 m          -0%
    salsa-brava         2303 m          1294 m         +78%
    cocles              4224 m          3202 m         +32%
    chiquita            4439 m          3055 m         +45%
    punta-uva           3119 m          2830 m         +10%

A line 78% longer than the beach it describes is not a smoothing problem, and no
amount of simplification fixes it: the extra kilometre IS the reef, traced.
Playa Negra scores -0% because it is the one zone with no reef near the shore,
which is exactly the control this diagnosis needs. The image cannot tell coral
from sand, so this stops asking it to.

WHAT IT USES INSTEAD
--------------------
OpenStreetMap `natural=coastline`, a human tracing of the mean high water line
that knows the difference between a reef and a beach. Three open ways cover this
coast and chain end to end:

    908286648  (486 pts)  Manzanillo   -> Punta Uva
    908286651  ( 41 pts)  Punta Uva    -> Puerto Viejo
    383710572  (365 pts)  Puerto Viejo -> north-west

The closed ways in the same bounding box (9 to 12 points, first point == last)
are islets and rocks, and they are DROPPED: an islet is not the shoreline a
swimmer stands on, and including one would put a small loop back into the line
for the same reason the mask did.

DIRECTION MATTERS AND IT IS NOT DECORATIVE. OSM's coastline convention is land
on the LEFT of the direction of travel. The chain is ordered west to east here,
which puts land on the right and open sea on the left, so the seaward normal is
the LEFT normal, (-dy, dx). Getting this backwards draws the whole map 25 m
inland, in the trees, and it would still look like a coastline.

THE PIPELINE
------------
1. CHAIN the open ways on shared endpoints, then order west to east.
2. RESAMPLE at 10 m. OSM vertices here run from 1 m to 285 m apart; a normal
   computed at the end of a 285 m segment is not local to the middle of it.
   Resampling first makes the offset local everywhere.
3. OFFSET 25 m seaward along the local normal. The line describes the water you
   would swim in, not the sand. It was 30 m on the traced version; 25 m keeps it
   off the sand at low tide without reaching the outer break.
4. CLIP to each zone at the resolved zone joints, interpolating an exact
   endpoint so two zones meet at a point rather than overlapping.
5. SIMPLIFY at 6 m, CHAIKIN twice, simplify again at 1 m.
   6 m is what "all linework needs to be simplified" turns into: it is 7 px at
   z18 and a third of a pixel at z12, so it removes wiggle nobody can see at any
   zoom this map allows while leaving every headland standing. The output is
   ~275 points against the 2,821 it replaces, and 6 KB against 62 KB in the
   service worker's critical precache, which is bytes somebody waits for on a
   two-bar signal at the water's edge.

ZONE BOUNDARIES. The five `span` values in index.html were derived from the
traced line, and because that line was too long, two pairs OVERLAPPED: Cocles
ran 171 m past the start of Chiquita, and Chiquita 172 m past the start of Punta
Uva. Overlapping spans would draw two tiers on the same water. Each joint is
resolved at the MIDPOINT of the disagreement, which also closes the 26 m and
70 m gaps at the other two joints, so the five zones tile the coast exactly
once. The resolved spans are printed at the end and belong back in index.html.

Usage:
    python tools/osm_coastline.py            # from the cached Overpass response
    python tools/osm_coastline.py --fetch    # re-query Overpass, then build
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "osm-coastline.json")
PAGE = os.path.join(ROOT, "web", "index.html")
OUT = os.path.join(ROOT, "web", "data", "zones-geometry.json")

BBOX = (9.610, -82.82, 9.700, -82.62)      # S, W, N, E
SEAWARD_M = 25
PROVISIONAL_EAST = -82.6500   # short of the point east of Manzanillo village
RESAMPLE_M = 10
SIMPLIFY_M = 6.0
CHAIKIN_PASSES = 2
FINAL_SIMPLIFY_M = 1.0
PRECISION = 6                              # 0.11 m of latitude

# A tangent plane at the coast's mean latitude. Over 16 km the equirectangular
# error is under a centimetre, and it makes "6 metres" mean 6 metres in both
# axes instead of 6 of two different units.
LAT0 = 9.645
M_PER_DEG_LAT = 111132.0
M_PER_DEG_LON = 111320.0 * math.cos(math.radians(LAT0))


def to_m(p):
    return (p[1] * M_PER_DEG_LON, p[0] * M_PER_DEG_LAT)


def to_ll(q):
    return [round(q[1] / M_PER_DEG_LAT, PRECISION),
            round(q[0] / M_PER_DEG_LON, PRECISION)]


# ------------------------------------------------------------------ overpass
def fetch():
    import urllib.request
    import urllib.parse
    s, w, n, e = BBOX
    q = ("[out:json][timeout:90];"
         'way["natural"="coastline"](%s,%s,%s,%s);out geom;' % (s, w, n, e))
    req = urllib.request.Request(
        "https://overpass-api.de/api/interpreter",
        data=urllib.parse.urlencode({"data": q}).encode(),
        headers={"User-Agent": "caribbean-guard-coastline/1.0",
                 "Content-Type": "application/x-www-form-urlencoded"})
    raw = urllib.request.urlopen(req, timeout=180).read()
    json.loads(raw)                        # fail here, not on the next run
    with open(CACHE, "wb") as fh:
        fh.write(raw)
    print("fetched %d bytes -> %s" % (len(raw), os.path.relpath(CACHE, ROOT)))


def chain():
    """The mainland coast, west to east, as one polyline of (lat, lon)."""
    with open(CACHE, encoding="utf-8") as fh:
        doc = json.load(fh)
    ways = {}
    for w in doc["elements"]:
        pts = [(p["lat"], p["lon"]) for p in w.get("geometry", [])]
        if len(pts) < 2 or pts[0] == pts[-1]:
            continue                       # closed ring: an islet, not the shore
        ways[w["id"]] = pts
    if not ways:
        raise SystemExit("no open coastline ways in %s" % CACHE)

    segs = list(ways.values())
    out = segs.pop(0)
    moved = True
    while segs and moved:
        moved = False
        for i, s in enumerate(segs):
            if s[0] == out[-1]:
                out = out + s[1:]
            elif s[-1] == out[-1]:
                out = out + s[::-1][1:]
            elif s[-1] == out[0]:
                out = s[:-1] + out
            elif s[0] == out[0]:
                out = s[::-1][:-1] + out
            else:
                continue
            segs.pop(i)
            moved = True
            break
    if segs:
        raise SystemExit("%d coastline way(s) would not chain; the bbox probably "
                         "clipped one mid-way" % len(segs))
    if out[0][1] > out[-1][1]:
        out = out[::-1]                    # west to east: seaward is the LEFT normal
    return out


# -------------------------------------------------------------- the pipeline
def resample(pts, step):
    out = [pts[0]]
    carry = 0.0
    for a, b in zip(pts, pts[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        if d == 0.0:
            continue
        t = step - carry
        while t <= d:
            out.append((a[0] + (b[0] - a[0]) * t / d, a[1] + (b[1] - a[1]) * t / d))
            t += step
        carry = (carry + d) % step
    if out[-1] != pts[-1]:
        out.append(pts[-1])
    return out


def offset(pts, dist):
    """Seaward along the LOCAL normal. See the header on why it is the left one."""
    out = []
    n = len(pts)
    for i, p in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        out.append((p[0] - dy / length * dist, p[1] + dx / length * dist))
    return out


def seg_dist(p, a, b):
    """Distance from p to the SEGMENT ab, not to the infinite line."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d2 = dx * dx + dy * dy
    if d2 == 0.0:
        return math.hypot(p[0] - a[0], p[1] - a[1])
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / d2
    t = 0.0 if t < 0.0 else (1.0 if t > 1.0 else t)
    return math.hypot(p[0] - (a[0] + t * dx), p[1] - (a[1] + t * dy))


def simplify(pts, tol):
    """Douglas-Peucker, iterative so a long trace cannot blow the stack."""
    if len(pts) < 3:
        return list(pts)
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j - i < 2:
            continue
        worst, wi = -1.0, -1
        for k in range(i + 1, j):
            d = seg_dist(pts[k], pts[i], pts[j])
            if d > worst:
                worst, wi = d, k
        if worst > tol:
            keep[wi] = True
            stack.append((i, wi))
            stack.append((wi, j))
    return [p for p, k in zip(pts, keep) if k]


def chaikin(pts):
    """One corner-cutting pass on an OPEN chain; the endpoints are pinned.

    They have to be: the five zones lie end to end, and a moving endpoint would
    open a gap between two of them at every joint."""
    if len(pts) < 3:
        return list(pts)
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        out.append((a[0] * .75 + b[0] * .25, a[1] * .75 + b[1] * .25))
        out.append((a[0] * .25 + b[0] * .75, a[1] * .25 + b[1] * .75))
    out.append(pts[-1])
    return out


def cut_at(a, b, x):
    """The point on segment ab at easting x."""
    t = (x - a[0]) / (b[0] - a[0])
    return (x, a[1] + (b[1] - a[1]) * t)


def clip(pts, w_m, e_m):
    """The CONTIGUOUS run of the chain between two eastings, ends interpolated.

    NOT "every point whose easting is in range, sorted by easting". That is the
    version this had first and it is wrong on exactly the features that matter.
    Punta Uva is a headland: the shore there runs east, turns north around the
    point and comes back WEST for 400 m before resuming. Easting is not the
    along-shore order on any such feature, and sorting by it interleaves the two
    sides of the point into a zigzag. It measured Punta Uva at 5,412 m against a
    2,755 m beach, which is the same class of error as the reef trace this file
    exists to replace, arrived at from the opposite direction.

    So: walk the chain in its own order, take the first point at or past the west
    cut and the last point at or before the east cut, and keep everything between
    them. An excursion past a cut and back inside the run is KEPT, because that
    is a real headland belonging to this beach, not a bookkeeping artefact."""
    inside = [i for i, p in enumerate(pts) if w_m <= p[0] <= e_m]
    if not inside:
        return []
    i0, i1 = inside[0], inside[-1]
    run = list(pts[i0:i1 + 1])
    if i0 > 0:
        run.insert(0, cut_at(pts[i0 - 1], pts[i0], w_m))
    if i1 + 1 < len(pts):
        run.append(cut_at(pts[i1], pts[i1 + 1], e_m))
    out = [run[0]]
    for q in run[1:]:
        if math.hypot(q[0] - out[-1][0], q[1] - out[-1][1]) > 0.01:
            out.append(q)
    return out


# ------------------------------------------------------------------ zone ids
def read_zones():
    """ids and spans, READ OUT OF index.html rather than constructed.

    `"cg:zone/" + key` would work today and would silently write a file the map
    cannot find the day somebody renames a zone."""
    with open(PAGE, encoding="utf-8") as fh:
        src = fh.read()
    pat = re.compile(r'id:"(cg:zone/([a-z\-]+))".*?'
                     r'span:\{w:(-?[\d.]+), e:(-?[\d.]+)\}', re.S)
    zones = [(m.group(1), m.group(2), float(m.group(3)), float(m.group(4)))
             for m in pat.finditer(src)]
    if len(zones) != 5:
        raise SystemExit("expected 5 zones in index.html, found %d" % len(zones))
    return zones


def resolve_joints(zones):
    """Make the five spans tile the coast exactly once. See the header."""
    cuts = [zones[0][2]]
    for (_, _, _, e), (_, _, w2, _) in zip(zones, zones[1:]):
        cuts.append((e + w2) / 2.0)
    cuts.append(zones[-1][3])
    return cuts


def main():
    if "--fetch" in sys.argv or not os.path.exists(CACHE):
        fetch()

    line = [to_m(p) for p in chain()]
    line = resample(line, RESAMPLE_M)
    line = offset(line, SEAWARD_M)

    zones = read_zones()
    cuts = resolve_joints(zones)

    out, spans, total = {}, [], 0
    for i, (zid, key, _w, _e) in enumerate(zones):
        sub = clip(line, cuts[i] * M_PER_DEG_LON, cuts[i + 1] * M_PER_DEG_LON)
        sub = simplify(sub, SIMPLIFY_M)
        for _ in range(CHAIKIN_PASSES):
            sub = chaikin(sub)
        sub = simplify(sub, FINAL_SIMPLIFY_M)
        if len(sub) < 2:
            raise SystemExit("zone %s clipped to %d points" % (key, len(sub)))
        length = sum(math.hypot(b[0] - a[0], b[1] - a[1])
                     for a, b in zip(sub, sub[1:]))
        out[zid] = [to_ll(p) for p in sub]
        spans.append((key, cuts[i], cuts[i + 1]))
        total += len(sub)
        print("  %-12s %4d pts  %6.0f m   span w:%.5f e:%.5f"
              % (key, len(sub), length, cuts[i], cuts[i + 1]))

    # PROVISIONAL EXTENTS (Daniel, 2026-09-23) for the two named beaches with
    # no Caribbean Guard boundary. Playa Grande runs from where Punta Uva ends
    # to the midpoint between its reference point and Manzanillo's; Manzanillo
    # runs from there to just short of the rocky point east of the village.
    # These are drawn GREY on the map and say "sin evaluar": a place to find,
    # never a tier. Replace them the day Caribbean Guard defines the beaches.
    provisional = {}
    joint = (-82.6783389 + -82.6571847) / 2
    for pid, w, e in (("cg:beach/playa-grande", cuts[-1], joint),
                      ("cg:beach/manzanillo", joint, PROVISIONAL_EAST)):
        sub = clip(line, w * M_PER_DEG_LON, e * M_PER_DEG_LON)
        sub = simplify(sub, SIMPLIFY_M)
        for _ in range(CHAIKIN_PASSES):
            sub = chaikin(sub)
        sub = simplify(sub, FINAL_SIMPLIFY_M)
        provisional[pid] = [to_ll(p) for p in sub]
        print("  provisional %-22s %4d pts  w:%.5f e:%.5f" % (pid, len(sub), w, e))

    doc = {
        "_": ("GENERATED by tools/osm_coastline.py from OpenStreetMap "
              "natural=coastline (tools/osm-coastline.json). Do not hand edit. "
              "Keyed by the zone ids in web/index.html. Coordinates are "
              "[lat, lon]."),
        "source": "openstreetmap natural=coastline",
        "licence": "ODbL, (c) OpenStreetMap contributors",
        "seaward_m": SEAWARD_M,
        "resample_m": RESAMPLE_M,
        "simplify_m": SIMPLIFY_M,
        "chaikin_passes": CHAIKIN_PASSES,
        "final_simplify_m": FINAL_SIMPLIFY_M,
        "zones": out,
        "provisional": provisional,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, separators=(",", ":"))
    print("\n  %d points, %.1f KB -> %s"
          % (total, os.path.getsize(OUT) / 1024.0, os.path.relpath(OUT, ROOT)))
    print("\n  spans for index.html (joints resolved, see the header):")
    for key, w, e in spans:
        print("    %-12s span:{w:%.5f, e:%.5f}," % (key, w, e))


if __name__ == "__main__":
    main()
