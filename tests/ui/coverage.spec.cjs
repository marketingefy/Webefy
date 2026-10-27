/* Browser contract checks with a simulated same-origin PHP endpoint.
 * Run: node tests/ui/coverage.spec.cjs
 * All identifiers are synthetic; no request reaches the real API.
 */
const assert = require('node:assert/strict');
const { spawn } = require('node:child_process');
const { once } = require('node:events');
const net = require('node:net');
const path = require('node:path');
const fs = require('node:fs/promises');
const playwright = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

async function localServer() {
  const socket = net.createServer();
  socket.listen(0, '127.0.0.1');
  await once(socket, 'listening');
  const port = socket.address().port;
  await new Promise(resolve => socket.close(resolve));
  const server = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', 'public'], {
    cwd: path.resolve(__dirname, '../..'), stdio: 'ignore'
  });
  const base = 'http://127.0.0.1:' + port;
  for (let attempt = 0; attempt < 100; attempt++) {
    if (server.exitCode !== null) throw Error('Local coverage test server exited');
    try { await fetch(base); return { base, stop: () => server.kill() }; }
    catch { await new Promise(resolve => setTimeout(resolve, 50)); }
  }
  server.kill();
  throw Error('Local coverage test server did not start');
}

const pending = 'La cartera de Privilegio está pendiente de incorporación.';
const listing = 'La vigencia corresponde al listado recibido; no acredita pagos ni cancelaciones posteriores.';
const synthetic = '0000000001';
const match = {
  ok: true, encontrado: true, fecha_consulta: '2026-10-26', fuentes_pendientes: ['PRIVILEGIO'],
  advertencias: [listing, pending],
  registros: [
    { aseguradora: 'PROASSISLIFE', contrato: '<img src=x onerror="window.__injected=true">', vigencia_inicio: '2026-01-01', vigencia_fin: '2027-01-01', estado: 'VIGENTE' },
    { aseguradora: 'PROASSISLIFE', contrato: 'PRUEBA-002', vigencia_inicio: null, vigencia_fin: null, estado: 'VENCIDA' }
  ]
};

async function choose(page) {
  await page.locator('#coverage-cooperative').selectOption('coopartamos');
  assert.equal(await page.locator('#coverage-cooperative-card').isVisible(), true);
  assert.equal(await page.locator('#coverage-cedula').isDisabled(), true);
  await page.locator('#coverage-confirm').check();
  await page.locator('#coverage-cedula').fill(synthetic);
  await page.locator('#coverage-consent').check();
}

(async () => {
  let server;
  let browser;
  try {
    server = await localServer();
    browser = await playwright.chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', headless: true, args: ['--no-sandbox'] });
    for (const pathname of ['/coberturas-cooperativas.html', '/nueva/coberturas-cooperativas.html']) {
      for (const width of [320, 390, 1440]) {
        const context = await browser.newContext({ viewport: { width, height: 1000 }, reducedMotion: 'reduce' });
        const page = await context.newPage();
        let response = { status: 200, data: match };
        let available = true;
        let csrf = 'test-session-1';
        const submissions = [];
        const errors = [];
        const urls = [];
        page.on('pageerror', error => errors.push(error.message));
        page.on('request', request => urls.push(request.url()));
        await page.route('**/nueva/api/coberturas.php', async route => {
          const request = route.request();
          assert.equal(new URL(request.url()).origin, server.base);
          assert.equal(new URL(request.url()).search, '');
          if (request.method() === 'GET') {
            await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, ready: available, csrf }) });
          } else {
            assert.equal(request.method(), 'POST');
            assert.ok(request.headers()['content-type'].startsWith('application/json'));
            submissions.push(request.postDataJSON());
            if (response.abort) await route.abort('failed');
            else await route.fulfill({ status: response.status, contentType: 'application/json', body: JSON.stringify(response.data) });
          }
        });
        await page.goto(server.base + pathname, { waitUntil: 'networkidle' });
        const storage = await page.evaluate(() => ({ local: { ...localStorage }, session: { ...sessionStorage } }));
        const initialUrl = page.url();
        assert.equal(await page.locator('#coverage-cedula').isDisabled(), true);
        assert.match(await page.locator('#coverage-status').textContent(), /disponible/);
        await choose(page);
        await page.locator('#coverage-cedula').fill('12345');
        await page.locator('#coverage-submit').click();
        assert.equal(submissions.length, 0);
        assert.equal(await page.locator('#coverage-cedula').evaluate(el => el.validity.valid), false);
        await page.locator('#coverage-cedula').fill(synthetic);
        await page.locator('#coverage-consent').uncheck();
        await page.locator('#coverage-submit').click();
        assert.equal(submissions.length, 0);
        await page.locator('#coverage-consent').check();
        await page.locator('#coverage-submit').click();
        await page.locator('#coverage-results').waitFor({ state: 'visible' });
        assert.equal(await page.locator('.coverage-record').count(), 2);
        assert.deepEqual(submissions[0], { cooperativa: 'coopartamos', cedula: synthetic, consent: true, csrf });
        assert.match(await page.locator('#coverage-records').textContent(), /vencida/i);
        assert.match(await page.locator('#coverage-records').textContent(), /No informada/);
        assert.equal(await page.locator('#coverage-records img').count(), 0);
        assert.equal(await page.evaluate(() => window.__injected), undefined);
        assert.match(await page.locator('#coverage-query-date').textContent(), /26.*octubre.*2026/);
        assert.match(await page.locator('body').textContent(), /Privilegio.*pendiente/s);
        assert.match(await page.locator('body').textContent(), /no acredita pagos ni cancelaciones posteriores/);
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
        if (pathname === '/coberturas-cooperativas.html' && [390, 1440].includes(width)) {
          await fs.mkdir(path.resolve('output/coverage'), { recursive: true });
          await page.screenshot({ path: path.resolve('output/coverage/coverage-result-' + width + '.png'), fullPage: true });
        }

        await page.locator('#coverage-cedula').fill('0000000002');
        assert.equal(await page.locator('#coverage-results').isHidden(), true);
        response = { status: 200, data: { ...match, encontrado: false, registros: [] } };
        await page.locator('#coverage-submit').click();
        await page.locator('#coverage-results').waitFor({ state: 'visible' });
        assert.match(await page.locator('#coverage-summary').textContent(), /no confirma que no tengas seguro/);
        assert.equal(await page.locator('.coverage-record').count(), 0);

        response = { status: 200, data: { ...match, encontrado: false, registros: [], fuentes_pendientes: [], advertencias: [listing] } };
        await page.locator('#coverage-submit').click();
        await page.locator('#coverage-results').waitFor({ state: 'visible' });
        assert.equal(await page.locator('#coverage-pending').isHidden(), true);
        assert.doesNotMatch(await page.locator('#coverage-summary').textContent(), /pendiente/);

        for (const failure of [
          { status: 502, data: { ok: false, message: 'Error' } },
          { status: 200, data: { ...match, encontrado: false } },
          { status: 429, data: { ok: false } },
          { abort: true }
        ]) {
          response = failure;
          await page.locator('#coverage-submit').click();
          await page.waitForFunction(() => document.querySelector('.coverage-workspace').getAttribute('aria-busy') === 'false');
          assert.equal(await page.locator('#coverage-results').isHidden(), true);
          assert.equal(await page.locator('#coverage-status').evaluate(el => el.classList.contains('is-error')), true);
        }

        response = { status: 419, data: { ok: false } };
        await page.locator('#coverage-submit').click();
        await page.locator('#coverage-retry').waitFor({ state: 'visible' });
        assert.equal(await page.locator('#coverage-submit').isDisabled(), true);
        csrf = 'test-session-2';
        await page.locator('#coverage-retry').click();
        await page.waitForFunction(() => document.querySelector('#coverage-submit').disabled === false);
        response = { status: 200, data: match };
        await page.locator('#coverage-submit').click();
        await page.locator('#coverage-results').waitFor({ state: 'visible' });
        assert.equal(submissions.at(-1).csrf, 'test-session-2');
        await page.locator('#coverage-clear').click();
        assert.equal(await page.locator('#coverage-cedula').inputValue(), '');
        assert.equal(await page.locator('#coverage-results').isHidden(), true);
        assert.equal(page.url(), initialUrl);
        assert.deepEqual(await page.evaluate(() => ({ local: { ...localStorage }, session: { ...sessionStorage } })), storage);
        assert.ok(urls.every(url => !url.includes(synthetic)));
        assert.deepEqual(errors, []);

        available = false;
        await page.reload({ waitUntil: 'networkidle' });
        assert.equal(await page.locator('#coverage-submit').isDisabled(), true);
        assert.equal(await page.locator('#coverage-retry').isVisible(), true);
        console.log('PASS ' + pathname + ' at ' + width + 'px: consent, identifier, results, privacy, errors, retry, no overflow');
        await context.close();
      }
    }
  } finally {
    if (browser) await browser.close();
    if (server) server.stop();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
