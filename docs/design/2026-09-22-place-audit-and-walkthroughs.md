# Place placement and three walkthroughs, 22 September 2026

## Placement decision

The PDF supplies 64 location marks without a geographic CRS. I compared every label and its provisional position with a bounded OpenStreetMap named-feature extract. The [marker audit](../data/place-marker-audit.csv) records the outcome for all 64, including the exact OSM feature URL for each fixed mark. Twenty-five distinctive names have a nearby, credible OSM record and now use that record's mapped coordinate or feature center. The remaining 39 marks retain an estimated position based on their PDF coordinates, the 25 fixed places, and the four existing station controls. The coincident duplicate mark 408 is retained in the audit but hidden in the UI.

Generic or incomplete PDF text such as “1 minuto,” “Hotel,” and “Centro” is shown as “Unidentified place.” “Salsa Brava” and “Bungalows” were left estimated because multiple interpretations could refer to different sites. A location without a source match is never described as fixed. OSM records can be stale and polygon centers are not surveyed entrances. The placement is for visual context, not navigation or rescue dispatch.

Sources: [OpenStreetMap API and ODbL attribution](https://www.openstreetmap.org/copyright), the [Overpass named-feature extract](https://wiki.openstreetmap.org/wiki/Overpass_API) queried for the project's coastal bounding box on this date, and the supplied `08102026_FULL MAP DRAFT.pdf`. The reproducible input is `tools/data/osm-place-candidates.json`; reviewed matches are `tools/data/place-matches.json`.

## Walkthrough 1: local resident

Path: open the coast list, choose Playa Negra, read safety guidance, inspect the map and directions action, then return to the list. The guidance and 911 link were readable, but an unnecessary vertical gap split the lower-risk caveat from the rip-current instruction on desktop. I moved the flexible space below the content and kept the site link at the bottom. I did not activate the emergency or external directions links.

## Walkthrough 2: tourist

Path: choose Playa Cocles, compare the beach status with the map, expand the sheet at a 390 × 844 mobile viewport, inspect regional weather, and switch to Spanish and back. The safety action, rip-current instruction, source caveat, and weather were legible. The desktop layout could place weather ahead of the rip-current instruction when space allowed; it now keeps safety guidance first. Both language versions and the mobile expansion worked. At detailed zoom, the dashed rip shafts looked fragmented against nearby annotations; I made them solid while preserving the outlined shaft and solid direction head.

## Walkthrough 3: Caribbean Guard member

Path: expand the legend, hide and restore proposals, inspect a proposed-equipment popup and an undefined-symbol popup, and review place-marker labels. Layer toggles responded correctly and the proposal popup still says “not available.” The popups repeated a long source disclaimer; they now show a short title and status, with provenance in the legend. Every place marker now exposes its actual display name to assistive technology where known; incomplete names use “Unidentified place.”

## Verification and follow-up

`npm run check:map`, `npm run build:map`, `node --check web/geometry.js`, and `git diff --check` passed. Desktop and mobile previews were inspected. Source-backed place coordinates remain map records rather than field-surveyed points, and the 39 estimated marks need ground confirmation before they can be used for directions or operations.
