/* Caribbean Guard safety map, map linework.
   ============================================================================

   WHAT THIS IS
   The four drawing decisions that carry meaning on the imagery, pulled out of
   index.html so they can be reasoned about and measured on their own:

     zoneStroke(tier, zoom)          consistent stroke and alert halo widths
     taperedPolyline(latlngs, ...)   continuous coast stroke and separate casing
     curveArrow(map, latlngs,...)    simplified rip direction with a filled head
     placeLabels(map, labels)        labels that never sit on top of each other

   A CLASSIC SCRIPT, ON PURPOSE. No module, no build step. index.html is one
   hand-written file plus small siblings, and it must run from a file:// copy and
   from a service worker cache with nothing to resolve. `window.CGGeom` is the
   whole interface.

   It takes `map` and `zoom` as ARGUMENTS and never reads a global. The old
   zoneStroke() closed over the page's `map` const, which is why it could not be
   called before the map existed and why the card swatches had to re-derive the
   same numbers from a second copy of the table. One table, one function, both
   callers.
   ============================================================================ */
(function (global) {
  "use strict";

  var L = global.L;

  /* The coast is 9.61 to 9.69 N. cos() varies by 1 part in 10,000 across it, so
     one latitude for the whole map is exact to well under a pixel. */
  var LAT = 9.645;

  /* Metres per pixel. This is what makes the sizing below physical rather than a
     curve someone liked the look of. */
  function MPP(zoom) {
    return 156543.03392 * Math.cos(LAT * Math.PI / 180) / Math.pow(2, zoom);
  }

  // Stable, continuous strokes. Text labels and symbols also identify each tier.
  // Splitting geometry into taper chunks used to restart dashes and leave seams.
  var TARGET_M=14, MIN_WEIGHT=2, MIN_VISIBLE_GAP=3, HALO_K=1.6, TAPER_M=0;
  var TIERS={high:{weight:3.6},moderate:{weight:3.2},low:{weight:2.8}};
  function zoneStroke(tier,zoom){
    var weight=Math.min(TIERS[tier]?.weight||2.8,Math.max(2,2+(zoom-13)*.4));
    return {weight:weight,halo:weight+4,dashArray:null};
  }
  // Retain the public helper name for existing callers. Each beach now has one
  // uninterrupted path, with all casings below all colored strokes.
  function taperedPolyline(latlngs,style,map){
    [['cgCoastCasing',390],['cgCoastInk',400]].forEach(function(entry){
      if(!map.getPane(entry[0])){
        map.createPane(entry[0]).style.zIndex=entry[1];
        map.getPane(entry[0]).style.pointerEvents='none';
      }
    });
    var g=L.layerGroup();
    var casing=L.polyline(latlngs,{pane:'cgCoastCasing',color:'#f8fcfd',weight:style.weight+2,
      opacity:1,lineCap:'butt',lineJoin:'round',smoothFactor:.5,interactive:false}).addTo(g);
    var halo=L.polyline(latlngs,{pane:'cgCoastCasing',color:style.halo?.color||'#fff',
      weight:style.halo?.weight||0,opacity:style.halo?.opacity||0,
      lineCap:'butt',lineJoin:'round',interactive:false}).addTo(g);
    var ink=L.polyline(latlngs,{pane:'cgCoastInk',color:style.color,weight:style.weight,
      dashArray:style.dashArray||null,opacity:1,lineCap:'butt',lineJoin:'round',smoothFactor:.5,interactive:false}).addTo(g);
    g.cgSetStyle=function(next){
      casing.setStyle({weight:next.weight+2});
      ink.setStyle({weight:next.weight,color:next.color||style.color,dashArray:next.dashArray||null});
      halo.setStyle({color:next.halo?.color||'#fff',weight:next.halo?.weight||0,opacity:next.halo?.opacity??(next.halo?.color ? .5 : 0)});
    };
    return g;
  }

  // Approved proof 03: one quadratic family, fixed filled heads, no casing.
  // Source annotations remain evidence; these curves communicate broad intent.
// Original experimental geometry primitive. No source drawing is mutated.
// Arc-length sampling prevents densely digitized sections from dominating the bend.
function simplifyCurve(points) {
  const length=[0];
  for(let i=1;i<points.length;i++) length.push(length[i-1]+Math.hypot(points[i][0]-points[i-1][0],points[i][1]-points[i-1][1]));
  const total=length.at(-1);
  if(!Number.isFinite(total)||total<1e-9) return null;
  function sample(t){
    const d=t*total;let i=1;while(i<length.length-1&&length[i]<d)i++;
    const f=(d-length[i-1])/(length[i]-length[i-1]||1);
    return points[i-1].map((v,j)=>v+(points[i][j]-v)*f);
  }
  const start=points[0].slice();
  const tail=[sample(.8),sample(.9),sample(1)];
  const end=[0,1].map(j=>tail.reduce((sum,p)=>sum+p[j],0)/3);
  const dx=end[0]-start[0],dy=end[1]-start[1],chord=Math.hypot(dx,dy);
  if(chord<1e-9)return null;
  const normal=[-dy/chord,dx/chord];
  const offsets=[.2,.35,.5,.65,.8].map(t=>{const p=sample(t);return ((p[0]-start[0])*normal[0]+(p[1]-start[1])*normal[1])/chord;});
  const mean=offsets.reduce((a,b)=>a+b,0)/offsets.length;
  // One normalized bow magnitude, mirrored only to retain the broad bend sense.
  const bow=Math.abs(mean)<.025?0:Math.sign(mean)*.22*chord;
  const control=[(start[0]+end[0])/2+normal[0]*bow,(start[1]+end[1])/2+normal[1]*bow];
  return {start,control,end,bowRatio:bow/chord};
}

  function ripShape(map, latlngs) {
    const curve=simplifyCurve(latlngs.map(ll=>{
      const p=map.latLngToLayerPoint(ll); return [p.x,p.y];
    }));
    if(!curve)return {shaft:[],head:[]};
    const {start:a,control:c,end:b}=curve;
    const convert=p=>map.layerPointToLatLng(L.point(p[0],p[1]));
    const shaft=[];
    for(let i=0;i<=32;i++){
      const t=i/32,v=1-t;
      shaft.push(convert([v*v*a[0]+2*v*t*c[0]+t*t*b[0],v*v*a[1]+2*v*t*c[1]+t*t*b[1]]));
    }
    const dx=b[0]-c[0],dy=b[1]-c[1],length=Math.hypot(dx,dy);
    const ux=dx/length,uy=dy/length;
    // Same 7 x 6 px head as the proof marker: tip 1 px beyond the shaft cap.
    const head=[[b[0]-6*ux-3*uy,b[1]-6*uy+3*ux],
      [b[0]+ux,b[1]+uy],[b[0]-6*ux+3*uy,b[1]-6*uy-3*ux]].map(convert);
    return {shaft,head};
  }
  function curveArrow(map,latlngs,opts={}) {
    if(!map.getPane('cgRipPane')){
      map.createPane('cgRipPane').style.zIndex=410;
      map.getPane('cgRipPane').style.pointerEvents='none';
    }
    const group=L.layerGroup(),color=opts.color||'#f04444';
    const shape=ripShape(map,latlngs);
    const shaft=L.polyline(shape.shaft,{pane:'cgRipPane',color,weight:2,opacity:1,
      dashArray:'8 6',lineCap:'round',lineJoin:'round',smoothFactor:0,
      interactive:false,className:'cg-rip-shaft cg-rip-dashes'}).addTo(group);
    // Open V, following the source flow direction. No closing edge or fill.
    const head=L.polyline(shape.head,{pane:'cgRipPane',color,weight:2,opacity:1,
      fill:false,lineCap:'round',lineJoin:'round',smoothFactor:0,
      interactive:false,className:'cg-rip-head'}).addTo(group);
    group.cgRedraw=function(m,lls){
      const next=ripShape(m,lls);shaft.setLatLngs(next.shaft);head.setLatLngs(next.head);
    };
    return group;
  }

  // Group only symbols that collide with a real member's anchor, never a
  // centroid. A chain of nearby stations must not swallow an entire coastline.
  function groupMarkers(entries,gap=12){
    const groups=[];
    for(const entry of entries){
      const group=groups.find(({anchor})=>{
        const clearance=(entry.size+anchor.size)/2+gap;
        return Math.abs(entry.x-anchor.x)<clearance&&Math.abs(entry.y-anchor.y)<clearance;
      });
      if(group)group.members.push(entry);
      else groups.push({anchor:entry,members:[entry]});
    }
    return groups;
  }

  // Labels may move within a small local radius; geographic symbols never do.
  // A crowded or off-screen beach yields instead of being pulled across the map.
  function layoutBeachLabels(entries, obstacles, bounds, gap=6){
    const placed=[], result=[];
    const hits=(a,b)=>a.left<b.right+gap&&a.right>b.left-gap&&a.top<b.bottom+gap&&a.bottom>b.top-gap;
    for(const entry of entries){
      const w=entry.width,h=entry.height;
      const candidates=[];
      const add=(left,top)=>{
        if(left<bounds.left||left+w>bounds.right||top<bounds.top||top+h>bounds.bottom)return;
        candidates.push({left,top,right:left+w,bottom:top+h});
      };
      add(entry.left,entry.top);
      for(let dy=-72;dy<=72;dy+=12)
        for(let dx=-72;dx<=72;dx+=12)
          if(Math.hypot(dx,dy)<=72)add(entry.left+dx,entry.top+dy);
      candidates.sort((a,b)=>{
        const cost=r=>2*Math.pow(r.left-entry.left,2)+Math.pow(r.top-entry.top,2);
        return cost(a)-cost(b);
      });
      const box=candidates.find(r=>!obstacles.some(o=>hits(r,o))&&!placed.some(o=>hits(r,o)));
      if(box){placed.push(box);result.push({...box,id:entry.id});}
    }
    return result;
  }

  // Screen-space selection only. Never offset, snap or alter source coordinates.
  // Required rescue markers always survive; others return as soon as space exists.
  function declutterMarkers(entries,gap=6){
    const kept=[];
    const ranked=entries.slice().sort((a,b)=>Number(!!b.required)-Number(!!a.required)||b.priority-a.priority);
    for(const entry of ranked){
      const clash=kept.some(other=>{
        const clearance=(entry.size+other.size)/2+gap;
        return Math.abs(entry.x-other.x)<clearance&&Math.abs(entry.y-other.y)<clearance;
      });
      if(entry.required||!clash)kept.push(entry);
    }
    return kept.map(entry=>entry.id);
  }

  /* ==========================================================================
     placeLabels
     ==========================================================================

     "PUERTO VIEJO" and "Playa Cocles" are 340 m apart and both sit on the water.
     Between z13 and z14 their boxes overlap and the two words interleave into
     one unreadable run, which is worse than either being absent: a label that
     cannot be read still costs the imagery underneath it.

     Resolved by PRIORITY, not by nudging. Nudging a label moves it off the thing
     it names, and on a 16 km strip there is nowhere to nudge to that is not also
     water somebody else has claimed. So the higher priority label keeps its
     place and the lower one is hidden outright. Zone names outrank town names:
     the zone is the thing the map is for, and a town the reader cannot see
     named is still a town they can see.

     Screen rectangles, not distance in metres: the labels are DOM elements of
     different lengths and the thing that must not overlap is the ink, and the
     ink is measured in pixels.

     labels: [{marker, priority, visible}]  -- `visible` is the caller's own zoom
     rule; this only ever hides, never shows something the caller ruled out.
     Returns {shown, hidden}. Idempotent: safe to call on every zoomend. */
  var LABEL_PAD = 4;

  function placeLabels(map, labels) {
    var i, entries = [];
    // Show everything the caller allows first. Measuring a display:none element
    // returns a zero rect, so a label hidden by the previous pass would look
    // like it collides with nothing and every pass would hide a different set.
    for (i = 0; i < labels.length; i++) {
      var el = labels[i].marker && labels[i].marker.getElement();
      if (!el) continue;
      if (labels[i].visible === false) { el.style.display = "none"; continue; }
      el.style.display = "";
      entries.push({ el: el, priority: labels[i].priority || 0 });
    }
    // Descending priority, so the first claim on a patch of screen is the one
    // that matters most. Stable enough: ties keep caller order.
    entries.sort(function (a, b) { return b.priority - a.priority; });

    var taken = [], shown = 0, hidden = 0;
    for (i = 0; i < entries.length; i++) {
      var r = entries[i].el.getBoundingClientRect();
      var box = { l: r.left - LABEL_PAD, t: r.top - LABEL_PAD,
                  r: r.right + LABEL_PAD, b: r.bottom + LABEL_PAD };
      var clash = false;
      for (var j = 0; j < taken.length; j++) {
        var o = taken[j];
        if (box.l < o.r && box.r > o.l && box.t < o.b && box.b > o.t) { clash = true; break; }
      }
      if (clash) { entries[i].el.style.display = "none"; hidden++; }
      else { taken.push(box); shown++; }
    }
    return { shown: shown, hidden: hidden };
  }

  global.CGGeom = {
    LAT: LAT,
    MPP: MPP,
    TIERS: TIERS,
    TARGET_M: TARGET_M,
    MIN_WEIGHT: MIN_WEIGHT,
    MIN_VISIBLE_GAP: MIN_VISIBLE_GAP,
    HALO_K: HALO_K,
    TAPER_M: TAPER_M,
    zoneStroke: zoneStroke,
    taperedPolyline: taperedPolyline,
    simplifyCurve: simplifyCurve,
    ripShape: ripShape,
    curveArrow: curveArrow,
    declutterMarkers: declutterMarkers,
    groupMarkers: groupMarkers,
    layoutBeachLabels: layoutBeachLabels,
    placeLabels: placeLabels
  };
})(typeof globalThis !== "undefined" ? globalThis : this);
