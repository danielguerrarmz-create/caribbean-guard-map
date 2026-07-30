"""Match the shoreline as a 1-D profile.

The 2-D approaches kept finding degenerate optima. The shoreline here is a
function: for each column there is one land/water boundary. Reducing both
images to y = shore(x) removes the ambiguity, makes the headlands legible, and
lets the scale be read off the spacing between them.

The mask is built by flood filling water inward from the top edge, so dark reef
patches inside the sea can no longer be mistaken for land.
"""
import glob, math, os, sys
import numpy as np, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:\Users\danie\Downloads\caribbean-guard-cuts\Complete Mapping.jpg"
Z, TS = 17, 256


def tile2deg(x, y, z):
    n = 2 ** z
    return (math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))),
            x / n * 360.0 - 180.0)


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


def water_mask(a, pct=45):
    """Flood fill water inward from the top edge. Reef and dark seabed inside
    the sea stay water, which a threshold alone gets wrong."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    idx = (b - g) + 0.35 * (b - r)
    idx = (idx - idx.min()) / (np.ptp(idx) + 1e-6)
    m = (idx > np.percentile(idx, pct)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    h, w = m.shape
    ff = m.copy()
    mask = np.zeros((h + 2, w + 2), np.uint8)
    for x in range(0, w, 8):                 # seed along the top edge
        if ff[0, x] == 1:
            cv2.floodFill(ff, mask, (x, 0), 2)
    return (ff == 2).astype(np.uint8)        # connected-to-open-sea water only


def shoreline(mask):
    """y of the water/land boundary per column; nan where the column is all one."""
    h, w = mask.shape
    prof = np.full(w, np.nan)
    for x in range(w):
        col = mask[:, x]
        land = np.where(col == 0)[0]
        if len(land) and land[0] > 0:
            prof[x] = land[0]
    return prof


def main():
    ref, tx0, ty0 = load_ref()
    RW, RH = ref.size
    nlat, _ = tile2deg(tx0, ty0, Z)
    GW = 1600
    rs = GW / RW
    ref_mpp = (156543.03392 * math.cos(math.radians(nlat)) / (2 ** Z)) / rs

    ra = cv2.resize(np.asarray(ref.convert("RGB")).astype(np.float32) / 255.0,
                    (GW, int(GW * RH / RW)), interpolation=cv2.INTER_AREA)
    rw = water_mask(ra)
    rp = shoreline(rw)
    cv2.imwrite(os.path.join(HERE, "dbg_ref_water.png"), rw * 255)

    bp_img = Image.open(BASE); BW, BH = bp_img.size
    bwid = 1600
    ba = np.asarray(bp_img.resize((bwid, int(bwid * BH / BW)), Image.LANCZOS)
                    ).astype(np.float32) / 255.0
    bw_ = water_mask(ba)
    bp = shoreline(bw_)
    cv2.imwrite(os.path.join(HERE, "dbg_base_water.png"), bw_ * 255)

    print(f"reference profile: {np.isfinite(rp).sum()}/{len(rp)} columns, "
          f"{ref_mpp:.2f} m per px")
    print(f"base profile:      {np.isfinite(bp).sum()}/{len(bp)} columns")

    # plot both, normalised to their own width, so the headlands can be compared
    Hplot = 420
    canvas = np.full((Hplot * 2 + 30, 1600, 3), 255, np.uint8)
    for k, (prof, colour, label) in enumerate([(rp, (60, 140, 40), "Bing reference"),
                                               (bp, (40, 60, 200), "your stitched base")]):
        off = k * (Hplot + 30)
        pts = [(x, off + int(np.clip(prof[x] / (rw.shape[0] if k == 0 else bw_.shape[0])
                                     * Hplot, 0, Hplot - 1)))
               for x in range(len(prof)) if np.isfinite(prof[x])]
        for i in range(1, len(pts)):
            if abs(pts[i][0] - pts[i-1][0]) <= 2:
                cv2.line(canvas, pts[i-1], pts[i], colour, 2)
        cv2.putText(canvas, label, (12, off + 24), cv2.FONT_HERSHEY_SIMPLEX, .7, colour, 2)
    cv2.imwrite(os.path.join(HERE, "dbg_profiles.png"), canvas)
    np.save(os.path.join(HERE, "prof_ref.npy"), rp)
    np.save(os.path.join(HERE, "prof_base.npy"), bp)
    print("wrote dbg_profiles.png, dbg_ref_water.png, dbg_base_water.png")


if __name__ == "__main__":
    main()
