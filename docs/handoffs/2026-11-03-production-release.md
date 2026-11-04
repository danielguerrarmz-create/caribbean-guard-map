# Coastal interface production release

Date: 2026-11-03

## What changed

PR #11 merged the reviewed responsive coastal design into master (1f9679b). All beach, rescue, access, Legend and forecast routes share connected panels. Map symbols, collisions, currents, coastal risk tint and loading motion follow the approved direction. Lifeguard reports remain a separate concept.

Production browser verification found an upgrade-path failure: new network-first HTML could receive cached unversioned geometry and symbol scripts from an older worker, preventing initialization before the new worker registered. Application bootstrap scripts and styles now use matching versioned request/cache keys. The static packager validates their local paths without the query. The cache is v71.

## Validation

72 Node tests, copy guard and static packaging (549 offline references). Secret scan and production dependency audit. The primary and mirror deployment code and sampled tiles matched release bytes; returning-browser verification identified and prompted the cache fix above. Physical phone GPS/offline checks remain separate.

## Deployment and rollback

Primary: https://web-five-beta-p7wt9cgwmf.vercel.app/
Mirror: https://caribbean-guard-map-6sqm.vercel.app/
Before this release, primary deployment was dpl_9wsZZJ8EAzHtaKMueq446KrKhMPN at https://caribbean-guard-6z88as2v0-danielguerrarmz-create11.vercel.app .

Publish complete web/ with local ignored tiles, following docs/deploy.md. Git-only builds intentionally skip. No domain changes or store submission.

## Files touched by cache follow-up

web/index.html, web/sw.js, tools/build_map.js, tools/tests/cache-upgrade.test.mjs, tools/tests/lifeguard-hours.test.mjs, docs/deploy.md and this handoff.
