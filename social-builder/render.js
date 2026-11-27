#!/usr/bin/env node
/*
 * X-ZONE Social Builder renderer.
 * Usage: node social-builder/render.js social-builder/specs/<id>.json [outDir]
 * Reads a JSON spec, renders PNG frames with Playwright (Chromium) and, for reels,
 * a silent MP4 with ffmpeg. Output goes to <outDir> (default social-builder/out/<id>).
 * Paths in a spec are relative to the repo root. Run from the repo root.
 *
 * Spec:
 *  { "id": "kebab-id", "format": "post" | "carousel" | "reel",
 *    "slides": [ {photo, hook, sub, callout, bullets[], button} ]   // post (1) and carousel (2 to 8)
 *    "beats":  [ {photo, hook, sub, seconds} ]                      // reel (2 to 6)
 *  }
 * Markup in hook/sub: [[word]] = lime underline behind the word (one per slide), **word** = bold.
 * Look and rules: brief/06-brand-spec.md ("Final look: price-change carousel").
 */
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const ROOT = process.cwd();
const FONTS = path.join(ROOT, 'guides/fonts');
const LOGO = path.join(ROOT, 'tools/logo-white.png');
const SIZES = { post: [1080, 1350], carousel: [1080, 1350], reel: [1080, 1920] };
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const mark = s => esc(s).replace(/\[\[(.+?)\]\]/g, '<span class="key">$1</span>').replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
const BANNED = /[—–]/;

function frameHtml(fmt, s, i, n) {
  const [W, H] = SIZES[fmt]; const reel = fmt === 'reel';
  const photoH = reel ? 1100 : 650, textTop = photoH + (reel ? 64 : 50), logoBottom = reel ? 320 : 57;
  const photo = 'file://' + path.join(ROOT, s.photo);
  const bullets = (s.bullets || []).map(b => `<li><i></i><span>${mark(b)}</span></li>`).join('');
  return `<!doctype html><meta charset="utf-8"><style>
${[300,400,500,600,700,800].map(w => `@font-face{font-family:Poppins;font-weight:${w};src:url('file://${FONTS}/poppins-${w}.woff2') format('woff2')}`).join('')}
*{box-sizing:border-box;margin:0}
body{width:${W}px;height:${H}px;background:#004F23;font-family:Poppins,sans-serif;color:#fff;position:relative;overflow:hidden}
.photo{position:absolute;left:0;top:0;width:${W}px;height:${photoH}px;object-fit:cover}
.txt{position:absolute;left:72px;right:72px;top:${textTop}px;max-height:${H - textTop - logoBottom - 100}px}
h1{text-wrap:balance;font-weight:800;font-size:${reel ? 80 : 70}px;line-height:1.14;letter-spacing:-.01em}
.key{background:linear-gradient(#E0E64A,#E0E64A) 0 88%/100% 8px no-repeat;padding:0 2px}
p{font-weight:500;font-size:${reel ? 38 : 32}px;line-height:1.5;margin-top:26px}
.callout{margin-top:30px;background:#E0E64A;color:#1F1C1D;font-weight:700;font-size:31px;line-height:1.35;border-radius:34px;padding:28px 44px}
ul{list-style:none;padding:0;margin-top:26px}
li{display:flex;gap:20px;align-items:center;font-weight:500;font-size:31px;margin-bottom:16px}
li i{flex:none;width:38px;height:38px;border-radius:50%;background:#E0E64A;position:relative}
li i:after{content:"";position:absolute;left:12px;top:8px;width:9px;height:17px;border:solid #004F23;border-width:0 5px 5px 0;transform:rotate(40deg)}
.button{display:inline-block;margin-top:24px;background:#003a19;color:#fff;font-weight:700;font-size:30px;border-radius:40px;padding:16px 36px}
.logo{position:absolute;right:72px;bottom:${logoBottom}px;width:260px}
.swipe{position:absolute;left:72px;bottom:${logoBottom + 14}px;font-weight:700;font-size:28px;letter-spacing:.04em}
.swipe em{font-style:normal;color:#E0E64A;margin-left:12px}
</style>
<img class="photo" src="${photo}">
<div class="txt" id="txt"><h1 id="h">${mark(s.hook)}</h1>${s.sub ? `<p id="sub">${mark(s.sub)}</p>` : ''}${bullets ? `<ul>${bullets}</ul>` : ''}${s.callout ? `<div class="callout">${mark(s.callout)}</div>` : ''}${s.button ? `<span class="button">${esc(s.button)}</span>` : ''}</div>
${fmt === 'carousel' && i === 0 ? '<div class="swipe">SWIPE<em>&rarr;</em></div>' : ''}
<img class="logo" id="logo" src="file://${LOGO}">`;
}

async function shoot(page, fmt, s, i, n, file, tmp) {
  const [W, H] = SIZES[fmt];
  for (const f of ['hook', 'sub']) if (s[f] && BANNED.test(s[f])) throw new Error(`Banned dash in ${f}`);
  const htmlFile = path.join(tmp, `f${i}.html`);
  fs.writeFileSync(htmlFile, frameHtml(fmt, s, i, n));
  await page.setViewportSize({ width: W, height: H });
  await page.goto('file://' + htmlFile); await page.evaluate(() => document.fonts.ready);
  // layout checks: hook max two lines, text clear of logo, nothing clipped
  const m = await page.evaluate(() => {
    const h = document.getElementById('h'), t = document.getElementById('txt'), l = document.getElementById('logo').getBoundingClientRect();
    const lh = parseFloat(getComputedStyle(h).lineHeight);
    const r = t.getBoundingClientRect(); const last = [...t.children].pop().getBoundingClientRect();
    return { lines: Math.round(h.getBoundingClientRect().height / lh), textBottom: last.bottom, logoTop: l.top, textRight: Math.max(...[...t.querySelectorAll('*')].map(e => e.getBoundingClientRect().right)), keys: document.querySelectorAll('.key').length };
  });
  if (m.lines > 2) throw new Error(`Slide ${i + 1}: hook runs to ${m.lines} lines (max 2). Shorten it.`);
  if (m.keys > 1) throw new Error(`Slide ${i + 1}: more than one highlighted word.`);
  if (m.textBottom > m.logoTop - 16 && fmt !== 'reel') throw new Error(`Slide ${i + 1}: text (${Math.round(m.textBottom)}) runs into the logo (${Math.round(m.logoTop)}). Shorten it.`);
  if (m.textBottom > H - 330 && fmt === 'reel') throw new Error(`Beat ${i + 1}: text sits in the reel's bottom UI zone. Shorten it.`);
  await page.screenshot({ path: file });
}

(async () => {
  const specPath = process.argv[2]; if (!specPath) { console.error('Usage: node social-builder/render.js <spec.json> [outDir]'); process.exit(1); }
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  const fmt = spec.format; if (!SIZES[fmt]) throw new Error('format must be post, carousel or reel');
  const out = process.argv[3] || path.join('social-builder/out', spec.id); fs.mkdirSync(out, { recursive: true });
  const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'sb-'));
  const items = fmt === 'reel' ? spec.beats : spec.slides;
  if (fmt === 'post' && items.length !== 1) throw new Error('A post has exactly one slide');
  if (fmt === 'carousel' && (items.length < 2 || items.length > 8)) throw new Error('A carousel has 2 to 8 slides');
  if (fmt === 'reel' && (items.length < 2 || items.length > 6)) throw new Error('A reel has 2 to 6 beats');
  const browser = await chromium.launch(); const page = await browser.newPage(); const files = [];
  for (let i = 0; i < items.length; i++) {
    const name = fmt === 'post' ? 'post.png' : fmt === 'carousel' ? `slide-${i + 1}.png` : `beat-${i + 1}.png`;
    await shoot(page, fmt, items[i], i, items.length, path.join(out, name), tmp); files.push(name);
  }
  await browser.close();
  if (fmt === 'reel') {
    fs.copyFileSync(path.join(out, 'beat-1.png'), path.join(out, 'cover.png')); files.push('cover.png');
    const X = 0.4, ins = [], filt = []; let acc = 0;
    items.forEach((b, i) => { const d = (b.seconds || 3) + (i < items.length - 1 ? X : 0); ins.push('-loop', '1', '-t', String(d), '-i', path.join(out, `beat-${i + 1}.png`)); });
    let last = '[0:v]';
    for (let i = 1; i < items.length; i++) { acc += (items[i - 1].seconds || 3); const o = i === items.length - 1 ? '[v]' : `[x${i}]`; filt.push(`${last}[${i}:v]xfade=transition=fade:duration=${X}:offset=${acc}${o}`); last = o; }
    const total = items.reduce((a, b) => a + (b.seconds || 3), 0);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...ins, '-f', 'lavfi', '-t', String(total), '-i', 'anullsrc=r=44100:cl=stereo', '-filter_complex', filt.join(';'), '-map', '[v]', '-map', `${items.length}:a`, '-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-c:a', 'aac', '-shortest', '-movflags', '+faststart', path.join(out, 'reel.mp4')]);
    files.push('reel.mp4');
    // small preview for the app
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', path.join(out, 'reel.mp4'), '-vf', 'scale=540:960', '-crf', '30', '-c:a', 'aac', '-movflags', '+faststart', path.join(out, 'preview-reel.mp4')]);
  }
  // small JPEG previews (600 px wide) for the app's asset store
  for (const f of files.filter(f => f.endsWith('.png'))) {
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', path.join(out, f), '-vf', 'scale=600:-1', '-q:v', '4', path.join(out, 'preview-' + f.replace('.png', '.jpg'))]);
  }
  console.log(JSON.stringify({ id: spec.id, format: fmt, out, files }));
})().catch(e => { console.error(e.message); process.exit(1); });
