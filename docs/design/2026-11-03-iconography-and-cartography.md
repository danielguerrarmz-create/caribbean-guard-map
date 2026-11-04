# Iconography, containers and hazard cartography

Update 2026-11-03: Daniel rejected both hazard treatments and their white outlines. Simplify the source rip drawings into one curve family and rebuild all arrowheads. Phosphor Regular remains selected. See `docs/design/2026-11-03-cartographic-precedents.md`; older cartographic recommendations below are superseded.

Date: 2026-11-03
Status: Research and visual comparison. Daniel approved the quieter overview direction. Daniel selected Phosphor Regular for its softer, thinner, less detailed character. The study now uses it; application rollout and cartographic decisions remain pending.

## Recommendation

Adopt **Phosphor Regular** for interface controls and ordinary amenities. Use one size / weight convention. Preserve Caribbean Guard's existing branded equipment mark until its simplified replacement has been reviewed. Treat the coast and rip arrows as cartography based on existing source geometry, rather than expecting a generic icon pack to draw them.

Use **fewer containers**, rather than replacing every rounded rectangle with a different shape. GPS, north, legend and other map actions should share a 44 px housing with a 10 px radius and a 24 px glyph. Ordinary rows and contextual information can use spacing and dividers without filled cards. Warning triangles, prohibition signs and equipment symbols retain their meaningful shapes.

For the coastline, prefer a **narrow reference-risk ribbon**, with explicit labels. For rip annotations, prefer **static, source-aligned red arrows with a pale casing**. A geographic outer border or a broad current channel can imply a measured hazard extent that the data does not support.

## Open-source asset research

| Library | Verified licence | Fit for this app | Decision |
|---|---|---|---|
| [Tabler](https://tabler.io/icons) / [source](https://github.com/tabler/tabler-icons) | [MIT](https://github.com/tabler/tabler-icons/blob/main/LICENSE) | Consistent 24-unit outline family, with swimmer, life ring, current location, compass, warning, water and place icons. Stronger strokes in the inspected 24 px samples | Heavier alternative retained for comparison |
| [Phosphor](https://phosphoricons.com/) / [source](https://github.com/phosphor-icons/core) | [MIT](https://github.com/phosphor-icons/core/blob/main/LICENSE) | Broad family and multiple weights, including a human swimmer. Regular appears lighter and more delicate in this comparison | Selected by Daniel for its softer, thinner, less detailed character; retain Regular weight and verify small-size legibility |
| [Lucide](https://lucide.dev/icons/) | [ISC, with MIT notices for inherited Feather icons](https://lucide.dev/license) | Clear general interface vocabulary. This selected sample has no corresponding swimmer, so navigation is explicitly shown as a non-equivalent example | Suitable, but less complete for this selected coastal vocabulary |
| [Maki](https://labs.mapbox.com/maki-icons/) / [source](https://github.com/mapbox/maki) | [CC0](https://github.com/mapbox/maki/blob/main/LICENSE.txt) | Small, solid map silhouettes: beach, swimming, information and hospital | Useful cartographic reference; avoid inserting its silhouettes randomly among outline controls |

These are assessments from the selected samples, not a benchmark of every icon in each library. Do not mix libraries by choosing each individual icon independently. The consistent stroke, optical size and simplification level are more valuable than an isolated clever glyph.

Tabler's official catalogue describes its 24 x 24 grid and 2 px stroke. The local comparison uses original downloaded SVGs, not hand-redrawn approximations. Raw SVGs suit the existing plain-JavaScript app and can be self-hosted for offline operation without introducing React or downloading an entire icon package.

### What is actually collected

- 28 SVGs and four complete licence files, 25,608 bytes combined at collection time.
- Exact upstream commits, source URLs and SHA-256 hashes in `symbol-study/assets/manifest.json`.
- Files validated as SVG, with no scripts, event handlers, external references or foreign-object content in the collected sample.
- `tools/collect_icon_study.py` reproduces this bounded, pinned collection.
- MIT and ISC notices remain bundled. Maki's CC0 text is also retained. No paid assets or subscriptions.

### Asset mapping

| App role | Selected Phosphor Regular asset | Semantic constraint |
|---|---|---|
| Locate me | `crosshair` | Button name explains GPS action; denial and loading states are separate |
| Orientation | `compass` | Need a clear north cue; do not imply live device heading without supported sensor data |
| Rescue equipment | `lifebuoy` | Means equipment, not an on-duty lifeguard. Study alternative only; brand mark decision remains open |
| General caution | `warning` | Always paired with the actual instruction |
| Swimming context | `person-simple-swim` | Never use alone to imply permission to enter the water |
| Swell / water context | `waves` | Not a rip-current location symbol and not a live measurement |
| Location | `map-pin` | Avoid using a place pin for an entire hazard area |
| Information / legend | `info` | Consistent glyph weight inside the same control housing |

A lifeguard-dependent instruction needs a distinctly understandable symbol and text. A generic life ring is not an acceptable shortcut for staffed supervision. A prohibition needs a clear prohibition sign and wording; do not label an ordinary swimmer icon “no swimming.” Library glyphs are not certified safety signs.

## Container continuity

| Role | Treatment | Reason |
|---|---|---|
| Map actions | 44 x 44 px, radius 10 px, icon 24 px | GPS and north stop looking like a separate product |
| Paired language controls | Same height and outer radius, shared divider | One related control group |
| Main sheet | One continuous surface, rounded top corners on mobile | The panel owns the container; every paragraph does not need another |
| Beach row | Unboxed glyph, title, instruction and quiet distance; bottom divider | Improves scanning without a row of competing circles |
| Equipment on map | Small, consistent high-contrast backing; visible glyph distinct from warning | A geographic mark can remain smaller than a control, but interaction needs an adequate target and overlap resolution |
| Warning / prohibition | Preserve triangle / prohibition silhouette | Semantic exceptions give shape a purpose |

Do not standardize visual map markers at 44 px each: they would cover the coast. Separate visible mark size from the touch strategy. Closely overlapping targets need a deterministic picker or another explicit interaction, not invisible overlapping 44 px boxes. Confirmed equipment is retained under the current visibility rule; this study does not authorize clustering it away.

## Rip currents: communicate the source, not simulated water

NWS describes rip currents as narrow seaward flows and documents multiple types and appearances ([science reference](https://www.weather.gov/safety/ripcurrent-science)). This is useful for understanding a directional symbol, but it does not validate Caribbean Guard's individual annotations.

The repository's projected rip features include `registration: pdf_direction_osm_shore_anchor` and `needs_confirmation: true`. That supports a mapped source annotation. It does not establish a measured velocity, live activity, channel width or a complete inventory of possible rips.

### Recommended representation

1. At beach scale, follow the existing source path and endpoints. Use a clear open head and restrained shaft. The comparison uses a 3 px red stroke, `#b62d42`, over a 6.5 px pale casing, `#fff8eb`.
2. The calculated color-pair contrast is 5.77:1. This checks red against its casing only, not every part of the map or every device. [WCAG's non-text contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) identifies a 3:1 threshold for required graphical information and discusses the weakness of very thin marks.
3. Keep the resting arrows static. If selection is animated, briefly emphasize the selected mark without marching particles or pulsing “live” behavior. Honor reduced motion.
4. Name the layer “Mapped rip currents.” On selection, show approximate source status and evidence. Do not imply that unmarked water is clear.
5. At coast scale, individual arrows become unreadable. Prototype a beach-associated hazard indicator with a clear zoom-in action. The study omits individual arrows below zoom 14 solely to demonstrate scale behavior; a complete overview aggregation and its explanation are still required.

### Alternatives considered

| Option | Advantage | Problem / decision |
|---|---|---|
| Existing thin red arrow | Very little visual mass | Weak separation over variable imagery; head and shaft can be hard to parse |
| Red arrow with pale casing | Stronger outline across dark water and busy shore | Recommended; compare casing width on device so it does not become a sticker |
| Broad translucent current channel | Easy to notice | Suggests unsupported width and affected water extent. Reject for this dataset |
| Animated particles / flowing dashes | Visually vivid | Can imply live flow, speed and direction. Reject as the default |
| Warning pin only | Compact and conventional | Loses the authored directional information. Use only as a scale-dependent summary, not the only detail representation |

An educational rip-current diagram can explain circulation separately from the geographic map. Do not add generic feeder currents to the real coastline merely because a teaching diagram includes them.

## Beach danger treatment

The current implementation uses a low-opacity display corridor, a dashed offshore edge and a colored shoreline. The user refers to this as the hatched outline; the new study includes an actual sparse diagonal hatch alternative. Neither the existing display buffer nor its hatch constitutes a surveyed danger boundary.

### A. Reference ribbon: recommended

- Use a fixed screen-width strip following the existing shoreline; the first study uses 5 px color inside a 9 px pale casing.
- Keep the same width across risk classes. Width should not imply a measured probability or hazard distance.
- Place an explicit label beside the selected beach: “High reference risk,” “Moderate reference risk,” “Caution,” or “Not assessed.” Preserve the existing entry instruction separately.
- Keep a neutral, distinctly labeled unassessed state. No green checkmark or “safe” wording.
- At lower zoom, simplify the line while retaining readable beach labels. At higher zoom, the strip remains a graphic locator instead of growing into a wide swath of purported dangerous water.
- The comparison still requires further visual tuning. Its casing is deliberately legible, and can be reduced if it starts to resemble a road route.

### B. Sparse hatching inside the existing corridor: viable alternative

- Preserve the generated polygon; use a sparse, screen-space pattern with a constant pitch, not dense crosshatching.
- A solid shoreline locates the beach. Keep the outer edge very quiet and explicitly explain that it is a display band.
- Do not encode severity solely through hatch density. Text and a clear symbol must survive grayscale and low vision.
- This shows the risk area more strongly but still risks implying that water outside the band is safer. It is my second choice for a consumer app.

### C. Full offshore wash / gradient: reject

Large red or amber gradients can look polished in a static mockup but obscure reefs, make layer overlaps muddy, and imply continuous risk estimates that do not exist. Use transparency only as secondary emphasis; no heatmap without an actual measured or modeled field and a defensible legend.

Do not convert these classifications to beach-flag icons. Physical beach flags already carry operational meaning. For example, RNLI explains red-and-yellow supervised swimming areas and red no-entry warnings ([flag context](https://rnli.org/water-safety/beach-safety)). This app's standing classifications and schedules are not equivalent to a flag currently flying at the beach.

## Review artifact and next application

Open http://127.0.0.1:5196/ while the app asset server remains on http://127.0.0.1:5174/. Switch the three treatments, toggle grayscale and rip arrows, zoom, and compare icons at 24 / 20 / 16 px. The baseline is an isolated approximation using the existing band geometry and arrow renderer, not a pixel-exact copy of the full app: roads, access markers and other evidence layers are deliberately absent.

The comparison's source geometry is read-only. Equipment glyphs are non-interactive study marks, not completed accessible app controls. The study does not solve label collisions or certify cartographic accuracy.

Next: apply the selected Phosphor Regular family to one complete control set, then implement the symbol legend and selected / focus / disabled states. Review all seven beach classifications, map scales, Spanish / English, reduced motion, sunlight, phone safe areas and color-vision simulations before a complete rollout.

## Burondono record

The unmodified source assets, licence files and manifest are copied to `burondono-design-system/docs/references/icon-study/` as research assets. The generic treatment and container principles are recorded with the intake. No new package export, global brand token or production-ready component is claimed. Completed refinements belong in their normal package locations with consumer provenance and validation.
