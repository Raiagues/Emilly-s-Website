import {test, before, after} from 'node:test';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {existsSync} from 'node:fs';
if (!process.env.PLAYWRIGHT_BROWSERS_PATH && existsSync('.runtime/browsers')) process.env.PLAYWRIGHT_BROWSERS_PATH = new URL('../.runtime/browsers', import.meta.url).pathname;
const {chromium, expect}=await import('@playwright/test');
const {default:AxeBuilder}=await import('@axe-core/playwright');
let browser,server,base;
const json=async path=>JSON.parse(await readFile(path,'utf8'));
const kernel=await json('content/kernel-os/evidence.json');
const flight=await json('content/flight-studio/runtime/evidence.json');
before(async()=>{
  server=spawn('python3',['tests/server.py'],{stdio:['ignore','pipe','pipe']});
  base=await new Promise((resolve,reject)=>{
    const timer=setTimeout(()=>reject(new Error('Test server timeout')),10000);
    server.once('error',reject);
    server.stdout.once('data',chunk=>{clearTimeout(timer);resolve(String(chunk).trim());});
  });
  browser=await chromium.launch({headless:true,...(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{})});
});
after(async()=>{
  await browser?.close();
  if(server&&server.exitCode===null){const end=once(server,'exit');server.kill();await end;}
});
async function visit(slug,lang='pt',options={}) {
  const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce',...options});
  const page=await context.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  assert.equal((await page.goto(`${base}${lang==='en'?'':lang+'/'}pages/projects/${slug}.html`)).status(),200);
  return {page,errors};
}
const tabs=(page,id)=>page.locator(`[data-select-group="${id}"] > [data-choices] > button`);
async function seek(panel,index) {
  await panel.locator('[data-replay-seek]').fill(String(index));
}

test('engineering captures retain source hashes, four translations and executable evidence',async()=>{
  const assets=[...await json('content/kernel-os/assets.json'),...await json('content/flight-studio/runtime/screenshots.json')];
  assert.equal(assets.length,44);
  for(const asset of assets){
    const bytes=await readFile(asset.file);
    assert.equal(createHash('sha256').update(bytes).digest('hex'),asset.sha256,asset.file);
    assert.equal(bytes.readUInt32BE(16),asset.width);assert.equal(bytes.readUInt32BE(20),asset.height);
    assert.deepEqual(await readFile('dist/'+asset.file),bytes);
  }
  const locales=await json('content/flight-studio/runtime/locales.json');
  for(const screen of flight.screenshots) for(const lang of ['en','pt','fr','es']) {
    const item=locales[screen.file.split('/').pop().replace('.png','')];
    assert.ok(item?.title[lang]&&item?.caption[lang],screen.file+' '+lang);
  }
  assert.equal(flight.command_flow.command_hex,'1882c000000100a4');
  assert.equal(flight.qemu_verification.current_invocation_operational,true);
  assert.equal(flight.qemu_verification.binary_matches_build,true);
  assert.equal(flight.qemu_verification.tmp105_qmp_value_millic,27830);
  assert.equal(kernel.activities.length,6);
  assert.deepEqual(kernel.activities.at(-1).frames.at(-1).observed.processes.map(p=>p.state_label),['RUN','DIE','DIE','DIE']);
});

test('both engineering pages fit four languages and all mobile/desktop widths',async()=>{
  for(const slug of ['nasa-cfs-platform','operating-system-kernel']) for(const lang of ['en','pt','fr','es']) {
    const {page,errors}=await visit(slug,lang);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('.flight-stop')).toHaveCount(22);
    for(const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:900});
      await page.evaluate(()=>document.fonts.ready);
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`${slug} ${lang} at ${width}`);
    }
    // Check alternate content, where long labels, code and arrays can overflow.
    await page.setViewportSize({width:320,height:900});
    const groups=slug==='nasa-cfs-platform'?['screens','architecture','layers','sensor-path']:['kernel-activities','memory','states'];
    for(const group of groups) for(const button of await tabs(page,group).all()) {
      await button.click();
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`${slug} ${lang} ${group} ${await button.textContent()}`);
    }
    assert.deepEqual(errors,[]);await page.close();
  }
});

test('Flight Studio shows all twelve real screens with keyboard tabs and photo zoom',async()=>{
  const {page,errors}=await visit('nasa-cfs-platform');
  const buttons=tabs(page,'screens');await expect(buttons).toHaveCount(12);
  for(let i=0;i<flight.screenshots.length;i++){
    await buttons.nth(i).click();
    const img=page.locator('#screens-view-'+i+' img');
    await img.evaluate(img=>img.decode());
    assert.equal(await img.evaluate(img=>img.naturalWidth),1728);
    assert.ok((await img.getAttribute('src')).endsWith(flight.screenshots[i].file));
  }
  await buttons.last().focus();await page.keyboard.press('Home');
  await expect(buttons.first()).toBeFocused();
  await page.keyboard.press('ArrowRight');await expect(buttons.nth(1)).toHaveAttribute('aria-selected','true');
  const link=page.locator('#screens-view-1 [data-gallery]');await link.click();
  await expect(page.locator('.photo-dialog')).toBeVisible();
  await expect(page.locator('.photo-dialog img')).toHaveAttribute('src',/native-cfs-operational.png$/);
  await page.keyboard.press('Escape');await expect(link).toBeFocused();
  assert.deepEqual(errors,[]);await page.close();
});

test('command replay and packet inspector connect NOOP to the observed counter change',async()=>{
  const {page,errors}=await visit('nasa-cfs-platform');
  await page.clock.install();
  await expect(page.locator('[data-message-count]')).toHaveText('1 / 6');
  await page.locator('[data-message-play]').click();await page.clock.fastForward(2300);
  await expect(page.locator('[data-message-count]')).toHaveText('2 / 6');
  await page.locator('[data-message-play]').click();await page.clock.fastForward(7000);
  await expect(page.locator('[data-message-count]')).toHaveText('2 / 6');
  await page.locator('[data-step-select="5"]').click();
  await expect(page.locator('[data-step-view="5"]')).toContainText('CommandCounter');
  const command=page.locator('[data-packet-view="command"]');
  const bytes=await command.locator('[data-byte] b').allTextContents();
  assert.equal(bytes.join('').toLowerCase(),flight.command_flow.command_hex);
  assert.equal(bytes.reduce((a,v)=>a^parseInt(v,16),0),255);
  await command.locator('[data-packet-field="4"]').click();
  await expect(command.locator('.is-selected b')).toHaveText('A4');
  for(const [id,value] of [['before','00'],['after','01']]) {
    await page.locator(`[data-packet-kind="${id}"]`).click();
    const packet=page.locator(`[data-packet-view="${id}"]`);
    await packet.locator('[data-packet-field="4"]').click();
    await expect(packet.locator('.is-selected')).toHaveCount(1);
    await expect(packet.locator('.is-selected b')).toHaveText(value);
    await expect(packet.locator('[data-byte="17"] b')).toHaveText('00');
  }
  assert.deepEqual(errors,[]);await page.close();
});

test('sensor explorer evaluates the source waveform and distinguishes QMP injection from app reading',async()=>{
  const {page,errors}=await visit('nasa-cfs-platform');
  for(const [time,celsius,millic] of [[0,'23.500','23500'],[7.5,'28.500','28500'],[22.5,'18.500','18500'],[30,'23.500','23500']]) {
    await page.locator('[data-signal-time]').fill(String(time));
    await expect(page.locator('[data-signal-c]')).toHaveText(celsius);
    await expect(page.locator('[data-signal-mc]')).toHaveText(millic);
  }
  await tabs(page,'sensor-path').last().click();
  await expect(page.locator('#sensor-path-view-3')).toContainText('não tinha uma app de leitura');
  await expect(page.locator('.eng-sensor-evidence')).toContainText('27830');
  assert.deepEqual(errors,[]);await page.close();
});

test('kernel replays all six real activities with source, frame controls and captured process state',async()=>{
  const {page,errors}=await visit('operating-system-kernel');await page.clock.install();
  for(let i=0;i<kernel.activities.length;i++) {
    const activity=kernel.activities[i];await tabs(page,'kernel-activities').nth(i).click();
    const panel=page.locator(`[data-replay="${activity.id}"]`);
    await expect(panel.locator('[data-source-path]').first()).toHaveAttribute('data-source-path',activity.source.path);
    await seek(panel,0);
    await expect(panel.locator('[data-frame] image')).toHaveAttribute('href',new RegExp(activity.frames[0].file+'$'));
    await panel.locator('[data-replay-next]').click();
    await expect(panel.locator('[data-frame-count]')).toContainText('02 /');
    await panel.locator('[data-replay-prev]').click();
    await expect(panel.locator('[data-frame-count]')).toContainText('01 /');
    await panel.locator('[data-replay-zoom]').click();
    await expect(panel.locator('[data-frame]')).toHaveAttribute('viewBox','0 0 1280 720');
    await panel.locator('[data-replay-zoom]').click();
    await panel.locator('[data-replay-play]').click();await page.clock.fastForward(1900);
    await expect(panel.locator('[data-frame-count]')).toContainText('02 /');
    await panel.locator('[data-replay-play]').click();await page.clock.fastForward(4000);
    await expect(panel.locator('[data-frame-count]')).toContainText('02 /');
    await tabs(page,'source-'+activity.id).last().click();
    await expect(panel.locator('[data-source-path]:visible')).toHaveAttribute('data-source-path',activity.demo_source.path);
  }
  const tasks=page.locator('[data-replay="processes"]');await seek(tasks,0);
  assert.deepEqual(await tasks.locator('[data-observed-state]').allTextContents(),['RUN','WAIT','WAIT','WAIT']);
  await seek(tasks,kernel.activities.at(-1).frames.length-1);
  assert.deepEqual(await tasks.locator('[data-observed-state]').allTextContents(),['RUN','DIE','DIE','DIE']);
  await tasks.locator('.eng-capture-notes summary').click();
  await tasks.locator('[data-gallery]').first().click();await expect(page.locator('.photo-dialog')).toBeVisible();
  await page.keyboard.press('Escape');assert.deepEqual(errors,[]);await page.close();
});

test('memory explorer computes valid addresses and draws the repository font bytes',async()=>{
  const {page,errors}=await visit('operating-system-kernel');
  for(const [x,y,expected] of [[0,0,'0x80000000'],[1,0,'0x80000004'],[0,1,'0x80001400'],[1279,719,'0x80383FFC']]) {
    await page.locator('[data-pixel-x]').fill(String(x));await page.locator('[data-pixel-y]').fill(String(y));
    await expect(page.locator('[data-pixel-address]')).toHaveText(expected);
  }
  await page.locator('[data-pixel-x]').fill('9999');await page.locator('[data-pixel-y]').click();
  await expect(page.locator('[data-pixel-x]')).toHaveValue('1279');
  await page.locator('[data-pixel-y]').fill('-10');await page.locator('[data-pixel-x]').click();
  await expect(page.locator('[data-pixel-y]')).toHaveValue('0');
  const glyphs=await json('content/kernel-os/glyphs.json');
  for(const char of ['A','R','0']) {
    await page.locator(`[data-glyph="${char}"]`).click();
    assert.deepEqual((await page.locator('[data-glyph-byte]').allTextContents()).map(v=>parseInt(v,16)),glyphs[char]);
    assert.equal(await page.locator('[data-bit].on').count(),glyphs[char].reduce((sum,b)=>sum+b.toString(2).replaceAll('0','').length,0));
  }
  await tabs(page,'memory').last().click();await expect(page.locator('.eng-memory-row.is-active code')).toHaveText('0x80000000');
  await tabs(page,'states').nth(2).click();await expect(page.locator('[data-state-node="2"]')).not.toHaveClass(/is-muted/);
  assert.deepEqual(errors,[]);await page.close();
});

test('engineering case studies remain complete and images link directly without JavaScript',async()=>{
  for(const [slug,count] of [['nasa-cfs-platform',14],['operating-system-kernel',32]]) {
    const {page}=await visit(slug,'pt',{javaScriptEnabled:false,viewport:{width:390,height:844}});
    await expect(page.locator('[data-gallery]')).toHaveCount(count);
    await expect(page.locator('[data-choices]:visible')).toHaveCount(0);
    for(const details of await page.locator('.eng-original,.eng-capture-notes').all()) await details.evaluate(e=>e.open=true);
    for(const img of await page.locator('[data-gallery] img').all()) {
      await img.scrollIntoViewIfNeeded();await img.evaluate(img=>img.decode());
      assert.ok(await img.evaluate(img=>img.naturalWidth>0));
    }
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
    const link=page.locator('[data-gallery]').first();
    assert.equal((await page.request.get(new URL(await link.getAttribute('href'),page.url()).href)).status(),200);
    await page.close();
  }
});

test('engineering pages and alternate interactive states pass automated WCAG A/AA checks',async()=>{
  for(const slug of ['nasa-cfs-platform','operating-system-kernel']) for(const lang of ['en','pt','fr','es']) {
    const {page}=await visit(slug,lang);
    const check=async label=>{
      const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
      assert.deepEqual(result.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})),[],`${slug} ${lang} ${label}`);
    };
    await check('initial');
    if(lang==='pt') {
      await page.setViewportSize({width:390,height:844});
      if(slug==='operating-system-kernel') {
        await tabs(page,'kernel-activities').last().click();await tabs(page,'memory').last().click();
      } else {
        await tabs(page,'screens').last().click();await page.locator('[data-packet-kind="after"]').click();
      }
      await check('alternate mobile');
    }
    await page.close();
  }
});
