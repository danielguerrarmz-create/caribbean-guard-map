# Hat 2 — Local parent, Puerto Viejo (ES only)

## Who I am
Tico from Puerto Viejo, two kids, Spanish only, mid-range Android. Weekends we go to Playa Negra or Punta Uva, late afternoon.
I know this coast, I know Salsa Brava is not for swimming, and I have seen Caribbean Guard's hand map on a sign.
In 10 seconds: is my beach OK now, where is help, is anyone watching today.

## Findings

**1. BLOCKER — Cocles orders me to use lifeguards who left at 5pm.** Status card, panel.
At 17:30 the card still reads SOLO CON GUARDAVIDAS while its own fact says "Guardavidas de 9:00 a 17:00". The only instruction I get cannot be obeyed. Evening is when families go down.
Evidence: line 568, class at 564. Fix: the instruction must know the clock; a closed post belongs on the card.

**2. BLOCKER — station pins promise gear that is gone at dusk.** Map pins 1 to 4.
The pins look permanent. The dawn-to-dusk sentence hides behind a heading reading "Equipo", so it reads as a kit list, not a schedule. At 18:00 I swim towards pin 4 expecting a rope box already taken in.
Evidence: 643-658, chrome label 774. Fix: give the pin a stocked or empty state, hours on the pin.

**3. BLOCKER — the map asserts a red-flag system nobody confirmed.** Cocles panel, facts.
"Banderas rojas marcan los canales activos" is stated flatly while your own commentary records that nobody confirmed flags here. I go looking, find none, stop believing the rest.
Evidence: 568 against the `defer` note at 716-720. Fix: unconfirmed facts get the provenance verdicts get, or get cut.

**4. MAJOR — the permission leak is in the prose, not the label.** Playa Negra panel.
The label grants nothing, then the sentence below calls this "la zona más tranquila de la costa para familias y niños", desk-written, reviewed by nobody. That sentence is what a parent acts on.
Evidence: 535-536. Fix: apply the no-permission rule to `why` and `facts`, and review the family beach first.

**5. MAJOR — two Spanish names for the thing that kills people.** Panels against map annotation.
Beach text says "corriente de retorno", the map pin says "corriente de resaca", your legend says Corriente de Resaca. I read both and think they are two phenomena.
Evidence: 553, 562, 566 against 729, 787; annotated-base-map-v5.png. Fix: one term, yours, everywhere.

**6. MAJOR — some words are not from here.** Badges and panel text.
"Sin relevar", "Fuera del relevamiento", "relevó" are Rioplatense; nobody in Limón says relevamiento. "Un parte" is peninsular, we say reporte. "Añadir" is Spain, we say agregar. These words say this was written elsewhere.
Evidence: 762-767, 738, 805. Fix: "sin recorrer", "fuera del tramo recorrido", "reporte", "agregar".

**7. MAJOR — five names for one structure.** Panels, pins, chrome.
Estación de salvamento, Estación, Puesto de rescate, Puesto de observación P.O. 4, puesto de guardavidas. Punta Uva's P.O. 4 and mapped station 4 sit about 200 m apart in the data, so I cannot tell if that is one structure or two.
Evidence: 642, 774, 538, 607, 566. Fix: one noun, theirs, and link every text mention to its pin.

**8. MAJOR — the map does not want what I know.** Whole app.
Every beach has read "Sin revisar · nadie todavía" since launch and there is no way to tell Caribbean Guard anything. I watched a rip pull a kid at Cocles last month and this app has nowhere to put that. By the third visit I stop opening it.
Evidence: all five zones `authored:"desk", reviewed:null` at 535, 550, 565, 580, 597; no contact affordance in 2,291 lines. Fix: an "Avisar a Caribbean Guard" action per beach, plus a last-changed date.

**9. MAJOR — my beach is five swipes away.** Phone card strip.
The strip is the only way in. It shows two cards, the second already clipped, no hint more exist. Punta Uva is fifth. A hunt, not two taps.
Evidence: shot 04, phone, bottom edge. Fix: one tap to a compact west-to-east list of all six.

**10. MINOR — "TEN CUIDADO IGUAL" is the wrong word order here.** Status card.
Trailing "igual" is how Buenos Aires says it. We front it: "Igual, ten cuidado".
Evidence: line 728. Fix: front the "igual".

## Keep
1. The "nobody signed today" notice with its reason underneath (reword "parte"). It separates how the beach is from how the sea is today, and no other map admits that.
2. "Si hay un guardavidas o una bandera, eso manda sobre este mapa." It puts real people above the app. Never remove it.
3. "El resto de la costa · Sin describir" as a real card. An empty stretch is not a safe stretch, and this is the only app that says so out loud.

## Layout vote
- Status cards: phone, one tap to a west-to-east list, not a blind strip; desktop, bottom strip as is.
- Legend: phone, inside the beach panel where the mark is used; desktop, bottom-left, always open.
- Beach panel: phone, sheet at 70% height so the coast stays visible; desktop, right rail, no map overlap.
- Emergency 911: both, pinned bottom-right, thumb-reachable, never in the header.
- Language toggle: phone and desktop, header, it is a once-ever choice.
- Locate button: phone, above the card strip on the right where it is; desktop, right edge, unchanged.
