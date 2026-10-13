/* Run: node tests/ui/services.spec.cjs
 * Optional: PLAYWRIGHT_MODULE, CHROMIUM_PATH, UI_BASE_URL.
 * Checks the real catalogue and its media without opening external links.
 */
const assert = require('node:assert/strict');
const { spawn } = require('node:child_process');
const { once } = require('node:events');
const net = require('node:net');
const path = require('node:path');
const playwright = require(process.env.PLAYWRIGHT_MODULE
  || '/workspace/tools/EFY-SKILLS-COMPLETAS-2026-10-09/runtimes/playwright/node_modules/playwright-core');

async function localServer() {
  const socket = net.createServer();
  socket.listen(0, '127.0.0.1');
  await once(socket, 'listening');
  const port = socket.address().port;
  await new Promise(resolve => socket.close(resolve));
  const server = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', 'public'], {
    cwd: path.resolve(__dirname, '../..'), stdio: 'ignore'
  });
  let startupError;
  server.once('error', error => { startupError = error; });
  const base = 'http://127.0.0.1:' + port;
  for (let attempt = 0; attempt < 100; attempt++) {
    if (startupError || server.exitCode !== null) {
      server.kill();
      throw startupError || Error('Local test server exited.');
    }
    try { await fetch(base); return { base, stop: () => server.kill() }; }
    catch { await new Promise(resolve => setTimeout(resolve, 50)); }
  }
  server.kill();
  throw Error('Local test server did not start.');
}

const counts = { Todas: 16, Movilidad: 4, Salud: 3, 'Vida y bienestar': 3, 'Patrimonio y actividad': 6 };
const anchors = { movilidad: 'Movilidad', salud: 'Salud', 'vida-bienestar': 'Vida y bienestar', 'patrimonio-actividad': 'Patrimonio y actividad' };
const shown = page => page.locator('#service-rail .service-card:not([hidden])');
const scrollLeft = page => page.locator('#service-rail').evaluate(rail => rail.scrollLeft);

async function category(page, name) {
  await page.locator(`[data-service-category="${name}"]`).click();
  await page.waitForFunction(expected => document.querySelectorAll('#service-rail .service-card:not([hidden])').length === expected, counts[name]);
  assert.equal(await page.locator(`[data-service-category="${name}"]`).getAttribute('aria-pressed'), 'true');
  assert.equal(await page.locator('[data-service-category][aria-pressed="true"]').count(), 1);
  await page.waitForFunction(total => document.querySelector('#service-position').textContent.endsWith(`de ${total} seguros`), counts[name]);
  await page.waitForFunction(() => document.querySelector('#service-prev').disabled);
  assert.equal(await page.locator('#service-prev').isDisabled(), true);
  assert.equal(await shown(page).count(), counts[name]);
}

(async () => {
  let server;
  let browser;
  try {
    server = process.env.UI_BASE_URL ? { base: process.env.UI_BASE_URL, stop() {} } : await localServer();
    browser = await playwright.chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', headless: true, args: ['--no-sandbox'] });
    for (const route of ['/servicios.html', '/nueva/servicios.html']) {
      for (const width of [320, 390, 1440]) {
        const context = await browser.newContext({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
        const page = await context.newPage();
        const errors = [];
        page.on('pageerror', error => errors.push(error.message));
        await page.goto(server.base + route, { waitUntil: 'networkidle' });
        const rail = page.locator('#service-rail');
        assert.equal(await shown(page).count(), 16);
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
        assert.equal(await rail.getAttribute('role'), 'region');
        assert.equal(await rail.getAttribute('aria-roledescription'), 'carrusel');
        assert.equal(await page.locator('#service-prev').isDisabled(), true);
        assert.equal(await page.locator('#service-next').isEnabled(), true);
        const initialPosition = await page.locator('#service-position').textContent();
        await rail.evaluate(element => {
          const original = element.scrollTo.bind(element);
          element.scrollTo = options => { window.lastServiceScroll = options; return original(options); };
        });
        await page.locator('#service-next').click();
        await page.waitForFunction(() => document.querySelector('#service-rail').scrollLeft > 1);
        assert.equal(await page.evaluate(() => window.lastServiceScroll.behavior), 'instant');
        await page.waitForFunction(initial => document.querySelector('#service-position').textContent !== initial, initialPosition);
        assert.equal(await page.locator('#service-prev').isEnabled(), true);
        await page.locator('#service-prev').click();
        await page.waitForFunction(() => document.querySelector('#service-rail').scrollLeft <= 1);
        await rail.evaluate(element => element.scrollBy({ left: element.clientWidth * .8, behavior: 'instant' }));
        await page.waitForFunction(() => document.querySelector('#service-rail').scrollLeft > 1);
        await page.waitForFunction(initial => document.querySelector('#service-position').textContent !== initial, initialPosition);

        const initialURL = page.url();
        for (const name of Object.keys(counts)) await category(page, name);
        assert.equal(page.url(), initialURL, 'Filtering should not replace the current URL.');
        await category(page, 'Todas');
        for (let index = 0; index < 16; index++) {
          const card = shown(page).nth(index);
          await card.scrollIntoViewIfNeeded();
          assert.ok(await card.locator('img').count(), 'Each insurance option needs an illustrative image.');
          await card.locator('img').first().evaluate(image => new Promise((resolve, reject) => {
            if (image.complete) { image.naturalWidth ? resolve() : reject(Error('Image failed to load')); return; }
            image.addEventListener('load', resolve, { once: true });
            image.addEventListener('error', () => reject(Error('Image failed to load')), { once: true });
          }));
        }

        for (const [anchor, name] of Object.entries(anchors)) {
          await page.evaluate(id => { location.hash = id; }, anchor);
          await page.waitForFunction(group => document.querySelector(`[data-service-category="${group}"]`).getAttribute('aria-pressed') === 'true', name);
          assert.equal(await shown(page).count(), counts[name]);
        }
        await page.goto(server.base + route + '#seguro-motos', { waitUntil: 'networkidle' });
        assert.equal(await page.locator('[data-service-category="Movilidad"]').getAttribute('aria-pressed'), 'true');
        const targetInView = await page.locator('#seguro-motos').evaluate(card => {
          const item = card.getBoundingClientRect();
          const rail = document.querySelector('#service-rail').getBoundingClientRect();
          return item.left < rail.right && item.right > rail.left;
        });
        assert.equal(targetInView, true, 'A direct insurance link should reveal that insurance.');
        await page.locator('#seguro-motos summary').click();
        assert.equal(await page.locator('#seguro-motos details').evaluate(details => details.open), true);
        const beforeChildKey = await scrollLeft(page);
        await page.locator('#seguro-motos summary').focus();
        await page.keyboard.press('ArrowRight');
        assert.equal(await scrollLeft(page), beforeChildKey, 'The rail must not intercept keys used by its children.');
        await rail.focus();
        await page.keyboard.press('Home');
        await page.waitForFunction(() => document.querySelector('#service-rail').scrollLeft <= 1);
        await page.keyboard.press('ArrowRight');
        await page.waitForFunction(() => document.querySelector('#service-rail').scrollLeft > 1);
        await page.keyboard.press('End');
        await page.waitForFunction(() => {
          const rail = document.querySelector('#service-rail');
          return rail.scrollLeft >= rail.scrollWidth - rail.clientWidth - 1;
        });
        await page.waitForFunction(() => document.querySelector('#service-next').disabled);
        await page.keyboard.press('Home');
        await page.waitForFunction(() => document.querySelector('#service-prev').disabled);
        await page.setViewportSize({ width: 390, height: 900 });
        await page.waitForFunction(() => document.querySelector('#service-next').disabled === false);
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
        assert.deepEqual(errors, []);
        console.log(`PASS ${route} at ${width} px: manual scrolling, 16 images, categories, legacy links, disclosures, keyboard, reduced motion.`);
        await context.close();
      }
    }
    const context = await browser.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: 'no-preference' });
    const page = await context.newPage();
    await page.goto(server.base + '/servicios.html', { waitUntil: 'networkidle' });
    await page.locator('#service-rail').evaluate(element => {
      const original = element.scrollTo.bind(element);
      element.scrollTo = options => { window.lastServiceScroll = options; return original(options); };
    });
    await page.locator('#service-next').click();
    assert.equal(await page.evaluate(() => window.lastServiceScroll.behavior), 'smooth');
    await page.waitForFunction(() => document.querySelector('#service-rail').scrollLeft > 1);
    console.log('PASS standard motion: navigation requests a smooth manual transition.');
    await context.close();
  } finally {
    if (browser) await browser.close();
    if (server) server.stop();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
