# Caribbean Guard, 2026-07-30: georeference solved, hazards extracted, site revamp

Supersedes the open items in `2026-07-29-mobile-safety-map.md`. Read that one only
for the record of what was already tried and ruled out.

## What

Three things happened.

**1. The georeference is solved and independently verified.** This was the blocker
on everything.

**2. Caribbean Guard's own hazard annotations turned out to already exist**, on
their own website, and are now real coordinates.

**3. A five-specialist pass over caribbeanguard.org** produced a synthesis and an
actionable fix list. Start at `docs/site-revamp/00-SYNTHESIS.md`.

## Why

The map's whole purpose is to tell someone standing on the sand whether they can
swim where they are. Without a georeference the blue dot is decorative. Without
attributed hazard data the verdicts are decoration too, and dangerous decoration,
because they carry the visual authority of an official assessment.

## The georeference

Solved by `tools/refine.py`: local patch matching against Bing z17 inside a small
search window, using a prior read off landmarks by hand.

| | |
|---|---|
| Bounds | `[[9.621462, -82.790863], [9.671534, -82.639053]]` |
| Coverage | 16.66 km east to west |
| Scale | 109.4 cm per source pixel |
| Rotation | +3.368 degrees off north |

**Accuracy, measured not assumed.** `tools/residual.py` samples 14 points along the
coast and matches each independently against Bing:

- Puerto Viejo to Punta Uva: **5 to 75 m**, median 50 m, 8 of 14 confirmed
- East of Punta Uva: **not confirmable**, best estimate 150 m

Two independent corroborations: the scale agrees with the hand-read prior to 0.7
percent, and the corners land within 45 m of the SIFT run discarded on 07-29.
Those methods share no machinery.

### The number that is NOT the accuracy

`tools/georef.json` reports a 4.0 m median residual. **That is the RANSAC residual
on the 14 inliers out of 109 control points, and it is circular.** RANSAC selects
the subset that agrees with the model, then measures how well that subset agrees
with the model. It proves those 14 points were mutually consistent. It says
nothing about where the image sits on the ground.

This has already been misread once, in a draft of `04-map-integration.md`, and it
concluded the georeference was 12 times better than it is. If you find yourself
about to quote 4.0 m as accuracy, stop.

### Why the east cannot be verified

The generative upscale replaced the water and reef with invented texture. Compare
`tools/georef_check_east.jpg`: Bing shows reef as dark patches in turquoise, the
base shows flat purple-grey with fabricated ripples and no reef at all.

This is a content problem, not only a matching problem. Reef-protected versus open
water is the entire safety story at Manzanillo, and the imagery no longer contains
it. That section needs real imagery before it can carry a swim recommendation.

### Rectification

`tools/rectify.py` resamples the source into north-up Web Mercator, because
Leaflet's `imageOverlay` cannot rotate and feeding it a rotated image's bounds
would smear the ends by up to 490 m, worse than no georeference at all.

Output is `web/img/base.webp`, 5000x1673, **1.19 MB with alpha**. The alpha carries
the wedges left by the 3.37 degree rotation so they render as page background
rather than black triangles.

## Caribbean Guard's hazard data

Found on `/programa-playa-organizada`, published, and invisible: both hazard maps
carry `alt=""` because the Squarespace carousel block emits two `alt` attributes
and the empty one wins.

`tools/georef_annot.py` georeferenced their `Annotated Base Map V5.png` against
Bing: **294 RANSAC inliers, 1.2 m median residual.** Unambiguous.

The contrast with the base image is the clearest evidence yet for the rule:
**5 inliers on generatively upscaled imagery, 294 on untouched imagery.**

`tools/extract_annotations.py` reads the graphics back off it into
`web/data/cg-hazards.geojson`:

- 11 rip currents, as directed line segments
- 4 rescue stations
- 1 shaded polygon, **deliberately left unlabelled**

Covers 1.82 km, about 11 percent of the base.

**On the unlabelled polygon.** The sheet's legend defines six things and the pink
shaded area is not one of them. Red reads as danger, but Caribbean Guard's own
programme text describes a "zona segura de bañado", a designated safe swimming
zone, which would sit in exactly that kind of sheltered bay. Guessing wrong
inverts a safety message, so it ships as `shaded_area_meaning_unknown` and must not
be rendered with a status until AJ says which it is.

Verify with `tools/annot_check.jpg`: cyan overlay must sit on the original
graphics. It does.

Thresholds in the extractor are measured off the sheet's own hue histogram, not
guessed. Saturation alone separates nothing, because tropical jungle and reef
water are both highly saturated and together are 10 percent of the image.

## The map

`web/index.html`. Changes today:

- Real bounds, and `GEO_ACCURACY_M` / `GEO_ACCURACY_EAST_M` constants
- **The locate circle shows GPS error and registration error combined in
  quadrature.** A tight 8 m GPS circle would claim precision this map lacks
- **Letterboxed full-coast default** instead of cover-fit, which on a 390 px
  portrait phone had been zooming to about 370 m of a 16.5 km coast: all water, no
  landmark, nothing telling you which beach you were looking at
- **Status polarity inverted.** Danger was a fine dotted line, the faintest mark on
  the map, meaning DO NOT SWIM. Now danger is 11 px unbroken, caution 8 px dashed,
  safe 5 px fine dots. The loud mark is the dangerous one, as every convention a
  tourist carries already says
- **The legend teaches itself.** Each picker card's swatch draws the actual map
  stroke for that status. The `legendSafe`/`legendCaution`/`legendDanger` strings
  had existed in the translation table referenced by nothing
- **Two-tier colour.** Dark values for text where 4.5:1 applies, vivid values for
  map lines where 3:1 applies. See the trap below
- **Provenance on every verdict**, see below
- Sheet no longer buries the zone it describes; toast has `aria-live="assertive"`
- **The full base is no longer fetched on load.** Ships `base-lo.webp` (45 KB) only;
  `base.webp` (1.19 MB) arrives on first zoom or pan. At the default letterboxed
  zoom the overlay is 1116x375 device px and the overview is 1000 px wide, so the
  full base buys nothing visible there. Someone who scans a QR, reads their status
  and pockets the phone never downloads it. Measured CLS on the upgrade is exactly 0.
  **Gotcha:** arm the trigger *after* the opening fit settles, or `fitBounds` fires
  its own `zoomend` and the base loads immediately anyway.

### The colour trap, recorded so it is not walked into again

`--safe #1f9d55` and `--caution #c77700` had luminance 0.251 and 0.254. Identical
brightness, so in sun, which kills hue first, "caution" and "swimming ok" were the
same colour. Both also failed AA as white-on-fill at 3.49:1 and 3.46:1.

Moving caution to `#9C5C00` fixes contrast and **creates a new collision**: it sits
1.06:1 from danger, and caution versus danger is the more expensive pair to
confuse. The trap is structural. Any all-dark-on-white palette hits it, because the
AA floor pushes every token into the same narrow luminance band.

Resolution is two tiers that diverge on purpose. On the map, caution is the
*brightest* of the three, so all three separate by brightness alone.

### Provenance

Every zone carries `reviewed: {by, on}` or `reviewed: null`, and every verdict
renders its provenance directly beneath itself:

- null: amber banner, "Not verified. Caribbean Guard has not reviewed this beach
  yet. Ask a lifeguard before you go in."
- fresh: muted, "Reviewed by X on 1 July 2026"
- older than `REVIEW_VALID_DAYS` (120): amber again, "Conditions may have changed."

Filling in a real review turns the warning off by itself, and ageing out turns it
back on with nobody having to remember.

**The governing rule, which nearly got broken today:** the interface may never
claim more currency or more authority than the data behind it has. Proposed link
copy described the map as "real time" and "marked by our lifeguards". Neither is
true: nothing polls anything, and no zone has been authored by Caribbean Guard. A
real-time claim on stale data is worse than the static PNG it replaces, because
the PNG never claimed to be current.

## Verify

    cd C:\Users\danie\caribbean-guard\web
    python -m http.server 8777 --bind 0.0.0.0

- Desktop: http://127.0.0.1:8777/index.html
- Phone, same wifi: http://192.168.1.223:8777/index.html
- QR deep link: http://127.0.0.1:8777/index.html?z=cocles

Checked at 390x844, 3x DPR, mobile and touch emulation. No console errors.

The ambiguity fix is verifiable: at the midpoint of the Cocles/Chiquita gap both
zones measure 209 m and the map asks rather than guessing. Standing on Cocles it
reads 0 m against 1123 m and opens confidently.

Regenerate everything:

    cd tools
    python refine.py && python rectify.py       # base
    python residual.py                          # accuracy, run this before believing anything
    python georef_annot.py && python extract_annotations.py   # hazards

## Left to do

**Blocking publication of the map:**

1. **Leaflet loads from unpkg with no SRI and no fallback.** If that request fails
   on beach signal the script throws and the page is a dark blue void with a brand
   label and a 911 button. Meanwhile the page tells the user to save it for offline
   use, with no service worker, manifest or cache behind that instruction. Self-host
   Leaflet and either implement the offline promise or stop making it.
2. **Hazard data needs AJ.** The 11 extracted rip currents need confirming and
   dating, and the pink polygon needs identifying.

**Next steps that are ready to go:**

3. Host on **Cloudflare Pages** at `mapa.caribbeanguard.org`, not GitHub Pages. Not
   a technical call: Cloudflare Direct Upload lets someone drag a folder into a
   dashboard, GitHub needs a git workflow that decays the first time the person who
   knew it is unavailable. **DNS is at WordPress.com**, not Squarespace, so the
   subdomain needs an account nobody has mentioned. Fallback is `pages.dev`.
4. **No tile pyramid in release one.** Overview image plus GeoJSON, first-useful at
   86 KB, fits in a service worker precache. The 1,300-tile assumption was
   inherited from the print version and never tested. The base is 3.33 m/px and the
   source was upscaled, so the extra resolution is partly synthetic: serving
   1.09 m/px tiles off imagery uncertain to 75 m would dress a guess up as a survey.

   **Implementation gotcha, do not skip.** Paint the 29 KB overview first, then
   request the full base hung off the overview's `load` event with
   `fetchPriority = "low"`. Firing both at once makes them compete for the same
   400 kbps and time-to-usable goes from 7.2 s to **31 s**, silently cancelling the
   entire benefit.

   **The rule that reconciles hosting with navigation: the embed is the browse
   path, the standalone is the emergency path.** Sofa visitor gets the map in
   context; sand visitor gets the standalone and nothing else. This takes the
   Squarespace plan question off the critical path, because no Code Blocks just
   means the tab holds a link card.
5. Redraw the zone geometry. The placeholder lines were drawn against the old wrong
   bounds and are now visibly off the coast.
6. Base still has panel tone mismatch and a horizontal water seam.

## Files

- `web/index.html` the map
- `web/img/base.webp` rectified north-up base, 1.19 MB
- `web/data/cg-hazards.geojson` extracted hazards, 16 features
- `tools/refine.py` georeference; `rectify.py` north-up resample
- `tools/residual.py` **the accuracy measurement, the one that matters**
- `tools/validate.py` three-landmark proof sheet, `EAST=1` for the east end
- `tools/georef_annot.py`, `extract_annotations.py` hazard extraction
- `tools/annot_check.jpg`, `georef_check.jpg`, `georef_check_east.jpg` proof sheets
- `reference/cg-existing-maps/` Caribbean Guard's own published maps
- `docs/site-revamp/00-SYNTHESIS.md` **start here for the website**

## Not done

Nothing committed or pushed. `C:\Users\danie\caribbean-guard` is still not a git
repo. Given there is now real extracted data and a lot of tooling in here, it
probably should be, with the large source imagery excluded.
