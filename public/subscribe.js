// The signup dialog. The form is ours; it posts the address straight to Buttondown (the email provider),
// which opens its own confirmation in a small window. Nothing from Buttondown loads until a reader submits.
(() => {
  const trigger = document.querySelector('[data-open-subscribe]');
  const dialog = document.querySelector('#subscribe-dialog');
  if (!trigger || !dialog) return;
  const form = dialog.querySelector('[data-subscribe-form]');
  const sent = dialog.querySelector('[data-signup-sent]');
  const email = form.querySelector('input[type=email]');

  const reset = () => { sent.hidden = true; form.hidden = false; };
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

  // Without this script the form still works: it posts to Buttondown in a new tab.
  form.addEventListener('submit', () => {
    // Called inside the submit gesture, so browsers allow the window. If one is blocked, the form falls back to a new tab.
    const popup = window.open('', 'buttondown-signup', 'popup,width=520,height=720');
    form.target = popup ? 'buttondown-signup' : '_blank';
    form.hidden = true;
    sent.hidden = false;
    sent.focus();
  });
  dialog.querySelector('[data-signup-again]').addEventListener('click', () => {
    reset();
    email.value = '';
    email.focus();
  });
})();
