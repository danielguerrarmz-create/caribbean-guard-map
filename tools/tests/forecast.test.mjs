import test from 'node:test';
import assert from 'node:assert/strict';
await import('../../web/forecast.js');
const forecast = globalThis.CGForecast;

test('trend keeps a zero baseline and actual time spacing without exaggerating a narrow range',()=>{
  const result=forecast.trend([{time:3600,swell:.8},{time:7200,swell:.9},{time:10800,swell:.8}],'swell');
  assert.equal(result.min,.8);assert.equal(result.max,.9);
  assert.ok(result.ceiling>=.9);
  assert.deepEqual(result.segments[0].map(p=>p.x),[0,.5,1]);
  for(const point of result.segments[0])assert.equal(point.y,1-point.value/result.ceiling);
});

test('trend breaks at missing readings and skipped hours instead of drawing a continuous forecast',()=>{
  const result=forecast.trend([{time:3600,wind:0},{time:7200,wind:null},{time:10800,wind:8},{time:18000,wind:10}],'wind');
  assert.equal(result.min,0);assert.equal(result.missing,1);
  assert.deepEqual(result.segments.map(s=>s.length),[1,1,1]);
  assert.equal(result.segments[0][0].y,1);
  assert.equal(result.segments.at(-1)[0].x,1);
});

test('trend handles empty, zero, single and invalid data without inventing values',()=>{
  assert.equal(forecast.trend([],'gust'),null);
  assert.equal(forecast.trend([{time:3600,gust:NaN},{time:7200,gust:-2}],'gust'),null);
  const zero=forecast.trend([{time:3600,gust:0}],'gust');
  assert.equal(zero.min,0);assert.equal(zero.max,0);
  assert.ok(zero.ceiling>0);
  assert.deepEqual(zero.segments[0][0],{time:3600,value:0,x:.5,y:1});
});
test('stale, future and malformed current values are not displayed as current', () => {
  assert.equal(forecast.current({time:1}, 20000), null);
  assert.equal(forecast.current({time:30000}, 20000), null);
  assert.equal(forecast.current({time:'20000'}, 20000), null);
  assert.equal(forecast.current({time:20000}, 20000).time, 20000);
});
test('forecast aligns by timestamps, preserves zero and leaves missing data empty', () => {
  const marine = {time:[3600,14400], swell_wave_height:[0,1.2]};
  const wind = {time:[14400,3600], wind_speed_10m:[12,0]};
  const rows = forecast.rows(marine, wind, 1);
  assert.equal(rows.length, 8);
  assert.deepEqual([rows[0].swell,rows[0].wind,rows[1].swell,rows[1].wind], [0,0,1.2,12]);
  assert.equal(rows[2].swell,null);
  assert.equal(forecast.format(null,' m'), '-');
  assert.equal(forecast.format(0,' m',1), '0.0 m');
});
test('missing or expired series do not reuse an old forecast', () => {
  assert.ok(forecast.rows({time:[0],swell_wave_height:[1]}, null, 90000).every(row => row.swell === null));
});

test('an old fetch expires even when its series still contains future hours', () => {
  const series = {time:[25000],swell_wave_height:[2]};
  assert.equal(forecast.freshHourly(series, 1000, 20000), null);
  assert.equal(forecast.freshHourly(series, 20001, 20000), null);
  assert.equal(forecast.freshHourly(series, 0, 20000), null);
  assert.equal(forecast.freshHourly(series, 19900, 20000), series);
});

 test('hourly date groups and clocks use Costa Rica across UTC midnight',()=>{
 const before=Date.parse('2026-11-04T05:00:00Z')/1000,after=before+3600;
 assert.equal(forecast.clock(before),'23:00');assert.equal(forecast.clock(after),'00:00');
 assert.notEqual(forecast.day(before,'en'),forecast.day(after,'en'));
});

test('hourly view covers 24 consecutive hours without inventing missing data',()=>{
 const times=Array.from({length:24},(_,i)=>(i+1)*3600);
 const marine={time:times,swell_wave_height:times.map((_,i)=>i/10)};
 const rows=forecast.hourlyRows(marine,null,1);
 assert.equal(rows.length,24);assert.equal(rows[23].time-rows[0].time,23*3600);
 assert.equal(rows[0].swell,0);assert.equal(rows[23].swell,2.3);
 assert.ok(rows.every(r=>r.wind===null));
});
