# Caribbean Guard, 2026-07-29: pivot to a mobile safety map

## What

Two things happened today.

**1. The deliverable changed shape.** It is no longer a printed banner. It is a
mobile-first interactive safety map, embedded on caribbeanguard.org, with QR
codes placed along the coast so someone standing on the sand can scan and
immediately see whether they can swim where they are. A working draft exists.

**2. Georeferencing the base image was attempted and is NOT finished.** Six
approaches were tried. None produced a validated transform. Best current
estimate is a hand-read prior, good to a few hundred metres, unvalidated.

## Why

A print banner is a poster. The actual failure mode being designed against is a
tourist drowning in a rip current at Cocles, so the artefact has to be on the
phone of the person in the water's edge, in their language, in one tap.

Georeferencing matters because without it the "you are here" blue dot is
decorative. A safety map that shows you in the wrong bay is worse than one that
shows nothing.

## Verify

    cd C:\Users\danie\caribbean-guard\web
    python -m http.server 8777 --bind 0.0.0.0

- Phone, same wifi: http://192.168.1.223:8777/index.html
- Desktop: http://127.0.0.1:8777/index.html
- QR deep link: http://127.0.0.1:8777/index.html?z=cocles
- Post deep link: http://127.0.0.1:8777/index.html?p=po4

Checked in a 390x844 viewport: no console errors, no dead grey bands, sheet
opens from both a card tap and a deep link.

## What the draft does

- **Beach picker, not a legend.** Bottom control is a horizontal row of beach
  cards showing status before anything is tapped. Nobody pans a 12 km map to
  find themselves; they read the name off the sign behind them.
- **Cover, not contain.** Computes the zoom at which the image fills a portrait
  viewport and locks that as `minZoom`.
- **Status never relies on colour alone.** Danger dotted, caution dashed, safe
  solid, plus a text label on every card.
- **Language auto-detects, ES fallback.** Tourists' phones are in English and
  tourists are who drown.
- **911 permanent** in the top bar.
- **QR deep links** via `?z=` and `?p=`.

## Georeferencing: what was tried and why each failed

Recorded so the next session does not repeat any of it.

| Approach | Result | Why it failed |
|---|---|---|
| SIFT feature match (`georef.py`) | 5 inliers | The generative upscale destroyed fine texture, so there is nothing real to match |
| Filled land/water mask + ECC (`georef3.py`) | Degenerate | Large uniform ocean and jungle dominate; score just rewards the smallest template |
| Edge correlation, TM_CCOEFF_NORMED (`georef4.py`) | Spurious `corr 1.0000` | Edge maps are mostly empty; where the reference patch is flat the normalising denominator collapses |
| One-way chamfer (`georef5.py`) | Monotone to sweep edge | A small footprint sits entirely near the shore and scores well while explaining nothing |
| Symmetric chamfer (`georef6.py`) | Still monotone | The reverse term only samples reference coast *inside* the footprint, so it does not punish shrinking either |
| 1-D shoreline profile fit (`fit_profile.py`) | 219 m residual, +11.3 deg | Implausible rotation; the fit is not converging |

**What did work: reading the two images side by side.** `cmp_bing.jpg` (Bing
with longitude gridlines) against `cmp_base.jpg` (base with fractional
gridlines) gives an unambiguous answer:

- Puerto Viejo town on its headland: **0.25** of base width = **-82.7545**
- Punta Uva point with its lagoon: **0.645** = **-82.695**
- East end runs through the reef crescent to Manzanillo at ~0.95

**Confirmed: the base image DOES reach Manzanillo.** It spans roughly
**-82.792 to -82.642, about 16.5 km**, at roughly **110 cm per source pixel**.
This resolves the coverage question that was open at the start of the day, and
it independently agrees with the discarded SIFT run (16.79 km), which suggests
that run was closer to right than its inlier count implied.

Current prior, **unvalidated, do not ship**:

    IMG_BOUNDS = [[9.6240, -82.7922], [9.6667, -82.6416]]

## Left to do

1. **Finish the georeference.** `refine.py` is the live approach: local patch
   matching against Bing inside a small search window, using the hand-read
   prior. It was mid-run when the session ended, rejecting all but 7 control
   points. Next step is looser thresholds (peak 0.22, distinctness 0.03) and a
   denser candidate grid. Then run `validate.py`, which renders the same three
   landmarks from Bing and from the georeferenced base side by side. Do not
   accept the transform until that sheet looks right.
2. **Tile pyramid and hosting.** The base is 63 MP and needs roughly 1,300 tiles.
   Squarespace cannot host a tile directory. Host on GitHub Pages or Cloudflare
   Pages and iframe it in; QR codes should point at the standalone URL, not the
   Squarespace page.
3. **Confirm the Squarespace plan.** Code Blocks need Business or above.
4. **Hazard data has no owner yet.** Every zone in the draft is a placeholder I
   wrote from general knowledge of that coast. Cocles genuinely is the rescue
   hotspot and Punta Uva genuinely is reef protected, but a map that says DO NOT
   SWIM must be able to say who decided that and when. This needs AJ and
   Caribbean Guard's guards.
5. **The stitched base still has tone mismatch** between panels and a straight
   horizontal seam in the water, plus 179 DPI at 7 ft if the print version ever
   comes back.

## Files

- `web/index.html` draft map, self-contained apart from Leaflet from CDN
- `web/img/base.jpg` 5000 px working base, 1.27 MB
- `tools/refine.py` live georeferencing approach
- `tools/validate.py` visual proof sheet, not yet run
- `tools/cmp_bing.jpg`, `tools/cmp_base.jpg` the side-by-side that gave the answer
- `tools/tilecache/` 1395 cached Bing z17 tiles, reusable
- `tools/georef*.py`, `fit_profile.py`, `profile_match.py` failed approaches, kept as a record

Source PSD and JPG remain in `C:\Users\danie\Downloads\caribbean-guard-cuts\`.

## Not done

Nothing was committed or pushed. `C:\Users\danie\caribbean-guard` is not a git
repo. If this should be version controlled, it needs `git init` and a decision
about whether the large source imagery belongs in it.
