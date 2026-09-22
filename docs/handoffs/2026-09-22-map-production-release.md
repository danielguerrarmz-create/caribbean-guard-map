# Safety map production release, 22 September 2026

## What changed

The current map source on `master` was deployed directly from `web/` to the existing Vercel map project. Production deployment `dpl_cbYYTGxGmfQxZCFWmzkXrBqGc5Pr` serves `https://web-five-beta-p7wt9cgwmf.vercel.app/` with service-worker cache `cg-map-v26`. The previous production deployment was `dpl_DyUsfQR1wXJ4Nc5Doxj8oiab1vDt` with `cg-map-v9`.

## Why

Merging the map changes into Git deployed the separate organization website, but did not publish the map's ignored satellite tiles or update the map project. The website's repaired `/mapa/` route therefore opened the old map. The map project requires a deployment from the local `web/` folder with its generated tile pyramid present.

## How to verify

The map project reports the new deployment as Ready and aliased to production. `npm run check:map` and `npm run build:map` passed, with 535 offline asset references validated. Production returned 200 for the document, CSS, symbols, geographic annotations, mobile preview, and a representative z13 tile. Downloaded production bytes matched local SHA-256 hashes for `index.html`, `coastal.css`, `symbols.js`, `sw.js`, `data/full-map-geographic.geojson`, and `tiles/13/2210/3871.jpg`. Desktop and 390 × 844 mobile views loaded in the browser, including the icon-only GPS control and map-first bottom panel. The organization site's Map navigation reached the production map.

## What's left

Returning browsers with the older service worker may briefly show old cached styling until they use the in-app version-update prompt and refresh. GPS permission, physical-device offline behavior, and the provisional beach/current positions still require field checks. If rollback is needed, use the previous deployment ID above with the procedure in `docs/deploy.md` and recheck the public alias.

## Files touched

No application source changed in this release. This handoff and the documentation links to it record the deployment.
