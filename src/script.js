'use strict';
// Progressive enhancement: every page and every language works without JavaScript.
const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');
if (menu && nav) {
  const mobile = window.matchMedia('(max-width: 850px)');
  const setMenu = (open) => {
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-collapsed', !open && mobile.matches);
  };
  setMenu(false);
  menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      menu.focus();
    }
  });
  mobile.addEventListener('change', () => setMenu(false));
}
// Keep the current section when changing language on the homepage.
for (const link of document.querySelectorAll('.languages a')) {
  link.addEventListener('click', () => { if (location.hash) link.hash = location.hash; });
}
const copy = document.querySelector('#copy-email');
if (copy && navigator.clipboard && window.isSecureContext) {
  copy.hidden = false;
  copy.addEventListener('click', async () => {
    const status = document.querySelector('#copy-status');
    try {
      await navigator.clipboard.writeText(copy.dataset.email);
      status.textContent = copy.dataset.success;
    } catch {
      status.textContent = copy.dataset.error;
    }
  });
}
for (const year of document.querySelectorAll('[data-year]')) year.textContent = new Date().getFullYear();
// Native form POST keeps verification and delivery reporting with the email provider.
// No fake success state, secret keys, or message content stored in the browser.
