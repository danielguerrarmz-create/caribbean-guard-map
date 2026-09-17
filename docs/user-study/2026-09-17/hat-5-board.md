# Hat 5 — AJ (James A. Smith) and the Caribbean Guard board

## Who I am
Forsite Studio principal who commissioned this and has to put my name beside it in front of a volunteer board.
I am on a laptop, sharing my screen, ten minutes before we vote on publishing it to caribbeanguard.org and printing QR signs.
In ten seconds I need to know: can we defend every word on it, does it look like us, and who keeps it true after today.

## Findings

**1. BLOCKER — Sheet, the TODAY block (every beach).** The most prominent block on every beach leads with "Nobody has signed a bulletin today," and nobody ever will: signing means editing JavaScript and redeploying. I would be approving a daily-signature feature no volunteer of ours can operate, and a permanent grey box teaches readers to skip the one line that would carry a real warning. *Evidence:* all five zones `today:null`; `TODAY_VALID_HOURS` comment at line 528 says "nobody has told us yet." *Fix:* name the person and the signing path, or ship without the TODAY axis and add it when the process exists.

**2. BLOCKER — Card strip and every sheet, provenance.** Every beach reads "Not reviewed" and "Not surveyed." We would publish five verdicts under our name that no guard of ours has confirmed, and in twelve months `CHARACTER_VALID_DAYS = 365` flips all five to "Review expired" with no owner. The honesty is right; the timing is not. *Evidence:* `reviewed:null` on all five zones and all four stations; shot 01. *Fix:* get one named guard to sign all five before launch, so the map ships reviewed and the machinery proves itself.

**3. BLOCKER — The address.** A QR sign is permanent once it is screwed to a post. Printing `caribbean-guard-map.vercel.app` means reprinting every sign the day we move it, and a tourist reading a vercel.app string has no reason to believe it is us. *Evidence:* live URL; `start_url` in manifest.json. *Fix:* put it on a caribbeanguard.org address before anything goes to print.

**4. MAJOR — Top bar, the wordmark.** Nothing anywhere links back to caribbeanguard.org. Our highest-traffic tourist touchpoint is a dead end with no "Donar ahora," no who-we-are, no way home. *Evidence:* the only outbound links in the file are two Google Maps directions calls, lines 1652 and 1709. *Fix:* make the wordmark a link home and put one quiet donate line at the foot of the sheet.

**5. MAJOR — Sharing the link.** When I paste this into the board WhatsApp it arrives as a bare URL with no title and no picture, because `card.jpg` ships but nothing references it. The image itself is a tilted screenshot on navy with the last card sliced off. *Evidence:* no `og:` or `twitter:` tags in index.html; card.jpg. *Fix:* wire a proper share card, redrawn, not screenshotted.

**6. MAJOR — Sheet, marked area and station scope.** The page tells the public that our own map has a red shape whose meaning our legend does not define, and that we claim nine stations but can only show four. Both are true internally. Published, they read as the association contradicting itself. *Evidence:* `areaWhy` line 867; `stationScope` line 856. *Fix:* one phone call to whoever drew v5 settles both before launch, not after.

**7. MAJOR — Desktop landing.** What the board sees first is the phone stretched to 1568px: a row of small tiles clipped by the bottom edge, no legend, no title, no explanation of what this is. *Evidence:* shot 01, bottom-right card cut off; the only desktop rule in the CSS moves the sheet, line 336. *Fix:* give desktop a left column holding the beaches, the legend and a short "what this map is."

**8. MAJOR — Map, no legend.** Four blue numbered circles sit on our coast meaning nothing until tapped, and the three coast strokes are only explained on the picker cards. Our own v5 carries a bilingual legend box in the corner. *Evidence:* shot 01 versus annotated-base-map-v5.png. *Fix:* a small always-visible legend, in our map's two-column bilingual style.

**9. MAJOR — Whole map, our visual vocabulary.** v5 is a wayfinding map: yellow stars for the lodgings people are actually staying in, with walking minutes to the nearest rescue point, blue roads, orange stations. None of that survives, and stations changed from orange to blue. It has become a swim-verdict map and stopped being ours. *Evidence:* annotated-base-map-v5.png. *Fix:* bring back the stars and the walking times as a layer; keep the station colour we already use.

**10. MINOR — Nowhere in the product.** No contact, no email, no WhatsApp, no "this is wrong, tell us." A safety instrument with no correction channel keeps a known error forever. *Fix:* one report-an-error line in the sheet footer.

**11. MINOR — Saved bar and app icon.** On the board's laptop it says "Saved on this phone," and the home-screen icon is the letters CG typed on navy. Small things, but they are what a donor screenshots. *Evidence:* shot 01; icons/icon-192.png. *Fix:* device-neutral wording; a real mark.

**12. MINOR — Map labels.** "PUERTO VIEJOPlaya Cocles" runs together and the station pins sit on top of "Playa Chiquita." *Evidence:* shots 02 and 04. *Fix:* collision-aware label placement.

## Keep
1. **The deferral sentence under every tier.** "If there is a lifeguard or a flag on the beach, that beats this map. This map cannot see today's sea." It is the sentence I would want read aloud in any inquiry, and it is on every level, not only the calm ones.
2. **The rest-of-the-coast card.** Listing what we have not described as a peer of what we have is the most defensible thing on the page, and it is where a board would otherwise be exposed.
3. **Provenance directly under the claim, in two fields.** Author and Reviewed, separately, beneath the verdict rather than in a footer. That is what turns a guarantee into a dated statement.

## Layout vote
- **Status cards:** phone, bottom scroll strip as now. Desktop, a fixed left column, all six visible, no scrolling.
- **Legend:** phone, inside the card swatches as now plus one line in the sheet. Desktop, permanent, top-right, bilingual, in v5's style.
- **Beach panel:** phone, bottom sheet as now. Desktop, right-hand panel as now, but never overlapping the coast it describes.
- **Emergency 911:** phone, top-right as now. Desktop, same position but showing the number as text, since a laptop cannot dial.
- **Language toggle:** both, top-right beside 911 as now. It is correct where it is.
- **Locate button:** phone, above the dock as now. Desktop, keep it but demote it; nobody locates themselves from a laptop.
