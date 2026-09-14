"""Build the map's tile pyramid for web/tiles/.

The map shipped as a single `imageOverlay` of `web/img/base.webp`, which forced
three things a tile layer simply does not have:

- **Black bands.** One finite rectangle over a 3.5:1 coast letterboxes on every
  viewport shape, and a large amount of machinery in `web/index.html` existed
  only to size a blurred copy of the image into those bands.
- **A zoom floor.** Zooming out past the image bought empty space, so the floor
  had to be computed and clamped on every resize.
- **5 to 75 m of displacement.** `base.webp` is a generative upscale of Google
  Earth captures; tiles are the ground truth the annotations are traced from.

EVERY LEVEL IS FETCHED NATIVE. z17 comes from the existing cache; z12 to z16 are
fetched from Bing at their own zoom.

The first version of this script derived the lower levels by averaging the four
children below each tile, which is the ordinary way to build a pyramid and was
wrong here for one reason: THE SOURCE IS A STRIP, NOT A SQUARE. One z13 tile
spans 16 x 16 z17 tiles, and the cache is a 56 x 27 rectangle hugging the coast,
so almost every z13 tile had a handful of real children and fifteen-sixteenths
background fill. That fill was the app's own navy, indistinguishable from the
black bands this change set out to remove: the map looked like it had no imagery
at exactly the zoom where it had the most. Every derived level carried a ring of
part-filled tiles at its edge for the same reason.

So the rule is: never derive a tile the source does not fully cover. Fetching is
cheaper to reason about than tracking coverage per tile, and native low-zoom
imagery is real imagery rather than a downsample of a strip.

BOXES DIFFER BY ZOOM, because the reason for each level differs. z12 to z14 cover
a wide context box so a zoomed-out viewport has sea and forest at its edges
instead of a void. z15 and z16 cover only the coast, because nobody reaches that
zoom except by going to a beach; fetching them across the context box would be
about 2,000 tiles of imagery no one will ever pan to.

LICENSING: serving these redistributes Bing imagery, which their terms do not
permit. Daniel's call on 2026-09-14 was to proceed on the basis that this is a
nonprofit safety map. Recorded here so nobody has to rediscover the question. The
alternative, if it is ever revisited, is Esri World Imagery: free with
attribution and finer than this cache, at the cost of offline precaching.

SELF SUFFICIENT. It needs no local tile cache and no other script: every level
including z17 is fetched if it is not already on disk. `tools/tilecache/` is a
seed that saves re-fetching 1,395 tiles, nothing more.

Usage:  python tools/build_tiles.py            # fills gaps, keeps what exists
        REBUILD=1 python tools/build_tiles.py  # from scratch
"""
import glob
import json
import math
import os
import re
import shutil
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "tilecache")
OUT = os.path.join(ROOT, "web", "tiles")
Z_NATIVE = 17       # the level the existing cache holds
QUALITY = 78        # measured: 82 costs 31% more bytes for no visible gain here

# S, W, N, E
COAST_BOX = (9.6143, -82.8012, 9.6874, -82.6474)      # the cache's own extent
CONTEXT_BOX = (9.5500, -82.8800, 9.7500, -82.5700)    # ~22 x 34 km of surrounds
BOX_FOR = {12: CONTEXT_BOX, 13: CONTEXT_BOX, 14: CONTEXT_BOX,
           15: COAST_BOX, 16: COAST_BOX, 17: COAST_BOX}

# Install BLOCKS on CRITICAL, so it holds the least that is still a working
# offline map: z12 and z13, the whole coast at 18.9 m/px with every zone line
# readable. Putting z14 in as well took the blocking set past 1.6 MB, and on the
# weak signal this map is built for that is the difference between saving and
# giving up. Detail is OPTIONAL and arrives in the background.
PRECACHE_CRITICAL = (12, 13)
PRECACHE_OPTIONAL = (14, 15)


def deg2tile(lat, lon, z):
    n = 2 ** z
    return ((lon + 180.0) / 360.0 * n,
            (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n)


def quadkey(x, y, z):
    q = ""
    for i in range(z, 0, -1):
        d, m = 0, 1 << (i - 1)
        if x & m:
            d += 1
        if y & m:
            d += 2
        q += str(d)
    return q


def fetch_one(job):
    z, x, y = job
    d = os.path.join(OUT, str(z), str(x))
    fp = os.path.join(d, f"{y}.jpg")
    if os.path.exists(fp) and os.path.getsize(fp) > 800:
        return "had"
    url = (f"http://ecn.t{(x + y) % 4}.tiles.virtualearth.net/"
           f"tiles/a{quadkey(x, y, z)}.jpeg?g=1")
    for _ in range(3):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 CaribbeanGuard/1.0"})
            with urllib.request.urlopen(req, timeout=25) as r:
                body = r.read()
            # 1033 bytes is Bing's "no imagery at this zoom" placeholder. Writing
            # it would put a grey NO DATA square on a safety map.
            if len(body) < 800 or len(body) == 1033:
                return "nodata"
            os.makedirs(d, exist_ok=True)
            with open(fp, "wb") as f:
                f.write(body)
            return "got"
        except Exception:
            pass
    return "failed"


def fetch_level(z):
    s, w, n, e = BOX_FOR[z]
    x0, y0 = deg2tile(n, w, z)
    x1, y1 = deg2tile(s, e, z)
    jobs = [(z, x, y)
            for x in range(int(x0), int(x1) + 1)
            for y in range(int(y0), int(y1) + 1)]
    with ThreadPoolExecutor(max_workers=8) as pool:
        res = list(pool.map(fetch_one, jobs))
    got, had = res.count("got"), res.count("had")
    print(f"z{z}: {len(jobs)} wanted, fetched {got}, already had {had}, "
          f"unavailable {len(res) - got - had}")


def copy_native():
    """Seed z17 from tools/tilecache/ if it is there. Missing tiles get fetched.

    THIS USED TO BE MANDATORY AND IT BROKE A CLEAN CLONE. It raised
    "no tile cache; run tools/georef2.py first", and that instruction does not
    work on any machine but the one it was written on: georef2.py reads an
    absolute path into a Downloads folder, at a file that is not in the
    repository. So the single command docs/deploy.md tells a deployer to run was
    false on a fresh checkout, and the failure pointed at a script that would
    also fail. A recovery instruction nobody has run from a clean state is a
    guess.

    The cache is now an optimisation, not a prerequisite: z17 sits in BOX_FOR
    like every other level and fetch_level fills whatever is missing. Keeping the
    cache still saves re-fetching 1,395 tiles.
    """
    files = glob.glob(os.path.join(CACHE, f"{Z_NATIVE}_*.jpg"))
    if not files:
        print(f"z{Z_NATIVE}: no local cache, fetching the level instead")
        return
    n = 0
    for f in files:
        _, x, y = os.path.basename(f)[:-4].split("_")
        d = os.path.join(OUT, str(Z_NATIVE), x)
        os.makedirs(d, exist_ok=True)
        try:
            Image.open(f).convert("RGB").save(
                os.path.join(d, f"{y}.jpg"), quality=QUALITY, optimize=True)
            n += 1
        except Exception:
            pass
    print(f"z{Z_NATIVE}: {n} tiles from the cache")


def tile_urls(z_from, z_to):
    out = []
    for z in range(z_from, z_to + 1):
        d = os.path.join(OUT, str(z))
        if not os.path.isdir(d):
            continue
        for x in sorted(os.listdir(d), key=int):
            for f in sorted(os.listdir(os.path.join(d, x)), key=lambda s: int(s[:-4])):
                out.append(f"tiles/{z}/{x}/{f}")
    return out


def write_sw_lists():
    """Rewrite the generated tile lists inside web/sw.js.

    Generated rather than hand written for the reason the worker's own header
    gives: a precache list naming a tile that is not deployed logs a failure on
    every install, and one omitting a deployed tile is a hole in the map at the
    water's edge. Neither is visible to whoever deployed it.
    """
    path = os.path.join(ROOT, "web", "sw.js")
    src = open(path, encoding="utf-8").read()
    crit, opt = tile_urls(*PRECACHE_CRITICAL), tile_urls(*PRECACHE_OPTIONAL)
    fmt = lambda name, urls: (f"const {name} = [\n  " +
                              ",\n  ".join(f'"{u}"' for u in urls) + "\n];")
    block = ("/* TILES:BEGIN generated by tools/build_tiles.py -- do not edit by hand */\n"
             + fmt("TILES_CRITICAL", crit) + "\n"
             + fmt("TILES_OPTIONAL", opt) + "\n"
             + "/* TILES:END */")
    new, n = re.subn(r"/\* TILES:BEGIN.*?/\* TILES:END \*/", lambda m: block, src, flags=re.S)
    if not n:
        raise SystemExit("sw.js has no TILES:BEGIN/TILES:END markers")
    open(path, "w", encoding="utf-8").write(new)
    kb = lambda u: sum(os.path.getsize(os.path.join(ROOT, "web", p)) for p in u) / 1024
    print(f"sw.js: {len(crit)} critical ({kb(crit):.0f} KB), "
          f"{len(opt)} optional ({kb(opt):.0f} KB)")


def main():
    if os.environ.get("REBUILD") == "1" and os.path.isdir(OUT):
        shutil.rmtree(OUT)

    copy_native()
    for z in sorted(BOX_FOR):
        fetch_level(z)
    write_sw_lists()

    total = sum(len(f) for _, _, f in os.walk(OUT))
    size = sum(os.path.getsize(os.path.join(r, f))
               for r, _, fs in os.walk(OUT) for f in fs)
    manifest = {"minZoom": min(BOX_FOR), "maxNativeZoom": Z_NATIVE,
                "contextBounds": [[CONTEXT_BOX[0], CONTEXT_BOX[1]],
                                  [CONTEXT_BOX[2], CONTEXT_BOX[3]]],
                "coastBounds": [[COAST_BOX[0], COAST_BOX[1]],
                                [COAST_BOX[2], COAST_BOX[3]]],
                "tiles": total, "bytes": size}
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"\n{total} tiles, {size/1024/1024:.1f} MB in web/tiles/")


if __name__ == "__main__":
    main()
