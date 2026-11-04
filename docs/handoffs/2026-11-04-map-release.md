# Map release, 4 November 2026

## What changed

- Desktop detail routes now fade their contents in a fixed sidebar. Mobile directional navigation and swipe Back remain intact.
- Rescue station names and symbols no longer show public station numbers; existing IDs and deep links remain stable. Group badges still indicate counts.
- Added registry-backed poster links and a mapped Calle Merlin trailhead candidate, clearly marked draft and awaiting field confirmation. No printed poster is approved or distributed.
- Preserved the latest upstream unreviewed-beach notice and offline-cache fixes. Bootstrap assets and service worker are coordinated at v75.

## Verification

- All 90 map tests pass, including route motion, mobile gestures, cache upgrade/failure, QR resolution and unknown/retired sign records.
- Copy checks pass. Offline packaging verifies 551 references, including locally generated tiles.
- Secret scanning of release commits passes. Desktop and mobile navigation were reviewed during the preceding design passes.

## Publication scope

Daniel authorized merging the map repository default branch and a separate owner-reviewed PR for `TommasoRibaudo/caribbeanguard-org`. Both repositories name their default branch `master`.

The standalone map requires uploading the complete `web/` folder because generated tiles are excluded from Git. Production before this release: `dpl_3urgdPkQVCYPBcPKzrqbyiNFcGoE`, `https://caribbean-guard-g1gwz7yt1-danielguerrarmz-create11.vercel.app`. Primary alias: `https://web-five-beta-p7wt9cgwmf.vercel.app/`.

Poster PDFs, generators, local review artifacts and the pre-existing symbol study remain outside this release. Poster design, installation point, permanent print QR URL and higher-resolution imagery remain pending review. No lifeguard-report integration, live beach-specific current measurements, portfolio or Forsite changes are included.
