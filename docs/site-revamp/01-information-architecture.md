# Caribbean Guard: information architecture

## Top three findings

1. **The site cannot currently answer the one question that matters most.** No
   destination in the nine-item nav tells a tourist "is it safe to swim where I am
   standing." The closest content, `/programa-playa-organizada`, describes the
   *program* (flag zones, rescue stations, courses) rather than live status, and it
   sits behind a label a first-time visitor has no reason to open. The safety map
   is not a feature to bolt onto this structure; it is the thing the structure is
   missing.
2. **Five of eleven live pages share the literal, unedited browser tab title
   "Services 4 — Caribbean Guard."** `/proyectos`, `/programa-playa-organizada`,
   `/freediving-club`, `/lifesaving-club`, and `/swim-club` all carry this default
   Squarespace title (confirmed via each page's `<title>` tag). A sixth,
   `/nuestro-trabajo`, carries the unedited "Services — Caribbean Guard." This is
   what shows in a browser tab, a shared link preview, and a bookmark. It is a
   five-minute Squarespace fix with an outsized payoff.
3. **`/nuestro-trabajo`, `/proyectos`, and `/programa-playa-organizada` are not
   the same page wearing different hats.** They read that way from the nav labels
   alone, but the content is genuinely distinct: `/nuestro-trabajo` is the founding
   history, `/proyectos` is a funding wishlist (warehouse, mobile guard, aquatic
   center), and `/programa-playa-organizada` is the live operational safety program
   (zones, rescue stations, courses) that the new map is a digital extension of.
   The problem is not duplication, it is that none of the three names say what the
   page actually contains.

## 1. Page inventory

All eleven documented URLs, plus the two confirmed 404s.

| URL | H1 on page | What it's genuinely for | Audience | Content volume | Earns its place? |
|---|---|---|---|---|---|
| `/` | "Caribbean Guard: Salvando Vidas" | Hero + embedded mission teaser + an embedded "Programa Playa Organizada" section (h3, not its own page reference) | Everyone, first stop | Medium: hero, mission block, one program teaser, ~17 images | Yes, but it already half-agrees with me: it teases the safety program before the nav even offers a real path to it. |
| `/vision` | "VISION" (decorative scrolling marquee text, not a real headline) | A public-policy argument: who should fund and run water safety in Costa Rica (a "law of thirds": community, businesses, government), tied to Law 9780 | Government contacts, press, partners, not tourists | Thin: one real paragraph block plus a policy-ask list, 1 image | Contentwise yes, this is a distinct advocacy stance the home page's mission blurb doesn't cover. As a flat top-level tab, no: almost nobody in the four personas needs this in one tap. |
| `/team` | none found (page opens straight into a photo grid) | 17 names with photos and **no visible role or bio** attached, followed by a separate 17-item accordion, same 17 names, that **does** contain role + full biography | Community, donors doing diligence, press | Substantial (17 photos + 17 real bios) but split into two disconnected blocks a visitor has to cross-reference by name | The content earns its place; the page structure hides most of it. Worth flagging to Sai: attach the bio to the card. |
| `/nuestro-trabajo` (nav label: "Historia") | "Quien salva una vida, salva al mundo entero." (a quote, not a description of what the page is) | The founding history: March 2021 origin, founder names, partnership with Swim Safe Costa Rica, 400+ trained, zero fatalities on watch | Donors, press, community wanting the origin story | Medium: one substantial narrative block, 3 images | Yes. Real, specific, unique content. The nav label ("Historia") and the URL slug (`nuestro-trabajo`, "our work") disagree with each other, which is a smaller but real problem. |
| `/proyectos` | none found | A funding wishlist, three named capital needs with real descriptions each: Bodega Digna (equipment warehouse, explicitly "priority #1"), Programa Guardia Móvil (mobile patrol), Centro Acuático de Alto Rendimiento (aspirational aquatic center) | Donors and sponsors deciding where money goes | Medium: 3 substantial description blocks, 3 images | Yes, this is the donor-facing "what we still need" page and nothing else on the site covers it. It is mislabeled: "Proyectos" reads like a portfolio, not a wishlist. |
| `/programa-playa-organizada` | "PROGRAMA PLAYA ORGANIZADA" (h3, no h1) | The live operational safety program: red/yellow flagged safe-swim zones, rescue lines, a drone-shot zone map with local partners marked, fixed rescue stations restocked daily, an emergency plan, and the lifeguard/CPR/first-aid course | Tourists (should be, isn't yet), locals, partner businesses | Substantial: 7 real sub-sections, 8 images. Per Edward's asset audit, this is the **heaviest page on the site** (2.9 MB, 67.3s to load on Slow 3G): the "map" under "Mapeo de la zona" is a static image (`Annotated Base Map V5.png`, 1,482 KB) uploaded **twice** as separate assets, rendered at 3950x1600 into a 390px viewport, unreadable on the device this content is for. | Yes for the program content, unchanged. No for the map: what's there today is a static, duplicated, illegible-on-mobile image standing in for a safety tool. Revised my recommendation below after seeing this. |
| `/lifesaving-club` | "LIFESAVING CLUB" | The core volunteer lifeguard unit: continuing education, beach watches ("Guardias"), rescue training, emergency alert network | Prospective lifeguard volunteers, community | Largest page on the site, 4 sub-sections, 5 images | Yes, clear and distinct from the other two clubs. |
| `/swim-club` | "SWIM CLUB" | Free open-water and pool swim training for the community, plus a children's Swim School; includes a real weekly schedule (Punta Uva Thu 7:15am, Playa Negra Tue/Fri 4pm) | Local parents and adults wanting to learn or improve swimming | Medium: one solid paragraph block with concrete times, 4 images | Yes. This is the page today that most cleanly answers a real question in one click, and it should stay that easy to reach. |
| `/freediving-club` | none (h3 "FREEDIVING CLUB", one heading level below the other two clubs' h1) | The newest, least developed unit: apnea/spearfishing tradition on the coast, stated intent to build courses, workshops, competitions | Local free-divers, spearfishers | Thin: one short paragraph, no schedule, no concrete offering yet, 4 images | Marginal today, honestly. It reads as "coming soon." Keep it (real community tradition, real intent) but don't pretend it's as developed as the other two clubs. |
| `/involcrate` (URL misspelling is live and must stay) | "INVOLÚCRATE" (h2, no h1) | Two different jobs on one page: (a) how to join as a volunteer or business, routed by swim skill, and (b) "Contáctanos": Instagram, site, email, and **the emergency phone number** | Prospective volunteers/partners (a); anyone needing to reach the org, including in an emergency (b) | Thin-medium: one paragraph block for joining, one small block for contact, 6 images | The volunteer content earns its place. Bundling the emergency phone number into this specific low-traffic page is a genuine safety problem: nobody in an emergency thinks to check "Get Involved." |
| `/donar` | none found (first heading is h3 "¿Por Qué Donar a Caribbean Guard?") | Direct-donation mechanics: bank account (CRC and USD), PayPal, SINPE Móvil | Donors ready to give right now | Thin but complete: it's a reference block, doesn't need to be long, 1 image | Yes, and it already has a persistent header CTA ("Donar ahora"), which is correct. No change needed to how it's reached. |
| `/nosotros` | — | **404.** Confirmed: renders the standard Squarespace "No pudimos encontrar la página que buscabas" page. | — | — | Currently a dead link, live in the footer. |
| `/unete` | — | **404.** Confirmed, same Squarespace not-found template. | — | — | Currently a dead link, live in the footer, target="_new" even though it goes nowhere. |

**Nav inventory, for the record.** The header nav (identical on desktop and the
mobile duplicate at a second breakpoint) currently lists nine items in this order:
Lifesaving Club, Swim Club, Freediving Club, Programa Playa Organizada, Proyectos,
Historia (→ `/nuestro-trabajo`), Team, Involúcrate, Vision. A tenth destination,
"Donar ahora," is a persistent CTA button, not a nav item. The footer separately
links four destinations in two text blocks: Únete (→ `/unete`, 404), Nuestro
Trabajo, Nosotros (→ `/nosotros`, 404), Donar. Two of those four footer links are
dead. That is where the brief's "at least ten destinations" comes from, and it
undercounts if you include the footer.

## 2. Overlap analysis

**`/nuestro-trabajo`, `/proyectos`, and `/programa-playa-organizada` are three
distinct pages, not one page in three costumes.** Confirmed by reading each:

- `/nuestro-trabajo` = history. Past tense. "In March 2021, Lucas Iturriza
  invited Joel Gagg..." Founders, timeline, partnership credit, achievement stats.
- `/proyectos` = wishlist. Future tense, capital needs. "One of our biggest needs
  is a safe, dry space for our equipment... it is the association's #1 priority."
- `/programa-playa-organizada` = present tense, operational. "Zona segura de
  bañado... delimited by two flags." "Mapeo de la zona, by drone." "Fixed
  structures on the beach with rescue floatation equipment."

None of these three is redundant with either of the other two. The confusion is
entirely nomenclature: "Nuestro Trabajo" (our work), "Proyectos" (projects), and
"Programa Playa Organizada" (organized beach program) are three names that all
plausibly mean "stuff we do," so a first-time visitor has no way to predict which
one has what. The fix is renaming and regrouping, not deleting.

**The three club pages are genuinely distinct programs, not duplicates**, each
with a different join funnel, and two of the three (Lifesaving, Swim) have concrete
schedules or requirements attached. Freediving is real but thin: it is the one
page on the site that is closer to "we intend to build this" than "here is the
program." That's a content-maturity gap, not a structural one, and it does not
justify merging it into another club: the community activity (freediving/apnea) is
distinct enough that folding it into Swim Club would misrepresent both.

**`/vision` and the home page's "Nuestra misión" section do overlap, partially.**
Home's mission block is a compressed restatement of mission, vision, and
objectives. `/vision` is the fuller policy argument (the "law of thirds," the Law
9780 ask). They are not identical, but a visitor who reads the home block has
already gotten 70% of what `/vision` says. `/vision` earns a subordinate spot
(inside an About grouping) rather than a flat top-level tab competing for the same
attention as the mission blurb already on the page everyone lands on first.

**`/team`'s two blocks (photo grid, bio accordion) are not overlap, they're a
split.** Same 17 people, same names, but one block has faces and no roles, the
other has roles and bios and no faces, and nothing connects them for a visitor
except matching the name by eye. This isn't an IA question so much as a
component fix, flagged here because it changes how much the page "earns its
place" and is worth a note to Sai.

## 3. The proposed structure

**Seven items in the header-nav-list, down from nine, plus the existing Donar
CTA left untouched, plus two dead links resolved.** (Inicio isn't counted on
either side: it's the logo/root, not one of the nine items in
`<nav class="header-nav-list">` today, and it stays that way. It's in the table
below only to show the full left-to-right bar.) Not five, not three: the map,
the beach-safety program page, and the three clubs each need one-tap reach
because they're where the four personas below actually transact (check safety,
check a class schedule, join a club). Everything else is credibility content
that supports a decision but isn't itself the destination anyone is trying to
reach in a hurry, so it collapses into one grouping.

**Revised after Edward's asset audit.** My first pass at this table merged the
map directly into `/programa-playa-organizada`, on the theory that they're the
same subject (still true, see section 5). Edward then measured that page at
2.9 MB, 67.3s to load on Slow 3G, the heaviest page on the site, with the
current "map" being a static PNG uploaded twice and unreadable on a phone.
Stacking a live interactive map onto the heaviest page on the site, under a
label a first-time tourist won't parse as "the map," is the wrong call. The map
now gets its own row: a new, minimal, fast-loading destination, first in the
bar. `/programa-playa-organizada` keeps its own slot right after it, scope
unchanged, with the duplicate PNG removed and a link card to the map added at
the top.

| # | Nav label | URL | Contains | What merges in | Redirect needed |
|---|---|---|---|---|---|
| — | Inicio | `/` (unchanged) | Hero, mission teaser, safety-map teaser | — | No |
| 1 | Mapa de Seguridad | New, e.g. `/mapa` (exact URL and embed method are Edward's call, see `04-map-integration.md`) | Nothing but the live map: a minimal page whose only job is to load fast and show status | New destination, not a merge | No, additive; nothing currently links here |
| 2 | Programa Playa Organizada | `/programa-playa-organizada` (unchanged) | The existing 7 program sub-sections (zones, rescue line, zone map, local partners, rescue stations, emergency plan, course), duplicate PNG asset removed, a "Ver el mapa en vivo" card added at the top | Nothing merges in; content unchanged, one duplicate asset removed | No, URL unchanged |
| 3 | Lifesaving Club | `/lifesaving-club` (unchanged) | Unchanged | — | No |
| 4 | Swim Club | `/swim-club` (unchanged) | Unchanged | — | No |
| 5 | Freediving Club | `/freediving-club` (unchanged) | Unchanged | — | No |
| 6 | Nosotros | `/nosotros` (currently 404, becomes real) | A short hub landing (who we are, one paragraph) linking to three or four children: Historia (`/nuestro-trabajo`), Visión (`/vision`), Equipo (`/team`), Proyectos (`/proyectos`) | Vision, Team, Historia, Proyectos all move from flat top-level items into this one grouping. **No URLs change** for any of the four; only their nav position does. | No new redirect: `/nosotros` stops being a dead link because real content now lives at the URL the footer already points to. |
| 7 | Involúcrate | `/involcrate` (unchanged, misspelling stays live) | Volunteer/join content only. Recommend moving "Contáctanos" (Instagram, email, and especially the emergency phone number) off this page into the site-wide footer, which already exists on every page. | — | No |
| CTA | Donar ahora | `/donar` (unchanged) | Unchanged | — | No |

**Two dead links resolved, zero net-new redirects beyond one:**

- `/nosotros`: stops 404ing because it becomes the real "Nosotros" hub described
  above. This is not a redirect, it's building the page the footer already
  promised.
- `/unete`: 301 redirect to `/involcrate`. "Únete" (join) and "Involúcrate" (get
  involved) are synonyms; there's no reason to keep them as separate concepts, and
  Squarespace's URL Mappings under Settings → Advanced handles this in one line.

Edward independently confirmed `/nosotros` and `/unete` are byte-identical
files, both rendering Squarespace's generic not-found page: the nav doesn't
point at two different dead pages, it points at the same dead page twice, under
two different labels. That doesn't change the fix, each URL still needs its own
resolution, it just confirms neither was ever real content to begin with.

**What this doesn't do:** it doesn't touch a single existing club, donate, or
program URL. The only redirect in this whole plan is one line
(`/unete` → `/involcrate`). Anything printed (a QR sticker, a business card) that
currently points at `/lifesaving-club`, `/swim-club`, `/freediving-club`,
`/donar`, `/involcrate`, or `/programa-playa-organizada` keeps working with zero
changes. The new map destination is additive: nothing currently links to it, so
there is nothing to break.

**What is lost, stated plainly:** Vision, Team, Historia, and Proyectos drop from
flat, always-visible top-level items to children of a "Nosotros" folder. On
Squarespace's mobile nav, opening a folder is usually one extra tap before you can
pick a child, so reaching, say, `/team` goes from 1 tap to 2. I judged this
acceptable because none of the four personas below need any of those four pages
in the first two clicks; they're pages people read after they've already decided
to care, not pages that decide anything by themselves. If Daniel or AJ disagree
that this loss is acceptable for a specific one of the four (Proyectos is the most
arguable, since a donor might want it fast), the fix is cheap: pull that one page
back out to flat top-level and leave the rest grouped.

## 4. First-visit paths

Counting taps from `/` (home). "1 click" means one nav or CTA tap gets you a
usable answer, not just a landing page.

| Persona | Today | Clicks today | Proposed | Clicks proposed |
|---|---|---|---|---|
| Tourist: "is it safe to swim here?" | No page answers this. Closest is opening "Programa Playa Organizada" from the nav, which describes the program, not live status. There is currently no status to find. | Unanswerable | Home → tap "Mapa de Seguridad" → tap their beach card in the picker | **2**. (For the QR-scanning case specifically, the QR deep-links straight to the standalone map per the existing handoff, so it's effectively 0 taps after the scan, independent of site nav entirely.) |
| Local parent: swim club for their kid | Home → tap "Swim Club" → schedule is on the page | **1** | Home → tap "Swim Club" (still flat top-level, unchanged) → schedule is on the page | **1**, unchanged. This is exactly why Swim Club (and the other two clubs) stay flat instead of folding into a dropdown. |
| Potential donor | Home → tap "Donar ahora" CTA → bank details page. (If they first want to see what their money builds, that's a second, unconnected trip to find "Proyectos" in the flat nav.) | **1** to give, **1** separately to see impact (but the two aren't linked to each other) | Home → tap "Donar ahora" CTA → bank details page, unchanged. Recommend adding a short "here's what your donation builds" block on `/donar` linking to Proyectos (a content change, not a nav change). | **1** to give, unchanged. Seeing impact first becomes Nosotros → Proyectos, **2**. |
| Would-be volunteer | Home → tap "Involúcrate" → join info on the page | **1** | Home → tap "Involúcrate" (unchanged, flat top-level) → join info, with Contáctanos content moved to the footer instead of sharing this page | **1**, unchanged |

Every persona is at or under two clicks under the proposed structure. Two of the
four (parent, volunteer) were already at one click today and stay there; the
donor's core action was already at one click and stays there. The one persona
that mattered most and had **no path at all** today (the tourist) now has a path
in two.

## 5. Where the safety map sits

**Revised from my first draft.** I originally argued for embedding the map
directly into `/programa-playa-organizada` rather than a separate URL, on the
grounds that the content is already the same subject (still true, see the
overlap analysis in section 2). Edward's asset audit changed the call: that
page is currently the heaviest on the site, 2.9 MB and 67.3s to load on Slow
3G, and the "map" already living there is a static, duplicated, illegible PNG.
Loading a real interactive map on top of that, on a mobile-first safety tool,
is the wrong trade. The map needs its own destination:

1. **It needs to be light, and `/programa-playa-organizada` currently isn't.**
   A minimal new page whose only job is to load fast and show status protects
   the map from inheriting that page's weight, and gives whoever builds it a
   clean slate rather than a cleanup job to do first.
2. **The content overlap argument still holds, it just doesn't mean "same
   URL."** `/programa-playa-organizada` already describes, in its own words,
   drone-mapped zone boundaries ("Mapeo de la zona, con dron... límites claros
   del área total"), fixed rescue stations with equipment lists ("Estaciones de
   Salvamento... tubos y torpedos de rescate, caja de mecate, salvavidas,
   chaleco y silbato"), and flag-delimited safe zones ("Zona segura de bañado,
   se delimita con dos banderas"). The map is the digital version of that
   content, so the two pages belong **adjacent** in the nav bar and should
   cross-link (a "Ver el mapa en vivo" card at the top of
   `/programa-playa-organizada`, a "Cómo funciona el programa" link from the
   map page), but adjacency solves the overlap problem without forcing the new
   tool to carry the old page's weight.
3. **The map does not depend on nav placement for its hardest case.** Per the
   existing map handoff, QR codes deep-link straight to the standalone map, not
   through the Squarespace site at all. That means nav placement doesn't affect
   the barefoot-on-the-sand scenario: the map's own hosting solves that. What
   nav placement *does* affect is the second most important case: a tourist
   checking conditions from a hotel room before walking down, or a local
   checking before their kid's swim class. For that case, one tap from the nav,
   first in the bar, not buried under "Nosotros" or a program name a
   first-time visitor won't parse as "the map," is the right bar.

I'd defer the exact URL and embed mechanism (a Squarespace Code Block iframing
the standalone Leaflet map vs. an external link straight to the standalone host)
to Edward's `04-map-integration.md`, since that's a hosting and performance call,
not an IA one. The IA requirement is just: its own top-level slot, first
position, minimal page weight, adjacent to (and cross-linked with)
`/programa-playa-organizada` rather than merged into it.

**Link card copy, for the top of `/programa-playa-organizada`. Revised.** My
first draft said "en tiempo real" / "real-time" and "marcado por nuestros
guardavidas" / "marked by our lifeguards." Both are false today: the map has no
live-update mechanism, statuses are static values in a file with no expiry, and
every zone/hazard reading in it is placeholder prose written from general
knowledge, not something Caribbean Guard's guards have signed off on. Claiming
"real-time" and "by our lifeguards" would tell a tourist to trust a reading that
could be stale or unverified, which is worse than the static PNG it replaces:
the PNG never claimed to be current. Corrected, on the team lead's flag:

Spanish:
> **Mapa de Seguridad**
> Dónde se puede nadar en esta costa, playa por playa. Ábrelo en el teléfono
> antes de entrar al mar.
> Revisado por última vez: [fecha] / Sin revisar aún
> Button: **Abrir el mapa**

English:
> **Safety Map**
> Where you can swim on this coast, beach by beach. Open it on your phone
> before you go in.
> Last reviewed: [date] / Not yet reviewed
> Button: **Open the map**

"Playa por playa" / "beach by beach" carries the "this is a tool, not one
picture" signal without asserting anything false, and "antes de entrar al mar" /
"before you go in" establishes it as something checked repeatedly, both without
a currency claim the artifact can't back up. The review-date line is built in
rather than retrofitted: if the honest answer at launch is that no beach has
been reviewed yet, it should say "Sin revisar aún" / "Not yet reviewed" rather
than imply verification that hasn't happened. Final wording is Erwin/Shikamaru's
call on tone; the constraint that shouldn't move is not claiming real-time or
attributing content to guards until `06-accessibility-and-safety.md`'s open
items (author, date, staleness default per reading) are closed.

## Needs confirmation from AJ

- Whether Squarespace's plan on this account is Business or above (required for
  the Code Block that will embed the standalone map; noted as unconfirmed in the
  existing map handoff, repeating it here because it directly gates the
  recommendation in section 5).
- Whether "Nosotros" is an acceptable umbrella label for Vision + Team + Historia
  + Proyectos, or whether AJ has a preferred term already in use with the board or
  funders.
- Whether the emergency phone number (+506 8339 6566) currently on `/involcrate`
  should also live in the site footer, in the map's top bar (the handoff already
  specifies "911 permanent" in the map's own UI), or both.
- Whether Freediving Club's thin, aspirational content ("we intend to build this")
  should stay live as-is, or whether AJ would rather hold it back until there's a
  concrete course or schedule to point to.
