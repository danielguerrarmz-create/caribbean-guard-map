# Map motion, decluttering and caption review

Date: 2026-11-03
Status: Local main-app implementation for review. No deployment.

## Motion precedents

- [amCharts: Map with Animated Lines](https://www.amcharts.com/demos/map-with-animated-lines/). Live demo visually inspected. A line travels between moving endpoints along an invisible guide. Direction is carried by the motion, with restrained line weight. Their discussion also cautions against constant motion across too many routes. Adopted principle: one traveling stroke per curve, with quiet intervals.
- [Mapbox: Animate a point along a line](https://docs.mapbox.com/mapbox-gl-js/example/animate-point-along-line/). Official example advances a point through a continuously updated position. Adopted principle: continuous forward progression rather than discrete steps or repeated dashes.
- [Windfinder: Forecast overlays](https://www.windfinder.com/help/weather-maps/forecast-overlays). Particle speed represents forecast wind speed. That relationship is unsuitable for source-map rip annotations without measured velocity. This consumer therefore uses a consistent symbolic cycle, independent of hazard strength.

No third-party code or assets were copied. These are motion precedents, not new runtime dependencies.

## Consumer adaptation

The previous 6/18 px repeated dash cycle was visually busy and read as a conveyor belt. The replacement has one 18%-length red sweep on each curve. SVG pathLength=100 normalizes it across zooms. The sweep travels toward the fixed head over 80% of a 3.6 s cycle, softly appearing/disappearing at the ends, with a 20% quiet interval. Source-coordinate-derived negative delays stagger neighboring arrows deterministically. The underlying 2 px opaque red shaft and filled head never fade. Reduced-motion users retain those static arrows; map gestures pause the sweep.

## Marker visibility

Geographic data and anchors are unchanged. Screen-space hit boxes reserve six pixels of clearance. Rescue markers always remain, then access markers, then contextual places. Only overlapping lower-priority markers are hidden. They return when zoom separates them or a blocking layer is disabled. Suppressed markers leave keyboard traversal and accessibility output until they return. Access routes and source features are not deleted. This step does not cluster overlapping rescue markers at coast overview.

## Caption decisions, both languages

| Location | Change |
| --- | --- |
| Legend | Removed the zoom/moving-current explanatory paragraph; retained Sources and accuracy |
| Beach list | Removed distance-origin caption; value tooltips and accessible labels retain origin and straight-line meaning |
| Overview forecast | Removed scope footnote; button is Coastal forecast, with the 24-hour range |
| Beach overview | Removed repeated review/live-condition sentence; Sources and review retains provenance |
| Swim advisory | Moved recent-data bookkeeping inside Why and what is missing; incomplete/stale data remains visible |
| Detailed forecast | Consolidated scope, direction convention, provider and retrieval timestamps into About this forecast |

Emergency instructions, actual restrictions, missing-data errors, field-verification limits on access details, and required map attribution remain. Expanding forecast details survives refresh and preserves keyboard focus.

## Verification

38 Node tests pass, including collision priority, six-pixel boundary, coordinate immutability, reappearance and all 53 rip curves through zoom redraw. Copy check and offline build pass (547 assets). Desktop and mobile rendered checks found no access/place overlaps. Desktop access count increased from 13 to 16 when the rescue layer was hidden, without moving the map. All rendered sweep paths report pathLength 100, 3.6 s duration and distinct delays. Consumer screenshots and audit JSON are in out/visual-review/declutter-*.
