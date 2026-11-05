"""Build every page of the site from content/*.json.

    python3 scripts/build.py

Writes: homepage, About, the problem collection and its briefs (plus worksheets),
the resource guides, the search script for the collection, and the sitemap.
"""
import json
from pathlib import Path

from layout import PUBLIC, ROOT, SITE, e, eagle, page

TOPICS = {'families': 'Children and families', 'business': 'Small business', 'work': 'Work and careers'}
REVIEWED = 'November 5, 2026'
STATUS = 'Ideas awaiting local testing'

problems = json.loads((ROOT / 'content/problems.json').read_text())
guides = json.loads((ROOT / 'content/guides.json').read_text())
guide_by_slug = {g['slug']: g for g in guides}


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


# ---------------------------------------------------------------- problem rows
def problem_row(x, number, level=3):
    searchable = ' '.join([x['title'], x['summary'], x['place'], TOPICS[x['topic']], x['keywords']])
    return (
        f'<article class="problem" data-entry data-topic="{x["topic"]}" data-search="{e(searchable)}">'
        f'<p class="problem-no" aria-label="Problem {number}">{number:02d}</p>'
        '<div class="problem-body">'
        f'<p class="problem-place">{e(x["place"])}</p>'
        f'<h{level}><a href="/problems/{x["slug"]}">{e(x["title"])}</a></h{level}>'
        f'<p>{e(x["summary"])}</p></div>'
        '<dl class="problem-facts">'
        f'<div><dt>Topic</dt><dd>{TOPICS[x["topic"]]}</dd></div>'
        f'<div><dt>Evidence</dt><dd>{e(x["source"])}</dd></div>'
        f'<div><dt>Status</dt><dd>{STATUS}</dd></div></dl></article>'
    )


def problem_rows(level):
    return ''.join(problem_row(x, i, level) for i, x in enumerate(problems, 1))


# ------------------------------------------------------------------- homepage
def build_home():
    film = f'''<section class="film" aria-labelledby="film-title">
<div class="film-frame"><div class="film-camera"><img class="film-img" src="/assets/bay-bridge-film-1920.webp" srcset="/assets/bay-bridge-film-960.webp 960w, /assets/bay-bridge-film-1920.webp 1920w" sizes="max(100vw, 110vh)" width="1920" height="1756" fetchpriority="high" decoding="async" alt="Aerial view of the two Chesapeake Bay Bridge spans crossing the open water."></div></div>
<div class="film-shade"></div>
{eagle("eagle film-eagle", "1.15")}
<div class="film-copy">
<h1 id="film-title">Find a Maryland problem <span>you can help solve.</span></h1>
<p class="film-lead">A growing collection of documented gaps in everyday Maryland life. Each comes with the evidence, ideas worth testing and a first conversation to have.</p>
<p class="film-actions"><a class="button button-light" href="/problems">Browse the problem collection</a><a class="film-link" href="/guides">Need help yourself? Resource guides</a></p>
</div>
<p class="film-credit"><a href="https://hdl.loc.gov/loc.pnp/highsm.14292">Chesapeake Bay Bridge · Carol M. Highsmith, Library of Congress</a></p>
</section>'''

    collection = f'''<section class="collection" id="problems" aria-labelledby="collection-title">
<div class="section-head"><h2 id="collection-title">The problem collection</h2>
<div><p>Each brief sets out who is affected, what the evidence shows and a first step to take locally. The ideas are proposals to test, not running projects.</p>
<p>Anyone can pick one up: neighbors, students, local businesses, community groups, founders. You do not need to write software.</p></div></div>
<div class="ledger">{problem_rows(3)}</div>
<p class="ledger-note">{len(problems)} problems documented so far. Briefs are added as their sources are checked. <a href="/problems">Search the collection</a></p>
</section>'''

    inside_items = [
        ('The evidence', 'What published research shows, where it applies and where it stops.'),
        ('Ideas to test', 'Practical proposals, labeled as untested.'),
        ('A first step', 'One conversation or small test you can start locally.'),
        ('Who to involve', 'The residents, providers and institutions worth talking to first.'),
        ('What to measure', 'What would show an idea is working, and what should make you stop.'),
        ('A worksheet', 'A plain-text download for recording what you learn.'),
    ]
    inside = (
        '<section class="inside" aria-labelledby="inside-title"><div class="inside-head">'
        '<h2 id="inside-title">Inside every brief</h2>'
        '<p>Built for someone who wants to start, not just read. See <a href="/about">how we choose and source them</a>.</p></div>'
        '<dl>' + ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in inside_items) + '</dl></section>'
    )

    guide_links = ''.join(
        f'<li><a href="/guides/{g["slug"]}"><span class="guide-title">{e(g["title"])}</span>'
        f'<span class="guide-cat">{e(g["category"])}</span></a></li>' for g in guides)
    help_band = f'''<section class="help" id="help" aria-labelledby="help-title"><div class="help-inner">
<div class="help-intro"><h2 id="help-title">Need help with something today?</h2>
<p>Resource guides point to Maryland services that already exist, with the questions worth asking and the limits worth knowing.</p>
<form class="home-search" role="search" action="/guides" method="get"><label for="home-query">What do you need help with?</label>
<div class="home-search-row"><input id="home-query" name="q" type="search" maxlength="160" placeholder="Try “electric bill” or “child care”" autocomplete="off"><button type="submit">Search guides</button></div></form></div>
<ul class="guide-index">{guide_links}</ul></div></section>'''

    updates = '''<section class="updates" id="subscribe" aria-labelledby="updates-title"><div class="updates-inner">
<h2 id="updates-title">Hear when a new problem is published.</h2>
<div><p>Free email, only when there is a new brief or a follow-up.</p>
<button class="button button-light" data-open-subscribe aria-haspopup="dialog" aria-controls="subscribe-dialog">Get email updates</button>
<noscript><p><a href="https://buttondown.com/eagles">Subscribe through Buttondown</a></p></noscript></div></div></section>'''

    desc = ('Explore documented Maryland problems, practical ideas residents can test and concrete first steps '
            'for local projects in their communities.')
    write(PUBLIC / 'index.html', page(
        'Find a Maryland problem you can help solve', desc, '/',
        film + collection + inside + help_band + updates,
        body_class='home', scripts=('/cinema.js', '/subscribe.js'), home=True, dialog=True))


# ---------------------------------------------------------------------- about
def build_about():
    sections = [
        ('From a problem to a first step',
         '<p>Our problem briefs bring together published evidence, the people affected, possible solutions and a small local starting point. A solution might be a service, a neighborhood effort, a better process or a tool. It does not have to be an app.</p>'
         '<p>We label our proposals as ideas to test. They are not proven interventions, funded projects or open roles. Named organizations are sources or possible places to learn, not partners unless we explicitly say so.</p>'),
        ('Evidence before promises',
         '<p>Each brief links to its sources and explains where the evidence applies. We distinguish published research from our own proposals. These first briefs are based on existing reports; they are not original interviews with residents. Local conversations should shape any project before it starts.</p>'),
        ('Help for what you are facing today',
         '<p>Our <a href="/guides">resource guides</a> point readers to existing Maryland services. The <a href="/problems">problem collection</a> is for people who want to work on the gaps.</p>'
         '<p><a href="/#subscribe">Subscribe for publication updates</a>.</p>'),
    ]
    body = (
        '<div class="page-head"><h1>About MD Eagles</h1>'
        '<p class="lead">Maryland has people ready to make things better. We help them find a useful place to start.</p></div>'
        '<div class="prose-lead"><p>Maryland Eagles Eyes is an independent publication about problems facing people in our state and practical ways to help solve them. A resident organizing neighbors, a student starting a project, a business owner or a founder should be able to find work worth taking on here.</p></div>'
        + ''.join(f'<section class="split"><h2>{h}</h2><div class="prose">{b}</div></section>' for h, b in sections)
    )
    write(PUBLIC / 'about.html', page(
        'About MD Eagles',
        'Learn how MD Eagles identifies Maryland problems, examines published evidence and proposes practical local projects residents can take up.',
        '/about', f'<div class="page">{body}</div>', current='about', dialog=True, scripts=('/subscribe.js',)))


# ----------------------------------------------------------- problem collection
def build_problems():
    form = '''<form class="directory-search" role="search" action="/problems"><div><label for="query">Search the collection</label><input id="query" name="q" type="search" maxlength="160" placeholder="Try child care, business or careers"></div><div><label for="topic">Topic</label><select id="topic" name="topic"><option value="">All topics</option><option value="families">Children and families</option><option value="business">Small business</option><option value="work">Work and careers</option></select></div><button>Search</button></form>
<noscript><p>All problems are listed below. Search filters require JavaScript.</p></noscript>
<div class="results-heading"><p id="result-count" role="status" aria-live="polite">3 problems</p><a id="clear-search" href="/problems">Clear filters</a></div>'''
    body = (
        '<div class="page"><div class="page-head"><h1>The problem collection</h1>'
        '<p class="lead">Choose a problem. Understand the evidence. Find a first step you can take with people in your community.</p>'
        '<p>Our first briefs pair published evidence with ideas to test. They are starting points for local work, not funded projects or proven solutions.</p></div>'
        + form + f'<div class="ledger">{problem_rows(2)}</div>'
        '<section id="no-results" class="empty-results" hidden><h2>No matching problems yet</h2>'
        '<p>Try a broader search or <a href="/problems">browse all problems</a>. This collection is just beginning.</p></section></div>'
    )
    write(PUBLIC / 'problems.html', page(
        'Problems to solve in Maryland',
        'Find documented Maryland challenges and possible local projects for residents, students, community groups, business owners and builders.',
        '/problems', body, current='problems', kind='CollectionPage', scripts=('/find-problems.js',)))

    for i, x in enumerate(problems, 1):
        ideas = ''.join(f'<h3>{e(t)}</h3><p>{e(c)}</p>' for t, c in x['ideas'])
        facts = (
            '<dl class="fact-strip">'
            f'<div><dt>Problem</dt><dd>{i:02d}</dd></div><div><dt>Place</dt><dd>{e(x["place"])}</dd></div>'
            f'<div><dt>Topic</dt><dd>{TOPICS[x["topic"]]}</dd></div><div><dt>Status</dt><dd>{STATUS}</dd></div>'
            f'<div><dt>Sources reviewed</dt><dd>{REVIEWED}</dd></div></dl>'
        )
        sections = [
            ('What the evidence shows', f'<p>{e(x["evidence"])}</p><p class="source-note">Source: <a href="{e(x["url"])}">{e(x["source"])}</a>.</p>'),
            ('Possible solutions to test',
             f'<p>These are MD Eagles proposals, not projects already operating. Test the need with residents and existing services before building.</p>{ideas}'),
            ('Your first step', f'<p>{e(x["first"])}</p><h3>Who to involve</h3><p>{e(x["people"])}</p><h3>What to measure</h3><p>{e(x["measure"])}</p>'),
            ('Build on what already exists',
             f'<p>Start by learning from <a href="{e(x["existing_url"])}">{e(x["existing"])}</a>. Ask what they already provide and what remains difficult. No partnership is implied.</p>'),
            ('Take this brief with you',
             f'<p><a href="/downloads/{x["slug"]}.md" download>Download the project worksheet (plain text)</a></p>'
             '<p>Use it to record local evidence, collaborators, costs and a small test before committing to a larger project.</p>'),
        ]
        sections_html = ''.join(
            '<section class="split"%s><h2>%s</h2><div class="prose">%s</div></section>'
            % (' id="start"' if h == 'Your first step' else '', h, b) for h, b in sections)
        body = (
            '<div class="page"><p class="breadcrumb"><a href="/problems">Problem collection</a></p>'
            f'<div class="page-head"><h1>{e(x["title"])}</h1><p class="lead">{e(x["summary"])}</p>'
            '<p><a class="button" href="#start">Start with a local conversation</a></p></div>'
            + facts + sections_html +
            f'<p class="aside-help">Facing this yourself? <a href="/guides/{x["help"]}">Find an existing service</a>.</p></div>'
        )
        write(PUBLIC / 'problems' / f'{x["slug"]}.html', page(
            x['title'],
            x['summary'] + ' Read the evidence, explore proposed solutions and plan a first conversation in your Maryland community.',
            '/problems/' + x['slug'], body, current='problems'))
        ideas_text = ''.join(f'### {a}\n{b}\n\n' for a, b in x['ideas'])
        write(PUBLIC / 'downloads' / f'{x["slug"]}.md',
              f'# {x["title"]}\n\nMD Eagles | {SITE}/problems/{x["slug"]}\nReviewed {REVIEWED}. Proposals, not proven solutions.\n\n'
              f'## Evidence\n{x["evidence"]}\nSource: {x["url"]}\n\n## Ideas to test\n{ideas_text}'
              f'## First step\n{x["first"]}\n\n## People to involve\n{x["people"]}\n\n## Measure\n{x["measure"]}\n\n'
              f'## Existing service\n{x["existing_url"]}\n\n## Your local project notes\n'
              '- City or county:\n- What residents told us (with permission):\n- Existing services and the remaining gap:\n'
              '- Smallest useful test:\n- Who will run it:\n- Costs and required permissions:\n'
              '- How we will measure improvement:\n- Review date and reasons to stop or change direction:\n')

    script = (PUBLIC / 'find-guides.js').read_text().replace("'guide' : 'guides'", "'problem' : 'problems'")
    write(PUBLIC / 'find-problems.js', script)


# ----------------------------------------------------------- resource guides
def guide_row(g):
    searchable = ' '.join(str(g[k]) for k in ['title', 'summary', 'audience', 'keywords', 'category'])
    return (
        f'<article class="guide" data-entry data-topic="{g["topic"]}" data-search="{e(searchable)}">'
        f'<p class="guide-cat">{e(g["category"])}</p>'
        f'<h2><a href="/guides/{g["slug"]}">{e(g["title"])}</a></h2>'
        f'<p>{e(g["summary"])}</p><p class="result-scope">{e(g["scope"])}</p></article>'
    )


def build_guides():
    options = ''.join(f'<option value="{g["topic"]}">{e(g["category"])}</option>' for g in guides)
    body = f'''<div class="page"><div class="page-head"><h1>What do you need a hand with?</h1>
<p class="lead">Start with your situation. Find a service, understand what to ask, and take the next step.</p></div>
<form class="guide-search directory-search" role="search" action="/guides" method="get"><div><label for="guide-query">Search the guides</label><input id="guide-query" name="q" type="search" placeholder="Try “electric bill” or “child care”" maxlength="160" autocomplete="off"></div><div><label for="guide-topic">Browse by need</label><select id="guide-topic" name="topic"><option value="">All needs</option>{options}</select></div><button type="submit">Search</button></form>
<noscript><p>Search filters need JavaScript. All {len(guides)} guides are listed below for you to browse.</p></noscript>
<div class="results-heading"><p id="result-count" role="status" aria-live="polite" aria-atomic="true">{len(guides)} guides</p><a id="clear-search" href="/guides">Clear filters</a></div>
<div id="guide-results" class="guide-list">{''.join(guide_row(g) for g in guides)}</div>
<section id="no-results" class="empty-results" hidden><h2>No guide matches that search yet.</h2><p>Try a shorter phrase such as “rent,” “jobs” or “care.” You can also clear the filters and browse every guide.</p><a href="/guides">Browse all guides</a></section>
<p class="directory-note">An initial collection of {len(guides)} resource guides, checked against the linked providers on November 4, 2026. Each explains its coverage and limits. Local services and eligibility can vary.</p></div>'''
    write(PUBLIC / 'guides.html', page(
        'Find your next step in Maryland',
        'Browse practical Maryland resource guides for bills, housing, jobs, child care, business, college, health coverage and caregiving.',
        '/guides', body, current='guides', kind='CollectionPage', scripts=('/find-guides.js',)))

    for g in guides:
        phone = ''
        if g.get('phone'):
            phone = (f'<p>Prefer to call? <a href="tel:{e(g["telephone"])}">{e(g["phone"])}</a> '
                     'is Maryland Health Connection’s consumer support number.</p>')
        steps = ''.join(f'<li>{e(s)}</li>' for s in g['steps'])
        related = ''.join(f'<li><a href="/guides/{s}">{e(guide_by_slug[s]["title"])}</a></li>' for s in g['related'])
        body = f'''<div class="page"><p class="breadcrumb"><a href="/guides">Resource guides</a> <span aria-hidden="true">/</span> <a href="/guides?topic={g["topic"]}">{e(g["category"])}</a></p>
<div class="page-head"><h1>{e(g["title"])}</h1><p class="lead">{e(g["summary"])}</p></div>
<dl class="fact-strip"><div><dt>Who this is for</dt><dd>{e(g["audience"])}</dd></div><div><dt>Where it applies</dt><dd>{e(g["scope"])}</dd></div><div><dt>Sources checked</dt><dd><time datetime="{g["checked"]}">November 4, 2026</time></dd></div></dl>
<section class="split"><h2>Where to start</h2><div class="prose"><p>{e(g["intro"])}</p><p><a class="button resource-action" href="{e(g["url"])}">{e(g["action"])}</a></p><p class="provider-caption">Takes you to {e(g["source"])}.</p>{phone}</div></section>
<section class="split"><h2>Your next steps</h2><div class="prose"><ol class="action-steps">{steps}</ol></div></section>
<section class="split"><h2>A question to take with you</h2><div class="prose"><blockquote class="question-prompt">{e(g["ask"])}</blockquote></div></section>
<section class="split"><h2>Before you rely on it</h2><div class="prose"><p>{e(g["limit"])}</p><p class="source-note">Source: <a href="{e(g["url"])}">{e(g["source"])}</a>. Provider information can change. Confirm current details with the service. MD Eagles is a publication, not the service provider.</p></div></section>
<section class="split"><h2>You may also need</h2><div class="prose"><ul class="related-list">{related}</ul></div></section></div>'''
        write(PUBLIC / 'guides' / f'{g["slug"]}.html', page(
            g['title'], g['summary'] + ' A practical starting point for Maryland residents, with provider links and questions to ask.',
            '/guides/' + g['slug'], body, current='guides'))


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
