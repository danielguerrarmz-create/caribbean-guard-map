"""Export the smoothed zone polylines the slippy map draws, to web/data/zones-geometry.json.

WHY THIS EXISTS
`web/index.html` carries the zone geometry inline, in `line:` arrays that came out
of `redraw_zones.py`. That script is the one the 2026-09-14 handoff retired: it
found the waterline with `shore_y[x] = col[0]`, one y per x, which forces the coast
to be a FUNCTION OF LONGITUDE. A real coast is not. Every headland has two or more
crossings at one longitude and the scan could keep only the northernmost, so the
inline arrays still double back on themselves -- Cocles alone has eight places
where the line runs east, then west, then east again inside forty metres. Those
reversals are the deleted half of a headland, drawn as a spike.

`tools/coastline.json` is the replacement: a contour trace, free to double back,
offset 30 m seaward along the local normal, sampled at an 8 m step. It is what the
four annotated sheets already draw. This script is the bridge that puts the same
geometry on the map, so the sheet and the map cannot disagree about where the
water is.

THE PIPELINE, AND WHY IT IS IN THIS ORDER
1. SIMPLIFY at 0.5 m (Douglas-Peucker). The trace is a pixel contour, so it
   carries a one-pixel staircase (1.18 m/px at z17) that no zoom of this map can
   resolve. Simplifying first matters: Chaikin cuts corners, and a staircase is
   all corners, so smoothing the raw trace spends four output points rounding off
   each step of a noise pattern.
2. CHAIKIN, twice. Corner cutting converges on a quadratic B-spline. Two passes is
   the point where the joints stop reading as joints at z17 and the line still
   sits inside the half-metre the trace is accurate to.
3. DECIMATE at 0.15 m. Chaikin quadruples the point count, and most of what it
   adds sits on straight runs where it buys nothing. 0.15 m is a QUARTER OF A
   PIXEL at the map's maximum zoom (z18 is 0.589 m/px at this latitude), so this
   pass cannot move a drawn pixel. It exists because this file is in the service
   worker's CRITICAL precache: it blocks install on the weak signal the whole map
   is built for, and every kilobyte there is bytes somebody waits for at the
   water's edge before the map will save.

Set DECIMATE_M = 0 to get the un-decimated spec pipeline and compare.

THE IDS ARE READ OUT OF index.html, NOT CONSTRUCTED. `"cg:zone/" + key` would
work today and would silently write a file the map cannot find the day somebody
renames a zone. This parses the ids the page actually uses and refuses to run if
the two sets differ.

Usage:  python tools/export_zones.py
"""
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "coastline.json")
PAGE = os.path.join(ROOT, "web", "index.html")
OUT = os.path.join(ROOT, "web", "data", "zones-geometry.json")

SIMPLIFY_M = 0.5        # below the trace's own accuracy
CHAIKIN_PASSES = 2
DECIMATE_M = 0.15       # a quarter pixel at z18; see the header
PRECISION = 6           # 1.1e-1 m of latitude. 5 would be 1.1 m, coarser than the simplify


# ---------- a local metric frame ----------
# Everything below works in metres on a plane tangent at the coast's mean
# latitude. Over 16 km of a 9.6 deg coast the equirectangular error is under a
# centimetre, which is two orders below the tolerances here, and it makes
# "0.5 metres" mean 0.5 metres in both axes instead of 0.5 of two different units.
LAT0 = 9.645
M_PER_DEG_LAT = 111132.0
M_PER_DEG_LON = 111320.0 * math.cos(math.radians(LAT0))


def to_m(p):
    return (p[1] * M_PER_DEG_LON, p[0] * M_PER_DEG_LAT)


def to_ll(q):
    return [round(q[1] / M_PER_DEG_LAT, PRECISION),
            round(q[0] / M_PER_DEG_LON, PRECISION)]


def seg_dist(p, a, b):
    """Distance from p to the SEGMENT ab, not to the infinite line."""
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    d2 = dx * dx + dy * dy
    if d2 == 0.0:
        return math.hypot(p[0] - ax, p[1] - ay)
    t = ((p[0] - ax) * dx + (p[1] - ay) * dy) / d2
    t = 0.0 if t < 0.0 else (1.0 if t > 1.0 else t)
    return math.hypot(p[0] - (ax + t * dx), p[1] - (ay + t * dy))


def simplify(pts, tol):
    """Douglas-Peucker, iterative so a 40,000 point trace cannot blow the stack."""
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
    """One corner-cutting pass on an OPEN chain.

    The endpoints are pinned. They have to be: these are five zones laid end to
    end along one coast, and a pass that moved the ends would open a gap between
    Cocles and Chiquita at exactly the boundary the 2026-07-30 review flagged as
    the place the map can assert the wrong verdict.
    """
    if len(pts) < 3:
        return list(pts)
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        out.append((0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]))
        out.append((0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1]))
    out.append(pts[-1])
    return out


def max_deviation(out_pts, src_pts):
    """Farthest any output point sits from the SOURCE polyline, in metres.

    Point-to-polyline, not point-to-point: the pipeline deletes and invents
    points on purpose, so comparing by index would measure the resampling rather
    than the displacement. Windowed around the running nearest index because the
    full cross product is 40,000 x 1,700 per zone.
    """
    if len(src_pts) < 2:
        return 0.0
    worst = 0.0
    j = 0
    for p in out_pts:
        lo, hi = max(0, j - 40), min(len(src_pts) - 1, j + 40)
        best, bj = float("inf"), j
        for k in range(lo, hi):
            d = seg_dist(p, src_pts[k], src_pts[k + 1])
            if d < best:
                best, bj = d, k
        j = bj
        if best > worst:
            worst = best
    return worst


def page_zone_ids():
    """The ids web/index.html actually keys its zones by, in page order."""
    src = open(PAGE, encoding="utf-8").read()
    ids = re.findall(r'id\s*:\s*"(cg:zone/[^"]+)"', src)
    if not ids:
        raise SystemExit("no cg:zone/ ids found in web/index.html")
    return ids


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    zones = data["zones"]
    ids = page_zone_ids()

    by_key = {i.split("/", 1)[1]: i for i in ids}
    missing = sorted(set(by_key) - set(zones))
    extra = sorted(set(zones) - set(by_key))
    if missing or extra:
        raise SystemExit(
            "coastline.json and index.html disagree about the zones.\n"
            f"  in the page but not the trace: {missing}\n"
            f"  in the trace but not the page: {extra}")

    out = {}
    rows = []
    for key in (i.split("/", 1)[1] for i in ids):
        src = [to_m(p) for p in zones[key]]
        n0 = len(src)

        pts = simplify(src, SIMPLIFY_M)
        n_simp = len(pts)
        for _ in range(CHAIKIN_PASSES):
            pts = chaikin(pts)
        n_smooth = len(pts)
        if DECIMATE_M > 0:
            pts = simplify(pts, DECIMATE_M)
        n_out = len(pts)

        dev = max_deviation(pts, src)
        # Ground length, so "points per km" is readable next to the 8 m source step.
        length = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))

        out[by_key[key]] = [to_ll(q) for q in pts]
        rows.append((key, n0, n_simp, n_smooth, n_out, dev, length))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = {
        "_": "GENERATED by tools/export_zones.py from tools/coastline.json. "
             "Do not hand edit. Keyed by the zone ids in web/index.html. "
             "Coordinates are [lat, lon].",
        "source": "tools/coastline.json",
        "step_m": data.get("step_m"),
        "seaward_m": data.get("seaward_m"),
        "simplify_m": SIMPLIFY_M,
        "chaikin_passes": CHAIKIN_PASSES,
        "decimate_m": DECIMATE_M,
        "zones": out,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, separators=(",", ":"))

    w = max(len(r[0]) for r in rows)
    print(f"{'zone'.ljust(w)}  source  simplified  smoothed  written   max dev   length")
    for key, n0, n_simp, n_smooth, n_out, dev, length in rows:
        print(f"{key.ljust(w)}  {n0:>6}  {n_simp:>10}  {n_smooth:>8}  {n_out:>7}"
              f"  {dev:>6.2f} m  {length/1000:>5.2f} km")
    tot_in = sum(r[1] for r in rows)
    tot_out = sum(r[4] for r in rows)
    worst = max(r[5] for r in rows)
    print(f"{'TOTAL'.ljust(w)}  {tot_in:>6}  {'':>10}  {'':>8}  {tot_out:>7}"
          f"  {worst:>6.2f} m")
    print(f"\n{OUT.replace(ROOT + os.sep, '')}: {os.path.getsize(OUT)/1024:.1f} KB")
    print(f"max deviation from the traced coastline: {worst:.2f} m "
          f"(the trace is itself a 30 m seaward offset of a 1.18 m/px contour)")


if __name__ == "__main__":
    main()
