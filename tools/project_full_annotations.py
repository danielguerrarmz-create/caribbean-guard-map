"""Project supplied PDF annotations onto the GPS map from four common stations.

The PDF has no geographic CRS. This is a provisional affine registration, not
surveyed positioning. Keep its provenance and uncertainty with every feature.
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "web/data/full-map-source.json"
REFERENCE = ROOT / "web/data/cg-hazards.geojson"
OUTPUT = ROOT / "web/data/full-map-geographic.geojson"
NUMBERS = ("3.2", "3.3", "3.5", "3.6")
ACCESS_KINDS = {"main_road", "side_road", "pedestrian", "location"}
# Named places were matched manually to OpenStreetMap/Nominatim on 2026-09-21.
# These point controls spread across the PDF, unlike the four GPS stations.
# They correct the document's access/place layer only; the safety marks retain
# their existing station-based registration until independent hazard controls exist.
PLACE_CONTROLS = {
    "Banana Azul": [-82.7732589, 9.6583982],
    "Rocking J’s": [-82.7460948, 9.6580667],
    "Congo Bongo": [-82.6639564, 9.6307495],
    "Maxi’s": [-82.6577014, 9.6326302],
}
METRES_PER_DEGREE = np.array([109700.0, 111200.0])


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

    place = {f["name"]: f["point"] for f in source["features"]
             if f["kind"] == "location" and f.get("name")}
    access_control_points = [np.array(place[n]) for n in PLACE_CONTROLS]
    access_control_deltas = [
        (np.array(ll) - np.array([*place[n], 1.0]) @ matrix) * METRES_PER_DEGREE
        for n, ll in PLACE_CONTROLS.items()
    ]
    # Zero-displacement anchors keep the access layer in register near the
    # stations whose GPS positions are already known.
    access_control_points += [np.array(page[n]) for n in NUMBERS]
    access_control_deltas += [np.zeros(2) for _ in NUMBERS]
    access_control_points = np.array(access_control_points)
    access_control_deltas = np.array(access_control_deltas)

    def access_correction(point):
        distances = np.linalg.norm(access_control_points - point, axis=1)
        weights = 1.0 / (distances**2 + 250.0**2)**2
        return np.average(access_control_deltas, axis=0, weights=weights)

    def locate(point, kind):
        ll = np.array([*point, 1.0]) @ matrix
        if kind in ACCESS_KINDS:
            ll += access_correction(np.array(point)) / METRES_PER_DEGREE
        return [round(float(ll[0]), 7), round(float(ll[1]), 7)]

    features = []
    for f in source["features"]:
        kind = f["kind"]
        if kind in {"rescue_station", "proposed_rescue_station"} and f.get("number") in NUMBERS:
            continue  # Preserve the four existing, more accurately placed GPS stations.
        if kind == "strong_current_area":
            continue  # Existing GPS polygon has a stronger georeference.
        if f["coordinates"]:
            coordinates = [locate(p, kind) for p in f["coordinates"]]
            if kind == "strong_current_area":
                geometry = {"type": "Polygon", "coordinates": [coordinates]}
            else:
                geometry = {"type": "LineString", "coordinates": coordinates}
        else:
            geometry = {"type": "Point", "coordinates": locate(f["point"], kind)}
        features.append({"type": "Feature", "id": f["id"], "geometry": geometry,
                         "properties": {"kind": kind, "number": f.get("number"),
                                        "name": f.get("name"), "source_page": 1,
                                        "registration": "manual_place_aligned" if kind in ACCESS_KINDS else "provisional_four_station_affine",
                                        "needs_confirmation": True}})

    output = {"type": "FeatureCollection", "properties": {
        "source": source["source"], "source_sha256": source["sha256"],
        "registration": "Affine PDF-page to WGS84, using existing station numbers 3.2, 3.3, 3.5 and 3.6",
        "control_residual_m": dict(zip(NUMBERS, np.round(residual, 1).tolist())),
        "maximum_control_residual_m": round(float(residual.max()), 1),
        "accuracy_note": "Control residual is not independent positional accuracy. Placement beyond the control stations is provisional; do not use for navigation or rescue dispatch.",
        "access_alignment": "Access and place marks have a smooth local offset fitted to four named OSM places and zero displacement at the four GPS stations; still provisional, not evidence of public access.",
        "access_place_controls": PLACE_CONTROLS,
        "page_to_lonlat": matrix.tolist(), "feature_count": len(features)},
        "features": features}
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, separators=(",", ":"))+"\n", encoding="utf8")
    print("wrote", OUTPUT, "features", len(features), "control residuals (m)", output["properties"]["control_residual_m"])


if __name__ == "__main__":
    main()
