import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source=fs.readFileSync(new URL('../../web/index.html',import.meta.url),'utf8').replace(/\r\n/g,'\n');
function fn(name){const start=source.indexOf('function '+name+'(');return source.slice(start,source.indexOf('\n}\n',start)+3);}
const classes=()=>({contains:()=>false,add(){},remove(){},toggle(){}});

test('the rescue layer owns original stations as well as imported equipment',()=>{
 const stations=[{id:'est1'},{id:'est3'},{id:'est4'}];
 const groups=[];
 const ctx={sourceLayerDefs:[['rescue'],['hazards']],map:{},postMarkers:Object.fromEntries(stations.map(s=>[s.id,s])),
  L:{layerGroup:()=>{const members=new Set();const group={addTo(){return this;},addLayer(marker){members.add(marker);},members};groups.push(group);return group;}}};
 const start=source.indexOf('const sourceLayers =');
 vm.runInNewContext(source.slice(start,source.indexOf('const ripReferenceMarkers',start)),ctx);
 assert.deepEqual([...groups[0].members],stations);
});

test('fallback rip arrows obey the same hazard switch when projected data is unavailable',()=>{
 const parents=[],hazards={id:'hazards'};
 const ctx={map:{on(){}},sourceLayers:{hazards},ANNOT:{rips:[]},L:{layerGroup:()=>({addTo(parent){parents.push(parent);return this;}})}};
 vm.runInNewContext(fn('drawAnnotations')+';drawAnnotations({features:[]});',ctx);
 assert.equal(parents[1],hazards);
});

test('reference-image pins yield to rescue and return when zoom separates them',()=>{
 const node=(kind,x)=>{const names=new Set([kind]),attributes=new Map();return {x,
  classList:{contains:key=>names.has(key),remove:key=>names.delete(key),toggle(key,on){on?names.add(key):names.delete(key);}},
  getBoundingClientRect(){return {x:this.x,y:100,width:44,height:44};},querySelector:()=>null,
  setAttribute:(key,value)=>attributes.set(key,value),getAttribute:key=>attributes.get(key)??null,removeAttribute:key=>attributes.delete(key)};};
 const rescue=node('projected-rescue',100),reference=node('rip-reference-marker',110);
 const ctx={markerLayoutFrame:0,requestAnimationFrame:callback=>{callback();return 0;},map:{eachLayer(){}},L:{Marker:class{}},
  document:{querySelectorAll:()=>[rescue,reference]},lang:'en',placeBeachLabels(){}};
 vm.runInNewContext(fs.readFileSync(new URL('../../web/geometry.js',import.meta.url),'utf8')+'\n'+fn('scheduleMarkerLayout')+';scheduleMarkerLayout();',ctx);
 assert.equal(reference.getAttribute('aria-hidden'),'true');assert.equal(reference.x,110);
 reference.x=220;
 vm.runInNewContext('scheduleMarkerLayout();',ctx);
 assert.equal(reference.getAttribute('aria-hidden'),null);assert.equal(reference.x,220);
});
test('the visible Legend launcher opens the shared sheet rather than a capped separate tray',()=>{
 const toggle={},el={classList:classes(),setAttribute(){},querySelector:()=>toggle,querySelectorAll:()=>[],contains:()=>false};
 const dock={setAttribute(){},removeAttribute(){}};
 const calls=[];
 const ctx={document:{activeElement:null,body:{classList:classes()},getElementById:id=>id==='legend-perm'?el:id==='dock'?dock:{classList:classes()}},
  lang:'en',legendExpanded:false,legendClosingTimer:null,legendParked:false,clearTimeout(){},desktop:()=>true,
  LEGEND_SECTIONS:[],sourceLayerDefs:[],sourceLayerState:{},CGSymbols:{svg:()=>''},
  navigateFromOverview:open=>{calls.push('route');open();},openLegend:()=>calls.push('legend')};
 vm.runInNewContext(fn('renderLegendPerm')+';renderLegendPerm();',ctx);
 toggle.onclick();
 assert.deepEqual(calls,['route','legend']);
});
test('closing a beach sheet retains its geographic highlight for the map view',()=>{
 let clears=0;const sheet={classList:{...classes(),contains:()=>true}};
 const ctx={clearAccessPath(){},clearBand(){clears++;},sheet,sheetClosing:false,lastFocus:null,
 document:{contains:()=>false,querySelector:()=>null,body:{classList:classes()}},
 lastRender:null,sheetTimer:null,clearTimeout(){},panelRoute:null,desktop:()=>false,
 dockEl:{removeAttribute(){}},placeControls(){},sheetPanel:{visible:()=>400,animateTo(){}},
 setDockStop(){},dockPanel:{animateTo(){}},markCurrent(){}};
 vm.runInNewContext(fn('closeSheet')+';closeSheet({fromHistory:true});',ctx);
 assert.equal(clears,0);
});

test('assessed and unassessed map labels use the same connected route as the beach list',()=>{
 const calls=[],labels=[{},{}],beaches=[{id:'known',character:{}},{id:'unknown'}];
 const ctx={zoneLabels:[labels[0]],unassessedLabels:[labels[1]],ZONES:[beaches[0]],UNASSESSED_BEACHES:[beaches[1]],
  tappableLabel:(label,callback)=>label.open=callback,
  navigateFromOverview:open=>{calls.push('route');open();},
  openZone:z=>calls.push(z.id),openUnassessedBeach:z=>calls.push(z.id)};
 const entry=source.includes('function openBeach(')?fn('openBeach'):source.match(/const openBeach=.*;/)[0];
 const wiring=source.split('\n').filter(line=>/^(zoneLabels|unassessedLabels)\.forEach.*tappableLabel/.test(line)).join('\n');
 vm.runInNewContext(entry+'\n'+wiring,ctx);
 labels.forEach(label=>label.open());
 assert.deepEqual(calls,['route','known','route','unknown']);
});
