// Render a Reel's overlay as transparent PNG frames.
// Usage: node render.js <page.html> <outDir> <seconds> [fps]
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [page, out, secs, fpsArg] = process.argv.slice(2);
  const fps = Number(fpsArg || 30);
  const n = Math.round(Number(secs) * fps);
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  pg.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exitCode = 1; });
  await pg.goto('file://' + path.resolve(page), { waitUntil: 'networkidle' });
  await pg.waitForFunction(() => window.READY === true);
  await pg.evaluate(() => document.fonts.ready);
  await pg.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  for (let i = 0; i < n; i++) {
    await pg.evaluate(t => window.seek(t), i / fps);
    await pg.screenshot({ path: `${out}/${String(i).padStart(5, '0')}.png`, omitBackground: true });
  }
  await b.close();
  console.log('frames', n);
})();
