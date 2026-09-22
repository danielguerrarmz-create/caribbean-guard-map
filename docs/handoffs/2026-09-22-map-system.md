# GPS map and coastal interface handoff

## What changed

The 53 headed rip-current arrows were re-registered to the GPS shoreline while retaining the source document's direction. Six red context strokes without heads are excluded, and twelve reverse-ordered source shafts are corrected. The selected beach band now begins at the shoreline. Arrows use restrained cubic shafts, wider open chevrons, and reduced-motion-aware whole-arrow fading. The overview withholds detailed hazard arrows and small points. The map legend now contains annotation layers only. Shared pictograms, beach guidance card, forecast, road linework, and desktop spacing were refined. Guidance cards have a neutral border on every beach.

## Why

The source PDF has document coordinates, not a geographic CRS. Its original arrow endpoints visibly missed the GPS coastline. The previous legend duplicated the beach list, and at a 720 px desktop height the forecast displaced the last beach. The new hierarchy keeps safety words legible while showing only context-appropriate map detail.

## How to verify

Run `python -X utf8 tools/project_full_annotations.py`, `python -X utf8 tools/audit_rip_registration.py`, `npm run check:map`, and `npm run build:map`. In the local preview, scan the 1280 × 720 overview, select Playa Cocles, zoom toward the shore to see the arrows, expand Map layers, toggle Rip currents, and inspect the 390 × 844 mobile view. The [design walkthrough](../design/2026-09-22-map-system-walkthrough.md) records three role paths and observed fixes.

## What's left

Registration is approximate. A qualified local review should confirm the mapped current positions, beach segments, and any operational use. Neither the arrow animation nor the forecast reports live current presence.

## Files touched

`tools/extract_full_map.py`, `tools/project_full_annotations.py`, `tools/audit_rip_registration.py`, `web/data/full-map-source.json`, `web/data/full-map-geographic.geojson`, `web/geometry.js`, `web/index.html`, `web/symbols.js`, `web/coastal.css`, `web/sw.js`, and this documentation. The working tree also contains earlier uncommitted place/road registration changes that should be reviewed as one local package; the unrelated `docs/handoffs/2026-09-17-auto.md` change was not part of this task.
