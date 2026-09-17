# Caribbean Guard coastal safety map

A bilingual, mobile-first beach guide for Puerto Viejo to Manzanillo, Costa Rica. The interface presents beach guidance, lifeguard information, rescue-equipment annotations and a regional forecast. It does not report observed live swimming conditions.

## Start here

- [Current release and verification](docs/handoffs/2026-09-17-coastal-interface-release.md)
- [Deployment and rollback](docs/deploy.md)
- [Interface audit and brand system](docs/design/coastal-interface-audit.md)
- [Icon vocabulary and full-map source review](docs/design/icon-system-and-source-review.md)

## Run and validate the map

```powershell
npm ci
npm run dev:map
```

Open `http://127.0.0.1:5174/`. The map runs from `web/`. For phone testing on the same network, run `npm run dev:map -- --host 0.0.0.0` and use the printed network URL.

```powershell
npm run check:map
npm run build:map
```

Packaging writes `dist-map/` and requires locally generated imagery. `web/tiles/` is excluded from Git. On a fresh checkout, run `python tools/build_tiles.py` before packaging or deploying; this requires its Python dependencies and network access. The default `npm run dev` and `npm run build` target the separate `site/` website, not the map.

Useful entry points:

- `/?z=cocles`: selected beach, including QR entry.
- `/?p=est2`: proposed station 3.3; stable ID preserved from the earlier map.
- `/source-map.html`: full annotated document in page coordinates, not GPS.

## Structure

| Path | Purpose |
|---|---|
| `web/index.html` | Leaflet map, beach records, interactions and bilingual copy |
| `web/coastal.css` | Responsive layout and visual tokens |
| `web/symbols.js` | Shared SVG status, hazard and facility pictograms |
| `web/source-map.html`, `web/source-map.js` | Full annotated document viewer |
| `web/data/cg-hazards.geojson` | Existing geographic hazards with supported source corrections |
| `web/data/full-map-source.json` | Extracted PDF features, labels, source fingerprint and page coordinates |
| `web/data/full-map-background.jpg` | Reduced source background for the annotated viewer |
| `web/geometry.js`, `web/data/zones-geometry.json` | Beach geometry and shoreline stroke rules |
| `web/sw.js` | Offline cache and update handling |
| `web/vendor/`, `web/fonts/` | Self-hosted Leaflet and Inter |
| `web/tiles/` | Generated satellite imagery; not versioned |
| `tools/` | Extraction, geographic processing, checks and packaging |

## Data provenance and limits

The geographic map retains the earlier annotation coordinates. The complete user-supplied `08102026_FULL MAP DRAFT.pdf` supports renumbering four stations to 3.2, 3.3, 3.5 and 3.6; station 3.3 is proposed. It also identifies the shaded bay as an area of strong currents. Equipment symbols do not establish staffing or current availability.

The full document viewer contains 320 extracted vectors/symbols, including 59 rip-current paths, 11 existing and 18 proposed rescue-equipment symbols. These counts are document features, not field-verified services. Two station symbols share number 4.1, and four facility symbols remain undefined.

Additional source features have **not** been assigned guessed GPS coordinates. Independent image-registration checks failed. The historical base-image alignment measured 5-75 m error on confirmed western points; eastern positions remain unconfirmed. See the source review before changing geographic data. `needs_confirmation: true` must remain until an accountable review supports changing it.

## Regenerate the full-map extraction

Use Python with PyMuPDF and Pillow. Keep the original PDF outside the public deploy folder.

```powershell
python tools/extract_full_map.py 'C:/path/to/08102026_FULL MAP DRAFT.pdf'
python tools/reconcile_full_map.py
```

The first command regenerates page-space JSON and the reduced background. The second applies the documented four-station crosswalk and strong-current classification without changing geometry. Review generated diffs before committing. `tools/inspect_full_map.py` additionally needs OpenCV and NumPy; it records an experimental registration report under ignored `out/pdf-review/` and never publishes geometry.

## Publishing and maintenance

Deploy the existing Vercel project from `web/` using the team scope in [the deployment guide](docs/deploy.md). Git push alone does not upload the ignored imagery. The original logo is unchanged.

Keep guidance, review status and proposal status explicit. Never convert lower-risk guidance into a claim that today's water is safe. Browser viewport checks do not replace field review, real-device offline testing, accessibility testing or imagery-rights review.
