import {test, before, after} from 'node:test';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {chromium, expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import {readdir} from 'node:fs/promises';
let browser, server, base;
before(async () => {
  server = spawn('python3', ['tests/server.py'], {stdio:['ignore','pipe','pipe']});
  let stderr = '';
  server.stderr.on('data', chunk => { stderr += chunk; });
  base = await new Promise((resolve,reject) => {
    const timer=setTimeout(()=>reject(new Error('Test server timeout: '+stderr)),10000);
    server.once('error',error=>{clearTimeout(timer);reject(error);});
    server.once('exit',code=>{clearTimeout(timer);reject(new Error(`Server exited ${code}: ${stderr}`));});
    server.stdout.once('data',chunk=>{clearTimeout(timer);resolve(String(chunk).trim());});
  });
  browser = await chromium.launch({headless:true, ...(process.env.BROWSER_EXECUTABLE ? {executablePath:process.env.BROWSER_EXECUTABLE} : {})});
});
after(async () => {
  await browser?.close();
  if(server && server.exitCode===null){const exited=once(server,'exit');server.kill();await exited;}
});
async function visit(path='', options={}) {
  const context=await browser.newContext(options);
  const page=await context.newPage();
  const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  const response=await page.goto(base+path);
  assert.equal(response.status(),200);
  return {page,errors};
}
test('directory shows every project and filters, search and reset compose correctly', async () => {
  const {page,errors}=await visit('projects.html');
  const visible=page.locator('[data-project]:visible');
  await expect(visible).toHaveCount(20);
  await page.locator('[data-filter=outreach]').click();
  await expect(visible).toHaveCount(5);
  assert.equal(new URL(page.url()).searchParams.get('area'),'outreach');
  await page.locator('#project-search').fill('EP Aero');
  await expect(visible).toHaveCount(1);
  await page.locator('#project-search').fill('zzzz-no-match');
  await expect(visible).toHaveCount(0);
  await expect(page.locator('#empty-state')).toBeVisible();
  await page.locator('#reset-filters').click();
  await expect(visible).toHaveCount(20);
  assert.equal(new URL(page.url()).search,'');
  await page.locator('#project-search').fill('STM32');
  await expect(visible).toHaveCount(1);
  assert.deepEqual(errors,[]);
  await page.close();
});
test('return link, browser back, reload and language changes retain directory filters', async () => {
  const {page,errors}=await visit('projects.html?area=space&q=CubeSat');
  await expect(page.locator('[data-project]:visible')).toHaveCount(1);
  await page.locator('[data-project]:visible a').click();
  await expect(page.locator('h1')).toHaveText('CubeSat embedded software');
  await page.reload();
  await page.locator('[data-back-results]').first().click();
  await expect(page.locator('#project-search')).toHaveValue('CubeSat');
  await expect(page.locator('[data-filter=space]')).toHaveAttribute('aria-pressed','true');
  await expect(page.locator('[data-project]:visible')).toHaveCount(1);
  assert.equal(new URL(page.url()).hash,'#project_9');
  await page.locator('.languages a[lang=pt]').click();
  await expect(page.locator('html')).toHaveAttribute('lang','pt');
  await expect(page.locator('#project-search')).toHaveValue('CubeSat');
  await page.locator('[data-project]:visible a').click();
  await expect(page.locator('h1')).toHaveText('Software embarcado para CubeSat');
  await page.goBack();
  await expect(page.locator('[data-project]:visible')).toHaveCount(1);
  await page.reload();
  await expect(page.locator('[data-project]:visible')).toHaveCount(1);
  assert.deepEqual(errors,[]);
  await page.close();
});
test('language switching preserves the case study and section links point to dedicated pages', async () => {
  const {page,errors}=await visit('pages/projects/project_9.html');
  for(const [lang,title] of [['pt','Software embarcado para CubeSat'],['fr','Logiciel embarqué pour CubeSat'],['es','Software embebido para CubeSat'],['en','CubeSat embedded software']]) {
    await page.locator(`.languages a[lang=${lang}]`).click();
    await expect(page.locator('html')).toHaveAttribute('lang',lang);
    await expect(page.locator('h1')).toHaveText(title);
    assert.ok(page.url().endsWith('pages/projects/project_9.html'));
  }
  await page.goto(base+'#recognition');
  await page.waitForURL('**/recognition.html');
  await page.locator('.languages a[lang=pt]').click();
  assert.ok(page.url().endsWith('/pt/recognition.html'));
  await expect(page.locator('#main-nav a[aria-current]')).toHaveText('Conquistas');
  assert.deepEqual(errors,[]);
  await page.close();
});
test('six main pages stay reachable on mobile; all languages fit phone, tablet and desktop', async () => {
  for(const lang of ['','pt/','fr/','es/']) {
    const {page,errors}=await visit(lang,{viewport:{width:390,height:844}});
    for(const file of ['index.html','projects.html','experience.html','about.html','recognition.html','contact.html']) {
      await page.goto(base+lang+file);
      await expect(page.locator('#main-nav a:visible')).toHaveCount(6);
      await expect(page.locator('#main-nav a[aria-current]')).toHaveCount(1);
      for(const width of [320,390,768,1024,1440]) {
        await page.setViewportSize({width,height:900});
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang}${file} overflows at ${width}px`);
      }
    }
    await page.setViewportSize({width:390,height:844});
    await page.locator('#main-nav a[href="projects.html"]').click();
    await expect(page.locator('[data-project]:visible')).toHaveCount(20);
    assert.deepEqual(errors,[]);
    await page.close();
  }
});
test('contact validates fields and posts to the confirmed email, with delivery intercepted', async () => {
  const {page}=await visit('contact.html');
  assert.equal(await page.locator('form').evaluate(form=>form.checkValidity()),false);
  await page.locator('[name=name]').fill('Portfolio test');
  await page.locator('[name=email]').fill('visitor@example.com');
  await page.locator('[name=subject]').fill('Engineering collaboration');
  await page.locator('[name=message]').fill('Test message intercepted locally; no email is sent.');
  assert.equal(await page.locator('form').evaluate(form=>form.checkValidity()),true);
  let requestData;
  await page.route('https://formsubmit.co/**',async route=> {
    requestData={url:route.request().url(),method:route.request().method(),body:route.request().postData()};
    await route.fulfill({status:200,contentType:'text/html',body:'<title>Intercepted locally</title>'});
  });
  await page.locator('button[type=submit]').click();
  await expect(page).toHaveTitle('Intercepted locally');
  assert.equal(requestData.url,'https://formsubmit.co/emillyraianerodrigues@gmail.com');
  assert.equal(requestData.method,'POST');
  const body=new URLSearchParams(requestData.body);
  assert.equal(body.get('email'),'visitor@example.com');
  assert.equal(body.get('subject'),'Engineering collaboration');
  assert.ok(body.get('message').startsWith('Test message'));
  assert.equal(body.has('_captcha'),false);
  await page.close();
});
test('clipboard confirms success and explains permission failure', async () => {
  const context=await browser.newContext({permissions:['clipboard-read','clipboard-write']});
  const page=await context.newPage();
  await page.goto(base+'contact.html');
  await page.locator('#copy-email').click();
  await expect(page.locator('#copy-status')).toHaveText('Email copied');
  assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),'emillyraianerodrigues@gmail.com');
  await page.evaluate(()=>{navigator.clipboard.writeText=async()=>{throw new Error('denied');};});
  await page.locator('#copy-email').click();
  await expect(page.locator('#copy-status')).toContainText('Please select and copy');
  await context.close();
});
test('navigation, all projects and contact remain available without JavaScript', async () => {
  const {page}=await visit('',{javaScriptEnabled:false,viewport:{width:390,height:844}});
  await expect(page.locator('#main-nav a:visible')).toHaveCount(6);
  await page.locator('#main-nav a[href="projects.html"]').click();
  await expect(page.locator('[data-project]:visible')).toHaveCount(20);
  await expect(page.locator('[data-project-tools]')).not.toBeVisible();
  await page.locator('.languages a[lang=fr]').click();
  await expect(page.locator('html')).toHaveAttribute('lang','fr');
  await page.locator('#main-nav a[href="contact.html"]').click();
  await expect(page.locator('form')).toHaveAttribute('method','POST');
  await page.close();
});
test('directory works when browser storage is unavailable and untrusted queries stay text', async () => {
  const {page,errors}=await visit('projects.html?q=%3Cimg%20onerror%3Dalert(1)%3E');
  await page.addInitScript(()=>{Object.defineProperty(window,'sessionStorage',{get(){throw new Error('Storage disabled');}});});
  await page.reload();
  await expect(page.locator('#empty-state')).toBeVisible();
  await page.locator('#reset-filters').click();
  await page.locator('#project-search').fill('CVA6');
  await expect(page.locator('[data-project]:visible')).toHaveCount(1);
  await page.locator('[data-project]:visible a').click();
  await expect(page.locator('[data-back-results]').first()).toHaveAttribute('href','../../projects.html');
  assert.deepEqual(errors,[]);
  await page.close();
});
test('new main pages and representative case studies meet automated WCAG A/AA checks', async () => {
  for(const path of ['', 'pt/', 'fr/', 'es/', 'projects.html','experience.html','about.html','recognition.html','contact.html', 'pages/projects/project_9.html', 'fr/pages/experience/cnes.html']) {
    const {page}=await visit(path,{viewport:{width:path==='pt/'?390:1440,height:1000}});
    const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
    assert.deepEqual(result.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)})),[],`Accessibility violations at ${path}`);
    await page.close();
  }
});
test('all 104 case studies load, show results and fit mobile under a repository prefix', async () => {
  const {page,errors}=await visit();
  for(const lang of ['','pt/','fr/','es/']) {
    for(const kind of ['projects','experience']) {
      const names=(await readdir(`dist/${lang}pages/${kind}`)).filter(x=>x.endsWith('.html')&&!x.includes('exemple'));
      for(const name of names) {
        const response=await page.goto(`${base}${lang}pages/${kind}/${name}`);
        assert.equal(response.status(),200,name);
        await expect(page.locator('h1')).toHaveCount(1);
        await expect(page.locator('#results')).toBeVisible();
        await expect(page.locator('.contents-nav a[href="#results"]')).toHaveCount(1);
        await expect(page.locator('#main-nav a[aria-current]')).toHaveAttribute('href',new RegExp(`${kind}.html$`));
        await page.setViewportSize({width:320,height:844});
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang}${name} overflows`);
      }
    }
  }
  assert.deepEqual(errors,[]);
  await page.close();
});

test('journal photos, report, chapters and translations load under the repository prefix', async () => {
  const {page,errors}=await visit('pt/');
  await page.locator('.journal-entry-link[href="journal/cern.html"]').click();
  await expect(page.locator('h1')).toHaveText('Meu verão no CERN');
  await expect(page.locator('#main-nav a[aria-current]')).toHaveText('Diário');
  await expect(page.locator('[data-gallery]')).toHaveCount(16);
  const report=await page.locator('.journal-resource a[href$=".pdf"]').getAttribute('href');
  const response=await page.request.get(new URL(report,page.url()).href);
  assert.equal(response.status(),200);
  assert.match(response.headers()['content-type'],/pdf/);
  for(const lang of ['en','fr','es','pt']) {
    await page.locator(`.languages a[lang=${lang}]`).click();
    await expect(page.locator('html')).toHaveAttribute('lang',lang);
    assert.ok(page.url().endsWith('journal/cern.html'));
    for(const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:844});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang} journal overflows at ${width}`);
    }
  }
  for(const image of await page.locator('[data-gallery] img').all()) {
    await image.scrollIntoViewIfNeeded();
    await expect(image).toHaveJSProperty('complete',true);
    assert.ok(await image.evaluate(img=>img.naturalWidth>0));
  }
  await page.locator('.journal-index a[href="#travel"]').click();
  await expect(page.locator('#travel')).toBeInViewport();
  await page.locator('.journal-back').click();
  await expect(page.locator('.journal-feed')).toBeInViewport();
  assert.deepEqual(errors,[]);
  await page.close();
});

test('photo viewer supports buttons, keyboard, focus restoration and mobile accessibility', async () => {
  const {page,errors}=await visit('pt/journal/cern.html',{viewport:{width:390,height:844}});
  const first=page.locator('[data-gallery]').first();
  await first.click();
  const dialog=page.locator('.photo-dialog');
  await expect(dialog).toBeVisible();
  await expect(dialog.locator('img')).toHaveAttribute('src',/globo.jpeg$/);
  await expect(page.locator('#photo-counter')).toHaveText('Foto 1 de 16');
  await page.keyboard.press('ArrowRight');
  await expect(dialog.locator('img')).toHaveAttribute('src',/atlas.jpeg$/);
  await dialog.locator('[data-photo-prev]').click();
  await page.keyboard.press('ArrowLeft');
  await expect(page.locator('#photo-counter')).toHaveText('Foto 16 de 16');
  await dialog.locator('[data-photo-next]').click();
  await expect(page.locator('#photo-counter')).toHaveText('Foto 1 de 16');
  const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
  assert.deepEqual(result.violations.map(v=>v.id),[]);
  await page.keyboard.press('Escape');
  await expect(dialog).not.toBeVisible();
  await expect(first).toBeFocused();
  assert.equal(await page.locator('html').evaluate(el=>el.classList.contains('photo-is-open')),false);
  await first.press('Enter');
  await dialog.locator('.photo-close').click();
  await expect(first).toBeFocused();
  assert.deepEqual(errors,[]);
  await page.close();
});

test('journal remains readable and photos open without JavaScript', async () => {
  const {page}=await visit('journal/cern.html',{javaScriptEnabled:false,viewport:{width:390,height:844}});
  await expect(page.locator('.journal-chapter')).toHaveCount(6);
  await expect(page.locator('[data-gallery]')).toHaveCount(16);
  await page.locator('[data-gallery]').first().click();
  assert.ok(page.url().endsWith('portifolio/cern/globo.jpeg'));
  await page.goBack();
  await page.locator('.languages a[lang=fr]').click();
  await expect(page.locator('h1')).toHaveText('Mon été au CERN');
  await page.close();
});

test('journal pages have no automated WCAG A/AA violations', async () => {
  for(const path of ['journal/cern.html','journal/estados-unidos.html','journal/visiona.html','journal/south-summit.html','journal/china.html','journal/connections.html']) {
    for(const prefix of ['','pt/','fr/','es/']) {
      const {page}=await visit(prefix+path,{viewport:{width:390,height:844}});
      const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
      assert.deepEqual(result.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)})),[],prefix+path);
      await page.close();
    }
  }
});


test('new pages load the restored layout even with a previous stylesheet cached', async () => {
  const {page,errors}=await visit('__legacy-cache.html',{viewport:{width:1440,height:1000}});
  assert.equal(await page.locator('body').evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(255, 0, 255)');
  await page.goto(base+'pt/');
  await expect(page.locator('link[rel=stylesheet]')).toHaveAttribute('href', /style\.css\?v=[a-f0-9]{12}$/);
  for(let attempt=0;attempt<2;attempt++) {
    assert.equal(await page.locator('body').evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(244, 241, 233)');
    assert.equal(await page.locator('.hero').evaluate(el=>getComputedStyle(el).display),'grid');
    assert.match(await page.locator('h1').evaluate(el=>getComputedStyle(el).fontFamily),/Georgia/);
    assert.equal(await page.locator('.orbit').first().evaluate(el=>getComputedStyle(el).position),'absolute');
    await page.reload();
  }
  assert.deepEqual(errors,[]);
  await page.close();
});


test('US diary is reachable from the feed and award, with translations and all 15 photos', async () => {
  const {page,errors}=await visit('pt/');
  await expect(page.locator('.journal-entry-link')).toHaveCount(5);
  await page.locator('.journal-entry-link[href="journal/estados-unidos.html"]').click();
  await expect(page.locator('h1')).toHaveText('Minha primeira vez nos Estados Unidos');
  await expect(page.locator('#visa')).toContainText('Anderson');
  await expect(page.locator('#boston')).toContainText('eu paguei por conta própria');
  await expect(page.locator('#aeroastro')).toContainText('Kerri Cahoy');
  await expect(page.locator('#back-home')).toContainText('Claude');
  await expect(page.locator('.journal-chapter')).toHaveCount(7);
  await expect(page.locator('[data-gallery]')).toHaveCount(15);
  await expect(page.locator('.journal-prose p>a[target="_blank"]')).toHaveCount(3);
  for(const lang of ['en','fr','es','pt']) {
    await page.locator(`.languages a[lang=${lang}]`).click();
    await expect(page.locator('html')).toHaveAttribute('lang',lang);
    assert.ok(page.url().endsWith('journal/estados-unidos.html'));
    for(const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:844});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang} US diary overflows at ${width}`);
    }
  }
  for(const image of await page.locator('[data-gallery] img').all()) {
    await image.scrollIntoViewIfNeeded();
    await expect(image).toHaveJSProperty('complete',true);
    assert.ok(await image.evaluate(img=>img.naturalWidth>0));
  }
  await page.locator('#main-nav a[href="../recognition.html"]').click();
  await page.locator('.award a[href="journal/estados-unidos.html"]').click();
  await expect(page.locator('h1')).toHaveText('Minha primeira vez nos Estados Unidos');
  await page.locator('[data-gallery]').first().click();
  await expect(page.locator('#photo-counter')).toHaveText('Foto 1 de 15');
  await page.keyboard.press('ArrowLeft');
  await expect(page.locator('#photo-counter')).toHaveText('Foto 15 de 15');
  await page.keyboard.press('Escape');
  assert.deepEqual(errors,[]);
  await page.close();
});


test('Visiona diary links both ways to experience and loads its six photos in every language', async () => {
  const {page,errors}=await visit('pt/',{reducedMotion:'reduce'});
  await page.locator('.journal-entry-link[href="journal/visiona.html"]').click();
  await expect(page.locator('h1')).toHaveText('Visiona: um novo olhar para o Brasil');
  await expect(page.locator('#entrevista')).toContainText('francês');
  await expect(page.locator('#sistemas')).toContainText('engenharia de sistemas');
  await expect(page.locator('#lit')).toContainText('INPE');
  await expect(page.locator('[data-gallery]')).toHaveCount(6);
  await page.locator('.journal-intro a').click();
  await expect(page.locator('h1')).toHaveText('Visiona · Software de voo embarcado');
  await page.locator('.journal-callout a').click();
  assert.ok(page.url().endsWith('journal/visiona.html'));
  for(const lang of ['en','fr','es','pt']) {
    await page.locator(`.languages a[lang=${lang}]`).click();
    await expect(page.locator('html')).toHaveAttribute('lang',lang);
    assert.ok(page.url().endsWith('journal/visiona.html'));
    await expect(page.locator('.journal-intro a')).toHaveAttribute('href','../pages/experience/visiona.html');
    for(const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:844});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang} Visiona diary overflows at ${width}`);
    }
  }
  for(const image of await page.locator('[data-gallery] img').all()) {
    await image.scrollIntoViewIfNeeded();
    await expect.poll(()=>image.evaluate(img=>img.complete&&img.naturalWidth>0)).toBeTruthy();
  }
  await page.locator('.journal-index a[href="#lit"]').click();
  const headingTop=await page.locator('#lit h2').evaluate(el=>el.getBoundingClientRect().top);
  const headerBottom=await page.locator('.site-header').evaluate(el=>el.getBoundingClientRect().bottom);
  assert.ok(headingTop>=headerBottom,'Chapter heading stays below the sticky navigation');
  await page.locator('[data-gallery]').last().click();
  await expect(page.locator('#photo-counter')).toHaveText('Foto 6 de 6');
  await page.keyboard.press('ArrowRight');
  await expect(page.locator('#photo-counter')).toHaveText('Foto 1 de 6');
  await page.keyboard.press('Escape');
  assert.deepEqual(errors,[]);
  await page.close();
});


test('timeline follows experience dates and links directly to the two US trip stages without JavaScript', async () => {
  const {page}=await visit('pt/',{javaScriptEnabled:false,reducedMotion:'reduce',viewport:{width:390,height:844}});
  assert.deepEqual(await page.locator('.journal-timeline time').evaluateAll(items=>items.map(i=>i.dateTime)),['2025-10','2026-01-25','2026-03-25','2026-04-06','2026-04-10','2026-07']);
  assert.deepEqual(await page.locator('.journal-entry-link').evaluateAll(items=>items.map(i=>i.getAttribute('href'))),['journal/visiona.html','journal/china.html','journal/south-summit.html','journal/estados-unidos.html','journal/cern.html']);
  await page.locator('.journal-timeline a[href="journal/estados-unidos.html#boston"]').click();
  await expect(page.locator('#boston h2')).toBeInViewport();
  await page.locator('.journal-back').click();
  await page.locator('.journal-timeline a[href="journal/south-summit.html"]').click();
  await expect(page.locator('[data-gallery]')).toHaveCount(10);
  await page.close();
});

test('people and institutions connect stories in all languages without fabricated related entries', async () => {
  for(const prefix of ['','pt/','fr/','es/']) {
    const {page,errors}=await visit(prefix+'journal/south-summit.html',{viewport:{width:390,height:844}});
    await page.locator('.journal-connections a[href="connections.html#visiona"]').click();
    await expect(page.locator('#visiona li')).toHaveCount(2);
    await expect(page.locator('#veronica li')).toHaveCount(1);
    await expect(page.locator('#fundacao-estudar li')).toHaveCount(1);
    await page.locator('#visiona a[href="visiona.html"]').click();
    await expect(page.locator('.journal-connections a[href="south-summit.html"]')).toHaveCount(1);
    await page.locator('.journal-connections a[href="south-summit.html"]').click();
    for(const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:844});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${prefix} South Summit overflows at ${width}`);
    }
    for(const img of await page.locator('[data-gallery] img').all()) {
      await img.scrollIntoViewIfNeeded();
      await expect.poll(()=>img.evaluate(i=>i.complete&&i.naturalWidth>0)).toBeTruthy();
    }
    assert.deepEqual(errors,[]);
    await page.close();
  }
});

test('email screenshots are real image links and sender-address masks are baked into the public PNGs', async () => {
  const {page,errors}=await visit('pt/journal/cern.html');
  await expect(page.locator('.journal-document')).toHaveCount(2);
  await expect(page.locator('.journal-transcript')).toHaveCount(2);
  const cases=[
    ['pt/journal/cern.html','recusa-cern-protegido.png',[190,59,397,79]],
    ['pt/journal/cern.html','aprovacao-cern-protegido.png',[139,159,311,179]],
    ['pt/journal/estados-unidos.html','aprovacao-bsv-protegido.png',[131,91,287,112]],
  ];
  for(const [path,file,box] of cases) {
    await page.goto(base+path);
    const img=page.locator(`.journal-document img[src$="${file}"]`);
    await img.scrollIntoViewIfNeeded();
    await expect.poll(()=>img.evaluate(i=>i.complete&&i.naturalWidth>0)).toBeTruthy();
    assert.equal(await img.evaluate((i,[x1,y1,x2,y2])=>{
      const canvas=document.createElement('canvas');canvas.width=i.naturalWidth;canvas.height=i.naturalHeight;
      const ctx=canvas.getContext('2d');ctx.drawImage(i,0,0);
      const data=ctx.getImageData(x1,y1,x2-x1+1,y2-y1+1).data;
      for(let j=0;j<data.length;j+=4) if(data[j]!==25||data[j+1]!==29||data[j+2]!==33||data[j+3]!==255)return false;
      return true;
    },box),true,`${file} must contain an opaque baked-in mask`);
    const href=await img.locator('..').getAttribute('href');
    assert.ok(href.endsWith(file));
    const response=await page.request.get(new URL(href,page.url()).href);
    assert.equal(response.status(),200);assert.match(response.headers()['content-type'],/image\/png/);
  }
  assert.deepEqual(errors,[]);
  await page.close();
});


test('China diary connects to its award, loads all 26 photos and keeps chapter navigation usable in four languages', async () => {
  for(const prefix of ['', 'pt/', 'fr/', 'es/']) {
    const {page,errors}=await visit(prefix+'recognition.html',{reducedMotion:'reduce',viewport:{width:390,height:844}});
    await page.locator('.award a[href="journal/china.html"]').click();
    await expect(page.locator('.journal-chapter')).toHaveCount(8);
    await expect(page.locator('[data-gallery]')).toHaveCount(26);
    await expect(page.locator('.journal-intro a[href="../recognition.html"]')).toHaveCount(1);
    await expect(page.locator('.journal-connections a[href="connections.html#na-pratica"]')).toHaveCount(1);
    for(const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:844});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${prefix} China diary overflows at ${width}`);
    }
    for(const img of await page.locator('[data-gallery] img').all()) {
      await img.scrollIntoViewIfNeeded();
      await expect.poll(()=>img.evaluate(i=>i.complete&&i.naturalWidth>0)).toBeTruthy();
    }
    await page.locator('.journal-index a[href="#regras-invisiveis"]').click();
    const headingTop=await page.locator('#regras-invisiveis h2').evaluate(el=>el.getBoundingClientRect().top);
    const headerBottom=await page.locator('.site-header').evaluate(el=>el.getBoundingClientRect().bottom);
    assert.ok(headingTop>=headerBottom,'Reflection heading is below the sticky header');
    await page.locator('[data-gallery]').last().click();
    await expect(page.locator('#photo-counter')).toContainText('26');
    await page.keyboard.press('Escape');
    await page.locator('.journal-connections a[href="connections.html#na-pratica"]').click();
    await expect(page.locator('#na-pratica a[href="china.html"]')).toHaveCount(1);
    assert.deepEqual(errors,[]);
    await page.close();
  }
});
