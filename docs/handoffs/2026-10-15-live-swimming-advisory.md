# Swimming advisory: research and first implementation

Date: 2026-10-15
Status: local experimental prototype, not validated for public swimming decisions. No push or deployment.

## Finding

The sources reviewed do not establish a universal wave-height or wind-speed cutoff that certifies swimming safety. Do not substitute offshore swell height for breaking surf, or modelled ocean currents for local rip-current measurements. A meaningful local classifier needs beach-specific validation and observations.

## Published guidance and its implications

| Primary source | Established guidance | Application here |
| --- | --- | --- |
| [ILS beach-safety tips](https://www.ilsf.org/safety-tips/) | Check water conditions, use lifeguarded areas, follow signs and designated swimming zones. | Local instructions take precedence. A timetable cannot establish current lifeguard presence. |
| [ILS LPS-14, flags, 2010](https://www.ilsf.org/wp-content/uploads/2019/01/LPS-14-2010-Flags.pdf), still listed on the [ILS position-statements index](https://www.ilsf.org/lifesaving/position-statements/) | Yellow denotes moderate hazards; red denotes high hazards; double red denotes closure; red/yellow identifies lifeguard supervision. | These are communication meanings, not numerical wave/wind thresholds. No flags are set automatically, no legal closure is asserted, and no compliance certification is claimed. |
| [NWS rip-current forecasting](https://www.weather.gov/ilm/ripcurrents) | The US model uses nearshore waves and tides and is refined with lifeguard reports. Forecasters also account for known biases. Rip currents can form in small surf. | Do not transplant US probabilities to Costa Rica or implement a wave-only traffic light. Need beach orientation, nearshore transformation, tide context, morphology and field evidence. |
| [NWS lightning guidance](https://www.weather.gov/safety/lightning-tips) | Hearing thunder warrants shelter in a substantial building or enclosed hard-topped vehicle; wait at least 30 minutes after the last thunder. | Display this guidance. A forecast is not an observed thunder event and cannot start or finish a reopening timer. |
| [MIO CIMAR services](https://miocimar.ucr.ac.cr/sobre-el-mio) and [local forecasts](https://miocimar.ucr.ac.cr/pronosticos-locales/) | Costa Rican oceanographic service provides wave/wind forecasts and commentary for bathers. Its [2023 bulletin](https://miocimar.ucr.ac.cr/advertencias/244) identifies CNE as the official alert authority. | Use these as local review sources. The old bulletin is historical evidence of procedure, not an active alert or a reusable numeric trigger. No automatic MIO/CNE feed has been integrated or its absence interpreted as no alert. |
| [Open-Meteo marine API](https://open-meteo.com/en/docs/marine-weather-api) | Model outputs include waves and swell. Modelled tide/current resolution and coastal accuracy are limited. | Regional context only. No live local rip detection or water-quality inference. |
| [Open-Meteo weather API](https://open-meteo.com/en/docs) and [weather-code reference](https://open-meteo.com/en/docs/gem-api) | WMO-style weather codes include thunderstorms (95, 96, 97, 99). | Request hourly weather codes alongside wind. Treat forecasts as model evidence, never sensor observations. |

These are safety guidance and source limitations, not a locally adopted Caribbean Guard operating standard.

## What changed

- Added a pure, versioned `CGAdvisory.evaluate` function with explicit reasons, missing inputs, source times and a permanently false `clearance` field.
- Reference no-swim guidance remains restrictive through calm forecasts and outages. Lifeguard-only guidance never assumes staffing from hours.
- Current/recent and next-three-hour regional thunderstorm model signals produce a draft stay-out advisory. This conservative three-hour planning window is our product choice, not an ILS/NWS rule or proof of lightning at a beach.
- Other outcomes require checking conditions locally or report an unassessed beach. No automated reopening, safe label, probability, score, or wave/wind threshold has been added.
- Marine and weather completeness are checked separately. Invalid, negative, null, expired and future-dated samples cannot become current evidence. A valid storm signal is retained even if other inputs are missing.
- The bilingual beach, access/QR and regional forecast panels show the experimental advisory, with reasons and sources available below it. Existing emergency guidance and 911 remain visible.
- Hourly weather codes join the existing live API request. Existing 15-minute refresh and one-minute expiry checks update the advisory. Service-worker packaging includes the new module.

## Implementation choices, not safety standards

| Setting | Value | Meaning |
| --- | --- | --- |
| Policy version | draft-1 | Identifies this prototype's behavior. |
| Fetch freshness limit | 3 hours | Cache/data-age guard; not proof of forecast accuracy. |
| Current sample age | 1 hour | Stricter than the existing context strip. Future current timestamps are rejected. |
| Storm planning horizon | 3 hours | Current model plus every hourly sample spanning this interval. |
| Refresh cadence | 15 minutes while active | Inherited polling cadence; not model production frequency. |
| Wave/wind thresholds | Unset | No locally validated numerical rule was found in the sources reviewed. |

No official-closure, water-quality, observed lightning, confirmed staffing, live rip-current or local incident feed is connected. Existing source-map current arrows remain provisional reference geometry. This feature does not validate them or move them to match a forecast.

## How to verify

1. Run `node --test tools/tests/*.test.mjs`, `npm run check:map`, `npm run build:map` and the site export checks after packaging.
2. Open `/mapa?z=playa-negra`: emergency section stays expanded; experimental guidance appears above the forecast. Inspect the reasons and model time.
3. Open Puerto Viejo: reference no-swim guidance must survive a calm or missing model. Open Cocles: lifeguard presence must remain unconfirmed. Open Playa Grande: no assessment is inferred from available weather.
4. Change ES/EN and refresh the forecast. The selected beach and open reasons disclosure must survive refresh.
5. Check desktop and 390px mobile, including the QR entry. No advisory is a new emergency button or a replacement for the persistent 911 control.
6. Unit scenarios cover forecast storm codes, nonaligned timestamps, incomplete/invalid data, expiry, static restriction precedence and no clearance after a storm signal disappears.

## What's left before operational use

- Caribbean Guard and a qualified local coastal/lifesaving reviewer must define scope, response ownership and beach operating procedures.
- Confirm source classifications, swimming sectors, rescue coverage, current staffing and usable observation/reporting workflows.
- Establish permitted official alert ingestion with source, geography, issued time, expiry and withdrawal semantics. Do not scrape a bulletin and silently assume it is current.
- Collect aligned local observations of breaking surf, rips, flags/closures, tide and model inputs. Evaluate proposed rules on held-out periods and across seasons; document false negatives and uncertainty for each beach. An expert should set acceptance criteria before validation.
- Define secure observation publishing and closure/reopening authority as a separate backend/auth task. This prototype deliberately has no public report switch that can clear a beach.
- Obtain explicit owner release approval after policy and field validation. Leave merging/deploying to the owner.

## Files touched by this addition

`web/advisory.js`, `web/index.html`, `web/coastal.css`, `web/sw.js`, `tools/prepare_site_assets.mjs`, `tools/tests/advisory.test.mjs`, this document. Earlier uncommitted map/QR/forecast changes are preserved.

## Verification record

- 16 Node tests passed, including 8 new advisory scenarios; the final advisory rerun also passed.
- Map copy checks passed. Packaging verified 538 offline references, including the advisory module. All 4 website export checks passed.
- Inline script syntax and whitespace checks passed. No new Next components were changed by this addition; the full Next build was not repeated.
- Browser checked at desktop and 390 x 844: visible 911 and current escape instructions, bilingual advisory, expandable reasons, forecast refresh, no-swim Puerto Viejo, lifeguard-required Cocles, unassessed Playa Grande and the Chiquita QR entry. Live model data loaded and the QR navigation had no reported console errors.
- Storm/expiry/invalid-data conditions were exercised with deterministic tests, not an actual storm observation or an operational field trial. No local safety validation is implied by passing software tests.
- Local preview: http://127.0.0.1:5198/mapa?z=playa-negra . Mobile review image: `out/advisory-mobile.jpg` (ignored QA artifact).
