# AJ rescue-equipment coordinates, 2026-10-27

## What changed

- Recorded AJ's 12 Google Maps pins in `tools/data/aj-rescue-positions.json` in the order supplied. Coordinates are stored as longitude, latitude.
- Moved five close numbered markers to AJ's supplied coordinates. The 2026 map called 1.1 and 2.2 proposed; AJ's later report of installed equipment now takes precedence at those two locations. The station-number matches are spatial inferences, not labels supplied by AJ.
- Added seven unnumbered rescue-equipment markers. They appear at zoom 15 or closer so the nearby points do not stack at the initial coast view.
- Updated the bilingual popups and station-scope text to distinguish AJ's reported installations from the older 2026 map. No rip arrows, hazard bands, or four detailed Chiquita station panels changed.

## Why

The 2026 PDF registration was provisional away from its four control stations. AJ supplied more precise map pins for installed equipment. Matching a pin to a numbered station is justified only when the old mark is nearby and that station has not already been matched to another pin. We used a one-to-one 75 m limit; all seven remaining pins stay unnumbered.

## Source and matching decisions

| AJ pin | Latitude, longitude | 2026 station | Previous distance | Source |
| ---: | --- | --- | ---: | --- |
| 1 | 9.659829, -82.774681 | 1.1, formerly proposed | 48.9 m | [Google Maps](https://maps.app.goo.gl/g4UKi6KAoYrbHjif9?g_st=i) |
| 2 | 9.658682, -82.773114 | 1.2 | 46.2 m | [Google Maps](https://maps.app.goo.gl/VUiEW15C895MoacL6?g_st=i) |
| 3 | 9.657806, -82.771783 | Unnumbered | | [Google Maps](https://maps.app.goo.gl/oQXqdp8o1LpF1NgA9?g_st=i) |
| 4 | 9.656622, -82.769121 | Unnumbered | | [Google Maps](https://maps.app.goo.gl/LPSgvFn1M193dvaZ7?g_st=i) |
| 5 | 9.655148, -82.765578 | 1.3 | 30.9 m | [Google Maps](https://maps.app.goo.gl/7LWYRn9pcbKtrDVM8?g_st=i) |
| 6 | 9.654753, -82.764055 | Unnumbered | | [Google Maps](https://maps.app.goo.gl/KSqGYrc4VF3yicpU9?g_st=i) |
| 7 | 9.654149, -82.761217 | Unnumbered | | [Google Maps](https://maps.app.goo.gl/XJyqQGRVwc8zpVUm7?g_st=i) |
| 8 | 9.654887, -82.756581 | Unnumbered | | [Google Maps](https://maps.app.goo.gl/YkgzbDxSYfZuR39n9?g_st=i) |
| 9 | 9.652781, -82.739543 | 2.2, formerly proposed | 33.8 m | [Google Maps](https://maps.app.goo.gl/T7vUTq2KajDpF7qY7?g_st=i) |
| 10 | 9.648687, -82.733608 | Unnumbered | | [Google Maps](https://maps.app.goo.gl/5CwFxEYd512Sj7NZ6?g_st=i) |
| 11 | 9.651622, -82.738316 | Unnumbered | | [Google Maps](https://maps.app.goo.gl/UWGfauUkE6GfeVkP9?g_st=i) |
| 12 | 9.650193, -82.736116 | 2.3 | 17.6 m | [Google Maps](https://maps.app.goo.gl/i3sPAFLWZPSs4eXu5?g_st=i) |

Daniel confirmed that AJ's pins mark currently installed equipment. A Google Maps pin is a supplied location, not an independent survey or a check of equipment contents or current usability. The popups say the equipment was reported installed. The two proposed-to-installed updates and all five numbered identities should be confirmed directly with AJ when possible.

## How to verify

1. Run `python -X utf8 tools/project_full_annotations.py`, `npm run check:map`, and `npm run build:map`.
2. Confirm `web/data/full-map-geographic.geojson` has 12 features with `registration: aj_google_maps_pin`: five numbered and seven unnumbered. Compare their coordinates to the registry.
3. In the local map, zoom along the west coast: numbered AJ markers are visible in the overview; the seven unnumbered markers appear at zoom 15. Open each popup in Spanish and English and check the location/status wording.
4. Confirm the four detailed Chiquita station panels and all hazard geometry remain unchanged.

The 12 short links were resolved again on 2026-10-27 and each redirect coordinate matched the registry. The generator, copy check, inline JavaScript syntax check, offline build (545 asset references), and `git diff --check` passed. A before/after GeoJSON comparison found exactly five modified existing features, seven added features, and no deletions.

## Production release

- Daniel authorized updating the map-only repository and dedicated Vercel link on 2026-10-27. `master` advanced to source commit `4c574ed` with this change and the previously reviewed rip-current reference images. No PR was created and the organization website repository was untouched.
- Git-triggered Vercel builds remain disabled because satellite tiles are ignored by Git. The complete `web/` directory was uploaded through the documented Vercel CLI path to project `prj_it5kQJM4XVWkmDu3NjEzGOfCcRc3`.
- Previous production deployment: `dpl_3PbG5rnQYkM1Dw4SuaK3TxQUBRwB`.
- New production deployment: `dpl_9wsZZJ8EAzHtaKMueq446KrKhMPN`, Ready, at [the dedicated map alias](https://web-five-beta-p7wt9cgwmf.vercel.app/).
- Live HTTP checks matched the local bytes for the main document, CSS, symbols, service worker, geographic data, reference-image registry, one reference image and the logo. Representative satellite tiles were available and matched local bytes. The live geographic data contained 12 AJ features, five numbered.
- The desktop browser showed the coast and equipment markers. After accepting the map's update prompt, a numbered AJ marker's popup correctly said that AJ supplied its location, reported it installed, and that the number was inferred by proximity. A mobile visual walkthrough was not repeated for this release.

## What's left

- Obtain AJ's labels for the seven unnumbered pins and confirm the five inferred station-number matches, especially 1.1 and 2.2.
- Obtain field verification if the map is to claim surveyed accuracy, equipment contents, or current usability.
- Localhost browser QA remained blocked by the saved browser permission; the deployed desktop view and popup were verified after release. A real-phone check of the update and offline behavior is still open.

## Files touched

- `tools/data/aj-rescue-positions.json`, `tools/project_full_annotations.py`
- `web/data/full-map-geographic.geojson`, `web/index.html`, `web/coastal.css`, `web/sw.js`
- This handoff document
