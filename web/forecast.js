/* Forecast values are regional model output, never a beach danger classifier. */
(function (root) {
  'use strict';
  const finite = value => typeof value === 'number' && Number.isFinite(value);
  function current(value, now = Date.now() / 1000) {
    return value && finite(value.time) && value.time <= now + 3600 && now - value.time <= 10800 ? value : null;
  }
  function rows(marine, wind, now = Date.now() / 1000, step = 3, count = 8) {
    const start = Math.ceil(now / 3600) * 3600;
    const marineTimes = marine?.time || [], windTimes = wind?.time || [];
    const value = (data, key, index) => index >= 0 && finite(data?.[key]?.[index]) ? data[key][index] : null;
    return Array.from({length: count}, (_, n) => {
      const time = start + n * step * 3600;
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
  const clock=value=>new Date(value*1000).toLocaleTimeString('en-GB',{timeZone:'America/Costa_Rica',hour:'2-digit',minute:'2-digit',hourCycle:'h23'});
  const day=(value,lang='es')=>new Date(value*1000).toLocaleDateString(lang==='es'?'es-CR':'en-GB',{timeZone:'America/Costa_Rica',weekday:'short',day:'numeric',month:'short'});
  const hourlyRows=(marine,wind,now=Date.now()/1000)=>rows(marine,wind,now,1,24);
  // A zero-based plot. Missing hours split paths; never imply a measured bridge.
  function trend(rows,key){
    const valid=r=>finite(r.time)&&finite(r[key])&&r[key]>=0;
    const values=rows.filter(valid).map(r=>r[key]);
    if(!values.length)return null;
    const min=Math.min(...values),max=Math.max(...values);
    const raw=Math.max(max,key==='swell'?.2:1)/3;
    const power=10**Math.floor(Math.log10(raw));
    const step=[1,2,5,10].find(n=>n*power>=raw)*power;
    const ceiling=Math.max(2*step,Math.ceil(max/step)*step);
    const times=rows.map(r=>r.time).filter(finite),start=Math.min(...times),end=Math.max(...times);
    const segments=[];let segment=[];
    rows.forEach((r,i)=>{
      if(!valid(r)){if(segment.length)segments.push(segment);segment=[];return;}
      if(segment.length&&r.time-rows[i-1].time!==3600){segments.push(segment);segment=[];}
      segment.push({time:r.time,value:r[key],x:end===start?.5:(r.time-start)/(end-start),y:1-r[key]/ceiling});
    });
    if(segment.length)segments.push(segment);
    return {min,max,ceiling,start,end,segments,missing:rows.length-values.length};
  }
  root.CGForecast = {current, rows, hourlyRows, freshHourly, format, time, clock, day, trend};
})(typeof window === 'undefined' ? globalThis : window);
