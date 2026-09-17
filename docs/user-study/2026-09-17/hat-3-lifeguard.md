# Hat 3 — Caribbean Guard volunteer lifeguard

## Who I am

Volunteer guard, Spanish first, fifteen years on this coast. I drew the annotated base map V5 with a colleague: the resaca arrows, the estaciones, the ubicaciones with walking minutes.

My name goes on the "Revisado" line of every beach the day I sign, so anything wrong here becomes something I said. Tourists show me this map and ask me to confirm it.

In ten seconds I need: does it say things I did not say, and can I fix it from the tower.

## Findings

**1. BLOCKER — Today bulletin has no way in.** Beach panel, TODAY block. All five zones ship `today:null` (index.html:541, 556, 571, 588, 610) and the only writer is an edit to a 2,291-line HTML file. No form, no mailto, no contact anywhere in it. So "Nadie ha firmado un parte hoy" is permanent, and my Revisado line implies a live channel that does not exist. *Fix: a phone-sized signing surface for the guard on duty, before any signature is collected.*

**2. BLOCKER — A rescue post that is not there.** Playa Negra panel, third fact: "Puesto de rescate a 600 m al este" (index.html:538). The nearest station in the app's own data is 4.34 km east at Playa Chiquita. Six hundred metres east of Playa Negra is Salsa Brava: live coral, class no-swim. A family walking east for help lands on the reef break. *Fix: delete it, or point it at a station the data holds.*

**3. MAJOR — "Sin relevar" is computed from the marks, not the survey.** Picker chips and panel. `SURVEY` is recomputed at index.html:2013 as the min and max longitude of the fetched features, so the surveyed stretch is by construction exactly where an arrow exists. Every metre I walked and found clean is republished as "nadie las marcó". V5 names Rincón Portoño, Lanna Ben and Dragon Fly Airbnb, all outside that window. *Fix: store the sheet's extent as its own datum.*

**4. MAJOR — "perpendicular a la playa" is a bearing I never drew.** Rip sheet, `ripDir` (index.html:793, 866) and `direction` in cg-hazards.geojson. Our dangerous-area-v4 sheet shows the opposite: feeders running *along* the shore, converging, then a curved channel exiting diagonally between the rocks. Nine identical straight arrows teach a swimmer to expect the pull one way. *Fix: mark position only, no shaft bearing, until we redraw the flows.*

**5. MAJOR — The Cocles flag system.** Playa Cocles panel, third fact: "Banderas rojas marcan los canales activos". There is no flag system at Cocles. The comment at index.html:717 knows this; the fact ships anyway. *Fix: cut the bullet, keep `defer`.*

**6. MAJOR — Two Spanish words for one current.** Our legend says **Corriente de Resaca**. The rip sheet matches, but every zone record says "corrientes de retorno" (Cocles `sub` and `why`, Salsa Brava fact). One coast, two names. *Fix: resaca throughout.*

**7. MAJOR — "Estación de salvamento" is not our word.** POSTS records (index.html:646 on) and the station sheet. Our legend says **Estación de Rescate**. *Fix: use the sheet's term.*

**8. MAJOR — The Ubicaciones layer is gone.** Map, all zooms. V5 carries yellow stars for named places with walking minutes to the accesses: La Caracola and Bilbo 1 minuto, Gypsea 3, Merlin 4. None survives. That is how I tell someone where to go. *Fix: restore the stars and the minutes.*

**9. MAJOR — Rip lengths printed as measurements.** Rip sheet, `ripLen`: "Aproximadamente 38 m desde la orilla", nine values from 29 to 94 m, got by measuring hand-drawn arrows. I drew symbols. *Fix: drop the metres.*

**10. MINOR — A bulletin outlives the shift.** `TODAY_VALID_HOURS = 12` (index.html:526), a placeholder. What I sign at 09:00 reads live at 20:00, towers empty. *Fix: expire at end of shift.*

**11. MINOR — "Sin relevar" reads as shift relief.** Picker chips. To a guard, relevar is being relieved on duty, so the chip reads "nobody took over". *Fix: "Fuera del mapa anotado".*

**12. MINOR — One post, two names.** Punta Uva facts say "Puesto de observación P.O. 4"; the station sheet calls it "Playa Chiquita 4". *Fix: one name per post.*

## Keep

1. **"Revisado: nadie todavía", printed in the open.** It says plainly that no name is on this yet. That protects me until I sign, and it is the reason I would sign.
2. **`defer` under every tier.** "Si hay un guardavidas o una bandera en la playa, eso manda sobre este mapa." On my own sand I am still the authority. Never soften it.
3. **The station scope sentence.** Four here, nine on the coast, do not count on these being all. An honest sentence about my own programme, and a rare one.

## Layout vote

- **Status cards:** phone, horizontal strip pinned at the bottom under the thumb; desktop, same strip along the bottom edge.
- **Legend:** phone, inside the cards as the stroke swatch, as now; desktop, a small fixed key bottom-left in the V5 words.
- **Beach panel:** phone, sheet over the lower two thirds with the map still visible; desktop, a right-hand column, not an overlay.
- **Emergency 911:** phone, top-right, always visible, never scrolled away; desktop, same corner.
- **Language toggle:** phone, top-right beside 911 but visibly smaller; desktop, same.
- **Locate button:** phone, right edge just above the card strip, one-handed reach; desktop, right edge above the compass.
