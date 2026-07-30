# Caribbean Guard site revamp — shared brief

Read this first. It is the common context for every specialist working this job.

## Who this is for

**Caribbean Guard** is a Costa Rican nonprofit on the Caribbean coast, Puerto Viejo
through Manzanillo, Limón province. Reached Daniel through AJ (James A. Smith) at
Forsite Studio. They run beach lifesaving, swim, and freediving programs and want
observation posts along the coast.

The site is **www.caribbeanguard.org**, on Squarespace, in Spanish.

## The job

A complete restructure and revamp. Specifically:

1. Analyze every page and what it is actually for.
2. Collapse the navigation into **fewer tabs**. There are currently at least ten
   destinations and it is not obvious which one a first-time visitor should open.
3. Inventory every image on the site and keep a running internal register.
4. Plan how the **interactive coastal safety map** we are building becomes part of
   this site.
5. Typography, colour, user flow, behaviour. Judge it from several different hats,
   not just a designer's.
6. **Mobile first, desktop second.** Not a slogan here. See below.

## Why mobile first is literal in this case

The safety map exists because a tourist can drown in a rip current at Playa Cocles.
QR codes go on posts along the sand. Someone scans one while standing barefoot in
the sun on a phone with one bar of signal, and needs to know in about two seconds
whether it is safe to swim where they are standing. That is the hardest case the
site has to serve, and it should shape the whole design rather than being bolted on.

Tourists' phones are in English. Tourists are who drown. The site is currently
Spanish only.

## What already exists

- Draft map: `C:\Users\danie\caribbean-guard\web\index.html`, Leaflet, mobile first,
  bilingual ES/EN, QR deep links via `?z=` and `?p=`.
- Handoff with full state: `C:\Users\danie\caribbean-guard\docs\handoffs\2026-07-29-mobile-safety-map.md`
- The georeference of the base imagery is now solved to roughly 50 m.

Known delivery constraint: **Squarespace cannot host a map tile pyramid.** The map
will live on GitHub or Cloudflare Pages as a standalone page and be embedded, with
QR codes pointing at the standalone URL. Squarespace Code Blocks need the Business
plan or above, which is not yet confirmed.

## Source material, already downloaded

Saved HTML of every live page is in this folder. Work from these files rather than
refetching, and use WebFetch only when you need something the HTML does not answer.

| File | URL path | Notes |
|---|---|---|
| `_home.html` | `/` | |
| `_vision.html` | `/vision` | |
| `_team.html` | `/team` | |
| `_nuestro-trabajo.html` | `/nuestro-trabajo` | "our work" |
| `_proyectos.html` | `/proyectos` | |
| `_programa-playa-organizada.html` | `/programa-playa-organizada` | organized beach program |
| `_lifesaving-club.html` | `/lifesaving-club` | largest page on the site |
| `_swim-club.html` | `/swim-club` | |
| `_freediving-club.html` | `/freediving-club` | |
| `_involcrate.html` | `/involcrate` | note the misspelling, it is in the live URL |
| `_donar.html` | `/donar` | donate |

`/nosotros` and `/unete` appear in the navigation markup but return **404**. Confirm
and flag: live navigation pointing at dead pages is a finding in its own right.

These are Squarespace pages, so the HTML is mostly framework noise. The useful parts
are the JSON blobs, `<h1>`/`<h2>`, the nav markup, `img` and `source` tags, and the
inline style/font declarations.

## House rules

- **No em dashes or en dashes in prose.** Hyphens in compound words are fine.
- Be specific and evidence-based. Quote the page and the line you are reacting to.
  "The hierarchy is unclear" is worthless; "the h1 on /proyectos is the org name
  rather than the project name" is useful.
- Say what is *good* as well as what is broken. This site was made by people who
  care, and the revamp has to survive their review.
- Do not invent facts about the organization, their programs, or the coast. If you
  need something you cannot verify, list it under "needs confirmation from AJ".
- Recommendations must be actionable inside Squarespace unless you say plainly that
  they are not.

## Deliverable

One markdown file, in this folder, named as your task specifies. Lead with your
three highest-value findings. Do not pad.
