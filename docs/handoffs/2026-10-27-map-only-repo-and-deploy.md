# Map-only repository and Vercel release, 27 October 2026

## What changed

- Removed the tracked `site/` Next.js subtree and obsolete website planning files and scripts from `caribbean-guard-map`.
- Made the root development and build commands target the map. Root Vercel Git builds are skipped because the satellite tile pyramid is intentionally ignored by Git.
- Made `web/vercel.json` explicitly static so the same complete map can deploy to both existing Vercel projects despite the legacy mirror's Vite preset.
- Kept the organization website in its separate repository, `TommasoRibaudo/caribbeanguard-org`.

## Why

This repository is the internal, current map tool only. The requested production address is `https://web-five-beta-p7wt9cgwmf.vercel.app/`, owned by the existing `caribbean-guard-map` Vercel project (`prj_it5kQJM4XVWkmDu3NjEzGOfCcRc3`). Deploying from `web/` includes the local imagery that a Git build would omit.

## How to verify

- `npm run check:map` passes.
- `npm run build` validates 539 offline assets and packages `dist-map/`.
- The four Node test files pass 16 tests; the Python coast tests pass four tests.
- Preview deployment `dpl_AjFw6CzC2LbCasTFvtDpsrEHkwQ5` is Ready. `coastal.css`, `sw.js`, `data/coast-bands.geojson`, a local font and a representative z13 tile match the local source byte for byte. Vercel adds a preview-toolbar script to the served HTML.
- Primary production deployment `dpl_9pJ4uu72JmsbqZWbeeSrPhtwdTmY` is Ready at `https://web-five-beta-p7wt9cgwmf.vercel.app/`. Its document, CSS, worker, coast bands, font, logo and representative z13 tile match local SHA-256 hashes. The document reports the map title and `cg-map-v47-option-b-type` worker; `/?z=cocles` and `/?p=est2` return 200, while the old website route `/team` returns 404.
- The former repo-root project now serves the same map at `https://caribbean-guard-map-6sqm.vercel.app/` from production deployment `dpl_6F3GaQkLRaPxStoDYbv8FF8SMwvf`. Its document, CSS, worker, coast bands and representative tile match local SHA-256 hashes.
- Before release, the primary alias pointed at `dpl_wVRFQiaEyViw9muVYfSLVaegRuWi`; the former repo-root project pointed at `dpl_CpcS4JAtb693aA4PBetLS3vXUNeF`.

## What's left

- The coast rendering and iPhone safe area still need a human visual review on a physical device. The map's provisional geographic annotations still need field review.

## Files touched

`site/`, `docs/site-revamp/`, `tools/extract_site_copy.py`, `tools/make_placeholders.py`, `.gitignore`, `web/.gitignore`, `web/vercel.json`, `package.json`, `vercel.json`, `README.md`, `docs/deploy.md`, `tools/build_map.js`, `tools/export_overview.py`, and this handoff.
