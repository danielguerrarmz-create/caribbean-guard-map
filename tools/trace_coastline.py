"""Trace the true coastline per zone, headlands and all.

WHY THIS EXISTS. `redraw_zones.py` finds the waterline with a per-column scan:

    for x in range(RW):
        col = np.nonzero(land[:, x])[0]
        shore_y[x] = col[0]          # first land pixel from the top

One y for every x. That forces the coastline to be a FUNCTION OF LONGITUDE, and a
coast is not one. Wherever the shore doubles back -- every headland, every point,
every bay mouth on this coast -- a function can keep only the northernmost
crossing and must throw the rest away. The output is provably a function: the
1,434 points in `shoreline.json` are strictly monotonic in longitude at a uniform
11.7 m step, which no real coastline is.

Two more things compound it. An 81-column box smooth (`k = 81`) averages the line
across roughly 95 m of longitude, rounding the corner off any headland that
survived the scan. And the 30 m seaward nudge is applied as `ys[i] - SEAWARD_M`,
straight north in pixels rather than along the local normal, so on a shore facing
any direction but due north it pushes partly ALONG the beach instead of off it.

None of this showed on the slippy map, because the map drew the 9-point decimated
version at low zoom, where a 250 m chord and a rounded-off headland look
identical. It is plainly visible the moment the line is drawn on the base image
at native resolution: at Playa Chiquita it runs straight through the point,
across the jungle and the buildings, and misses the bay entirely.

WHAT THIS DOES INSTEAD. Take the sea/land boundary as a contour, which is free to
double back, and offset each point along the LOCAL normal, choosing the side the
water is actually on. The water mask itself is carried over unchanged: the flood
fill from the top edge is a good idea and was never the broken part.

AND IT CONTOURS ONE ZONE AT A TIME. The mosaic is a rectangle laid over a
diagonal coast, so 10.9% of it is unfetched black in the far corners, and
`water_mask` reads black as sea (`v < 60`). Contouring the whole mosaic threads
the boundary around every hole: splitting that on no-data produced 21 overlapping
runs totalling 45 km against a 16.7 km coast, nine of them piled on one hole at
the west end. Every tile ALONG THE SHORE is present (72 of 72 shoreline samples
hit a cached tile), so cropping to a zone removes the holes from the picture
instead of reasoning around them, and makes each zone's line stop at its own edge.

Output: `tools/coastline.json`, one dense west-to-east polyline per zone.
"""
import glob
import json
import math
import os
import re

import cv2
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
Z, TS = 17, 256
SEAWARD_M = 30      # off the sand, into the water the line describes
SMOOTH = 9          # points, ALONG THE CONTOUR -- never along longitude
MIN_RUN = 200       # contour points (~235 m); shorter is surf noise, not coast
STEP_M = 8          # resample interval
MARGIN_M = 120      # crop margin either side of a zone


def tile2deg(x, y, z):
    n = 2 ** z
    return (math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))),
            x / n * 360.0 - 180.0)


def deg2tile(lat, lon, z):
    n = 2 ** z
    return ((lon + 180.0) / 360.0 * n,
            (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n)


def load_ref():
    files = glob.glob(os.path.join(HERE, "tilecache", f"{Z}_*.jpg"))
    if not files:
        raise SystemExit("no tile cache; run tools/georef2.py first")
    xs = sorted({int(os.path.basename(f).split("_")[1]) for f in files})
    ys = sorted({int(os.path.basename(f).split("_")[2].split(".")[0]) for f in files})
    x0, y0 = xs[0], ys[0]
    mos = Image.new("RGB", ((xs[-1] - x0 + 1) * TS, (ys[-1] - y0 + 1) * TS))
    for f in files:
        _, x, y = os.path.basename(f).replace(".jpg", "").split("_")
        try:
            mos.paste(Image.open(f).convert("RGB"), ((int(x) - x0) * TS, (int(y) - y0) * TS))
        except Exception:
            pass
    return np.asarray(mos), x0, y0


def water_mask(rgb):
    """Sea by SATURATION and hue. Flood filled from the top edge.

    THE OLD TEST CLASSIFIED THE JUNGLE AS SEA. `redraw_zones.py` uses

        seaish = ((h > 70) & (h < 115) & (v < 190)) | (v < 60)

    and that trailing `| (v < 60)` calls every dark pixel water. Shadowed rain
    forest is dark. The fill then leaks off the beach into the canopy and keeps
    going: over the Playa Chiquita window the mask came out 88.7% sea, with the
    whole forest flooded and only bright sand and rooftops left standing as land.

    It never broke `redraw_zones.py` because a per-column scan takes the first
    LAND pixel from the top, and the first bright thing below the water is the
    sand. The beach rescued a mask that was wrong about everything behind it. A
    contour has no such luck: it follows the true boundary of the region, and the
    true boundary of that region runs through the trees.

    Measured at Punta Uva and Playa Chiquita, 50 px patches, 5th to 95th centile:

        open sea       h  90-99   s 193-245   v 50-77
        reef shallow   h  99-102  s 206-239   v 59-70
        shallow inshore h 69-92   s  49-228   v 43-86
        surf           h  93      s 202-233   v 58-67
        dark jungle    h  20-66   s   7-190   v 32-116
        beach sand     h  26-70   s  44-170   v 26-145

    HUE is the discriminator, and it is the only one that separates every class:
    water of any depth sits at 69 and above, land at 70 and below. Saturation
    looked decisive on deep water alone (193 up against 190 down) but the pale
    inshore shelf runs down to 49, and keying on it put the line out at the reef
    edge instead of on the sand. Value does not separate them at all, which is
    why the old `| (v < 60)` flooded the forest.

    The saturation floor is only there to reject near-grey rooftops, whose hue is
    unstable. Anything inland that still slips through is unreachable anyway: the
    fill starts at the top edge and only sea connects to open ocean.
    """
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h, s = hsv[..., 0].astype(int), hsv[..., 1].astype(int)
    seaish = (h >= 72) & (h <= 118) & (s >= 45)
    seaish = cv2.morphologyEx(seaish.astype(np.uint8), cv2.MORPH_CLOSE,
                              np.ones((9, 9), np.uint8))
    H, W = seaish.shape
    ff = np.zeros((H + 2, W + 2), np.uint8)
    m = seaish.copy()
    for x in range(0, W, 40):
        if m[0, x]:
            cv2.floodFill(m, ff, (x, 0), 2)
    return (m == 2).astype(np.uint8)


def zone_windows():
    """The five zone spans, read from redraw_zones.py rather than copied.

    Duplicating them is how the sheet and the map drift apart, and that list is
    already the single place this coast is divided.
    """
    src = open(os.path.join(HERE, "redraw_zones.py"), encoding="utf-8").read()
    block = src[src.index("ZONES = ["):]
    block = block[: block.index("]") + 1]
    return [(m.group(1), float(m.group(2)), float(m.group(3)))
            for m in re.finditer(r'\("([^"]+)",\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\)', block)]


def trace_window(sea, tx0, mpp, wlon, elon):
    """Longest sea/land boundary run inside one zone's longitude window."""
    RH, RW = sea.shape
    pad = int(MARGIN_M / mpp)
    lon_to_px = lambda lon: (deg2tile(9.645, lon, Z)[0] - tx0) * TS
    x0 = int(max(0, min(lon_to_px(wlon), lon_to_px(elon)) - pad))
    x1 = int(min(RW, max(lon_to_px(wlon), lon_to_px(elon)) + pad))
    sub = sea[:, x0:x1]

    cont, _ = cv2.findContours(sub, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not cont:
        return None
    c = max(cont, key=cv2.contourArea).reshape(-1, 2).astype(np.float64)

    # Border-touching points separate sea from the edge of the crop, not land.
    b = 3
    H, W = sub.shape
    on_edge = ((c[:, 0] < b) | (c[:, 0] > W - 1 - b)
               | (c[:, 1] < b) | (c[:, 1] > H - 1 - b))
    N = len(c)
    best, run = [], []
    for i in range(2 * N):
        if len(run) > N:
            break
        if not on_edge[i % N]:
            run.append(i % N)
            if len(run) > len(best):
                best = list(run)
        else:
            run = []
    if len(best) < MIN_RUN:
        return None
    line = c[best].copy()
    line[:, 0] += x0
    return line


def dress(line, sea, mpp, tx0, ty0):
    """Smooth along the contour, resample evenly, offset along the local normal."""
    RH, RW = sea.shape

    # A 9-point window at ~1.2 m per point is about 11 m of coast: enough to
    # settle pixel noise at the surf line, far too short to erase a headland.
    k = SMOOTH
    padded = np.vstack([line[:1].repeat(k, 0), line, line[-1:].repeat(k, 0)])
    ker = np.ones(k) / k
    sm = np.stack([np.convolve(padded[:, 0], ker, "same"),
                   np.convolve(padded[:, 1], ker, "same")], 1)[k:-k]

    seg = np.hypot(*(sm[1:] - sm[:-1]).T)
    dist = np.concatenate([[0], np.cumsum(seg)])
    if dist[-1] < 1:
        return None
    want = np.arange(0, dist[-1], STEP_M / mpp)
    rs = np.stack([np.interp(want, dist, sm[:, 0]),
                   np.interp(want, dist, sm[:, 1])], 1)
    if len(rs) < 3:
        return None

    # Offset along the LOCAL normal, toward whichever side the water is on. The
    # old code subtracted the nudge from y alone, which is due north, and due
    # north is the seaward direction only on a shore that happens to face north.
    tang = np.gradient(rs, axis=0)
    tl = np.hypot(tang[:, 0], tang[:, 1])
    tl[tl == 0] = 1
    nx, ny = -tang[:, 1] / tl, tang[:, 0] / tl
    probe = np.clip(np.round(rs + np.stack([nx, ny], 1) * 6), 0,
                    [RW - 1, RH - 1]).astype(int)
    sign = np.where(sea[probe[:, 1], probe[:, 0]] > 0, 1.0, -1.0)
    out = rs + np.stack([nx * sign, ny * sign], 1) * (SEAWARD_M / mpp)

    pts = [[round(la, 6), round(lo, 6)]
           for la, lo in (tile2deg(tx0 + x / TS, ty0 + y / TS, Z) for x, y in out)]
    if pts[0][1] > pts[-1][1]:
        pts.reverse()
    return pts


def main():
    ref, tx0, ty0 = load_ref()
    RH, RW = ref.shape[:2]
    nlat, _ = tile2deg(tx0, ty0, Z)
    mpp = 156543.03392 * math.cos(math.radians(nlat)) / (2 ** Z)
    print(f"reference {RW}x{RH}, {mpp:.3f} m/px")

    sea = water_mask(ref)
    print(f"water is {sea.mean()*100:.1f}% of the mosaic")

    # CLOSE bridges surf and sandbars so the sea stays one region. OPEN then
    # removes thin intrusions of sea into the land: river mouths, drainage cuts
    # and dark wet channels a few metres across. Without it the contour runs up
    # each one and back, and those hairs are what pushed Playa Chiquita to 5.13 km
    # of traced coast over 2.49 km of span. A disk of radius 7 is 16 m across at
    # 1.18 m/px, comfortably under the 30 m the line is offset seaward anyway, so
    # it cannot round off anything the sheet draws at this scale.
    disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    sea = cv2.morphologyEx(sea, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    sea = cv2.morphologyEx(sea, cv2.MORPH_OPEN, disk)

    out, total_backs = {}, 0
    for zid, w, e in zone_windows():
        line = trace_window(sea, tx0, mpp, w, e)
        if line is None:
            print(f"  {zid:14} no coast run found")
            continue
        pts = dress(line, sea, mpp, tx0, ty0)
        if pts is None:
            print(f"  {zid:14} run too short to dress")
            continue
        lons = [p[1] for p in pts]
        backs = sum(1 for a, b in zip(lons, lons[1:]) if b < a)
        total_backs += backs
        length = sum(math.hypot((b[1] - a[1]) * 111320 * math.cos(math.radians(9.645)),
                                (b[0] - a[0]) * 110570) for a, b in zip(pts, pts[1:]))
        span = (max(lons) - min(lons)) * 111320 * math.cos(math.radians(9.645))
        out[zid] = pts
        print(f"  {zid:14} {len(pts):4d} pts  {length/1000:.2f} km of coast over "
              f"{span/1000:.2f} km of span  {backs:3d} reversals")

    print(f"\n{total_backs} longitude reversals in total. Each one is a place the "
          f"per-column scan\nhad to delete part of the coast to stay a function.")
    path = os.path.join(HERE, "coastline.json")
    with open(path, "w") as f:
        json.dump({"seaward_m": SEAWARD_M, "step_m": STEP_M, "zones": out}, f)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
