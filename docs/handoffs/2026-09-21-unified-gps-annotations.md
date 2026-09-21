# Unified GPS annotations, 2026-09-21

## What changed

- Kept the existing satellite GPS map as the single interface map and replaced the annotated/GPS view switch with five annotation layer controls in the permanent legend.
- Projected 315 PDF features into `web/data/full-map-geographic.geojson` using the four rescue-equipment numbers shared with the existing GPS data. Existing GPS positions for those four stations and the strong-current area are preserved.
- Reduced overview marker size, hid document roads and places until zoom 15, and identified projected positions as approximate in the legend and popups. The source document page is no longer linked or packaged offline.
- Preserved the concurrent global panel revisions: compact two-line beach entries, circular symbols, always-visible coastal forecast, and shared detail spacing.
- Adjusted source roads, footpaths and place markers with a smooth local offset using four named OpenStreetMap place controls across the coast, while keeping the four existing GPS station positions fixed. Hazard and equipment annotations retain their earlier station-based fit.
- Drew all rip arrows through one shared curved-shaft component with a solid arrowhead. Added a little vertical space to every beach entry and removed the duplicate title inside the coastal forecast card.
- Made the map key a compact pill that expands to the full legend and layer controls. Reorganized the key's spacing and grouped the sea-model time with its Open-Meteo attribution on a second line below the coast-wide scope note.
- Removed the obsolete, separately reachable document-coordinate viewer and its deploy image from `web/`; source extraction JSON and the projection script remain available for audit and regeneration.

## Why

The document and satellite map showed the same coast in incompatible coordinate systems. One GPS map lets readers compare the document marks with the coast and control their display in one place.

PR #2 is stacked on PR #1 (`feat/ui-overhaul`). It is a code review of the local map work, not a deployment or field-safety release. The unrelated generated `docs/handoffs/2026-09-17-auto.md` working-tree edit is excluded.

## How to verify

1. Open `http://127.0.0.1:5174/`. There should be one map, with the satellite image behind beach zones and PDF markers.
2. Toggle each document layer in the upper-right legend. Turning proposals off removes the dashed proposal symbols; turning it on restores them. Zoom in to see source roads and place markers.
3. Open a projected marker. Its popup must say the GPS alignment is provisional and must not offer directions to proposed equipment.
4. At zoom 15 or above, compare the road and place layer to named landmarks from Playa Negra through Manzanillo. Check that arrowheads are filled, beach entries have even padding, and the forecast has one heading.
5. Run `python tools/project_full_annotations.py`, `npm run check:map`, and `npm run build:map` from the repository root.

## What remains

The four station controls span only the Chiquita area. Their fit residuals are 1.4 to 9.2 metres, but this is not independent accuracy. The access/place adjustment uses Banana Azul, Rocking J's, Congo Bongo and Maxi's as manual controls from OpenStreetMap/Nominatim (© OpenStreetMap contributors, ODbL); fitting those points does not validate other roads or places. The previously tested Aguas Claras place remains about 55 metres north of the OSM point. The earlier background-image matching attempt failed holdout validation. Obtain independent road and landmark checks, plus field confirmation of hazards/equipment, before treating PDF-derived GPS positions as precise or using them for navigation or rescue dispatch. Source roads do not establish access rights.

## Files touched

`web/index.html`, `web/coastal.css`, `web/geometry.js`, `web/sw.js`, `web/data/full-map-geographic.geojson`, `tools/project_full_annotations.py`, and `docs/design/icon-system-and-source-review.md`. PR cleanup also updates `README.md`, `docs/deploy.md`, `tools/build_map.js`, `tools/extract_full_map.py`, `web/_headers` and `web/vercel.json`, and removes `web/source-map.html`, `web/source-map.js` and `web/data/full-map-background.jpg` from the deploy folder.
