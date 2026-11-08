// Preserve shared section links and directory filters when an old URL is opened.
const redirect = document.querySelector('script[data-redirect]');
if (redirect) {
  const target = new URL(redirect.dataset.redirect, location.href);
  target.search = location.search;
  target.hash = location.hash;
  location.replace(target.href);
}
