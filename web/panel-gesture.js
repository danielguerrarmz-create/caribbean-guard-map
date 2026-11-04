/* Direction-locked back gesture. Vertical scrolling and panel dragging keep
   their existing owner; horizontal table overflow is never intercepted. */
(function(root){
  const shouldGoBack=(dx,dy,width,velocity=0)=>dx>Math.abs(dy)*1.3&&
    (dx>=Math.min(110,width*.28)||(dx>40&&velocity>.45));
  function attach(el,options){
    let gesture=null,blockClick=false;
    function start(x,y,target){
      if(!options.enabled())return;
      const table=target.closest('.forecast-table-wrap,.hourly-scroll');
      if(target.closest('input,textarea,select')||(table&&table.scrollWidth>table.clientWidth+1))return;
      gesture={x,y,lastX:x,lastTime:performance.now(),dx:0,dy:0,velocity:0,locked:false,ignored:false};
    }
    function move(x,y){
      if(!gesture||gesture.ignored)return false;
      const g=gesture,now=performance.now();g.dx=x-g.x;g.dy=y-g.y;
      if(!g.locked){
        if(Math.max(Math.abs(g.dx),Math.abs(g.dy))<10)return false;
        if(g.dx<=0||Math.abs(g.dy)*1.3>g.dx){g.ignored=true;return false;}
        g.locked=true;el.classList.add('swipe-back-active');
        root.getSelection?.()?.removeAllRanges();
      }
      g.velocity=(x-g.lastX)/Math.max(1,now-g.lastTime);g.lastX=x;g.lastTime=now;
      options.progress(Math.max(0,Math.min(el.clientWidth,g.dx)),el.clientWidth);
      return true;
    }
    function end(cancelled=false){
      if(!gesture)return;
      const g=gesture;gesture=null;el.classList.remove('swipe-back-active');
      if(!g.locked)return;
      blockClick=true;
      const velocity=performance.now()-g.lastTime<120?g.velocity:0;
      if(!cancelled&&shouldGoBack(g.dx,g.dy,el.clientWidth,velocity))options.commit();
      else options.cancel();
    }
    el.addEventListener('touchstart',e=>{
      blockClick=false;
      if(e.touches.length!==1){end(true);return;}
      const t=e.touches[0];start(t.clientX,t.clientY,e.target);
    },{passive:true});
    el.addEventListener('touchmove',e=>{
      if(e.touches.length!==1){end(true);return;}
      const t=e.touches[0];if(move(t.clientX,t.clientY)&&e.cancelable)e.preventDefault();
    },{passive:false});
    el.addEventListener('touchend',()=>end());
    el.addEventListener('touchcancel',()=>end(true));
    el.addEventListener('pointerdown',e=>{
      if(e.pointerType==='touch'||e.button!==0)return;
      blockClick=false;start(e.clientX,e.clientY,e.target);if(!gesture)return;
      const mv=event=>{if(move(event.clientX,event.clientY))event.preventDefault();};
      const up=event=>{
        window.removeEventListener('pointermove',mv);window.removeEventListener('pointerup',up);window.removeEventListener('pointercancel',up);
        end(event.type==='pointercancel');
      };
      window.addEventListener('pointermove',mv);window.addEventListener('pointerup',up);window.addEventListener('pointercancel',up);
    });
    el.addEventListener('click',e=>{if(blockClick){blockClick=false;e.preventDefault();e.stopImmediatePropagation();}},true);
    el.addEventListener('dragstart',e=>{if(gesture)e.preventDefault();});
  }
  root.CGPanelGesture={attach,shouldGoBack};
})(typeof window==='undefined'?globalThis:window);
