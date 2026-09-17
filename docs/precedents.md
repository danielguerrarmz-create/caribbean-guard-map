# Precedents: who else maps beach safety, and what we take from them

Surveyed 2026-09-17. Every URL below was loaded on that date; where a claim comes
from a press report rather than from the thing itself, it says so. Re-check before
citing any of this in front of the board, because a dead link in a precedent list
is worse than no precedent list.

## The finding that matters most

**Costa Rica has no live public per-beach hazard map.** We looked for one across
Cruz Roja Costarricense, the ICT, Bandera Azul Ecológica, and any Talamanca or
Limón municipal source, and found none.

- Cruz Roja Costarricense and the Universidad Nacional studied roughly 160
  beaches (reported by *La Nación*, 2016). The study exists; a public map of it
  does not.
- The ICT's answer is **physical signage** at 100+ beaches. That is a real
  intervention and it is not addressable from a phone.
- **Bandera Azul Ecológica** covers 151 beaches and is a *sanitation and
  environment* award. It is not a hazard classification, and reading it as one is
  the specific trap this project exists to avoid: a blue flag says the water is
  clean, not that it will not drown you. Brazil's `balneabilidade.ima.sc.gov.br`
  and Ireland's `beaches.ie` fall in the same category.

So Caribbean Guard is not a worse copy of something that already exists here. It
is the first of its kind in this country, and the precedents below are all
foreign. That is the argument for AJ and the board, and it is also the reason the
provenance doctrine matters: there is no incumbent whose authority we can borrow.

## The local incumbent

**Puerto Viejo Satellite — safety page**
https://www.puertoviejosatellite.com/en/safety/ (live 2026-09-17)

Community-run (Doh Media), bilingual, and genuinely instructional: it tells you
to ask locals before getting in, and it carries the swim-parallel escape advice.
It is prose, not a map; there is no per-beach classification and no named author.

This is what a visitor to Puerto Viejo finds today. Anything we publish is
measured against it, and the two things we must beat are **per-beach specificity**
and **a named organisation behind the claim**.

## 1. Surf Life Saving Australia — Beachsafe

https://beachsafe.org.au/ · example page:
https://beachsafe.org.au/beach/nsw/waverley/bondi/bondi-beach

The only per-beach system at national scale. Every Australian beach has a page
carrying an expert-written description, a length, seven days of patrol times, and
a hazard rating on the Short and Hogan 1-to-10 scale. Bondi reads, verbatim:

> General Hazard Rating: 7/10 (Highly hazardous)

**What we take:** that a beach deserves a page, that the page names its patrol
hours, and that somebody with expertise writes the description rather than a
template filling it in.

**What we deliberately reject: the number.** "7/10 Highly hazardous" tells a
tourist standing on the sand nothing they can act on. It is a comparison between
beaches, and a person is standing on exactly one beach. Every Caribbean Guard tier
is a verb phrase for this reason. When somebody asks why we did not use a
0-to-10 rating, Beachsafe is the thing to point at: it is the best-resourced
beach safety system in the world and its top-line output is still a number you
have to translate before you can obey it.

## 2. NOAA / National Weather Service — rip current risk

https://www.nhc.noaa.gov/rip-currents/map.html

**This is where our tier vocabulary comes from, and we should say so out loud.**
The four states, quoted verbatim from the map's own legend on 2026-09-17:

| level | NOAA's wording |
|---|---|
| HIGH | "Life-threatening rip currents are likely. Swimming conditions are unsafe for all levels of swimmers. **Stay out of the water.**" |
| MODERATE | "Life-threatening rips are possible and may appear suddenly. Remain in shallow water and beware of surf that can knock you off your feet." |
| LOW | "Always exercise caution in the ocean. **Life-threatening rip currents are still possible near groins, jetties, reefs, and piers.**" |
| NO DATA | "Exercise caution and heed the advice of the local beach patrol and flag warning systems." |

Compare our own strings in `web/index.html`:

- `"no-swim"` EN is **STAY OUT OF THE WATER**, which is NOAA's HIGH instruction
  word for word.
- `charLowerRiskRider` EN is *"Lower risk does not mean safe. Life threatening rip
  currents are still possible near reefs, channels, headlands and river mouths"*,
  which is NOAA's LOW with our coast's features substituted for theirs.

That matters for two reasons. The 08-06 ruling that no tier may grant permission
(`SE PUEDE NADAR` deleted) is not our invention or our caution: **the United
States' national rip current forecast will not say a beach is safe either, on any
tier, ever.** And the NO DATA row is the precedent for our deferral sentence.

**What we take:** the whole vocabulary, and the right to cite an authority for it
rather than defend it as taste.

## 3. Safeswim — Auckland Council, Surf Life Saving New Zealand and others

https://safeswim.org.nz/

Map-first: pins on a coastline, per-beach panels, patrol times for every SLSNZ
beach. It carries water quality *and* safety hazards on the same map and keeps
them visually distinct, which is the same two-axis problem our CHARACTER / TODAY
split solves.

The part to study is the input path. Per Auckland Council's own description,
**surf lifeguards on patrol upload public safety warnings from the beach** —
dangerous waves, rip currents, jellyfish, shark sightings — and those appear on
the map. (Sourced from Auckland Council's Safeswim media guide, not from reading
their admin tool.)

**What we take:** this is the answer to the open governance item in every recent
handoff, *"TODAY has no way in"*. Safeswim is proof that a phone-sized signing
surface for the guard on duty is a solved problem at a comparable scale, and it
is the thing to show AJ when asking who will sign a bulletin.

## 4. Cruz Roja Española — Estado de las Playas

https://www.cruzroja.es/appjv/consPlayas/listaPlayas.do (live 2026-09-17)

The nearest Spanish-language NGO equivalent, and it is included because of how
**thin** it is, not how good. On the date checked it returned "Se han encontrado
66 playas" as a plain text list, heavily weighted to Bizkaia, the Canaries, the
Balearics and Valencia. The page contained exactly one link, back to the index:
no map, no per-beach page reachable from there, no hazard classification.

**What we take:** calibration. This is the Spanish Red Cross, a national
organisation, and its public beach-state tool is a list of 66 names. A small
Costa Rican NGO shipping a per-beach instruction map is not behind the
Spanish-language field; it is ahead of it.

## 5. Chile — DIRECTEMAR "Playas Chile"

https://www.directemar.cl/directemar/servicios-online/aplicaciones-moviles/playas-habilitadas
(landing page; the product itself is iOS and Android only, so we could not
inspect it. Everything below is from the Armada's own announcement and press
coverage, and is UNVERIFIED against the app.)

The Chilean Navy classifies beaches on **two independent axes**:

- **apta / no apta** — is the water itself dangerous (currents, whirlpools,
  bottom)
- **habilitada / no habilitada** — is anyone watching it

A beach can be dangerous but staffed, or benign but unstaffed, and those are
different instructions. Reportedly 869 beaches nationally are flagged *no apta*.

**What we take:** a sharper reading of our own tiers. `ONLY WITH LIFEGUARDS` at
Cocles is really *apta-when-habilitada*, and the `hoursLine()` that appends
"ahora sin guardavidas" after 17:00 is us discovering the second axis by hand.
If the tier set is ever revisited, this is the model to revisit it against.

## Also looked at, ranked lower

| what | url | why it ranks low |
|---|---|---|
| Safe Beach Day (Hawaii) | https://safebeachday.com/ | Per-beach hazard from live weather and surf feeds. Honest disclaimers ("conditions are informational only and not always real-time"), but no named human assessor, and it is derived data rather than local knowledge. |
| Hawaii Ocean Safety | https://oceansafety.hawaii.gov/ | Official, but mostly advice pages and a list of lifeguarded beaches. |
| RNLI beach finder | https://rnli.org/find-my-nearest/lifeguarded-beaches | Live in a browser; blocks automated fetching, so not inspected in depth. Lifeguard coverage and tide, not per-beach hazard classification. |
| beaches.ie (Ireland) | https://www.beaches.ie/ | **Water quality, not drowning risk.** Its four-year standing classification (excellent / good / sufficient / poor) next to the latest sample is a good structural precedent for CHARACTER vs TODAY, and nothing else here transfers. |
| Cancún Tablero de Playas | https://tablerodeplayas.implancancun.gob.mx/ | Municipal, Spanish only, live weather plus a red/yellow/green by zone per press reports. Zone-level, not beach-level. |
| Puerto Rico DRNA / Sea Grant | — | A real yellow/red/black wave-flag system across roughly 90 beaches in PR and the USVI, but **we could not find a live public map URL**, only news references. Worth one more look before citing. |

## Where this leaves us

Every system above chooses one of three postures, and it is worth knowing which
one we are:

1. **Rate the beach** (Beachsafe): durable, comparative, needs translating before
   anyone can act.
2. **Report the conditions** (Safeswim, Safe Beach Day, NOAA): current, actionable,
   needs a live feed or a person on duty.
3. **Instruct the reader** (Caribbean Guard): actionable with no feed and no
   staff, and it stakes the organisation's name on a standing claim about a place.

We are the third, and the third is the only one available to an NGO with no
sensor network and no duty roster. It is also the one that carries the most risk
if a claim is wrong, which is exactly why the trust line on every sheet says who
has reviewed the beach and why the deferral sentence outranks everything above
it. None of the five precedents above defers to a lifeguard on the sand as
explicitly as we do. That is ours.
