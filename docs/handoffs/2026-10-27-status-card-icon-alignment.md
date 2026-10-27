# Beach status icon alignment, 27 October 2026

## What changed

The shared beach status card now centers its icon vertically beside the risk label, instruction and optional lifeguard-hours line. The service-worker cache is `cg-map-v48-status-icon-center` so returning visitors receive the new CSS.

## Why

The icon was pinned to the top of a three-row grid, which made it sit high beside some beach instructions. One shared CSS rule renders every assessed beach panel in both languages.

## How to verify

- `npm run check:map` and `npm run build` pass; the package validates 539 offline assets.
- The production CSS and service worker match local SHA-256 hashes on both Vercel aliases.
- In the live desktop browser, all five assessed beach panels in Spanish and English computed `align-self: center`; the icon and text-group centers were within 1.5 CSS px. Playa Grande and Manzanillo have no status card because they remain unassessed.
- Primary: `https://web-five-beta-p7wt9cgwmf.vercel.app/`, deployment `dpl_3PbG5rnQYkM1Dw4SuaK3TxQUBRwB`.
- Mirror: `https://caribbean-guard-map-6sqm.vercel.app/`, deployment `dpl_33rVjPn1eJuQWJcHGtJsLcL3mLTb`.
- Application source commit: `c82def3`.

## What's left

Visual confirmation on a physical iPhone remains open. A returning browser may show its saved version until the in-app **Actualizar** prompt is used.

## Files touched

`web/coastal.css`, `web/sw.js`, and this handoff.
