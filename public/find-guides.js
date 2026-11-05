// Search only this publication's guide collection. Nothing is sent to a search provider.
(() => {
  const form = document.querySelector('.directory-search');
  if (!form) return;
  const query = form.querySelector('[name=q]');
  const topic = form.querySelector('[name=topic]');
  const cards = [...document.querySelectorAll('.guide-result')];
  const normalize = value => value.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
  const stopwords = new Set(['i','im','a','an','the','and','for','to','my','with','need','help','me','in','maryland','how','can','do','get','am','is','of','find','near','where','what','which','cant','cannot','t','want','about','looking','someone','pay','paying','afford']);
  const render = () => {
    const terms = normalize(query.value).split(' ').filter(word => word && !stopwords.has(word));
    let count = 0;
    cards.forEach(card => {
      const words = normalize(card.dataset.search).split(' ');
      const match = (!topic.value || card.dataset.topic === topic.value) && terms.every(term => words.some(word => word === term || (term.length >= 3 && word.startsWith(term))));
      card.hidden = !match;
      if (match) count++;
    });
    document.querySelector('#result-count').textContent = `${count} ${count === 1 ? 'guide' : 'guides'}${query.value.trim() ? ' matching your search' : ''}`;
    document.querySelector('#no-results').hidden = count !== 0;
  };
  const readURL = () => {
    const params = new URLSearchParams(location.search);
    query.value = (params.get('q') || '').slice(0,160);
    const selected = params.get('topic') || '';
    topic.value = [...topic.options].some(option => option.value === selected) ? selected : '';
    render();
  };
  const update = () => {
    const params = new URLSearchParams();
    if (query.value.trim()) params.set('q',query.value.trim());
    if (topic.value) params.set('topic',topic.value);
    const search = params.toString();
    history.replaceState(null,'',location.pathname+(search?'?'+search:''));
    render();
  };
  form.addEventListener('submit',event => { event.preventDefault(); update(); });
  query.addEventListener('input',update);
  topic.addEventListener('change',update);
  document.querySelector('#clear-search').addEventListener('click',event => {
    event.preventDefault(); query.value=''; topic.value=''; update(); query.focus();
  });
  window.addEventListener('popstate',readURL);
  readURL();
})();
