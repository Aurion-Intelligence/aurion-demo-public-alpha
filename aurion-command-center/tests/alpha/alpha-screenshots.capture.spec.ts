/**
 * alpha-screenshots.capture.spec.ts
 * [alpha-screenshot-capture-001]
 *
 * Captures the Demo Public Alpha screenshot set by rendering the REAL Command
 * Center UI against deterministic seeded fixtures built from the genuine
 * PUBLIC-SPINE-DEMO-LOOP-001 Mission Receipt.
 *
 * Honesty:
 *  - The UI is the real app (AlphaCockpit, MissionReceiptsView, cockpit components).
 *  - Mission-receipt data is the actual demo receipt (see build_screenshot_fixtures.py).
 *  - Other API calls return honest empty-but-valid responses → honest empty states.
 *  - These are demo, fixture-backed screenshots — NOT full-stack production screenshots.
 *
 * Run via scripts/alpha/capture_screenshots.sh (handles vite + fixtures + this spec).
 */

import { test, type Page, type Route } from '@playwright/test';
import { resolve } from 'path';
import { readFileSync, mkdirSync } from 'fs';

const REPO_ROOT = resolve(__dirname, '..', '..', '..');
const FIXTURE_DIR = resolve(__dirname, '..', 'fixtures', 'alpha-screenshots');
const OUT_DIR = resolve(REPO_ROOT, 'docs', 'alpha', 'screenshots');

const DEMO_RECEIPT_ID = 'rcpt-demo-PUBLIC-SPINE-DEMO-LOOP-001';

const listFixture = readFileSync(resolve(FIXTURE_DIR, 'mission-receipts.list.json'), 'utf-8');
const detailFixture = readFileSync(resolve(FIXTURE_DIR, 'mission-receipt.detail.json'), 'utf-8');

function jsonRoute(route: Route, body: string) {
  return route.fulfill({ status: 200, contentType: 'application/json', body });
}

// The Command Center resolves backend calls to this origin (apiBase.ts default).
// We scope ALL interception to this origin so we never intercept Vite-served source
// modules (which contain "/src/api/..." in their path) — those must pass through.
const BACKEND = 'http://127.0.0.1:8000';

/** Wire up deterministic API interception for every Command Center backend call.
 *
 * NOTE: Playwright matches routes in REVERSE registration order (most recent
 * first), so the broad catch-all is registered FIRST and the specific routes
 * LAST — specific handlers therefore win. */
async function seedApi(page: Page) {
  // Catch-all (registered first → lowest priority): any backend GET returns an
  // honest empty-but-valid object so the shell renders honest empty states, never a
  // network error. Scoped to the backend origin only.
  await page.route(`${BACKEND}/api/**`, (route) => {
    if (route.request().method() !== 'GET') return route.continue();
    return jsonRoute(route, JSON.stringify({ ok: true, items: [], count: 0, warnings: [], note: '' }));
  });

  // Honest empty-but-valid responses for the cockpit's specific list calls.
  const empties: Record<string, string> = {
    [`${BACKEND}/api/missions**`]: JSON.stringify({ ok: true, items: [], count: 0, warnings: [], note: '' }),
    [`${BACKEND}/api/approval/proposals**`]: JSON.stringify({ ok: true, proposals: [], count: 0, warnings: [], note: '' }),
    [`${BACKEND}/api/sandbox-longrun/latest-summary**`]: JSON.stringify({ ok: false, error: 'No sandbox long-run in demo mode.' }),
  };
  for (const [glob, body] of Object.entries(empties)) {
    await page.route(glob, (route) => jsonRoute(route, body));
  }

  // Mission receipts — list vs detail by URL.
  await page.route(`${BACKEND}/api/mission-receipts**`, (route) => {
    const isDetail = /\/api\/mission-receipts\/[^?]+/.test(new URL(route.request().url()).pathname);
    return jsonRoute(route, isDetail ? detailFixture : listFixture);
  });

  // System truth drives the nav module-status gating (NavV2.getModuleStatus →
  // truth.modules.find). Empty modules → every module renders "ready" (honest default).
  await page.route(`${BACKEND}/api/system/truth**`, (route) =>
    jsonRoute(route, JSON.stringify({
      generated_at: '', build: {}, env: {}, modules: [], capabilities: {},
      config_health: { ok: true, errors: [], warnings: [] }, flags: {}, env_snapshot: {},
    })));

  // Boot handshake probes (registered last → highest priority) — must succeed for
  // the app to leave the "Backend Offline" gate (App.tsx → performBackendHandshake).
  await page.route(`${BACKEND}/api/system/health**`, (route) =>
    jsonRoute(route, JSON.stringify({ status: 'ok', ok: true })));
  await page.route(`${BACKEND}/api/version**`, (route) =>
    jsonRoute(route, JSON.stringify({ api_version: 'demo', ok: true })));
  await page.route(`${BACKEND}/api/system/routes**`, (route) =>
    jsonRoute(route, JSON.stringify({ routers: [], ok: true })));
}

test.beforeAll(() => {
  mkdirSync(OUT_DIR, { recursive: true });
});

test.beforeEach(async ({ page }) => {
  await seedApi(page);
  await page.setViewportSize({ width: 1440, height: 900 });
});

/** Navigate and wait for the real app to mount (past the backend handshake gate). */
async function gotoReady(page: Page, path: string) {
  await page.goto(path);
  await page.waitForFunction(() => (window as unknown as { __CC_READY__?: boolean }).__CC_READY__ === true, null, { timeout: 15000 }).catch(() => undefined);
  await page.waitForLoadState('networkidle').catch(() => undefined);
  await page.waitForTimeout(900);
}

/** Open the public-spine demo receipt detail by clicking its row in the list
 * (deep-link param is `receipt_id`; clicking is the most authentic path). */
async function openDemoReceiptDetail(page: Page) {
  await gotoReady(page, `/mission-receipts?receipt_id=${DEMO_RECEIPT_ID}`);
  const row = page.locator('text=/Public Spine Demo Loop/i').first();
  if (await row.count()) {
    await row.click().catch(() => undefined);
    await page.waitForTimeout(700);
  }
}

test.describe('Alpha screenshot capture [alpha-screenshot-capture-001]', () => {
  test('01 — command center shell (mission control cockpit)', async ({ page }) => {
    await gotoReady(page, '/mission-control');
    await page.screenshot({ path: resolve(OUT_DIR, '01-command-center-shell.png'), fullPage: true });
  });

  test('02 — mission receipts list (public spine demo receipt)', async ({ page }) => {
    await gotoReady(page, '/mission-receipts');
    await page.screenshot({ path: resolve(OUT_DIR, '02-mission-receipts-list.png'), fullPage: true });
  });

  test('03 — public spine demo receipt detail', async ({ page }) => {
    await openDemoReceiptDetail(page);
    await page.screenshot({ path: resolve(OUT_DIR, '03-public-spine-demo-receipt-detail.png'), fullPage: true });
  });

  test('04 — demo governance evidence (permission / audit / blackbox / cost)', async ({ page }) => {
    await openDemoReceiptDetail(page);
    // Scroll the detail panel down to the Permissions / Audit Trail / Decision Trace
    // (BlackBox) evidence region so this shot differs from the top-of-detail shot.
    const target = page.getByText(/Audit Trail refs|Decision Trace refs|Permissions/i).last();
    if (await target.count()) {
      await target.scrollIntoViewIfNeeded().catch(() => undefined);
      await page.waitForTimeout(400);
    }
    // Viewport shot (not full-page) so the scrolled-to governance/evidence region is
    // framed, distinct from the top-of-detail full-page shot (03).
    await page.screenshot({ path: resolve(OUT_DIR, '04-demo-governance-evidence.png') });
  });

  test('05 — alpha status / cockpit status surface', async ({ page }) => {
    await gotoReady(page, '/mission-control');
    const status = page.locator('text=/alpha|status|readiness|known issue/i').first();
    if (await status.count()) {
      await status.scrollIntoViewIfNeeded().catch(() => undefined);
      await page.waitForTimeout(300);
    }
    await page.screenshot({ path: resolve(OUT_DIR, '05-alpha-status.png'), fullPage: true });
  });
});
