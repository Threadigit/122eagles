"""Render the 1200x630 social preview (public/assets/social-mdeagles.jpg).

Uses the graded bridge photograph and the self-hosted Schibsted Grotesk and Hanken Grotesk fonts (pinned to one weight and converted from
woff2 in memory with fontTools + brotli). Run: python3 scripts/make-social-card.py
"""
import io
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw, ImageFont

assets = Path(__file__).resolve().parents[1] / 'public' / 'assets'
W, H = 1200, 630


def font(name, size, weight=400):
    ttf = instancer.instantiateVariableFont(TTFont(assets / name), {'wght': weight})
    ttf.flavor = None
    buffer = io.BytesIO()
    ttf.save(buffer)
    buffer.seek(0)
    return ImageFont.truetype(buffer, size)


photo = Image.open(assets / 'bay-bridge-film-1920.webp').convert('RGB')
crop_h = round(photo.width * H / W)
top = 330
card = photo.crop((0, top, photo.width, top + crop_h)).resize((W, H), Image.LANCZOS)

shade = Image.new('RGBA', (W, H))
px = shade.load()
for x in range(W):
    for y in range(H):
        left = max(0.0, 1 - x / (W * 0.78)) ** 1.2
        bottom = max(0.0, (y - H * 0.35) / (H * 0.65)) ** 1.5
        px[x, y] = (6, 17, 23, min(235, int(255 * (0.82 * left + 0.55 * bottom))))
card = Image.alpha_composite(card.convert('RGBA'), shade)

draw = ImageDraw.Draw(card)
white = (251, 249, 243, 255)
# eagle mark (same geometry as assets/eagle.svg), scaled from the 64-unit grid
def pt(x, y, ox=64, oy=60, k=2.6):
    return (ox + (x - 8) * k, oy + (y - 22) * k)
for pts in ([(32, 38), (22, 26), (8, 22), (19, 37), (32, 45)],
            [(32, 38), (42, 26), (56, 22), (45, 37), (32, 45)],
            [(27, 32), (32, 24), (37, 32)], [(32, 38), (32, 45)]):
    draw.line([pt(*p) for p in pts], fill=white, width=3, joint='curve')
draw.text((64 + 48 * 2.6 + 22, 62), 'MD Eagles', font=font('schibsted-grotesk.woff2', 40, 600), fill=white)

title = font('schibsted-grotesk.woff2', 78, 700)
gold = (255, 200, 56, 255)
for i, line in enumerate(['Fix what’s missing.', 'Find what already works.']):
    draw.text((64, 316 + i * 100), line, font=title, fill=white if i == 0 else gold)
draw.text((66, 540), 'Maryland problems with possible solutions, and the help that already exists.', font=font('hanken-grotesk.woff2', 28, 400), fill=(201, 210, 212, 255))
card.convert('RGB').save(assets / 'social-mdeagles.jpg', quality=88, optimize=True)
print('wrote social-mdeagles.jpg')
