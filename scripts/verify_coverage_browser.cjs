/* Verify the published coverage form with one documented synthetic lookup.
 * No customer identifiers, credentials, response bodies, or screenshots are logged.
 * Optional local fixture: EFY_COVERAGE_VERIFY_URL=http://127.0.0.1:PORT/coberturas-cooperativas.html
 * Dependencies: PLAYWRIGHT_MODULE (playwright-core path) and optional CHROMIUM_PATH.
 */
'use strict';

const fs = require('node:fs');

const productionUrl = 'https://www.efyseguros.com/coberturas-cooperativas.html';
const allowedPaths = new Set(['/coberturas-cooperativas.html', '/nueva/coberturas-cooperativas.html']);
let stage = 'setup';

function fail(code) {
  const error = new Error(code);
  error.verificationCode = code;
  throw error;
}

function targetUrl() {
  const override = process.env.EFY_COVERAGE_VERIFY_URL;
  if (!override) return new URL(productionUrl);
  let target;
  try { target = new URL(override); } catch { fail('INVALID_LOCAL_TARGET'); }
  if (!['localhost', '127.0.0.1'].includes(target.hostname) ||
      target.protocol !== 'http:' || target.username || target.password ||
      target.search || target.hash || !allowedPaths.has(target.pathname)) {
    fail('INVALID_LOCAL_TARGET');
  }
  return target;
}

function executable() {
  if (process.env.CHROMIUM_PATH) return process.env.CHROMIUM_PATH;
  const installed = ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium']
    .find(candidate => fs.existsSync(candidate));
  if (!installed) fail('BROWSER_UNAVAILABLE');
  return installed;
}

function logStatus(label, response) {
  const status = response?.status();
  console.log(`coverage-browser stage=${label} http=${Number.isInteger(status) ? status : 0}`);
  return status;
}

async function json(response) {
  try { return await response.json(); } catch { fail('INVALID_JSON'); }
}

async function verify() {
  const target = targetUrl();
  let playwright;
  try { playwright = require(process.env.PLAYWRIGHT_MODULE || 'playwright-core'); }
  catch { fail('PLAYWRIGHT_UNAVAILABLE'); }
  let browser;
  let timedOut = false;
  // Bound the complete run, including launch, network waits, and cleanup.
  const deadline = setTimeout(() => {
    timedOut = true;
    console.error(`coverage-browser stage=${stage} error=DEADLINE_EXCEEDED`);
    process.exit(1);
  }, 55000);
  try {
    stage = 'launch';
    browser = await playwright.chromium.launch({
      executablePath: executable(), headless: true, timeout: 10000,
      args: ['--no-sandbox']
    });
    const context = await browser.newContext({ viewport: { width: 1280, height: 960 }, reducedMotion: 'reduce' });
    const page = await context.newPage();
    page.setDefaultTimeout(8000);
    page.setDefaultNavigationTimeout(20000);
    const isEndpoint = (response, method) => {
      const responseUrl = new URL(response.url());
      return responseUrl.origin === target.origin && responseUrl.pathname === '/nueva/api/coberturas.php' &&
        !responseUrl.search && response.request().method() === method;
    };

    stage = 'page';
    const [, configuration] = await Promise.all([
      page.goto(target.href, { waitUntil: 'domcontentloaded' }).then(navigation => {
        if (logStatus('page', navigation) !== 200) fail('PAGE_HTTP_ERROR');
        const current = new URL(page.url());
        if (current.origin !== target.origin || current.pathname !== target.pathname) fail('UNEXPECTED_REDIRECT');
      }),
      page.waitForResponse(response => isEndpoint(response, 'GET'), { timeout: 25000 })
    ]);

    stage = 'configuration';
    if (logStatus('configuration', configuration) !== 200) fail('CONFIGURATION_HTTP_ERROR');
    const config = await json(configuration);
    if (config?.ok !== true || config.ready !== true || typeof config.csrf !== 'string' || !config.csrf) {
      fail('CONFIGURATION_NOT_READY');
    }

    stage = 'form';
    await page.locator('#coverage-cooperative').selectOption('coopartamos');
    stage = 'branding';
    const logosLoaded = await page.evaluate(async () => {
      const config = JSON.parse(document.querySelector('#coverage-branding').textContent);
      const urls = [config.cooperativa.logo, ...Object.values(config.aseguradoras).map(item => item.logo)];
      return Promise.all(urls.map(src => new Promise(resolve => {
        const img = new Image();
        const timer = setTimeout(() => resolve(false), 10000);
        img.referrerPolicy = 'no-referrer';
        img.onload = () => { clearTimeout(timer); resolve(img.naturalWidth > 0); };
        img.onerror = () => { clearTimeout(timer); resolve(false); };
        img.src = src;
      })));
    });
    if (!logosLoaded.every(Boolean)) fail('BRAND_LOGO_UNAVAILABLE');
    console.log('coverage-browser stage=branding result=ok');
    stage = 'form';
    await page.locator('#coverage-confirm').check();
    await page.locator('#coverage-cedula').fill('0000000001');
    await page.locator('#coverage-consent').check();

    stage = 'lookup';
    const [lookup] = await Promise.all([
      page.waitForResponse(response => isEndpoint(response, 'POST'), { timeout: 25000 }),
      page.locator('#coverage-submit').click()
    ]);
    if (logStatus('lookup', lookup) !== 200) {
      const allowedReasons = new Set([
        'UPSTREAM_AUTHENTICATION', 'UPSTREAM_ACCESS_DENIED', 'UPSTREAM_UNAVAILABLE', 'UPSTREAM_RATE_LIMITED',
        'UPSTREAM_HTTP_ERROR', 'UPSTREAM_TIMEOUT', 'UPSTREAM_TLS_ERROR',
        'UPSTREAM_CONNECTION_ERROR', 'UPSTREAM_RESPONSE_INVALID', 'PROXY_UNAVAILABLE'
      ]);
      let reason = 'UNKNOWN';
      try {
        const errorResult = await lookup.json();
        if (allowedReasons.has(errorResult?.unavailable_reason)) reason = errorResult.unavailable_reason;
      } catch { /* An HTML or unreadable error remains an HTTP failure. */ }
      console.log(`coverage-browser stage=lookup reason=${reason}`);
      fail('LOOKUP_HTTP_ERROR');
    }
    const result = await json(lookup);
    if (result?.ok !== true || typeof result.encontrado !== 'boolean' || !Array.isArray(result.registros) ||
        result.encontrado !== (result.registros.length > 0)) {
      fail('INVALID_LOOKUP_RESULT');
    }

    stage = 'result';
    await page.locator('#coverage-results').waitFor({ state: 'visible' });
    await page.waitForFunction(() =>
      document.querySelector('#coverage-status')?.textContent.trim() === 'Consulta completada.',
    null, { timeout: 8000 });
    if (!(await page.locator('#coverage-summary').textContent())?.trim()) fail('RESULT_SUMMARY_MISSING');
    if (await page.locator('#coverage-records .coverage-record').count() !== result.registros.length) {
      fail('RESULT_COUNT_MISMATCH');
    }
    console.log('coverage-browser stage=completed result=ok');
  } finally {
    if (browser) await browser.close().catch(() => {});
    if (!timedOut) clearTimeout(deadline);
  }
}

verify().catch(error => {
  const known = new Set([
    'INVALID_LOCAL_TARGET', 'BROWSER_UNAVAILABLE', 'PLAYWRIGHT_UNAVAILABLE', 'INVALID_JSON',
    'PAGE_HTTP_ERROR', 'UNEXPECTED_REDIRECT', 'CONFIGURATION_HTTP_ERROR', 'CONFIGURATION_NOT_READY',
    'LOOKUP_HTTP_ERROR', 'INVALID_LOOKUP_RESULT', 'RESULT_SUMMARY_MISSING', 'RESULT_COUNT_MISMATCH', 'BRAND_LOGO_UNAVAILABLE'
  ]);
  const code = known.has(error?.verificationCode) ? error.verificationCode :
    error?.name === 'TimeoutError' ? 'STAGE_TIMEOUT' : 'VERIFICATION_FAILED';
  console.error(`coverage-browser stage=${stage} error=${code}`);
  process.exitCode = 1;
});
