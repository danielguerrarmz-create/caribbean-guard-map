/* Caribbean Guard safety map, map linework.
   ============================================================================

   WHAT THIS IS
   The four drawing decisions that carry meaning on the imagery, pulled out of
   index.html so they can be reasoned about and measured on their own:

     zoneStroke(tier, zoom)          how heavy, how dashed, how haloed
     taperedPolyline(latlngs, ...)   a zone line that stops without a blunt cut
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

  /* ==========================================================================
     zoneStroke
     ==========================================================================

     WEIGHT IS SOLVED FOR A WIDTH ON THE GROUND, not for a zoom ramp. TARGET_M is
     30, a little under a beach width, so the stroke never claims more coast than
     the zone holds. The ramp this replaced put the `high` stroke at 149 m of
     ground width at the whole-coast view, describing a beach about 40 m wide,
     with a halo adding 472 m on top: the map read as a continuous wall of hazard
     from the opening view. Clamped at both ends, because physics alone makes the
     line invisible at z12 and absurd at z18.

     THE DASH CARRIES THE TIER, NOT THE WEIGHT. This is the change that matters.
     At the landing zoom the ground solve clamps, and all three weights land
     within half a pixel of each other: 2.42, 2.00, 2.00 px. Weight cannot
     separate the tiers there and nothing can make it, because 30 m is 0.8 px at
     z12. The old code scaled each dash COMPONENT by the same k, which floored
     "2 8" to "2 2" -- 1:4 became 1:1 -- and "16 10" to "3.5 2.2". The three
     textures converged at exactly the zoom a deuteranope first looks at, which
     is where colour is already gone. So:

       - the RATIO dash:gap is fixed per tier and never scales (1:4 low,
         1.6:1 moderate, solid high);
       - the gap has a floor, and the floor is MEASURED FROM THE VISIBLE GAP.
         Round caps extend every dash by weight/2 at each end, so a nominal 3 px
         gap on a 2 px line shows as 1 px of daylight. The floor is 3 + weight.

     At z12 that gives low "1.25 5" against moderate "8 5" against solid: three
     textures nobody has to see colour to separate. At z17 the nominal spacing is
     the larger of the two and the floor stops binding, so the close-up pattern
     is unchanged from what the sheets already show.

     HALO is weight * 1.6, and nothing else. It used to be weight * 2.4 + 6, and
     that constant 6 px is 113 m at z13: a bulletin halo wider than the beach it
     sat under. A halo that scales with its stroke cannot outgrow it. */
  /* HALVED ON 2026-09-17, and the ground solve is why it needed halving.
     TARGET_M was 30 and K_MAX was 1.3, which put the `high` stroke at 14.3 px
     at z17. A 14 px line at 0.89 m/px is 13 m of ground: a red band as wide as
     half the beach, drawn on top of the imagery the reader is trying to see
     through it. Daniel's finding was "all linework needs to be simplified", and
     the wandering trace was only half of that; the other half is that the line
     was too heavy to read as a line at all.
     TARGET_M is now 14, so the heaviest stroke describes 14 m of water rather
     than 30, and K_MAX is 1.0, so nothing is ever drawn heavier than its tier
     weight. `high` lands at 7 px at z17 against 14.3, and the ranking between
     the three tiers and the dash textures below are all unchanged. */
  var TARGET_M = 14;
  var MIN_WEIGHT = 2;        // a 1.6 px line on a 2x DPR phone in sun is not there
  var MIN_VISIBLE_GAP = 3;   // px of actual daylight, after round caps eat theirs
  var HALO_K = 1.6;

  var TIERS = {
    /* weight: the reference ratio between the tiers. The loudest mark is always
       the most dangerous one, and that ranking is preserved at every zoom.
       ratio:  dash length / gap length. null is solid.
       gapK:   nominal gap in units of stroke weight, so the texture stays
               proportional to the line when the floor is not binding. */
    high: { weight: 7, ratio: null, gapK: 0 },
    moderate: { weight: 5.5, ratio: 1.6, gapK: 1.25 },
    low: { weight: 4, ratio: 0.25, gapK: 1.6 }
  };

  var K_MIN = 0.3, K_MAX = 1.0;

  function round2(n) { return Math.round(n * 100) / 100; }

  function zoneStroke(tier, zoom) {
    var base = TIERS[tier] || TIERS.low;
    // Solved against the heaviest tier so the ratio between the three survives
    // the scaling; it is the ranking, not the absolute width, that does the work.
    var k = TARGET_M / (MPP(zoom) * TIERS.high.weight);
    if (k < K_MIN) k = K_MIN;
    if (k > K_MAX) k = K_MAX;

    var weight = Math.max(MIN_WEIGHT, base.weight * k);
    var out = { weight: round2(weight), halo: round2(weight * HALO_K), dashArray: null };

    if (base.ratio) {
      var gap = Math.max(base.gapK * weight, MIN_VISIBLE_GAP + weight);
      var dash = Math.max(1, gap * base.ratio);
      out.dashArray = round2(dash) + " " + round2(gap);
    }
    return out;
  }

  /* ==========================================================================
     taperedPolyline
     ==========================================================================

     A zone ends where somebody decided it ends, not where the coast does. Cocles
     runs into Chiquita with 419 m between their nearest vertices and no feature
     on the water marking the change. A full-weight stroke stopping dead draws a
     boundary the sea does not have, and a reader takes a hard edge as a fact.
     The last 40 m ramps to 40% weight so the line admits it is fading out of a
     claim rather than hitting the edge of one.

     40 m is chosen against the thing it has to survive: it is about a third of
     the shortest zone's own taper budget, one pixel at z12 (so it costs nothing
     where it would only blur), and 34 px at z17 (where it reads as a taper).

     Drawn as a handful of constant-weight chunks rather than a true variable
     width stroke, because SVG has no variable width stroke and a polygon outline
     would have to be rebuilt on every zoom. Five chunks per end at 0.4, 0.55,
     0.7, 0.85 and 1.0 of the weight, sharing endpoints, round caps: the steps
     are under a pixel apart at every zoom this map allows.

     The chunk boundaries are computed in GROUND distance once and cached. They
     do not move with zoom, so a restyle only rewrites weights. */
  var TAPER_M = 40;
  var TAPER_STEPS = 5;
  var TAPER_MIN_FRAC = 0.4;

  function cumulative(map, pts) {
    var cum = [0], i;
    for (i = 1; i < pts.length; i++) {
      cum.push(cum[i - 1] + map.distance(pts[i - 1], pts[i]));
    }
    return cum;
  }

  // The point at cumulative distance d, interpolating inside whatever segment
  // holds it. Linear in lat/lon: over a segment of a few metres the difference
  // from a great-circle interpolation is micrometres.
  function atDistance(pts, cum, d) {
    if (d <= 0) return pts[0].slice();
    var last = cum.length - 1;
    if (d >= cum[last]) return pts[last].slice();
    var lo = 0, hi = last;
    while (hi - lo > 1) {
      var mid = (lo + hi) >> 1;
      if (cum[mid] <= d) lo = mid; else hi = mid;
    }
    var span = cum[hi] - cum[lo];
    var t = span > 0 ? (d - cum[lo]) / span : 0;
    return [pts[lo][0] + (pts[hi][0] - pts[lo][0]) * t,
            pts[lo][1] + (pts[hi][1] - pts[lo][1]) * t];
  }

  // Every source vertex strictly between d0 and d1, with exact interpolated ends.
  // Keeping the interior vertices is the point: a chunk is a slice of the coast,
  // not a chord across it.
  function slice(pts, cum, d0, d1) {
    var out = [atDistance(pts, cum, d0)], i;
    for (i = 0; i < pts.length; i++) {
      if (cum[i] > d0 && cum[i] < d1) out.push(pts[i].slice());
    }
    out.push(atDistance(pts, cum, d1));
    return out;
  }

  function taperPlan(map, pts) {
    var cum = cumulative(map, pts);
    var total = cum[cum.length - 1];
    var chunks = [], i;
    // A zone shorter than three tapers is all end and no middle; shrink rather
    // than skip, so a short zone still stops softly.
    var taper = Math.min(TAPER_M, total / 3);
    if (!(total > 0) || taper <= 0) return [{ pts: pts.map(function (p) { return p.slice(); }), frac: 1 }];

    var step = taper / TAPER_STEPS;
    var ramp = function (j) {
      return TAPER_MIN_FRAC + (1 - TAPER_MIN_FRAC) * (j / (TAPER_STEPS - 1));
    };
    for (i = 0; i < TAPER_STEPS; i++) {
      chunks.push({ pts: slice(pts, cum, i * step, (i + 1) * step), frac: ramp(i) });
    }
    chunks.push({ pts: slice(pts, cum, taper, total - taper), frac: 1 });
    for (i = TAPER_STEPS - 1; i >= 0; i--) {
      chunks.push({
        pts: slice(pts, cum, total - (i + 1) * step, total - i * step),
        frac: ramp(i)
      });
    }
    return chunks;
  }

  /* style: {color, weight, dashArray, opacity, halo:{color, weight, opacity}}
     Returns an L.LayerGroup carrying cgSetStyle(style), so a zoom handler
     updates weights without rebuilding geometry. The halo tapers with the line;
     a full-width halo under a tapering stroke puts the blunt end back. */
  function taperedPolyline(latlngs, style, map) {
    var g = L.layerGroup();
    var plan = taperPlan(map, latlngs);
    var haloLayers = [], lineLayers = [], i;

    function mk(chunk, colour, weight, opacity, dash) {
      return L.polyline(chunk.pts, {
        color: colour, weight: weight, opacity: opacity,
        dashArray: dash || null,
        lineCap: "round", lineJoin: "round",
        interactive: false
      }).addTo(g);
    }

    // Halo first: everything in this group draws in insertion order, and the
    // bulletin halo is additive UNDER the character stroke, never instead of it.
    if (style.halo) {
      for (i = 0; i < plan.length; i++) {
        haloLayers.push(mk(plan[i], style.halo.color,
          (style.halo.weight || style.weight * HALO_K) * plan[i].frac,
          style.halo.opacity == null ? 0.5 : style.halo.opacity, null));
      }
    }
    for (i = 0; i < plan.length; i++) {
      lineLayers.push(mk(plan[i], style.color, style.weight * plan[i].frac,
        style.opacity == null ? 1 : style.opacity, style.dashArray));
    }

    g.cgPlan = plan;
    g.cgSetStyle = function (s) {
      var j;
      for (j = 0; j < lineLayers.length; j++) {
        lineLayers[j].setStyle({
          color: s.color == null ? style.color : s.color,
          weight: s.weight * plan[j].frac,
          dashArray: s.dashArray || null
        });
      }
      if (s.halo) {
        for (j = 0; j < haloLayers.length; j++) {
          haloLayers[j].setStyle({
            color: s.halo.color,
            weight: (s.halo.weight || s.weight * HALO_K) * plan[j].frac
          });
        }
      }
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
    return { weight: 1.7 + t * 1.3, head: 9 + t * 9, shaftMin: 20 - t * 16 };
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

    function poly(pts, c, w, op, d, klass) {
      return L.polyline(pts, {
        color: c, weight: w, opacity: op, dashArray: d || null,
        lineCap: "round", lineJoin: "round", interactive: false,
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

    // One fine outline makes the mark legible over dark reef and pale surf.
    var phase = Math.abs(Math.round((latlngs[0][0] + latlngs[0][1]) * 100000)) % 4;
    var pulse = 'cg-current-pulse cg-current-phase-' + phase;
    var shaftOut = poly(drawn, oc, w + 2 * ow, oo, dash, pulse);
    var shaft = poly(drawn, colour, w, 1, dash, pulse);
    var headOut = poly(head, oc, w + 2 * ow, oo, null, pulse);
    var headLine = poly(head, colour, w, 1, null, pulse);

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
