# 2026-08-06 · Map schema, absence states, and the offline copy

Written against `web/index.html` at 117,848 bytes, `web/data/cg-hazards.geojson`
at 9,885 bytes (14 features), and the four precedent documents under
`docs/precedents/`.

Everything below was verified in a real browser, headless Chrome 150 over CDP,
against `web/` served by `python -m http.server 5199`. That is the production
shape rather than the local site build: no vite client injection, no site
wrapper, service worker at scope `/`. Byte figures are measured, gzip -9 for text
and raw for images, which is the same method that produced the 153 KB figure in
`docs/precedents/01-mapping-tools.md`.

---

## What

### 1. `status` split into two axes, and one of them is new

`ZONES[].status` was a single word carrying two claims that change on different
timescales: that Cocles is the beach with the most rescues on this coast (true
for years) and that Cocles is dangerous today (true for hours). Ireland's EPA
refuses to merge those and labels both prominently. Now:

```js
character: { class, authored, reviewed, why, facts, caveats }   // years
today:     { notice, by, org, at } | null                       // hours
```

`character.class` has **four** values against **three** visual tiers:

| class | tier | ES label | EN label |
|---|---|---|---|
| `no-swim` | high | NO ENTRES AL AGUA | STAY OUT OF THE WATER |
| `high-risk` | high | SOLO CON GUARDAVIDAS | ONLY WITH LIFEGUARDS |
| `conditional` | moderate | REVISA ANTES DE ENTRAR | CHECK BEFORE YOU GO IN |
| `lower-risk` | low | TEN CUIDADO IGUAL | TAKE CARE ANYWAY |

Four classes because "never swim here" (Salsa Brava) and "swim only in front of
the guard post" (Cocles) were both `danger`, which is the same flattening the
split exists to undo. Three tiers because the stroke vocabulary's brightness
ladder only works with three, and that ladder is load bearing in sunlight.

`today` has three notices, `no-swim` / `care` / `normal`, and `normal` carries an
explicit rider that nothing unusual is not the same as safe.

**beaches.ie's stars do not transfer, and the file says why in a comment.** A
star count is an ordinal quality rating averaged over four seasons of sampling.
There is no sampling programme here, and a hazard character is not
better-or-worse, it is a different kind of water. What transfers is the
principle: the two axes are encoded in different channels. Character is colour
plus weight plus dash and it owns the map stroke. Today is a dated bordered block
with a person and an organisation on it, in violet (`--today`), a hue outside the
hazard palette so it cannot be read as a tier, and it never recolours the line.
When a bulletin exists it draws an additive halo underneath the character stroke,
so both claims stay legible at once.

### 2. Three rules now govern the level names, not one

The first pass of this work fixed only the second of these, and it was not
enough. Recording the mistake because it is instructive: replacing
`SE PUEDE NADAR` with `MENOS RIESGO` removes the permission but produces a
**rating**, and a rating tells you how bad somebody thinks it is rather than what
to do. The whole vocabulary had drifted from instructions into ratings.

**1. Every level name is an instruction.** SMN Argentina's levels are
"Informate", "Preparate", "Segui instrucciones oficiales": the level name *is*
the action. `RIESGO ALTO` is a rating and it is not good enough. See the table
above; every label now contains a verb the reader can act on.

**2. No level name reads as permission.** `SE PUEDE NADAR` / `SWIMMING OK` was a
stronger claim than the lowest tier of the United States national rip current
forecast is willing to make, on imagery uncertain to 75 m, about beaches no guard
has reviewed. NOAA's LOW tier does not contain the word safe. Ours is
`TEN CUIDADO IGUAL` / `TAKE CARE ANYWAY`, plus NOAA's structure-naming sentence
on every `lower-risk` character:

> Que el riesgo sea menor no quiere decir que sea seguro. Todavía puede haber
> corrientes de resaca peligrosas junto a los arrecifes, los canales, las puntas
> y las bocas de río.

NOAA names groins, jetties, reefs and piers; those are adapted to structures that
exist on this coast, which is also exactly the Punta Uva case.

**3. Every level defers downward**, to the guards and the flags on the sand. This
is SLSA's third move, which we were missing: after downgrading the artefact and
naming the reason, hand the reader a rule that still works when the artefact is
wrong. `T.defer` renders under **every** character, and also on the rip current
sheet and the unmapped-coast sheet:

> Si hay un guardavidas o una bandera en la playa, eso manda sobre este mapa.
> Este mapa no ve el mar de hoy.

It is styled unlike a caveat on purpose: solid ink border, no fill. A caveat
qualifies the verdict above it; this outranks the verdict above it.

**Note the conditional phrasing, and do not "fix" it.** Caribbean Guard's rescue
towers at Cocles and Playa Grande are verified. A red flag *system* along this
coast is not: our own Cocles copy asserts one and nobody has confirmed it. "If
there is a guard or a flag" is true whether or not the system exists, and it is
stronger than asserting it. It becomes "obey the flags" only once Caribbean Guard
confirms there are flags to obey, which is open question 1 below.

### 3. The Punta Uva contradiction is fixed

Punta Uva was `safe` while its own third `facts` bullet said "avoid the channel at
the far east end, there is current there", stranded where nothing could act on it.
`character.caveats[]` is new: a caveat renders as its own bordered block directly
under the character, above the provenance, so an exception modifies the verdict
where the verdict is read. Playa Chiquita gained one too, for low tide.

### 4. Three absences, three marks, never one banner

Safeswim publishes two distinct pins for two distinct kinds of not knowing. Ours
has three and they can co-occur, so they render as a stack:

| state | mark | when |
|---|---|---|
| `never` | amber `?` | `character.reviewed` is null |
| `expired` | amber `!` | reviewed, older than `CHARACTER_VALID_DAYS` |
| `unsurveyed` | grey `⌀` | the whole zone is outside Caribbean Guard's annotated sheet |
| `partial` | grey `◐` | part of it is |

They render in three places: a chip row on every picker card, visible before
anything is tapped; a sentence list in the sheet; and, for the third, a permanent
hatched card at the end of the picker reading "El resto de la costa · Sin
describir", which opens a sheet computing the real numbers from loaded data
(16.7 km imaged, 9.4 km described, 1.86 km surveyed).

**The old coverage toast is gone.** It fired six seconds after load and vanished.
Four of the five beaches are entirely outside the surveyed window and the map
never said so per beach; now every one of them carries the mark permanently.

The surveyed window is seeded from a constant so the picker renders before the
fetch, then recomputed from the fetched features so it cannot drift from what is
drawn.

### 5. Ids namespaced, `org` and `authored` on provenance

`<org>:<type>/<local>`: `cg:zone/cocles`, `cg:station/est1`, `cg:rip/fdae545d`,
`cg:area/d5a5d841`. QR deep links carry the **local part only**, so `?z=cocles`
and `?p=est2` still work and the codes already printed stay valid.

Rip and area ids are a sha1 of the rounded geometry, so re-extracting an unchanged
sheet reproduces them exactly and an id changes only when the feature moves, which
is the correct trigger. **Station ids are positional, west to east**, because the
numbering is already published on the markers and inside QR codes and has to
survive a re-extraction even when a station moves; a fifth station is a
renumbering decision for a human, and `extract_annotations.py` now prints a notice
when the count changes.

Provenance follows OVSICORI, whose every earthquake popup carries `Autor` and
`Revisado`. Both render as separate rows, always:

```
Autor:    escrito desde conocimiento general, sin visita al sitio
Revisado: nadie todavía
```

`reviewed` gained `org` alongside `by`, so the record answers which organisation
stands behind a verdict, not only which person typed it. `needs_confirmation` in
the geojson is replaced by `reviewed: null`, which was true in the file and
invisible on screen and is now both.

`CHARACTER_VALID_DAYS = 365` and `TODAY_VALID_HOURS = 12` replace the single
`REVIEW_VALID_DAYS = 120`. Two clocks for two kinds of claim is the first place
the split pays for itself.

### 6. The stations, resolved by joining

The four `rescue_station` features were **not** orphaned, which the audit got
slightly wrong: `tools/build_site.py` reads them for the text alternative on
`/playa-organizada`. Dropping them silently changed that page to "0 estaciones",
which is why they are joined rather than deleted.

The **geojson geometry is authoritative**. `POSTS` keeps the name, hours and
equipment copy no machine reading a graphic can produce, plus a fallback `ll` so
stations still draw with no signal and before the fetch resolves. On load the map
joins on id, moves each marker onto the real position, and logs a console warning
if the fallback has drifted more than a metre or if either side has a record the
other lacks. Moving a station in the geojson now changes the map.

Every station sheet carries `stationScope`: these are the four inside the surveyed
window, Caribbean Guard's own press says nine along the coast, do not count on
these being all of them. The four-versus-nine question itself is untouched.

### 7. Register unified on tú

Applied from the table in `docs/precedents/03-voice-and-ia.md` section 3, plus the
Cocles hazard line it flagged separately ("si te arrastra la corriente: no luches,
nada paralelo a la playa"). Verified: no `Usted`, `Active la`, `Pregunte` or
`Guarde` remains in `T.es`.

### 8. Leaflet vendored, overview re-exported

`web/vendor/leaflet.{js,css}`, 1.9.4, no CDN and no fallback. If the local copy
ships anyway, shipping only the local copy removes the origin, the DNS lookup, the
TLS handshake, the integrity question and the fallback code in one edit. Leaflet's
CSS references three images, all for the layers control and the default marker
icon; the map adds neither, so those requests never fire and nothing was vendored
for them.

`base-lo.webp` was 88,718 B at 1200x402, not the 63 KB the 2026-07-30 handoff
claimed. Re-exported by the new `tools/export_overview.py` at the already specced
1000x335 q70: **35,932 B**, alpha preserved, corners still transparent.

### 9. Manifest, service worker, Add to Home Screen

`web/manifest.json`, `web/sw.js`, `web/icons/*` (placeholders, `tools/make_icons.py`,
plain navy tiles for Caribbean Guard to replace).

**The precache list is not an `addAll`.** MDN: if the promise rejects,
installation fails and the worker does nothing, so one 404 silently disables
offline entirely. It is `Promise.allSettled` over individual `cache.put()` calls,
each fetched with `cache:"reload"`, tiered into CRITICAL and OPTIONAL so
`base.webp` at 2.52 MB failing cannot take down a working overview-resolution map.
Failures are logged and named.

**The timestamp is only written when the whole critical set landed.** Stamping a
partial precache would put a fresh date on a cache missing pieces.

**HTML is network first with a 4 s timeout, everything else cache first.** The
document carries the verdicts, so somebody with signal gets today's copy.

**Update path**: Surfrider's pattern. `updatefound` to `installed` while a
controller exists reveals an in-page banner; tapping it posts `SKIP_WAITING` and
`controllerchange` reloads. Also re-checks on `visibilitychange`, which on a phone
is the moment somebody has walked down to the beach and reopened it.

**Honest copy**, Material Money's triple in one permanent strip above the picker:
a labelled timestamp ("Guardado en este teléfono · 6 ago, 12:24"), the refresh
cadence, and a manual refresh button. Beachsafe's "Never" default is copied: a
cache that has never populated says so. Tapping it opens a sheet that states iOS
may clear the copy after about a week of Safari use without a visit and that the
home screen prevents that, then offers the install prompt on Chromium, the Share
sheet instructions on iOS, or nothing if already installed.
`navigator.storage.persist()` is called after registration.

`say(T[lang].save)` fired unconditionally on every load, telling every visitor to
do something the page could not do. It is replaced by an install nudge that fires
once, only when installing is possible and the page is not already installed, and
is remembered in `localStorage`.

### 10. The map now refits when the viewport changes, and there is a test for it

Found by the team lead after the rest had landed. **The map did not refit on
resize or rotation.** Measured before the fix: resizing 1201x801 to 502x845
without reloading left the base image 1052 px wide inside a 502 px viewport, and
several resizes compounding walked it to `[29, 1350, 442, 148]`, entirely below
the fold with only the blurred backdrop showing. On a 3:1 coast, rotating the
phone to see more of it is the single most natural gesture there is, and it
produced something indistinguishable from a broken page.

There *was* a `resize` handler calling `fitCoast()`. Two things inside it were
wrong, and both only appear when the viewport changes:

1. **No `invalidateSize()`.** Leaflet caches the container size in `map._size`
   and only recomputes it there. So `getBoundsZoom()`, `fitBounds()` and
   `sizeBackdrop()` were all computing against the viewport as it was at load.
   That is the 1052-in-502 result exactly.
2. **`maxBounds` was stale during the fit.** The pan limit is derived from the
   backdrop, which is itself sized for whichever viewport was current when it was
   last computed. Leaving the old limit in force meant `fitBounds` was dragged
   back toward the previous viewport's centre, and since each fit then started
   from an already displaced centre, **the error compounded**. That is the
   `y: 1350` row. `map.setMaxBounds(null)` before fitting, rebuilt after.

Also listening to `orientationchange` and `visualViewport.resize` as well as
`resize`. iOS Safari reports the old `innerHeight` for a frame or two after
`orientationchange`, so that path fires a second trailing refit at 500 ms. The
fit is `animate:false`, because a layout correction is not a journey and an
animated refit during a rotation is a camera moving under somebody's thumb.

**Rotation is deliberately not debounced.** A drag-resize fires continuously and
its intermediate sizes are meaningless, so it waits 150 ms. A rotation is one
discrete event whose intermediate size is the *old* one. Measured at a 150 ms
debounce, 120 ms after rotating to landscape the strip was still 442 px wide in
an 846 px viewport and only reached its correct 744 px by 300 ms. Nobody rotates
this map to recentre it, they rotate it to get more coast, so the thing they
asked for must not be the thing that lags. A rotation now refits on the next
tick, measured at 744 px by 44 ms, and a `rotateUntil` window makes sure the
`resize` that accompanies a rotation cannot reintroduce the delay.

**A fourth, and it is the one that matters most, because it was a regression
introduced by the fix above and my 114 green assertions did not catch it.**

`getBoundsZoom()` subtracts the padding from the map size. Hand it a padding
**larger than the map** and the scale it computes is garbage, which Leaflet
clamps to `maxZoom`. That garbage then became the zoom floor via `setMinZoom()`,
and every branch landed on it. Measured: a 400x200 viewport, where the topbar and
dock total 216 px, drew the 744 px coast at **28,299 px wide**, a 38x overzoom
that is stable rather than transient because the floor has latched.

Two ways to reach it. A genuinely short landscape window, and, far more
importantly, **the middle of a phone rotation**: the viewport passes through very
short intermediate shapes, and removing the rotation debounce meant the refit
now fires straight into one.

Fixed by `fitPadding()`, which caps total padding at 60 percent of each axis and
splits the remainder in the ratio the real chrome asked for, plus an `isFinite`
guard so a bad floor can never be stored. The clamp only engages below about
360 px of height, where it lets the dock overlap the map slightly, which is
strictly better than the map being unreadable. Same 400x200 viewport now draws
221 px at z11.

**Why 114 assertions missed it.** Every geometry check was satisfied by an image
38x too large exactly as readily as by a correct one: a 28,299 px image starting
at x=-17558 does intersect the viewport, does have its centre on screen, and does
match its own projection. The check that cannot be fooled is comparing against a
**fresh load at the same viewport**, because the browser computes the right
answer independently and there is exactly one of it. That is `verify6`, and it is
now the primary assertion for this feature.

**And a third failure mode, found by the test written for the second one.**
`maxBounds` is the backdrop rather than the image, deliberately, so `flyClear`
can push the centre off the image to clear the bottom sheet. The backdrop is
sized for the viewport at the *zoom floor*, so it is enormous geographically, and
a centre that is a harmless few pixels off the image at the floor is thousands of
pixels off it at z16. Rotating from that state put the coast 2,900 px above the
viewport: measured, box `[-235, -2925, 742, -2257]` in an 845x502 window. So
keeping the view is now conditional on the view still containing some coast:
`if(map.getBounds().intersects(BB)) return;` falls back to the full fit
otherwise. That makes "the map is gone" structurally unreachable from any
viewport change, rather than fixed one cause at a time.

**A second defect, which my own new test found while proving the first was
fixed.** The refit reset the camera to the whole coast unconditionally, so
somebody who had zoomed into Cocles and rotated the phone lost the beach they had
navigated to. This was pre-existing and merely invisible while the refit did not
work at all. `fitCoast({keepView:true})` now always recomputes the floor, the
backdrop and the pan limit, which have to track the viewport, but only resets the
camera when it was sitting at the floor anyway. The preserved zoom is raised to
the new floor with `Math.max` when rotation raises it, portrait 12 to landscape
12.75 here, or the map would sit below its own minimum.

**The assertion that was missing, and it is the real lesson.** The old suite
asserted the base overlays existed in the DOM and passed happily while the map
was 1350 px below the fold. "It renders" is not the same claim as "it is where
somebody can see it". The new `verify4` probe reads the real base layer's
`getBoundingClientRect()`, excludes the deliberately unreadable backdrop, and
asserts against the projection rather than a remembered number: the rect
intersects the viewport, its centre is on screen, it fits the viewport width, its
drawn width is within 2 px of `latLngToContainerPoint` for `IMG_BOUNDS`, and the
map sits at its floor. Run at portrait, at desktop, across a resize with no
reload, across a rotation each way, and after six compounding resizes.

**Three things in that suite are worth reading before editing it**, because each
one is a mistake this work made and then had to unmake.

1. **No coordinate is pinned.** Rotating changes the viewport aspect, the
   backdrop and therefore `maxBounds` are resized from it, and Leaflet clamps the
   centre so the whole viewport stays inside the limit. Both latitude and
   longitude legitimately move. The first draft asserted latitude, then
   longitude, and both were wrong for the same reason. The suite now asserts the
   user-facing property, that the beach is still on screen at the zoom the user
   chose, by projecting the zone's own polyline into container space.
2. **The zoomed-in case zooms onto the beach, not about the current centre.** A
   plain `setZoom(16)` inherits `flyClear`'s off-image centre and puts the coast
   off screen *before* the rotation happens, so there is nothing legitimate left
   to preserve and the assertion tests nothing. It now does
   `setView(zoneCentre, 16)` and asserts the beach is visible before rotating as
   an explicit precondition.
3. **`verify5` dispatches no synthetic events at all.** `verify4` fires
   `new Event("resize")` by hand, which proves the handler is correct but not
   that a real rotation reaches it. `verify5` drives `screenOrientation` through
   CDP and relies entirely on what the browser emits by itself, counting the
   events the page received so a viewport change that fires nothing is
   distinguishable from a handler that ran and got it wrong.

`verify2` needed the same treatment for a different reason: in-page
`unregister()` plus a reload leaves the origin with an active worker and a
waiting one and the page controlled by neither, in which state the update banner
*correctly* refuses to appear. That produced three false failures before it was
diagnosed. It now clears the origin with `Storage.clearDataForOrigin` and polls
for a controller as an explicit, reported precondition.

---

## Why

The governing rule is that nothing may claim more currency or authority than the
data has. Four of the nine changes above are that rule applied somewhere it was
not being applied: to the capability claim in "Guarde esta página", to the word
`safe` at the lowest tier, to an absence rendered as nothing, and to a saved-copy
timestamp that would have moved forward on a refresh that fetched no bytes.

The schema items had a deadline, which is why they came first. They are all cheap
today and all expensive the moment a guard reviews and dates a single verdict,
because at that point migrating means rewriting a provenance record, and a
provenance record's whole value is being an unaltered timestamped statement of who
said what.

---

## Verify

Headless Chrome 150 over CDP against `web/` served by
`python -m http.server 5199`, which is the production shape: no vite client, no
site wrapper, worker at scope `/`. **164 assertions across six suites, all
passing.**

| suite | assertions | covers |
|---|---|---|
| `verify` | 33 | renders, schema, the three absence states, level-name rules, deference, deep links, precache |
| `verify2` | 18 | genuinely offline, failed refresh, update banner end to end |
| `verify3` | 14 | the `today` axis, exercised by injecting records at runtime |
| `verify4` | 41 | viewport geometry across resize, rotation and compounding |
| `verify5` | 8 | rotation with **no synthetic events**, sampled over time |
| `verify6` | 50 | **rotation equals a fresh load**, 8 viewports plus compounding |

**`verify6` is the one to trust.** It compares every rotated result against a
fresh load at the same viewport, which is the only form of this check that cannot
be satisfied by a wrong answer. It runs the real device shapes plus two
deliberately degenerate ones, and it passes identically against the vite dev
server at `site/mapa/app/` and the static server at `web/`:

| viewport | fresh | rotated |
|---|---|---|
| 844x390 iPhone 14 landscape | 442 | 442 |
| 812x375 iPhone X landscape | 442 | 442 |
| 736x414 iPhone Plus landscape | 525 | 525 |
| 640x360 small Android landscape | 372 | 372 |
| 568x320 iPhone SE landscape | 372 | 372 |
| 1024x600 small tablet | 885 | 885 |
| 500x250 degenerate short | 263 | 263 |
| 400x200 padding exceeds viewport | 221 | 221 |

Seven compounding rotations and resizes then land on 442 px at z12, identical to
a fresh load at that viewport.

**Viewport geometry, base layer rect as `[x, y, w, h]` against the projected
width, after the fix:**

| case | viewport | rect | projected w | at floor |
|---|---|---|---|---|
| fresh load, portrait | 502x845 | `[30, 309, 442, 148]` | 442 | z12 = min12 |
| fresh load, desktop | 1201x801 | `[74, 185, 1052, 352]` | 1052 | z13.25 = min13.25 |
| desktop to portrait, no reload | 502x845 | `[30, 309, 442, 148]` | 442 | z12 = min12 |
| rotated to landscape | 845x502 | `[51, 86, 744, 249]` | 744 | z12.75 = min12.75 |
| rotated back to portrait | 502x845 | `[30, 309, 442, 148]` | 442 | z12 = min12 |
| after six compounding resizes | 502x845 | `[30, 309, 442, 148]` | 442 | z12 = min12 |

The last row is the one that mattered: it was `[29, 1350, 442, 148]`, and it is
now byte identical to a fresh load, so the fit is idempotent under repeated
viewport changes rather than merely better. Landscape reaches 744 px of projected
width against portrait's 442, which is the point of rotating a 3:1 coast in the
first place.

**Rotation timing, driven by `screenOrientation` with no synthetic events**,
portrait 502x845 to landscape 846x503, base width sampled:

| | before | after |
|---|---|---|
| t = 44 ms | 442 | **744** |
| t = 120 ms | 442 | 744 |
| t = 300 ms | 744 | 744 |

Both the freshly-loaded landscape and the rotated-into landscape measure 744 px,
so a rotation now lands on exactly what a fresh load would have produced. The
browser fires `resize` and `orientationchange` by itself; nothing in the page
depends on a test dispatching them.

- Renders: two image overlays, 38 paths, four station markers, no console errors.
- Zoom floor: `getZoom() === getMinZoom() === 11.75` on load, and after both deep
  links. The floor is derived from `getBoundsZoom`, not from `getZoom()` after an
  animating `fitBounds`, which is the bug fixed previously and still holds.
- Deep links: `?z=cocles` opens Playa Cocles, `?p=est2` opens Rescue station
  Playa Chiquita 2, both respecting the floor.
- Absences: chips render on every card; `never` and `unsurveyed` both present;
  `surveyRelation` returns `out` for four zones and `partial` for Chiquita;
  the sheet renders two `.gaplist` items; the void card is in the picker.
- Two axes: `.today.none` and `.status.low` both present; no `SE PUEDE NADAR` or
  `SWIMMING OK` in any rendered element; the NOAA rider present; the Punta Uva
  channel text is inside a `.caveat`, not a `facts` bullet; two `.prov .row`.
- Level names, asserted against all three rules: no label matches a risk rating
  (`RIESGO ALTO`, `HIGH RISK`, `LOWER RISK` and friends all fail the suite now);
  no label grants permission; every label in both languages contains an
  actionable verb. A `.defer` block is present on all five zones **and** on the
  unmapped-coast sheet, and the deference string is asserted to be conditional.
- `today` exercised by injecting a record at runtime: a signed bulletin renders in
  its own block with person and organisation, the character survives beside it,
  the card gains a today mark without losing the character label, a bulletin older
  than 12 h says so and is marked stale, `normal` draws no halo and states it is
  not safe, `no-swim` returns the halo colour.
- **Offline, with the network cut on the service worker target as well as the
  page**: document renders, Leaflet runs, the overview paints at
  `naturalWidth=1000`, six cards, chips still render, nine rips still drawn from
  cache, a verdict sheet opens with its provenance, and the bar names a date.
  A manual refresh with no network says "No signal. You are still seeing the saved
  copy." and **does not move the timestamp**.
- Update banner: absent on a clean load; appears after a new build installs;
  `SKIP_WAITING` reloads onto the new worker; banner gone afterwards.
- `python tools/build_site.py` runs clean, 14 pages, `/playa-organizada` still
  reads "9 corrientes, 4 estaciones", and `site/mapa/app/index.html` is byte
  identical to `web/index.html`. That page's text alternative is why the station
  features were joined rather than dropped.

  One `NameError: n_rips` was seen mid-session and reported; it was this file
  being edited concurrently, not a defect, and it is resolved.

### The measured critical path

| Asset | On disk | On the wire |
|---|---|---|
| `web/index.html` | 117,848 | 41,280 gz |
| `web/vendor/leaflet.js` | 147,552 | 42,356 gz |
| `web/vendor/leaflet.css` | 14,806 | 3,534 gz |
| `web/img/base-lo.webp` | 35,932 | 35,932 |
| `web/data/cg-hazards.geojson` | 9,885 | 1,549 gz |
| `web/manifest.json` | 690 | 333 gz |
| `web/icons/icon-192.png` | 3,604 | 3,604 |
| **Total** | | **128,588 B = 126 KB, 7 requests, one origin** |

Plus `sw.js` at 3,401 gz, not render blocking, and `base.webp` at 2.52 MB still
deferred to the first zoom or pan.

Before this work, measured the same way: **157,076 B = 153 KB, 5 requests, two
origins.** Net 29 KB lighter and one origin gone, despite `index.html` growing
again.

**`index.html` now costs 41,280 gz, of which roughly 18 KB is inline design commentary.**
That is 14 percent of the whole critical path spent on prose no user reads.
Stripping comments at deploy would recover it and would cost the file its
convention that the reasoning lives beside the code, with no build step. Left as
a decision rather than taken unilaterally.

---

## Left

**For Caribbean Guard.**

1. **Is there a working red flag system on this coast?** The Cocles copy asserts
   "Banderas rojas marcan los canales activos" and it is unverified. If it is real
   and maintained, the RNLI model is available and it removes the review cadence
   dependency the whole project rests on. If it is not, the map is carrying more
   weight than anyone has acknowledged.
2. **Four stations or nine?** Untouched, as instructed. The station layer now says
   out loud that its four are the ones inside the surveyed window.
3. **What is the actual patrol shift?** `TODAY_VALID_HOURS = 12` is a placeholder.
   It should be however long a signed bulletin is good for, and nobody has said.
4. **The third disclaimer sentence.** SLSA gives the user a rule that works when
   the map is wrong. The equivalent for this coast is theirs to write.
5. **What is the shaded polygon?** Still rendered grey and unlabelled.
6. **Replace the icons.** `web/icons/*` are plain navy CG tiles, deliberately not
   an invented logo.

**For us.**

7. Nothing has ever been reviewed, so `expired` renders correctly by construction
   but has never been seen with real data. Same for `authoredField`.
8. **Green is the last thing in the vocabulary that reads as permission.** The
   lowest tier now says `TEN CUIDADO IGUAL` under a green pill and a green dotted
   stroke. The words grant nothing and the rider is explicit, so the colour is the
   only remaining channel saying "go", and it says it to somebody glancing at the
   picker without reading. Not changed here because the three tier colours are
   separated by *brightness* rather than hue, deliberately, so the map survives a
   sun-washed screen, and swapping green out breaks a ladder that was measured.
   Worth a deliberate decision rather than a drive-by: the honest options are a
   desaturated blue-grey at the same luminance, or keeping green and accepting
   that the pattern plus the words carry it.
9. Open Graph tags on the deep links, audit item 12, not done. Out of scope here.
10. A stale `CACHE` version string is survivable, because install always re-fetches
    with `cache:"reload"`, but the browser only notices a new worker when `sw.js`
    itself changes. Adding a build stamp to `sw.js` at deploy would close that.

---

## Files

**Changed**
- `web/index.html` two axis schema, four character classes, absence states, void
  card, station join, tú register, NOAA copy, vendored Leaflet, saved-copy bar,
  update banner, install prompt, service worker registration
- `web/data/cg-hazards.geojson` stable ids, `authored` and `reviewed` replacing
  `needs_confirmation`, `station_layer` note naming the authoritative source
- `tools/extract_annotations.py` `feature_id()`, positional station ids,
  station count notice, provenance fields
- `docs/handoffs/2026-07-30-site-rebuild-and-map-polish.md` corrected the 63 KB
  overview figure in both places
- `docs/site-revamp/04-map-integration.md` corrected the 86 KB critical path, the
  geojson feature counts, and restated the iOS eviction note so the fix is visible

**New**
- `web/sw.js`, `web/manifest.json`, `web/icons/icon-{180,192,512}.png`,
  `web/icons/icon-maskable-512.png`
- `web/vendor/leaflet.js`, `web/vendor/leaflet.css` (1.9.4)
- `tools/export_overview.py`, `tools/make_icons.py`

**Not touched**, as instructed: `tools/build_site.py`, everything under `site/`
except by running the build. The rip direction logic, drawn along the local
seaward normal of the traced coastline, is untouched. `IMG_BOUNDS` was not
generalised and nothing multi-region was built.
