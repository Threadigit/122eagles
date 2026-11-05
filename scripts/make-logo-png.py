"""Export the MD Eagles logo as transparent PNGs into brand/.

The artwork is the site's own: the eagle mark from scripts/layout.py (viewBox 6 20 52 27, stroke 2, round caps and joins)
beside the "MD Eagles" wordmark in Newsreader 500, -0.02em tracking, 11 px gap, exactly as .identity is set in
public/style.css. Everything is drawn at 4x and shrunk for clean edges; the background is fully transparent.

Outputs (brand/):
  mdeagles-logo-on-dark.png   gold mark + cream wordmark, for dark backgrounds
  mdeagles-logo-on-light.png  near-black mark + wordmark, for light backgrounds
  mdeagles-mark-gold.png / -ink.png / -white.png   the eagle alone (gold, near-black, white)
Run: python3 scripts/make-logo-png.py
"""
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'brand'
OUT.mkdir(exist_ok=True)

GOLD, INK, CREAM, WHITE = (255, 200, 56), (35, 31, 32), (244, 238, 225), (255, 255, 255)
# The mark, in the site's viewBox "6 20 52 27" coordinates
PATHS = [
    [(32, 38), (22, 26), (8, 22), (19, 37), (32, 45)],
    [(32, 38), (42, 26), (56, 22), (45, 37), (32, 45)],
    [(27, 32), (32, 24), (37, 32)],
    [(32, 38), (32, 45)],
]
VB_X, VB_Y, VB_W, VB_H = 6, 20, 52, 27
STROKE = 2

SUPER = 4        # supersampling factor
S = 12           # one CSS pixel of the site = S output pixels for the lockup
MARK_W, MARK_H = 40, 21       # .identity-mark
GAP = 11                      # .identity gap
FONT_PX = 1.55 * 16           # 1.55rem
TRACKING = -0.02              # em
OPSZ = FONT_PX                # font-optical-sizing: auto sets opsz to the px size
PAD = 3                       # transparent margin, in site px


def newsreader():
    path = Path(tempfile.gettempdir()) / 'mdeagles-newsreader.ttf'
    f = TTFont(ROOT / 'public/assets/newsreader.woff2')
    f.flavor = None
    f.save(path)
    return path


def draw_mark(draw, x, y, width, colour, k):
    """Draw the mark with its viewBox top-left at (x, y); `width` is the box width in canvas px."""
    scale = width / VB_W
    w = STROKE * scale
    for path in PATHS:
        pts = [(x + (px - VB_X) * scale, y + (py - VB_Y) * scale) for px, py in path]
        draw.line(pts, fill=colour, width=round(w), joint='curve')
        for cx, cy in pts:
            draw.ellipse([cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2], fill=colour)


def save(img, name, scale=S):
    bbox = img.getchannel('A').getbbox()
    pad = round(PAD * scale)
    img = img.crop(bbox)
    out = Image.new('RGBA', (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    out.paste(img, (pad, pad))
    out.save(OUT / name, optimize=True)
    print(f'{name}: {out.width} x {out.height}px, transparent')


MARK_SCALE = 40  # the eagle alone is exported larger: about 1600 px wide


def mark_only(colour, name):
    k = MARK_SCALE * SUPER
    w, h = MARK_W * k, MARK_H * k
    img = Image.new('RGBA', (round(w + 8 * k), round(h + 8 * k)), (0, 0, 0, 0))
    draw_mark(ImageDraw.Draw(img), 4 * k, 4 * k, w, colour, k)
    save(img.resize((img.width // SUPER, img.height // SUPER), Image.LANCZOS), name, MARK_SCALE)


def lockup(mark_colour, text_colour, name):
    k = S * SUPER
    font = ImageFont.truetype(str(newsreader()), round(FONT_PX * k))
    font.set_variation_by_axes([500, OPSZ])  # Weight, Optical Size
    ascent, descent = font.getmetrics()
    text = 'MD Eagles'
    track = TRACKING * FONT_PX * k
    width = sum(font.getlength(text[: i + 1]) - font.getlength(text[:i]) + track for i in range(len(text)))
    row_h = max(MARK_H * k, FONT_PX * k)
    total_w = MARK_W * k + GAP * k + width
    img = Image.new('RGBA', (round(total_w + 16 * k), round(row_h + 16 * k)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ox, oy = 8 * k, 8 * k
    # flex centring: the mark box and the line box (line-height 1) share a centre
    draw_mark(draw, ox, oy + (row_h - MARK_H * k) / 2, MARK_W * k, mark_colour, k)
    line_top = oy + (row_h - FONT_PX * k) / 2
    baseline = line_top + ((FONT_PX * k) - (ascent + descent)) / 2 + ascent
    x = ox + MARK_W * k + GAP * k
    for i, ch in enumerate(text):
        draw.text((x, baseline), ch, font=font, fill=text_colour, anchor='ls')
        x += font.getlength(text[: i + 1]) - font.getlength(text[:i]) + track
    save(img.resize((img.width // SUPER, img.height // SUPER), Image.LANCZOS), name)


lockup(GOLD, CREAM, 'mdeagles-logo-on-dark.png')
lockup(INK, INK, 'mdeagles-logo-on-light.png')
mark_only(GOLD, 'mdeagles-mark-gold.png')
mark_only(INK, 'mdeagles-mark-ink.png')
mark_only(WHITE, 'mdeagles-mark-white.png')


# ---- square icons (for places that crop to a square: Buttondown's icon, social avatars, app icons) ----
# The bolder favicon drawing (scripts/make-favicons.py geometry) so the eagle stays legible small, fully inside the square
# with about 20% margin on each side, so nothing is cropped.
ICON_WINGS = [(8, 22), (22, 26), (32, 38), (42, 26), (56, 22), (45, 37), (32, 45), (19, 37)]
ICON_BODY = [[(27, 32), (32, 24), (37, 32)], [(32, 38), (32, 45)]]
ICON_STROKE, ICON_EDGE = 3.6, 2.6


def icon(size, name, transparent):
    big = size * 8
    img = Image.new('RGBA', (big, big), (0, 0, 0, 0) if transparent else INK + (255,))
    d = ImageDraw.Draw(img)
    k = big * 0.60 / 48                      # the mark spans 48 units (x 8..56): 60% of the square
    ox, oy = big / 2 - 32 * k, big / 2 - 33.5 * k  # centred on the mark (x 8..56, y 22..45)
    layers = [(ICON_STROKE + ICON_EDGE, INK), (ICON_STROKE, GOLD)] if transparent else [(ICON_STROKE, GOLD)]
    for width, colour in layers:
        w = width * k
        for path in [ICON_WINGS + [ICON_WINGS[0]]] + ICON_BODY:
            pts = [(ox + x * k, oy + y * k) for x, y in path]
            d.line(pts, fill=colour, width=round(w), joint='curve')
            for cx, cy in pts:
                d.ellipse([cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2], fill=colour)
    img.resize((size, size), Image.LANCZOS).save(OUT / name, optimize=True)
    print(f'{name}: {size} x {size}px, {"transparent" if transparent else "near-black background"}')


icon(512, 'mdeagles-icon-512.png', transparent=False)
icon(128, 'mdeagles-icon-128.png', transparent=False)
icon(512, 'mdeagles-icon-512-transparent.png', transparent=True)
