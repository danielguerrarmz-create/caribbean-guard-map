# 03. Image register, caribbeanguard.org

Internal running register of every image on the live site, plus the analysis that
comes out of it. Measured 2026-07-30 against the saved HTML in this folder and
against the live CDN and the live site in an emulated iPhone 12.

Everything numeric in this document was measured, not estimated, unless it says
otherwise. Method and regeneration instructions are at the bottom.

---

## The three findings that matter

### 1. The homepage silently downloads a 6 minute 52 second video that nobody pressed play on

The homepage carries a native Squarespace video block
(`data-config-video`, `systemDataId 7abab123-3a68-44e3-b309-4beff323b12c`,
`durationSeconds 412.413417`, 1920x1080 h264). Squarespace's player buffers it
eagerly through a MediaSource blob, while the `<video>` element itself stays
paused.

Measured, three separate runs, emulated iPhone 12, no clicks and no scrolling:

| Connection | Time to `load` | Bytes at `load` | Bytes after 60 s sitting still | of which video |
|---|---|---|---|---|
| Wifi, unthrottled | 1.2 s | 1.94 MB | **52.09 MB** | 50.13 MB |
| Fast 3G, 1.6 Mbps | 16.0 s | 6.17 MB | **14.43 MB** | 12.47 MB |
| Slow 3G, 400 kbps | 59.2 s | 6.15 MB | 6.15 MB | 4.21 MB |

At the moment I queried the element after 15 seconds in view with no click:
`{paused: true, autoplay: false, muted: false, currentTime: 0, duration: 412.4}`.
It is not playing. It is buffering, to the limit of whatever bandwidth exists.

The non-video part of the homepage is about 1.9 MB: roughly 1,011 KB of
Squarespace JavaScript, 643 KB of images, 157 KB of CSS, 29 KB of fonts.
So of a 52 MB homepage visit on wifi, **96 percent is a video nobody asked for**.

This dwarfs every image problem on the site combined. On a prepaid Costa Rican
SIM this is real money out of a tourist's data bundle, and on Slow 3G the page
takes **59 seconds** to reach `load` with a first contentful paint at 11.2 s.
Fixing it is one setting: remove the video block from the homepage, or replace it
with a poster image that links to the video. Nothing else on this list comes close
in value per minute of work.

### 2. Every single content image on the site has a broken `alt` attribute, and the breakage is invisible in the Squarespace editor

Squarespace 7.1 emits the `alt` attribute twice on list, carousel and gallery
images. Example, `/team`, AJ Smith's portrait, verbatim from `_team.html`:

```html
<img
  data-image-focal-point=","
  alt=""
  data-src="https://images.squarespace-cdn.com/.../aj.jpg"
  data-image-dimensions="2315x3087" data-image-focal-point="0.5,0.5" alt="aj.jpg"
  class="user-items-list-carousel__media" ...
/>
```

Two things are wrong at once:

- **Duplicate `alt`.** HTML says the first occurrence wins, so the effective alt
  text is `""`. The `alt="aj.jpg"` that Squarespace also writes is dead markup.
  Result: 17 of 17 team portraits are announced by a screen reader as unlabelled
  images or skipped entirely.
- **Malformed focal point.** `data-image-focal-point=","` appears **31 times**
  across the site, including on all 17 team portraits. It is an empty focal point,
  which is why several portraits crop badly (see finding 3).

Counts across all 13 saved pages, 103 `<img>` tags:

| Condition | Count |
|---|---|
| First `alt` is empty (effective alt is blank) | 47 |
| No `alt` attribute at all | 8 |
| A filename appears in some `alt` | 38 |
| Malformed `data-image-focal-point=","` | 31 |

Where the filename does land first, as in the `/involcrate` gallery, a screen
reader reads out "WhatsApp Image 2024 dash 09 dash 30 at 17 dot 35 dot 17 dot
jpeg". That is worse than silence.

Separately, the 16 Instagram tiles on the homepage carry the Instagram caption as
alt text, **double HTML-escaped**. The raw markup is
`alt="Atenci&amp;oacute;n Caribe Sur ..."`, which the browser parses to the
literal string `Atenci&oacute;n Caribe Sur`. Screen readers say "Atenci ampersand
oacute semicolon n". Every accented character on the homepage's alt text is
mangled this way.

None of this is visible from inside the Squarespace editor. Somebody has to be
told it is happening.

**One of those tiles is an image of the organisation's banking details.**
`CG-C833D`, 1044x1210, on the homepage. Its alt attribute, raw:

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

Three defects in one attribute. It is double-escaped, so `&amp;iquest;` reaches
the reader as the literal text `&iquest;`. It is **truncated at roughly 300
characters, mid account number**, ending on the digit `2`. And the underlying
asset is an image of text carrying the PayPal address, the legal entity name and
the Cédula Jurídica, which is WCAG 1.4.5 (Images of Text) regardless of the alt.

**Severity, stated accurately:** this is a defect, not a blocker. I checked
`/donar`, and the same details are present there as real selectable text,
including both IBANs (`CR93 0151 0932 0020 0328 81` and
`CR17 0151 0932 0010 0856 38`), the cédula and the PayPal address. So no donor is
actually prevented from donating. The fix is still worth doing, because the
homepage is where the donation prompt appears and a truncated bank account read
aloud is worse than no alt at all.

### 3. PNG is being used for photographs, and Squarespace will not rescue you from that

The CDN already negotiates modern formats: with a browser `Accept` header,
every asset comes back as `image/webp`. That handles ordinary JPEG waste. What it
does not handle is a **photograph uploaded as a PNG**, because the WebP transcode
of a lossless source stays near-lossless and stays enormous.

| ID | File | Source px | Served at 1500w |
|---|---|---|---|
| `CG-69169` / `CG-0754B` | Annotated Base Map V5.png | 3950x1600 | **1,482 KB** |
| `CG-ABD63` | staff Naima.png | 1502x1170 | 797 KB |
| `CG-522FB` | free diving.png | 1423x939 | 736 KB |
| `CG-B146C` | freediving.png | 1138x973 | 697 KB |
| `CG-1BF7C` | Dangerous Area V4.png | 842x596 | **665 KB** |
| `CG-271B8` | staff Hershell.png | 879x1155 | 392 KB |

`Dangerous Area V4.png` is 842x596. That is a small image. It costs 665 KB. A
JPEG at quality 80 of the same picture would be roughly 60 KB. `free diving.png`
at 1423x939 costs 736 KB where a JPEG would be about 130 KB.

Re-saving these six files as JPEG quality 82 and re-uploading recovers roughly
**4.0 MB** with no visible change, and it is a five minute job with no code.
`Annotated Base Map V5.png` alone accounts for 1.5 MB of it, and that one is
about to be replaced by the interactive map anyway (see `04-map-integration.md`).

---

## A class of their own: the two authored hazard maps

These do not belong in the same bucket as the beach photography and the register
should not have filed them there. Everything else on this site is a photograph of
something that happened. **These two are original safety documents that Caribbean
Guard authored**, and they are the only place on the entire website where the
organisation's actual operational knowledge of that coast is written down.

| ID | File | Source px | Served | Where | Alt |
|---|---|---|---|---|---|
| `CG-69169` | Annotated Base Map V5.png | 3950x1600 | 1,482 KB | `/programa-playa-organizada`, carousel block | `""` |
| `CG-0754B` | Annotated Base Map V5.png | 3950x1600 | 1,482 KB | same page, Fluid Engine image block | none at all |
| `CG-1BF7C` | Dangerous Area V4.png | 842x596 | 665 KB | same page, carousel block | `""` |

They carry rip current arrows, rescue station positions and a bilingual legend.
That content exists **only as pixels**. There is no text anywhere on that page
saying where the rip currents are. So:

- **Google cannot index any of it.** A tourist searching "rip current Cocles" or
  "corrientes Playa Cocles" finds nothing from the organisation that has the
  answer drawn on a map.
- **A screen reader conveys nothing.** Both carousel copies have the duplicate
  `alt` defect with the empty one first.
- **Anyone whose images fail to load, which on this coast is common, gets a blank
  space** where the safety information should be.
- **At 390 px wide it is unreadable anyway.** `Annotated Base Map V5.png` is
  3950 px of detail rendered into a phone. The legend text is sub-pixel.

One correction to how these were reported to me: they are not both carousel
blocks. `Annotated Base Map V5.png` is **uploaded twice as two separate assets**
(`f15318a5…` and `17bff6c7…`) on the same page. One is the carousel copy with
`alt=""` first. The other is a Fluid Engine image block (`data-block-type="1337"`,
`data-sqsp-image-block-image`) carrying a full seven step srcset and `sizes="auto,
(max-width: 640px) 100vw, ..."`, with no usable alt at all. Two different blocks,
two different bugs, 1,482 KB each. That is also why the page reports the same file
twice in the register: it genuinely is two files as far as any browser is
concerned.

**What to do, in order:**

1. **Write real alt text today.** Not "mapa" or "map". Describe what it shows:
   which beaches, that it marks rip currents and rescue stations. This is minutes
   of work and it is the highest value per minute anywhere in this register.
2. **Put the content in text on the page**, next to the image. A list of the
   beaches with a sentence each. That is what Google indexes, what a screen reader
   reads, and what survives when the image does not load. The image becomes the
   illustration rather than the sole carrier.
3. **Delete the duplicate upload.** 1,482 KB of the same file, twice, on the
   heaviest page on the site.
4. **Then replace both with the interactive map**, which makes the annotations
   real data rather than pixels. That work is already underway: the sheet has been
   georeferenced against Bing and its annotations extracted to
   `web/data/cg-hazards.geojson` as 11 rip currents, 4 rescue stations and one
   deliberately unlabelled polygon. See `04-map-integration.md`.

   **Do not quote a metre figure for those hazard positions from this document.**
   An earlier draft of this line said "georeferenced to a 1.2 m median residual",
   which is a RANSAC residual on the selected inliers, the same self-consistency
   measure that misled a draft of `04-map-integration.md` into claiming the base
   image was accurate to 4 m. The meaningful signal in that fit is **294 inliers
   against the base image's 14**, because the annotation sheet is untouched artwork
   while the base is generatively upscaled, and that is a statement about which
   fit can be trusted rather than about metres on the ground. The hazard features
   also inherit the base image's own registration error, which is **75 m west of
   Punta Uva and not confirmable east of it**. Those are the numbers the map itself
   uses, and they are the numbers to quote.

Steps 1 to 3 do not depend on step 4 and should not wait for it.

### The sentence to say to Caribbean Guard

Worth stating on its own, because it is the whole argument for taking accessibility
seriously here and it needs no WCAG citation:

> **An accessibility bug hid your most valuable asset from your own team.**

The thing this project spent two days missing was attributed hazard data: real rip
current positions decided by people who know that coast, instead of placeholder
prose written from general knowledge. It turned out to be **already published, on
their own public website, drawn by their own guards.** It was invisible because of
the duplicate `alt` defect in finding 2. Nobody searching the site could find it,
no screen reader announced it, and no search engine indexed it, so as far as
anything outside a browser tab was concerned it did not exist.

That is also why the machine-read extraction in `web/data/cg-hazards.geojson` was
possible at all: 11 rip currents and 4 rescue stations recovered by georeferencing
a PNG, because the data was only ever available as pixels.

Attribution, since this deserves to be accurate rather than tidy: the alt defect
came out of this register's parse, the georeferencing and annotation extraction
were done separately with `tools/georef_annot.py` and
`tools/extract_annotations.py`, and the framing above is
`06-accessibility-and-safety.md`'s. It took all three to see it.

---

## What is good

Worth saying, because the revamp has to survive review by the people who built this.

- **The photography is genuinely theirs.** These are real rescue posts, real
  courses, real people on that coast. Nothing here is stock. That is rare and it
  is the site's biggest asset.
- **Squarespace's responsive pipeline is doing real work.** Every fluid-engine
  image carries a full seven step srcset from 100w to 2500w, and the CDN serves
  WebP. On `/nuestro-trabajo` the browser correctly fetched 500w, 1000w and 1500w
  variants for three different column widths. That part is not broken.
- **`/involcrate` is the best behaved page on the site.** The gallery grid uses
  honest `sizes` values (`(max-width:768px)49.3vw,32.4vw`), so a phone pulls 750w
  tiles at 30 to 95 KB each. 7 images for 441 KB total. This is the pattern the
  rest of the site should copy.
- **The team page exists at all, with 17 named people.** Most small nonprofits
  never get that far.

---

## The register

72 distinct CDN assets across 13 URLs. Sorted by page, then by weight.

**ID scheme.** `CG-` plus the first five hex characters of the SHA-1 of the
canonical CDN URL, uppercased. Stable as long as the file is not re-uploaded.
Re-uploading the same photo produces a new Squarespace asset ID and therefore a
new register ID, which is correct: to the browser it genuinely is a different
file with a different cache entry.

**Columns.** `Source px` is Squarespace's `data-image-dimensions`, the uploaded
original. `Served @1500w` is the real transfer size a modern phone gets at
`?format=1500w` with an `Accept: image/avif,image/webp,...` header, measured by
HEAD against the live CDN. `Alt`: `yes` means a human wrote something, `filename`
means the only alt text is a filename, `MISSING` means no usable alt text
reaches the browser.

| ID | File | Page | Source px | AR | Role | Alt | Served @1500w | Type |
|---|---|---|---|---|---|---|---|---|
| `CG-9EB7C` | favicon.ico | all 13 | 665x677 | 0.98 | favicon | MISSING | 16 KB | png |
| `CG-E1D42` | Logo.png | all 13 | 665x677 | 0.98 | logo, site header | yes | 16 KB | png |
| `CG-AE1CB` | Logo.png | /nosotros, /unete | 665x677 | 0.98 | og:image, social share card | n/a | 16 KB | png |
| `CG-F18DD` | image-asset.jpeg | / | 1350x1688 | 0.80 | Instagram feed tile | IG caption, double-escaped | 523 KB | jpeg |
| `CG-493F1` | image-asset.jpeg | / | 1350x1688 | 0.80 | Instagram feed tile | IG caption, double-escaped | 300 KB | jpeg |
| `CG-F9C12` | image-asset.jpeg | / | 900x1600 | 0.56 | Instagram feed tile | MISSING | 297 KB | jpeg |
| `CG-2AE51` | image-asset.jpeg | / | 1350x1688 | 0.80 | Instagram feed tile | IG caption, double-escaped | 276 KB | jpeg |
| `CG-D1096` | caribbean_guard_foto-transformed.jpeg | / | 3840x2160 | 1.78 | hero, full-bleed section background | filename | 165 KB | jpeg |
| `CG-6EF19` | image-asset.jpeg | / | 1080x1346 | 0.80 | Instagram feed tile | IG caption, double-escaped | 161 KB | jpeg |
| `CG-93F57` | image-asset.jpeg | / | 1080x1920 | 0.56 | Instagram feed tile | MISSING | 150 KB | jpeg |
| `CG-FB97D` | image-asset.jpeg | / | 720x1280 | 0.56 | Instagram feed tile | MISSING | 137 KB | jpeg |
| `CG-F0BE2` | image-asset.jpeg | / | 1080x1350 | 0.80 | Instagram feed tile | IG caption, double-escaped | 136 KB | jpeg |
| `CG-F7F68` | image-asset.jpeg | / | 1440x1800 | 0.80 | Instagram feed tile | IG caption, double-escaped | 124 KB | jpeg |
| `CG-C833D` | image-asset.jpeg | / | 1044x1210 | 0.86 | Instagram feed tile | IG caption, double-escaped | 114 KB | jpeg |
| `CG-AD979` | image-asset.jpeg | / | 720x1280 | 0.56 | Instagram feed tile | MISSING | 104 KB | jpeg |
| `CG-711C2` | image-asset.jpeg | / | 640x1136 | 0.56 | Instagram feed tile | MISSING | 83 KB | jpeg |
| `CG-F77F4` | image-asset.jpeg | / | 1350x1688 | 0.80 | Instagram feed tile | IG caption, double-escaped | 66 KB | jpeg |
| `CG-05C20` | image-asset.jpeg | / | 640x1136 | 0.56 | Instagram feed tile | MISSING | 51 KB | jpeg |
| `CG-DDBC2` | image-asset.jpeg | / | 640x1138 | 0.56 | Instagram feed tile | MISSING | 40 KB | jpeg |
| `CG-BB8B3` | image-asset.jpeg | / | 640x1138 | 0.56 | Instagram feed tile | MISSING | 28 KB | jpeg |
| `CG-607DF` | homepage.jpeg | /vision | 1600x1200 | 1.33 | section image, full width | MISSING | 167 KB | jpeg |
| `CG-A1329` | historia.jpg | /nuestro-trabajo | 2736x3648 | 0.75 | section image, 29.2vw column | MISSING | 170 KB | jpg |
| `CG-AA3B6` | historia4.jpg | /nuestro-trabajo | 3648x2736 | 1.33 | section image, 45.8vw column | MISSING | 110 KB | jpg |
| `CG-859EB` | historia+home.jpg | /nuestro-trabajo | 3648x2736 | 1.33 | section image, full width | MISSING | 77 KB | jpg |
| `CG-3ADC6` | WhatsApp Image 2024-09-30 at 17.22.50.jpeg | /proyectos | 1200x1600 | 0.75 | section image | filename | 212 KB | jpeg |
| `CG-E056C` | RCP o hp.jpeg | /proyectos | 2048x1536 | 1.33 | section image | filename | 194 KB | jpeg |
| `CG-25483` | homepage2.jpeg | /proyectos | 1280x661 | 1.94 | section image | filename | 95 KB | jpeg |
| `CG-69169` | Annotated Base Map V5.png | /programa-playa-organizada | 3950x1600 | 2.47 | **AUTHORED HAZARD MAP**, carousel block | filename | 1,482 KB | png |
| `CG-0754B` | Annotated Base Map V5.png | /programa-playa-organizada | 3950x1600 | 2.47 | **AUTHORED HAZARD MAP**, duplicate upload, image block | MISSING | 1,482 KB | png |
| `CG-1BF7C` | Dangerous Area V4.png | /programa-playa-organizada | 842x596 | 1.41 | **AUTHORED HAZARD MAP**, carousel block | filename | 665 KB | png |
| `CG-EE3EA` | Screenshot 2024-10-11 191441.jpg | /programa-playa-organizada | 1036x1372 | 0.76 | screenshot | filename | 489 KB | jpg |
| `CG-1403D` | rcp.jpeg | /programa-playa-organizada | 1152x2048 | 0.56 | section image | filename | 376 KB | jpeg |
| `CG-5E2F6` | WhatsApp Image 2024-09-30 at 17.22.45.jpeg | /programa-playa-organizada | 1200x1600 | 0.75 | section image | filename | 315 KB | jpeg |
| `CG-6BC1F` | proyectos.jpg | /programa-playa-organizada | 4608x3456 | 1.33 | section image | filename | 260 KB | jpg |
| `CG-F4ABD` | WhatsApp Image 2024-10-11 at 10.39.30.jpeg | /programa-playa-organizada | 1280x960 | 1.33 | section image | filename | 184 KB | jpeg |
| `CG-DDE57` | lifesaving.jpeg | /lifesaving-club | 1200x1600 | 0.75 | section image | filename | 293 KB | jpeg |
| `CG-67A65` | WhatsApp Image 2024-09-30 at 17.33.53.jpeg | /lifesaving-club | 960x1280 | 0.75 | section image | filename | 269 KB | jpeg |
| `CG-99040` | lifesaving2 home.jpg | /lifesaving-club | 4608x3456 | 1.33 | section image | filename | 217 KB | jpg |
| `CG-45E5E` | life saving.jpg | /lifesaving-club | 3904x2928 | 1.33 | section image | filename | 210 KB | jpg |
| `CG-47F34` | lifesaving-club-fullcolor.png | /lifesaving-club | 1899x1753 | 1.08 | club badge, 20.8vw | MISSING | 192 KB | png |
| `CG-1D563` | swim club.jpg | /swim-club | 3904x2928 | 1.33 | section image, 50vw | MISSING | 340 KB | jpg |
| `CG-05985` | swimclub.jpg | /swim-club | 3904x2928 | 1.33 | section image, 50vw | MISSING | 214 KB | jpg |
| `CG-9F645` | swim-club-fullcolor.png | /swim-club | 1649x1753 | 0.94 | club badge, 20.8vw | MISSING | 197 KB | png |
| `CG-0940A` | swim club3.jpg | /swim-club | 4608x3456 | 1.33 | section image, 50vw | MISSING | 171 KB | jpg |
| `CG-522FB` | free diving.png | /freediving-club | 1423x939 | 1.52 | section image, full width | MISSING | 736 KB | png |
| `CG-B146C` | freediving.png | /freediving-club | 1138x973 | 1.17 | section image, full width | MISSING | 697 KB | png |
| `CG-9C6F2` | IMG_5815.jpg | /freediving-club | 4032x2268 | 1.78 | section image, full width | MISSING | 449 KB | jpg |
| `CG-C04E0` | freediving-fullcolor.png | /freediving-club | 1899x1753 | 1.08 | club badge | MISSING | 197 KB | png |
| `CG-BA2B2` | IMG_20210505_092112.jpg | /involcrate | 3648x2736 | 1.33 | gallery grid tile | filename | 390 KB | jpg |
| `CG-43A20` | IMG_20210505_092450_1.jpg | /involcrate | 4608x3456 | 1.33 | gallery grid tile | filename | 257 KB | jpg |
| `CG-E895D` | WhatsApp Image 2024-09-30 at 17.33.50.jpeg | /involcrate | 1600x898 | 1.78 | gallery grid tile | filename | 238 KB | jpeg |
| `CG-B001D` | IMG_20220414_125441.jpg | /involcrate | 4608x3456 | 1.33 | gallery grid tile | filename | 197 KB | jpg |
| `CG-EF64B` | WhatsApp Image 2024-09-30 at 17.35.17.jpeg | /involcrate | 1280x853 | 1.50 | gallery grid tile | filename | 96 KB | jpeg |
| `CG-EA1B4` | WhatsApp Image 2024-09-30 at 17.25.55.jpeg | /involcrate | 1280x853 | 1.50 | section image | filename | 49 KB | jpeg |
| `CG-1DF95` | WhatsApp Image 2024-09-30 at 17.25.55.jpeg | /donar | 1280x853 | 1.50 | section image, **same photo re-uploaded** | MISSING | 49 KB | jpeg |
| `CG-ABD63` | staff Naima.png | /team | 1502x1170 | 1.28 | portrait, Naima Montejo, 1:1 crop | filename | 797 KB | png |
| `CG-6CD07` | staff JOel Gagg.JPG | /team | 3024x4032 | 0.75 | portrait, Joel Gaggstatter, 1:1 crop | filename | 695 KB | jpg |
| `CG-C4B5E` | staff Elias.JPG | /team | 2062x3664 | 0.56 | portrait, Elías Brown, 1:1 crop | filename | 673 KB | jpg |
| `CG-271B8` | staff Hershell.png | /team | 879x1155 | 0.76 | portrait, Hershell Lewis, 1:1 crop | filename | 392 KB | png |
| `CG-2C088` | staff sofia paso viola.jpg | /team | 2000x3000 | 0.67 | portrait, Sofía Paso Viola, 1:1 crop | filename | 327 KB | jpg |
| `CG-49EC0` | mike geist.jpg | /team | 2725x3633 | 0.75 | portrait, Mike Geist, 1:1 crop | filename | 322 KB | jpg |
| `CG-8B60C` | aj.jpg | /team | 2315x3087 | 0.75 | portrait, AJ Smith, 1:1 crop | filename | 254 KB | jpg |
| `CG-D38EE` | staff sofia cordoba.jpg | /team | 2000x3000 | 0.67 | portrait, Sofía Córdoba, 1:1 crop | filename | 243 KB | jpg |
| `CG-FDD88` | staff Georgina.jpg | /team | 2576x1932 | 1.33 | portrait, Georgina De Puch, 1:1 crop | filename | 238 KB | jpg |
| `CG-3B459` | Mila.jpg | /team | 2278x3051 | 0.75 | portrait, Milagro Muñoz Araya, 1:1 crop | filename | 237 KB | jpg |
| `CG-0CDF0` | staff Sophia Graff.jpeg | /team | 942x1446 | 0.65 | portrait, Sofia Graff, 1:1 crop | filename | 216 KB | jpeg |
| `CG-FAD51` | staff lucas.jpg | /team | 1224x1734 | 0.71 | portrait, Lucas Iturriza, 1:1 crop | filename | 165 KB | jpg |
| `CG-5D397` | staff Mel gromo .jpeg | /team | 1200x1599 | 0.75 | portrait, Melisa Gromöller, 1:1 crop | filename | 157 KB | jpeg |
| `CG-C64F5` | Gloriana Barrantes.jpg | /team | 1023x1384 | 0.74 | portrait, Gloriana Barrantes, 1:1 crop | filename | 111 KB | jpg |
| `CG-9FD0A` | Melissa Gonzales.jpg | /team | 718x954 | 0.75 | portrait, Melissa Gonzalez, 1:1 crop | filename | 91 KB | jpg |
| `CG-4ACFD` | staff Dexter.jpeg | /team | 853x1280 | 0.67 | portrait, Dexter Lewis, 1:1 crop | filename | 80 KB | jpeg |
| `CG-3E62C` | staff Tapas.jpg | /team | 1024x471 | 2.17 | portrait, Andrés "Tapas" Hernández, 1:1 crop | filename | 61 KB | jpg |

Portrait names were matched positionally: the 17 `<img>` tags in `_team.html`
interleave one-to-one with the 17 carousel titles, in document order. Worth a
five second eyeball by AJ before anything is published from this mapping.

---

## Analysis

### Reuse across pages: there is almost none, and that is the problem

Only three assets appear on more than one page, and two of them are the logo:

| Asset | Pages | Note |
|---|---|---|
| `CG-E1D42` Logo.png | all 13 | correct, this is what caching is for |
| `CG-9EB7C` favicon.ico | all 13 | see below |
| `CG-AE1CB` Logo.png | /nosotros, /unete | og:image, but on an `http://` URL, not `https://` |

Where the *same photograph* appears twice, it has been **uploaded twice**, so it
is two assets with two URLs and two cache entries:

- `WhatsApp Image 2024-09-30 at 17.25.55.jpeg` is asset `7cbc1c7d...` on
  `/involcrate` and asset `bf050dc8...` on `/donar`. Identical 1280x853 photo,
  49 KB downloaded twice by anyone who visits both pages.
- `Annotated Base Map V5.png` is uploaded **twice onto the same page**, as assets
  `f15318a5...` and `17bff6c7...`. One of them is inside a desktop-only content
  block. That is 1.5 MB of duplicate storage.

The fix is to insert the existing asset from the Squarespace library rather than
re-uploading the file. Small effect on bandwidth, real effect on the library
staying navigable as this grows.

### The favicon is the logo, at 665x677

`favicon.ico` and `Logo.png` return **identical byte counts (44,268 raw / 16 KB
as WebP) and identical served dimensions (665x677)**, and both come back with
`content-type: image/png` despite the `.ico` extension. It is the same file
uploaded under a second asset ID and renamed.

A favicon should be a 32x32 and 180x180 pair, around 2 to 5 KB total. At 665x677
the browser downsamples a near-square logo with fine text into a 16x16 tab icon,
which is why it reads as a grey smudge. This one is cheap to fix and it is the
first thing anyone sees in a browser tab.

### Oversized for how it is displayed

The srcset pipeline handles most of this correctly. The genuine waste is
concentrated in three places.

**a) The homepage hero declares `200vw` on mobile.**

```
sizes="(max-width: 799px) 200vw, 100vw"
```

On a 390 px phone that resolves to 780 CSS px, which at DPR 2 or 3 pushes the
browser past every srcset step and lands on `2500w`. Measured live: the phone
fetches `caribbean_guard_foto-transformed.jpeg?format=2500w` at **338.8 KB**.
The same image at `1500w` is 164.6 KB and at `1000w` is 87.8 KB, and the element
is 390 px wide. That is **251 KB wasted on the first image of the first page**,
purely because of a `sizes` value Squarespace generates for full-bleed background
sections. It is not directly editable in the editor, but choosing a normal image
section instead of a full-bleed background section avoids it.

**b) Six photographs stored as PNG.** Covered in finding 3. About 4.0 MB
recoverable.

**c) The team carousel loads one full portrait per swipe.** Measured live, the
`/team` page loads exactly one image on arrival: `staff+Elias.JPG?format=1500w`
at **672.7 KB**. Each subsequent swipe fetches the next portrait at 1500w. A
visitor who swipes through all 17 downloads roughly **5.0 MB** of portraits to
look at 17 circles about 300 px across. The carousel is rendering these into a
`data-media-aspect-ratio="1:1"` slot, so a 750w variant would be indistinguishable
and would cost about 1.6 MB for the set.

Total recoverable across the site, excluding the video: roughly **9 MB**, of which
about 4 MB is the PNG conversion and about 3.4 MB is the team carousel.

### Missing alt text

Covered in finding 2. Summarised as a work list:

| Where | Assets | What to write |
|---|---|---|
| 17 team portraits | `CG-ABD63` through `CG-3E62C` | The person's name. That is the correct alt text for a portrait next to a caption that also names them, and it costs nothing. |
| 5 `/involcrate` gallery tiles | `CG-BA2B2`, `CG-43A20`, `CG-E895D`, `CG-B001D`, `CG-EF64B` | What is happening in the photo, one short clause. |
| 3 club badges | `CG-47F34`, `CG-9F645`, `CG-C04E0` | "Lifesaving Club logo" and so on. |
| 16 Instagram tiles | all `image-asset.jpeg` | Not editable. Fixed by removing the feed block, see below. |
| Hero, section images | `CG-D1096` and the rest | Most of these are decorative next to a heading that already says the thing. An explicit empty alt is the right answer, but it has to be a deliberate empty alt, not the accidental one Squarespace is emitting. |
| favicon | `CG-9EB7C` | n/a, but replace the file. |

### Portraits of real people

17 of the 72 assets are portraits of named individuals. These carry obligations
that a photo of a beach does not.

- **Every one of them is cropped square from a source that is not square, with a
  broken focal point.** All 17 carry `data-image-focal-point=","`, so Squarespace
  falls back to centre-crop. The correct way to read that is not "the crop is
  centred on purpose" but **"nobody ever reviewed the crop"**. Discarded frame,
  computed per portrait:

  | Portrait | Source | Crops | Frame discarded |
  |---|---|---|---|
  | Andrés "Tapas" Hernández | 1024x471 | horizontal | **54%** |
  | Elías Brown | 2062x3664 | vertical | 44% |
  | Sofia Graff | 942x1446 | vertical | 35% |
  | Sofía Córdoba, Dexter Lewis, Sofía Paso Viola | 2000x3000, 853x1280 | vertical | 33% |
  | Lucas Iturriza | 1224x1734 | vertical | 29% |
  | Gloriana Barrantes | 1023x1384 | vertical | 26% |
  | 7 others at aspect 0.75 | various | vertical | 25% |
  | Georgina De Puch, Naima Montejo | 2576x1932, 1502x1170 | horizontal | 25%, 22% |

- **I rendered all 17 crops to check whether faces are being cut. They are not.**
  Fetched each asset, applied the same centre square crop Squarespace applies, and
  looked at the contact sheet. **Every one of the 17 contains a complete,
  unobstructed face.** The worry that a 54 percent discard was decapitating
  somebody does not materialise, largely because people centre themselves in
  photographs. Worth stating plainly so nobody re-raises it.

- **The real problem is framing variance, and no focal point can fix it.** The
  square crops are consistent; the source photographs are not. Some are tight head
  and shoulders. Several are full-body shots where the face ends up a small
  fraction of a 300 px circle: Hershell Lewis standing with a surfboard, Joel
  Gaggstatter at distance in jungle. Dexter Lewis is a shirtless torso-dominant
  frame where the square pushes down onto the chest, which reads as a holiday snap
  next to colleagues in uniform. Melisa Gromöller's face is largely behind
  sunglasses and a raised camera. At least five of the seventeen have sunglasses on.
  Moving the crop centre cannot turn a full-body photo into a portrait. **This needs
  new photographs of a few people, not a settings change.**
- **Quality is uneven in a way that reads as hierarchy.** `Melissa Gonzales.jpg`
  is 718x954, the smallest source on the page. `staff Tapas.jpg` is 1024x471.
  Meanwhile `staff JOel Gagg.JPG` is 3024x4032. When these sit in one row, the
  small ones look like placeholders, which is a message nobody intended to send
  about those individuals.
- **Consent and takeaway.** There is no evidence in the markup either way about
  photo consent. Before this register is used to drive a redesign, someone should
  confirm with AJ that all 17 people agreed to appear on a public website, and
  that there is a route for a volunteer who leaves to have their portrait removed.
  Volunteers rotate. This is not a hypothetical.
- **Filenames leak.** `aj.jpg`, `Mila.jpg`, `staff Mel gromo .jpeg`. Because the
  filename is also written into a duplicate `alt`, these strings are in the page
  source. Low risk, but it is a person's name in a URL that will outlive their
  involvement.

Recommendation: re-crop the 17 portraits to square at source with the subject
placed deliberately, replace the two that cannot work (`CG-3E62C`, `CG-9FD0A`),
set real alt text to each person's name, and confirm consent.

### Low enough quality that they should be replaced

| ID | File | Why |
|---|---|---|
| `CG-3E62C` | staff Tapas.jpg | 1024x471 landscape in a 1:1 slot. Cannot be made to work. |
| `CG-9FD0A` | Melissa Gonzales.jpg | 718x954, the lowest resolution portrait, visibly softer than its neighbours. |
| `CG-EE3EA` | Screenshot 2024-10-11 191441.jpg | It is a phone screenshot, 489 KB, presented as content. Whatever it is showing should be redrawn or retyped. |
| `CG-1BF7C` | Dangerous Area V4.png | 842x596 diagram at 665 KB. Low resolution for a hazard diagram and heavy for its size. Superseded by the interactive map. |
| `CG-9EB7C` | favicon.ico | 665x677 logo doing a 16x16 job. |
| `CG-69169`, `CG-0754B` | Annotated Base Map V5.png | Not a quality problem so much as a format one. 3.9 K px wide, 1.5 MB, and unreadable at 390 px. This is the artefact the interactive map exists to replace. |

---

## Totals and what the homepage costs on 3G

**Library totals**, measured against the live CDN with a browser `Accept` header,
so these are real transfer sizes and not on-disk sizes:

| Metric | Value |
|---|---|
| Distinct CDN image assets | 72 |
| Distinct source photographs, ignoring duplicate uploads | 69 |
| Whole library at `1500w` | 19.1 MB |
| Whole library at `2500w`, the CDN's delivery ceiling | 30.8 MB |
| Sum of uploaded source pixels | roughly 380 megapixels |
| Largest single asset | `Annotated Base Map V5.png`, 1,482 KB at 1500w |

Note: `?format=original` does **not** return the uploaded original. Squarespace
caps delivery at 2500 px wide. The 4608x3456 phone photos on this site are served
at 2500x1875 at most, so their upload size is irrelevant to bandwidth. It still
matters for the media library and for anyone re-downloading them to reuse.

**Per page, measured live on an emulated iPhone 12**, on arrival plus a scroll to
the bottom:

| Page | Image requests | Image KB | Squarespace JS KB | Total KB |
|---|---|---|---|---|
| `/programa-playa-organizada` | 3 | 1,814 | 913 | 2,939 |
| `/freediving-club` | 5 | 1,775 | 923 | 2,902 |
| `/swim-club` | 5 | 855 | 1,052 | 2,113 |
| `/` (excluding the video) | 10 | 894 | 998 | 2,079 |
| `/team` (before any swipe) | 2 | 689 | 858 | 1,774 |
| `/lifesaving-club` | 3 | 572 | 930 | 1,716 |
| `/involcrate` | 7 | 441 | 862 | 1,513 |
| `/vision` | 2 | 183 | 936 | 1,331 |
| `/nuestro-trabajo` | 4 | 188 | 906 | 1,305 |
| `/proyectos` | 2 | 111 | 851 | 1,179 |
| `/donar` | 2 | 66 | 910 | 1,162 |

Read the last two columns together. **On eight of eleven pages, Squarespace's own
JavaScript outweighs every image on the page.** `/donar` is the clearest case
because it has no video to blame: 66 KB of images against 910 KB of script, a
factor of **fourteen**.

**Two conclusions follow, and the second one partly undercuts this document.**

*This platform cannot deliver a two second answer, and no work inside it will
change that.* The homepage's 59.2 s on Slow 3G reads as "the home page is slow,
fix it", which is the wrong lesson. `/donar` is the right one: roughly 1 MB of
framework before a single donation detail renders, on the page that is the
conversion path, with nothing on it to optimise away. That is a floor, not a
defect. It is the strongest structural argument for hosting the safety map
standalone, stronger than the tile-pyramid constraint that originally drove that
decision. Credit to `06-accessibility-and-safety.md` for sharpening it from a
supporting number into the conclusion.

*Image optimisation on these pages is close to pointless while the framework is
fourteen times the weight of the imagery.* Converting the six PNGs recovers about
4 MB across the whole site and is worth doing because it is five minutes of work.
Beyond that, this register's performance findings should not be used to justify a
programme of image work. **Removing the homepage video and moving the safety map
off Squarespace are worth more than every remaining image fix in this document
combined.** The register's durable value is the inventory, the alt text audit and
the consent questions, not the kilobytes.

**The homepage on 3G**, measured, not modelled:

| | Slow 3G, 400 kbps | Fast 3G, 1.6 Mbps |
|---|---|---|
| First contentful paint | 11.2 s | 3.0 s |
| DOM content loaded | 42.2 s | 10.0 s |
| `load` event | **59.2 s** | 16.0 s |
| Bytes by `load` | 6.15 MB | 6.17 MB |
| Bytes after 60 s | 6.15 MB | 14.43 MB |

Slow 3G is roughly what one bar of signal on that coast looks like. **Just under a
minute** before the homepage finishes loading, and the first thing that appears
does so at 11 seconds. The brief's scenario, someone barefoot in the sun with one
bar wanting to know in two seconds whether it is safe to swim, is not survivable
on this page. That is not a criticism of the design. It is arithmetic about 1 MB
of framework JavaScript plus a 6 minute video.

If the video block is removed and the six PNGs are converted, the homepage falls
to roughly **1.5 MB and about 30 seconds on Slow 3G**. Still not two seconds.
Which is the case for `04-map-integration.md`.

---

## How to regenerate this register

The register goes stale the moment anyone uploads an image. To rebuild it:

1. **Re-save the HTML.** Save each page from the URL list in `BRIEF.md` into this
   folder with the same `_slug.html` names. Squarespace's server-rendered markup
   carries everything needed; do not use "save complete web page".
2. **Extract references.** Parse each file for `<img>`, `<source srcset>`, CSS
   `background-image: url(...)`, `og:image`, and the entity-escaped JSON blobs
   where `"assetUrl"` is followed by `"originalSize"`. Canonicalise each URL by
   stripping the query string and forcing `https`. Source dimensions come from
   `data-image-dimensions`, which matches `originalSize` in the JSON.
3. **Measure real weight.** HEAD each canonical URL at
   `?format=300w|500w|750w|1000w|1500w|2500w` **with a browser `Accept` header**
   (`image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8`). Without
   it the CDN returns the original JPEG or PNG and every number is 40 to 60
   percent too high. This is the single easiest thing to get wrong.
4. **Confirm what actually loads.** Drive the live site with Playwright using the
   `iPhone 12` device profile and record every response. Squarespace picks the
   format at runtime through its own loader for carousel, gallery and list blocks,
   so the markup alone cannot tell you which variant a phone gets.
5. **Assign IDs.** `CG-` plus `sha1(canonical_url)[:5].upper()`.
6. **Diff against this file.** New IDs are new uploads. Vanished IDs are removals
   or re-uploads. A changed weight for an unchanged ID means Squarespace changed
   its encoder, not that anyone touched the site.

Working scripts used for this pass are in the session scratchpad and are not
checked in. Steps 2, 3 and 5 are about 80 lines of Python; step 4 is about 30
lines with `playwright`. Worth committing to `tools/` if this becomes routine.

---

## Needs confirmation from AJ

1. **The homepage video.** What is it, and is it meant to be there? Removing it is
   the single highest-value change on the site, but it is somebody's work.
2. **Photo consent for the 17 team portraits**, and what happens when a volunteer
   leaves. Related: is there a preferred name or spelling for anyone on `/team`.
   The portrait-to-name mapping in this register was derived positionally from the
   markup and should be eyeballed once.
3. **The 17.25.55 photo appears on both `/involcrate` and `/donar`.** Deliberate,
   or an accident of re-uploading.
4. **`Screenshot 2024-10-11 191441.jpg`** on `/programa-playa-organizada`. What is
   it showing, and can it be replaced with real content.
5. **Portrait sources.** *Do not ask this separately.* It is folded into item 11 of
   `06-accessibility-and-safety.md`, which is the single request AJ should receive.
   What this register contributes is the evidence behind it:

   - The two weakest sources are `staff Tapas.jpg` at **1024x471** (landscape, so a
     square crop is impossible at any focal point) and `Melissa Gonzales.jpg` at
     **718x954**, the lowest resolution on the page.
   - A higher resolution original fixes the crop. It does not fix framing or
     sunglasses, which is why item 11 asks about originals **first**: the answer
     determines how many people genuinely need rephotographing, and it may be
     far fewer than the framing analysis alone suggests.
   - Per-portrait discard percentages and the "no face is cut" finding are in
     "Portraits of real people" above.

   Raise it in the **first** conversation despite it not blocking launch.
   Coordinating a volunteer organisation on a coast to reshoot portraits has a lead
   time measured in weeks, and it is the only item in this register that cannot be
   compressed by working harder later.
6. **Site language is declared as `es-AR`** and the site timezone is
   `America/Chicago`. Both are in `Static.SQUARESPACE_CONTEXT` on every page.
   Neither is Costa Rica. Probably harmless defaults, but `es-AR` affects date and
   number formatting and any future translation work, and it is a two click fix.

## Verified, for the record

Things asserted here that were checked directly rather than assumed:

- WebP negotiation: every asset returns `content-type: image/webp` to a browser
  `Accept` header. Verified across all 72 assets.
- The 2500 px delivery cap: verified by reading the JPEG SOF and PNG IHDR headers
  off ranged GETs. `caribbean_guard_foto-transformed.jpeg` uploads at 3840x2160
  and serves at 2500x1406 for both `?format=2500w` and `?format=original`.
- Favicon equals logo: identical content length and identical decoded dimensions
  (665x677), different asset IDs.
- The duplicate `alt` and malformed focal point: read verbatim out of
  `_team.html`, counted across all 13 saved files.
- `/nosotros` and `/unete` are **byte-identical 110,979 byte files** containing
  the string `404`. Confirmed: the navigation points at two dead destinations, and
  they are the same dead destination. Flagged for `02-ia-nav`.
- Video buffering while paused: three independent runs, element state queried
  directly.
