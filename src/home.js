/* Home-only interactions. The generated content remains usable without JS. */
(() => {
  const header = document.querySelector('.home-header');
  const previousSections = {projects:'projects.html', 'about-me':'about.html', contact:'contact.html'};
  const previous = previousSections[location.hash.slice(1)];
  if (previous) location.replace(new URL(previous, location.href).href);
  let pendingDestination = '';
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', event => {
      if (!event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey) pendingDestination = link.hash;
    });
  });
  window.addEventListener('scrollend', () => { pendingDestination = ''; });
  window.addEventListener('wheel', () => { pendingDestination = ''; }, {passive:true});
  window.addEventListener('touchmove', () => { pendingDestination = ''; }, {passive:true});
  document.querySelectorAll('.languages a').forEach(link => {
    link.addEventListener('click', () => {
      link.hash = pendingDestination || document.querySelector('#main-nav a[aria-current]')?.hash || location.hash;
    });
  });
  const navigation = [...document.querySelectorAll('#main-nav a')];
  function highlightDestination() {
    const edge = (header?.getBoundingClientRect().bottom || 0) + 64;
    let current = navigation[0];
    navigation.slice(1).forEach(link => {
      const section = document.querySelector(link.hash);
      if (section && section.getBoundingClientRect().top <= edge) current = link;
    });
    if (Math.ceil(window.scrollY + window.innerHeight) >= document.documentElement.scrollHeight) {
      current = navigation[navigation.length - 1];
    }
    navigation.forEach(link => {
      if (link === current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  window.addEventListener('hashchange', highlightDestination);
  window.addEventListener('resize', highlightDestination);
  window.addEventListener('load', highlightDestination);
  let scrollPending = false;
  window.addEventListener('scroll', () => {
    if (scrollPending) return;
    scrollPending = true;
    requestAnimationFrame(() => { highlightDestination(); scrollPending = false; });
  }, {passive:true});
  highlightDestination();

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
