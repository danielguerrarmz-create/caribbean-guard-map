# Map access and forecast preview

Date: 2026-10-15
Branch: `codex/map-access-forecast`
Base: `394a75a`, including the clean-URL repair from upstream PR #3.
Status: local review changes only. No push, merge, or production deployment.

## What changed

- Added Open-Meteo swell height, period, direction, wind speed, direction and gust forecasts. The table shows eight three-hour samples across the next day, using Costa Rica time.
- Added timestamps, refresh/loading/failure states, 12-second request timeouts and periodic refresh. Current model values and fetched hourly series expire after three hours. Missing values remain unavailable, not zero.
- Kept forecasts separate from standing beach classifications and mapped current annotations. Forecasts do not calculate swimming permission or a live rip-current danger score.
- Added reference risk text to map labels and detail panels. Unassessed beaches remain explicitly unassessed.
- Removed proposed rescue stations from rendering, retaining original source records.
- Replaced the estimated offshore color polygons with outlined shoreline highlights. This removes self-intersections and overlapping wedges without inventing a hazard boundary.
- Increased road/path contrast, added walking icons at mapped path endpoints, and highlighted the selected path above road layers.
- Added stable `?a=osm-<way-id>` links. Each opens its mapped path, associated beach guidance, source current annotations and regional forecast. Website iframe navigation preserves the access query.
- Tightened beach fits and corrected startup/layout interference with QR positioning. Mobile navigation from expanded details lowers the panel to reveal the selected region. Desktop detail panels now scroll to the forecast.

## Follow-up visual review

- Beach panels now lead with the beach name and instruction, followed by essential emergency guidance and the forecast. The beach description and review notes are in a separate section below the forecast. Supporting source information is expandable. Rip-current escape guidance is permanently visible, with a prominent 911 button in the panel and fixed header. Existing cautions and review status remain available; the persistent header retains emergency access.
- Forecast captions are shorter and smaller. A circular, labelled reload control sits beside the forecast heading. Mobile scrolling content clears the fixed close control.
- Access badges are 24 px visually with unchanged 44 px hit targets. The selected path uses a restrained continuous highlight.
- Road casings and center strokes use separate global panes. Junctions no longer acquire cuts from later road outlines. Source OSM vertices remain unchanged.
- Each beach uses a single continuous stroke with a separate casing, solid color and butt caps at shared boundaries. Removed chunked tapers, overlapping ambient/selected highlights and translucent offshore polygons. Unassessed areas retain a neutral continuous line.
- Rip arrows use continuous shafts and open chevrons. Close document marks are decluttered at every zoom; their original invisible hit paths remain available at detail zoom. No source hazard records or geographic positions were removed.

- Overview cleanup: removed the extra undescribed-coast list entry and region subtitle, removed sidebar divider rules, aligned three forecast metrics with consistent insets, and changed map-only risk captions to short bold text on solid backgrounds. Detailed source qualifications remain in beach panels.

- Responsive redraw repair: disable Leaflet CSS zoom animation and stop active camera motion before a full view reset on resize. Verified expanded mobile panel and language changes followed by desktop resize; SVG roads/coasts remain registered to the imagery.

- Icon refinement: increased symbol and control artwork by about 12%, including rescue equipment, place markers, risk symbols, legend icons, GPS, compass and refresh. Trail badges are 27 px with 18 px artwork; existing marker anchors and touch targets are preserved.

## Why

The requested QR should let someone understand the surrounding beach and forecast immediately. The previous camera could return to the whole coast during startup. Offshore polygon offsets could fold across one another. Thin access routes were hard to read against imagery.

## Data sources and limits

- Marine API: https://open-meteo.com/en/docs/marine-weather-api
- Weather API: https://open-meteo.com/en/docs
- Marine OpenAPI specification: https://github.com/open-meteo/open-meteo/blob/main/openapi/marine.yml
- Existing OpenStreetMap roads and paths: `web/data/osm-roads.geojson`, ODbL attribution retained.

Both APIs returned valid 48-hour series during verification. The marine request at 9.647, -82.727 resolved to an offshore model cell at approximately 9.791664, -82.70833. These are regional model forecasts, not beach instruments or local rip-current observations. No new key, credential, backend or paid service was added.

The 20 access entries preserve existing OSM path geometry. Endpoint selection and nearest-beach association are draft editorial choices. Every record is `verified: false`; the interface explicitly states that position and public access need field confirmation. This is not a routing or rescue-dispatch dataset.

The demonstration uses `osm-458862734`, a mapped path near station 3.6 at Playa Chiquita. Its chosen endpoint is longitude -82.7091869, latitude 9.6373785. The screenshot appears to match this area, but Daniel has not confirmed the exact sign location. Do not print this demonstration QR as a confirmed access sign.

## How to verify

1. Build the website with `npm --prefix site run build`. Tile prerequisites remain unchanged.
2. Open `/mapa?a=osm-458862734` at desktop width and 390 x 844. Check the path, highlighted beach, source hazard arrows and forecast. Expand the mobile sheet to read the table.
3. Select “Ver toda la playa”. The camera fits the beach and the mobile sheet lowers.
4. Test every beach card, ES/EN, forecast refresh, close and the QR-link disclosure. The copied URL must retain `a=osm-458862734`.
5. Run `node --test tools/tests/*.test.mjs`, `npm --prefix site run test:export`, `npm run check:map`, `npm run build:map`, `npm --prefix site run lint` and `git diff --check`.

Verified locally:
- Website production build and TypeScript completed successfully. Subsequent static map refinements were repackaged into that export.
- All seven desktop beach cards opened the correct named panel and URL, with eight forecast rows and scrollable details.
- 390 x 844 QR view, expanded forecast, ES/EN, refresh and whole-beach transition checked visually. Body width remained 390 px; forecast table fit at 335 px.
- Eight forecast/access/linework regression tests and four site-export tests passed, including clean map URLs and query variants.
- Map copy checks, inline JavaScript syntax, lint, map packaging and diff checks passed. Packaging verified 537 offline asset references.
- No console errors from the final preview origin. Actual iOS/Android hardware and offline device storage were not tested.

## What's left

- Confirm the exact QR/sign point and public access in the field. Review all draft access associations before publishing them as official entrances.
- Obtain dated Caribbean Guard review for standing danger classifications and mapped hazards; existing provisional provenance remains visible.
- Confirm the final production domain before generating printable QR artwork.
- Review the local rendition before requesting publication. Leave PR #3 and owner-controlled merge/deployment intact.
- Instagram image sourcing is deferred; a reminder is scheduled for October 16 at 9 a.m. America/Chicago.

## Files touched

- `web/index.html`, `web/coastal.css`, `web/geometry.js`, `web/symbols.js`, `web/sw.js`
- `web/forecast.js`, `web/data/access-points.json`
- `site/src/app/mapa/MapFrame.tsx`, `site/tests/site-export.test.mjs`
- `tools/prepare_site_assets.mjs`, `tools/tests/forecast.test.mjs`, `tools/tests/access-points.test.mjs`, `tools/tests/linework.test.mjs`
- This handoff document.

Local preview helper and generated assets are ignored artifacts, not publication source.
# Follow-up: scrolling close control and coastline offset loops

2026-10-15: The close control now lives in a shared title row inside the sheet scroller. Its visible circle is 32px, with a 44px touch target on mobile. All sheet renderers, including language changes, reuse the same button and listener. The embedded packager no longer adds an absolute-position override.

The Cocles hook came from a self-crossing 25m display offset in `tools/osm_coastline.py`. The generator now trims offset loops before its existing smoothing steps. Regenerated `web/data/zones-geometry.json` also removes small loops in Salsa Brava and Punta Uva; the other four beach paths are unchanged and all shared endpoints remain exact. The original OSM coastline and hazard annotations are untouched. This is a display-geometry correction, not a new geographic survey or safety assessment.

Verification: 4 Python geometry checks and 16 Node checks pass, along with map copy checks. Desktop and 390px mobile checks covered title alignment, scrolling, closing after a language change, and the Cocles bend at 50m scale. Review image: `out/coast-title-fix-desktop.jpg`.
