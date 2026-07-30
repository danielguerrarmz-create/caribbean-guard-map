"""Solve the georeference from the two shoreline profiles.

Model: ref_y(x) = s * base_y((x - dx)/s) + c + m*(x - dx)
  s   scale, base ground width relative to the reference
  dx  horizontal placement
  c   vertical placement
  m   linear trend, which is the rotation between the two

c and m are solved in closed form for every (s, dx), so only two parameters are
actually searched. The loss is the MEDIAN absolute residual, not RMS, because
both profiles have spikes where river mouths and reef break the simple
land/water rule and a squared loss would chase them.
"""
import json, math, os
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:\Users\danie\Downloads\caribbean-guard-cuts\Complete Mapping.jpg"

rp = np.load(os.path.join(HERE, "prof_ref.npy"))
bp = np.load(os.path.join(HERE, "prof_base.npy"))
N = len(rp)

# geometry of the reference mosaic, exact by construction
Z, TS = 17, 256
import glob
files = glob.glob(os.path.join(HERE, "tilecache", f"{Z}_*.jpg"))
xs = sorted({int(os.path.basename(f).split("_")[1]) for f in files})
ys = sorted({int(os.path.basename(f).split("_")[2].split(".")[0]) for f in files})
TX0, TY0 = xs[0], ys[0]
RW, RH = (xs[-1]-xs[0]+1)*TS, (ys[-1]-ys[0]+1)*TS


def tile2deg(x, y, z):
    n = 2 ** z
    return (math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))),
            x / n * 360.0 - 180.0)


NLAT, WLON = tile2deg(TX0, TY0, Z)
MPP_FULL = 156543.03392 * math.cos(math.radians(NLAT)) / (2 ** Z)   # m per ref full px
SCALE_R = N / RW                       # profile samples per ref full px
MPP = MPP_FULL / SCALE_R               # metres per profile sample
REF_KM = RW * MPP_FULL / 1000.0
print(f"reference spans {REF_KM:.2f} km, {MPP:.2f} m per profile sample")

bimg = Image.open(BASE); BW, BH = bimg.size
# the base profile was sampled at 1600 across BW, and its y units are rows of a
# 1600-wide render, so y and x share the same scale in both profiles
BASE_ASPECT = BH / BW

rp_v = np.isfinite(rp)
bp_v = np.isfinite(bp)


def evaluate(s, dx):
    """s: base width in profile samples. dx: left edge in profile samples."""
    if s < 200 or dx < -s * 0.2 or dx + s > N + s * 0.2:
        return None
    xs_ref = np.arange(N)
    u = (xs_ref - dx) / s * (len(bp) - 1)          # position within base profile
    ok = (u >= 0) & (u <= len(bp) - 1) & rp_v
    if ok.sum() < 250:
        return None
    ui = u[ok]
    lo = np.floor(ui).astype(int); hi = np.minimum(lo + 1, len(bp) - 1)
    w = ui - lo
    valid = bp_v[lo] & bp_v[hi]
    if valid.sum() < 250:
        return None
    yb = (bp[lo] * (1 - w) + bp[hi] * w)[valid]
    yr = rp[ok][valid]
    xr = xs_ref[ok][valid].astype(float)
    # base y is in rows of a 1600-wide render; rescale to the candidate width
    yb = yb * (s / len(bp))
    A = np.column_stack([np.ones_like(xr), xr - dx])
    coef, *_ = np.linalg.lstsq(A, yr - yb, rcond=None)
    resid = yr - yb - A @ coef
    return float(np.median(np.abs(resid))), coef, valid.sum(), ok


best = None
prof_curve = {}
for km in np.arange(8.0, 22.01, 0.1):
    s = km / REF_KM * N
    for dx in np.arange(-0.15 * N, N * 0.35, 3.0):
        r = evaluate(s, dx)
        if r is None:
            continue
        err = r[0] * MPP
        prof_curve[round(km, 1)] = min(prof_curve.get(round(km, 1), 1e9), err)
        if best is None or err < best[0]:
            best = (err, km, dx, s, r[1], r[2])

err, km, dx, s, coef, npts = best
rot = math.degrees(math.atan(coef[1]))
print(f"\nBEST span {km:.2f} km, median shoreline residual {err:.1f} m, "
      f"{npts} columns compared, rotation {rot:+.2f} deg")

ks = sorted(prof_curve)
print("\nresidual (m) vs assumed span (km):")
for i in range(0, len(ks), 6):
    print("  " + "  ".join(f"{k:.0f}:{prof_curve[k]:.0f}" for k in ks[i:i+6]))
interior = ks[0] < km < ks[-1]
print(f"minimum is {'interior, good' if interior else 'AT SWEEP EDGE, suspect'}")

# ---- corners ----
# base image maps to reference profile coords: x_ref = dx + (px/BW)*s
# y_ref  = c + m*(x_ref-dx) + (py/BW)*s        (same scale in x and y)
c, m = coef
def base_to_ref(px, py):
    xr = dx + (px / BW) * s
    yr = c + m * (xr - dx) + (py / BW) * s
    return xr / SCALE_R, yr / SCALE_R          # -> reference FULL px

lls = []
for px, py in [(0, 0), (BW, 0), (BW, BH), (0, BH)]:
    fx, fy = base_to_ref(px, py)
    lls.append(tile2deg(TX0 + fx / TS, TY0 + fy / TS, Z))
for nm, (la, lo) in zip(["NW", "NE", "SE", "SW"], lls):
    print(f"  {nm}  {la:.6f}, {lo:.6f}")

lats = [p[0] for p in lls]; lons = [p[1] for p in lls]
span_m = (max(lons)-min(lons)) * 111320 * math.cos(math.radians(np.mean(lats)))
print(f"\ncoverage {span_m/1000:.2f} km east-west, {span_m/BW*100:.1f} cm per source px")
print(f"IMG_BOUNDS = [[{min(lats):.6f}, {min(lons):.6f}], [{max(lats):.6f}, {max(lons):.6f}]];")

json.dump({"corners": dict(zip(["NW", "NE", "SE", "SW"], lls)),
           "rotation_deg": rot, "median_shoreline_residual_m": err,
           "columns_compared": int(npts),
           "bounds": [[min(lats), min(lons)], [max(lats), max(lons)]],
           "span_km": span_m/1000, "cm_per_px": span_m/BW*100,
           "zoom": Z, "ref_origin_tile": [TX0, TY0], "interior_minimum": bool(interior)},
          open(os.path.join(HERE, "georef.json"), "w"), indent=2)
print("\nwrote georef.json")
