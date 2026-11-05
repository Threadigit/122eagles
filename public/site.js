// Site-wide behaviour: floating navigation, mobile menu, pointer light, county memory.
// Everything here is progressive enhancement; the links and forms work without it.
(() => {
  const TZ = 'America/New_York';
  const KEY = 'mde-county';
  const county = {
    get() { try { return localStorage.getItem(KEY) || ''; } catch { return ''; } },
    set(value) { try { value ? localStorage.setItem(KEY, value) : localStorage.removeItem(KEY); } catch { /* private mode */ } },
    label(value) { return !value ? '' : /City|County/.test(value) ? value : `${value} County`; },
  };
  window.mdeCounty = county;

  const header = document.querySelector('[data-masthead]');
  const nav = document.querySelector('[data-island-nav]');
  const toggle = document.querySelector('[data-menu-toggle]');
  const menu = document.querySelector('[data-menu]');
  let menuOpen = false;

  /* ---- the sliding highlight in the island ---- */
  if (nav) {
    const pill = nav.querySelector('.island-pill');
    const links = [...nav.querySelectorAll('a')];
    const current = links.find(link => link.hasAttribute('aria-current'));
    const move = link => {
      if (!link || !nav.offsetWidth) { pill.style.opacity = '0'; return; }
      pill.style.setProperty('--x', `${link.offsetLeft}px`);
      pill.style.setProperty('--w', `${link.offsetWidth}px`);
      pill.style.opacity = '1';
    };
    const rest = () => move(current);
    links.forEach(link => {
      link.addEventListener('pointerenter', () => move(link));
      link.addEventListener('focus', () => move(link));
    });
    nav.addEventListener('pointerleave', rest);
    nav.addEventListener('focusout', event => { if (!nav.contains(event.relatedTarget)) rest(); });
    window.addEventListener('resize', rest);
    rest();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(rest);
  }

  /* ---- compact after a little scroll, hide going down, return going up ---- */
  if (header) {
    let last = window.scrollY;
    let queued = false;
    const update = () => {
      queued = false;
      const y = window.scrollY;
      header.toggleAttribute('data-scrolled', y > 40);
      if (!menuOpen) {
        if (y > 260 && y > last + 6) header.setAttribute('data-hidden', '');
        else if (y < last - 6 || y <= 260) header.removeAttribute('data-hidden');
      }
      last = y;
    };
    window.addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(update); } }, { passive: true });
    header.addEventListener('focusin', () => header.removeAttribute('data-hidden'));
    update();
  }

  /* ---- the full-screen menu on small screens ---- */
  if (toggle && menu) {
    const inertTargets = () => [document.querySelector('main'), document.querySelector('.site-footer')].filter(Boolean);
    const focusables = () => [toggle, ...menu.querySelectorAll('a')];
    const setMenu = open => {
      menuOpen = open;
      menu.hidden = !open;
      toggle.setAttribute('aria-expanded', String(open));
      toggle.querySelector('.menu-toggle-label').textContent = open ? 'Close' : 'Menu';
      document.body.toggleAttribute('data-menu-open', open);
      header.removeAttribute('data-hidden');
      inertTargets().forEach(el => el.toggleAttribute('inert', open));
      if (open) menu.querySelector('a').focus();
    };
    toggle.addEventListener('click', () => setMenu(!menuOpen));
    menu.addEventListener('click', event => { if (event.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', event => {
      if (!menuOpen) return;
      if (event.key === 'Escape') { setMenu(false); toggle.focus(); }
      if (event.key === 'Tab') {
        const items = focusables();
        const first = items[0];
        const last = items[items.length - 1];
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
    });
    window.matchMedia('(min-width: 761px)').addEventListener('change', event => { if (event.matches && menuOpen) setMenu(false); });
  }

  /* ---- Maryland time and the chosen county in the menu footer ---- */
  const menuClock = document.querySelector('[data-md-clock]');
  const menuCounty = document.querySelector('[data-menu-county]');
  const renderMenuFoot = () => {
    if (menuClock) {
      const time = new Intl.DateTimeFormat('en-US', { timeZone: TZ, hour: 'numeric', minute: '2-digit' }).format(new Date());
      menuClock.textContent = `${time} in Maryland`;
    }
    if (menuCounty) menuCounty.textContent = county.get() ? county.label(county.get()) : '';
  };
  renderMenuFoot();
  setInterval(renderMenuFoot, 30000);
  window.addEventListener('mde:county', renderMenuFoot);

  /* ---- a soft light that follows the pointer over interactive surfaces ---- */
  if (window.matchMedia('(pointer: fine)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    let frame = 0;
    document.addEventListener('pointermove', event => {
      const target = event.target.closest && event.target.closest('.spot');
      if (!target || frame) return;
      frame = requestAnimationFrame(() => {
        frame = 0;
        const box = target.getBoundingClientRect();
        target.style.setProperty('--mx', `${event.clientX - box.left}px`);
        target.style.setProperty('--my', `${event.clientY - box.top}px`);
      });
    }, { passive: true });
  }

  /* ---- the county tile map ---- */
  const tiles = [...document.querySelectorAll('[data-county]')];
  const caption = document.querySelector('[data-tile-caption]');
  if (tiles.length) {
    const fallback = caption ? caption.textContent : '';
    const markSelected = () => {
      const chosen = county.get();
      tiles.forEach(tile => (tile.dataset.county === chosen ? tile.setAttribute('aria-current', 'true') : tile.removeAttribute('aria-current')));
    };
    tiles.forEach(tile => {
      const show = () => { if (caption) caption.textContent = `${county.label(tile.dataset.county)}: see local help`; };
      const hide = () => { if (caption) caption.textContent = fallback; };
      tile.addEventListener('pointerenter', show);
      tile.addEventListener('focus', show);
      tile.addEventListener('pointerleave', hide);
      tile.addEventListener('blur', hide);
      tile.addEventListener('click', () => county.set(tile.dataset.county));
    });
    markSelected();
    window.addEventListener('mde:county', markSelected);
  }
})();
