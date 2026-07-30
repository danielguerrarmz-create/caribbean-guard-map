"""Generate image placeholders that match the site's structure.

Caribbean Guard has real photography of a beautiful coast and it is one of their
genuine assets. This does not invent it. It reserves the slot, at the exact
aspect ratio the layout expects, and states in the frame what photograph belongs
there and roughly what it should show, so the gaps are a shot list rather than a
blank.

SVG rather than a raster: a few hundred bytes each, sharp at any size, and the
brief is readable in the file itself.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "site", "assets", "img", "placeholder")

INK = "#0B1C2C"
SAND = "#EFEADF"
RULE = "#CFC6B6"
MUTED = "#7A8894"

# slug, w, h, section label, what the photograph needs to show
SHOTS = [
    ("hero", 1600, 900, "Portada",
     "Guardavidas en el agua o patrullando, hora dorada. Horizontal, con espacio "
     "a la izquierda para el titular."),
    ("mapa", 1200, 800, "Mapa de Seguridad",
     "Alguien mirando el teléfono en la playa, con el mar detrás. Vertical u "
     "horizontal, la pantalla no tiene que leerse."),
    ("lifesaving", 1200, 900, "Lifesaving Club",
     "Entrenamiento de salvamento: entrada al agua con tabla o tubo de rescate."),
    ("swim", 1200, 900, "Swim Club",
     "Grupo nadando en aguas abiertas en Punta Uva o Playa Negra, temprano."),
    ("freediving", 1200, 900, "Freediving Club",
     "Apnea sobre el arrecife, vista desde superficie o desde abajo."),
    ("playa-organizada", 1600, 900, "Playa Organizada",
     "Banderas roja y amarilla plantadas en la arena, con la zona segura detrás."),
    ("estacion", 1200, 900, "Estación de salvamento",
     "Estación fija con tubos, mecate y salvavidas, al amanecer cuando se monta."),
    ("historia", 1600, 900, "Historia",
     "Foto de archivo de las primeras guardias, 2021. Aunque sea de baja calidad: "
     "es un documento, no una postal."),
    ("equipo", 1000, 1000, "Retrato de equipo",
     "Cuadrado, cara visible y ocupando buena parte del encuadre. Sin lentes de sol."),
    ("proyectos", 1200, 800, "Proyectos",
     "El equipo guardado hoy: tablas y cajas en un garaje prestado. Muestra el problema."),
    ("involucrate", 1200, 800, "Involúcrate",
     "Voluntarios en un curso o entrenamiento, gente reconocible de la comunidad."),
]


def wrap(text, per_line):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > per_line:
            lines.append(cur); cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


def svg(slug, w, h, label, brief):
    ratio = f"{w}×{h}"
    # keep type legible whatever the box: size from the shorter edge
    base = min(w, h)
    lab = round(base * 0.055)
    dim = round(base * 0.036)
    body = round(base * 0.032)
    pad = round(base * 0.075)
    lines = wrap(brief, 52)
    tspans = "".join(
        f'<tspan x="{pad}" dy="{body * 1.45 if i else 0}">{l}</tspan>'
        for i, l in enumerate(lines))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"
     width="{w}" height="{h}" role="img"
     aria-label="Espacio reservado para fotografía: {label}">
  <rect width="{w}" height="{h}" fill="{SAND}"/>
  <rect x="6" y="6" width="{w-12}" height="{h-12}" fill="none"
        stroke="{RULE}" stroke-width="3" stroke-dasharray="14 10"/>
  <path d="M{pad} {pad+lab*0.9} h{lab*1.6}" stroke="{INK}" stroke-width="{max(2,round(lab*0.12))}"/>
  <text x="{pad}" y="{pad + lab*2.2}" font-family="Poppins, system-ui, sans-serif"
        font-size="{lab}" font-weight="700" fill="{INK}">{label}</text>
  <text x="{pad}" y="{pad + lab*3.4}" font-family="ui-monospace, Menlo, Consolas, monospace"
        font-size="{dim}" fill="{MUTED}">FOTOGRAFÍA PENDIENTE · {ratio}</text>
  <text x="{pad}" y="{h - pad - body * (len(lines) - 1) * 1.45}"
        font-family="system-ui, sans-serif" font-size="{body}" fill="{INK}"
        opacity=".78">{tspans}</text>
</svg>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for slug, w, h, label, brief in SHOTS:
        p = os.path.join(OUT, f"{slug}.svg")
        open(p, "w", encoding="utf-8").write(svg(slug, w, h, label, brief))
        total += os.path.getsize(p)
        print(f"  {slug:18} {w}x{h}  {os.path.getsize(p):5d} B  {label}")
    print(f"\n{len(SHOTS)} placeholders, {total/1024:.1f} KB total -> {OUT}")


if __name__ == "__main__":
    main()
