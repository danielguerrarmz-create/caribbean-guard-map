# Caribbean Guard, 2026-09-14: the annotated sheets, and the basemap ruling

Picks up the decision recorded at the end of `2026-08-06-map-schema-and-offline.md`:
write annotations onto the base image, treated as an annotated picture rather than a
slippy map, because that is what Caribbean Guard already makes by hand and the shorter
path to something they will sign.

Nothing in this session is committed.

## What

**Four annotated sheets**, rendered by a new `tools/render_annotated.py`.

| Sheet | Size | Zones | CG marks |
|---|---|---|---|
| `web/sheets/cocles.png` | 3159 x 1289 | Salsa Brava + Cocles | none |
| `web/sheets/chiquita.png` | 2385 x 973 | Chiquita | 9 rips, 4 stations |
| `web/sheets/punta-uva.png` | 2054 x 838 | Punta Uva | none |
| `web/sheets/playa-negra.png` | 1557 x 635 | Playa Negra | none |

**A new coastline tracer**, `tools/trace_coastline.py`, writing `tools/coastline.json`.

Three decisions from Daniel this session:

1. **The basemap is Bing, not `web/img/base.webp`.**
2. **Salsa Brava folds into the Cocles sheet.** On its own it was 560 m of coast, a
   562 px sheet the text panel ate whole.
3. **Unsigned sheets must look unsigned.** A red `SIN FIRMAR / UNSIGNED` band sits above
   everything else on all four.

## Why

### The basemap ruling

Drawn with the same traced coastline on each, `base.webp` puts the line on dry sand and
Bing puts it on the surf edge. The base is the Gemini upscale of the Google Earth
captures and carries **5 to 75 m of registration error**, measured 2026-07-30 by
`tools/residual.py`. Cocles beach is about 40 m wide, so the error is wider than the
beach. A line accurate to Bing cannot be drawn on a base displaced from Bing.

Bing is also the better picture for this job: **1.18 m/px against 1.85**, real imagery
rather than invented texture, and every annotation already lives in its coordinates
(the coastline is traced from it, CG's own hazard sheet georeferenced against it at
1.2 m). Nothing had to be warped.

### Three bugs, in the order they were found

**1. The zone lines are decimated to nine points.** `redraw_zones.py` sets
`MAX_POINTS = 9`, right for a slippy map at low zoom. Over 2.25 km that chords at
250 m, so the line cuts inland on every convex bend. Invisible on the map, obvious the
moment it is drawn at native resolution.

**2. The coastline could not represent a headland at all.** `redraw_zones.py` finds the
waterline with `shore_y[x] = col[0]`, one y per x, which forces the coast to be a
**function of longitude**. It is provably one: the 1,434 points in `shoreline.json` are
strictly monotonic in longitude at a uniform 11.7 m step, which no real coast is. Every
headland has two or more crossings at one longitude and the scan can keep only the
northernmost. Compounding it, an 81-column box smooth averages across ~95 m of
longitude, and the 30 m seaward nudge is applied as `ys[i] - SEAWARD_M`, straight north
rather than along the local normal.

`trace_coastline.py` traces the sea/land contour instead, which is free to double back,
and offsets along the local normal toward whichever side the water is on. **298
longitude reversals** across the coast: each one is a place the old scan had to delete
part of the shore.

**3. The water mask called the jungle sea.** The worst of the three and the reason the
contour trace kept failing. `water_mask` ends `| (v < 60)`, so every dark pixel is
water. Shadowed rainforest is dark. Over the Chiquita window the mask came out **88.7%
sea**, the canopy flooded, only sand and rooftops standing as land.

It never broke `redraw_zones.py` because a per-column scan takes the first *land* pixel
from the top, and the first bright thing below the water is the sand. **The beach
rescued a mask that was wrong about everything behind it.** A contour follows the
region's true boundary, and that boundary ran through the trees.

Rebuilt on measured pixels, 50 px patches, 5th to 95th centile:

| | h | s | v |
|---|---|---|---|
| open sea | 90-99 | 193-245 | 50-77 |
| reef shallow | 99-102 | 206-239 | 59-70 |
| shallow inshore | 69-92 | 49-228 | 43-86 |
| dark jungle | 20-66 | 7-190 | 32-116 |
| beach sand | 26-70 | 44-170 | 26-145 |

**Hue is the only discriminator that separates every class**: water 69 and up, land 70
and down. Saturation looked decisive on deep water alone (193 up against 190 down) but
the pale inshore shelf runs to 49, and keying on it put the line at the reef edge
instead of the sand. Value separates nothing, which is why the old test flooded the
forest.

### Apple Maps, probed and rejected

Daniel raised Apple's imagery mid-session. Probed at Punta Uva, same window and zoom.

- **Quality: too close to call.** Apple's water is more saturated, but the submerged reef
  is at least as legible on Bing and Bing is slightly sharper on land. No resolution
  argument for switching.
- **Licensing: barred.** MapKit JS Schedule 6 section 2.5 forbids caching, pre-fetching
  or storing Map Data other than temporarily to improve performance, and requires
  deletion after use. A printed sheet, or a PNG committed to a public repo, is exactly
  that stored copy. There is no public tile endpoint; imagery comes only through MapKit
  JS or the Snapshots API, both requiring a paid Apple Developer account.
- **Nonprofit status does not change it.** The restriction is on storing and
  redistributing imagery, not on who pays, and Apple publishes no nonprofit imagery
  programme comparable to Google for Nonprofits.

Bing stays. It is cleanly licensed for this, already cached as 1,395 z17 tiles, and
exceeds the print requirement.

## What the sheets carry

Everything that survived the change of surface from the 2026-08-06 schema freeze:

- **Instructions, never ratings.** `NO ENTRES AL AGUA`, `SOLO CON GUARDAVIDAS`,
  `REVISA ANTES DE ENTRAR`, `TEN CUIDADO IGUAL`. No label grants permission.
- **Provenance on every panel.** `Autor` and `Revisado`, with `nadie todavía` in red.
- **The deferral under every character**, still phrased conditionally because a red flag
  *system* on this coast is unconfirmed.
- **ES then EN on every block**, English smaller and dimmer, never absent. Spanish stays
  primary: it is the community's language and Caribbean Guard's own.

The zone records are parsed out of `web/index.html` rather than copied, so the sheet and
the map cannot drift apart. The zone spans in `trace_coastline.py` are read from
`redraw_zones.py` for the same reason.

## Verify

```
python tools/trace_coastline.py      # rewrites tools/coastline.json
python tools/render_annotated.py     # rewrites web/sheets/*.png
```

The tracer prints traced coast over span per zone. **Sinuosity is the check**: a real
coast runs about 1.1 to 1.5. Playa Negra is 1.07, Punta Uva 1.48, Cocles 1.67,
Chiquita 1.78. Anything above about 2.5 means the contour is running up river mouths
again and the opening radius needs raising.

## Left

1. **Salsa Brava has no on-image label** on the merged sheet: its line falls under the
   text panel, and the placement rule skips a label it cannot put somewhere visible.
   Cosmetic, but it means two same-coloured lines share a sheet with only one named.
2. **`shoreline.json` and the nine-point `line:` fields in `web/index.html` are still
   the broken geometry.** The sheets no longer use them; the slippy map still does.
   Either retire the map or re-run its geometry through the new tracer.
3. **Nothing is committed**, and `tools/` still holds a large pile of debug images from
   earlier sessions.
4. Four of five zones carry no Caribbean Guard data at all. That is not a gap to fill
   with desk work, it is the sheet series naming which beaches need a guard.

## Open with Caribbean Guard

Unchanged from 2026-08-06, still seven, still unanswered. The red flag question is
still the biggest: our Cocles copy asserts a flag system and nobody has confirmed it.

## Files

- `tools/render_annotated.py` — the sheet renderer (new)
- `tools/trace_coastline.py` — the coastline tracer (new)
- `tools/coastline.json` — one dense polyline per zone (new, generated)
- `web/sheets/*.png` — four sheets (new, generated)
