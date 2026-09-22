"""Project supplied PDF annotations onto the GPS map from four common stations.

The PDF has no geographic CRS. This is a provisional affine registration, not
surveyed positioning. Keep its provenance and uncertainty with every feature.
"""
import json
from pathlib import Path

import numpy as np
from osm_coastline import chain, M_PER_DEG_LAT, M_PER_DEG_LON

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "web/data/full-map-source.json"
REFERENCE = ROOT / "web/data/cg-hazards.geojson"
OUTPUT = ROOT / "web/data/full-map-geographic.geojson"
NUMBERS = ("3.2", "3.3", "3.5", "3.6")
ACCESS_KINDS = {"location"}
ROAD_KINDS = {"main_road", "side_road", "pedestrian"}
# Manually reviewed OSM matches span the coast and correct the document's
# place layer. Safety marks retain their separate station-based registration.
MATCHES = ROOT / "tools/data/place-matches.json"
OSM_PLACES = ROOT / "tools/data/osm-place-candidates.json"
METRES_PER_DEGREE = np.array([M_PER_DEG_LON, M_PER_DEG_LAT])


def main():
    source = json.loads(SOURCE.read_text(encoding="utf8"))
    reference = json.loads(REFERENCE.read_text(encoding="utf8"))
    page = {f["number"]: f["point"] for f in source["features"] if f.get("number")}
    gps = {f["properties"]["source_number"]: f["geometry"]["coordinates"]
           for f in reference["features"] if f["properties"].get("source_number")}
    train = np.array([page[n]+[1] for n in NUMBERS], dtype=float)
    target = np.array([gps[n] for n in NUMBERS], dtype=float)
    matrix = np.linalg.lstsq(train, target, rcond=None)[0]
    residual = np.linalg.norm((train @ matrix-target)*METRES_PER_DEGREE, axis=1)
    if residual.max() > 20:
        raise RuntimeError(f"Control point residual too high: {residual}")

    match_refs = json.loads(MATCHES.read_text(encoding="utf8"))
    osm = json.loads(OSM_PLACES.read_text(encoding="utf8"))
    osm_by_ref = {f"{e['type']}/{e['id']}": e for e in osm["elements"]}
    source_by_id = {f["id"].split("/")[-1]: f for f in source["features"]}
    fixed = {}
    for number, ref in match_refs.items():
        f = source_by_id[number]
        if f["kind"] != "location" or ref not in osm_by_ref:
            raise ValueError(f"Invalid place match: {number} -> {ref}")
        e = osm_by_ref[ref]
        fixed[f["id"]] = {"coordinates": [e["lon"], e["lat"]],
                          "url": f"https://www.openstreetmap.org/{ref}",
                          "name": e["name"]}
    access_control_points = [np.array(source_by_id[n]["point"]) for n in match_refs]
    access_control_deltas = [
        (np.array(fixed[source_by_id[n]["id"]]["coordinates"])
         - np.array([*source_by_id[n]["point"], 1.0]) @ matrix) * METRES_PER_DEGREE
        for n in match_refs
    ]
    # Zero-displacement anchors keep the access layer in register near the
    # stations whose GPS positions are already known.
    access_control_points += [np.array(page[n]) for n in NUMBERS]
    access_control_deltas += [np.zeros(2) for _ in NUMBERS]
    access_control_points = np.array(access_control_points)
    access_control_deltas = np.array(access_control_deltas)
    coastline = np.array([[lon * M_PER_DEG_LON, lat * M_PER_DEG_LAT]
                          for lat, lon in chain()])
    coast_a, coast_v = coastline[:-1], np.diff(coastline, axis=0)
    coast_len2 = np.sum(coast_v * coast_v, axis=1)

    def nearest_shore(point):
        t = np.clip(np.sum((point - coast_a) * coast_v, axis=1) /
                    np.maximum(coast_len2, 1), 0, 1)
        nearest = coast_a + coast_v * t[:, None]
        i = int(np.argmin(np.sum((nearest - point) ** 2, axis=1)))
        tangent = coast_v[i] / np.sqrt(coast_len2[i])
        normal = np.array([-tangent[1], tangent[0]])  # OSM west-to-east, sea on left.
        return nearest[i], normal, float(np.linalg.norm(nearest[i] - point))

    def access_correction(point):
        distances = np.linalg.norm(access_control_points - point, axis=1)
        weights = 1.0 / (distances**2 + 250.0**2)**2
        return np.average(access_control_deltas, axis=0, weights=weights)

    def locate(point, kind):
        ll = np.array([*point, 1.0]) @ matrix
        if kind in ACCESS_KINDS:
            ll += access_correction(np.array(point)) / METRES_PER_DEGREE
        return [round(float(ll[0]), 7), round(float(ll[1]), 7)]

    def register_rip(points):
        """Fit along-coast position from place controls, then anchor to GPS shore.

        The source PDF supplies direction and curve, not absolute GPS positions.
        Use whichever endpoint approaches the mapped coast. Keep the original
        arrow vector; a landward-pointing document arrow must not be reversed.
        """
        pts = np.array([np.array([*p, 1.0]) @ matrix for p in points])
        correction = access_correction(np.array(points[0])) / METRES_PER_DEGREE
        pts += correction
        xy = pts * METRES_PER_DEGREE
        start = nearest_shore(xy[0])
        end = nearest_shore(xy[-1])
        i = 0 if start[2] <= end[2] else -1
        shore, normal, distance = start if i == 0 else end
        shifted = xy + (shore + normal * 24.0 - xy[i])
        # A small seaward clearance keeps a curved arrow off the sand without
        # changing its document direction or the shoreline anchor it follows.
        minimum = min(float(np.dot(p - nearest_shore(p)[0], nearest_shore(p)[1]))
                      for p in shifted)
        if minimum < 6:
            shifted += normal * (6 - minimum)
        return [[round(float(lon), 7), round(float(lat), 7)]
                for lon, lat in shifted / METRES_PER_DEGREE], round(distance, 1)

    features = []
    for f in source["features"]:
        kind = f["kind"]
        if kind in ROAD_KINDS:
            continue  # Roads come from geographic OpenStreetMap data.
        if kind in {"rescue_station", "proposed_rescue_station"} and f.get("number") in NUMBERS:
            continue  # Preserve the four existing, more accurately placed GPS stations.
        if kind == "strong_current_area":
            continue  # Existing GPS polygon has a stronger georeference.
        rip_shift = None
        if f["coordinates"]:
            if kind == "rip_current":
                coordinates, rip_shift = register_rip(f["coordinates"])
            else:
                coordinates = [locate(p, kind) for p in f["coordinates"]]
            if kind == "strong_current_area":
                geometry = {"type": "Polygon", "coordinates": [coordinates]}
            else:
                geometry = {"type": "LineString", "coordinates": coordinates}
        else:
            geometry = {"type": "Point", "coordinates":
                        fixed[f["id"]]["coordinates"] if f["id"] in fixed else locate(f["point"], kind)}
        matched = fixed.get(f["id"])
        features.append({"type": "Feature", "id": f["id"], "geometry": geometry,
                         "properties": {"kind": kind, "number": f.get("number"),
                                        "name": f.get("name"), "source_page": 1,
                                        "registration": "osm_named_place" if matched else ("estimated_from_nearby_places" if kind in ACCESS_KINDS else "pdf_direction_osm_shore_anchor" if kind == "rip_current" else "provisional_four_station_affine"),
                                        "pdf_anchor_to_shore_m": rip_shift,
                                        "osm_name": matched["name"] if matched else None,
                                        "source_url": matched["url"] if matched else None,
                                        "needs_confirmation": not bool(matched)}})

    output = {"type": "FeatureCollection", "properties": {
        "source": source["source"], "source_sha256": source["sha256"],
        "registration": "Affine PDF-page to WGS84, using existing station numbers 3.2, 3.3, 3.5 and 3.6",
        "control_residual_m": dict(zip(NUMBERS, np.round(residual, 1).tolist())),
        "maximum_control_residual_m": round(float(residual.max()), 1),
        "accuracy_note": "Control residual is not independent positional accuracy. Rip arrows are anchored to an OSM shoreline from PDF positions and directions; they do not verify live current positions. Do not use for navigation or rescue dispatch.",
        "place_alignment": f"{len(fixed)} named places use OSM coordinates. Other place marks are estimates from the PDF page fitted to those places and four GPS stations; still provisional.",
        "access_place_controls": {n: match_refs[n] for n in match_refs},
        "fixed_place_count": len(fixed),
        "page_to_lonlat": matrix.tolist(), "feature_count": len(features)},
        "features": features}
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, separators=(",", ":"))+"\n", encoding="utf8")
    print("wrote", OUTPUT, "features", len(features), "control residuals (m)", output["properties"]["control_residual_m"])


if __name__ == "__main__":
    main()
