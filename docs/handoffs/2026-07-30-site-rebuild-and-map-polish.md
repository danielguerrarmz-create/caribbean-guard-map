# Caribbean Guard, 2026-07-30 (afternoon): website rebuilt, map finished

Continues `2026-07-30-georeference-solved-and-site-revamp.md`, which covers the
morning: the georeference, the hazard extraction, and the five-specialist review.
Read that one first for anything about the imagery or the audit.

Everything below is committed and pushed to
**https://github.com/danielguerrarmz-create/caribbean-guard-map** (public).

## What

**1. The website was rebuilt** from the revamp findings. 14 pages, one shared
layout, all copy Caribbean Guard's own.

**2. The map was finished** to the point where the only thing missing is
Caribbean Guard's sign-off. Real zone geometry, their own rescue stations, their
own rip currents, a north arrow, and honest provenance on every claim.

## Verify

    cd C:\Users\danie\caribbean-guard
    npm install     # first time only
    npm run dev

- Site: http://192.168.1.223:5174/
- Map: http://192.168.1.223:5174/mapa/app/index.html
- QR deep links: `?z=cocles`, `?p=est2`

Vite serves `site/`. `tools/build_site.py` copies the map into `site/mapa/app/`
so the whole thing is navigable as one tree locally; in production the map
deploys separately, because the point of it is not sitting behind anything
heavier than itself.

## The website

Built by `tools/build_site.py` from one `page()` function, so the navigation and
footer exist in exactly one place. The live Squarespace build emits its header
markup three times per page and its footer points at two URLs that 404.

Copy is extracted verbatim by `tools/extract_site_copy.py`. Worth knowing: the
section copy on the programme, projects and club pages is **not in the HTML body
at all**. It lives as escaped JSON inside the carousel block's
`data-current-context`, which is why a plain scrape returns headings with nothing
under them.

| | |
|---|---|
| Contact | A real form, `mailto:`, `tel:`. The live site has none of these anywhere. `/unete` stops 404ing. |
| Hazard maps | Real alt text plus a text equivalent listing all rip currents and stations, generated from the GeoJSON so page and map cannot disagree |
| Titles | Every page real. Five previously shared `Services 4 — Caribbean Guard` |
| Nav | Nine items to seven, map first |
| Homepage weight | **30 KB, 3 requests**, against 1.94 MB at load and 52 MB after a minute on the live site |
| Hazard imagery | 4.88 MB PNG to 0.59 MB WebP |
| Mobile | 44px targets, 16px inputs so iOS does not zoom, one h1 per page, no heading skips |

Photography is **reserved, not faked**: 11 SVG placeholders, 11 KB for all of
them, each at the ratio its layout expects and each stating in the frame what
belongs there. The gaps are a shot list.

**Deliberately left alone, on instruction:** `lang="es-AR"` and Spanish only.
Note for when that is revisited: their own copy uses tú imperatives (`Únete`,
`Involúcrate`), so the new copy matches that rather than the voseo the `es-AR`
tag implies. Those two already disagree on the live site.

**Deliberately NOT resolved**, because resolving them means guessing for a safety
organization: `+506 8339 6566` still appears as both the contact number and the
Sinpe Móvil line, and eleven team members have no published role because the live
site still says "Description goes here" for them.

## The map

### Base imagery
Rebuilt from `FULL RESOLUTION MAPPING.png` instead of the JPEG, which had been
compressed twice (generative upscale, then quality-80). Same 15000x4219 framing,
verified by phase correlation at **0.1 px** with a mean difference of 0.9/255, so
the solved georeference applied unchanged.

Output is **9000 px, 1.85 m/px, 2.52 MB**. Chosen by measurement: 5000 is 1.07 MB,
11000 is 3.17 MB. The source is a generative upscale, so detail finer than roughly
2 m/px is largely invented and paying for it is the trade the tile pyramid was
rejected for.

Load strategy: the **1200 px, 63 KB overview** is all that loads on arrival. The
full base is fetched only on first zoom or pan, so its weight is paid by people
who ask for it. Someone who scans a QR code, reads their status and pockets the
phone never downloads it.

### Zone geometry
Redrawn by `tools/redraw_zones.py` against the **Bing mosaic**, not the base.
Bing is untouched imagery already in true coordinates, so its waterline is ground
truth; the base carries 5 to 75 m of registration error. Flood-fill the sea from
the top edge rather than thresholding on colour, take the first land pixel per
column, smooth over ~95 m, nudge 30 m seaward. Verified in `tools/zones_check.jpg`.

The script also exports `tools/shoreline.json`, the dense waterline at one point
per 12 m. `zone_lines.json` is nine points per beach: fine for drawing, useless
for measuring distance against.

### Caribbean Guard's own data
Their annotated map, georeferenced at 294 inliers / 1.2 m, gives:
- **9 rip currents** (not 11: that was fragments, see below)
- **4 rescue stations**, replacing the observation posts I had invented, with
  their own description of what a station holds and the real fact that the
  equipment goes out at dawn and comes in at dusk
- **1 shaded polygon**, drawn grey on purpose because their legend does not
  define it and it could be a hazard zone or a designated safe swimming zone

Because this covers only 1.82 km of 16.66 km, the map says out loud that the rest
is unmapped **and that this does not mean it is safe**.

### Rip direction: read this before touching it
Position is Caribbean Guard's. **Direction is not.** Recovering a bearing from a
hand-drawn dashed arrow needs the arrowhead identified, and at this resolution the
head is a few pixels wider than the shaft. Three proxies were tried and each was
wrong somewhere on the sheet:

| Proxy | Failure |
|---|---|
| Principal axis of the blob | Returns the chord of a curved arrow, near perpendicular to the current on the hooked ones |
| "Point north, the sea is north" | Fine vertically, useless horizontally. One arrow came out at 291°, along the beach |
| Order by distance from the waterline | Inverts wherever the coast bends back on itself |

Arrows are now drawn along the **local seaward normal of the traced coastline**,
anchored at the marked position. True of rip currents in general, cannot point
inland or along the beach, and the sheet says exactly that. Do not "improve" this
into a bearing read from pixels without solving arrowhead detection first.

Also: the arrows are dashed AND curved, so closing the dashes leaves several
components per arrow. 15 fragments were being counted as 11 rips. They are now
clustered at 55 px, giving 9.

### Presentation
- **No flat fill at any zoom.** The coast is 3:1, so a letterbox is unavoidable
  once the whole thing is on screen. A blurred, darkened copy of the overview
  sits behind the base and is sized at runtime from what the viewport can reach
  at the zoom floor. Deliberately unreadable so it cannot be mistaken for data.
- **Strokes and arrows scale with zoom**, 0.42x at the overview to 1.5x on a
  single beach. The dash pattern scales with the weight, because at the overview
  a fixed 16 px gap closes up and "caution" stops looking dashed, silently
  removing the pattern that carries status for anyone who cannot separate the
  colours. The ratio between the three weights is preserved at every zoom.
- **Danger is the loudest mark.** It used to be the faintest.
- **North arrow**, live where the hardware allows. Untested on real hardware:
  the emulator has no magnetometer.

### Provenance
Every zone carries `reviewed: {by, on}` or `null`, and every verdict renders its
provenance beneath itself. Null shows an amber "not verified" banner; a review
older than `REVIEW_VALID_DAYS` (120) turns it back on by itself.

**The rule: the interface may never claim more currency or authority than its data
has.** Proposed link copy described the map as "en tiempo real" and "marcado por
nuestros guardavidas". Both false. Nothing polls anything and no zone has been
authored by Caribbean Guard.

## Bugs found today, recorded so they are not reintroduced

- `arrowHead` declared `const L` for its length, shadowing Leaflet's `L`
- Zoom floor derived from `getZoom()` right after `fitBounds`, which animates, so
  it captured the OLD zoom and the map sat below its own minimum
- A nested array rewritten with `[^\]]*`, which stops at the first inner bracket
  and leaves the old polyline's tail behind as valid-looking broken JS
- `typeof layers === "undefined"` does **not** guard a `const` in the temporal
  dead zone: `typeof` throws there too. Use a boolean flag
- `maxBounds` clamped to the image dragged the padded fly target back, putting
  the deep-linked zone behind the bottom sheet
- Covering `IMG_BOUNDS` still showed page colour, because that is the bounding box
  of a rotated quad and its corners are transparent wedges
- `/nosotros/` page body was a plain string, not an f-string, so `shot()` calls
  rendered as literal text

## Left to do

**Blocking publication:**
1. **Self-host Leaflet.** It loads from unpkg with no fallback, so a failed
   request on beach signal renders a dark void. The page also tells the user to
   save it for offline use with no service worker behind that promise. Both
   halves are the same fix.
2. **Every hazard needs an owner.** Zone descriptions are placeholder prose; the
   extracted rips and stations need confirming and dating.

**Ready to go:**
3. Deploy to **Cloudflare Pages**, not GitHub Pages: Direct Upload lets a
   non-technical person update it. DNS is at **WordPress.com**, not Squarespace.
4. Split `status.json` out of the GeoJSON. Geometry changes rarely and needs
   coordinates; status changes often and is the point. A guard can maintain one
   word and one date per beach; nobody should be editing six-decimal coordinates.
5. Test the compass on real hardware.
6. Base still has panel tone mismatch and a horizontal water seam.

## Files

- `site/` the website, built by `tools/build_site.py`
- `web/index.html` the map
- `web/img/base.webp` 9000 px north-up base; `base-lo.webp` the 63 KB overview
- `web/data/cg-hazards.geojson` their annotations, 14 features
- `tools/refine.py` georeference · `rectify.py` north-up resample
- `tools/residual.py` **the accuracy measurement, the one that matters**
- `tools/redraw_zones.py` coastline tracing + dense shoreline export
- `tools/georef_annot.py`, `extract_annotations.py`, `swap_stations.py`
- `tools/make_placeholders.py` the photography shot list
- `docs/site-revamp/00-SYNTHESIS.md` **the audit, start here for the website**
