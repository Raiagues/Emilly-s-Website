import {test, before, after} from 'node:test';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {existsSync} from 'node:fs';
import {readFile} from 'node:fs/promises';
if (!process.env.PLAYWRIGHT_BROWSERS_PATH && existsSync('.runtime/browsers')) {
  process.env.PLAYWRIGHT_BROWSERS_PATH = new URL('../.runtime/browsers', import.meta.url).pathname;
}
const {chromium, expect} = await import('@playwright/test');
const {default:AxeBuilder} = await import('@axe-core/playwright');
let browser,server,base;
before(async () => {
  server=spawn('python3',['tests/server.py'],{stdio:['ignore','pipe','pipe']});
  base=await new Promise((resolve,reject)=>{
    const timeout=setTimeout(()=>reject(new Error('Server timeout')),10000);
    server.once('error',error=>{clearTimeout(timeout);reject(error);});
    server.stdout.once('data',chunk=>{clearTimeout(timeout);resolve(String(chunk).trim());});
  });
  browser=await chromium.launch({headless:true,...(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{})});
});
after(async()=>{await browser?.close();if(server?.exitCode===null){const exited=once(server,'exit');server.kill();await exited;}});
const path='pages/projects/damas-espaciais.html';
const cell=(page,n)=>page.locator(`[data-cell="${n}"]`);
async function open(prefix='',options={}) {
  const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce',...options});
  const page=await context.newPage(),errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  assert.equal((await page.goto(base+prefix+path)).status(),200);
  return {page,context,errors};
}

test('Damas preserves the supplied design, professor credentials and responsive navigation in all four languages',async()=>{
  for(const lang of ['','pt/','fr/','es/']) {
    const {page,context,errors}=await open(lang);
    await expect(page.locator('#damas-board')).toHaveAttribute('data-ready','true');
    await expect(page.locator('.damas-pass h1')).toHaveText('Damas Espaciais');
    await expect(page.locator('#credits')).toContainText('Marcelo Serrano Zanetti');
    await expect(page.locator('#credits')).toContainText('ETH Zürich');
    await expect(page.locator('#credits a')).toHaveAttribute('href','https://ufsmpublica.ufsm.br/docente/17861');
    await expect(page.locator('#main-nav [aria-current]')).toContainText(/Projetos|Projects|Projets|Proyectos/);
    await expect(page.locator('.damas-report a[href$=".dc.html"],.damas-report sc-for')).toHaveCount(0);
    await expect(page.locator('[data-cell]')).toHaveCount(64);
    await expect(page.locator('[data-cell] img')).toHaveCount(24);
    for(const width of [320,390,768,1024,1440]) {
      await page.setViewportSize({width,height:900});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang} at ${width}`);
    }
    for(const version of ['2021','2026']) {
      await page.locator(`[data-version="${version}"]`).click();
      await expect(page.locator(`[data-version-panel="${version}"]`)).toBeVisible();
      const audit=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
      assert.deepEqual(audit.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})),[]);
    }
    await page.locator('[data-screen=RULES]').click();
    await expect(page.locator('[data-screen-image]')).toHaveAttribute('src',/rules.jpg$/);
    await page.locator('[data-screen=VICTORY]').click();
    await expect(page.locator('[data-screen-image]')).toHaveAttribute('src',/victory.jpg$/);
    await page.locator('[data-back-results]').click();
    await expect(page.locator('#damas-espaciais .project-card')).toBeVisible();
    await expect(page.locator('[data-project]')).toHaveCount(22);
    assert.deepEqual(errors,[]);
    await context.close();
  }
});

test('the shared C engine rejects invalid moves, captures rivals, passes turns and resets from the keyboard',async()=>{
  const {page,context,errors}=await open('pt/');
  const board=page.locator('#damas-board');
  await expect(board).toHaveAttribute('data-ready','true');
  await cell(page,17).click(); // B3
  await expect(cell(page,26)).toHaveClass(/legal/);
  const before=await page.locator('[data-cell]').evaluateAll(cells=>cells.map(c=>c.dataset.piece));
  await cell(page,18).click(); // C3: not a diagonal
  assert.deepEqual(await page.locator('[data-cell]').evaluateAll(cells=>cells.map(c=>c.dataset.piece)),before);
  await expect(board).toHaveAttribute('data-turn','1');
  await expect(page.locator('[data-check=diagonal]')).toHaveAttribute('data-state','fail');
  await expect(page.locator('[data-inspector-result]')).toContainText('false');
  await cell(page,26).click(); // C4
  await expect(cell(page,26)).toHaveAttribute('data-piece','1');
  await expect(board).toHaveAttribute('data-turn','2');
  await cell(page,44).click(); await cell(page,37).click(); // E6 -> F5: free the landing square
  await cell(page,19).click(); await cell(page,28).click(); // D3 -> E4
  await cell(page,42).click(); await cell(page,35).click(); // C6 -> D5
  await cell(page,26).click(); await cell(page,35).click(); // click rival, land on E6
  await expect(cell(page,35)).toHaveAttribute('data-piece','0');
  await expect(cell(page,44)).toHaveAttribute('data-piece','1');
  await expect(page.locator('[data-cell] img')).toHaveCount(23);
  await expect(page.locator('[data-check=jump]')).toHaveAttribute('data-state','pass');
  await cell(page,40).click(); await cell(page,40).click(); // pass pink's turn
  await expect(board).toHaveAttribute('data-turn','1');
  await expect(page.locator('[data-inspector-result]')).toContainText('Vez passada');
  await page.locator('[data-game-action=matrix]').click();
  await expect(page.locator('.cell-number:visible')).toHaveCount(64);
  await page.locator('[data-game-action=reset]').click();
  await expect(page.locator('[data-cell] img')).toHaveCount(24);
  await expect(cell(page,17)).toBeFocused();
  await page.keyboard.press('Enter');
  await page.keyboard.press('ArrowDown');await page.keyboard.press('ArrowRight');await page.keyboard.press('Space');
  await expect(cell(page,26)).toHaveAttribute('data-piece','1');
  await expect(board).toHaveAttribute('data-turn','2');
  await page.locator('[data-game-action=reset]').click();
  await cell(page,17).click();await page.locator('[data-game-action=legal]').click();
  await expect(page.locator('.cell.legal')).toHaveCount(0);
  await page.locator('[data-game-action=drop]').click();
  await expect(page.locator('.cell[aria-selected=true]')).toHaveCount(0);
  assert.deepEqual(errors,[]);await context.close();
});

test('the board, screen gallery and code comparison support touch with a fixed header',async()=>{
  const {page,context,errors}=await open('pt/',{viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  await expect(page.locator('#damas-board')).toHaveAttribute('data-ready','true');
  await cell(page,17).tap();await cell(page,26).tap();
  await expect(cell(page,26)).toHaveAttribute('data-piece','1');
  await page.locator('[data-screen=COUNTDOWN]').tap();
  await expect(page.locator('[data-screen-image]')).toHaveAttribute('src',/countdown.jpg$/);
  await page.locator('[data-version="2026"]').tap();
  await expect(page.locator('[data-version-panel="2026"]')).toContainText('WebAssembly');
  await expect(page.locator('.home-header')).toBeVisible();
  assert.ok(Math.abs((await page.locator('.home-header').boundingBox()).y)<1,'header remains at the top after scrolling');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
  assert.deepEqual(errors,[]);await context.close();
});

test('the page remains useful without JavaScript or when the game module fails to load',async()=>{
  const {page,context}=await open('pt/',{javaScriptEnabled:false,viewport:{width:320,height:844}});
  await expect(page.locator('.damas-fallback')).toBeVisible();
  await expect(page.locator('[data-version-panel="2021"]')).toBeVisible();
  await expect(page.locator('[data-version-panel="2026"]')).toBeVisible();
  await expect(page.locator('.damas-controls')).toBeHidden();
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
  await context.close();
  const c=await browser.newContext({viewport:{width:390,height:844}}),p=await c.newPage();
  await p.route('**/game.wasm*',route=>route.fulfill({status:503,body:'Unavailable'}));
  await p.goto(base+'pt/'+path);
  await expect(p.locator('#damas-status')).toContainText('Não foi possível');
  await expect(p.locator('.damas-fallback a')).toHaveAttribute('href','https://raiagues.github.io/Jogo-Damas-Espaciais/');
  await p.locator('[data-screen=RULES]').click();
  await expect(p.locator('[data-screen-image]')).toHaveAttribute('src',/rules.jpg$/);
  await c.close();
});

test('a full match promotes rockets, announces victory and starts a fresh game',async()=>{
  const {page,context,errors}=await open();
  await expect(page.locator('#damas-board')).toHaveAttribute('data-ready','true');
  const fixture=JSON.parse(await readFile('tests/fixtures/damas-match.json','utf8'));
  let sawKing=false;
  for(const [from,to] of fixture.moves) {
    await cell(page,from).click();await cell(page,to).click();
    sawKing ||= Number(await cell(page,to).getAttribute('data-piece'))>2;
  }
  assert.ok(sawKing,'the match must exercise promotion');
  await expect(page.locator('#damas-board')).toHaveAttribute('data-winner',String(fixture.winner));
  await expect(page.locator('.damas-winner')).toBeVisible();
  await expect(page.locator('.damas-winner')).toContainText('Pink wins!');
  await expect(page.locator('.damas-winner button')).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.locator('.damas-winner')).toBeHidden();
  await expect(page.locator('[data-cell] img')).toHaveCount(24);
  await expect(page.locator('#damas-board')).toHaveAttribute('data-turn','1');
  assert.deepEqual(errors,[]);await context.close();
});

test('retired CVs and raw design references are absent from the public artifact',async()=>{
  for(const name of ['CV_Emilly.pdf','Emilly_Rodrigues_Resume.pdf','doc/CV_RODRIGUES_Emilly.pdf','local-reference']) {
    assert.equal(existsSync('dist/'+name),false,name);
  }
  const context=await browser.newContext(),page=await context.newPage();
  for(const lang of ['','pt/','fr/','es/']) for(const name of ['index.html','about.html','contact.html']) {
    await page.goto(base+lang+name);
    await expect(page.locator('a[download],a[href*="CV_"],a[href*="Resume"]')).toHaveCount(0);
  }
  await context.close();
});
