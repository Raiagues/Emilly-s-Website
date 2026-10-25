import {test, before, after} from 'node:test';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {existsSync} from 'node:fs';
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
const path='pages/projects/wing-box-analysis.html';
async function open(prefix='',options={}) {
  const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce',...options});
  const page=await context.newPage(),errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  assert.equal((await page.goto(base+prefix+path)).status(),200);
  if(options.javaScriptEnabled!==false)await expect(page.locator('.wingbox-page')).toHaveAttribute('data-ready','true');
  return {page,context,errors};
}
const selected=(page,key)=>page.locator(`[data-${key}-panel]:visible`);

test('wing box keeps the supplied chapters and CAD asset in four accessible, responsive languages',async()=>{
  for(const lang of ['','pt/','fr/','es/']) {
    const {page,context,errors}=await open(lang);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('.wingbox-pass')).toHaveCount(1);
    await expect(page.locator('#main-nav [aria-current]')).toHaveAttribute('href','../../projects.html');
    await expect(page.locator('main sc-for,main a[href$=".dc.html"]')).toHaveCount(0);
    await expect(page.locator('main header img')).toHaveAttribute('src',/img\/wing-box\/wing-cad.jpg$/);
    await expect(page.locator('main a[href="https://github.com/Raiagues/areonautical_structure"]')).toHaveCount(1);
    await expect(page.locator('main a[href="https://raiagues.github.io/areonautical_structure/"]')).toHaveCount(1);
    for(const id of ['wing','envelope','loads','torsion','buckling','results'])await expect(page.locator('#'+id)).toHaveCount(1);
    for(const width of [320,390,768,1024,1440]) {
      await page.setViewportSize({width,height:900});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang} at ${width}`);
      const controls=page.locator('[data-viewer="A"] button');
      const rects=await controls.evaluateAll(els=>els.map(el=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,r:r.right,b:r.bottom}}));
      for(let i=0;i<rects.length;i++)for(let j=i+1;j<rects.length;j++){
        const a=rects[i],b=rects[j];
        assert.ok(Math.min(a.r,b.r)-Math.max(a.x,b.x)<1||Math.min(a.b,b.b)-Math.max(a.y,b.y)<1,`overlapping viewer controls ${lang} ${width}`);
      }
    }
    const audit=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
    assert.deepEqual(audit.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})),[]);
    await page.locator('#buckling').scrollIntoViewIfNeeded();
    assert.ok(Math.abs((await page.locator('.home-header').boundingBox()).y)<2);
    assert.deepEqual(errors,[]);await context.close();
  }
});

test('five V-n points work with the keyboard and synchronize all fifteen load comparisons',async()=>{
  const {page,context,errors}=await open();
  const cases=[['1','229.1 MPa','32.52°'],['2','25.93 MPa','90.75°'],['3','92.35 MPa','9.479°'],['4','44.62 MPa','93.47°'],['5','62.04 MPa','105.1°']];
  const paths=new Set();
  for(const [condition,stress,angle] of cases) {
    await selected(page,'envelope').locator(`[data-condition="${condition}"]`).focus();
    await page.keyboard.press(Number(condition)%2?'Enter':'Space');
    await expect(selected(page,'envelope')).toHaveAttribute('data-envelope-panel',condition);
    await expect(selected(page,'envelope')).toContainText(stress);
    await expect(selected(page,'envelope')).toContainText(angle);
    await expect(selected(page,'envelope').locator(`[data-condition="${condition}"]`)).toBeFocused();
    await expect(page.locator(`#loads [data-condition="${condition}"]`)).toHaveAttribute('aria-pressed','true');
    for(const mode of ['loads','bend','torque']){
      await page.locator(`[data-mode="${mode}"]`).click();
      await expect(selected(page,'charts')).toHaveAttribute('data-charts-panel',`${condition}-${mode}`);
      const summary=page.locator('[data-load-summary]:visible');
      await expect(summary).toHaveAttribute('data-load-summary',`${condition}-${mode}`);
      await expect(selected(page,'charts').locator('figure')).toHaveCount(mode==='bend'?2:1);
      if(mode==='bend')await expect(summary).toContainText('17.97 mm');
      paths.add(await selected(page,'charts').locator('path').first().getAttribute('d'));
    }
  }
  assert.ok(paths.size>=10,'chart geometry changes across the load cases');
  await page.locator('#loads [data-condition="1"]').click();
  await expect(selected(page,'envelope')).toHaveAttribute('data-envelope-panel','1');
  assert.deepEqual(errors,[]);await context.close();
});

test('all six torsion cases and nine buckling configurations retain the original numerical results',async()=>{
  const {page,context,errors}=await open();
  for(const [key,q,max] of [['f','0.3935','3.935 Pa'],['c1','0.2794','5.012 Pa'],['c2','0.5702','22.9 Pa'],['c3','0.3304','5.417 Pa'],['c4','0.3739','18.69 Pa'],['c5','0.3277','16.38 Pa']]) {
    await page.locator(`[data-torsion="${key}"]`).click();
    await expect(selected(page,'torsion')).toHaveAttribute('data-torsion-panel',key);
    await expect(selected(page,'torsion')).toContainText(q);
    await expect(selected(page,'torsion')).toContainText(max);
  }
  for(const [part,values] of [['top',['29.93','486','685.1']],['side',['92.22','399.4','889.4']],['ribs',['1.249','570.4','595.8']]]){
    for(const [i,choice] of ['none','fewer','ideal'].entries()){
      await page.locator(`[data-part="${part}"][data-choice="${choice}"]:visible`).click();
      const panel=page.locator(`[data-part-panel="${part}-${choice}"]`);
      await expect(panel).toBeVisible();
      await expect(panel).toHaveAttribute('data-holds',String(choice==='ideal'));
      await expect(panel.locator('[data-critical]')).toHaveText(`Critical stress ${values[i]} MPa · needed 572.8 MPa`);
      await expect(panel.locator(`[data-choice="${choice}"]`)).toBeFocused();
    }
  }
  // Failure is conveyed in words, not color alone, and remains accessible.
  await page.locator('[data-part="top"][data-choice="none"]:visible').click();
  await expect(page.locator('[data-part-panel="top-none"] [data-verdict]')).toHaveText('Buckles');
  const audit=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
  assert.deepEqual(audit.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})),[]);
  assert.deepEqual(errors,[]);await context.close();
});

test('both 3D viewers render and respond to presets, drag, zoom, keyboard and touch',async()=>{
  const {page,context,errors}=await open('pt/');
  const fingerprint=canvas=>canvas.evaluate(el=>el.toDataURL());
  for(const key of ['A','B']) {
    const canvas=page.locator(`[data-wing-canvas="${key}"]`);
    await expect(canvas).toHaveAttribute('data-ready','true');
    await canvas.scrollIntoViewIfNeeded();
    const original=await fingerprint(canvas);assert.ok(original.length>10000);
    for(const view of ['top','front','side']) {
      await page.locator(`[data-camera="${key}"][data-view="${view}"]`).click();
      assert.notEqual(await fingerprint(canvas),original);
      await expect(page.locator(`[data-camera="${key}"][data-view="${view}"]`)).toHaveAttribute('aria-pressed','true');
    }
    await canvas.focus();await page.keyboard.press('Home');
    const reset=await fingerprint(canvas);
    await page.keyboard.press('ArrowRight');assert.notEqual(await fingerprint(canvas),reset);
    const rotated=await fingerprint(canvas);await page.keyboard.press('+');assert.notEqual(await fingerprint(canvas),rotated);
    const beforeDrag=await fingerprint(canvas),box=await canvas.boundingBox();
    await page.mouse.move(box.x+box.width*.45,box.y+box.height*.5);await page.mouse.down();
    await page.mouse.move(box.x+box.width*.6,box.y+box.height*.6,{steps:6});await page.mouse.up();
    assert.notEqual(await fingerprint(canvas),beforeDrag);
    const beforeWheel=await fingerprint(canvas);await page.mouse.wheel(0,200);await page.waitForTimeout(100);
    assert.notEqual(await fingerprint(canvas),beforeWheel);
  }
  assert.deepEqual(errors,[]);await context.close();
  const mobile=await open('pt/',{viewport:{width:390,height:844},hasTouch:true,isMobile:true});
  const canvas=mobile.page.locator('[data-wing-canvas="A"]');await canvas.scrollIntoViewIfNeeded();
  const before=await fingerprint(canvas),r=await canvas.boundingBox();
  const session=await mobile.context.newCDPSession(mobile.page);
  const points=[{x:r.x+r.width*.35,y:r.y+r.height*.5},{x:r.x+r.width*.65,y:r.y+r.height*.5}];
  await session.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:points});
  await session.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{...points[0],x:points[0].x-20},{...points[1],x:points[1].x+20}]});
  await session.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
  assert.notEqual(await fingerprint(canvas),before);
  assert.deepEqual(mobile.errors,[]);await mobile.context.close();
});

test('flow animation can pause and respects reduced motion',async()=>{
  const {page,context}=await open('',{reducedMotion:'no-preference'});
  const flow=page.locator('[data-torsion-panel="f"] .flow').first();
  assert.equal(await flow.evaluate(el=>getComputedStyle(el).animationPlayState),'running');
  await page.locator('[data-flow-toggle]').click();
  assert.equal(await flow.evaluate(el=>getComputedStyle(el).animationPlayState),'paused');
  await page.locator('[data-flow-toggle]').click();
  assert.equal(await flow.evaluate(el=>getComputedStyle(el).animationPlayState),'running');
  await page.emulateMedia({reducedMotion:'reduce'});
  await expect(page.locator('[data-flow-toggle]')).toHaveAttribute('aria-pressed','true');
  assert.equal(await flow.evaluate(el=>getComputedStyle(el).animationName),'none');
  await context.close();
});

test('the original results and CAD images stay readable without JavaScript',async()=>{
  for(const prefix of ['','pt/','fr/','es/']){
    const {page,context}=await open(prefix,{javaScriptEnabled:false,viewport:{width:390,height:844}});
    await expect(page.locator('noscript table tbody tr')).toHaveCount(5);
    await expect(page.locator('noscript table')).toContainText('229.1 MPa');
    await expect(page.locator('noscript table')).toContainText('25.93 MPa');
    await expect(page.locator('.wingbox-canvas-fallback').first()).toBeVisible();
    await expect(page.locator('[data-mode="loads"]')).toBeDisabled();
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
    await context.close();
  }
});

test('project catalogue filters, language changes, ticket and real neighbours lead to valid routes',async()=>{
  const {page,context,errors}=await open('pt/');
  await page.goto(base+'pt/projects.html');
  await page.locator('[data-filter="structures"]').click();
  await expect(page.locator('[data-project]:visible')).toHaveCount(1);
  await page.locator('#wing-box-analysis a').click();
  await expect(page.locator('h1')).toHaveText('Análise da caixa da asa');
  await page.locator('[data-back-results]').click();
  await expect(page.locator('[data-filter="structures"]')).toHaveAttribute('aria-pressed','true');
  await page.locator('#wing-box-analysis a').click();
  const english=page.locator('.home-header a[hreflang="en"]');
  await english.click();await expect(page.locator('h1')).toHaveText('Wing box analysis');
  await expect(page.locator('.flight-stop')).toHaveCount(22);
  await expect(page.locator('.flight-stop[aria-current="page"]')).toContainText('2023');
  await page.locator('.wingbox-next').click();
  await expect(page.locator('h1')).toHaveText('Low-level OS kernel');
  await page.goto(base+path);
  for(const rel of ['prev','next']){
    const target=await page.locator(`.case-pagination a[rel="${rel}"]`).getAttribute('href');
    assert.equal((await page.request.get(new URL(target,page.url()).href)).status(),200);
  }
  assert.deepEqual(errors,[]);await context.close();
});
