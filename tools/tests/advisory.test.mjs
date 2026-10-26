import test from 'node:test';
import assert from 'node:assert/strict';
await import('../../web/advisory.js');
const {evaluate, POLICY}=globalThis.CGAdvisory;
const now=1800000000;
const input=()=>({now,beachClass:'lower-risk',marineFetchedAt:now,weatherFetchedAt:now,
  marine:{time:now,wave_height:.5,wave_period:6,swell_wave_height:.3,swell_wave_period:8},
  weather:{time:now,wind_speed_10m:5,wind_gusts_10m:8,weather_code:0},
  weatherHourly:{time:[now,now+3600,now+7200,now+10800],weather_code:[0,0,0,0]}});

test('calm and extreme model conditions never grant swimming clearance or invent wave thresholds',()=>{
  for (const height of [0,.3,1,2,5,10]) for (const beachClass of ['lower-risk','conditional','high-risk','no-swim',null]) {
    const data=input();data.beachClass=beachClass;data.marine.wave_height=height;
    const result=evaluate(data);
    assert.equal(result.clearance,false);
    assert.ok(result.reasons.includes('wave-wind-policy-unvalidated'));
    assert.ok(result.missing.includes('local-rip-observations'));
    assert.notEqual(result.decision,'safe');
  }
});
test('standing restrictions survive calm forecasts, outages and model expiry',()=>{
  for (const data of [input(),{now}]) {
    assert.equal(evaluate({...data,beachClass:'no-swim'}).decision,'avoid-water');
    assert.equal(evaluate({...data,beachClass:'high-risk'}).decision,'lifeguard-required');
  }
  assert.equal(evaluate({...input(),now:now+POLICY.maxFetchAge+1,beachClass:'no-swim'}).decision,'avoid-water');
});
test('every supported thunderstorm code escalates even an unassessed beach',()=>{
  for (const code of [95,96,97,99]) {
    const data=input();data.beachClass=null;data.weatherHourly.weather_code[2]=code;
    const result=evaluate(data);
    assert.equal(result.decision,'avoid-water');
    assert.equal(result.stormAt,now+7200);
    assert.equal(result.thunderstorm,true);
  }
});
test('current model storms remain independent of missing hourly or marine data',()=>{
  const data=input();data.weather.weather_code=95;data.weatherHourly=null;data.marine=null;
  const result=evaluate(data);
  assert.equal(result.decision,'avoid-water');assert.equal(result.coverage,'incomplete');
});
test('time alignment uses all hourly points, rejects stale/future fetches and ignores far-future storms',()=>{
  const data=input();data.weatherHourly={time:[now+7200,now,now+3600,now+10800,now+14400],weather_code:[0,0,0,0,95]};
  assert.equal(evaluate(data).thunderstorm,false);
  data.weatherHourly.weather_code[2]=95;
  assert.equal(evaluate(data).stormAt,now+3600);
  for(const fetchedAt of [0,now+1,now-10801,'1800000000',NaN]) {
    const result=evaluate({...data,weatherFetchedAt:fetchedAt});
    assert.equal(result.thunderstorm,false);assert.equal(result.coverage,'incomplete');
  }
});
test('missing, malformed and duplicate values never become complete or clear',()=>{
  for(const invalid of [null,undefined,-1,'0',NaN,Infinity]) {
    const data=input();data.marine.wave_height=invalid;
    assert.equal(evaluate(data).coverage,'incomplete');
  }
  const data=input();data.weatherHourly.weather_code[1]=null;
  assert.equal(evaluate(data).coverage,'incomplete');
  data.weatherHourly.time.push(now+3600);data.weatherHourly.weather_code.push(95);
  const result=evaluate(data);
  assert.equal(result.coverage,'incomplete');assert.equal(result.thunderstorm,true);
});
test('freshness boundaries and the passing hour are explicit',()=>{
  const data=input();assert.equal(evaluate(data).coverage,'available');
  assert.equal(evaluate({...data,now:now+3601}).coverage,'incomplete');
  data.weather.time=now+1;data.weather.weather_code=95;
  assert.equal(evaluate(data).thunderstorm,false);
  assert.throws(()=>evaluate({now:NaN}),TypeError);
});
test('a cleared forecast never reports reopening or verified local conditions',()=>{
  const data=input();data.weather.weather_code=95;
  assert.equal(evaluate(data).decision,'avoid-water');
  data.weather.weather_code=0;
  const result=evaluate(data);
  assert.equal(result.decision,'check-locally');assert.equal(result.clearance,false);
  assert.ok(result.reasons.includes('local-observation-missing'));
});
