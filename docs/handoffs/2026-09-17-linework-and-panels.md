# Caribbean Guard map, 2026-09-17 (afternoon): the linework and the panels

Branch `feat/ui-overhaul`, on top of `a37c063`. Nothing committed yet, nothing
deployed. Supersedes parts of `2026-09-17-ui-overhaul.md` from this morning; read
that one first for everything not listed here.

Six findings from Daniel against the morning's preview, all six addressed.

**Preview:** `python -m http.server 5173 --directory web` then
http://127.0.0.1:5173/

## 1. The linework followed the reef, not the coast

Daniel marked the drawn line in red and the real shore in yellow. The two
disagree by 20 to 130 m, and the diagnosis is in the numbers rather than in the
picture:

| zone | traced length | true coast | excess |
|---|---|---|---|
| playa-negra | 1618 m | 1625 m | -0% |
| salsa-brava | 2303 m | 1294 m | **+78%** |
| cocles | 4224 m | 3202 m | +32% |
| chiquita | 4439 m | 3055 m | +45% |
| punta-uva | 3119 m | 2830 m | +10% |

`trace_coastline.py` found the shore by flood-filling a water mask out of the
satellite mosaic and thresholding on brightness (`v < 60` is sea). Shallow water
over live coral is BRIGHT, so the mask read every reef as land and the contour
walked around each reef patch instead of along the beach. Playa Negra is the one
zone with no reef near the shore and it is the one zone that was right, which is
what makes this a diagnosis rather than a guess. Smoothing cannot fix it: the
extra kilometre at Salsa Brava IS the reef, traced.

**New source: OpenStreetMap `natural=coastline`**, a human tracing of the mean
high water line that knows a reef from a beach. Three open ways chain end to end
across this coast; the 9-to-12-point closed ways in the same box are islets and
are dropped. `tools/osm_coastline.py` chains them, resamples at 10 m, offsets
25 m seaward along the local normal, clips per zone, simplifies at 6 m, Chaikins
twice. Output: **258 points and 6.0 KB**, against 2,821 points and 62 KB.

- `tools/osm_coastline.py` — new, with the full argument in its docstring
- `tools/osm-coastline.json` — the cached Overpass response, so the build is
  reproducible offline. `--fetch` re-queries.
- `tools/export_zones.py` — **RETIRED and now exits 1.** Running it would
  overwrite the fix with the reef trace, in place, with a success message.
  Commit `7d6baa1` is titled after the last time that happened. Original source
  at `6be0f66:tools/export_zones.py`.
- Weights halved: `TARGET_M` 30 to 14, `K_MAX` 1.3 to 1.0 in `web/geometry.js`.
  The `high` stroke was **14.3 px at z17**, which is 13 m of ground, a band as
  wide as half the beach. It is 7 px now. The tier ranking and all three dash
  textures are unchanged.

**The spans changed and the joints are now exact.** The old values came off the
reef trace, so Cocles overlapped Chiquita by 171 m and Chiquita overlapped Punta
Uva by 172 m: two tiers claiming the same water. Each joint is resolved at the
midpoint, which also closes the 26 m and 70 m gaps at the other two. The five
zones now tile the coast exactly once, verified at 0.0 m between every pair.

## 2 and 3. The blue boxes and the repeated text

- **The navy swatch box is gone** (`<rect fill="#24384a">`). Eight of them down a
  white rail was a third container layer around 24 px of line. The swatch now
  draws the stroke's weight and dash exactly and its colour in the light-ground
  `--*-text` variant; only moderate differs in hue, and that was already true of
  the bar beside it.
- **The tinted panel behind every instruction is gone** (`background:#f2f5f8`),
  and so is the grey panel behind the why and the boxed deferral.
- **The solid tier bar is gone too.** It and the swatch were the same colour
  token 10 px apart; the swatch carries colour AND texture. One tier mark per
  instruction.
- **The provenance chips are gone from the cards.** "Sin revisar" and "Sin
  recorrer" rendered on all five beaches, always, because nothing is reviewed and
  only the middle 1.86 km is surveyed. Ten marks that never differ cannot
  distinguish one beach from another, which is the rail's only job. The claim
  moves to the sheet's trust line. If one beach is ever reviewed and its
  neighbours are not, that rule inverts and the chip comes back.

The rail is now: brand, one line of what this is, the saved-offline row, five
beaches, the rest-of-the-coast card, the bilingual legend.

## 4. The beach extent band

Selecting a beach now draws its extent, **on the water only**. The zone line and
the same line pushed 120 m further seaward, filled at 22% in the tier colour.

- **Solid end caps.** Where one beach stops and the next starts IS a decision
  somebody took, on continuous sand, and it is what a reader needs when the
  instruction changes under their feet.
- **Dashed seaward edge.** The hazard does not stop at 120 m; that is how far out
  this beach is still this beach. A fill alone was invisible over reef imagery.
- **No landward edge at all.** Nothing here is entitled to draw a line across
  somebody's garden on imagery accurate to 75 m.
- Own pane at z-index 350, between the tiles and the strokes, so it can never
  dilute the line that carries the instruction. Drawn from z13 up: a deep link to
  Cocles on a 390 px phone with the sheet open fits at z13.75, so a floor of 14
  removed the band on exactly the device this was built for.

## 5. The sheet is a lifeguard sign

Order: name, sub, **instruction**, hours, one sentence of why, the exceptions
that change the instruction, the escape sentence, a full-width **Call 911**, one
trust line, then Directions and Report an error.

Deleted: the Autor/Revisado row, the TODAY line, the "Sin revisar" box, the
"Fuera del recorrido" box, the boxed deferral and the facts bullet list. The four
absence surfaces said the same thing in four visual languages and together took
more height than the instruction, the reason and the escape combined.

**The trust line** replaces all four, and it still carries `t.defer` word for
word. Daniel's ruling: sign plus one trust line.

> **Nobody at Caribbean Guard has reviewed this beach.** If there is a lifeguard
> or a flag on the beach, that beats this map. This map cannot see today's sea.

The five `why` strings were cut to one or two sentences; the one fact per beach
that changed what a swimmer would do was folded in, the rest described the place.
The escape sentence is untouched and still renders on all five beaches.

PEEK went 33vh to **42vh**: the sheet is shorter overall, but the 911 button moved
up into the opening view and at 33vh it was cut through the middle.

**Five functions were deleted, not left unreferenced:** `absences`, `cardChips`,
`gapList`, `factsOf`, `todayBlock`. This page renders its cards twice already
(static HTML for first paint, `cardHTML()` on a language switch); a third path
nothing calls is a trap. `todayState` and `todayHalo` stay live, because the map
still draws a signed bulletin as a halo. The TODAY vocabulary stays in `T`, in
both languages, because that axis is waiting on the signing surface, not
cancelled.

## 6. Type

**Inter replaces Atkinson Hyperlegible**, self-hosted, latin subset, 400 / 600 /
800, 71 KB against 35 KB. Daniel's call, knowing the trade: Atkinson is the
better letterform-by-letterform font for a low-vision reader, and it shipped in
two weights, which cannot build a hierarchy across six levels.

Scale **30 / 21 / 17 / 15 / 13 / 12**, was 22 / 18 / 15 / 13 / 12. The heading
was 1.22x the instruction and 1.47x the body, so nothing could dominate. Size is
never the only signal now: 800 ink instruction, 600 ink names, 400 ink body, 400
muted secondary. 12 px is still the floor.

`web/sw.js` is `cg-map-v4`; CRITICAL is **155 entries at 1,596 KB**, down from
165 at 2,070 KB. The three fonts cost 36 KB and the geometry gave back 56 KB.

## The guard was extended and mutation-tested

`tools/check_copy.js` scoped the deferral rule to each sheet renderer's own body,
so delegating to `trustLine()` failed it. It now accepts the indirect route and
checks `trustLine()` itself by the same regex.

It also had a real hole: `live.indexOf("function " + name)` matched a PREFIX, so
renaming `trustLine` to `trustLineX` and leaving the call site pointing at
nothing still passed. Anchored on `function NAME(` now.

Five mutations, each exits 1, control exits 0:

| mutation | exit |
|---|---|
| `trustLine()` drops `t.defer` | 1 |
| `openZone()` drops the trust line | 1 |
| `trustLine` definition renamed | 1 |
| `openZone` renamed | 1 |
| `openVoid()` drops `t.defer` | 1 |
| unmutated control | 0 |

## Verify

```
node tools/check_copy.js            # PASS, 9 banned-word rules, 8 tier labels, 5 sheets
python tools/osm_coastline.py       # 258 points, 6.0 KB, prints the resolved spans
python tools/build_tiles.py         # precache audit: 15 hand-written entries, all present
python -m http.server 5173 --directory web
```

Checked live at 1550x784 and 390x844, both languages, every sheet
(5 zones, void, legend, post, rip, area): no console errors, `t.defer` present in
all ten, language switch re-renders the open sheet.

## Left

0. Fixed after Daniel's ruling: `tools/render_annotated.py` now reads
   `web/data/zones-geometry.json` instead of `tools/coastline.json`, re-keying
   the full zone ids to the short names `SHEETS` uses. All four sheets
   re-rendered, and they picked up the tightened `why` copy in both languages at
   the same time. The map and the sheet read ONE file now, so they cannot
   disagree about where the water is.

1. The **Punta Uva sheet carries two caveats plus the lower-risk rider**, which
   is three qualifying paragraphs on the calmest beach. Both caveats genuinely
   change the instruction on a named part of the beach, so neither was cut
   without Daniel. It is the one sheet still longer than a sign.
2. **THE PRINTED SHEETS CARRY A SECOND COPY OF THE SAFETY VOCABULARY.**
   `tools/render_annotated.py` has its own English tier labels and its own
   English deferral, and they have drifted from the page:

   | | the page | the sheet |
   |---|---|---|
   | `no-swim` EN | STAY OUT OF THE WATER | DO NOT ENTER THE WATER |
   | deferral EN | that **beats** this map | that **overrides** this map |

   `tools/check_copy.js` checks the page's eight labels and cannot see these.
   This is the same class of fault as the geometry fixed above, one axis over:
   two copies of a safety string, one of them unguarded. Not changed here,
   because rewording a printed safety instruction is Daniel's and AJ's call, not
   a tidy-up. Decide which wording is right, then make the sheet read the page's
   strings rather than its own, and extend check_copy to cover it.

   `tools/coastline.json` and `tools/trace_coastline.py` are left on disk as the
   record of what was measured off the imagery. Nothing reads them now.
3. Everything in the morning handoff's governance list still stands: TODAY has no
   way in, no beach is reviewed, the QR address must not be a vercel.app URL.

## Files

- `tools/osm_coastline.py`, `tools/osm-coastline.json` — new
- `tools/export_zones.py` — retired, exits 1
- `tools/check_copy.js` — indirect deferral, prefix-match hole closed
- `web/data/zones-geometry.json` — regenerated, 62 KB to 6.0 KB
- `web/index.html` — fonts, scale, cards, sheet, trust line, extent band, spans
- `web/geometry.js` — stroke weights halved
- `web/sw.js` — `cg-map-v4`, Inter in CRITICAL
- `web/fonts/` — Atkinson out, `inter-latin-{400,600,800}-normal.woff2` in
