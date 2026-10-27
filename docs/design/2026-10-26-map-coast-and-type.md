# Coastal map linework and type system

Date: 2026-10-26
Status: Review branch; no merge or production deployment.

## Coast display

The older browser-side coastal band offset folded over itself at bends. Its Salsa Brava, Cocles, Chiquita, and Punta Uva polygons were invalid or self-intersecting. The replacement in `web/data/coast-bands.geojson` buffers the complete seven-stretch shoreline once, then divides the continuous corridor at beach joints. `tools/build_coast_bands.py` regenerates it with Shapely 2.x. The five assessed beaches retain their existing tier colors; Playa Grande and Manzanillo remain neutral because they are unassessed. The narrow safety stroke stays above the fill, and the separate strong-current area is unchanged.

The generated linework has no self-intersections, overlapping band polygons, or joint gaps. That is a geometry check, not field verification of the shoreline or a rendered visual signoff. See the map's existing source and copy checks for hazard provenance.

## Font hierarchy

The approved pairing is **Zilla Slab + Source Sans 3**, both self-hosted under the SIL Open Font License. The raster logo remains unchanged.

| Role | Family and weight | Map use |
| --- | --- | --- |
| Identity and coast title | Zilla Slab 700 | Wordmark and coast heading; the rail heading scales from 32 px on desktop to about 20 px on phones |
| Beach sheet title | Zilla Slab 600 | 27 px detail heading |
| Beach name | Source Sans 3 700 | 13 to 16 px in the compact rail |
| Safety instruction | Source Sans 3 700 | 13 to 14 px in the rail; larger in the detail sheet |
| Body and guidance | Source Sans 3 400 | Typically 14 to 15 px |
| Navigation and actions | Source Sans 3 600 to 700 | Weight follows action priority |
| Caption and metadata | Source Sans 3 400 to 600 | Typically 11 to 13 px |

Zilla Slab never carries a hazard instruction. `web/index.html` loads the families and defines base roles; `web/coastal.css` handles compact layouts; `web/sw.js` precaches the three files in `web/fonts/` for offline use. Color, safety meaning, and hazard data do not change with the typography.

## Mobile safe area

The satellite map remains full bleed behind the iPhone status area. The top controls use `safe-area-inset-top`, and the bottom sheet continues to respect `safe-area-inset-bottom`. This uses one responsive map implementation. A physical iPhone is still required to confirm Dynamic Island and home-indicator clearance in Safari and Add to Home Screen mode.

## Review and regeneration

1. Run `npm run check:map` and `npm run build:map`.
2. To regenerate the colored bands, install `tools/requirements-coast.txt` in a Python environment and run `python tools/build_coast_bands.py`. Review the resulting GeoJSON diff before committing it.
3. Walk the complete coast at desktop and phone widths, checking band joins, colors, hatching, labels, beach sheets, language switching, and offline behavior. The browser tool denied the local standalone-map origin during the latest walkthrough, so this rendered check remains open.
