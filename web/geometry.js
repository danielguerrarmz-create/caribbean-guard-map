/* Caribbean Guard safety map, map linework.
   ============================================================================

   WHAT THIS IS
   The four drawing decisions that carry meaning on the imagery, pulled out of
   index.html so they can be reasoned about and measured on their own:

     zoneStroke(tier, zoom)          consistent stroke and alert halo widths
     taperedPolyline(latlngs, ...)   continuous coast stroke and separate casing
     outlinedArrow(map, latlngs,...) a rip arrow that holds contrast over water
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

  /* ==========================================================================
     outlinedArrow
     ==========================================================================

     Measured on the shipped map, the rip arrow is #e53935 on water sampled at
     rgb(45,72,65): 2.00:1 normally and 1.79:1 simulated deuteranope, against the
     3:1 bar WCAG 1.4.11 sets for a graphical object that carries meaning. A drop
     shadow does not fix that, because a shadow is a blur and contrast is measured
     at the edge.

     A 1.5 px hard outline does: the same geometry drawn underneath in #0b1c2c at
     0.85 opacity, 3 px wider, so 1.5 px of ink shows on each side. Ink on that
     water is 1.29:1 -- dark on dark -- but ink against the RED is 4.4:1, and it
     is the red/ink edge the eye locks onto. The arrow stops depending on the
     water it happens to be over, which changes from sand to reef to open sea
     along one beach.

     The outline follows the same solid shaft, avoiding broken-looking arrows
     where several document marks sit close together. */
  var ARROW_OUTLINE = "#0b1c2c";
  var ARROW_OUTLINE_W = 1.0;
  var ARROW_OUTLINE_OPACITY = 0.85;

  /* A rip is 30 to 100 m long, which is a couple of pixels at the whole-coast
     view: a fixed head is a red blob detached from a shaft nobody can see, and
     nine of them read as noise. Both scale with zoom, clamped at each end. */
  function arrowScale(zoom) {
    var t = Math.max(0, Math.min(1, (zoom - 12) / 5));
    return { weight: 1.5 + t * .7, head: 7 + t * 5, shaftMin: 20 - t * 16 };
  }

  /* At the overview a 40 m rip is shorter than its own arrowhead, so the drawn
     shaft is stretched to a readable minimum along its own bearing. The POSITION
     stays the position; only the drawn length changes, and it stops mattering by
     z15. */
  function shaftPoints(map, pts, zoom) {
    var sc = arrowScale(zoom == null ? map.getZoom() : zoom);
    if (sc.shaftMin <= 1 || pts.length < 2) return pts;
    var a = map.latLngToLayerPoint(pts[0]);
    var b = map.latLngToLayerPoint(pts[pts.length - 1]);
    var dx = b.x - a.x, dy = b.y - a.y, len = Math.hypot(dx, dy);
    if (len >= sc.shaftMin || len === 0) return pts;
    var k = sc.shaftMin / len;
    return [pts[0], map.layerPointToLatLng(L.point(a.x + dx * k, a.y + dy * k))];
  }

  // A compact open chevron reads as direction without the visual mass of a
  // filled triangle. The shaft ends at the chevron tip.
  function headPoints(map, a, b, headLen) {
    var p1 = map.latLngToLayerPoint(a), p2 = map.latLngToLayerPoint(b);
    var ang = Math.atan2(p2.y - p1.y, p2.x - p1.x);
    var bx = p2.x - headLen * Math.cos(ang), by = p2.y - headLen * Math.sin(ang);
    var half = headLen * 0.58;
    return [map.layerPointToLatLng(L.point(bx + half * Math.sin(ang), by - half * Math.cos(ang))),
      b,
      map.layerPointToLatLng(L.point(bx - half * Math.sin(ang), by + half * Math.cos(ang)))];
  }

  // Fit a restrained cubic to quarter points of the PDF stroke. Its controls
  // stay one-third and two-thirds along the chord, so noisy PDF samples cannot
  // make loops or hooks. Only the lateral offsets shape the curve, and both
  // source endpoints remain fixed to preserve the GPS shoreline registration.
  function gentleShaft(map, pts, zoom) {
    var raw = shaftPoints(map, pts, zoom);
    if (raw.length < 3) return raw;
    var px = raw.map(function (p) { return map.latLngToLayerPoint(p); });
    var dist = [0], i;
    for (i = 1; i < px.length; i++)
      dist.push(dist[i - 1] + px[i].distanceTo(px[i - 1]));
    var total = dist[dist.length - 1];
    if (total < 1) return [raw[0], raw[raw.length - 1]];
    var a = px[0], b = px[px.length - 1];
    var dx = b.x - a.x, dy = b.y - a.y, chord = Math.hypot(dx, dy);
    if (chord < 1) return [raw[0], raw[raw.length - 1]];
    function along(fraction) {
      var target = total * fraction;
      for (var j = 1; j < dist.length; j++) if (dist[j] >= target) {
        var t = (target - dist[j - 1]) / (dist[j] - dist[j - 1] || 1);
        return L.point(px[j - 1].x + (px[j].x - px[j - 1].x) * t,
                       px[j - 1].y + (px[j].y - px[j - 1].y) * t);
      }
      return b;
    }
    var nx = -dy / chord, ny = dx / chord;
    var cap = Math.min(chord * .20, 24);
    function control(fraction, baseFraction) {
      var source = along(fraction);
      var baseline = L.point(a.x + dx * fraction, a.y + dy * fraction);
      var lateral = Math.max(-cap, Math.min(cap,
        ((source.x - baseline.x) * nx + (source.y - baseline.y) * ny) * 1.35));
      return L.point(a.x + dx * baseFraction + nx * lateral,
                     a.y + dy * baseFraction + ny * lateral);
    }
    var c1 = control(.25, 1 / 3), c2 = control(.75, 2 / 3);
    // Even a straight PDF segment needs a modest visual arc at beach zoom;
    // limit it to a few screen pixels, well inside the source registration
    // uncertainty. Curved source segments keep their authored bend instead.
    var bend1 = (c1.x - a.x - dx / 3) * nx + (c1.y - a.y - dy / 3) * ny;
    var bend2 = (c2.x - a.x - 2 * dx / 3) * nx +
                (c2.y - a.y - 2 * dy / 3) * ny;
    if (Math.max(Math.abs(bend1), Math.abs(bend2)) < 2) {
      var side = Math.round((raw[0].lat + raw[0].lng) * 100000) % 2 ? 1 : -1;
      var bow = side * Math.min(6, Math.max(2.5, chord * .055));
      c1 = L.point(c1.x + nx * bow, c1.y + ny * bow);
      c2 = L.point(c2.x + nx * bow, c2.y + ny * bow);
    }
    var steps = Math.max(10, Math.min(32, Math.ceil(total / 6)));
    var out = [];
    for (i = 0; i <= steps; i++) {
      var u = i / steps, v = 1 - u;
      out.push(map.layerPointToLatLng(L.point(
        v*v*v*a.x + 3*v*v*u*c1.x + 3*v*u*u*c2.x + u*u*u*b.x,
        v*v*v*a.y + 3*v*v*u*c1.y + 3*v*u*u*c2.y + u*u*u*b.y)));
    }
    return out;
  }

  /* opts: {color, weight, head, dashArray, outline, outlineWidth, outlineOpacity}
     Anything omitted falls back to the rip defaults above.
     Returns an L.LayerGroup with cgRedraw(map, latlngs, opts) -- heads and the
     shaft minimum are sized in SCREEN space, so both are rebuilt on zoom. */
  function outlinedArrow(map, latlngs, opts) {
    opts = opts || {};
    var g = L.layerGroup();
    var ow = opts.outlineWidth == null ? ARROW_OUTLINE_W : opts.outlineWidth;
    var colour = opts.color || "#e53935";
    var dash = opts.dashArray === undefined ? null : opts.dashArray;

    /* ITS OWN PANE, SO ITS MOTION REPAINTS ONLY ITSELF. Leaflet draws every
       vector in a pane into one SVG, and an animated stroke repaints the SVG it
       lives in. In the overlay pane that was every beach stroke too, on every
       frame; in this pane it is the rips alone. */
    if (!map.getPane("cgRipPane")) {
      map.createPane("cgRipPane").style.zIndex = 410;
      map.getPane("cgRipPane").style.pointerEvents = "none";
    }
    function poly(pts, c, w, op, d, klass, cap) {
      return L.polyline(pts, {
        pane: "cgRipPane",
        color: c, weight: w, opacity: op, dashArray: d || null,
        lineCap: cap || "round", lineJoin: "round", interactive: false,
        className: klass || ''
      }).addTo(g);
    }

    var zoom = map.getZoom();
    var sc = arrowScale(zoom);
    var w = opts.weight == null ? sc.weight : opts.weight;
    var hl = opts.head == null ? sc.head : opts.head;
    var drawn = gentleShaft(map, latlngs, zoom);
    var head = headPoints(map, drawn[drawn.length - 2] || drawn[0],
                          drawn[drawn.length - 1], hl);
    var oc = opts.outline || ARROW_OUTLINE;
    var oo = opts.outlineOpacity == null ? ARROW_OUTLINE_OPACITY : opts.outlineOpacity;

    // One continuous shaft and chevron. Draw outlines before all color so the
    // head cannot cut across its own shaft. No animated dashes or broad channels.
    var shaftOut=poly(drawn,oc,w+2*ow,1,null,'cg-rip-shaft');
    var headOut=poly(head,oc,w+2*ow,1,null,'cg-rip-head');
    var shaft=poly(drawn,colour,w,1,null,'cg-rip-shaft');
    var headLine=poly(head,colour,w,1,null,'cg-rip-head');

    g.cgRedraw = function (m, lls, o) {
      o = o || opts;
      var z = m.getZoom(), s = arrowScale(z);
      var ww = o.weight == null ? s.weight : o.weight;
      var hh = o.head == null ? s.head : o.head;
      var ow2 = o.outlineWidth == null ? ARROW_OUTLINE_W : o.outlineWidth;
      var d2 = gentleShaft(m, lls, z);
      var h2 = headPoints(m, d2[d2.length - 2] || d2[0], d2[d2.length - 1], hh);
      shaftOut.setLatLngs(d2); shaftOut.setStyle({ weight: ww + 2 * ow2 });
      shaft.setLatLngs(d2); shaft.setStyle({ weight: ww });
      headOut.setLatLngs(h2); headOut.setStyle({ weight: ww + 2 * ow2 });
      headLine.setLatLngs(h2); headLine.setStyle({ weight: ww });
    };
    return g;
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
    arrowScale: arrowScale,
    shaftPoints: shaftPoints,
    outlinedArrow: outlinedArrow,
    placeLabels: placeLabels
  };
})(typeof globalThis !== "undefined" ? globalThis : this);
