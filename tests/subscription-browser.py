"""Signup-dialog regression checks. The form is ours and the reader never leaves the page: the address goes to
Buttondown's create-subscriber endpoint and the result is shown in the dialog. Every Buttondown request is intercepted
and answered locally, so this test never subscribes anyone or sends email."""
import json,os,shutil
from playwright.sync_api import sync_playwright,expect
URL=os.environ.get('EAGLES_TEST_URL','http://127.0.0.1:8012/')
ENDPOINT='https://buttondown.com/api/emails/create-subscriber'
with sync_playwright() as p:
 executable=os.environ.get('EAGLES_BROWSER') or shutil.which('chromium')
 options={'headless':True}
 if executable:options.update(executable_path=executable,args=['--no-sandbox'])
 browser=p.chromium.launch(**options)
 for width,height in [(320,740),(390,844),(844,390),(1440,1000)]:
  context=browser.new_context(viewport={'width':width,'height':height},ignore_https_errors=True,reduced_motion='reduce')
  page=context.new_page()
  seen=[];answer={'status':201,'body':{'subscriber':{'type':'unactivated'}}}
  def handle(route):
   seen.append(route.request)
   headers={'access-control-allow-origin':'*','access-control-allow-headers':'content-type'}
   if route.request.method=='OPTIONS':return route.fulfill(status=200,headers=headers)
   route.fulfill(status=answer['status'],headers=headers,content_type='application/json',body=json.dumps(answer['body']))
  context.route('https://buttondown.com/**',handle)
  popups=[];context.on('page',lambda pg:popups.append(pg))
  page.goto(URL,wait_until='networkidle');page.evaluate('document.fonts.ready')
  assert seen==[],seen
  trigger=page.locator('[data-open-subscribe]')
  assert trigger.is_enabled()
  trigger.click();dialog=page.locator('#subscribe-dialog')
  assert dialog.evaluate('(e)=>e.open') and page.locator('iframe').count()==0
  assert seen==[],seen  # opening the dialog loads nothing from Buttondown
  form=page.locator('[data-subscribe-form]');email=form.locator('input[type=email]');sent=page.locator('[data-signup-sent]')
  assert email.evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')>=16  # keeps iOS from zooming
  bounds=dialog.bounding_box();assert bounds['x']>=0 and bounds['x']+bounds['width']<=width+.5
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  # client-side checks: nothing is sent for an empty or malformed address
  form.get_by_role('button',name='Subscribe').click()
  expect(page.locator('[data-signup-error]')).to_have_text('Enter your email address.')
  email.fill('not-an-email');form.get_by_role('button',name='Subscribe').click()
  expect(page.locator('[data-signup-error]')).to_contain_text('doesn’t look like an email')
  assert seen==[],seen
  # each answer Buttondown can give
  cases=[(201,{'subscriber':{'type':'unactivated'}},'Check your inbox.'),
         (201,{'subscriber':{'type':'regular'}},'You’re on the list.'),
         (400,{'subscriber':{'type':'regular'},'error':'Email already exists'},'You’re already on the list.'),
         (400,{'risk_scores':{},'error':'captcha'},'One more step.')]
  for status,body,title in cases:
   answer.update(status=status,body=body)
   email.fill('reader@example.com');form.get_by_role('button',name='Subscribe').click()
   expect(page.locator('[data-sent-title]')).to_have_text(title)
   expect(form).to_be_hidden();expect(sent).to_be_focused()
   assert page.url==URL and popups==[],'the reader must stay on the page'
   if status==201 and body['subscriber']['type']=='unactivated':
    post=[r for r in seen if r.method=='POST'][-1];sent_body=json.loads(post.post_data)
    assert sent_body['email_address']=='reader@example.com' and sent_body['newsletter_id']=='7dddd7e8-db8d-4109-9a55-79b5117e990c'
   if title=='One more step.':expect(page.get_by_role('button',name='Continue with Buttondown')).to_be_visible()
   else:expect(page.get_by_role('button',name='Continue with Buttondown')).to_be_hidden()
   page.get_by_role('button',name='Use a different address').click()
   expect(form).to_be_visible();expect(email).to_have_value('');expect(email).to_be_focused()
  # an error from Buttondown keeps the form and the address
  answer.update(status=500,body={})
  email.fill('reader@example.com');form.get_by_role('button',name='Subscribe').click()
  expect(page.locator('[data-signup-error]')).to_contain_text('couldn’t sign you up')
  expect(email).to_have_value('reader@example.com')
  page.get_by_role('button',name='Close signup').click()
  assert not dialog.evaluate('(e)=>e.open')
  expect(trigger).to_be_focused()
  trigger.click();expect(form).to_be_visible()  # reopening starts from the form again
  page.keyboard.press('Escape');assert not dialog.evaluate('(e)=>e.open')
  assert page.evaluate('document.getAnimations().length')==0
  page.screenshot(path=f'/tmp/eagles-signup-qa-{width}.png',full_page=True)
  print(f'PASS {width}px: in-page signup, no redirect, validation, every Buttondown answer, error recovery, close/focus, reduced motion',flush=True)
  context.close()
 browser.close()
