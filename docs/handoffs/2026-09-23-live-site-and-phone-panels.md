# Live website import and phone panel rebuild, 23 September 2026

Branch `feat/live-site-merge`, local only. Nothing pushed or deployed.

## What changed

- **Website swapped.** The Vite replica in `site/` is gone (with `vite.config.js` and `tools/build_site.py`). `site/` is now a git subtree of `TommasoRibaudo/caribbeanguard-org` at `28adfa6`, history kept. The upstream repository was not modified.
- **Mapa tab.** `site/src/components/layout/Header.tsx` links to `MAP_URL` (`site/src/lib/map.ts`, env `NEXT_PUBLIC_MAP_URL`, production alias by default). The desktop nav now switches in at 1400 px, because ten tabs plus Donar overflowed at 1440.
- **Root build.** `npm run dev`/`build` run the Next.js site; `npm run setup` installs both. Root `vercel.json` builds `site/` and serves `site/out`, keeping the `/mapa` redirects.
- **Phone panels** (`web/index.html`, `createPanel`): dock and sheet sit at full height and move by `translate3d`; the whole panel is the grab area; at the top stop the list scrolls and a pull down from its first row lowers the panel; release projects the flick 200 ms and settles on a spring (response 0.34 s, damping 0.86) that starts at finger velocity; ends rubber-band. Detents are cached per measure: a per-frame read cost 110 ms of forced reflow at 6x CPU.
- **History.** Opening a sheet pushes one entry, closing pops it, Forward reopens the beach. Deep links land on the map first. No entry is pushed before the first user gesture (Chrome's history intervention).
- **Polish.** Sentence-case layer toggle, lighter eyebrow tracking, smaller scale bar, compact landscape-phone rail, org links open in the same tab. `sw.js` is `cg-map-v29`.

## How it was verified

`npm run check:map`, `npm run build:map` (535 assets), `npm run build` in `site/` (15 routes). Scripted touch walkthroughs at 390x844, 360x740, 375x553 and 844x390: every beach card opens its own sheet and address, close, Back, Forward, rapid open/close (history length constant), language switch with a sheet open, layers tray, saved-copy sheet. Frame pacing at 6x CPU: median 16.7 ms. Gojo reviewed the engine; its eight findings are fixed in the follow-up commit.

Not verified: a real iPhone or Android device, VoiceOver/TalkBack.

## Open

- The map's Vercel project must have Root Directory `web`; if it builds from the repo root it will now build the website.
- Drive-hosted images on the website did not render in the automation browser (they load via curl). Upstream concern, not changed here.
- Faint tile seams are visible on desktop imagery at some zooms; pre-existing.

## Previews (23 September, after review)

- Map preview (public): https://caribbean-guard-1smruw1t5-danielguerrarmz-create11.vercel.app, worker `cg-map-v36`, deployed from `web/`.
- Site preview (behind Vercel login): https://caribbean-guard-map-6sqm-29r8cjsnp-danielguerrarmz-create11.vercel.app, built with `NEXT_PUBLIC_MAP_URL` set to the map preview so its Mapa tab opens the new map. Deployed from the root with a temporary `.vercelignore` (only `site/`, `vercel.json`, `package.json`), removed afterwards.
- Production aliases untouched.

## Phone review round (23 September)

Daniel's seven items, all applied in `98d0aef`: equipment marks set on the beach (OSM along-coast correction plus a 15 m shoreline setback, `tools/project_full_annotations.py`), one panel at a time on mobile, Leyenda/Legend, Spanish default with remembered EN, forecast card rhythm and one-line footer, tighter brand pill, Poppins Bold as the heaviest weight.

## Rips, beach areas, stations (23 September, second round)

`45d381b`, `63f5098`. Rips are a channel plus seaward-flowing streaks (~23 px/s, linear, own pane, paused under motion and reduced-motion), 40 m offshore with 25 m minimum clearance. Beach bands show at z14+ and open on tap; names relocate to clear every pin. Stations use the logo's lifebuoy. 911 verified as Costa Rica's unified line. Playa Grande and Manzanillo have grey provisional bands (13d86f2), cut from the OSM coastline, dashed ends, until Caribbean Guard defines them.

## Round three (23 September)

`b3fbdd0`: legend parks the beach panel; legend pill matches ES/EN; places in five categories (`tools/data/place-categories.json`) with icons and a three-section legend; band joints share one edge; beach sheets drop the subtitle.

## Round four (23 September)

`fd8dcfd`: saved sheet shortened and platform-specific (iPhone Share steps, Android install button or menu steps), swipe to close; beach cards show straight-line distance from the reader (if location already granted and within 25 km) or from central Puerto Viejo; legend closes by swipe. GPS distances are untested in the field.
