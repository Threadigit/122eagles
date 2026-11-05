"""Prepare the Maryland place photographs and the film-grain texture.

Sources (public-domain Library of Congress, Carol M. Highsmith) live in
content/source/places. Outputs go to public/assets/places as 640 and 1024px WebP.
Run: python3 scripts/prepare-photos.py
"""
from pathlib import Path

import numpy as np
from PIL import Image

root = Path(__file__).resolve().parents[1]
src = root / 'content' / 'source' / 'places'
out = root / 'public' / 'assets' / 'places'
out.mkdir(parents=True, exist_ok=True)

for photo in sorted(src.glob('*.jpg')):
    image = Image.open(photo).convert('RGB')
    # never upscale: widths up to the source width, plus the source width itself
    for width in sorted({w for w in (640, 1024) if w < image.width} | {image.width}):
        height = round(image.height * width / image.width)
        resized = image if image.width == width else image.resize((width, height), Image.LANCZOS)
        resized.save(out / f'{photo.stem}-{width}.webp', quality=80, method=6)
    print('prepared', photo.stem)

# A small tiling grain (transparent speckle) that gives dark surfaces a printed, tactile feel.
rng = np.random.default_rng(7)
size = 180
noise = rng.normal(0.5, 0.22, (size, size)).clip(0, 1)
alpha = (np.abs(noise - 0.5) * 2 * 255 * 0.55).astype(np.uint8)
value = np.where(noise > 0.5, 255, 0).astype(np.uint8)
grain = np.dstack([value, value, value, alpha])
Image.fromarray(grain).save(root / 'public' / 'assets' / 'grain.png', optimize=True)
print('wrote grain.png')
