# Beach detail visual continuity

Date: 2026-11-03
Status: local preview, no commit, push or deployment.

## What changed

- Assessed and unassessed beach detail templates share the approved coastal composition: 32 px title, larger instruction and supporting copy, restrained risk-tinted surface, consistent spacing and readable emergency guidance.
- Beach forecasts reuse the full-day trend and exact hourly readings. The compact advisory preserves beach-specific restrictions; storm escalation and lifeguard schedule logic remain intact. Access-point sheets retain their existing table.
- Mobile scrollbars are hidden across the app, preserving native scroll overflow. Small down-arrow controls page sheet/list content and disappear near the end. Hourly strips support swipe plus 44 px earlier/later controls, disabled at their edges. Motion respects reduced-motion preferences.
- Desktop scrollbar behavior and map markers/geography are unchanged.

## Why

Carry the approved coastal hierarchy into beach pages while giving the standing safety instruction the strongest weight. Make mobile overflow discoverable without scrollbar chrome.

## How to verify

1. Open http://127.0.0.1:5174/mobile-preview.html, expand Beaches and choose Playa Cocles. Desktop: http://127.0.0.1:5174/?z=cocles.
2. Review instruction, lifeguard hours, always-visible emergency text and call action. The advisory must retain the Cocles-specific lifeguard requirement.
3. Expand the mobile sheet, use the lower-right arrow to advance, then scroll to the end. The cue disappears. There must be no vertical or horizontal scrollbar chrome on mobile.
4. Switch Swell/Wind/Gusts, swipe the hourly strip or use its arrows. Refresh retains the selected metric and horizontal position. Swipe right on the page, outside the hourly strip, to return to the list.
5. Open an unassessed beach. It must still explicitly say Not assessed and retain the local guidance deferral.

## Validation

- All 52 Node tests pass. Inline scripts parse. Copy checks pass. Offline build validates 549 asset references.
- Browser reviewed at 390 x 844 mobile and 1031 x 859 desktop. Mobile sheet has no horizontal overflow; computed scrollbar width is none. Verified cue paging/end hiding, hourly paging and metric switching, and actual rightward Back gesture. Reviewed Playa Grande's unassessed state on desktop. No console errors observed in either Cocles preview.
- Proofs: out/visual-review/cocles-detail-mobile.png, cocles-detail-desktop.png, cocles-forecast-mobile.png.

## What's left

User visual review of Cocles. Physical iOS/Android and assistive-technology checks remain part of store readiness. Existing safety wording and classification were preserved; this is a visual/interaction change.

## Files touched

- web/index.html: beach templates, forecast detail variant, mobile scroll affordances.
- web/coastal-panels.css: beach composition and mobile scrollbar/cue styling.
- web/sw.js: cache cg-map-v63-beach-detail-continuity.
- This handoff and local screenshots.
- Burondono docs/references/coastal-panels: updated CSS/README, mobile-scroll-cues.js; docs/references/hourly-forecast.js updated. Local review references, not published packages.
