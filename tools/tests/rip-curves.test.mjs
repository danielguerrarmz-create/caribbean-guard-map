import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

const context={L:{point:(x,y)=>({x,y})}};
runInNewContext(readFileSync(new URL('../../web/geometry.js',import.meta.url),'utf8'),context);
const {simplifyCurve,ripShape}=context.CGGeom;
const rips=JSON.parse(readFileSync(new URL('../../web/data/full-map-geographic.geojson',import.meta.url),'utf8')).features.filter(f=>f.properties.kind==='rip_current');
const distance=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
function projection(scale){return {
  latLngToLayerPoint:([lat,lng])=>({x:lng*scale,y:-lat*scale}),
  layerPointToLatLng:p=>p
};}

test('all source rips match the current app baseline without changing evidence',()=>{
  // Labelled baseline of app behaviour captured 2026-11-04, not approved symbol-study curves.
  const baseline=JSON.parse(readFileSync(new URL('./fixtures/rip-curves.app-baseline-2026-11-04.json',import.meta.url),'utf8'));
  const keyFor=(feature,index)=>feature.id!=null?`feature.id:${JSON.stringify(feature.id)}`:
    feature.properties.id!=null?`properties.id:${JSON.stringify(feature.properties.id)}`:`index:${index}`;
  const source=JSON.parse(readFileSync(new URL('../../web/data/full-map-geographic.geojson',import.meta.url),'utf8'));
  const keys=source.features.flatMap((feature,index)=>feature.properties.kind==='rip_current'?[keyFor(feature,index)]:[]);
  const original=JSON.stringify(rips);
  assert.equal(rips.length,53);
  assert.equal(baseline.featureCount,53);
  assert.equal(new Set(keys).size,53,'source feature keys must be unique');
  assert.deepEqual(Object.keys(baseline.entries).sort(),[...keys].sort(),'baseline keys must match exactly');
  for(const [index,feature] of rips.entries()){
    const points=feature.geometry.coordinates;
    const actual=simplifyCurve(points);
    assert.deepEqual(JSON.parse(JSON.stringify(actual)),baseline.entries[keys[index]],keys[index]);
    assert.ok(Object.values(actual).flat().every(Number.isFinite));
    assert.ok(Object.values(baseline.entries[keys[index]]).flat().every(Number.isFinite));
  }
  assert.equal(JSON.stringify(rips),original);
});

test('heads stay 7 by 6 screen pixels and align to the terminal tangent across zooms',()=>{
  for(const scale of [12000,24000,96000])for(const feature of rips){
    const map=projection(scale),pts=feature.geometry.coordinates.map(([lng,lat])=>[lat,lng]);
    const shape=ripShape(map,pts),[left,tip,right]=shape.head;
    const base={x:(left.x+right.x)/2,y:(left.y+right.y)/2};
    assert.ok(Math.abs(distance(left,right)-6)<1e-7);
    assert.ok(Math.abs(distance(base,tip)-7)<1e-7);
    const curve=simplifyCurve(pts.map(p=>{const q=map.latLngToLayerPoint(p);return[q.x,q.y];}));
    const dx=curve.end[0]-curve.control[0],dy=curve.end[1]-curve.control[1];
    assert.ok(Math.abs((tip.x-base.x)*dy-(tip.y-base.y)*dx)<1e-5);
    assert.ok((tip.x-base.x)*dx+(tip.y-base.y)*dy>0,'head must face forward');
  }
});

test('degenerate annotations produce no stray head or invalid path',()=>{
  for(const pts of [[],[[0,0]],[[1,1],[1,1]]]){
    assert.equal(simplifyCurve(pts),null);
    const shape=ripShape(projection(1),pts);
    assert.equal(shape.shaft.length,0);
    assert.equal(shape.head.length,0);
  }
});

test('each rip renders one moving dashed shaft and an open red head through zoom changes',()=>{
  const layer=(points,options)=>({points,options,
    addTo(group){group.layers.push(this);return this;},setLatLngs(next){this.points=next;return this;}});
  const renderer={L:{point:(x,y)=>({x,y}),layerGroup:()=>({layers:[]}),polyline:layer}};
  runInNewContext(readFileSync(new URL('../../web/geometry.js',import.meta.url),'utf8'),renderer);
  for(const feature of rips){
    const map={...projection(24000),getPane:()=>({style:{}})};
    const pts=feature.geometry.coordinates.map(([lng,lat])=>[lat,lng]);
    const group=renderer.CGGeom.curveArrow(map,pts);
    assert.equal(group.layers.length,2,'no continuous underlay or second moving stroke');
    const [shaft,head]=group.layers;
    assert.equal(shaft.options.dashArray,'8 6');
    assert.equal(shaft.options.opacity,1);
    assert.equal(head.options.color,shaft.options.color);
    assert.equal(head.options.fill,false);
    assert.equal(head.points.length,3,'head contains only two sides');
    assert.equal(shaft.options.interactive,false);
    const before=JSON.stringify(shaft.points);
    group.cgRedraw({...map,...projection(96000)},pts);
    assert.notEqual(JSON.stringify(shaft.points),before);
    assert.equal(head.points.length,3);
  }
});
