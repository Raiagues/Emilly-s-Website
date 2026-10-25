import {test, before, after} from 'node:test';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {readdir, readFile} from 'node:fs/promises';
import {existsSync} from 'node:fs';
// ./setup --with-tests keeps downloaded browsers inside the checkout.
if (!process.env.PLAYWRIGHT_BROWSERS_PATH && existsSync('.runtime/browsers')) {
  process.env.PLAYWRIGHT_BROWSERS_PATH = new URL('../.runtime/browsers', import.meta.url).pathname;
}
const {chromium, expect} = await import('@playwright/test');
const {default: AxeBuilder} = await import('@axe-core/playwright');
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
async function chooseLanguage(page, lang) {
  await page.locator(`.languages a[lang=${lang}]`).click();
}
async function openArchive(page) {
  if (!new URL(page.url()).pathname.endsWith('/journal.html')) await page.locator('#journal .section-heading a[href="journal.html"]').click();
}
async function openStories(page) {
  await page.locator('.flight-path').scrollIntoViewIfNeeded();
}
async function openFlightStory(page, slug) {
  await page.locator(`.flight-map a[href="${slug}.html"]`).click();
  if (!page.url().endsWith(`/${slug}.html`)) {
    await page.locator('.flight-preview:visible .btn').click();
  }
}
async function openChapter(page, id) {
  if (!await page.locator('.story-contents').evaluate(el=>el.open)) {
    await page.locator('.story-contents>summary').click();
  }
  await page.locator(`.story-contents a[href="#${id}"]`).click();
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
  await chooseLanguage(page, 'pt');
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
    await chooseLanguage(page, lang);
    await expect(page.locator('html')).toHaveAttribute('lang',lang);
    await expect(page.locator('h1')).toHaveText(title);
    assert.ok(page.url().endsWith('pages/projects/project_9.html'));
  }
  await page.goto(base+'recognition.html');
  await chooseLanguage(page, 'pt');
  assert.ok(page.url().endsWith('/pt/recognition.html'));
  await expect(page.locator('#main-nav a[aria-current]')).toHaveText('Conquistas');
  assert.deepEqual(errors,[]);
  await page.close();
});
test('persistent seven-item navigation keeps every destination reachable across languages and viewport sizes', async () => {
  for(const lang of ['','pt/','fr/','es/']) {
    const {page,errors}=await visit(lang,{viewport:{width:390,height:844}});
    for(const file of ['index.html','projects.html','experience.html','about.html','recognition.html','journal.html','contact.html']) {
      await page.goto(base+lang+file);
      await expect(page.locator('#main-nav a:visible')).toHaveCount(7);
      await expect(page.locator('#main-nav a[aria-current]')).toHaveCount(1);
      for(const width of [360,390,768,1024,1440]) {
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
  await expect(page.locator('#main-nav a:visible')).toHaveCount(7);
  await page.locator('#current-work .section-heading a[href="projects.html"]').click();
  await expect(page.locator('[data-project]:visible')).toHaveCount(20);
  await expect(page.locator('[data-project-tools]')).not.toBeVisible();
  await chooseLanguage(page, 'fr');
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
  for(const path of ['', 'pt/', 'fr/', 'es/', 'projects.html','experience.html','about.html','recognition.html','contact.html','journal.html','pt/journal.html','fr/journal.html','es/journal.html', 'pages/projects/project_9.html', 'fr/pages/experience/cnes.html']) {
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
        await expect(page.locator('.case-boarding')).toHaveCount(1);
        await expect(page.locator('.flight-stop')).toHaveCount(kind==='projects'?20:6);
        await expect(page.locator('.flight-stop[aria-current=page]')).toHaveCount(1);
        await expect(page.locator('#main-nav a[aria-current]')).toHaveAttribute('href',new RegExp(`${kind}.html$`));
        await page.setViewportSize({width:320,height:844});
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang}${name} overflows`);
        for (const photo of await page.locator('.case-photo-slots img').all()) {
          await photo.scrollIntoViewIfNeeded();
          await photo.evaluate(img=>img.decode());
          const ratio=await photo.evaluate(img=>({rendered:img.clientWidth/img.clientHeight,original:img.naturalWidth/img.naturalHeight}));
          assert.ok(Math.abs(ratio.rendered-ratio.original)<.02,`${lang}${name} has a distorted photo`);
        }
      }
    }
  }
  assert.deepEqual(errors,[]);
  await page.close();
});

test('journal photos, report, chapters and translations load under the repository prefix', async () => {
  const {page,errors}=await visit('pt/');
  await openArchive(page);
  await page.locator('.story-archive>ol>li>a[href="journal/cern.html"]').click();
  await expect(page.locator('h1')).toHaveText('Meu verão no CERN');
  await expect(page.locator('#main-nav a[aria-current]')).toHaveText('Diário');
  await expect(page.locator('[data-gallery]')).toHaveCount(16);
  const report=await page.locator('.journal-resource a[href$=".pdf"]').getAttribute('href');
  const response=await page.request.get(new URL(report,page.url()).href);
  assert.equal(response.status(),200);
  assert.match(response.headers()['content-type'],/pdf/);
  for(const lang of ['en','fr','es','pt']) {
    await chooseLanguage(page, lang);
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
  await openChapter(page, 'travel');
  await expect(page.locator('#travel')).toBeInViewport();
  await page.locator('.inner-breadcrumb .btn').click();
  await expect(page.locator('.postcard-rack')).toHaveCount(1);
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
  await chooseLanguage(page, 'fr');
  await expect(page.locator('h1')).toHaveText('Mon été au CERN');
  await page.close();
});

test('journal pages have no automated WCAG A/AA violations', async () => {
  for(const path of ['journal/cern.html','journal/cnes.html','journal/estados-unidos.html','journal/visiona.html','journal/south-summit.html','journal/china.html','journal/premio-na-pratica.html','journal/fundacao-estudar.html','journal/brafitec.html']) {
    for(const prefix of ['','pt/','fr/','es/']) {
      const {page}=await visit(prefix+path,{viewport:{width:390,height:844}});
      const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
      assert.deepEqual(result.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)})),[],prefix+path);
      await page.close();
    }
  }
});


test('home redesign loads even with a previous stylesheet cached', async () => {
  const {page,errors}=await visit('__legacy-cache.html',{viewport:{width:1440,height:1000}});
  assert.equal(await page.locator('body').evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(255, 0, 255)');
  await page.goto(base+'pt/');
  await expect(page.locator('link[rel=stylesheet][href*="home.css"]')).toHaveAttribute('href', /home\.css\?v=[a-f0-9]{12}$/);
  for(let attempt=0;attempt<2;attempt++) {
    assert.equal(await page.locator('body').evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(244, 238, 226)');
    assert.equal(await page.locator('.hero').evaluate(el=>getComputedStyle(el).display),'grid');
    assert.match(await page.locator('h1').evaluate(el=>getComputedStyle(el).fontFamily),/Big Shoulders Display/);
    await expect(page.locator('.hero h1')).toHaveText('Emilly RodriguesPortfólio');
    await expect(page.locator('.hero-launch')).toHaveCount(1);
    await page.reload();
  }
  assert.deepEqual(errors,[]);
  await page.close();
});


test('US diary is reachable from the feed and award, with translations and all 15 photos', async () => {
  const {page,errors}=await visit('pt/');
  await openArchive(page);
  await expect(page.locator('.story-archive>ol>li>a')).toHaveCount(9);
  await page.locator('.story-archive>ol>li>a[href="journal/estados-unidos.html"]').click();
  await expect(page.locator('h1')).toHaveText('Minha primeira vez nos Estados Unidos');
  await expect(page.locator('#visa')).toContainText('27 de fevereiro de 2026');
  await expect(page.locator('#visa')).toContainText('Fundação Estudar');
  await expect(page.locator('#boston')).toContainText('eu paguei por conta própria');
  await expect(page.locator('#aeroastro')).toContainText('Kerri Cahoy');
  await expect(page.locator('#back-home')).toContainText('Claude');
  await expect(page.locator('.journal-chapter')).toHaveCount(7);
  await expect(page.locator('[data-gallery]')).toHaveCount(15);
  await expect(page.locator('.journal-prose p>a[target="_blank"]')).toHaveCount(3);
  for(const lang of ['en','fr','es','pt']) {
    await chooseLanguage(page, lang);
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
  await page.locator('#main-nav a[href="../about.html"]').click();
  await page.locator('main a[href="recognition.html"]').click();
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


test('Visiona diary links both ways to experience and loads its nine photos in every language', async () => {
  const {page,errors}=await visit('pt/',{reducedMotion:'reduce'});
  await openArchive(page);
  await page.locator('.story-archive>ol>li>a[href="journal/visiona.html"]').click();
  await expect(page.locator('h1')).toHaveText('Software de voo e engenharia de sistemas na Visiona');
  await expect(page.locator('#entrevista')).toContainText('francês');
  await expect(page.locator('#sistemas')).toContainText('engenharia de sistemas');
  await expect(page.locator('#lit')).toContainText('INPE');
  await expect(page.locator('[data-gallery]')).toHaveCount(9);
  await page.locator('.journal-intro a').click();
  await expect(page.locator('h1')).toHaveText('Visiona · Software de voo embarcado');
  await page.locator('.journal-callout a').click();
  assert.ok(page.url().endsWith('journal/visiona.html'));
  for(const lang of ['en','fr','es','pt']) {
    await chooseLanguage(page, lang);
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
  await openChapter(page, 'lit');
  const headingTop=await page.locator('#lit h2').evaluate(el=>el.getBoundingClientRect().top);
  const headerBottom=await page.locator('.home-header').evaluate(el=>el.getBoundingClientRect().bottom);
  assert.ok(headingTop>=headerBottom,'Chapter heading stays below the sticky navigation');
  await page.locator('[data-gallery]').last().click();
  await expect(page.locator('#photo-counter')).toHaveText('Foto 9 de 9');
  await page.keyboard.press('ArrowRight');
  await expect(page.locator('#photo-counter')).toHaveText('Foto 1 de 9');
  await page.keyboard.press('Escape');
  assert.deepEqual(errors,[]);
  await page.close();
});


test('postcard route follows story dates and preserves access to each trip stage without JavaScript', async () => {
  const {page}=await visit('pt/journal.html',{javaScriptEnabled:false,reducedMotion:'reduce',viewport:{width:390,height:844}});
  const dates=await page.locator('.rack-route time').evaluateAll(items=>items.map(i=>i.dateTime));
  assert.equal(dates.length,9);
  assert.deepEqual(dates,[...dates].sort().reverse());
  await page.locator('.postcard-card[href="journal/estados-unidos.html"]').click();
  await openChapter(page,'boston');
  await expect(page.locator('#boston h2')).toBeInViewport();
  await openChapter(page,'silicon-valley');
  await expect(page.locator('#silicon-valley h2')).toBeInViewport();
  await page.locator('.inner-breadcrumb .btn').click();
  await page.locator('.postcard-card[href="journal/south-summit.html"]').click();
  await expect(page.locator('[data-gallery]')).toHaveCount(10);
  await page.close();
});

test('stories remain connected without a public people directory in every language', async () => {
  for(const prefix of ['','pt/','fr/','es/']) {
    const {page,errors}=await visit(prefix+'journal/south-summit.html',{viewport:{width:390,height:844}});
    await expect(page.locator('a[href*="connections.html"]')).toHaveCount(0);
    assert.equal((await page.request.get(base+prefix+'journal/connections.html')).status(),404);
    await openStories(page);
    await openFlightStory(page, 'visiona');
    await expect(page.locator('.flight-map a[href="south-summit.html"]')).toHaveCount(1);
    await openStories(page);
    await openFlightStory(page, 'south-summit');
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
    await expect(page.locator('.journal-intro a[href="premio-na-pratica.html"]')).toHaveCount(1);
    await expect(page.locator('a[href*="connections.html"]')).toHaveCount(0);
    for(const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:844});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${prefix} China diary overflows at ${width}`);
    }
    for(const img of await page.locator('[data-gallery] img').all()) {
      await img.scrollIntoViewIfNeeded();
      await expect.poll(()=>img.evaluate(i=>i.complete&&i.naturalWidth>0)).toBeTruthy();
    }
    await openChapter(page, 'regras-invisiveis');
    const headingTop=await page.locator('#regras-invisiveis h2').evaluate(el=>el.getBoundingClientRect().top);
    const headerBottom=await page.locator('.home-header').evaluate(el=>el.getBoundingClientRect().bottom);
    assert.ok(headingTop>=headerBottom,'Reflection heading is below the sticky header');
    await page.locator('[data-gallery]').last().click();
    await expect(page.locator('#photo-counter')).toContainText('26');
    await page.keyboard.press('Escape');
    await openStories(page);
    await openFlightStory(page, 'premio-na-pratica');
    await expect(page.locator('.flight-map a[href="china.html"]')).toHaveCount(1);
    assert.deepEqual(errors,[]);
    await page.close();
  }
});


test('award story connects China and US diaries, keeps both award links, and loads its photos in every language', async () => {
  for(const prefix of ['', 'pt/', 'fr/', 'es/']) {
    const {page,errors}=await visit(prefix+'recognition.html',{reducedMotion:'reduce',viewport:{width:390,height:844}});
    const award=page.locator('.award').filter({has:page.locator('a[href="journal/premio-na-pratica.html"]')});
    await expect(award.locator('a[href="journal/china.html"]')).toHaveCount(1);
    await award.locator('a[href="journal/premio-na-pratica.html"]').click();
    await expect(page.locator('.journal-chapter')).toHaveCount(6);
    await expect(page.locator('[data-gallery]')).toHaveCount(14);
    await expect(page.locator('.journal-intro a[href="../recognition.html"]')).toHaveCount(1);
    await expect(page.locator('.flight-map a[href="china.html"]')).toHaveCount(1);
    await expect(page.locator('.flight-map a[href="estados-unidos.html"]')).toHaveCount(1);
    for(const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:844});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${prefix} Award diary overflows at ${width}`);
    }
    for(const img of await page.locator('[data-gallery] img').all()) {
      await img.scrollIntoViewIfNeeded();
      await expect.poll(()=>img.evaluate(i=>i.complete&&i.naturalWidth>0)).toBeTruthy();
    }
    await openChapter(page, 'resultado');
    assert.ok(await page.locator('#resultado h2').evaluate(el=>el.getBoundingClientRect().top)>=await page.locator('.home-header').evaluate(el=>el.getBoundingClientRect().bottom));
    await openStories(page);
    await openFlightStory(page, 'china');
    await page.locator('.journal-intro a[href="premio-na-pratica.html"]').click();
    await openStories(page);
    await openFlightStory(page, 'estados-unidos');
    await expect(page.locator('.flight-map a[href="premio-na-pratica.html"]')).toHaveCount(1);
    assert.deepEqual(errors,[]);
    await page.close();
  }
});


test('home preview follows the new section order with official content in four languages', async () => {
  const {page,errors}=await visit('',{reducedMotion:'reduce'});
  const latest=JSON.parse(await readFile('content/journal/cern.json','utf8'));
  for(const lang of ['en','pt','fr','es']) {
    await page.goto(base+(lang==='en'?'':lang+'/'));
    assert.deepEqual(await page.locator('main>section[id]').evaluateAll(nodes=>nodes.map(n=>n.id)),['experience','current-work','my-story','recognition','media','journal','newsletter','say-hello']);
    await expect(page.locator('.story-preview')).toHaveCount(2);
    await expect(page.locator('.story-preview').first().locator('h3')).toHaveText(latest.title[lang]);
    await expect(page.locator('.story-preview').first().locator('.story-preview-copy>p:not(.eyebrow)')).toHaveText(latest.intro[lang]);
    await expect(page.locator('[data-featured-project]')).toHaveCount(3);
    await expect(page.locator('#current-work [data-filter]')).toHaveCount(0);
    await expect(page.locator('#current-work .section-heading a[href="projects.html"]')).toHaveAttribute('href','projects.html');
    await expect(page.locator('.boarding-pass')).toHaveCount(3);
    await expect(page.locator('.boarding-pass img, #current-work img')).toHaveCount(0);
    await expect(page.locator('.boarding-pass svg.illustration')).toHaveCount(3);
    await expect(page.locator('#my-story .letter-lines')).toContainText('Jaru, Rondônia');
    await expect(page.locator('#my-story .letter-lines p')).toHaveCount(2);
    await expect(page.locator('.award-card')).toHaveCount(4);
    await expect(page.locator('.section-heading .section-number,.section-heading .sticker,.journey-strip')).toHaveCount(0);
    await page.locator('#main-nav a[href="#current-work"]').click();
    await expect(page.locator('.current-panel')).toBeInViewport();
    for(const width of [360,390,768,1024,1440]) {
      await page.setViewportSize({width,height:900});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang} home at ${width}`);
    }
    for(const img of await page.locator('main img').all()) {
      await img.scrollIntoViewIfNeeded();
      await expect.poll(()=>img.evaluate(el=>el.complete&&el.naturalWidth>0)).toBeTruthy();
      assert.ok((await img.getAttribute('alt')).length>0);
    }
    await expect(page.locator('#say-hello .btn-solid')).toHaveAttribute('href','mailto:emillyraianerodrigues@gmail.com');
  }
  assert.deepEqual(errors,[]);
  await page.close();
});

test('three featured experiences link to the full list and the inactive newsletter behaves honestly', async () => {
  const {page,errors}=await visit('');
  const passes=page.locator('.boarding-pass');
  await expect(passes.first().locator('.next-destination')).toHaveCount(0);
  await expect(passes.nth(1).locator('.next-destination')).toHaveText('CERN · GVA');
  await expect(passes.nth(2).locator('.next-destination')).toHaveText('VISIONA · BR');
  await expect(page.locator('.experience-filters,[data-experience-filter]')).toHaveCount(0);
  await expect(page.locator('#experience .section-heading .btn')).toContainText('6');
  await expect(page.locator('#experience .section-heading .btn')).toHaveAttribute('href','experience.html');
  await expect(page.locator('.award-card .more')).toHaveCount(0);
  await expect(page.locator('.boarding-pass:visible')).toHaveCount(3);
  await expect(page.locator('#newsletter input[type=checkbox]')).toHaveCount(3);
  await expect(page.locator('#newsletter input[type=radio]')).toHaveCount(2);
  await page.locator('#newsletter input[value="6"]').check();
  await expect(page.locator('#newsletter input[value="6"]')).toBeChecked();
  await expect(page.locator('#newsletter-email')).toBeDisabled();
  await expect(page.locator('#newsletter button')).toBeDisabled();
  await expect(page.locator('#newsletter form')).toHaveCount(0);
  await expect(page.locator('#newsletter-status')).toContainText('No email addresses are collected.');
  assert.deepEqual(errors,[]);
  await page.close();
});

test('personal envelope and illustrated media retain magazines, interviews and news without social reels', async () => {
  const data=JSON.parse(await readFile('content/media.json','utf8'));
  const {page,errors}=await visit('pt/',{viewport:{width:1440,height:1000},reducedMotion:'reduce'});
  await page.evaluate(()=>document.fonts.ready);
  const about=await page.locator('.envelope-copy>p:not(.eyebrow)').evaluate(el=>({height:el.clientHeight,line:parseFloat(getComputedStyle(el).lineHeight)}));
  assert.ok(about.height/about.line<=4,'Home biography stays within four lines on desktop');
  assert.ok(await page.locator('#my-story .envelope').evaluate(el=>el.clientHeight)<600,'Envelope retains the compact prototype proportions');
  await expect(page.locator('.media-magazine img')).toHaveAttribute('src',/exame-cover\.png$/);
  await expect(page.locator('.media-magazine')).toHaveAttribute('href',data.cover.url);
  const tapes=page.locator('.media-tape');
  await expect(tapes).toHaveCount(7);
  assert.deepEqual(await tapes.evaluateAll(items=>items.map(i=>i.getAttribute('href'))),data.videos.map(i=>i.url));
  await expect(page.locator('.media-tape:visible')).toHaveCount(1);
  const next=page.locator('.tape-player [data-carousel-next]');
  await next.focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('.media-tape:visible')).toHaveAttribute('href',data.videos[1].url);
  await expect(page.locator('.media-tape:visible .cassette-art svg')).toHaveCount(1);
  await expect(page.locator('.newspaper-clip:visible')).toHaveCount(2);
  await page.locator('.press-clippings [data-carousel-next]').click();
  await expect(page.locator('.newspaper-clip:visible').first()).toHaveAttribute('href',data.press[2].url);
  await expect(page.locator('.media-phone,.media-social')).toHaveCount(0);
  for(const width of [360,390,768,1440]) {
    await page.setViewportSize({width,height:900});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`Media overflow at ${width}px`);
  }
  assert.deepEqual(errors,[]);
  await page.close();
  const fallback=await visit('pt/',{javaScriptEnabled:false,viewport:{width:360,height:844}});
  await expect(fallback.page.locator('.media-tape:visible')).toHaveCount(7);
  await expect(fallback.page.locator('.newspaper-clip:visible')).toHaveCount(4);
  await fallback.page.close();
});

test('home restores the illustrated opening, original colours and controllable motion', async () => {
  const {page,errors}=await visit('pt/',{reducedMotion:'no-preference'});
  await page.evaluate(()=>document.fonts.ready);
  await expect(page.locator('.hero h1')).toHaveText('Emilly RodriguesPortfólio');
  await expect(page.locator('.hero .btn')).toHaveCount(2);
  await expect(page.locator('.guide')).toBeVisible();
  await expect(page.locator('.hero-launch .launch-window>svg')).toHaveCount(1);
  await expect(page.locator('.hero img')).toHaveAttribute('src',/portrait-lab\.jpeg$/);
  assert.equal(await page.locator('.boarding-pass').first().evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(230, 221, 234)');
  assert.equal(await page.locator('.boarding-pass').nth(1).evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(220, 234, 231)');
  assert.equal(await page.locator('.boarding-pass').nth(2).evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(244, 227, 209)');
  assert.ok(await page.locator('.launch-window').evaluate(el=>el.getAnimations({subtree:true}).length)>0);
  await page.locator('.motion-toggle').click();
  await expect(page.locator('.motion-toggle')).toHaveAttribute('aria-pressed','true');
  assert.equal(await page.locator('.launch-window').evaluate(el=>el.getAnimations({subtree:true}).every(a=>a.playState==='paused')),true);
  await page.locator('.motion-toggle').click();
  for(const width of [320,390,768,1024,1440]) {
    await page.setViewportSize({width,height:900});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`Opening overflow at ${width}`);
  }
  await expect(page.locator('.languages a:visible')).toHaveCount(4);
  await page.locator('.languages a[lang=fr]').focus();
  await expect(page.locator('.languages a[lang=fr]')).toBeFocused();
  await page.locator('#main-nav a[href="#journal"]').click();
  await chooseLanguage(page, 'fr');
  await expect(page.locator('html')).toHaveAttribute('lang','fr');
  assert.equal(new URL(page.url()).hash,'#journal');
  await page.emulateMedia({reducedMotion:'reduce'});
  assert.equal(await page.evaluate(()=>document.getAnimations().length),0);
  assert.deepEqual(errors,[]);
  await page.close();
});

test('cover stays self-contained and both postcard previews fit below the persistent header', async () => {
  const {page}=await visit('pt/',{reducedMotion:'reduce'});
  for (const [width,height] of [[1920,960],[1440,900],[1366,768]]) {
    await page.setViewportSize({width,height});
    await page.goto(base+'pt/');
    await page.evaluate(()=>document.fonts.ready);
    await expect(page.locator('#main-nav a[href="#top"]')).toHaveAttribute('aria-current','location');
    assert.ok(await page.locator('#experience').evaluate(el=>el.getBoundingClientRect().top>=innerHeight));
    for (const panel of await page.locator('.hero-scrapbook,.hero-copy,.hero-launch').all()) {
      assert.ok(await panel.evaluate(el=>el.getBoundingClientRect().bottom<=innerHeight),`Cover fits at ${width}×${height}`);
    }
    for (const img of await page.locator('#journal img').all()) {
      await img.scrollIntoViewIfNeeded();
      await img.evaluate(el=>el.decode());
    }
    await page.locator('#main-nav a[href="#journal"]').click();
    await expect(page.locator('#main-nav a[href="#journal"]')).toHaveAttribute('aria-current','location');
    const bounds=await page.evaluate(()=>({
      header:document.querySelector('.home-header').getBoundingClientRect().toJSON(),
      diary:document.querySelector('#journal').getBoundingClientRect().toJSON(),
      entries:[...document.querySelectorAll('.story-preview')].map(el=>({
        row:el.getBoundingClientRect().toJSON(),
        copy:el.querySelector('.story-preview-copy').getBoundingClientRect().toJSON(),
        photos:el.querySelector('.story-photos').getBoundingClientRect().toJSON(),
      })),
    }));
    assert.ok(Math.abs(bounds.header.top)<1,'Header stays at the top');
    assert.ok(bounds.diary.top>=bounds.header.bottom,`Diary heading is clear at ${width}`);
    assert.ok(bounds.entries[1].row.bottom<=height,`Both stories fit at ${width}×${height}`);
    assert.ok(bounds.entries[0].row.right<=bounds.entries[1].row.left);
    assert.ok(Math.abs(bounds.entries[0].row.top-bounds.entries[1].row.top)<1);
    assert.ok(bounds.entries.every(entry=>entry.photos.bottom<=entry.copy.top));
    await page.locator('#main-nav a[href="#say-hello"]').click();
    await expect(page.locator('#main-nav a[href="#say-hello"]')).toHaveAttribute('aria-current','location');
    await page.locator('#main-nav a[href="#top"]').click();
    await expect(page.locator('#main-nav a[href="#top"]')).toHaveAttribute('aria-current','location');
  }
  await page.close();
});

test('Fundação Estudar joins the award and story paths, with nine photos and honest Lyfe participation in every language', async () => {
  const markers={en:'did not complete the programme',pt:'não concluí o programa',fr:'sans terminer le programme',es:'no terminé el programa'};
  for(const lang of ['en','pt','fr','es']) {
    const prefix=lang==='en'?'':lang+'/';
    const {page,errors}=await visit(prefix+'recognition.html',{viewport:{width:390,height:844},reducedMotion:'reduce'});
    await page.locator('.award a[href="journal/fundacao-estudar.html"]').click();
    await expect(page.locator('.journal-chapter')).toHaveCount(7);
    await expect(page.locator('[data-gallery]')).toHaveCount(9);
    await expect(page.locator('#limites')).toContainText(markers[lang]);
    await expect(page.locator('#primeira-tentativa')).toContainText('2022');
    for(const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:844});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang} foundation at ${width}`);
    }
    for(const img of await page.locator('[data-gallery] img').all()) {
      await img.scrollIntoViewIfNeeded();
      await expect.poll(()=>img.evaluate(i=>i.complete&&i.naturalWidth>0)).toBeTruthy();
    }
    for(const slug of ['premio-na-pratica','china','estados-unidos','south-summit']) {
    await openStories(page);
      await openFlightStory(page, slug);
      assert.ok(page.url().endsWith(`journal/${slug}.html`));
    await openStories(page);
      await openFlightStory(page, 'fundacao-estudar');
    }
    await openStories(page);
    await openFlightStory(page, 'south-summit');
    await openStories(page);
    await openFlightStory(page, 'fundacao-estudar');
    await openChapter(page, 'lyfe');
    await expect(page.locator('#lyfe h2')).toBeInViewport();
    assert.ok(await page.locator('#lyfe h2').evaluate(el=>el.getBoundingClientRect().top)>=await page.locator('.home-header').evaluate(el=>el.getBoundingClientRect().bottom));
    await page.locator('[data-gallery]').last().click();
    await expect(page.locator('.photo-dialog')).toBeVisible();
    await expect(page.locator('#photo-counter')).toContainText('9');
    await page.keyboard.press('Escape');
    assert.deepEqual(errors,[]);
    await page.close();
  }
});

test('every project and experience has a clickable original illustration; motion respects reduced motion', async () => {
  const {page}=await visit('pt/projects.html',{viewport:{width:1440,height:1000},reducedMotion:'no-preference'});
  await expect(page.locator('[data-project] svg.illustration')).toHaveCount(20);
  await expect(page.locator('[data-project] .row-open')).toHaveCount(0);
  for(const card of await page.locator('[data-project]').all()) await expect(card.locator('a')).toHaveCount(1);
  const satellite=page.locator('#project_9 .project-card');
  await satellite.scrollIntoViewIfNeeded();
  await page.mouse.move(0,0);
  const part=satellite.locator('.float');
  assert.equal(await part.evaluate(el=>getComputedStyle(el).animationName),'float');
  await satellite.hover();
  const before=await part.evaluate(el=>getComputedStyle(el).transform);
  await expect.poll(()=>part.evaluate(el=>getComputedStyle(el).transform)).not.toBe(before);
  await page.emulateMedia({reducedMotion:'reduce'});
  assert.equal(await part.evaluate(el=>getComputedStyle(el).animationName),'none');
  await satellite.locator('svg.illustration').click();
  await expect(page.locator('h1')).toContainText('CubeSat');
  await page.goto(base+'pt/experience.html');
  await expect(page.locator('.boarding-pass .art svg.illustration')).toHaveCount(6);
  const experience=page.locator('.boarding-pass').first();
  await experience.focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('.boarding-art svg')).toHaveCount(1);
  await page.close();
});

test('case flight paths preview every chronological stop with keyboard and link to real destinations', async () => {
  for (const [kind,id,count] of [['projects','project_9',20],['experience','cnes',6]]) {
    const {page}=await visit(`pt/pages/${kind}/${id}.html`,{viewport:{width:1440,height:900},reducedMotion:'reduce'});
    const stops=page.locator('.flight-stop');
    await expect(stops).toHaveCount(count);
    const dates=await stops.evaluateAll(items=>items.map(item=>item.dataset.date.match(/\d{4}/g).join('-')));
    assert.deepEqual(dates,[...dates].sort());
    const current=await page.locator('.flight-stop[aria-current=page]').getAttribute('href');
    await stops.first().focus();
    await page.keyboard.press('Space');
    await expect(stops.first()).toHaveAttribute('aria-pressed','true');
    await expect(page.locator('.flight-preview:visible')).toHaveCount(1);
    await expect(page.locator('.flight-stop[aria-current=page]')).toHaveAttribute('href',current);
    for(const width of [320,360,768]) {
      await page.setViewportSize({width,height:844});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
    }
    const next=page.locator('.boarding-stub .next-destination');
    const expected=await page.locator('.flight-stop[aria-current=page]').evaluate(el=>el.nextElementSibling?.getAttribute('href'));
    if (expected) await expect(next).toHaveAttribute('href',expected);
    await stops.first().focus();
    await page.keyboard.press('Enter');
    await page.locator('.flight-preview:visible .btn').click();
    await expect(page.locator('.case-boarding')).toHaveCount(1);
    await page.close();
  }
});

test('CNES diary joins the timeline and professional experience, with 26 photos and a return path from Visiona', async () => {
  for(const lang of ['en','pt','fr','es']) {
    const prefix=lang==='en'?'':lang+'/';
    const {page,errors}=await visit(prefix+'pages/experience/cnes.html',{viewport:{width:390,height:844},reducedMotion:'reduce'});
    await page.locator('.journal-callout a[href="../../journal/cnes.html"]').click();
    await expect(page.locator('h1')).toContainText('CNES');
    await expect(page.locator('.journal-chapter')).toHaveCount(7);
    await expect(page.locator('[data-gallery]')).toHaveCount(26);
    await expect(page.locator('#aerosat')).toContainText('AEROSAT');
    await expect(page.locator('#escolha')).toContainText('2025');
    await expect(page.locator('#escolha')).toContainText('2026');
    await expect(page.locator('.journal-intro a')).toHaveAttribute('href','../pages/experience/cnes.html');
    await expect(page.locator('a[href="https://cnes.fr/projets/nanolab-academy"]')).toHaveCount(1);
    for(const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:844});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang} CNES at ${width}`);
    }
    for(const img of await page.locator('[data-gallery] img').all()) {
      await img.scrollIntoViewIfNeeded();
      await expect.poll(()=>img.evaluate(i=>i.complete&&i.naturalWidth>0)).toBeTruthy();
    }
    await openChapter(page, 'aerosat');
    await expect(page.locator('#aerosat h2')).toBeInViewport();
    assert.ok(await page.locator('#aerosat h2').evaluate(el=>el.getBoundingClientRect().top)>=await page.locator('.home-header').evaluate(el=>el.getBoundingClientRect().bottom));
    await page.locator('[data-gallery]').last().click();
    await expect(page.locator('#photo-counter')).toContainText('26');
    await page.keyboard.press('Escape');
    await openStories(page);
    await openFlightStory(page, 'visiona');
    await openStories(page);
    await openFlightStory(page, 'cnes');
    await expect(page.locator('h1')).toContainText('CNES');
    await openStories(page);
    await openFlightStory(page, 'cern');
    await openStories(page);
    await openFlightStory(page, 'cnes');
    await page.locator('.inner-breadcrumb .btn').click();
    await openArchive(page);
    await expect(page.locator('.rack-route a[href="#archive-cnes"] time')).toHaveAttribute('datetime','2025-02');
    assert.deepEqual(errors,[]);
    await page.close();
  }
});

test('separate diary archive and full project catalogue work without JavaScript', async () => {
  const {page}=await visit('pt/',{javaScriptEnabled:false,viewport:{width:360,height:844},reducedMotion:'reduce'});
  await expect(page.locator('.project-card:visible')).toHaveCount(3);
  await expect(page.locator('.current-panel')).toHaveCount(1);
  await expect(page.locator('.story-preview')).toHaveCount(2);
  await openArchive(page);
  assert.ok(page.url().endsWith('/pt/journal.html'));
  await expect(page.locator('.story-archive>ol>li>a:visible')).toHaveCount(9);
  await chooseLanguage(page,'fr');
  assert.ok(page.url().endsWith('/fr/journal.html'));
  await expect(page.locator('.story-archive>ol>li>a:visible')).toHaveCount(9);
  await page.locator('.inner-breadcrumb a').click();
  await expect(page.locator('.boarding-pass:visible')).toHaveCount(3);
  await page.locator('#current-work .section-heading a[href="projects.html"]').click();
  await expect(page.locator('[data-project]')).toHaveCount(20);
  await page.close();
});

test('story flight path uses event dates and the closing envelope preserves the original text', async () => {
  const {page}=await visit('pt/journal/fundacao-estudar.html',{viewport:{width:1440,height:1000},reducedMotion:'reduce'});
  await expect(page.locator('.flight-map a')).toHaveCount(9);
  const dates=await page.locator('.flight-stop').evaluateAll(items=>items.map(i=>i.dataset.date));
  assert.deepEqual(dates,[...dates].sort());
  await expect(page.locator('.flight-stop[aria-current=page]')).toHaveAttribute('href','fundacao-estudar.html');
  const official=JSON.parse(await readFile('content/journal/fundacao-estudar.json','utf8'));
  await expect(page.locator('.journal-closing p')).toHaveText(official.closing.pt);
  assert.equal(await page.locator('h1,h2,h3').evaluateAll(items=>items.some(i=>/Verônica|Marcel|Lemann|Sicupira/.test(i.textContent))),false);
  await expect(page.locator('#lyfe')).toContainText('Verônica');
  await openFlightStory(page,'south-summit');
  await expect(page.locator('#mentoria h2')).toHaveText('Uma ideia da minha mentora');
  await page.close();
});

test('story contents collapse with keyboard and without JavaScript while photographs stay proportionate', async () => {
  for(const javaScriptEnabled of [true,false]) {
    const {page,errors}=await visit('pt/journal/cnes.html',{javaScriptEnabled,viewport:{width:1813,height:915},reducedMotion:'reduce'});
    const menu=page.locator('.story-contents>summary');
    const chapters=page.locator('.story-contents nav');
    await expect(chapters).not.toBeVisible();
    await menu.focus();
    await page.keyboard.press('Enter');
    await expect(chapters).toBeVisible();
    await page.keyboard.press('Space');
    await expect(chapters).not.toBeVisible();
    for(const width of [320,360,390,768,1100,1280,1813,2560]) {
      await page.setViewportSize({width,height:915});
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`Horizontal overflow at ${width}px`);
      const geometry=await page.locator('[data-gallery] img').evaluateAll(images=>images.map(img=>({height:img.clientHeight,ratio:img.clientWidth/img.clientHeight,original:Number(img.getAttribute('width'))/Number(img.getAttribute('height'))})));
      assert.ok(geometry.every(img=>img.height<=401),`Oversized photo at ${width}px`);
      assert.ok(geometry.every(img=>Math.abs(img.ratio-img.original)<.02),`Distorted photo at ${width}px`);
    }
    await page.setViewportSize({width:390,height:844});
    await openChapter(page,'aerosat');
    await expect(page.locator('#aerosat h2')).toBeInViewport();
    await openFlightStory(page,'brafitec');
    await expect(page.locator('h1')).toHaveText('O caminho até Grenoble');
    assert.deepEqual(errors,[]);
    await page.close();
  }
});

test('BRAFITEC has translated chapters, proportionate photographs and an accessible photo viewer', async () => {
  const {page,errors}=await visit('pt/',{viewport:{width:390,height:844},reducedMotion:'reduce'});
  await openArchive(page);
  await page.locator('.story-archive>ol>li>a[href="journal/brafitec.html"]').click();
  await expect(page.locator('h1')).toHaveText('O caminho até Grenoble');
  await expect(page.locator('#primeira-tentativa')).toContainText('2022');
  await expect(page.locator('#frances')).toContainText('certificado oficial');
  await expect(page.locator('.journal-chapter')).toHaveCount(8);
  await expect(page.locator('[data-gallery]')).toHaveCount(23);
  for(const lang of ['en','fr','es','pt']) {
    await chooseLanguage(page, lang);
    await expect(page.locator('html')).toHaveAttribute('lang',lang);
    for(const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:900});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang} BRAFITEC overflows at ${width}`);
      for(const img of await page.locator('.story-opening-photos img, [data-gallery] img').all()) {
        // CSS must preserve the photograph's ratio, including portrait covers.
        const ratio=await img.evaluate(el=>({rendered:el.clientWidth/el.clientHeight,original:Number(el.getAttribute('width'))/Number(el.getAttribute('height'))}));
        assert.ok(Math.abs(ratio.rendered-ratio.original)<.02,`Photo distorted at ${width}px (${await img.getAttribute('src')}) ${JSON.stringify(ratio)}`);
      }
    }
  }
  for(const img of await page.locator('[data-gallery] img').all()) {
    await img.scrollIntoViewIfNeeded();
    await expect.poll(()=>img.evaluate(el=>el.complete&&el.naturalWidth>0)).toBeTruthy();
  }
  const first=page.locator('[data-gallery]').first();
  await first.click();
  await expect(page.locator('#photo-counter')).toHaveText('Foto 1 de 23');
  await page.keyboard.press('ArrowLeft');
  await expect(page.locator('#photo-counter')).toHaveText('Foto 23 de 23');
  await page.keyboard.press('Escape');
  await expect(first).toBeFocused();
  await page.goto(base+'pt/recognition.html');
  await page.locator('.award a[href="journal/brafitec.html"]').click();
  await expect(page.locator('h1')).toHaveText('O caminho até Grenoble');
  assert.deepEqual(errors,[]);
  await page.close();
});

test('all journal editorial text has four languages and follows the requested punctuation', async () => {
  function inspect(value,location) {
    if(Array.isArray(value)) return value.forEach((v,i)=>inspect(v,`${location}/${i}`));
    if(!value||typeof value!=='object') return;
    if('en' in value) {
      for(const lang of ['en','pt','fr','es']) {
        assert.ok(value[lang]?.trim(),`Missing translation at ${location}/${lang}`);
        assert.doesNotMatch(value[lang],/[:;—–]/,`Punctuation at ${location}/${lang}`);
      }
    } else for(const [key,item] of Object.entries(value)) inspect(item,`${location}/${key}`);
  }
  for(const file of await readdir('content/journal')) {
    if(!file.endsWith('.json')||file==='entities.json') continue;
    inspect(JSON.parse(await readFile(`content/journal/${file}`,'utf8')),file);
  }
});

test('postcard rack sorts, keeps a fixed header and previews stories on hover and focus', async () => {
  const {page,errors}=await visit('pt/journal.html',{viewport:{width:1440,height:900},reducedMotion:'reduce'});
  await expect(page.locator('.postcard-card')).toHaveCount(9);
  await expect(page.locator('.postcard-card').first()).toHaveAttribute('href','journal/cern.html');
  await page.locator('[data-story-order=oldest]').click();
  await expect(page.locator('.postcard-card').first()).toHaveAttribute('href','journal/brafitec.html');
  await page.locator('[data-story-order=newest]').click();
  await expect(page.locator('.postcard-card').first()).toHaveAttribute('href','journal/cern.html');
  await page.locator('.rack-stop[href="#archive-estados-unidos"]').click();
  await expect(page.locator('#archive-estados-unidos')).toBeInViewport();
  assert.equal(await page.locator('.home-header').evaluate(el=>el.getBoundingClientRect().top),0);
  await expect(page.locator('.journal-archive-page #newsletter,.journal-archive-page .dispatch-card')).toHaveCount(0);
  await page.locator('.postcard-card[href="journal/estados-unidos.html"]').click();
  await page.locator('.story-explorer').scrollIntoViewIfNeeded();
  const stop=page.locator('.story-stop[href="brafitec.html"]');
  await stop.hover();
  await expect(page.locator('.story-explorer-preview:visible h3')).toHaveText('O caminho até Grenoble');
  assert.ok(page.url().endsWith('estados-unidos.html'),'Hover does not navigate');
  await stop.focus();
  await page.keyboard.press('ArrowDown');
  await expect(page.locator('.story-stop[href="cnes.html"]')).toBeFocused();
  await expect(page.locator('.story-explorer-preview:visible h3')).toContainText('CNES');
  assert.ok(await page.locator('.story-explorer .flight-map').evaluate(el=>el.scrollHeight>el.clientHeight&&el.clientHeight<=250));
  const railHeight=await page.locator('.story-explorer .flight-map').evaluate(rail=>{
    const height=rail.clientHeight;
    while(rail.children.length<100) rail.append(rail.firstElementChild.cloneNode(true));
    return {before:height,after:rail.clientHeight,scroll:rail.scrollHeight};
  });
  assert.equal(railHeight.after,railHeight.before,'A hundred stories keep the same compact rail');
  assert.ok(railHeight.scroll>railHeight.after*10);
  await page.locator('.story-explorer-preview:visible .btn').click();
  await expect(page.locator('h1')).toContainText('CNES');
  assert.deepEqual(errors,[]);
  await page.close();
});

test('home projects are whole-card links and the on-air indicator respects reduced motion', async () => {
  const {page}=await visit('pt/',{viewport:{width:1440,height:900},reducedMotion:'no-preference'});
  await expect(page.locator('.current-panel')).toHaveAttribute('href','pages/projects/flight-platform.html');
  await expect(page.locator('.current-panel .btn,.current-panel button,.project-grid .more')).toHaveCount(0);
  await expect(page.locator('#current-work .section-heading a')).toContainText('20');
  assert.ok(await page.locator('.current-panel .live-dot').evaluate(el=>el.getAnimations({subtree:true}).length)>0);
  await page.emulateMedia({reducedMotion:'reduce'});
  assert.equal(await page.locator('.current-panel .live-dot').evaluate(el=>el.getAnimations({subtree:true}).length),0);
  await page.locator('.current-panel').click();
  await expect(page.locator('.case-boarding h1')).toBeVisible();
  await page.close();
});
