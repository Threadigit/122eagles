"""Check real discovery journeys, search state, progressive enhancement and guide links."""
import os,json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
BASE=os.environ.get('EAGLES_TEST_URL','http://127.0.0.1:8014/').rstrip('/')
with sync_playwright() as p:
 options={'headless':True}
 if os.environ.get('EAGLES_BROWSER'):options['executable_path']=os.environ['EAGLES_BROWSER']
 browser=p.chromium.launch(**options)
 for width,height in [(320,740),(390,844),(844,390),(1440,1000)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(BASE+'/',wait_until='networkidle');page.evaluate('document.fonts.ready')
  assert page.locator('.film [data-open-subscribe]').count()==0
  assert page.locator('[data-entry]').count()==3
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert page.evaluate('document.getAnimations().length')==0
  page.screenshot(path=f'/tmp/md-home-{width}.png',full_page=True)
  page.goto(BASE+'/guides')
  page.get_by_label('Search the guides',exact=True).fill('electric bill')
  page.get_by_role('button',name='Search',exact=True).click()
  expect(page.locator('[data-entry]:visible')).to_have_count(1)
  assert 'utility-bills' in page.locator('[data-entry]:visible h2 a').get_attribute('href')
  page.reload();expect(page.locator('[data-entry]:visible')).to_have_count(1)
  page.get_by_role('link',name='Clear filters').click()
  expect(page.locator('[data-entry]:visible')).to_have_count(8)
  page.goto(BASE+'/guides?county=Howard&topic=housing');expect(page.locator('.county-note:visible')).to_contain_text('Howard County')
  page.goto(BASE+'/guides')
  for query,slug in [('daycare','child-care'),('laid off','career-support'),('cashflow','business-advice'),('résumé','career-support'),("I can't pay rent",'rental-housing')]:
   page.get_by_label('Search the guides',exact=True).fill(query)
   expect(page.locator('[data-entry]:visible')).to_have_count(1)
   assert slug in page.locator('[data-entry]:visible h2 a').get_attribute('href')
  page.get_by_label('Search the guides',exact=True).fill('<img src=x onerror=alert(1)>')
  expect(page.locator('#no-results')).to_be_visible()
  assert page.locator('#guide-results img').count()==0
  page.get_by_role('link',name='Clear filters').click()
  page.get_by_label('Browse by need').select_option('care')
  expect(page.locator('[data-entry]:visible')).to_have_count(1)
  page.screenshot(path=f'/tmp/md-directory-{width}.png',full_page=True)
  page.locator('[data-entry]:visible h2 a').click()
  expect(page.locator('h1')).to_contain_text('local starting point')
  assert page.locator('.resource-action').get_attribute('href').startswith('https://aging.maryland.gov/')
  page.screenshot(path=f'/tmp/md-guide-{width}.png',full_page=True)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.goto(BASE+'/guides?topic=missing&q=',wait_until='networkidle')
  expect(page.locator('[data-entry]:visible')).to_have_count(8)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not errors,errors
  print(f'PASS {width}px: home search, synonym matches, filter/reset, reload, empty state, guide action, no overflow/errors',flush=True)
  page.close()
 # All published guides have a working internal route and an explicit provider action.
 page=browser.new_page()
 data=json.loads((Path(__file__).resolve().parents[1]/'content/guides.json').read_text())
 for guide in data:
  response=page.goto(BASE+'/guides/'+guide['slug'])
  assert response.status==200
  expect(page.locator('.resource-action')).to_have_attribute('href',guide['url'])
  assert page.locator('time').get_attribute('datetime')==guide['checked']
 page.close()
 context=browser.new_context(java_script_enabled=False)
 page=context.new_page();page.goto(BASE+'/guides?q=jobs')
 assert page.locator('[data-entry]:visible').count()==8
 assert page.locator('noscript').is_visible()
 print('PASS all guide routes, provider links and no-JavaScript browsing',flush=True)
 context.close();browser.close()
