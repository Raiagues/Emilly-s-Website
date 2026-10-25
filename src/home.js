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

  const motion = document.querySelector('.motion-toggle');
  if (motion) {
    motion.hidden = false;
    motion.addEventListener('click', () => {
      const paused = document.body.classList.toggle('motion-paused');
      motion.setAttribute('aria-pressed', String(paused));
      motion.textContent = paused ? motion.dataset.play : motion.dataset.pause;
    });
  }
  // Keep previously shared links to archive entries working after the move.
  function redirectArchive() {
    if (location.hash.startsWith('#archive-')) {
      location.replace(new URL('journal.html' + location.hash, location.href).href);
    }
  }
  window.addEventListener('hashchange', redirectArchive);
  redirectArchive();
})();
