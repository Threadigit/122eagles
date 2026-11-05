"""Signup-dialog regression checks. Live mode reads the provider form; never subscribes."""
import os,shutil
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright,expect
URL=os.environ.get('EAGLES_TEST_URL','http://127.0.0.1:8012/')
EMBED='https://buttondown.com/eagles?as_embed=true'
FIXTURE='''<!doctype html><html lang="en"><body><form><label>Email <input type="email" required></label><button type="submit">Subscribe</button></form></body></html>'''
with sync_playwright() as p:
 executable=os.environ.get('EAGLES_BROWSER') or shutil.which('chromium')
 options={'headless':True}
 if executable:options.update(executable_path=executable,args=['--no-sandbox'])
 browser=p.chromium.launch(**options)
 for width,height in [(320,740),(390,844),(844,390),(1440,1000)]:
  page=browser.new_page(viewport={'width':width,'height':height},ignore_https_errors=True,reduced_motion='reduce')
  requests=[];page.on('request',lambda r:requests.append(r.url) if urlparse(r.url).hostname=='buttondown.com' else None)
  page.route(EMBED,lambda r:r.fulfill(status=200,content_type='text/html',body=FIXTURE))
  page.goto(URL,wait_until='networkidle');page.evaluate('document.fonts.ready')
  assert requests==[],requests
  trigger=page.locator('[data-open-subscribe]')
  assert trigger.is_enabled()
  assert page.get_by_role('heading',name='Fix what’s missing.').is_visible()
  trigger.click();dialog=page.locator('#subscribe-dialog')
  assert dialog.evaluate('(e)=>e.open')
  assert page.evaluate('document.body.hasAttribute("data-signup-open")')
  frame=page.frame_locator('[data-subscribe-frame]');email=frame.locator('input[type=email]')
  email.wait_for(state='visible')
  assert requests==[EMBED],requests
  email.fill('not-an-email');assert not email.evaluate('(e)=>e.checkValidity()')
  assert page.url==URL
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  bounds=dialog.bounding_box();assert bounds['x']>=0 and bounds['x']+bounds['width']<=width+.5
  assert bounds['y']>=0 and bounds['y']+bounds['height']<=height+.5
  page.get_by_role('button',name='Close signup').click()
  assert not dialog.evaluate('(e)=>e.open')
  page.locator('body:not([data-signup-open])').wait_for(state='attached')
  expect(trigger).to_be_focused()
  trigger.click();assert len(requests)==1
  page.get_by_role('button',name='Close signup').focus();page.keyboard.press('Escape')
  assert not dialog.evaluate('(e)=>e.open')
  expect(trigger).to_be_focused()
  trigger.click()
  page.get_by_role('button',name='Reload signup form').scroll_into_view_if_needed()
  with page.expect_request(EMBED):page.get_by_role('button',name='Reload signup form').click()
  assert len(requests)==2,requests
  assert page.evaluate('document.getAnimations().length')==0
  page.screenshot(path=f'/tmp/eagles-signup-qa-{width}.png',full_page=True)
  print(f'PASS {width}px: copy, lazy signup, validation, same-page modal, close/focus, cached reopening, reload and reduced motion',flush=True)
  page.close()
 if os.environ.get('EAGLES_LIVE_FORM')=='1':
  page=browser.new_page(viewport={'width':390,'height':844},ignore_https_errors=True,reduced_motion='reduce')
  posts=[];page.on('request',lambda r:posts.append(r.url) if r.method=='POST' and urlparse(r.url).path!='/cdn-cgi/rum' else None)
  page.goto(URL,wait_until='networkidle')
  trigger=page.locator('[data-open-subscribe]');trigger.click()
  email=page.frame_locator('[data-subscribe-frame]').locator('input[type=email]').first
  email.wait_for(state='visible',timeout=30000)
  email.fill('not-an-email');assert not email.evaluate('(e)=>e.checkValidity()')
  email.fill('reader@example.com');assert email.evaluate('(e)=>e.checkValidity()')
  email.fill('')
  assert page.url==URL
  assert posts==[],posts
  page.screenshot(path='/tmp/eagles-live-signup.png',full_page=True)
  page.get_by_role('button',name='Close signup').click()
  expect(trigger).to_be_focused()
  print('PASS live Buttondown form rendered in place; email validation checked; no subscription/email sent',flush=True)
 browser.close()

# Read-only provider preview: Buttondown exposes confirmation via query state.
# This displays its real outcome UI without posting an address or sending mail.
if os.environ.get('EAGLES_LIVE_CONFIRMATION')=='1':
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
  for width,height in [(320,740),(390,844),(844,390),(1440,1000)]:
   page=browser.new_page(viewport={'width':width,'height':height},ignore_https_errors=True,reduced_motion='reduce')
   posts=[];page.on('request',lambda r:posts.append(r.url) if r.method=='POST' and urlparse(r.url).hostname=='buttondown.com' and urlparse(r.url).path!='/cdn-cgi/rum' else None)
   page.goto(URL,wait_until='networkidle');page.locator('[data-open-subscribe]').click()
   page.locator('[data-subscribe-frame]').evaluate("e=>e.src=e.dataset.src+'&state=confirmation_required&email_address=maryland.reader.preview%40gmail.com'")
   frame=page.frame_locator('[data-subscribe-frame]')
   message=frame.locator('.subscription-success-message')
   expect(message).to_be_visible(timeout=30000)
   gmail=frame.get_by_role('link',name='Take me to Gmail')
   expect(gmail).to_be_visible(timeout=15000)
   # Wait for the provider sheet transition before checking its actual geometry.
   page.wait_for_timeout(400)
   assert message.evaluate('e=>{const r=e.getBoundingClientRect();const actions=e.parentElement.nextElementSibling.getBoundingClientRect();return r.top>=0&&r.bottom<=actions.top+.5&&actions.bottom<=innerHeight+.5}'), 'Provider confirmation overlaps its actions'
   assert gmail.evaluate("e=>getComputedStyle(e).backgroundColor")=='rgb(23, 43, 54)', 'Provider brand colour changed'
   # A short landscape viewport may scroll; closing must remain visible throughout.
   page.locator('#subscribe-dialog').evaluate('e=>e.scrollTop=e.scrollHeight')
   close=page.get_by_role('button',name='Close signup');rect=close.bounding_box()
   assert rect['y']>=0 and rect['y']+rect['height']<=height
   frame.get_by_role('button',name='Got it').click()
   expect(message).not_to_be_visible()
   expect(frame.locator('input[type=email]').first).to_be_visible()
   close.click();assert not page.locator('#subscribe-dialog').evaluate('e=>e.open')
   assert not posts,posts
   print(f'PASS {width}px: actual provider confirmation, full message/actions, navy branding, sticky close, no subscription sent',flush=True)
   page.close()
  browser.close()
