# Visual system and mobile design spec

Owner: Sai (design). Read `BRIEF.md` first. Evidence pulled from the saved HTML in
this folder and from the live draft map at `C:\Users\danie\caribbean-guard\web\index.html`.
Where the static export did not expose a value (Squarespace computes some typography
and header sizing from an external stylesheet that was not saved), I say so rather
than inventing a number.

## Three highest value findings

1. **The home hero is 10vh tall by explicit setting, not by accident.** `_home.html`
   sets `"sectionHeight": "section-height--custom", "customSectionHeight": 10` and
   renders `style="min-height: 10vh;"` on the hero section. On a 390 x 844 phone that
   is about 84px, roughly the height of the header alone. Whoever set this was almost
   certainly looking at a desktop preview, where 10vh still reads as a slim banner.
   On the device that matters most this hero has no room to hold a headline. This is
   the single clearest piece of evidence that the site was designed desktop first.

2. **The two safety colours that most need to be told apart in bright sun are almost
   the same brightness.** The map's `--safe:#1f9d55` and `--caution:#c77700` have
   relative luminance 0.251 and 0.254, a ratio of 1.01, effectively identical. Hue
   tells them apart in good light; hue is exactly what direct sun and a dimmed screen
   destroy first. `--danger:#c62828` is fine (luminance 0.137, well separated from
   both). Section 3 below gives a replacement caution value and the full multi
   channel rule this depends on.

3. **The site has almost no colour system today.** Every page's header config
   specifies only `colorName: "white"` and `colorName: "black"` for background and
   navigation, ten times each, identical across all twelve pages. Squarespace's own
   theme file (`site.css`) does define an accent (`--accent-hsl:204.39,79.49%,38.24%`,
   which converts to roughly `#1570AF`, a mid saturated blue) but I found no place in
   the header, nav, or footer chrome that actually calls it. This is not a case of
   too many colours; it is a site running on black, white, and photography, with an
   unused accent sitting in the template. Section 2 turns that gap into a real,
   restrained palette, and it is a genuine gift: `#1570AF` lands within a few points
   of the map's own already shipped locate blue, `#1565c0`. One accent, already
   half chosen.

---

## 1. What is actually there now

**Type.** One family is loaded: Poppins, at weights 300, 400, 500, and 700 (confirmed
by the `@font-face` blocks repeated identically on every saved page, latin + latin-ext
+ devanagari subsets). No second family appears anywhere in the twelve pages. I could
not extract the live computed font sizes for h1/h2/body from the saved HTML: Squarespace
7.1 resolves that scale through a versioned external stylesheet that the export did not
capture in full, and a targeted fetch of `site.css` returned only the colour token block
(below), not typography. Treat the current size scale as **unverified** rather than
assume it is fine; section 2 proposes a full new scale from scratch, mobile first, which
sidesteps the need to know the old numbers.

**Colour.** From `site.css`:

| Token | HSL | Approx hex | Where it is actually invoked |
|---|---|---|---|
| `--black-hsl` | 0, 0%, 0% | `#000000` | Header/nav text and background on every page |
| `--white-hsl` | 0, 0%, 100% | `#FFFFFF` | Header/nav background on every page |
| `--accent-hsl` | 204.39, 79.49%, 38.24% | `#1570AF` | Not found in header/nav chrome on any saved page. Likely reachable on buttons via the default `theme-btn--primary` class, unverified without a live render. |
| `--darkAccent-hsl` | 209.23, 52.7%, 70.98% | `#8FB8D8` | Not found in use |
| `--lightAccent-hsl` | 240, 10.53%, 92.55% | `#E9E9EC` | Not found in use |

Good: black and white on photography is a legitimate, restrained choice and is not
the problem. The problem is that it is the *only* choice being made anywhere I could
find, so nothing signals "this is the important button" or "this is a link" except
position.

**Imagery.** The organisation has real photography. Evidence, read directly off
`data-image-dimensions`:

- Home hero: `3840x2160` (16:9), full bleed, genuinely high resolution.
- `_lifesaving-club.html` body: `4608x3456` and `3904x2928` (both 4:3, real camera
  files, large).
- Home body gallery, in order: `720x1280`, `1350x1688`, `1350x1688`, `1080x1920`,
  `1350x1688`, `640x1136`, `900x1600`, `720x1280`, `1350x1688`, `1080x1350`,
  `640x1138`, `640x1138`, `1080x1346`, `640x1136`, `1044x1210`, `1440x1800`.

That is **seven different aspect ratios in one gallery**, and several of them
(`720x1280`, `640x1136`, `1080x1920`, `900x1600`) are exact or near exact phone
screen resolutions, meaning uncropped photos straight off a camera roll rather than
a chosen crop. `_lifesaving-club.html` repeats the pattern: two real 4:3 photographs
sitting next to `1899x1753` (near square) and `1200x1600`/`960x1280` (3:4 phone
portrait). The photography is good; the crop discipline is not there yet, and that
is what reads as amateurish, not the subject matter.

Squarespace's own responsive pipeline is already active (I can see `?format=100w`
through `?format=2500w` variants generated automatically in the srcset), so file
weight at delivery time is already handled by the platform. The lever the team
actually controls is the crop, and the source resolution fed in.

**Hero text-over-image.** The home hero applies `"imageOverlayOpacity": 0.15` on a
plain black `section-background-overlay`, i.e. a flat 15% black wash over the whole
photo, not a directional scrim. A flat 15% wash will not reliably hold light text
legible over a bright sky or sunlit sand, only over the darker parts of the frame,
and there is no way to know which part of the frame sits under the headline without
a live render. Compare this with the map, which already solved the identical problem
correctly: a directional gradient anchored to where the text actually is
(`linear-gradient(180deg, rgba(11,28,44,.92), rgba(11,28,44,0))`), strong right where
the words are, gone by the time it would compete with the photo. Section 4 recommends
reusing that exact recipe on the site.

Also present on the hero: a scroll-linked parallax effect
(`backgroundMediaEffect: {type: "parallax", rotation: 113, intensity: 12}`). I could
not confirm from the static export whether this is gated behind
`prefers-reduced-motion`. Flagged under needs confirmation.

**Needs confirmation from AJ / a live Squarespace session, not guessed here:**
- Actual computed h1/h2/body font sizes and line heights on the live site.
- Whether `--accent-hsl` (`#1570AF`) is actually rendering on any button today.
- Whether the hero parallax respects reduced motion.
- Current mobile header height in px.

---

## 2. The proposed system

Two families, both already free to use. **Poppins** (already loaded, weights 500 and
700 only) for display and headings. **System UI sans**
(`-apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif`) for body and
interface text, zero additional network request, renders instantly on a weak beach
connection, and is the exact stack the map already uses for everything. This is also
why the pairing is not arbitrary: it makes the map's typography a subset of the
site's, not a mismatch to reconcile later.

### Colour, named by role

| Token | Hex | Role | Contrast on Paper (#FFFFFF) |
|---|---|---|---|
| `--ink` | `#0B1C2C` | All headings, all body text, primary icon fill | 17.3:1 |
| `--paper` | `#FFFFFF` | Page background, the map's sheet background | — |
| `--sand` | `#F3EEE6` | Secondary section background, card fill, alternating with paper | Ink on sand: 14.9:1 |
| `--muted` | `#5B6B7A` | Captions, metadata, secondary text | 5.5:1 (5.0:1 on sand) |
| `--signal` | `#1565C0` | The one accent: links, active nav state, focus ring, primary button fill | 5.7:1 (also carries white text at 5.7:1) |

`--ink` and `--muted` are taken verbatim from the map so the two surfaces already
agree before anything else is done. `--signal` is not a new invention either: it is
within 3 points of hue and lightness of the Squarespace theme's own unused
`--accent-hsl` (`#1570AF`) and is the exact value already driving the map's own
"locate me" button and blue location dot. Canonising `#1565C0` site-wide means the
map is not adapting to the site, and the site is not adapting to the map; both were
already circling the same blue independently.

Per the standing rule on this account: `--signal` is functional only. Links, the
active tab underline, a focused input's ring, the fill on a primary call to action.
Never a decorative dot, tick, or line ahead of a heading or label.

### Type scale, mobile first (390px viewport)

| Role | Family / weight | Size | Line height |
|---|---|---|---|
| Display / H1 | Poppins 700 | 32px | 1.15 |
| H2 (section title) | Poppins 700 | 24px | 1.2 |
| H3 (card / subsection title) | Poppins 500 | 18px | 1.3 |
| Body | System UI 400 | 16px | 1.55 |
| Body small / caption | System UI 400 | 14px | 1.45 |
| Label / eyebrow / button | System UI 700, uppercase, +0.03em | 13px | 1.2 |

16px is the floor for body text specifically because anything smaller triggers
Safari's auto-zoom on input focus on iOS, which is its own kind of mobile failure.
At desktop, scale H1 up via `clamp(32px, 4vw + 12px, 56px)` and H2 via
`clamp(24px, 2.2vw + 10px, 34px)`; body stays at 16-17px at every width, since
desktop reading width, not desktop font size, is what should change.

### Spacing scale

Base unit 4px: `4, 8, 12, 16, 24, 32, 48, 64, 96`. Page gutter at 390px is **20px**
(5 units), deliberately looser than the map's 12px chrome padding. The map is an
edge to edge instrument the thumb operates while standing; the site is a document
the eye reads while scrolling, and it earns the extra 8px of margin.

---

## 3. The safety colour problem

Red, amber, green fails about 1 in 12 men on hue alone, and the map draft already
knows this: zone lines are pattern coded (solid = safe, dashed = caution, dotted =
danger) with a white halo underneath, and every status carries a text label. That
part is correct and should not change. Two things are not yet covered.

**First, the luminance problem found above.** `--safe` (L 0.251) and the current
`--caution` (`#c77700`, L 0.254) are, in a strict lightness sense, the same colour.
Under the exact condition named in the brief, a bright phone screen at low brightness
in direct sun, hue is the first channel to wash out; lightness is the last. Two
statuses that only differ in hue and are equal in lightness are the pair most likely
to become indistinguishable exactly when it matters most.

Fix: replace `--caution` with **`#9C5C00`** (luminance 0.147, contrast on white
5.3:1). This sits roughly midway in lightness between `--safe` (0.251) and
`--danger` (0.137), still reads unambiguously as amber rather than brown at the
stroke weights the map already uses, and now clears text contrast on its own so it
no longer needs a separate darker variant for solid fills.

**Second, the contrast failure on the status pill itself.** The bottom sheet's
`.status` pill sets white, 800 weight, 13px text directly on the raw `--safe` and
`--caution` fills. Computed against WCAG 2.1: white on `#1f9d55` is **3.49:1**, white
on the old `#c77700` is **3.46:1**. Both fail the 4.5:1 required for text this size;
13px bold does not qualify for the 3:1 large text exception (that needs roughly
18.66px bold or larger). `--danger` was already fine at 5.62:1.

Fix: a two tier token system rather than raising font size, since the pill needs to
stay compact.

| Use | Safe | Caution | Danger |
|---|---|---|---|
| Graphic only (line, dot, icon fill, left border), needs 3:1 | `--safe: #1F9D55` | `--caution: #9C5C00` (already passes both) | `--danger: #C62828` |
| Solid fill with white/light text, needs 4.5:1 | `--safe-text: #178049` (4.98:1) | same `--caution` token, no second value needed | same `--danger` token, no second value needed |

**The rule, stated once, to apply everywhere this status can appear** (map zone
lines, map status pill, map beach picker card, and any future Squarespace status
block): a status is never carried by colour alone, and never optional on the text
label.

1. **Text is mandatory.** The fixed strings already in the map's `T` object
   (`SE PUEDE NADAR` / `PRECAUCIÓN` / `NO NADAR`, `SWIMMING OK` / `CAUTION` /
   `DO NOT SWIM`). Never abbreviated to just the colour or just an icon.
2. **Shape is mandatory wherever colour appears.** Linear elements: solid = safe,
   dashed = caution, dotted = danger, as shipped. Iconic elements (dots, pills,
   badges): filled circle = safe, filled triangle = caution, filled octagon or X =
   danger. One icon set, reused everywhere, not re-decided per component. This
   closes the one real gap in the current picker card, where the 11px status dot
   is colour only until the eye reaches the adjacent text; giving the dot itself a
   shape means the signal survives even at that small size or in a screenshot with
   no text at all.
3. **Colour uses the two tier tokens above**, matched to whether text sits on top.

**Why amber and red specifically need the shape and text channels, not just a
lightness fix.** Amber sits closer to red than to green on the confusion line for
red-green colour blindness, the most common form. Getting the luminance right helps
everyone in bright glare; it does not by itself fix the amber-versus-red confusion
for a colour blind viewer, which is precisely what channels 1 and 2 are for.

**Minimum size for glare.** Recommend a floor of 8px stroke weight for any
status-bearing line (the map's 9px already clears this) and **16px minimum** for any
status-bearing dot or icon glyph, up from the picker card's current 11px. Small
saturated patches are the first thing to disappear in direct sun; a larger area
keeps giving the eye a signal even once the colour itself has washed toward grey.

---

## 4. Imagery treatment

Adopt exactly two house ratios and crop everything into them, rather than displaying
whatever ratio a phone happened to produce.

- **16:9** for hero and full-width section banners. This is already the shape of
  the one image on the site shot at real quality (`3840x2160`), so it costs nothing
  to standardise on it there.
- **4:5** for card and gallery imagery. Several current images are already exactly
  this ratio (`1350x1688`, `1080x1350`) and can move over with no recrop. The
  phone-screenshot ratios (`640x1136`, `720x1280`, `1080x1920`, `900x1600`, all
  close to 9:16) get centre-cropped up to 4:5, trimming sky or foreground rather
  than displaying the raw elongated frame.

**Source resolution, not just crop.** Since Squarespace already generates the
delivery sizes automatically, the only thing the team needs to get right on upload
is feeding it enough real resolution to downsample from: minimum 2400px on the long
edge for anything that will run full width. An upscaled small phone photo will look
soft at every generated size no matter how the crop is fixed.

**Text over photography.** Never a flat opacity wash at a single global percentage,
which is what the home hero does today and which cannot guarantee legibility across
a photo with both dark jungle and bright sky in frame. Reuse the map's own proven
recipe instead, since it already exists and already works: a directional gradient
anchored to the side the text sits on, strong near the text and fully transparent
by the far edge (`linear-gradient(180deg, rgba(11,28,44,.92) 0%, rgba(11,28,44,0) 100%)`
for text anchored at the top; flip the direction for text anchored at the bottom).

---

## 5. How the map inherits this, and what stays different on purpose

The map is a separate host and will not pick up Squarespace's styles by default. To
make the seam between site and map invisible, it needs to copy specific things, not
everything.

**Copy exactly:**
- **Ink.** The map's `--ink: #0b1c2c` becomes the site's `--ink` too. No change
  needed on the map; the site is adopting the map's value, not the other way round.
- **Signal blue.** Add `--signal: #1565c0` as a named token in the map's `:root`
  (it is currently hardcoded at two call sites, `.fab.on svg{color:#1565c0}` and the
  `meMarker`/`meCircle` fill) and reuse the same token on the site for links and
  primary buttons. This is the accent both surfaces were already independently
  reaching for.
- **The brand wordmark's font.** Right now `.brand` renders "CARIBBEAN GUARD" in the
  system stack at weight 800. Set it to Poppins 700 instead, matching the site's
  headings. The exact hosted file already exists and can be linked directly with no
  new licence or CDN: `https://file.squarespace-cdn.com/content/v2/namespaces/fonts/
  libraries/sqsp/assets/95402d3d-cf4f-4ff3-b652-fa1bddbe79de/latin.woff2` (Poppins,
  latin subset, weight 700, normal style, the same file the site already loads).
  Everything else on the map, all the dense UI text in cards and the sheet, stays on
  the system stack, which is now also the site's body font, so nothing else needs
  to change.
- **Corner radii.** Pill/button radius `999px` (fully round, matches the map's
  language switch and buttons; adopt this on the site's CTA buttons, which
  Squarespace tends to ship more square by default). Card radius `14px`. Sheet or
  panel radius `20px`, top corners only. New for the site only: a smaller `12px` for
  section images, since marketing imagery isn't sitting in a sheet and doesn't need
  the full treatment.
- **Shadow language.** Exactly the two the map already tuned, reused as is:
  `--shadow-sm: 0 3px 14px rgba(0,0,0,.34)` for cards and buttons,
  `--shadow-lg: 0 -6px 28px rgba(0,0,0,.35)` for anything lifting off the page like
  a sheet or modal. Apply `--shadow-sm` to the site's new card components (donation
  card, programme card) so hover and elevation read identically on both surfaces.
- **The header scrim recipe.** The site's new sticky mobile header should use the
  exact same gradient formula as the map's topbar
  (`linear-gradient(180deg, rgba(11,28,44,.92), rgba(11,28,44,0))`), so scrolling
  behaviour and header legibility feel like the same product whether the visitor is
  on a Squarespace page or inside the embedded map.

**Deliberately different, and why:**
- **Background stays pure white (`--paper`) on the map, not `--sand`.** Safety
  content read outdoors in direct sun needs the maximum contrast available; the
  site's warmer `--sand` neutral is for marketing sections where a little warmth
  helps the photography, not for a sheet someone is reading to decide whether it is
  safe to swim.
- **Status colours (`--safe`, `--caution`, `--danger`) are map-only.** They must
  never be reused as decoration on the marketing site (a "safe" green should not
  show up as a generic accent on an unrelated button), because their entire value
  depends on the visitor learning that these three colours mean exactly one thing
  and nothing else.

---

## 6. Mobile-first spec, 390px viewport

| Element | Value |
|---|---|
| Sticky header height | 56px |
| Page gutter (left/right margin) | 20px |
| Minimum tap target | 44 x 44px, 48px for primary actions (donate, call, language switch), matching the map's own buttons which are already 40-52px |
| Body text size / line height | 16px / 1.55 |
| Caption text size / line height | 14px / 1.45 |
| Card corner radius | 14px |
| Card shadow | `--shadow-sm` |
| Status glyph minimum size | 16px (icon/dot), 8px (line stroke) |

**Where the thumb can actually reach.** Primary, repeated actions (donate, call
911-equivalent, switch language, pick a beach) belong in the bottom third of the
viewport or in a sticky bottom bar, exactly where the map already puts its beach
picker and bottom sheet. One-time, per-session actions (logo, main menu) stay
top-anchored, since they are opened once and dismissed, not repeatedly reached for
mid-scroll. The map already got this right; the Squarespace site's mobile layout
should follow the same logic rather than defaulting to Squarespace's standard
top-heavy template.

**What changes at desktop, not the reverse.** Page gutter widens from 20px toward a
max content width (recommend 1080-1200px, centred). H1 scales from 32px toward
56px via the `clamp()` given in section 2. Body text stays at 16-17px; reading
measure is controlled by column width, not by growing the font. The bottom sheet
already has a desktop override in the map (`@media (min-width:820px)`, becomes a
390px-wide anchored panel instead of a full-width sheet); the site's mobile bottom
bar pattern should get the equivalent treatment, collapsing into normal inline
placement above 820px rather than staying pinned to the viewport edge.
