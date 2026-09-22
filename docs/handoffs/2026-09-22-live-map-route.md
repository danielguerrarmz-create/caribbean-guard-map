# Live safety-map route repair

## What changed

The organization site now builds all eleven HTML pages instead of only its home page. Its Vercel `/mapa` and `/mapa/` routes redirect to the separate safety-map production alias. The map landing page's local call to action points to that alias. Site scripts are bundled as modules so the mobile menu works in the production build.

## Why

On 22 September 2026, `https://caribbean-guard-map-6sqm.vercel.app/` served the organization home page, but its Map navigation opened `/mapa/`, which returned `404 NOT_FOUND`. The site's Vite build emitted only `dist/index.html`. The separate map alias was reachable and showed the older `cg-map-v9` interface, while the current source uses `cg-map-v26`. These are distinct Vercel projects; the site deployment did not publish the current map.

## How to verify

Run `npm run build` and confirm all eleven pages, including `dist/mapa/index.html`, exist and the bundled site JavaScript is present. Confirm root `vercel.json` has both temporary external redirects. After the website deployment, request `/mapa/` and verify it redirects to the map alias with a successful map document. After a separate deployment from `web/`, verify `/sw.js` reports `cg-map-v26`, representative imagery tiles load, and the GPS map appears on mobile and desktop.

## What's left

The website route will continue to show the older map until the map project is separately deployed with its generated tiles. A durable custom map domain would replace the temporary Vercel alias later. No deployment was performed in this repair.

## Files touched

`vite.config.js`, root `vercel.json`, the eleven `site/**/index.html` pages, `docs/deploy.md`, and this handoff.
