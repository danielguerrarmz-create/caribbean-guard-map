"""Rewrite the slippy map's zone polylines from the traced coastline.

`web/index.html` still carries the geometry `redraw_zones.py` produced: nine
points per zone, from a per-column scan that forced the coastline to be a
function of longitude. `tools/trace_coastline.py` replaced that with a real
contour (see its docstring for the measurements). This carries the fix across so
the map and the annotated sheets agree about where a beach is.

SIMPLIFIED BY DISTANCE, NOT BY COUNT. The old code took `MAX_POINTS = 9` evenly
spaced samples, which spends the same number of points on a straight beach as on
a headland and is why the line chorded at 250 m. Douglas-Peucker instead keeps a
point wherever dropping it would move the line by more than TOLERANCE_M, so
detail lands where the coast actually bends. A straight stretch costs almost
nothing and a point keeps what it needs.

TOLERANCE is 12 m. The map is drawn over imagery whose own registration is good
to a few metres, and the line marks a zone boundary rather than a surveyed edge,
so tightening this further buys nothing anyone can see and costs critical-path
bytes on a page measured at ~123 KB over 7 requests.
"""
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOLERANCE_M = 12.0
LAT_M = 110570.0
LON_M = 111320.0 * math.cos(math.radians(9.645))


def simplify(pts, tol_m):
    """Douglas-Peucker, iterative so a 500-point run cannot blow the stack."""
    if len(pts) < 3:
        return list(pts)
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        if b <= a + 1:
            continue
        (ya, xa), (yb, xb) = pts[a], pts[b]
        ax, ay = xa * LON_M, ya * LAT_M
        bx, by = xb * LON_M, yb * LAT_M
        dx, dy = bx - ax, by - ay
        seg = math.hypot(dx, dy)
        worst, wi = -1.0, a
        for i in range(a + 1, b):
            px, py = pts[i][1] * LON_M, pts[i][0] * LAT_M
            if seg == 0:
                dist = math.hypot(px - ax, py - ay)
            else:
                # perpendicular distance to the chord, clamped to the segment
                t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (seg * seg)))
                dist = math.hypot(px - (ax + t * dx), py - (ay + t * dy))
            if dist > worst:
                worst, wi = dist, i
        if worst > tol_m:
            keep[wi] = True
            stack.append((a, wi))
            stack.append((wi, b))
    return [p for p, k in zip(pts, keep) if k]


def main():
    coast = json.load(open(os.path.join(HERE, "coastline.json")))["zones"]
    path = os.path.join(ROOT, "web", "index.html")
    src = open(path, encoding="utf-8").read()
    before = len(src.encode("utf-8"))

    n = 0
    for zid, pts in coast.items():
        keep = simplify(pts, TOLERANCE_M)
        # 5 decimal places is ~1.1 m of latitude here, finer than the tolerance
        # and finer than the imagery; 6 would only pad the critical path.
        arr = "[" + ",".join(f"[{round(a,5)},{round(b,5)}]" for a, b in keep) + "]"
        pat = re.compile(r'(id:"cg:zone/' + re.escape(zid) + r'".*?\n\s*line:)\[\[.*?\]\]',
                         re.S)
        src, c = pat.subn(lambda m: m.group(1) + arr, src, count=1)
        n += c
        if not c:
            print(f"  WARNING: could not find line: for {zid}")
            continue
        backs = sum(1 for a, b in zip(keep, keep[1:]) if b[1] < a[1])
        print(f"  {zid:14} {len(pts):4d} -> {len(keep):3d} pts, "
              f"{backs:2d} longitude reversals kept")

    open(path, "w", encoding="utf-8").write(src)
    after = len(src.encode("utf-8"))
    d = after - before
    print(f"\nrewrote {n} zone polylines; index.html {before:,} -> {after:,} B "
          f"({d:+,} B on the critical path)")


if __name__ == "__main__":
    main()
