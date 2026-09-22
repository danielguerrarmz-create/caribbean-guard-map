# Puerto Viejo, Playa Grande and Manzanillo, 2026-09-22

## What changed

- The existing Salsa Brava safety zone is displayed as Puerto Viejo in the list, map label and detail title. Its internal ID and GPS coastline geometry remain unchanged so existing links still work. The detail identifies the Salsa Brava section that the no-swim guidance describes.
- Playa Grande and Manzanillo are now named beach entries, map labels and concise detail panels. Both are marked **Not assessed / Sin evaluar**. They do not receive a safety-zone color or an inferred swimming verdict.
- Manzanillo's town label uses its OSM location. Town labels yield to beach labels at shared zoom levels, avoiding duplicates.
- The compact desktop list fits all eight entries at a 720 px viewport. Offline cache advances to `v28`.

## Why

The requested name reflects the local Puerto Viejo beach area, which Costa Rica tourism material also calls Salsa Brava. Playa Grande here means the Caribbean stretch west of Manzanillo, not the Pacific beach of the same name. Naming the two additional locations should not imply that their swimming conditions have been assessed.

Location references: [Costa Rica tourism material](https://www.visitcostarica.com/sites/default/files/2024-10/2.2.4.5.12%20Agua.pdf), [Museo Nacional's Playa Grande coordinate](https://www.museocostarica.go.cr/nuestro-trabajo/investigaciones/arqueologia/pecio/), and [OpenStreetMap Playa Manzanillo](https://www.openstreetmap.org/way/37606802). The museum coordinate is a reference point on Playa Grande, not a surveyed beach center or access point.

## How to verify

1. Open `http://127.0.0.1:5174/mobile-preview.html` and `http://127.0.0.1:5174/`.
2. Check the Puerto Viejo card and detail, including the Salsa Brava section label and unchanged no-swim guidance.
3. Open Playa Grande and Manzanillo in English and Spanish. Verify their neutral status, distinct map locations and deep links `?b=playa-grande` and `?b=manzanillo`.
4. At a 720 px desktop height, confirm all entries and the coastal forecast fit without a cut-off row.
5. Run `npm run check:map`, `npm run build:map`, inline script syntax and `git diff --check`.

## What's left

Caribbean Guard has not reviewed beach-specific guidance or boundaries for Playa Grande and Manzanillo. Their map points are approximate location references. The changes are local pending release.

## Files touched

- `web/index.html`
- `web/coastal.css`
- `web/sw.js`
- `docs/handoffs/2026-09-22-beach-list-expansion.md`
