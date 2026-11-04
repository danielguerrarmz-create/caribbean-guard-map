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

## Release outcome and tile-build follow-up

- PR #14 merged to `master` as `8bf2b2efa46fce8d99551fb9ea62af5f19464774`.
- Production deployment `dpl_55mUbqVwt7oDaZgat8Usoo3FDU8f` is Ready at `https://caribbean-guard-ehyyobta9-danielguerrarmz-create11.vercel.app`, serving the primary alias above. Main document, worker, styles, sign module/registry, access data and representative imagery match local SHA-256 hashes. Browser verified the live Rescue Station, draft sign link and Legend.
- Official website PR: `https://github.com/TommasoRibaudo/caribbeanguard-org/pull/5`, left for owner review and merge.
- That website's first remote preview failed. The cloud tile-generation path exposed a reproducible audit failure: version queries were treated as filenames, and unused icon-source folders were required in the precache. The audit now resolves versioned filenames and checks declared assets plus launcher icons. Three Python regressions preserve missing-file and missing-launcher rejection. This tool-only correction is synchronized to both repositories; it does not change the already-deployed map assets.
