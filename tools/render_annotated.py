"""Render an annotated sheet: satellite imagery with the annotations written ON it.

Not a slippy map. The output is one picture a guard can print, hand over, mark up
with a pen and sign. That is the artefact Caribbean Guard already makes by hand
(`reference/cg-existing-maps/annotated-base-map-v5.png`) and the shorter path to
something they will actually sign.

THE BASEMAP IS BING, NOT `web/img/base.webp`. Ruled by Daniel on 2026-09-14 after
the two were compared with the same traced coastline drawn on each: on Bing the
line sits on the surf edge for the whole of Cocles, on the base it sits on the dry
sand. `base.webp` is a generative upscale of Google Earth captures and carries 5
to 75 m of registration error (measured 2026-07-30 by `tools/residual.py`). Cocles
beach is about 40 m wide, so the error is wider than the beach. Bing is also the
finer picture, 1.18 m/px against 1.85, and it is real imagery rather than invented
texture. Every annotation already lives in Bing coordinates: the coastline is
traced from it, and Caribbean Guard's own hazard sheet georeferenced against it at
1.2 m. Nothing has to be warped to make this work.

Three rules carried over from the map, unchanged, because they are properties of
the data and not of the surface that draws it:

1.  NO LABEL GRANTS PERMISSION. The level names are instructions, not ratings.
    `SE PUEDE NADAR` does not exist here either. See web/index.html, the three
    rules above `const T`.
2.  EVERY MARK CARRIES ITS PROVENANCE. `authored` and `reviewed` travel with the
    annotation onto the sheet, and an unsigned sheet says so in its own band at
    the top. A mark nobody has signed must look different from a mark a guard
    signed, or the sheet launders a guess into an authority.
3.  RIP BEARING IS NOT CLAIMED. Position is Caribbean Guard's. The arrowheads on
    their sheet were never machine-read, so arrows are drawn along the local
    seaward normal and the legend says the direction is indicative. Do not
    "improve" this into a real bearing without solving arrowhead detection.

Usage:  python tools/render_annotated.py            # every sheet
        python tools/render_annotated.py chiquita   # one
"""
import json
import math
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "tools"
HAZARDS = json.loads((ROOT / "web" / "data" / "cg-hazards.geojson").read_text())
# THE SHEETS AND THE MAP READ THE SAME FILE. 2026-09-17.
#
# This was `coastline.json`, the contour traced out of the satellite mosaic's
# water mask, which on this reef coast followed the reef and not the beach: the
# Salsa Brava line came out 2,303 m long against a 1,294 m beach. The map moved
# to the OpenStreetMap coastline the same day and this did not, which left the
# printed sheet and the slippy map disagreeing about where the water is, in
# opposite directions, on the same stretch of sand.
#
# That is the exact failure the morning's work set out to prevent, so there is
# now ONE file and no second copy to drift: whatever tools/osm_coastline.py
# writes for the map is what gets printed. It is keyed by the full zone id
# because index.html is, and the ids are read out of index.html rather than
# constructed; SHEETS below is keyed by the short name, so it is re-keyed here
# and nowhere else.
_GEOM = json.loads((ROOT / "web" / "data" / "zones-geometry.json").read_text())
COAST = {zid.split("/", 1)[1]: pts for zid, pts in _GEOM["zones"].items()}
# OUTSIDE web/. The sheets are a deliverable for Caribbean Guard, not an asset of
# the map, and web/ is the folder a deployer drags into Cloudflare Pages whole.
# Left in there, four unsigned draft sheets carrying a SIN FIRMAR band would be
# published to the open internet by the deploy step, silently, as a side effect
# of shipping the map. A safety document nobody has reviewed must not reach the
# public by accident.
OUT = ROOT / "out" / "sheets"
Z, TS = 17, 256

# WHICH ZONES SHARE A SHEET. Salsa Brava is 560 m of coast; on its own it made a
# 562 px sheet that the text panel ate whole. Daniel's call was to fold it into
# Cocles rather than invent a minimum width, which is also how the two read on
# foot: one continuous stretch of Puerto Viejo shore with a reef break at the
# west end. A merged sheet draws each zone's own line and its own instruction.
SHEETS = {
    "playa-negra": ["playa-negra"],
    "cocles":      ["salsa-brava", "cocles"],
    "chiquita":    ["chiquita"],
    "punta-uva":   ["punta-uva"],
}


# ---------------------------------------------------------------- projection
def deg2tile(lat, lon, z=Z):
    n = 2 ** z
    return ((lon + 180.0) / 360.0 * n,
            (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n)


TILES = ROOT / "web" / "tiles" / str(Z)


def tile_bounds():
    """Extent of the z17 imagery, read from web/tiles/ rather than tools/tilecache.

    It used to read the cache and die with "run tools/georef2.py first" when that
    was absent, which is every clean clone, and the script it named reads an
    absolute path into a Downloads folder at a file not in the repository. So the
    sheets were unbuildable by anyone but the machine they were written on, and
    the error pointed at a dead end.

    web/tiles/ is the right source anyway: it is what `build_tiles.py` produces,
    what the map serves, and therefore the same pixels a reader sees. One
    command, `python tools/build_tiles.py`, now makes both the map and the sheets
    possible from a fresh checkout.
    """
    if not TILES.is_dir():
        raise SystemExit("no imagery; run: python tools/build_tiles.py")
    xs = sorted(int(d.name) for d in TILES.iterdir() if d.is_dir())
    ys = sorted(int(f.stem) for d in TILES.iterdir() if d.is_dir()
                for f in d.glob("*.jpg"))
    if not xs or not ys:
        raise SystemExit("no imagery; run: python tools/build_tiles.py")
    return xs[0], ys[0], xs[-1], ys[-1]


TX0, TY0, TX1, TY1 = tile_bounds()
MPP = 156543.03392 * math.cos(math.radians(9.645)) / (2 ** Z)


def to_px(lat, lon):
    """Mosaic pixel, with the cache's north-west tile as the origin."""
    x, y = deg2tile(lat, lon)
    return (x - TX0) * TS, (y - TY0) * TS


def mosaic(x0, y0, x1, y1):
    """Paste only the tiles the crop needs, rather than the whole 14336x6912."""
    tx_a, tx_b = TX0 + x0 // TS, TX0 + (x1 - 1) // TS
    ty_a, ty_b = TY0 + y0 // TS, TY0 + (y1 - 1) // TS
    img = Image.new("RGB", ((tx_b - tx_a + 1) * TS, (ty_b - ty_a + 1) * TS), (8, 14, 20))
    for tx in range(tx_a, tx_b + 1):
        for ty in range(ty_a, ty_b + 1):
            p = TILES / str(tx) / f"{ty}.jpg"
            if p.exists():
                try:
                    img.paste(Image.open(p).convert("RGB"),
                              ((tx - tx_a) * TS, (ty - ty_a) * TS))
                except Exception:
                    pass
    ox, oy = (tx_a - TX0) * TS, (ty_a - TY0) * TS
    return img.crop((x0 - ox, y0 - oy, x1 - ox, y1 - oy))


# ------------------------------------------------------------------ the zones
# Parsed out of web/index.html rather than duplicated. The schema was frozen on
# 2026-08-06 and copying it here would let the sheet and the map drift apart,
# which is the one failure a dated provenance record cannot survive.
def load_zones():
    src = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    block = src[src.index("const ZONES = ["):]
    block = block[: block.index("\n];") + 3]
    zones = {}
    for chunk in re.split(r"\n  \{\n", block)[1:]:
        zid = re.search(r'id:"([^"]+)"', chunk).group(1)
        reviewed = re.search(r"reviewed:(null|\"[^\"]*\")", chunk).group(1)
        caveat = re.search(r'caveats:\[\{es:"([^"]+)"', chunk)
        local = zid.split("/")[-1]
        caveat_en = re.search(r'caveats:\[\{es:"[^"]+",\s*\n?\s*en:"([^"]+)"', chunk)
        zones[local] = dict(
            id=zid, local=local,
            name=re.search(r'name:\{es:"([^"]+)"', chunk).group(1),
            sub=re.search(r'sub:\{es:"([^"]+)"', chunk).group(1),
            sub_en=re.search(r'sub:\{es:"[^"]+",\s*en:"([^"]+)"', chunk).group(1),
            klass=re.search(r'class:"([^"]+)"', chunk).group(1),
            authored=re.search(r'authored:"([^"]+)"', chunk).group(1),
            reviewed=None if reviewed == "null" else reviewed.strip('"'),
            why=re.search(r'why:\{es:"([^"]+)"', chunk).group(1),
            why_en=re.search(r'why:\{es:"[^"]+",\s*\n?\s*en:"([^"]+)"', chunk).group(1),
            caveat=caveat.group(1) if caveat else None,
            caveat_en=caveat_en.group(1) if caveat_en else None,
        )
    return zones


# ------------------------------------------------------------ visual language
# Colours follow Caribbean Guard's own sheet where it has an opinion: red dashed
# rips, orange hexagon stations, a bilingual legend boxed in the top right. The
# tier colours are the map's, measured for sun-washed phone screens.
TIER = {
    "no-swim":     ((229, 57, 53),  "NO ENTRES AL AGUA",      "DO NOT ENTER THE WATER"),
    "high-risk":   ((229, 57, 53),  "SOLO CON GUARDAVIDAS",   "ONLY WITH LIFEGUARDS"),
    "conditional": ((251, 140, 0),  "REVISA ANTES DE ENTRAR", "CHECK BEFORE YOU ENTER"),
    "lower-risk":  ((67, 160, 71),  "TEN CUIDADO IGUAL",      "TAKE CARE ANYWAY"),
}
RIP = (229, 57, 53)
STATION = (245, 150, 30)
UNSIGNED = (255, 82, 82)
INK = (255, 255, 255)
PANEL = (12, 22, 30)

DEFER_ES = ("Si hay un guardavidas o una bandera en la playa, eso manda sobre este mapa. "
            "Este mapa no ve el mar de hoy.")
DEFER_EN = ("If there is a lifeguard or a flag on the beach, that overrides this map. "
            "This map cannot see today's sea.")
UNSIGNED_ES = "SIN FIRMAR  ·  nadie de Caribbean Guard ha revisado esta hoja"
UNSIGNED_EN = "UNSIGNED  ·  nobody at Caribbean Guard has reviewed this sheet"

FONTS = Path("C:/Windows/Fonts")
font = lambda name, size: ImageFont.truetype(str(FONTS / name), size)


def wrap(d, text, f, width):
    out, line = [], ""
    for word in text.split():
        probe = (line + " " + word).strip()
        if d.textlength(probe, font=f) <= width:
            line = probe
        else:
            out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def fit(d, text, name, size, width):
    """Largest size at or below `size` keeping `text` inside `width`.

    The instruction is the one string on the sheet that may not be truncated or
    wrapped, so the type gives way to it rather than the other way round.
    """
    while size > 12:
        f = font(name, size)
        if d.textlength(text, font=f) <= width:
            return f
        size -= 1
    return font(name, 12)


def dashed(d, a, b, colour, width, dash=14, gap=10):
    (x1, y1), (x2, y2) = a, b
    total = math.hypot(x2 - x1, y2 - y1)
    if total == 0:
        return
    ux, uy = (x2 - x1) / total, (y2 - y1) / total
    t = 0.0
    while t < total:
        e = min(t + dash, total)
        d.line([x1 + ux * t, y1 + uy * t, x1 + ux * e, y1 + uy * e], fill=colour, width=width)
        t = e + gap


def dashed_path(d, pts, colour, width, dash=26, gap=12):
    """Dash along a whole polyline, carrying the phase across vertices.

    Dashing segment by segment restarts the pattern at every point, and the
    coastline's points are 8 m apart, so each segment is shorter than one dash
    and the line comes out solid. The phase has to survive the vertex.
    """
    phase = 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        seg = math.hypot(x2 - x1, y2 - y1)
        if seg == 0:
            continue
        ux, uy = (x2 - x1) / seg, (y2 - y1) / seg
        t = 0.0
        while t < seg:
            cycle = phase % (dash + gap)
            if cycle < dash:
                e = min(t + (dash - cycle), seg)
                d.line([x1 + ux * t, y1 + uy * t, x1 + ux * e, y1 + uy * e],
                       fill=colour, width=width)
            else:
                e = min(t + (dash + gap - cycle), seg)
            phase += e - t
            t = e


def arrowhead(d, tip, ux, uy, colour, size):
    px, py = -uy, ux
    d.polygon([
        tip,
        (tip[0] - ux * size + px * size * 0.5, tip[1] - uy * size + py * size * 0.5),
        (tip[0] - ux * size - px * size * 0.5, tip[1] - uy * size - py * size * 0.5),
    ], fill=colour)


def hexagon(d, cx, cy, r, fill, outline, width):
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
           for a in range(0, 360, 60)]
    d.polygon(pts, fill=fill, outline=outline)
    d.line(pts + [pts[0]], fill=outline, width=width)


# ---------------------------------------------------------------------- sheet
MARGIN_M = 160
ASPECT = 2.45        # Caribbean Guard's own sheet is 2500 x 1013


def render(sheet_id, members, zones):
    pts_all = [p for z in members for p in COAST[z]]
    xs = [to_px(la, lo)[0] for la, lo in pts_all]
    ys = [to_px(la, lo)[1] for la, lo in pts_all]
    pad = MARGIN_M / MPP
    x0, x1 = int(min(xs) - pad), int(max(xs) + pad)
    w = x1 - x0
    h = int(w / ASPECT)
    # Centre on the waterline, then pull north: the water is the subject, and a
    # sheet framed on the mean latitude spends half its height on jungle.
    cy = (min(ys) + max(ys)) / 2
    y0 = int(cy - h * 0.42)

    sheet = mosaic(x0, y0, x1, y0 + h).convert("RGBA")
    d = ImageDraw.Draw(sheet, "RGBA")
    P = lambda la, lo: (to_px(la, lo)[0] - x0, to_px(la, lo)[1] - y0)

    # -- each zone's waterline ---------------------------------------------
    # Dashed, not solid: the trace is good to a few metres but the line marks a
    # zone boundary, which is a judgement about where one beach ends, not a
    # surveyed edge. A solid line would claim more than anyone has established.
    for z in members:
        colour = TIER[zones[z]["klass"]][0]
        line = [P(la, lo) for la, lo in COAST[z]]
        dashed_path(d, line, (0, 0, 0, 150), 11)
        dashed_path(d, line, colour, 6)

    # -- hazards and panels are drawn below; naming happens last -----------

    # -- Caribbean Guard's own marks, only where they exist -----------------
    rips = stations = 0
    for f in HAZARDS["features"]:
        g, kind = f["geometry"], f["properties"]["kind"]
        if kind == "rip_current":
            c = [P(la, lo) for lo, la in g["coordinates"]]
            if not (0 < c[0][0] < sheet.width and 0 < c[0][1] < sheet.height):
                continue
            rips += 1
            for a, b in zip(c, c[1:]):
                dashed(d, a, b, (0, 0, 0, 130), 9, dash=11, gap=8)
                dashed(d, a, b, RIP, 4, dash=11, gap=8)
            # Head scaled to the rip it terminates. Caribbean Guard's rips run
            # 38 to 66 m, which is 32 to 56 px at 1.18 m/px, so a fixed head was
            # longer than the current it marked on the shortest ones.
            (ax, ay), (bx, by) = c[-2], c[-1]
            ln = math.hypot(bx - ax, by - ay) or 1
            span = math.hypot(c[-1][0] - c[0][0], c[-1][1] - c[0][1])
            arrowhead(d, (bx, by), (bx - ax) / ln, (by - ay) / ln, RIP,
                      max(11, min(24, span * 0.32)))
        elif kind == "rescue_station":
            lo, la = g["coordinates"]
            cx, cyy = P(la, lo)
            if not (0 < cx < sheet.width and 0 < cyy < sheet.height):
                continue
            stations += 1
            hexagon(d, cx, cyy, 16, STATION, (30, 20, 10), 3)

    coast_px = {z: [P(la, lo) for la, lo in COAST[z]] for z in members}
    sides = panel_sides(members, coast_px, sheet.width, sheet.height,
                        560, 28, len(members))
    boxes = draw_panels(d, sheet, [zones[z] for z in members], rips, stations, sides)
    if len(members) > 1:
        name_lines(d, sheet, members, zones, coast_px, boxes)

    # parents=True: out/ does not exist on a clean clone, and mkdir without it
    # fails with a bare WinError 3 that reads like a broken path.
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{sheet_id}.png"
    sheet.convert("RGB").save(path)
    return path, sheet.size, rips, stations


def name_lines(d, sheet, members, zones, coast_px, boxes):
    """Say which line is which, on a sheet that carries more than one zone.

    Not decoration. Salsa Brava is `no-swim` and Cocles is `high-risk`, two
    classes that share the `high` tier and therefore the same red on purpose, so
    without naming there is nothing on the picture that says where one zone ends
    and the next begins.

    TWO WAYS TO NAME A LINE, and which one applies is a property of the geometry
    rather than a preference. A zone with shore clear of the text column gets a
    plate on the water. Salsa Brava has none: it is 560 m at the west end of the
    sheet and its entire line runs behind its own panel, so an earlier version
    silently drew nothing and left two identical red lines with one name between
    them. That zone gets a leader instead, a thin rule from its panel out to the
    nearest point of its own shore, so the panel does the naming and no new ink
    lands on the water.
    """
    fl = font("arialbd.ttf", 26)
    # A point is nameable if it is on the picture and under none of the panels.
    # Testing "right of my own panel" was wrong the moment a panel could sit on
    # the right edge: it pushed every candidate off the sheet.
    def blocked(p):
        for b in boxes.values():
            if b[0] - 30 < p[0] < b[2] + 30 and b[1] - 30 < p[1] < b[3] + 30:
                return True
        return False

    for z in members:
        colour = TIER[zones[z]["klass"]][0]
        pts = coast_px[z]
        box = boxes.get(z)
        clear = [p for p in pts
                 if 40 < p[0] < sheet.width - 40 and 100 < p[1] < sheet.height - 130
                 and not blocked(p)]

        if clear:
            mid = clear[len(clear) // 2]
            name = zones[z]["name"]
            tw = d.textlength(name, font=fl)
            bx, by = mid[0] - tw / 2 - 14, mid[1] - 58
            d.rounded_rectangle((bx, by, bx + tw + 28, by + 38), radius=8,
                                fill=(8, 16, 22, 216), outline=colour, width=2)
            d.text((bx + 14, by + 7), name, font=fl, fill=INK)
            continue

        # Leader: from the middle of the panel's right edge to the closest point
        # on this zone's shore. A dot lands on the shore rather than an arrowhead,
        # because an arrow on this sheet already means a rip current.
        #
        # THE TARGET HAS TO BE ON THE PICTURE. Pointing at a coordinate that is
        # off the top of the frame, or behind the panel the leader starts from,
        # draws a confident rule to nothing; the first version of this did
        # exactly that and ran a red line across the unsigned band to a dot on
        # the sheet edge. Better to name nothing than to point at nothing.
        if not box or not pts:
            continue
        # Leave from whichever edge of the panel faces the shore.
        cx = sum(p[0] for p in pts) / len(pts)
        ax = box[2] if cx > box[2] else box[0]
        ay = (box[1] + box[3]) / 2
        visible = [p for p in pts
                   if 40 < p[0] < sheet.width - 30
                   and 100 < p[1] < sheet.height - 130 and not blocked(p)]
        if not visible:
            continue
        tx, ty = min(visible, key=lambda p: (p[0] - ax) ** 2 + (p[1] - ay) ** 2)
        stub = 26 if ax == box[2] else -26
        d.line([ax, ay, ax + stub, ay], fill=(0, 0, 0, 170), width=6)
        d.line([ax, ay, ax + stub, ay], fill=colour, width=3)
        d.line([ax + stub, ay, tx, ty], fill=(0, 0, 0, 170), width=6)
        d.line([ax + stub, ay, tx, ty], fill=colour, width=3)
        d.ellipse((tx - 9, ty - 9, tx + 9, ty + 9), fill=(8, 16, 22, 230),
                  outline=colour, width=3)


def panel_sides(members, coast_px, sheet_w, sheet_h, pw, margin, n_panels):
    """Which edge ALL the text blocks sit on. One side for the sheet, not per zone.

    Left by default. It flips when a zone would otherwise have no visible shore
    at all, which on a merged sheet is a real case: Salsa Brava is 560 m at the
    west end, its shore runs x 136 to 164, and the panel column occupies x 28 to
    588. At 1.18 m/px a 560 m beach is 474 px against a 560 px panel, so no
    framing at native resolution clears it and the zone simply could not be named.

    Per-zone sides were tried first and do not work. Moving only Salsa Brava's
    panel right leaves Cocles' panel on the left, still covering Salsa Brava's
    shore: the column hides that zone regardless of whose text is in it. What
    matters is which EDGE the column occupies, so the choice has to be made once
    for the sheet.
    """
    left_col = (margin - 30, margin + pw + 30)
    right_col = (sheet_w - margin - pw - 30, sheet_w - margin + 30)

    def hidden(col):
        n = 0
        for pts in coast_px.values():
            vis = [p for p in pts
                   if 0 < p[0] < sheet_w and 100 < p[1] < sheet_h - 130
                   and not (col[0] < p[0] < col[1])]
            if not vis:
                n += 1
        return n

    side = "left" if hidden(left_col) <= hidden(right_col) else "right"
    return {z: side for z in members}


def draw_panels(d, sheet, members, rips, stations, sides=None):
    Wd, Ht = sheet.size
    f_name = font("arialbd.ttf", 34)
    f_sub = font("arial.ttf", 23)
    f_body = font("arial.ttf", 22)
    f_small = font("arial.ttf", 18)
    f_en_body = font("arial.ttf", 19)   # English rider under every Spanish block
    f_smb = font("arialbd.ttf", 18)
    f_band = font("arialbd.ttf", 20)

    pw, margin = 560, 28
    sides = sides or {}
    # One cursor per edge. Panels stack down their own side, so a zone moved to
    # the right does not leave a gap in the left column.
    ycur = {"left": 28, "right": 28}
    # The band belongs with the text, so it sits at the head of the panel column
    # wherever that column ended up. Leaving it pinned left while the panels moved
    # right stranded it under the legend.
    side0 = sides.get(members[0]["local"], "left") if members else "left"
    px = margin if side0 == "left" else sheet.size[0] - margin - pw
    y = ycur[side0]

    # -- unsigned band, above everything -----------------------------------
    # Daniel's call: an unsigned sheet must LOOK unsigned. It is also the ask to
    # Caribbean Guard, stated on the artefact itself: these are the beaches still
    # waiting for a guard to put their name to them.
    if all(m["reviewed"] is None for m in members):
        bh = 62
        fb = fit(d, UNSIGNED_ES, "arialbd.ttf", 20, pw - 36)
        fbe = fit(d, UNSIGNED_EN, "arial.ttf", 18, pw - 36)
        d.rounded_rectangle((px, y, px + pw, y + bh), radius=10,
                            fill=(60, 12, 12, 240), outline=UNSIGNED, width=3)
        d.text((px + 18, y + 10), UNSIGNED_ES, font=fb, fill=UNSIGNED)
        d.text((px + 18, y + 36), UNSIGNED_EN, font=fbe, fill=(255, 176, 176))
        ycur[side0] = y + bh + 14

    boxes = {}
    for m in members:
        side = sides.get(m["local"], "left")
        px = margin if side == "left" else sheet.size[0] - margin - pw
        y = ycur[side]
        colour, es_word, en_word = TIER[m["klass"]]
        f_word = fit(d, es_word, "arialbd.ttf", 52, pw - 56)
        f_en = fit(d, en_word, "arial.ttf", 27, pw - 56)
        # ES then EN, every block. English is smaller and dimmer, never absent:
        # this coast's drownings are overwhelmingly visitors, and a sheet that
        # only speaks Spanish cannot instruct the people most likely to need it.
        # Spanish stays primary because it is the community's language and
        # Caribbean Guard's own.
        why = wrap(d, m["why"], f_body, pw - 48)
        why_en = wrap(d, m["why_en"], f_en_body, pw - 48)
        cav = wrap(d, m["caveat"], f_body, pw - 66) if m["caveat"] else []
        cav_en = wrap(d, m["caveat_en"], f_en_body, pw - 66) if m["caveat_en"] else []
        ph = (24 + 42 + 26 + 44 + (f_word.size + 8) + 42
              + len(why) * 28 + 6 + len(why_en) * 24
              + (14 + len(cav) * 28 + 4 + len(cav_en) * 24 if cav else 0) + 104)

        d.rounded_rectangle((px, y, px + pw, y + ph), radius=14, fill=PANEL + (232,))
        d.rectangle((px, y, px + 10, y + ph), fill=colour)

        yy = y + 24
        d.text((px + 28, yy), m["name"], font=f_name, fill=INK)
        yy += 42
        d.text((px + 28, yy), m["sub"], font=f_sub, fill=(168, 186, 198))
        yy += 26
        d.text((px + 28, yy), m["sub_en"], font=f_en_body, fill=(120, 140, 154))
        yy += 44

        # The instruction. Never a colour name, never a rating. See rule 1.
        d.text((px + 28, yy), es_word, font=f_word, fill=colour)
        yy += f_word.size + 8
        d.text((px + 28, yy), en_word, font=f_en, fill=(196, 210, 220))
        yy += 42

        for ln in why:
            d.text((px + 28, yy), ln, font=f_body, fill=(226, 236, 242))
            yy += 28
        yy += 6
        for ln in why_en:
            d.text((px + 28, yy), ln, font=f_en_body, fill=(148, 166, 180))
            yy += 24

        if cav:
            yy += 14
            bar = yy
            for ln in cav:
                d.text((px + 46, yy), ln, font=f_body, fill=(255, 214, 150))
                yy += 28
            yy += 4
            for ln in cav_en:
                d.text((px + 46, yy), ln, font=f_en_body, fill=(196, 160, 110))
                yy += 24
            d.rectangle((px + 28, bar, px + 32, yy), fill=(251, 140, 0))

        # -- provenance, the part that may never be dropped -----------------
        yy += 18
        d.line((px + 28, yy, px + pw - 28, yy), fill=(60, 78, 92), width=1)
        yy += 14
        authored = {"desk": "escrito desde conocimiento general, sin visita al sitio",
                    "sheet": "leído del mapa anotado de Caribbean Guard, sin fecha",
                    "field": "levantado en el sitio"}[m["authored"]]
        d.text((px + 28, yy), "Autor", font=f_smb, fill=(138, 158, 172))
        d.text((px + 98, yy), authored, font=f_small, fill=(196, 210, 220))
        yy += 26
        d.text((px + 28, yy), "Revisado", font=f_smb, fill=(138, 158, 172))
        d.text((px + 118, yy), m["reviewed"] or "nadie todavía", font=f_small,
               fill=(196, 210, 220) if m["reviewed"] else UNSIGNED)
        boxes[m["local"]] = (px, y, px + pw, y + ph)
        ycur[side] = y + ph + 16

    # -- the deferral, across the foot of the sheet -------------------------
    # Rendered under every character, not only the lowest one. Phrased
    # conditionally on purpose: a red flag SYSTEM on this coast is unconfirmed.
    fh = 96
    d.rectangle((0, Ht - fh, Wd, Ht), fill=(8, 16, 22, 230))
    d.text((28, Ht - fh + 20), DEFER_ES, font=f_body, fill=(255, 236, 190))
    d.text((28, Ht - fh + 54), DEFER_EN, font=f_small, fill=(170, 188, 200))

    # -- legend, top right, following their sheet ---------------------------
    rows = [("zone", "Límite de la zona / Zone extent")]
    if rips:
        rows.append(("rip", f"Corriente de resaca ({rips}) / Rip current"))
    if stations:
        rows.append(("station", f"Estación de rescate ({stations}) / Rescue station"))
    note = "Posición de Caribbean Guard. La dirección es indicativa."
    legend_colour = TIER[members[0]["klass"]][0]

    lw = int(max([d.textlength(t, font=f_small) + 100 for _, t in rows]
                 + [d.textlength(note, font=f_small) + 40]))
    lh = 18 + 32 * len(rows) + 28
    # The legend lives top right, unless the panel column does. Drawing both
    # there put the legend straight over the Salsa Brava heading.
    on_right = any(b[0] > Wd / 2 for b in boxes.values()) if boxes else False
    lx = 28 if on_right else Wd - lw - 28
    ly = 28
    d.rounded_rectangle((lx, ly, lx + lw, ly + lh), radius=12, fill=PANEL + (226,))
    yy = ly + 18
    for kind, text in rows:
        if kind == "zone":
            d.line((lx + 20, yy + 10, lx + 66, yy + 10), fill=legend_colour, width=6)
        elif kind == "rip":
            dashed(d, (lx + 20, yy + 10), (lx + 56, yy + 10), RIP, 4, dash=9, gap=6)
            arrowhead(d, (lx + 66, yy + 10), 1, 0, RIP, 15)
        else:
            hexagon(d, lx + 38, yy + 10, 11, STATION, (30, 20, 10), 2)
        d.text((lx + 82, yy), text, font=f_small, fill=INK)
        yy += 32
    d.text((lx + 20, yy - 2), note, font=f_small, fill=(150, 168, 182))
    return boxes


def main():
    zones = load_zones()
    want = sys.argv[1:] or list(SHEETS)
    for sid in want:
        if sid not in SHEETS:
            sys.exit(f"unknown sheet {sid!r}; have: {', '.join(SHEETS)}")
        path, size, rips, stations = render(sid, SHEETS[sid], zones)
        who = " + ".join(SHEETS[sid])
        print(f"{path.name:18} {size[0]}x{size[1]}  {who}  rips={rips} stations={stations}")


if __name__ == "__main__":
    main()
