"""Re-export web/img/base-lo.webp, the overview that is the whole critical path.

The overview is the ONLY image that loads on arrival. base.webp (2.52 MB) is
deferred to the first zoom or pan, so every byte here is paid by every visitor
including the one who scans a QR code, reads their beach card and pockets the
phone. That user is the dominant one.

Size is not a guess. At the default letterboxed zoom on a portrait phone the
overlay measures 372x125 CSS px, which is 1116x375 device px at DPR 3. A 1000 px
wide overview is already at that effective resolution, so anything wider is
resolution nobody can see.

    docs/site-revamp/04-map-integration.md specced 1000x335 q70 and it was never
    exported; the repo shipped 1200x402 at 88,718 B until 2026-08-06.

Alpha is mandatory. The source is a rotated quad resampled north-up, so the four
corners are transparent wedges. Flatten them and the map grows black triangles.

Run:  python tools/export_overview.py
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "web", "img", "base.webp")
DST = os.path.join(ROOT, "web", "img", "base-lo.webp")

WIDTH, HEIGHT, QUALITY = 1000, 335, 70


def main():
    src = Image.open(SRC)
    if src.mode != "RGBA":
        src = src.convert("RGBA")
    before = os.path.getsize(DST) if os.path.exists(DST) else 0

    out = src.resize((WIDTH, HEIGHT), Image.LANCZOS)
    out.save(DST, "WEBP", quality=QUALITY, method=6, exact=False)

    after = os.path.getsize(DST)
    print(f"{SRC} {src.size}")
    print(f"{DST} {out.size} q{QUALITY}")
    print(f"  before {before:,} B")
    print(f"  after  {after:,} B   (saved {before - after:,} B)")


if __name__ == "__main__":
    main()
