/* Real links remain available when scripts are disabled. */
(() => {
  const rack = document.querySelector('.postcard-rack');
  if (rack) {
    const list = rack.querySelector('ol');
    const cards = [...list.children];
    const route = document.querySelector('.rack-route-stops');
    const stops = [...route.children];
    const more = rack.querySelector('.rack-more');
    let visible = 12;
    const paginate = () => {
      [...list.children].forEach((card, i) => { card.hidden = i >= visible; });
      more.hidden = visible >= cards.length;
    };
    const revealHash = () => {
      const target = [...list.children].find(card => '#' + card.id === location.hash);
      if (!target) return;
      route.querySelectorAll('a').forEach(link => {
        if (link.hash === location.hash) link.setAttribute('aria-current','location');
        else link.removeAttribute('aria-current');
      });
      visible = Math.max(visible, [...list.children].indexOf(target) + 1);
      paginate();
      requestAnimationFrame(() => target.scrollIntoView({block:'start'}));
    };
    document.querySelector('.rack-sort').hidden = false;
    document.querySelectorAll('[data-story-order]').forEach(button => {
      button.addEventListener('click', () => {
        const direction = button.dataset.storyOrder === 'newest' ? -1 : 1;
        const compare = (a, b) => direction * a.dataset.date.localeCompare(b.dataset.date);
        cards.sort(compare).forEach(card => list.append(card));
        stops.sort(compare).forEach(stop => route.append(stop));
        document.querySelectorAll('[data-story-order]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        visible = 12;
        paginate();
      });
    });
    more.addEventListener('click', () => {
      const next = list.children[visible];
      visible += 12;
      paginate();
      next?.querySelector('a').focus({preventScroll:true});
    });
    window.addEventListener('hashchange', revealHash);
    paginate();
    revealHash();
  }
  document.querySelectorAll('.story-explorer').forEach(explorer => {
    const stops = [...explorer.querySelectorAll('[data-flight-stop]')];
    const rail = explorer.querySelector('.flight-map');
    const controls = explorer.querySelector('.explorer-controls');
    const preview = stop => {
      stops.forEach(item => {
        const active = item === stop;
        item.dataset.previewActive = String(active);
        document.getElementById(item.dataset.preview).hidden = !active;
      });
    };
    stops.forEach((stop, index) => {
      stop.addEventListener('pointerenter', event => { if (event.pointerType !== 'touch') preview(stop); });
      stop.addEventListener('focus', () => preview(stop));
      stop.addEventListener('keydown', event => {
        if (!['ArrowUp','ArrowDown','Home','End'].includes(event.key)) return;
        event.preventDefault();
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? stops.length - 1 : (index + (event.key === 'ArrowDown' ? 1 : -1) + stops.length) % stops.length;
        stops[next].focus({preventScroll:true});
        stops[next].scrollIntoView({block:'nearest',inline:'nearest'});
      });
    });
    controls.hidden = false;
    controls.querySelector('[data-story-prev]').addEventListener('click', () => rail.scrollBy({top:-rail.clientHeight*.8}));
    controls.querySelector('[data-story-next]').addEventListener('click', () => rail.scrollBy({top:rail.clientHeight*.8}));
    const current = stops.find(stop => stop.hasAttribute('aria-current')) || stops[0];
    preview(current);
    rail.scrollTop = current.offsetTop - rail.offsetTop - rail.clientHeight / 2 + current.offsetHeight / 2;
  });
})();
