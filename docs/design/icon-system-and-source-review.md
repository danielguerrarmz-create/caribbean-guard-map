# Icon system and full-map reconciliation

Review date: 17 September 2026. Implementation and source review. Deployment status: [release handoff](../handoffs/2026-09-17-coastal-interface-release.md).
Source: `08102026_FULL MAP DRAFT.pdf`, user supplied, page 1. Source fingerprint and page coordinates are recorded in `web/data/full-map-source.json`.

## Interface changes

- Compact title and location; removed the draft paragraph from the title block.
- Beach cards contain a large status pictogram, name, action and separate lifeguard information.
- No-swim uses a prohibited-swimming symbol; conditional entry uses an exclamation triangle; lifeguard-dependent guidance uses a lookout pictogram; lower-risk guidance uses waves plus a caution mark. No icon asserts that today's water is safe.
- Rescue equipment uses a life ring on amber. Proposed equipment uses an outlined/dashed ring. A proposed CG facility uses a dashed building symbol. These do not imply staffing.
- A permanent map key replaces the collapsed legend button on desktop and mobile.
- The metric scale now has a segmented horizontal ruler and continues to calculate distance from map zoom.
- Original Caribbean Guard logo retained.

The current symbols use familiar safety-sign shapes and redundant text, following the design principles in [ISO 7010](https://www.iso.org/standard/72424.html) and [ISO 20712-3](https://www.iso.org/standard/86050.html). They are original interface pictograms, not certified ISO signs. The fixed lifeguard category no longer uses a flag because [ILS water-safety flag guidance](https://www.ilsf.org/wp-content/uploads/2019/01/LPS-14-2010-Flags.pdf) associates red-and-yellow flags with a designated supervised swimming area; this map does not verify who is on duty. The on-map key names each beach-guidance category and separately identifies hazards, existing equipment and dashed proposed equipment. Color is never the only cue.

The detail panel uses a shared 20 px inset and 12/8 px spacing rhythm across all five beaches. On taller desktops, regional weather sits between the primary instruction and the lower safety guidance; the latter and the footer sit near the bottom. Weather condenses or disappears when needed to keep the complete safety guidance visible without scrolling, including the longer Punta Uva notes and compact desktop heights. On phones the sheet scrolls normally. Weather uses an [Open-Meteo](https://open-meteo.com/en/docs) model point near Puerto Viejo, with its model time, source, and an explicit statement that it does not indicate swimming safety. Testing the provider against all five beach coordinates returned the same default grid cell, so the UI does not claim beach-level precision.

## Supported changes to the geographic map

| Existing stable ID | Full-map number | Source status |
|---|---|---|
| cg:station/est1 | 3.2 | Shown as existing equipment |
| cg:station/est2 | 3.3 | Proposed equipment |
| cg:station/est3 | 3.5 | Shown as existing equipment |
| cg:station/est4 | 3.6 | Shown as existing equipment |

The four features were visually matched by shoreline, access-road and bay context. Coordinates and stable IDs are preserved. The proposed station no longer offers directions as though it were available rescue equipment. The previously unidentified shaded bay is explicitly labeled an area of strong currents in the supplied map; its classification and presentation were corrected. Source status still requires field confirmation.

## Unified GPS map

The satellite GPS map is the sole public map view. The legend now controls five groups of annotations projected from the full PDF onto that map: hazards, rescue equipment, proposals, roads/access and places. The old `source-map.html` page remains in the repository as a source-audit artifact but is no longer linked from the interface or included in the offline bundle. Four stations numbered 3.2, 3.3, 3.5 and 3.6 exist in both datasets and anchor the page-to-GPS affine transform in `tools/project_full_annotations.py`. Their fit residuals are 2.9, 1.4, 9.2 and 7.6 metres. The resulting `web/data/full-map-geographic.geojson` contains 315 additional features; the four anchor stations and existing GPS strong-current polygon are retained in their more accurately registered positions rather than duplicated.

The four controls occupy one short coastal stretch, so their fit does not establish positional accuracy across the full PDF. A previous imagery matching attempt did not pass independent holdout checks. The legend and feature popups call the new positions approximate; they do not offer directions or claim live conditions. Undefined facility symbols appear as unknown, not as operational services. Roads and place markers become visible on zoom to preserve legibility at the coast overview.

Following local preview redlines on 21 September, the roads, footpaths and place markers gained a separate smooth offset fitted to four named OpenStreetMap/Nominatim places distributed across the coast: Banana Azul, Rocking J's, Congo Bongo and Maxi's (© OpenStreetMap contributors, ODbL). The four GPS stations remain zero-displacement controls. Hazard arrows and equipment retain the station-based fit. This manual adjustment reduces the obvious coast-wide drift of the access/place layer, but it is provisional: an independent Aguas Claras comparison still differs by about 55 metres, and no road-network or field validation was available. Every rip arrow now uses the same gently curved shaft and solid filled head component.

| Extracted category | Count |
|---|---:|
| Rip-current paths | 59 |
| Strong-current area | 1 |
| Existing rescue-equipment symbols | 11 |
| Proposed rescue-equipment symbols | 18 |
| Proposed CG station | 1 |
| Undefined facility symbols | 4 |
| Location symbols | 64 |
| Main-road paths | 2 |
| Side-road paths | 157 |
| Pedestrian paths | 3 |

These are extracted vector/symbol counts, not verified numbers of distinct roads or active services. Original location text is retained at its document position instead of relying on uncertain nearest-label assignments.

## Unresolved source questions

- Number 4.1 appears at two separate station symbols. Both are retained, with an explanatory popup.
- Four facility symbols are not defined by the source legend. They are shown as unknown, not assumed to be medical or lifeguard services.
- Image registration against cached geographic tiles failed independent holdout checks. The attempt had 17 matches, only 3 training inliers and no holdout match within 20 metres. Its transform was not used. The provisional four-station transform is a different fit and also needs distant independent controls before any feature becomes authoritative for navigation or safety operations.
- Access paths do not establish public access rights or present passability.
- Lifeguard schedules and equipment presence are not live operational reports.

## Verification

- `npm run check:map`: passed.
- `npm run build:map`: passed.
- JavaScript syntax checks passed, including inline map code.
- Data assertions passed: geographic geometry unchanged, station crosswalk and proposal status correct, 320 extracted features, duplicated 4.1 retained, no rescue-equipment number incorrectly assigned to the proposed CG station.
- Browser reviewed at desktop and 390 x 844: beach list, selected beach, proposed-station detail, permanent legend and annotated view. Scale observed changing between kilometre and metre distances.
- Fixed service-worker navigation caching to retain each document under its own URL. CSS precaching now requests CSS explicitly, preventing Vite from caching JavaScript in place of styles during local refresh.
