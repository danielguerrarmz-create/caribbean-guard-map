# Deploying the safety map

## Website and map are separate Vercel projects

The organization website at `https://caribbean-guard-map-6sqm.vercel.app/` is deployed from the repository root. Since 23 September 2026 it is the Next.js site in `site/` (a subtree of the live caribbeanguard.org repository); root `vercel.json` installs and builds it and serves `site/out`. Its `/mapa/` route redirects to the safety map project at `https://web-five-beta-p7wt9cgwmf.vercel.app/`. Deploying the website does not publish map changes or its ignored satellite tiles. Deploy the website from the repository root and the map from `web/` when both have changed. Verify the website route and the map's worker version after both releases.

## Existing target

The map is a static Vercel project. Deploy **`web/`**, not the repository root or the `site/` website.

- Project: `caribbean-guard-map`
- Project ID: `prj_it5kQJM4XVWkmDu3NjEzGOfCcRc3`
- Team scope: `team_XOr1KdFeEvqhDcHZMsmeoLA6`
- Existing production alias: https://web-five-beta-p7wt9cgwmf.vercel.app
- Current deployment record: [22 September map release](handoffs/2026-09-22-map-production-release.md)

The local `web/.vercel/project.json` may still contain the historical name `web`; its project ID is authoritative. Do not create another project to resolve the stale name. `.vercel/` is ignored and must not be committed.

## Prepare

Install dependencies with `npm ci`. Ensure `web/tiles/` exists; generated imagery is intentionally excluded from Git. On a fresh checkout run `python tools/build_tiles.py` with its dependencies and network access. Missing imagery produces an incomplete map even if HTML serves successfully.

```powershell
npm run check:map
npm run build:map
```

Packaging validates every service-worker asset reference before copying the map into `dist-map/`. The production CLI command below uses the source `web/` folder, including its local tiles. `npm run build` targets the separate organization site and is not the map deployment command.

## Publish to the existing project

Install the official Vercel CLI and sign in if needed. From the repository root:

```powershell
Set-Location web
vercel project inspect caribbean-guard-map --scope team_XOr1KdFeEvqhDcHZMsmeoLA6
vercel deploy --prod --yes --scope team_XOr1KdFeEvqhDcHZMsmeoLA6
```

Omit `--prod` to create a preview instead. The team scope is required with this account. Record the resulting deployment URL, deployment ID, source commit, production alias and validation in the release handoff. Do not record tokens or authentication files.

Do not replace this with a Git-only deployment without adding imagery generation to that build: Git does not contain the tiles.

## Verify after publishing

1. Confirm Vercel reports Ready and lists the expected production alias.
2. Check `/`, `/coastal.css`, `/symbols.js`, `/sw.js`, the geographic map JSON files, logo and representative tiles return successful responses with suitable content types.
3. Open the production URL at desktop and phone viewport sizes. Check the compact heading, status cards, collapsible map key, scale and beach selection.
4. Test `/?z=cocles` and `/?p=est2`. The latter must describe proposed station 3.3 and must not offer directions as if it were operating equipment.
5. Expand the key and toggle each annotation layer on the GPS map. Projected positions must be described as approximate, with proposed equipment kept distinct from available equipment.
6. For returning visitors, use the update prompt. On a real phone, let assets finish saving, enable airplane mode and reload the map. Document this separately from desktop emulation; do not claim a field offline test from HTTP checks alone.

## Cache behavior

`web/vercel.json` and Cloudflare fallback `web/_headers` carry corresponding response rules. The map document and worker revalidate. The service worker uses network-first document requests with an offline fallback and cache-first assets with background revalidation. Its version must change for a coordinated interface/data release.

Critical assets include the main interface, symbols, fonts, projected annotation data and overview tiles. CSS precaching explicitly requests `text/css`, including during Vite development.

Tiles and icons have long-lived immutable URLs. If their bytes change, use a new filename/prefix and update references and cache lists. Do not silently replace imagery under old tile URLs.

## Rollback

Record the current production deployment before publishing. If validation fails, restore that deployment through Vercel's deployment controls or the official CLI:

```powershell
vercel rollback <previous-production-deployment-url> --scope team_XOr1KdFeEvqhDcHZMsmeoLA6
```

Inspect the resulting production alias and recheck the main document and imagery. Existing installed clients can retain an older worker until they reconnect and update; a server rollback does not instantly erase device caches. Prefer a forward fix with a new worker version when cached assets need coordinated replacement.

## Domain and field release

No custom-domain or DNS changes are included in this release. `mapa.caribbeanguard.org` remains an intended future address, subject to ownership and DNS access. Confirm a durable address before printing permanent QR codes. Deployment does not establish field accuracy, lifeguard sign-off or imagery rights.

Cloudflare Pages remains a static-host fallback using `web/_headers`; upload the complete `web/` contents with generated tiles if that migration is explicitly requested.
