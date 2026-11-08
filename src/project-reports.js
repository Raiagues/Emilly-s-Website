/* Original figures remain readable in document order without JavaScript. */
(() => {
  document.querySelectorAll('[data-report-switcher]').forEach(group => {
    const controls = group.querySelector('[data-report-choices]');
    const buttons = [...controls.querySelectorAll('[data-report-choice]')];
    const panels = [...group.querySelectorAll('[data-report-panel]')];
    if (!buttons.length || buttons.length !== panels.length) return;
    controls.setAttribute('role', 'tablist');
    const select = (index, focus = false) => {
      buttons.forEach((button, i) => {
        button.setAttribute('aria-selected', String(i === index));
        button.tabIndex = i === index ? 0 : -1;
        panels[i].hidden = i !== index;
      });
      if (focus) buttons[index].focus();
    };
    buttons.forEach((button, i) => {
      button.setAttribute('role', 'tab');
      panels[i].setAttribute('role', 'tabpanel');
      panels[i].setAttribute('aria-labelledby', button.id);
      button.addEventListener('click', () => select(i));
      button.addEventListener('keydown', event => {
        const index = {ArrowRight: (i + 1) % buttons.length, ArrowLeft: (i - 1 + buttons.length) % buttons.length, Home: 0, End: buttons.length - 1}[event.key];
        if (index === undefined) return;
        event.preventDefault();
        select(index, true);
      });
    });
    select(0);
    controls.hidden = false;
    group.classList.add('is-enhanced');
  });
})();
