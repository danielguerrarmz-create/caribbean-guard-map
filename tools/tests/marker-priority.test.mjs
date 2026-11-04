import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

const context={};
runInNewContext(readFileSync(new URL('../../web/geometry.js',import.meta.url),'utf8'),context);
const layout=entries=>Array.from(context.CGGeom.declutterMarkers(entries));
const rescue={id:'rescue',x:100,y:100,size:44,priority:100,required:true};
const access={id:'access',x:120,y:110,size:44,priority:50};
const groups=entries=>context.CGGeom.groupMarkers(entries);

test('colliding stations group at an existing anchor without modifying coordinates',()=>{
  const entries=[rescue,{...rescue,id:'second',x:130},{...rescue,id:'third',x:220}];
  const before=JSON.stringify(entries),result=groups(entries);
  assert.equal(result.length,2);
  assert.equal(result[0].anchor,entries[0]);
  assert.deepEqual(Array.from(result[0].members,m=>m.id),['rescue','second']);
  assert.equal(JSON.stringify(entries),before);
});

test('zoom separates every station and no chain pulls distant stations into a group',()=>{
  assert.equal(groups([rescue,{...rescue,x:160},{...rescue,x:220}]).length,3);
  const result=groups([rescue,{...rescue,x:150},{...rescue,x:200}]);
  assert.equal(result.length,2);
  assert.equal(result[0].members.length,2);
  assert.equal(groups([]).length,0);
});

test('rescue wins over nearby access without changing either geographic anchor',()=>{
  const entries=[access,rescue],before=JSON.stringify(entries);
  assert.deepEqual(layout(entries),['rescue']);
  assert.equal(JSON.stringify(entries),before);
});
test('access returns when zoom separates it or its blocking layer is removed',()=>{
  assert.deepEqual(layout([rescue,{...access,x:160}]),['rescue','access']);
  assert.deepEqual(layout([access]),['access']);
});
test('access beats a place, access pairs thin consistently, all rescue markers remain',()=>{
  const other={...rescue,id:'rescue2',x:102};
  const a={...access,x:200,y:200};
  const b={...a,id:'access2',x:210};
  const place={...a,id:'place',priority:10};
  assert.deepEqual(layout([place,a,b,other,rescue]),['rescue2','rescue','access']);
});
test('touch areas retain six pixels of separation at the exact boundary',()=>{
  assert.deepEqual(layout([rescue,{...access,x:149,y:100}]),['rescue']);
  assert.deepEqual(layout([rescue,{...access,x:150,y:100}]),['rescue','access']);
});
