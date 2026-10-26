import test from 'node:test';
import assert from 'node:assert/strict';
await import('../../web/forecast.js');
const forecast = globalThis.CGForecast;
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
