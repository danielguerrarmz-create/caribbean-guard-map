# Mobile motion and gestures, 2026-09-22

## What changed

- The beach dock follows a handle drag and settles at map-only, rest, or full height using distance and release speed. Its controls track its animated height.
- Beach details use the same brief easing when opening, closing, and changing height. Only the handle resizes the sheet; its content scrolls normally.
- Map layers enter and exit as a tray. Mobile controls use short pressed-state feedback.
- All added motion is disabled when the device requests reduced motion. Buttons retain click and keyboard operation.
- The offline cache version advances so returning visitors receive the updated stylesheet.

## Why

The beach dock previously jumped between fixed heights after a swipe. This felt disconnected from the finger and made the map controls jump as well. The sheet and layer tray needed a consistent motion rhythm without delaying safety content.

The interaction follows [Apple's Motion guidance](https://developer.apple.com/design/human-interface-guidelines/motion), [W3C Pointer Events](https://www.w3.org/TR/pointerevents/) for a dedicated `touch-action:none` drag handle, and [MDN's reduced-motion guidance](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion).

## How to verify

1. Open `http://127.0.0.1:5174/mobile-preview.html` at its 390 × 844 viewport.
2. Drag the beach handle down and up. The panel should follow the pointer, then settle smoothly; GPS and north controls should remain above it.
3. Open a beach and drag its handle up/down. Scroll within the details and confirm that the text scrolls without resizing the sheet.
4. Open and close Map layers. Check its keyboard button and layer checkboxes.
5. Enable the device's Reduce Motion preference and confirm these transitions stop.

Validation: `npm run check:map`, `npm run build:map`, inline JavaScript syntax check, and `git diff --check` passed. Phone preview was exercised for dock collapse/expand, sheet expansion, and layer tray open/close.

## What's left

Changes are local for visual review. A production release was not requested in this task.

## Files touched

- `web/index.html`
- `web/coastal.css`
- `web/sw.js`
- `docs/handoffs/2026-09-22-mobile-motion.md`
