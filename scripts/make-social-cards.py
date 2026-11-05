"""Render the 1200x630 social preview cards used for Open Graph and Twitter.

public/assets/social-mdeagles.jpg is the default (homepage). Every brief, guide and section page also gets its
own card in public/assets/social/ showing that page's title, so a link shared in a text, group chat or on social
media says what the page is. Uses the graded bridge photograph and the self-hosted Newsreader and Hanken Grotesk
fonts (pinned to one weight, converted from woff2 in memory).
Run: python3 scripts/make-social-cards.py
"""
import io
import json
from pathlib import Path

import numpy as np
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
assets = root / 'public' / 'assets'
out_dir = assets / 'social'
out_dir.mkdir(exist_ok=True)
W, H = 1200, 630
WHITE, GOLD, SOFT = (251, 249, 243, 255), (255, 200, 56, 255), (201, 210, 212, 255)
_fonts = {}


def font(name, size, weight=400, opsz=None):
    key = (name, size, weight, opsz)
    if key not in _fonts:
        axes = {'wght': weight}
        if opsz:
            axes['opsz'] = opsz
        ttf = instancer.instantiateVariableFont(TTFont(assets / name), axes)
        ttf.flavor = None
        buffer = io.BytesIO()
        ttf.save(buffer)
        buffer.seek(0)
        _fonts[key] = ImageFont.truetype(buffer, size)
    return _fonts[key]


photo = Image.open(root / 'content' / 'source' / 'chesapeake-bay-bridge-1920.webp').convert('RGB')
# the graded film image is what the site shows, so use it
photo = Image.open(assets / 'bay-bridge-film-1920.webp').convert('RGB')
xs, ys = np.meshgrid(np.arange(W), np.arange(H))
left = np.clip(1 - xs / (W * 0.82), 0, 1) ** 1.2
bottom = np.clip((ys - H * 0.3) / (H * 0.7), 0, 1) ** 1.5
alpha = np.clip(255 * (0.86 * left + 0.6 * bottom), 0, 238).astype(np.uint8)
shade = Image.fromarray(np.dstack([np.full((H, W), 18), np.full((H, W), 15), np.full((H, W), 16), alpha]).astype(np.uint8), 'RGBA')


def background(top):
    crop_h = round(photo.width * H / W)
    card = photo.crop((0, top, photo.width, top + crop_h)).resize((W, H), Image.LANCZOS).convert('RGBA')
    card = Image.alpha_composite(card, shade)
    d = ImageDraw.Draw(card)
    k = 2.4
    for pts in ([(32, 38), (22, 26), (8, 22), (19, 37), (32, 45)], [(32, 38), (42, 26), (56, 22), (45, 37), (32, 45)],
                [(27, 32), (32, 24), (37, 32)], [(32, 38), (32, 45)]):
        d.line([(64 + (x - 8) * k, 58 + (y - 22) * k) for x, y in pts], fill=GOLD, width=3, joint='curve')
    d.text((64 + 48 * k + 20, 56), 'MD Eagles', font=font('newsreader.woff2', 42, 500, 24), fill=WHITE)
    d.text((W - 64, 66), 'mdeagles.com', font=font('hanken-grotesk.woff2', 24, 400), fill=SOFT, anchor='ra')
    return card


BASES = [background(top) for top in (330, 90, 540)]


def wrap(text, face, width):
    lines, current = [], ''
    for word in text.split():
        trial = f'{current} {word}'.strip()
        if face.getlength(trial) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def card(title, kicker, path, variant=0):
    img = BASES[variant % 3].copy()
    d = ImageDraw.Draw(img)
    size = 84
    while True:
        face = font('newsreader.woff2', size, 400, 72)
        lines = wrap(title, face, 1040)
        if len(lines) <= 3 or size <= 52:
            break
        size -= 4
    y = 520 - len(lines) * int(size * 1.08)
    d.text((64, y - 58), kicker.upper(), font=font('hanken-grotesk.woff2', 22, 500), fill=GOLD)
    for i, line in enumerate(lines):
        d.text((64, y + i * int(size * 1.08)), line, font=face, fill=WHITE)
    img.convert('RGB').save(path, quality=84, optimize=True, progressive=True)


# default / homepage card
home = BASES[0].copy()
d = ImageDraw.Draw(home)
big = font('newsreader.woff2', 92, 400, 72)
d.text((64, 316), 'Fix what’s missing.', font=big, fill=WHITE)
d.text((64, 416), 'Find what already works.', font=big, fill=GOLD)
d.text((66, 540), 'Maryland problems with possible solutions, and the help that already exists.', font=font('hanken-grotesk.woff2', 28, 400), fill=SOFT)
home.convert('RGB').save(assets / 'social-mdeagles.jpg', quality=88, optimize=True, progressive=True)

card('Maryland problems to solve', 'Problem collection', out_dir / 'problems.jpg', 1)
card('Help that already exists, by county or need', 'Resource guides', out_dir / 'guides.jpg', 2)
card('An independent publication about Maryland', 'About MD Eagles', out_dir / 'about.jpg', 0)
for i, p in enumerate(json.loads((root / 'content/problems.json').read_text())):
    card(p['title'], f'Problem brief · {p["place"].split(" · ")[0]}', out_dir / f'{p["slug"]}.jpg', i + 1)
for i, g in enumerate(json.loads((root / 'content/guides.json').read_text())):
    card(g['title'], f'Resource guide · {g["category"]}', out_dir / f'{g["slug"]}.jpg', i + 2)
print('wrote', len(list(out_dir.glob('*.jpg'))) + 1, 'social cards')
