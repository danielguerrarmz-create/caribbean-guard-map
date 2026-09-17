"""Which tiles can web/index.html actually ask for?

Ports the parts of Leaflet 1.x that decide it -- project/unproject, getBoundsZoom,
_getBoundsCenterZoom, the van Wijk flyTo path, and GridLayer._update -- and runs
the app's own scenarios through them. Answers a coverage question by measurement
rather than by a margin somebody liked the look of.

THE PART THAT MATTERS: the tile layer is updateWhenIdle:false, so GridLayer
updates on every `move` and `zoom` frame, not just at the end. flyTo uses van
Wijk's smooth path, which ZOOMS OUT IN THE MIDDLE of a long flight. So a fly from
the whole-coast view to one beach passes through a low zoom with the centre
somewhere off the coast, and requests tiles there. Endpoint analysis misses it
entirely.
"""
import json
import math
import os

R = 6378137.0
ROOT = "C:/Users/danie/caribbean-guard"


# ---------- Leaflet CRS.EPSG3857 ----------
def project(lat, lon, zoom):
    """LatLng -> pixel coordinates at `zoom`, exactly as L.Map.project does."""
    d = math.pi / 180
    maxlat = 85.0511287798
    lat = max(min(maxlat, lat), -maxlat)
    sin = math.sin(lat * d)
    x = R * lon * d
    y = R * math.log((1 + sin) / (1 - sin)) / 2
    scale = 256 * 2 ** zoom
    # transformation (a,b,c,d) = (0.5/(pi*R), 0.5, -0.5/(pi*R), 0.5)
    a = 0.5 / (math.pi * R)
    return (scale * (a * x + 0.5), scale * (-a * y + 0.5))


def unproject(px, py, zoom):
    scale = 256 * 2 ** zoom
    a = 0.5 / (math.pi * R)
    x = (px / scale - 0.5) / a
    y = (py / scale - 0.5) / -a
    d = 180 / math.pi
    return (2 * math.atan(math.exp(y / R)) * d - 90, x * d / R)


def scale_zoom(scale, from_zoom):
    return from_zoom + math.log(scale) / math.log(2)


# ---------- the app's own constants, read from index.html ----------
IMG_BOUNDS = ((9.621462, -82.790863), (9.671534, -82.639053))   # S,W  N,E
TILE_FULL = ((9.61429, -82.801208), (9.687398, -82.6474))
MAXZOOM, ZOOMSNAP = 18, 0.25


def pad_bounds(b, r):
    (s, w), (n, e) = b
    dy, dx = (n - s) * r, (e - w) * r
    return ((s - dy, w - dx), (n + dy, e + dx))


def bounds_zoom(b, size_x, size_y, pad_x, pad_y, minz, maxz=MAXZOOM, zoom=0):
    """L.Map.getBoundsZoom(bounds, inside=false, padding)."""
    (s, w), (n, e) = b
    nw = project(n, w, zoom)
    se = project(s, e, zoom)
    bw, bh = abs(se[0] - nw[0]), abs(se[1] - nw[1])
    sx, sy = size_x - pad_x, size_y - pad_y
    if bw <= 0 or bh <= 0:
        return maxz
    # Padding wider than the viewport. Leaflet takes log of a negative scale and
    # gets NaN, which clamps to minZoom in the Math.max below; do the same rather
    # than pretend this is a view somebody can reach.
    if sx <= 0 or sy <= 0:
        return minz
    z = scale_zoom(min(sx / bw, sy / bh), zoom)
    z = round(z / (ZOOMSNAP / 100)) * (ZOOMSNAP / 100)
    z = math.floor(z / ZOOMSNAP) * ZOOMSNAP
    return max(minz, min(maxz, z))


def bounds_center_zoom(b, size_x, size_y, ptl, pbr, max_zoom, minz):
    """L.Map._getBoundsCenterZoom -- what flyToBounds flies to."""
    z = bounds_zoom(b, size_x, size_y, ptl[0] + pbr[0], ptl[1] + pbr[1], minz)
    z = min(max_zoom, z)
    off = ((pbr[0] - ptl[0]) / 2.0, (pbr[1] - ptl[1]) / 2.0)
    (s, w), (n, e) = b
    sw = project(s, w, z)
    ne = project(n, e, z)
    cx = (sw[0] + ne[0]) / 2 + off[0]
    cy = (sw[1] + ne[1]) / 2 + off[1]
    return unproject(cx, cy, z), z


def limit_center(lat, lon, zoom, mb, size_x, size_y):
    """L.Map._limitCenter -- the maxBounds clamp that setView applies."""
    if mb is None:
        return lat, lon
    c = project(lat, lon, zoom)
    hx, hy = size_x / 2.0, size_y / 2.0
    pmin = (c[0] - hx, c[1] - hy)
    pmax = (c[0] + hx, c[1] + hy)
    (s, w), (n, e) = mb
    b1 = project(n, e, zoom)
    b2 = project(s, w, zoom)
    bmin = (min(b1[0], b2[0]), min(b1[1], b2[1]))
    bmax = (max(b1[0], b2[0]), max(b1[1], b2[1]))

    def rebound(left, right):
        if left + right > 0:
            return round((left - right) / 2.0)
        return max(0, math.ceil(left)) - max(0, math.floor(right))

    dx = rebound(bmin[0] - pmin[0], -(bmax[0] - pmax[0]))
    dy = rebound(bmin[1] - pmin[1], -(bmax[1] - pmax[1]))
    return unproject(c[0] + dx, c[1] + dy, zoom)


def fly_path(c0, z0, c1, z1, size_x, size_y, frames=400):
    """L.Map.flyTo -- van Wijk smooth zoom. Yields (lat, lon, zoom) per frame."""
    frm = project(c0[0], c0[1], z0)
    to = project(c1[0], c1[1], z0)
    w0 = max(size_x, size_y)
    w1 = w0 * (2 ** (z0 - z1))          # getZoomScale(startZoom, targetZoom)
    u1 = math.hypot(to[0] - frm[0], to[1] - frm[1]) or 1.0
    rho = 1.42
    rho2 = rho * rho

    def r(i):
        s1 = -1 if i else 1
        s2 = w1 if i else w0
        t1 = w1 * w1 - w0 * w0 + s1 * rho2 * rho2 * u1 * u1
        b1 = 2 * s2 * rho2 * u1
        b = t1 / b1
        sq = math.sqrt(b * b + 1) - b
        return -18.0 if sq < 1e-9 else math.log(sq)

    r0 = r(0)
    cosh = math.cosh
    sinh = math.sinh
    tanh = math.tanh

    def w(s):
        return w0 * (cosh(r0) / cosh(r0 + rho * s))

    def u(s):
        return w0 * (cosh(r0) * tanh(r0 + rho * s) - sinh(r0)) / rho2

    S = (r(1) - r0) / rho
    out = []
    for i in range(frames + 1):
        t = i / frames
        s = (1 - (1 - t) ** 1.5) * S       # easeOut
        k = u(s) / u1
        px = frm[0] + (to[0] - frm[0]) * k
        py = frm[1] + (to[1] - frm[1]) * k
        z = scale_zoom(w0 / w(s), z0)
        lat, lon = unproject(px, py, z0)
        out.append((lat, lon, z))
    out.append((c1[0], c1[1], z1))
    return out


def tiles_for(lat, lon, zoom, size_x, size_y, layer_min=10, layer_max=18,
              native_max=17):
    """L.GridLayer._update -- the tile range one frame actually requests."""
    # JS Math.round rounds .5 UP; Python's round() is banker's rounding and sends
    # 16.5 to 16 instead of 17. zoomSnap is 0.25, so half-integer zooms are common
    # and this is the difference between simulating z17 demand and missing it.
    tz = math.floor(zoom + 0.5)
    tz = min(max(tz, layer_min), layer_max)
    tz = min(tz, native_max)                 # maxNativeZoom
    if tz < layer_min:
        return []
    scale = 2 ** (zoom - tz)
    cx, cy = project(lat, lon, tz)
    cx, cy = math.floor(cx), math.floor(cy)
    hx, hy = size_x / (scale * 2), size_y / (scale * 2)
    x0 = math.floor((cx - hx) / 256)
    x1 = math.ceil((cx + hx) / 256) - 1
    y0 = math.floor((cy - hy) / 256)
    y1 = math.ceil((cy + hy) / 256) - 1
    return [(tz, x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]


# ---------- the app's scenarios ----------
def zones():
    z = json.load(open(os.path.join(ROOT, "web/data/zones-geometry.json")))["zones"]
    out = {}
    for k, line in z.items():
        lats = [p[0] for p in line]
        lons = [p[1] for p in line]
        out[k] = ((min(lats), min(lons)), (max(lats), max(lons)))
    return out


def posts():
    gj = json.load(open(os.path.join(ROOT, "web/data/cg-hazards.geojson")))
    return [(f["geometry"]["coordinates"][1], f["geometry"]["coordinates"][0])
            for f in gj["features"]
            if f["properties"].get("kind") == "rescue_station"]


def run():
    want = set()
    BB = IMG_BOUNDS
    MB_FLY = pad_bounds(TILE_FULL, 0.08)     # fitCoast's setMaxBounds
    ZONES = zones()

    # Viewports, and the chrome heights swept rather than assumed: the dock and
    # the sheet are content sized and workstream B is still moving them.
    viewports = [(390, 844), (360, 740), (412, 915), (1280, 800), (1440, 900)]
    dock_hs = [96, 160, 220, 300]
    sheet_fracs = [0.33, 0.70, 1.0]          # STOPS: peek, half, full

    for (sx, sy) in viewports:
        desktop = sx >= 820
        for dock in dock_hs:
            # ---- fitCoast() ----
            top = 64 + 8
            if desktop:
                bot, left, right = 16, 360 + 16, 0 + 16
            else:
                bot, left, right = dock + 8, 0, 0
            capY = sy * 0.6
            if top + bot > capY:
                k = capY / (top + bot)
                top, bot = math.floor(top * k), math.floor(bot * k)
            padx = min(8, sx * 0.3)
            zfit = bounds_zoom(BB, sx, sy, 2 * padx, top + bot, 0)
            cfit = limit_center(*[sum(x) / 2 for x in zip(*BB)], zfit, MB_FLY, sx, sy)
            for z in [zfit, zfit + 0.25, zfit + 0.5]:
                want.update(tiles_for(cfit[0], cfit[1], z, sx, sy, layer_min=10))

            # ---- every flyClear the app can run ----
            targets = []
            for b in ZONES.values():
                targets.append((pad_bounds(b, 0.55), 17))
            for (plat, plon) in posts():
                targets.append((pad_bounds(((plat, plon), (plat, plon)), 0.002), 16.5))
            for sf in sheet_fracs:
                sheetH = int(sy * sf)
                if desktop:
                    ptl = (360 + 24, 64 + 16)
                    pbr = (400 + 24, 32)
                else:
                    ptl = (24, 64 + 16)
                    pbr = (24, sheetH + 16)
                for (tb, mz) in targets:
                    ctr, zt = bounds_center_zoom(tb, sx, sy, ptl, pbr, mz, zfit)
                    for (lat, lon, z) in fly_path(cfit, zfit, ctr, zt, sx, sy, frames=160):
                        if z < zfit - 0.01:
                            z = zfit          # minZoom clamps the camera
                        want.update(tiles_for(lat, lon, z, sx, sy, layer_min=10))
                    # and the reverse flight, beach back to the coast, and
                    # beach to beach, which is what the card strip does
                    for (tb2, mz2) in targets:
                        c2, z2 = bounds_center_zoom(tb2, sx, sy, ptl, pbr, mz2, zfit)
                        for (lat, lon, z) in fly_path(ctr, zt, c2, z2, sx, sy, frames=60):
                            if z < zfit - 0.01:
                                z = zfit
                            want.update(tiles_for(lat, lon, z, sx, sy, layer_min=10))
    return want


def on_disk():
    have = set()
    base = os.path.join(ROOT, "web", "tiles")
    for z in os.listdir(base):
        if not z.isdigit():
            continue
        for x in os.listdir(os.path.join(base, z)):
            for f in os.listdir(os.path.join(base, z, x)):
                have.add((int(z), int(x), int(f[:-4])))
    return have


if __name__ == "__main__":
    want = run()
    have = on_disk()
    missing = sorted(want - have)
    by_z = {}
    for z, x, y in missing:
        by_z.setdefault(z, []).append((x, y))
    print(f"requestable: {len(want)} tiles   on disk: {len(have)}   MISSING: {len(missing)}")
    for z in sorted(by_z):
        xs = [t[0] for t in by_z[z]]
        ys = [t[1] for t in by_z[z]]
        print(f"  z{z}: {len(by_z[z]):5d} missing   x {min(xs)}..{max(xs)}   y {min(ys)}..{max(ys)}")
    # the box each level needs, as S,W,N,E
    print("\nbox each level must cover (S, W, N, E):")
    for z in sorted({t[0] for t in want}):
        ts = [t for t in want if t[0] == z]
        x0, x1 = min(t[1] for t in ts), max(t[1] for t in ts)
        y0, y1 = min(t[2] for t in ts), max(t[2] for t in ts)
        n, w = unproject(x0 * 256, y0 * 256, z)
        s, e = unproject((x1 + 1) * 256, (y1 + 1) * 256, z)
        print(f"  z{z}: x {x0}..{x1}  y {y0}..{y1}  "
              f"({s:.4f}, {w:.4f}, {n:.4f}, {e:.4f})  {(x1-x0+1)*(y1-y0+1)} tiles")
