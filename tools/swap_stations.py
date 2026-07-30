"""Replace the invented observation posts with Caribbean Guard's real stations.

The POSTS array in index.html was mine: four posts at coordinates I chose, with
staffing hours I made up. Caribbean Guard's own annotated map marks four actual
rescue stations, and tools/extract_annotations.py already lifted them into
web/data/cg-hazards.geojson at 1.2 m.

What the sheet gives us is a POSITION and nothing else. So this names each one by
the beach it sits on rather than inventing an identity, and takes the description
of what a station holds from Caribbean Guard's own Playa Organizada page rather
than writing new copy:

    "Estructuras fijas, en la playa con implementos de flotación para rescate:
     tubos y torpedos de rescate, caja de mecate (200 metros), salvavidas,
     chaleco y silbato. Compromiso con socios locales de poner y sacar cada día
     los implementos —al amanecer y atardecer—."

That last clause replaces the invented "9:00 a 17:00": the equipment goes out at
dawn and comes in at dusk, put there by local partners. It is a real fact about
how the stations work, and it is a more useful thing to tell somebody than a
staffing window that was never true.

Every station carries needs_confirmation, because the sheet is undated.
"""
import json, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# The named beaches, west to east, so a station can be labelled by where it is.
BEACHES = [
    (-82.7700, -82.7580, "Playa Negra"),
    (-82.7580, -82.7480, "Puerto Viejo"),
    (-82.7480, -82.7270, "Playa Cocles"),
    (-82.7270, -82.7060, "Playa Chiquita"),
    (-82.7060, -82.6880, "Punta Uva"),
    (-82.6880, -82.6300, "Manzanillo"),
]


def beach_for(lon):
    for w, e, name in BEACHES:
        if w <= lon < e:
            return name
    return "la costa"


def main():
    gj = json.load(open(os.path.join(ROOT, "web", "data", "cg-hazards.geojson"),
                       encoding="utf-8"))
    st = [f for f in gj["features"] if f["properties"]["kind"] == "rescue_station"]
    st.sort(key=lambda f: f["geometry"]["coordinates"][0])   # west to east
    print(f"{len(st)} rescue stations in Caribbean Guard's sheet")

    # more than one station can share a beach, so number within it
    seen = {}
    rows = []
    for i, f in enumerate(st, 1):
        lon, lat = f["geometry"]["coordinates"]
        b = beach_for(lon)
        seen[b] = seen.get(b, 0) + 1
        suffix = f" {seen[b]}" if [beach_for(x["geometry"]["coordinates"][0])
                                   for x in st].count(b) > 1 else ""
        rows.append({
            "id": f"est{i}", "n": str(i), "kind": "station",
            "ll": [round(lat, 5), round(lon, 5)],
            "es": f"Estación de salvamento · {b}{suffix}",
            "en": f"Rescue station · {b}{suffix}",
        })
        print(f"  {rows[-1]['id']}  {lat:.5f}, {lon:.5f}   {b}{suffix}")

    block = "const POSTS = [\n" + ",\n".join(
        f'  {{id:"{r["id"]}", n:"{r["n"]}", kind:"{r["kind"]}", ll:[{r["ll"][0]},{r["ll"][1]}],\n'
        f'   name:{{es:"{r["es"]}", en:"{r["en"]}"}},\n'
        f'   hours:{{es:"Equipo colocado al amanecer y retirado al atardecer por los socios locales",\n'
        f'          en:"Equipment put out at dawn and taken in at dusk by local partners"}},\n'
        f'   reviewed: null}}'
        for r in rows) + "\n];"

    p = os.path.join(ROOT, "web", "index.html")
    src = open(p, encoding="utf-8").read()
    new, n = re.subn(r"const POSTS = \[.*?\n\];", block, src, count=1, flags=re.S)
    if not n:
        raise SystemExit("could not find the POSTS array")
    open(p, "w", encoding="utf-8").write(new)
    print(f"\nreplaced the POSTS array in web/index.html")


if __name__ == "__main__":
    main()
