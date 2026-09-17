# Safeswim teardown: the visual language we are adopting

Measured from https://safeswim.org.nz/locations/point-chevalier on 2026-09-17, by
reading computed styles out of the live DOM rather than by eye. Every number
below is what the browser actually resolved, not an estimate from a screenshot.

Daniel's instruction, 2026-09-17: *"adopt most of the visual language coming from
safeswim.org. Their entire dashboard and organization is ideal and what we should
strive for in content, legends, organization, component."*

This file is the reference. `docs/precedents.md` says WHY Safeswim is the
precedent; this says WHAT it is made of.

---

## 1. The one idea worth more than the rest

**Every section is the same three-part component, and it never varies:**

```
EYEBROW      10px / 700 / uppercase / +0.2px     the QUESTION this answers
verdict      20px / 700                          the ANSWER, in plain language
detail       14px / 400                          why, how, or what to do
link         14px / 400                          somewhere to learn more
```

Measured instances, in the order they appear in the panel:

| eyebrow | verdict |
|---|---|
| `CURRENT WATER QUALITY` | Good water quality |
| `SURF LIFE SAVING` | Beach not lifeguarded |
| `FORECAST` | Water and weather |
| `TIDE` | Currently outgoing |

That is the whole organisation. A reader learns the shape once and then reads
four sections without re-learning anything. Note what the verdict is NOT: it is
not a rating, not a number, not a colour-only signal. "Beach not lifeguarded" is
a sentence a person can act on, and it sits at 20/700 where nothing else on the
panel competes with it.

**The eyebrow is the part we were missing.** Caribbean Guard's sheet runs name,
instruction, why, escape, 911, trust — six things in six different shapes, and a
reader has to work out what each one is FOR. Safeswim labels the job of every
block before the block speaks.

## 2. Type scale, as resolved

Family is **National** (Klim Type Foundry, commercial licence). We cannot ship it
and we do not need to: it is a neutral grotesque and Inter already stands in for
it. What we take is the scale and the weight discipline, not the face.

| role | size / weight | notes |
|---|---|---|
| page hero | 68 / 700 | homepage only |
| page heading | 36 / 400 | note the light weight at the largest size |
| location name | 28 / 700 | `#2F54A1` blue, on the photo header |
| tab heading | 24 / 700 | "Beach Info" |
| **verdict** | **20 / 700** | the workhorse |
| section / tab label | 14 / 700 | "Beach status", "Beach info" |
| **body** | **14 / 400** | 526 elements, by far the dominant size |
| emergency lead-in | 14 / 700 uppercase | white on dark |
| group label | 12 / 700 uppercase / +0.25px | `HAZARDS`, `FACILITIES`, and the day columns |
| **eyebrow** | **10 / 700 uppercase / +0.2px** | above every verdict |

Only **three weights** in use: 400, 700, and nothing else. Size plus uppercase
plus letter-spacing does the rest.

## 3. Palette, by painted area

| colour | hex | where |
|---|---|---|
| dark navy | `#21263D` | the dominant chrome: icon tiles, emergency block, top banner. 24 painted elements, more than any other |
| white | `#FFFFFF` | panel and page ground |
| deep blue | `#005284` | secondary tiles |
| light blue | `#56BBD8` | tide tiles |
| warm off-white | `#F4F3F2` | section grounds |
| warm paper | `#FAF9F5` | page ground |
| near-black | `#30302E` | text |
| heading navy | `#1C3250` | headings |
| green | `#3B9C00` | low risk |

**The basemap is doing the most important job in the palette.** Safeswim draws on
a desaturated OpenStreetMap: beige land, pale blue water, grey roads, no
saturated colour anywhere. So the only strong colours on screen are the safety
pins, and they read instantly at any zoom.

Caribbean Guard draws on satellite imagery, which is full of saturated greens,
browns, turquoise and white surf. Our marks compete with the ground for
attention, and they lose at low zoom. **This is the single biggest structural
difference between the two products and it is not a styling change**; see the
open question at the end.

## 4. Geometry

| property | value |
|---|---|
| panel width | 384 px, fixed, with its own scroller and a hidden scrollbar |
| dominant radius | **4 px** (323 elements) |
| secondary radius | 6 px (100 elements) |
| pill radius | full round, for chips and the one floating action |
| larger radii | 8, 12, 14, 16 px, fewer than 20 elements combined |

Safeswim is **square**. 4 px is the house radius and almost everything obeys it.
Caribbean Guard is currently at 10 to 14 px on cards, sheets and buttons, which
reads softer and more consumer-app. Moving to 4 px and 6 px is the most visible
single change we can make and it costs nothing.

## 5. Components, and what each is for

### 5.1 The panel header
`< Close` (14/400) top-left, a photo band, the council's logo lock-up in the
top-right of the photo, and the location name at 28/700 in blue overlapping the
photo's lower edge. The attribution sits ON the header, not in a footer: whose
map this is, before anything it says.

### 5.2 Two tabs: `Beach status` | `Beach info`
The active tab is 14/700, the inactive 14/400. Nothing else distinguishes them.

This is the same split as our CHARACTER / TODAY axes, solved as navigation
instead of as stacked blocks:

- **Beach status** = what is true right now (water quality, lifeguard on duty,
  forecast, tide)
- **Beach info** = what is always true (description, hazards, facilities, images)

Under `Beach info`: a 24/700 heading, a prose paragraph at 16/400, then
`IMAGES`, `HAZARDS`, `FACILITIES` as 12/700 uppercase group labels over plain
14/400 lists. The hazards at Point Chevalier are literally "Deep water",
"Quicksand", "Shallow water" — nouns, no severity, no colour.

### 5.3 The emergency block
Dark navy panel. Uppercase 14/700 white lead-in, then the number:

> **IF SOMEONE IN THE WATER IS IN TROUBLE:**
> Dial 111
> Police.

The lead-in is the part to steal. It says **when** to call before it says what to
call, so the number is attached to a trigger rather than floating as a button
somebody might press for directions. Our red `Call 911` button has the number and
no trigger.

### 5.4 The legend sits next to the data it decodes
`Low Risk` / `High Risk` / `Wastewater overflow` renders as a compact icon-plus-
label row **directly above the forecast strip**, using the same pins the map
draws. It is not in a separate legend panel and there is no legend button.

This is the organisational idea Daniel is pointing at when he says "legends". A
key three scroll-lengths away from the thing it decodes is a key nobody reads.

### 5.5 The column strip
A horizontally scrollable grid: one column per time step, three stacked rows
sharing the column grid (risk pin, weather, wind), with the day label at 12/700
uppercase above each column and the value at 14/400 below each icon tile. Icon
tiles are ~40 px squares at 4 px radius on solid grounds.

We have no time series and no feed, so we do not need this component. We DO need
its discipline: **glyph above, value below, one column per thing, aligned grid.**

### 5.6 Map chrome
Small square controls at 4 px radius bottom-right (locate, +, −). One pill-shaped
floating action top-right, `Find Lifeguarded`, carrying the red-and-yellow flag
glyph. Attribution bottom-right at 12/400.

---

## 6. What we take, what we change, and why

| Safeswim | Caribbean Guard | decision |
|---|---|---|
| eyebrow / verdict / detail | six blocks in six shapes | **TAKE.** It is the best idea here |
| eyebrow at 10 px | our floor is 12 px (`--t-min`) | **ADAPT to 12 px.** Hat 4's accessibility floor outranks fidelity. Do not copy a 10 px label onto a sun-washed phone |
| body 14 px | ours is 15 px | **KEEP 15.** Same reason |
| verdict 20/700 | instruction 21/800 | **KEEP ours.** The instruction has to out-shout the verdict pattern, because ours is an order and theirs is a status |
| 4 px radius | 10 to 14 px | **TAKE 4 px / 6 px** |
| National | Inter | **KEEP Inter.** National is licensed; Inter is the same species |
| dark navy `#21263D` chrome | `#0b1c2c` ink | **TAKE their navy for the emergency block**, keep our ink for text |
| legend adjacent to its data | legend in a separate rail block | **TAKE.** Put the tier key next to the beach list, and the map-mark key next to the map |
| emergency lead-in above the number | bare red button | **TAKE the lead-in** |
| two tabs, status vs info | one sheet, cut to sign depth | **HOLD.** See the fork below |
| desaturated basemap | satellite imagery | **HOLD.** See the fork below |
| facilities, images, tides, forecast | none of it | **REJECT.** We have no feed and no survey. Rendering an empty forecast would be the "absence rendered as nothing" failure this project exists to avoid |

## 7. Two forks that are not mine to settle

**A. Density.** On 2026-09-17 Daniel ruled the right panel down to a lifeguard
sign plus one trust line, because there was "FAR TOO MUCH INFORMATION". Safeswim's
panel is denser than that: four sections, two tabs, three strips. Adopting its
*structure* is compatible with the sign ruling; adopting its *density* reverses
that ruling. This work takes the structure and holds the density, and the tabs
are not built.

**B. The basemap.** Safeswim's marks read because nothing else on screen is
saturated. Ours compete with satellite imagery. Switching to a desaturated
basemap would be the single largest legibility gain available, and it would cost:
the 2,389 precached satellite tiles (22.2 MB), the georeferencing work behind
them, and the thing that makes our map recognisable as YOUR beach rather than a
diagram. Not a styling decision.

---

## 8. What the first pass missed, corrected 2026-09-17

Daniel: *"How come nothing from the safeswim website brand language has been
adopted?"* He was right. The first pass took the skeleton and left the skin.

What was missing, found by opening a beach that actually has a status
(`/locations/piha-beach` rather than the quiet one I measured first):

**The verdict is not text on a white panel. It is a SOLID COLOURED CARD.**

```
+------------------------------------------+
|  [glyph tile]                            |   34 px rounded square, 4 px radius
|  CURRENT WATER QUALITY                   |   eyebrow, white, uppercase
|  Good water quality                      |   verdict, white, 20/700
|  Safeswim modelling predicts that the    |   detail, white, 14/400
|  water quality at this location is       |
|  suitable for swimming.                  |
|  ( Find out more  >               )      |   outlined pill, white, full width
+------------------------------------------+
```

Two grounds, and only two: **green** where the colour and the words agree
("Good water quality"), **navy** where the colour carries no verdict
("Lifeguards not on duty until next Summer"). The emergency block is not a peer
of the card, it is NESTED INSIDE the navy one, darker, with a red bar down its
left edge.

### Adopted

| | |
|---|---|
| solid status card, white text, glyph tile, eyebrow / verdict / detail | `.statuscard` |
| nested emergency sub-block, darker, red left bar | `.sos911` |
| outlined pill CTA inside the card | `.statuscard .cta` |
| white top bar, one hairline, no shadow | `.topbar` |

Their header measures `#fff`, 80 px, a 0.67 px bottom border and
`box-shadow:none`. Ours was a navy gradient fading into the imagery, so the bar
had no edge at all and the wordmark needed a text-shadow to survive whatever was
under it. A solid bar needs no shadow on anything, and the focus ring left the
white-outline list on the same day, because a white ring on a white bar is no
ring.

### The one thing we take differently, and why

**The ground is always navy here. It is never the tier colour.**

Safeswim can fill a card green because their lowest state is genuinely good.
Ours is IGUAL, TEN CUIDADO, which is not permission. A green card under those
words would say GO louder than the words say CARE, and on a safety map green
wins that argument every time; the 08-06 ruling that deleted SE PUEDE NADAR is
the same ruling. So the tier colour lives in the glyph tile and the left accent
bar at full strength, and the ground stays a constant that means nothing.

This is adopting one of Safeswim's two treatments rather than softening either.
