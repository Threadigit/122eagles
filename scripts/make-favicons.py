"""Draw the MD Eagles favicon set from the logo geometry.

The mark is the same eagle as assets/eagle.svg, drawn bolder so it stays legible at 16 px:
Maryland gold on near-black. Outputs (public/): favicon.ico (16/32/48), assets/favicon.svg,
assets/apple-touch-icon.png (180), assets/icon-192.png, assets/icon-512.png.
Run: python3 scripts/make-favicons.py
"""
from pathlib import Path

from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1] / 'public'
GOLD, INK = (255, 200, 56, 255), (35, 31, 32, 255)
WINGS = [(8, 22), (22, 26), (32, 38), (42, 26), (56, 22), (45, 37), (32, 45), (19, 37)]
BODY = [[(27, 32), (32, 24), (37, 32)], [(32, 38), (32, 45)]]
STROKE = 3.6


def draw_mark(size, scale, rounded, glyph=0.88):
    """Render at 8x and shrink for clean edges."""
    big = size * 8
    img = Image.new('RGBA', (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if rounded:
        d.rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * 0.22), fill=INK)
    else:
        d.rectangle([0, 0, big, big], fill=INK)
    k = big / 64 * glyph * scale
    ox, oy = big / 2 - 32 * k, big / 2 - 33.5 * k

    def pt(p):
        return (ox + p[0] * k, oy + p[1] * k)

    w = STROKE * k
    for path in [WINGS + [WINGS[0]]] + BODY:
        pts = [pt(p) for p in path]
        d.line(pts, fill=GOLD, width=int(w), joint='curve')
        for x, y in pts:  # round joins and caps
            d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=GOLD)
    return img.resize((size, size), Image.LANCZOS)


# favicon.ico: rounded square, large mark
base = draw_mark(256, 1.18, True)
base.save(root / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
# PNG icons
draw_mark(180, 1.0, False, 0.82).convert('RGB').save(root / 'assets' / 'apple-touch-icon.png', optimize=True)
draw_mark(192, 1.0, False, 0.82).save(root / 'assets' / 'icon-192.png', optimize=True)
draw_mark(512, 1.0, False, 0.82).save(root / 'assets' / 'icon-512.png', optimize=True)

# favicon.svg: same drawing, vector
wings = ' '.join(f'{x} {y}' for x, y in WINGS)
svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#231f20"/>'
    f'<g fill="none" stroke="#ffc838" stroke-width="{STROKE}" stroke-linejoin="round" stroke-linecap="round" '
    'transform="translate(32 32) scale(1.18) translate(-32 -33.5)">'
    f'<path d="M{wings}Z"/><path d="M27 32 32 24l5 8M32 38v7"/></g></svg>\n'
)
(root / 'assets' / 'favicon.svg').write_text(svg)
print('wrote favicon.ico, favicon.svg, apple-touch-icon.png, icon-192.png, icon-512.png')
