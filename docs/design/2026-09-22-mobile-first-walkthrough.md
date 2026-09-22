# Mobile-first walkthrough, 22 September 2026

Preview: 390 × 844 CSS pixels. Stress check: 320 × 568. Three paths were exercised in the live in-app browser against the local Vite preview.

| ID | Perspective and path | Finding | Change and verification |
| --- | --- | --- | --- |
| M1 | Local: open the beach list, inspect Playa Negra, return to the map | The coastal forecast disappeared entirely from the default phone view. A resident could read beach status without seeing the regional conditions. | The dock now shows the forecast before the beach list. At 390 × 844, its four metrics, regional scope, source and model time are visible without opening another view. |
| M2 | Local: repeat the path at 320 × 568 | The forecast and fixed dock chrome consumed all list space, leaving no complete beach entry. | Short phones use a compact forecast while keeping the full explanation in the expanded list. Two complete beach entries are visible in the initial 320 × 568 check, and the list remains scrollable. |
| M3 | Tourist: select Playa Cocles and read the safety instruction | In the initial sheet, the full-width emergency action pushed the rip-current advice below the bottom edge. | The emergency prompt and `tel:911` action share a row at phone widths, with the button still 44 px tall. At 390 × 844, the rip-current heading and complete instruction enter the opening sheet. |
| M4 | Tourist: repeat at 320 × 568 | The short peek cut off the emergency action itself. | The short-phone beach sheet opens at full available height with its own scroll. The emergency button is visible immediately. |
| M5 | Guard: open map layers, toggle rip currents, return to the map | The top-anchored expanded legend filled nearly the entire space between header and dock, obscuring the map while editing layers. | The layer panel expands upward from the bottom on phones. The map remains visible above it; the rip-current checkbox changed state and restored correctly. |

Checks that did not expose a new defect: EN-to-ES switching kept the Cocles sheet open with translated safety text; the emergency link remained `tel:911`; `See all` revealed every beach and the full forecast; the expanded sheet scrolled to its weather and source content. External Directions and Report actions were inspected by destination without activating them.

The overview map at 320 × 568 is necessarily sparse at coast-wide zoom. The list remains the primary way to choose a beach at that size. Geographic annotation accuracy remains provisional as documented in the map-system review; this walkthrough changes layout, not coordinates or safety classifications.
