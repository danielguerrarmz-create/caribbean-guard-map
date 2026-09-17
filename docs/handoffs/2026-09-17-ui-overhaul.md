# Caribbean Guard map, 2026-09-17: the UI overhaul

Branch `feat/ui-overhaul`, commit `6be0f66`, **PR #1** on the public repo. One session,
orchestrated: a five-hat user study, a signed-off spec, two builders on disjoint files,
one QA gate pinned to a frozen file hash. Nothing is in production.

**Preview:** https://caribbean-guard-qnvlqchx9-danielguerrarmz-create11.vercel.app
**Deploy gotcha:** from `web/`, a bare `vercel` returns "Not authorized" even though
`vercel whoami` is fine. Every deploy needs the team scope:
`vercel deploy --yes --scope team_XOr1KdFeEvqhDcHZMsmeoLA6` (add `--prod` to publish).

## What

- **User study.** Five reviewers with different hats (tourist scanning a QR at
  Cocles, local parent in Spanish, the CG lifeguard who drew the V5 sheet, a
  deuteranope on a budget Android over slow 3G, AJ and the board). 55 findings.
  All five kept the same three things: instruction words, the deferral sentence,
  provenance printed under the verdict.
- **Layout.** Phone: bottom dock with one instruction-first card in view, a "1 of 6"
  counter and edge fade, a Legend chip, a first-run "¿En qué playa estoy?" action.
  Beach sheet with three stops (33 / 70 / 100 vh), instruction first, TODAY
  collapsed to one line, provenance directly under the verdict, escape sentence on
  every beach, deferral boxed, actions row. Desktop (>= 820 px): left rail with all
  six cards and a permanent bilingual legend, right column panel that never covers
  the coast.
- **Visual language.** Atkinson Hyperlegible, self-hosted, two weights, in
  `web/fonts/`. Scale 22 / 18 / 15 / 13 / 12; nothing under 12 px. Instruction text
  is always ink; the tier lives in the swatch (colour + dash + weight) and the pill's
  left bar. Two pill kinds only: status pill and provenance chip. Rescue stations
  are V5 orange hexagons; below zoom 15 the four collapse into one "×4" badge.
- **Legend.** Merged: our four tiers under "Qué hacer", CG's V5 vocabulary under
  "En el mapa" (Corriente de Resaca, Estación de Rescate, the undefined marked
  area, your location). ES and EN side by side like the V5 sheet.
- **Linework.** The five nine-point `line:` arrays are gone. `tools/export_zones.py`
  reads `tools/coastline.json` (8 m step), simplifies at 0.5 m, Chaikin twice, and
  writes `web/data/zones-geometry.json` (160 to 917 points per zone, max deviation
  1.31 m from the trace). `web/geometry.js` (`window.CGGeom`) draws tapered ends
  (last 40 m ramp to 40 % weight), round joins, ratio-preserving dashes with a 3 px
  minimum gap, outlined rip arrows, and a label collision pass in which station
  markers win over place labels.
- **Tiles.** z10 and z11 added; the z12 to z15 boxes widened. The phone's navy
  landing was never a missing zoom level: `fitCoast()` floors at about 11.75 and
  requests z12, whose box was 22 km tall against a 36 km viewport. Edward also found
  that `flyTo` zooms out mid-flight and requests tiles neither endpoint shows, so
  the deep-link sweep (`tile_demand.py`, scratchpad) drove the box sizes. 129 tiles
  added, zero missing across five viewports. `sw.js` cache is `cg-map-v3`; CRITICAL
  is 165 entries at 2.07 MB including fonts, geometry and the document.
- **Content corrections.** The false "rescue post 600 m east" fact at Playa Negra
  is deleted (600 m east is Salsa Brava reef). The unconfirmed Cocles red-flag fact
  is deleted. Rip metres and the "perpendicular" bearing sentence are gone; the rip
  sheet now says position is CG's and direction is not drawn. One word for the
  current (resaca), one for the post (Estación de Rescate N). Rioplatense and
  peninsular words replaced: recorrer, reporte, agregar, baño; "IGUAL, TEN CUIDADO".
  Cocles shows "Guardavidas 9:00 a 17:00" and, off-hours by the device clock,
  "ahora sin guardavidas" in ink.
- **Accessibility.** Sheet is `hidden` + `inert` when closed, named by its h2, takes
  focus on open, closes on Escape, survives a language switch. One global
  `:focus-visible`. Every aria-label translated. Toast is `role="alert"` and stacks
  with the update banner instead of being covered by it. A failed geometry fetch
  fires the alert for 60 s, because a coast with no strokes reads as no hazards.
- **Guard.** `tools/check_copy.js` (run with `node`) fails on banned words in live
  copy, em or en dashes, any tier label that grants permission, or a sheet renderer
  missing the deferral. Mutation-tested: six injected faults each exit 1.

## Why the two rulings that did not change

- `SOLO CON GUARDAVIDAS` has no verb. QA flagged it; it stays. The 08-06 ruling
  accepted it as fail-safe: with no guard present it reads as "do not go in".
- `nadie todavía` renders amber (`--gap`, #7a4a00), not red, byte-identical to
  HEAD. **Daniel ruled 2026-09-17: amber stays**, absence is not a hazard colour.
  The printed sheets (`tools/render_annotated.py`) still use red and should follow.

## Verify

```
node tools/check_copy.js            # copy rules
python tools/export_zones.py        # regenerates zones-geometry.json byte-identically
python tools/build_tiles.py         # fills web/tiles/ and audits the precache
python -m http.server 5173 --directory web
```

Open http://127.0.0.1:5173/ at 390 x 844 and 1280 x 800. Imagery corner to corner
on both. Tap a card: sheet opens at the peek stop with the instruction visible.
Switch language with the sheet open: it stays open. `?z=chiquita`: no 404s, four
stations clustered as one badge, tap it to expand.

## Left, for Daniel and AJ (governance, not UI)

1. **TODAY has no way in.** Nobody can sign a bulletin without editing the source.
   Either a phone-sized signing surface for the guard on duty, or the axis stays a
   single line until one exists.
2. **Every beach is unreviewed** and the 365-day clock has no owner. One named guard
   signing all five before launch would prove the machinery.
3. **The address.** A QR sign is permanent; it must carry a caribbeanguard.org
   URL, not vercel.app, before anything is printed.
4. The **Ubicaciones layer** (V5's yellow stars with walking minutes) does not
   exist yet; the legend row appears only when it does.
5. The **red polygon** on V5 is still undefined; one call to whoever drew it.
6. **Share card** (`og:` tags, a drawn card.jpg) and a donate line: AJ's call.

## Files

- `web/index.html` — rewritten UI, content, a11y (3,587 lines)
- `web/geometry.js`, `web/data/zones-geometry.json`, `web/fonts/` — new
- `web/sw.js` — cg-map-v3, regenerated lists; `web/manifest.json`
- `tools/export_zones.py`, `tools/check_copy.js` — new; `tools/build_tiles.py`
- Session scratchpad: `SPEC.md`, `hats/`, `INTEGRATION.md`, `tile_demand.py`
