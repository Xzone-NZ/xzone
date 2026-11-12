// Export every Instagram carousel slide in the mock-up as a 1080 x 1350 PNG.
// Run after build.py:  node ambassadors/export_instagram.js
// Output: ambassadors/instagram/<slug>-slide-<n>.png
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const here = __dirname;
  const out = path.join(here, 'instagram');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const probe = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await probe.goto('file://' + path.join(here, 'xzone-ambassador-posts.html'));
  const w = await probe.$eval('.slide', (n) => n.getBoundingClientRect().width);
  await probe.close();
  // Render at a scale where one slide is 1080 px wide.
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1080 / w });
  await page.goto('file://' + path.join(here, 'xzone-ambassador-posts.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  const sections = await page.$$('section.amb');
  let count = 0;
  for (const sec of sections) {
    const slug = await sec.getAttribute('id');
    const slides = await sec.$$('.slide');
    for (let i = 0; i < slides.length; i++) {
      await slides[i].scrollIntoViewIfNeeded();
      await page.waitForTimeout(150);
      const b = await slides[i].boundingBox();
      // inset 1px so no border or neighbouring pixels leak in; export_instagram.py resizes to 1080 x 1350
      await page.screenshot({ path: path.join(out, `${slug}-slide-${i + 1}.png`), clip: { x: b.x + 1, y: b.y + 1, width: b.width - 2, height: b.height - 2 } });
      count++;
    }
  }
  await browser.close();
  console.log(`Exported ${count} slides to ${out}`);
})();
