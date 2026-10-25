/* Portfolio interaction layer. Moves are authoritative in the vendored C/Wasm engine. */
(() => {
  'use strict';
  const root = document.querySelector('.damas-page');
  if (!root) return;
  const config = JSON.parse(document.getElementById('damas-data').textContent);
  const t = config.text;
  const $ = selector => root.querySelector(selector);
  const $$ = selector => [...root.querySelectorAll(selector)];
  const format = (text, values) => text.replace(/\{(\w+)\}/g, (_, key) => values[key] ?? '');
  const owner = p => p === 1 || p === 3 ? 1 : p === 2 || p === 4 ? 2 : 0;
  const inside = (r, c) => r >= 0 && r < 8 && c >= 0 && c < 8;
  const square = ([r, c]) => `${String.fromCharCode(65 + c)}${r + 1}`;
  const player = p => p === 1 ? t.blueName : t.pinkName;
  const names = [t.empty, t.blue, t.pink, t.blueKing, t.pinkKing];

  // The screen gallery and code comparison work even if Wasm cannot load.
  const screens = $$('[data-screen]');
  for (const button of screens) {
    button.disabled = false;
    button.addEventListener('click', () => {
      const key = button.dataset.screen;
      const screen = config.screens[key];
      screens.forEach(el => el.setAttribute('aria-pressed', String(el === button)));
      $('[data-screen-tag]').textContent = key;
      $('[data-screen-text]').textContent = screen.text;
      $('[data-screen-image]').src = screen.image;
      $('[data-screen-image]').alt = screen.alt;
      $('[data-screen-caption]').textContent = `${t.artwork} · ${key}`;
    });
  }
  const versionButtons = $$('[data-version]');
  function version(year) {
    versionButtons.forEach(el => el.setAttribute('aria-pressed', String(el.dataset.version === year)));
    $$('[data-version-panel]').forEach(el => { el.hidden = el.dataset.versionPanel !== year; });
  }
  version('2021');
  versionButtons.forEach(button => button.addEventListener('click', () => version(button.dataset.version)));
  root.classList.add('damas-enhanced');

  const cells = $$('[data-cell]');
  const status = $('#damas-status');
  const controls = $('.damas-controls');
  const grid = $('#damas-board');
  let engine, selected = null, showMatrix = false, showLegal = true;
  const checks = $$('[data-check]');
  const win = document.createElement('div');
  win.className = 'damas-winner';
  win.hidden = true;
  const winTitle = document.createElement('strong');
  const winReason = document.createElement('p');
  winReason.textContent = t.winReason;
  const again = document.createElement('button');
  again.type = 'button'; again.className = 'tog'; again.textContent = t.again;
  win.append(winTitle, winReason, again);
  // Keep the overlay outside the ARIA grid's row/cell hierarchy.
  const boardWrap = document.createElement('div'); boardWrap.className = 'damas-board-wrap';
  grid.before(boardWrap); boardWrap.append(grid, win);

  function inspect(title, result, states = {}) {
    $('[data-inspector-title]').textContent = title;
    $('[data-inspector-result]').textContent = result;
    for (const el of checks) {
      const state = states[el.dataset.check] || (Object.keys(states).length ? 'skip' : 'idle');
      el.dataset.state = state;
      el.querySelector('.check-icon').textContent = {pass:'✓', fail:'×', skip:'·', idle:'·'}[state];
      el.querySelector('.check-status').textContent = ` (${t[{pass:'checkPass',fail:'checkFail',skip:'checkSkip',idle:'checkIdle'}[state]]})`;
    }
  }

  // This trace only explains the C checks; it never commits or authorizes a move.
  function trace([r,c], [tr,tc]) {
    const states = {};
    function check(key, ok) { states[key] = ok ? 'pass' : 'fail'; return ok; }
    if (!check('inside', inside(r,c) && inside(tr,tc))) return states;
    const p = engine.web_piece(r,c), turn = engine.web_turn();
    if (!check('owner', owner(p) === turn)) return states;
    if (Math.abs(tr-r) === 1 && Math.abs(tc-c) === 1 && owner(engine.web_piece(tr,tc)) === 3-turn) {
      tr += tr-r; tc += tc-c;
    }
    states.landing = 'pass';
    if (!check('empty', inside(tr,tc) && engine.web_piece(tr,tc) === 0)) return states;
    const dr = tr-r, dc = tc-c;
    if (!check('diagonal', Math.abs(dr) === Math.abs(dc) && Math.abs(dr) >= 1 && Math.abs(dr) <= 2)) return states;
    if (!check('direction', !(p === 1 && dr < 0) && !(p === 2 && dr > 0))) return states;
    check('jump', Math.abs(dr) !== 2 || owner(engine.web_piece(r+dr/2,c+dc/2)) === 3-turn);
    return states;
  }

  function render() {
    const turn = engine.web_turn(), winner = engine.web_winner();
    status.textContent = winner ? format(t.winner,{player:player(winner)}) : `${format(t.turn,{player:player(turn)})} · ${t.blueName} ${engine.web_count(1)} / ${t.pinkName} ${engine.web_count(2)}`;
    grid.dataset.turn = turn;
    grid.dataset.winner = winner;
    win.hidden = !winner;
    winTitle.textContent = winner ? format(t.winner,{player:player(winner)}) : '';
    $('[data-game-action=drop]').disabled = !selected || Boolean(winner);
    cells.forEach((cell, i) => {
      const r = Math.floor(i/8), c = i%8, piece = engine.web_piece(r,c);
      const isSelected = selected?.[0] === r && selected?.[1] === c;
      const legal = Boolean(!winner && selected && !isSelected && engine.web_can_move(...selected,r,c));
      cell.disabled = false;
      cell.classList.toggle('selected', isSelected);
      cell.classList.toggle('legal', legal && showLegal);
      cell.setAttribute('aria-selected', String(isSelected));
      cell.setAttribute('aria-disabled', String(Boolean(winner)));
      cell.setAttribute('aria-label', `${square([r,c])}, ${names[piece]}${isSelected ? ', '+t.selected : ''}${legal ? ', '+t.legal : ''}`);
      if (cell.dataset.piece !== String(piece)) {
        cell.querySelector('img')?.remove();
        if (piece) {
          const image = document.createElement('img');
          image.src = config.pieces[piece]; image.alt = ''; image.width = 80; image.height = 80; image.draggable = false;
          cell.prepend(image);
        }
        cell.dataset.piece = piece;
      }
      const number = cell.querySelector('.cell-number');
      number.hidden = !showMatrix; number.textContent = piece;
    });
  }

  function reset(focus = false) {
    engine.web_reset(); selected = null;
    inspect(t.initial,t.start); render();
    cells.forEach((cell,i) => { cell.tabIndex = i === 17 ? 0 : -1; });
    if (focus) cells[17].focus({preventScroll:true});
  }

  function pick(row,col) {
    if (!engine || engine.web_winner()) return;
    if (!selected) {
      if (owner(engine.web_piece(row,col)) !== engine.web_turn()) {
        inspect(t.selectOwn, t.start, {inside:'pass',owner:'fail'});
        return;
      }
      selected = [row,col];
      inspect(format(t.selection,{square:square(selected)}),t.start);
    } else {
      const from = selected, to = [row,col];
      const pass = from[0] === row && from[1] === col;
      const states = pass ? {} : trace(from,to);
      const accepted = Boolean(engine.web_move(...from,row,col));
      if (accepted) selected = null;
      inspect(format(t.move,{from:square(from),to:square(to)}),accepted ? (pass ? t.passed : t.accepted) : t.rejected,states);
    }
    render();
    if (engine.web_winner()) again.focus({preventScroll:true});
  }

  cells.forEach((cell,i) => {
    cell.addEventListener('click', () => pick(Math.floor(i/8),i%8));
    cell.addEventListener('focus', () => cells.forEach(other => { other.tabIndex = other === cell ? 0 : -1; }));
    cell.addEventListener('keydown', event => {
      const row = Math.floor(i/8), col = i%8;
      const next = {ArrowUp:Math.max(0,row-1)*8+col,ArrowDown:Math.min(7,row+1)*8+col,ArrowLeft:row*8+Math.max(0,col-1),ArrowRight:row*8+Math.min(7,col+1),Home:row*8,End:row*8+7}[event.key];
      if (next !== undefined) { event.preventDefault(); cells[next].focus({preventScroll:true}); }
      if (event.key === 'Escape') { selected = null; inspect(t.cleared,t.start); render(); }
    });
  });
  controls.addEventListener('click', event => {
    const button = event.target.closest('[data-game-action]');
    if (!button || !engine) return;
    const action = button.dataset.gameAction;
    if (action === 'reset') { reset(true); return; }
    if (action === 'drop') { selected = null; inspect(t.cleared,t.start); }
    if (action === 'matrix') { showMatrix = !showMatrix; button.setAttribute('aria-pressed', String(showMatrix)); }
    if (action === 'legal') { showLegal = !showLegal; button.setAttribute('aria-pressed', String(showLegal)); }
    render();
  });
  again.addEventListener('click', () => reset(true));

  async function start() {
    status.textContent = t.loading;
    try {
      const response = await fetch(config.engine);
      if (!response.ok) throw new Error('Engine unavailable');
      const {instance} = await WebAssembly.instantiate(await response.arrayBuffer(), {});
      engine = instance.exports;
      reset();
      controls.hidden = false;
      $('.damas-fallback').hidden = true;
      grid.dataset.ready = 'true';
    } catch {
      status.textContent = t.error;
      $('.damas-fallback').hidden = false;
      inspect(t.error,t.initial);
    }
  }
  start();
})();
