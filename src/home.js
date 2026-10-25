/* Home-only interactions. The generated content remains usable without JS. */
(() => {
  const header = document.querySelector('.home-header');
  if (header && 'ResizeObserver' in window) {
    new ResizeObserver(() => {
      document.documentElement.style.setProperty('--home-header-height', `${header.getBoundingClientRect().height}px`);
    }).observe(header);
  }
  const previousSections = {projects:'projects.html', 'about-me':'about.html', contact:'contact.html'};
  const previous = previousSections[location.hash.slice(1)];
  if (previous) location.replace(new URL(previous, location.href).href);
  document.querySelectorAll('.languages a').forEach(link => {
    link.addEventListener('click', () => { link.hash = location.hash; });
  });
  const navigation = [...document.querySelectorAll('#main-nav a')];
  function highlightDestination() {
    const groups = {'#recognition': '#my-story', '#media': '#journal', '#newsletter': '#journal'};
    const current = navigation.find(link => link.hash === (groups[location.hash] || location.hash));
    navigation.forEach(link => {
      if (link === current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  window.addEventListener('hashchange', highlightDestination);
  highlightDestination();
  const filters = document.querySelector('.experience-filters');
  if (filters) {
    filters.hidden = false;
    filters.addEventListener('click', event => {
      const button = event.target.closest('[data-experience-filter]');
      if (!button) return;
      const selected = button.dataset.experienceFilter;
      filters.querySelectorAll('button').forEach(item => {
        item.setAttribute('aria-pressed', String(item === button));
      });
      document.querySelectorAll('[data-experience]').forEach(pass => {
        pass.hidden = selected !== 'all' && pass.dataset.experience !== selected;
      });
    });
  }

  // Preserve archive links even when a browser opens a fragment inside details.
  function revealArchiveTarget() {
    let fragment;
    try { fragment = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(fragment);
    const archive = target?.closest('details');
    if (archive) {
      archive.open = true;
      target.scrollIntoView();
    }
  }
  window.addEventListener('hashchange', revealArchiveTarget);
  revealArchiveTarget();
})();
