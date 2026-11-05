"""Welcome, clock, sky, county memory and navigation checks (localhost only: uses ?demo=).

Needs Playwright for Python and EAGLES_BROWSER pointing at a Chromium binary.
Run the preview first: python3 scripts/serve.py 8012
"""
import os
from playwright.sync_api import sync_playwright, expect
BASE = os.environ.get('EAGLES_TEST_URL', 'http://127.0.0.1:8012/').rstrip('/')
CASES = [  # Maryland wall-clock time on Nov 5, 2026 (sunrise 6:37 AM, sunset 5:02 PM EST)
    ('06:55', 'dawn', 'Good morning, neighbor.'), ('12:10', 'day', 'Good afternoon, neighbor.'),
    ('16:45', 'golden', 'Good afternoon, neighbor.'), ('17:30', 'dusk', 'Good evening, neighbor.'),
    ('22:30', 'night', 'Still up, neighbor.'),
]
with sync_playwright() as p:
    options = {'headless': True}
    if os.environ.get('EAGLES_BROWSER'):
        options['executable_path'] = os.environ['EAGLES_BROWSER']
    browser = p.chromium.launch(**options)
    for width, height in [(390, 844), (1440, 900)]:
        page = browser.new_page(viewport={'width': width, 'height': height}, timezone_id='America/New_York')
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        for clock, phase, greeting in CASES:
            page.goto(f'{BASE}/?demo=2026-11-05T{clock}', wait_until='networkidle')
            expect(page.locator('[data-film]')).to_have_attribute('data-phase', phase)
            expect(page.locator('[data-greeting]')).to_have_text(greeting)
        page.goto(f'{BASE}/?demo=2026-11-05T09:20', wait_until='networkidle')
        expect(page.locator('[data-sunrise]')).to_have_text('6:37 AM')
        expect(page.locator('[data-sunset]')).to_have_text('5:02 PM')
        page.locator('[data-county-pick]').select_option('Howard')
        expect(page.locator('[data-greeting]')).to_have_text('Good morning, Howard County.')
        page.reload(wait_until='networkidle')
        expect(page.locator('[data-county-pick]')).to_have_value('Howard')
        page.goto(f'{BASE}/guides', wait_until='networkidle')
        expect(page.locator('[name=county]')).to_have_value('Howard')
        if width < 761:
            page.goto(BASE + '/')
            page.get_by_role('button', name='Menu').click()
            expect(page.locator('[data-menu]')).to_be_visible()
            page.keyboard.press('Escape')
            expect(page.locator('[data-menu]')).to_be_hidden()
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert not errors, errors
        page.close()
        print(f'PASS {width}px: greeting, phases, sun times, county memory, menu')
    browser.close()
