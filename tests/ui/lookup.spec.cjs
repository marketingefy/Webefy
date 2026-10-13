/* Run with node tests/ui/lookup.spec.cjs. Uses a local static server by default.
 * Override PLAYWRIGHT_MODULE, CHROMIUM_PATH or UI_BASE_URL when needed.
 * All identifiers are synthetic. The test never opens mailto links or sends mail.
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
    try {
      await fetch(base);
      return { base, stop: () => server.kill() };
    } catch {
      await new Promise(resolve => setTimeout(resolve, 50));
    }
  }
  server.kill();
  throw Error('Local test server did not start.');
}

async function prepare(page) {
  await page.locator('#lookup-form button[type="submit"]').click();
}

async function checkDraft(page, topic, identifier, method) {
  await page.locator('#lookup-result').waitFor({ state: 'visible' });
  const text = await page.locator('#lookup-summary').inputValue();
  assert.ok(text.includes(topic));
  assert.ok(text.includes(method + ': ' + identifier));
  const link = new URL(await page.locator('#lookup-email').getAttribute('href'));
  assert.equal(link.protocol, 'mailto:');
  assert.equal(link.pathname, 'siniestros@efyseguros.com');
  assert.equal(link.searchParams.get('body'), text);
  assert.ok(link.searchParams.get('subject').includes(topic));
}

(async () => {
  let server;
  let browser;
  try {
    server = process.env.UI_BASE_URL ? { base: process.env.UI_BASE_URL, stop() {} } : await localServer();
    browser = await playwright.chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', headless: true, args: ['--no-sandbox'] });
    for (const route of ['/consultas.html', '/nueva/consultas.html']) {
      for (const width of [320, 390, 1440]) {
        const context = await browser.newContext({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
        const page = await context.newPage();
        const errors = [];
        const requests = [];
        page.on('pageerror', error => errors.push(error.message));
        page.on('request', request => requests.push({ url: request.url(), type: request.resourceType() }));
        await page.goto(server.base + route, { waitUntil: 'networkidle' });
        const initialURL = page.url();
        const initialRequests = requests.length;
        const storageBefore = await page.evaluate(() => ({ local: { ...localStorage }, session: { ...sessionStorage } }));

        assert.equal(await page.locator('#lookup-cedula').isEnabled(), true);
        await page.locator('#lookup-cedula').fill('0102030405');
        await prepare(page);
        await checkDraft(page, 'siniestro vehicular', '0102030405', 'Cédula');
        await page.locator('#lookup-cedula').fill('01234');
        assert.equal(await page.locator('#lookup-result').isHidden(), true);
        await prepare(page);
        assert.equal(await page.locator('#lookup-cedula').evaluate(el => el.validity.patternMismatch), true);
        assert.equal(await page.locator('#lookup-cedula').evaluate(el => el === document.activeElement), true);
        assert.equal(await page.locator('#lookup-result').isHidden(), true);

        await page.locator('input[name="lookup-method"][value="placa"]').check();
        assert.equal(await page.locator('#lookup-cedula').isDisabled(), true);
        assert.equal(await page.locator('#lookup-cedula').evaluate(el => el.required), false);
        assert.equal(await page.locator('#lookup-plate').isEnabled(), true);
        for (const invalid of ['12345', 'ABCDE', 'AB*123', 'AB1234567', '-----', '     ']) {
          await page.locator('#lookup-plate').fill(invalid);
          await prepare(page);
          assert.equal(await page.locator('#lookup-plate').evaluate(el => el.validity.customError), true);
          assert.equal(await page.locator('#lookup-result').isHidden(), true);
        }
        await page.locator('#lookup-plate').fill('abc-1234');
        await prepare(page);
        assert.equal(await page.locator('#lookup-plate').inputValue(), 'ABC1234');
        await checkDraft(page, 'siniestro vehicular', 'ABC1234', 'Placa del vehículo');
        assert.equal((await page.locator('#lookup-summary').inputValue()).includes('0102030405'), false);

        await page.locator('#lookup-type').selectOption('reembolso');
        assert.equal(await page.locator('#lookup-plate-option').isHidden(), true);
        assert.equal(await page.locator('#lookup-plate').isDisabled(), true);
        assert.equal(await page.locator('#lookup-plate').evaluate(el => el.required), false);
        assert.equal(await page.locator('#lookup-cedula').isEnabled(), true);
        assert.equal(await page.locator('#lookup-result').isHidden(), true);
        await page.locator('#lookup-cedula').fill('0102030405');
        await prepare(page);
        await checkDraft(page, 'reembolso', '0102030405', 'Cédula');
        await page.locator('#lookup-type').selectOption('siniestro');
        await prepare(page);
        await checkDraft(page, 'otro siniestro', '0102030405', 'Cédula');

        assert.equal(page.url(), initialURL);
        assert.deepEqual(await page.evaluate(() => ({ local: { ...localStorage }, session: { ...sessionStorage } })), storageBefore);
        assert.deepEqual(requests.slice(initialRequests), [], 'Preparing a draft must make no network request.');
        assert.deepEqual(errors, []);
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth), false);
        console.log('PASS ' + route + ' at ' + width + ' px: editable inputs, validation, type switching, local draft, no network or storage.');
        await context.close();
      }
    }
  } finally {
    if (browser) await browser.close();
    if (server) server.stop();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
