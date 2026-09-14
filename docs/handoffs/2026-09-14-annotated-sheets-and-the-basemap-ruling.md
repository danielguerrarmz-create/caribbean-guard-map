# Caribbean Guard, 2026-09-14: the annotated sheets, and the basemap ruling

Picks up the decision recorded at the end of `2026-08-06-map-schema-and-offline.md`:
write annotations onto the base image, treated as an annotated picture rather than a
slippy map, because that is what Caribbean Guard already makes by hand and the shorter
path to something they will sign.

Committed on `feat/annotated-sheets` in two commits: the sheets and the coastline
(`4c73fa7`), then the map (`635fc3e`).

## What

**Four annotated sheets**, rendered by a new `tools/render_annotated.py`.

| Sheet | Size | Zones | CG marks |
|---|---|---|---|
| `out/sheets/cocles.png` | 3159 x 1289 | Salsa Brava + Cocles | none |
| `out/sheets/chiquita.png` | 2385 x 973 | Chiquita | 9 rips, 4 stations |
| `out/sheets/punta-uva.png` | 2054 x 838 | Punta Uva | none |
| `out/sheets/playa-negra.png` | 1557 x 635 | Playa Negra | none |

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

## The map, second half of the same day

The sheets moved to Bing; the slippy map at `web/index.html` had not. Daniel asked for
four things: fill the black at full zoom-out, make the linework read correctly zoomed
out, add notations, and put the same Bing imagery on the main view.

### The basemap is a tile pyramid now

`tools/build_tiles.py` builds `web/tiles/` — 2,152 tiles, 19.8 MB. The single
`imageOverlay` is gone, and with it `sizeBackdrop()` and the blurred-copy layer.

One image caused three problems that were being *managed* rather than fixed: black
bands on every viewport shape, a zoom floor that had to be computed and clamped on
every resize, and the 5 to 75 m displacement. Tiles have none of them.

| Level | Source | Extent |
|---|---|---|
| z12-14 | fetched native | context box, 22 x 34 km |
| z15-16 | fetched native | coast box |
| z17 | the existing z17 cache | coast box |

### The black was the pyramid, not coverage

**This is the finding worth keeping.** The first build derived z12-16 the ordinary way,
averaging each tile's four children. That assumes the source is a square. Ours is a
**strip**: one z13 tile spans 16 x 16 z17 tiles, and the cache is a 56 x 27 rectangle
hugging the coast, so nearly every low-zoom tile was a handful of real children and
fifteen-sixteenths background fill. The fill was the app's own navy, indistinguishable
from the bands the change set out to remove. **The map looked like it had no imagery at
exactly the zoom where it had the most.** Every derived level carried the same ring of
part-filled tiles at its edge.

The rule: never derive a tile the source does not fully cover. Fetching each level
natively is cheaper to reason about than tracking coverage per tile.

**And the fix stayed invisible for three rebuilds.** Everything but the HTML is served
cache-first, so the old navy tiles kept coming from `cg-map-v1` no matter what was
rebuilt. `CACHE` is now `cg-map-v2`, with a note in `sw.js` that any `web/tiles/` change
requires the bump. When a change should be visible and is not, suspect the cache before
the code.

### Strokes are sized to the ground, not to a zoom ramp

The old ramp, `k = 0.42 + t * 1.08` over zoom 11.5 to 17, put the `high` stroke at
7.9 px at the whole-coast view. A pixel is 18.9 m at z13, so that was a **149 m line
describing a 40 m beach**, with a `weight * 2.4 + 6` halo adding **472 m** on top.
Zoomed out, the map read as a continuous wall of hazard and as far less precise than it
is. `zoneStroke()` now solves for a target width on the ground and clamps at both ends.

| | z13 line | z13 halo | z17 line |
|---|---|---|---|
| Before | 149 m | 472 m | 19 m |
| After | 46 m | 107 m | 17 m |

The change lands almost entirely where the problem was, which is the sign it is the
right variable. The halo scales with the stroke instead of adding a constant.

### Notations

Beach names, Puerto Viejo, Manzanillo, Mar Caribe, and a scale bar. Deliberately few:
every label is ink on top of the thing the reader needs to see, and Caribbean Guard's
own sheet already carries roads and businesses. All non-interactive, so a label cannot
swallow a tap meant for the zone under it. Shown by zoom, because the same set is
clutter at one scale and too sparse at another.

### Offline, retiered

| Tier | Levels | Tiles | Bytes |
|---|---|---|---|
| CRITICAL (install blocks) | z12-13 | 52 | 456 KB |
| OPTIONAL (background) | z14-15 | 270 | 2.6 MB |
| On visit only | z16-17 | 1,773 | ~20 MB |

The lists are generated into `sw.js` by `build_tiles.py`, so they cannot drift from what
is deployed.

### Bing licensing

Serving these tiles redistributes Bing imagery, which their terms do not permit.
**Daniel's call, 2026-09-14: proceed, on the basis that this is a nonprofit safety map.**
Recorded in `build_tiles.py` so nobody rediscovers the question. If it is ever revisited
the alternative is Esri World Imagery, free with attribution and finer than this cache,
at the cost of offline precaching. Apple Maps was probed the same day and rejected: the
imagery is no better here, and MapKit JS Schedule 6 section 2.5 bars caching or storing
Map Data at all.

### web/tiles/ is gitignored

2,152 files and 20 MB is the wrong thing to put in a public repository when the build is
deterministic. `docs/deploy.md` now opens by telling a deployer to run
`python tools/build_tiles.py` first, because **deploying without it produces a map with
every zone line and label in place over a blank navy field, and nothing warns you.**
Keep those two facts in step.

## Verify

```
python tools/trace_coastline.py      # rewrites tools/coastline.json
python tools/render_annotated.py     # rewrites out/sheets/*.png
python tools/build_tiles.py          # fills web/tiles/ (REBUILD=1 to start over)
```

For the map, serve `web/` and open it. The check that matters is the **whole-coast
view**: imagery corner to corner with no navy showing, and zone lines thin enough that
the beach under them is still visible. If tiles look stale after a rebuild, the cache
version in `sw.js` was not bumped.

The tracer prints traced coast over span per zone. **Sinuosity is the check**: a real
coast runs about 1.1 to 1.5. Playa Negra is 1.07, Punta Uva 1.48, Cocles 1.67,
Chiquita 1.78. Anything above about 2.5 means the contour is running up river mouths
again and the opening radius needs raising.

## Left

1. ~~Salsa Brava has no on-image label.~~ **Fixed.** Both zones on the merged sheet are
   now named on the water. The panel column moved to the right edge, which is chosen
   for the SHEET rather than per zone: moving only Salsa Brava's panel was tried first
   and failed, because Cocles' panel on the left still covered Salsa Brava's shore. The
   column hides that zone regardless of whose text is in it, so what matters is which
   edge the column occupies. The unsigned band follows the column and the legend takes
   the opposite corner. The leader-line mechanism stays in as a fallback for a zone
   that has no clear shore on either side, guarded so it never points off the picture.
2. **`shoreline.json` and the nine-point `line:` fields in `web/index.html` are still
   the broken geometry.** The sheets no longer use them; the slippy map still does.
   Either retire the map or re-run its geometry through the new tracer.
3. `tools/` still holds a pile of debug images from earlier sessions. All are
   gitignored, and `.gitignore` notes that `annot_check.jpg` and `georef_check*.jpg`
   are the evidence behind the georeference, so they are kept rather than swept.
   `georef.py` through `georef6.py` are six superseded attempts, kept as the record
   of what failed; only `georef2.py` is referenced anywhere and it is now referenced
   by nothing that runs.
4. **Nothing is deployed.** Host is Vercel (Daniel, 2026-09-14); `docs/deploy.md`
   carries the CLI steps, `web/vercel.json` the caching rules, and `web/_headers` the
   same rules for Cloudflare as a fallback. A Git-connected Vercel deploy would ship a
   map with no imagery, because `web/tiles/` is gitignored; the CLI deploy sends what
   is on disk and is the documented path.
5. Four of five zones carry no Caribbean Guard data at all. That is not a gap to fill
   with desk work, it is the sheet series naming which beaches need a guard.

## Cleanup at session close, 2026-09-14

**`redraw_zones.py` now refuses to run** and exits 1. Its last act was to write
straight into `web/index.html`, and everything it writes is now known wrong, so
running it would silently replace the corrected coastline with the broken one and
report success. It cannot be deleted: `trace_coastline.py` reads the five zone
longitude spans out of its ZONES list.

**The clean-clone path was broken in two places and is now proved, not assumed.**
Both `build_tiles.py` and `render_annotated.py` died with
`no tile cache; run tools/georef2.py first` on a fresh checkout, and that
instruction is a dead end: `georef2.py` reads an absolute path into a Downloads
folder, at a file that is not in the repository. So the single command
`docs/deploy.md` tells a deployer to run was false for anyone but this machine.

- `build_tiles.py` now fetches z17 like every other level; `tools/tilecache/` is a
  seed that saves 1,395 fetches, not a prerequisite.
- `render_annotated.py` reads `web/tiles/` instead of the cache, which is also the
  right source: it is what the map serves, so the sheets and the map show the same
  pixels.
- Verified by cloning the repo to a scratch directory and running both from
  nothing: 2,195 tiles and 21.1 MB fetched, then all four sheets rendered at
  identical dimensions. A recovery instruction nobody has run from a clean state
  is a guess.

**`extract_annotations.py` still reads the superseded `shoreline.json`**, and now
says so at the function, with what it costs and why it is survivable today.

## Open with Caribbean Guard

Unchanged from 2026-08-06, still seven, still unanswered. The red flag question is
still the biggest: our Cocles copy asserts a flag system and nobody has confirmed it.

## Files

- `tools/render_annotated.py` — the sheet renderer (new)
- `tools/trace_coastline.py` — the coastline tracer (new)
- `tools/coastline.json` — one dense polyline per zone (new, generated)
- `out/sheets/*.png` — four sheets (new, generated, gitignored). **Outside `web/`
  on purpose:** `web/` is dragged into Cloudflare Pages whole, so sheets left in
  there would publish four unsigned drafts to the open internet as a silent side
  effect of deploying the map.
- `tools/build_tiles.py` — the tile pyramid builder (new)
- `web/tiles/` — 2,152 tiles, 19.8 MB (new, generated, gitignored)
- `web/index.html` — tile basemap, ground-based strokes, notations
- `web/sw.js` — generated tile precache lists, cache bumped to v2
- `docs/deploy.md` — renamed from `deploy-cloudflare-pages.md`; Vercel is the host
- `web/vercel.json` — caching rules for Vercel (new)
- `web/img/base.webp`, `web/img/base-lo.webp` — **deleted**, nothing referenced them
