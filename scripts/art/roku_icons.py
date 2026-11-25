"""Draw the Roku app's channel icons and splash: python3 scripts/art/roku_icons.py roku/images

Needs Pillow. Flat shapes only (a pie-plate mark and the title), so the output is small and
reproducible; re-run it to restyle, the art is not hand-edited.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (30, 26, 23)
ACCENT = (224, 164, 88)
TEXT = (244, 237, 228)
CRUST = (176, 112, 52)
SIZES = {"icon_hd.png": (290, 218), "icon_sd.png": (246, 140), "splash_hd.png": (1280, 720)}


def font(px):
    for name in ("DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, px)
        except OSError:
            pass
    return ImageFont.load_default()


def draw(w, h):
    im = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(im)
    r = int(min(w, h) * 0.26)
    cx, cy = w // 2, int(h * 0.40)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CRUST)
    d.ellipse((cx - r * 0.82, cy - r * 0.82, cx + r * 0.82, cy + r * 0.82), fill=ACCENT)
    for i in range(-2, 3):                              # crumble dots
        for j in range(-2, 3):
            if i * i + j * j <= 5:
                x, y = cx + i * r * 0.28, cy + j * r * 0.28
                d.ellipse((x - r * 0.08, y - r * 0.08, x + r * 0.08, y + r * 0.08), fill=CRUST)
    f = font(max(14, int(h * 0.12)))
    label = "Recipe Book"
    tw = d.textlength(label, font=f)
    d.text(((w - tw) / 2, cy + r + h * 0.06), label, fill=TEXT, font=f)
    return im


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "roku/images")
    out.mkdir(parents=True, exist_ok=True)
    for name, (w, h) in SIZES.items():
        draw(w, h).quantize(32).save(out / name, optimize=True)
        print(out / name)
