# Cartographic precedents after rejected first study

Date: 2026-11-03
Status: Research complete; replacement map treatment not yet designed or approved.

## Daniel's corrections are the new brief

1. The original rip strokes were copied from a drawing. Preserve approximate location and intended direction, not exact endpoints, hand-drawn wiggles or tiny terminal bends. A single consistent mathematical curve family is explicitly permitted.
2. Reject the thick white casing on both arrows and shorelines. Fix every arrowhead as a system, not individual exceptions.
3. Both the reference ribbon and hatched band renditions are rejected. Their old recommendation is superseded. Phosphor Regular and the quieter application layout remain selected.

The prior instruction to preserve every rip vertex was an unnecessarily literal interpretation on our part. Keep original annotations as evidence, and derive simplified display symbols separately. This permission concerns illustrative current strokes; it does not authorize straightening the geographic shoreline, moving equipment, changing risk classes or inventing current measurements.

## Visually inspected precedents

Review board: http://127.0.0.1:5196/research.html

### 1. Copernicus Marine: current vector map

[Official tutorial and figure](https://help.marine.copernicus.eu/en/articles/7044577-how-to-plot-current-vectors-with-python), updated September 29, 2026. Inspected the actual Agulhas figure in the browser.

Black arrows have compact filled heads and a consistent construction. Blue shading is a separate layer. The documentation explicitly controls arrow density and scale; length and background color encode modeled velocity. The useful visual principle is consistent arrow grammar and deliberate spacing. Caribbean Guard should borrow that discipline, not the velocity scaling or an invented field of evenly distributed arrows. Our proposed curves are a design adaptation, not something demonstrated by this straight-vector figure.

### 2. SLSA Beachsafe: Bondi Beach

[Selected beach](https://beachsafe.org.au/beach/nsw/waverley/bondi-beach/bondi-beach). Inspected its hazard list, general hazard rating and map.

The map uses a quiet street basemap, a beach marker, a label and a broad selection circle. Specific hazards are explained separately with symbols and words. It does not trace each listed rip on this view. Take the separation of location, selection and hazard information. Do not copy the literal yellow circle as a hazard boundary, the flags as our standing risk classes, or its long grid of sign icons as our UI aesthetic. Some neighboring symbols did not render completely in this session.

### 3. Coogee SLSC: hazard and risk management map

[Patrol Operations Manual 2024/25, printed page 11](https://www.coogeesurfclub.com.au/uploads/1/3/1/7/131710500/coogee_slsc_patrol_operations_manual_2024-25.pdf#page=11). Rendered and inspected the full page.

The satellite map uses localized red marks and an adjacent text label for a recurring rip, rather than coloring the entire coastline. Other hazards have separate labeled marks. This supports attaching explanation to a particular hazard location. Its dense red texture and older graphic styling are not a quality target. The patrol context also differs from a visitor app. Do not copy its flags, data or source imagery into the app.

### 4. NOAA/NWS: South Florida beach forecast

[Live experimental forecast map](https://www.weather.gov/beach/forecast?site=mfl&action=). Visually inspected the regional view on November 3, 2026.

The displayed view uses broad red coastal regions, separate beach targets, an issue time and an explicit risk legend. It is effective at regional classification, but the large saturated strip would recreate much of what Daniel rejected. Borrow the distinction between region-level risk and individual beach targets, not its band width, umbrella artwork or current forecast values. Caribbean Guard's standing classifications are not equivalent to this issued forecast.

### 5. Ventusky: sea currents

[Current layer](https://www.ventusky.com/sea-map/currents). Inspected the moving flow texture and speed legend over the western North Atlantic.

Fine trails form a continuous field over a colored magnitude layer; muted land gives the water data priority. This supports reducing basemap competition instead of adding heavy outlines. It is not a suitable literal transfer: the texture is tied to modeled currents, with a time and speed scale. Our sketches do not provide such a vector field. Neither the animation, palette nor proprietary renderer has been extracted.

### 6. NOAA/DMA: historical chart symbol sheet

[Chart No. 1, sixth edition, July 1975](https://repository.library.noaa.gov/view/noaa/49552/noaa_49552_DS1.pdf). Rendered printed pages 13 and 15 (PDF pages 18 and 20).

Current symbols use thin shafts and compact directional heads. Area limits use distinct fine line patterns and labels; some show optional tints. The useful lesson is to separate a directional symbol, an area edge and its explanation. This is explicitly a historical visual reference, not current navigation guidance or a specification for our app. Current NOAA and NGA publication pages were consulted, but their current full PDF was too large or unavailable through the initial web fetch.

## Revised design direction to test

### Arrow construction

- One quadratic Bezier family per arrow, with a single broad bend. Use the sketch's approximate shore origin, overall heading and bend sense as input; ignore terminal wiggles. Do not force the tip onto the old last vertex.
- Use one normalized construction, rotated and scaled into place. A starting model is `B(t)=(1-t)^2 P0+2(1-t)t C+t^2 P2`. A shared bow-to-length ratio makes the family coherent; straight arrows are the zero-bow case. This equation is our proposed implementation, not a borrowed standard.
- Orient every head to the terminal curve tangent `P2-C`, rather than the last sampled segment of the drawing. Use one head definition for all arrows, fixed in screen pixels. The shaft must meet the head cleanly without protruding beyond it.
- Begin the next proof with a roughly 2 px single-color shaft and compact 6-7 px filled head, with no white casing. Those are trial dimensions, not accepted production values. Test a restrained coral against both the existing image and a quieter basemap treatment.
- Keep arrow size independent of supposed flow speed. Keep the original annotations intact and separately available as source evidence. Review all arrows for intended seaward or alongshore direction after simplification, including unusual bends; no blind normalization that reverses intent.

### Areas and hierarchy

Test two materially different approaches, not thinner versions of the rejected white-edged strip:

1. **Label-led overview, selected-area tint:** beach name plus concise risk text/symbol carries the standing classification. Leave the coastline visually quiet. Selecting a beach adds a low-opacity, flat, single-color indication within the existing display corridor, without a heavy perimeter. This is a selection aid, not a claim about measured hazard extent. Current arrows remain distinct from that selection.
2. **Fine boundary with sparse identification:** if an always-visible area boundary proves essential, compare one fine broken edge with an explicit area label and no full hatch or white casing. Pattern has a defined semantic purpose; it is not decorative texture. This option still needs careful review because an offshore edge may be misread as an exact limit.

The first option is my current hypothesis, not a new approved recommendation. Compare both on the same viewport, imagery and geography. Keep area classification, rip presence and operational staffing separate. Do not suppress a hazard merely to obtain a cleaner screenshot.

### Basemap contribution

The current satellite image has bright foam, dark sea, roads, reefs and vegetation at once. Try modest saturation and contrast reduction on the imagery, and compare a restrained cartographic base if suitable licensed assets are available. Do not wash out shoreline detail or solve every local contrast problem by outlining every symbol. No new map provider, paid imagery or external basemap dependency is introduced by this research.

## Acceptance for the next proof

- All arrowheads use the same dimensions and tangent alignment; no hooks, double tips, white perimeter or last-vertex artifacts.
- One smooth curve per annotation conveys the broad intention; source evidence remains intact.
- At least one view has no continuous risk ribbon or hatch at rest.
- Risk wording remains visible without relying solely on color. Selected state must not imply that unselected water is safe.
- Evaluate the same representative beach at coast, beach and close scales, plus a 390 px mobile view. Check every annotation, not just the most attractive three.
- Keep Phosphor Regular at its original weight. Resolve equipment overlap independently rather than hiding it behind revised cartography.
- Get visual review of this one replacement screen before rolling the system through the application.

## Research artifacts and reuse

The board contains attributed screenshots and page renders for design criticism only. These are not open-source app assets and do not enter `web/` or package exports. Original PDFs and full captures remain in local scratch. Burondono receives a reference and decision record; no new third-party component or renderer has been copied. Any future reusable curve/arrow primitive needs its own implementation, provenance and validation in the appropriate package.


## Proof 03 implementation

Built at http://127.0.0.1:5196/proof.html. The comparison implements both hypotheses on the same map, with one normalized quadratic family (signed bow ratio 0.22, or zero for nearly straight inputs), arc-length sampling to remove terminal wiggles, tangent-aligned 7 x 6 px heads and 2 px single-color shafts. Original annotations remain unchanged. The two area treatments share geography and risk wording. Neither is approved for application rollout yet.

Reviewed the 53-annotation atlas, desktop comparison, 390 px stacked phone layout, synchronized zoom, beach switching and selected/unselected state. Captures are in ignored `out/visual-review/proof03-*.png`. The original curve module and its provenance are mirrored as an experimental reference in Burondono, outside public exports. Equipment positions and their coast-scale overlap remain separate work.
