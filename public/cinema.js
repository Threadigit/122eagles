// Starts the bridge film once its photograph has decoded, and rests it while off screen.
// Without this script the photograph simply stays still; the page works either way.
(() => {
  const film = document.querySelector('.film');
  const photo = film && film.querySelector('.film-img');
  if (!photo) return;

  const begin = () => requestAnimationFrame(() => requestAnimationFrame(() => film.setAttribute('data-ready', '')));
  const ready = () => (photo.decode ? photo.decode().then(begin, begin) : begin());
  if (photo.complete && photo.naturalWidth) ready();
  else photo.addEventListener('load', ready, { once: true });

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => film.toggleAttribute('data-offscreen', !entry.isIntersecting)).observe(film);
  }
})();
