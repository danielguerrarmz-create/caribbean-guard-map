# Caribbean Guard visual review handoff

Update 2026-11-03: Daniel rejected both hazard treatments and their white outlines. Simplify the source rip drawings into one curve family and rebuild all arrowheads. Phosphor Regular remains selected. See `docs/design/2026-11-03-cartographic-precedents.md`; older cartographic recommendations below are superseded.

Date: 2026-11-03
Status: Daniel approved the quieter overview. Daniel selected Phosphor Regular. The separate study uses it for controls, symbols and equipment examples; hazard treatments remain proposals and larger redesign remains open.

## What changed

- Created managed worktree `C:\Users\danie\.codex\worktrees\map-visual-review\caribbean-guard` from GitHub master `fbc65fa`, branch `codex/map-visual-review`.
- Refined coast-overview spacing, list hierarchy, forecast density, header controls and small control transitions.
- Corrected label placement skipping labels hidden by the first collision pass; reduced overly wide label boxes.
- Added the component audit, design direction, dual-platform release work and source intake in Burondono.
- Researched four open-source icon families and collected 28 original SVGs with pinned revisions, hashes and licences. Added a live comparison of existing geometry styling, a reference-risk ribbon and a hatched band at http://127.0.0.1:5196/ (retained exec session 80601).

## Why

The opening phone sheet prioritized weather over beach selection. Map labels were hidden prematurely and equipment marks compete at coast scale. The larger redesign needs an approved representative screen before rollout, as requested in Daniel's global instructions.

## How to verify

- Preview remains running at http://127.0.0.1:5174/ and http://127.0.0.1:5174/mobile-preview.html (retained exec session 80335).
- `node --test tools/tests/*.test.mjs`: 26 passed.
- `npm run check:map`: passed.
- `npm run build:map`: passed, 546 asset references.
- `git diff --check`: passed.
- Browser: desktop overview / Cocles / legend; phone overview / expanded list / Cocles / ES switch / close.
- Proof screenshots are under ignored `out/visual-review/`.

## What's left

- Hazard-treatment review and selected Phosphor Regular application, then map symbol system and complete component rollout. See `docs/design/2026-11-03-iconography-and-cartography.md` for the research and `docs/design/2026-11-03-product-review.md` for the release sequence.
- Some coast-scale labels still yield to collisions; equipment still overlaps. Not a solved cartographic system.
- Physical-device / accessibility / offline testing, imagery rights evidence, toolchain audit fixes and native packaging for iOS and Android.
- Burondono creator references are intake records, not shipped components. Add refined implementations to their proper package locations when they exist.

## Files touched

- `web/coastal.css`
- `web/index.html`
- `tools/tests/beach-labels.test.mjs`
- `docs/design/2026-11-03-product-review.md`
- `docs/handoffs/2026-11-03-visual-review.md`
- `docs/design/2026-11-03-iconography-and-cartography.md`
- `docs/design/symbol-study/`
- `tools/collect_icon_study.py`
- Ignored local `web/tiles/` copied from the existing checkout; generated `dist-map/`; local screenshots in `out/`.

Related local design-system checkout: `C:\Users\danie\code\burondono-design-system`, branch `codex/caribbean-creator-intake`. Changed `CONTRIBUTING.md` and added `docs/references/{README,gabriel-metadata-disclosure,transitions-motion}.md`. No package changes.

The icon study also adds `docs/references/icon-study/` there, including the same licensed source assets. Browser review covered 24 px and 16 px samples, treatment switching, grayscale, arrow visibility and map zoom. The overview still has overlapping equipment marks; the study does not solve their interaction. No new icon family or hazard geometry has been applied to the main app in this research step.

Existing dirty checkouts were preserved. No commits, pushes, deployments, external posts or store submissions were made.


## Proof 03 update

- Changed: added the synchronized two-panel proof at http://127.0.0.1:5196/proof.html, using simplified curves and identical compact filled heads with no white outline. A compares selected tint; B compares an unfilled fine broken boundary.
- Why: Daniel rejected traced micro-curves and both earlier area treatments, then authorized this replacement comparison.
- Verify: open the proof; compare Cocles, switch beaches, toggle selection and equipment, zoom either panel, inspect the 53-curve atlas. Browser review included desktop and 390 px mobile. All 53 source curves produce finite quadratic geometry; JavaScript syntax checks pass.
- Left: Daniel's visual review, production symbol density and equipment collision handling, then application integration. This remains a local visual proof.
- Files: `docs/design/symbol-study/{proof.html,proof.css,proof.mjs,curve.mjs,README.md,research.html}`, the cartographic precedent report and this handoff. Burondono adds `docs/references/coastal-curve-proof/` and updates its intake record. No main-app edits in this step.


## Approved main-app integration

- What changed: selected beach receives the approved 19% flat tint. Ambient bands, coastal classification strokes and selected perimeter/caps are removed. Original coast tap targets and signed current-advisory halos remain. All rip renderers use the approved quadratic family, a 2 px coral shaft and fixed 7 x 6 px tangent-aligned filled head, without casing. Original Rescue Station glyphs and their styling remain.
- Why: Daniel approved treatment A and requested it in the main app, while preferring the original colorful Rescue Stations to the boxed neutral Phosphor samples.
- Verify: http://127.0.0.1:5174/?z=cocles and http://127.0.0.1:5174/mobile-preview.html. Open Cocles from the mobile list. Close details to remove the tint; select another beach to move it. Arrows appear from zoom 14 with existing density management. Station overview styling retains its prior zoom-15 threshold.
- Validation: 29 Node tests pass; `check:map` passes; `build:map` validates 546 offline references. Service-worker version is bumped for the changed renderer. Source geometry and hazard evidence are untouched.
- Alternatives: http://127.0.0.1:5196/icon-alternatives.html compares original Rescue Station artwork with colored Regular and Duotone candidates without rectangular backgrounds. Two pinned original Duotone SVGs plus MIT licence were added to the asset manifest and mirrored in Burondono. Candidate iconography is not applied to the app.
- Files: `web/index.html`, `web/geometry.js`, `web/sw.js`, `tools/tests/rip-curves.test.mjs`, `tools/collect_icon_study.py`, study assets and icon-alternatives page. Burondono adds the explicit-dependency Leaflet adapter and icon color/container record.
- Left: visual feedback on the integrated screen and supporting-icon alternatives; station overlap and full application/store release work remain. No commit, push or deployment.

Final browser evidence: `out/visual-review/applied-desktop.png`, `applied-mobile.png` and `icon-alternatives.png`. Selected-area count verified as one while selected and zero after close. Desktop rendered head and shaft counts match, with no captured console errors. The rejected first study now uses `archive-geometry.js` to preserve its original renderer after the main app integration.


## Colored Duotone and lighter selection update

- Changed: 35 semantic symbols now use 28 pinned Phosphor Duotone source SVGs plus preserved original rescue artwork. Map glyphs have a silhouette-following white contour, approximately 0.5–0.7 px, with no background badges. Places/access are teal, hazard glyphs coral, caution amber. Controls, beach cards, forecast refresh and location symbols use the shared renderer. Rip arrow geometry remains unchanged and outline-free.
- Why: Daniel approved Colored Duotone and requested a discreet outward white offset over satellite imagery. He additionally requested a lighter selected-area tint and mobile parity.
- Tint: reduced from 19% to 13% on the shared map renderer. Browser DOM confirms mobile fill-opacity 0.13. No hatch or boundary was reintroduced. Tint remains selection-only.
- Verify: desktop and mobile previews remain on port 5174. Open Cocles, zoom in for places/access icons, open the legend, expand the mobile beach list, and compare the shoreline imagery through the tint. Full family review: http://127.0.0.1:5196/duotone.html.
- Validation: 33 tests pass, copy check passes, offline build validates 547 assets. New tests cover every symbol, safe fallback, retained branded artwork and upstream SHA-256 integrity. No external SVG or runtime icon package is needed offline. Source licences are bundled.
- Files: `web/symbols.js`, `web/icons/phosphor-duotone/`, preserved `web/icons/{rescue-station,proposed-rescue-station}.svg`, `web/coastal.css`, `web/index.html`, `web/sw.js`, `tools/build_symbols.py`, `tools/collect_icon_study.py`, `tools/tests/symbols.test.mjs`, source-study assets and `duotone.html`.
- Burondono: source assets and manifest updated; renderer and consumer style snapshot added under `docs/references/colored-map-icons/`, outside package exports.
- Left: visual feedback, existing dense-marker overlap, physical-device compass and broader release validation. No commit, push or deployment.

Final captures: `out/visual-review/duotone-desktop.png`, `duotone-mobile.png`, `duotone-family.png`. Both rendered selected areas report fill-opacity 0.13; no captured desktop console errors. Map contour, the complete symbol family, phone list, phone details and desktop detail scale were visually reviewed.


## Icon contrast compromise study

- Daniel found the silhouette contour pixelated and asked about balancing imagery intensity, icon color and white backing size.
- Added `docs/design/symbol-study/contrast.{html,css,mjs}` with three synchronized actual-map panels: current contour, recommended 34 px backing, and a larger 38 px backing. Both candidates use 28 px glyphs, quieter imagery and deeper teal. Original rescue artwork, source positions, arrows and the 13% tint remain consistent.
- Recommendation: 34 px at 84% white, imagery saturation .45 / contrast .85 / brightness 1.03, glyph teal #087d87. The larger 38 px alternative is more prominent but crowds adjacent symbols.
- Verify: http://127.0.0.1:5196/contrast.html. Pan or zoom one panel; the others follow. Review the stacked layout on a narrow screen.
- Main application unchanged in this step. Await visual feedback before rollout. CSS and provenance copied to Burondono `docs/references/colored-map-icons/contrast-study.*`.


## Balanced approved and integrated

- What changed: option 02 is applied to the shared mobile/desktop map. Satellite tiles alone use saturation .45, contrast .85, brightness 1.03. Supporting icons use deep teal #087d87 and a smooth 34 px circular white backing at 84% opacity; the rejected silhouette filter is disabled. Original Rescue Station artwork is retained and excluded from the backing.
- Why: Daniel approved Balanced and explicitly requested defined red hazards unaffected by the quieter imagery.
- Hazards: arrows use opaque #f04444 with unchanged simplified curves and consistent heads. The selected high-risk area uses #e83e3e at 22% opacity; other tiers retain their colors and 13% opacity. No white outlines, hatch texture or selected perimeter was added. Source geometry is unchanged.
- Verify: http://127.0.0.1:5174/?z=cocles and http://127.0.0.1:5174/mobile-preview.html. Select Cocles, zoom for supporting icons and compare the original Rescue Stations. Browser review covers desktop and the 390 x 844 mobile app.
- Validation: all 33 Node tests, check:map and build:map pass; offline build validates 547 assets. Cache bumped to cg-map-v54-balanced-red-hazards.
- Files: web/coastal.css, web/geometry.js, web/index.html, web/sw.js, this handoff; Burondono colored-map-icons consumer CSS and approval documentation plus coastal-curve-proof arrow color mirror.
- Evidence: out/visual-review/balanced-desktop.png and balanced-mobile.png.
- Left: existing dense-marker overlap, physical-device and store-release validation. No commit, push or deployment.


## Rescue-first hierarchy, placement and motion

- Changed: all station renderers now use the pinned Phosphor Duotone lifebuoy in warm orange; original brand SVGs remain archived. Detail hierarchy is 40/32 px rescue backing/glyph, 30/22 access, 26/18 places, 32/24 references. Overview rescue is 32/25. Map hit boxes are centered 44 px; rescue markers draw above nearby places.
- Why: Daniel clarified that stations should also use Duotone, requested rescue priority, reported icons escaping their backings, requested animated rip currents and a simpler north pointer.
- Placement root cause: 28 px place glyphs sat in the legacy 20 px grid with an inherited 1.12 scale. Grid tracks, explicit container/glyph tokens and absolute centering now keep glyph, backing and geographic anchor aligned. No source positions moved.
- Motion: steady opaque red shaft/head plus red 6/18 px flow pulses moving toward the head in a 1.4 s cycle. All renderer paths use the shared implementation. Reduced motion keeps the static arrow, and pan/zoom pauses pulses. Motion communicates direction only, not live speed. Selected-area red remains unchanged.
- North: simple two-tone pointer; live heading rotation remains attached and centered on the viewBox.
- Verify: desktop and mobile previews on port 5174. Select Cocles and zoom to detail. Run tools/browser/map-symbol-audit.js read-only in each document; 108 rendered markers pass containment/centering in both views. All visible shafts have running pulse layers. Browser captures: out/visual-review/hierarchy-desktop.png and hierarchy-mobile.png.
- Tests: Duotone rescue contract test first failed against the previous brand renderer, then passed after regeneration. New Leaflet-boundary regression covers all 53 current annotations through redraw/zoom. All 34 tests, check:map and build:map pass; 547 offline assets. Cache is cg-map-v55-rescue-hierarchy-flow.
- Files: web/coastal.css, web/geometry.js, web/index.html, web/symbols.js, web/sw.js; tools/build_symbols.py, tools/tests/symbols.test.mjs, tools/tests/rip-curves.test.mjs, tools/browser/map-symbol-audit.js; this handoff. Burondono receives renderer/CSS/adapter mirrors and marker-hierarchy.md.
- Remaining: visual sign-off, dense-marker collision refinement and physical-device compass/release checks. No commit, push or deployment.


## Decluttering, restrained motion and caption cleanup

- Changed: source coordinates stay fixed while lower-priority access/place markers yield six pixels around occupied hit boxes. All rescue markers remain. Suppressed items leave focus/accessibility order and return after zoom or layer changes. No source features are deleted.
- Motion: replaced repeated 1.4 s dashes with one normalized 18% stroke on a 3.6 s cycle, deterministic staggering and a quiet interval. Underlying opaque red shaft/head and reduced-motion static alternative remain. Research and rationale: docs/design/2026-11-03-map-motion-and-content.md.
- Copy: removed legend zoom/motion caption, distance-origin caption, overview forecast footnote and repeated beach review caption in both languages. Recent-data bookkeeping and forecast metadata are inside relevant disclosures; incomplete data, actual restrictions and emergency instructions remain visible. Distance context remains accessible on its value.
- Verify: main desktop/mobile at port 5174. Zoom Cocles, toggle rescue equipment in Legend, expand About this forecast and refresh, review the beach list. Browser checks show zero access/place collisions in both views; hiding rescue increased visible desktop access from 13 to 16. Screenshots/audit are out/visual-review/declutter-*.
- Validation: all 38 tests, check:map and build:map pass, 547 offline assets. New priority tests failed before implementation and pass after. No captured desktop console errors.
- Files: web/index.html, web/geometry.js, web/coastal.css, web/sw.js; tools/tests/marker-priority.test.mjs, tools/tests/rip-curves.test.mjs; design research and this handoff. Burondono includes marker-priority.mjs, updated CSS/arrow adapter and motion precedent record outside package exports.
- Remaining: visual feedback on revised motion; overview rescue-to-rescue clustering and physical-device release work. No commit, push or deployment.


## Moving dashes, open navigation and overview spacing

- Changed: the rip shaft itself is dashed (8 px on, 6 px off) and moves toward its open two-sided arrowhead at one 14 px period per 1.2 s. The previous continuous underlay/sweep is removed. Reduced motion retains static dashes. Red, geography, simplified curves and marker decluttering are unchanged.
- Navigation: next/external use the same custom two-sided, unfilled, right-facing chevron. These interface primitives are distinct from pinned Phosphor map assets. The directional map arrows retain their flow orientation; the compass retains north.
- Layout: mobile overview title padding is 16 px top / 24 px bottom, desktop 32/24. The forecast action is centered in a 64 px row with no additional gap or bottom padding before the list divider. Mobile browser measurements: 32 px above/below its center. This shifts the beach list downward while retaining its scroller.
- Verify: expanded mobile overview at http://127.0.0.1:5174/mobile-preview.html; dashed currents on Cocles at http://127.0.0.1:5174/?z=cocles. Capture: out/visual-review/open-chevron-mobile.png and dashed-currents-desktop.png.
- Validation: 39 Node tests, check:map and build:map pass (547 offline assets). Renderer regression verifies exactly two line layers, open unfilled heads and dashed shafts across all 53 curves. Navigation regression verifies matching open chevrons. Cache bumped to cg-map-v57-dashes-open-chevron.
- Files: web/geometry.js, web/coastal.css, web/symbols.js, web/sw.js; tools/build_symbols.py, tools/tests/rip-curves.test.mjs, tools/tests/symbols.test.mjs, tools/browser/map-symbol-audit.js; handoff. Burondono CSS, symbol and arrow adapter mirrors plus current reference notes updated locally.
- Remaining: visual feedback and broader physical-device/store release checks. No commit, push or deployment.


## Rescue grouping and horizontal detail navigation

- Changed: rescue collisions now produce Duotone count badges anchored to an actual member, with no coordinate offsets or centroid positions. Tap/Enter zoom two levels; groups dissolve when separated. Maximum-zoom overlap has a member chooser. All 20 existing rescue records, including previously hidden unnumbered source pins, now participate at overview zoom. Proposed locations retain their prior detail-zoom rule.
- Navigation: forecast and every beach-list row enter from the right; the open left chevron plus Back returns to the list's original detent and scroll position. Opening focuses the heading; Back restores the initiating control. Native browser Back still closes the detail. Independent translate animation avoids the vertical drag controller's transform; reduced motion skips travel and re-entry cancels pending animations.
- Layout: English title is Southern Caribbean Beaches. Collapsed panel is 96 px tall (112 px below 370 px viewport width), with the complete title, handle and upward chevron. Hidden lower content leaves keyboard/AT order. Scale is a compact metric rule with end ticks and a smaller paper backing; distances remain computed by Leaflet.
- Why: previous forced visibility made rescue icons collide; the former 64 px collapsed detent clipped the newly padded title. Detail actions now communicate a consistent page hierarchy.
- Validation: 41 Node tests, check:map and build:map pass; 547 offline assets. Browser marker audit passes at overview and close zoom, including all 75 rendered symbols and 47 moving rip shafts. Verified mobile 390 by 844 and desktop 1031 by 859; beach/forecast entry, Back restoring full list and focus, and keyboard group expansion. No desktop console errors after final reload.
- Verify: http://127.0.0.1:5174/mobile-preview.html and http://127.0.0.1:5174/. Expand a rescue count, zoom until it separates, open the beach list, enter forecast or a beach, use Back. Mobile collapsed view and scale are in out/visual-review/rescue-groups-mobile.png; forecast in forecast-navigation-mobile.png.
- Files touched this pass: web/index.html, web/coastal.css, web/geometry.js, web/sw.js; tools/tests/marker-priority.test.mjs; tools/browser/map-symbol-audit.js; this handoff. Cache cg-map-v58-rescue-groups-panel-navigation. Burondono mirrors grouping, CSS and panel motion in docs/references/colored-map-icons and panel-route-motion.js, with provenance in transitions-motion.md.
- Remaining: physical-device/store release validation and visual feedback. No commit, push or deployment.


## Persistent names, swipe Back and forecast restructuring

- What changed: all seven beach labels now search available viewport space and retain fine leaders to unchanged geographic anchors. Boxes fit their text; rescue/count markers and controls are obstacles. Close-zoom eligibility stays limited to anchors in the visible map.
- Why: the former fixed offset list hid names when every nearby slot was occupied. Fixed 136 px boxes also exaggerated collisions.
- Navigation: routed forecast and beach pages support rightward touch/mouse/pen swipes. The page follows horizontal movement; a completed gesture runs the same Back action, and a short/cancelled gesture returns. Direction locking preserves vertical scrolling and sheet dragging. Reduced motion removes movement without disabling Back.
- Forecast: current swell, wind and gust readings lead; the large experimental-guidance card becomes a compact notice. Storm restrictions retain their red emphasis. Hourly dates are grouped by Costa Rica day; times and units are no longer repeated in every value. Hairlines replace blue zebra striping. Missing/stale data and safety evaluation are unchanged.
- Verify: open the full mobile beach list, enter Coastal forecast, drag right to return; repeat with a beach. Short horizontal drags must cancel, vertical scrolling must stay in the page. In the overview count seven beach names and confirm no label/rescue overlap.
- Files: web/index.html, web/geometry.js, web/forecast.js, web/panel-gesture.js, web/coastal.css, web/sw.js; tools/tests/beach-labels.test.mjs, panel-gesture.test.mjs, forecast.test.mjs; tools/browser/beach-label-audit.js. Burondono references updated with gesture, label layout, CSS and forecast documentation. Cache v59; gesture module added to offline assets.
- Remaining: physical iOS/Android device testing and user visual feedback. No commit, push or deployment.

- Final validation: all 47 Node tests, copy checks, inline script parsing and build pass; 548 offline assets. Browser overview audits report seven labels and zero marker overlaps on mobile and desktop. Live short-swipe cancellation and full-swipe Back passed. Captures: out/visual-review/persistent-beach-names-mobile.png, forecast-restructured-mobile.png, forecast-restructured-desktop.png.


## Selective labels and hourly forecast strip

- What changed: reversed forced all-seven label visibility. Eligible anchors must be inside the visible map at every zoom; label search is limited to 72 px from its home placement. Crowded labels yield. Fine leaders and rescue/control clearance remain; no geographic coordinates changed.
- Why: names should describe the current frame without being pulled in from remote beaches. Desktop closer-zoom audit shows three nearby names and zero label/marker overlaps.
- Forecast: compact yellow safety surface replaces the vertical accent bar. Refresh uses a clean regular silhouette plus label with a 44 px target. Current values and safety evaluation remain unchanged.
- Next 24 hours: Apple Weather screenshot-inspired horizontal hourly strip with Swell/Wind/Gusts tabs, 24 hourly readings, Costa Rica day/time, units and period/direction. No Apple assets/code copied. Missing bearings omit arrows. Embedded beach forecasts retain their table.
- Interaction: keyboard tab navigation; selected metric, horizontal position, disclosures and vertical position survive refresh. Horizontal strip gestures do not trigger Back; rightward Back remains available elsewhere. Physical iOS/Android testing remains release work.
- Verify: http://127.0.0.1:5174/mobile-preview.html and http://127.0.0.1:5174/. Enter Coastal forecast, switch metrics, browse later hours and refresh. Zoom the map to confirm remote labels disappear and visible names clear rescue symbols. Proofs: out/visual-review/hourly-forecast-mobile.png, hourly-forecast-desktop.png, selective-labels-desktop.png.
- Validation: 49 Node tests, copy check and build pass; 548 offline assets. Cache cg-map-v60-hourly-forecast. Browser confirms 24 cells, selected wind/scroll retention on refresh and zero desktop label overlaps.
- Files: web/index.html, web/geometry.js, web/forecast.js, web/panel-gesture.js, web/coastal.css, web/sw.js; tools/tests/beach-labels.test.mjs, forecast.test.mjs, panel-gesture.test.mjs; this handoff. Burondono local references mirror label layout, styles, gesture exclusion and hourly renderer with provenance.
- Left: user visual feedback and physical-device/store-release validation. No commit, push or deployment.


## Forecast symbols and visual-quality diagnosis

- What changed: forecast-only symbols use pinned MIT Phosphor Regular paths. Swell is two vertically scaled wave-sine paths with a subordinate second layer; Wind and Gusts share an upright airflow symbol. Direction stays textual. SVG size is 32 px with ocean/slate-blue tones, no backing or halo. Map Duotone artwork and red hazards remain unchanged.
- Why: the filled waves were visually dense; rotating arrows conflated the weather category with direction. Gusts are a wind metric, so the label/value carry that distinction without inventing a separate weather condition icon.
- References: Apple Weather icons (https://support.apple.com/guide/iphone/learn-the-weather-icons-iph4305794fb/ios), SF Symbols optical weight and hierarchical rendering (https://developer.apple.com/design/human-interface-guidelines/sf-symbols), Phosphor pinned revision 2b75f3ad12b420c9504ef05df8d2564a28f8500e. Meteocons was evaluated, not used. No Apple assets/code copied.
- Verification: all 49 tests pass, including integrity checks extended to the new Regular assets; copy check and 548-reference offline build pass. Mobile Swell/Wind/Gusts and desktop Wind reviewed in browser; no desktop console errors. Cache v61-weather-symbols. Captures: out/visual-review/weather-swell-mobile.png, weather-gust-mobile.png, weather-wind-desktop.png.
- Files: tools/build_symbols.py, tools/tests/symbols.test.mjs, web/icons/phosphor-regular/*, web/symbols.js, web/index.html, web/coastal.css, web/sw.js, this handoff. Burondono docs/references/weather-symbols holds original assets, license, hashes, generator adapter and provenance; renderer/styles mirrored locally.
- Left: visual sign-off and physical-device release checks. No commit, push or deployment.

### Design diagnosis and terminology

This is a design judgment from the rendered mobile/desktop screens, not a usability-study result. Iterative component fixes have improved local clarity while leaving the whole-screen composition unresolved. The issue is compressed visual hierarchy and inconsistent visual grammar, not a shortage of decorative effects.

1. Visual hierarchy / salience: the three current readings have equal weight, while the yellow advisory dominates through area and color. Each page needs an intentional first, second and third reading priority. Keep safety information visible, but size and position it deliberately alongside the page's task.
2. Typographic hierarchy / optical sizing: secondary forecast details currently run at 9-12 CSS px. Small text and nearly uniform modest headings make the screen feel miniature and cautious. Increase useful secondary text and establish display, heading, body and metadata roles. Optical size means adjusting shapes/spacing for their actual rendered size, not merely assigning equal bounding boxes.
3. Tonal hierarchy / materiality / elevation: paper, pale ocean cards and controls are only weakly separated; the map is a different visual world. Define canvas, content and floating-control levels. Use restrained luminance differences, edge highlights or contact shadows only to explain layers. Blanket blur or shadows would add noise and reduce map legibility.
4. Rhythm / proximity: equal gaps are not automatically good composition. Related values should sit closer together than unrelated sections. Larger intentional pauses should separate major groups. Use a spacing scale, but let relationships choose the token.
5. Semantic density / data visualization: repeating an identical icon each hour has diminishing information value. A compact trend can reveal when swell or wind changes faster than scanning 24 numbers. Keep exact values available. The current icon refinement improves recognition but does not solve that larger information-design opportunity.
6. Visual grammar / art direction: rounded notices, segmented tabs, circular map controls, badges, icons and typography need explicit roles. Continuity means related construction rules, not forcing everything into the same rectangle. Establish a recognizably coastal identity through type, palette and restrained illustration; preserve learned weather conventions.
7. Interaction choreography / state completeness: press, loading, error, empty, stale-data, scrolling, Back and reduced-motion states affect perceived quality. Define timing, interruption and spatial direction across the whole journey. Test outdoors, with larger text, screen readers and on actual iOS/Android hardware. Browser polish alone is not release quality.

Recommended next pass, not implemented here: compose one complete forecast screen with a clear primary reading, more legible secondary type, a compact visible advisory, deliberate surface levels and a trend overview; visually approve that screen before applying the system elsewhere. This is a composition task rather than another round of isolated icon or radius changes.
