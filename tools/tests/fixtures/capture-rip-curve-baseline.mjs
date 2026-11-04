import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync,writeFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

// Explicit snapshot date, not the regeneration date. Run with Node from any cwd.
// Re-running overwrites the 2026-11-04 fixture under that date; after web/geometry.js changes, copy this script with a new date and filename for a new baseline.
const root=new URL('../../../',import.meta.url);
const geometryPath='web/geometry.js';
const sourceDataPath='web/data/full-map-geographic.geojson';
const geometry=readFileSync(new URL(geometryPath,root));
const data=readFileSync(new URL(sourceDataPath,root));
const sha256=bytes=>createHash('sha256').update(bytes).digest('hex');
const context={L:{point:(x,y)=>({x,y})}};
runInNewContext(geometry.toString('utf8'),context);
const entries={};
for(const [index,feature] of JSON.parse(data).features.entries()){
  if(feature.properties.kind!=='rip_current')continue;
  const key=feature.id!=null?`feature.id:${JSON.stringify(feature.id)}`:
    feature.properties.id!=null?`properties.id:${JSON.stringify(feature.properties.id)}`:`index:${index}`;
  assert.ok(!Object.hasOwn(entries,key),`duplicate feature key: ${key}`);
  const actual=context.CGGeom.simplifyCurve(feature.geometry.coordinates);
  assert.ok(actual&&Object.values(actual).flat().every(Number.isFinite),key);
  entries[key]=JSON.parse(JSON.stringify(actual));
}
assert.equal(Object.keys(entries).length,53);
const fixture={
  description:'Baseline of current app behaviour, NOT the approved symbol-study curves; docs/design/symbol-study/curve.mjs was never committed.',
  capturedOn:'2026-11-04',
  implementation:`${geometryPath} CGGeom.simplifyCurve`,
  sourceDataPath,
  featureCount:Object.keys(entries).length,
  sha256:{[geometryPath]:sha256(geometry),[sourceDataPath]:sha256(data)},
  keyStrategy:'feature.id, else properties.id, else index in the full source FeatureCollection; IDs are JSON-encoded with a field prefix.',
  entries
};
writeFileSync(new URL('rip-curves.app-baseline-2026-11-04.json',import.meta.url),JSON.stringify(fixture,null,2)+'\n');
