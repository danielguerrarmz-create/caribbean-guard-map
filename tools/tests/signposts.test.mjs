import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
const read=path=>readFileSync(new URL('../../'+path,import.meta.url),'utf8');
const data=path=>JSON.parse(read(path));
const context={URL};runInNewContext(read('web/signposts.js'),context);
const {resolve,link}=context.CGSignposts;
const signs=data('web/data/signposts.json').entries;
const accesses=data('web/data/access-points.json').entries;
const references=data('web/data/rip-reference-images.json').features;

test('each poster resolves to its fixed point, mapped access and real reference image',()=>{
  const ids=new Set();
  for(const sign of signs){
    assert.ok(!ids.has(sign.id));ids.add(sign.id);
    const result=resolve(sign.id,signs,accesses,references);
    assert.ok(result,sign.id);
    assert.ok(['draft','verified'].includes(sign.status));
    if(sign.status==='verified')assert.ok(sign.verifiedAt);
    assert.ok(read('web/'+result.reference.image).length);
  }
});
test('the Merlin draft preserves the road junction candidate and supplied image association',()=>{
  const result=resolve('merlin-entrance',signs,accesses,references);
  assert.deepEqual(result.sign.point,[-82.7172165,9.6402744]);
  assert.ok(result.access.path.some(p=>JSON.stringify(p)===JSON.stringify(result.sign.point)));
  assert.equal(result.reference.id,'merlin');
  assert.equal(result.sign.status,'draft');assert.equal(result.sign.verifiedAt,null);
});
test('printed sign URLs retain the deployment path without leaking other URL parameters',()=>{
  const url=link('https://map.example/mapa?z=cocles&lang=en#old','merlin-entrance');
  assert.equal(url,'https://map.example/mapa?sign=merlin-entrance');
  assert.equal(link('http://127.0.0.1:5174/','merlin-entrance'),'http://127.0.0.1:5174/?sign=merlin-entrance');
  assert.throws(()=>link('javascript:alert(1)','merlin-entrance'));
  assert.throws(()=>link('https://map.example/','../other'));
});
test('unknown, orphaned and invalid poster records cannot choose arbitrary map positions',()=>{
  assert.equal(resolve('unknown',signs,accesses,references),null);
  assert.equal(resolve(signs[0].id,signs,[],references),null);
  assert.equal(resolve(signs[0].id,signs,accesses,[]),null);
  assert.equal(resolve(signs[0].id,[{...signs[0],status:'retired'}],accesses,references),null);
  for(const point of [[NaN,1],[1,91],[181,1],[1],null]){
    assert.equal(resolve(signs[0].id,[{...signs[0],point}],accesses,references),null);
  }
});
test('rescue station names omit public numbering while old station URLs remain valid',()=>{
  const html=read('web/index.html');
  const start=html.indexOf('const POSTS = [');
  const end=html.indexOf('.filter(post => !post.proposed);',start)+'.filter(post => !post.proposed);'.length;
  const posts=runInNewContext(html.slice(start,end)+'; POSTS');
  assert.equal(posts.find(post=>post.id==='cg:station/est1').name.en,'Rescue Station');
  for(const post of posts)for(const label of Object.values(post.name))assert.doesNotMatch(label,/\d/);
});
