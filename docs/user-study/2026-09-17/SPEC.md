# Caribbean Guard map: UI overhaul spec (signed off by Daniel, 2026-09-17)

Repo: C:\Users\danie\caribbean-guard   Branch: feat/ui-overhaul (already checked out)
Local server: http://127.0.0.1:5173/ serves web/ (python http.server, already running; reload only)
User study: hats/hat-1..5-*.md next to this file. Read them; they are the evidence.
Reference look: shots/annotated-base-map-v5.png (CG's own hand-made map and legend).

## RULES THAT DO NOT MOVE (project doctrine, from memory and handoffs)
- Status words are instructions, never ratings, never permission. The four tiers stay:
  NO ENTRES AL AGUA / SOLO CON GUARDAVIDAS / REVISA ANTES DE ENTRAR / TEN CUIDADO IGUAL
  (Spanish fix below changes the last one to "IGUAL, TEN CUIDADO"; EN unchanged).
- Never claim more currency or authority than the data has. Author + Reviewed stay under the
  verdict. "nadie todavía" stays red. Unreviewed must look unreviewed at >= 12 px.
- Colour is never the only channel. Swatch = real stroke (colour + dash + weight) + the word.
- Spanish primary, tú register, Costa Rican Caribbean; English always present.
- Deferral sentence under every tier stays word for word.
- Offline-first: everything new must be precached by web/sw.js; bump CACHE to cg-map-v3.
- No build step: web/index.html stays a single hand-written file plus small sibling files.
  Keep the inline design commentary convention (explain why, in place).
- DO NOT COMMIT. The orchestrator commits. Do not touch files outside your workstream.

## DECISIONS TAKEN TODAY
- Legend = merged: our four tiers + CG's V5 vocabulary (Corriente de Resaca, Estación de
  Rescate, Ubicaciones; roads/paths listed only if a layer exists, otherwise omit).
- Font: Atkinson Hyperlegible, self-hosted WOFF2, Regular + Bold only, in web/fonts/.
  font-display: swap; system stack as fallback. Add to the sw precache.
- Green stays on the lowest tier stroke/swatch; the instruction TEXT is always ink (#0b1c2c),
  never tier-coloured.
- TODAY block collapses to ONE line under provenance: "Hoy: sin reporte firmado" /
  "Today: no signed report". Violet tag kept. Full block only renders when today != null.
- Content corrections (workstream B does these in the zone records):
  * Playa Negra: DELETE the "Puesto de rescate a 600 m al este" fact (it points at Salsa Brava).
  * Cocles: DELETE "Banderas rojas marcan los canales activos" (unconfirmed). Keep defer.
  * Rip sheet: drop ripLen metres and the "perpendicular a la playa" bearing sentence; say
    position is CG's, direction not drawn.
  * Vocabulary, everywhere: "corriente de resaca" (never retorno), "Estación de Rescate"
    (never salvamento), one name per post: "Estación de Rescate N".
  * Spanish: relevar/relevamiento -> "recorrer"/"tramo recorrido" ("Sin recorrer",
    "Fuera del tramo recorrido"); "parte" -> "reporte"; "Añadir" -> "Agregar";
    "TEN CUIDADO IGUAL" -> "IGUAL, TEN CUIDADO".
  * Cocles card shows the post hours next to the instruction: "Guardavidas 9:00 a 17:00";
    when the device clock is outside those hours append "ahora sin guardavidas" (ink, not red).
  * Rescue station markers: V5 ORANGE (#f39c12 family), hexagon like V5, not blue circles.
  * Every beach with rips gets the escape sentence in its facts: "Si una corriente te
    arrastra: no nades contra ella, flota, y nada paralelo a la playa hasta salir."
  * Add a "Reportar un error" mailto: line and a wordmark link to https://caribbeanguard.org
    in the sheet footer. Leave the donate line out (AJ's call).

## LAYOUT (phone first; desktop is min-width: 820px)
Phone
- Top bar: wordmark left (links home). Right: "911 Emergencia" pill 44 px, then ES|EN 44 px.
- Map fills the screen. Zoom floor: build z11 tiles (workstream A) so a 390 px phone lands
  on imagery, not navy.
- Locate: 52 px round button right edge above the dock. First run only: a full-width
  dock action "¿En qué playa estoy?" above the cards; after one use it becomes the icon.
- Dock (bottom): the "saved" bar shrinks to one 12 px line. Card strip: one card ~ 84vw,
  scroll-snap, edge fade both sides, a "2 de 6" counter, and when a deep link (?z=) opens
  the strip scrolls to that beach. The "rest of the coast" card is visually a different
  species (dashed border, no pill) and sits last.
- Card anatomy (top to bottom): name 15/800; instruction pill (18 px, uppercase, ink text,
  swatch on the left drawing the real stroke, tier colour as the pill's left bar not fill);
  provenance chips 12 px outline: "Sin revisar" / "Sin recorrer"; hours line for Cocles.
- Legend: a "Leyenda" chip at the left end of the dock opens a sheet: two sections,
  "Qué hacer" (4 tiers with swatches) and "En el mapa" (V5 marks), ES/EN two columns.
- Beach sheet: three stops. PEEK ~ 32vh: name, sub, instruction pill, provenance line.
  HALF 70vh, FULL 100vh minus safe area. Drag handle + swipe; close button 44 px;
  Escape closes; focus moves to the h2; aria-labelledby the h2; closed = hidden + inert.
  Order inside: name/sub -> instruction pill -> Autor / Revisado one line -> today line ->
  why -> facts (escape sentence for rip beaches) -> deferral (boxed) -> actions row:
  Cómo llegar, Reportar un error, 911.
  Language switch re-renders the open sheet in place, never closes it.
Desktop (>= 820)
- Left rail 360 px: title + one-line "qué es este mapa", then all six cards stacked, then
  the legend permanently open under them (V5 style, bilingual). Map fills the rest.
- Beach panel: right column 400 px, full height, never overlapping the coast.
- 911 shows the number as text; locate demoted to a small control.

## TYPE + SPACE + PILLS
- Atkinson Hyperlegible. Scale: 22 (sheet h2), 18 (instruction), 15 (names, body),
  13 (secondary), 12 (chips, floor). Line-height 1.3 body. Letter-spacing .02em uppercase.
- 8 px grid. 16 px gutters. Card padding 14/16. Sheet radius 20 (keep). Targets >= 44 px.
- Exactly two pill kinds: status pill (described above) and provenance chip (outline,
  neutral, icon + word). TODAY tag violet stays outside the hazard palette.
- One global :focus-visible outline (2 px, ink on light, white on map).
- Translate every aria-label in setLang; toast: role="alert" for assertive.
- Ship the six cards as static HTML so the first instruction paints before Leaflet parses.

## MAP LINEWORK (workstream A: tools/, web/data/, web/geometry.js, web/sw.js, tiles)
- Source: tools/coastline.json (8 m step, per zone). Replace the 9-point `line:` arrays.
- Smooth: Chaikin 2 passes after a 0.5 m simplify; round joins and caps.
- Ends: taper the last 40 m (weight ramps to 40%) so no blunt cut-offs; the halo tapers too.
- Stroke: keep ground-based sizing, but dashes scale by RATIO (keep 1:4 for low, 1.6:1
  moderate) and never floor below a 3 px gap; minimum weight 2 px, halo = weight * 1.6.
- Arrows: 1.5 px dark outline (#0b1c2c at .85) under the red so they hold 3:1 over water.
- Labels: collision avoidance so "PUERTO VIEJO" and "Playa Cocles" never touch; place
  labels are hidden when they would collide with a zone label.
- Tiles: add z11 (and z10 if cheap) to tools/build_tiles.py; regenerate sw.js lists;
  CACHE -> cg-map-v3.

## ACCEPTANCE (Gojo verifies)
- 390x844 and 1280x800 screenshots: imagery corner to corner at landing on both.
- No text under 12 px; instruction is the largest text on every card.
- Deuteranope simulation: the three tiers are distinguishable by dash pattern at z12 and z17.
- Sheet: opens at PEEK with instruction visible without scrolling; language switch keeps it.
- Every rule assertion in the existing tests (no permission labels, every label has a verb)
  still passes; grep for "retorno", "salvamento", "relevar", "parte hoy", "600 m" returns 0.
- Offline: after first load, airplane mode reload still shows cards, font, legend and z11-13.
