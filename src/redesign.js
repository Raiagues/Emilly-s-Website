/* Progressive enhancement for the original prototype interactions. */
(() => {
  const header = document.querySelector('.home-header');
  if (header && 'ResizeObserver' in window) {
    const measureHeader = () => document.documentElement.style.setProperty('--header-height', `${header.getBoundingClientRect().height}px`);
    measureHeader();
    new ResizeObserver(measureHeader).observe(header);
  }
  document.querySelectorAll('[data-carousel]').forEach(carousel => {
    const items=[...carousel.querySelectorAll('[data-carousel-item]')];
    const controls=carousel.querySelector('.media-controls');
    if (!items.length || !controls) return;
    let selected=0;
    const show=index => {
      selected=(index+items.length)%items.length;
      items.forEach((item,i)=>{item.hidden=i!==selected;});
      controls.querySelector('[data-carousel-count]').textContent=`${selected+1} / ${items.length}`;
    };
    controls.hidden=items.length<2;
    controls.querySelector('[data-carousel-prev]').addEventListener('click',()=>show(selected-1));
    controls.querySelector('[data-carousel-next]').addEventListener('click',()=>show(selected+1));
    show(0);
  });
  document.querySelectorAll('.flight-path:not(.story-explorer)').forEach(route => {
    const stops=[...route.querySelectorAll('[data-flight-stop]')];
    const show=stop => {
      stops.forEach(item=>{
        const selected=item===stop;
        item.setAttribute('aria-pressed',String(selected));
        document.getElementById(item.dataset.preview).hidden=!selected;
      });
    };
    stops.forEach(stop=>{
      stop.setAttribute('role','button');
      stop.setAttribute('aria-controls',stop.dataset.preview);
      stop.addEventListener('click',event=>{
        if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||event.button!==0)return;
        event.preventDefault();show(stop);
      });
      stop.addEventListener('keydown',event=>{
        if(event.key===' '){event.preventDefault();show(stop);}
      });
    });
    show(stops.find(stop=>stop.hasAttribute('aria-current'))||stops[0]);
  });
})();
