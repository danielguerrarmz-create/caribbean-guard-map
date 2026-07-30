# 06 Accessibility and safety-critical correctness

Reviewer: Lelouch. Scope: the saved live site (`_*.html` in this folder) and the
draft safety map (`C:\Users\danie\caribbean-guard\web\index.html`).

This is not a WCAG checkbox pass. The map's job is to tell a barefoot tourist
with one bar of signal whether they can swim. A presentation failure here has a
physical consequence, so I have separated findings that **block launch** from
findings that can follow, and I have not softened the blockers.

---

## The three findings that matter most

**1. The map can silently tell someone the wrong beach is safe.**
`index.html:386-389` auto-opens a full-screen safety verdict for whichever zone
has the nearest vertex, if that vertex is within 450 m. The Cocles zone ends at
`9.6452,-82.7228` and the Chiquita zone begins at `9.6448,-82.7190`. That is
**419 m apart**, which is *less than the 450 m trigger radius*. Cocles is
`danger`, Chiquita is `caution`. So there is a stretch of coast where both
qualify and the winner is decided by a few metres of vertex geometry, on top of
a georeference the file itself labels `PLACEHOLDER` (`index.html:165`) and a GPS
fix. The user is not asked to confirm. They are shown a verdict. Nothing in the
interface signals that the verdict was guessed. **Blocks launch.**

**2. Every hazard verdict on the map is placeholder prose with no author and no
date, presented with the visual authority of an official assessment.**
The `ZONES` block (`index.html:172-223`) declares "NO NADAR", "la zona más segura
para familias y niños", "Guardavidas de 9:00 a 17:00" and "Banderas rojas marcan
los canales activos". The handoff is explicit that all of it was written from
general knowledge, not by Caribbean Guard's guards. There is no author field, no
assessment date, no review date, and no UI anywhere that says who decided this.
A public map that says DO NOT SWIM must be able to say who said so and when.
**Blocks launch.**

**3. The map is one CDN request away from a dark blue void, and it tells the user
it works offline when it does not.**
Leaflet is loaded from `unpkg.com` (`index.html:8` and `157`) with no SRI, no
fallback and no self-hosted copy. If that request fails on beach signal, `L` is
undefined, the inline script throws at line 258, `buildPicker()` never runs, and
the page renders `body{background:var(--ink)}` (#0b1c2c) with a brand label and a
911 button. No beach names, no statuses, no explanation. Separately, the page
opens with a toast reading *"Guarde esta página. La señal es débil en la playa"*
/ *"Save this page. Signal is weak on the beach"* (`index.html:244`, `251`), but
there is no service worker, no manifest, and no cache. The artifact instructs the
user to do something it has not implemented. **Blocks launch.**

---

# Part one: the existing site

## Severity table

| # | Severity | Finding | Evidence |
|---|---|---|---|
| S1 | High | Donation bank details are an image of text, and the alt text is broken and truncated mid account number. **Downgraded from Critical:** `/donar` carries the same details as real text, so a blind donor is not blocked | `_home.html:3488-3514`, asset `CG-C833D` |
| S2 | Critical | The organisation's stated emergency phone number is the same number as its Sinpe Móvil donation line, labelled differently on two pages | `_involcrate.html:1954`, `_donar.html:1895` |
| S3 | High | No phone number anywhere is a `tel:` link. One `mailto:` on the whole site. | grep across all 13 pages |
| S4 | High | `lang="es-AR"` on every page of a Costa Rican site | `_home.html:2`, `_donar.html:2`, all pages |
| S5 | High | The site is Spanish only, and tourists are who drown | BRIEF, and no `lang="en"` content found |
| S6 | Medium | `<meta name="description" content="" />` empty | `_donar.html:21` |
| S7 | Medium | Bank details and IBANs contain `&nbsp;` inside the number groups | `_donar.html:1895` |
| S8 | Low, and good | No `user-scalable=no` or `maximum-scale` anywhere; pinch zoom works | grep returned zero matches across all 13 files |
| S9 | Critical | **There are no forms anywhere on the site.** No contact, no volunteer, no newsletter, no donation form | zero matches for `<form`/`<input`/`<label` across all 13 pages |
| S10 | High | Eight of thirteen pages have no `h1`. Home has four (two empty). `/vision` marks a decorative `*` as `h1`. `/donar` starts at `h3` | `_home.html:1939,2760`, `_vision.html:2022,2028`, `_donar.html:1895` |
| S11 | High | `/nosotros` and `/unete` are 404 pages, and the 404 page has no heading, a title that says only "Caribbean Guard", and two "click here" links | `_nosotros.html:9,1615-1620` |
| S12 | High | Mobile menu has no `aria-expanded` or `aria-controls`, and both of its accessible names are `hidden` | `_home.html:949-951`, zero matches for `aria-expanded` |
| S13 | Low, and good | A working Spanish skip link is the first focusable element | `_home.html:629-634` |
| S14 | High | Squarespace writes `alt` **twice, empty first**, so 47 of 103 images are effectively unlabelled and 8 have no `alt` at all. The site looks tagged in the editor and is silent in practice | `_team.html` carousel markup; per-asset table in `03-image-register.md` |
| S15 | Critical | Home page `load` **59.2 s** on Slow 3G, FCP **11.2 s**, from a paused video block buffering ~50 MB | measured, see S15 |

## S1. The donation instructions are a JPEG

The home page presents the entire "how to donate" block as an image
(`image-asset.jpeg`, 1044x1210) with the payment details baked into the pixels.
The `alt` attribute carries a copy of that text, and this is where it goes wrong:

```
alt="Ayudenos a seguir salvando vidas 🛟❤️&amp;zwj;🔥🙌🏼

&amp;iquest;Como podes donar?

Paypal
caribbeanguard.pv@gmail.com

Banco Nacional de Costa Rica
Asociaci&amp;oacute;n Caribbean Guard
&amp;bull; C&amp;eacute;dula Juridica:
3-002-881795

Cuenta en US d&amp;oacute;lares
2"
```

Four separate failures in one attribute:

- **It is double-escaped.** `&amp;iquest;`, `&amp;oacute;`, `&amp;eacute;`,
  `&amp;bull;` will be announced literally. A screen reader user hears
  "ampersand i q u e s t semicolon Como podes donar". Every accented Spanish
  character on the site's primary donation asset is broken in the accessible copy.
- **It is truncated.** The string ends `Cuenta en US dólares\n2`. A blind user is
  given the first digit of a bank account number and nothing else. That is worse
  than no alt text, because it looks like information.
- **It is a content dump in an alt attribute.** Fifteen lines including four
  emoji read as one unbroken utterance. Alt text is for describing an image, not
  for carrying the page's primary content.
- **It fails WCAG 1.4.5 Images of Text.** There is no functional reason for an
  account number to be a raster image. It cannot be selected, copied into a
  banking app, zoomed without pixelation, browser-translated, or read by a
  password manager.

**Severity: High, not Critical, and the report should say why.** Edward checked
`/donar` and the same details are all there as real selectable text: both IBANs
(`CR93 0151 0932 0020 0328 81`, `CR17 0151 0932 0010 0856 38`), the cédula
`3-002-881795`, and the PayPal address. So a blind donor is **not prevented from
donating**. They just cannot do it from the prompt they were shown on the home
page. An accessible alternative exists on another page, and a reviewer who checks
will find it, so claiming Critical here would cost the report credibility on the
findings that genuinely are.

**It is not a placed donation block. It is asset `CG-C833D`, one of the 16
Instagram feed tiles.** That changes the fix. There is no gallery image to swap
for a text block, because the image arrives from the Instagram feed, and the
double-escaping and the ~300 character truncation are both properties of that
feed integration. See S14: removing the feed block is the only fix, and it is
already T0b-9.

**Fix:** removing the Instagram block deletes this asset along with the other 15.
That leaves the home page with **no donation prompt at all**, so the revamp has
to add a real one: a text block or button linking to `/donar`, not an image. Also
strip the `&nbsp;` characters out of the IBAN groups on `/donar` (S7), because
some banking apps reject a pasted U+00A0.

## S2. One phone number, two contradictory labels

On `/involcrate`:

```html
<p>Teléfono de emergencias: +506 8339 6566</p>
```

On `/donar`:

```html
<p>Sinpe Móvil</p><p>+506 8339 6566</p>
```

Same digits. On one page it is the emergency line, on the other it is the mobile
payment account. A visitor cannot tell which it is, and neither page tells them
the other role exists.

This matters for the map. My brief asks whether the emergency affordance is
right, and the honest answer is that Caribbean Guard's own fastest contact is a
number the site presents ambiguously and never makes tappable. For a rip current
in progress, a guard 600 m up the beach with a board is faster than a 911
dispatch. But I will not put a number on a public map that thousands of tourists
may call until AJ confirms what it actually is, who answers it, and during what
hours. **Listed under "needs confirmation from AJ".**

Note also that the emergency number appears on `/involcrate`, the get-involved
page, which is the last place someone in trouble would look. It is not on the
home page and not in the footer.

## S3. Nothing is tappable

A grep for `tel:`, `mailto:`, `whatsapp` and `wa.me` across all thirteen saved
pages returns exactly one hit: the `mailto:` on `_involcrate.html:1954`. The
phone number is plain text on both pages that carry it. The Instagram handle
`@caribbeanguard` is plain text, not a link. On a phone, the primary contact
methods of a rescue organisation cannot be actioned with a tap.

There is also `<a href="http://www.caribbeanguard.org" target="_new">` on
`_involcrate.html:1954`: plain HTTP, a non-standard `target` value, and a link
from the site to itself.

**Fix:** `tel:+50683396566`, `mailto:`, and `https://wa.me/50683396566` if
WhatsApp is used, in the footer of every page. In Costa Rica WhatsApp is the
default contact channel and the site has none.

## S4. `lang="es-AR"`

Every page opens:

```html
<html xmlns:og="..." xmlns:fb="..." lang="es-AR">
```

Argentine Spanish on a Costa Rican organisation's site. Squarespace is separately
serving `es-419` locale assets
(`_nosotros.html:244`, `...-min.es-419.css`), so the site is internally
inconsistent about its own locale. The practical effect is that a screen reader
selects an Argentine voice and pronunciation for Costa Rican content, and
translation tooling is given a wrong regional signal. The copy does read as
voseo in places (`¿Como podes donar?` rather than `¿Cómo podés donar?`, itself
missing both accents), so the tag may reflect who wrote it.

**Fix:** set the site language to `es-CR` in Squarespace site settings. One
setting, all pages.

## S5. Spanish only, on a page whose audience drowns

This is the IA specialist's territory more than mine, but it has an
accessibility dimension worth stating plainly: `lang` correctness is meaningless
if the language itself is wrong for the reader. The map already solves this
correctly with `navigator.language` detection and an ES/EN toggle. The site does
not. Any safety content that lands on the Squarespace side needs the same
treatment or it will not be read by the people it is for.

## S9. There are no forms on this website. At all.

A grep for `<form`, `<input`, `<label` and `<textarea` across all thirteen saved
pages returns **zero matches**.

My brief asked me to check form labels on the donate and contact flows. There is
nothing to label. There is no contact form, no volunteer signup, no newsletter
capture, and no donation form. Every conversion path on the site terminates in
plain text that the user must retype into another application:

- **Donate:** copy a 17-digit account number or a 22-character IBAN out of a
  paragraph, or send PayPal to a Gmail address. No button, no checkout, no card.
- **Volunteer or contact:** copy an email address, or open Instagram.
- **Emergency:** read a phone number and dial it manually.

Severity: **Critical**, and it is the same root cause as S1 and S3. This site
cannot be *actioned* from a phone. Every path requires the user to leave, switch
app, and retype something without a typo. For a donor that is friction. For
someone trying to reach a rescue organisation it is worse.

This is fixable inside Squarespace without a plan upgrade: Squarespace Form
Blocks are available on every plan and generate labelled fields. That single
change closes the contact, volunteer and newsletter gaps.

## S10. Heading structure

| Page | h1 | Problem |
|---|---|---|
| `_home.html` | 4 h1 elements | `"Caribbean Guard: Salvando Vidas"` (1939), `"Nuestra misión"` (2760), plus **two empty h1s** at 2760 with `data-rte-preserve-empty="true"` |
| `_vision.html` | 2 h1 elements | Both are **scrolling marquee decoration**: `"VISION"` (2022) and, separately, `"*"` (2028). A decorative asterisk is marked up as a top-level heading |
| `_nuestro-trabajo.html` | 1 | The h1 is a **quotation**, not the page subject: `"Quien salva una vida, salva al mundo entero."` (2017) |
| `_lifesaving-club.html` | 1 | `"LIFESAVING CLUB"` (2029). Correct |
| `_swim-club.html` | 1 | `"SWIM CLUB"` (2227). Correct |
| `_team.html` | **none** | |
| `_proyectos.html` | **none** | |
| `_programa-playa-organizada.html` | **none** | |
| `_freediving-club.html` | **none** | |
| `_involcrate.html` | **none** | Top heading is `<h2>Contáctanos</h2>` (1954) |
| `_donar.html` | **none** | Starts at `<h3>¿Por Qué Donar a Caribbean Guard?</h3>` then `<h4>Cómo Donar</h4>` (1895). No h1, no h2 anywhere on the page |
| `_nosotros.html` | **none** | No h1, h2 or h3 at all |
| `_unete.html` | **none** | Same |

Eight of thirteen pages have no h1. A screen reader user navigating by heading,
which is the primary navigation mode for most screen reader users, gets no entry
point on the donate page, the team page, the projects page or the get-involved
page. `_donar.html` skipping straight to h3 also breaks the level sequence.

The two empty h1s on the home page are announced as blank headings, and the
`"*"` h1 on `/vision` is announced as "asterisk, heading level 1". These are
Squarespace RTE artifacts, and both are fixable in the editor.

## S11. `/nosotros` and `/unete` are 404 pages, and the 404 page is itself broken

The brief asked me to confirm this. **Confirmed.** Both saved files are the
Squarespace error page:

```html
<li>La página que estás buscando cambió de ubicación o fue eliminada.</li>
<p>
 Para volver a tu página de inicio <a href="/">haz clic aquí</a>, o puedes intentar buscar el
 contenido que deseas <a href="/search">aquí</a>.
</p>
```
`_nosotros.html:1615-1620`, identical at the same line numbers in `_unete.html`.

Live navigation pointing at dead pages is a finding in its own right, and the IA
document owns that. What I add is that the error page a user lands on has three
accessibility failures of its own:

1. **The `<title>` is `Caribbean Guard`** (`_nosotros.html:9`), not "Página no
   encontrada". A screen reader announces the organisation name on page load. The
   user is given no signal that they hit a dead end. Sighted users at least see
   the error text; screen reader users navigating by title or heading get
   nothing, because...
2. **There is no heading at any level on the page.**
3. **Both recovery links are non-descriptive**: `haz clic aquí` and `aquí`. These
   are the textbook example. Out of context, a link list reads "here" and "here".

Squarespace lets you set a custom 404 page. That page should have an h1 reading
"Página no encontrada", a title to match, and links reading "Ir al inicio" and
"Buscar en el sitio".

## S12. The mobile menu

The burger is a real `<button>`, which is the right start:

```html
<button class="header-burger-btn burger" data-test="header-burger">
  <span hidden class="js-header-burger-open-title visually-hidden">Abrir menú</span>
  <span hidden class="js-header-burger-close-title visually-hidden">Cerrar menú</span>
```
`_home.html:949-951`

Two problems:

- **Both accessible names are `hidden`.** The `hidden` attribute removes an
  element from the accessibility tree. Squarespace's JS is expected to unhide the
  correct one, so the button's name depends on script execution. Before that runs,
  or if it fails, the control is an unnamed button.
- **There is no `aria-expanded` and no `aria-controls` anywhere in the page.** A
  grep for both across `_home.html` returns zero matches. A screen reader user
  cannot tell whether the menu is open or closed, which is the single most
  important piece of state a disclosure control has.

`aria-expanded` on a Squarespace burger is not editable without code injection,
so this one is **not** actionable inside Squarespace on the current plan. Flagging
it as a platform limitation rather than a to-do.

**Genuinely good:** there is a working skip link, in Spanish, as the first
focusable element:

```html
<a href="#page" class="header-skip-link sqs-button-element--primary">
  Saltar al contenido
</a>
```
`_home.html:629-634`

That is better than most small nonprofit sites manage, and it should survive the
revamp.

## S14. Alt text: Squarespace writes `alt` twice, empty first, so the site looks tagged and is silent

Credit to Edward, who found the mechanism while building the image register. His
per-asset audit supersedes my first count and corrects my framing, so I am using
his numbers. Full table with stable asset IDs:
`C:\Users\danie\caribbean-guard\docs\site-revamp\03-image-register.md`, column
"Alt".

**Squarespace 7.1 emits the `alt` attribute twice on every list, carousel and
gallery image, empty first:**

```html
<img data-image-focal-point=","
     alt=""
     data-src=".../aj.jpg" data-image-dimensions="2315x3087"
     data-image-focal-point="0.5,0.5" alt="aj.jpg"
     class="user-items-list-carousel__media" ... />
```
`_team.html`, AJ Smith's portrait

Duplicate attributes are invalid HTML and the parser keeps the **first**
occurrence, so the effective alt is `""`. The site looks fully alt-tagged in the
editor and is unlabelled in practice. That gap between what the editors see and
what a screen reader gets is the reason this went unnoticed.

Across all 13 pages, 103 `<img>` tags:

| Effective state | Count |
|---|---|
| First `alt` empty, so effective alt is blank | **47** |
| No `alt` attribute at all | **8** |
| A filename appears in some `alt` | 38, but see below |
| Malformed `data-image-focal-point=","`, forces centre-crop | 31, including all 17 team portraits |

**Correction to my earlier framing.** I first reported these 38 as "announced as
filenames". That is wrong for most of them: where the empty `alt` wins, they are
announced as *nothing*. The distinction matters because the fix is the same but
the symptom is not, and 47 silent images is a larger number than 38 noisy ones.

**The one place where the filename does win** is `/involcrate`, where it lands
first, so a screen reader genuinely reads out
"WhatsApp Image 2024 dash 09 dash 30 at 17 dot 35 dot 17 dot jpeg". That is worse
than silence.

**The team page is the sharpest case.** It exists to introduce the people who run
the organisation, and to a screen reader user it introduces nobody.

**The Instagram feed on the home page cannot be fixed in the editor.** Its 16
tiles carry the IG caption double HTML-escaped: the raw markup is
`alt="Atenci&amp;oacute;n Caribe Sur ..."`, so the parsed alt is the literal
string `Atenci&oacute;n Caribe Sur`. Every accented character is mangled.

**This is the same defect as S1**, where the donation JPEG's alt contains
`&amp;iquest;` and `&amp;oacute;`. So the double-escaping is systematic to how
this site's image alt text is generated, not a one-off authoring slip. Any
revamp that keeps the feed block keeps the bug. Removing the block is the only
fix.

**Fix:** per-image alt is editable in the Squarespace editor for the ordinary
image blocks, so the 17 team portraits are 17 edits (name and role, "Elias,
guardavidas", not the filename). Setting a real alt should resolve the duplicate
attribute at the same time, but verify on a live render rather than assume.
The Instagram block has to go.

### This bug was hiding the project's most valuable asset

The strongest argument for fixing S14 is not a conformance one. Caribbean Guard's
own annotated hazard maps were already published on
`/programa-playa-organizada`, with 11 rip currents and 4 rescue stations drawn on
them by the people who actually work that coast. **Both carry `alt=""` for exactly
the reason documented above**, the carousel block emitting two `alt` attributes
with the empty one winning.

So the single thing this entire project was missing, attributed hazard data from
the guards rather than placeholder prose, was sitting on the public site the whole
time, made invisible by an accessibility defect. It has now been georeferenced
(294 RANSAC inliers, 1.2 m median residual) and extracted to
`web/data/cg-hazards.geojson`.

An alt-text bug is usually framed as a cost to blind users. Here it also cost the
sighted project team, because nothing indexed, searched, or summarised that image
either. Worth putting in front of Caribbean Guard in those terms, because it is a
far more persuasive case for the fix than a WCAG citation, and because it is true
rather than rhetorical.

**Attribution, because this one took three parts and no single part would have
got there.** The duplicate-`alt` mechanism came out of Edward's parse of the
saved HTML. The georeferencing and extraction into `cg-hazards.geojson` were done
separately with `tools/georef_annot.py` and `tools/extract_annotations.py`. The
framing above, that this is the sentence to say to Caribbean Guard, is mine. The
register records it the same way.

### Settled: the malformed focal point is not cutting anyone's face

Recording this so it is not re-raised as a suspicion later. I flagged that
`data-image-focal-point=","` on all 17 team portraits means the crop is
*unreviewed* rather than deliberately centred, and worried that faces were being
cut. Edward tested it rather than reasoning about it: he fetched all 17 assets,
applied the same centre square crop Squarespace applies, and checked the contact
sheet.

**All 17 contain a complete, unobstructed face**, including Tapas at a 54%
horizontal discard and Elías at 44% vertical. People centre themselves in
photographs, so the centre crop gets lucky. Per-portrait discard percentages are
in `03-image-register.md` under "Portraits of real people".

The real problem is one no focal point can fix: **framing variance in the source
photographs.** Several are full-body shots where the face is a small fraction of
a 300 px circle, and at least five of seventeen are wearing sunglasses. That
makes the alt text *more* load-bearing, not less, because the image itself
conveys less about who the person is. It also means a subset of these people need
to be rephotographed, which is a content task with a lead time, so it should be
raised with Caribbean Guard early rather than discovered during the rebuild.

## S15. The home page takes 59.2 seconds to load on Slow 3G

Measured by Edward, not asserted: **`load` at 59.2 s, first contentful paint at
11.2 s on Slow 3G**, because a native Squarespace video block buffers roughly
50 MB while paused.

I am ranking this **Critical**, and treating it as an accessibility finding
rather than a performance one, for two reasons.

**It fails WCAG 2.2 in its own right.** Content that is unreachable on a slow or
metered connection is unavailable to users who are on one, and in Limón province
that is a large share of the audience, not an edge case. A 50 MB autobuffer on a
paused video is also a real financial cost to a user on a prepaid data plan.

**More importantly, it settles an open design question.** The whole premise of
this project is a barefoot tourist on one bar of signal who needs an answer in
about two seconds. An 11.2 s first paint is roughly five times over that budget
before the map has even been requested. That means:

- **No safety-critical content may live on the Squarespace page.** Not the map,
  not a summary of the map, not a "check conditions" panel. The Squarespace site
  can point at safety information; it cannot be the thing that delivers it under
  pressure.
- **This is now the strongest argument for the standalone map host**, stronger
  than the tile-pyramid constraint that originally drove that decision. The QR
  codes must resolve to the standalone URL, and that is a correctness
  requirement, not a convenience. It is already in Tier 1.
- **It sets the budget for the map itself.** If Squarespace is 11.2 s to first
  paint, the map has to be dramatically better, which means self-hosted Leaflet
  (F1), a static no-JS beach list (F2), and `base-lo.jpg` first (F3). Those three
  were already Tier 0. This is the measurement that justifies them.

### `/donar` is the sharper number, because there is no video to blame

Also measured by Edward, per-page table in `03-image-register.md`:

| `/donar` | Weight |
|---|---|
| Images | 66 KB |
| **Squarespace framework JavaScript** | **910 KB** |
| Total | 1,162 KB |

**On eight of eleven pages the framework JS outweighs every image combined.**

The conversion path is roughly 1.2 MB of framework before a single donation
detail renders, and none of it is content. This matters more than the 59.2 s
figure because it establishes a **floor**. The video block is removable. The
910 KB of Squarespace JavaScript is not: it is the platform, it is not reducible
in the editor, and no amount of image optimisation touches it.

So the conclusion above hardens. It is not "the home page is slow and we should
fix it". It is **"this platform cannot deliver a two-second answer, and no work
inside it will change that"**. Optimising images on these pages is close to
pointless while the framework is fourteen times the weight of the imagery.

**Fix:** remove or lazy-load the video block, which recovers the worst of the
home page. Then set a page weight budget for the revamp, with the explicit
caveat that roughly 910 KB of it is spent before you start. If the video block
cannot be stopped from buffering while paused, replace it with a poster image
linking to the video.

## Site-wide positives worth protecting

- No `user-scalable=no` and no `maximum-scale` on any page. Pinch zoom works
  everywhere. Zero matches across all thirteen files.
- The skip link above.
- `/donar` carries the payment details as correctly accented real text, which is
  the correct version of the content the home page renders as a broken JPEG.
- Squarespace emits `<noscript>` fallbacks for its lazy-loaded images, so the
  gallery content survives with JS disabled.

---

# Part two: the safety map

`C:\Users\danie\caribbean-guard\web\index.html`

> **Implementation status, 2026-07-30.** The map was substantially rewritten
> while this review was in progress, and most of Tier 0 is now closed. The
> sections below are kept because they record the reasoning and the measurements,
> but read this box first for what is actually still open. Everything here I
> verified against the current file, not against the handoff.
>
> **Closed and verified:** the 450 m auto-open is gone, replaced by an ambiguity
> prompt ("Está entre dos playas. Toque el nombre de la playa donde está"); real
> georeference bounds with `GEO_ACCURACY_M` 75 and `GEO_ACCURACY_EAST_M` 150,
> combined with GPS error in quadrature; `reviewed: {by, on}` or `reviewed: null`
> on every zone with a `REVIEW_VALID_DAYS = 120` staleness downgrade rendering
> through `.prov.unverified`; the toast now has `role="status"
> aria-live="assertive"`; the legend is rendered as a per-card swatch drawing the
> real map stroke; stroke polarity inverted so danger is the heaviest mark
> (11 px unbroken) and safe the lightest (5 px fine dots); progressive
> `base-lo.webp` then `base.webp`.
>
> **Still open from Tier 0:** Leaflet is still loaded from `unpkg` with no SRI
> and no self-hosted copy (lines 8 and 186), so **F1 is unchanged and remains the
> single worst failure mode**. There is still no `<noscript>` (F2). The emergency
> button is still `min-height:40px` and still adjacent to the language toggle
> (line 60), so T0-12 is unchanged.

## The one thing the palette fix did not carry over

The two-tier colour split is the right resolution and I want to be clear that it
works **on the map**. Verified from `COLOR` at line 336:

| Tier | Safe | Caution | Danger | Separation |
|---|---|---|---|---|
| Map lines (`COLOR`) | `#1f9d55` L 0.251 | `#f5b942` **L 0.545** | `#c62828` L 0.137 | monotonic, caution brightest, 1.98:1 / 1.61:1 / 3.19:1 |
| Pill fills (`--*-text`) | `#178049` L 0.161 | `#9c5c00` L 0.147 | `#c62828` L 0.137 | **1.07:1 / 1.06:1 / 1.13:1** |

On the map the fix is real: caution is now the brightest of the three, all three
separate by brightness alone, and weight and dash pattern reinforce it. My
original concern is resolved there.

**The `.status` pill in the bottom sheet did not get the same treatment.** Lines
106 and 107 fill it with the *text* tier, so all three pill backgrounds sit
within **1.13:1** of each other. In greyscale the pill is one colour.

Two honest qualifications, because this should not be over-ranked:

- **It is not a safety failure.** The pill always contains the word,
  "NO NADAR" / "PRECAUCIÓN" / "SE PUEDE NADAR", and the user reached the sheet by
  tapping a specific beach whose card already carried a well-separated swatch. The
  meaning is carried. It is the *colour* that has stopped saying anything.
- **It is narrower than my earlier draft implied.** Every other surface is fixed.

But it is worth the two lines it costs, for one reason beyond contrast: the map
now teaches an intensity ramp, safe lightest through danger heaviest, and the
pill contradicts it by making all three the same darkness. The pill is the
largest colour object in the sheet and it is the one place the ramp breaks.

**Fix:** give the pill the map tier for its field and pick the text colour per
tier, so the pill mirrors the stroke.

```css
.status.caution{background:var(--caution); color:#111}  /* 11.9:1, and brightest */
```

`#f5b942` with near-black text measures **11.9:1**, comfortably AAA, and restores
caution as the brightest of the three in the sheet exactly as it is on the map.

## What is already right

Worth stating before the criticism, because these are correct instincts and the
revamp should not undo them.

- **The beach picker instead of a legend.** Status is visible before anything is
  tapped, and the navigation is beach *names*, which is what the person actually
  knows because it is on the sign behind them. This is the single best decision
  in the file.
- **Cover, not contain** (`fitCover()`, lines 270-274). No dead grey bands on a
  portrait phone.
- **Language auto-detect with ES fallback** (line 253).
- **The intent to encode status redundantly** (lines 284-287, and the comment
  above them). The intent is right. The execution does not survive contact with
  a phone in the sun, which is section 2.1.
- **`rel="noopener"`** on both external links. Correct.
- **911 is permanently visible**, not buried behind a tap.

## 2.1 Does the status encoding survive the real world?

Short answer: **no, not yet**, and the reason is not the one the code comments
assume.

### The colour numbers

I computed these independently and they agree exactly with `02-visual-system.md`,
which is a useful cross-check:

| Token | Hex | Relative luminance | White text on it | Verdict |
|---|---|---|---|---|
| `--safe` | `#1f9d55` | 0.2506 | **3.49:1** | Fails AA 4.5:1 |
| `--caution` | `#c77700` | 0.2535 | **3.46:1** | Fails AA 4.5:1 |
| `--danger` | `#c62828` | 0.1367 | 5.62:1 | Passes AA |

The `.status` pill is `font-size:13px; font-weight:800` (line 86). Bold 13px does
not qualify for the 3:1 large-text exception, which needs roughly 18.66px bold.
The same two colours are used as *text* colours at **11.5px** on the picker cards
(`.card .st`, line 60), which is the label a person reads to make the decision.

### The failure that matters more than contrast

**All three statuses sit within 1.6:1 of each other in luminance, and safe and
caution are 1.01:1 apart.** Convert the screen to greyscale, which is what glare,
a cheap panel, a cracked screen and a polarised sunglass lens all approximate,
and `#1f9d55` and `#c77700` are *the same colour*. Under deuteranopia they also
converge in hue. So on the picker card the encoding degrades to the text label
alone, and the text label is 11.5px at 3.46:1.

The `.dot` swatch (line 63) is an 11px rounded square, identical in shape for all
three statuses, differing only by fill. It carries no redundant information at
all.

### The line patterns are documented nowhere and point the wrong way

Two problems with `dashArray:"2 13"` for danger and `"18 9"` for caution
(lines 286-287):

- **There is no legend.** `T.es.legendSafe`, `legendCaution` and `legendDanger`
  are defined at lines 239 and 246 and **never referenced anywhere in the file**.
  The pattern vocabulary is undocumented in the UI. A user cannot learn that
  dotted means stop.
- **The polarity is inverted.** Dotted is visually the *lightest* mark on the
  map and it means the most dangerous thing. Solid is the *heaviest* mark and it
  means safe. Every other visual convention a tourist carries, road markings,
  hazard tape, warning signage, says the loud mark is the dangerous one. At a
  glance the map currently shouts safety and whispers danger.

### Screen reader

- The zone polylines are Leaflet SVG `<path>` elements with a click handler only
  (`hit.on("click")`, line 290). No `tabindex`, no role, no accessible name. A
  screen reader user gets nothing from the map graphics.
- The base image alt is `{alt:"Costa de Talamanca"}` (line 264). It describes the
  photograph, not the safety information, and it is hardcoded Spanish that never
  updates on language switch.
- Post markers use `L.divIcon` with inner text `1`, `2`, `3`, `4` (line 295).
  Leaflet's `Marker` defaults to `keyboard: true`, which sets `tabIndex = '0'`
  and `role="button"` on the icon element, and the `alt` option is applied
  **only** to `<img>` icons, not divIcons. So the map contributes four focusable
  buttons whose entire accessible name is a single digit.
- **The bottom sheet is always in the accessibility tree.** It is hidden with
  `transform:translateY(102%)` (line 79), not `display:none` or `aria-hidden`.
  Before any tap it is a `role="dialog"` containing an empty body and a "Cerrar"
  button that a keyboard user will tab into and that does nothing.
- **Opening the sheet announces nothing.** `sheetBody.innerHTML = ...` swaps
  content silently. Focus is never moved into the sheet, Escape does not close
  it, and focus is never returned. A screen reader user taps a beach card and
  receives no feedback that a verdict was rendered.
- **The toast has no `aria-live`.** `#toast` (line 140) is a plain div.
  `say()` is how the map communicates "Buscando su ubicación", "Active la
  ubicación", "Usted está fuera de esta costa" and the offline advice. All of it
  is invisible to assistive technology, and all of it is safety-relevant.
- `aria-label="Mi ubicación"` (line 142) and `aria-label="Cerrar"` (line 153) are
  hardcoded Spanish and are never updated by `setLang()`. An English user gets
  Spanish control labels. So does `role="group" aria-label="Idioma"` (line 134).
- `<title>` never changes language either.
- There is no `<h1>`; the sheet uses `<h2>` (line 89) with no `h1` above it. There
  are no landmarks, no `<main>`.
- `.grab` (line 83) draws a drag handle. The sheet has no drag handlers. The
  affordance is a lie.

### Recommendation: three tiers, not three hues

You cannot fix this by retuning hues, and I want to flag a problem with the fix
proposed in `02-visual-system.md`. That document moves `--caution` to `#9C5C00`
to clear text contrast. That does clear contrast, but `#9C5C00` has luminance
**0.147** and `--danger` `#c62828` has luminance **0.137**. The two are then
**1.06:1 apart**. The safe/caution collision is solved by creating a
caution/danger collision, and caution versus danger is the more expensive pair to
confuse. Any all-dark-on-white palette hits this wall, because the AA floor
pushes every token into the same narrow luminance band.

The way out is to vary the **field**, not just the ink. Three tiers, monotonic
from light to dark, with shape and word carrying the same signal:

| Status | Field | Text | Field luminance | Text contrast | Shape | Word |
|---|---|---|---|---|---|---|
| Safe | `#FFFFFF` paper, dark green 2px border | `#0A5C2E` | 1.000 | 8.13:1 | filled circle | SE PUEDE NADAR / SWIMMING OK |
| Caution | `#F5A623` amber | `#111111` | 0.468 | 10.4:1 | triangle | PRECAUCIÓN / CAUTION |
| Danger | `#8C1111` near-black red | `#FFFFFF` | 0.060 | 9.5:1 | octagon or ✕ | NO NADAR / DO NOT SWIM |

Field-to-field separation: safe/caution 2.03:1, caution/danger 4.71:1,
safe/danger 9.53:1. Every pair separates in pure greyscale, the ordering is
monotonic light to dark so it reads as an intensity scale even with no colour
perception at all, and all three clear AAA 7:1 for text. AAA rather than AA is
the right bar here: 4.5:1 is an indoor baseline, and this is read in direct
equatorial sun.

Then:

- Give `.dot` three distinct **shapes**, not three fills.
- Make the danger chip physically larger than the other two.
- Invert the line weights. Danger should be the **thickest** stroke with a
  repeating hazard hatch. Safe should be the thinnest and plainest.
- **Render the legend.** The strings already exist at lines 239 and 246. Show
  them, with the shape and the line pattern beside each, collapsed by default and
  one tap away.
- Raise `.card .st` from 11.5px to at least 14px and `.status` from 13px to 16px.

## 2.2 What happens when it fails

A safety map that fails silently is worse than no map. Every mode below is
currently silent unless noted.

| # | Failure | Current behaviour | What the user must see |
|---|---|---|---|
| F1 | unpkg unreachable or slow | `L` undefined, script throws at line 258, empty picker, dark blue void with a 911 button | Self-host Leaflet. Then: the beach list and statuses must render from **static HTML** with the map as progressive enhancement, so the answer survives with zero JS |
| F2 | JavaScript blocked or broken | Same dark void. No `<noscript>` | A `<noscript>` block containing the full beach list, status, and the one-line why for each, plus 911 |
| F3 | `img/base.jpg` fails | `L.imageOverlay` has no error handler. Coloured lines float on blank white with no coastline | Wire `errorOverlayUrl:"img/base-lo.jpg"`, which **already exists** in `web/img/`, plus an `error` listener that shows a persistent banner: the map image did not load, the beach list below is still valid |
| F4 | No signal at all after first load | Nothing cached. Reload gives nothing | Service worker precaching Leaflet, `base-lo.jpg`, and the zone data. Until that exists, **delete the "save this page" toast**, which promises a capability that does not exist |
| F5 | Geolocation denied | `say(t.denied)`, a 5-second toast with no `aria-live` | A persistent state on the locate button, not a toast. And the picker already works without location, so say that: "choose your beach below" |
| F6 | Geolocation times out or is unavailable | The error callback at line 390 collapses **every** error code into "turn on location". Under jungle canopy a 9-second timeout is likely | Branch on `err.code`. Telling someone to enable a permission they already granted costs them time and trust |
| F7 | Position outside the image bounds | Lines 377-380 draw the marker and accuracy circle **before** the bounds check, then return without removing them. A stale dot persists off-screen behind `maxBounds` | Check bounds first, draw nothing, and show a persistent message |
| F8 | Page served over HTTP, or iframed without permission | `navigator.geolocation` requires a secure context, and cross-origin iframes are blocked by default: the embedding page must set `allow="geolocation"` on the iframe. Currently this fails into F5 and tells the user to enable a setting that will not help | HTTPS only, and the Squarespace embed must carry `allow="geolocation"`. Verify on the real page before QR codes are printed |
| F9 | `tel:` from inside a sandboxed iframe | Untested | Point the QR codes at the **standalone** URL, never the Squarespace embed. The brief already plans this; this is a second reason for it |
| F10 | Stale hazard data | No dates exist, so staleness is undetectable | See 2.4 |

Two more, lower severity:

- No `prefers-reduced-motion` guard on `flyToBounds` (line 320),
  `scrollIntoView({behavior:"smooth"})` (line 358) or the sheet transition.
- `html,body{overflow:hidden}` disables pull-to-refresh, which is the gesture a
  user will reach for when the page half-loads on bad signal.

**One forward-looking correctness issue.** `openZone` and `openPost` build the
panel with `innerHTML` and interpolate `z.why[lang]` and `z.facts[lang]`
directly. Today that data is a hardcoded const in the same file, so there is no
injection risk. The moment Caribbean Guard's guards author it, whether through a
JSON file or a CMS, this becomes an injection vector, and more immediately a
single `<` in a Spanish hazard description will silently break the panel. Move to
`textContent` and DOM construction **before** the data moves out of the file, not
after.

## 2.3 The georeference, and how to be honest about it

> **Numbers in this section are superseded, and the reasoning is not.** This was
> written against the pre-2026-07-30 file, when the working figure was "roughly
> 50 m" from the 07-29 handoff. The measured figures are now **75 m from Puerto
> Viejo to Punta Uva and 150 m east of it**, from `tools/residual.py`, and they
> are the constants in the code (`GEO_ACCURACY_M`, `GEO_ACCURACY_EAST_M`) and in
> `04-map-integration.md`. Where this section says 50 m, read 75 m, and the
> conclusions get stronger rather than weaker, because the dot was understating
> the error by more than I calculated.
>
> **Do not quote 4.0 m as the accuracy.** That figure in `tools/georef.json` is
> the RANSAC residual on 14 self-selected inliers out of 109 control points. It
> measures whether that subset agrees with the model, not whether the model is
> right on the ground. An earlier draft of `04-map-integration.md` read it as
> accuracy and concluded the georeference was twelve times better than it is;
> that section now carries an explicit correction. Internal consistency and
> ground accuracy are different claims.

### The current state is not shippable

`IMG_BOUNDS = [[9.6355,-82.7750],[9.6620,-82.6800]]` at line 165 carries the
comment `PLACEHOLDER`, and it is **not** the handoff's own best estimate
(`[[9.6240,-82.7922],[9.6667,-82.6416]]`). So the file ships a worse value than
the one already derived. Fix that regardless of everything below.

### The dot claims precision it does not have

At zoom 17 and latitude 9.65, ground resolution is **1.18 m per pixel**. So:

- A 50 m georeference error is **42 px** of radius.
- `meMarker` is drawn at `radius:8` (line 379), so **16 px** across.
- `meCircle` uses `radius: acc` (line 378), the **GPS** accuracy only. On an open
  beach with `enableHighAccuracy` that is typically 5 to 20 m, so 4 to 17 px.

The circle the user is shown is between 2.5x and 10x too small in radius, because
it omits the georeference error entirely. And `map.setView(ll, 17)` (line 383)
zooms in hard, which amplifies the impression of precision. Zooming past your own
uncertainty is a lie told by the camera.

### Recommendations

1. **Combine the two error terms.** Radius should be
   `sqrt(gpsAccuracy² + georefSigma²)`, roughly 52 m for a 15 m GPS fix against a
   50 m georeference. Publish `georefSigma` as a named constant.
2. **Make the sigma vary along the coast.** The west is good to roughly 50 m; the
   east toward Manzanillo is less certain. One number for 16.5 km of coast is
   itself a false precision. If the eastern sigma is genuinely unknown, either
   use a much larger disc there or disable position display east of the last
   validated control point and say why.
3. **Drop the crisp centre dot.** The primitive should read as "somewhere in
   here", not "here". A soft disc with no hard centre, or at most a very low
   contrast centre mark.
4. **Cap the auto-zoom** so the uncertainty disc is never smaller than about 25%
   of the viewport width. The camera must not out-zoom the error.
5. **Never auto-open a verdict.** Replace lines 386-389 with a confirmable
   prompt: *"You look like you are near Playa Cocles. Is that right?"* with the
   beach name, a confirm, and a "choose a different beach". The person standing
   on the sand knows the beach name from the sign. The map does not. Let the
   human be the authority.
6. **If the disc overlaps more than one zone, say so** and list them **worst
   status first**. Never render a single verdict from an ambiguous position.
7. **Use distance to the nearest point on the segment, not the nearest vertex.**
   The zone lines have three or four vertices over roughly a kilometre, so
   mid-segment the nearest vertex can be 250 m away while you are standing
   directly on the zone.
8. **State the accuracy in words** in the sheet: "Su ubicación es aproximada,
   unos 50 m" / "Your location is approximate, about 50 m", alongside a permanent
   line saying the sign on the beach and the lifeguard are the authority, not
   this map.
9. **Unassessed coast is a status.** Five zones cover 16.5 km. Between them the
   map currently says nothing, which reads as "no hazard". Render the unassessed
   stretches explicitly in a neutral grey with the word "sin evaluar / not
   assessed".

### The coverage claim is wrong

`T.es.outside` says *"El mapa cubre Puerto Viejo hasta Punta Uva"* (line 242).
The handoff establishes the base image reaches **Manzanillo**, roughly
-82.792 to -82.642. The shipped `IMG_BOUNDS` says something third. So the image
extent, the zone data and the message shown to the user are three different
answers, and someone standing at Manzanillo will be told they are outside a
coastline the map is in fact showing them.

## 2.4 Provenance: what the interface must show before this is public

Currently zero. `ZONES` has no author, no date, no source, no review interval.
Before publication the interface must carry all of the following.

1. **Per-zone attribution, visible in the sheet, not in a footer.** Who assessed
   it, as a named body and role, for example "Evaluado por los guardavidas de
   Caribbean Guard", the assessment date, and the last review date.
2. **A validity statement.** This is a general seasonal assessment, not today's
   conditions. The map cannot see the swell, the tide, or last night's rain.
3. **A statement of what it is not.** Not a live feed, not a substitute for the
   flags or the lifeguard on the beach.
4. **Automatic staleness downgrade.** If `reviewed` is older than an agreed
   interval, the UI must visibly say so. Silent stale safety data is the classic
   failure mode of this artifact class.
5. **A page version and last-updated stamp**, so a QR poster screwed to a post in
   2026 can be cross-checked against what it now resolves to.
6. **A correction channel.** One line, "report a problem with this map", going to
   a WhatsApp or email that a guard or a local will actually read.
7. **Move the data out of `index.html`.** As long as the authoritative safety data
   is a hand-edited const in an HTML file, the provenance claim cannot be
   maintained, because anyone with repo access can change a verdict and the page
   will look identical. It needs its own versioned data file with a named owner
   and a review workflow.

### Specific placeholder claims that must be verified or removed

These are checkable assertions currently presented as fact. Each one is a
promise the organisation is making to a stranger in the water.

- `"Guardavidas de 9:00 a 17:00"` on Cocles, and the identical hours on three
  `POSTS` entries. Every day? Year round? Who confirms?
- `"Banderas rojas marcan los canales activos"`. **If Caribbean Guard does not
  actually run a red flag system at Cocles, this sentence is an active hazard**:
  it tells a tourist to look for a signal that does not exist and to infer safety
  from its absence.
- `"La zona más segura para familias y niños"` on Playa Negra. This is the
  highest-liability sentence on the page: declaring a beach safest for children
  at a location with no lifeguard. It comes from the guards or it comes out.
- `"Puesto de rescate a 600 m al este"`, `"Arrecife a menos de 1 m bajo la
  superficie"`, `"Puesto de observación P.O. 4"`.
- Post 3 is `kind:"proposed"`. `.po.proposed` renders as dashed at 85% opacity
  (line 109), which at 30px on a phone is nearly identical to a staffed post. A
  tourist walks to a marker expecting a lifeguard and finds nothing. Either take
  proposed posts off the public map or make them unmistakable and label them.
- `openPost` renders `<span class="status safe">1</span>` (line 327): a green
  status pill containing a digit. It reads as a verdict and says nothing. It
  should read "CON GUARDAVIDAS 9:00-17:00" or "SIN PERSONAL".
- The page has the device clock and does not use it. "Abierto ahora" / "Cerrado,
  última patrulla 17:00" is cheap and high value.

**Licensing, flagged not asserted.** My project memory records the base sheet as
having been assembled from Google Earth tiles rather than drone imagery. If that
is right, publishing it as a public web map has redistribution implications that
could stop launch for reasons entirely unrelated to accessibility. Needs
confirmation before hosting.

## 2.5 The emergency call affordance

**911 is correct for Costa Rica.** It is the national emergency number covering
police, fire and ambulance, reachable from fixed lines, prepaid and postpaid
mobile, and VoIP, and the service operates bilingual Spanish/English call takers
specifically because of tourist volume. That last point matters here and is worth
surfacing to the user: an English-speaking tourist can be told the call will be
answered in English. `128` is the Cruz Roja direct line, but I would **not** add
it. One number, no decision, is the right design under panic.

**The `tel:` path works**, with caveats:

- `.sos` sits inside `.topbar`, which is `pointer-events:none` (line 27), but
  `.sos` sets `pointer-events:auto` (line 41). Correct.
- iOS Safari and Android Chrome both present a confirmation before dialling, so
  it will not silently place a call. Good.
- **Untested and must be tested:** the same link from inside the Squarespace
  iframe (F9 above).

**What is wrong with it:**

1. **The tap target is 40px.** `.sos` is `padding:9px 14px; min-height:40px`
   (line 43). This is the emergency control on a safety map. It should be 48px
   minimum.
2. **It is roughly 10px from the language toggle.** Two controls, adjacent,
   tiny, with wildly different consequences. The realistic mis-tap is a tourist
   reaching for EN and dialling Costa Rican emergency services. Separate them.
   Move 911 to its own reserved position with nothing else near it.
3. **Its accessible name is "911".** It should carry a language-aware
   `aria-label`: "Llamar al 911, emergencias" / "Call 911, emergency", with the
   visible text staying "911".
4. **Red is doing two jobs.** `.btn.primary` uses `var(--danger)` (line 100), the
   same red that means "do not swim". In a danger sheet the user sees a red
   status chip beside a red call button. Give the emergency action its own
   treatment, distinct from the hazard scale.
5. **Caribbean Guard's own number is absent**, see S2. Pending AJ's confirmation
   this is probably the more useful second action than Google Maps directions to
   a beach the user is already standing on.
6. **The directions button is close to useless.** `Cómo llegar` opens Google Maps
   to the midpoint of the zone you are standing in, and it needs signal to work.
   Directions to the **nearest staffed post**, or to the nearest clinic, would
   earn that slot.

---

# Launch gates

## Tier 0: block the map going public at all

| | Item | Section |
|---|---|---|
| T0-1 | Remove the 450 m auto-open verdict. Replace with a confirmable prompt | 2.3.5 |
| T0-2 | Real hazard data from Caribbean Guard's guards, with author and date, or the map does not publish | 2.4 |
| T0-3 | Provenance UI: author, assessed date, reviewed date, "not a live feed" statement | 2.4 |
| T0-4 | Self-host Leaflet, add a no-JS static beach list, add `<noscript>` | F1, F2 |
| T0-5 | Delete the "save this page" toast, or ship the service worker | F4 |
| T0-6 | Finish and validate the georeference, or ship with the locate button disabled and say why | 2.3 |
| T0-7 | Uncertainty disc that includes georeference error; no crisp centre dot; capped auto-zoom | 2.3.1-2.3.4 |
| T0-8 | Three-tier status system with shape and word redundancy; render the legend | 2.1 |
| T0-9 | Fix or remove the unverifiable claims, red flags and "safest for children" first | 2.4 |
| T0-10 | Fix the coverage string so the image, the zones and the message agree | 2.3 |
| T0-11 | `aria-live` on the toast; sheet focus management; language-aware control labels | 2.1 |
| T0-12 | Emergency button to 48px and moved away from the language toggle | 2.5.1, 2.5.2 |
| T0-13 | Remove the truncated, double-escaped donation image from the home page | S1 |

## Tier 0b: block the revamped Squarespace site going live

These are all editor-level changes, no plan upgrade needed, except where noted.

| | Item | Section |
|---|---|---|
| T0b-1 | Removing the Instagram block (T0b-9) also deletes the banking image. Add a real donation CTA to the home page to replace it, text or button, not an image | S1 |
| T0b-2 | Add a contact form and a volunteer form. There are currently none | S9 |
| T0b-3 | Make every phone number a `tel:` link and every email a `mailto:` link | S3 |
| T0b-4 | Resolve what +506 8339 6566 is, then label it once, consistently, everywhere | S2 |
| T0b-5 | One `h1` per page, matching the page subject. Eight pages currently have none | S10 |
| T0b-6 | Real alt text on the 17 team portraits and the rest of the 47 blank and 8 missing | S14 |
| T0b-7 | Fix or remove `/nosotros` and `/unete` in the navigation, and write a proper 404 page | S11 |
| T0b-8 | Set the site language to `es-CR` | S4 |
| T0b-9 | Remove the Instagram feed block. Its 16 alt strings are double-escaped and it is not editable | S14 |
| T0b-10 | Kill the ~50 MB paused-video buffer on the home page and set a page weight budget | S15 |

## Tier 1: before QR codes are printed and screwed to posts

Physical deployment is harder to reverse than a web deploy, so these get their
own gate.

- Verify `tel:911` and geolocation both work from the **real** Squarespace embed,
  with `allow="geolocation"` present, over HTTPS, on a real iPhone and a real
  Android, outdoors.
- Confirm the QR target is the standalone URL and that URL is stable.
- Put the page version and last-updated stamp in place first, so a poster can be
  audited later.
- Confirm the imagery licensing.
- Test at Manzanillo and at the Cocles/Chiquita boundary specifically, because
  that is where the geometry is worst.

## Fast follow

- Image overlay `errorOverlayUrl` fallback to `base-lo.jpg`.
- Branch geolocation errors on `err.code`.
- Fix the F7 stale-marker ordering bug.
- `prefers-reduced-motion` guard.
- Post "open now" / "closed" from the device clock.
- Move zone rendering from `innerHTML` to `textContent`, before the data leaves
  the file.
- Site-wide: `lang="es-CR"`, `tel:`/`mailto:`/WhatsApp links, page descriptions,
  strip `&nbsp;` from the IBANs.

---

# Needs confirmation from AJ

1. **What is +506 8339 6566?** The site calls it the emergency line on one page
   and the Sinpe Móvil donation account on another. Who answers it, during what
   hours, and is Caribbean Guard willing to have it on a public map that tourists
   will call? Until answered it goes nowhere near the map.
2. **Who authors hazard assessments**, by name and role, and how often are they
   reviewed? This determines the provenance UI and it blocks launch.
3. **Are the posts actually staffed 09:00 to 17:00?** Every day, all year?
4. **Is there a red flag system at Cocles?** If not, that line comes out.
5. **Is Playa Negra genuinely the safest stretch for children**, in Caribbean
   Guard's own judgement, and are they willing to publish that?
6. **Post 3 at Chiquita is marked proposed.** Should it appear on a public map at
   all before it is staffed?
7. **Where did the base imagery come from**, and is it licensed for public
   redistribution?
8. **Is there a nearest clinic or Cruz Roja station** worth routing to, and does
   Caribbean Guard want the map to point at it?
9. **Does Caribbean Guard use WhatsApp** as a contact channel, and on what number?
10. **Is the Squarespace plan Business or above**, which determines whether any of
    the Squarespace-side code fixes are possible at all.
11. **Staff portraits: do higher-resolution originals exist, and can a few people
    be rephotographed?** Ask these as **one question**, in this order, because the
    first may remove the need for the second. `03-image-register.md` item 5 is
    cross-referenced to this one; it is a single request and AJ should receive it
    once, not twice in two shapes from two documents.

    Several portraits are full-body shots where the face is a small fraction of a
    300 px circle, and at least five of seventeen are wearing sunglasses. A
    higher-resolution original solves the crop problem but not the framing or the
    sunglasses, so the answer to the first question determines how many people
    actually need rephotographing.

    **Raise this in the first conversation, not during the rebuild**, because
    rephotographing volunteers on a coast has a lead time measured in weeks and it
    is the only item on this list that cannot be compressed by working harder.

    **This is deliberately not a Tier 0 item**, and Edward and I disagreed about
    where it belongs. The site can launch with the existing photographs plus
    correct alt text, which is already T0b-6. Putting a weeks-long content
    dependency in the launch-blocking list would inflate the blocker set, and the
    credibility of that list is the reason it is useful. It is on this list
    instead because it needs to *start* early, which is a different thing from
    blocking launch.
