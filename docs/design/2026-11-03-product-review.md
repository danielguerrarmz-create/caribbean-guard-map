# Caribbean Guard product review and design direction

Update 2026-11-03: Daniel rejected both hazard treatments and their white outlines. Simplify the source rip drawings into one curve family and rebuild all arrowheads. Phosphor Regular remains selected. See `docs/design/2026-11-03-cartographic-precedents.md`; older cartographic recommendations below are superseded.

Date: 2026-11-03
Status: Initial review and one-screen design proof. Not a completed redesign or store-ready release.

Update: Daniel approved the quieter overview layout on 2026-11-03. The next requested work is open-source icon research, container continuity and stronger rip-current / danger-band cartography. See [the research and comparison](2026-11-03-iconography-and-cartography.md).
Baseline: `origin/master` at `fbc65fa`. Working branch: `codex/map-visual-review`.
Distribution target: iOS and Android, confirmed by Daniel; desktop browser remains supported.

## Finding

The principal problem is hierarchy. Map equipment, beach guidance, forecast, source material and controls compete for attention. The same interface also mixes several generations of spacing and motion rules. More animation alone will not resolve this.

The first screen should answer: where am I looking, which beach do I need, what is its standing guidance, and where can I get help? Fine-grained source material belongs after that decision. Safety instructions must not require hover.

## Evidence and limits

- Inspected the live local application at 1280 x 720 and inside its existing 390 x 844 phone preview. Opened the coast overview, expanded beach list, Cocles details and desktop legend; exercised mobile beach selection, close and language switching.
- Inspected source for symbols, layout, label placement, panel springs, forecast rendering, service worker and PWA manifest.
- This is not an exhaustive audit of all beach and emergency states. Physical-device gestures, screen readers, offline installation, reduced-motion OS behavior, GPS permissions, large text and all intermediate widths remain unverified.
- The initial fresh worktree lacked ignored satellite tiles. Copied the existing local tile cache into the new worktree. No imagery was regenerated or uploaded.
- Browser snapshots after initial load show overlapping equipment and missing beach labels. The first collision pass hid labels before the pass intended to reposition them. Regression tests reproduced that defect before the fix.

## Component review and next implementation

| Surface | Finding | Direction / acceptance |
|---|---|---|
| Header and identity | Brand, language and emergency control have inconsistent containers | Retain the original logo and approved type pair; common control geometry, 44 px touch actions, visible focus; verify phone safe areas |
| Coast overview | Safety symbols compete with geography; some beach names disappear | Reserve separate visual roles for area guidance, equipment, paths and evidence; map labels should correspond clearly to their shore segments |
| Beach list | Small type and repeated bold status rows flatten hierarchy | Strong beach name, readable instruction, quieter distance; common inset and row spacing; preserve distance origin |
| Forecast summary | Large card and heading dominate the opening phone sheet | Compact three-column summary, direct forecast action, visible regional-model limitation; do not delay or hide beach selection |
| Beach details | Several cards restate related guidance and occupy most of the viewport | Establish one primary instruction, operational schedule context, then immediate help, beach context and forecast; retain uncertainty |
| Experimental guidance | Appears as another competing safety block | Review whether it earns its place in the primary flow; never imply observed beach conditions from regional weather |
| Rescue equipment | Overlapping rings, multiple number treatments; some map buttons have no accessible name | Preserve equipment identity and coordinates; refine outline, hierarchy and selected state; uniquely name each interactive marker |
| Rip-current annotations | Moving arrows can suggest measured water movement | Retain provenance; review static baseline and purposeful selected emphasis; no invented speed or live-current implication |
| Risk shoreline | Band, casing and stroke compete at different zooms | Review contrast and width on actual imagery at overview, beach and access scales; keep classification and geometry intact |
| Access and roads | Dense access symbols and road lines at detail scale | Tune visual priority by zoom; explicit approximate-source treatment and access limitations |
| Legend / layers | Mixes explanatory legend and layer controls | Separate what a mark means from visibility controls; improve selected states and touch targets |
| Evidence images | Distinct evidence markers add another map symbol family | Use an identifiable evidence glyph and consistent viewer behavior; preserve original images and attribution |
| Offline / install | Local preview deliberately disables service-worker saving | Review on a packaged origin: download progress, interrupted download, stale copy, retry and offline reopen |
| GPS and compass | Separate round controls; permission and error states not exercised | Shared sizing and focus; clear denied/unavailable/outside-region states; no prompt before the user requests location |
| Bilingual content | Spanish summary still uses “Swell”; some equipment labels remain English | Complete ES/EN state inventory; review terminology with the content owner; long text must wrap without clipping |
| Motion | Existing physics-driven sheets plus layered CSS transition rules | Keep a single owner for each transform; shared control timing; interruption tests and reduced-motion checks |
| Accessibility | Empty equipment button names observed; mobile proof is browser emulation | Audit names, focus restoration, keyboard access, contrast, target size and large text; verify VoiceOver/TalkBack on devices |

## Proposed visual system

- Keep Zilla Slab for identity / headings and Source Sans 3 for functional text. The 2026-10-26 type decision is already recorded in this repository.
- Use white and very pale neutral surfaces, dark coastal ink and restrained ocean blue for navigation. Hazard colors retain semantic meaning; they are not decorative brand accents.
- Use 24 px desktop and 20 px phone content insets, a 4 px spacing base, and a small set of container radii. Equal relationships matter more than forcing every element to the same padding.
- Give the map three scales: coast orientation, selected beach, precise feature inspection. Do not silently remove equipment or relocate geographic anchors to solve overlap. Any changed equipment visibility policy needs explicit design approval because prior source comments preserve confirmed equipment at every zoom.
- Favor brief state feedback and direct manipulation. Do not animate all content continuously or stagger essential instructions.
- Treat information density as a product decision: the first proof exposes two beach rows at mobile rest, compared with roughly one before. Larger readable desktop rows require scrolling at 720 px height. Review this tradeoff before generalizing it.

## First proof implemented

`web/coastal.css`: bounded overview styles for header controls, heading, list rhythm, forecast and map-label text; fine-pointer row feedback; reduced-motion CSS for the new transitions. Existing sheet springs remain unchanged.

`web/index.html`: eligible beach labels are reconsidered after an earlier collision pass; label boxes reduced from 190 to 136 px. Source geography and safety copy remain unchanged. The finite candidate search can still omit names at crowded coast zooms; this is not a complete map-label redesign.

`tools/tests/beach-labels.test.mjs`: hidden-but-eligible labels recover, colliding labels move, below-threshold labels remain hidden. The first two tests failed before the correction and all three passed after it.

Local review:

- Desktop: http://127.0.0.1:5174/
- Phone: http://127.0.0.1:5174/mobile-preview.html
- Evidence: `out/visual-review/overview-desktop.jpg`, `out/visual-review/overview-mobile.jpg` (local, ignored).

## References and design-system handoff

[Gabriel's post](https://x.com/gabriell_lab/status/2117611847805272267) describes secondary metadata disclosure. Its text was visible; the video could not play, so exact visual fidelity is unverified. Apply the principle only to secondary information, with touch and keyboard equivalents. Do not copy source code without checking its licence.

[Transitions.dev](https://transitions.dev/) provides relevant panel, disclosure and state-transition references. No code was copied or installed. Use existing local motion foundations and refine specific interactions after the overview direction is accepted.

Daniel requested reusable refined creator components also enter `danielguerrarmz-create/burondono-design-system`. Its local checkout now contains a source intake register under `docs/references/`, linked from `CONTRIBUTING.md`. Each completed component belongs in its normal package location with provenance, accessibility contract, tests and playground entry. No creator component has been extracted yet. Caribbean Guard branding must not overwrite Burondono's global font or color tokens.

## iOS and Android release work

This checkout contains a PWA manifest and service worker, not native iOS / Android application projects. Decide packaging after the product interaction contract is stable. A wrapper alone is not evidence of store readiness.

| Workstream | Evidence / next deliverable |
|---|---|
| Imagery | Source comments in `web/index.html` flag redistribution rights for the cached Bing imagery. Resolve documented provider rights and offline terms; this review did not determine the legal position |
| Data authority | Confirm ownership and update process for standing guidance, schedules, equipment and provisional annotations; label stale/unverified information consistently |
| Dependency maintenance | `npm audit` reports 4 affected development packages: 3 high, 1 moderate. Review a supported toolchain upgrade separately; no forced upgrade performed |
| Native integration | Choose packaging and document navigation, location permission, safe areas, external directions / phone links and persistent offline assets on both systems |
| Platform validation | Real iPhone and Android checks: first launch, airplane mode, permission denial, interrupted downloads, resume, rotation, accessibility and back navigation |
| Store submission | Prepare privacy disclosures, support and privacy URLs, accurate listing media, signing, review instructions and beta distribution |

Apple's [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) cover completeness, minimum functionality, privacy and rights. Google's [app setup guide](https://support.google.com/googleplay/android-developer/answer/9859152) covers app setup, signed bundles, testing and listing preparation. Requirements must be rechecked at submission; neither approval nor a date is promised here.

## Delivery sequence

1. Obtain visual direction approval on this coast-overview proof; record requested corrections.
2. Complete the map symbol and label system across coast, beach and feature scales, including selected / keyboard states.
3. Apply the accepted layout and content hierarchy to every panel and error / empty / stale state. Consolidate superseded CSS instead of continuing to stack overrides.
4. Refine motion, verify rapid interruption and reduced motion, and add proven reusable creator adaptations to Burondono with source credit.
5. Resolve release blockers, choose native packaging and run iOS / Android beta acceptance before requesting store submission approval.

## Verification for this proof

- 26 Node tests passed, including three new label-placement regressions.
- Copy checks passed.
- Map build passed, validating 546 offline asset references. This verifies packaging references, not offline browser behavior or imagery rights.
- Whitespace diff check passed.
- Desktop and 390 x 844 browser review completed for the stated flows. Not a physical-device or full accessibility sign-off.
- No commit, push, deployment, store submission or package publication.
