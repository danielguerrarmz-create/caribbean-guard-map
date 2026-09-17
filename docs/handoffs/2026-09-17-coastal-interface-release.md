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

Deployment is performed from `web/` with local generated imagery. The result and live checks are appended after the host confirms readiness.

## Working-tree boundary

The pre-existing automatic handoff edit in `docs/handoffs/2026-09-17-auto.md` is left untouched and excluded from this release commit. Local Vercel authentication/link metadata, generated tiles, build output and original source PDF are not committed. The reduced annotated background and extracted JSON are included because the source viewer requires them.
