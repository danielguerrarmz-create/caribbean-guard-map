"""Print nearby OSM name candidates for human review of PDF place marks."""
import difflib
import json
import math
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def normal(name):
    name = unicodedata.normalize("NFKD", name or "")
    return "".join(c.lower() for c in name if c.isalnum() and not unicodedata.combining(c))


def distance(a, b):
    return math.hypot((a[0]-b[0])*109700, (a[1]-b[1])*111200)


def main():
    source = json.loads((ROOT / "web/data/full-map-geographic.geojson").read_text(encoding="utf8"))
    osm = json.loads((ROOT / "tools/data/osm-place-candidates.json").read_text(encoding="utf8"))
    for f in source["features"]:
        p = f["properties"]
        if p["kind"] != "location":
            continue
        name = p.get("name") or ""
        center = f["geometry"]["coordinates"]
        candidates = []
        for item in osm["elements"]:
            point = [item["lon"], item["lat"]]
            d = distance(center, point)
            if d > 1800:
                continue
            similarity = difflib.SequenceMatcher(None, normal(name), normal(item["name"])).ratio()
            if normal(name) in normal(item["name"]) and len(normal(name)) >= 5:
                similarity = max(similarity, .82)
            candidates.append((similarity, d, item))
        candidates.sort(key=lambda c: (-c[0], c[1]))
        top = [(round(s, 2), round(d), i["name"], f"{i['type']}/{i['id']}",
                [i["lon"], i["lat"]]) for s,d,i in candidates[:3]]
        print(f["id"].split("/")[-1], repr(name), top)


if __name__ == "__main__":
    main()
