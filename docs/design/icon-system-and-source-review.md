# Icon system and full-map reconciliation

Review date: 17 September 2026. Implementation and source review. Deployment status: [release handoff](../handoffs/2026-09-17-coastal-interface-release.md).
Source: `08102026_FULL MAP DRAFT.pdf`, user supplied, page 1. Source fingerprint and page coordinates are recorded in `web/data/full-map-source.json`.

## Interface changes

- Compact title and location; removed the draft paragraph from the title block.
- Beach cards contain a large status pictogram, name, action and separate lifeguard information.
- No-swim uses a prohibited-swimming symbol; conditional entry uses an exclamation triangle; lifeguard-dependent guidance uses a flag; lower-risk guidance uses waves with the existing caution text. No icon asserts that today's water is safe.
- Rescue equipment uses a life ring on amber. Proposed equipment uses an outlined/dashed ring. A proposed CG facility uses a dashed building symbol. These do not imply staffing.
- A permanent map key replaces the collapsed legend button on desktop and mobile.
- The metric scale now has a segmented horizontal ruler and continues to calculate distance from map zoom.
- Original Caribbean Guard logo retained.

## Supported changes to the geographic map

| Existing stable ID | Full-map number | Source status |
|---|---|---|
| cg:station/est1 | 3.2 | Shown as existing equipment |
| cg:station/est2 | 3.3 | Proposed equipment |
| cg:station/est3 | 3.5 | Shown as existing equipment |
| cg:station/est4 | 3.6 | Shown as existing equipment |

The four features were visually matched by shoreline, access-road and bay context. Coordinates and stable IDs are preserved. The proposed station no longer offers directions as though it were available rescue equipment. The previously unidentified shaded bay is explicitly labeled an area of strong currents in the supplied map; its classification and presentation were corrected. Source status still requires field confirmation.

## Full annotated view

The permanent legend links to `source-map.html`. It uses the original document background and extracted page-space vectors, with the new pictograms and switchable layers. This lets readers inspect the added material without treating uncertain document placement as GPS geometry.

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
- Image registration against cached geographic tiles failed independent holdout checks. The attempt had 17 matches, only 3 training inliers and no holdout match within 20 metres. Its transform was not used.
- Additional page-space features must be aligned to verified geographic control points before joining the GPS map. Access paths do not establish public access rights or present passability.
- Lifeguard schedules and equipment presence are not live operational reports.

## Verification

- `npm run check:map`: passed.
- `npm run build:map`: passed.
- JavaScript syntax checks passed, including inline map code.
- Data assertions passed: geographic geometry unchanged, station crosswalk and proposal status correct, 320 extracted features, duplicated 4.1 retained, no rescue-equipment number incorrectly assigned to the proposed CG station.
- Browser reviewed at desktop and 390 x 844: beach list, selected beach, proposed-station detail, permanent legend and annotated view. Scale observed changing between kilometre and metre distances.
- Fixed service-worker navigation caching to retain each document under its own URL. CSS precaching now requests CSS explicitly, preventing Vite from caching JavaScript in place of styles during local refresh.
