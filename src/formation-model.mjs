/* Equations and educational scenarios adapted from the supplied Formation prototype.
 * Not an exact reproduction of the original MATLAB result logs. See content/ita-formation/README.md. */
export class FormationEngine {
  C() {
    var MU = 3.986004418e14, RE = 6378140, A0 = RE + 600e3;
    return { MU: MU, RE: RE, A0: A0, N0: Math.sqrt(MU / Math.pow(A0, 3)), D2R: Math.PI / 180 };
  }
  setup(dyn) {
    var c = this.C();
    if (dyn === 'lin') {
      return { nx: 6, X0: [69.78e3, 139.56e3, 104.67e3, 7.5579, -151.116, 15.116], P0: [20, 20, 20, 0.1, 0.1, 0.1], Q: [1, 1, 1, 0.01, 0.01, 0.01] };
    }
    var e0 = 0.1, r0 = c.A0 * (1 - e0 * e0) / (1 + e0), td = Math.sqrt(c.MU / Math.pow(c.A0 * (1 - e0 * e0), 3)) * Math.pow(1 + e0, 2);
    return {
      nx: 10,
      X0: [-0.01127 * c.A0, 0, 0.1 * c.A0, 0.02 * c.N0 * c.A0, 0.02 * c.N0 * c.A0, 0, r0, 0, 0, td],
      P0: [20, 20, 20, 0.1, 0.1, 0.1, 0.15, 1e-10, 1e-10 * c.D2R, 0.001 * c.D2R],
      Q: [1, 1, 1, 0.01, 0.01, 0.01, 1, 1e-15, 1e-15 * c.D2R, 1e-4 * c.D2R]
    };
  }
  fdyn(dyn, s) {
    var c = this.C(), MU = c.MU;
    if (dyn === 'lin') { var n = c.N0; return [s[3], s[4], s[5], 2 * n * s[4] + 3 * n * n * s[0], -2 * n * s[3], -n * n * s[2]]; }
    var x = s[0], y = s[1], z = s[2], xd = s[3], yd = s[4], r0 = s[6], r0d = s[7], td = s[9];
    var rr = Math.pow((r0 + x) * (r0 + x) + y * y + z * z, 1.5), tdd = -2 * r0d * td / r0;
    return [xd, yd, s[5],
      2 * td * yd + tdd * y + td * td * x - MU * (r0 + x) / rr + MU / (r0 * r0),
      -2 * td * xd - tdd * x + td * td * y - MU * y / rr,
      -MU * z / rr,
      r0d, r0 * td * td - MU / (r0 * r0), td, tdd];
  }
  jac(dyn, s) {
    var c = this.C(), m = c.MU;
    if (dyn === 'lin') { var n = c.N0; return [[0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1], [3 * n * n, 0, 0, 0, 2 * n, 0], [0, 0, 0, -2 * n, 0, 0], [0, 0, -n * n, 0, 0, 0]]; }
    var x = s[0], y = s[1], z = s[2], xd = s[3], yd = s[4], r0 = s[6], r0d = s[7], td = s[9];
    var q = (r0 + x) * (r0 + x) + y * y + z * z, r3 = Math.pow(q, 1.5), r5 = Math.pow(q, 2.5), F = [];
    for (var i = 0; i < 10; i++) F.push([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
    F[0][3] = 1; F[1][4] = 1; F[2][5] = 1; F[6][7] = 1; F[8][9] = 1;
    F[3][0] = td * td - m / r3 + 3 * m * (r0 + x) * (r0 + x) / r5;
    F[3][1] = 3 * m * y * (r0 + x) / r5 - 2 * r0d * td / r0;
    F[3][2] = 3 * m * z * (r0 + x) / r5;
    F[3][4] = 2 * td;
    F[3][6] = 3 * m * (r0 + x) * (r0 + x) / r5 - m / r3 - 2 * m / (r0 * r0 * r0) + 2 * r0d * td * y / (r0 * r0);
    F[3][7] = -2 * td * y / r0;
    F[3][9] = 2 * yd + 2 * td * x - 2 * r0d * y / r0;
    F[4][0] = 2 * r0d * td / r0 + 3 * m * y * (r0 + x) / r5;
    F[4][1] = td * td - m / r3 + 3 * m * y * y / r5;
    F[4][2] = 3 * m * y * z / r5;
    F[4][3] = -2 * td;
    F[4][6] = 3 * m * y * (r0 + x) / r5 - 2 * r0d * td * x / (r0 * r0);
    F[4][7] = 2 * td * x / r0;
    F[4][9] = 2 * td * y - 2 * xd + 2 * r0d * x / r0;
    F[5][0] = 3 * m * z * (r0 + x) / r5;
    F[5][1] = 3 * m * y * z / r5;
    F[5][2] = 3 * m * z * z / r5 - m / r3;
    F[5][6] = 3 * m * z * (r0 + x) / r5;
    F[7][6] = 2 * m / (r0 * r0 * r0) + td * td;
    F[7][9] = 2 * r0 * td;
    F[9][6] = 2 * r0d * td / (r0 * r0);
    F[9][7] = -2 * td / r0;
    F[9][9] = -2 * r0d / r0;
    return F;
  }
  rk4(dyn, s, h) {
    var self = this;
    function ad(a, b, k) { return a.map(function (v, i) { return v + k * b[i]; }); }
    var k1 = self.fdyn(dyn, s), k2 = self.fdyn(dyn, ad(s, k1, h / 2)), k3 = self.fdyn(dyn, ad(s, k2, h / 2)), k4 = self.fdyn(dyn, ad(s, k3, h));
    return s.map(function (v, i) { return v + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]); });
  }
  mm(A, B) {
    var n = A.length, m = B[0].length, k = B.length, R = new Array(n);
    for (var i = 0; i < n; i++) { var row = new Array(m), Ai = A[i]; for (var j = 0; j < m; j++) { var v = 0; for (var t = 0; t < k; t++) v += Ai[t] * B[t][j]; row[j] = v; } R[i] = row; }
    return R;
  }
  tr(A) { return A[0].map(function (_, j) { return A.map(function (r) { return r[j]; }); }); }
  phi(F, h) {
    var n = F.length, Fh = F.map(function (r) { return r.map(function (v) { return v * h; }); });
    var F2 = this.mm(Fh, Fh), F3 = this.mm(F2, Fh);
    return Fh.map(function (r, i) { return r.map(function (v, j) { return (i === j ? 1 : 0) + v + F2[i][j] / 2 + F3[i][j] / 6; }); });
  }

  /* the filter loop of main.m: update with the reading, then carry state and covariance forward 5 s */
  ekf(dyn, r, qs, seed) {
    var key = [dyn, r, qs, seed].join('|');
    if (!this._runs) this._runs = {};
    if (this._runs[key]) return this._runs[key];
    var S = this.setup(dyn), nx = S.nx, dt = 5, self = this;
    var sd = seed * 7919 + 17;
    function rnd() { sd = (sd * 16807) % 2147483647; return sd / 2147483647; }
    function gauss() { return Math.sqrt(-2 * Math.log(rnd())) * Math.cos(2 * Math.PI * rnd()); }
    var xt = S.X0.slice(), xb = S.X0.slice(), Pb = [];
    for (var a = 0; a < nx; a++) { Pb.push(new Array(nx).fill(0)); Pb[a][a] = S.P0[a] * S.P0[a]; }
    var Qd = S.Q.map(function (v) { return v * v * qs * dt; });
    var N = Math.floor(4 * 5752 / dt), R2 = r * r;
    var o = { t: [], tru: [], mea: [], est: [], sg: [], inn: [], bnd: [] };
    var sm = 0, se = 0, cnt = 0, inside = 0, K00 = 0;
    for (var k = 0; k < N; k++) {
      var y = [xt[0] + r * gauss(), xt[1] + r * gauss(), xt[2] + r * gauss()];
      var M = [[Pb[0][0] + R2, Pb[0][1], Pb[0][2]], [Pb[1][0], Pb[1][1] + R2, Pb[1][2]], [Pb[2][0], Pb[2][1], Pb[2][2] + R2]];
      var A1 = M[1][1] * M[2][2] - M[1][2] * M[2][1], B1 = -(M[1][0] * M[2][2] - M[1][2] * M[2][0]), C1 = M[1][0] * M[2][1] - M[1][1] * M[2][0];
      var det = M[0][0] * A1 + M[0][1] * B1 + M[0][2] * C1;
      var Si = [[A1 / det, -(M[0][1] * M[2][2] - M[0][2] * M[2][1]) / det, (M[0][1] * M[1][2] - M[0][2] * M[1][1]) / det],
        [B1 / det, (M[0][0] * M[2][2] - M[0][2] * M[2][0]) / det, -(M[0][0] * M[1][2] - M[0][2] * M[1][0]) / det],
        [C1 / det, -(M[0][0] * M[2][1] - M[0][1] * M[2][0]) / det, (M[0][0] * M[1][1] - M[0][1] * M[1][0]) / det]];
      var Kg = Pb.map(function (row) { return [0, 1, 2].map(function (j) { return row[0] * Si[0][j] + row[1] * Si[1][j] + row[2] * Si[2][j]; }); });
      var res = [y[0] - xb[0], y[1] - xb[1], y[2] - xb[2]];
      var xc = xb.map(function (v, i) { return v + Kg[i][0] * res[0] + Kg[i][1] * res[1] + Kg[i][2] * res[2]; });
      var IKH = Pb.map((row, i) => row.map((_, j) => (i === j ? 1 : 0) - (j < 3 ? Kg[i][j] : 0)));
      var Pc = this.mm(this.mm(IKH, Pb), this.tr(IKH));
      for (let i = 0; i < nx; i++) for (let j = 0; j < nx; j++)
        Pc[i][j] += R2 * (Kg[i][0]*Kg[j][0] + Kg[i][1]*Kg[j][1] + Kg[i][2]*Kg[j][2]);
      var t = k * dt;
      if (t >= 500) {
        for (var q = 0; q < 3; q++) {
          sm += Math.pow(y[q] - xt[q], 2); se += Math.pow(xc[q] - xt[q], 2);
          if (Math.abs(res[q]) <= 3 * Math.sqrt(M[q][q])) inside++;
        }
        cnt += 3;
      }
      o.t.push(t); o.tru.push(xt.slice(0, 3)); o.mea.push(y); o.est.push(xc.slice(0, 3));
      o.sg.push(Math.sqrt(Pc[0][0])); o.inn.push(res[0]); o.bnd.push(3 * Math.sqrt(M[0][0]));
      K00 = Kg[0][0];
      var Ph = this.phi(this.jac(dyn, xc), dt);
      var xn = xc;
      for (var st = 0; st < 5; st++) xn = this.rk4(dyn, xn, 1);
      xb = xn;
      Pb = this.mm(this.mm(Ph, Pc), this.tr(Ph));
      for (var d = 0; d < nx; d++) Pb[d][d] += Qd[d];
      for (var st2 = 0; st2 < 5; st2++) xt = this.rk4(dyn, xt, 1);
    }
    o.rm = Math.sqrt(sm / cnt); o.re = Math.sqrt(se / cnt); o.K = K00; o.sig = o.sg[o.sg.length - 1]; o.inside = inside / cnt;
    const keys = Object.keys(this._runs);
    if (keys.length >= 6) delete this._runs[keys[0]];
    this._runs[key] = o;
    return o;
  }

  /* one orbit of the true motion, for the drawings */
  orbit(dyn) {
    if (!this._orb) this._orb = {};
    if (this._orb[dyn]) return this._orb[dyn];
    var c = this.C(), S = this.setup(dyn), T = 2 * Math.PI / c.N0, s = S.X0.slice(), out = [s.slice()], n = 240, h = T / n;
    for (var i = 0; i < n; i++) { for (var k = 0; k < 6; k++) s = this.rk4(dyn, s, h / 6); out.push(s.slice()); }
    var mn = [1e12, 1e12, 1e12], mx = [-1e12, -1e12, -1e12], dmin = 1e12, dmax = 0;
    out.forEach(function (p) { for (var j = 0; j < 3; j++) { mn[j] = Math.min(mn[j], p[j]); mx[j] = Math.max(mx[j], p[j]); } var d = Math.sqrt(p[0] * p[0] + p[1] * p[1] + p[2] * p[2]); dmin = Math.min(dmin, d); dmax = Math.max(dmax, d); });
    this._orb[dyn] = { pts: out, mn: mn, mx: mx, dmin: dmin, dmax: dmax, T: T };
    return this._orb[dyn];
  }

  /* z loop of the control project: A = [0 1; -4 0], B = [0; 0.25], K = [446.8362 59.9766], ki = 1581.14 */
  servo(limit) {
    var key = limit ? 'lim' : 'free';
    if (!this._servo) this._servo = {};
    if (this._servo[key]) return this._servo[key];
    var z = 0, v = 0, xi = 0, dt = 1e-4, peak = 0, zmax = 0, T = [], Z = [], V = [], U = [], Uw = [];
    for (var i = 0; i <= 25000; i++) {
      var uw = -446.8362 * z - 59.9766 * v + 1581.1388 * xi, u = uw;
      if (limit) u = Math.max(-50, Math.min(50, u));
      if (Math.abs(uw) > peak) peak = Math.abs(uw);
      if (z > zmax) zmax = z;
      if (i % 50 === 0) { T.push(i * dt); Z.push(z); V.push(v); U.push(u); Uw.push(uw); }
      var acc = -4 * z + 0.25 * u;
      z += v * dt; v += acc * dt; xi += (1 - z) * dt;
    }
    this._servo[key] = { T: T, Z: Z, V: V, U: U, Uw: Uw, peak: limit ? 50 : peak, ask: peak, zmax: zmax, zend: z };
    return this._servo[key];
  }

  /* ================= charts on paper ================= */
  chart(series, o) {
    var W = 440, H = 200, x0 = 52, x1 = 428, y0 = 14, y1 = 170;
    var lo = o.lo, hi = o.hi;
    if (lo === undefined || hi === undefined) {
      var l2 = Infinity, h2 = -Infinity;
      series.forEach(function (s) { s.v.forEach(function (v, i) { if (s.x[i] < o.xa || s.x[i] > o.xb) return; if (v < l2) l2 = v; if (v > h2) h2 = v; }); });
      if (lo === undefined) lo = l2; if (hi === undefined) hi = h2;
    }
    var span = hi - lo || 1, raw = span / 4, mag = Math.pow(10, Math.floor(Math.log10(raw)));
    var step = [1, 2, 2.5, 5, 10].map(function (f) { return f * mag; }).filter(function (s) { return s >= raw; })[0];
    lo = Math.floor(lo / step + 1e-9) * step; hi = Math.ceil(hi / step - 1e-9) * step;
    function X(x) { return x0 + (x - o.xa) / (o.xb - o.xa) * (x1 - x0); }
    function Y(v) { return y1 - (Math.max(lo, Math.min(hi, v)) - lo) / (hi - lo) * (y1 - y0); }
    function pc(v, t) { return (v / t * 100).toFixed(2) + '%'; }
    function fmt(v) { if (Math.abs(v) < 1e-9) return '0'; if (Math.abs(v) >= 1000) return (v / 1000) + 'k'; return String(+v.toFixed(3)); }
    var grid = [], labels = [];
    for (var v = lo; v <= hi + 1e-9; v += step) { grid.push({ y: Y(v).toFixed(1) }); labels.push({ l: pc(x0 - 20, W), t2: pc(Y(v), H), t: fmt(v) }); }
    o.ticks.forEach(function (x) { labels.push({ l: pc(X(x), W), t2: pc(186, H), t: String(x) }); });
    var paths = series.map(function (s) {
      var d = '', ev = s.every || 1;
      for (var i = 0; i < s.v.length; i += ev) { if (s.x[i] < o.xa || s.x[i] > o.xb) continue; d += (d ? 'L' : 'M') + X(s.x[i]).toFixed(1) + ' ' + Y(s.v[i]).toFixed(1); }
      return { d: d, c: s.c, w: s.w || '2', dash: s.dash || 'none', op: s.op || '1' };
    });
    var bands = (o.lines || []).map(function (l) { return { y: Y(l.v).toFixed(1), c: l.c }; });
    var legend = series.filter(function (s) { return s.name; }).map(function (s) { return { c: s.c, t: s.name, st: s.dash && s.dash !== 'none' ? 'dashed' : 'solid' }; })
      .concat((o.lines || []).filter(function (l) { return l.name; }).map(function (l) { return { c: l.c, t: l.name, st: 'dashed' }; }));
    function up(t) { return String(t).replace(/Σ/g, 'σ'); }
    legend.forEach(function (l) { l.t = up(l.t); });
    return { grid: grid, labels: labels, paths: paths, bands: bands, title: up(o.title), unit: up(o.unit), legend: legend };
  }

  sci(v) {
    if (v === 0) return '0';
    var a = Math.abs(v);
    if (a >= 0.01 && a < 1e5) return String(+v.toPrecision(4));
    var e = Math.floor(Math.log10(a)), m = v / Math.pow(10, e), sup = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
    return m.toFixed(3) + ' × 10' + String(e).split('').map(function (ch) { return sup[ch]; }).join('');
  }

  renderVals() {
    var s = this.state || {}, self = this;
    function seg(list, cur, key, on) {
      return list.map(function (d) { var a = d.k === cur; return { label: d.label, pressed: a ? 'true' : 'false', bg: a ? (on || '#1F4A4F') : '#EADFC8', fg: a ? '#F4EEE2' : '#1E3A3D', key: key, value: String(d.k) }; });
    }
    function f(x, d) { return Number(x).toFixed(d); }
    var dyn = s.dyn || 'lin', lin = dyn === 'lin';
    var dynBtns = seg([{ k: 'lin', label: 'Linear · Clohessy–Wiltshire' }, { k: 'nl', label: 'Nonlinear · full motion' }], dyn, 'dyn', '#D9694E');

    /* ---------- 02 the two models ---------- */
    var O = this.orbit(dyn), S0 = this.setup(dyn);
    var model = lin ? {
      name: 'Clohessy–Wiltshire',
      text: 'The Clohessy–Wiltshire equations assume that the leader flies a circular orbit and that the follower stays close to it. That makes the motion linear, and six states are enough, the position and speed of the follower. In this case the follower starts 70 km above, 140 km ahead and 105 km to the side of a leader at 600 km of altitude.',
      eqs: ['ẍ = 2nẏ + 3n²x', 'ÿ = −2nẋ', 'z̈ = −n²z'],
      eqNote: 'n is the constant orbital rate of the leader.',
      states: ['x', 'y', 'z', 'ẋ', 'ẏ', 'ż'],
      orbitTxt: 'Circular'
    } : {
      name: 'Nonlinear relative motion',
      text: 'The nonlinear model keeps the full pull of Earth and lets the leader fly an elliptical orbit. The distance r₀ of the leader to Earth and its angle θ₀ along the orbit now change in time, so they join the state, which grows to ten. In this case the leader orbit has an eccentricity of 0.1, and the follower starts 79 km below and 698 km to the side of the leader, too far for the linear model.',
      eqs: ['ẍ = 2θ̇₀ẏ + θ̈₀y + θ̇₀²x − μ(r₀ + x) / r³ + μ / r₀²', 'ÿ = −2θ̇₀ẋ − θ̈₀x + θ̇₀²y − μy / r³', 'z̈ = −μz / r³', 'r̈₀ = r₀θ̇₀² − μ / r₀²', 'θ̈₀ = −2ṙ₀θ̇₀ / r₀'],
      eqNote: 'r = √((r₀ + x)² + y² + z²) is the distance from the follower to the centre of Earth.',
      states: ['x', 'y', 'z', 'ẋ', 'ẏ', 'ż', 'r₀', 'ṙ₀', 'θ₀', 'θ̇₀'],
      orbitTxt: 'Ellipse · e = 0.1'
    };
    var stateChips = model.states.map(function (t, i) { return { t: t, bg: i < 6 ? '#F4EEE2' : '#F2CBAE' }; });
    var modelFacts = [
      { k: 'States', v: String(S0.nx) },
      { k: 'Leader orbit', v: model.orbitTxt },
      { k: 'Closest approach', v: f(O.dmin / 1000, 0) + ' km' },
      { k: 'Farthest point', v: f(O.dmax / 1000, 0) + ' km' }
    ];
    var view = s.view || 'rel';
    var viewBtns = seg([{ k: 'rel', label: 'From the leader' }, { k: 'earth', label: 'From Earth' }], view, 'view', '#D9694E');
    var views = [{ k: 'iso', label: '3D' }, { k: 'top', label: 'Top' }, { k: 'front', label: 'Front' }, { k: 'side', label: 'Side' }].map(function (v) { return { label: v.label, key: 'preset', value: v.k }; });
    var viewNote = view === 'rel'
      ? (lin ? 'Seen from the leader, the follower loops once per orbit around a point about 125 km ahead of it.' : 'Seen from the leader, the follower swings far out of the orbit plane, and the loop does not close because the leader speeds up and slows down on its ellipse.')
      : (lin ? 'Seen from Earth the two orbits are almost the same circle. The gap between them is drawn 15 times larger here.' : 'Seen from Earth the leader flies an ellipse and the follower a tilted orbit beside it. The gap between them is drawn 3 times larger here.');

    /* ---------- 03 the Jacobian ---------- */
    var rowsL = ['ẋ', 'ẏ', 'ż', 'ẍ', 'ÿ', 'z̈', 'ṙ₀', 'r̈₀', 'θ̇₀', 'θ̈₀'], cols = model.states;
    var FX = lin ? {
      '3,0': '3n²', '3,4': '2n', '4,3': '−2n', '5,2': '−n²'
    } : {
      '3,0': 'θ̇₀² − μ / r³ + 3μ(r₀ + x)² / r⁵',
      '3,1': '3μy(r₀ + x) / r⁵ − 2ṙ₀θ̇₀ / r₀',
      '3,2': '3μz(r₀ + x) / r⁵',
      '3,4': '2θ̇₀',
      '3,6': '3μ(r₀ + x)² / r⁵ − μ / r³ − 2μ / r₀³ + 2ṙ₀θ̇₀y / r₀²',
      '3,7': '−2θ̇₀y / r₀',
      '3,9': '2ẏ + 2θ̇₀x − 2ṙ₀y / r₀',
      '4,0': '2ṙ₀θ̇₀ / r₀ + 3μy(r₀ + x) / r⁵',
      '4,1': 'θ̇₀² − μ / r³ + 3μy² / r⁵',
      '4,2': '3μyz / r⁵',
      '4,3': '−2θ̇₀',
      '4,6': '3μy(r₀ + x) / r⁵ − 2ṙ₀θ̇₀x / r₀²',
      '4,7': '2θ̇₀x / r₀',
      '4,9': '2θ̇₀y − 2ẋ + 2ṙ₀x / r₀',
      '5,0': '3μz(r₀ + x) / r⁵',
      '5,1': '3μyz / r⁵',
      '5,2': '3μz² / r⁵ − μ / r³',
      '5,6': '3μz(r₀ + x) / r⁵',
      '7,6': 'θ̇₀² + 2μ / r₀³',
      '7,9': '2r₀θ̇₀',
      '9,6': '2ṙ₀θ̇₀ / r₀²',
      '9,7': '−2θ̇₀ / r₀',
      '9,9': '−2ṙ₀ / r₀'
    };
    var F0 = this.jac(dyn, S0.X0), nx = S0.nx;
    var sel = s.cell && s.cell.dyn === dyn ? s.cell.k : '3,0';
    var nOnes = 0, nD = 0;
    var mRows = [];
    for (var i = 0; i < nx; i++) {
      var cells = [];
      for (var j = 0; j < nx; j++) {
        var k2 = i + ',' + j, isD = !!FX[k2], one = !isD && F0[i][j] === 1, on = sel === k2;
        if (isD) nD++; if (one) nOnes++;
        (function (k3, isD2, one2, on2, ii, jj) {
          cells.push({
            t: isD2 ? '∂' : (one2 ? '1' : ''),
            bg: on2 ? '#D9694E' : (isD2 ? '#1F4A4F' : (one2 ? '#EADFC8' : '#FBF8F1')),
            fg: on2 || isD2 ? '#F4EEE2' : '#1E3A3D',
            bd: on2 ? '#B04A32' : '#E3D8C3',
            pressed: on2 ? 'true' : 'false',
            aria: '∂' + rowsL[ii] + ' / ∂' + cols[jj],
            key: 'cell', value: k3, tab: on2 ? '0' : '-1'
          });
        })(k2, isD, one, on, i, j);
      }
      mRows.push({ h: rowsL[i], cells: cells });
    }
    var si = +sel.split(',')[0], sj = +sel.split(',')[1];
    var cellFx = FX[sel] || (F0[si][sj] === 1 ? '1' : '0');
    var cellInfo = {
      title: '∂' + rowsL[si] + ' / ∂' + cols[sj],
      fx: cellFx,
      val: this.sci(F0[si][sj]),
      note: FX[sel] ? (lin ? 'A constant, the same at every step.' : 'Depends on where the satellites are, so the filter evaluates it again every 5 s.') : (F0[si][sj] === 1 ? 'A rate is the derivative of its state, so this term is simply 1.' : 'This equation does not depend on this state.')
    };
    var matStats = '{{text.mat_stats}}', matTerms = nx * nx, matNonzero = nD + nOnes, matDerived = nD;
    var colHeads = cols.map(function (c) { return { t: c }; });

    /* ---------- 04 Kalman steps ---------- */
    var kstep = s.kstep || 1;
    var stepDefs = [
      { k: 1, label: '1 Predict', text: 'The filter carries its last estimate forward 5 s with the model of the motion. On the way its uncertainty grows, because no model is perfect.' },
      { k: 2, label: '2 Measure', text: 'A new GPS reading arrives. It is noisy, so it comes with its own cloud of uncertainty.' },
      { k: 3, label: '3 Compare', text: 'The gap between the reading and the prediction is called the innovation. In a healthy filter this gap stays inside three standard deviations almost all the time.' },
      { k: 4, label: '4 Correct', text: 'The new estimate lands between the two, closer to whichever is more certain. The Kalman gain sets that balance, and the uncertainty shrinks. Then the loop starts again.' }
    ];
    var kBtns = seg(stepDefs, kstep, 'kstep');
    var kText = stepDefs[kstep - 1].text;
    var kOp = { a: '1', b: kstep >= 2 ? '1' : '0', c: kstep >= 3 ? '1' : '0', d: kstep >= 4 ? '1' : '0', b2: kstep >= 2 ? '0' : '1' };

    /* ---------- 05 the lab ---------- */
    var nk = s.noise || 'n14', tk = s.trust || 'mine', seed = s.seed || 1;
    var rMap = { n5: 5, n14: 10 * Math.SQRT2, k1: 2000, k5: 20000 }, qMap = { more: 0.01, mine: 1, less: 25 };
    var r = rMap[nk], unreal = nk === 'k1' || nk === 'k5';
    var E = this.ekf(dyn, r, qMap[tk], seed);
    var noiseBtns = seg([{ k: 'n5', label: '5 m' }, { k: 'n14', label: '14 m · my setup' }, { k: 'k1', label: '2 km · unreal' }, { k: 'k5', label: '20 km · unreal' }], nk, 'noise');
    var trustBtns = seg([{ k: 'more', label: 'More' }, { k: 'mine', label: 'My setting' }, { k: 'less', label: 'Less' }], tk, 'trust');
    /* orbit before and after, first orbit only */
    var ax = lin ? [1, 0] : [2, 1], axN = ['x · away from Earth', 'y · along the orbit', 'z · out of the plane'];
    var nOrb = Math.floor(5752 / 5), lo = [1e12, 1e12], hi = [-1e12, -1e12];
    for (var q = 0; q < nOrb; q++) { for (var a2 = 0; a2 < 2; a2++) { var v2 = E.tru[q][ax[a2]]; lo[a2] = Math.min(lo[a2], v2); hi[a2] = Math.max(hi[a2], v2); } }
    var PW = 520, PH = 360, pad = 34, spanX = hi[0] - lo[0], spanY = hi[1] - lo[1];
    var scl = Math.min((PW - 2 * pad) / spanX, (PH - 2 * pad) / spanY);
    var ox = PW / 2 - (lo[0] + hi[0]) / 2 * scl, oy = PH / 2 + (lo[1] + hi[1]) / 2 * scl;
    function PX(p) { return (ox + p[ax[0]] * scl).toFixed(1) + ' ' + (oy - p[ax[1]] * scl).toFixed(1); }
    var dTru = '', dEst = '', dMea = '';
    for (var q2 = 0; q2 < nOrb; q2 += 2) { dTru += (q2 ? 'L' : 'M') + PX(E.tru[q2]); dEst += (q2 ? 'L' : 'M') + PX(E.est[q2]); }
    for (var q3 = 0; q3 < nOrb; q3 += 3) dMea += 'M' + PX(E.mea[q3]) + 'h0.01';
    var kmStep = spanX / 1000 > 400 ? 200 : (spanX / 1000 > 150 ? 50 : 25), barPx = kmStep * 1000 * scl;
    var plot = {
      tru: dTru, est: dEst, mea: dMea, hx: axN[ax[0]], vy: axN[ax[1]], bar: f(24 + barPx, 1), barT: kmStep + ' km',
      note: unreal ? '{{text.plot_unreal}}' : '{{text.plot_real}}'
    };
    var hrs = E.t.map(function (t) { return t / 3600; }), mins = E.t.map(function (t) { return t / 60; });
    var errM = E.mea.map(function (p, i) { return p[0] - E.tru[i][0]; }), errE = E.est.map(function (p, i) { return p[0] - E.tru[i][0]; });
    var lim = Math.ceil(r * 3.4 / Math.pow(10, Math.floor(Math.log10(r * 3.4)))) * Math.pow(10, Math.floor(Math.log10(r * 3.4)));
    var nb = E.bnd.map(function (v) { return -v; });
    var labCharts = [
      this.chart([
        { x: hrs, v: errM, c: '#E58C70', w: '1', op: '0.7', name: 'GPS reading', every: 3 },
        { x: hrs, v: errE, c: '#1F4A4F', w: '1.6', name: 'Filter estimate', every: 3 }
      ], { xa: 0, xb: 6.4, ticks: [0, 1, 2, 3, 4, 5, 6], lo: -lim, hi: lim, title: 'Error in x against the true position', unit: 'm · hours' }),
      this.chart([
        { x: mins, v: E.sg, c: '#D9694E', w: '2.4', name: 'Filter uncertainty σx' }
      ], unreal ? { xa: 0, xb: 60, ticks: [0, 10, 20, 30, 40, 50, 60], lo: 0, title: 'How sure the filter is, first hour', unit: 'm · minutes' } : { xa: 0, xb: 10, ticks: [0, 2, 4, 6, 8, 10], lo: 0, title: 'How sure the filter is, first 10 minutes', unit: 'm · minutes' }),
      this.chart([
        { x: hrs, v: E.inn, c: '#4E7F7B', w: '1', op: '0.85', name: 'Innovation in x', every: 3 },
        { x: hrs, v: E.bnd, c: '#B04A32', w: '1.4', dash: '5 4', name: '±3σ', every: 3 },
        { x: hrs, v: nb, c: '#B04A32', w: '1.4', dash: '5 4', every: 3 }
      ], { xa: 0, xb: 6.4, ticks: [0, 1, 2, 3, 4, 5, 6], lo: -lim * 1.2, hi: lim * 1.2, title: 'Innovation and its ±3σ limits', unit: 'm · hours' })
    ];
    function m(v) { return v >= 1000 ? f(v / 1000, 2) + ' km' : f(v, v < 10 ? 2 : 1) + ' m'; }
    var labVals = [
      { k: 'GPS error', v: m(E.rm) },
      { k: 'Filter error', v: m(E.re) },
      { k: 'Uncertainty settles at', v: m(E.sig) },
      { k: 'Kalman gain', v: f(E.K, 3) },
      { k: 'Innovation inside ±3σ', v: f(E.inside * 100, 1) + '%' }
    ];
    var labText = '{{text.lab_summary}}', improvement = f(100 - 100 * E.re / E.rm, 0), gain = f(E.K, 3);

    /* ---------- 07 control ---------- */
    var thr = s.thr || 'free', Sv = this.servo(thr === 'lim');
    var ctrlCharts = [
      this.chart([
        { x: Sv.T, v: Sv.Z, c: '#1F4A4F', w: '2.4', name: 'z (m)' },
        { x: Sv.T, v: Sv.V, c: '#D9694E', w: '2.4', name: 'vz (m/s)' }
      ], { xa: 0, xb: 2.5, ticks: [0, 0.5, 1, 1.5, 2, 2.5], lo: -0.5, hi: 3, title: 'Position and speed in z', unit: 'seconds', lines: [{ v: 1, c: '#9AA5B1', name: 'Reference 1 m' }] }),
      this.chart([
        { x: Sv.T, v: Sv.U, c: '#1F4A4F', w: '2.4', name: 'Thrust given' }
      ].concat(thr === 'lim' ? [{ x: Sv.T, v: Sv.Uw, c: '#1F4A4F', w: '1.2', dash: '3 4', op: '0.6', name: 'Thrust asked' }] : []),
      { xa: 0, xb: 2.5, ticks: [0, 0.5, 1, 1.5, 2, 2.5], lo: -60, hi: 100, title: 'Thrust in z', unit: 'N · seconds', lines: [{ v: 50, c: '#C2383D', name: 'Limit ±50 N' }, { v: -50, c: '#C2383D' }] })
    ];
    var thrBtns = seg([{ k: 'free', label: 'Ideal thrusters' }, { k: 'lim', label: '50 N limit' }], thr, 'thr', '#D9694E');
    var ctrlVals = [
      { k: 'Thrust asked', v: f(Sv.ask, 1) + ' N', c: Sv.ask > 50 ? '#B04A32' : '#1E3A3D' },
      { k: 'Thrust given', v: f(Sv.peak, 1) + ' N', c: '#1E3A3D' },
      { k: 'Highest position', v: f(Sv.zmax, 3) + ' m', c: '#1E3A3D' },
      { k: 'Position at 2.5 s', v: f(Sv.zend, 3) + ' m', c: '#1E3A3D' }
    ];
    var ctrlText = thr === 'lim' ? '{{text.control_limited}}' : '{{text.control_ideal}}';
    return {
      matTerms, matNonzero, matDerived, improvement, gain, noiseKm: String(r / 1000), asked: f(Sv.ask, 1), dyn, nx,
      dynBtns: dynBtns, dynName: lin ? 'Linear model' : 'Nonlinear model',
      model: model, stateChips: stateChips, modelFacts: modelFacts,
      views: views, viewBtns: viewBtns, viewNote: viewNote,
      mRows: mRows, colHeads: colHeads, cellInfo: cellInfo, matStats: matStats, gridCols: 'repeat(' + (nx + 1) + ', minmax(0, 1fr))',
      kBtns: kBtns, kText: kText, kOp: kOp, 
      noiseBtns: noiseBtns, trustBtns: trustBtns, plot: plot, labCharts: labCharts, labVals: labVals, labText: labText,
      thrBtns: thrBtns, ctrlCharts: ctrlCharts, ctrlVals: ctrlVals, ctrlText: ctrlText,
    };
  }
}
