"""One-off OSM place candidate audit for the PDF's location marks.

The output is evidence for manual review, not an automatic name-only match.
"""
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools/data/osm-place-candidates.json"
QUERY = '''[out:json][timeout:90];
(nwr["name"](9.600,-82.790,9.680,-82.640););
out center tags;'''


def main():
    request = urllib.request.Request(
        "https://overpass-api.de/api/interpreter",
        data=urllib.parse.urlencode({"data": QUERY}).encode(),
        headers={"User-Agent": "CaribbeanGuardMap/0.1 (one-off place audit)",
                 "Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        data = json.load(response)
    items = []
    for element in data["elements"]:
        tags = element.get("tags", {})
        center = element.get("center", element)
        if "lat" not in center or "lon" not in center:
            continue
        items.append({"type": element["type"], "id": element["id"],
                      "name": tags["name"], "lat": center["lat"],
                      "lon": center["lon"], "tags": tags})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"source": "OpenStreetMap contributors",
                               "license": "ODbL 1.0", "url": "https://www.openstreetmap.org/copyright",
                               "query": QUERY, "elements": items}, ensure_ascii=False, indent=2), encoding="utf8")
    print(f"Saved {len(items)} named OSM records to {OUT}")


if __name__ == "__main__":
    main()
