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
test('filters, search, reset, show more and empty state compose correctly', async () => {
  const {page,errors}=await visit();
  const visible=page.locator('[data-project]:visible');
  await expect(visible).toHaveCount(6);
  await page.locator('#show-more').click();
  await expect(visible).toHaveCount(20);
  await page.locator('[data-filter=outreach]').click();
  await expect(visible).toHaveCount(5);
  await page.locator('#project-search').fill('EP Aero');
  await expect(visible).toHaveCount(1);
  await page.locator('#project-search').fill('zzzz-no-match');
  await expect(visible).toHaveCount(0);
  await expect(page.locator('#empty-state')).toBeVisible();
  await page.locator('#reset-filters').click();
  await expect(visible).toHaveCount(6);
  await expect(page.locator('[data-filter=all]')).toHaveAttribute('aria-pressed','true');
  await page.locator('#project-search').fill('STM32');
  await expect(visible).toHaveCount(1);
  await page.locator('#project-search').fill('');
  await page.locator('#show-more').click();
  await page.locator('#show-more').click();
  await expect(visible).toHaveCount(6);
  assert.deepEqual(errors,[]);
  await page.close();
});
test('language switching preserves the case study and homepage section', async () => {
  const {page,errors}=await visit('pages/projects/project_9.html');
  for(const [lang,title] of [['pt','Um CubeSat que acompanha a luz.'],['fr','Un CubeSat qui suit la lumière.'],['es','Un CubeSat que sigue la luz.'],['en','A CubeSat that follows the light.']]) {
    await page.locator(`.languages a[lang=${lang}]`).click();
    await expect(page.locator('html')).toHaveAttribute('lang',lang);
    await expect(page.locator('h1')).toHaveText(title);
    assert.ok(page.url().endsWith('pages/projects/project_9.html'));
  }
  await page.goto(base+'#recognition');
  await page.locator('.languages a[lang=pt]').click();
  assert.ok(page.url().endsWith('/pt/index.html#recognition'));
  assert.deepEqual(errors,[]);
  await page.close();
});
test('all languages fit mobile, tablet and desktop; menu supports keyboard and resize', async () => {
  for(const lang of ['en','pt','fr','es']) {
    const {page,errors}=await visit(lang==='en'?'':`${lang}/`,{viewport:{width:390,height:844}});
    await expect(page.locator('#main-nav')).not.toBeVisible();
    await page.locator('.menu-toggle').click();
    await expect(page.locator('#main-nav')).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(page.locator('#main-nav')).not.toBeVisible();
    await expect(page.locator('.menu-toggle')).toBeFocused();
    for(const width of [320,390,768,1024,1440]) {
      await page.setViewportSize({width,height:900});
      const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
      assert.equal(overflow,false,`${lang} overflows at ${width}px`);
    }
    await expect(page.locator('#main-nav')).toBeVisible();
    await page.setViewportSize({width:390,height:844});
    await page.locator('.menu-toggle').click();
    await page.locator('#main-nav a').first().click();
    await expect(page.locator('#main-nav')).not.toBeVisible();
    assert.deepEqual(errors,[]);
    await page.close();
  }
});
test('contact validates fields and posts to the confirmed email, with delivery intercepted', async () => {
  const {page}=await visit();
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
  assert.equal(body.has('_captcha'),false); // Provider verification remains enabled.
  await page.close();
});
test('clipboard confirms success and explains permission failure', async () => {
  const context=await browser.newContext({permissions:['clipboard-read','clipboard-write']});
  const page=await context.newPage();
  await page.goto(base);
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
  await expect(page.locator('[data-project]:visible')).toHaveCount(20);
  await expect(page.locator('#main-nav')).toBeVisible();
  await expect(page.locator('[data-project-tools]')).not.toBeVisible();
  await page.locator('.languages a[lang=fr]').click();
  await expect(page.locator('html')).toHaveAttribute('lang','fr');
  await expect(page.locator('form')).toHaveAttribute('method','POST');
  await page.close();
});
test('representative homepages and case studies meet automated WCAG A/AA checks', async () => {
  for(const path of ['', 'pt/', 'fr/', 'es/', 'pages/projects/project_9.html', 'fr/pages/experience/cnes.html']) {
    const {page}=await visit(path,{viewport:{width:path==='pt/'?390:1440,height:1000}});
    const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
    assert.deepEqual(result.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)})),[],`Accessibility violations at ${path}`);
    await page.close();
  }
});
test('every generated case study loads without JS errors or missing imagery under a repository prefix', async () => {
  const {page,errors}=await visit();
  for(const lang of ['','pt/','fr/','es/']) {
    for(const kind of ['projects','experience']) {
      const names=(await readdir(`dist/${lang}pages/${kind}`)).filter(x=>x.endsWith('.html')&&!x.includes('exemple'));
      for(const name of names) {
        const response=await page.goto(`${base}${lang}pages/${kind}/${name}`);
        assert.equal(response.status(),200,name);
        await expect(page.locator('h1')).toHaveCount(1);
        await expect(page.locator('.detail-image img')).toBeVisible();
        await page.waitForFunction(()=>document.querySelector('.detail-image img').complete);
        assert.equal(await page.locator('.detail-image img').evaluate(img=>img.naturalWidth>0),true,name);
        await page.setViewportSize({width:320,height:844});
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`${lang}${name} overflows`);
      }
    }
  }
  assert.deepEqual(errors,[]);
  await page.close();
});
