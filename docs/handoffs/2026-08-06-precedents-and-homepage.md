# Caribbean Guard, 2026-08-06: precedent research and the mobile homepage

Companion to `2026-08-06-map-schema-and-offline.md`, which covers the map. Read that
one for anything about `web/`. This covers `docs/precedents/`, `tools/build_site.py`,
`tools/make_placeholders.py` and `site/assets/site.css`.

Nothing here is committed.

## What

**1. Five precedent files** in `docs/precedents/`, from a five-agent research wave.
29 organizations and roughly 20 maps verified by direct fetch. Every failure is
recorded in a table rather than described from a search snippet.

| File | Covers |
|---|---|
| `00-catalog.md` | 29 LatAm nonprofits protecting people or marine life, sorted by fit |
| `01-mapping-tools.md` | Public safety and hazard maps, inspected at bundle and API level |
| `02-visual-language.md` | Typography, colour, imagery, mobile layout across 13 sites |
| `03-voice-and-ia.md` | Voice, Spanish register, safety-critical copy, navigation, user flow |
| `04-sector-scan.md` | Caribbean Guard's own ecosystem, partners, funding, the information gap |

**2. The homepage reordered for a phone**, plus a trust-row component that ships
built and empty.

## Why

### The strategic finding

**Caribbean Guard is a founding member of FECOGU**, the Federación Costarricense de
Guardavidas, constituted 2024-10-08 with Swim Safe and Playa Grande Lifeguards. Not
a recent joiner, which is how an earlier pass had it. Verified in a browser because
costaricalifeguards.org returns 403 to every automated fetch.

Measured on FECOGU's own homepage: **25 of its 33 links are dead `#` placeholders**,
the impact counters render labels with no numbers, and the nav item **"Playas y
Seguridad"** has no page behind it. The only working external affiliate link on the
whole site points at caribbeanguard.org.

Three findings converge:

1. No authoritative beach-by-beach safety resource exists for this coast. A visitor
   today gets a US Embassy page saying "if there is no lifeguard, do not swim", one
   plain-text community page, and TripAdvisor threads full of near-drowning accounts
   doing the work of a warning system.
2. None exists nationally either, only an empty nav item where one was intended.
3. Caribbean Guard co-founded the body that would host it.

**Do not approach FECOGU on Caribbean Guard's behalf.** This is intelligence for
Daniel and AJ. It is written up in full in `04-sector-scan.md` §1b.

### What the sector actually looks like

- **Nobody in the people-safety family publishes a hazard map.** Not one of the
  fourteen lifeguard, rescue or water-safety organizations catalogued has an
  interactive map. Every map found belongs to a marine-life org, and they are all
  animal tracking maps.
- **Of eight verified national public-safety maps** across Chile, Mexico, Brazil,
  Costa Rica, Argentina and Colombia, **not one registers a service worker.** None
  works offline. For a beach with no signal that is the gap none of them fills.
- **Formal standing and a working website are unrelated.** Mexico's national ILS
  member is an eleven-year-old Blogger post. Chile's has not been touched since 2018.
  Two of the three FECOGU founders have no website at all.
- **The credibility currency is numbers, not design.** Every well-regarded org in the
  set answers "why trust you" with specific figures. Costa Ballena leads with 6,700
  preventions and zero on-duty drownings; Santa Teresa with 216 rescues across 365
  patrol days; COASTS with 7,695 hours patrolled and a cédula jurídica.

### The three precedents

1. **Guardavidas Costa Ballena** (lifeguardscostaballena.com). Costa Rica, Pacific.
   The closest structural analogue that exists: same country, same volunteer model,
   same funding precarity. Astro, no framework bloat, which is evidence that the fast
   undecorated approach is also the credible one in this category.
2. **Santa Teresa Lifeguards** (santateresalifeguards.org). Same function, and the
   closest match to Caribbean Guard's split local-and-international audience. Uses one
   educational rip-current diagram alongside real photography rather than instead of it.
3. **beaches.ie**, Irish EPA, for the map. Keeps a long-run classification (shown as
   stars) apart from today's operational verdict (shown as colour), so a beach can be
   rated Excellent and be under a prohibition the same day.

## The homepage

**Order, mobile first:** hero → map → "busca la torre" → mission → three clubs → donate.

The map card now lands on the first screen at 390 px. It previously sat below a full
hero plus a reserved photograph. Three changes got it there:

- Removed the duplicate "Ver el mapa de seguridad" button. The card *is* that action,
  and two competing map CTAs a screen apart is one too many.
- Moved `shot("hero")` down into the mission section, where it still reserves its slot.
- New `section.lead` pulls the map tight against the hero instead of a full section
  rhythm away.

**The trust row (`stats()` in `tools/build_site.py`) is built and empty.** It renders
nothing at all while unfilled, so there is no gap and no placeholder on the page today.
It is **guarded rather than commented**: it requires both figures and a `STATS_SOURCE`
attribution string before anything renders, so a number cannot ship without a source
even if someone forgets to add one. Each figure carries its own period, because a
number without a window invites the reader to supply one.

Press coverage (delfino.cr, April 2025) gives real figures. They are deliberately not
used: a news article is a weaker source than the organization for its own impact
claims, and the station count contradicts our own map.

**Photography.** Three new reserved shots, chosen from what the precedents actually
photograph, which is operations rather than portraits or coastline: `torre` (the real
towers at Cocles and Playa Grande), `equipo-rescate` (the torpedoes and rope at dawn,
which is what makes a shift concrete) and `curso`. Also wired up `estacion`, which was
being generated and never placed. 14 placeholders, 14.3 KB total.

**No new decorative motif, deliberately.** Not one precedent studied, including those
at the top of this category's budget, invests in a bespoke graphic identity. This field
wins on photography credibility and numeric honesty. `site.css` keeps its existing
system; the only additions are `.stats` and `section.lead`.

## Two defects found and fixed

**The homepage was reintroducing the exact claim the map had just removed.** The map
card read "Dónde se puede nadar en esta costa", a permission claim about a map where no
zone has been reviewed. The same phrasing was in `/mapa`'s lede and its meta
description. All three now describe what the map shows and leave the judgement to the
reader. A sweep across all 14 pages is clean.

**The annotated map's alt text had drifted from the data.** It hand-counted "diez
corrientes" while `hazard_summary()`, generated from the same GeoJSON three lines
below, said nine. New `hazard_counts()` reads both numbers from the file, so the page
and the map cannot disagree. That was the whole point of the text equivalent.

## Verify

    cd C:\Users\danie\caribbean-guard
    python tools/make_placeholders.py
    python tools/build_site.py
    npm run dev

- Site: http://localhost:5173/
- Map: http://localhost:5173/mapa/app/index.html
- Homepage critical path: **24.4 KB** (`index.html` 8,171 + `site.css` 15,314 +
  `site.js` 1,549), inside the 30 KB budget.
- At a 390 px viewport the map card is above the fold.
- Permission-claim sweep, should return nothing outside code comments:

      grep -rn "se puede nadar\|es seguro nadar\|tiempo real" site/ --include=*.html | grep -v "site/mapa/app/"

## The site cut (later the same day)

Daniel's read after seeing it: still too much, cut hard, map first and everything
else secondary.

**Navigation: 7 items to 4.** Mapa de Seguridad · Playa Organizada · Clubes ·
Involúcrate. Nosotros moved to the footer.

A navigation bar is a claim about what matters, and seven items claimed that a
visitor deciding whether to enter the water and a visitor thinking about apnea
classes deserve the same weight. They do not. What a person arrives with, in
order: am I safe here, what do you run, how do I take part, who are you.

**Three club pages collapsed into one.** `/clubes/`, three sections, one form.
Three pages made the reader choose a club before knowing what any of them was,
and put two thirds of the answer one tap away from wherever they landed. Nobody
arrives certain they want apnea rather than open water. 14 pages to 12.

**The homepage is now the map plus who they are.** The mission block was five
paragraphs, which became the least minimal thing on the page once everything
around it was cut. It is now its first block only, with the rest moved intact to
`/nosotros/`. **Excerpted, never rewritten** — the words on the page are still
exactly Caribbean Guard's. The clubs section went from three full rows with
reserved photographs to two lines and a link.

Homepage **8,147 B to 5,422 B**. Critical path **24.4 KB to 22.3 KB**.

### Two pre-existing broken links, found and fixed

`tools/` gained no link checker, but one was written for this restructure
(scratchpad, not committed) and it caught two live defects that predate today:

- `/mapa/` linked to `mapa/`, resolving to `/mapa/mapa/`
- `/playa-organizada/` linked to `mapa/`, resolving to `/playa-organizada/mapa/`

Both were `map_card()` called without its `up` argument on depth-1 pages. Fixed by
passing `"../"`. **All 142 internal links now resolve.** Worth adding a permanent
link check to the build; the whole class is invisible until someone taps.

## Squarespace: answered

**A Code Block cannot host the map.** Decided and settled, so it does not get
relitigated:

- A Code Block renders inline in the page's own document, not a sandbox, so our
  CSS and JS collide with Squarespace's.
- **A service worker cannot register**, because Squarespace will not serve
  `sw.js` at a usable scope. Everything built today for offline dies on that path.
- The parent page is 67 s on Slow 3G against 7.8 s standalone. A factor of 36.
- On Basic or Personal, JavaScript and iframes are premium, the block silently
  renders nothing to the public, and only a logged-in admin sees a notice.

**Decision: standalone URL plus a link card on Squarespace.** The link card is
plain HTML with no JavaScript, so it works on every plan and cannot fail
silently. The QR codes point at the map's own URL, so Squarespace never gated the
safety map to begin with.

**Open for AJ, 30 seconds, no billing access needed:** paste
`<iframe src="https://example.com" height="200"></iframe>` into a Code Block on
any page and save. A notice saying the code is unsupported means Basic or
Personal. Delete it afterwards. This decides whether an embed is ever an option;
it blocks nothing now.

## Tomorrow: annotations first, map second

**Daniel's direction, and it reframes the deliverable.** The next session goes to
**writing annotations on the base image, treated as an annotated image rather
than as a map**. That is what the Caribbean Guard team needs most.

Read that as a change of surface, not a reversal. What survives it, unchanged:

- The georeference and the rectified north-up base. An annotation lands in the
  right place because of that work, whatever draws it.
- `cg-hazards.geojson` and the extraction pipeline. Nine rips, four stations, one
  unlabelled polygon, all with coordinates.
- The provenance model: `authored`, `reviewed`, `org`, the two clocks, and the
  three distinct absences. An annotation nobody has signed is exactly as unowned
  as a zone nobody has signed.
- The status vocabulary. Instructions rather than ratings, and the rule that no
  label may grant permission, hold whether the thing is a slippy map or a labelled
  picture.
- The precedent research, particularly the sector finding that **nobody in the
  people-safety family publishes an interactive map at all**, which is an argument
  for the annotated image rather than against it.

What is genuinely map-shaped and should not absorb more effort until this is
settled: the zoom floor and refit machinery, the backdrop letterboxing, the
locate control, and the deep-link camera behaviour.

The honest framing for tomorrow: an annotated image is what Caribbean Guard
already made by hand, and what they published. Meeting them there is the shorter
path to something they will actually use and sign.

## Left to do

1. **Fill the stat row.** Needs figures from Caribbean Guard directly, plus a date.
2. **Sharpen the shot list further** once someone can shoot: the briefs are written but
   no photograph has been taken.
3. **The `lang="es-AR"` question** is still deliberately untouched. Worth knowing when
   it is revisited: their own copy uses tú imperatives, so the tag and the copy already
   disagree, and the map has now been unified onto tú to match.
4. Nothing is committed.

## Open questions for Caribbean Guard

Seven, consolidated so they can go across in one message.

1. **Is there a working red flag system on this coast?** Biggest one. Our Cocles copy
   asserts one and it is unverified. If it is real, the RNLI model of schedule plus
   doctrine plus explicit uncertainty becomes available, and it removes the
   review-cadence dependency the whole project currently rests on.
2. Four rescue stations or nine? Press says nine, our map shows four. Both can be true,
   since the annotated sheet covers only 1.82 km of 16.66 km, but we do not know that.
3. The eleven team members with no published role. Press gives two names and a
   certification body; that is not enough to publish.
4. Can the FECOGU founding membership be stated publicly?
5. Can the Cruz Roja co-operation at Cocles and Manzanillo be stated publicly?
6. What is the actual patrol shift? `TODAY_VALID_HOURS = 12` is a placeholder.
7. What does the shaded polygon on their annotated map mean? It is not in their legend
   and could be a hazard zone or a designated safe swimming zone.

## Files

- `docs/precedents/00-catalog.md` … `04-sector-scan.md` — the research
- `tools/build_site.py` — `stats()`, `hazard_counts()`, homepage order, map card copy
- `tools/make_placeholders.py` — three new shots plus the note on what precedents shoot
- `site/assets/site.css` — `.stats`, `section.lead`
