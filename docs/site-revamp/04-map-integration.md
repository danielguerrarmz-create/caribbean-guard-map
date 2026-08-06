# 04. How the coastal safety map becomes part of caribbeanguard.org

Written 2026-07-30 against `C:\Users\danie\caribbean-guard\web\index.html` as it
stood at 10:19, the handoff at
`docs\handoffs\2026-07-29-mobile-safety-map.md`, `tools\georef.json`, and live
measurements of caribbeanguard.org.

Every timing and byte figure below was measured on an emulated iPhone 12 with
Chrome DevTools network throttling, using the same harness for the live site and
for the map, so the comparisons are like for like. Where something could not be
verified without access Daniel has to obtain, it is in the list at the end.

---

## The three findings that matter

### 1. The map must not be an iframe on a Squarespace page. The numbers are not close.

Measured, iPhone 12 profile, throttled with Chrome's own 3G presets:

| What | Transfer | Slow 3G, time to `load` | Fast 3G |
|---|---|---|---|
| `caribbeanguard.org/` homepage | 6.2 MB, growing to 14.4 MB | **59.2 s** | 16.0 s |
| `/programa-playa-organizada`, which holds today's static map | 3.1 MB | **67.3 s** | 17.7 s |
| Current map draft, `web/index.html` as it stands | 1.24 MB | 30.6 s | 7.7 s |
| **The same map with Leaflet self-hosted and a small overview base** | **86 KB** | **7.8 s** | **2.1 s** |

The last row is not a projection. I built it: copied the current `index.html`,
pointed it at a local Leaflet instead of unpkg, swapped the 1.13 MB `base.webp`
for a 1000x335 WebP at 29 KB, served it gzipped the way GitHub Pages and
Cloudflare Pages do, and measured. 85.9 KB across 4 requests, first contentful
paint at 1.2 s on Fast 3G.

An iframe on `/programa-playa-organizada` inherits that page's 67 second Slow 3G
load *before the iframe is allowed to start*. The 913 KB of Squarespace
JavaScript on that page is not optional and cannot be trimmed from inside
Squarespace. Whatever the map costs, the parent page costs 36 times more.

So: **the map is a standalone page, and the QR codes point directly at it.** An
embed on the Squarespace site is a secondary, desktop-oriented convenience, not
the delivery mechanism.

### 2. Cloudflare Pages, because of who has to update it after Daniel hands it over

Both hosts are free and both do custom subdomains with automatic HTTPS. The
decision is not technical, it is about the next person.

| | GitHub Pages | Cloudflare Pages |
|---|---|---|
| Cost | Free | Free |
| Custom subdomain + HTTPS | Yes, Let's Encrypt, automatic | Yes, automatic on deploy, including custom domains |
| Bandwidth | 100 GB per month, **soft** limit | Unlimited on the free plan |
| Site size | 1 GB published | 1 GB per deployment, 20,000 files, 25 MiB per file |
| Deploys | 10 builds per hour, soft | 500 per month |
| **Repo must be public** | **Yes on a free account.** Pages from a private repo needs GitHub Pro or Team | Not applicable |
| **Update without Git** | No. Someone needs a GitHub account and either `git` or the web file editor | **Yes. Direct Upload: drag a folder into the dashboard** |

Per finding 3, stage 1 is **six files totalling 1.25 MB**, so the limits are not a
constraint on either host and never become one, even if the tile pyramid is built
later.

The deciding line is the last one. Caribbean Guard is a small nonprofit on the
Caribbean coast. When a guard needs to change Cocles from danger to caution
because the sandbar moved, the realistic path is somebody logging into a
dashboard and dragging a folder, or editing one JSON file. Cloudflare Pages
Direct Upload supports exactly that. GitHub Pages requires a git workflow that
will decay the first time the person who knew it is unavailable.

**Recommendation: Cloudflare Pages, at `mapa.caribbeanguard.org`.**

One wrinkle nobody has mentioned yet, and it is a real one:
**`caribbeanguard.org` DNS is not managed at Squarespace.** The nameservers are
`ns1/ns2/ns3.wordpress.com`. `www` is a CNAME to `ext-cust.squarespace.com` and
the apex points at Squarespace's IPs, but the zone lives in a WordPress.com
account. Adding `mapa.caribbeanguard.org` means getting into that account, not the
Squarespace one. Nobody has mentioned a WordPress.com login, so this could be a
forgotten account from a previous site. Find out early, because it blocks the
custom subdomain and nothing else.

Fallback if that account is unrecoverable: run on the free
`caribbean-guard-map.pages.dev` subdomain. It works, HTTPS and all, and the QR
codes do not care what the hostname looks like. Losing the branded subdomain is a
dignity cost, not a functional one, and it should not hold up shipping.

### 3. Ship one image, not a tile pyramid. I had assumed the pyramid; the numbers do not support it.

I originally specced a 1,300 tile pyramid because the handoff called for one.
Pushed to price the single-image option against it properly, the single image wins
on every axis that matters here, and it wins decisively on the two that matter
most.

Both options measured on the same harness, iPhone 12 profile, gzipped server:

| | One image, progressive | Tile pyramid |
|---|---|---|
| Usable map, Fast 3G | **2.0 s at 86 KB** | 2.0 s at 86 KB, then tiles |
| Usable map, Slow 3G | **7.2 s at 86 KB** | 7.2 s at 86 KB, then tiles |
| Full detail arrives | +0.7 s Fast 3G, +24 s Slow 3G, in the background | only for what you look at |
| Best resolution | 3.33 m/px | 1.09 m/px nominal |
| Files to deploy | **6** | about 1,300 |
| Payload ceiling | **1.25 MB** | 5.5 MB on disk |
| **Fully precacheable offline** | **Yes, the whole map, 1.25 MB** | **No, shell plus z11 to z14 only** |
| Tooling to build and maintain | none, the file already exists | a tiler, a manifest, a redeploy story |

What makes the first column work is that **the 1.19 MB base does not have to be in
the critical path.** Paint the 29 KB overview, then request the full base at low
priority. First-useful is 86 KB either way.

This is easy to get wrong and I got it wrong on the first attempt: firing both
image requests together made them compete for the same 400 kbps and the map was
not usable until 31 s. Hanging the upgrade off the overview's `load` event and
setting `fetchPriority = "low"` fixed it. Copy that sequencing deliberately,
because the naive version silently cancels the whole benefit.

**Does the swap flash or shift? No. Measured, not assumed.**

| | Result |
|---|---|
| Cumulative Layout Shift | **exactly 0**, zero shift events recorded |
| Pixels differing by more than 8 of 255 | 5.1 percent |
| Pixels differing by more than 32 | 0.03 percent |
| Maximum delta on any pixel | 81 of 255 |

Layout shift is structurally impossible here: Leaflet image overlays are absolutely
positioned inside the overlay pane, and both overlays resolve to the identical rect
and identical transform. Nothing reflows. Visually the swap is a slight sharpening
of jungle texture and reef edges, not a flash. The overview stays underneath rather
than being removed, so there is no moment of blank.

**But the measurement turned up something better than the answer to the question.**
At the default letterboxed zoom the map overlay is 372x125 CSS px, which on a DPR 3
phone is 1116x375 device px. The overview is 1000 px wide. **The two are already at
the same effective resolution, so at the default view the 1.19 MB base buys
essentially nothing visible.** That is why the diff is so small.

The implication is a free improvement: **do not fetch the full base on load at
all.** Fetch it on the first zoom or pan past the default view, or on idle after
the user has clearly stayed. Someone who scans a QR code, reads their beach status
off the card and puts the phone away never downloads the 1.19 MB. The map costs
them 86 KB, full stop. Only someone who actually zooms in pays for detail, and they
pay for it at the moment they ask for it.

That makes the single-image option cheaper than the pyramid on first-visit bytes as
well as on every other axis, since the pyramid always fetches its first tiles.

**Two reasons the decision is not close.**

*Offline.* A phone on a beach with no signal can hold the entire map at full
available detail for 1.25 MB. The pyramid cannot, without shipping 5.5 MB on spec
that iOS will evict anyway. For an artefact whose purpose is working at the
water's edge, being completely precacheable beats nominal resolution.

*The resolution the pyramid would serve is false precision.* See the correction
below: ground accuracy is 5 to 75 m from Puerto Viejo to Punta Uva and **not
confirmable at all east of Punta Uva**, where the generative upscale invented the
water and reef texture. Serving 1.09 m/px tiles off imagery that is positionally
uncertain to 75 m, and partly fabricated in its eastern half, would dress a guess
up as a survey. A visibly softer image is the more honest artefact, and a guard
who knows that coastline will trust it more.

**Recommendation: stage 1 ships one rectified WebP plus the GeoJSON. No pyramid.**
Revisit only if a real guard reports the beach-level view is too soft to use.
The full pyramid spec is kept below for that case.

### 3b. If the pyramid is ever built, do not reach for GDAL

The georeference is finished and the base is rectified to an axis-aligned bounding
box, which is what removes the need for a reprojecting tiler.

> **Corrected 2026-07-30.** An earlier draft of this section read the 4.0 m figure
> in `tools/georef.json` as the accuracy of the georeference and concluded that
> "roughly 50 m" was out of date. That is backwards.
>
> 4.0 m is the RANSAC residual on the **14 inliers out of 109 control points**.
> RANSAC selects the subset that agrees with the model, then measures how well
> that subset agrees with the model. It is circular: it shows 14 points were
> mutually consistent, not that the model is right. A tight residual on a
> self-selected subset is exactly the failure that cost most of 2026-07-29 on this
> project.
>
> Ground accuracy comes from `tools/residual.py`, which matches 14 points along
> the coast against Bing independently: **5 to 75 m from Puerto Viejo to Punta Uva
> across 8 confirmed points, and not confirmable at all east of Punta Uva**, where
> the generative upscale replaced the water and reef with invented texture. The
> map uses 75 m west and 150 m east, combined with GPS error in quadrature.
>
> Internal consistency and ground accuracy are different claims. Do not let a
> number from a self-selected subset carry the word "accuracy".

The internal-consistency check below still stands on its own terms, and is worth
keeping: the Mercator aspect ratio of the declared bounds is 2.9890 and
`base.webp` is 5000x1673, which is 2.9886. Those agree to 0.02 percent, so the
rectification and the bounds are telling the same story about each other, which is
a genuine and useful check. It says nothing about where either of them sits on the
ground.

Because the extent spans only 0.050 degrees of latitude at 9.65 degrees north,
the difference between treating the rectified image as flat and treating it as
Web Mercator is **0.031 pixels at worst**. Three hundredths of one pixel. The
Mercator scale factor varies by 0.015 percent across the whole map.

Practical consequence: **the tiler is about 40 lines of Python with Pillow.** Slice
the rectified image on a linear grid, save each tile, done. No GDAL, no GeoTIFF,
no `gdal2tiles`, no reprojection step, no dependency that will be painful to
reinstall in two years. That removes the single most annoying piece of toolchain
from this project.

---

## Where things stand right now

Verified by reading the files, not assumed. `web/index.html` is being actively
edited by another agent and grew from 29.9 KB to 34.5 KB during this pass, so line
numbers move. The asset loading has not changed and every point below still holds:

- Leaflet 1.9.4 still loaded from `unpkg.com`, lines 8 and 186.
- One `L.imageOverlay("img/base.webp", IMG_BOUNDS, ...)`, line 345. No tiles.
  `base.webp` is 5000x1673, 1,189,862 bytes, 81.65 percent opaque, the transparent
  part being the corners left over from the 3.37 degree rotation.
- `IMG_BOUNDS` carries the georeference from `tools/georef.json`,
  `[[9.621462, -82.790863], [9.671534, -82.639053]]`.
- `img/base-lo.webp` exists at 118 KB, 1400x468. Nothing references it.
- `web/data/cg-hazards.geojson`, 8,809 bytes, 16 features. **Nothing loads it.**
  It is on disk and inert; the map still uses the hardcoded `ZONES` array. Wiring
  it up is stage 1 work.
- QR deep links `?z=` and `?p=` still work.
- **No service worker, no manifest, no cache handling of any kind.** Zero matches
  for `serviceWorker`, `caches.`, `rel="manifest"`.
- The interface tells the user "Guarde esta página. La señal es débil en la
  playa." / "Save this page. Signal is weak on the beach." On iOS that instruction
  currently does nothing useful. See the offline section.

Also worth knowing about the destination: the source imagery is
`Complete Mapping.jpg`, 15000x4219, 63.3 megapixels, at 109.4 cm per source pixel
over a 16.66 km span. That is the ceiling on any future tile detail, and per
finding 3 some of it is generative rather than observed.

---

## Embed or destination, and what the QR codes point at

### The QR codes point at the standalone map. This is not a close call.

`https://mapa.caribbeanguard.org/?z=cocles`

Reasons, in order of weight:

1. **Time to useful.** 2.1 s on Fast 3G standalone against 17.7 s for the
   Squarespace page that would host it, before the iframe starts. Measured.
2. **Vertical space.** Measured on the live site at iPhone 12 dimensions: the
   Squarespace header is **100 px tall** and the viewport is **664 px**. An iframe
   loses 15 percent of the screen to a header the person scanning the QR code did
   not ask for, on the device that has the least screen. On an iPhone SE the
   header is 91 px of 568 px, so 16 percent. The standalone map already uses
   `100%` height plus `env(safe-area-inset-*)` and gets all of it.
3. **The map controls its own chrome.** The standalone page puts `911` in a
   permanent top bar. Inside an iframe that bar sits below a Squarespace header
   that also has a hamburger menu, and the most important control on the page is
   now the second most prominent thing at the top of the screen.
4. **Scroll conflict.** A pannable map inside a scrollable page is a known bad
   interaction on touch. A drag intended to pan the coast scrolls the article
   instead, or the map traps the scroll and the visitor cannot get past it.
5. **A QR code that resolves to a page inside a page is harder to debug** when
   somebody reports that it does not work, and somebody will.

### The embed still has a job

Put a **link card**, not an iframe, on the Squarespace page: a still image of the
map, a heading, and a big button to `mapa.caribbeanguard.org`. It costs one image
and works on every Squarespace plan, including the ones without code blocks. That
is the version that ships first.

If and when the plan supports iframes, add one **on desktop only** on
`/programa-playa-organizada` where the map replaces `Annotated Base Map V5.png`
(register IDs `CG-69169` and `CG-0754B`, 1,482 KB each, uploaded twice). Desktop
has vertical space to spare and no QR scanner is involved. The iframe needs:

```html
<iframe src="https://mapa.caribbeanguard.org/?embed=1"
        title="Mapa de seguridad costera"
        allow="geolocation"
        loading="lazy"
        style="width:100%;aspect-ratio:16/10;border:0;border-radius:12px"></iframe>
```

Two details that are easy to get wrong:

- **`allow="geolocation"` is mandatory.** I checked the response headers on
  caribbeanguard.org: Squarespace sends `X-Frame-Options: SAMEORIGIN` and
  **no `Permissions-Policy` header at all**. With no header, `geolocation`
  defaults to `self`, which means a cross-origin iframe gets nothing unless the
  iframe element grants it. Without that attribute the "you are here" dot silently
  never appears, and it will look like a bug in the map.
- **`X-Frame-Options: SAMEORIGIN` cuts the other way.** It stops anyone framing
  *caribbeanguard.org*. It does not stop caribbeanguard.org framing our map. No
  action needed, but somebody will misread that header, so it is written down.
- `?embed=1` lets the map suppress its own duplicate branding when it knows it is
  inside a page that already has a header.

### What actually goes on the physical QR signs

- Include the human-readable URL under the code. Camera scanning fails in bright
  sun, in salt spray, on scratched laminate, and on old phones. A tourist who can
  read `mapa.caribbeanguard.org` off the sign and type it is not stranded.
- One code per post with `?p=poN`, so the sign knows where it is standing. That
  already works.
- Error correction level H, not the default M. These live outdoors, on a beach.
- Do not put a URL shortener in the path. It adds a redirect, a third-party
  dependency, and an extra round trip on the exact connection that cannot afford
  one. It also becomes a dead link the day the shortener account lapses.

---

## What ships: the base imagery and the data layer

### The base, stage 1

Six files. All of them already exist or are one export away.

```
index.html                  30 KB raw, 12 KB gzipped
vendor/leaflet.js           41 KB gzipped   <- vendored, not unpkg
vendor/leaflet.css           3 KB gzipped
img/overview.webp           29 KB           <- 1000x335, q70, the instant paint
img/base.webp             1,190 KB          <- the existing rectified 5000x1673, deferred
data/cg-hazards.geojson      9 KB           <- fetched at runtime
```

Critical path is the first four, **86 KB measured**. `base.webp` loads afterwards
at low priority. Note `img/base-lo.webp` already in the repo is 118 KB at
1400x468; the 29 KB version at 1000x335 is a better fit for this job, since the
overview only has to be good enough to recognise the coast and place the beach
cards, not to be read.

> **CORRECTION, 2026-08-06. The 86 KB figure above is stale and it was quoted
> onward as if it were current. Do not requote it.**
>
> Re-measured against the repo on 2026-08-06, before that day's work:
>
> | Asset | On the wire |
> |---|---|
> | `web/index.html` | 21,155 gz |
> | `leaflet.js` (unpkg) | 42,481 gz |
> | `leaflet.css` (unpkg) | 3,543 gz |
> | `web/img/base-lo.webp` | 88,718 |
> | `web/data/cg-hazards.geojson` | 1,179 gz |
> | **Total** | **157,076 B = 153 KB, 5 requests, 2 origins** |
>
> 78 percent over the number in this document. Two causes, and only one of them
> is an oversight: `index.html` had grown from 30 KB to 57.5 KB raw since this was
> written, and the 1000x335 overview specced two paragraphs up was never actually
> exported.
>
> **After the 2026-08-06 work it is 124,763 B = 122 KB over 7 requests and one
> origin**, with the overview re-exported (35,932 B), Leaflet vendored, and the
> manifest and one icon added. `index.html` grew again, to 37,455 gz, of which
> 16,912 is the inline design commentary. See
> `docs/handoffs/2026-08-06-map-schema-and-offline.md`.
>
> The lesson worth keeping: a critical-path figure in a plan is a measurement with
> a date on it, not a property of the design. This one was three numbers stale and
> nothing in the document said so.

### The data layer

`web/data/cg-hazards.geojson`, 8,809 bytes, 16 features:

| Geometry | Kind | Count |
|---|---|---|
| LineString | `rip_current` | 11 |
| Point | `rescue_station` | 4 |
| Polygon | `shaded_area_meaning_unknown` | 1 |

> **CORRECTION, 2026-08-06.** The counts above have not matched the file since the
> rip extraction was fixed in `bf601ce`. The file is now **9,885 bytes, 14
> features: 9 `rip_current`, 4 `rescue_station`, 1
> `shaded_area_meaning_unknown`**, and every feature now carries a stable `id`
> plus `authored` and `reviewed`. `needs_confirmation` is gone, replaced by
> `reviewed: null`, which renders on screen instead of only existing in the file.

It covers 1.82 km, about 11 percent of the 16.66 km base, and every feature
carries `"needs_confirmation": true` plus a file-level warning that it was
machine-read off a published graphic. Three things follow from that.

**1. Fetch it, do not inline it.** The whole point is that a beach status can
change without an engineer. Inlining it into `index.html` makes every edit a code
change. `fetch("data/cg-hazards.geojson")` at runtime, with the current hardcoded
`ZONES` array as the fallback if the fetch fails, which also covers the offline
case for free.

**2. Cache it differently from everything else.** A `_headers` file on Cloudflare
Pages:

```
/img/*
  Cache-Control: public, max-age=31536000, immutable
/vendor/*
  Cache-Control: public, max-age=31536000, immutable
/data/*
  Cache-Control: public, max-age=300, stale-while-revalidate=86400
```

Base imagery never refetches. Hazard data is at most five minutes stale, and
`stale-while-revalidate` means a weak connection shows yesterday's data instantly
rather than a spinner. **Squarespace cannot express any of this**, which is the
real reason it cannot host the map: not a file count limit, but no control over
cache headers.

**3. The `needs_confirmation` flag has to reach the screen.** It is currently
honest metadata that no user sees. Until a guard has confirmed a feature and dated
it, the map should say so on the feature itself. The unlabelled polygon is the
sharpest case: something is shaded on the original sheet, nobody knows what it
means, and leaving it deliberately unlabelled was the right call. Do not let a
later pass quietly invent a label for it.

Suggested per-feature fields to add when the guards review:
`confirmed_by`, `confirmed_on`, `review_due`. A feature past `review_due` renders
in the unconfirmed style automatically, so the map degrades honestly instead of
silently ageing.

### Who edits this after handover

This is the part that decides whether the map is alive in a year, and it is worth
being blunt: **if updating the map requires Daniel, the map dies when Daniel stops
answering emails.**

**The honest answer is that nobody at Caribbean Guard should ever edit
`cg-hazards.geojson`.** Here is one of its 16 features, verbatim:

```json
{ "type": "Feature",
  "geometry": { "type": "LineString",
    "coordinates": [[-82.71804, 9.645272], [-82.717735, 9.645516]] },
  "properties": { "kind": "rip_current", "length_m": 43,
    "direction": "seaward, inferred from sheet orientation",
    "needs_confirmation": true } }
```

That is a pair of six-decimal coordinates. There is no version of "train a
lifeguard to maintain this" that survives contact with reality, and pretending
otherwise is how projects end up with a CMS nobody asked for and nobody uses.

**The way out is that this is two different jobs wearing one filename.**

| | Hazard geometry | Beach status |
|---|---|---|
| What | where a rip current is, in coordinates | whether Cocles is danger, caution or safe today |
| Changes | rarely, when a rip actually moves | often, and it is the thing the map exists to say |
| Lives in | `data/cg-hazards.geojson` | the `ZONES` array, hardcoded in `index.html` |
| Who can edit it | someone comfortable with coordinates | should be any guard |

Right now the frequently-changing half is the one buried in a 34 KB HTML file, and
the rarely-changing half is the one in a tidy data file. That is backwards.

**Recommendation: split them.** Pull the status out into its own tiny file that
contains no geometry at all:

```json
{ "updated": "2026-08-14",
  "zones": {
    "playa-negra":  { "status": "safe",    "reviewed_by": "Elías",  "reviewed_on": "2026-08-14" },
    "salsa-brava":  { "status": "danger",  "reviewed_by": "Elías",  "reviewed_on": "2026-08-14" },
    "cocles":       { "status": "caution", "reviewed_by": "Naima",  "reviewed_on": "2026-08-12" },
    "chiquita":     { "status": "caution", "reviewed_by": null,     "reviewed_on": null },
    "punta-uva":    { "status": "safe",    "reviewed_by": "Naima",  "reviewed_on": "2026-08-12" } } }
```

Five lines a person can read. Changing Cocles from danger to caution means editing
one word and one date. That is a realistic ask for a non-technical person in a web
dashboard, and it slots directly into the provenance machinery already built into
`index.html`, which reads `reviewed: {by, on}` and expires a review after
`REVIEW_VALID_DAYS = 120`.

**So the tiers, honestly stated:**

| Tier | Who | What they touch | Realistic? |
|---|---|---|---|
| 1 | Any guard with the Cloudflare login | `status.json`, five lines, no coordinates | **Yes, if the split happens** |
| 2 | Same, via a form | a page with five dropdowns that writes `status.json` | Only if tier 1 is observed to fail |
| 3 | Someone technical | `cg-hazards.geojson` geometry | **Accept this constraint.** It changes rarely enough that "email whoever built it" is a legitimate answer |

Tier 3 is the constraint to accept rather than engineer around. Rip current
geometry moving is a once-a-season event at most, and when it happens somebody has
to go and look at the beach anyway. Do not build a geometry editor.

**Two things that matter more than any of this:**

1. **Someone at Caribbean Guard, not Daniel, owns the Cloudflare account**, and a
   second person also has the login. Written down. This is the single most
   important handover artefact and it takes five minutes.
2. **If the split does not happen, tier 1 does not exist**, and the true answer to
   "who edits this" is "Daniel, forever". Daniel should decide that consciously
   rather than discover it in six months.

---

## The tile pyramid, if it is ever needed

Deferred per finding 3. Specced here so the decision can be revisited without
redoing the arithmetic.

### Zoom range

Source resolution is 1.094 m per pixel. Web Mercator resolution at latitude 9.65:

| Zoom | m/px | Verdict |
|---|---|---|
| z13 | 18.84 | whole coast in one screen |
| z14 | 9.42 | |
| z15 | 4.71 | |
| z16 | 2.36 | |
| **z17** | **1.18** | **native. Matches the source's 1.094 m/px** |
| z18 | 0.59 | pure upsampling. Costs 4,256 more tiles and adds blur |

**Ship z11 to z17.** Stop at z17. Zooming past native resolution on imagery that
has already been through a generative upscale, which is what defeated six
georeferencing attempts per the handoff, makes the map look less trustworthy, not
more. Set `maxZoom: 17` on the tile layer and let Leaflet's `maxNativeZoom`
handle any request beyond it if a deeper zoom is ever wanted for the overlays.

### Tile count and weight

Computed against the exact rectified bounds:

| Zoom | Grid | Tiles | Cumulative |
|---|---|---|---|
| z11 | 1 x 2 | 2 | 2 |
| z12 | 2 x 2 | 4 | 6 |
| z13 | 4 x 3 | 12 | 18 |
| z14 | 8 x 4 | 32 | 50 |
| z15 | 15 x 6 | 90 | 140 |
| z16 | 29 x 11 | 319 | 459 |
| z17 | 57 x 20 | 1,140 | **1,599** |

The rectified image is 81.65 percent opaque, so roughly 18 percent of those tiles
are entirely transparent corner. Skipping them lands at **about 1,300 tiles**,
which is exactly the handoff's estimate arrived at independently.

Encoding weight, measured by cropping eight real 256 px tiles out of
`Complete Mapping.jpg` at native resolution and encoding them:

| Format | Mean tile |
|---|---|
| WebP q72 | 4.1 KB |
| WebP q80 | 5.2 KB |
| JPEG q72 | 7.1 KB |
| JPEG q80 | 8.6 KB |

**Use WebP q75, 256 px tiles.** Whole pyramid: **about 5.5 MB on disk**, roughly
1,300 files. Under every limit on both hosts. Keep a JPEG fallback only if
somebody produces evidence of a real visitor on a browser without WebP, which in
2026 means essentially nobody.

What matters is not the total, it is the first view. A 390x664 viewport at z13
pulls roughly 12 to 20 tiles, so **50 to 85 KB**, against the 1,482 KB static PNG
sitting on the Squarespace page today. Then zooming into one beach pulls that
beach's z16 and z17 tiles and nothing else. The visitor at Cocles never downloads
Manzanillo.

### Generation

```
tools/tile.py
  in:  Complete Mapping.jpg (15000x4219) + tools/georef.json
  out: web/tiles/{z}/{x}/{y}.webp   for z in 11..17
```

The whole thing is Pillow. Rectify once to the bounds already in `georef.json`,
then for each zoom, resize the rectified image to `2^z * 256` scaled to the
bounds, slice on the tile grid, drop any tile that is fully transparent, save as
WebP q75. Because the Mercator correction is 0.031 px it can be ignored; assert
that in a comment with the number, so nobody "fixes" it later by adding GDAL.

Two things to build in from the start:

- **Write a `tiles/manifest.json`** listing which `{z}/{x}/{y}` actually exist.
  Leaflet's `errorTileUrl` handles the gaps, but a manifest is what lets the
  service worker precache a sensible subset without probing 1,300 URLs.
- **Make it deterministic and re-runnable.** Same input, same bytes out, so a
  re-run only changes the tiles that actually changed and the deploy stays small.

In Leaflet:

```js
L.tileLayer("tiles/{z}/{x}/{y}.webp", {
  minZoom: 11, maxZoom: 17, maxNativeZoom: 17,
  bounds: BB, noWrap: true, keepBuffer: 4,
  errorTileUrl: "img/blank.png",
  attribution: "Caribbean Guard"
}).addTo(map);
```

with the 29 KB overview WebP kept underneath as an `imageOverlay` at low opacity
so the map is never blank while tiles arrive. That is the layer that makes the
first paint feel instant.

### Deploy and update, if tiles ever exist

Add `/tiles/` alongside the layout already described under "The data layer", with
the same one year immutable header the `/img/*` rule uses. Nothing else about the
deploy changes: the hazard data stays separate and stays short-cached either way,
which is the property that actually matters.

The one new cost the pyramid introduces is that a base imagery change stops being
"replace one file" and becomes "re-run the tiler and redeploy about 1,300 files".
Worth pricing that into any future decision to build it, because base imagery on
this project has already been re-cut more than once.

---

## Offline and weak signal

Be honest about what is achievable, because this is a safety artefact and
over-promising here is worse than under-delivering.

**What is realistic:**

1. **A service worker that precaches the entire map.** This is the payoff from
   choosing one image over a pyramid. `index.html`, Leaflet, the overview, the
   hazard JSON **and the full 1.19 MB base**, so about **1.25 MB total**. After one
   successful visit anywhere with signal, the map opens instantly and works with no
   connection at all, **at full available detail rather than coast-overview
   detail**. Cache-first for imagery, stale-while-revalidate for `data/`.

   Worth dwelling on, because it is the single strongest argument in this document:
   1.25 MB is less than a quarter of what the caribbeanguard.org homepage
   currently downloads in video alone on a Fast 3G visit. The whole safety map,
   permanently, for a fraction of what one unwanted autoplay buffer costs once.
2. **Precache on a deliberate action, not on arrival.** Do not fire a 1.19 MB
   background download at somebody who scanned a QR code on 400 kbps. Precache
   after the map is usable and the connection looks healthy, or behind an explicit
   "Guardar para usar sin señal" control that shows the size. The first visit stays
   86 KB either way.
3. **`Cache-Control: immutable` on `/img/*` and `/vendor/*`.** Free, and it means a
   returning visitor revalidates nothing.
4. **A real "works offline" state, not a spinner.** When the base cannot load, show
   the 29 KB overview with the beach cards and status labels over it, plus a
   dated line: "Datos guardados el 14 de agosto. Sin conexión." The beach cards
   already carry the status text before anything is tapped, which is the single
   best decision in the current draft, and it is exactly what survives offline.
   Because the overview is only 29 KB it can be inlined as a data URI in
   `index.html` if it comes to it, so the map is never blank even on a cold cache
   with one asset request.
5. **Add to Home Screen.** A web manifest turns the map into a launchable icon.
   This is what the line at index.html:282, "Guarde esta página", is reaching for
   and currently cannot deliver. Right now on iOS that instruction does nothing.
   Either back it with a manifest and a service worker, or change the wording.

**What is not realistic, and should not be promised:**

- **iOS evicts service worker caches** after roughly seven unused days, and clears
  them under storage pressure. A tourist who installs the map in San José and
  arrives at Manzanillo two weeks later may find it empty. Never let the interface
  say "available offline" as an unqualified promise. Say when the data was cached.

  > **CORRECTION, 2026-08-06. This is true, and it is stated in the form that
  > hides the fix.** Read as written, it says offline on iOS is a lost cause and
  > the most you can do is apologise with a timestamp. Two qualifications from
  > WebKit's own documentation change what to build:
  >
  > 1. It is seven days **of Safari use without interaction on the site**, not
  >    seven calendar days. A tourist who opens the map once a week keeps it.
  > 2. **Home Screen web applications are exempted.** WebKit, verbatim: they have
  >    "their own counter of days of use" reset by real interaction, and "We do not
  >    expect the first-party in such a web application to have its website data
  >    deleted." WebKit's storage-policy page adds that
  >    `StorageManager.persist()` excludes data from eviction and that it grants
  >    the request on heuristics including whether the site is a Home Screen web
  >    app. `navigator.storage.persist()` has been Baseline since December 2021.
  >
  > So Add to Home Screen is not the nice-to-have that finding 5 below calls it.
  > **It is the documented mechanism by which the cache survives on the platform
  > most tourists carry, which makes the manifest and the service worker one
  > feature rather than two.** Shipped 2026-08-06: manifest, worker, install
  > prompt, and a `persist()` call. The interface still never says "works
  > offline"; it says the page is saved on this phone, gives the date, states the
  > refresh cadence, offers a manual refresh, and says plainly that iOS may clear
  > it and that the home screen prevents that.
- **The first scan must work with no cache.** A tourist scanning a QR code on the
  sand has never visited before. The service worker helps the second visit, not
  the first. This is why the 86 KB critical path matters more than any caching
  strategy.
- **Geolocation needs no network but does need sky.** GPS works offline. What
  breaks offline is the Google Maps directions button at index.html:377 and 407.
  It should be visibly secondary to the 911 button, which works with no data at
  all, only signal.
- **A full offline pyramid would not have been on the table.** 5.5 MB downloaded on
  spec to a tourist's phone is not reasonable and iOS would not keep it. This is
  the constraint that decided finding 3: the single image is the version that can
  actually be held offline.

**Two things to fix in the current draft regardless of any of the above:**

- **Self-host Leaflet.** It is still loaded from `unpkg.com` at lines 8 and 186 of
  the current `index.html`. That is a separate origin needing its own DNS lookup,
  TCP handshake and TLS negotiation, roughly three extra round trips, which on a
  high-latency link is several seconds before the first byte of Leaflet arrives.
  It also cannot be precached by a service worker without CORS cooperation, and it
  means the map has a hard dependency on a third-party CDN staying up. Copy the two
  files in. It is 45 KB gzipped and it removes a whole class of failure.
- **Set an explicit timeout on imagery loading and on `getCurrentPosition`.** The
  geolocation call already has `timeout: 9000`. The image overlay has nothing. On
  one bar, Leaflet will sit on a half-arrived base indefinitely and the visitor
  sees a blank navy rectangle rather than a message. With the progressive base this
  matters less, since the overview lands first, but the deferred full base still
  needs a failure path.

---

## Squarespace Code Blocks: how they work and what breaks

**What a Code Block is.** A block you drop into any page that renders raw markup
inline in the page body. It is not an iframe and not a sandbox. The code runs in
the page's own document, alongside Squarespace's own scripts.

**What breaks, in the order people hit it:**

1. **The plan gate.** On the entry-level plan a Code Block accepts plain text,
   HTML, Markdown and CSS inside `<style>` tags. **JavaScript and iframes are a
   premium feature.** If somebody pastes an iframe on the wrong plan, the code
   stays in the block, the editor shows a note to logged-in admins, and
   **visitors see nothing at all**. That failure is silent to the public and
   invisible to anyone not logged in. It is the single most likely way this goes
   wrong.
2. **The editor rewrites your markup.** Squarespace's sanitiser reformats and
   sometimes reorders attributes on save. Unclosed tags, or anything that looks
   like it escapes the block, gets mangled. Keep the block to one self-contained
   element with no clever nesting.
3. **Fluid Engine will not size it for you.** A code block sits in a grid cell.
   An iframe with a percentage height inside a cell of unspecified height
   collapses to nothing. Use `aspect-ratio`, or a fixed `min-height`, never
   `height: 100%`.
4. **The editor preview is not the site.** Code blocks often render differently
   or not at all inside the editor. Always check the published page in a private
   window, on a phone.
5. **Editing risk.** Anyone editing that page in future can delete the block with
   one click and will not know what it was. Put an HTML comment at the top of the
   block saying what it is and who to contact.

**The exact question for AJ.** Squarespace renamed its plans, so the answer
depends on when the site was signed up, and asking about the wrong set of names
gets a confused answer. Ask this:

> Can you check which Squarespace plan Caribbean Guard is on? In the Squarespace
> dashboard it is under **Settings > Billing > Billing and plan**, or
> **Account and Security > Billing**. I need the exact plan name. It will be one of
> the current names, **Basic, Core, Plus or Advanced**, or one of the older names
> if the site has been going a while, **Personal, Business, Commerce Basic or
> Commerce Advanced**. I specifically need to know whether it is **Basic** or
> **Personal**, because those two are the only ones that cannot run the map embed.

**The 30 second test if billing access is a problem.** Anyone who can edit the
site can answer this without seeing the bill: add a Code Block to any page, paste
`<iframe src="https://example.com" height="200"></iframe>`, and save. If a notice
appears saying the code is not supported on this plan, it is Basic or Personal.
If it renders, the plan supports the embed. Delete the block afterwards.

**Why this is a scheduling question, not a blocker.** Because the QR codes point
at `mapa.caribbeanguard.org` and not at Squarespace, **the plan does not gate the
safety map**. It gates only the desktop convenience embed. If the answer comes
back Basic, the site gets a link card instead of an iframe and nothing else
changes. Do not let this question hold up stage 1.

I could not determine the plan from outside. I checked: there are zero code
blocks anywhere on the site, no code injection, and the native video block that
made me hopeful turns out to be available on every plan with 30 minutes of free
video storage. `Static.SQUARESPACE_CONTEXT` carries the template version, 7.1, and
the site id, but no entitlement information.

---

## Staged plan

### Stage 1: something real, on the beach. No Squarespace involvement at all.

Ship the map as it stands today, minus its performance problems, at a real URL.

- Self-host Leaflet, drop the unpkg dependency.
- Export the 29 KB overview and wire the progressive base: overview paints, full
  `base.webp` upgrades afterwards at low priority. **No tile pyramid.**
- Deploy to Cloudflare Pages. `mapa.caribbeanguard.org` if the WordPress.com DNS
  account can be reached, otherwise `*.pages.dev` and move on.
- Hazard data fetched from `data/`, not inlined, with the existing `ZONES` array
  as the offline fallback.
- `_headers` file: immutable on `/img/*` and `/vendor/*`, short plus
  stale-while-revalidate on `/data/*`.
- **Hazard data reviewed and signed off by Caribbean Guard's guards, with a date.**
  This is a hard gate, not a nice-to-have. `cg-hazards.geojson` currently carries
  its own warning that it was machine-read off a published graphic, and every one
  of its 16 features carries `needs_confirmation: true`. A map that says DO NOT
  SWIM has to be able to say who decided that and when. Nothing reaches a printed
  QR code before this is done.
- **Surface the uncertainty the data already admits to.** Unconfirmed features
  render in the unconfirmed style, and the positional accuracy caveat is visible
  rather than buried in a JSON comment. Especially east of Punta Uva, where the
  base imagery is not confirmable at all.
- Print QR codes for the four posts, error correction H, human-readable URL
  underneath.

Six files, 86 KB critical path, 1.25 MB total. A working, useful, scannable
artefact that does not depend on the Squarespace plan, the site revamp, or
anything else in this folder.

### Stage 2: connect it to the site

- Replace `Annotated Base Map V5.png` on `/programa-playa-organizada` with a link
  card to the map. Works on every plan. Removes 1,482 KB from that page, twice
  over, since the file is uploaded there twice.
- Write real alt text and on-page text for the hazard maps in the meantime. That is
  independent of the map work and should not wait for it. See
  `03-image-register.md`.
- **The nav plan in `00-SYNTHESIS.md` gives the map its own top-level slot**,
  "Mapa de Seguridad", pointing at the standalone page rather than at a relabelled
  `/programa-playa-organizada`. `/programa-playa-organizada` keeps its scope and
  gets a link card at the top. That supersedes an earlier version of the plan that
  folded the map into that page, and the reason it changed was the measurement in
  finding 1: putting a 2 second artefact behind a 67 second page throws away the
  reason for building it.

  The governing rule, which holds under either plan:

  > **The embed is the browse path. The standalone is the emergency path.**

  Someone on a sofa gets the map in context, next to the programme that produced
  it. Someone on the sand gets the standalone and nothing else, because they are
  not browsing. QR codes always point at `mapa.caribbeanguard.org` directly.
- Under the current nav plan **no iframe is needed at all**, which takes the
  Squarespace plan question off the critical path entirely. Keep the iframe
  guidance above only for the case where somebody later wants the map inline on
  `/programa-playa-organizada` as well. If that happens, `allow="geolocation"` is
  mandatory or the blue dot silently never appears.

### Stage 3: make it durable

- **Service worker precaching the whole map, about 1.25 MB**, triggered on a
  deliberate action rather than on arrival. This is the payoff for choosing one
  image over a pyramid, and it is the difference between a map that works on that
  beach and one that only works where there is signal.
- Web manifest, so Add to Home Screen works and the "save this page" line becomes
  true.
- A visible "data as of DATE" line, wired to `version.json`.
- Confirm tier 1 editing actually gets used, and only then consider tier 2. See
  "Who edits this after handover".

### Stage 4: the things that need other people

- English throughout, since tourists' phones are in English and tourists are who
  drown. The map already auto-detects. The rest of the site does not.
- Tide data on `/chiquita`, which is the one beach whose status genuinely changes
  with the tide, per the current zone copy.
- A reporting path so a guard can flag a new rip from their own phone.

---

## Needs confirmation

Things I could not verify without access Daniel has to obtain.

1. **Which Squarespace plan.** Not determinable from outside. Question and
   self-test above. Gates the iframe only, not the map.
2. **The WordPress.com account that holds `caribbeanguard.org` DNS.** Nameservers
   are `ns1/ns2/ns3.wordpress.com`. Somebody has to be able to log in to add
   `mapa.caribbeanguard.org`. If nobody can, the fallback is a `pages.dev`
   subdomain.
3. **Who owns the Cloudflare account.** It should be a Caribbean Guard address,
   not Daniel's, or the map has a single point of failure that walks out the door
   with him. Same question for whoever holds the domain.
4. **Every hazard zone in the current draft.** The five zones and four posts in
   `web/index.html` were written from general knowledge of the coast, and
   `cg-hazards.geojson` was machine-read off a published graphic. Both carry
   warnings saying so. Needs the guards, and needs a date attached.
5. **Whether the four posts are correct**, staffed and proposed, and whether the
   9:00 to 17:00 hours are current and the same year-round.
6. **Whether 911 is the right number** for a water rescue on that coast, or
   whether Caribbean Guard has a direct line that reaches a guard faster. The
   911 button is the most important control on the map and it is currently an
   assumption.
7. **The homepage video.** Unrelated to the map, but see `03-image-register.md`.
   It is 96 percent of the homepage payload and it is the cheapest fix available
   anywhere in this project.
8. **Whether 3.33 m/px is good enough at the beach.** This is the one open question
   behind finding 3, and it is answerable by a person rather than by measurement:
   show a guard the map zoomed to Cocles on a phone and ask whether they can tell
   which stretch of sand it is. If yes, the pyramid never gets built. If no, the
   spec is ready. Do not decide this from a desktop screen.
9. **What the unlabelled polygon in `cg-hazards.geojson` means.** One shaded area
   on the original sheet whose legend entry does not exist. Leaving it unlabelled
   was correct. Somebody at Caribbean Guard drew it and knows why.

---

## Method

- Live page and map timings: Playwright, Chromium, `iPhone 12` device profile,
  390x664 viewport at DPR 3, throttled with `Network.emulateNetworkConditions`
  using Chrome DevTools' own Slow 3G (400 kbps, 2000 ms RTT) and Fast 3G
  (1.6 Mbps, 562 ms RTT) presets. Same harness for every row.
- Proposed-architecture timing: two prototypes, both built from the current
  `web/index.html` copied to a scratch directory, served from a local gzipping HTTP
  server so text assets compress the way they would on either host. Measured, not
  modelled.
  - *Prototype 1*, the critical-path floor: Leaflet vendored locally, `base.webp`
    replaced outright by a 1000x335 WebP q70. 85.9 KB.
  - *Prototype 2*, the progressive two-step actually recommended: overview plus a
    deferred `base.webp`, upgraded on the overview's `load` event with
    `fetchPriority = "low"`. Instrumented to record when each asset's headers
    arrive, so "usable" and "full detail" are separate measurements rather than one
    load figure.
  - The first attempt at prototype 2 fired both image requests together and
    measured 31 s to usable on Slow 3G, because they competed for the same
    bandwidth. That failure is reported in finding 3 rather than quietly fixed,
    because whoever implements this will hit it.
- Tile counts: Web Mercator tile arithmetic against the exact bounds in
  `tools/georef.json`.
- Tile weights: eight 256 px crops taken at native resolution from
  `Complete Mapping.jpg` and encoded with Pillow.
- Header height and viewport: measured on the live site via
  `getBoundingClientRect` at three device profiles.
- Response headers: direct HEAD and GET against caribbeanguard.org.
- DNS: `nslookup` against 8.8.8.8.
- Nothing in `C:\Users\danie\caribbean-guard\web\` was modified. Another agent was
  editing it during this session.
