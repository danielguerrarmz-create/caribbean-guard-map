# Workstream A -> index.html: what to call, what to delete

Written 2026-09-17 by workstream A (map linework and tiles). Nothing here edits
`web/index.html`; all of it is yours to apply.

**Line numbers are from `web/index.html` at 2,985 lines and they will have moved
by the time you read this.** Every item names the anchor text as well. Search for
the anchor, not the number.

---

## 0. One new script tag, one new fetch

```html
<script src="vendor/leaflet.js"></script>
<script src="geometry.js"></script>      <!-- ADD, after Leaflet, before the app -->
```

Anchor: `<script src="vendor/leaflet.js"></script>`, line **709**.

`geometry.js` is a classic script. It defines `window.CGGeom` and nothing else,
reads no global, and takes `map` and `zoom` as arguments. It must load AFTER
Leaflet (it captures `window.L` at definition time) and BEFORE the app script.

Both files are already in the service worker's CRITICAL precache along with
`data/zones-geometry.json` and the two Atkinson woff2 files, and `CACHE` is now
`cg-map-v3`.

---

## 1. Zone geometry moves out of the HTML

**Delete the five `line:` arrays** inside `ZONES` (`const ZONES = [`, line **828**;
the arrays are at lines **849, 866, 898, 919, 950**). They are the broken
nine-to-sixty-point decimations from the retired `redraw_zones.py`, the ones that
cut inland on every convex bend and that the 2026-09-14 handoff left as open item
2. Keep every other field in the zone records.

**Load the replacement** from `data/zones-geometry.json`, keyed by the same
`cg:zone/...` ids, coordinates as `[lat, lon]`:

```js
const zoneGeom = await fetch("data/zones-geometry.json").then(r => r.json());
// zoneGeom.zones["cg:zone/cocles"] -> [[lat, lon], ...]
```

Regenerate it with `python tools/export_zones.py`. It reads the ids out of
index.html and refuses to run if the two sets have drifted, so a renamed zone is a
loud failure rather than a missing line.

| zone | points before | points now |
|---|---|---|
| playa-negra | 7 | 160 |
| salsa-brava | 34 | 448 |
| cocles | 38 | 793 |
| chiquita | 60 | 917 |
| punta-uva | 32 | 503 |

**A DECISION FOR YOU.** Drawing needs the geometry, and the geometry now arrives
over the network. The zone CARDS do not need it and must still paint before
Leaflet parses, which is hat 4's finding 6. So render the cards from `ZONES`
synchronously as planned, and let the lines appear when the fetch lands. Do not
keep a short fallback copy of the geometry in the HTML: a hazard line in the
wrong place is a claim, not a gap.

---

## 2. `zoneStroke` — replace the body, keep the name

**Delete** `const STROKE` (line **1979**), `const MPP` (**1998**), `const TARGET_M`
(**2013**) and `function zoneStroke(tier)` (**2014**). Replace every call with:

```js
CGGeom.zoneStroke(tier, map.getZoom())   // -> {weight, halo, dashArray|null}
```

The old one closed over the page's `map`, so it could not be called before the map
existed and the card swatch had to re-derive the same numbers from a second copy
of the table. The new one takes the zoom, so the swatch and the map read one
table. `CGGeom.TIERS` exposes the reference weights if the swatch wants them.

What changed in the numbers, and why it matters to your cards:

| | z12 (landing) | z17 (a beach) |
|---|---|---|
| high | 2.42 px, solid | 14.3 px, solid |
| moderate | 2 px, `8 5` | 10.4 px, `21.44 13.4` |
| low | 2 px, `1.25 5` | 6.5 px, `2.6 10.4` |

At z17 the patterns are within a rounding of what ships today. At z12 they are the
fix for hat 4's blocker 4: the old code scaled each dash COMPONENT by the same
factor, which floored `"2 8"` to `"2 2"` and turned 1:4 into 1:1, so all three
textures converged at exactly the zoom a deuteranope first looks at. Now the
dash:gap RATIO is fixed per tier and only the gap has a floor, measured from the
VISIBLE gap after round caps eat their half-weight at each end.

Minimum weight is 2 px. Halo is `weight * 1.6` and nothing else.

---

## 3. Zone lines: `taperedPolyline`

In the `/* ---------- draw zones ---------- */` block (line **2049**), replace the
`L.polyline` for the halo and the `L.polyline` for the line with one call:

```js
const st = CGGeom.zoneStroke(tierOf(z), map.getZoom());
const g = CGGeom.taperedPolyline(zoneGeom.zones[z.id], {
  color: COLOR[tierOf(z)],
  weight: st.weight,
  dashArray: st.dashArray,
  halo: todayHalo(z) ? {color: todayHalo(z), weight: st.halo, opacity: .5} : null
}, map).addTo(map);
layers[z.id] = g;
```

Keep your own invisible hit polyline exactly as it is; `taperedPolyline` sets
`interactive: false` on everything it draws so it cannot swallow a tap.

In `restyleZones()` (line **2035**) replace the two `setStyle` calls with:

```js
const st = CGGeom.zoneStroke(tierOf(z), map.getZoom());
layers[z.id].cgSetStyle({
  weight: st.weight * (current ? 1.25 : 1),
  dashArray: st.dashArray,
  halo: haloColour ? {color: haloColour, weight: st.halo} : null
});
```

The taper is 40 m at each end ramping to 40% weight, as five constant-weight
chunks sharing endpoints. Chunk boundaries are computed once in ground distance
and cached on the group, so a restyle only rewrites weights. The halo tapers with
the line; a full-width halo under a tapering stroke puts the blunt end back.

---

## 4. Rip arrows: `outlinedArrow`

**Delete** `function arrowScale()` (**2586**), `function arrowHead()` (**2593**)
and `function shaftPoints()` (**2611**). In `drawAnnotations()` (**2621**), the
`rip_current` branch becomes:

```js
const pts = f.geometry.coordinates.map(c => [c[1], c[0]]);
const arrow = CGGeom.outlinedArrow(map, pts, {}).addTo(layer);
ANNOT.rips.push({f, pts, arrow});
```

and the `zoomend` handler becomes:

```js
ANNOT.rips.forEach(r => r.arrow.cgRedraw(map, r.pts, {}));
```

Defaults are the rip defaults: `#e53935`, dash `9 6`, `#0b1c2c` at 0.85 opacity,
1.5 px of ink on each side, head and weight from zoom. `CGGeom.arrowScale(zoom)`
and `CGGeom.shaftPoints(map, pts, zoom)` are exported if you need them directly.

This is hat 4's finding 5: the red measures 2.00:1 against sampled water and
1.79:1 simulated deuteranope, against a 3:1 bar. A shadow cannot fix that, because
contrast is measured at the edge and a shadow is a blur. Ink against the red is
4.4:1, and that is the edge the eye locks onto, so the arrow stops depending on
whatever water it happens to be over.

---

## 5. Labels: `placeLabels`

At the end of `restyleLabels()` (line **1874**), after your own zoom rules have
decided what is eligible, add:

```js
CGGeom.placeLabels(map, [
  ...zoneLabels.map(m  => ({marker: m, priority: 10, visible: zoomAllowsZones})),
  ...placeMarks.map(m  => ({marker: m, priority: 1,  visible: zoomAllowsPlaces})),
  {marker: seaLabel, priority: 5, visible: zoomAllowsSea}
]);
// -> {shown, hidden}
```

It only ever hides. `visible: false` is your ruling and is never overturned.
Higher priority keeps its place and the loser is hidden outright, because nudging
a label moves it off the thing it names and on a 16 km strip there is nowhere to
nudge to that is not water somebody else has claimed. Zone names outrank town
names: a town the reader cannot see named is still a town they can see. Idempotent
and safe on every `zoomend`.

Note `placeLabels` is a FUNCTION here. The current file has a CONST of that name
(`const placeLabels = PLACES.map(...)`, near line **1855**). Rename yours;
`placeMarks` is used above.

---

## 6. Tiles: three things to change

`web/tiles/` now runs z10 to z17, 2,388 tiles, 22.2 MB.

**a. Lower the layer's floor.** Anchor: `minZoom: 12, maxNativeZoom: 17`.

```js
minZoom: 10,   // was 12
```

**b. Widen `TILE_CONTEXT`, or the new tiles are never requested.** Anchor:
`const TILE_CONTEXT = L.latLngBounds([[9.55, -82.88], [9.75, -82.57]]);`
That box is the layer's `bounds`, so Leaflet will not ask for a tile outside it
however many are on disk.

```js
const TILE_CONTEXT = L.latLngBounds([[9.0570, -83.1617], [10.2448, -82.2869]]);
```

Leave `TILE_FULL` and the `maxBounds` built from it alone. The pan limit stays on
the coast box for the reason the existing comment gives.

**c. THIS IS THE ONE THAT ACTUALLY FIXES THE NAVY, and it was not a missing zoom
level.** `fitCoast()` sets `minZoom` to whatever fits 16.66 km of coast in the
viewport, so a 390 x 844 phone lands at about zoom 11.8 and Leaflet requests LEVEL
12. At that zoom a pixel is 43 m, so 844 px of phone is 36 km of ground, and the
z12 box was 22 km tall: the opening view ran out of imagery about 7 km above and
below the coast on every portrait phone. z12's box is now 48 x 58 km, which covers
it. z11 and z10 would never have been requested at all at that floor; they are
insurance for a sub-313 px viewport, for the transient zoom during a pinch, and
for the day somebody sets a fixed floor instead of a derived one.

So if you keep the derived floor, (a) and (b) are all that is needed and z10/z11
sit there unused but precached. If you set a fixed `minZoom: 11`, they come alive.

Precache tiers: CRITICAL is now z11 to z13, 155 tiles, 1,596 KB (was z12 to z13,
52 tiles, 455 KB) and is ON the 1.6 MB line rather than under it; `sw.js` carries
the one line lever for bringing it down. OPTIONAL is z10, z14, z15: 360 tiles,
3.5 MB. The boxes are measured by `tile_demand.py` in this folder, which ports
Leaflet's flyTo path and GridLayer._update; rerun it after any change to
`fitCoast()`, `flyClear()`, the dock height or the sheet stops. Rerun
`python tools/build_tiles.py` after any change to `web/tiles/` and bump `CACHE` in
`sw.js`; the lists between the `TILES:BEGIN` / `TILES:END` markers are generated.

---

## 7. Fonts

`web/fonts/AtkinsonHyperlegible-Regular.woff2` and `-Bold.woff2` are already on
disk and are already named in the sw CRITICAL list. The names are a contract: if
you rename them, change `web/sw.js` too. A missing one degrades to the system
stack and logs one failure rather than killing the install.

---

## 8. Checking it

```
node <scratchpad>/check_geometry.js          # 90 assertions, no browser needed
cp  <scratchpad>/geomcheck.html web/_geomcheck.html
#   open http://127.0.0.1:5173/_geomcheck.html
rm  web/_geomcheck.html                      # web/ is deployed whole
```

`geomcheck.html` draws all five smoothed zones, the labels and the rip arrows over
the tile pyramid with the real `CGGeom` output, and prints the weights, dash
arrays, ground widths and collision count at the current zoom.
