"""Write a reviewable record of every PDF place mark and its map position."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEO = ROOT / "web/data/full-map-geographic.geojson"
OUT = ROOT / "docs/data/place-marker-audit.csv"


def main():
    geo = json.loads(GEO.read_text(encoding="utf8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["pdf_marker_id", "pdf_label", "display_label", "longitude", "latitude",
                         "placement", "source_url", "review_note"])
        for feature in geo["features"]:
            p = feature["properties"]
            if p["kind"] != "location":
                continue
            number = feature["id"].split("/")[-1]
            ambiguous = number in {"339", "343", "406", "408", "466", "470", "472"}
            note = ("Coincident duplicate of 406; hidden in UI" if number == "408" else
                    "Generic or truncated PDF label; identity unresolved" if ambiguous else
                    "OSM mapped point or feature center; not a field survey" if p["source_url"] else
                    "Estimated from PDF page and nearby fixed place controls")
            lon, lat = feature["geometry"]["coordinates"]
            writer.writerow([feature["id"], p.get("name") or "", p.get("osm_name") or
                             ("Unidentified place" if ambiguous else p.get("name") or "Unidentified place"),
                             lon, lat, p["registration"], p.get("source_url") or "", note])
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
