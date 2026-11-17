// Renders guide.html to the PDF. Called by _build.py.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.join(dir, 'guide.html')); await p.waitForTimeout(1500);
  await p.pdf({ path: path.join(dir, 'Move-Freely-Shopify-Setup-Guide.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;font-size:8px;color:#5d6f62;font-family:Arial;padding:0 17mm;display:flex;justify-content:space-between"><span>Move Freely · Shopify setup guide</span><span class="pageNumber"></span></div>' });
  await b.close();
})();
