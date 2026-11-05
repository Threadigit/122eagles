"""Signup-dialog regression checks. The form is ours and posts to Buttondown; every Buttondown request is
intercepted and answered locally, so this test never subscribes anyone or sends email."""
import os,shutil
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright,expect
URL=os.environ.get('EAGLES_TEST_URL','http://127.0.0.1:8012/')
ENDPOINT='https://buttondown.com/api/emails/embed-subscribe/eagles'
RESULT='<!doctype html><html lang="en"><body><p>Fixture: Buttondown confirmation</p></body></html>'
with sync_playwright() as p:
 executable=os.environ.get('EAGLES_BROWSER') or shutil.which('chromium')
 options={'headless':True}
 if executable:options.update(executable_path=executable,args=['--no-sandbox'])
 browser=p.chromium.launch(**options)
 for width,height in [(320,740),(390,844),(844,390),(1440,1000)]:
  context=browser.new_context(viewport={'width':width,'height':height},ignore_https_errors=True,reduced_motion='reduce')
  page=context.new_page()
  seen=[];posts=[]
  def handle(route):
   seen.append(route.request.url)
   if route.request.method=='POST':posts.append(parse_qs(route.request.post_data or ''))
   route.fulfill(status=200,content_type='text/html',body=RESULT)
  context.route('https://buttondown.com/**',handle)
  page.goto(URL,wait_until='networkidle');page.evaluate('document.fonts.ready')
  assert seen==[],seen
  trigger=page.locator('[data-open-subscribe]')
  assert trigger.is_enabled()
  assert page.get_by_role('heading',name='Fix what’s missing.').is_visible()
  trigger.click();dialog=page.locator('#subscribe-dialog')
  assert dialog.evaluate('(e)=>e.open')
  assert page.evaluate('document.body.hasAttribute("data-signup-open")')
  assert page.locator('iframe').count()==0
  assert seen==[],seen  # opening the dialog loads nothing from Buttondown
  form=page.locator('[data-subscribe-form]');email=form.locator('input[type=email]')
  assert form.get_attribute('action')==ENDPOINT and form.get_attribute('method')=='post'
  assert form.locator('input[name=embed]').get_attribute('value')=='1'
  expect(email).to_be_visible()
  assert email.evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')>=16  # keeps iOS from zooming
  email.fill('not-an-email');assert not email.evaluate('(e)=>e.checkValidity()')
  email.fill('');assert not email.evaluate('(e)=>e.checkValidity()')
  assert page.url==URL
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  bounds=dialog.bounding_box();assert bounds['x']>=0 and bounds['x']+bounds['width']<=width+.5
  assert bounds['y']>=0 and bounds['y']+bounds['height']<=height+.5 or width>height  # short landscape phones scroll the dialog
  # submit: the address goes to Buttondown in a separate window; the dialog says so
  email.fill('reader@example.com')
  with context.expect_page() as popup_info:form.get_by_role('button',name='Subscribe').click()
  popup=popup_info.value;popup.wait_for_load_state()
  assert posts and posts[0].get('email')==['reader@example.com'] and posts[0].get('embed')==['1'],posts
  assert page.url==URL
  expect(page.locator('[data-signup-sent]')).to_be_visible()
  expect(form).to_be_hidden()
  popup.close()
  page.get_by_role('button',name='Use a different address').click()
  expect(form).to_be_visible();expect(email).to_have_value('');expect(email).to_be_focused()
  page.get_by_role('button',name='Close signup').click()
  assert not dialog.evaluate('(e)=>e.open')
  page.locator('body:not([data-signup-open])').wait_for(state='attached')
  expect(trigger).to_be_focused()
  trigger.click()
  expect(form).to_be_visible()  # reopening starts from the form again
  page.get_by_role('button',name='Close signup').focus();page.keyboard.press('Escape')
  assert not dialog.evaluate('(e)=>e.open')
  expect(trigger).to_be_focused()
  assert page.evaluate('document.getAnimations().length')==0
  page.screenshot(path=f'/tmp/eagles-signup-qa-{width}.png',full_page=True)
  print(f'PASS {width}px: native form, nothing loaded from Buttondown until submit, validation, submit to Buttondown, sent state, close/focus, reduced motion',flush=True)
  context.close()
 browser.close()
