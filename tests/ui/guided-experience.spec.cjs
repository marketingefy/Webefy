/* Run: node tests/ui/guided-experience.spec.cjs. No messages or real API calls. */
'use strict';
const assert = require('node:assert/strict');
const http = require('node:http');
const fs = require('node:fs/promises');
const path = require('node:path');
const { once } = require('node:events');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname, '../../public');

(async () => {
  const server = http.createServer(async (request, response) => {
    try {
      const pathname = decodeURIComponent(new URL(request.url, 'http://local').pathname);
      if (pathname.endsWith('.php')) {
        response.writeHead(503, {'Content-Type': 'application/json'});
        response.end('{"ok":false,"ready":false}'); return;
      }
      const filename = path.resolve(root, '.' + (pathname.endsWith('/') ? pathname + 'index.html' : pathname));
      if (!filename.startsWith(root + path.sep)) throw Error('outside root');
      const content = await fs.readFile(filename);
      const type = {'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.woff2':'font/woff2','.webp':'image/webp','.mp4':'video/mp4','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg'}[path.extname(filename)];
      response.writeHead(200, {'Content-Type':type || 'application/octet-stream'}); response.end(content);
    } catch { response.writeHead(404); response.end(); }
  });
  let browser;
  try {
    server.listen(0, '127.0.0.1'); await once(server, 'listening');
    const base = `http://127.0.0.1:${server.address().port}`;
    browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', headless:true, args:['--no-sandbox'] });
    const context = await browser.newContext({viewport:{width:390,height:844}, reducedMotion:'reduce'});
    context.setDefaultTimeout(5000);
    const errors = [];
    context.on('page', page => page.on('pageerror', error => errors.push(error.message)));
    await context.route('https://**/*', route => route.abort());
    const page = await context.newPage();
    let tested = 0;
    for (const prefix of ['/', '/nueva/']) {
      await page.setViewportSize({width:390,height:844});
      await page.goto(base + prefix + 'index.html');
      assert.deepEqual(await page.locator('.hero-copy .actions a').allTextContents().then(a => a.map(t => t.trim())), ['Solicitar cotización', 'Necesito asistencia']);
      const needs = await page.locator('.protection-card').evaluateAll(nodes => nodes.map(n => ({url:n.href, title:n.querySelector('h3').textContent})));
      assert.deepEqual(needs.map(n => n.title), ['Auto','Salud','Vida','Hogar','Empresa']);
      // Each need has its own in-frame image: Safari must not lazy-load an
      // oversized, offscreen sprite whose selected tile can remain blank.
      for (const card of await page.locator('.protection-card').all()) {
        await card.scrollIntoViewIfNeeded();
        const image = card.locator('.model-single img');
        await image.evaluate(img => img.decode());
        assert.equal(await image.getAttribute('loading'), null);
        assert.equal(await image.evaluate(img => img.naturalWidth), 300);
        const imageBox = await image.boundingBox(), stageBox = await card.locator('.product-stage').boundingBox();
        assert.ok(imageBox.width > 60 && imageBox.height > 60);
        assert.ok(imageBox.x >= stageBox.x && imageBox.x + imageBox.width <= stageBox.x + stageBox.width + 1);
        assert.ok(Math.min(imageBox.y + imageBox.height, stageBox.y + stageBox.height) > Math.max(imageBox.y, stageBox.y));
      }
      for (const need of needs) {
        const target = new URL(need.url);
        assert.equal(target.pathname, prefix + 'cotizar.html');
        await page.goto(need.url);
        assert.equal(await page.locator('#quote-branch').inputValue(), target.searchParams.get('ramo'));
      }
      await page.goto(base + prefix + 'cotizar.html?ramo=not-a-real-service');
      await page.locator('#quote-next').click();
      assert.equal(await page.locator('#quote-progress').getAttribute('value'), '1');
      await page.locator('#quote-branch').selectOption('hogar');
      await page.locator('#quote-next').click();
      assert.equal(await page.locator('#quote-progress').getAttribute('value'), '2');
      await page.locator('#quote-next').click();
      assert.equal(await page.locator('#quote-progress').getAttribute('value'), '2');
      await page.locator('#quote-goal').selectOption({label:'Comparar mi seguro actual'});
      await page.locator('#quote-notes').fill('<img src=x onerror=alert(1)> Quiero proteger mi casa.');
      await page.locator('#quote-next').click();
      assert.equal(await page.locator('#quote-progress').getAttribute('value'), '3');
      assert.match(await page.locator('#quote-summary').inputValue(), /Ramo: Seguro de hogar/);
      assert.equal(await page.locator('.quote-workspace img').count(), 0);
      for (const [index, number] of ['593967146828','593983538633'].entries()) {
        await page.locator('#quote-advisor').selectOption(String(index));
        const outgoing = new URL(await page.locator('#quote-whatsapp').getAttribute('href'));
        assert.equal(outgoing.hostname, 'wa.me'); assert.equal(outgoing.pathname, '/' + number);
        assert.match(outgoing.searchParams.get('text'), /^¡Hola, Efy Seguros! 🩷💙/);
        assert.match(outgoing.searchParams.get('text'), /Ramo: Seguro de hogar/);
      }
      await page.locator('#quote-back').click();
      assert.equal(await page.locator('#quote-goal').inputValue(), 'Comparar mi seguro actual');
      await page.locator('#quote-back').click();
      await page.locator('#quote-branch').selectOption('pymes');
      await page.locator('#quote-next').click(); await page.locator('#quote-next').click();
      assert.match(await page.locator('#quote-summary').inputValue(), /Ramo: Seguro para pymes/);

      await page.goto(base + prefix + 'index.html');
      await page.locator('.chat-fab').click();
      const quoteShortcut = page.locator('#evia-dialog .chat-business-options a').filter({hasText:'Solicitar asesoría y cotización'});
      assert.equal(new URL(await quoteShortcut.getAttribute('href')).pathname, prefix + 'cotizar.html');
      await page.locator('#close-chat').click();
      await page.locator('.menu-toggle').click();
      assert.deepEqual(await page.locator('.nav-link').allTextContents().then(a => a.map(t => t.trim())), ['Inicio','Servicios','Asistencias','Aliados','Conócenos','Contacto','Ayuda']);
      await page.locator('[aria-label="Desplegar opciones de Ayuda"]').click();
      await page.locator('#nav-preview-ayuda a').filter({hasText:'Centro de ayuda'}).click();
      assert.equal(new URL(page.url()).pathname, prefix + 'ayuda.html');

      await page.locator('.menu-toggle').click();
      await page.locator('[aria-label="Desplegar opciones de Servicios"]').click();
      assert.equal(await page.locator('#nav-preview-servicios a').count(), 5);
      await page.locator('#nav-preview-servicios a').filter({hasText:'Patrimonio y actividad'}).click();
      assert.equal(new URL(page.url()).pathname, prefix + 'servicios.html');
      assert.equal(new URL(page.url()).hash, '#patrimonio-actividad');
      await page.waitForFunction(() => document.querySelector('[data-service-category][aria-pressed=true]')?.dataset.serviceCategory === 'Patrimonio y actividad');
      assert.equal(await page.locator('[data-service-category][aria-pressed=true]').getAttribute('data-service-category'), 'Patrimonio y actividad');

      await page.locator('.menu-toggle').click();
      await page.locator('[aria-label="Desplegar opciones de Asistencias"]').click();
      await page.locator('#nav-preview-asistencia a').filter({hasText:'Consulta de reembolso'}).click();
      await page.waitForLoadState('domcontentloaded');
      assert.equal(await page.locator('#lookup-type').inputValue(), 'reembolso');
      assert.equal(await page.locator('#lookup-cedula').isEnabled(), true);
      assert.equal(await page.locator('#lookup-plate-option').isVisible(), false);

      await page.locator('.menu-toggle').click();
      await page.locator('[aria-label="Desplegar opciones de Asistencias"]').click();
      await page.locator('#nav-preview-asistencia a').filter({hasText:'Consulta de siniestro'}).click();
      await page.waitForLoadState('domcontentloaded');
      assert.equal(await page.locator('#lookup-type').inputValue(), 'vehicular');
      await page.locator('input[name=lookup-method][value=placa]').check();
      assert.equal(await page.locator('#lookup-plate').isEnabled(), true);

      await page.setViewportSize({width:1440,height:1000});
      await page.goto(base + prefix + 'index.html');
      assert.equal(await page.locator('#page-title').innerText(), 'Tu confianza.\nNuestro\ncompromiso.');
      for (const name of ['Servicios','Asistencias','Aliados','Conócenos','Contacto','Ayuda']) {
        const trigger = page.locator(`[aria-label="Desplegar opciones de ${name}"]`);
        await trigger.hover();
        assert.equal(await trigger.getAttribute('aria-expanded'), 'true');
        const id = await trigger.getAttribute('aria-controls');
        assert.equal(await page.locator('#' + id).isVisible(), true);
      }
      await page.locator('[aria-label="Desplegar opciones de Conócenos"]').click();
      assert.equal(await page.locator('#nav-preview-nosotros').isVisible(), true);
      await page.keyboard.press('Escape');
      assert.equal(await page.locator('#nav-preview-nosotros').isVisible(), false);
      assert.equal(await page.locator('[aria-label="Desplegar opciones de Conócenos"]').evaluate(e => e === document.activeElement), true);

      for (const file of ['index.html','cotizar.html','empresas.html','clientes.html','servicios.html','nosotros.html','contactos.html','asistencia.html','coberturas-cooperativas.html','resenas.html','ayuda.html','consultas.html','reportar-siniestro.html']) {
        for (const width of [320,390,1440]) {
          await page.setViewportSize({width,height:900});
          await page.goto(base + prefix + file); await page.evaluate(() => document.fonts.ready);
          const typography = await page.evaluate(() => ({
            body: getComputedStyle(document.body).fontFamily,
            heading: getComputedStyle(document.querySelector('h1')).fontWeight,
            label: (() => {
              const style = getComputedStyle(document.querySelector('.eyebrow'));
              return {family:style.fontFamily,weight:style.fontWeight,size:parseFloat(style.fontSize),spacing:style.letterSpacing};
            })(),
            overflow: document.documentElement.scrollWidth > innerWidth + 1,
          }));
          assert.match(typography.body, /IBM Plex Sans/); assert.equal(typography.heading,'600');
          assert.match(typography.label.family, /IBM Plex Sans/);
          assert.equal(typography.label.weight, '600');
          assert.ok(typography.label.size >= 13, `Section label too small: ${prefix}${file}`);
          assert.match(typography.label.spacing, /^(normal|0px)$/);
          assert.equal(typography.overflow, false, `${prefix}${file} ${width}px overflows`);
          tested++;
        }
      }
    }
    for (const prefix of ['/', '/nueva/']) {
     for (const width of [390,1440]) {
      const animated = await browser.newContext({viewport:{width,height:1000}});
      const animationPage = await animated.newPage();
      await animationPage.goto(base + prefix + 'index.html');
      await animationPage.waitForFunction(() => document.querySelector('.scene-video')?.currentTime > 0);
      assert.equal(new URL(await animationPage.locator('.scene-video').getAttribute('src')).pathname,
        width <= 760 ? '/assets/evia-interacciones-mobile-20261029.mp4' : '/assets/evia-interacciones-20261029.mp4');
      const media = await animationPage.locator('.scene-video').evaluate(e => ({width:e.videoWidth,duration:e.duration}));
      assert.equal(media.width, width <= 760 ? 720 : 1280);
      assert.equal(media.duration, 11.5);
      assert.equal(await animationPage.locator('.scene').evaluate(e => e.classList.contains('is-playing')), true);
      await animationPage.locator('.premium-home .about-section').scrollIntoViewIfNeeded();
      await animationPage.waitForFunction(() => document.querySelector('.scene-video').paused);
      await animated.close();
     }
    }

    const fallback = await browser.newContext({viewport:{width:390,height:844}});
    await fallback.route('**/*.mp4', route => route.abort());
    const fallbackPage = await fallback.newPage();
    await fallbackPage.goto(base + '/');
    await fallbackPage.waitForFunction(() => document.querySelector('.scene-video')?.error);
    assert.equal(await fallbackPage.locator('.scene-poster').isVisible(), true);
    assert.equal(await fallbackPage.locator('.scene').evaluate(e => e.classList.contains('is-playing')), false);
    await fallback.close();
    await page.goto(base + '/cotizar.html');
    const cdp = await context.newCDPSession(page);
    await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
    const document = await cdp.send('DOM.getDocument');
    const fonts = [];
    for (const selector of ['h1','.quote-guide>p:not(.eyebrow)','#quote-next','.quote-intro .eyebrow']) {
      const {nodeId} = await cdp.send('DOM.querySelector',{nodeId:document.root.nodeId,selector});
      const rendered = await cdp.send('CSS.getPlatformFontsForNode',{nodeId});
      assert.ok(rendered.fonts.some(f => f.isCustomFont && /IBM Plex Sans/.test(f.familyName)), `Actual IBM font missing for ${selector}`);
      fonts.push({selector,fonts:rendered.fonts.map(f=>({family:f.familyName,postscript:f.postScriptName,custom:f.isCustomFont}))});
    }
    await fs.mkdir(path.resolve(__dirname,'../../output/playwright'),{recursive:true});
    await page.setViewportSize({width:1440,height:1000}); await page.goto(base + '/index.html');
    await page.screenshot({path:path.resolve(__dirname,'../../output/playwright/guided-home-desktop.png'),fullPage:true});
    await page.setViewportSize({width:390,height:844}); await page.goto(base + '/index.html');
    await page.screenshot({path:path.resolve(__dirname,'../../output/playwright/guided-home-mobile.png'),fullPage:true});
    await page.goto(base + '/cotizar.html?ramo=hogar'); await page.locator('#quote-next').click();
    assert.equal(await page.evaluate(() => document.activeElement.tagName), 'LEGEND');
    await page.evaluate(() => window.scrollTo({top:0,behavior:'instant'}));
    await page.screenshot({path:path.resolve(__dirname,'../../output/playwright/guided-quote-mobile.png'),fullPage:true});
    assert.deepEqual(errors, []);
    console.log(JSON.stringify({ok:true,views:tested,actualFonts:fonts}));
  } finally { await browser?.close(); server.close(); }
})().catch(error => {console.error(error);process.exitCode=1;});
