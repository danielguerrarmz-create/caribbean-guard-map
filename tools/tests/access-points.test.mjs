import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
const read = path => readFileSync(new URL('../../'+path, import.meta.url),'utf8');
const registry = JSON.parse(read('web/data/access-points.json'));
const roads = JSON.parse(read('web/data/osm-roads.geojson'));
const map = read('web/index.html');
const start = map.indexOf('const ZONES = [');
const end = map.indexOf('/* Rescue stations:',start);
const beachIds = runInNewContext(map.slice(start,end)+'; [...ZONES,...UNASSESSED_BEACHES].map(b=>b.id)');

test('QR access records preserve OSM source paths and only reference known beaches',()=>{
  const ids = new Set();
  for(const access of registry.entries){
    assert.match(access.id,/^osm-\d+$/);
    assert.ok(!ids.has(access.id),'duplicate QR ID');ids.add(access.id);
    const osmId = Number(access.id.slice(4));
    const source = roads.features.find(f=>f.properties.osm_way_id===osmId);
    assert.ok(source,`missing source for ${access.id}`);
    assert.deepEqual(access.path,source.geometry.coordinates,'must not invent path geometry');
    assert.ok(access.path.some(point=>JSON.stringify(point)===JSON.stringify(access.point)),'access point must be on its mapped path');
    assert.ok(access.path.every(point=>point.length===2&&point.every(Number.isFinite)));
    assert.ok(beachIds.includes(access.beach),'orphan beach reference');
    assert.ok(!['private','no'].includes(source.properties.access),'restricted source path');
    assert.equal(access.verified,false,'draft locations must stay unverified');
    assert.equal(access.source,`https://www.openstreetmap.org/way/${osmId}`);
  }
});

test('the demonstration QR retains its fixed access point and beach association',()=>{
  const demo = registry.entries.find(entry=>entry.id==='osm-458862734');
  assert.deepEqual(demo.point,[-82.7091869,9.6373785]);
  assert.equal(demo.beach,'cg:zone/chiquita');
});
