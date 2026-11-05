// The signup dialog. The form is ours and the reader never leaves the page: the address goes to Buttondown (our email
// provider) with the same request Buttondown's own embedded form makes, and the result is shown here.
// Without this script the form still works as a plain post to Buttondown in a new tab. If Buttondown asks for a
// spam check (which only it can show), a clearly labelled button continues in a small Buttondown window.
(() => {
  const trigger = document.querySelector('[data-open-subscribe]');
  const dialog = document.querySelector('#subscribe-dialog');
  if (!trigger || !dialog) return;
  const ENDPOINT = 'https://buttondown.com/api/emails/create-subscriber';
  const NEWSLETTER = '7dddd7e8-db8d-4109-9a55-79b5117e990c'; // Maryland Eagles Eyes on Buttondown (public)
  const form = dialog.querySelector('[data-subscribe-form]');
  const email = form.querySelector('input[type=email]');
  const submit = form.querySelector('[data-signup-submit]');
  const error = dialog.querySelector('[data-signup-error]');
  const sent = dialog.querySelector('[data-signup-sent]');
  const sentTitle = dialog.querySelector('[data-sent-title]');
  const sentBody = dialog.querySelector('[data-sent-body]');
  const proceed = dialog.querySelector('[data-signup-continue]');
  const looksLikeEmail = value => value.length <= 254 && /^[a-zA-Z0-9.'_%+\-!]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/.test(value);
  form.noValidate = true; // our own message below replaces the browser's bubble
  let busy = false;

  const clearError = () => { error.hidden = true; error.textContent = ''; email.removeAttribute('aria-invalid'); };
  const showError = text => { error.textContent = text; error.hidden = false; email.setAttribute('aria-invalid', 'true'); email.focus(); };
  const setBusy = on => {
    busy = on;
    submit.disabled = on;
    submit.textContent = on ? 'Subscribing…' : 'Subscribe';
    if (on) form.setAttribute('aria-busy', 'true'); else form.removeAttribute('aria-busy');
  };
  const reset = () => { clearError(); setBusy(false); sent.hidden = true; proceed.hidden = true; form.hidden = false; };
  const showSent = (title, body, withContinue = false) => {
    sentTitle.textContent = title;
    sentBody.textContent = body;
    proceed.hidden = !withContinue;
    form.hidden = true;
    sent.hidden = false;
    sent.focus();
  };

  const openSignup = () => {
    reset();
    dialog.showModal();
    dialog.scrollTop = 0;
    document.body.setAttribute('data-signup-open', '');
  };
  trigger.addEventListener('click', openSignup);
  if (location.hash === '#subscribe') openSignup();
  dialog.querySelector('[data-close-subscribe]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.removeAttribute('data-signup-open');
    trigger.focus();
  });
  email.addEventListener('input', () => { if (!error.hidden) clearError(); });

  // Buttondown's answers: a subscriber (created, or already known), a spam-check request, or an error.
  const interpret = (ok, data) => {
    const subscriber = data && data.subscriber;
    if (subscriber) {
      const pending = subscriber.type === 'unactivated';
      if (!ok || data.error || data.detail) {
        return pending
          ? { title: 'Check your inbox.', body: 'This address is already waiting for confirmation. Open the email from Buttondown and confirm it.' }
          : { title: 'You’re already on the list.', body: 'This address already gets Maryland Eagles Eyes. Nothing more to do.' };
      }
      return pending
        ? { title: 'Check your inbox.', body: 'We sent you an email to confirm your address. Open it and confirm, and you’re on the list.' }
        : { title: 'You’re on the list.', body: 'We’ll email you when a new brief or follow-up is published.' };
    }
    if (data && data.risk_scores) return { captcha: true };
    const detail = data && (data.error || data.detail);
    if (Array.isArray(detail) && detail.some(item => (item.loc || []).includes('email_address'))) return { invalid: true };
    return { failed: true };
  };

  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy) return;
    const address = email.value.trim();
    if (!looksLikeEmail(address)) { showError(address ? 'That doesn’t look like an email address. Check it and try again.' : 'Enter your email address.'); return; }
    clearError();
    setBusy(true);
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15000);
    try {
      const response = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email_address: address, newsletter_id: NEWSLETTER, metadata: {}, tags: [], turnstile_response_token: null, form_id: null }),
        signal: controller.signal,
        credentials: 'omit',
      });
      let data = null;
      try { data = await response.json(); } catch { /* not JSON */ }
      const result = interpret(response.ok, data);
      setBusy(false);
      if (result.title) showSent(result.title, result.body);
      else if (result.captcha) showSent('One more step.', 'Buttondown needs to check that you’re a person. This opens a small Buttondown window; your address is already filled in.', true);
      else if (result.invalid) showError('That doesn’t look like an email address. Check it and try again.');
      else showError('We couldn’t sign you up just now. Please try again in a moment.');
    } catch {
      setBusy(false);
      showError('We couldn’t reach the signup service. Check your connection and try again.');
    } finally {
      clearTimeout(timer);
    }
  });

  // The one place a Buttondown window opens: a spam check only Buttondown can show. A click opens it, so browsers allow it.
  proceed.addEventListener('click', () => {
    form.hidden = false; // keep the address in the form that posts
    const popup = window.open('', 'buttondown-signup', 'popup,width=520,height=720');
    form.target = popup ? 'buttondown-signup' : '_blank';
    HTMLFormElement.prototype.submit.call(form);
    form.hidden = true;
  });
  dialog.querySelector('[data-signup-again]').addEventListener('click', () => {
    reset();
    email.value = '';
    email.focus();
  });
})();
