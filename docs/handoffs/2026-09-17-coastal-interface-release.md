# Coastal interface release - 17 September 2026

## Scope

User authorized commit, push and deployment of the reviewed map changes. Source branch: `codex/coastal-interface`, based on `f664e43` (the existing `feat/ui-overhaul` head). This release preserves that history and does not merge PR #1 into master.

Includes compact mobile/desktop navigation, the unchanged Caribbean Guard logo, large beach-status pictograms, separate lifeguard labels, a persistent map key, a zoom-responsive metric ruler, and a full annotated document viewer. The source reconciliation changes four station numbers, identifies station 3.3 as proposed and labels the strong-current bay. Geographic geometry is unchanged.

The new source viewer retains uncertain annotations in PDF-page coordinates. Duplicate 4.1 and undefined facilities remain flagged. Field sign-off and additional geographic alignment are outstanding.

## Documentation

- [README](../../README.md): setup, paths, entry points, provenance and regeneration.
- [Deployment guide](../deploy.md): existing Vercel target, checks, cache behavior and rollback.
- [Interface audit](../design/coastal-interface-audit.md): brand decisions and initial responsive work.
- [Icon and source review](../design/icon-system-and-source-review.md): vocabulary, feature inventory, crosswalk and unresolved source questions.

## Validation before deployment

- Safety-copy checks passed: nine banned-word rules, eight tier labels, five sheet-renderer deferral checks.
- Packaging passed and verified all 537 critical/optional offline asset references exist locally.
- JavaScript syntax checks and Git whitespace checks passed.
- Previous browser review covered desktop and 390 x 844 mobile, selection, proposed station detail, permanent legend and source view.
- Source assertions confirmed unchanged geographic geometry, correct crosswalk, 320 extracted features and preservation of the duplicate station number.
- Worker version: `cg-map-v9`. Annotated JSON now uses the same URL as its offline precache entry. Both HTML routes have explicit revalidation headers.

No claim is made of a real-phone airplane-mode test or field safety validation.

## Deployment record

Target: `caribbean-guard-map` in team `team_XOr1KdFeEvqhDcHZMsmeoLA6`, project `prj_it5kQJM4XVWkmDu3NjEzGOfCcRc3`.

Previous Ready production deployment (rollback target):
https://caribbean-guard-q409yajva-danielguerrarmz-create11.vercel.app

Existing production alias:
https://web-five-beta-p7wt9cgwmf.vercel.app

Deployed from `web/` with local generated imagery. Vercel confirmed **READY**, target **production**, on 17 September 2026.

- Application commit: `34c0486` - Redesign coastal map interface and reconcile annotated source.
- Pushed branch: `origin/codex/coastal-interface`.
- Deployment ID: `dpl_DyUsfQR1wXJ4Nc5Doxj8oiab1vDt`.
- Immutable deployment URL: https://caribbean-guard-pr0ne1v4s-danielguerrarmz-create11.vercel.app
- Production alias: https://web-five-beta-p7wt9cgwmf.vercel.app
- Annotated view: https://web-five-beta-p7wt9cgwmf.vercel.app/source-map.html

### Live verification

Twelve release assets returned HTTP 200 with appropriate content types and SHA-256 byte equality against local files: both HTML documents, coastal.css, symbols.js, source-map.js, sw.js, cg-hazards.geojson, full-map-source.json, full-map-background.jpg, the original logo, Leaflet JavaScript and a representative z11 tile.

Production browser checks confirmed the desktop interface and 390 x 844 mobile proposed-station view. Station 3.3 displayed the proposal statement with zero Directions links. The source view loaded and its roads/access and location toggles worked. The permanent legend and scale were visible, and the browser displayed a saved-copy timestamp. This confirms online rendering and cache-install feedback, not airplane-mode behavior. The Cocles deep link was also checked. Viewport emulation was reset afterwards.

This documentation follow-up records the completed deployment; it does not change deployed application bytes.

## Working-tree boundary

The pre-existing automatic handoff edit in `docs/handoffs/2026-09-17-auto.md` is left untouched and excluded from this release commit. Local Vercel authentication/link metadata, generated tiles, build output and original source PDF are not committed. The reduced annotated background and extracted JSON are included because the source viewer requires them.
