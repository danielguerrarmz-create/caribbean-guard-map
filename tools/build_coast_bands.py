"""Build fold-free, colored coast-band geometry from zones-geometry.json.

Requires Shapely 2.x. The complete coast is buffered once, then divided at the
shared beach endpoints. This avoids the self-intersecting vertex-normal offsets
used by the older browser-side bandPolygon implementation.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "web/data/zones-geometry.json"
TARGET = ROOT / "web/data/coast-bands.geojson"
M_LAT = 111132.0
M_LON = 111320.0 * math.cos(math.radians(9.645))
SEA_M = 95.0
LAND_M = 25.0
PLANE_SIZE_M = 100_000.0


def to_xy(point: list[float]) -> tuple[float, float]:
    return (point[1] * M_LON, point[0] * M_LAT)


def to_lon_lat(point: tuple[float, float]) -> list[float]:
    return [round(point[0] / M_LON, 7), round(point[1] / M_LAT, 7)]


def serialize_polygon(shape):
    if shape.geom_type == "Polygon":
        return {"type": "Polygon", "coordinates": [
            [to_lon_lat(p) for p in shape.exterior.coords],
            *[[to_lon_lat(p) for p in ring.coords] for ring in shape.interiors],
        ]}
    if shape.geom_type == "MultiPolygon":
        return {"type": "MultiPolygon", "coordinates": [
            serialize_polygon(part)["coordinates"] for part in shape.geoms
        ]}
    raise ValueError(f"Unexpected band geometry: {shape.geom_type}")


def serialize_line(shape):
    if shape.is_empty:
        return {"type": "MultiLineString", "coordinates": []}
    if shape.geom_type == "LineString":
        return {"type": "LineString", "coordinates": [to_lon_lat(p) for p in shape.coords]}
    parts = [part for part in getattr(shape, "geoms", []) if part.geom_type == "LineString"]
    return {"type": "MultiLineString", "coordinates": [
        [to_lon_lat(p) for p in part.coords] for part in parts
    ]}


def half_plane(point, tangent, sign):
    """The seaward band side of a cross-shore cut at a zone joint."""
    tx, ty = tangent
    nx, ny = -ty, tx
    d = PLANE_SIZE_M
    a = (point[0] - nx * d, point[1] - ny * d)
    b = (point[0] + nx * d, point[1] + ny * d)
    shift = (sign * tx * d, sign * ty * d)
    return Polygon([a, b, (b[0] + shift[0], b[1] + shift[1]),
                    (a[0] + shift[0], a[1] + shift[1])])


def main():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    beaches = list(source["zones"].items()) + list(source["provisional"].items())
    all_points = []
    joint_indices = [0]
    for index, (_, points) in enumerate(beaches):
        projected = [to_xy(point) for point in points]
        if index:
            if projected[0] != all_points[-1]:
                raise ValueError("Adjacent beach lines do not share an endpoint")
            all_points.extend(projected[1:])
        else:
            all_points.extend(projected)
        joint_indices.append(len(all_points) - 1)

    coast = LineString(all_points)
    if not coast.is_simple:
        raise ValueError("The source coastline crosses itself")
    sea = coast.buffer(SEA_M, single_sided=True, cap_style="flat", join_style="round", quad_segs=12)
    land = coast.buffer(-LAND_M, single_sided=True, cap_style="flat", join_style="round", quad_segs=12)
    corridor = unary_union([sea, land])
    offshore_edge = coast.offset_curve(SEA_M, join_style="round", quad_segs=12)
    if not corridor.is_valid:
        raise ValueError("The complete coast band is invalid")

    cuts = []
    for index in joint_indices:
        # Flat buffer caps use the first and last segment's exact direction.
        # Interior cuts average nearby bearings so adjacent colors share a
        # stable cross-shore boundary through each joint.
        span = 1 if index in (0, len(all_points) - 1) else 3
        before = all_points[max(0, index - span)]
        after = all_points[min(len(all_points) - 1, index + span)]
        length = math.dist(before, after)
        tangent = ((after[0] - before[0]) / length, (after[1] - before[1]) / length)
        cuts.append((all_points[index], tangent))

    features = []
    parts = []
    for index, (zone_id, _) in enumerate(beaches):
        west = half_plane(*cuts[index], +1)
        east = half_plane(*cuts[index + 1], -1)
        cell = west.intersection(east)
        band = corridor.intersection(cell)
        edge = offshore_edge.intersection(cell)
        if band.is_empty or not band.is_valid or band.geom_type not in ("Polygon", "MultiPolygon"):
            raise ValueError(f"Invalid generated band for {zone_id}: {band.geom_type}")
        parts.append(band)
        features.append({"type": "Feature", "properties": {"id": zone_id, "kind": "band"},
                         "geometry": serialize_polygon(band)})
        features.append({"type": "Feature", "properties": {"id": zone_id, "kind": "offshore"},
                         "geometry": serialize_line(edge)})
        for side, cut in (("west", cuts[index]), ("east", cuts[index + 1])):
            point, (tx, ty) = cut
            nx, ny = -ty, tx
            cap = LineString([
                (point[0] - nx * LAND_M, point[1] - ny * LAND_M),
                (point[0] + nx * SEA_M, point[1] + ny * SEA_M),
            ])
            features.append({"type": "Feature", "properties": {"id": zone_id, "kind": "cap", "side": side},
                             "geometry": serialize_line(cap)})

    joined = unary_union(parts)
    missing = corridor.difference(joined).area
    excess = joined.difference(corridor).area
    if missing > 0.01 or excess > 0.01:
        raise ValueError(f"The divided bands do not cover the complete coast corridor: missing={missing:.2f}, excess={excess:.2f}")
    for i, one in enumerate(parts):
        for two in parts[i + 1:]:
            if one.intersection(two).area > 0.01:
                raise ValueError("Two adjacent colored bands overlap")
    TARGET.write_text(json.dumps({
        "type": "FeatureCollection",
        "_": "Generated by tools/build_coast_bands.py. Approximate display extent, not a surveyed hazard boundary.",
        "source": "web/data/zones-geometry.json",
        "seaward_m": SEA_M,
        "landward_m": LAND_M,
        "features": features,
    }, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Generated {len(parts)} valid, nonoverlapping coast bands: {TARGET}")


if __name__ == "__main__":
    main()
