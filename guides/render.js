// Prints each guide HTML to an A4 PDF and reports pages whose content runs into the footer.
const { chromium } = require('playwright');
const { pathToFileURL } = require('url');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const j of jobs) {
    await page.goto(pathToFileURL(j.html).href, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const poppins = await page.evaluate(() => document.fonts.check('600 12px Poppins'));
    const overflow = await page.evaluate(() => [...document.querySelectorAll('.page')].map((el, i) => {
      const foot = el.querySelector('.foot');
      const limit = foot ? foot.offsetTop - 2 : el.clientHeight;
      let max = 0;
      for (const c of el.children) { if (c.classList.contains('foot')) continue; max = Math.max(max, c.offsetTop + c.offsetHeight); }
      return max > limit ? `${i + 1}:+${max - limit}px` : null;
    }).filter(Boolean));
    await page.pdf({ path: j.pdf, format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    console.log(`${j.pdf.split('/').pop()}  poppins=${poppins}  overflow=${overflow.length ? overflow.join(' ') : 'none'}`);
  }
  await browser.close();
})();
