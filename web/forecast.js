/* Forecast values are regional model output, never a beach danger classifier. */
(function (root) {
  'use strict';
  const finite = value => typeof value === 'number' && Number.isFinite(value);
  function current(value, now = Date.now() / 1000) {
    return value && finite(value.time) && value.time <= now + 3600 && now - value.time <= 10800 ? value : null;
  }
  function rows(marine, wind, now = Date.now() / 1000) {
    const start = Math.ceil(now / 3600) * 3600;
    const marineTimes = marine?.time || [], windTimes = wind?.time || [];
    const value = (data, key, index) => index >= 0 && finite(data?.[key]?.[index]) ? data[key][index] : null;
    return Array.from({length: 8}, (_, n) => {
      const time = start + n * 3 * 3600;
      const m = marineTimes.indexOf(time), w = windTimes.indexOf(time);
      return {time, swell: value(marine, 'swell_wave_height', m), period: value(marine, 'swell_wave_period', m),
        swellFrom: value(marine, 'swell_wave_direction', m), wind: value(wind, 'wind_speed_10m', w),
        windFrom: value(wind, 'wind_direction_10m', w), gust: value(wind, 'wind_gusts_10m', w)};
    });
  }
  function freshHourly(value, fetchedAt, now = Date.now() / 1000) {
    return finite(fetchedAt) && fetchedAt > 0 && fetchedAt <= now && now - fetchedAt <= 10800 ? value : null;
  }
  function format(value, suffix, digits = 0) {
    return finite(value) ? value.toFixed(digits) + suffix : '-';
  }
  function time(value, lang = 'es') {
    return new Date(value * 1000).toLocaleString(lang === 'es' ? 'es-CR' : 'en-GB', {
      timeZone:'America/Costa_Rica', day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit', hourCycle:'h23'
    });
  }
  root.CGForecast = {current, rows, freshHourly, format, time};
})(typeof window === 'undefined' ? globalThis : window);
