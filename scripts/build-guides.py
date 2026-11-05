"""Generate crawlable guide pages from reviewed editorial data. No runtime dependencies."""
import json,re,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PUBLIC=ROOT/'public'
guides=json.loads((ROOT/'content/guides.json').read_text())
e=lambda v:html.escape(v,quote=True)
base=(PUBLIC/'about.html').read_text()
identity=re.search(r'<a class="identity".*?</a>',base,re.S)[0]
nav=f'<header class="masthead">{identity}<nav class="site-nav" aria-label="Main navigation"><a href="/problems">Problems to solve</a><a href="/guides">Find help</a><a href="/about">About</a></nav></header>'
footer='<footer><a href="/">Maryland Eagles Eyes</a><div class="footer-links"><a href="/guides">All guides</a><a href="/about">About</a><a href="/#subscribe">Email updates</a></div></footer>'
def head(title,desc,path,kind='WebPage'):
 s=base[:base.index('<body')]
 s=re.sub(r'<title>.*?</title>',f'<title>{e(title)} | MD Eagles</title>',s)
 s=re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*',lambda m:m[1]+e(desc),s)
 s=re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*',lambda m:m[1]+e(title+' | MD Eagles'),s)
 s=s.replace('https://mdeagles.com/about','https://mdeagles.com'+path)
 schema={'@context':'https://schema.org','@type':kind,'name':title,'description':desc,'url':'https://mdeagles.com'+path,'inLanguage':'en-US','isPartOf':{'@id':'https://mdeagles.com/#website'}}
 s=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda m:'<script type="application/ld+json">'+json.dumps(schema)+'</script>',s)
 return s if '/discovery.css' in s else s.replace('</head>','<link rel="stylesheet" href="/discovery.css">\n</head>')
def card(g):
 searchable=' '.join(str(g[k]) for k in ['title','summary','audience','keywords','category'])
 return f'''<article class="guide-result" data-topic="{g['topic']}" data-search="{e(searchable)}"><p class="item-category">{e(g['category'])}</p><h2><a href="/guides/{g['slug']}">{e(g['title'])}<span aria-hidden="true"> ↗</span></a></h2><p>{e(g['summary'])}</p><p class="result-scope">{e(g['scope'])}</p></article>'''
options=''.join(f'<option value="{g["topic"]}">{e(g["category"])}</option>' for g in guides)
index=head('Find your next step in Maryland','Browse practical Maryland resource guides for bills, housing, jobs, child care, business, college, health coverage and caregiving.','/guides','CollectionPage')
index+='''<body class="information-page discovery-page"><a class="skip-link" href="#main">Skip to content</a>'''+nav+'''<main id="main" class="directory-main"><p class="section-kicker">The Maryland guide</p><h1>What do you need a hand with?</h1><p class="directory-intro">Start with your situation. Find a service, understand what to ask, and take the next step.</p>
<form class="guide-search directory-search" role="search" action="/guides" method="get"><div><label for="guide-query">Search the guides</label><input id="guide-query" name="q" type="search" placeholder="Try “electric bill” or “child care”" maxlength="160" autocomplete="off"></div><div><label for="guide-topic">Browse by need</label><select id="guide-topic" name="topic"><option value="">All needs</option>'''+options+'''</select></div><button class="primary-button" type="submit">Search</button></form>
<noscript><p>Search filters need JavaScript. All eight guides are listed below for you to browse.</p></noscript>
<div class="results-heading"><p id="result-count" role="status" aria-live="polite" aria-atomic="true">8 guides</p><a class="text-link" href="/guides" id="clear-search">Clear filters</a></div>
<div id="guide-results" class="guide-results">'''+''.join(card(g) for g in guides)+'''</div>
<section id="no-results" class="empty-results" hidden><h2>No guide matches that search yet.</h2><p>Try a shorter phrase such as “rent,” “jobs” or “care.” You can also clear the filters and browse every guide.</p><a class="text-link" href="/guides">Browse all guides</a></section>
<p class="directory-note">An initial collection of eight resource guides, checked against the linked providers on November 4, 2026. Each explains its coverage and limits. Local services and eligibility can vary.</p>
</main>'''+footer+'<script src="/find-guides.js" defer></script></body></html>'
(PUBLIC/'guides.html').write_text(index)
by_slug={g['slug']:g for g in guides}
for g in guides:
 desc=g['summary']+' A practical starting point for Maryland residents, with provider links and questions to ask.'
 page=head(g['title'],desc,'/guides/'+g['slug'])+'<body class="information-page guide-page"><a class="skip-link" href="#main">Skip to content</a>'+nav
 page+=f'''<main id="main"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="/guides">All guides</a><span aria-hidden="true"> / </span><a href="/guides?topic={g['topic']}">{e(g['category'])}</a></nav><p class="section-kicker">Resource guide</p><h1>{e(g['title'])}</h1><p class="page-intro">{e(g['summary'])}</p><p class="review-date">Sources checked <time datetime="{g['checked']}">November 4, 2026</time></p><dl class="guide-context"><div><dt>Who this is for</dt><dd>{e(g['audience'])}</dd></div><div><dt>Where it applies</dt><dd>{e(g['scope'])}</dd></div></dl><p>{e(g['intro'])}</p><a class="primary-button resource-action" href="{g['url']}">{e(g['action'])} <span aria-hidden="true">↗</span></a><p class="provider-caption">Takes you to {e(g['source'])}.</p><h2>Your next steps</h2><ol class="action-steps">'''+''.join(f'<li>{e(step)}</li>' for step in g['steps'])+f'''</ol><h2>A question to take with you</h2><blockquote class="question-prompt">{e(g['ask'])}</blockquote><h2>Before you rely on it</h2><p>{e(g['limit'])}</p><p class="source-note">Source: <a href="{g['url']}">{e(g['source'])}</a>. Provider information can change. Confirm current details with the service. MD Eagles is a publication, not the service provider.</p><section class="related-guides"><h2>You may also need</h2><ul>'''+''.join(f'<li><a href="/guides/{slug}">{e(by_slug[slug]["title"])}</a></li>' for slug in g['related'])+'</ul></section></main>'+footer+'</body></html>'
 if g.get('phone'):
  page=page.replace('<h2>Your next steps</h2>',f'<p>Prefer to call? <a class="text-link" href="tel:{g["telephone"]}">{e(g["phone"])}</a> is Maryland Health Connection’s consumer support number.</p><h2>Your next steps</h2>')
 (PUBLIC/'guides'/f'{g["slug"]}.html').write_text(page)
paths=['/' if f.stem=='index' else '/'+str(f.relative_to(PUBLIC).with_suffix('')) for f in sorted(PUBLIC.rglob('*.html'))]
(PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>https://mdeagles.com{path}</loc></url>' for path in paths)+'</urlset>')
print('Generated resource guides and sitemap.')
