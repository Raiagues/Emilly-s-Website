'use strict';
// Every main destination is visible, including on mobile and with JS disabled.
const scriptRoot = new URL('../', document.currentScript.src).pathname;
const header = document.querySelector('.site-header');
if (header && 'ResizeObserver' in window) {
  new ResizeObserver(() => document.documentElement.style.setProperty('--header-height', `${header.getBoundingClientRect().height}px`)).observe(header);
}
// Retain the actual section, not an obsolete anchor, on older shared home URLs.
const oldSections = {projects:'projects.html',experience:'experience.html','about-me':'about.html',recognition:'recognition.html',contact:'contact.html'};
if (document.body.dataset.page === 'home' && oldSections[location.hash.slice(1)]) {
  location.replace(new URL(oldSections[location.hash.slice(1)], location.href).href);
}
for (const link of document.querySelectorAll('.languages a')) {
  link.addEventListener('click', () => { if (location.hash) link.hash = location.hash; });
}
// A project opened from filtered results returns to those results, also across languages.
try {
  const allowedAreas = ['space','hardware','control','software','outreach'];
  for (const link of document.querySelectorAll('[data-back-results]')) {
    const kind = link.dataset.directoryKind === 'experience' ? 'experience' : 'projects';
    const saved = new URLSearchParams(sessionStorage.getItem(`emilly-${kind}:${scriptRoot}`) || '');
    const safe = new URLSearchParams();
    if (allowedAreas.includes(saved.get('area'))) safe.set('area', saved.get('area'));
    if (saved.get('q')) safe.set('q', saved.get('q').slice(0,120));
    const target = new URL(link.href);
    target.search = safe.toString();
    target.hash = link.dataset.backResults;
    link.href = target.href;
  }
} catch { /* Native links remain available if browser storage is restricted. */ }
const copy = document.querySelector('#copy-email');
if (copy && navigator.clipboard && window.isSecureContext) {
  copy.hidden = false;
  copy.addEventListener('click', async () => {
    const status = document.querySelector('#copy-status');
    try {
      await navigator.clipboard.writeText(copy.dataset.email);
      status.textContent = copy.dataset.success;
    } catch { status.textContent = copy.dataset.error; }
  });
}
for (const year of document.querySelectorAll('[data-year]')) year.textContent = new Date().getFullYear();

// Keep the project sidebar oriented to the section currently being read.
const chapterLinks = [...document.querySelectorAll('.project-sidebar .contents-nav a')];
if (chapterLinks.length) {
  const chapters = chapterLinks.map(link => document.querySelector(link.hash));
  let pending = false;
  const updateChapter = () => {
    const edge = (header?.getBoundingClientRect().bottom || 0) + 100;
    let active = 0;
    chapters.forEach((section, index) => { if (section && section.getBoundingClientRect().top <= edge) active = index; });
    chapterLinks.forEach((link, index) => {
      if (index === active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    pending = false;
  };
  window.addEventListener('scroll', () => {
    if (!pending) { pending = true; requestAnimationFrame(updateChapter); }
  }, {passive: true});
  window.addEventListener('resize', updateChapter);
  updateChapter();
}
