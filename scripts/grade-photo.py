"""Colour-grade the Bay Bridge photograph for the cinematic homepage film.

The ungraded master is content/source/chesapeake-bay-bridge-1920.webp (public-domain
Library of Congress photograph, see PHOTO-CREDIT.md). The grade is baked into the
files so the browser needs no filters or blend modes while the camera moves.
Run: python3 scripts/grade-photo.py
"""
from pathlib import Path
import numpy as np
from PIL import Image

root = Path(__file__).resolve().parents[1]
assets = root / 'public' / 'assets'
rgb = np.asarray(Image.open(root / 'content' / 'source' / 'chesapeake-bay-bridge-1920.webp').convert('RGB'), dtype=np.float32) / 255
W = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)


def luma(a):
    return (a * W).sum(axis=2, keepdims=True)


# 1. Mute the saturated blue and pull it toward a cooler teal-slate.
y = luma(rgb)
a = y + (rgb - y) * 0.52
a = a * np.array([0.90, 1.00, 1.03], dtype=np.float32)

# 2. Darker mids with a firm S-curve: moody water, bright steel.
a = np.clip(a, 0, 1) ** 1.38
s = a * a * (3 - 2 * a)
a = a * 0.45 + s * 0.55

# 3. Split tone: navy in the shadows, warm daylight in the highlights.
y = luma(a)
navy = np.array([0.012, 0.050, 0.078], dtype=np.float32)
warm = np.array([1.00, 0.90, 0.74], dtype=np.float32)
a = a + (1 - y) ** 2.2 * navy * 0.9
a = a * (1 - y ** 2.5 * 0.22) + a * warm * y ** 2.5 * 0.22
a = np.clip(a, 0, 1)

graded = Image.fromarray((a * 255 + 0.5).astype(np.uint8))
graded.save(assets / 'bay-bridge-film-1920.webp', quality=80, method=6)
graded.resize((960, round(960 * graded.height / graded.width)), Image.LANCZOS).save(
    assets / 'bay-bridge-film-960.webp', quality=80, method=6)
print('wrote bay-bridge-film-1920.webp and bay-bridge-film-960.webp')
