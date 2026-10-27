import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

function renderer(){
  const L={layerGroup:()=>({layers:[]}),polyline:(points,options)=>({
    points,options:{...options},addTo(group){group.layers.push(this);return this;},
    setStyle(style){Object.assign(this.options,style);}
  })};
  const context={L};
  runInNewContext(readFileSync(new URL('../../web/geometry.js',import.meta.url),'utf8'),context);
  const panes={};
  const map={getPane:name=>panes[name],createPane:name=>(panes[name]={style:{}})};
  return {geometry:context.CGGeom,map,panes};
}

test('a shoreline stays one continuous source path when its zoom style changes',()=>{
  const {geometry,map,panes}=renderer();
  const points=[[9.65,-82.76],[9.651,-82.755],[9.652,-82.75]];
  const original=JSON.stringify(points);
  const group=geometry.taperedPolyline(points,{color:'#258051',weight:3},map);
  const ink=group.layers.filter(layer=>layer.options.pane==='cgCoastInk');
  assert.equal(ink.length,1,'segmented strokes create seams and restart patterns');
  assert.equal(ink[0].points,points,'all source vertices and shared endpoints are retained');
  for(const zoom of [12,14,16,18])group.cgSetStyle(geometry.zoneStroke('low',zoom));
  assert.equal(JSON.stringify(points),original,'rendering must not modify source geography');
  assert.ok(Number(panes.cgCoastCasing.style.zIndex)<Number(panes.cgCoastInk.style.zIndex));
  assert.equal(ink[0].options.lineCap,'butt','shared zone ends must not overpaint their neighbor');
});

test('shoreline styling remains finite and restrained across all supported zoom levels',()=>{
  const {geometry}=renderer();
  for(const tier of ['low','moderate','high'])for(let zoom=10;zoom<=18;zoom+=.25){
    const style=geometry.zoneStroke(tier,zoom);
    assert.ok(style.weight>=2&&style.weight<=3.6);
    assert.equal(style.dashArray,null,'continuous colored coast should not become a white dotted rail');
  }
});
