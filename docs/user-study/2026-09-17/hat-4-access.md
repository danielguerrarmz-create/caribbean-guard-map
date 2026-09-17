# Hat 4 — `access`

## Who I am
Deuteranope, mildly presbyopic, budget Android (360x740, 2x DPR, low-contrast panel), Slow 3G at 2 bars, midday sun.
Red, amber and green are one olive family to me; under 14 px is guesswork; one wet thumb.
In ten seconds I need one readable sentence telling me what to do at the beach named behind me.

## Findings

**1. BLOCKER — card status line: the instruction is the smallest important type on screen.**
*Me:* "NO ENTRES AL AGUA" is 11.5 px; the optional prose in the panel is 14.5 px. What I must obey is smaller than what I may skip.
*Evidence:* index.html:137 vs 202; shot 03. *Fix:* make the instruction the largest text on the card.

**2. BLOCKER — card absence chips ("Sin revisar", "Sin relevar"): 9.5 px.**
*Me:* the "unreviewed must look unreviewed" doctrine sits at a size I cannot resolve, so every beach reads as reviewed.
*Evidence:* index.html:150. *Fix:* floor absence text at 12 px, or fold it into the status line.

**3. BLOCKER — cards and strokes: the three status colours are one colour at one lightness.**
*Me:* they render `#178049 → #61614b`, `#9c5c00 → #6f6f00`, `#c62828 → #565624`. All olive, and contrast between any two -text tokens is 1.06:1 to 1.13:1, so lightness does not rescue hue.
*Evidence:* index.html:46-48, measured. *Fix:* keep the tokens; let the swatch and word separate the tiers, never the fill.

**4. BLOCKER — strokes at the landing zoom: the dash vocabulary dies where I first look.**
*Me:* at z12 `k` clamps to 0.22, so `low`'s "2 8" floors to "2 2" (1:4 becomes 1:1) and `moderate`'s "16 10" becomes "3.5 2.2"; weights land at 1.6, 1.76 and 2.42 px. The pattern that replaces colour for me is gone.
*Evidence:* index.html:1524-1529; in shot 01 the Chiquita amber stroke totals 8 pixels. *Fix:* scale the dash by ratio, not per component; hold a minimum weight gap.

**5. MAJOR — Cocles to Chiquita: rip arrows fail non-text contrast over water.**
*Me:* arrow `(197,66,61)` on adjacent water `(45,72,65)` is 2.00:1 normally, 1.79:1 as I see it, against a 3:1 bar.
*Evidence:* sampled from shot 01; WCAG 1.4.11. *Fix:* outline the arrow, not only a drop shadow.

**6. MAJOR — first load: nothing readable paints until 147 KB of Leaflet arrives.**
*Me:* `#picker` ships empty, filling only after `vendor/leaflet.js` parses. Ten-plus seconds of navy before the first instruction word, and I need no satellite image to be told to stay out.
*Evidence:* index.html:394, 1736. *Fix:* ship the five cards as static HTML, let the script adopt them.

**7. MAJOR — beach sheet: the closed panel stays in my screen reader.**
*Me:* closing only translates it off-screen, so TalkBack swipes into "Cerrar, botón" and a panel that is not visible.
*Evidence:* index.html:1616, 1864. *Fix:* toggle `inert` and `hidden` with the open class.

**8. MAJOR — beach sheet: the dialog has no name and never takes focus.**
*Me:* I tap a card, the panel opens, TalkBack says nothing.
*Evidence:* `role="dialog"` with no `aria-labelledby` at index.html:403; `openZone` adds `.open` without moving focus, 1654. *Fix:* name it from the `h2`, move focus to the heading.

**9. MAJOR — language toggle: switching to Spanish closes the panel I am reading.**
*Me:* I open Playa Cocles, cannot read the English, tap ES, and the verdict vanishes. I must re-tap the card.
*Evidence:* `setLang` ends with `sheet.classList.remove("open")`, index.html:1864. *Fix:* re-render the open sheet instead of dismissing it.

**10. MAJOR — whole page: no focus ring exists.**
*Me:* on a switch or keyboard I cannot see what is selected.
*Evidence:* no `:focus` or `:focus-visible` rule exists in the stylesheet. *Fix:* one global `:focus-visible` outline.

**11. MINOR — top bar and saved bar: targets are legal but not comfortable.**
*Me:* language buttons 36 px and adjacent, 911 at 40 px, sheet close 38 px, refresh 34x30. All clear the 24 px floor; none reaches 44.
*Evidence:* index.html:112, 117, 275, 309. *Fix:* 44 px minimum in the top bar.

**12. MINOR — screen reader: Spanish labels persist in English; the toast contradicts itself.**
*Me:* in English, close says "Cerrar", refresh "Actualizar", the toggle group "Idioma"; only `#locate` is relabelled. The toast pairs `role="status"` with `aria-live="assertive"`, which assistive tech resolves inconsistently.
*Evidence:* index.html:350, 359, 387, 400, 1860. *Fix:* translate every `aria-label` in `setLang`; use `role="alert"` for assertive.

## Keep
1. **The card swatch draws the real map stroke.** The only channel that survives my eyes, sitting where the decision is made.
2. **Violet for TODAY, outside the hazard palette.** It simulates to `#3a3aa0`, still unmistakably blue, at 8.2:1 on white. It can never be read as a tier.
3. **Status words are instructions, and absence is stated greyly.** "NO ENTRES AL AGUA" needs no colour, and the dashed grey "nobody signed a bulletin today" block never shouts amber.

## Layout vote
- **Status cards:** phone, bottom dock, one card wide, instruction as headline. Desktop, a left rail showing all five.
- **Legend:** phone, inside each card as the swatch. Desktop, same plus a key under the rail.
- **Beach panel:** phone, bottom sheet at 74vh, retained across a language switch. Desktop, right-side card.
- **Emergency 911:** phone and desktop, top right at 44 px.
- **Language toggle:** phone and desktop, top right beside 911 at 44 px, ES and EN separated.
- **Locate button:** phone, bottom right above the dock at 52 px. Desktop, above the compass.
