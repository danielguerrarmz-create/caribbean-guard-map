# Map controls, compact Legend and remaining detail pages

## What changed
- Compact three-group, two-column Legend with matching map glyphs and animated dashed rip symbol.
- Selected coastal reference tint increased from 0.13/0.22 to 0.40, using saturated red/amber/green; neutral unassessed 0.22.
- All beach entry paths use openBeach and connected navigation; generic sheets now also receive Back/right-swipe route behavior.
- Unified top app controls and lower map tools, including iPhone safe-area handling and a development simulator toggle.
- Shared info-page typography, spacing, status surfaces, actions and source disclosures across original/proposed rescue records, newer rescue pins, access, reference images, current/area information, places, roads, unassessed-region and saved-copy information.
- Access details reuse the current beach instruction and integrated weather advisory, including lifeguard clock refresh. New projected place/rescue pages do not add routes to provisional coordinates.

## Why
Map-label taps bypassed the connected route, leaving a separate-looking page with a filled X. Legend rows consumed too much vertical space. Lower-priority destinations retained the older visual style and newer pins used unrelated popups. Safe-area bottom padding moved below the screen with partially translated panels.

## How to verify
- http://127.0.0.1:5174/mobile-preview.html and http://127.0.0.1:5174/
- Rescue deep links: mobile-preview.html?p=est1 and /?p=est1. Pull the mobile handle to full height.
- Access deep links: mobile-preview.html?a=osm-360220452 and /?a=osm-360220452.
- Select Cocles from the list, return, collapse the list and tap the beach name. Back must be present, X hidden, and the selected red coast remain on the map after returning.
- Open Legend from the lower map tool row, toggle layers and expand sources. All layer choices are above the source disclosure. Rip symbol matches moving map dashes.
- Mobile preview checkbox simulates top 59 px and bottom 34 px insets. Inspect both full and partial sheet positions and swipe right to return.
- Source-map rescue pins now open full details with availability unconfirmed and record-specific attribution.

## Validation
- 55 node tests pass; new label-route regression failed before the fix.
- check:map passes; build:map validates 549 offline assets; inline scripts parse.
- Browser review: mobile/desktop Legend, original rescue, access; desktop source rescue/place/current/reference/offline; mobile beach-label Back, station swipe-back, selected tint and safe-area composition.
- Screenshots: out/visual-review/legend-compact-mobile.png, legend-compact-desktop.png, rescue-refined-mobile.png, rescue-refined-desktop.png, rescue-pin-refined-desktop.png, coastal-bold-mobile.png.

## What's left
Physical iPhone/Safari and Android device verification, production service-worker/offline behavior, store packaging, field validation of map records and geography. No safety classifications or geographic anchors changed. This is a local visual review, not a deployment or field survey. No commit, push or publication performed.

## Files touched
web/index.html, web/coastal-panels.css, web/symbols.js, web/mobile-preview.html, web/sw.js, tools/build_symbols.py, tools/tests/legend-map-continuity.test.mjs, this handoff. Local Burondono mirrors: docs/references/coastal-panels/{coastal-panels.css,legend-panel.js,secondary-details.js,README.md}, docs/references/colored-map-icons/symbols.js.

## Safe-area reference
https://webkit.org/blog/7929/designing-websites-for-iphone-x/ - viewport-fit=cover and env safe-area padding. Hardware is not paintable; the map extends behind the sensor area and controls remain below it.

## Follow-up: Rescue and Legend refinement (v67)
- Shared rescueStatus component uses the beach hierarchy: 13 px context, 25 px primary status, 15 px support, no redundant decorative icon. Call 911 sits 16 px below; reported equipment/record starts 32 px later.
- Original station equipment is a three-row list with reported schedule separated below. Source pins retain their own attribution and do not gain unverified inventory or schedule.
- Coastal reference colors now sit in one inset two-column key with High risk, Moderate, Caution and Not assessed. Layer toggles remain separate. Group spacing is 24 px.
- Legend floating scroll cue removed because it obscured the final checkbox. Gesture scrolling remains.
- Validation: 55 tests, copy check, build (549 references), inline-script parse; mobile and desktop Rescue/Legend review, Spanish Legend wrapping, source rescue pin 2.2. Screenshots: rescue-spacing-mobile.png, rescue-spacing-desktop.png, legend-grouped-mobile.png, legend-grouped-desktop.png.
- Local Burondono CSS and function snapshots refreshed. No deployment, purchase or live-current feature added.

## Live-current data feasibility, checked 2026-11-03
Conclusion: open calls can provide regional model conditions near beach coordinates. No documented public feed of live rip-current measurements for the Caribbean Guard beaches was found. Absence from this search is not proof that a private or partner feed does not exist.

1. Open-Meteo Marine: ocean_current_velocity and ocean_current_direction, waves and swell are exposed in JSON. Current fields are modeled, not local sensor measurements; currents/tides use about 8 km cells with explicitly limited coastal accuracy. The app already uses Open-Meteo waves and weather; no new integration is needed merely to prove feasibility.
   https://open-meteo.com/en/docs/marine-weather-api
2. Read-only sample request: https://marine-api.open-meteo.com/v1/marine?latitude=9.647&longitude=-82.727&current=wave_height,swell_wave_height,ocean_current_velocity,ocean_current_direction&forecast_days=1
   Returned point: 9.791664,-82.70833, approximately 16 km from the requested coordinate. Sample timestamp 2026-11-03T23:30 UTC; wave_height .86 m, swell_wave_height .86 m, ocean_current_velocity .6 km/h, ocean_current_direction 146 degrees. These values document successful access only, not beach conditions or validated accuracy. The requested current time interval was 900 seconds, not evidence of 15-minute sensor updates.
3. Open-Meteo free endpoint is noncommercial with 10,000 requests/day and no uptime guarantee; commercial hosted use requires a subscription. Data attribution is required. No purchase authorized or made.
   https://open-meteo.com/en/pricing
4. Copernicus Marine global physics provides programmatic surface currents around 0.083 degrees, about 9 km. Free registration/data access; toolbox Python/CLI services. Similar spatial limitation for surf-zone/rip features. Dataset catalog includes hourly surface products and six-hourly currents; hourly outputs do not mean hourly observations.
   https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/services
   https://help.marine.copernicus.eu/en/articles/4220332-how-to-register-for-copernicus-marine-service
5. MIO-CIMAR/UCR publishes local marine forecasts and regional warnings including Caribbean rip-current concerns. Found no documented public live beach-rip API. Direct pages require JavaScript for full content; official indexed descriptions and warning text established forecast scope. Partner access/permission and Cocles-specific coverage remain unverified.
   https://miocimar.ucr.ac.cr/sobre-el-mio
   https://miocimar.ucr.ac.cr/pronosticos-locales/
   https://miocimar.ucr.ac.cr/advertencias/247 (historical example, not a current warning)
6. NOAA's local rip prediction precedent combines wave-model predictors with lifeguard observations and local verification. It is a useful method precedent, not a Costa Rica data source.
   https://vlab.noaa.gov/web/mdl/rip-current-observation-and-prediction

Recommendation: retain explicit model forecast labels and static reference arrows. Do not reinterpret a regional ocean-current vector as a live beach rip or automatically change swimming classifications from it. To pursue truly beach-specific status, first establish a lifeguard/MIO-CIMAR partnership with observation timestamps, expiry and responsibility for updates, then scope any feature. No partner contacted.
