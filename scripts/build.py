"""Build every page of the site from content/*.json.

    python3 scripts/build.py

Writes: homepage, About, the problem collection and its briefs (plus Word worksheets),
the resource guides, the search script for the collection, and the sitemap.
"""
import json
import math
import zipfile

from layout import PLACES, PUBLIC, ROOT, SITE, band, county_options, e, eagle, page, place_img, typo

TOPICS = {'families': 'Children and families', 'business': 'Small business', 'work': 'Work and careers'}
REVIEWED = 'November 5, 2026'
STATUS = 'Ideas awaiting local testing'

problems = json.loads((ROOT / 'content/problems.json').read_text())
guides = json.loads((ROOT / 'content/guides.json').read_text())
guide_by_slug = {g['slug']: g for g in guides}


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def detect_only():
    return ('<button class="detect" type="button" data-detect-county><svg viewBox="0 0 20 20" width="15" height="15" fill="none" '
            'stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="10" cy="10" r="4.5"/>'
            '<path d="M10 1.5v3M10 15.5v3M1.5 10h3M15.5 10h3"/></svg>Use my location</button>')


def detect_status():
    return '<p class="detect-status" data-detect-status role="status" aria-live="polite"></p>'


def detect_button():
    return detect_only() + detect_status()


def arrow():
    return '<svg class="arrow" viewBox="0 0 20 20" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M4 10h11M11 5.5 15.5 10 11 14.5"/></svg>'


# ------------------------------------------------------------------ worksheets
def worksheet_docx(x, path):
    """A fill-in project worksheet as a Word document (opens in Word, Google Docs and Pages)."""
    import datetime
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor

    INK, MUTED = RGBColor(0x23, 0x1F, 0x20), RGBColor(0x6C, 0x65, 0x67)
    doc = Document()
    for section in doc.sections:
        section.left_margin = section.right_margin = Inches(0.9)
        section.top_margin = section.bottom_margin = Inches(0.8)
    normal = doc.styles['Normal']
    normal.font.name, normal.font.size, normal.font.color.rgb = 'Calibri', Pt(11), INK
    normal.paragraph_format.space_after = Pt(6)
    for name, size in (('Title', 26), ('Heading 1', 15), ('Heading 2', 12)):
        style = doc.styles[name]
        style.font.name, style.font.size, style.font.bold, style.font.color.rgb = 'Georgia', Pt(size), False, INK
        style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Georgia')

    def link(paragraph, url, text=None):
        rid = paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)
        h = OxmlElement('w:hyperlink')
        h.set(qn('r:id'), rid)
        r = OxmlElement('w:r')
        rpr = OxmlElement('w:rPr')
        color = OxmlElement('w:color'); color.set(qn('w:val'), 'C8122C'); rpr.append(color)
        under = OxmlElement('w:u'); under.set(qn('w:val'), 'single'); rpr.append(under)
        r.append(rpr)
        tx = OxmlElement('w:t'); tx.text = text or url; r.append(tx)
        h.append(r)
        paragraph._p.append(h)

    def shade(cell, fill):
        shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear'); shd.set(qn('w:fill'), fill)
        cell._tc.get_or_add_tcPr().append(shd)

    doc.add_paragraph(x['title'], style='Title')
    meta = doc.add_paragraph()
    run = meta.add_run(f'MD Eagles project worksheet · Reviewed {REVIEWED} · Proposals, not proven solutions · ')
    run.font.size, run.font.color.rgb = Pt(9.5), MUTED
    link(meta, f'{SITE}/problems/{x["slug"]}', f'mdeagles.com/problems/{x["slug"]}')

    doc.add_heading('What the evidence shows', level=1)
    doc.add_paragraph(x['evidence'])
    source = doc.add_paragraph('Source: ')
    link(source, x['url'], x['source'])

    doc.add_heading('Possible solutions to test', level=1)
    for title, copy in x['ideas']:
        doc.add_heading(title, level=2)
        doc.add_paragraph(copy)

    doc.add_heading('Your first step', level=1)
    doc.add_paragraph(x['first'])
    for label, key in (('Who to involve', 'people'), ('What to measure', 'measure')):
        para = doc.add_paragraph()
        para.add_run(f'{label}. ').bold = True
        para.add_run(x[key])
    existing = doc.add_paragraph()
    existing.add_run('Build on what exists. ').bold = True
    link(existing, x['existing_url'], x['existing'])
    existing.add_run('. No partnership is implied.')

    doc.add_page_break()
    doc.add_heading('Your local project notes', level=1)
    intro = doc.add_paragraph('Fill this in as you learn. Keep it short and honest: record what residents actually told you, with their permission.')
    intro.runs[0].font.color.rgb = MUTED
    prompts = [
        'City or county', 'What residents told us (with permission)', 'Existing services and the remaining gap',
        'Smallest useful test', 'Who will run it', 'Costs and required permissions',
        'How we will measure improvement', 'Review date and reasons to stop or change direction',
    ]
    table = doc.add_table(rows=len(prompts), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    for row, prompt in zip(table.rows, prompts):
        row.height = Inches(0.95)
        left, right = row.cells
        left.width, right.width = Inches(2.2), Inches(4.5)
        shade(left, 'F5EFE3')
        left.paragraphs[0].add_run(prompt).bold = True
    doc.core_properties.title = f'{x["title"]}: project worksheet'
    doc.core_properties.author = 'MD Eagles'
    doc.core_properties.created = doc.core_properties.modified = datetime.datetime(2026, 11, 5)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)
    # Fixed timestamps inside the zip so rebuilding does not change the file.
    with zipfile.ZipFile(path) as z:
        data = {info.filename: z.read(info.filename) for info in z.infolist()}
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, content in data.items():
            z.writestr(zipfile.ZipInfo(name, date_time=(2026, 11, 5, 0, 0, 0)), content, zipfile.ZIP_DEFLATED)


# ---------------------------------------------------------------- problem cases
def solutions_list(x, level):
    return ''.join(
        f'<li><span class="sol-mark" aria-hidden="true">{chr(65 + i)}</span><div><h{level}>{e(t)}</h{level}><p>{e(c)}</p></div></li>'
        for i, (t, c) in enumerate(x['ideas']))


def case(x, number, level=3):
    searchable = ' '.join([x['title'], x['summary'], x['place'], TOPICS[x['topic']], x['keywords']]
                          + [a + ' ' + b for a, b in x['ideas']])
    n = len(x['ideas'])
    return (
        f'<article class="case" data-entry data-topic="{x["topic"]}" data-search="{e(searchable)}">'
        '<div class="case-problem">'
        f'<p class="case-no" aria-label="Problem {number}">{number:02d}</p>'
        f'<p class="case-place">{e(x["place"])} <span aria-hidden="true">/</span> {TOPICS[x["topic"]]}</p>'
        f'<h{level}><a href="/problems/{x["slug"]}">{e(x["title"])}</a></h{level}>'
        f'<p class="case-summary">{e(x["summary"])}</p>'
        f'<p class="case-evidence"><span>Evidence</span>{e(x["source"])}</p></div>'
        '<div class="case-solutions">'
        f'<p class="label">Possible solutions to test <span>{n} ideas</span></p>'
        f'<ol>{solutions_list(x, level + 1)}</ol>'
        f'<a class="case-link" href="/problems/{x["slug"]}">Read the full brief and first step {arrow()}</a></div></article>'
    )


def cases(level):
    return ''.join(case(x, i, level) for i, x in enumerate(problems, 1))


# ------------------------------------------------------------------- homepage
# A real map of Maryland's 24 jurisdictions, drawn from the simplified Census shapes
# (public/assets/md-counties.json). Every county links to /guides?county=...
def _inside(x, y, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def _edge_distance(x, y, ring):
    best = 1e9
    for i in range(len(ring)):
        (x1, y1), (x2, y2) = ring[i], ring[(i + 1) % len(ring)]
        dx, dy = x2 - x1, y2 - y1
        t = 0 if dx == dy == 0 else max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
        best = min(best, math.hypot(x - (x1 + t * dx), y - (y1 + t * dy)))
    return best


def county_map():
    shapes = json.loads((PUBLIC / 'assets' / 'md-counties.json').read_text())['counties']
    xs = [x for c in shapes for poly in c['p'] for x in poly[0][0::2]]
    ys = [y for c in shapes for poly in c['p'] for y in poly[0][1::2]]
    lon0, lon1, lat0, lat1 = min(xs) - 0.2, max(xs) + 0.3, min(ys) - 0.14, max(ys) + 0.16
    k = math.cos(math.radians((lat0 + lat1) / 2))
    width = 1000.0
    scale = width / ((lon1 - lon0) * k)
    height = (lat1 - lat0) * scale

    def project(lon, lat):
        return ((lon - lon0) * k * scale, (lat1 - lat) * scale)

    def to_ring(flat):
        return [project(flat[i], flat[i + 1]) for i in range(0, len(flat), 2)]

    groups = []
    for index, county in enumerate(sorted(shapes, key=lambda c: c['n'])):
        name = county['n']
        rings = [[to_ring(r) for r in poly] for poly in county['p']]
        d = ''.join('M' + ' '.join(f'{x:.1f} {y:.1f}' for x, y in r) + 'Z' for poly in rings for r in poly)
        # the point deepest inside the largest piece, for the label and the "you are here" pin
        outer = max((poly[0] for poly in rings), key=lambda r: abs(sum(r[i][0] * r[(i + 1) % len(r)][1] - r[(i + 1) % len(r)][0] * r[i][1] for i in range(len(r)))))
        bx0, bx1 = min(p[0] for p in outer), max(p[0] for p in outer)
        by0, by1 = min(p[1] for p in outer), max(p[1] for p in outer)
        best = (0, (bx0 + bx1) / 2, (by0 + by1) / 2)
        for i in range(1, 36):
            for j in range(1, 36):
                px, py = bx0 + (bx1 - bx0) * i / 36, by0 + (by1 - by0) * j / 36
                if _inside(px, py, outer):
                    dist = _edge_distance(px, py, outer)
                    if dist > best[0]:
                        best = (dist, px, py)
        radius, cx, cy = best
        lines = typo(name).split(' ')
        label = ''
        longest = max(len(line) for line in lines) * 5.9
        if radius >= longest / 2 * 0.72 and radius >= 7:
            first = cy - (len(lines) - 1) * 6.5 + 3.5
            label = ''.join(f'<tspan x="{cx:.1f}" y="{first + n * 13:.1f}">{e(line)}</tspan>' for n, line in enumerate(lines))
            label = f'<text class="county-name" text-anchor="middle">{label}</text>'
        groups.append(
            f'<a class="county" href="/guides?county={e(name).replace(chr(39), "%27")}" data-county="{e(name)}" tabindex="-1">'
            f'<path d="{d}" fill-rule="evenodd"/>{label}'
            f'<g class="pin"><circle class="pin-ring" cx="{cx:.1f}" cy="{cy - (11 if label else 0):.1f}" r="7"/><circle class="pin-dot" cx="{cx:.1f}" cy="{cy - (11 if label else 0):.1f}" r="5"/></g></a>')

    context = [('PENNSYLVANIA', -77.3, 39.9, ''), ('WEST VIRGINIA', -79.55, 39.2, 'v'), ('VIRGINIA', -78.0, 38.05, ''),
               ('DELAWARE', -75.45, 39.5, 'v'), ('ATLANTIC OCEAN', -74.93, 38.25, 'v')]
    texts = ''
    for label, lon, lat, mode in context:
        x, y = project(lon, lat)
        rotate = f' transform="rotate(-90 {x:.1f} {y:.1f})"' if mode == 'v' else ''
        anchor = ' text-anchor="end"' if mode == 'r' else ''
        texts += f'<text class="map-context" x="{x:.1f}" y="{y:.1f}"{anchor}{rotate}>{label}</text>'
    bx, by = project(-76.3, 37.98)
    bay = f'<text class="map-bay" x="{bx:.1f}" y="{by:.1f}" text-anchor="middle">Chesapeake Bay</text>'

    names = sorted(TILE_NAMES)
    links = ''.join(f'<li><a href="/guides?county={e(n).replace(chr(39), "%27")}" data-county="{e(n)}">{e(typo(n))}</a></li>' for n in names)
    return (
        '<div class="mapcard"><svg class="mdmap" viewBox="0 0 1000 %.0f" aria-hidden="true" focusable="false">%s<g class="county-layer">%s</g>%s</svg>'
        '<div class="map-intro"><p class="map-title">Where are you?</p>'
        '<p class="map-caption" data-tile-caption>Choose your county or Baltimore City to see local help.</p>'
        % (height, texts, ''.join(groups), bay)
        + detect_button() + '<p class="detect-note">Your location stays on your device.</p></div></div>'
        f'<ul class="county-list" aria-label="All 24 places">{links}</ul>'
    )


TILE_NAMES = [
    'Allegany', 'Anne Arundel', 'Baltimore City', 'Baltimore County', 'Calvert', 'Caroline', 'Carroll', 'Cecil',
    'Charles', 'Dorchester', 'Frederick', 'Garrett', 'Harford', 'Howard', 'Kent', 'Montgomery', "Prince George's",
    "Queen Anne's", "St. Mary's", 'Somerset', 'Talbot', 'Washington', 'Wicomico', 'Worcester',
]


def build_home():
    ideas = sum(len(x['ideas']) for x in problems)
    film = f"""<section class="film night" data-film aria-labelledby="film-title">
<div class="film-frame"><div class="film-camera"><img class="film-img" src="/assets/bay-bridge-film-1920.webp" srcset="/assets/bay-bridge-film-960.webp 960w, /assets/bay-bridge-film-1920.webp 1920w" sizes="max(100vw, 110vh)" width="1920" height="1756" fetchpriority="high" decoding="async" alt="Aerial view of the two Chesapeake Bay Bridge spans crossing the open water."></div></div>
<div class="film-tone" aria-hidden="true"></div><div class="film-shade"></div><div class="film-grain" aria-hidden="true"></div>
<div class="film-grid"><div class="film-copy">
<p class="welcome" data-welcome><span class="welcome-greeting" data-greeting>Welcome, neighbor.</span> <span class="welcome-sub" data-greeting-sub>Pull up a chair.</span></p>
<h1 id="film-title"><span class="line"><span>Fix what’s missing.</span></span> <span class="line line-2"><span>Find what already works.</span></span></h1>
<p class="film-lead">MD Eagles documents the open problems in everyday Maryland life, with possible solutions anyone can take on. And it points residents to the help that already exists in their county.</p>
<div class="doors">
<article class="door spot"><p class="door-for">For people who want to build</p><h2><a href="/problems">Problem collection</a></h2><p>Documented gaps with the evidence behind them and possible solutions to test.</p><span class="door-go" aria-hidden="true">{arrow()}</span></article>
<article class="door spot"><p class="door-for">For anyone who needs help today</p><h2><a href="/guides">Resource guides</a></h2><p>Problems that already have an answer. Find it by county or by what is going on in your life.</p><span class="door-go" aria-hidden="true">{arrow()}</span></article>
</div></div>
<aside class="clock" data-clock aria-label="Maryland time and daylight" hidden>
<p class="label">Maryland right now</p>
<p class="clock-time"><time data-md-time>--:--</time><span class="clock-sec" data-md-sec aria-hidden="true"></span><span class="clock-ampm" data-md-ampm></span></p>
<p class="clock-date" data-md-date></p>
<svg class="sun-arc" viewBox="0 0 240 70" aria-hidden="true" focusable="false"><path class="sun-track" d="M16 60 A104 52 0 0 1 224 60"/><line class="sun-horizon" x1="4" y1="60" x2="236" y2="60"/><circle class="sun-dot" data-sun-dot cx="16" cy="60" r="7"/></svg>
<dl class="sun-times"><div><dt>Sunrise</dt><dd data-sunrise>--</dd></div><div><dt>Sunset</dt><dd data-sunset>--</dd></div></dl>
<p class="clock-you" data-you hidden>Where you are: <time data-you-time></time></p>
<div class="clock-county"><label for="county-pick">Your county</label><select id="county-pick" data-county-pick>{county_options('Choose to personalize')}</select>{detect_button()}</div>
</aside></div>
<p class="film-credit"><a href="https://hdl.loc.gov/loc.pnp/highsm.14292">Chesapeake Bay Bridge · Carol M. Highsmith, Library of Congress</a></p>
</section>"""

    stats = [(str(len(problems)), 'open problems documented'), (str(ideas), 'possible solutions to test'),
             (str(len(guides)), 'resource guides'), ('24', 'places: 23 counties and Baltimore City')]
    hello = f"""<section class="hello" aria-labelledby="hello-title"><div class="wrap hello-grid">
<div class="hello-copy"><p class="label">Welcome to the neighborhood</p>
<h2 id="hello-title">Maryland is <span class="nb">twenty-four</span> places with the same everyday questions. <em>How do we get by, and how do we make it better?</em></h2>
<p>Some gaps are still open. Some problems already have an answer. We keep track of both, so you can build what is missing or find what works, wherever you live.</p>
<ul class="stats">{''.join(f'<li><strong>{n}</strong><span>{t}</span></li>' for n, t in stats)}</ul></div>
<div class="hello-photos" aria-label="Photographs of Maryland places">
<figure class="ph ph-a">{place_img('baltimore', 'ph-img', '(max-width: 760px) 60vw, 28vw')}<figcaption>Baltimore’s Inner Harbor</figcaption></figure>
<figure class="ph ph-b">{place_img('annapolis', 'ph-img', '(max-width: 760px) 70vw, 30vw')}<figcaption>Harbor at Annapolis</figcaption></figure>
<figure class="ph ph-c">{place_img('farm', 'ph-img', '(max-width: 760px) 70vw, 30vw')}<figcaption>A working farm in Queen Anne’s County</figcaption></figure>
</div></div></section>"""

    includes = ['The evidence', 'Possible solutions', 'A first step', 'Who to involve', 'What to measure', 'A worksheet']
    collection = f"""<section class="collection night" id="problems" aria-labelledby="collection-title"><div class="wrap">
<div class="section-head"><div><p class="label">Problem collection</p><h2 id="collection-title">Open problems, and <em>what could solve them.</em></h2></div>
<div><p>Each problem comes with the evidence behind it, possible solutions to test and a first step. They are proposals, not running projects.</p>
<p>Anyone can pick one up: neighbors, students, local businesses, community groups, founders. You do not need to write software.</p></div></div>
<div class="cases">{cases(3)}</div>
<div class="includes"><p class="label">Every brief includes</p><ul>{''.join(f'<li>{i}</li>' for i in includes)}</ul></div>
<p class="collection-note">{len(problems)} problems documented so far. More are added as their sources are checked. <a href="/problems">Search the collection</a></p>
</div></section>"""

    chips = ''.join(f'<li><a href="/guides?topic={g["topic"]}">{e(g["category"])}</a></li>' for g in guides)
    index = ''.join(
        f'<li><a href="/guides/{g["slug"]}"><span class="guide-cat">{e(g["category"])}</span>'
        f'<span class="guide-title">{e(g["title"])}</span></a></li>' for g in guides)
    resources = f"""<section class="resources" id="help" aria-labelledby="help-title"><div class="wrap">
<div class="section-head"><div><p class="label">Resource guides</p><h2 id="help-title">Already solved? <em>Find the help that exists.</em></h2></div>
<div><p>Plenty of problems already have an answer. Our guides point you to it, with the questions worth asking and the limits worth knowing.</p>
<p>Start with where you live, or with what is going on in your life.</p></div></div>
{county_map()}
<div class="life"><h3>Or start with what is going on in your life</h3><ul class="chips">{chips}</ul></div>
<ul class="guide-index">{index}</ul>
</div></section>"""

    updates = f"""<section class="updates night" id="subscribe" aria-labelledby="updates-title">
{place_img('sunset', 'updates-img', '100vw')}<div class="updates-shade"></div><div class="wrap updates-inner">
<h2 id="updates-title">Hear when a new problem is <em>published.</em></h2>
<div><p>Free email, only when there is a new brief or a follow-up.</p>
<button class="button" data-open-subscribe aria-haspopup="dialog" aria-controls="subscribe-dialog">Get email updates</button>
<noscript><p><a href="https://buttondown.com/eagles">Subscribe through Buttondown</a></p></noscript></div></div>
<p class="photo-credit"><a href="{PLACES['sunset'][1]}">Chesapeake Bay sunset · Carol M. Highsmith, Library of Congress</a></p></section>"""

    desc = ('MD Eagles documents open problems in Maryland life with possible solutions anyone can take on, '
            'and guides residents to the help that already exists by county or by what they need.')
    write(PUBLIC / 'index.html', page(
        'Maryland problems worth solving, and the help that already exists', desc, '/',
        film + hello + collection + resources + updates,
        body_class='home', scripts=('/cinema.js', '/welcome.js', '/subscribe.js'), home=True, dialog=True))


# ---------------------------------------------------------------------- about
def build_about():
    sections = [
        ('Two ways in',
         '<p>The <a href="/problems">problem collection</a> is for gaps that are still open: documented problems with possible solutions that people can test. The <a href="/guides">resource guides</a> cover problems that already have an answer, found by county or by what is going on in your life.</p>'),
        ('From a problem to a first step',
         '<p>Our problem briefs bring together published evidence, the people affected, possible solutions and a small local starting point. A solution might be a service, a neighborhood effort, a better process or a tool. It does not have to be an app.</p>'
         '<p>We label our proposals as ideas to test. They are not proven interventions, funded projects or open roles. Named organizations are sources or possible places to learn, not partners unless we explicitly say so.</p>'),
        ('Evidence before promises',
         '<p>Each brief links to its sources and explains where the evidence applies. We distinguish published research from our own proposals. These first briefs are based on existing reports; they are not original interviews with residents. Local conversations should shape any project before it starts.</p>'),
        ('Independent',
         '<p>MD Eagles is an independent publication. It is not affiliated with, endorsed by or operated by the State of Maryland or any government agency. Its colors are a tribute to the Maryland flag, not a sign of official status. Where we point to a public service, we link to the agency that runs it.</p>'),
        ('Stay in touch',
         '<p><a href="/#subscribe">Subscribe for publication updates</a>. We send a note when a new problem or follow-up is published.</p>'),
    ]
    head = band('About MD Eagles',
                '<p class="lead">Maryland has people ready to make things better. We help them find a useful place to start.</p>', pos=3, place='baltimore')
    body = (
        '<div class="page"><div class="prose-lead"><p>Maryland Eagles Eyes is an independent publication about problems facing people in our state and practical ways to help solve them. A resident organizing neighbors, a student starting a project, a business owner or a founder should be able to find work worth taking on here.</p></div>'
        + ''.join(f'<section class="split"><h2>{h}</h2><div class="prose">{b}</div></section>' for h, b in sections) + '</div>'
    )
    write(PUBLIC / 'about.html', page(
        'About MD Eagles',
        'Learn how MD Eagles identifies Maryland problems, examines published evidence and proposes practical local projects residents can take up.',
        '/about', head + body, current='about', dialog=True, scripts=('/subscribe.js',)))


# ----------------------------------------------------------- problem collection
def build_problems():
    form = '''<form class="directory-search" role="search" action="/problems"><div><label for="query">Search the collection</label><input id="query" name="q" type="search" maxlength="160" placeholder="Try child care, business or careers"></div><div><label for="topic">Topic</label><select id="topic" name="topic"><option value="">All topics</option><option value="families">Children and families</option><option value="business">Small business</option><option value="work">Work and careers</option></select></div><button class="button">Search</button></form>
<noscript><p>All problems are listed below. Search filters require JavaScript.</p></noscript>
<div class="results-heading"><p id="result-count" role="status" aria-live="polite">3 problems</p><a id="clear-search" href="/problems">Clear filters</a></div>'''
    head = band('The problem collection',
                '<p class="lead">Choose a problem. Understand the evidence. Weigh the possible solutions and find a first step you can take with people in your community.</p>'
                '<p class="band-note">Our first briefs pair published evidence with ideas to test. They are starting points for local work, not funded projects or proven solutions. Looking for help that already exists? See the <a href="/guides">resource guides</a>.</p>',
                pos=2, place='farm')
    body = ('<div class="page"><div class="wrap">' + form + f'<div class="cases">{cases(2)}</div>'
            '<section id="no-results" class="empty-results" hidden><h2>No matching problems yet</h2>'
            '<p>Try a broader search or <a href="/problems">browse all problems</a>. This collection is just beginning.</p></section></div></div>')
    write(PUBLIC / 'problems.html', page(
        'Problems to solve in Maryland',
        'Find documented Maryland challenges and possible local projects for residents, students, community groups, business owners and builders.',
        '/problems', head + body, current='problems', kind='CollectionPage', scripts=('/find-problems.js',),
        body_class='theme-night'))

    for i, x in enumerate(problems, 1):
        crumb = '<p class="breadcrumb"><a href="/problems">Problem collection</a> <span aria-hidden="true">/</span> Problem %02d</p>' % i
        lead = f'<p class="lead">{e(x["summary"])}</p><p class="band-cta"><a class="button" href="#start">Start with a local conversation {arrow()}</a></p>'
        facts = (
            '<dl class="fact-strip">'
            f'<div><dt>Place</dt><dd>{e(x["place"])}</dd></div>'
            f'<div><dt>Topic</dt><dd>{TOPICS[x["topic"]]}</dd></div><div><dt>Status</dt><dd>{STATUS}</dd></div>'
            f'<div><dt>Sources reviewed</dt><dd>{REVIEWED}</dd></div></dl>'
        )
        evidence = (f'<section class="split"><h2>What the evidence shows</h2><div class="prose"><p>{e(x["evidence"])}</p>'
                    f'<p class="source-note">Source: <a href="{e(x["url"])}">{e(x["source"])}</a>.</p></div></section>')
        solutions = (
            '<section class="solutions" aria-labelledby="solutions-title"><div class="solutions-head">'
            '<h2 id="solutions-title">Possible solutions to test</h2>'
            '<p>These are MD Eagles proposals, not projects already operating. Test the need with residents and existing services before building.</p></div>'
            f'<ol class="solution-list">{solutions_list(x, 3)}</ol></section>'
        )
        rest = [
            ('Your first step', f'<p>{e(x["first"])}</p><h3>Who to involve</h3><p>{e(x["people"])}</p><h3>What to measure</h3><p>{e(x["measure"])}</p>'),
            ('Build on what already exists',
             f'<p>Start by learning from <a href="{e(x["existing_url"])}">{e(x["existing"])}</a>. Ask what they already provide and what remains difficult. No partnership is implied.</p>'
             f'<p>Facing this yourself? <a href="/guides/{x["help"]}">Find an existing service in the resource guides</a>.</p>'),
            ('Take this brief with you',
             f'<p><a href="/downloads/{x["slug"]}.docx" download>Download the project worksheet (Word document)</a></p>'
             '<p>Use it to record local evidence, collaborators, costs and a small test before committing to a larger project. Opens in Word, Google Docs and Pages.</p>'),
        ]
        rest_html = ''.join(
            '<section class="split"%s><h2>%s</h2><div class="prose">%s</div></section>'
            % (' id="start"' if h == 'Your first step' else '', h, b) for h, b in rest)
        write(PUBLIC / 'problems' / f'{x["slug"]}.html', page(
            x['title'],
            x['summary'] + ' Read the evidence, explore proposed solutions and plan a first conversation in your Maryland community.',
            '/problems/' + x['slug'],
            band(e(x['title']), lead, crumb, pos=(i % 3) + 1, place=['farm', 'bridge', 'baltimore'][i % 3]) + '<div class="page">' + facts + evidence + solutions + rest_html + '</div>',
            current='problems'))
        worksheet_docx(x, PUBLIC / 'downloads' / f'{x["slug"]}.docx')

    script = (PUBLIC / 'find-guides.js').read_text().replace("'guide' : 'guides'", "'problem' : 'problems'")
    write(PUBLIC / 'find-problems.js', script)


# ----------------------------------------------------------- resource guides
def guide_row(g):
    searchable = ' '.join(str(g[k]) for k in ['title', 'summary', 'audience', 'keywords', 'category'])
    reach = 'campus' if g['slug'] == 'student-essentials' else 'local'
    return (
        f'<article class="guide" data-entry data-topic="{g["topic"]}" data-local="{reach}" data-search="{e(searchable)}">'
        f'<p class="guide-cat">{e(g["category"])}</p>'
        f'<div class="guide-main"><h2><a href="/guides/{g["slug"]}">{e(g["title"])}</a></h2>'
        f'<p>{e(g["summary"])}</p></div>'
        f'<div class="guide-side"><p class="result-scope">{e(g["scope"])}</p><p class="county-note" hidden></p></div></article>'
    )


def build_guides():
    options = ''.join(f'<option value="{g["topic"]}">{e(g["category"])}</option>' for g in guides)
    head = band('Help that already exists.',
                '<p class="lead">These problems already have an answer. Find it by county, or by what is going on in your life, then take the next step.</p>'
                '<p class="band-note">Looking to work on a gap that is still open? Explore the <a href="/problems">problem collection</a>.</p>',
                pos=1, place='annapolis')
    body = f'''<div class="page"><div class="wrap">
<form class="directory-search guide-search" role="search" action="/guides" method="get"><div><label for="guide-query">Search the guides</label><input id="guide-query" name="q" type="search" placeholder="Try “electric bill” or “child care”" maxlength="160" autocomplete="off"></div><div><label for="guide-county">Your county</label><select id="guide-county" name="county">{county_options('Anywhere in Maryland')}</select></div><div><label for="guide-topic">What you need</label><select id="guide-topic" name="topic"><option value="">All needs</option>{options}</select></div><button class="button" type="submit">Search</button></form>
<noscript><p>Search filters need JavaScript. All {len(guides)} guides are listed below for you to browse.</p></noscript>
<div class="results-heading"><p id="result-count" role="status" aria-live="polite" aria-atomic="true">{len(guides)} guides</p><span class="results-actions">{detect_only()}<a id="clear-search" href="/guides">Clear filters</a></span></div>
{detect_status()}
<div id="guide-results" class="guide-list">{''.join(guide_row(g) for g in guides)}</div>
<section id="no-results" class="empty-results" hidden><h2>No guide matches that search yet.</h2><p>Try a shorter phrase such as “rent,” “jobs” or “care.” You can also clear the filters and browse every guide.</p><a href="/guides">Browse all guides</a></section>
<p class="directory-note">An initial collection of {len(guides)} resource guides, checked against the linked providers on November 4, 2026. Most services are delivered through local offices, so a county choice reminds you to ask for yours; it does not guarantee availability. Each guide explains its coverage and limits.</p></div></div>'''
    write(PUBLIC / 'guides.html', page(
        'Find your next step in Maryland',
        'Browse practical Maryland resource guides for bills, housing, jobs, child care, business, college, health coverage and caregiving, by county or by what you need.',
        '/guides', head + body, current='guides', kind='CollectionPage', scripts=('/find-guides.js',)))

    for n, g in enumerate(guides):
        phone = ''
        if g.get('phone'):
            phone = (f'<p>Prefer to call? <a href="tel:{e(g["telephone"])}">{e(g["phone"])}</a> '
                     'is Maryland Health Connection’s consumer support number.</p>')
        steps = ''.join(f'<li>{e(s)}</li>' for s in g['steps'])
        related = ''.join(f'<li><a href="/guides/{s}">{e(guide_by_slug[s]["title"])}</a></li>' for s in g['related'])
        crumb = f'<p class="breadcrumb"><a href="/guides">Resource guides</a> <span aria-hidden="true">/</span> <a href="/guides?topic={g["topic"]}">{e(g["category"])}</a></p>'
        head = band(e(g['title']), f'<p class="lead">{e(g["summary"])}</p>', crumb, pos=(n % 3) + 1, place=['annapolis', 'bridge', 'sunset'][n % 3])
        body = f'''<div class="page">
<dl class="fact-strip"><div><dt>Who this is for</dt><dd>{e(g["audience"])}</dd></div><div><dt>Where it applies</dt><dd>{e(g["scope"])}</dd></div><div><dt>Sources checked</dt><dd><time datetime="{g["checked"]}">November 4, 2026</time></dd></div></dl>
<section class="split"><h2>Where to start</h2><div class="prose"><p>{e(g["intro"])}</p><p><a class="button resource-action" href="{e(g["url"])}">{e(g["action"])} <svg class="arrow" viewBox="0 0 20 20" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M6 14 14 6M7 6h7v7"/></svg></a></p><p class="provider-caption">Takes you to {e(g["source"])}.</p>{phone}</div></section>
<section class="split"><h2>Your next steps</h2><div class="prose"><ol class="action-steps">{steps}</ol></div></section>
<section class="split"><h2>A question to take with you</h2><div class="prose"><blockquote class="question-prompt">{e(g["ask"])}</blockquote></div></section>
<section class="split"><h2>Before you rely on it</h2><div class="prose"><p>{e(g["limit"])}</p><p class="source-note">Source: <a href="{e(g["url"])}">{e(g["source"])}</a>. Provider information can change. Confirm current details with the service. MD Eagles is a publication, not the service provider.</p></div></section>
<section class="split"><h2>You may also need</h2><div class="prose"><ul class="related-list">{related}</ul>
<p class="aside-help">Want to work on gaps like this one? <a href="/problems">Explore the problem collection</a>.</p></div></section></div>'''
        write(PUBLIC / 'guides' / f'{g["slug"]}.html', page(
            g['title'], g['summary'] + ' A practical starting point for Maryland residents, with provider links and questions to ask.',
            '/guides/' + g['slug'], head + body, current='guides'))


# -------------------------------------------------------------------- sitemap
def build_sitemap():
    paths = ['/' if f.stem == 'index' and f.parent == PUBLIC else '/' + str(f.relative_to(PUBLIC).with_suffix(''))
             for f in sorted(PUBLIC.rglob('*.html'))]
    urls = ''.join(f'<url><loc>{SITE}{p}</loc></url>' for p in paths)
    write(PUBLIC / 'sitemap.xml',
          '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + '</urlset>')


if __name__ == '__main__':
    build_home()
    build_about()
    build_problems()
    build_guides()
    build_sitemap()
    print('Built site.')
