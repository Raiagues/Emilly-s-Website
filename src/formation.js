import {FormationEngine} from './formation-model.mjs';

class FormationViewer extends FormationEngine {
  cam() {
    if (!this._cams) this._cams = {};
    var k = this.vkey();
    if (!this._cams[k]) this._cams[k] = this.camDefault(k);
    return this._cams[k];
  }
  vkey() { var s = this.state || {}; return (s.dyn || 'lin') + '-' + (s.view || 'rel'); }
  camDefault(k) { return k.indexOf('earth') > 0 ? { yaw: -0.5, pitch: 0.78, zoom: 1 } : { yaw: -0.38, pitch: 0.36, zoom: 1 }; }
  preset(name) {
    var c = this.cam(), d = this.camDefault(this.vkey());
    var P = { iso: [d.yaw, d.pitch], top: [0, 1.5607], front: [-Math.PI / 2, 0.02], side: [0, 0.02] }[name];
    c.yaw = P[0]; c.pitch = P[1]; if (name === 'iso') c.zoom = 1;
    this.drawA();
  }
  zoom(f) { var c = this.cam(); c.zoom = Math.max(0.4, Math.min(8, c.zoom * f)); this.drawA(); }
  drawA() {
    var cv = this.cvA;
    if (!cv || !cv.getContext) return;
    var st = this.state || {}, dyn = st.dyn || 'lin', mode = st.view || 'rel';
    var dpr = Math.min(window.devicePixelRatio || 1, 2), W = cv.clientWidth || 600, H = cv.clientHeight || 400;
    if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)) { cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
    var g = cv.getContext('2d');
    if (!g) return;
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, W, H);
    /* a few fixed stars */
    g.fillStyle = 'rgba(244,238,226,0.55)';
    [[0.08, 0.12], [0.2, 0.7], [0.33, 0.2], [0.5, 0.88], [0.64, 0.1], [0.77, 0.62], [0.9, 0.3], [0.95, 0.85], [0.42, 0.5], [0.13, 0.42]].forEach(function (p) { g.beginPath(); g.arc(p[0] * W, p[1] * H, 1.1, 0, 6.3); g.fill(); });
    var cam = this.cam(), cy = Math.cos(cam.yaw), sy = Math.sin(cam.yaw), cp = Math.cos(cam.pitch), sp = Math.sin(cam.pitch);
    var C = this.C(), O = this.orbit(dyn), orb = O.pts, ph = this._phase === undefined ? 0.42 : this._phase;
    var M = function (s) { return [s[1], -s[2], s[0]]; };
    var ctr = [0, 0, 0], R;
    if (mode === 'rel') {
      var a = M(O.mn), b = M(O.mx);
      ctr = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0];
      R = Math.max(Math.abs(b[0] - a[0]), Math.abs(b[1] - a[1]), Math.abs(b[2] - a[2])) * 0.62;
    } else R = 1.0e7;
    var sc = Math.min(W, H * 1.5) / (R * 2.2) * cam.zoom, Dd = R * 6;
    function P(p) {
      var px = p[0] - ctr[0], py = p[1] - ctr[1], pz = p[2] - ctr[2];
      var x1 = px * cy - py * sy, y1 = px * sy + py * cy;
      var y2 = y1 * cp - pz * sp, z2 = y1 * sp + pz * cp, k = Dd / (Dd + y2);
      return [W / 2 + x1 * sc * k, H / 2 - z2 * sc * k, y2, k];
    }
    var items = [];
    function seg(a2, b2, c, w, dash, al) { var pa = P(a2), pb = P(b2); items.push({ t: 'l', a: pa, b: pb, d: (pa[2] + pb[2]) / 2, c: c, w: w, dash: dash, al: al }); }
    function dot(p, r, c, ring) { var q = P(p); items.push({ t: 'd', p: q, d: q[2] - 1, r: r, c: c, ring: ring }); }
    function label(p, txt, c, dy, dx) { var q = P(p); items.push({ t: 't', p: [q[0] + (dx || 0), q[1] + (dy || 0)], d: -1e15, txt: txt, c: c }); }
    var idx = Math.floor(ph * (orb.length - 1));
    var CREAM = '#F4EEE2', SAGE = '#A9CBC5', CORAL = '#E58C70', SAND = '#F1E2B2';
    if (mode === 'rel') {
      var L = R * 0.9;
      seg([-L * 0.3 + ctr[0] * 0, 0, 0], [0, 0, 0], 'rgba(169,203,197,0.6)', 1, [], 1);
      seg([0, 0, 0], [L, 0, 0], 'rgba(169,203,197,0.6)', 1, [], 1);
      seg([0, -L * 0.7, 0], [0, L * 0.7, 0], 'rgba(169,203,197,0.6)', 1, [], 1);
      seg([0, 0, -L * 0.45], [0, 0, L * 0.45], 'rgba(169,203,197,0.6)', 1, [], 1);
      label([L * 1.08, 0, 0], this.labels.axis_y, SAGE);
      label([0, -L * 0.78, 0], this.labels.axis_z, SAGE);
      label([0, 0, L * 0.52], this.labels.axis_x, SAGE);
      for (var i = 0; i < orb.length - 1; i++) seg(M(orb[i]), M(orb[i + 1]), CREAM, 1.6, [5, 5], 0.85);
      for (var tt = 0; tt < 26; tt++) { var a1 = idx - tt, a0 = a1 - 1; if (a0 < 0) break; seg(M(orb[a0]), M(orb[a1]), CORAL, 3, [], 1 - tt / 26); }
      var fp = M(orb[idx]);
      seg([0, 0, 0], fp, CORAL, 1.2, [2, 4], 0.8);
      dot(fp, 7, CORAL, '#1F4A4F');
      dot([0, 0, 0], 8, SAND, '#1F4A4F');
      label([fp[0], fp[1], fp[2] + R * 0.09], this.labels.follower, CORAL);
      label([0, 0, -R * 0.1], this.labels.leader, SAND);
    } else {
      var Re = C.RE, ex = dyn === 'lin' ? 15 : 3;
      var E = P([0, 0, 0]);
      items.push({ t: 'e', p: E, d: E[2], r: Re * sc * E[3] });
      var lead = function (s) {
        if (dyn === 'lin') { var th = 2 * Math.PI * (orb.indexOf(s) / (orb.length - 1)); return { r: C.A0, th: th }; }
        return { r: s[6], th: s[8] };
      };
      var abs = function (s, mag) {
        var L2 = lead(s), rx = L2.r + mag * s[0], ry = mag * s[1];
        return [rx * Math.cos(L2.th) - ry * Math.sin(L2.th), rx * Math.sin(L2.th) + ry * Math.cos(L2.th), mag * s[2]];
      };
      var pl = null, pf = null;
      for (var k = 0; k < orb.length; k++) {
        var ql = abs(orb[k], 0), qf = abs(orb[k], ex);
        if (pl) { seg(pl, ql, SAND, 1.6, [], 0.95); seg(pf, qf, CORAL, 1.6, [5, 5], 0.95); }
        pl = ql; pf = qf;
      }
      var lp = abs(orb[idx], 0), fq = abs(orb[idx], ex);
      seg(lp, fq, CORAL, 1.2, [2, 3], 1);
      var er = Re * sc * E[3];
      var hid = function (p) { var q = P(p), dx = q[0] - E[0], dy = q[1] - E[1]; return dx * dx + dy * dy < er * er && q[2] > E[2]; };
      if (!hid(lp)) { dot(lp, 7, SAND, '#1F4A4F'); label(lp, this.labels.leader, SAND, 18, -34); }
      if (!hid(fq)) { dot(fq, 6, CORAL, '#1F4A4F'); label(fq, this.labels.follower, CORAL, -18, 40); }
    }
    items.sort(function (p, q) { return q.d - p.d; });
    items.forEach(function (o) {
      g.globalAlpha = o.al === undefined ? 1 : o.al;
      if (o.t === 'l') {
        g.beginPath(); g.moveTo(o.a[0], o.a[1]); g.lineTo(o.b[0], o.b[1]);
        g.strokeStyle = o.c; g.lineWidth = o.w; g.lineCap = 'round'; g.setLineDash(o.dash || []); g.stroke(); g.setLineDash([]);
      } else if (o.t === 'd') {
        g.beginPath(); g.arc(o.p[0], o.p[1], o.r, 0, Math.PI * 2); g.fillStyle = o.c; g.fill();
        if (o.ring) { g.lineWidth = 2.5; g.strokeStyle = o.ring; g.stroke(); }
      } else if (o.t === 'e') {
        var gr = g.createRadialGradient(o.p[0] - o.r * 0.35, o.p[1] - o.r * 0.4, o.r * 0.1, o.p[0], o.p[1], o.r);
        gr.addColorStop(0, '#CFE3DF'); gr.addColorStop(0.55, '#7FA9A3'); gr.addColorStop(1, '#3D6F6C');
        g.beginPath(); g.arc(o.p[0], o.p[1], o.r, 0, Math.PI * 2); g.fillStyle = gr; g.fill();
        g.lineWidth = 6; g.strokeStyle = 'rgba(169,203,197,0.25)'; g.stroke();
      } else if (o.t === 't') {
        g.font = '11px "Space Mono", monospace'; g.fillStyle = o.c; g.textAlign = 'center'; g.textBaseline = 'middle';
        const text = o.txt.toUpperCase(), half = Math.min(g.measureText(text).width, W - 24) / 2;
        g.fillText(text, Math.max(half + 12, Math.min(W - half - 12, o.p[0])), Math.max(95, Math.min(H - 60, o.p[1])), W - 24);
      }
    });
    g.globalAlpha = 1;
  }

  /* ================= text helpers ================= */
}

const root = document.querySelector('[data-formation]');
if (root) start(root);

function start(root) {
  const config = JSON.parse(document.querySelector('#formation-data').textContent);
  const status = root.querySelector('[data-formation-status]');
  const viewer = new FormationViewer();
  viewer.labels = config.text;
  viewer.state = {dyn: 'lin', view: 'rel'};
  viewer.cvA = root.querySelector('canvas');
  let state = {dyn: 'lin', view: 'rel', kstep: 1, noise: 'n14', trust: 'mine', seed: 1, thr: 'free'};
  let shown = {...state}, serial = 0, timer, worker, fallback, stopped = false;
  const htmlCache = new Map();
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reduced.matches, visible = false, raf = 0, last = 0;
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const lookup = (key, context) => key.split('.').reduce((obj, part) => obj[part], context);
  const raw = (value, context) => {
    value = config.translations[String(value)] ?? String(value);
    return value.replace(/\{\{([\w.-]+)\}\}/g, (_, key) => raw(lookup(key, context), context));
  };
  function fill(template, context) {
    const loop = /<sc-for\s+as="(\w+)"\s+list="\{\{([\w.]+)\}\}">/;
    let match;
    while ((match = loop.exec(template))) {
      let depth = 1, begin = match.index + match[0].length, start, end;
      for (const tag of template.slice(begin).matchAll(/<sc-for\b[^>]*>|<\/sc-for>/g)) {
        depth += tag[0].startsWith('</') ? -1 : 1;
        if (!depth) {start = begin + tag.index; end = start + tag[0].length; break;}
      }
      if (depth) throw new Error('Unclosed formation template');
      const body = template.slice(begin, start);
      const out = lookup(match[2], context).map(item => fill(body, {...context, [match[1]]: item})).join('');
      template = template.slice(0, match.index) + out + template.slice(end);
    }
    return template.replace(/\{\{([\w.-]+)\}\}/g, (_, key) => escape(raw(lookup(key, context), context)));
  }
  function update(values) {
    const context = {...values, text: config.text};
    for (const [name, template] of Object.entries(config.templates)) {
      const html = fill(template, context);
      if (htmlCache.get(name) === html) continue;
      htmlCache.set(name, html);
      const region = root.querySelector(`[data-region="${name}"]`);
      const active = region.contains(document.activeElement) ? document.activeElement : null;
      const focus = active?.dataset.control ? {key: active.dataset.control, value: active.dataset.value} : null;
      const canvasFocused = active === viewer.cvA;
      const fragment = document.createElement('template');
      fragment.innerHTML = html;
      const canvas = fragment.content.querySelector('canvas');
      if (canvas) canvas.replaceWith(viewer.cvA);
      region.replaceChildren(fragment.content);
      if (canvasFocused) viewer.cvA.focus({preventScroll:true});
      else if (focus) {
        const next = [...region.querySelectorAll('[data-control]')].find(el => el.dataset.control === focus.key && el.dataset.value === focus.value);
        next?.focus({preventScroll:true});
      }
    }
    viewer.state = {...state};
    shown = {...state};
    viewer.drawA();
    root.dataset.model = state.dyn;
    root.dataset.seed = state.seed;
    root.dataset.ready = 'true';
    root.setAttribute('aria-busy','false');
    root.querySelectorAll('[data-control]').forEach(el => el.disabled = false);
    syncMotion();
  }
  function error() {
    state = {...shown};
    root.setAttribute('aria-busy','false');
    status.classList.add('formation-error');
    status.textContent = config.text.error;
  }
  function receive({id, values, error: failed}) {
    if (stopped || id !== serial) return;
    clearTimeout(timer);
    if (failed) return error();
    try {update(values);status.textContent = config.text.ready;} catch {error();}
  }
  function fallbackRun(id, next) {
    setTimeout(() => {
      if (id !== serial || stopped) return;
      try {
        fallback ??= new FormationEngine();
        fallback.state = next;
        receive({id, values:fallback.renderVals()});
      } catch {receive({id,error:true});}
    }, 30);
  }
  function run() {
    const id = ++serial, next = structuredClone(state);
    root.setAttribute('aria-busy','true');
    status.classList.remove('formation-error');
    status.textContent = config.text.busy;
    clearTimeout(timer);
    if (worker) {
      worker.postMessage({id,state:next});
      timer = setTimeout(() => {
        worker?.terminate();worker = null;fallbackRun(id,next);
      },10000);
    } else fallbackRun(id,next);
  }
  try {
    worker = new Worker(new URL(config.worker,location.href),{type:'module'});
    worker.onmessage = e => receive(e.data);
    worker.onerror = e => {
      e.preventDefault();worker?.terminate();worker = null;clearTimeout(timer);
      fallbackRun(serial,structuredClone(state));
    };
  } catch {worker = null;}

  function syncMotion() {
    root.dataset.paused = String(paused);
    const button = root.querySelector('[data-control="pause"]');
    button.textContent = paused ? config.text.resume : config.text.pause;
    button.setAttribute('aria-pressed', String(paused));
    const moving = !paused && visible && !document.hidden && !stopped;
    root.dataset.animating = String(moving);
    if (!moving) {cancelAnimationFrame(raf);raf = 0;last = 0;}
    else if (!raf) raf = requestAnimationFrame(tick);
  }
  function tick(time) {
    if (last) viewer._phase = ((viewer._phase ?? .42) + Math.min(time-last,64)/20000)%1;
    last = time;
    viewer.drawA();
    raf = requestAnimationFrame(tick);
  }
  root.addEventListener('click', e => {
    const button = e.target.closest('[data-control]');
    if (!button || !root.contains(button)) return;
    const key = button.dataset.control, value = button.dataset.value;
    if (key === 'pause') {paused = !paused;syncMotion();return;}
    if (key === 'preset') {viewer.preset(value);return;}
    if (key === 'zoomIn' || key === 'zoomOut') {viewer.zoom(key === 'zoomIn' ? 1.25 : .8);return;}
    if (key === 'cell') {
      if (state.dyn !== shown.dyn) return;
      state.cell = {dyn:state.dyn,k:value};
    }
    else if (key === 'nextStep') state.kstep = state.kstep % 4 + 1;
    else if (key === 'rerun') state.seed++;
    else if (['dyn','view','kstep','noise','trust','thr'].includes(key)) state[key] = key === 'kstep' ? Number(value) : value;
    else return;
    run();
  });
  root.addEventListener('keydown', e => {
    const cell = e.target.closest('[data-control="cell"]');
    if (!cell || !['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home','End'].includes(e.key)) return;
    e.preventDefault();
    const n = shown.dyn === 'lin' ? 6 : 10;
    let [row,col] = cell.dataset.value.split(',').map(Number);
    if (e.key === 'ArrowLeft') col = (col+n-1)%n;
    if (e.key === 'ArrowRight') col = (col+1)%n;
    if (e.key === 'ArrowUp') row = (row+n-1)%n;
    if (e.key === 'ArrowDown') row = (row+1)%n;
    if (e.key === 'Home') col = 0;
    if (e.key === 'End') col = n-1;
    const next = root.querySelector(`[data-control="cell"][data-value="${row},${col}"]`);
    next.focus({preventScroll:true});next.click();
  });
  const canvas = viewer.cvA, pointers = new Map();
  let pinch = 0;
  canvas.addEventListener('pointerdown', e => {
    pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});canvas.setPointerCapture(e.pointerId);
    canvas.style.cursor = 'grabbing';pinch = distance();
  });
  const distance = () => {
    const [a,b] = [...pointers.values()];return b ? Math.hypot(a.x-b.x,a.y-b.y) : 0;
  };
  canvas.addEventListener('pointermove', e => {
    const previous = pointers.get(e.pointerId);if (!previous) return;
    pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});
    if (pointers.size > 1) {
      const next = distance();if (pinch && next) viewer.zoom(next/pinch);pinch = next;
    } else {
      const c = viewer.cam();c.yaw += (e.clientX-previous.x)*.008;
      c.pitch = Math.max(-1.56,Math.min(1.56,c.pitch+(e.clientY-previous.y)*.008));viewer.drawA();
    }
  });
  const end = e => {pointers.delete(e.pointerId);pinch = distance();canvas.style.cursor = pointers.size ? 'grabbing' : 'grab';};
  ['pointerup','pointercancel','lostpointercapture'].forEach(name=>canvas.addEventListener(name,end));
  canvas.addEventListener('wheel',e=>{e.preventDefault();viewer.zoom(Math.exp(-e.deltaY*.0015));},{passive:false});
  canvas.addEventListener('keydown',e=>{
    if (!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','=','-','Home'].includes(e.key)) return;
    e.preventDefault();const c = viewer.cam();
    if (e.key === 'Home') return viewer.preset('iso');
    if (e.key === '+' || e.key === '=') return viewer.zoom(1.25);
    if (e.key === '-') return viewer.zoom(.8);
    c.yaw += e.key === 'ArrowLeft' ? -.12 : e.key === 'ArrowRight' ? .12 : 0;
    c.pitch = Math.max(-1.56,Math.min(1.56,c.pitch+(e.key === 'ArrowUp' ? -.12 : e.key === 'ArrowDown' ? .12 : 0)));
    viewer.drawA();
  });
  const observer = new IntersectionObserver(entries=>{visible = entries[0].isIntersecting;syncMotion();},{threshold:.1});
  observer.observe(canvas);
  new ResizeObserver(()=>viewer.drawA()).observe(canvas);
  document.addEventListener('visibilitychange',syncMotion);
  reduced.addEventListener('change',()=>{paused = reduced.matches;syncMotion();});
  window.addEventListener('pagehide',()=>{stopped = true;clearTimeout(timer);worker?.terminate();worker=null;syncMotion();});
  window.addEventListener('pageshow',e=>{
    if(e.persisted){stopped=false;syncMotion();if(root.getAttribute('aria-busy')==='true')run();}
  });
  viewer.drawA();
  root.classList.add('formation-enhanced');
  root.querySelectorAll('[data-control]').forEach(el=>el.disabled=false);
  syncMotion();run();
}
