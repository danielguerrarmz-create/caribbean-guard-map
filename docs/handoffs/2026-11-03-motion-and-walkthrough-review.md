# Motion and walkthrough review

Date: 2026-11-03
Status: local review only. Awaiting Daniel's visual review. No commit, push or deployment.

## What changed

- Original Rescue Station markers now belong to the same Legend layer as imported equipment. Previously switching rescue off left three original markers on the map.
- Fallback rip arrows now belong to the hazard layer too. They obey the switch even when the newer document annotation feed fails.
- Reference-image markers join the existing marker hierarchy: rescue 100, access 50, reference image 30, place 10. Occluded lower-priority markers return when zoom separates them. Geographic anchors are unchanged.
- Interrupted horizontal route transitions start from their currently presented position, avoiding a jump when reversing before entry finishes. Normal route duration remains 320 ms.
- Forecast metric changes use a 180 ms fade and 4 px entry offset. Selecting the active metric does not replay the animation. The selected hour/scroll position is retained.
- First-load forecast placeholders use a restrained 1.8-second opacity cycle and reserve approximately the loaded card's space: 410 px desktop, 448 px mobile. Missing overview values receive the same treatment. Existing readings stay visible during refresh.
- Refresh remains keyboard-focusable while busy, communicates aria-busy/aria-disabled, and relies on the existing request guard to reject duplicate requests. Focus survives the rendered panel replacement at both ends of the refresh.
- New motion skips animation under prefers-reduced-motion. Small control feedback uses 160 ms color/background transitions.
- Service-worker cache identifier is cg-map-v68-motion-review.
- Lifeguard reports remain an isolated concept. No reports, publishing workflow, new live-current source or partner integration was added.

## Walkthrough coverage

Pass 1 reviewed beach routes and layout on desktop and a 390 x 844 mobile frame. Pass 2 exercised controls, gestures, data refresh and secondary map routes. Pass 3 repeated affected paths after fixes and after restarting the interrupted preview server.

| Path or behavior | Evidence |
| --- | --- |
| Seven beach-list destinations | Opened Playa Negra, Puerto Viejo, Cocles, Chiquita, Punta Uva, Grande and Manzanillo on both layouts; shared Back route and no horizontal detail overflow in inspected views. |
| Beach map entry | Cocles map label opens the same connected detail page, with Back and the old close button hidden. Assessed/unassessed label wiring also has regression coverage. |
| History | Desktop browser Back returned to overview; Forward restored Cocles. Deep-linked Chiquita survived reload. |
| Mobile gestures | Rightward swipe returned from full forecast to overview; Legend opened at the full detent. Existing touch tests distinguish vertical scrolling, cancelled swipes and the hourly strip's horizontal scrolling. |
| Forecast | Swell/Wind/Gusts tabs, ArrowLeft keyboard navigation, later-hour paging, source disclosure, refresh, retained metric, retained readings and focus. Mobile and desktop revisited after fixes. |
| Legend | All nine switches toggled off/on; original rescue DOM count changed 3 to 0 to 3 after the fix. Mobile full-height grouping inspected again after restart. |
| Rescue | Group expansion, original Rescue Station 3.2 page and source equipment 3.1 page. Telephone/directions/report hrefs inspected without dispatching calls or messages. |
| Access | Path at Playa Cocles, safety/forecast composition and source link. |
| Places | Agapi Hostel and Residencial Sara source records. |
| Reference image | Calle Merlin / Punta Cocles image page; image loaded successfully in the shared panel. Occluded Jaguar reference now suppressed behind rescue instead of exposing a misleading target. |
| Currents and roads | Rip current, Area of strong currents and Calle Caracola road information opened through map targets. |
| Saved map | Local-preview saved-copy information page opened and returned correctly. |
| Language | ES/EN changed in place on Cocles; beach route remained open. |
| Loading | Initial loading status observed in the live app. Shared skeleton rendered separately for visual inspection; fresh mobile reload and settled forecast revisited. |

Some automation clicks initially hit an occluding map marker or an offscreen target. Those attempts are not counted as successful routes; final results were verified using visible targets and page titles.

## Validation

- `node --test tools/tests/*.test.mjs`: 64 passing tests.
- `npm run check:map`: passed.
- `npm run build:map`: passed, 549 offline asset references validated.
- Rescue ownership and fallback hazard ownership regressions were demonstrated failing before their fixes and passing afterward.
- Added behavior coverage for reference-image decluttering/reappearance, interrupted route reversal, reduced motion, hour/focus retention, duplicate requests and failed refresh preservation.
- All inline scripts parsed while extracting the local motion reference.
- Desktop console review showed no errors. One un-attributed MutationObserver error appeared during initial mobile tab creation after the interruption; it did not recur on fresh reload, and all subsequent mobile routes and controls completed. Its origin was not established, so this is not a claim of a completely clean mobile console history.

## How to review

- Desktop: http://127.0.0.1:5174/
- Mobile: http://127.0.0.1:5174/mobile-preview.html
- Both are left on the coastal forecast for review. Open a beach, return before its transition finishes, switch forecast metrics and refresh. Toggle rescue in Legend, then inspect the restored stations. Zoom around Chiquita to see image markers yield and return.
- Evidence: `out/visual-review/motion-forecast-mobile.jpg`, `motion-forecast-desktop.jpg`, `motion-loading.jpg`. The isolated loading markup is `out/visual-review/forecast-loading.html`; it is not part of the app build.

## Files touched in this pass

- `web/index.html`
- `web/coastal-panels.css`
- `web/sw.js`
- `tools/tests/legend-map-continuity.test.mjs`
- `tools/tests/motion-review.test.mjs`
- This handoff and local visual-review outputs.
- Local Burondono references: `docs/references/coastal-panels/motion-loading.js`, companion CSS and README. These are unshipped reference snapshots, not a standalone production package.

## What's left

- Daniel's visual review. Do not expand the redesign while awaiting feedback.
- Physical iOS/Android touch, assistive technology, installation, safe-area behavior and production offline caching need device/release QA. The mobile frame simulates safe insets; it does not certify Safari or native behavior.
- GPS permission, live location, emergency calls, mail dispatch and external directions were not executed. Relevant link destinations were inspected.
- This is route-family and representative-map-target coverage, not a manual click of every imported geographic record or exhaustive device/network combinations.
- Lifeguard reporting requirements remain with AJ and the team.


## Review refinement: quieter loading

The repeated column skeleton was replaced with the actual forecast card structure: metric labels, faint chart grid, a diffuse teal wash, and hourly dashes. No curve, times or values are fabricated. The wash and missing overview values breathe over 2.8 seconds; reduced motion stays static. On first data arrival, the resolved card fades from 0.5 to full opacity over 220 ms. Refreshes with existing data retain their original behavior. The mobile replay snapshot and local Burondono reference were updated. Cache v69.
