import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
const html=readFileSync(new URL('../../web/index.html',import.meta.url),'utf8');
const sw=readFileSync(new URL('../../web/sw.js',import.meta.url),'utf8');
const assets=runInNewContext(sw.slice(0,sw.indexOf('async function put('))+'\nCRITICAL',{});
test('a new document cannot boot with unversioned application assets from an older offline cache',()=>{
 const urls=[...html.matchAll(/(?:src|href)="([^"/]+\.(?:js|css)(?:\?[^"]*)?)"/g)].map(m=>m[1]);
 assert.ok(urls.length>=8);
 const version=sw.match(/const CACHE = "cg-map-v(\d+)/)[1];
 for(const url of urls){
  assert.equal(new URL(url,'https://map.test/').searchParams.get('v'),version,url);
  assert.ok(assets.includes(url),'precache must use the exact request key: '+url);
 }
});
