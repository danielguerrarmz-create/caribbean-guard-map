"""Fetch mapped roads and paths for the coastal map from OpenStreetMap.

The extract is geographic source data, not proof that a road is public, open,
safe, or passable. Run explicitly when the checked-in extract needs review.
"""
import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "web/data/osm-roads.geojson"
OSM_API = "https://api.openstreetmap.org/api/0.6/map"
BBOX = (9.600, -82.790, 9.680, -82.640)  # south, west, north, east
# Smaller requests are faster and less disruptive to the main OSM map API.
BOXES = [
    (-82.790, 9.600, -82.740, 9.680),
    (-82.740, 9.600, -82.690, 9.680),
    (-82.690, 9.600, -82.640, 9.680),
]

KEEP = {
    "motorway", "trunk", "primary", "secondary", "tertiary",
    "unclassified", "residential", "living_street", "service",
    "track", "path", "footway", "pedestrian", "cycleway", "steps",
}


def road_class(highway):
    if highway in {"motorway", "trunk", "primary", "secondary", "tertiary"}:
        return "main"
    if highway in {"path", "footway", "pedestrian", "cycleway", "steps"}:
        return "path"
    return "local"


def main():
    nodes = {}
    ways = {}
    for west, south, east, north in BOXES:
        url = f"{OSM_API}?bbox={west},{south},{east},{north}"
        request = urllib.request.Request(
            url, headers={"User-Agent": "CaribbeanGuardMap/0.1 (source-data refresh)"}
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            root = ET.parse(response).getroot()
        for node in root.findall("node"):
            nodes[node.attrib["id"]] = [float(node.attrib["lon"]), float(node.attrib["lat"])]
        for way in root.findall("way"):
            tags = {tag.attrib["k"]: tag.attrib["v"] for tag in way.findall("tag")}
            highway = tags.get("highway")
            if highway in KEEP:
                ways[way.attrib["id"]] = {
                    "tags": tags,
                    "refs": [nd.attrib["ref"] for nd in way.findall("nd")],
                }

    features = []
    for way_id, way in ways.items():
        tags = way["tags"]
        highway = tags.get("highway")
        geometry = [nodes[ref] for ref in way["refs"] if ref in nodes]
        if len(geometry) < 2:
            continue
        features.append({
            "type": "Feature",
            "id": f"osm:way/{way_id}",
            "geometry": {"type": "LineString", "coordinates": [
                [round(point[0], 7), round(point[1], 7)]
                for point in geometry
            ]},
            "properties": {
                "osm_way_id": int(way_id),
                "highway": highway,
                "road_class": road_class(highway),
                "name": tags.get("name"),
                "surface": tags.get("surface"),
                "access": tags.get("access"),
                "source": "OpenStreetMap contributors",
            },
        })

    output = {
        "type": "FeatureCollection",
        "properties": {
            "source": "OpenStreetMap contributors",
            "license": "ODbL 1.0",
            "source_url": "https://www.openstreetmap.org/copyright",
            "api_endpoint": OSM_API,
            "bbox": BBOX,
            "accuracy_note": "Mapped roads and paths; not proof of public access, current condition, or passability.",
            "feature_count": len(features),
        },
        "features": features,
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf8")
    print(f"wrote {OUTPUT} features {len(features)}")


if __name__ == "__main__":
    main()
