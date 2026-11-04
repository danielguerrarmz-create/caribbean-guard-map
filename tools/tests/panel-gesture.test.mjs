import test from 'node:test';
import assert from 'node:assert/strict';
await import('../../web/panel-gesture.js');
const back=globalThis.CGPanelGesture.shouldGoBack;
test('a deliberate rightward swipe goes back, a short drag returns to the page',()=>{
 assert.equal(back(120,12,390,0),true);assert.equal(back(30,2,390,0),false);
});
test('vertical scrolling and left swipes never go back',()=>{
 assert.equal(back(120,160,390,1),false);assert.equal(back(-140,2,390,1),false);
});
test('a short fast rightward flick works but a stationary short drag does not',()=>{
 assert.equal(back(55,8,390,.6),true);assert.equal(back(55,8,390,0),false);
});

function harness(){
 const handlers={},calls=[];
 const el={clientWidth:390,classList:{add(){},remove(){}},addEventListener(name,fn){handlers[name]=fn;}};
 CGPanelGesture.attach(el,{enabled:()=>true,progress:()=>calls.push('progress'),commit:()=>calls.push('back'),cancel:()=>calls.push('cancel')});
 const event=(x,y)=>({touches:[{clientX:x,clientY:y}],target:{closest:()=>null},cancelable:true,preventDefault(){calls.push('prevent');}});
 return {handlers,calls,event};
}
test('touch listeners follow horizontal motion and commit exactly one Back',()=>{
 const {handlers,calls,event}=harness();
 handlers.touchstart(event(20,200));handlers.touchmove(event(170,205));handlers.touchend();
 assert.deepEqual(calls,['progress','prevent','back']);
});
test('vertical touch scroll is not captured and touch cancellation restores the page',()=>{
 const a=harness();a.handlers.touchstart(a.event(20,200));a.handlers.touchmove(a.event(25,300));a.handlers.touchend();
 assert.deepEqual(a.calls,[]);
 const b=harness();b.handlers.touchstart(b.event(20,200));b.handlers.touchmove(b.event(170,205));b.handlers.touchcancel();
 assert.deepEqual(b.calls,['progress','prevent','cancel']);
});

test('an overflowing hourly strip keeps its horizontal gesture instead of navigating Back',()=>{
 const {handlers,calls,event}=harness();
 const start=event(20,200);
 start.target.closest=selector=>selector.includes('.hourly-scroll')?{scrollWidth:1600,clientWidth:340}:null;
 handlers.touchstart(start);handlers.touchmove(event(170,205));handlers.touchend();
 assert.deepEqual(calls,[]);
});
