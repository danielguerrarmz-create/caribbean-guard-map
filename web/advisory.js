/* Experimental advisory policy v1. Published guidance and limits:
 * docs/handoffs/2026-10-15-live-swimming-advisory.md
 * No wave/wind thresholds are calibrated for these beaches. No clearance output.
 * Forecast freshness and the 3-hour planning window are product settings, NOT
 * swimming-safety standards. Regional models do not observe the surf zone.
 */
(function (root) {
  'use strict';
  const POLICY = Object.freeze({version:'draft-1', maxFetchAge:10800, currentMaxAge:3600, horizon:10800});
  const STORMS = new Set([95,96,97,99]);
  const WEATHER_CODES = new Set([0,1,2,3,45,48,51,53,55,56,57,61,63,65,66,67,71,73,75,77,80,81,82,85,86,95,96,97,99]);
  const finite = n => typeof n === 'number' && Number.isFinite(n);
  const nonnegative = n => finite(n) && n >= 0;
  function fresh(at, now, age) { return finite(at) && at > 0 && at <= now && now - at <= age; }
  function snapshot(value, fetchedAt, now) {
    return fresh(fetchedAt, now, POLICY.maxFetchAge) && fresh(value?.time, now, POLICY.currentMaxAge) ? value : null;
  }
  function evaluate({beachClass=null, marine=null, weather=null, weatherHourly=null,
    marineFetchedAt=0, weatherFetchedAt=0, now=Date.now()/1000} = {}) {
    if (!finite(now) || now <= 0) throw new TypeError('Advisory requires a valid Unix timestamp in seconds');
    const sea = snapshot(marine, marineFetchedAt, now);
    const air = snapshot(weather, weatherFetchedAt, now);
    const marineComplete = !!sea && ['wave_height','wave_period','swell_wave_height','swell_wave_period'].every(k=>nonnegative(sea[k]));
    const windComplete = !!air && ['wind_speed_10m','wind_gusts_10m'].every(k=>nonnegative(air[k]));
    const weatherFresh = fresh(weatherFetchedAt, now, POLICY.maxFetchAge);
    const start = Math.floor(now/3600)*3600;
    const hours = Array.from({length:4}, (_,i)=>start+i*3600);
    // Match times, never array positions. Missing/invalid codes are unknown.
    const samples = hours.map(time=>{
      const matches = weatherFresh && Array.isArray(weatherHourly?.time)
        ? weatherHourly.time.flatMap((t,i)=>t===time?[weatherHourly.weather_code?.[i]]:[]) : [];
      // Duplicate timestamps are malformed. Retain a storm signal, but never
      // count conflicting/duplicated entries as complete coverage.
      return {time, code:matches.find(c=>STORMS.has(c)) ?? (matches.length===1?matches[0]:null), complete:matches.length===1 && WEATHER_CODES.has(matches[0])};
    });
    const stormTimes = samples.filter(s=>STORMS.has(s.code)).map(s=>s.time);
    if (air && STORMS.has(air.weather_code)) stormTimes.push(air.time);
    const thunderstorm = stormTimes.length>0;
    const weatherComplete = !!air && WEATHER_CODES.has(air.weather_code) && samples.every(s=>s.complete);
    const reasons = [];
    if (beachClass === 'no-swim') reasons.push('standing-no-swim');
    if (thunderstorm) reasons.push('regional-thunderstorm');
    if (beachClass === 'high-risk') reasons.push('lifeguard-required');
    if (!['no-swim','high-risk','conditional','lower-risk'].includes(beachClass)) reasons.push('beach-unassessed');
    if (!marineComplete) reasons.push('marine-incomplete');
    if (!windComplete || !weatherComplete) reasons.push('weather-incomplete');
    reasons.push('local-observation-missing','wave-wind-policy-unvalidated');
    const decision = beachClass === 'no-swim' || thunderstorm ? 'avoid-water'
      : beachClass === 'high-risk' ? 'lifeguard-required'
      : reasons.includes('beach-unassessed') ? 'unassessed' : 'check-locally';
    return {
      policy:POLICY.version, decision, clearance:false, reasons,
      thunderstorm, stormAt:thunderstorm?Math.min(...stormTimes):null,
      coverage:marineComplete && windComplete && weatherComplete?'available':'incomplete',
      window:{from:now,to:now+POLICY.horizon}, evaluatedAt:now,
      inputs:{marineAt:sea?.time??null, weatherAt:air?.time??null,
        marineFetchedAt:fresh(marineFetchedAt,now,POLICY.maxFetchAge)?marineFetchedAt:null,
        weatherFetchedAt:weatherFresh?weatherFetchedAt:null},
      missing:['local-rip-observations','lifeguard-presence','official-alert-feed','water-quality','nearshore-wave-validation']
    };
  }
  root.CGAdvisory = Object.freeze({evaluate, POLICY});
})(typeof window === 'undefined' ? globalThis : window);
