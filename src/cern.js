/* Progressive controls for the supplied CERN report. Content stays in HTML. */
(() => {
  const report = document.querySelector('.cern-report');
  const source = document.querySelector('#cern-data');
  if (!report || !source) return;
  const data = JSON.parse(source.textContent);
  const setValue = (key, value) => report.querySelectorAll(`[data-cern-value="${key}"]`).forEach(node => { node.textContent = value; });
  const select = (kind, key) => report.querySelectorAll(`[data-${kind}]`).forEach(button => button.setAttribute('aria-pressed', String(button.dataset[kind] === key)));
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const pause = report.querySelector('[data-atlas-pause]');
  const scene = report.querySelector('[data-atlas-scene]');
  let paused = motion.matches;
  const updatePause = () => {
    pause.hidden = motion.matches;
    scene.dataset.paused = String(paused);
    pause.setAttribute('aria-pressed', String(paused));
    pause.setAttribute('aria-label', paused ? data.play : data.pause);
    pause.querySelector('span').textContent = paused ? '▷' : 'Ⅱ';
  };
  pause.addEventListener('click', () => { paused = !paused; updatePause(); });
  motion.addEventListener('change', () => { paused = motion.matches; updatePause(); });
  updatePause();
  report.querySelectorAll('[data-layer]').forEach(button => button.addEventListener('click', () => {
    const key = button.getAttribute('aria-pressed') === 'true' ? '' : button.dataset.layer;
    select('layer', key);
    report.querySelectorAll('[data-atlas-layer]').forEach(shape => {
      shape.style.opacity = key && key !== shape.dataset.atlasLayer ? '.06' : shape.dataset.opacity;
    });
    setValue('atlasNote', data.layers.find(item => item.key === key)?.note || data.atlasNote);
  }));
  report.querySelectorAll('[data-visibility]').forEach(button => button.addEventListener('click', () => {
    const key = button.dataset.visibility;
    const item = data.visibility[key];
    select('visibility', key);
    const image = report.querySelector('[data-visibility-image]');
    const link = report.querySelector('[data-visibility-link]');
    image.src = item.img;
    image.alt = item.alt;
    link.href = item.img;
    link.dataset.caption = item.alt;
    for (const field of ['label','found','extra','note']) setValue('vis' + field[0].toUpperCase() + field.slice(1), item[field]);
  }));
  const showModel = key => {
    const model = data.models[key];
    select('model', key);
    for (const [field, value] of Object.entries(model)) {
      const percentage = ['eff','pur','acc','sel'].includes(field);
      setValue('cm.' + field, percentage ? value.toFixed(1) + '%' : value);
      if (percentage) report.style.setProperty('--' + field + 'W', value + '%');
    }
  };
  report.querySelectorAll('[data-model]').forEach(button => button.addEventListener('click', () => showModel(button.dataset.model)));
  showModel('v0');
  setValue('atlasNote', data.atlasNote);
  report.querySelectorAll('[data-cern-controls]').forEach(group => { group.hidden = false; });
  updatePause();
  report.dataset.ready = 'true';
  if ('ResizeObserver' in window) {
    new ResizeObserver(([entry]) => scene.style.setProperty('--atlas-scale', Math.min(1, (entry.contentRect.width - 16) / 460))).observe(scene);
  }
})();
