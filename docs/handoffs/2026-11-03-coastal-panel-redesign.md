# Coastal forecast and beach overview composition

Date: 2026-11-03
Status: local visual review. No commit, push or deployment.

## What changed

- Coastal forecast has a 64 px primary swell value, a quieter wind/gust column, larger supporting text, a sea-tinted current summary and a compact yellow safety disclosure. The safety headline and practical instruction remain visible when collapsed. Storm escalation retains its red prominent treatment.
- Next 24 hours combines a full-day trend with 24 exact hourly entries. Swell/Wind/Gusts tabs update both views. One category icon appears in the chart caption instead of being repeated every hour. Graphs use a zero baseline, true extrema, timestamp-based horizontal position and explicit breaks for missing hours. Isolated readings draw a point; unavailable metrics show no invented trend.
- Southern Caribbean Beaches has a larger title, a consistent current forecast summary, 18/19 px beach names, 12 px guidance and a quieter distance column. Header, forecast, list and footer now have the same visual and keyboard order on desktop and mobile.
- The mobile middle detent is 52% of viewport height, previously 44%, to leave a complete beach row visible under the larger summary. The collapsed title and existing drag controller remain.
- New styles live in web/coastal-panels.css and are scoped to these two surfaces. Individual beach detail pages, map geography, red hazards and map symbols retain their current design.

## Why

The previous composition gave most content a similar modest weight, while the yellow advisory dominated through area. Small repeated symbols and metadata consumed attention without revealing the day's trend. This pass establishes a clear reading order and larger useful text while preserving exact values and safety semantics.

## How to verify

1. Open http://127.0.0.1:5174/mobile-preview.html and http://127.0.0.1:5174/.
2. Expand Southern Caribbean Beaches. Scroll to Manzanillo to confirm the whole list is reachable. Enter a beach, then swipe right or use Back to return to the prior list position.
3. Open Coastal forecast. Review the primary reading, compact notice and day trend. Expand the notice to inspect model limitations.
4. Switch Swell/Wind/Gusts using tap or keyboard arrows. Scroll the hourly values horizontally, then Refresh. Metric and horizontal position must persist; the chart and hourly values must agree.
5. Check missing and zero data using the forecast tests. Empty/missing input must not become a continuous line or a positive reading. Existing advisory tests continue to verify that forecasts do not grant swimming clearance.

## Validation

- All 52 Node tests pass, including three new trend behavior tests covering the zero baseline, real time spacing, missing/skipped readings, zero and invalid values.
- Inline JavaScript parses; copy checks pass; offline build validates 549 asset references, including the new stylesheet. Cache cg-map-v62-coastal-composition.
- Browser review: 390 x 844 mobile and 1031 x 859 desktop. Verified 24 hourly entries, one active metric, refresh retaining Wind/scroll position, expandable safety notice, reachability of the last beach, and actual rightward swipe Back restoring the full list. No desktop console errors during final review.
- Proofs: out/visual-review/composed-beaches-mobile.png, composed-beaches-desktop.png, composed-forecast-mobile.png, composed-forecast-desktop.png.

## What's left

User visual sign-off before applying this composition to individual beach detail or other screens. Physical iOS/Android, larger text, screen-reader and store-release checks remain part of release preparation. No new safety classifications, medical guidance or geographical edits were introduced.

## Files touched

- web/index.html: overview/current/advisory/chart renderers, selected-metric state, DOM order and middle detent.
- web/forecast.js: pure trend model.
- web/coastal-panels.css: scoped composition and responsive styling.
- web/sw.js: stylesheet caching and cache version.
- tools/tests/forecast.test.mjs: chart behavior tests.
- This handoff.
- Burondono local docs/references/coastal-panels: consumer CSS, forecast adapter and rationale; docs/references/hourly-forecast.js and coastal-forecast-layout.md updated. These remain review references outside shipped packages.
