import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source=fs.readFileSync(new URL('../../web/index.html',import.meta.url),'utf8').replace(/\r\n/g,'\n');
function fn(name){const start=source.indexOf('function '+name+'(');return source.slice(start,source.indexOf('\n}\n',start)+3);}

test('loading values preserve valid zero readings and stop claiming a request after failure',()=>{
 const ctx={lang:'en'};vm.runInNewContext(fn('loadingValue'),ctx);
 assert.equal(ctx.loadingValue('0',true),'0');assert.equal(ctx.loadingValue('-',false),'-');
 assert.match(ctx.loadingValue('-',true),/role="status"/);
 ctx.lang='es';assert.match(ctx.loadingValue('-',true),/Cargando/);
});

test('a pending location search cannot be duplicated and failure releases its busy state',()=>{
 let calls=0,fail;const messages=[];
 const ctx={locateBusy:false,lang:'en',T:{en:{locating:'Finding location',denied:'Unavailable'}},say:text=>messages.push(text),
  setLocateBusy:busy=>ctx.locateBusy=busy,navigator:{geolocation:{getCurrentPosition(ok,error){calls++;fail=error;}}}};
 vm.runInNewContext(fn('doLocate')+';doLocate();doLocate();',ctx);
 assert.equal(calls,1);assert.equal(ctx.locateBusy,true);fail();assert.equal(ctx.locateBusy,false);
 assert.deepEqual(messages,['Finding location','Unavailable']);
 vm.runInNewContext('doLocate();',ctx);assert.equal(calls,2);
});

for(const valid of [false,true])test(`cached reference image resolves to ${valid?'content':'an error'} instead of loading forever`,()=>{
 const classes=new Set(['is-loading']),attrs=new Map([['aria-busy','true']]),status={};let fades=0;
 const media={isConnected:true,classList:{remove:k=>classes.delete(k),toggle(k,v){v?classes.add(k):classes.delete(k);}},removeAttribute:k=>attrs.delete(k),querySelector:()=>status};
 const img={complete:true,naturalWidth:valid?1212:0,closest:()=>media,addEventListener(){},animate(){fades++;}};
 vm.runInNewContext(fn('prepareReferenceImages')+';prepareReferenceImages();',{sheetBody:{querySelectorAll:()=>[img]},lang:'en',reducedMotion:{matches:false}});
 assert.equal(classes.has('is-loading'),false);assert.equal(classes.has('is-error'),!valid);
 assert.equal(attrs.has('aria-busy'),false);assert.equal(status.hidden,valid);assert.equal(fades,valid?1:0);
});

test('a detached image and reduced-motion image do not animate',()=>{
 for(const connected of [false,true]){
  const media={isConnected:connected,classList:{remove(){},toggle(){}},removeAttribute(){},querySelector:()=>({})};
  const img={complete:true,naturalWidth:100,closest:()=>media,addEventListener(){},animate(){assert.fail('unexpected animation');}};
  vm.runInNewContext(fn('prepareReferenceImages')+';prepareReferenceImages();',{sheetBody:{querySelectorAll:()=>[img]},lang:'en',reducedMotion:{matches:true}});
 }
});
