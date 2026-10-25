/* Schematic geometry and historical load formulas adapted from the supplied Wingbox design. */
(() => {
"use strict";
class WingViewer {
  constructor(conditions) { this.conditions = conditions; this.state = {cond: 1, mode: "loads"}; }
  data() { return {C: this.conditions}; }
  loads(c) {
    /* same formulas as PLOTS.distribuicao_forcas and AERODINAMICA, lift and drag only */
    var W = 9.80665 * 5500, b = 12, S = 24, rho = 1, CD0 = 0.017, K = 0.021, N = 50;
    var L = c.n * W, ys = [], Le = [], De = [];
    for (var i = 0; i < N; i++) {
      var y = 6 * i / (N - 1);
      var we = (4 * L / (Math.PI * b)) * Math.sqrt(Math.max(0, 1 - Math.pow(2 * y / b, 2)));
      var l = (we + L / b) / 2;
      var CL = 2 * l / (rho * c.v * c.v * S);
      ys.push(y); Le.push(l); De.push(0.5 * rho * c.v * c.v * (CD0 + K * CL * CL) * S);
    }
    function fromTip(f) { var out = new Array(N); out[N - 1] = 0; for (var j = N - 2; j >= 0; j--) out[j] = out[j + 1] + (f[j] + f[j + 1]) / 2 * (ys[j + 1] - ys[j]); return out; }
    function fromRoot(f) { var out = new Array(N); out[0] = 0; for (var j = 1; j < N; j++) out[j] = out[j - 1] + (f[j] + f[j - 1]) / 2 * (ys[j] - ys[j - 1]); return out; }
    var V = fromTip(Le), M = fromTip(V);
    var slope = fromRoot(M), defl = fromRoot(slope);
    var m = 0.5 * rho * c.v * c.v * (-0.078) * S * 2;
    var mdist = m / 6, T = ys.map(function (y) { return mdist * (6 - y); });
    var twist = fromRoot(T);
    return { ys: ys, L: Le, D: De, V: V, M: M, defl: defl, T: T, twist: twist, Ltot: L, m: m, mdist: mdist };
  }

  /* ---------------- tiny 3D renderer on a 2D canvas ---------------- */
  cams() {
    if (!this._cams) this._cams = { A: { yaw: -0.5, pitch: 0.38, zoom: 1.2 }, B: { yaw: -0.55, pitch: 0.42, zoom: 1.15 } };
    return this._cams;
  }
  preset(key, name) {
    var c = this.cams()[key];
    var P = { iso: [key === 'A' ? -0.5 : -0.55, key === 'A' ? 0.38 : 0.42], top: [0, 1.5607], front: [-Math.PI / 2, 0.02], side: [0, 0.02] }[name];
    c.yaw = P[0]; c.pitch = P[1]; if (name === 'iso') c.zoom = key === 'A' ? 1.2 : 1.15;
    this.drawOne(key);
  }
  zoom(key, f) { var c = this.cams()[key]; c.zoom = Math.max(0.5, Math.min(6, c.zoom * f)); this.drawOne(key); }
  shade(hex, f) {
    var n = parseInt(hex.slice(1), 16), r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
    r = Math.min(255, Math.round(r * f)); g = Math.min(255, Math.round(g * f)); b = Math.min(255, Math.round(b * f));
    return 'rgb(' + r + ',' + g + ',' + b + ')';
  }
  render(cv, cam, items, center, radius) {
    if (!cv || !cv.getContext) return;
    var dpr = Math.min(window.devicePixelRatio || 1, 2), W = cv.clientWidth || 600, H = cv.clientHeight || 380;
    if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)) { cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
    var g = cv.getContext('2d');
    if (!g) return;
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, W, H);
    var cy = Math.cos(cam.yaw), sy = Math.sin(cam.yaw), cp = Math.cos(cam.pitch), sp = Math.sin(cam.pitch);
    var sc = Math.min(W, H * 1.6) / (radius * 2.3) * cam.zoom, Dd = radius * 5;
    function P(p) {
      var x = p[0] - center[0], y = p[1] - center[1], z = p[2] - center[2];
      var x1 = x * cy - y * sy, y1 = x * sy + y * cy;
      var y2 = y1 * cp - z * sp, z2 = y1 * sp + z * cp;
      var k = Dd / (Dd + y2);
      return [W / 2 + x1 * sc * k, H / 2 - z2 * sc * k, y2];
    }
    var light = [0.35, -0.45, 0.82];
    var self = this, list = [];
    items.forEach(function (it) {
      var pp = it.pts.map(P), d = 0;
      pp.forEach(function (q) { d += q[2]; });
      d = d / pp.length + (it.bias || 0);
      var col = it.c;
      if (it.t === 'poly' && it.pts.length > 2) {
        var a = it.pts[0], b = it.pts[1], c2 = it.pts[2];
        var u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], v = [c2[0] - a[0], c2[1] - a[1], c2[2] - a[2]];
        var n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
        var ln = Math.sqrt(n[0] * n[0] + n[1] * n[1] + n[2] * n[2]) || 1;
        var dot = Math.abs((n[0] * light[0] + n[1] * light[1] + n[2] * light[2]) / ln);
        col = self.shade(it.c, 0.72 + 0.38 * dot);
      }
      list.push({ it: it, pp: pp, d: d, col: col });
    });
    list.sort(function (p, q) { return q.d - p.d; });
    list.forEach(function (o) {
      var it = o.it, pp = o.pp;
      g.globalAlpha = it.a === undefined ? 1 : it.a;
      g.beginPath();
      g.moveTo(pp[0][0], pp[0][1]);
      for (var i = 1; i < pp.length; i++) g.lineTo(pp[i][0], pp[i][1]);
      if (it.t === 'poly') {
        g.closePath(); g.fillStyle = o.col; g.fill();
        if (it.s) { g.globalAlpha = it.sa === undefined ? 0.8 : it.sa; g.strokeStyle = it.s; g.lineWidth = it.w || 0.7; g.stroke(); }
      } else {
        g.strokeStyle = it.c; g.lineWidth = it.w || 1.5; g.lineCap = 'round'; g.setLineDash(it.dash || []); g.stroke(); g.setLineDash([]);
      }
    });
    g.globalAlpha = 1;
  }
  arrow(items, a, b, color, w) {
    items.push({ t: 'line', pts: [a, b], c: color, w: w || 2.2, bias: -0.02 });
    var d = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], L = Math.sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2]);
    if (L < 1e-6) return;
    var hl = Math.min(0.12, L * 0.35), u = [d[0] / L, d[1] / L, d[2] / L];
    var side = Math.abs(u[0]) > 0.9 ? [0, 1, 0] : [1, 0, 0];
    var s2 = [u[1] * side[2] - u[2] * side[1], u[2] * side[0] - u[0] * side[2], u[0] * side[1] - u[1] * side[0]];
    var base = [b[0] - u[0] * hl, b[1] - u[1] * hl, b[2] - u[2] * hl];
    items.push({ t: 'line', pts: [[base[0] + s2[0] * hl * 0.5, base[1] + s2[1] * hl * 0.5, base[2] + s2[2] * hl * 0.5], b, [base[0] - s2[0] * hl * 0.5, base[1] - s2[1] * hl * 0.5, base[2] - s2[2] * hl * 0.5]], c: color, w: w || 2.2, bias: -0.03 });
  }
  airfoil() {
    /* NACA 2415-like outline, a simplified stand-in for the NACA 63A415 */
    var m = 0.02, p = 0.4, t = 0.15, N = 22, up = [], lo = [];
    for (var i = 0; i <= N; i++) {
      var x = (1 - Math.cos(Math.PI * i / N)) / 2;
      var yt = 5 * t * (0.2969 * Math.sqrt(x) - 0.126 * x - 0.3516 * x * x + 0.2843 * x * x * x - 0.1036 * x * x * x * x);
      var yc = x < p ? m / (p * p) * (2 * p * x - x * x) : m / ((1 - p) * (1 - p)) * (1 - 2 * p + 2 * p * x - x * x);
      up.push([x, yc + yt]); lo.push([x, yc - yt]);
    }
    return { up: up, lo: lo };
  }
  sceneB(modeArg) {
    var s = this.state || {}, C = this.data().C, c = C[(s.cond || 1) - 1], mode = modeArg || s.mode || 'loads';
    if (mode === 'structure') c = C[0];
    var Ld = this.loads(c), af = this.airfoil(), items = [];
    var chord = 2, LE = -1;
    var N = Ld.ys.length;
    function idx(x) { return Math.min(N - 1, Math.round(x / 6 * (N - 1))); }
    var dmax = Math.abs(Ld.defl[N - 1]) || 1, tmax = Math.abs(Ld.twist[N - 1]) || 1;
    var defScale = mode === 'bend' ? 0.7 * (c.n / 7.5) : 0;
    var twScale = mode === 'torque' ? (12 * Math.PI / 180) * (Ld.m / Math.abs(this.loads(C[1]).m)) : 0;
    var pivot = [-0.1, 0];
    function sec(x, X, Z) {
      var i = idx(x);
      var dz = defScale * Ld.defl[i] / dmax;
      var th = -twScale * Ld.twist[i] / tmax;
      var y = LE + X * chord, z = Z * chord;
      var yy = pivot[0] + (y - pivot[0]) * Math.cos(th) - (z - pivot[1]) * Math.sin(th);
      var zz = pivot[1] + (y - pivot[0]) * Math.sin(th) + (z - pivot[1]) * Math.cos(th);
      return [x, yy, zz + dz];
    }
    var segs = 12, SK = '#C3CCD8', skinA = mode === 'structure' ? 0.12 : 0.16;
    var outline = af.up.slice().reverse().concat(af.lo.slice(1));
    for (var k = 0; k < segs; k++) {
      var x0 = 6 * k / segs, x1 = 6 * (k + 1) / segs;
      for (var i = 0; i < outline.length - 1; i++) {
        var a = outline[i], b = outline[i + 1];
        items.push({ t: 'poly', pts: [sec(x0, a[0], a[1]), sec(x1, a[0], a[1]), sec(x1, b[0], b[1]), sec(x0, b[0], b[1])], c: SK, a: skinA });
      }
    }
    [0, 6].forEach(function (x) { items.push({ t: 'poly', pts: outline.map(function (p) { return sec(x, p[0], p[1]); }), c: SK, a: 0.35, s: '#6B7785', sa: 0.9, w: 1 }); });
    for (var r = 1; r < 21; r++) { var xr = 6 * r / 21; items.push({ t: 'line', pts: outline.map(function (p) { return sec(xr, p[0], p[1]); }), c: '#9AA5B1', w: 0.8, bias: 0.02 }); }
    /* wing box placed as in the CAD model, between 25% and 65% of the chord */
    function surf(list, X) { for (var i = 0; i < list.length - 1; i++) if (X >= list[i][0] && X <= list[i + 1][0]) { var f = (X - list[i][0]) / (list[i + 1][0] - list[i][0]); return list[i][1] + f * (list[i + 1][1] - list[i][1]); } return 0; }
    var bx0 = 0.25, bx1 = 0.65, zt = Math.min(surf(af.up, bx0), surf(af.up, bx1)) - 0.004, zb = Math.max(surf(af.lo, bx0), surf(af.lo, bx1)) + 0.004;
    var webs = [bx0, bx0 + (bx1 - bx0) / 3, bx0 + 2 * (bx1 - bx0) / 3, bx1];
    for (var k2 = 0; k2 < segs; k2++) {
      var xa = 6 * k2 / segs, xb = 6 * (k2 + 1) / segs;
      items.push({ t: 'poly', pts: [sec(xa, bx0, zt), sec(xb, bx0, zt), sec(xb, bx1, zt), sec(xa, bx1, zt)], c: '#8080FF', a: 0.55, s: '#3A3AD0', sa: 0.3, w: 0.5 });
      items.push({ t: 'poly', pts: [sec(xa, bx0, zb), sec(xb, bx0, zb), sec(xb, bx1, zb), sec(xa, bx1, zb)], c: '#8080FF', a: 0.55, s: '#3A3AD0', sa: 0.3, w: 0.5 });
      webs.forEach(function (X) { items.push({ t: 'poly', pts: [sec(xa, X, zb), sec(xb, X, zb), sec(xb, X, zt), sec(xa, X, zt)], c: '#80C080', a: 0.7, s: '#2E7D2E', sa: 0.3, w: 0.5 }); });
    }
    if (mode === 'structure') {
      var self2 = this;
      function bstrip(X, Z, col) { for (var k3 = 0; k3 < segs; k3++) items.push({ t: 'line', pts: [sec(6 * k3 / segs, X, Z), sec(6 * (k3 + 1) / segs, X, Z)], c: col, w: 1.8, bias: -0.01 }); }
      var cw = (bx1 - bx0) / 3, hh = zt - zb;
      for (var i4 = 0; i4 < 4; i4++) { bstrip(bx0 + (i4 + 1) * cw / 5, zt - 0.006, '#1F1FB0'); bstrip(bx0 + 2 * cw + (i4 + 1) * cw / 5, zb + 0.006, '#1F1FB0'); }
      for (var i5 = 0; i5 < 2; i5++) { var zz2 = zb + (i5 + 1) * hh / 3; bstrip(bx0 + 0.006, zz2, '#1E6B1E'); bstrip(bx1 - 0.006, zz2, '#1E6B1E'); }
    }
    var maxL = 38315;
    if (mode === 'loads') {
      for (var st = 0; st <= 10; st++) {
        var x = 6 * st / 10, i2 = idx(x), l = Ld.L[i2], d = Ld.D[i2];
        var base = sec(x, 0.25, l >= 0 ? surf(af.up, 0.25) : surf(af.lo, 0.25));
        this.arrow(items, base, [base[0], base[1], base[2] + 1.1 * l / maxL], '#FF0000', 2.4);
        var tb = sec(x, 1, 0);
        this.arrow(items, tb, [tb[0], tb[1] + 1.1 * 5 * d / maxL, tb[2]], '#0000FF', 2);
      }
    }
    if (mode === 'torque') {
      var sign = Ld.m < 0 ? -1 : 1;
      for (var st2 = 0; st2 <= 4; st2++) {
        var x2 = 0.6 + 4.8 * st2 / 4, pts = [];
        for (var q = 0; q <= 14; q++) { var ang = sign * (0.3 + 4.2 * q / 14), rr = 0.42; pts.push(sec(x2, (pivot[0] - LE) / chord + rr * Math.cos(ang) / chord, rr * Math.sin(ang) / chord)); }
        items.push({ t: 'line', pts: pts, c: '#1F77B4', w: 2.2, bias: -0.05 });
        this.arrow(items, pts[pts.length - 2], pts[pts.length - 1], '#1F77B4', 2.2);
      }
    }
    if (mode === 'bend' || mode === 'torque') {
      var tipGhost = outline.map(function (p) { return [6, LE + p[0] * chord, p[1] * chord]; });
      items.push({ t: 'line', pts: tipGhost, c: '#55605E', w: 1, dash: [4, 4], bias: -0.1 });
    }
    return { items: items, center: [3, -0.1, 0.1], radius: 3.4 };
  }
  drawOne(key) {
    var cv = this['cv' + key];
    if (!cv) return;
    var sc = key === 'A' ? this.sceneB('structure') : this.sceneB();
    this.render(cv, this.cams()[key], sc.items, sc.center, sc.radius);
  }

}
const page = document.querySelector('.wingbox-page');
const data = document.getElementById('wingbox-data');
if (!page || !data) return;
const config = JSON.parse(data.textContent);
const viewer = new WingViewer(config.conditions);
const state = {condition: '1', mode: 'loads', torsion: 'f', top: 'ideal', side: 'ideal', ribs: 'ideal'};
const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
const status = page.querySelector('[data-wing-status]');
let announcement;
function announce(message) {
  clearTimeout(announcement);
  announcement = setTimeout(() => { status.textContent = message; }, 90);
}
function update() {
  const visible = (selector, key) => page.querySelectorAll(selector).forEach(el => {
    el.hidden = el.getAttribute(selector.slice(1, -1)) !== key;
  });
  visible('[data-envelope-panel]', state.condition);
  visible('[data-charts-panel]', `${state.condition}-${state.mode}`);
  visible('[data-load-summary]', `${state.condition}-${state.mode}`);
  visible('[data-torsion-panel]', state.torsion);
  page.querySelectorAll('[data-part-panel]').forEach(el => {
    const [part, choice] = el.dataset.partPanel.split('-');
    el.hidden = state[part] !== choice;
  });
  for (const key of ['condition', 'mode', 'torsion']) {
    page.querySelectorAll(`[data-${key}]`).forEach(el => el.setAttribute('aria-pressed', String(el.dataset[key] === state[key])));
  }
  viewer.state.cond = Number(state.condition);
  viewer.state.mode = state.mode;
  viewer.drawOne('B');
  page.dataset.selectedCondition = state.condition;
  page.dataset.selectedMode = state.mode;
}

// Pointer capture keeps a drag within its viewer; a second finger pinches to zoom.
function bindCanvas(canvas, key) {
  if (!canvas.getContext('2d')) return;
  viewer['cv' + key] = canvas;
  const points = new Map();
  let last = null;
  function gesture() {
    const p = [...points.values()];
    if (!p.length) return null;
    return p.length === 1 ? {x: p[0].x, y: p[0].y, distance: 0} :
      {x: (p[0].x + p[1].x) / 2, y: (p[0].y + p[1].y) / 2, distance: Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y)};
  }
  function rotate(dx, dy) {
    const cam = viewer.cams()[key];
    cam.yaw += dx;
    cam.pitch = Math.max(-1.56, Math.min(1.56, cam.pitch + dy));
    page.querySelectorAll(`[data-view][data-camera="${key}"]`).forEach(el => el.setAttribute('aria-pressed', 'false'));
    viewer.drawOne(key);
  }
  canvas.addEventListener('pointerdown', event => {
    if (event.pointerType === 'mouse' && event.button !== 0) return;
    points.set(event.pointerId, {x: event.clientX, y: event.clientY});
    canvas.setPointerCapture(event.pointerId);
    last = gesture(); canvas.style.cursor = 'grabbing';
  });
  canvas.addEventListener('pointermove', event => {
    if (!points.has(event.pointerId)) return;
    points.set(event.pointerId, {x: event.clientX, y: event.clientY});
    const now = gesture();
    if (last && now.distance && last.distance) viewer.zoom(key, now.distance / last.distance);
    else if (last && now && !now.distance) rotate((now.x - last.x) * .008, (now.y - last.y) * .008);
    last = now;
  });
  const end = event => {
    points.delete(event.pointerId); last = gesture();
    if (!points.size) canvas.style.cursor = '';
  };
  for (const type of ['pointerup', 'pointercancel', 'lostpointercapture']) canvas.addEventListener(type, end);
  canvas.addEventListener('wheel', event => {
    // Browser zoom remains available with Ctrl/Cmd; ordinary scrolling zooms the model.
    if (event.ctrlKey || event.metaKey) return;
    event.preventDefault();
    viewer.zoom(key, Math.exp(-event.deltaY * .0015));
  }, {passive: false});
  canvas.addEventListener('keydown', event => {
    const turns = {ArrowLeft: [-.15, 0], ArrowRight: [.15, 0], ArrowUp: [0, -.15], ArrowDown: [0, .15]};
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    if (turns[event.key]) rotate(...turns[event.key]);
    else if (event.key === '+' || event.key === '=') viewer.zoom(key, 1.25);
    else if (event.key === '-' || event.key === '−') viewer.zoom(key, .8);
    else if (event.key === 'Home') setView(key, 'iso');
    else return;
    event.preventDefault();
  });
  const observer = new ResizeObserver(() => viewer.drawOne(key));
  observer.observe(canvas);
  viewer.drawOne(key);
  canvas.dataset.ready = 'true';
  canvas.parentElement.querySelector('.wingbox-canvas-fallback').hidden = true;
}
function setView(key, view) {
  viewer.preset(key, view);
  page.querySelectorAll(`[data-view][data-camera="${key}"]`).forEach(el => el.setAttribute('aria-pressed', String(el.dataset.view === view)));
}
for (const canvas of page.querySelectorAll('[data-wing-canvas]')) {
  try { bindCanvas(canvas, canvas.dataset.wingCanvas); setView(canvas.dataset.wingCanvas, 'iso'); }
  catch { /* Keep the supplied CAD image if this browser cannot draw a canvas. */ }
}
page.querySelectorAll('[data-wing-control]').forEach(el => {
  if (el.dataset.camera && !viewer['cv' + el.dataset.camera]) return;
  el.removeAttribute('disabled');
  if (el.classList.contains('vpt')) { el.removeAttribute('aria-disabled'); el.tabIndex = 0; }
});
page.addEventListener('click', event => {
  const el = event.target.closest('[data-condition],[data-mode],[data-torsion],[data-choice],[data-view],[data-zoom]');
  if (!el || el.disabled) return;
  if (el.dataset.view) { setView(el.dataset.camera, el.dataset.view); return; }
  if (el.dataset.zoom) { viewer.zoom(el.dataset.camera, Number(el.dataset.zoom)); return; }
  const fromDiagram = el.closest('[data-envelope-panel]');
  if (el.dataset.condition) state.condition = el.dataset.condition;
  if (el.dataset.mode) state.mode = el.dataset.mode;
  if (el.dataset.torsion) state.torsion = el.dataset.torsion;
  if (el.dataset.choice) state[el.dataset.part] = el.dataset.choice;
  update();
  // The old SVG/part panel is now hidden. Keep keyboard focus on its replacement.
  if (fromDiagram) page.querySelector(`[data-envelope-panel="${state.condition}"] [data-condition="${state.condition}"]`).focus({preventScroll: true});
  if (el.dataset.choice) {
    const result = page.querySelector(`[data-part-panel="${el.dataset.part}-${el.dataset.choice}"]`);
    result.querySelector(`[data-choice="${el.dataset.choice}"]`).focus({preventScroll: true});
    announce(result.querySelector('[data-verdict]').textContent + ' · ' + result.querySelector('[data-critical]').textContent);
  } else if (el.dataset.torsion) {
    announce(config.selection + ': ' + el.textContent.trim());
  } else {
    announce(config.selection + ': P' + state.condition + ' · ' + config.modes[state.mode]);
  }
});
page.addEventListener('keydown', event => {
  const point = event.target.closest('.vpt');
  if (point && (event.key === 'Enter' || event.key === ' ')) {
    event.preventDefault(); point.dispatchEvent(new MouseEvent('click', {bubbles: true}));
  }
});

const flowButton = page.querySelector('[data-flow-toggle]');
let paused = motion.matches;
function flowState() {
  page.dataset.flowPaused = String(paused);
  flowButton.setAttribute('aria-pressed', String(paused));
  flowButton.setAttribute('aria-label', paused ? config.resume : config.pause);
  flowButton.title = paused ? config.resume : config.pause;
  flowButton.textContent = paused ? '▶' : 'Ⅱ';
}
flowButton.hidden = false;
flowButton.addEventListener('click', () => { paused = !paused; flowState(); });
motion.addEventListener('change', event => { paused = event.matches; flowState(); });
flowState(); update();
page.dataset.ready = 'true';
})();
