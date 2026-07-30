# Caribbean Guard: site revamp, synthesis

2026-07-30. Pulls together five specialist passes over caribbeanguard.org and the
draft safety map. Each section links to the detailed report behind it.

This is the document to read. The others are the evidence.

---

## The one-paragraph version

Caribbean Guard has better material than its website admits. Named staff with real
certifications, a founding claim that nobody has died on their watch since 2021,
a named partnership model with dated installs, and a hand-authored hazard map with
rip currents and rescue stations already drawn on it. Almost none of that reaches
a visitor. The credentials are inside a collapsed accordion, the hazard map is
published with `alt=""` so neither Google nor a screen reader knows it exists, the
site has no contact mechanism of any kind, and it is written only in the language
that the people most likely to drown do not read. The revamp is mostly an exercise
in surfacing what is already there.

---

## The six things to fix first

Ranked by consequence, not by effort. Effort is noted so the cheap ones are obvious.

### 1. There is no way to contact this organization. Anywhere.

Zero `<form>` elements site-wide. Zero `<input>`. No `mailto:`. No `tel:`. No
WhatsApp link. `/involcrate`, the page whose entire job is recruiting volunteers,
offers no mechanism to make contact, and the footer link labelled "Únete" that a
would-be volunteer would click **404s**.

The one email address on the site is plain unlinked text on the donate page. The
one phone number is plain unlinked text, and see finding 2.

**Effort: hours.** Add a Squarespace form block, make the email a `mailto:`, make
the phone a `tel:`, and 301 `/unete` to `/involcrate`.

### 2. The emergency number and the donation number are the same number, labelled differently on two pages

`/involcrate` presents `+506 8339 6566` as the contact route. `/donar` presents
the same digits as the SINPE Móvil donation line. Whatever the truth is, the site
currently says both, and one of those two claims is wrong.

This one needs AJ before anything is changed. It is listed first among the
questions at the end.

**Effort: one conversation, then minutes.**

### 3. The organization's two hazard maps are invisible

`Annotated Base Map V5.png` and `Dangerous Area V4.png` on
`/programa-playa-organizada` are the most valuable safety content the organization
has published. Both carry `alt=""`.

The cause is a real Squarespace bug rather than an oversight: the carousel block
emits **two** `alt` attributes on the same `<img>`, and the empty one comes first,
so browsers take it and silently discard the real one. The image block on other
pages has the same bug with the order reversed, which is why `/involcrate` shows
the opposite failure, six images whose accessible name is a camera-roll filename
like `IMG_20210505_092112.jpg`.

`Annotated Base Map V5.png` is also **uploaded twice** as two separate assets
(`f15318a5…` and `17bff6c7…`), one a carousel copy with `alt=""` first and one a
Fluid Engine image block with no alt at all. So it is 1,482 KB served and stored
twice, and neither copy is reachable by a screen reader or a search engine.

A drowning-prevention charity's hazard diagram currently conveys nothing to a
blind user, nothing to a search engine, and nothing to anyone whose images fail to
load. It also means the annotations exist only as pixels: there is no text
anywhere on the page saying where the rip currents are.

**Effort: minutes per image**, and it is the highest value per minute on this list.

### 4. `lang="es-AR"` on a Costa Rican site, and no English at all

Every page declares Argentine Spanish. Squarespace is simultaneously serving
`es-419` (Latin American Spanish) assets, 67 references per page, so the site
disagrees with itself. A screen reader gets Rioplatense pronunciation for Costa
Rican content.

Separately and more importantly, `languagePicker` is explicitly `"enabled": false`
with no language flags. Bilingual support is not half-built, it is absent. The
organization's own founding logic is that tourists drown and tourists read
English, and the four English nav labels that do exist ("Lifesaving Club", "Swim
Club", "Freediving Club", "Team") are announced to Spanish screen reader users as
Spanish phonetics.

**Recommendation: selective bilingual, not full.** Home hero, one trust block, and
one new English trip-planning page. Full site-wide bilingual is not maintainable
for an organization whose only contact is a single Gmail address. This matches
what the map draft already does: auto-detect with a Spanish fallback.

**Effort: `lang` fix is one setting. Selective bilingual is a real content project.**

### 5. The homepage downloads a 52 MB video nobody pressed play on

Measured on an emulated iPhone 12, three runs, no clicks and no scrolling. The
homepage carries a Squarespace video block, 6 minutes 52 seconds, 1920x1080, and
the player buffers it eagerly through a MediaSource blob while the `<video>`
element itself stays paused. Queried after 15 seconds in view:
`{paused: true, autoplay: false, currentTime: 0, duration: 412.4}`. It is not
playing. It is buffering to the limit of whatever bandwidth exists.

| Connection | Bytes at `load` | Bytes after 60 s sitting still | of which video |
|---|---|---|---|
| Wifi | 1.94 MB | **52.09 MB** | 50.13 MB |
| Fast 3G | 6.17 MB | 14.43 MB | 12.47 MB |
| Slow 3G | 6.15 MB | 6.15 MB | 4.21 MB |

**96% of a 52 MB homepage visit is a video nobody asked for.** On a prepaid Costa
Rican SIM that is real money out of a tourist's data bundle. Slow 3G reaches
`load` at 59 seconds, first contentful paint at 11.2 s.

This dwarfs every image problem on the site combined. Full detail in
[03-image-register.md](03-image-register.md).

### 6. Five pages ship the unedited Squarespace placeholder title

`/proyectos`, `/programa-playa-organizada`, `/freediving-club`, `/lifesaving-club`
and `/swim-club` all have the literal `<title>Services 4 — Caribbean Guard</title>`.
`/nuestro-trabajo` has `Services — Caribbean Guard`.

That string is what appears in a browser tab, a bookmark, a shared link preview,
a Google result, and a screen reader's page announcement.

**Effort: five minutes total.** The single cheapest credibility win available.

---

## Navigation: nine tabs to seven

Full reasoning and click-path traces in
[01-information-architecture.md](01-information-architecture.md).

| | Nav label | URL | Change |
|---|---|---|---|
| — | Inicio | `/` | unchanged |
| 1 | **Mapa de Seguridad** | new, standalone | nothing but the live map: a minimal page whose only job is to load fast and show status |
| 2 | Programa Playa Organizada | `/programa-playa-organizada` | unchanged in scope; duplicate PNG removed, link card to the live map added at the top |
| 3 | Lifesaving Club | `/lifesaving-club` | unchanged |
| 4 | Swim Club | `/swim-club` | unchanged |
| 5 | Freediving Club | `/freediving-club` | unchanged |
| 6 | **Nosotros** | `/nosotros` | currently a 404; becomes a hub over Historia, Visión, Equipo, Proyectos |
| 7 | Involúcrate | `/involcrate` | unchanged; contact moves to the site-wide footer |
| CTA | Donar ahora | `/donar` | unchanged |

**This changed once, and the reason is worth keeping.** The first version folded the
map into `/programa-playa-organizada` and relabelled that page, on the reasoning
that the map is a digital extension of the programme it documents. The performance
measurements killed it: that page is the heaviest on the site at 2.9 MB and 67.3
seconds on Slow 3G, and the "map" already on it is a static PNG, uploaded twice,
illegible on a phone. Putting a two-second artifact behind a 67-second page throws
away the entire point of building it. The map gets its own slot, first in the bar.

Still seven items, down from nine: four fold into Nosotros, Nosotros adds one, the
map adds one.

Two properties worth noting. **No existing URL changes**, so anything already
printed keeps working, and the only redirect needed is one line, `/unete` to
`/involcrate`. And `/nosotros` stops being a dead link not by redirecting it but by
finally building the page the footer has been promising.

What is lost: Visión, Equipo, Historia and Proyectos go from one tap to two.
Proyectos is the arguable one, since a donor may want it fast. If AJ disagrees,
pull that single page back out and leave the rest grouped.

The three clubs deliberately stay flat. They are where two of the four personas
already get a one-click answer today, and folding them costs a tap on
Squarespace's mobile nav for no gain.

---

## Visual system

Full palette, type scale and 390 px numbers in
[02-visual-system.md](02-visual-system.md).

**The site has no colour system in practice.** Every page's header config
specifies only `white` and `black`, ten times per page. Squarespace's own theme
defines an accent, roughly `#1570AF`, that nothing on the site ever calls. That
lands within a few points of the blue the map had already picked independently
for its locate control, `#1565C0`. Both surfaces were circling the same colour
without knowing it, so canonize it.

**One font, Poppins**, in four weights, and it is loading a full Devanagari subset
this Spanish site will never render.

**The home hero is `min-height: 10vh`.** About 84 px on a phone, barely taller
than the header, with no room for a headline. Set deliberately
(`customSectionHeight: 10`), which means someone chose it while looking at a
desktop preview. It is the clearest single piece of evidence that this site was
built desktop-first.

**Smallest type on the site is 8px** (`0.5rem` button labels on `/proyectos` and
`/lifesaving-club`). Staff biography body copy is 14.4px.

**Social links are 20×20px hit areas** with `margin: 0` and a 12px gap, against a
44×44 target. The inner glyph is scaled 2× so they *look* about 40px. Users will
aim at the glyph and miss.

Good news worth stating: the viewport meta is clean on all thirteen pages, no
`maximum-scale`, no `user-scalable=no`, so pinch zoom is not blocked. The carousel
arrows are properly labelled, the `/team` accordion is a correct ARIA pattern, and
there is a working skip link on every page.

---

## The safety status colour problem

This is the one place where two specialists disagreed with each other and with me,
and the disagreement is worth preserving because the conclusion is not obvious.

Red, amber, green is the natural language for swim status. It fails three ways at
once here: for the roughly one in twelve men who cannot separate red from green,
in direct sun, and on a dimmed screen.

The measured problem in the shipped draft: `--safe #1f9d55` and `--caution #c77700`
had relative luminance **0.251 and 0.254**, a ratio of 1.01:1. Identical
brightness. Hue told them apart, and hue is exactly the channel glare destroys
first. Both also failed WCAG AA outright as white-on-fill: **3.49:1 and 3.46:1**
against a 4.5:1 requirement, and 13px bold does not qualify for the large-text
exception.

I fixed the contrast by moving caution to `#9C5C00`. The accessibility pass then
caught that this **creates a new collision**: `#9C5C00` at luminance 0.147 sits
1.06:1 from `--danger #c62828` at 0.137. The safe/caution collision was traded for
a caution/danger collision, and confusing caution with danger is the more
expensive pair.

That is a genuine trap, and it is structural: any all-dark-on-white palette hits
it, because the AA floor pushes every token into the same narrow luminance band.

**The resolution now in the map** is two tiers that diverge on purpose:

| | Text and dots on white, needs 4.5:1 | Lines on the map, needs 3:1 vs imagery |
|---|---|---|
| safe | `#178049` (4.98:1) | `#1F9D55` (L 0.251) |
| caution | `#9C5C00` (5.32:1) | `#F5B942` (L 0.545) |
| danger | `#C62828` (5.62:1) | `#C62828` (L 0.137) |

On the map the three now separate by brightness alone: caution is the brightest,
safe sits in the middle, danger is darkest, with 3.19:1 between the extremes. All
three text values clear AA. Colour is still only ever a reinforcement: the text
label and the line pattern each carry the full signal independently.

**Still outstanding, and the sharpest observation anyone made today:** the line
patterns are backwards. Dotted means danger and solid means safe, so the lightest
mark on the map is the most dangerous thing on it. Every convention a tourist
carries, road markings, hazard tape, warning signage, says the loud mark is the
dangerous one. The map currently shouts safety and whispers danger. And the legend
strings that would teach the vocabulary (`legendSafe`, `legendCaution`,
`legendDanger`) are defined in the translation table and **never referenced
anywhere in the file**, so the pattern language is undocumented in the interface.

---

## The map: three things that block publishing it

From [06-accessibility-and-safety.md](06-accessibility-and-safety.md). These are
about the draft I built, and I agree with all three.

**1. It can silently show the wrong verdict.** The locate handler auto-opens a
full-screen verdict for whichever zone has the nearest vertex within 450 m. The
Cocles zone ends 419 m from where the Chiquita zone begins. That is *inside* the
trigger radius, so there is a stretch of coast where both qualify and the winner
is decided by a few metres of vertex geometry, on top of a GPS fix and a
georeference good to 75 m at best. The user is shown a verdict, not asked to
confirm, and nothing signals that it was guessed.

**2. Every verdict is unattributed placeholder prose.** "NO NADAR", "la zona más
segura para familias y niños", "Guardavidas de 9:00 a 17:00". All written from
general knowledge. No author field, no assessment date, no review date, no UI
anywhere that says who decided. A public map that says DO NOT SWIM must be able to
say who said so and when.

**3. It is one CDN request from a blank screen, and it lies about working
offline.** Leaflet loads from unpkg with no SRI, no fallback and no self-hosted
copy. If that request fails on beach signal, the inline script throws and the page
renders as a dark blue void with a brand label and a 911 button: no beach names,
no statuses, no explanation. Meanwhile the page opens with a toast telling the
user to save the page because signal is weak, and there is no service worker, no
manifest, and no cache behind that instruction.

Plus a substantial accessibility list: the toast has no `aria-live` even though it
carries all the safety messaging; the bottom sheet sits in the accessibility tree
permanently as an empty dialog; opening it announces nothing and never moves
focus; Escape does not close it; the four observation post markers are focusable
buttons whose entire accessible name is a single digit; several `aria-label`s are
hardcoded Spanish that never update on language switch; there is no `h1` and no
landmarks; and the drag handle on the sheet is drawn but has no drag handlers, so
the affordance is a lie.

---

## What changed today, before this synthesis

- **The base imagery is georeferenced and verified.** 16.66 km, 109.4 cm per
  source pixel, +3.368° off north. Measured accuracy 5 to 75 m from Puerto Viejo
  to Punta Uva across 8 confirmed points; not confirmable east of Punta Uva, best
  estimate 150 m.
- **The east third cannot be verified because the generative upscale replaced the
  water and reef with invented texture.** That is a content problem as much as a
  matching one: reef-protected versus open water is the whole safety story at
  Manzanillo, and the imagery no longer contains it.
- **The base is rectified north-up** into Web Mercator so Leaflet's bounds are
  exact, and re-encoded as WebP with alpha at 1.19 MB.
- **Caribbean Guard's own hazard annotations are now data.** Their published sheet
  georeferenced against Bing at **294 inliers, 1.2 m residual**, and its graphics
  extracted to `web/data/cg-hazards.geojson`: 11 rip currents, 4 rescue stations,
  and one shaded polygon left deliberately unlabelled because it is not in the
  legend and could be either a hazard zone or a designated safe swimming zone.
  Covers 1.82 km, about 11% of the coast.

The contrast between 5 inliers on the upscaled base and 294 on the untouched sheet
is the clearest evidence yet for the rule: generative upscaling destroys the
correspondence that georeferencing depends on.

---

## The rule that governs all copy about the map

Recording this because it nearly went wrong in a first draft of the link-card copy,
and it will keep trying to go wrong.

Proposed copy described the map as showing conditions **"en tiempo real"** and
**"marcado por nuestros guardavidas"**. Both read naturally and both are false.

There is no live status mechanism. Statuses are static values in a file, nothing
polls anything, nothing expires, and there is no channel by which a guard on the
beach changes what the map says. And no zone status has been authored by Caribbean
Guard: the prose is placeholder, and the extracted rip currents carry
`needs_confirmation: true` on every feature because nobody there has signed off on
them yet.

Telling a tourist the reading is real-time invites them to trust something that
could be six months old, which is worse than the static PNG it replaces, because
the PNG never claimed to be current. Attributing it to their lifeguards puts words
in the mouths of the people whose judgment the whole thing depends on.

**The rule: the interface may never claim more currency or more authority than the
data behind it actually has.** Concretely, for now and until the two open blockers
close:

- No "real-time", "live", "current conditions" or equivalent
- No attribution to Caribbean Guard's guards until they have signed off
- Every status carries a review date, and if nothing has been reviewed yet, it says so
- Stale defaults to unknown, never to safe

An organization that admits what it has not checked is more trustworthy than one
that implies it has checked everything. That is the difference between a
timestamped observation and an implied guarantee, and it is the whole liability
position in one sentence.

---

## How the map actually ships

From [04-map-integration.md](04-map-integration.md), all figures measured on an
emulated iPhone 12 with the same throttling harness applied to both the live site
and the map, so the comparison is like for like.

**Not an iframe. The numbers are not close.**

| | Transfer | Slow 3G to `load` |
|---|---|---|
| `caribbeanguard.org/` | 6.2 MB, growing to 14.4 MB | 59.2 s |
| `/programa-playa-organizada` | 3.1 MB | 67.3 s |
| Map draft as it stands | 1.24 MB | 30.6 s |
| **Map with Leaflet self-hosted and a small overview base** | **86 KB** | **7.8 s** |

That last row was built and measured, not projected. An iframe inherits the parent
page's 67 seconds before it is allowed to start, and the 913 KB of Squarespace
JavaScript on that page cannot be trimmed from inside Squarespace.

**So the map is a standalone page and the QR codes point straight at it.**

The cleanest way to hold the two paths in mind, and the rule that reconciles the
hosting plan with the navigation plan:

> **The embed is the browse path. The standalone is the emergency path.**

Someone reading the website from a sofa gets the map inside the site, in context,
next to the programme that produced it. Someone standing on wet sand who has just
scanned a QR code gets the standalone page and nothing else, because they are one
hop from what they scanned rather than two, and because they are not browsing.

That is why the map also takes its own top-level nav slot rather than living only
inside `/programa-playa-organizada`. And it degrades cleanly: if the Squarespace
plan turns out not to support Code Blocks, the tab still works, it just holds a
link card instead of an embed. Nothing about the emergency path depends on that
question being answered.

**Host on Cloudflare Pages, at `mapa.caribbeanguard.org`.** Both hosts are free
and both do custom subdomains with automatic HTTPS, so the decision is not
technical. It is about who updates this after Daniel hands it over. Cloudflare's
Direct Upload lets someone drag a folder into a dashboard. GitHub Pages needs a
git workflow that will decay the first time the person who knew it is unavailable.
GitHub Pages also requires a public repo on a free account.

**One blocker nobody had spotted: the DNS is not at Squarespace.** The nameservers
are `ns1/ns2/ns3.wordpress.com`. Adding `mapa.caribbeanguard.org` means getting
into a WordPress.com account nobody has mentioned, possibly a forgotten one from a
previous site. Worth finding out early because it blocks the subdomain and nothing
else. Fallback is the free `pages.dev` subdomain, which works fine and which the
QR codes do not care about.

**And in fact, no tile pyramid at all in the first release.** This is the second
recommendation that reversed under measurement, and it is the better outcome.

The plan had assumed roughly 1,300 tiles from the start, and that assumption was
never tested. It should have been. Load a 29 KB overview first and swap the full
1.19 MB base in after paint, and first-useful stays at **86 KB** while the whole
artifact still fits inside a service worker precache, which a 1,300-file pyramid
does not. That matters more than sharpness for something used on a beach.

The detail argument for the pyramid is also weaker than the arithmetic suggests.
The 5000 px base is 3.33 m per pixel, and the source went through a generative
upscale that destroyed fine texture, so z17's nominal 1.09 m per pixel is partly
synthetic. Paying 1,300 files for resolution that is not real is a bad trade.

So **stage one is one image, one GeoJSON, no tiler**, with the pyramid deferred and
built only if someone actually complains about sharpness standing on the sand.

If it is ever needed: no GDAL. The extent spans 0.050 degrees of latitude, so the
difference between treating the rectified image as flat and as Web Mercator is
**0.031 pixels** at worst, which makes the tiler about 40 lines of Pillow.

### A correction worth recording

The integration report initially read the georeference as accurate to 4.0 m and
concluded the earlier 50 m figure was out of date. That is backwards, and the
reason is the same trap that cost most of yesterday.

The 4.0 m figure is the RANSAC residual on the **14 inliers out of 109**. RANSAC
selects the subset that agrees with the model and then measures how well that
subset agrees with the model. It is circular. It cannot tell you the model is
right, only that 14 points were mutually consistent with it.

Ground accuracy comes from `tools/residual.py`, which matches 14 points along the
coast against Bing independently: **5 to 75 m in the west across 8 confirmed
points, not confirmable at all east of Punta Uva.** Those are the numbers the map
uses, and it combines them with GPS error in quadrature when drawing the location
circle rather than claiming a precision it does not have.

Internal consistency and ground accuracy are different claims. Do not let a tight
number from a self-selected subset carry the word "accuracy".

---

## Questions for AJ

Ordered by how much they block.

1. **Is `+506 8339 6566` the emergency number, the SINPE donation number, or
   both?** The site currently says both, on different pages.
2. **Is `Annotated Base Map V5` current, and does it cover more of the coast than
   the 1.82 km published?** The extraction gives 11 rip currents; are they still
   accurate, and who signs off on them?
3. **What is the shaded pink polygon at Playa Chiquita?** Hazard zone or safe
   swimming zone. It is not in the legend and the answer inverts the message.
4. **Who has the WordPress.com account that holds the DNS?** The nameservers for
   caribbeanguard.org are `ns*.wordpress.com`, not Squarespace. This blocks
   `mapa.caribbeanguard.org` and nothing else, but it is worth chasing early.
5. **Which Squarespace plan?** Code Blocks need Business or above. Less critical
   than it was, since the map now ships as a standalone page rather than an embed.
6. **Is the homepage video meant to be there?** It costs 50 MB per visit and
   nobody presses play.
7. **Who at Caribbean Guard will hold the Cloudflare login, and who is the second
   person who also holds it?** This is the whole handover. If updating the map
   requires Daniel, the map dies when Daniel stops answering emails. It also
   answers the related question of who owns hazard status and how often it is
   reviewed, since the map now needs an author and a date on every verdict and
   expires them after 120 days by itself.
8. **Is 3.33 m per pixel actually good enough standing on the beach?** Not
   answerable by measurement, and not from a desktop screen. Someone has to show a
   guard a phone on the sand. If the answer is no, the tile pyramid comes back.
9. Rescue count to date, and the source for the drowning statistics.
10. Are the two `/proyectos` items built or aspirational? The page states both in
   the same confident tense with no status marker, which an institutional funder
   will not tolerate.
11. Is "Nosotros" an acceptable label for the new hub?

---

## Reports behind this

| | Report | Owner |
|---|---|---|
| 01 | [Information architecture](01-information-architecture.md) | Lelouch |
| 02 | [Visual system](02-visual-system.md) | Sai |
| 03 | [Image register](03-image-register.md) | Edward |
| 04 | [Map integration](04-map-integration.md) | Edward |
| 05 | [Audience and behaviour](05-audience-and-behaviour.md) | Erwin |
| 06 | [Accessibility and safety](06-accessibility-and-safety.md) | Lelouch |
