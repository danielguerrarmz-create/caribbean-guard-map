"""Measure how far off the georeference still is, in metres, at each landmark.

validate.py proves the transform is roughly right by eye. This puts a number on
it. For each check point it crops the georeferenced base and searches for that
crop inside a larger Bing window. The offset of the correlation peak is the
residual error at that point.

Correlation is used here in the one situation where it is trustworthy: real
greyscale imagery with plenty of texture, inside a window small enough that
there is only one plausible answer, with the peak checked against the runner-up.
It is NOT trusted on sparse edge maps, which is what produced spurious 1.0
scores earlier in this project.

A residual that grows towards the ends means the hand stitch has scale error and
one global transform is not enough.
"""
import glob, json, math, os
import numpy as np, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:\Users\danie\Downloads\caribbean-guard-cuts\Complete Mapping.jpg"
Z, TS = 17, 256

# Sample the whole coast, not three hand-picked spots. Two weak landmarks at the
# east end could mean the transform drifts there, or could just mean those two
# crops happened to be featureless water. A dense sweep separates the two: a real
# drift shows up as a trend across many points, bad luck does not.
_W, _E = (9.6553, -82.7540), (9.6320, -82.6520)
CHECKS = [(f"p{i:02d} lon {_W[1] + (_E[1]-_W[1])*i/13:.4f}",
           _W[0] + (_E[0]-_W[0]) * i / 13,
           _W[1] + (_E[1]-_W[1]) * i / 13) for i in range(14)]
HALF_M = 600          # half-size of the base crop
# Wide enough that the answer is never the window edge. A residual equal to
# SEARCH_M is not a measurement, it is a clamp, and reading it as a measurement
# is how the earlier sweeps in this project produced confident nonsense.
SEARCH_M = 1500


def deg2tile(lat, lon, z):
    n = 2 ** z
    return ((lon + 180.0) / 360.0 * n,
            (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n)


def load_ref():
    files = glob.glob(os.path.join(HERE, "tilecache", f"{Z}_*.jpg"))
    xs = sorted({int(os.path.basename(f).split("_")[1]) for f in files})
    ys = sorted({int(os.path.basename(f).split("_")[2].split(".")[0]) for f in files})
    x0, y0 = xs[0], ys[0]
    mos = Image.new("RGB", ((xs[-1]-x0+1)*TS, (ys[-1]-y0+1)*TS))
    for f in files:
        _, x, y = os.path.basename(f).replace(".jpg", "").split("_")
        try:
            mos.paste(Image.open(f).convert("RGB"), ((int(x)-x0)*TS, (int(y)-y0)*TS))
        except Exception:
            pass
    return mos, x0, y0


def prep(a):
    g = cv2.cvtColor(np.asarray(a), cv2.COLOR_RGB2GRAY)
    return cv2.createCLAHE(3.0, (8, 8)).apply(g).astype(np.float32)


def main():
    gj = json.load(open(os.path.join(HERE, "georef.json")))
    c = gj["corners"]
    NW, NE, SE, SW = (np.array(c[k], float) for k in ["NW", "NE", "SE", "SW"])

    base = Image.open(BASE).convert("RGB")
    BW, BH = base.size
    base_np = np.asarray(base)
    ref, tx0, ty0 = load_ref()
    ref_np = np.asarray(ref)

    nlat = NW[0]
    MPP = 156543.03392 * math.cos(math.radians(nlat)) / (2 ** Z)

    def base_px_to_ll(px, py):
        u, v = px / BW, py / BH
        top = NW + (NE - NW) * u
        bot = SW + (SE - SW) * u
        return top + (bot - top) * v

    def ll_to_base_px(lat, lon):
        target = np.array([lat, lon])
        p = np.array([BW / 2.0, BH / 2.0])
        for _ in range(40):
            f = base_px_to_ll(*p) - target
            e = 1.0
            J = np.column_stack([
                (base_px_to_ll(p[0]+e, p[1]) - base_px_to_ll(p[0]-e, p[1])) / (2*e),
                (base_px_to_ll(p[0], p[1]+e) - base_px_to_ll(p[0], p[1]-e)) / (2*e)])
            try:
                p = p - np.linalg.solve(J, f)
            except np.linalg.LinAlgError:
                break
        return p

    mlat = 111320.0
    rows = []
    for name, la, lo in CHECKS:
        dlat = HALF_M / mlat
        dlon = HALF_M / (mlat * math.cos(math.radians(la)))

        side = int(2 * HALF_M / MPP)          # crop size in reference pixels
        pts = np.array([ll_to_base_px(la+dlat, lo-dlon),
                        ll_to_base_px(la+dlat, lo+dlon),
                        ll_to_base_px(la-dlat, lo+dlon),
                        ll_to_base_px(la-dlat, lo-dlon)], np.float32)
        if (pts < 0).any() or (pts[:, 0] > BW).any() or (pts[:, 1] > BH).any():
            rows.append((name, None, None, None, "outside the base image"))
            continue
        dstq = np.array([[0, 0], [side, 0], [side, side], [0, side]], np.float32)
        tmpl = prep(cv2.warpPerspective(base_np, cv2.getPerspectiveTransform(pts, dstq),
                                        (side, side)))

        pad = int(SEARCH_M / MPP)
        x0, y0 = deg2tile(la + dlat, lo - dlon, Z)
        rx0, ry0 = int((x0-tx0)*TS) - pad, int((y0-ty0)*TS) - pad
        win = ref_np[ry0:ry0+side+2*pad, rx0:rx0+side+2*pad]
        if win.shape[0] < side + 4 or win.shape[1] < side + 4:
            rows.append((name, None, None, None, "outside the reference mosaic"))
            continue
        win = prep(win)

        res = cv2.matchTemplate(win, tmpl, cv2.TM_CCOEFF_NORMED)
        _, peak, _, loc = cv2.minMaxLoc(res)
        m = res.copy()
        cv2.circle(m, loc, max(4, side // 8), float(res.min()), -1)
        second = float(m.max())

        dx, dy = loc[0] - pad, loc[1] - pad     # 0,0 would be a perfect georeference
        err_m = math.hypot(dx, dy) * MPP
        east_m, north_m = dx * MPP, -dy * MPP
        note = "" if (peak > 0.30 and peak - second > 0.05) else "WEAK, ignore"
        rows.append((name, err_m, (east_m, north_m), (peak, peak - second), note))

    print(f"{'landmark':22} {'error':>9}  {'east':>7} {'north':>7}   "
          f"{'peak':>5} {'sharp':>6}")
    good = []
    for name, err, off, q, note in rows:
        if err is None:
            print(f"{name:22} {note}")
            continue
        print(f"{name:22} {err:7.0f} m  {off[0]:6.0f}m {off[1]:6.0f}m   "
              f"{q[0]:5.2f} {q[1]:6.2f}  {note}")
        if not note:
            good.append(err)
    if good:
        print(f"\n{len(good)}/{len(CHECKS)} landmarks confirmed, "
              f"median residual {np.median(good):.0f} m, worst {max(good):.0f} m")
    else:
        print("\nno landmark confirmed; the transform is not usable")


if __name__ == "__main__":
    main()
