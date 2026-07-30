# Audience and behaviour

Evidence pulled from the saved HTML in this folder. Quotes are translated where
useful; original Spanish is kept where the exact wording matters.

## Three highest-value findings

1. **The organization's best trust evidence is real and specific, but it is
   scattered where a skeptical visitor will never open it.** Named staff carry
   real certifications ("Guardavidas certificada ILTP," "Instructor de
   Instructores de RCP & EFR by Ellis & Associates," ISA surf certification,
   six years as a Red Cross lifeguard/swim instructor in the US), and the org
   states plainly on `/lifesaving-club`: "Desde la creación de la organización,
   hasta hoy, nunca murió nadie en nuestras guardias" (no one has ever died on
   our watches, since founding). None of this appears on `/`, none of it
   appears on `/swim-club` where a parent is deciding, and the credential
   detail lives inside a collapsed accordion on `/team` that most visitors
   will never expand.

2. **The site has zero English infrastructure**, confirmed in the Squarespace
   config itself: `"languagePicker": {"enabled": false, ... "languageFlags": []}`.
   Not partially built, not disabled by mistake in one place, simply absent.
   This matters because the site's own founding logic says tourists drown and
   tourists read English, and the map draft already solved this with
   auto-detect. The main site has not.

3. **The map is about to make a promise the rest of the org's content has
   never had to make.** Every existing safety artifact on the site (the PPO
   flag system, the survival line, the rescue stations) is *descriptive of
   infrastructure*, never a live per-location verdict. "This equipment exists
   here" is a different claim from "it is safe to swim here right now." The
   map is the org's first live claim, and there is currently no stated rule
   for who updates it, how often, or what a stale reading defaults to.

---

## The audiences

### The tourist standing on the sand

**Arrives wanting:** one answer, in English, in about two seconds, possibly
managing kids at the same time.

**Emotional state:** distracted, physically uncomfortable (sun, sand, phone
glare), often already carrying some vague warning from a hostel or local
("watch that current"). Not in a reading mood.

**What the site currently gives them:** nothing, because the QR code and the
main Squarespace site are not the same product and are not currently linked
to each other. This person's entire experience is the map (or will be); the
`.org` site with its ten Spanish destinations is irrelevant to them in the
moment of standing on the beach.

**What they actually need:** a status they can read without translating, in
under two seconds, plus one unambiguous next action if the answer is bad
(call this number, walk to this tower).

**Single highest-value change:** treat the QR-to-map path as fully separate
from the main site's navigation and language problems, and make sure the map
itself never requires a trip back to caribbeanguard.org to find the
emergency number. The draft already does the "911 permanent in the top bar"
part right; keep that as non-negotiable.

### The tourist planning the trip

**Arrives wanting:** to decide which beach town to stay in, weeks out, from
another country, in English, most likely via a search engine.

**Emotional state:** in planning mode, comparing options, not yet anxious
about safety specifically, more likely searching "is Playa Cocles safe to
swim" or "best beach Puerto Viejo family."

**What the site currently gives them:** nothing indexable. There is no
English content anywhere, no page written for pre-trip research intent
("which beaches have lifeguards," "when is the dangerous season"), and the
existing content is written entirely from the inside, for an already-engaged
Costa Rican community member, donor, or volunteer. This is the audience the
brief correctly flags as "currently not being reached at all," and the HTML
confirms it: there is no `/en/` anything, no bilingual meta description, no
content shaped like a travel-safety answer.

**What they actually need:** a short, plainly-titled English page that
answers the actual pre-trip question (which beaches, what the flag system
means, when lifeguards patrol) and is written to be found by search, not
just browsed by someone already on the site.

**Single highest-value change:** one English page built for this exact
search intent, not a translated mirror of the whole site. This is also the
page most likely to eventually rank and drive the QR/map story to people
before they land at the beach, not just once they're standing on it.

### The local parent considering the swim club

**Reads Spanish.** Cares about safety, cost, schedule, competence.

**What the site gives them, from `/swim-club`:** a real, specific schedule
("Punta Uva: todos los jueves a las 7.15am," "Playa Negra: todos los martes y
viernes 4pm"), a statement that it is free ("gratuitas y abiertas a la
comunidad"), and a line that the children's Swim School is taught by
"instructores certificados." That is a good, concrete page by the standard of
the rest of the site.

**What is missing:** the certification claim is not backed up on this page.
The credentialed instructors (ILTP-certified lifeguard, Red Cross-trained
instructor, Ellis & Associates EFR instructor) exist and are named on
`/team`, but `/swim-club` does not link to them, name them, or state an age
range or intake process for a child. A parent reading only this page has to
take "certified" on faith with no name attached, and has no stated way to
actually enroll a child beyond presumably showing up.

**Single highest-value change:** name at least one certified instructor
directly on `/swim-club`, with their real credential line pulled from
`/team`, plus one sentence on how to bring a child (age range, what to show
up with, which of the two locations is more suited to a first-timer).

### The volunteer or trainee

**Probably young, probably local, probably on a phone with limited data.**

**What `/involcrate` gives them:** a warm, honest pitch. It explicitly
welcomes people who are not strong swimmers ("Si no tienes mucha experiencia
en el agua, unirse al Swim Club es una gran forma") and explicitly says the
org needs people from different trades, not just lifeguards ("Se necesita
gente de la comunidad de diferentes oficios, no solo Guardavidas"), closing
with "¿Cuáles son tus fortalezas?" That is a genuinely good, non-gatekeeping
tone and should survive the revamp.

**What is missing:** no next step. There is no WhatsApp link, no form, no
named Saturday training location repeated here (it exists on
`/lifesaving-club`: "Todos los sábados a la mañana... entrenamiento... abiertos
a la comunidad," but `/involcrate` does not point to it). The only contact
method on the page is Instagram, a general Gmail address, and an emergency
phone number that should not be the first thing a nervous 19-year-old dials
to ask about joining. The page is also a large image gallery, which is the
wrong shape for someone on limited mobile data trying to find one fact.

**Single highest-value change:** end the page with one concrete, low-friction
next action (a WhatsApp link if one exists, or explicit "show up here, this
time" pointing at the Saturday training already described elsewhere on the
site) and cut the gallery weight.

### The individual donor

**Small amount, moved by a story. Needs to believe the money does something
specific.**

**What `/donar` gives them:** a generic paragraph ("Tu donación nos ayuda a
salvar vidas ofreciendo clases de natación gratuitas, entrenamiento de
guardavidas y talleres de seguridad comunitaria...") and full payment detail:
Banco Nacional de Costa Rica account numbers and IBANs in both USD and
colones, a PayPal email address, and a Sinpe Móvil number. The payment
mechanics are thorough and specific, which is good.

**What is missing:** zero connection between a donation amount and an
outcome, and zero use of the org's own strongest proof points, which exist
elsewhere on the site but not here: zero deaths on duty since founding, 400+
community members trained since 2021, the 70+ member emergency alert network,
the Swim Safe Costa Rica partnership that donated equipment and ran four
lifeguard courses. A donor lands on a page that is all mechanism and no
story, right next to pages that have all the story and no ask.

**Single highest-value change:** put two or three of the org's real numbers
directly on `/donar`, and if a specific cost is known (a rescue tube, a
course seat, a survival line), state it. Right now the page never tells
someone what they are buying.

### The institutional funder or partner

**A municipality, hotel association, or NGO. Punishes vagueness.**

**The single strongest piece of content on the entire site for this audience
is `/programa-playa-organizada`, and it is three clicks deep with no
funder-facing framing.** It lays out a concrete, replicable partnership
model: a marked safe-swim zone, a survival line (rope and buoys, "Ya se
colocó la primera en junio 2024" — the first one was actually installed, with
a date), drone-mapped zones, named local partners who fund and maintain
equipment ("Ellos ayudan a financiar, se comprometen con el equipo: sacarlo y
meterlo todos los días"), fixed rescue stations with a specific equipment
list, a written emergency protocol, and a CPR/first-aid/lifeguard course
specifically for hotel and business staff. This is exactly the kind of
concrete, operational detail a hotel association or municipality would need
to say yes to a partnership, and it currently reads as a program page buried
in the nav rather than a pitch.

**The `/proyectos` page mixes done and not-done without marking which is
which**, which is the one thing this audience will not tolerate. The
survival line has a real installation date. The "Centro Acuático de Alto
Rendimiento" (a semi-Olympic pool, a children's pool, a dive tank, classrooms,
volunteer housing, parking) is described in the same confident, specific
tense but does not exist yet. A funder reading this page cannot tell built
from planned without inferring it, and a funder who infers wrong and finds
out later will not come back.

**Also relevant and currently invisible to this audience:** the org is
pursuing a national "Federación de Guardavidas" in coalition with other
organizations, mentioned once, in a single sentence, inside the origin-story
paragraph on `/nuestro-trabajo`. That is a civic-credibility signal
(this is not a lone group, it is part of a sector-wide push) that belongs
somewhere a funder will actually see it.

**Single highest-value change:** mark every forward-looking project with an
explicit status (planned / underway / built), and give
`/programa-playa-organizada` the framing of a partnership offer, not a
program description.

### The journalist or researcher

**Wants a citable fact and a contact.**

**What the site gives them:** an Instagram handle, a general Gmail address
(`caribbeanguard.pv@gmail.com`), and an emergency phone number
(+506 8339 6566) that is explicitly labeled "Teléfono de emergencias" on
`/involcrate`, which is the wrong number to hand a reporter. There is no
press contact, no fact sheet, no downloadable one-pager, and the one
regional statistic on the site ("los domingos, los días con más incidencias
de ahogamiento en todo el país" — Sunday is the day with the most drowning
incidents nationally) has no cited source anywhere on the page it appears on.

**Single highest-value change:** a named press contact separate from the
emergency line, and confirmation of whether the Sunday statistic is
citable (see "needs confirmation from AJ" below) before it goes back out to
a journalist through a revamped site.

---

## The trust question

Assessed honestly: the underlying qualifications are real and, once you dig
for them, more substantial than the site's presentation suggests.

**What's genuinely there:** an ILTP-certified lifeguard who is also a
certified CPR/EFR instructor through Ellis & Associates (a real, recognized
credentialing body); an ISA-certified surf instructor who is also certified
as a water rescue instructor through Mar Chen and is described as likely the
person with the most water rescues on the Caribbean coast; a US-trained,
Red Cross-certified lifeguard and swim instructor with six years of
professional experience before joining; a founder-run organization with a
five-year operating history (founded March 2021), 400+ community members
run through its courses as of September 2024, and a formal partnership with
an existing organization, Swim Safe Costa Rica, that donated equipment and
delivered four lifeguard courses. And the flat, unhedged claim that repeats
twice in the source material: no one has died on one of their watches since
founding.

**What's missing is not the substance, it's the placement.** All of that
lives on `/team` (behind a collapsed accordion) and `/nuestro-trabajo` (a
page named "our work," which is not where a first-time visitor deciding
whether to trust this organization's judgment about water safety is going to
look). `/` and `/lifesaving-club`, the two pages most likely to be a
stranger's first stop, currently state zero credentials, zero track record,
and zero named individuals. `/lifesaving-club` opens straight from the H1
into a carousel with no framing paragraph at all.

**One credibility gap worth being honest about:** `/vision` lists
"Homologación del Programa Playa Organizada, Bandera Roja y Amarilla. ICT."
as a goal, not an achievement, meaning the organization's own flag system is
not (as of this source material) officially recognized by Costa Rica's
tourism board. That's not disqualifying, but it means any revamped page
should not imply official government sign-off on the flag or safety system
that doesn't exist yet. This also bears directly on the map's liability
question below.

**Recommendation:** build a short, factual trust block (three or four
sentences, real numbers, no hedge words) and put it on `/` and
`/lifesaving-club`, then link outward to full bios on `/team`. The material
to build it from already exists verbatim in the source HTML; nothing here
needs to be invented.

---

## The language decision

**Recommendation: selective bilingual, not full site-wide bilingual, matching
the pattern the map draft already uses (auto-detect, Spanish fallback).**

Full bilingual across all ten-plus current pages would mean translating and
permanently maintaining Spanish and English versions of policy-advocacy
content aimed at Costa Rican institutions (`/vision`'s references to Ley 9780
and MEP curriculum requirements mean nothing to a tourist and don't need to
exist in English), internal team bios, and donor mechanics, on an
organization whose only visible point of contact is a single Gmail address.
That is not a maintainable commitment for a volunteer-run nonprofit, and a
half-translated bilingual site (some pages updated, some stale) is worse for
trust than an honest Spanish-only site, because it signals neglect rather
than a deliberate choice.

**What should be bilingual:** the pages a tourist actually needs before or
during a trip. Concretely: the home page hero and trust block, the map
itself (already solved), and the one new English-facing page recommended
above for the trip-planning audience. That's a bounded, maintainable set,
built once and touched only when the underlying facts change, not on every
site update.

**Cost:** translating and maintaining roughly two to three pages, once,
rather than the whole site, continuously. This is the same reasoning the map
draft already reached independently ("Language auto-detects, ES fallback.
Tourists' phones are in English and tourists are who drown"); the
recommendation here is to extend that one decision to the rest of the site
rather than inventing a second approach.

---

## The hardest tension: a map that says "safe" is a promise

The map is the single most useful thing this organization could publish, and
it is also the first time the organization will make a live, specific,
time-bound safety claim rather than a description of infrastructure or
training. Real position, not a hedge:

**Don't default to safe. Default to unknown.** Established lifesaving
practice (the ICT's own Bandera Roja/Amarilla flag model that Caribbean
Guard is trying to get formally recognized under, and international
lifesaving federations generally) does not treat a flag as a static
publication. It is a live signal, set and re-set by a person, on a
schedule, at a location, and it defaults to the most restrictive state when
nobody has checked recently. A map that shows a beach as "safe" because
nobody has updated it in three days is more dangerous than a map that says
nothing, because it converts silence into false reassurance. The single
design rule that follows: every status the map shows needs a "last checked"
timestamp attached to it, and a beach with a stale or missing timestamp
should render as unknown, never as safe.

**Don't use the word "safe" as a verdict. Describe conditions and staffing
instead.** "Seguro / Safe" as a standalone label is exactly the implied
assurance that creates liability, because it reads as a guarantee rather than
an observation. Caribbean Guard's own program content already models the
right vocabulary without realizing it: "patrullado," "sin guardia," language
that describes what is actually true right now (patrolled, unpatrolled,
reported rip current) rather than issuing a yes/no verdict on something the
ocean can change in minutes. This is not burying the risk in fine print,
it's building the uncertainty into the state model itself so it can't be
skimmed past, which is a stronger version of a disclaimer than a paragraph
nobody reads.

**Attribute every status to a person or process, the way `/programa-playa-organizada`
already does for equipment.** The PPO content states explicitly who is
responsible for setting out and collecting rescue equipment each day (the
local partner business). The map needs the same discipline for hazard
status: not "Cocles: caution" as an anonymous assertion, but "Cocles:
caution, reported by [X] at [time]." The handoff document already flags this
as unresolved ("Hazard data has no owner yet... a map that says DO NOT SWIM
must be able to say who decided that and when"). That's correct, and it's
the same principle the org already applies to physical equipment; it should
be non-negotiable before the map ships hazard data beyond a placeholder.

This keeps the map genuinely useful (a real status, not a wall of caveats)
without making a promise the organization cannot keep (a guarantee about an
ocean it does not control), by shifting what's being asserted from a verdict
to an observation with a timestamp and a source.

---

## Story and proof

**Evidence that already exists in the source material but is not being used
where it would do the most work:**

- "No one has died on our watches since founding" (2021 to present) appears
  twice (`/lifesaving-club`, `/nuestro-trabajo`) and nowhere else. It belongs
  on `/`, `/donar`, and the map's about/credibility surface.
- 400+ community members trained since founding (as of September 2024)
  appears once, on `/nuestro-trabajo`.
- The 70+ member community emergency alert network (guards, surfers,
  swimmers, fishermen, divers, freedivers) appears twice, never on `/donar`
  or `/`.
- Named, credentialed staff bios (ILTP, Ellis & Associates EFR, ISA, Red
  Cross) exist only inside a collapsed accordion on `/team`.
- The survival line's actual installation date (June 2024) and the fixed
  rescue station equipment list are buried inside the `/programa-playa-organizada`
  carousel, the single strongest funder-facing content on the site.
- The full origin story (Semana Santa 2021, a big swell, 30 volunteers
  patrolling 6 beaches in one weekend, the founding group of eight named
  people, the Swim Safe Costa Rica partnership that donated equipment and ran
  four lifeguard courses) exists only on `/nuestro-trabajo`. This is strong,
  specific, human material and is currently the least likely page in the
  navigation for a donor or journalist to open first.

**What to ask AJ for, concretely, before the revamp locks in claims:**

- Whether there is an actual rescue count or incident log the org keeps
  (distinct from "no deaths on our watches"), since a number of lives saved
  or incidents responded to would strengthen the donor and funder case
  considerably if it exists and is real.
- Whether the ICT Bandera Roja/Amarilla homologation listed as a goal on
  `/vision` has since been achieved, and the current status of Ley 9780
  implementation, so the revamped site doesn't overstate official recognition
  of the flag system.
- Whether "Sunday is the highest-drowning-incident day nationally" is a
  sourced, citable statistic (which agency) or internal knowledge, before it
  is repeated to a journalist.
- A press or media contact, distinct from the emergency phone number.
- Whether an online donation mechanism exists beyond bank transfer, PayPal
  email, and Sinpe Móvil (no PayPal button or checkout link was found in the
  source HTML; confirm this is accurate before the revamp, since it changes
  how much friction the donor flow has).
- Whether the swim club has any registration process at all for children
  (age range, intake), since none is stated anywhere on `/swim-club` or
  `/involcrate`.
- Current real status of the two `/proyectos` items (Programa Guardia Móvil
  and CADAR): planned, funded, under construction, or purely aspirational,
  so the revamp can mark them honestly instead of in the same confident tense
  as things that already exist.
- Any regional drowning data the org tracks, or that ICT or Cruz Roja
  publishes for this stretch of coast, both for the journalist audience and
  as a possible real data source for the map itself rather than the
  placeholder hazard zones flagged in the 2026-07-29 handoff.

## Needs confirmation from AJ (summary list)

- Rescue/incident count if logged
- ICT Bandera Roja/Amarilla homologation status and Ley 9780 status
- Source for the "Sunday" drowning statistic
- A press contact separate from the emergency line
- Whether an online donation button exists beyond the bank/PayPal/Sinpe details found
- Whether swim club has a stated child registration process
- Built/funded/planned status of Programa Guardia Móvil and CADAR
- Any regional drowning data the org has access to, for the journalist audience and the map
