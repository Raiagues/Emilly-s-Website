'use strict';
(() => {
  const grid = document.querySelector('#project-grid');
  if (!grid) return;
  const cards = [...grid.querySelectorAll('[data-project]')];
  const search = document.querySelector('#project-search');
  const filters = [...document.querySelectorAll('[data-filter]')];
  const count = document.querySelector('#results-count');
  const reset = document.querySelector('#reset-filters');
  const empty = document.querySelector('#empty-state');
  const categories = new Set(filters.map(button => button.dataset.filter));
  const storageKey = `emilly-${document.querySelector('[data-directory-kind]').dataset.directoryKind}:${new URL('../', document.currentScript.src).pathname}`;
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  let category = 'all';

  function render(updateURL = false) {
    const query = normalize(search.value);
    const matching = cards.filter(card => (category === 'all' || card.dataset.category === category) && normalize(card.dataset.search).includes(query));
    cards.forEach(card => { card.hidden = !matching.includes(card); });
    count.textContent = `${matching.length} ${count.dataset.label}`;
    empty.hidden = matching.length !== 0;
    reset.hidden = category === 'all' && !search.value;
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    const params = new URLSearchParams();
    if (category !== 'all') params.set('area', category);
    if (search.value.trim()) params.set('q', search.value.trim());
    if (updateURL) {
      const url = new URL(location.href);
      url.search = params.toString();
      url.hash = '';
      history.replaceState(null, '', url);
    }
    // Storage is optional. Directories and sharing still work when storage is blocked.
    try { sessionStorage.setItem(storageKey, params.toString()); } catch { /* Private browsing */ }
    document.querySelectorAll('.languages a').forEach(link => { link.search = params.toString(); });
  }
  function restoreFromURL() {
    const params = new URLSearchParams(location.search);
    category = categories.has(params.get('area')) ? params.get('area') : 'all';
    search.value = (params.get('q') || '').slice(0, 120);
    render();
  }
  filters.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; render(true); }));
  search.addEventListener('input', () => render(true));
  reset.addEventListener('click', () => { category = 'all'; search.value = ''; render(true); search.focus(); });
  window.addEventListener('popstate', restoreFromURL);
  window.addEventListener('pageshow', restoreFromURL);
  document.querySelector('[data-project-tools]').hidden = false;
  restoreFromURL();
})();
