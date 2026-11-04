// Start the opening camera move when its photograph is ready to be seen.
(() => {
  const photo = document.querySelector('.landscape img');
  if (!photo) return;
  const begin = () => requestAnimationFrame(() => requestAnimationFrame(() => {
    document.body.setAttribute('data-scene-ready', '');
  }));
  const ready = () => {
    if (photo.decode) photo.decode().then(begin, begin);
    else begin();
  };
  if (photo.complete && photo.naturalWidth) ready();
  else photo.addEventListener('load', ready, { once: true });
})();
