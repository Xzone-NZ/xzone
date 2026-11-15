// Render one hand-built design (.dc.html from the design canvas) at full size.
// Usage: node render_designs.js <blobmap.json> <outDir> <src.dc.html>...
// Canvas images (/_blob/<id>) are swapped for local photos from blobmap.json. A photo that only
// exists on the canvas is rendered twice (black, then white) so export_media.py can find where it
// sits and fill it from the preview JPG: writes <name>-a.png, plus <name>-b.png when one is missing.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BLK = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVR4nGNgAAAAAgABSK+kcQAAAABJRU5ErkJggg==';
const WHT = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVR4nGP4DwABAQEAG7buVgAAAABJRU5ErkJggg==';

(async () => {
  const [mapFile, out, ...srcs] = process.argv.slice(2);
  const M = JSON.parse(fs.readFileSync(mapFile, 'utf8'));
  const b = await chromium.launch();
  for (const src of srcs) {
    const raw = fs.readFileSync(src, 'utf8');
    const name = path.basename(src, '.dc.html');
    let missing = 0;
    const make = fill => raw
      .replace(/\/_blob\/([0-9a-f]{32})/g, (x, id) => { if (M[id]) return 'file://' + M[id]; missing++; return fill; })
      .replace('<script src="./support.js"></script>', '');
    const m = raw.match(/"\$preview":\{"width":(\d+),"height":(\d+)\}/);
    const W = +m[1], H = +m[2];
    const pg = await b.newPage({ viewport: { width: W, height: H } });
    const tmp = path.join(out, `_${name}.html`);
    const shot = async (html, file) => {
      fs.writeFileSync(tmp, html);
      await pg.goto('file://' + tmp, { waitUntil: 'networkidle' });
      await pg.evaluate(() => document.fonts.ready);
      await pg.waitForTimeout(250);
      await pg.screenshot({ path: file, clip: { x: 0, y: 0, width: W, height: H } });
    };
    await shot(make(BLK), path.join(out, `${name}-a.png`));
    if (missing) await shot(make(WHT), path.join(out, `${name}-b.png`));
    fs.unlinkSync(tmp);
    await pg.close();
    if (missing) console.log(name, 'canvas-only photos:', missing / 2);
  }
  await b.close();
})();
