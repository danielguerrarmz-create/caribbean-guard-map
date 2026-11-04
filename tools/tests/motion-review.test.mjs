import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source=fs.readFileSync(new URL('../../web/index.html',import.meta.url),'utf8').replace(/\r\n/g,'\n');
function fn(name){const start=source.indexOf('function '+name+'(');return source.slice(start,source.indexOf('\n}\n',start)+3);}

test('reversing a route begins at its presented position, not the end of the previous journey',()=>{
 const calls=[],old=[{cancel(){calls.push('cancel');}}];
 const element=(translate,opacity='1')=>({style:{},presented:{translate,opacity},animate(frames){const animation={frames,cancel(){}};calls.push(animation);return animation;}});
 const sheet=element('41% 0'),dockEl=element('-10% 0','.8');
 const ctx={sheet,dockEl,desktop:()=>false,routeAnimations:old,reducedMotion:{matches:false},getComputedStyle:el=>{assert.equal(calls.length,0);return el.presented;}};
 vm.runInNewContext(fn('animatePanelRoute')+';animatePanelRoute(true);',ctx);
 assert.equal(calls[1].frames.translate[0],'41% 0');
 assert.equal(calls[2].frames.translate[0],'-10% 0');
 assert.equal(calls[2].frames.opacity[0],'.8');
});

test('reduced motion finishes a route without starting an animation',()=>{
 let done=0;const el={style:{translate:'10px',opacity:'.8'},animate(){assert.fail('animation under reduced motion');}};
 const ctx={sheet:el,dockEl:el,desktop:()=>false,routeAnimations:[],reducedMotion:{matches:true},done:()=>done++};
 vm.runInNewContext(fn('animatePanelRoute')+';animatePanelRoute(false,done);',ctx);
 assert.equal(done,1);assert.equal(el.style.translate,'');
});

for(const back of [false,true])for(const reduced of [false,true])test(`desktop route keeps the sidebar stationary (back ${back}, reduced motion ${reduced})`,()=>{
 let done=0;const calls=[];
 const element=name=>({style:{},animate(frames,timing){const a={cancel(){}};calls.push({name,frames,timing,a});return a;}});
 const sheet=element('sheet'),sheetBody=element('content'),dockEl=element('overview');
 const ctx={sheet,sheetBody,dockEl,document:{getElementById:()=>element('overview')},desktop:()=>true,routeAnimations:[],reducedMotion:{matches:reduced},done:()=>done++};
 vm.runInNewContext(fn('animatePanelRoute')+`;animatePanelRoute(${back},done);`,ctx);
 assert.equal(calls.length,reduced?0:1);
 if(!reduced){
  assert.equal(calls[0].name,back?'overview':'content');
  assert.deepEqual(Object.keys(calls[0].frames),['opacity'],'desktop must never sweep across the map');
  assert.ok(calls[0].timing.duration<=180);
  if(back)assert.equal(done,1,'reveal overview before fading its content');
  calls[0].a.onfinish();
 }
 assert.equal(done,1,'completion runs exactly once');
});

for(const wide of [false,true])for(const reduced of [false,true])test(`forecast metric preserves hour and focus (desktop ${wide}, reduced motion ${reduced})`,()=>{
 let focused='',animations=0;
 const tracks={swell:{scrollLeft:460},wind:{scrollLeft:0},gust:{scrollLeft:0}};
 const buttons=Object.keys(tracks).map(key=>({dataset:{forecastMetric:key},setAttribute(name,value){this[name]=value;},focus(){focused=key;}}));
 const views=Object.keys(tracks).map(key=>({id:'hourly-'+key,hidden:key!=='swell',querySelector:()=>tracks[key],animate(frames){animations++;if(wide)assert.equal(frames.transform,undefined,'desktop charts should not bounce vertically');}}));
 const panel={dataset:{metric:'swell'},querySelector:()=>tracks.swell,querySelectorAll:selector=>selector==='[data-forecast-metric]'?buttons:views};
 const ctx={panel,desktop:()=>wide,reducedMotion:{matches:reduced},scheduleScrollCues(){}};
 vm.runInNewContext(fn('selectForecastMetric')+`;selectForecastMetric(panel,'wind',true);`,ctx);
 assert.equal(tracks.wind.scrollLeft,460);assert.equal(focused,'wind');
 assert.equal(views.filter(v=>!v.hidden).length,1);assert.equal(animations,reduced?0:1);
 vm.runInNewContext(`selectForecastMetric(panel,'wind',true);`,ctx);
 assert.equal(animations,reduced?0:1,'reselecting the same metric must not replay motion');
});

test('a duplicate forecast refresh makes no requests while loading',async()=>{
 const ctx={forecastBusy:true,fetch(){assert.fail('duplicate request');}};
 const start=source.indexOf('async function refreshForecast(');
 await vm.runInNewContext(source.slice(start,source.indexOf('\n}\n',start)+3)+';refreshForecast();',ctx);
});

test('a failed refresh preserves available readings and exits its loading state',async()=>{
 const previous={swell_wave_height:.9},updates=[];
 const ctx={forecastBusy:false,forecastFailed:false,seaData:previous,seaHourly:{time:[1]},weatherData:null,windHourly:null,
  SEA_URL:'marine',WEATHER_URL:'wind',Date,AbortSignal,
  fetch:async()=>{throw new Error('offline');},renderSea:()=>updates.push('summary'),refreshForecastPanel:()=>updates.push('panel'),refreshWeatherPanel(){},measureDock(){}};
 const start=source.indexOf('async function refreshForecast(');
 await vm.runInNewContext(source.slice(start,source.indexOf('\n}\n',start)+3)+';refreshForecast();',ctx);
 assert.equal(ctx.forecastBusy,false);assert.equal(ctx.forecastFailed,true);assert.equal(ctx.seaData,previous);
 assert.deepEqual(updates,['summary','panel','summary','panel']);
});
