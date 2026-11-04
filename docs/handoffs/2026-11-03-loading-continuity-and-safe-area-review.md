# Loading continuity and safe-area review

Date: 2026-11-03
Status: Local review only. No commit, push or deployment.

## What changed / Why

- Shared breathing-dash treatment across current forecast readings. Existing readings remain legible during refresh.
- Reference images reserve their true aspect ratio, breathe subtly while pending, and fade in over 220 ms. Failed images leave loading and show an unavailable message. All five source-image dimensions were checked against the files.
- GPS search and offline-refresh controls use the same quiet pulse, with busy semantics. Repeated GPS clicks are guarded until completion.
- GPS feedback clears the toolbar. The mobile scroll hint clears the saved-copy footer by 12 px, including the bottom safe area.
- Preview-only time, signal and battery explain the system-owned space beside Dynamic Island. Production controls remain below safe-area insets; no fake system status is added to the main app.
- Review harness offers mobile/desktop layout and six replay controls. GPS and offline operations are explicitly labeled simulations and do not request location or save a cache.

## How to verify

Open http://127.0.0.1:5174/@fs/C:/Users/danie/.codex/worktrees/map-visual-review/caribbean-guard/out/visual-review/mobile-motion-review.html

Use first load, refresh and reference-image buttons in both layout sizes. GPS and offline buttons preview feedback only. The normal preview is http://127.0.0.1:5174/mobile-preview.html .

Validation: all 69 node tests passed; npm run check:map passed; npm run build:map validated 549 offline asset references. Browser checks covered reference-image completion, desktop forecast loading, mobile footer spacing and GPS toast clearance. No horizontal overflow in the checked desktop view. Reduced-motion and cached/error image paths are covered by tests.

## What's left

- Physical-device review of location permission prompts, actual positioning and installed offline cache operations.
- Physical iPhone Safari/PWA safe-area verification. Desktop simulation is illustrative, not device certification.
- Satellite tiles keep their existing progressive loading; no artificial progress overlay was added.
- Lifeguard reports remain isolated pending AJ/team definition.

## Files touched

web/index.html; web/coastal-panels.css; web/data/rip-reference-images.json; web/mobile-preview.html; web/preview-device.css; web/preview-device.js; web/sw.js; tools/tests/loading-continuity.test.mjs; out/visual-review/mobile-motion-review.html; out/visual-review/motion-review-app.html.

Local Burondono references updated: docs/references/coastal-panels/{coastal-panels.css,motion-loading.js,secondary-details.js,README.md}. Unshipped reference only.
