# Rip-current reference images, 2026-10-27

## What changed

- Added the five supplied annotated JPEGs as optional reference images in the map-only site.
- Added a neutral, separately switchable image-reference layer. Its markers open bilingual image sheets on mobile and desktop. They do not replace or redraw the 2026 hazard arrows.
- Explained the dotted survivor line in the Shawandha image using Daniel's definition: a large rope with flotation devices intended as a last aid and a boundary not to swim beyond. The sheet says the image does not verify present installation or usability.
- Retained the 2026 rescue-station numbering, positions, status, and existing rip-current geometry. The 2025 sign PDFs did not change those data.

## Why

The JPEGs contain valuable site-specific visual context, but four do not register reliably to the current satellite imagery. Publishing their red shapes as GPS hazard polygons would invent precision and could conflict with the 2026 map that Daniel designated authoritative. A neutral reference-image layer lets reviewers inspect the material at the named coast while keeping the map's current hazard data intact.

## Placement and evidence

| Image | Map placement | 2026 rip arrows within 350 m | Limit |
| --- | --- | ---: | --- |
| Jaguar Rescue Center / El Rincón Porteño | 2026 station 3.1 area, snapped to OSM shore | 3 | Area association only; no image match. |
| Aguas Claras | Matched to current z17 satellite tiles with 2,221 RANSAC inliers; its footprint is stored in the registry | 4 | The matched image extends east of the Aguas Claras landmark through the Chiquita coast. Its filename is not a precise point label. Tile registration is not independent GPS verification. |
| Calle Merlin / Punta Cocles | 2026 Merlin label, snapped to OSM shore | 1 | Area association only; no image match. |
| Paradise Trail | 2026 Paradise label, snapped to OSM shore | 4 | Area association only; no image match. |
| Entrada Shawandha / Gypsea Trail | 2026 Gypsea / Shawandha label, snapped to OSM shore | 4 | Area association only; survivor-line geometry and present condition unknown. |

The images have no embedded GPS metadata. A feature-matching check against local map tiles and the existing V5 image found a strong match only for Aguas Claras. The other four align by named 2026 map locations and are explicitly labeled approximate. All five reference points are near existing 2026 rip arrows, but proximity does not prove that an old red shape is the same current as a 2026 arrow; the 350 m counts overlap between sites. No route button is offered from a reference marker.

## How to verify

1. Run `python -X utf8 tools/audit_rip_reference_images.py`, `npm run check:map`, and `npm run build:map`.
2. Run the local map and open the legend. Switch **Reference images / Imágenes de referencia** off and on.
3. Zoom to 15 or closer around the Chiquita coast. Open all five neutral image markers in Spanish and English. Check image loading, full-image links, sheet close, and mobile scrolling.
4. Check Shawandha's dotted-line explanation. Confirm the map never depicts it as a GPS line or currently available equipment.
5. Compare station counts, numbers, and status with the previous revision; they must be identical.

## What's left

- Daniel reviewed the local result on 2026-10-27 and said it looks good for now. The agent's browser was still blocked from the localhost origin, so an agent-rendered mobile and desktop walkthrough remains unverified.
- Wait for AJ's additional information before changing the 2026 map or making further content decisions.
- Caribbean Guard should verify whether the survivor line exists now and provide surveyed endpoints before it becomes a mapped line or a live safety resource.
- Confirm rights to redistribute the five satellite images before a public deployment.
- Item 3 from the review remains open: confirm whether the secondary emergency number on the 2025 signs is active, and approve bilingual bystander rescue wording. Neither was added to the map.
- No PR, push, merge, or deployment was made.

## Files touched

- `web/index.html`, `web/coastal.css`, `web/symbols.js`, `web/sw.js`
- `web/data/rip-reference-images.json`
- `web/reference/rip-currents/*.jpg`
- `tools/audit_rip_reference_images.py`, `tools/check_copy.js`
- This handoff document
