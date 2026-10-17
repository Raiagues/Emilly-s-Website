'use strict';
(() => {
  const grid = document.querySelector('#project-grid');
  if (!grid) return;
  const cards = [...grid.querySelectorAll('[data-project]')];
  const search = document.querySelector('#project-search');
  const filters = [...document.querySelectorAll('[data-filter]')];
  const count = document.querySelector('#results-count');
  const more = document.querySelector('#show-more');
  const empty = document.querySelector('#empty-state');
  const initialCount = 6;
  let category = 'all';
  let expanded = false;
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const update = () => {
    const query = normalize(search.value);
    const matching = cards.filter(card => (category === 'all' || card.dataset.category === category) && normalize(card.dataset.search).includes(query));
    const filtering = category !== 'all' || query.length > 0;
    const visible = filtering || expanded ? matching : matching.slice(0, initialCount);
    cards.forEach(card => { card.hidden = !visible.includes(card); });
    count.textContent = `${matching.length} ${count.dataset.label}`;
    empty.hidden = matching.length > 0;
    more.hidden = filtering || matching.length <= initialCount;
    more.textContent = expanded ? more.dataset.less : more.dataset.more;
    more.setAttribute('aria-expanded', String(expanded));
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
  };
  document.querySelector('[data-project-tools]').hidden = false;
  filters.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; expanded = false; update(); }));
  search.addEventListener('input', () => { expanded = false; update(); });
  more.addEventListener('click', () => {
    expanded = !expanded;
    update();
    if (!expanded) document.querySelector('.project-tools').scrollIntoView({block:'start',behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
  });
  document.querySelector('#reset-filters').addEventListener('click', () => {
    category = 'all'; expanded = false; search.value = ''; update(); search.focus();
  });
  update();
})();
