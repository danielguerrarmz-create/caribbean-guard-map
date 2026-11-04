# Shared beach and Legend continuity

Date: 2026-11-03
Status: local review. No commit, push or deployment.

## What changed

- Extended the approved safety composition to the remaining beach states. Existing lower-risk warnings and specific caveats sit inside the safety component. Unassessed beaches retain their explicit status, with geographic context and sources arranged consistently below the forecast.
- Replaced the separate Legend tray with the existing shared sheet. Mobile opens at full height and supports the same middle/full stops, Back, right-swipe and vertical overflow cues. Desktop uses the left reading column. Layer controls retain their actual map connections.
- Legend uses 24 px insets, 32 px section spacing, 32 px title, 21 px section headings, 15 px row labels and 56 px rows. Native checkbox targets sit opposite colored semantic icons. Sources and accuracy expands through a full-width chevron action.
- Closing beach details retains the last selected coastal reference tint. Opening the generic forecast/Legend also preserves it. Selecting another beach replaces it as before. No new hazard areas or changes to geography were introduced.
- Hide the map scale behind full-height mobile sheets; it previously translated up underneath the logo. Mobile remains scrollbar-free.

## Root causes

1. Legend used an older independent controller, a 45dvh CSS cap and upward rubber-band resistance, so it had no full detent.
2. closeSheet always called clearBand. The coastal tint existed on mobile while details were open but disappeared exactly when Back uncovered the map. Reproduced in browser: 1 selected SVG before Back, 0 afterward. Fixed: 1 after Back, including after returning from Legend.

## How to verify

- Open http://127.0.0.1:5174/mobile-preview.html and http://127.0.0.1:5174/.
- Open Legend. On mobile its top should align below the header, y=72 in the 390 x 844 frame. Drag down to the middle and up to full. Right-swipe or Back returns to the previous beach-panel stop.
- Toggle Rescue equipment. Projected rescue markers disappear and return. Other layer controls use the same event binding.
- Read all beach pages, including Playa Grande and Manzanillo. Keep Not assessed distinct from the risk-colored states. Emergency guidance and the regional forecast must remain reachable.
- Select Playa Cocles, use Back, then collapse the beach list. The red reference-area tint remains over the coastline. It remains #e83e3e at 0.22 opacity on mobile and desktop. This is the previously approved selected-area tint, not a new patterned hatch.

## Validation

- Two added regression tests demonstrated the failures before the fix and pass afterward. All 54 Node tests pass. Inline scripts parse, copy checks pass, offline build validates 549 asset references.
- Browser checks: seven beach pages on mobile and desktop, representative risk/caution/unassessed layouts, full/middle/full Legend gesture, right-swipe Back, bottom content reachability, actual layer removal (17 projected rescue markers to 0) and restoration, retained coastal tint after beach and Legend Back. No console errors observed.
- Proofs: out/visual-review/legend-shared-mobile.png, legend-shared-desktop.png, coastal-highlight-mobile.png.

## What's left

User visual review and physical iOS/Android release checks. No store submission or production deployment performed.

## Files touched

web/index.html, web/coastal-panels.css, web/sw.js (v65), tools/tests/legend-map-continuity.test.mjs, this handoff and screenshots. Burondono local docs/references/coastal-panels CSS/README updated and legend-panel.js added as an unshipped consumer reference.
