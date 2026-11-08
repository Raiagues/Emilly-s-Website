/* Small, local enhancements. The documents, source and captures work without JS. */
(() => {
  const root = document.querySelector('.engineering-case');
  const dataNode = document.getElementById('engineering-data');
  if (!root || !dataNode) return;
  const data = JSON.parse(dataNode.textContent);
  const pauses = [];

  root.querySelectorAll('[data-select-group]').forEach(group => {
    const controls = group.querySelector(':scope > [data-choices]');
    const buttons = [...controls.children];
    const views = [...group.querySelector(':scope > .eng-views').children];
    if (!buttons.length || buttons.length !== views.length) return;
    controls.setAttribute('role', 'tablist');
    const select = (index, focus = false) => {
      buttons.forEach((button, i) => {
        button.setAttribute('aria-selected', String(i === index));
        button.tabIndex = i === index ? 0 : -1;
        views[i].hidden = i !== index;
      });
      const name = group.dataset.selectGroup;
      if (name === 'architecture') {
        root.querySelectorAll('[data-arch-node]').forEach(node => {
          node.style.opacity = node.dataset.archNode === ['web', 'backend', 'flight'][index] ? '1' : '.55';
        });
      }
      if (name === 'layers') root.querySelectorAll('[data-stack-layer]').forEach((node, i) => node.classList.toggle('is-active', i === index));
      if (name === 'memory') root.querySelectorAll('[data-memory-row]').forEach((node, i) => node.classList.toggle('is-active', i === index));
      if (name === 'states') root.querySelectorAll('[data-state-node]').forEach(node => node.classList.toggle('is-muted', Number(node.dataset.stateNode) !== index));
      if (name === 'sensor-path') root.querySelectorAll('[data-sensor-node]').forEach((node,i) => node.classList.toggle('is-active',i === index));
      if (name === 'kernel-activities') pauses.forEach(pause => pause());
      if (focus) buttons[index].focus();
    };
    buttons.forEach((button, i) => {
      button.setAttribute('role', 'tab');
      views[i].setAttribute('role', 'tabpanel');
      views[i].setAttribute('aria-labelledby', button.id);
      button.addEventListener('click', () => select(i));
      button.addEventListener('keydown', event => {
        const index = {ArrowRight:(i+1)%buttons.length, ArrowLeft:(i-1+buttons.length)%buttons.length, Home:0, End:buttons.length-1}[event.key];
        if (index === undefined) return;
        event.preventDefault();
        select(index, true);
      });
    });
    select(0);
    controls.hidden = false;
    group.classList.add('is-enhanced');
  });

  const sensorLab = root.querySelector('[data-sensor-lab]');
  if (sensorLab) {
    const time = sensorLab.querySelector('[data-signal-time]');
    const show = () => {
      const seconds = Number(time.value);
      const wave = Math.sin(2 * Math.PI * seconds / 30);
      const temperature = 23.5 + 5 * wave;
      const x = 30 + seconds * 16, y = 135 - 65 * wave;
      sensorLab.querySelector('[data-signal-c]').textContent = temperature.toFixed(3);
      sensorLab.querySelector('[data-signal-mc]').textContent = String(Math.round(temperature * 1000));
      sensorLab.querySelector('[data-signal-seconds]').textContent = seconds.toFixed(2) + ' s';
      sensorLab.querySelector('[data-signal-dot]').setAttribute('cx', x);
      sensorLab.querySelector('[data-signal-dot]').setAttribute('cy', y);
      sensorLab.querySelector('[data-signal-guide]').setAttribute('d', `M${x} 40V215`);
    };
    time.addEventListener('input', show);
    sensorLab.querySelector('[data-signal-controls]').hidden = false;
    show();
  }

  const messageLab = root.querySelector('[data-message-lab]');
  if (messageLab) {
    const nodes = [...messageLab.querySelectorAll('[data-step-select]')];
    const views = [...messageLab.querySelectorAll('[data-step-view]')];
    const play = messageLab.querySelector('[data-message-play]');
    let index = 0, timer = null;
    const stop = () => { clearInterval(timer); timer=null; play.textContent='▶ '+play.dataset.playLabel; play.setAttribute('aria-pressed','false'); };
    const show = next => {
      index = (next+views.length)%views.length;
      nodes.forEach((node,i) => {
        if (i===index) node.setAttribute('aria-current','step'); else node.removeAttribute('aria-current');
        views[i].hidden = i!==index;
      });
      messageLab.querySelector('[data-message-count]').textContent=`${index+1} / ${views.length}`;
    };
    nodes.forEach((node,i) => node.addEventListener('click',event => { if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey) return; event.preventDefault();stop();show(i); }));
    messageLab.querySelector('[data-message-prev]').addEventListener('click',()=>{stop();show(index-1);});
    messageLab.querySelector('[data-message-next]').addEventListener('click',()=>{stop();show(index+1);});
    play.addEventListener('click',()=>{
      if(timer){stop();return;}
      play.textContent='Ⅱ '+play.dataset.pauseLabel; play.setAttribute('aria-pressed','true');
      timer=setInterval(()=>{ if(index===views.length-1){stop();return;} show(index+1); },2200);
      if(index===views.length-1) show(0);
    });
    pauses.push(stop);show(0);messageLab.querySelector('[data-message-controls]').hidden=false;
  }

  (data.kernel || []).forEach(record => {
    const panel=root.querySelector(`[data-replay="${record.id}"]`);
    if(!panel) return;
    const svg=panel.querySelector('[data-frame]');
    const image=svg.querySelector('image');
    const play=panel.querySelector('[data-replay-play]');
    const seek=panel.querySelector('[data-replay-seek]');
    const zoom=panel.querySelector('[data-replay-zoom]');
    let index=record.initial || 0, timer=null, detail=true;
    const stop=()=>{clearTimeout(timer);timer=null;play.textContent='▶ '+play.dataset.playLabel;play.setAttribute('aria-pressed','false');};
    const show=next=>{
      index=Math.max(0,Math.min(record.frames.length-1,next));
      const frame=record.frames[index];
      image.setAttribute('href',frame.file);
      svg.setAttribute('viewBox',detail ? frame.focus.join(' ') : '0 0 1280 720');
      svg.setAttribute('aria-label',frame.label);
      panel.querySelector('[data-frame-caption]').textContent=frame.label;
      panel.querySelector('[data-frame-count]').textContent=`${String(index+1).padStart(2,'0')} / ${String(record.frames.length).padStart(2,'0')}`;
      panel.querySelector('[data-uart-output]').textContent=(frame.uart_display || '').trim();
      (frame.observed?.processes || []).forEach(task => {
        const card=panel.querySelector(`[data-observed-task="${task.pid}"]`);
        if (!card) return;
        card.querySelector('[data-observed-state]').textContent=task.state_label;
        card.querySelector('[data-observed-sp]').textContent='sp '+task.saved_sp;
      });
      seek.value=String(index);
      const breakpoint=/([^/]+\.[cS]):(\d+)/.exec(frame.breakpoint || '');
      panel.querySelectorAll('[data-source-path]').forEach(block=>{
        const match=breakpoint && block.dataset.sourcePath.endsWith('/'+breakpoint[1]);
        block.querySelectorAll('[data-line]').forEach(line=>line.classList.toggle('is-active',Boolean(match && Number(line.dataset.line)===Number(breakpoint[2]))));
      });
    };
    const advance=()=>{
      if(index===record.frames.length-1){stop();return;}
      show(index+1);timer=setTimeout(advance,1800);
    };
    play.addEventListener('click',()=>{
      if(timer){stop();return;}
      if(index===record.frames.length-1) show(0);
      play.textContent='Ⅱ '+play.dataset.pauseLabel;play.setAttribute('aria-pressed','true');
      timer=setTimeout(advance,1800);
    });
    panel.querySelector('[data-replay-prev]').addEventListener('click',()=>{stop();show(index-1);});
    panel.querySelector('[data-replay-next]').addEventListener('click',()=>{stop();show(index+1);});
    seek.addEventListener('input',()=>{stop();show(Number(seek.value));});
    zoom.addEventListener('click',()=>{detail=!detail;zoom.setAttribute('aria-pressed',String(detail));show(index);});
    pauses.push(stop);show(index);panel.querySelector('[data-replay-controls]').hidden=false;
  });

  const pixel=root.querySelector('[data-pixel-lab]');
  if(pixel){
    const xInput=pixel.querySelector('[data-pixel-x]'), yInput=pixel.querySelector('[data-pixel-y]');
    const update=()=>{
      const x=Math.max(0,Math.min(1279,Math.trunc(Number(xInput.value)||0)));
      const y=Math.max(0,Math.min(719,Math.trunc(Number(yInput.value)||0)));
      const offset=4*(y*1280+x);
      pixel.querySelector('[data-x]').textContent=String(x);pixel.querySelector('[data-y]').textContent=String(y);
      pixel.querySelector('[data-pixel-address]').value='0x'+(0x80000000+offset).toString(16).toUpperCase().padStart(8,'0');
      pixel.querySelector('[data-pixel-offset]').textContent=String(offset);
      const sx=x/2,sy=y/2;
      pixel.querySelector('[data-pixel-dot]').setAttribute('cx',String(sx));pixel.querySelector('[data-pixel-dot]').setAttribute('cy',String(sy));
      pixel.querySelector('[data-pixel-guide]').setAttribute('d',`M0 ${sy}H${sx}V360`);
      const coordinates=pixel.querySelector('[data-pixel-coordinates]');
      coordinates.setAttribute('x',String(Math.max(12,Math.min(490,sx+14))));coordinates.setAttribute('y',String(Math.max(24,sy-12)));coordinates.textContent=`(${x}, ${y})`;
    };
    [xInput,yInput].forEach(input=>{
      input.addEventListener('input',update);
      input.addEventListener('change',()=>{input.value=String(Math.max(Number(input.min),Math.min(Number(input.max),Math.trunc(Number(input.value)||0))));update();});
    });
    pixel.querySelector('[data-pixel-inputs]').hidden=false;update();
  }
  const glyph=root.querySelector('[data-glyph-lab]');
  if(glyph && data.glyphs){
    const choices=[...glyph.querySelectorAll('[data-glyph]')];
    choices.forEach(button=>button.addEventListener('click',()=>{
      const rows=data.glyphs[button.dataset.glyph];
      choices.forEach(choice=>choice.setAttribute('aria-pressed',String(choice===button)));
      glyph.querySelectorAll('[data-bit]').forEach((cell,i)=>cell.classList.toggle('on',Boolean((rows[Math.floor(i/8)]>>(i%8))&1)));
      glyph.querySelectorAll('[data-glyph-byte]').forEach((span,i)=>span.textContent='0x'+rows[i].toString(16).toUpperCase().padStart(2,'0'));
    }));
    glyph.querySelector('[data-glyph-controls]').hidden=false;
  }
  const packets=root.querySelector('[data-packet-inspector]');
  if(packets && data.packets){
    const options=[...packets.querySelectorAll('[data-packet-kind]')];
    const panels=[...packets.querySelectorAll('[data-packet-view]')];
    const showField=(panel,record,index)=>{
      const field=record.fields[index];
      panel.querySelectorAll('[data-byte]').forEach((byte,i)=>byte.classList.toggle('is-selected',i>=field.start && i<field.start+field.size));
      panel.querySelectorAll('[data-packet-explanation]').forEach((view,i)=>view.hidden=i!==index);
      panel.querySelectorAll('[data-packet-field]').forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
    };
    panels.forEach((panel,i)=>{
      panel.querySelectorAll('[data-packet-field]').forEach((button,index)=>button.addEventListener('click',()=>showField(panel,data.packets[i],index)));
      panel.querySelector('[data-packet-fields]').hidden=false;
      showField(panel,data.packets[i],0);
    });
    const select=index=>{
      panels.forEach((panel,i)=>panel.hidden=i!==index);
      options.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
    };
    options.forEach((button,i)=>button.addEventListener('click',()=>select(i)));
    packets.querySelector('[data-packet-kinds]').hidden=false;
    select(0);
  }
  document.addEventListener('visibilitychange',()=>{if(document.hidden)pauses.forEach(pause=>pause());});
})();
