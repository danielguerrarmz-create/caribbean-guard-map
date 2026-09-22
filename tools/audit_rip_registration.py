"""Inspect PDF rip-arrow registration against GPS shoreline zone geometry."""
import json
import math
from pathlib import Path
from shapely.geometry import LineString, Point
from shapely.ops import nearest_points
from osm_coastline import chain, to_m

ROOT = Path(__file__).resolve().parents[1]
geo = json.loads((ROOT / "web/data/full-map-geographic.geojson").read_text(encoding="utf8"))


def metres(ll):
    return to_m((ll[1], ll[0]))


shore = LineString([to_m(point) for point in chain()])
rows = []
for feature in geo["features"]:
    if feature["properties"]["kind"] != "rip_current":
        continue
    pts = feature["geometry"]["coordinates"]
    start = Point(metres(pts[0]))
    closest = nearest_points(start, shore)[1]
    length = math.dist(metres(pts[0]), metres(pts[-1]))
    end = Point(metres(pts[-1]))
    d = shore.project(closest)
    before = shore.interpolate(max(0, d - 5))
    after = shore.interpolate(min(shore.length, d + 5))
    tx, ty = after.x - before.x, after.y - before.y
    nx, ny = -ty / math.hypot(tx, ty), tx / math.hypot(tx, ty)
    bearing = ((metres(pts[-1])[0]-start.x)*nx +
               (metres(pts[-1])[1]-start.y)*ny) / length
    signed = (start.x-closest.x)*nx + (start.y-closest.y)*ny
    rows.append((feature["id"].split("/")[-1], round(start.distance(closest)),
                 round(end.distance(shore)), round(signed), round(length), round(bearing, 2)))

if len(rows) != 53:
    raise SystemExit(f"Expected 53 headed PDF rip arrows; found {len(rows)}")
bad = [r for r in rows if r[1] > 30 or r[3] < 0 or r[4] < 12 or r[5] < .2]
if bad:
    raise SystemExit(f"Rip anchors, seaward directions, or lengths invalid: {bad}")
print(f"PASS: {len(rows)} headed rip arrows; starts "
      f"{min(r[1] for r in rows)}-{max(r[1] for r in rows)} m seaward of OSM coastline; "
      f"shortest arrow {min(r[4] for r in rows)} m")
