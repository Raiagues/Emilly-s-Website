import {test,before,after} from 'node:test';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {existsSync} from 'node:fs';
if (!process.env.PLAYWRIGHT_BROWSERS_PATH && existsSync('.runtime/browsers')) process.env.PLAYWRIGHT_BROWSERS_PATH=new URL('../.runtime/browsers',import.meta.url).pathname;
const {chromium,expect}=await import('@playwright/test');
const {default:AxeBuilder}=await import('@axe-core/playwright');
let browser,server,base;
before(async()=>{
  server=spawn('python3',['tests/server.py'],{stdio:['ignore','pipe','pipe']});
  base=await new Promise((resolve,reject)=>{
    const timeout=setTimeout(()=>reject(new Error('Server timeout')),10000);
    server.once('error',reject);
    server.stdout.once('data',v=>{clearTimeout(timeout);resolve(String(v).trim());});
  });
  browser=await chromium.launch({headless:true,...(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{})});
});
after(async()=>{await browser?.close();if(server?.exitCode===null){const stopped=once(server,'exit');server.kill();await stopped;}});
const path='pages/experience/experience_2.html';
async function open(lang='',options={},blockWorker=false) {
  const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce',...options});
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  if(blockWorker)await page.route('**/src/formation-worker.js',r=>r.abort());
  assert.equal((await page.goto(base+lang+path)).status(),200);
  if(options.javaScriptEnabled!==false)await expect(page.locator('[data-formation]')).toHaveAttribute('data-ready','true');
  return {page,context,errors};
}
async function choose(page,key,value,section='') {
  await page.locator(`${section} [data-control="${key}"][data-value="${value}"]`).first().click();
  await expect(page.locator('[data-formation]')).toHaveAttribute('aria-busy','false');
  await expect(page.locator(`${section} [data-control="${key}"][data-value="${value}"]`).first()).toHaveAttribute('aria-pressed','true');
}

test('ITA design has eight chapters, real sources and accessible responsive layouts in four languages',async()=>{
  for(const lang of ['','pt/','fr/','es/']) {
    const {page,context,errors}=await open(lang);
    await expect(page.locator('.formation-pass')).toHaveCount(1);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('#main-nav [aria-current]')).toHaveAttribute('href','../../experience.html');
    await expect(page.locator('main sc-for,main a[href$=".dc.html"]')).toHaveCount(0);
    for(const id of ['why','models','matrix','filter','lab','results','control','next'])await expect(page.locator('#'+id)).toHaveCount(1);
    await expect(page.locator('a[href="https://github.com/Raiagues/flight-formation"]')).toHaveCount(1);
    await expect(page.locator('a[href="https://github.com/Raiagues/flight-formation/blob/main/research/relatorio.pdf"]')).toHaveCount(1);
    await expect(page.locator('#results')).toContainText('14.082 m');
    await expect(page.locator('#results')).toContainText('4.961 m');
    await expect(page.locator('#results')).not.toContainText('81.7%');
    for(const width of [320,390,768,1024,1440]) {
      await page.setViewportSize({width,height:900});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang} at ${width}`);
      const rects=await page.locator('.formation-viewer-shell button').evaluateAll(els=>els.map(el=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,r:r.right,b:r.bottom};}));
      for(let i=0;i<rects.length;i++)for(let j=i+1;j<rects.length;j++) {
        const a=rects[i],b=rects[j];assert.ok(Math.min(a.r,b.r)-Math.max(a.x,b.x)<1||Math.min(a.b,b.b)-Math.max(a.y,b.y)<1,`overlap at ${lang} ${width}`);
      }
    }
    const audit=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
    assert.deepEqual(audit.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})),[]);
    assert.deepEqual(errors,[]);await context.close();
  }
});

test('both models synchronize the page, matrix keyboard navigation and the four Kalman stages',async()=>{
  const {page,context,errors}=await open('pt/');
  for(const [dyn,count] of [['nl',100],['lin',36]]) {
    await choose(page,'dyn',dyn,'#models');
    await expect(page.locator('.mcell')).toHaveCount(count);
    await expect(page.locator(`#lab [data-control=dyn][data-value=${dyn}]`)).toHaveAttribute('aria-pressed','true');
    const selected=page.locator('.mcell[aria-pressed=true]');await selected.focus();await page.keyboard.press('ArrowRight');
    await expect(page.locator('.mcell[data-value="3,1"]')).toHaveAttribute('aria-pressed','true');
    await expect(page.locator('.mcell[data-value="3,1"]')).toBeFocused();
    await expect(page.locator('#matrix .night')).toContainText('∂ẍ / ∂y');
    await page.keyboard.press('Home');await expect(page.locator('.mcell[data-value="3,0"]')).toHaveAttribute('aria-pressed','true');
  }
  const explanations=new Set();
  for(const step of [2,3,4,1]) {
    await page.locator('[data-control=nextStep]').click();
    await expect(page.locator(`[data-control=kstep][data-value="${step}"]`)).toHaveAttribute('aria-pressed','true');
    explanations.add(await page.locator('#filter [aria-live]').textContent());
  }
  assert.equal(explanations.size,4);assert.deepEqual(errors,[]);await context.close();
});

test('filter noise, trust and random seed recalculate plots; the course controller applies its limit',async()=>{
  const {page,context,errors}=await open();
  const before=await page.locator('#lab').textContent(),plots=new Set();
  for(const noise of ['n5','n14','k1','k5']) {
    await choose(page,'noise',noise,'#lab');
    plots.add(await page.locator('#lab svg[role=img]').first().innerHTML());
    await expect(page.locator('#lab')).not.toContainText('NaN');
  }
  // Auto-scaled axes move even the truth path in SVG coordinates. The model
  // tests check invariant physical truth; here each noise level redraws the plot.
  assert.equal(plots.size,4);
  for(const trust of ['more','less','mine'])await choose(page,'trust',trust,'#lab');
  const old=await page.locator('#lab svg[role=img]').innerHTML();
  await page.locator('[data-control=rerun]').click();
  await expect(page.locator('[data-formation]')).toHaveAttribute('data-seed','2');
  assert.notEqual(await page.locator('#lab svg[role=img]').innerHTML(),old);
  assert.notEqual(await page.locator('#lab').textContent(),before);
  await choose(page,'thr','lim','#control');
  await expect(page.locator('#control')).toContainText('50.0 N');
  await choose(page,'thr','free','#control');
  await expect(page.locator('#control')).toContainText('66.9 N');
  assert.deepEqual(errors,[]);await context.close();
});

test('orbital viewer supports keyboard, touch, saved cameras and pausing off screen',async()=>{
  const {page,context,errors}=await open('',{hasTouch:true});
  const root=page.locator('[data-formation]'),cv=page.locator('canvas');
  await cv.scrollIntoViewIfNeeded();
  const capture=()=>cv.evaluate(c=>c.toDataURL());
  const initial=await capture();await cv.focus();await page.keyboard.press('ArrowRight');assert.notEqual(await capture(),initial);
  await page.keyboard.press('+');const zoomed=await capture();await choose(page,'view','earth','#models');
  assert.notEqual(await capture(),zoomed);await choose(page,'view','rel','#models');assert.equal(await capture(),zoomed);
  await page.locator('[data-control=preset][data-value=iso]').click();const reset=await capture();
  const box=await cv.boundingBox(),cdp=await context.newCDPSession(page);
  const points=d=>[{x:box.x+box.width/2-d,y:box.y+180,id:1},{x:box.x+box.width/2+d,y:box.y+180,id:2}];
  await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:points(30)});
  await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:points(65)});
  await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
  assert.notEqual(await capture(),reset);
  await expect(root).toHaveAttribute('data-paused','true');
  await page.locator('[data-control=pause]').click();await expect(root).toHaveAttribute('data-animating','true');
  await page.locator('#results').scrollIntoViewIfNeeded();await expect(root).toHaveAttribute('data-animating','false');
  await cv.scrollIntoViewIfNeeded();await expect(root).toHaveAttribute('data-animating','true');
  await page.locator('[data-control=pause]').click();await expect(root).toHaveAttribute('data-animating','false');
  assert.deepEqual(errors,[]);await context.close();
});

test('initial content works without scripts and calculation falls back if a worker cannot start',async()=>{
  const {page,context}=await open('fr/',{javaScriptEnabled:false});
  await expect(page.locator('#results')).toContainText('4.961 m');
  await expect(page.locator('#lab')).toContainText('4.81 m');
  await expect(page.locator('.formation-static-orbit')).toBeVisible();
  await expect(page.locator('[data-control]:not([disabled])')).toHaveCount(0);
  await context.close();
  const fallback=await open('es/',{},true);
  await choose(fallback.page,'dyn','nl','#models');await expect(fallback.page.locator('.mcell')).toHaveCount(100);
  assert.deepEqual(fallback.errors,[]);await fallback.context.close();
});

test('ITA keeps its experience URL, directory filters, language and previous/next navigation',async()=>{
  const {page,context,errors}=await open('pt/');
  await expect(page.locator('.flight-stop')).toHaveCount(6);
  await expect(page.locator('[data-back-results]')).toHaveAttribute('href',/\/pt\/experience.html#experience_2$/);
  await page.locator('[data-back-results]').click();await expect(page).toHaveURL(/\/pt\/experience.html#experience_2$/);
  const card=page.locator('a[href="pages/experience/experience_2.html"]').first();await card.click();
  await expect(page.locator('.formation-pass')).toBeVisible();
  await page.locator('.language-switch a[lang=fr],.home-languages a[lang=fr],a[hreflang=fr]').last().click();
  await expect(page).toHaveURL(/\/fr\/pages\/experience\/experience_2.html$/);
  assert.deepEqual(errors,[]);await context.close();
});
