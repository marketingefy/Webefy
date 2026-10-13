// Run with Node against the local static server; this suite never visits production.
// Optional environment: UI_BASE_URL, PLAYWRIGHT_MODULE, CHROMIUM_PATH.
const assert = require('node:assert/strict');
const fs = require('node:fs');

let playwright;
try {
  playwright = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
} catch (error) {
  if (process.env.PLAYWRIGHT_MODULE) throw error;
  playwright = require('/workspace/tools/EFY-SKILLS-COMPLETAS-2026-10-09/runtimes/playwright/node_modules/playwright-core');
}

const base = new URL(process.env.UI_BASE_URL || 'http://127.0.0.1:8080/');
assert(['localhost', '127.0.0.1', '[::1]'].includes(base.hostname), 'UI_BASE_URL must use a local server.');
const executablePath = process.env.CHROMIUM_PATH || (fs.existsSync('/usr/bin/chromium') ? '/usr/bin/chromium' : undefined);
let passed = 0;

async function check(name, callback) {
  await callback();
  passed += 1;
  console.log(`PASS ${name}`);
}

async function localContext(browser, options) {
  const context = await browser.newContext(options);
  await context.route('**/*', route => {
    if (new URL(route.request().url()).origin === base.origin) return route.continue();
    return route.abort();
  });
  return context;
}

async function expanded(page, index, value) {
  await page.waitForFunction(({ index, value }) => {
    const link = document.querySelectorAll('#site-nav .nav-link')[index];
    const panel = link && document.getElementById(link.getAttribute('aria-controls'));
    return link?.getAttribute('aria-expanded') === String(value) && panel?.hidden === !value;
  }, { index, value });
}

(async () => {
  const browser = await playwright.chromium.launch({ executablePath, headless: true });
  try {
    const desktop = await localContext(browser, { viewport: { width: 1440, height: 900 } });
    const page = await desktop.newPage();
    await page.goto(base.href, { waitUntil: 'domcontentloaded' });
    const links = page.locator('#site-nav .nav-link');
    assert(await links.count() >= 2, 'At least two preview-enabled navigation items are required.');

    await check('Desktop hover shows one preview and permits movement into its panel', async () => {
      await links.nth(0).hover();
      await expanded(page, 0, true);
      const panelId = await links.nth(0).getAttribute('aria-controls');
      const panel = page.locator(`#${panelId}`);
      const bounds = await panel.boundingBox();
      assert(bounds, 'An open preview has a visible box.');
      await page.mouse.move(bounds.x + Math.min(30, bounds.width / 2), bounds.y + Math.min(30, bounds.height / 2));
      await page.waitForTimeout(150);
      await expanded(page, 0, true);
      await links.nth(1).hover();
      await expanded(page, 0, false);
      await expanded(page, 1, true);
      assert.equal(await page.locator('#site-nav .nav-link[aria-expanded="true"]').count(), 1);
    });

    await check('Leaving the navigation closes the preview after its pointer bridge', async () => {
      await page.mouse.move(5, 850);
      await expanded(page, 1, false);
    });

    await check('Keyboard focus reaches preview links and Escape restores the original trigger', async () => {
      await links.nth(0).focus();
      await expanded(page, 0, true);
      await page.keyboard.press('Tab');
      assert(await page.evaluate(() => {
        const link = document.querySelector('#site-nav .nav-link[aria-expanded="true"]');
        return document.getElementById(link.getAttribute('aria-controls')).contains(document.activeElement);
      }), 'Tab reaches a link inside the preview.');
      await page.keyboard.press('Escape');
      await expanded(page, 0, false);
      await page.waitForTimeout(150);
      assert(await links.nth(0).evaluate(link => link === document.activeElement));
      await expanded(page, 0, false);
    });

    await check('Focus moving outside and clicking outside both dismiss the preview', async () => {
      await links.nth(1).focus();
      await expanded(page, 1, true);
      await page.locator('.brand').focus();
      await expanded(page, 1, false);
      await links.nth(1).hover();
      await expanded(page, 1, true);
      await page.mouse.click(5, 850);
      await expanded(page, 1, false);
    });

    await check('Compact and desktop navigation fit at both sides of the 1180 px breakpoint', async () => {
      await links.nth(0).hover();
      await expanded(page, 0, true);
      for (const width of [900, 1101, 1180]) {
        await page.setViewportSize({ width, height: 900 });
        await expanded(page, 0, false);
        assert(await page.locator('.menu-toggle').isVisible(), `The compact menu is available at ${width} px.`);
        await page.locator('.menu-toggle').click();
        await links.nth(0).focus();
        await expanded(page, 0, false);
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `The compact menu fits at ${width} px.`);
        await page.keyboard.press('Escape');
        assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'false');
      }
      for (const width of [1181, 1280, 1440]) {
        await page.setViewportSize({ width, height: 900 });
        assert(!(await page.locator('.menu-toggle').isVisible()), `The desktop navigation is available at ${width} px.`);
        await links.nth(0).hover();
        await expanded(page, 0, true);
        assert(await page.evaluate(() => {
          const link = document.querySelector('#site-nav .nav-link[aria-expanded="true"]');
          const bounds = document.getElementById(link.getAttribute('aria-controls')).getBoundingClientRect();
          return document.documentElement.scrollWidth <= innerWidth && bounds.left >= 0 && bounds.right <= innerWidth;
        }), `The desktop navigation and preview fit at ${width} px.`);
        await page.mouse.move(5, 850);
        await expanded(page, 0, false);
      }
    });

    await check('Preview behavior preserves the main desktop link destination', async () => {
      const destination = new URL(await links.nth(1).getAttribute('href'), page.url()).pathname;
      await links.nth(1).hover();
      await expanded(page, 1, true);
      await links.nth(1).click();
      await page.waitForURL(url => url.pathname === destination);
    });

    await check('The existing EVIA dialog keeps its Escape and return-focus behavior', async () => {
      await page.goto(base.href, { waitUntil: 'domcontentloaded' });
      await page.locator('#site-nav .nav-link').nth(0).hover();
      await expanded(page, 0, true);
      await page.locator('.chat-fab').click();
      await expanded(page, 0, false);
      await page.waitForFunction(() => document.querySelector('#evia-dialog').open);
      await page.keyboard.press('Escape');
      await page.waitForFunction(() => !document.querySelector('#evia-dialog').open);
      assert(await page.locator('.chat-fab').evaluate(button => button === document.activeElement));
    });

    const mobile = await localContext(browser, { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
    const touch = await mobile.newPage();
    await touch.goto(base.href, { waitUntil: 'domcontentloaded' });
    await check('Touch navigation reaches the original module without opening a hover preview', async () => {
      await touch.locator('.menu-toggle').tap();
      const link = touch.locator('#site-nav .nav-link').nth(1);
      const destination = new URL(await link.getAttribute('href'), touch.url()).pathname;
      await link.tap();
      await touch.waitForURL(url => url.pathname === destination);
      assert.equal(await touch.locator('#site-nav .nav-link[aria-expanded="true"]').count(), 0);
      assert.equal(await touch.locator('#site-nav .nav-preview:not([hidden])').count(), 0);
    });
    console.log(`Navigation verification passed: ${passed} checks.`);
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
