# Hat 1 — Tourist scanning the QR at Playa Cocles

## Who I am
Foreign tourist, English with some German, never heard of Caribbean Guard, cannot picture a rip current.
On the sand at Cocles: wet hands, one thumb, screen at 40% brightness in sun, kids waiting.
Ten seconds, one question: can I go in right now, and what do I watch for.

## Findings

**1. BLOCKER — the printed sheet carries no QR code.**
Where: `out/sheets/cocles.png`, the artefact stapled to the post.
Me: the code supports `?z=cocles` and would open my beach directly (index.html:2261-2273), but this sheet has no code on it. So I land on the coast-wide view and must work out which of five beaches I am on.
Fix: put the QR on the sheet carrying `?z=<beach>`; a bare URL is a defect.

**2. BLOCKER — the panel opens with an apology, not an instruction.**
Where: beach panel, phone. `openZone` renders `todayBlock` before the status (index.html:1631-1645).
Me: in shot 03 the top 40% of the sheet is "Nobody has signed a bulletin today" plus three grey lines. I read "nobody", decide the app knows nothing, and close it. On Cocles (shot 04) the red ONLY WITH LIFEGUARDS sits below it.
Fix: keep today first in the hierarchy, but collapse the no-bulletin state to one line so the instruction is the first large thing on screen.

**3. MAJOR — nothing tells me what to do if a rip takes me.**
Where: `ripWhy` (index.html:865) renders only at index.html:1980, in the sheet for a tapped arrow.
Me: the Cocles panel says rips pull straight out with no warning (shot 04) and never says swim parallel. The sentence that could save me sits behind a tap on an arrow I do not know is tappable.
Fix: put the escape instruction in the panel of every beach whose hazard is rips.

**4. MAJOR — green cancels the words at arm's length.**
Where: card strip, Playa Negra and Punta Uva; `--low` is `#1f9d55` (index.html:926), swatch and text both green.
Me: in sun I register colour before text. Green on a safety map means go, so "TAKE CARE ANYWAY" arrives second and loses. The wording works; the palette undoes it.
Fix: take green out of the lowest tier and let the words carry it.

**5. MAJOR — four of six cards are invisible and nothing says to scroll.**
Where: `.picker`, phone (shots 02, 04), a horizontal scroller with both scrollbars hidden (index.html:126-129).
Me: I see Playa Negra and half of Salsa Brava. Cocles is card three. I do not know a third card exists.
Fix: give the row an edge fade or a position count so it announces its own length.

**6. MAJOR — the control that answers my only question looks like a map widget.**
Where: locate button, bottom right of every shot (index.html:361-372).
Me: an unlabelled crosshair under a compass. Nothing calls `getCurrentPosition` on load, only the handler at index.html:1805, so the app never offers to tell me where I am.
Fix: on first run make it a labelled dock action, "Which beach am I on?", then the icon.

**7. MINOR — the red marks on the water have no key.**
Where: zoomed map at Cocles (shot 04).
Me: red arrows and a red shaded patch on imagery. The card is the legend for the stroke (index.html:1721) but not for these, so I never learn the arrows are rips unless I tap one.
Fix: label the first arrow inline, or state the rip count in the beach panel.

**8. MINOR — the 911 pill carries no word.**
Where: topbar (index.html:349).
Me: I do not know Costa Rica uses 911 and not 112, and a bare red badge beside a language toggle reads as decoration.

Fix: pair the digits with the word.

**9. MINOR — "The rest of the coast" reads as a sixth beach.**
Where: last card in the picker (shot 01).
Me: same size, shape and row as the beaches, only greyer, so I skim past the most honest thing here.
Fix: separate it from the beach row so it cannot be mistaken for one.

## Keep

1. **Status words as instructions.** "ONLY WITH LIFEGUARDS" told a stranger what to do, with no scale to decode. This is the product.
2. **The defer line.** "If there is a lifeguard or a flag on the beach, that beats this map." It made me look up from the phone at the actual beach.
3. **"Saved on this phone · 17 Sept, 09:39."** No signal on the sand, and that bar said the page still works, with an age attached.

## Layout vote

- **Status cards:** phone, bottom thumb zone, opened scrolled to my beach not card one; desktop, one row, all six visible.
- **Legend:** phone, card swatches plus an inline label on the first rip arrow; desktop, the same plus a small key for arrows and shaded areas.
- **Beach panel:** phone, full-height sheet, instruction first, today collapsed to a line above it; desktop, the right-hand panel as it is.
- **Emergency 911:** phone, top right with the word added, and repeated as the sheet's bottom button as now; desktop, unchanged.
- **Language toggle:** phone, beside 911 with a much larger hit area; desktop, same corner, unchanged.
- **Locate button:** phone, a labelled full-width action above the cards on first run, then the icon; desktop, leave it floating.
