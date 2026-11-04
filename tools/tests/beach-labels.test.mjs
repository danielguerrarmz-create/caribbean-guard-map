import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
const context={};
runInNewContext(readFileSync(new URL('../../web/geometry.js',import.meta.url),'utf8'),context);
const layout=context.CGGeom.layoutBeachLabels;
const bounds={left:12,right:378,top:90,bottom:470};
const overlaps=(a,b)=>a.left<b.right+5&&a.right>b.left-5&&a.top<b.bottom+5&&a.bottom>b.top-5;
test('crowded beach names yield instead of covering rescue icons or moving far away',()=>{
  const labels=Array.from({length:7},(_,id)=>({id,left:150+id*12,top:220+id*3,width:110,height:44}));
  const icons=[{left:120,right:164,top:210,bottom:254},{left:240,right:284,top:230,bottom:274}];
  const before=JSON.stringify(labels),placed=layout(labels,icons,bounds);
  assert.ok(placed.length>0&&placed.length<7);
  placed.forEach((box,i)=>{
    assert.ok(box.left>=bounds.left&&box.right<=bounds.right&&box.top>=bounds.top&&box.bottom<=bounds.bottom);
    assert.ok(!icons.some(icon=>overlaps(box,icon)));
    assert.ok(!placed.slice(0,i).some(other=>overlaps(box,other)));
  });
  assert.equal(JSON.stringify(labels),before);
});
test('off-screen beach names are not pulled into the current frame',()=>{
  const placed=layout([{id:1,left:-200,top:300,width:120,height:44},{id:2,left:700,top:800,width:120,height:44}],[],bounds);
  assert.equal(placed.length,0);
  placed.forEach(b=>assert.ok(b.left>=12&&b.right<=378&&b.bottom<=470));
});
test('a clear label stays at its home position',()=>{
  const placed=layout([{id:1,left:80,top:130,width:120,height:44}],[],bounds);
  assert.equal(placed[0].left,80);assert.equal(placed[0].top,130);
});

test('the unreviewed beach notice is outside the collapsed sources section and absent for reviewed beaches',()=>{
  const html=readFileSync(new URL('../../web/index.html',import.meta.url),'utf8').replace(/\r\n/g,'\n');
  const start=html.indexOf('function openZone(');
  const source=html.slice(start,html.indexOf('\n}\n',start)+3);
  for(const lang of ['en','es']) for(const reviewed of [null,{by:'Guard',on:'2026-11-04'}]){
    let panel;
    const z={id:'test',at:[0,0],line:[],name:{en:'Beach',es:'Playa'},character:{class:'conditional',why:{en:'Context',es:'Contexto'},reviewed}};
    const noop=()=>{};
    runInNewContext(source+';openZone(z);',{
      z,lang,T:{[lang]:{}},clearAccessPath:noop,tierOf:()=>'',statusCardInner:()=>'',
      renderSwimAdvisory:()=>'',renderForecastPanel:()=>'',trustLine:()=>'',renderWeatherPanel:()=>'',
      reportHref:()=>'',sheetFoot:()=>'',openSheet:html=>{panel=html;},requestAnimationFrame:noop,
      fitZoneDetail:noop,markCurrent:noop,flyClear:noop,showBand:noop,sheetAddress:noop,localId:id=>id,
      L:{latLngBounds:()=>({})}
    });
    const text=lang==='en'?'Not locally reviewed. No live conditions.':'Sin revisión local. Sin condiciones en vivo.';
    const details=panel.match(/<details\b[^>]*>[\s\S]*?<\/details>/g)||[];
    assert.ok(details.length>0);
    assert.ok(details.every(section=>!section.includes(text)));
    assert.equal(panel.includes(text),!reviewed);
    if(!reviewed) assert.ok(panel.includes(`<p class="beach-meta">${text}</p>`));
  }
});
