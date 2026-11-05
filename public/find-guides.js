// Search only this publication's guide collection. Nothing is sent to a search provider.
(() => {
  const form = document.querySelector('.directory-search');
  if (!form) return;
  const query = form.querySelector('[name=q]');
  const topic = form.querySelector('[name=topic]');
  const county = form.querySelector('[name=county]');
  const cards = [...document.querySelectorAll('[data-entry]')];
  const normalize = value => value.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
  const stopwords = new Set(['i','im','a','an','the','and','for','to','my','with','need','help','me','in','maryland','how','can','do','get','am','is','of','find','near','where','what','which','cant','cannot','t','want','about','looking','someone','pay','paying','afford']);
  const place = value => (/City|County/.test(value) ? value : `${value} County`);
  const render = () => {
    const terms = normalize(query.value).split(' ').filter(word => word && !stopwords.has(word));
    let count = 0;
    cards.forEach(card => {
      const words = normalize(card.dataset.search).split(' ');
      const match = (!topic.value || card.dataset.topic === topic.value) && terms.every(term => words.some(word => word === term || (term.length >= 3 && word.startsWith(term))));
      card.hidden = !match;
      if (match) count++;
      // A county does not filter anything: services are delivered locally, so it only reminds the reader to ask for their office.
      const note = card.querySelector('.county-note');
      if (note) {
        note.hidden = !(county && county.value && match);
        if (county && county.value) note.textContent = card.dataset.local === 'campus' ? 'Through your university, not your county.' : `Local help: ask which office serves ${place(county.value)}.`;
      }
    });
    const where = county && county.value ? ` for ${place(county.value)}` : '';
    document.querySelector('#result-count').textContent = `${count} ${count === 1 ? 'guide' : 'guides'}${query.value.trim() ? ' matching your search' : ''}${where}`;
    document.querySelector('#no-results').hidden = count !== 0;
  };
  const readURL = () => {
    const params = new URLSearchParams(location.search);
    query.value = (params.get('q') || '').slice(0,160);
    const selected = params.get('topic') || '';
    topic.value = [...topic.options].some(option => option.value === selected) ? selected : '';
    if (county) {
      const chosen = params.get('county') || '';
      county.value = [...county.options].some(option => option.value === chosen) ? chosen : '';
    }
    render();
  };
  const update = () => {
    const params = new URLSearchParams();
    if (query.value.trim()) params.set('q',query.value.trim());
    if (topic.value) params.set('topic',topic.value);
    if (county && county.value) params.set('county',county.value);
    const search = params.toString();
    history.replaceState(null,'',location.pathname+(search?'?'+search:''));
    render();
  };
  form.addEventListener('submit',event => { event.preventDefault(); update(); });
  query.addEventListener('input',update);
  topic.addEventListener('change',update);
  if (county) county.addEventListener('change',update);
  document.querySelector('#clear-search').addEventListener('click',event => {
    event.preventDefault(); query.value=''; topic.value=''; if (county) county.value=''; update(); query.focus();
  });
  window.addEventListener('popstate',readURL);
  readURL();
})();
