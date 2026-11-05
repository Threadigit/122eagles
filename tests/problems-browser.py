import os,json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
base=os.environ.get('EAGLES_TEST_URL','http://127.0.0.1:8014/').rstrip('/')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ['EAGLES_BROWSER'])
 for width in [320,390,844,1440]:
  page=b.new_page(viewport={'width':width,'height':900})
  page.goto(base)
  page.locator('.door a').first.click()
  page.wait_for_load_state('networkidle')
  expect(page.locator('[data-entry]')).to_have_count(3)
  page.get_by_label('Search the collection').fill('daycare')
  expect(page.locator('[data-entry]:visible')).to_have_count(1)
  page.reload();expect(page.locator('[data-entry]:visible')).to_have_count(1)
  page.locator('[data-entry]:visible h2 a').click()
  page.get_by_role('link',name='Start with a local conversation').click()
  assert page.url.endswith('#start')
  with page.expect_download() as download:page.get_by_role('link',name='Download the project worksheet (Word document)').click()
  assert download.value.suggested_filename.endswith('.docx')
  import zipfile;assert 'Your local project notes' in zipfile.ZipFile(download.value.path()).read('word/document.xml').decode()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=f'/tmp/md-problem-{width}.png',full_page=True)
  page.goto(base+'/problems?topic=business');expect(page.locator('[data-entry]:visible')).to_have_count(1)
  page.get_by_label('Search the collection').fill('zzzz');expect(page.locator('#no-results')).to_be_visible()
  page.get_by_role('link',name='Clear filters').click();expect(page.locator('[data-entry]:visible')).to_have_count(3)
  page.close();print(f'PASS {width}px: problem navigation, search, filters, download and layout',flush=True)
 context=b.new_context(java_script_enabled=False);page=context.new_page();page.goto(base+'/problems');expect(page.locator('[data-entry]')).to_have_count(3)
 for item in json.loads(Path('content/problems.json').read_text()):
  assert page.goto(base+'/problems/'+item['slug']).status==200
  expect(page.get_by_role('heading',name='Possible solutions to test')).to_be_visible()
 b.close()
