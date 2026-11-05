"""Simplify Maryland's county boundaries for on-device county detection.

Source: content/source/us-counties.geojson, US Census Bureau county boundaries
(public domain; the plotly/datasets copy of the Census cartographic file). Output:
public/assets/md-counties.json, a few tens of KB. The visitor's location is only ever
compared to these shapes in their own browser. Run: python3 scripts/prepare-counties.py
"""
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parents[1]
FIPS = {
    '24001': 'Allegany', '24003': 'Anne Arundel', '24005': 'Baltimore County', '24009': 'Calvert',
    '24011': 'Caroline', '24013': 'Carroll', '24015': 'Cecil', '24017': 'Charles', '24019': 'Dorchester',
    '24021': 'Frederick', '24023': 'Garrett', '24025': 'Harford', '24027': 'Howard', '24029': 'Kent',
    '24031': 'Montgomery', '24033': "Prince George's", '24035': "Queen Anne's", '24037': "St. Mary's",
    '24039': 'Somerset', '24041': 'Talbot', '24043': 'Washington', '24045': 'Wicomico', '24047': 'Worcester',
    '24510': 'Baltimore City',
}
TOLERANCE = 0.0012  # degrees, about 130 m


def simplify(points, tol):
    """Douglas-Peucker on a closed ring."""
    def dist(p, a, b):
        (x, y), (x1, y1), (x2, y2) = p, a, b
        dx, dy = x2 - x1, y2 - y1
        if dx == dy == 0:
            return math.hypot(x - x1, y - y1)
        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
        return math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))

    def dp(pts):
        if len(pts) < 3:
            return pts
        index, worst = 0, 0
        for i in range(1, len(pts) - 1):
            d = dist(pts[i], pts[0], pts[-1])
            if d > worst:
                index, worst = i, d
        if worst > tol:
            return dp(pts[:index + 1])[:-1] + dp(pts[index:])
        return [pts[0], pts[-1]]

    half = len(points) // 2
    left, right = dp(points[:half + 1]), dp(points[half:])
    ring = left[:-1] + right
    return ring if len(ring) >= 4 else points


features = json.loads((root / 'content/source/us-counties.geojson').read_text())['features']
counties = []
for feature in features:
    name = FIPS.get(str(feature['id']))
    if not name:
        continue
    geometry = feature['geometry']
    polygons = geometry['coordinates'] if geometry['type'] == 'MultiPolygon' else [geometry['coordinates']]
    out = []
    for polygon in polygons:
        rings = []
        for ring in polygon:
            ring = simplify([tuple(p) for p in ring], TOLERANCE)
            rings.append([round(c, 4) for p in ring for c in p])
        out.append(rings)
    xs = [c for polygon in out for c in polygon[0][0::2]]
    ys = [c for polygon in out for c in polygon[0][1::2]]
    counties.append({'n': name, 'b': [min(xs), min(ys), max(xs), max(ys)], 'p': out})
assert len(counties) == 24, len(counties)
target = root / 'public' / 'assets' / 'md-counties.json'
target.write_text(json.dumps({'counties': sorted(counties, key=lambda c: c['n'])}, separators=(',', ':')))
print(f'wrote {target.name}: {target.stat().st_size} bytes, {sum(len(r) // 2 for c in counties for p in c["p"] for r in p)} vertices')
