"""Signup-dialog regression checks. Live mode reads the provider form; never subscribes."""
import os,shutil
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright,expect
URL=os.environ.get('EAGLES_TEST_URL','http://127.0.0.1:8012/')
EMBED='https://buttondown.com/eagles?as_embed=true'
FIXTURE='''<!doctype html><html lang="en"><body><form><label>Email <input type="email" required></label><button type="submit">Subscribe</button></form></body></html>'''
with sync_playwright() as p:
 executable=shutil.which('chromium')
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
  assert page.get_by_role('heading',name='Maryland, made clear.').is_visible()
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
  with page.expect_request(EMBED):page.get_by_role('button',name='Reload signup form').click()
  assert len(requests)==2,requests
  assert page.evaluate('document.getAnimations().length')==0
  page.screenshot(path=f'/tmp/eagles-signup-qa-{width}.png',full_page=True)
  print(f'PASS {width}px: copy, lazy signup, validation, same-page modal, close/focus, cached reopening, reload and reduced motion',flush=True)
  page.close()
 if os.environ.get('EAGLES_LIVE_FORM')=='1':
  page=browser.new_page(viewport={'width':390,'height':844},ignore_https_errors=True,reduced_motion='reduce')
  posts=[];page.on('request',lambda r:posts.append(r.url) if r.method=='POST' else None)
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
