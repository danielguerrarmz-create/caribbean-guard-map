# Sector scan — Caribbean Guard's own ecosystem

Research: Izaya (market intel lens), 2026-08-06. Read-only sweep, deliberately
aimed at the angles the design, voice, map and catalog lenses would miss.

**Verification status:** every claim below came from a WebFetch or a search result
that was corroborated. Where a page would not render or returned an error, it is
marked UNVERIFIED and should be opened by a human before anything is published on
the strength of it.

---

## 1. Facts about Caribbean Guard we did not have

These came from their own live site plus a delfino.cr article dated April 2025.
They are the most immediately useful output of this whole scan, because the
rebuilt site currently has gaps that these fill.

| Fact | Source | Status |
|---|---|---|
| Founder and President: **Lucas Iturriza** | caribbeanguard.org | WebFetch rendered |
| Operations Chief: **Elías Brown** | caribbeanguard.org | WebFetch rendered |
| ~17 team members, ILTP and Ellis & Associates CPR-EFR certified | caribbeanguard.org | WebFetch rendered |
| Physical rescue towers at **Cocles** and **Playa Grande** | caribbeanguard.org | WebFetch rendered |
| **Nine rescue stations** installed (torpedoes, ropes, tubes, life jackets, signage) | delfino.cr, April 2025 | Single source |
| ~100 community volunteers (surfers, fishermen, divers) | delfino.cr, April 2025 | Single source |
| Zero additional deaths at Playa Chiquita since the programme started; later expanded with zero fatalities to Playa Negra, Cocles and Manzanillo | delfino.cr, April 2025 | Single source |
| Costa Rica averages 270+ drowning deaths nationally over two years, 99% at unguarded beaches | delfino.cr citing Cruz Roja | Second-hand citation |
| ~~Recently joined~~ **Founding member** of the **Federación Costarricense de Guardavidas** | delfino.cr 2024-10-08 + FECOGU's own site | **VERIFIED in a browser 2026-08-06**, see 1b |

### ⚠ Discrepancy that blocks a factual claim on the map

The delfino.cr article says **nine rescue stations**. Our map shows **four**,
extracted from Caribbean Guard's own annotated sheet and georeferenced at 294
inliers / 1.2 m.

Both numbers can be true at once. The annotated sheet covers only 1.82 km of the
16.66 km coast, so four stations inside the annotated window and nine along the
whole coast is entirely consistent. But we do not currently know that, and the
map does not say which number it is showing.

**Do not reconcile this by guessing.** It goes to Caribbean Guard as a question,
alongside the existing hazard-ownership question. Until it is answered, the map
must not imply its four stations are all of them. The existing "unmapped, and
unmapped does not mean safe" language already covers this, but the station layer
specifically should carry the same caveat.

### On the eleven team members with no published role

The handoff records that the live site still says "Description goes here" for
eleven people, so the rebuild left their roles blank rather than invent them.
This scan produced two real names and roles (Iturriza, Brown) and a real
certification body (ILTP, Ellis & Associates). That is enough to fill part of the
gap **if** Caribbean Guard confirms it. It is not enough to publish unilaterally,
because a second-hand press article is a weaker source than the org itself for
who works there.

---

## 1b. FECOGU verified in a browser: the strategic finding

Two research agents were blocked by a 403 on costaricalifeguards.org. It was
opened directly in a browser on 2026-08-06. The site is live. What it shows
changes the picture, so it is recorded in detail.

**Federación Costarricense de Guardavidas (FECOGU)** is real. Founded, per
delfino.cr dated 2024-10-08, at the Costa Rica Tennis Club by three founding
associations: **Swim Safe, Caribbean Guard, and Playa Grande Lifeguards**.
President: Ernst van der Poll of Swim Safe.

**Correction to section 1 above.** The earlier scan reported that Caribbean Guard
"recently joined" the federation. That is wrong, or at least understated.
Caribbean Guard is a **founding member**. Their own site's affiliates section
lists exactly two organizations, Playa Grande Lifeguards and Caribbean Guard, and
carries Caribbean Guard's own mission text verbatim:

> "Nuestro objetivo principal es desarrollar y crear una comunidad que se sienta
> segura y sea fuerte en el agua."

This is a stronger credibility claim than anything currently on our site, it is
verifiable, and it comes from a third party.

### The state of the federation's own site

Measured in the browser, not inferred:

| Measure | Value |
|---|---|
| Total links on the homepage | 33 |
| Links pointing at `#`, i.e. dead | **25** |
| Working external links | 3: caribbeanguard.org, their Instagram, and the theme vendor |
| Stat counters (instructors, clubs, certified lifeguards, volunteers, rescues, preventions) | Labels render, **numbers are empty** |
| Platform | WordPress with the Divi theme (Elegant Themes) |

Their primary navigation contains an item called **"Playas y Seguridad"**, beaches
and safety. **It is one of the 25 dead links.** There is no page behind it.

### Why this matters more than any design precedent

The national lifeguard federation of Costa Rica has a beaches-and-safety section
that does not exist, and empty counters where its impact numbers should be. The
only working affiliate link on the entire site points at Caribbean Guard.

That means the map is not just a good idea for one nonprofit on one 16 km stretch
of coast. **It is the thing the national federation has a hole shaped like.**
Three separate findings now point the same direction:

1. No authoritative beach-by-beach safety resource exists for this coast (angle 4)
2. No authoritative resource exists at the national level either, only an empty
   nav item where one was intended
3. Caribbean Guard is a founding member of the body that would host it

This is a partnership and distribution argument, and it is Daniel's call and
Caribbean Guard's call, not ours. But it materially raises the value of getting
the map right, and it argues for building the data model so a second organization
could add a second stretch of coast without a rewrite. Playa Grande Lifeguards is
the obvious first candidate.

It is also a caution. If our map becomes the federation's de facto safety page,
the provenance rule stops being a nicety and becomes the whole basis for trusting
it. Nothing about this finding justifies loosening it.

**Do not approach the federation on Caribbean Guard's behalf.** This is
intelligence for AJ and for Caribbean Guard to act on.

---

## 2. Two real institutional partners, already in place

Trust signals do not have to be invented here. Two exist.

**Cruz Roja Costarricense** runs an ICT-Cruz Roja lifeguard project active on six
national beaches. Two of them, **Cocles and Manzanillo**, are Caribbean Guard's
own territory. That makes Cruz Roja a genuine co-operator on the same sand, not
merely an emergency number to call. Any credibility section on the site can say
so factually.

**Federación Costarricense de Guardavidas**, the national lifeguard federation,
which Caribbean Guard reportedly joined recently. This is exactly the kind of
third-party accreditation a small volunteer org needs in order to look
accountable. Worth a link and a badge, **after** the membership is confirmed
directly, since costaricalifeguards.org blocked our fetch with a 403 and the only
evidence is the delfino.cr mention.

---

## 3. The closest sibling in the country: Costa Ballena Lifeguards

**Fundación SOMOS**, es.somos.cr/programs/costa-ballena-lifeguards, Pacific side,
Costa Ballena and Osa.

This is the single most useful organizational precedent found, because it is the
same programme on the other coast, and it is further along.

- Running since 2014
- 400+ rescues, roughly 8,000 warnings issued
- Public-private partnership with Municipio de Osa, Guardacostas, Fuerza Pública
  and Cruz Roja
- Partly funded via UNDP grants
- Explicitly working with the federal government and the U.S. Embassy toward a
  national lifeguard service

Two separate things to take from it:

1. **A funding pathway.** Municipality plus UNDP plus embassy is a concrete,
   demonstrated route for a Costa Rican beach-safety programme to get money and
   institutional cover. This is a conversation for AJ, not a design decision.
2. **A page structure.** Impact statistics, then donate CTA, then a partner-logo
   row. Simple, and it is what a funder scanning the page is looking for.

---

## 4. The information gap that justifies the map

This is the finding that most validates the project, and it is an absence rather
than a precedent.

What a visitor to Puerto Viejo can find today about water safety:

- **U.S. Embassy Costa Rica**, "Aquatic Safety Tips for Travelers"
  (cr.usembassy.gov/aquatic-safety). Fetch returned garbled output, so treat the
  detail as UNVERIFIED, but the substance is corroborated across other sources:
  dozens of US citizens drown in Costa Rica yearly, most beaches have no
  lifeguards and no flags, and the guidance amounts to "if there is no lifeguard
  and no flag, do not swim."
- **puertoviejosatellite.com/en/safety**, a community-run local outlet. Plain
  text. States that only Playa Cocles is patrolled. Generic "swim parallel to
  shore" advice. No map, no flag system, and it leans on visitor comments.
- **TripAdvisor threads on Playa Cocles**, full of first-hand near-drowning
  accounts. This is functioning as an informal crowd warning system. It is
  unstructured and unreliable, and it is demonstrably where people search when
  they type "Puerto Viejo rip current."

**There is no authoritative, beach-by-beach digital safety resource for this
coast.** Nothing to compete with, and a real vacuum to fill. It also means the
map does not need to be better than an incumbent, it needs to be trustworthy
enough to become one.

Note the tension this creates with our own provenance rule: the moment this map
becomes the authoritative source, the cost of overclaiming goes up, not down.

---

## 5. Marine life: mostly a gap on this coast

Included for completeness. Lower relevance than the above.

- **COASTS** (coasts-cr.org), grassroots sea turtle nonprofit. Useful for one
  specific reason: it displays legal registration (La Gaceta number plus cédula
  jurídica) alongside SDG-alignment badges and partner logos. That is a working
  answer to "how does a small org look legitimate without an annual report."
  No financial transparency documents published.
- **Turtle Love** (turtlelovecr.org) and **Sea Turtle Conservancy** / Tortuguero.
  Caribbean side, but nesting-beach focused rather than hazard-safety. Low
  relevance, noted so nobody re-searches them.
- **Marine mammals and mangroves in Talamanca: thin to absent.** The nearest
  active marine-mammal research is Panacetacea in Bocas del Toro, Panama, on a
  genetically isolated dolphin population of fewer than 100 individuals
  threatened by boat traffic. Costa Rican mangrove restoration is concentrated on
  the Pacific side (Corcovado Foundation, Tierra Pura). No Caribbean-side
  mangrove organization surfaced.

That last point is a gap rather than a precedent, and worth remembering only if
Caribbean Guard ever widens its scope beyond human safety.

**Bandera Azul Ecológica**, the national beach ecolabel run by ICT, uses a star
system whose criteria include water quality, safety and environmental education.
A plausible third-party credibility target for Caribbean Guard to pursue or
reference.

**SINAC / La Amistad Caribe Conservation Area (ACLAC)** covers the Talamanca
coast, 26,386 marine hectares. A regulator, not a partner. Relevant if the map
ever needs official sanction.

---

## 6. Funding and credibility infrastructure

No Latin American equivalent of Candid or GuideStar surfaced. There does not
appear to be a regional nonprofit-transparency registry that a donor would check.

That makes the two working substitutes found here more important than they would
otherwise be: SOMOS's UNDP-plus-embassy pathway for actual money, and COASTS's
displayed registration number for cheap, verifiable legitimacy.

---

## 7. Adjacent channels

- **Surf-forecast.com, Surfline, meteoblue** all carry Puerto Viejo swell and
  wind data, with zero hazard framing. A possible future data integration, not a
  safety precedent, and integrating it would raise the overclaiming risk sharply.
- **Dive shop safety pages and WhatsApp or Facebook alert groups: not found.**
  Searches returned only generic community and expat pages. Marked UNVERIFIED and
  not-found rather than absent. Do not assume that channel exists, and do not
  assume it does not. A local would know in one question.

---

## Open questions for Caribbean Guard

Consolidated, so they can go across in one message rather than five.

1. Four rescue stations or nine? Is the annotated sheet a subset of a longer
   coast, and where are the others?
2. Confirm the eleven team roles. We have two names and a certification body from
   press coverage; we will not publish roles on that basis alone.
3. Confirm Federación Costarricense de Guardavidas membership, so it can be shown.
4. Confirm the Cruz Roja co-operation at Cocles and Manzanillo can be stated
   publicly.
5. Who owns each hazard verdict, and on what date. Still the largest blocker,
   unchanged from the 2026-07-30 handoff.
