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


  /* ---- detect the county from the device's location ----
     The coordinates are compared with the county shapes inside this browser and are
     never sent or stored; only the county name is remembered. */
  const detectButtons = [...document.querySelectorAll('[data-detect-county]')];
  const detect = (() => {
    let shapes = null;
    const load = async () => {
      if (!shapes) shapes = (await (await fetch('/assets/md-counties.json')).json()).counties;
      return shapes;
    };
    const inRing = (x, y, ring) => {
      let inside = false;
      for (let i = 0, j = ring.length - 2; i < ring.length; j = i, i += 2) {
        const xi = ring[i], yi = ring[i + 1], xj = ring[j], yj = ring[j + 1];
        if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside;
      }
      return inside;
    };
    const inPolygon = (polygon, x, y) => inRing(x, y, polygon[0]) && !polygon.slice(1).some(hole => inRing(x, y, hole));
    const find = (lon, lat, list) => {
      for (const c of list) {
        const [x0, y0, x1, y1] = c.b;
        if (lon < x0 || lon > x1 || lat < y0 || lat > y1) continue;
        if (c.p.some(polygon => inPolygon(polygon, lon, lat))) return c.n;
      }
      // The shapes are simplified, so allow about a kilometre of slack at the edge.
      const kx = Math.cos((lat * Math.PI) / 180) * 111.32;
      let best = null, bestDistance = 1.5;
      for (const c of list) for (const polygon of c.p) {
        const ring = polygon[0];
        for (let i = 0; i < ring.length; i += 2) {
          const d = Math.hypot((ring[i] - lon) * kx, (ring[i + 1] - lat) * 110.57);
          if (d < bestDistance) { bestDistance = d; best = c.n; }
        }
      }
      return best;
    };
    const say = text => document.querySelectorAll('[data-detect-status]').forEach(el => { el.textContent = text; });
    const busy = on => detectButtons.forEach(b => (on ? b.setAttribute('aria-busy', 'true') : b.removeAttribute('aria-busy')));
    const run = ({ silent = false } = {}) => new Promise(resolve => {
      if (!('geolocation' in navigator)) { if (!silent) say('This browser cannot share its location. Choose your county instead.'); return resolve(null); }
      busy(true);
      if (!silent) say('Looking up your county…');
      navigator.geolocation.getCurrentPosition(async position => {
        try {
          const name = find(position.coords.longitude, position.coords.latitude, await load());
          if (name) {
            county.set(name);
            window.dispatchEvent(new Event('mde:county'));
            say(`Detected ${county.label(name)}. Not right? Choose another.`);
          } else if (!silent) say('Your location looks to be outside Maryland, or out on the water. Choose your county instead.');
          resolve(name);
        } catch { if (!silent) say('Could not check your location. Choose your county instead.'); resolve(null); }
        finally { busy(false); }
      }, error => {
        busy(false);
        if (!silent) say(error.code === 1 ? 'Location is blocked for this site. Choose your county instead.' : 'Could not find your location. Choose your county instead.');
        resolve(null);
      }, { enableHighAccuracy: false, timeout: 12000, maximumAge: 600000 });
    });
    return { run, find: async (lon, lat) => find(lon, lat, await load()) };
  })();
  window.mdeDetect = detect;
  detectButtons.forEach(button => button.addEventListener('click', () => detect.run()));
  // Detect automatically when the reader has already allowed location for this site.
  if (detectButtons.length && !county.get() && navigator.permissions && navigator.permissions.query) {
    navigator.permissions.query({ name: 'geolocation' }).then(result => { if (result.state === 'granted') detect.run({ silent: true }); }).catch(() => {});
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
