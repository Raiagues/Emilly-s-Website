/* Photos stay ordinary image links when JavaScript or <dialog> is unavailable. */
(() => {
  const links = [...document.querySelectorAll('[data-gallery]')];
  const dialog = document.querySelector('.photo-dialog');
  if (!links.length || !dialog || typeof dialog.showModal !== 'function') return;
  const image = dialog.querySelector('img');
  const caption = dialog.querySelector('figcaption');
  const counter = dialog.querySelector('#photo-counter');
  let index = 0;
  let opener;
  const show = next => {
    index = (next + links.length) % links.length;
    const link = links[index];
    image.src = link.href;
    image.alt = link.dataset.caption;
    caption.textContent = link.dataset.caption;
    counter.textContent = `${dialog.dataset.photoLabel} ${index + 1} ${dialog.dataset.ofLabel} ${links.length}`;
  };
  links.forEach((link, position) => link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
    event.preventDefault();
    opener = link;
    show(position);
    dialog.showModal();
    document.documentElement.classList.add('photo-is-open');
  }));
  dialog.querySelector('.photo-close').addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-photo-prev]').addEventListener('click', () => show(index - 1));
  dialog.querySelector('[data-photo-next]').addEventListener('click', () => show(index + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      show(index + (event.key === 'ArrowLeft' ? -1 : 1));
    }
  });
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => {
    document.documentElement.classList.remove('photo-is-open');
    opener?.focus({preventScroll:true});
  });
})();
