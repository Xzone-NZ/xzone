// Render every scheduled post to upload-ready media in media/<post id>/.
// Images: 1080x1080 JPEG (single posts, and every carousel slide).
// Reels: one 1080x1920 frame per shot (media/<id>/frames/), stitched into an MP4 by reels.py.
// Run: python3 build.py && node render.js && python3 reels.py
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const H = __dirname;
const OUT = path.join(H, 'media');

const EXPORT_CSS = `
  body{margin:0;padding:0;background:#000}
  .wrap,.ov{display:none!important}
  #stage{position:fixed;left:0;top:0}
  #stage .pv{width:1080px}
  #stage .pv .dots,#stage .pv .badge,#stage .pv .play{display:none}
  /* reel frames */
  .rf{width:1080px;height:1920px;aspect-ratio:auto!important}
  .rf .rt{position:absolute;left:7cqw;right:7cqw;top:56%;font-weight:800;font-size:9cqw;line-height:1.08;letter-spacing:-.01em;text-shadow:0 .4cqw 2cqw rgba(0,0,0,.35)}
  .rf .rt em{display:block;font-style:normal;color:var(--pa);font-weight:600;font-size:5.2cqw;line-height:1.2;margin-top:3cqw;letter-spacing:0;text-shadow:none}
  .rf .lg{width:26cqw;top:6cqw;left:6cqw}
  .rf .ft{height:8cqw;font-size:3.2cqw}
  .rf.end{display:grid;place-items:center}
  .rf.end .ph,.rf.end .wash{display:none}
  .rf.end .big{width:56cqw;filter:brightness(0) invert(1);position:absolute;left:22cqw;top:36%}
  .rf.end .rt{top:52%;text-align:center;color:var(--pa);font-size:7cqw}
`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(H, 'xzone-feed-preview.html'));
  await page.waitForLoadState('networkidle');
  await page.evaluate(() => document.fonts.ready);
  await page.addStyleTag({ content: EXPORT_CSS });
  await page.evaluate(() => { const s = document.createElement('div'); s.id = 'stage'; document.body.appendChild(s); });

  const list = await page.evaluate(() => posts.map(p => ({ id: p.id, template: p.template, n: (p.slides || []).length, shots: (p.shots || []).length })));
  const manifest = [];
  for (const p of list) {
    const dir = path.join(OUT, p.id);
    fs.rmSync(dir, { recursive: true, force: true });
    fs.mkdirSync(dir, { recursive: true });
    const entry = { id: p.id, template: p.template, files: [] };
    if (p.template === 'reel') {
      fs.mkdirSync(path.join(dir, 'frames'));
      for (let i = 0; i < p.shots; i++) {
        await page.evaluate(([id, i]) => {
          const p = posts.find(x => x.id === id), s = p.shots[i];
          const end = /end card/i.test(s.shot) || i === p.shots.length - 1 && /logo/i.test(s.shot);
          const txt = i === 0 && !s.text ? `${esc(p.headline)}<em>${esc(p.subline)}</em>` : esc(s.text);
          document.getElementById('stage').innerHTML = end
            ? `<div class="pv tall rf end r-${p.range || 'all'}"><img class="big" src="${IMG.logo}" alt=""><div class="rt">${txt}</div><div class="ft">@xzonenz · xzone.nz</div></div>`
            : `<div class="pv tall rf r-${p.range || 'all'}"><div class="ph" style="background-image:url(${photo(p.photo)})"></div><div class="wash"></div>${logo()}<div class="rt">${txt}</div><div class="ft">@xzonenz</div></div>`;
        }, [p.id, i]);
        const f = path.join(dir, 'frames', `${String(i + 1).padStart(2, '0')}.png`);
        await page.locator('#stage .pv').screenshot({ path: f });
      }
      entry.files.push(`${p.id}/reel.mp4`);
    } else {
      const count = p.template === 'carousel' && p.n ? p.n : 1;
      for (let i = 0; i < count; i++) {
        await page.evaluate(([id, i, count]) => {
          const p = posts.find(x => x.id === id);
          document.getElementById('stage').innerHTML = count > 1 ? slide(p, p.slides[i], i, count) : preview(p);
        }, [p.id, i, count]);
        const name = count > 1 ? `slide-${String(i + 1).padStart(2, '0')}.jpg` : 'post.jpg';
        await page.locator('#stage .pv').screenshot({ path: path.join(dir, name), type: 'jpeg', quality: 90 });
        entry.files.push(`${p.id}/${name}`);
      }
    }
    manifest.push(entry);
    console.log(p.id, entry.files.length);
  }
  fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify(manifest, null, 1));
  await browser.close();
})();
