import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {runInNewContext} from 'node:vm';

const root=new URL('../../',import.meta.url);
const read=path=>readFileSync(new URL(path,root),'utf8');
const context={window:{}};
runInNewContext(read('web/symbols.js'),context);
const symbols=context.window.CGSymbols;

test('every semantic symbol renders offline, decorative, and without active SVG content',()=>{
  assert.equal(symbols.kinds.length,38);
  for(const kind of symbols.kinds){
    const svg=symbols.svg(kind);
    assert.match(svg,/<svg[^>]+aria-hidden="true"[^>]+focusable="false"/);
    assert.match(svg,/<(?:path|circle) /);
    assert.doesNotMatch(svg,/<(?:script|image|use|foreignObject)\b|\bon\w+=|\bhref=/i);
  }
});

test('unknown symbols use a visible fallback and caller text cannot become markup',()=>{
  assert.equal(symbols.svg('__proto__'),symbols.svg('unknown'));
  assert.equal(symbols.svg('<script>'),symbols.svg('unknown'));
  assert.doesNotMatch(symbols.badge('unknown','"><script>alert(1)</script>'),/<script>/);
});

test('all rescue stations use the pinned Duotone lifebuoy with distinct proposal tone',()=>{
  for(const kind of ['rescue_station','proposed_rescue_station']){
    const paths=read('web/icons/phosphor-duotone/lifebuoy-duotone.svg').match(/<svg\b[^>]*>(.*)<\/svg>/s)[1];
    assert.ok(symbols.svg(kind).includes(paths));
    assert.match(symbols.svg(kind),/viewBox="0 0 256 256" fill="currentColor"/);
  }
  assert.match(symbols.svg('rescue_station'),/data-tone="rescue"/);
  assert.match(symbols.svg('proposed_rescue_station'),/data-tone="muted"/);
});

test('bundled source SVGs match their pinned upstream integrity records',()=>{
  for(const family of ['phosphor-duotone','phosphor-regular']){
    const manifest=JSON.parse(read(`web/icons/${family}/manifest.json`));
    for(const row of manifest.assets){
      const file=row.file.split('/').at(-1);
      const bytes=readFileSync(new URL(`web/icons/${family}/${file}`,root));
      assert.equal(createHash('sha256').update(bytes).digest('hex'),row.sha256,file);
    }
  }
});

test('forward navigation uses matching open right chevrons without diagonal or filled triangles',()=>{
  for(const kind of ['next','external']){
    const svg=symbols.svg(kind);
    assert.match(svg,/fill="none"/);
    assert.match(svg,/d="m9 5 7 7-7 7"/);
    assert.match(svg,/stroke="currentColor"/);
    assert.doesNotMatch(svg,/opacity=|[zZ]"/);
  }
});
