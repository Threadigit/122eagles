// Load Buttondown's supported signup form only when a reader opens the dialog.
(() => {
  const trigger = document.querySelector('[data-open-subscribe]');
  const dialog = document.querySelector('#subscribe-dialog');
  if (!trigger || !dialog) return;
  const frame = dialog.querySelector('[data-subscribe-frame]');
  const loadForm = () => {
    frame.src = frame.dataset.src;
  };
  const openSignup = () => {
    dialog.showModal();
    dialog.scrollTop = 0;
    document.body.setAttribute('data-signup-open', '');
    if (!frame.hasAttribute('src')) loadForm();
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
  dialog.querySelector('.signup-reload').addEventListener('click', loadForm);
})();
