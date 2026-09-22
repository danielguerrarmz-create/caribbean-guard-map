# Map system and role walkthrough, 22 September 2026

## Design and registration decisions

The GPS satellite map remains the only map. The 53 PDF rip-current arrows with actual arrowheads retain their source direction and curve, but their beach-facing endpoints are anchored about 3–24 m seaward of the OpenStreetMap GPS shoreline after the reviewed place-control correction. This removes the largest document registration offsets. The registration audit passes for all 53 arrows. These are approximate *mapped hazard indications*, not observed currents, surveyed positions, navigation instructions, or rescue-dispatch data. The desktop legend's Sources and accuracy disclosure says this explicitly. The colored selection band is built from the same GPS shoreline and now begins at the coast instead of starting 25 m offshore.

The visual system uses a common 24-unit, 1.9-unit-stroke pictogram vocabulary for beach guidance, annotation controls, and coastal forecast. Pictograms accompany words; color never carries a safety verdict alone. Circular badges identify a type, dashed outlines mean proposed, and the current line ends in an open chevron. These are project pictograms, **not certified ISO 20712-1 water-safety signs**. The visible map control contains five annotation layers only. Roads and source caveats sit under the same control; redundant beach-guidance keys were removed.

Desktop composition at the tested 1280 × 720 viewport: 80 px header, 390 px rail, 20 px rail content inset, 50 px minimum beach rows at shorter heights, and a compact forecast below the six entries. The legend is a single pill at the upper right until opened. Typography has three clear tiers: 22–27 px place/rail title, 13–18 px action and beach names, 10–12 px labels and attribution. White and pale blue-gray are neutral surfaces; red, amber, and green are reserved for their labeled safety meanings. The main road is a thin neutral line at overview, with local paths, place points, and rip arrows revealing as zoom increases. Open chevrons and a whole-arrow fade appear on rip arrows at detailed zoom; reduced-motion preference disables the animation.

## Walkthrough 1: local resident

Path: land on the coast at desktop overview, scan all six beach entries, choose Playa Negra and Playa Cocles, read the guidance, compare the highlighted coast and mapped road. Finding: at 1280 × 720, the original row height let the forecast cover the final beach. Fix: use 50 px list rows at shorter desktop heights, smaller badges and two-line text hierarchy, and reduce forecast padding. All entries and the forecast now fit, including when the live model loads. The selected Cocles band was visibly offset offshore; it now starts on the GPS shoreline. The 911 link remains `tel:911` in the panel and header. I did not trigger a call or external directions.

## Walkthrough 2: tourist

Path: open Playa Cocles at 390 × 844, read the first mobile sheet, verify the emergency action, close it, inspect the collapsed and expanded layer control, and return to desktop. Finding: the mobile first sheet shows the status and Call 911 but requires scrolling or Show more for the longer rip instruction; this is acceptable because the emergency action remains in the first view and the sheet visibly scrolls. The expanded legend stays within the mobile viewport. The forecast icon set now uses the same SVG system as the beach and annotation symbols, avoiding platform-dependent glyphs.

## Walkthrough 3: Caribbean Guard member

Path: open the layer control, hide and restore Rip currents, compare the coast at overview and beach zoom, inspect sources/accuracy, and verify the prior proposal labeling logic. Finding: the earlier full key duplicated beach status, and bright blue main roads competed with safety strokes. Fix: keep only five annotation toggles and tone roads down to a thin neutral line. The rip layer toggle changed state immediately and restored. At overview, main roads, named beaches, and the main station remain visible while arrows and small points are withheld. At detailed zoom, arrows appear from the coast with open chevrons. The previous walkthrough's short marker popups, named place accessibility, proposed-equipment caveat, safety-first panel order, and weather placement remain intact.

## Verification and limits

`python -X utf8 tools/project_full_annotations.py`, `python -X utf8 tools/audit_rip_registration.py`, `npm run check:map`, `npm run build:map`, JavaScript syntax checks, and `git diff --check` passed. Desktop and 390 × 844 browser previews were inspected. The underlying PDF has no geographic CRS; OSM geometry and hand-reviewed place controls improve alignment but do not establish metre-level accuracy. Field validation remains necessary before the annotations can support operations.

### Follow-up visual correction

Reviewing the original PDF revealed six red dashed context strokes with no arrowhead that had been counted as rip currents. The 53 true arrows each match a separate filled triangular head; twelve PDF path sequences run backward and are now reversed during extraction. This preserves the authored seaward direction. The map uses a restrained cubic through the source path's quarter points, a wider open chevron, and a synchronized fade across each entire arrow instead of a moving dash. A neutral border replaces the colored left edge on every beach guidance card. The shoreline registration remains approximate.

References: [Google Maps control patterns](https://developers.google.com/maps/documentation/javascript/controls), [Google Maps zoom-dependent point density](https://developers.google.com/maps/documentation/android-sdk/cloud-customization/poi-behavior-customization), [USWDS icon accessibility](https://designsystem.digital.gov/components/icon/accessibility-tests/), [ISO 20712-1 scope](https://www.iso.org/obp/ui/?_escaped_fragment_=iso%3Astd%3Aiso%3A20712%3A-1%3Aed-1%3Av1%3Aen).
