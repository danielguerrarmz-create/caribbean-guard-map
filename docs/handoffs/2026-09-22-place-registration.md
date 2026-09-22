# Place registration handoff, 22 September 2026

## What changed

All 64 PDF location marks were audited. Twenty-five unambiguous OpenStreetMap matches now use fixed mapped coordinates. Thirty-nine remain estimated from the source PDF using those matches and four station controls. One coincident duplicate is hidden from the UI but retained in the audit. Small map popups show a name and one short status line. Place buttons expose meaningful names. Desktop safety guidance spacing, weather order, and rip-arrow shafts were corrected.

## Why

The original PDF has no GPS coordinate system, and its generic affine placement visibly displaced place markers. Name-only matching can also be wrong, so uncertain and generic labels remain marked as estimates.

## How to verify

Run `python -X utf8 tools/project_full_annotations.py`, `python -X utf8 tools/write_place_audit.py`, `npm run check:map`, and `npm run build:map`. Inspect `docs/data/place-marker-audit.csv`; each fixed row links to its OSM feature. In the local preview, zoom into Cocles and Manzanillo to inspect named place popups, toggle layers in the legend, and open a beach sheet on desktop and mobile.

## What's left

Confirm the 39 estimated PDF marks with local ground evidence before using them for directions or operations. OSM coordinates and footprint centers may themselves be stale or unsuitable as entrances. The current map remains illustrative, not rescue-dispatch data.

## Files touched in this change

`tools/project_full_annotations.py`, `tools/resolve_osm_places.py`, `tools/audit_place_matches.py`, `tools/write_place_audit.py`, `tools/data/*`, `web/data/full-map-geographic.geojson`, `web/index.html`, `web/coastal.css`, `web/geometry.js`, `web/sw.js`, `docs/data/place-marker-audit.csv`, and `docs/design/2026-09-22-place-audit-and-walkthroughs.md`.
