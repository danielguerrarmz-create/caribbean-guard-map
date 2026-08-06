"""Generate the home screen icons for web/manifest.json.

These are PLACEHOLDERS and they are deliberately plain: navy tile, white CG. No
logo is invented here, because inventing a mark for somebody else's organisation
and then bolting it to a tourist's home screen is not ours to do. Caribbean Guard
should replace these with their own mark; the sizes and filenames are what the
manifest expects, so a straight swap works.

Add to Home Screen is not decoration on this project. WebKit deletes script
writable storage, service worker registrations and caches included, after seven
days of Safari use without interaction on a site, and it exempts Home Screen web
applications, which get their own counter reset by real use. So the manifest is
the half that makes the offline half durable on the platform most tourists carry,
and an icon is what the platform needs to offer the install at all.

Run:  python tools/make_icons.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "web", "icons")

NAVY = (11, 28, 44, 255)
WHITE = (255, 255, 255, 255)

# any bold sans will do; the first one that exists wins
FONTS = [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]


def font_at(size):
    for p in FONTS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def icon(px, inset):
    """inset is the fraction of the tile the mark is allowed to occupy.

    Maskable icons get 0.42 rather than 0.62: the platform may crop the tile to
    any shape inside a circle of 80% diameter, so anything outside that circle can
    be shaved off. A wordmark that loses a letter to a rounded corner is worse
    than one that is slightly small.
    """
    im = Image.new("RGBA", (px, px), NAVY)
    d = ImageDraw.Draw(im)
    f = font_at(int(px * inset * 0.62))
    box = d.textbbox((0, 0), "CG", font=f)
    d.text(((px - (box[2] - box[0])) / 2 - box[0],
            (px - (box[3] - box[1])) / 2 - box[1]), "CG", font=f, fill=WHITE)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    made = []
    for name, px, inset in [("icon-180.png", 180, 0.62),
                            ("icon-192.png", 192, 0.62),
                            ("icon-512.png", 512, 0.62),
                            ("icon-maskable-512.png", 512, 0.42)]:
        p = os.path.join(OUT, name)
        icon(px, inset).save(p, "PNG", optimize=True)
        made.append((name, os.path.getsize(p)))
    for name, size in made:
        print(f"  {name:26} {size:>7,} B")
    print(f"wrote {len(made)} icons to {OUT}")


if __name__ == "__main__":
    main()
