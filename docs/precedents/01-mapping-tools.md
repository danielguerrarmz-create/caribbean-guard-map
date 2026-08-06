# 01. Mapping tool precedents, and what they say about ours

Written 2026-08-06 against `web/index.html` as it stands today (57,567 bytes),
`web/data/cg-hazards.geojson` (14 features), and the two handoffs at
`docs/handoffs/2026-07-30-*.md`.

**How things were verified.** Every site below was fetched over HTTP and its raw
response inspected. Nothing here is described from memory. Where a claim comes
from reading response bytes it is marked OBSERVED; where it is a reasonable
reading of those bytes it is marked INFERRED. Sites that would not load are
listed as UNVERIFIED with the failure, and are not described.

**One limitation, stated up front.** I inspected HTTP responses, not running
browsers. I can tell you exactly what bytes a site sends and what libraries it
references. I cannot tell you what its bottom sheet feels like under a thumb.
Anything about interaction feel below is INFERRED from markup and should be
treated as weaker evidence than the byte counts.

**One input from outside this file.** The multi-organisation section responds to
the FECOGU finding in `docs/precedents/04-sector-scan.md` section 1b, which was
verified in a real browser after `costaricalifeguards.org` returned 403 to every
automated fetch attempted here. I have not independently verified it and I am
relying on it as reported.

---

## The shortlist

Revised after four research lanes reported. Ranked by how much each one should
change the next build, not by how impressive the site is.

| # | Precedent | Why it is on this list |
|---|---|---|
| 1 | **beaches.ie**, Environmental Protection Agency, Ireland | Displays **two** quality indicators side by side and says so out loud: the latest sample, and a rating averaged over four prior seasons. A beach can be Excellent and prohibited on the same day. Our `status` is one field doing both jobs. |
| 2 | **Safeswim**, Surf Life Saving NZ / Auckland Council | The most complete vocabulary found for *not knowing*: two distinct pin types mean "no data", separate from every verdict pin. |
| 3 | **NOAA National Hurricane Center** | The best-calibrated safety copy in the field. Its LOW tier does not contain the word safe, names the structures where rips persist anyway, and defers to the flags. Ours says `SWIMMING OK`. |
| 4 | **Blue Water Task Force**, Surfrider Foundation | A nonprofit our size running Workbox over Leaflet with a working update prompt, so blocker 2 is demonstrably solvable. Also the best small-org maintenance model: two front doors on one datastore. |
| 5 | **RNLI** | Publishes no live status **by choice**: schedule, doctrine, disclaimer, and the verdict pushed to the physical flags. The closest analogue to our real situation, and an architecture we have not seriously considered. |
| n/a | **Swim Guide**, Swim Drink Fish | The negative precedent. Same mission, same nonprofit scale, 868 KB of HTML on the map page, an ad script, two public CDNs and no integrity hashes. |

**What moved and why.** beaches.ie and Safeswim swapped into the top two because
both are schema decisions with a deadline: they get expensive the moment a guard
signs a single verdict. NOAA NHC entered at 3 because it indicts a label we are
shipping today on five unreviewed beaches. Surfrider fell to 4 because its
headline lesson is now qualified (see the `addAll` correction) and because it is
an implementation pattern rather than a decision. Beachsafe and Alerta Rio remain
below as full entries; they inform, but nothing about them changes what we build
next.

**A note on 1 and 3 together.** They are the same defect seen from two sides.
beaches.ie says our status field has too few dimensions. NOAA says the top value
on that field claims too much. Fixing one without the other leaves the map
still saying `SWIMMING OK` about water nobody has looked at.

---

## 1. Safeswim (Surf Life Saving New Zealand / Auckland Council)

**Map:** https://www.safeswim.org.nz/
**Legend:** https://www.safeswim.org.nz/pins

Beach-by-beach swim advice for the Auckland region, aimed at the public rather
than at lifeguards.

### The thing worth stealing: a vocabulary for not knowing

OBSERVED, fetched verbatim from `/pins`. Eleven pin types across three families:

| Family | Pin | Meaning, verbatim |
|---|---|---|
| Water quality | Green | "Good water quality: Water quality predicted to meet guidelines (low risk of illness)" |
| | Red | "Swimming not advised: Water quality predicted to exceed guidelines (high risk of illness)" |
| | Black | "Do not swim: Wastewater overflow nearby" |
| | Long-term red | "Swimming not advised: Water quality consistently poor" |
| | **Grey** | **"Data not available: Real-time water quality data is temporarily unavailable"** |
| | **Safety information** | **"Water safety information only: Real-time water quality not available"** |
| Lifeguards | On duty | "Surf Life Saving: Lifeguards are currently on duty" |
| | Off duty | "Surf Life Saving: Lifeguards are **not** on duty" |
| | Dangerous conditions | "Dangerous Conditions: Lifeguard warning. Stay out of the water." |
| Alerts | Hazard | "Hazard: Safety warning" |
| | Information | "Information: Other information of note." |

Three separate lessons in that table.

**First, "no data" is a first-class state with two flavours.** Grey means the
feed broke. "Water safety information only" means this beach was never in the
water quality programme at all. Those are different facts and they get different
pins. Our map collapses both into one amber "not verified" banner, and it has no
concept at all of a beach that is deliberately outside the programme.

**Second, the word is "predicted", not "is".** Every water quality verdict is
phrased as a prediction against a guideline, not as a measurement of the water in
front of you. OBSERVED elsewhere on the site: "Take care. There may be times when
the water is not suitable for swimming. Safeswim's water quality forecasts are
updated every 15 minutes." They tell you the cadence and they call it a forecast.

**Third, lifeguard presence is a separate axis from the swim verdict.** A beach
can be green and unpatrolled. We already do this correctly: blue station markers
are visually distinct from the status strokes, and the file comments say why
("a station is infrastructure rather than a swim verdict, and must not read as a
status"). Independent convergence with the largest surf lifesaving body in the
southern hemisphere is a good sign that decision was right.

### What it costs

OBSERVED, measured:

| | |
|---|---|
| Document | 97,591 bytes |
| `_next/static` chunks in the document | 20, totalling **317,722 bytes gzipped** |
| Total before any map library, tile or datum | **~415 KB** |
| Map library | Not present in the initial 20 chunks. Chunk `5855-aaf704f7531c8f24.js` contains the string `mapboxgl-children`. INFERRED: Mapbox GL JS or MapLibre, lazy-loaded in a chunk beyond the initial set. Mapbox GL JS is itself a further large download. |
| Viewport | `width=device-width, initial-scale=1`. Pinch zoom allowed. |
| Service worker / manifest | None found in the document. |

Next.js App Router (OBSERVED: `/_next/static/chunks/app/(frontend)/(withMap)/`).
No per-beach deep link found in the document; the only routes exposed are
`/about`, `/beach-safety`, `/contact`, `/faqs`, `/pins`,
`/terms-and-conditions`. INFERRED: beach selection is client-side state, not a
URL. That is a real weakness for a QR-code workflow and one we already beat.

### Verdict

Best-in-class semantics, expensive delivery. **Take the pin taxonomy. Take
nothing about the stack.** Our whole map is smaller than their JavaScript.

---

## 2. beaches.ie (Environmental Protection Agency, Ireland)

**Site:** https://www.beaches.ie/
**The explanation:** https://www.beaches.ie/frequently-asked-questions/

Every designated bathing water in Ireland, authored, hosted and maintained by the
EPA. It is here for one structural reason that changes our data model.

### One beach, two quality numbers, and they are different kinds of thing

OBSERVED, verbatim from their FAQ:

> "On www.beaches.ie, two quality indicators are displayed prominently. The
> 'Bathing Season Water Quality' refers to the result of the last sample taken...
> Annual Water Quality Ratings are the rating which the beach received for the
> previous season based on an average of the 4 prior seasons."

And, on the annual rating: "The annual water quality rating of a beach is based
on water quality monitoring results covering the previous four years."

The long-run classification is OBSERVED as `★★★ Excellent`, `★★ Good`,
`★ Sufficient`, `‾ Poor`. Note the glyph. **The classification is carried by a
count of stars, not by a colour**, which means it survives greyscale, sunlight
and colour blindness with no redundant encoding bolted on afterwards.

Separately, and on a different axis entirely, they run short-term notices.
OBSERVED, three named types: **"Prior Warning Notices"**, **"Advice Against
Bathing"**, **"Temporary Bathing Prohibitions"**.

### Why this is the second-most important entry in this document

Our `ZONES[].status` is a single field with three values, and it is currently
being asked to carry two different claims at once:

| Claim | Example from our own copy | How often it changes |
|---|---|---|
| What this beach *is* | Cocles: "The beach with the most rescues on this coast. Shifting sandbars create rip currents." | Rarely. Years. |
| What this beach *is like today* | Cocles is `danger` right now | Often. That is the point of the map. |

Today those are one word. The consequence is concrete and it is already visible
in the plan: `04-map-integration.md` describes a guard "changing Cocles from
danger to caution because the sandbar moved" by editing one word in
`status.json`. But the same word is also the thing that says Cocles is the most
dangerous beach on this coast. Flip it to `caution` and the map now says that
standing fact is no longer true, when all the guard meant was that the water is
calmer this week.

Worse in the other direction: **a beach whose standing character is benign can
be dangerous today, and our schema has no way to say so without permanently
relabelling the beach.** Punta Uva is `safe` and our own copy already carries the
exception ("Avoid the channel at the far east end, there is current there").
That exception lives in a `facts` bullet where nothing can act on it.

The EPA solved this by refusing to collapse the axes and by labelling both
prominently. We should copy the structure, not the four-year statistics, which
we have no data for and should not pretend to.

---

## 3. Blue Water Task Force (Surfrider Foundation)

**Map:** https://bwtf.surfrider.org/

Volunteer-collected water quality sampling, published as a map. A nonprofit at
roughly our scale, running roughly our architecture, having already solved the
thing that is blocking us.

### It is Leaflet, and it is a real PWA

OBSERVED, from the document and from `service-worker.js`:

- `<link rel="manifest" href="/manifest.json">`, plus `apple-touch-icon` at five
  sizes and `apple-mobile-web-app-capable`.
- An inline registration block: `navigator.serviceWorker.register('service-worker.js', { scope: '/' })`.
- `service-worker.js` is 21,261 bytes and identifies itself as
  **`workbox:precaching:5.1.4`** and `workbox:core:5.1.4`.
- The precache manifest at the tail holds **148 entries** as
  `{'revision': '<md5>', 'url': '<path>'}` pairs, including `index.html`,
  `main.js`, `manifest.json`, 14 lazy chunks `0.js` through `14.js`, and the
  image set.
- Three of those entries are `img/marker-icon_2273e3d.png`,
  `img/marker-icon-2x_401d815.png` and `img/marker-shadow_44a526e.png`. Those
  are Leaflet's own default marker assets. **INFERRED, with high confidence:
  Leaflet, bundled into `main.js` rather than loaded from a CDN.**

### The update prompt is the part people forget

OBSERVED, in the document body:

```html
<div id="update" class=""><span class="close">&times;</span>
<span id="reload">There is a new version available. <strong>RELOAD</strong></span></div>
```

The registration code listens for `updatefound`, watches the new worker reach
`installed`, and only then reveals that banner; clicking it posts
`{ action: 'SKIP_WAITING' }` to the waiting worker, and a `controllerchange`
listener reloads the page.

This matters more for us than for them. A cached-first safety map that cannot
tell the user "the beach statuses you are looking at are the old ones, tap to
get today's" is a map that will confidently show a stale verdict forever. If we
ship a service worker without this, we will have built exactly the failure mode
the provenance machinery exists to prevent, one layer further down.

### What it costs

OBSERVED, measured:

| | |
|---|---|
| Document | 8,073 bytes. A genuine app shell: one custom element, one `<script src="main.js">`. |
| `main.js` | **1,369,345 bytes raw, 245,271 gzipped** |
| Lazy chunks | 14 more, precached |
| Third-party in the document | Google Tag Manager, Google Fonts, and `cdn.jsdelivr.net/npm/halfmoon@1.1.1` |
| Integrity attributes | **None** |

So: the right architecture, carrying a payload we should not copy. Their
`main.js` alone, gzipped, is larger than our entire map including imagery.

### Verdict

**This is the answer to blocker 2, and it is proof by existence.** A nonprofit
beach-water charity ships Workbox over Leaflet and a manifest, and it works. Copy
the shape: precache manifest with content revisions, `SKIP_WAITING` update
prompt, manifest for Add to Home Screen. Copy none of the weight.

---

## 4. Beachsafe (Surf Life Saving Australia)

**Map / directory:** https://beachsafe.org.au/
**A beach page:** https://beachsafe.org.au/beach/qld/gympie/inskip/rainbow-beach

Every beach in Australia, for the public. The most authoritative body in the
field, and the closest thing to a national standard.

### Server-rendered, and the numbers are startling

OBSERVED, measured:

| | |
|---|---|
| Home document | 53,982 bytes |
| Beach page document | 55,358 bytes |
| `<script src=...>` tags in either document | **zero** |
| `<script>` tags on the beach page | 2, both `application/ld+json` |
| Map library referenced in the document | none found |

A national beach safety service delivers a beach's hazard information as plain
HTML with no client-side JavaScript in the document at all. INFERRED: the map is
a separate view, and the per-beach content deliberately does not depend on it.

That is the same instinct behind our beach picker cards carrying their status
text before anything is tapped, taken further. Their beach page works with
JavaScript switched off. Ours does not: our `ZONES` array is rendered by script.

### Status encoding: an ordinal, not a colour

OBSERVED, verbatim from the Rainbow Beach page:

> `Beach Length: 0.012km   General Hazard Rating: 5/10`

And a patrol schedule laid out by named day (`Sun 09 Aug`, `Mon 03 Aug`,
`Tue 04 Aug` and so on), with an image whose alt text is
`Patrolled Beach Flag`.

A ten-point ordinal survives greyscale, sunlight, colour blindness and
translation with no redundant encoding needed at all. It is not right for us,
because our three-way swim verdict is a decision, not a scale, and "6/10" does
not tell a tourist whether to get in the water. But it is worth knowing that the
biggest organisation in this field chose a number over a colour.

### The disclaimer, verbatim, and it is the best one found

OBSERVED:

> "SLSA provides this information as a guide only. Surf conditions are variable
> and therefore this information should not be relied upon as a substitute for
> observation of local conditions and an understanding of your abilities in the
> surf. SLSA reminds you to always swim between the red and yellow flags and
> never swim at unpatrolled beaches."

Three moves in three sentences: downgrade the artefact ("a guide only"), name the
reason (conditions are variable), and hand the user a rule that works when the
artefact is wrong (swim between the flags). Our map does the first two and not
the third.

### Two things not to copy

OBSERVED, the home document's viewport:

```
viewport-fit=cover, width=device-width, height=device-height,
initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no
```

**Pinch zoom is disabled.** On a beach safety site, on the device with the
smallest screen, used in bright sun by people who may be older or without their
glasses. Our map uses `maximum-scale=5` and allows it. We are right and they are
wrong.

OBSERVED, also on that page, an image alt attribute reading
`"Beach is patrolled and has green covid status"`. A COVID-era string still
shipping in 2026, on a page a screen reader user will hear. INFERRED: nobody has
audited the alt text since roughly 2021. Cautionary: a safety site's copy rots
quietly, and the accessibility layer rots first because nobody looks at it.

### Two data-model details from the beach-safety lane

Beachsafe ships **`weather.timediff`**, seconds since the observation, as a
first-class field alongside `rendered_at`. The interface can therefore age a
reading out on its own rather than making the client do date arithmetic against a
timestamp of unknown timezone.

We currently do exactly the arithmetic they avoided. `provenance()` in
`index.html` parses `reviewed.on`, constructs a local-time `Date` to dodge a UTC
off-by-one that the file's own comment records as a real bug ("a review dated the
1st displayed as 30 June"), then diffs against `Date.now()` and compares to
`REVIEW_VALID_DAYS`. That code is correct now, and it is the kind of correct that
breaks quietly. Shipping an age alongside the date would make the staleness rule
data rather than logic.

Second: Beachsafe's offline settings panel shows **`Beaches last synchronized
at:`** defaulting to the literal string **`Never`**. That is the honest-offline
pattern in four characters. A cache that has never populated says so, rather than
showing an empty field that reads as zero or as fine.

### PWA

OBSERVED, `manifest.json` exists and is well-formed: `display: standalone`,
`orientation: portrait`, two shortcuts ("My Beaches", "Surf Safety"), and
`related_applications` pointing at native iOS and Android apps. No service worker
registration found in the document.

---

## 5. Alerta Rio (Centro de Operações Rio, Rio de Janeiro)

**Site:** https://alertario.rio.rj.gov.br/

Municipal rainfall, radar and landslide-risk alerting for a city of six million.
The Latin American precedent that most directly addresses our provenance rule.

OBSERVED, measured: document 108,340 bytes, 31 script tags, references
`maps.googleapis`. INFERRED: Google Maps JavaScript API. Viewport
`width=device-width, initial-scale=1.0`, pinch zoom allowed.

### They say "tempo real", and they have earned it

OBSERVED, via fetch: the site carries "Registros em tempo real", "Imagens em
tempo real" for radar, and meteorological data "de 15 em 15 minutos". A rain
gauge network polling every fifteen minutes is entitled to the phrase.

This is the useful calibration for our own rule. The handoff's rule reads "the
interface may never claim more currency or authority than its data has", and it
was written after a proposed link description called our map "en tiempo real".
Alerta Rio is the counter-example that shows the rule is about *fit*, not about
banning the phrase. Nothing in our map polls anything, so the phrase is a lie
for us and true for them.

### The pattern worth taking: dated per-sensor outage notices

OBSERVED: the site publishes individual dated posts when a single instrument
goes down. Fetched examples include
`/2026/07/17/manutencao-da-estacao-iraja-4/`,
`/2026/06/12/manutencao-da-estacao-jardim-botanico-3/` and several
`manutencao-do-radar-meteorologico-do-sumare` notices.

The Irajá notice reads, verbatim: *"O sensor de umidade da estação Irajá
encontram-se em manutenção."* ("The humidity sensor at the Irajá station is
undergoing maintenance.") It carries a report stamp of `N200 17/07/2025 –
14h45min`.

Two honest observations about that. It gives no end date, only a start. And the
URL path says 2026 while the body says 2025, which is an internal inconsistency
on their site that I am reporting rather than resolving.

The principle survives the sloppiness: **a public safety map tells the public,
by name and with a date, which part of it is not currently reporting.** That is
exactly the shape of the statement our map needs for the 14.84 km east of the
annotated stretch, and for any beach whose review has expired. We currently say
it well in prose (`annotCoverage`, the amber unverified banner) but we say it
nowhere durable and nowhere dated.

---

## The negative precedent: Swim Guide (Swim Drink Fish)

**Map:** https://www.theswimguide.org/map/

A nonprofit beach water quality map, same mission family as ours, same
organisational scale. It is on this list because of what it costs.

OBSERVED, measured on the map page:

| | |
|---|---|
| Document | **868,656 bytes** |
| Framework | Nuxt (Vue), ten-plus `/_nuxt/*.js` chunks after the document |
| Third-party script origins in the document | **seven** |
| Integrity attributes | **zero** |

The seven, OBSERVED verbatim from `<script src>`:

```
//static.filestackapi.com/filestack-js/3.x.x/filestack.min.js
https://unpkg.com/supercluster@7.1.2/dist/supercluster.min.js
//api.tiles.mapbox.com/mapbox.js/plugins/geo-viewport/v0.1.1/geo-viewport.js
https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-...
https://static.cdn.prismic.io/prismic.js?new=true&repo=swim-guide
https://www.googletagmanager.com/gtag/js?id=G-CCB2KZWMSD
https://d3n6by2snqaq74.cloudfront.net/forms/keela-forms.min.js
```

Note the third line: a version-pinned plugin from `api.tiles.mapbox.com`, a
Mapbox path published around 2015, still in the critical path in 2026. Note the
fourth: **a Google AdSense script on a public water safety map.** Note
`filestack-js/3.x.x`, which is a floating version specifier, meaning the exact
code that executes changes without anyone at the organisation deciding it
should.

Seven origins means up to seven DNS lookups, seven TCP handshakes and seven TLS
negotiations before the map is usable. Our measurement of a single extra origin
(unpkg, below) put TLS alone at 1.27 s on a good home connection.

**This is what our map becomes if nobody defends it.** Not through one bad
decision, but through a decade of individually reasonable ones. It is the
strongest argument in this document for the constraint the project already has:
six files, one origin, no build step.

---

## The regional picture, and what it means for our priorities

Reported by the Latin America research lane, fetched not inferred. Across eight
verified national public-safety map viewers (SENAPRED Chile, CONAGUA Mexico,
CETESB São Paulo, CNE Costa Rica, OVSICORI Costa Rica, SMN Argentina, Cemaden
Brazil, IDEAM Colombia):

> **Not one registers a service worker or ships a manifest.** Five of eight are
> Esri-hosted. None uses MapLibre, Mapbox GL, deck.gl or Cesium.

That reframes our blocker 2. Offline is not a standard we are behind on. It is
the gap the entire regional field leaves open, on a continent where the people
most likely to need a hazard map are the ones least likely to have signal.

### Four patterns worth taking

**OVSICORI, Costa Rica, and this one is in-country.** Every earthquake popup
carries two provenance fields: `Autor` (what process produced this record) and
`Revisado` (has a human checked it, currently rendering `-`). That is exactly our
unowned-verdict problem, solved by the national volcanological observatory, with
the empty-review state rendering visibly rather than hiding. Our `reviewed`
object should carry the same two-part distinction: machine-extracted versus
human-confirmed are different claims, and today `cg-hazards.geojson`'s
`needs_confirmation: true` says so in the file and nowhere on screen.

**CETESB São Paulo**, the closest regional analogue to a beach verdict map at
2.1 million views, carries **three** date fields on every record:
`data_amostra_inicio`, `data_amostra_final`, `data_atual`, plus a dashboard
widget named `Proxima Atualizacao`. The window the observation covers, the moment
it was published, and when the next one is due are three different facts. Ours
collapses all of it into `reviewed.on`.

**SMN Argentina** names its severity levels with the instruction rather than the
colour: `Nivel amarillo - Informate`, `naranja - Preparate`,
`rojo - Segui instrucciones oficiales`. We already do this
(`NO NADAR`, `PRECAUCIÓN`, `SE PUEDE NADAR` are instructions, not hues), so this
is confirmation rather than a change. Worth recording so nobody "simplifies" the
labels into colour names later.

**SENAPRED Chile's entry splash** declares the data `REFERENCIAL`, tells the user
to verify with the responsible technical body, states it must not be used for
technical purposes, carries a version stamp matching the real publish date, and
includes an "Aclaraciones" panel explaining why hazard layers do not align at
their seams. That last part is the interesting one: they explain their own
registration error to the public rather than hoping nobody notices. We have a
5 to 75 m western error and an unconfirmable eastern third, currently explained
only in a source comment.

### Three cautionary findings, all observed by the lane

- **IDEAM Colombia** serves live `ALERTA ROJA` polygons with **no date field of
  any kind** in the attribute set and `timeInfo: None`, while press material
  calls it "tiempo real".
- **IMN Costa Rica** displays "Page updated: October 31th, 2023" above live map
  data.
- **SINAPROC Panama** publishes a genuinely good three-state beach flag
  vocabulary (`Baño libre`, `Baño con precaución`, `Prohibido el baño`) as three
  2020 JPEGs with empty `alt` attributes. No map, no location, no date.

The last one is the closest thing to a Central American precedent for what we are
building, and it is three untagged images from six years ago. That is the
standard in the region. It is not a high bar, which is a reason to be careful
rather than relaxed: the first artefact that looks authoritative here will be
believed.

---

## NOAA National Hurricane Center: the copy precedent

**Map:** https://www.nhc.noaa.gov/rip-currents/map.html

Verified by me, verbatim. Three tiers:

> **HIGH:** "Life-threatening rip currents are likely. Swimming conditions are
> unsafe for all levels of swimmers. Stay out of the water."
>
> **MODERATE:** "Life-threatening rips are possible and may appear suddenly.
> Remain in shallow water and beware of surf that can knock you off your feet."
>
> **LOW:** "Always exercise caution in the ocean. Life-threatening rip currents
> are still possible near groins, jetties, reefs, and piers."

Plus, on the same page: "Always follow advice from the local beach patrol and
flag warning systems" and "Swim near lifeguards and pay attention to the flags!"

**Read the LOW tier again.** The lowest rung of the United States' national rip
current forecast does not contain the word safe. It names the specific
structures where rips persist even when the risk is low, and then defers to the
flags on the sand.

Ours says `SE PUEDE NADAR` / `SWIMMING OK`. That is a stronger claim than NOAA
is willing to make at its lowest tier, on imagery positionally uncertain to 75 m,
about beaches no guard has yet reviewed.

And we already know it is too strong in at least one case. Punta Uva is `safe`,
and our own `facts` copy for it reads "Avoid the channel at the far east end,
there is current there." A reef, a channel and a headland are precisely the
NOAA list. The exception is already written; it is just not allowed to modify
the verdict.

---

## RNLI: the precedent for publishing no live status at all

Reported by the beach-safety lane. The RNLI publishes **no live beach status**,
by choice. What it publishes is a lifeguard patrol schedule, safety doctrine, and
an explicit uncertainty disclaimer, and it pushes the verdict itself to the flags
on the sand.

This deserves stating plainly because **it is the closest analogue to our actual
situation, and it is an architecture we have not seriously considered.** Today
zero of our five zones have been reviewed by anybody. If Caribbean Guard's guards
cannot sustain a review cadence after handover, the RNLI model is not a failure
state. It is a legitimate design: publish the geography, the stations, the rip
positions, the patrol hours and the doctrine, and let the physical flags carry
the verdict.

The decision that follows is worth putting to Caribbean Guard directly rather
than assuming: **is there a red-flag system on this coast, and does it work?**
Our Cocles copy already asserts "Red flags mark the active channels", which is
unverified. If that system is real and maintained, the RNLI model is available
and it removes the review-cadence dependency that currently threatens the whole
project after Daniel stops answering emails. If it is not real, the map is
carrying more weight than any of us have acknowledged.

---

## Also verified, briefly

| Site | URL | Measured | Note |
|---|---|---|---|
| Protected Planet (UNEP-WCMC) | https://www.protectedplanet.net/en | 45,242 B doc, 6 scripts, `mapbox-gl`, `manifest.json` | **Viewport is `maximum-scale=1, user-scalable=0`.** Pinch zoom disabled on a global public map. Second precedent to fail this; we pass. |
| Global Fishing Watch | https://globalfishingwatch.org/map | 154,189 B doc decoded (52,489 transferred), entry bundle `index-CVtilSow.js` **164,030 B transferred** | Desktop analyst tool. The map is the product, but the product assumes a laptop. |
| Allen Coral Atlas | https://allencoralatlas.org/atlas/ | 17,810 B doc, 3 scripts, React | Small shell, React app behind it. Could not observe status encoding from HTTP alone. |
| Marine Protection Atlas | https://mpatlas.org/zones | 89,003 B doc, React, `.webmanifest` | Could not observe map behaviour from HTTP alone. |
| NOAA rip currents | https://www.ripcurrents.noaa.gov/ | 26,170 B, jQuery 1.10.2 (2013), self-hosted, script block duplicated | An information page, not the forecast map. Everything self-hosted, which is the one thing it does better than us. |
| BeachWatch NSW | https://beachwatch.nsw.gov.au/waterMonitoring/searchBeach | 36,475 B, Angular shell, empty to a plain fetch | **Viewport `user-scalable=yes, ..., maximum-scale=5`.** Same choice we made. |
| NSRI (South Africa) | https://www.nsri.org.za/ | 59,160 B, 17 scripts, `cdnjs`, `.webmanifest` | Not primarily a map. |
| Shark Smart NSW | https://www.sharksmart.nsw.gov.au/ | 33,075 B, `mapbox-gl`, `cdnjs` | Hazard map, government, CDN-dependent. |
| SINAC (Costa Rica) | https://www.sinac.go.cr/ES/Paginas/default.aspx | 132,206 B, **52 scripts**, SharePoint, `user-scalable=no` | In-country agency. Blocks pinch zoom. |
| OVSICORI (Costa Rica) | https://www.ovsicori.una.ac.cr/ | 59,812 B, 30 scripts, `user-scalable=no` | In-country agency. Blocks pinch zoom. |

**UNVERIFIED, would not load, not described:**
`https://costaricalifeguards.org/` (HTTP 403 to every automated attempt;
subsequently opened in a browser by the team lead, see
`docs/precedents/04-sector-scan.md` section 1b),
`https://rnli.org/find-my-nearest/lifeguarded-beaches` (HTTP 403),
`https://environment.data.gov.uk/bwq/profiles/` (HTTP 403),
`https://tasks.hotosm.org/explore` (HTTP 403),
`https://www.cne.go.cr/` (HTTP 403),
`https://www.infopraia.pt/`, `https://swimfo.environment.data.gov.uk/`,
`https://www.surfguard.co.uk/`, `https://visor.snamchile.cl/`,
`https://www.chilepreparado.cl/`, `https://mapainteractivo.cenapred.unam.mx/`
(all connection failures).

Four of those five Latin American and European government URLs were my own
guesses at a path and were wrong. Recorded so nobody repeats the guess.

---

## The two publication blockers, answered

### Blocker 1: Leaflet from unpkg, no fallback

OBSERVED in our file, lines 8 and 225:

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
```

`grep -c "integrity=\|crossorigin="` over `web/index.html` returns **0**.

That is worse than the handoff records. The handoff frames this as a performance
and availability problem. It is also an **integrity** problem: the map executes
whatever unpkg serves, unverified, on a page whose job is to tell people whether
to enter the sea. There is no third-party script on the page at all except this
one, so the whole category of risk exists for one dependency that is 46 KB.

Three findings that close the argument:

**1. The cross-site caching benefit is gone, and has been since 2020.**
OBSERVED, from Chrome's own documentation at
https://developer.chrome.com/blog/http-cache-partitioning: partitioning rolled
out "through late 2020" starting in Chrome 86, and the cache key became a tuple
of top-level site, current-frame site and resource URL. The page acknowledges
the consequence for CDNs directly: services "that serve large volumes of highly
cacheable resources across many sites (such as fonts and popular scripts) may
see an increase in their traffic." The old justification for unpkg, that a
visitor might already hold Leaflet from some other site, no longer holds in any
current browser.

**2. The second origin is measurably expensive, on a good connection.**
Measured by me against unpkg from a home link:

```
leaflet.js   42,481 B gz   dns 0.054  connect 0.254  tls 1.267  ttfb 1.535 s
leaflet.css   3,543 B gz   dns 0.004  connect 0.187  tls 0.402  ttfb 0.438 s
```

1.27 s of TLS negotiation alone, on a connection far better than any beach in
Talamanca. That cost is paid before the first byte of Leaflet arrives, and it is
paid to reach a host we do not control.

**3. Vendoring has no version-churn cost.** OBSERVED from the npm registry:
Leaflet's `latest` dist-tag is **still 1.9.4**, published 2023-05-18. There has
been no stable release in three years; `2.0.0` exists only as `alpha.1`.
Vendoring 1.9.4 does not commit us to chasing anything.

**How the precedents solve it.** Surfrider bundles Leaflet into `main.js`.
Beachsafe ships no third-party JavaScript on a beach page at all. NOAA
self-hosts every script including a 2013 jQuery. Swim Guide does the opposite,
and is the cautionary tale. Of the sites examined, **no organisation that
treats its map as safety infrastructure loads its map library from a public
CDN.**

The fallback pattern (`onerror` to a local copy) is not worth building. If we
are shipping the local copy anyway, ship only the local copy: it removes the
CDN, the DNS lookup, the TLS handshake, the integrity question and the fallback
code in one edit.

### Blocker 2: an offline promise with no service worker

OBSERVED in our file: `grep -c` over `web/index.html` returns **0** for
`serviceWorker`, `caches.`, `rel="manifest"`, `webmanifest` and
`navigator.onLine`. And line 1021 runs, unconditionally, on every page load:

```js
say(T[lang].save,5200);
```

which displays, verbatim, `"Guarde esta página. La señal es débil en la playa."`
and `"Save this page. Signal is weak on the beach."`

So the single most-seen string on the map, shown to every visitor before they do
anything, instructs them to perform an action the page cannot perform. **This is
the same class of failure as "en tiempo real", applied to capability instead of
data,** and it is currently shipping while the data-side rule is enforced
rigorously three functions away. That inconsistency is the sharpest thing in this
audit.

**The iOS eviction claim in `04-map-integration.md` is true, but the doc states
it in the form that leads to the wrong conclusion.**

OBSERVED, from WebKit's own post at
https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/,
verbatim:

> "ITP has aligned the remaining script-writable storage forms with the existing
> client-side cookie restriction, deleting all of a website's script-writable
> storage after seven days of Safari use without user interaction on the site."

The affected forms are listed explicitly and include **Service Worker
registrations and cache**. So the seven days are real.

But two qualifications change what we should build:

- It is **seven days of Safari use without interaction on the site**, not seven
  calendar days. A tourist who opens the map once a week keeps it.
- **Home Screen web applications are exempted.** WebKit, verbatim, on the same
  page: home screen applications have "their own counter of days of use" that
  resets with actual app interaction, and "We do not expect the first-party in
  such a web application to have its website data deleted."

And WebKit's current storage-policy page at
https://webkit.org/blog/14403/updates-to-storage-policy/ gives the mechanism:
an origin can request persistent mode via `StorageManager.persist()`, in which
data is "excluded from eviction", and WebKit "currently grants a request based
on heuristics like whether the website is opened as a Home Screen Web App."

MDN (https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist)
confirms `navigator.storage.persist()` is Baseline and has been available across
browsers since December 2021, resolving `true` when granted, in which case
"Storage will not be cleared except by explicit user action."

**The consequence for us is a reordering, not a new idea.** The web manifest is
currently listed in stage 3 as a nice-to-have that makes the "save this page"
line true. It is not a nice-to-have. **Add to Home Screen is the documented
mechanism by which our offline cache survives on the platform most tourists
carry.** Manifest and service worker are one feature, not two, and the manifest
is the half that makes the other half durable.

Surfrider proves the whole shape is achievable by an organisation our size, and
supplies the update-prompt pattern that keeps a cached safety verdict from going
silently stale.

### On the `status.json` split

No precedent examined publishes its editable status layer, so I cannot show you
one doing this. What the precedents do establish is the **shape** the split has
to take, and three requirements the current proposal misses.

**1. Two axes, not one.** Per beaches.ie above: the EPA displays a standing
classification and a current reading as two prominently labelled indicators, and
refuses to merge them. Our single `status` word is being asked to mean both "what
this beach is" and "what it is like today", and the split as currently specced in
`04-map-integration.md` would harden that conflation into the file a guard edits.
Fix it in the schema, before anyone writes the first record.

**2. Absence is not one thing.** Safeswim's eleven pins carry two distinct
no-data states. Our `reviewed: null` currently renders one amber banner for at
least three different situations: nobody has ever checked, the check expired, and
the beach was never in scope. A guard reading "sin verificar" cannot tell which,
and the three call for different behaviour from a swimmer.

**3. Provenance needs an organisation, not just a person.** See the multi-org
section below. `reviewed: {by: "Elías", on: "..."}` identifies a human but not
who stands behind the verdict.

And a finding from our own repo that bears directly on the split, verified today:

**`web/data/cg-hazards.geojson` contains four `rescue_station` features that the
map never reads.** `drawAnnotations()` handles only `rip_current` and
`shaded_area_meaning_unknown`; the string `rescue_station` does not appear in
`web/index.html` at all. Meanwhile `POSTS` hardcodes the same four stations. I
compared them: the coordinates are identical to five decimal places across all
four. So the same four objects have two sources of truth, and the copy that lives
in the file called "the data file" is inert. Anyone who moves a station in the
GeoJSON, which is the obvious place to move it, will change nothing.

That has to be resolved as part of the split, or the split will add a third
place.

### The challenge to this whole recommendation, and it is a fair one

The marine lane found something about Surfrider that cuts against the file-based
approach. BWTF runs **two front doors on one datastore**: an authenticated
`/dashboard/` where volunteers enter results, and a public `/explore/` that reads
the same store. **Nobody edits code, or a file, to update the map.**

`04-map-integration.md` reaches the opposite conclusion, and reaches it for a
good reason: it is blunt that "if updating the map requires Daniel, the map dies
when Daniel stops answering emails", and it explicitly rejects building "a CMS
nobody asked for and nobody uses". Its tier 2 (a form that writes `status.json`)
is deferred until tier 1 is "observed to fail".

I think that sequencing is still right, and here is the honest reason rather than
a restatement: **Surfrider's dashboard exists because they have a volunteer
sampling programme producing a stream of records. Caribbean Guard has five zones
and a review cadence nobody has yet demonstrated.** Building the editing surface
first optimises a workflow we have not observed. Tier 1 is cheap enough that
finding out costs almost nothing.

But the lane's framing is worth keeping on the record because it names the real
risk: **"every hazard needs an owner" may be an editing-surface problem, not a
data-format problem.** If the guards' sign-off round stalls, the diagnosis to
reach for first is not a better schema. It is that editing a file in a Cloudflare
dashboard is still too much friction for somebody who has just come off a beach,
and the answer then is a form, quickly, not a redesign.

A related open question the sector scan raised and this one cannot answer:
`docs/precedents/04-sector-scan.md` records a delfino.cr report of **nine**
rescue stations against the **four** on our map. Both can be true, since the
annotated sheet covers 1.82 km of 16.66 km. But whatever `status.json` ends up
looking like, the station layer needs a field that distinguishes "these are all
of them" from "these are the ones inside the mapped window", or the map silently
asserts the stronger claim.

---

## Should the data model support a second organisation?

Raised by the team lead off the back of the FECOGU finding in
`docs/precedents/04-sector-scan.md` section 1b: Caribbean Guard is a **founding
member** of the Federación Costarricense de Guardavidas, whose own site has a
`Playas y Seguridad` nav item that is one of 25 dead `#` links, and whose only
working affiliate link points at caribbeanguard.org. Playa Grande Lifeguards is
the obvious second contributor.

I was asked to say plainly if this is premature. **It is mostly premature, and
there are exactly two seams worth leaving open. Both are one field each.**

### First, the part that is genuinely premature

A second stretch of coast is **not a data-model problem. It is a georeference
problem.** Everything that made this project hard lives in constants that are
specific to one 16.66 km strip:

```
IMG_BOUNDS          the solved georeference for this coast
IMG_SAFE            the inscribed rectangle of this rotated quad
GEO_ACCURACY_M 75   what we can defend in the west of this coast
GEO_ACCURACY_EAST_M 150
GEO_EAST_OF -82.699 the longitude where confidence drops, on this coast
```

Plus one base image, one blurred backdrop sized from it, and a coastline traced
by `tools/redraw_zones.py` against Bing for this shoreline. Adding Playa Grande
means acquiring imagery, solving a georeference, measuring its residual, and
tracing its waterline. That is where essentially all of 2026-07-29 and 2026-07-30
went.

Generalising `IMG_BOUNDS` into a per-region structure today would add indirection
with no second case to validate it against, and it would produce something that
**looks** multi-region without being it. Given this project's own standing rule
about not claiming more than the artefact supports, shipping a "multi-org data
model" that cannot actually hold a second coast would be the same failure one
level up. Do not build it.

### Second, the two seams that are cheap now and corrosive to retrofit

**Seam 1: namespace the zone and station ids.** Ids are currently bare strings
(`"cocles"`, `"est1"`). This is not hypothetical: `04-sector-scan.md` line 24
records that Caribbean Guard has rescue towers at Cocles **and at a "Playa
Grande"**, and Playa Grande Lifeguards is a Pacific-side organisation named after
a different Playa Grande. The collision exists inside the current data set,
before any second org is involved.

**Seam 2: put the organisation on the provenance record**, alongside the person.

Cost now: a prefix convention and one field in the `status.json` schema. An hour,
most of it deciding the convention.

Cost of retrofit later: **every verdict that has already been reviewed and dated
has to be rewritten.** And provenance records are the one category of data in
this system that should never be rewritten, because their entire value is being
an unaltered, timestamped statement of who said what. The handoff is explicit
about why that matters: it "turns the claim from a guarantee into a timestamped
observation, which is the difference that matters if this is ever read back to
somebody after an accident." A migration that rewrites those records destroys
precisely the property they exist to provide.

**That asymmetry is the whole argument, and it does not depend on a second
organisation ever appearing.** It is not "multi-org is likely". It is "this
particular retrofit corrupts the one thing we most care about, and avoiding it
costs an hour."

The federation finding raises the stakes on provenance rather than lowering
them, and the sector scan says so too. If this map becomes the federation's de
facto safety page, `reviewed.by` needs to answer "which organisation stands
behind this verdict", not just "which person typed it".

---

## The audit

Ranked. Everything in the first group is justified by something specific above.

### Ranked, by what it costs against what it buys

| # | Change | Costs | Buys | Reversible? |
|---|---|---|---|---|
| 1 | Vendor Leaflet, drop unpkg | 46 KB in repo, 2 lines | Removes the only third-party dependency and the only unverified code path on a safety page | Trivially |
| 2 | Re-export the overview at 1000x335 q70 | One command | **52.8 KB off the critical path**, already specced, never done | Trivially |
| 3 | Change the "Guarde esta página" string | One line | Stops the map promising a capability it does not have, on every load | Trivially |
| 4 | Two axes in `status.json`, before it is written | A schema decision, ~1 hour | Stops one word meaning both "what this beach is" and "what it is like today" | **No.** Every record written under the wrong schema has to be migrated |
| 5 | "No data" as a rendered state with reasons | ~half a day | Three different absences stop rendering as one amber banner | Cheap while there are zero reviewed records; expensive after |
| 6 | Namespace ids + `org` on provenance | ~1 hour | The two seams a second organisation would need | **No.** Retrofit means rewriting dated provenance records |
| 7 | `id` on every GeoJSON feature | ~1 hour | Makes the guards' sign-off workflow buildable at all | No. Retrofit breaks any review already attached |
| 8 | Manifest + service worker + `persist()` | Days | The offline promise, durably, on iOS | Yes, but it gates publication |
| 9 | Resolve the duplicated stations | ~1 hour | One source of truth for the four stations | Yes |
| 10 | Third disclaimer sentence | Needs Caribbean Guard | A rule that works when the map is wrong | Yes |
| 11 | Soften `SE PUEDE NADAR` toward NOAA's LOW tier | One string, needs sign-off | Stops the map making a claim the US national forecast will not make at its lowest tier | Yes |
| 12 | `og:` tags on the deep links | ~20 lines, no JS | A WhatsApp-pasted `?z=cocles` previews and reopens at the right beach | Yes |

**Items 4, 5, 6 and 7 are the ones with a deadline.** They are all cheap today
and all expensive the moment a guard has reviewed and dated a single verdict,
because that is the point at which migrating the schema means rewriting a
provenance record. Everything else on this list can be done in any order, at any
time, for the same price. If only one thing comes out of this document, it should
be that **the schema decisions have to land before the sign-off round, not
after.**

### The detail

Numbered to match the table above. Grouped by theme rather than by rank, so they
do not appear in numerical order.

**1. Vendor Leaflet, delete the unpkg tags, and do not build a fallback.**
Justified by: no cross-site cache benefit since Chrome 86 (Chrome docs); 1.27 s
of measured TLS to a second origin; zero integrity attributes today; 1.9.4 is
still `latest` so there is nothing to chase; and no safety-infrastructure map
examined uses a public CDN for its map library. 46 KB, two lines changed, one
whole class of failure and one supply-chain exposure removed.

**8. Manifest plus service worker, shipped together, with an update prompt.**
Justified by: WebKit's documented Home Screen exemption and
`StorageManager.persist()`; and Surfrider's live Workbox implementation as proof
of feasibility at our scale. Take their `SKIP_WAITING` reload banner too. A
cached safety verdict with no way to announce that it is old is worse than no
cache.

**Correction to my earlier draft, and it matters.** I recommended copying
Surfrider's precache shape. Their 148-entry `addAll` list is the fragile part,
and I should not have pointed at it without this caveat. MDN's Using Service
Workers guide, verbatim:

> "If the promise is rejected, the installation fails, and the worker won't do
> anything."

`addAll` is all-or-nothing, and the specification makes it reject on any response
outside the 200 range. **One 404 in the precache list silently disables offline
support entirely,** with nothing visible to the user and nothing visible to the
person who deployed it. On a map whose offline capability is the reason it exists,
that failure mode is unacceptable as a silent one.

Two ways out, both cheap at our size: enumerate the list from a build-time
manifest so it cannot drift from what is on disk, or use `Promise.allSettled`
over individual `cache.put()` calls so a missing asset degrades one file instead
of the whole feature. With six files we can afford to do both and log what
failed.

Note also that our critical assets and our optional assets are different: the
2.52 MB `base.webp` failing should not take down a precache that would otherwise
have delivered a working overview-resolution map. Tier the list.

**3. Until 8 ships, change the string.** `"Guarde esta página"` currently
promises a capability the page does not have, on every load. One-line fix, and
it is the same rule the file already enforces for data. Change it or back it.

**4. Split `status` into two fields before `status.json` is written.**
Justified by beaches.ie, which displays a standing classification and a current
reading as two prominently labelled indicators and refuses to merge them. Ours is
one word carrying both claims, and the split as currently specced would harden
that into the file a guard edits. Concretely: a `character` field that changes
in years and a `today` field that changes in days, with the interface showing
both and saying which is which. We have no four-year statistics and should not
imitate the EPA's numbers, only its structure.

**5. Make "no data" a rendered state with a reason, not an absence.**
Justified by Safeswim's grey pin ("Data not available") and its safety-
information pin ("Water safety information only"), which are two different ways
of not knowing and get two different marks. Today a `null` review means "nobody
checked", "the review expired" and "this beach was never in scope" all at once,
and the amber banner cannot tell the reader which. The third case matters most:
14.84 km of our 16.66 km coast is outside the annotated window, and the map
currently says so in a toast that fires once, six seconds after load, and then
disappears. An absence rendered as nothing is indistinguishable from an absence
of hazard, which is the precise misreading the coverage caveat exists to
prevent.

**6. Namespace the ids and put the organisation on the provenance record.**
Two fields. See the multi-org section for the full argument; the short version is
that the retrofit cost is paid in rewritten provenance records, which is the one
migration this system should never perform.

**7. Give every GeoJSON feature a stable `id`.** Verified: no feature in
`cg-hazards.geojson` has one. Property keys across all 14 features are exactly
`area_m2, direction, kind, length_m, needs_confirmation, note, source`. Without
an id there is nothing to attach `confirmed_by` and `confirmed_on` to that
survives a re-extraction, so the review workflow the whole project is gated on
cannot be built. This is a prerequisite for the guards' sign-off, not a nice-to-have.

**9. Resolve the duplicated stations before splitting `status.json`.** Four
`rescue_station` features in the GeoJSON are dead; `POSTS` in `index.html` is
live; the coordinates agree exactly. Pick one owner.

**11. Soften the `safe` label toward NOAA's LOW tier.** See the NHC section.
The lowest rung of the US national rip current forecast does not contain the word
safe, and names the structures where rips persist anyway. Ours says
`SE PUEDE NADAR` / `SWIMMING OK` on unreviewed beaches, and our own Punta Uva
copy already contradicts it. This is a copy change that needs Caribbean Guard's
sign-off rather than ours, because softening a safety label is their call, but it
should go to them as a recommendation rather than a question.

**12. Add `og:` tags that preserve the deep link.** From MarViva, see the
link-rot section. Twenty lines, no JavaScript, and it makes a shared
`?z=cocles` legible in the channel this will actually be shared in.

**10. Add the third sentence to the disclaimer.** SLSA's verbatim text gives the
user a rule that works when the map is wrong: "always swim between the red and
yellow flags and never swim at unpatrolled beaches." We tell people what we do
not know and stop there. The equivalent for this coast, whatever Caribbean Guard
says it is, belongs on the map. This one needs them, not us.

**2. Re-export the overview. It is 52.8 KB heavier than specced.**
Measured, not estimated. `04-map-integration.md` specced a 1000x335 q70 overview
at 29 KB and it was never exported; the repo still ships `base-lo.webp` at
1200x402, **88,718 bytes**. The 2026-07-30 handoff calls it "the 1200 px, 63 KB
overview", which is wrong by 41 percent against the file on disk. I re-exported
from `base.webp` into the scratchpad, production untouched:

| Export | Bytes |
|---|---|
| **1000x335 q70** | **35,932** |
| 1200x401 q60 | 43,170 |
| 1200x401 q70 | 50,454 |
| 1400x468 q70 | 69,716 |
| shipping today (1200x402) | 88,718 |

One command, 52,786 bytes off the critical path.

### The number that motivates 1 and 2 together

Our real critical path today, measured from the repo this morning:

| Asset | On disk | On the wire |
|---|---|---|
| `web/index.html` | 57,567 | 21,155 gz |
| `leaflet.js` (unpkg) | | 42,481 gz |
| `leaflet.css` (unpkg) | | 3,543 gz |
| `web/img/base-lo.webp` | 88,718 | 88,718 |
| `web/data/cg-hazards.geojson` | 8,821 | 1,179 gz |
| **Total** | | **157,076 B = 153 KB, 5 requests, 2 origins** |

`04-map-integration.md` states this is **86 KB**. It is 153 KB, 78 percent over.
Two causes: `index.html` grew from 30 KB to 57.5 KB raw since that measurement,
and the specced overview was never exported.

Doing 1 and 2 gets it to **104,290 B = 102 KB, 5 requests, one origin**, without
touching a line of application logic. The remaining gap to the original 86 KB
figure is `index.html` itself, which has nearly doubled. That is worth knowing
before anyone quotes the 86 KB number again.

### Changes that are just different, not better

- **Ordinal hazard ratings (Beachsafe's 5/10).** Robust to every display
  problem, but it does not answer "can I swim". Our three-way verdict is the
  right shape for a decision. Do not convert.
- **A pin-per-beach map (Safeswim).** Their coastline is a bay system with
  discrete beaches. Ours is one continuous 16.6 km strip where the question is
  "which stretch am I on", which is why our polylines and picker cards are right
  and pins would be worse.
- **Separating patrol status from swim verdict.** Already done, correctly, for
  the reason the file's own comment gives.
- **Framework rewrite.** Every precedent that adopted one pays 250 KB to 415 KB
  for it. Nothing in this document suggests a benefit that would justify that
  here.

### Do NOT copy

- **Disabling pinch zoom.** Beachsafe (`user-scalable=no`), Protected Planet
  (`user-scalable=0`), SINAC and OVSICORI all do it. On a safety map read in
  bright sun by people who may not have their glasses, it is indefensible. Our
  `maximum-scale=5` is correct. Note it in the file so nobody "fixes" it.
- **Third-party scripts of any kind.** Swim Guide carries seven origins
  including AdSense and a floating `3.x.x` version. Our map has exactly one
  third-party dependency and this document argues for removing it. Hold that
  line: the constraint is one origin, not "few origins".
- **Unbounded reliance on Google Maps for directions.** We link out twice
  (`openZone`, `openPost`). Those are the only remaining external references
  after Leaflet is vendored, and they are dead offline. Keep them visibly
  secondary to `tel:911`, which the current layout already does.
- **PMTiles.** See the dedicated section below. Short version: it is real, it
  works with Leaflet, and it is the wrong tool here for a reason that is
  specific and checkable rather than a matter of taste.
- **Alerta Rio's "tempo real" language.** They earned it with a fifteen-minute
  polling network. We would be borrowing the word without the machinery.
- **A generalised multi-region architecture.** See the multi-org section. Two
  fields yes, an abstraction no. Building something that looks multi-region
  without being able to hold a second coast would be the project's own
  overclaiming rule violated one level up, in the architecture instead of the
  copy.
- **beaches.ie's four-year statistics.** Copy the two-axis structure. Do not
  imitate the numbers: the EPA has a sampling programme and we have none, and a
  standing classification that looks computed when it was typed would be the
  worst kind of borrowed authority.

---

## How small nonprofit maps actually die, and it is never the code

Reported by the marine lane, all observed. This is the most useful section in the
document for anyone who has to keep this map alive after handover, because every
single failure below is a **link** problem, not a programming problem, and every
one of them would have been prevented by the same rule.

| Organisation | What has happened to it |
|---|---|
| Reef Check (a subdomain) | Now `302`s to gambling spam |
| MarViva | `404`s its own stylesheet, pulls CSS from `cdn.rawgit.com`, which has been sunset |
| SkyTruth | Loads two scripts from `cdn.rawgit.com` off a mutable `master` branch, no SRI |
| SINAC, Costa Rica | Serves only a leaf certificate with no intermediate, so stricter clients fail outright |
| Protected Planet | Ships two Font Awesome versions from two dead CDNs |

Nobody wrote a bug. Domains lapsed, CDNs shut down, certificate chains were
misconfigured, and a subdomain was allowed to expire into the hands of somebody
selling casinos. The organisations are still operating. The maps are broken
anyway.

Two things follow, and they are the same thing viewed from two angles.

**First, this is the strongest possible argument for zero third-party origins.**
Not "few". Zero. Every one of the rows above is a dependency somebody reasonably
took on years ago. Our map currently has exactly one, and it is `unpkg`. Removing
it is recommendation 1 and this table is why the recommendation is not about
performance.

**Second, the "gambling spam" row is the one to sit with.** A conservation
nonprofit's link now points at a casino. If a Caribbean Guard QR code on a
physical sign at Cocles ever resolves to something like that, it will be printed
on aluminium, bolted to a post, and unfixable in the field. **The QR codes are
the most permanent thing this project will produce and the least revisable.**
That argues for the human-readable URL under every code, which
`04-map-integration.md` already specifies, and for the domain being owned by
Caribbean Guard rather than by anyone else, which the same document flags as an
open question. Both matter more after reading this table than before.

### One cheap trick worth stealing, from MarViva

Despite everything above, MarViva does one thing well: it server-renders
`og:title`, `og:description`, `og:image` and `og:url` on an otherwise-empty app
shell, **with its `location=lat,lon,zoom` deep link preserved in `og:url`**.

We have deep links already (`?z=cocles`, `?p=est2`) and no Open Graph tags at
all. Our map will be shared in WhatsApp, because that is how information moves
on this coast, and today a pasted link previews as nothing and carries no
indication of which beach it is about. Static `og:` tags plus a preview image
are perhaps twenty lines and no JavaScript. Do it when the deep links are next
touched.

### And one negative worth quoting when somebody suggests ArcGIS Hub

Somebody will, because five of eight regional agencies are Esri-hosted and it is
the obvious institutional answer. Measured by the marine lane: **MarViva's ArcGIS
Hub geoportal is 2,175 KB compressed and renders 38 characters of text without
JavaScript.**

That is most of our entire offline payload, spent before a single hazard is
drawn, on a platform we could not add a service worker to.

---

## PMTiles: the call, and the reason it is not a judgement call

Asked directly: should PMTiles plus `leafletRasterLayer` replace the single-image
base?

**No. It is over-engineering for this strip, and there is one hard technical
reason on top of that which is worth writing down because it is not obvious and
it will come up again.**

Everything about it checks out first. OBSERVED from
https://docs.protomaps.com/pmtiles/leaflet, the integration is genuinely a
three-liner:

```javascript
import { PMTiles, leafletRasterLayer } from 'pmtiles';
const p = new PMTiles('https://example.com/data.pmtiles');
leafletRasterLayer(p).addTo(map)
```

`leafletRasterLayer` ships in the `pmtiles` package, works on raster archives
(the docs note "the base distribution of Leaflet only supports raster images for
tiled data sources"), and I confirmed range serving works in practice: a
`Range: bytes=0-127` against the protomaps demo archive returned
`206 Partial Content` with `Content-Range: bytes 0-127/137205571996`.

### The hard reason: a 206 cannot go in the Cache API

PMTiles works by HTTP Range requests. Range requests return `206 Partial
Content`. And the Service Worker specification forbids storing a 206 in the
Cache API, in both entry points. OBSERVED, verbatim from
https://w3c.github.io/ServiceWorker/:

> For `addAll`: "If response's type is `error`, or response's status is not an ok
> status **or is 206**, reject responsePromise with a TypeError."

> For `put`: "If innerResponse's status **is 206**, return a promise rejected
> with a TypeError."

(MDN's `Cache.put` page does not mention this. The specification is the
authority, and it is unambiguous in both places.)

So a PMTiles base **cannot be precached by a service worker in the ordinary
way.** That is not a minor inconvenience. Full precacheability is the exact
property that decided the single-image architecture over the tile pyramid in
`04-map-integration.md`, on measured grounds, for an artefact whose purpose is
working at the water's edge with no signal. Adopting PMTiles would trade away the
deciding property to solve a problem we measured ourselves not to have.

You could work around it: fetch the whole archive as one ordinary 200 request and
cache that, or cache decoded tiles individually. But the first is the single
image with extra steps, and the second is the tile pyramid with extra steps. Both
carry a new runtime dependency.

### Giving the strongest version of the case its due

The offline lane found real points in its favour and they deserve engaging rather
than brushing past, because two of my earlier objections were weaker than I
stated:

- It works with **plain Leaflet, no WebGL, no tile server**, on any static host
  with range requests.
- The browser bundle is small. I measured it: **19,668 bytes raw, 7,755 gzipped.**
  My "adds a third-party runtime dependency" objection is true but the weight
  version of it is not: 7.8 KB is noise next to Leaflet's 42 KB.
- `pmtiles extract --bbox --maxzoom` runs against a remote URL, so building a
  strip-sized archive does not require downloading a continent.
- The US National Park Service runs PMTiles in production.

So the objection cannot be weight or ergonomics. It has to be the arithmetic, and
the arithmetic is where it fails.

### The arithmetic, run honestly

Suppose we cap at z16 (2.36 m/px, near our 1.85 m/px ceiling). From
`04-map-integration.md`'s own tile counts and measured WebP encoding weights,
z11 through z16 is 459 tiles at roughly 4.1 KB, so **about 1.9 MB**. That is
genuinely smaller than the 2.52 MB single image. On disk, PMTiles wins.

It loses on the number that actually matters:

| | Single image, as built | PMTiles, z11 to z16 |
|---|---|---|
| Bytes for someone who scans a QR code, reads their status and pockets the phone | **88,718** today, **35,932** after recommendation 2 | The archive header, plus every tile covering the opening view |
| Bytes to hold the whole thing offline | 2.52 MB, one `cache.put` | 1.9 MB, **which the Cache API will not store**, because every read is a 206 |
| Runtime dependency | none beyond Leaflet | +7,755 gzipped |

The dominant user on this map is the one who scans, reads a card and leaves. The
progressive single-image strategy is built precisely around never charging that
person for detail they did not ask for, and it is the reason
`04-map-integration.md` chose it. PMTiles cannot beat 36 KB for a first view,
and it cannot be precached at all.

**NPS running it in production is not evidence it fits us.** They have continental
coverage, deep zoom, a tile budget and a team. We have a 16.66 km strip, a
1.85 m/px ceiling on partly generative imagery, and one volunteer nonprofit who
will inherit this. Scale mismatch cuts both ways and this is the direction that
matters.

### Two smaller reasons that also hold

1. **It buys resolution we should not serve.** Our imagery is positionally
   uncertain to 75 m in the west and not confirmable at all east of Punta Uva.
   Deeper tiles would dress a guess up as a survey. Settled already in
   `04-map-integration.md`; PMTiles does not change the underlying imagery.
2. **Cloudflare Pages range support is unconfirmed.** My tests returned `200`
   from a transforming layer rather than `206`, which proves nothing either way.
   GitHub Pages is confirmed (`206`, `Accept-Ranges: bytes`). Since the hosting
   decision is already made in favour of Cloudflare Pages for handover reasons,
   this would need testing against a real deployment first.

**Revisit only if a guard, standing on the sand, says 1.85 m/px is too soft to
use.** That is the question `04-map-integration.md` already flagged as the one
that would reopen this, and it is answerable by a person in five minutes. If the
answer ever comes back "too soft", PMTiles is then the right tool and this
section becomes the build plan rather than the rejection.

---

## Open, and honestly so

1. I did not run any of these in a browser. Interaction claims are INFERRED from
   markup and are the weakest evidence here.
2. Safeswim, Allen Coral Atlas, Marine Protection Atlas and BeachWatch NSW
   return app shells to a plain fetch. Their status encoding at the pin level is
   only as verified as their published legend pages, and only Safeswim publishes
   one.
3. I found **no** Costa Rican or Central American precedent for a public coastal
   safety map. SINAC and OVSICORI were reachable but are agency sites, not
   beach-safety maps. `costaricalifeguards.org` returned 403 to every automated
   fetch I attempted; the team lead opened it in a real browser and the result is
   in `docs/precedents/04-sector-scan.md` section 1b. It confirms the absence
   rather than filling it: the national federation's own `Playas y Seguridad` nav
   item is a dead `#` link with no page behind it. That absence is itself worth
   knowing. If this ships, it may be the first of its kind in the country, which
   raises rather than lowers the bar on the provenance rules.
4. Cloudflare Pages' HTTP Range support is **not confirmed**. My test URLs
   returned `200` from a transforming layer rather than `206`, which proves
   nothing either way. If PMTiles is ever revisited, test it against a real
   deployment first. GitHub Pages is confirmed (`206`, `Accept-Ranges: bytes`).
