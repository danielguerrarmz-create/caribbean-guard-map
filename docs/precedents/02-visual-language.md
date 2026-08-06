# 02. Visual language precedent research

Owner: Sai (design). Method: WebFetch against the live site, not memory or brand
decks. Where WebFetch's HTML-to-markdown conversion strips the information a
question needs (this happened to every hex value and every font-family name
across every site attempted, without exception, including sites that clearly
have a designed identity) that is stated as **unverifiable**, not guessed. No
hex value or typeface name in this document was invented; where I could not
read it off the fetched content it is not listed.

19 sites were attempted. 13 returned enough real content to analyse. 6 were
blocked or dead ends, listed at the end because that is itself a finding.

---

## The three that fit Caribbean Guard best

**1. Costa Ballena Lifeguards** (`lifeguardscostaballena.com`) is the single
closest precedent in existence: a small volunteer lifeguard NGO on Costa
Rica's Pacific coast, same country, same function, same funding model. It
opens with the risk stated plainly ("lives at risk," "fatal in seconds") and
immediately answers it with a real, checkable number ("0 on-duty drownings"),
which is structurally the same move Caribbean Guard's own draft homepage copy
already makes ("Desde 2021 nunca murió nadie durante nuestras guardias"). It
is also the only precedent site built the way this project's own site is
built: a static site generator (Astro), WebP/AVIF imagery, no framework
bloat. If Caribbean Guard wants proof that the boring, fast, undecorated
approach is also the credible one in this exact category, this is the
organisation to point to.

**2. Santa Teresa Lifeguards** (`santateresalifeguards.org`) is the second
volunteer lifeguard NGO on the same coast of the same country, and it is the
precedent for two things Caribbean Guard should copy directly: a bilingual
toggle aimed at both the local community and the international volunteers who
fund and staff these organisations, and a single reusable educational
diagram (a rip current illustration, not a photo) sitting alongside the real
photography rather than replacing it. Its footer credits its designers by
name, a small, correct choice for a volunteer organisation.

**3. WIDECAST** (`widecast.org`) is the weakest in production values of the
three and the most useful for tone. It is a Caribbean-wide volunteer research
network, and its imagery is unglamorous field documentation, researchers and
turtles in real habitat, not a hero shoot. Its copy is invitational rather
than alarmist ("Please join the conversation!") even though its subject
matter is genuinely at-risk species. For a safety organisation that has
already committed, correctly, to never overclaiming currency or authority it
does not have, WIDECAST is proof that calm and credible are not the same as
polished, and that under-producing the imagery does not read as amateurish
when the subject matter itself is doing the work.

---

## Method note, stated once because it applies to every entry below

WebFetch converts the fetched page to markdown before an analysis pass runs
over it. That step reliably discards `<style>` blocks, `<link>` tags to font
services, and inline colour values. It reliably keeps image filenames, alt
text, navigation labels, headings, and body copy. The practical effect: this
research can say with confidence what every site photographs and how it talks
about itself, and cannot respond with confidence on what typeface or exact
hex any of them use, no matter how design-forward the organisation. That
asymmetry turned into a finding in its own right, see the proposals section.

---

## The 13 sites with real findings

### Costa Ballena Lifeguards — `lifeguardscostaballena.com`
Costa Rica, Pacific coast, volunteer lifeguards. **Typography/colour:**
unverifiable via this method; the fetched content references named supporter
tiers ("Blue," "Red," "Black," "Silver," "Gold") implying those colours carry
meaning in the design, but no hex was exposed. **Imagery:** real operational
photography only, filenames read like a shot log: `domi-tower-inauguration`,
`lifeguard-testing-day`, `Volunteer.CxCrHijh.jpg`, `JuniorLifeguard`,
`CommunityOutreach`. No stock. **Structure:** problem statement, then proof
(preventions, rescues, "0 on-duty drownings"), then transparency, then three
programme pillars, then numbered support tiers (01 to 06), then an active
campaign. **Register:** crisis-then-capability, professional but human, not
alarmist. **Weight:** WebP/AVIF, static site generator (Astro), no framework
signature, reads as built for a slow connection. **Language:** ES with an
EN toggle, aimed at local trust and international donors/volunteers at once.

### Santa Teresa Lifeguards — `santateresalifeguards.org`
Costa Rica, Pacific coast, volunteer lifeguards. **Imagery:** documentary
photography (a lifeguard in action, a person with a surfboard, beach scenes)
plus one educational illustration, a rip current diagram, used deliberately
alongside the photography rather than instead of it. **Structure:** hero is a
literal service statement, "24/7 SURFER RESCUE," then About, Volunteer
Program, Programs, Tips, Gym, News, Store, Donate. **Motifs:** minimalist SVG
icons for rescue/prevention/first aid/flags, simple stat blocks for annual
impact. **Register:** community-driven, urgent in the specific sense of
naming the service ("safer beaches") without theatrics. **Language:** EN/ES
toggle, footer credits the site's designers by name. **Weight:** unverifiable
precisely, WebP in use.

### WIDECAST — `widecast.org`
Caribbean-wide, sea turtle research/volunteer network. **Imagery:** six real
photographs, researchers and turtles in habitat, hatchlings, underwater work,
no stock, no polish. **Structure:** nine-item nav (About, Network, Biology,
Management, Conservation, Medicine, Ecotourism, Library, Support), a centred
welcome hero, mission statement, stakeholder framing. **Register:**
invitational and evidence-based rather than urgent, "Please join the
conversation!" next to genuinely endangered-species content. **Weight/lang:**
unverifiable, English primary.

### Sea Turtle Conservancy — `conserveturtles.org`
US-headquartered, major Caribbean-coast Costa Rica programme (Tortuguero,
the same coast Caribbean Guard patrols further south). **Imagery:** real,
photo-credited (Ralph Pace, Ben Hicks, Celeste McWilliams named), individual
tagged turtles given names as a device (Krysta, Fin Diesel), volunteers doing
field work. **Motifs:** satellite migration maps as a recurring graphic,
numeric stat callouts (8 countries, 550 turtles tagged, 1,200 researchers
trained). **Structure:** mission, four impact areas, a live tracking tool,
news, shop, IRS Form 990 and audit linked in the footer, a real transparency
signal. **Register:** shifts from scientific to conversational by section,
participation-focused ("adopt," "track," "join"). This is the most
resourced org in the set and still leans entirely on real photography and
named credit rather than illustration or a heavier visual system.

### Osa Conservation — `osaconservation.org`
Costa Rica, Osa Peninsula, conservation nonprofit. **Colour:** the only site
in the set where a hex value, `#ffffff`, was directly visible, plus a logo
file literally named `OSA-Logo-Green.png` (the actual green hex was not
exposed). **Imagery:** documentary field photography, aerial ridge-to-reef
landscape shots, team and community members in action. **Motifs:** a map
visualisation of the region, quantified impact metrics (145,650 hatchlings
released) stated prominently. **Structure:** Home, About, Our Impact, Media &
Resources, Visit Us, Donate, with an EN/ES language toggle. **Register:**
optimistic and science-backed, names the threat (rapid climate change) then
pivots to agency.

### The Ocean Cleanup — `theoceancleanup.com`
International, very well funded, the ceiling reference in this set.
**Imagery:** operational documentation only, vessels, river interceptor
barriers, drone footage, located and dated (Guatemala, Malaysia, Jamaica,
Thailand, Indonesia). No 3D renders despite the budget this org clearly has,
which is itself worth noting: even at the top of the category, credibility
is built on real documentation, not illustration. **Structure:** mega-menu,
"Join the largest cleanup in history," before/after quantification
throughout, corporate partner logos (Kia, Deloitte), a dense news archive.
**Register:** professional, urgency stated in numbers ("90% by 2040") rather
than adjectives. **Weight:** the heaviest site in the set by a wide margin,
multiple embedded videos, dense imagery, production-grade rather than
minimal. This is the useful negative case: it is the org with the biggest
budget and the least resemblance to what a 30 KB, one-bar-of-signal safety
page needs to be.

### Reef Check — `reefcheck.org`
International, volunteer diver network. **Imagery:** real divers doing
surveys, named species photography, no stock aesthetic. **Motifs:** one
stylised angelfish graphic as the sole illustration, used as a hero accent
rather than a substitute for photography; marine-creature illustrations used
specifically as content breaks between real photo sections, a useful pattern
if Caribbean Guard ever wants a small graphic device between photo-heavy
sections without pretending it is a photograph. **Structure:** three-part
programme carousel, species database, stats, news. **Register:**
participatory, "We're a team!"

### ISLA — `islasurf.org`
International volunteer lifeguard placement network operating in Costa Rica,
Mexico, Nicaragua, India. **The negative case for imagery in this category.**
Every image referenced in the fetched content was illustrated or a logo:
abstract figures representing people, sponsor logos, no actual photograph of
a lifeguard, a rescue, or water. For an organisation whose entire value
proposition is "real people do real rescues," leaning on symbolic
illustration instead of documentation is a legible credibility gap, visible
even from a text-only fetch. **Structure:** "We are WATER PEOPLE /
LIFEGUARDS / GLOBETROTTERS / ACTIVISTS," featured-operation cards by country
and date. **Register:** inspirational, global-scale.

### Surf Life Saving New Zealand — `surflifesaving.org.nz`
National federation, professional/volunteer hybrid. **Imagery:** mostly
organisational (logos, partner logos, one unlabelled campaign photo); no red
and yellow flag or rescue-equipment imagery surfaced in the fetched content,
which may be an artefact of the method rather than the actual site, flagged
as such rather than stated as fact. **Motifs:** a hard stat block (285,960
patrol hours, 4,633 lifeguards, 624 lives saved, 304 searches), the largest
and most specific numeric claim in the whole set. **Register:** authoritative
("can be the difference between life and death") balanced against
"incredible community." **This is the precedent for the stat-row proposal
below**, done at a scale Caribbean Guard cannot and should not try to match,
but the pattern, name the real number, keep it small and factual, transfers
at any scale.

### Ocean Conservancy — `oceanconservancy.org`
International, large. **Imagery:** real wildlife and volunteer photography
(a sea lion with a disposable glove, a named "Team Ocean Captain"), video
background on the hero. **Motifs:** stat callouts (53 years, 400M pounds of
trash, 19M volunteers), a corporate-partner logo grid. **Structure:** hero
video, Spotlight, Our Work (three pillars), News, Get Involved. **Register:**
community-focused with real urgency on plastics and climate, not
fear-driven. **Weight:** a video-background hero is a direct counter-example
to Caribbean Guard's own finding that the live Squarespace site's biggest
single defect is an unrequested autoplaying video; noted as what not to do,
not what to copy.

### Surfrider Foundation — `surfrider.org`
International with grassroots local chapters (200+), the organisational
model closest to Caribbean Guard's own chapter-of-volunteers structure even
though the org itself is far larger. **Imagery:** documentary/activist
photography (an oil-drilling campaign image, a beach cleanup with real
volunteers) plus five stylised initiative icons. **Structure:** Learn / Get
Involved / Give / Shop, a chapter locator, impact metrics (200 chapters,
930+ victories, 185K volunteer hours), a merchandise shop. **Register:**
activist urgency paired with community optimism, threat and hope imagery
side by side.

### Asociación ANAI — `anaicostarica.org`
Costa Rica, Gandoca-Manzanillo, the same stretch of coast Caribbean Guard
patrols. **The fetched content exposed almost no imagery**, one logo file
and nothing else, which most likely reflects the homepage's structure rather
than an absence of photography on the site as a whole; flagged as
unverified rather than treated as a finding about the org's actual
photography. **Structure:** deep nav (About, Coastal Lowland Initiative,
Stream Bio-monitoring, Talamanca Initiative, Beyond Talamanca, Donate), hero
states "50 years" of work. **Register:** legacy-focused ("our grandchildren's
grandchildren"), copyright footer reads 2020, plausibly a site that has not
been redesigned recently. Worth a second, deeper fetch later given the
geographic overlap, but not worth stalling this document on.

### Latin American Sea Turtles / LAST — `latinamericanseaturtles.com`
Costa Rica, formerly WIDECAST-Costa Rica. **Note:** the domain
`latinamericanseaturtles.org` (no `.com`) has been taken over and now serves
unrelated Korean-language gambling content; this is a live squatted-domain
risk worth naming to Caribbean Guard for their own domain hygiene, not a
design finding. The correct `.com` domain returned mostly partner/validation
badges (GlobalGiving, CAF International) and a dense footer of 40+ affiliate
links; volunteer-recruitment framing ("Be part of the change, join the team,
volunteer today!"). Real imagery content was not exposed by this fetch.

---

## Attempted and not usable, listed because it is itself a finding

| Site | Result |
|---|---|
| `rnli.org` (RNLI, UK) | HTTP 403, bot-blocked |
| `sls.com.au` (Surf Life Saving Australia) | HTTP 403, bot-blocked |
| `worldwildlife.org` (WWF Oceans) | HTTP 403, bot-blocked |
| `cruzroja.or.cr` (Cruz Roja Costarricense) | Fetched empty, no usable content returned |
| `marviva.net` | HTTP 403, bot-blocked |
| `usla.org` (US Lifesaving Association) | HTTP 403, bot-blocked |
| `pretoma.org` | Site is a placeholder, "an amazing site is coming to this web address" |
| `latinamericanseaturtles.org` | Domain squatted, serves Korean-language gambling content, unrelated to the org |

Pattern worth naming: every blocked site is a larger, more institutional
organisation (a UK royal charity, a national federation, WWF, a US
professional association). Every site that returned real content is either a
small volunteer org or a mid-size one running on a simpler stack. That is
mild evidence, not proof, but it lines up with the rest of this research:
the organisations Caribbean Guard most resembles are also the ones easiest
to actually study.

---

## Applying this to Caribbean Guard

### What the current system already gets right, confirmed rather than changed

`tools/build_site.py` and `site/assets/site.css` already implement almost
everything this research would otherwise recommend: real photography
reserved rather than faked (11 SVG placeholders stating what belongs in each
frame), one signal colour used functionally only, a two-tier safety colour
system with real contrast math already solved in `02-visual-system.md`, a
30 KB / 3-request homepage, 44px tap targets, 16px form inputs. Nothing here
argues for touching that. The strongest confirmation from this research is
negative: not one of the 13 sites studied, including The Ocean Cleanup at
the top of the category's budget range, invests in a bespoke typographic
identity that a fetch can even detect. This category wins on the credibility
of its photography and the clarity of its numbers, not on type. Caribbean
Guard's Poppins-plus-system-stack pairing, already shipped, is not
underdressed for this category; it is exactly matched to what the category
actually spends its effort on.

### Three highest-impact changes for the mobile homepage

**1. Photograph operations, not portraits, first.** Every lifeguard-specific
precedent (Costa Ballena, Santa Teresa) and every marine precedent (Reef
Check, Sea Turtle Conservancy, WIDECAST) builds credibility from people
doing the work in frame: a tower inauguration, a gear-testing day, a
researcher's hands on a turtle, a diver mid-survey. ISLA is the visible
counter-example: an org whose entire premise is real people doing rescues,
relying on illustrated figures instead, and it reads thinner for it even
from a text-only fetch. Caribbean Guard's own shot list
(`tools/make_placeholders.py`) already asks for "entrada al agua con tabla
o tubo de rescate" for `lifesaving` and "banderas... con la zona segura
detrás" for `playa-organizada`, which is the right instinct. Sharpen it
further: add one shot per club showing equipment or a real drill in use
(a rescue board entry, a buoy line being set, a freediving safety check),
not just the wide establishing shot the current briefs describe. For
`equipo`, keep the square portrait brief but add two or three candid
operational photos to the lifesaving-club and involúcrate pages
specifically, so the team is documented working, not only named.

**2. Add one honest, small stat row under the hero, once AJ supplies real
numbers.** This is the single most consistent motif across every precedent
that returned content, from Surf Life Saving New Zealand's 285,960 patrol
hours down to Costa Ballena's "0 on-duty drownings," and it is the one
thing every precedent has that Caribbean Guard's current homepage does not.
The homepage already states the qualitative version ("Desde 2021 nunca
murió nadie durante nuestras guardias"); the missing piece is three or four
compact numbers next to it, years active, number of active volunteers,
beaches patrolled, people trained. Every number must be one Caribbean Guard
can actually stand behind, per the standing rule that this interface may
never claim more currency or authority than its data has; this is a request
to AJ, not a number to invent here. Visually this is cheap: a `dl.facts`
row already exists in `site.css`, reused at larger type, sitting between the
hero and the map card.

**3. Do not add a graphic motif; if one is ever wanted, it is a diagram, not
a decoration.** The one recurring non-photographic device that earns its
place across these precedents is the single-purpose educational diagram,
Santa Teresa's rip current illustration, Reef Check's between-section
creature graphic used sparingly. If Caribbean Guard ever wants a visual
device beyond photography, the correct application is a small, reusable
"how to spot a rip current" line diagram on the `/mapa` education section,
matching the shape language the status system already uses (solid/dashed/
dotted), not a decorative wave or buoy motif on the homepage. This is
explicitly not a stat-badge, icon-set, or hero illustration proposal; the
research does not support adding decoration where none exists today, and
Daniel's standing rule against decorative marks ahead of text applies with
or without the colour being blue.

### On the 30 KB budget

Argued for, not against, with one addition. The HTML+CSS budget should stay
where it is; nothing in this research suggests spending more of it on
typography or layout complexity. Photography is the one place weight will
legitimately grow once real images replace the placeholders, and the
precedent to follow there is Costa Ballena Lifeguards specifically: WebP/AVIF,
no framework, static output. Applying the house ratios already specified in
`02-visual-system.md` (16:9 hero, 4:5 card) at the same delivery discipline
`03-image-register.md` already recommends for the hazard maps (quality 82,
re-encoded, not the raw camera file) should keep a filled-in hero photo
around 80 to 120 KB, in the same order of magnitude as the map's own 63 KB
overview image, not the 250+ KB the live Squarespace hero currently wastes
on an oversized `sizes` value.
