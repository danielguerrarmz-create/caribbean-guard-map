# Map-only repository and Vercel release, 27 October 2026

## What changed

- Removed the tracked `site/` Next.js subtree and obsolete website planning files and scripts from `caribbean-guard-map`.
- Made the root development and build commands target the map. Root Vercel Git builds are skipped because the satellite tile pyramid is intentionally ignored by Git.
- Kept the organization website in its separate repository, `TommasoRibaudo/caribbeanguard-org`.

## Why

This repository is the internal, current map tool only. The requested production address is `https://web-five-beta-p7wt9cgwmf.vercel.app/`, owned by the existing `caribbean-guard-map` Vercel project (`prj_it5kQJM4XVWkmDu3NjEzGOfCcRc3`). Deploying from `web/` includes the local imagery that a Git build would omit.

## How to verify

- `npm run check:map` passes.
- `npm run build` validates 539 offline assets and packages `dist-map/`.
- The four Node test files pass 16 tests; the Python coast tests pass four tests.
- Preview deployment `dpl_AjFw6CzC2LbCasTFvtDpsrEHkwQ5` is Ready. `coastal.css`, `sw.js`, `data/coast-bands.geojson`, a local font and a representative z13 tile match the local source byte for byte. Vercel adds a preview-toolbar script to the served HTML.
- Confirm the production alias, map document, style, worker, coast bands, font, representative tile and deep links after release.

## What's left

- Merge the map-only PR, deploy `web/` to the existing production project and record the deployment ID and verified asset hashes.
- The coast rendering and iPhone safe area still need a human visual review on a physical device. The map's provisional geographic annotations still need field review.

## Files touched

`site/`, `docs/site-revamp/`, `tools/extract_site_copy.py`, `tools/make_placeholders.py`, `.gitignore`, `web/.gitignore`, `package.json`, `vercel.json`, `README.md`, `docs/deploy.md`, `tools/build_map.js`, `tools/export_overview.py`, and this handoff.
