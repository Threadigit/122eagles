// The homepage welcome: a greeting, Maryland's clock and daylight, and a sky that follows them.
// Maryland's sun comes from NOAA's solar equations; nothing is sent anywhere.
(() => {
  const film = document.querySelector('[data-film]');
  const panel = document.querySelector('[data-clock]');
  if (!film || !panel) return;

  const TZ = 'America/New_York';
  const LAT = 38.9784; // Annapolis
  const LON = -76.4922;
  const county = window.mdeCounty || { get: () => '', set() {}, label: v => v };
  const $ = selector => panel.querySelector(selector);
  const greetingEl = document.querySelector('[data-greeting]');
  const subEl = document.querySelector('[data-greeting-sub]');
  const pick = document.querySelector('[data-county-pick]');

  // On localhost only, ?demo=2026-11-05T17:30 previews a Maryland wall-clock time.
  const local = ['localhost', '127.0.0.1', '[::1]'].includes(location.hostname);
  const demoParam = local ? new URLSearchParams(location.search).get('demo') : null;
  const started = Date.now();
  const mdFormatter = new Intl.DateTimeFormat('en-US', {
    timeZone: TZ, hourCycle: 'h23', year: 'numeric', month: 'numeric', day: 'numeric',
    hour: 'numeric', minute: 'numeric', second: 'numeric',
  });
  const mdParts = date => Object.fromEntries(mdFormatter.formatToParts(date).filter(p => p.type !== 'literal').map(p => [p.type, Number(p.value)]));
  const offsetMinutes = date => {
    const p = mdParts(date);
    return (Date.UTC(p.year, p.month - 1, p.day, p.hour, p.minute, p.second) - Math.floor(date.getTime() / 1000) * 1000) / 60000;
  };
  const demoBase = (() => {
    if (!demoParam) return null;
    const m = demoParam.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})$/);
    if (!m) return null;
    const wall = Date.UTC(+m[1], +m[2] - 1, +m[3], +m[4], +m[5]);
    let guess = new Date(wall);
    guess = new Date(wall - offsetMinutes(guess) * 60000);
    return new Date(wall - offsetMinutes(guess) * 60000).getTime();
  })();
  const now = () => new Date(demoBase ? demoBase + (Date.now() - started) : Date.now());

  // NOAA solar equations: sunrise and sunset as minutes after local midnight in Maryland.
  const sunTimes = date => {
    const p = mdParts(date);
    const dayOfYear = Math.round((Date.UTC(p.year, p.month - 1, p.day) - Date.UTC(p.year, 0, 0)) / 864e5);
    const g = (2 * Math.PI / 365) * (dayOfYear - 1);
    const eqt = 229.18 * (0.000075 + 0.001868 * Math.cos(g) - 0.032077 * Math.sin(g) - 0.014615 * Math.cos(2 * g) - 0.040849 * Math.sin(2 * g));
    const decl = 0.006918 - 0.399912 * Math.cos(g) + 0.070257 * Math.sin(g) - 0.006758 * Math.cos(2 * g) + 0.000907 * Math.sin(2 * g) - 0.002697 * Math.cos(3 * g) + 0.00148 * Math.sin(3 * g);
    const lat = LAT * Math.PI / 180;
    const cosHa = Math.cos(90.833 * Math.PI / 180) / (Math.cos(lat) * Math.cos(decl)) - Math.tan(lat) * Math.tan(decl);
    const ha = Math.acos(Math.max(-1, Math.min(1, cosHa))) * 180 / Math.PI;
    const shift = offsetMinutes(date);
    const wrap = m => ((m % 1440) + 1440) % 1440;
    return { rise: wrap(720 - 4 * (LON + ha) - eqt + shift), set: wrap(720 - 4 * (LON - ha) - eqt + shift) };
  };

  const phaseOf = (minute, sun) => {
    if (minute >= sun.rise - 40 && minute < sun.rise + 60) return 'dawn';
    if (minute >= sun.rise + 60 && minute < sun.set - 90) return 'day';
    if (minute >= sun.set - 90 && minute < sun.set + 5) return 'golden';
    if (minute >= sun.set + 5 && minute < sun.set + 45) return 'dusk';
    return 'night';
  };
  const skyLine = {
    dawn: 'First light over the Bay.',
    day: 'A bright day across Maryland.',
    golden: 'The light is going golden over the Bay.',
    dusk: 'Dusk is settling over the Bay.',
    night: 'The Bay is quiet tonight.',
  };
  const greetingFor = hour => (hour >= 5 && hour < 12 ? 'Good morning' : hour >= 12 && hour < 17 ? 'Good afternoon' : hour >= 17 && hour < 21 ? 'Good evening' : 'Still up');

  const clockFormat = (date, zone) => new Intl.DateTimeFormat('en-US', { timeZone: zone, hour: 'numeric', minute: '2-digit', hour12: true });
  const clock = clockFormat(null, TZ);
  const dateFormat = new Intl.DateTimeFormat('en-US', { timeZone: TZ, weekday: 'long', month: 'long', day: 'numeric' });
  const zoneFormat = new Intl.DateTimeFormat('en-US', { timeZone: TZ, timeZoneName: 'short' });
  const visitorZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const clockTime = (minute) => {
    const h = Math.floor(minute / 60);
    const m = Math.floor(minute % 60);
    const period = h >= 12 ? 'PM' : 'AM';
    return `${h % 12 || 12}:${String(m).padStart(2, '0')} ${period}`;
  };

  const place = (point, sun, minute) => {
    const dot = $('[data-sun-dot]');
    const t = (minute - sun.rise) / (sun.set - sun.rise);
    if (t >= 0 && t <= 1) {
      const angle = Math.PI * (1 - t);
      dot.setAttribute('cx', (120 + 104 * Math.cos(angle)).toFixed(1));
      dot.setAttribute('cy', (60 - 52 * Math.sin(angle)).toFixed(1));
      dot.classList.remove('is-moon');
    } else {
      dot.setAttribute('cx', minute < sun.rise ? '16' : '224');
      dot.setAttribute('cy', '60');
      dot.classList.add('is-moon');
    }
  };

  let lastDay = '';
  let sun = null;
  const render = () => {
    const date = now();
    const p = mdParts(date);
    const minute = p.hour * 60 + p.minute + p.second / 60;
    const dayKey = `${p.year}-${p.month}-${p.day}`;
    if (dayKey !== lastDay) {
      lastDay = dayKey;
      sun = sunTimes(date);
      $('[data-sunrise]').textContent = clockTime(sun.rise);
      $('[data-sunset]').textContent = clockTime(sun.set);
      $('[data-md-date]').textContent = `${dateFormat.format(date)} · ${zoneFormat.formatToParts(date).find(x => x.type === 'timeZoneName').value}`;
    }
    const parts = clock.formatToParts(date);
    const get = type => (parts.find(x => x.type === type) || {}).value || '';
    const timeEl = $('[data-md-time]');
    timeEl.textContent = `${get('hour')}:${get('minute')}`;
    timeEl.setAttribute('datetime', `${String(p.hour).padStart(2, '0')}:${String(p.minute).padStart(2, '0')}`);
    $('[data-md-sec]').textContent = `:${String(p.second).padStart(2, '0')}`;
    $('[data-md-ampm]').textContent = get('dayPeriod');

    const phase = phaseOf(minute, sun);
    film.dataset.phase = phase;
    document.documentElement.dataset.phase = phase;
    place(null, sun, minute);

    // The visitor's own time, shown only when it differs from Maryland's.
    const you = $('[data-you]');
    if (visitorZone && visitorZone !== TZ) {
      const yourFormat = new Intl.DateTimeFormat('en-US', { timeZone: visitorZone, hour: 'numeric', minute: '2-digit', timeZoneName: 'short' });
      const yours = yourFormat.format(date);
      const mine = clock.format(date);
      you.hidden = yours.replace(/\s?[A-Z]{2,5}$/, '') === mine;
      $('[data-you-time]').textContent = yours;
    }

    // Greet by the visitor's own hour (Maryland's, when previewing a demo time).
    const hour = demoBase ? p.hour : date.getHours();
    const chosen = county.get();
    greetingEl.textContent = `${greetingFor(hour)}, ${chosen ? county.label(chosen) : 'neighbor'}.`;
    subEl.textContent = skyLine[phase];
  };

  panel.hidden = false;
  if (pick) {
    pick.value = county.get();
    pick.addEventListener('change', () => {
      county.set(pick.value);
      window.dispatchEvent(new Event('mde:county'));
      render();
    });
  }
  window.addEventListener('mde:county', () => { if (pick) pick.value = county.get(); });
  render();
  setInterval(render, 1000);
})();
