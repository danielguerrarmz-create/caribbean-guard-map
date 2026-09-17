# Caribbean Guard: coastal interface audit and implementation

17 September 2026 · Initial design audit; updated with the approved icon revision · `codex/coastal-interface`

Deployment status is recorded in [the release handoff](../handoffs/2026-09-17-coastal-interface-release.md). [The source review](icon-system-and-source-review.md) describes the subsequent PDF reconciliation. Screenshots below document the initial pass, before the icon revision.

## Recommendation

Make the map a calm, practical guide to this coast. The primary journey is **choose a beach → read its instruction → understand the reason → return to the coast**. A QR link enters directly at the second step. Brand character comes from the original logo, a consistent type hierarchy, ocean blue, warm paper, and straightforward language.

This is an implementation in the map repository, not a deployment or a rewrite of the separate organization website. The initial pass retained hazard data. The subsequent PDF review corrected station numbers, proposal status and the strong-current-area classification, while retaining geometry. Current beach records still require review by Caribbean Guard; the interface retains the existing review and deferral statements.

## What I reviewed

- [Current deployed map](https://caribbean-guard-mlhinxzqg-danielguerrarmz-create11.vercel.app/): live browser review, including the desktop list and legend.
- [Map PR #1](https://github.com/danielguerrarmz-create/caribbean-guard-map/pull/1): public change history and the local implementation at `f664e43` before this work.
- [Safeswim](https://safeswim.org.nz/): live homepage and map; existing local teardown used as supporting project context, not a new measurement of every Safeswim component.
- [Caribbean Guard website](https://www.caribbeanguard.org/): live header, logo, home content, navigation and imagery.
- [Organization website repository](https://github.com/TommasoRibaudo/caribbeanguard-org): current README, global styles, header component and repository tree. This is a Next.js project; it is separate from this workspace's static `site/` implementation.

## Findings and responses

| Finding | Effect on a resident using the map | Implemented response |
|---|---|---|
| The desktop legend occupies a second scrolling region beneath the beach list. | Basic navigation competes with a reference manual. | Use a compact, always-visible map key following user feedback. Show only the chosen language. |
| Desktop opens a second full-height panel on the opposite side. | The map loses much of its usable width, especially on laptops. | Details replace the beach list in the same 380 px left panel. |
| Raised cards repeat large, uppercase instructions throughout the list. | Everything looks equally urgent; comparing beach names is harder. | Use flat rows, modest separators and compact instruction text. Keep a larger instruction in the selected beach. |
| Mobile selection uses a horizontal carousel. | Offscreen beaches require a less obvious navigation gesture. | Use a vertical list with an explicit See all / Show map control. |
| Regional model numbers appear above the main task. | They attract attention before beach selection and can look like local observations. | Move the forecast into a disclosure after the list, preserving its model/source labels. On mobile it appears in the expanded list. |
| The map's header uses a text name without the existing logo. | It feels disconnected from the organization. | Self-host the original logo, unchanged, in a consistent header. |
| Tight map pan limits cancel the mobile panel's camera offset at low zoom. | The selected shore sits under the detail sheet. | Use the existing wider tile-coverage bounds at low zoom; keep tight detail coverage at high zoom. |

Safeswim's most useful contribution is a stable division between navigation, map, and selected-place information. Its broad search/filter/navigation surface suits its larger coverage. Caribbean Guard currently has five named beach records; a readable list is simpler than adding search and filters now. The redesign retains satellite imagery and the existing patterned safety lines because changing them would alter this project's mapping approach as well as its interface.

## Brand system

| Role | Decision |
|---|---|
| Logo | Existing website PNG, byte-for-byte download; no tracing, recoloring, cropping or redesign. |
| Main ink | `#132F3C`, deep navy; headings and selected instruction card. |
| Main surface | `#FFFEFA`, warm white; readable without a clinical pure-white appearance. |
| Secondary surface | `#F4F3EC`, pale sand; offline/reference toolbar. |
| Interactive accent | `#126780`, ocean blue; secondary controls and small geographic heading. |
| Secondary text | `#536974`; descriptions and metadata. |
| Typography | Existing self-hosted Inter, weights 400 / 600 / 800. One family, consistent spacing and a distinct heading/instruction/body hierarchy. |
| Geometry | Flat list rows; 6–10 px control/card radii; rounded mobile sheet. Remove heavy repeated shadows. |
| Safety palette | Existing red, amber, green and patterned strokes remain semantic map information. Never turn the lower-risk instruction into a green permission card. |

Logo source: [original website asset](https://images.squarespace-cdn.com/content/v1/6658cf433f03af778644f50f/fc04cf74-fd0a-4c71-a1e5-e96955c89ace/Logo.png?format=1500w). Stored at `web/icons/caribbean-guard-logo.png`, approximately 17 KB. The image includes its existing lettering; the adjacent text identifies the product in a readable size.

For the organization website, extend these same tokens and type roles, use real community photography, and group navigation into Our work, About, Get involved, Map, and Donate. That is a recommended next application of the system, not a change made to the other repository in this task.

## Responsive behavior

- **Desktop, 820 px and above:** persistent header, one left panel, map in the remaining visible area. Selecting a beach replaces the list; close or Escape restores it and the coast overview.
- **Mobile:** map above a bottom beach list. See all expands the list. Details start at 56% of viewport height; Show more expands beneath the header. Scrolling still works inside either panel. Visible expand buttons complement the existing drag gesture.
- **Language:** both ES and EN remain available in the header. The open detail updates in place; selection is retained after rebuilding translated rows.
- **Supporting information:** the map key is permanently visible; offline information uses the detail panel. The forecast remains explicitly regional and model-derived.
- **Accessibility:** retain focus outlines, descriptive control names, 44 px main controls, inert hidden navigation, close/Escape behavior and a focus-return fallback after language changes. Reduced-motion users receive no sheet transition.

## Implementation and local review

`web/coastal.css` contains the new visual layer. `web/index.html` adds the original logo, simplified panel controls and state handling. `web/sw.js` includes the new CSS/logo in the critical cache and increments the cache version. The older embedded styles remain as the underlying map/component styles; this is an additive, reviewable redesign rather than a framework migration.

```sh
npm run dev:map      # http://127.0.0.1:5174/
npm run check:map    # existing safety-copy regression checks
npm run build:map    # static deployable package in dist-map/
```

The default `npm run dev` and `npm run build` still target `site/`. Map packaging copies the original static assets intact so classic scripts, relative tile URLs and the service worker remain together. Tiles are generated assets excluded from Git; they must exist locally before packaging.

## Verification and limits

- `npm run check:map`: passed all existing copy rules, eight tier labels and five sheet-renderer deferral checks.
- `npm run build:map`: passed. Inline application JavaScript and worker syntax checks passed; all 529 referenced cache asset paths exist locally.
- Browser review at 320 × 568 and 390 × 844 phone sizes, and desktop layouts including 1024 × 768 and the default approximately 1280 × 720 viewport.
- Confirmed mobile list expansion, selected beach expansion/collapse, English/Spanish switching on Cocles, and the `?z=cocles` QR entry.
- Checked all five English beach detail pages for guidance, review status and emergency links. Spanish interaction was also exercised, but the first batched test timed out before returning its full result; no all-Spanish automated pass is claimed.
- Confirmed no document horizontal overflow at 320 px and 390 px. Verified Cocles' label above the mobile sheet after the camera correction.
- No real emergency calls, email messages, location permission grants, or deployments were performed.
- Real iOS/Android hardware, sunlight readability, assistive-technology testing and a disconnected offline session remain field checks. Browser viewport emulation does not establish those results.
- Content sign-off and imagery licensing remain release dependencies documented by the existing repository; a visual redesign does not resolve them.

Screenshots: [desktop](coastal-interface/desktop.png), [mobile overview](coastal-interface/mobile.png), [mobile beach detail](coastal-interface/mobile-detail.png).

## Resident validation to run next

Ask several local residents to find Cocles, explain its instruction, switch languages, find another beach, and identify whether the information describes today's observed conditions. Include an older resident and a person using a small phone. Observe hesitation and wrong interpretations, not just aesthetic preference. In particular, validate the clarity of the review statements, the See all control and the separation of a regional forecast from beach guidance before public rollout.
