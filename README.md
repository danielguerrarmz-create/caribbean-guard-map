# Caribbean Guard coastal safety map

A mobile-first interactive safety map for the Puerto Viejo to Manzanillo coast,
Limón, Costa Rica. QR codes go on posts along the sand; someone scans one and sees
whether they can swim where they are standing.

Built for **Caribbean Guard**, a Costa Rican nonprofit, via AJ (James A. Smith).

> **Not publishable yet.** Two things block it, and one of them is not code. See
> "Before this can be published" below.

## Start here

| | |
|---|---|
| Current state, decisions, gotchas | [`docs/handoffs/2026-07-30-georeference-solved-and-site-revamp.md`](docs/handoffs/2026-07-30-georeference-solved-and-site-revamp.md) |
| Website revamp | [`docs/site-revamp/00-SYNTHESIS.md`](docs/site-revamp/00-SYNTHESIS.md) |

## Run it

    npm install
    npm run dev

Vite serves `web/` and prints a LAN address so you can open it on a phone on the
same wifi, which is the only way to judge it honestly.

Deep links, which is what the QR codes use:

- `?z=cocles` opens a beach
- `?p=po4` opens an observation post

## Layout

    web/index.html              the map, self-contained apart from Leaflet
    web/img/base-lo.webp        45 KB overview, the only image fetched on load
    web/img/base.webp           1.19 MB base, fetched on first zoom or pan
    web/data/cg-hazards.geojson hazards extracted from Caribbean Guard's own sheet
    tools/                      georeferencing pipeline
    reference/cg-existing-maps/ Caribbean Guard's published maps, the source data
    docs/                       handoffs and the site revamp

## The georeference

The base is generatively upscaled Google Earth imagery, which cannot be aligned by
ordinary feature matching because the upscaler invents texture. `tools/refine.py`
solves it by local patch matching against Bing using a hand-read prior, and
`tools/rectify.py` resamples the result north-up into Web Mercator so Leaflet's
`imageOverlay` bounds are exact.

**Accuracy, measured by `tools/residual.py` against independent points:**

| | |
|---|---|
| Puerto Viejo to Punta Uva | 5 to 75 m, 8 of 14 points confirmed |
| East of Punta Uva | **not confirmable**, estimate 150 m |

The east cannot be verified because the upscale replaced the water and reef with
invented texture. That is a content problem as well: reef-protected versus open
water is the whole safety story at Manzanillo.

> `tools/georef.json` reports a 4.0 m residual. **That is not the accuracy.** It is
> RANSAC's residual on its own inliers, which is circular. Use `residual.py`.

Regenerate:

    cd tools
    python refine.py && python rectify.py                     # base
    python residual.py                                        # accuracy
    python georef_annot.py && python extract_annotations.py   # hazards

`tools/georef2.py` will re-download the Bing tile cache, which is gitignored.
`georef3.py` through `georef6.py`, `fit_profile.py` and `profile_match.py` are
failed approaches kept deliberately so they are not retried; the handoff has a
table of why each one failed.

## Hazard data

`web/data/cg-hazards.geojson` is machine-read off Caribbean Guard's own published
`Annotated Base Map V5.png` (georeferenced at 294 inliers, 1.2 m): 11 rip currents,
4 rescue stations, and 1 shaded polygon **deliberately left unlabelled** because it
is not in the sheet's legend and could be either a hazard zone or a designated safe
swimming zone. Guessing wrong inverts a safety message. Covers 1.82 km, about 11%
of the coast.

Every feature carries `needs_confirmation: true`. That must survive to production.

## The rule

**The interface may never claim more currency or more authority than its data has.**

No "real time", no "live conditions", no attribution to Caribbean Guard's guards
until they have signed off. Every verdict renders who reviewed it and when, reviews
expire after `REVIEW_VALID_DAYS`, and stale defaults to unknown rather than to safe.
An organization that admits what it has not checked is more trustworthy than one
that implies it has checked everything.

## Before this can be published

1. **Self-host Leaflet.** It currently loads from unpkg with no fallback, so a
   failed request on beach signal renders a dark blue void. The page also tells the
   user to save it for offline use with no service worker behind that promise. Both
   halves are the same fix.
2. **Every hazard needs an owner.** The zone descriptions are placeholder prose, and
   the extracted rip currents need Caribbean Guard to confirm and date them. A map
   that says DO NOT SWIM must be able to say who decided that and when.

Deployment target is Cloudflare Pages, not GitHub Pages, because Direct Upload lets
a non-technical person update it. Note that `caribbeanguard.org` DNS is at
WordPress.com, not Squarespace.
