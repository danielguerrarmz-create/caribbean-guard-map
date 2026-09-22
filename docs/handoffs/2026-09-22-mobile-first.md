# Mobile-first layout handoff

## What changed

The phone dock now opens at about 40% of the viewport, with a swipe handle that cycles between a small tab, the default panel, and the full list. The map fills the screen behind a transparent header and floating controls. Beach sheets use an icon-only swipe handle, and the legend replaces the dock while open. An icon-only GPS control sits beside the north control; after a real geolocation fix, a blue person marker identifies that position. The initial beach sheet keeps the emergency call and rip-current advice visible.

## Why

Three live role-based walks found hidden forecast data, missing beach choices at 320 × 568, clipped emergency content, and a layer panel that covered the usable map. The revised panel states give the map priority while retaining a compact forecast and quick access to every beach. The layer panel now occupies the same bottom-panel slot as the beach list.

## How to verify

Open the persistent 390 × 844 preview at `http://127.0.0.1:5174/mobile-preview.html`. Swipe the dock handle down to the small tab and up through the default and full positions. Open Cocles and confirm `Call 911` and the rip-current instruction are visible; swipe its handle to expand. Open Map layers and confirm it replaces the beach panel. The preview is an interactive 390 × 844 iframe, so it retains the phone breakpoint in a desktop browser. Check the app at 320 × 568 and run `npm run check:map`, `npm run build:map`, and `git diff --check`.

## What's left

Review the mobile layout on physical iOS and Android devices, especially browser chrome, safe-area insets, GPS permission, and the blue person marker. Live GPS was not activated during visual review because it requests the user's location. This pass did not alter the provisional GPS annotation data.

## Files touched

`web/index.html`, `web/coastal.css`, `web/sw.js`, `web/mobile-preview.html`, `docs/design/2026-09-22-mobile-first-walkthrough.md`, and this handoff.
