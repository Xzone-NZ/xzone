"""Make upload-ready files for every scheduled post and story, for Buffer.

Writes buffer/media/<post id>/ and buffer/media/stories/, plus buffer/media-manifest.json:
- carousels: slide-01.jpg ... at 1080 x 1350 (slide 1 is the hand-built cover; the rest are the
  calendar's generated slides; ambassador carousels use ambassadors/instagram/)
- single posts: post.jpg at 1080 x 1350
- Reels: reel-cover.jpg at 1080 x 1920 (the video itself is filmed from the shot list)
- stories: stories/<story id>.jpg at 1080 x 1920
Hand-built designs are re-rendered from brief/designs/**/*.dc.html with the best local photo.
Run after build.py:  python3 build.py && python3 export_media.py && python3 buffer_export.py
Needs node with Playwright (render_designs.js, render_slides.js in export/).
"""
import glob, json, os, re, shutil, subprocess, tempfile
from PIL import Image, ImageChops, ImageFilter

H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(H)
OUT = os.path.join(H, 'buffer', 'media')
AMB = {'w7-amb-jasmine': 'jasmine-marsters', 'w10-amb-mollie': 'mollie-allison'}


def blobmap():
    """Canvas image id -> best local file (largest width wins)."""
    spec = open(os.path.join(ROOT, 'brief/designs/weeks-5-13/_specs.py')).read()
    names = {v: k for k, v in re.findall(r"'([\w-]+)': '([0-9a-f]{32})'", spec)}
    names['bc9c642fb9787508d512b14216a6a0fd'] = 'relief-rollon-shoulder'
    # photos added in the repo after the canvas designs (no canvas upload id; these ids are local only)
    names['b0c1ea4b0c1ea4b0c1ea4b0c1ea4b0c1'] = 'bush-clear'   # the waterfall without the green wash (17 Nov)
    names['c0a1ea4c0a1ea4c0a1ea4c0a1ea4c0a1'] = 'kumarahou'    # kūmarahou in flower, from the promo video
    m = {}
    for blob, n in names.items():
        c = [p for p in (f'brief/photos/{n}.jpg', f'calendar/small/{n}.jpg', f'calendar/small/{n}.png')
             if os.path.exists(os.path.join(ROOT, p))]
        if c:
            m[blob] = os.path.join(ROOT, max(c, key=lambda p: Image.open(os.path.join(ROOT, p)).size[0]))
    return m


def save(im, path):
    im.convert('RGB').save(path, 'JPEG', quality=92, optimize=True, progressive=True)


def main():
    tmp = tempfile.mkdtemp(prefix='xzone-media-')
    mapf = os.path.join(tmp, 'blobmap.json')
    json.dump(blobmap(), open(mapf, 'w'))
    srcs = sorted(glob.glob(os.path.join(ROOT, 'brief/designs/weeks-*/W*.dc.html')))
    subprocess.run(['node', os.path.join(H, 'export/render_designs.js'), mapf, tmp, *srcs], check=True)
    subprocess.run(['node', os.path.join(H, 'export/render_slides.js'), tmp], check=True)

    page = open(os.path.join(H, 'xzone-summer-calendar.html')).read()
    DES = json.loads(re.search(r'const DES=(\{.*?\});', page).group(1))
    D = json.loads(re.search(r'<script type="application/json" id="data">(.*?)</script>', page, re.S)
                   .group(1).replace('<\\/', '</'))

    soft = []

    def design(rel, owner):
        n = os.path.basename(rel)[:-4]
        a = Image.open(f'{tmp}/{n}-a.png').convert('RGB')
        b = f'{tmp}/{n}-b.png'
        if os.path.exists(b):   # a canvas-only photo: fill it from the 540px preview, and flag it
            mask = (ImageChops.difference(a, Image.open(b).convert('RGB')).convert('L')
                    .point(lambda v: 255 if v > 6 else 0).filter(ImageFilter.MaxFilter(3)))
            prev = Image.open(os.path.join(H, rel)).convert('RGB').resize(a.size, Image.LANCZOS)
            a = Image.composite(prev, a, mask)
            soft.append(owner)
        return a

    # keep the motion Reels (made by reels/make_reels.py) across a rebuild
    keep = {f: open(f, 'rb').read() for f in glob.glob(os.path.join(OUT, '*', 'reel.mp4')) + glob.glob(os.path.join(OUT, '*', 'reel-cover-frame.jpg'))}
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(os.path.join(OUT, 'stories'))
    for f, b in keep.items():
        os.makedirs(os.path.dirname(f), exist_ok=True)
        open(f, 'wb').write(b)
    man = {'posts': {}, 'stories': {}}
    rel = lambda f: os.path.relpath(f, os.path.join(H, 'buffer'))
    for w in D['weeks']:
        for p in w['posts']:
            pid = p['id']
            d = os.path.join(OUT, pid)
            os.makedirs(d, exist_ok=True)
            files = []
            if pid in AMB:
                for i in (1, 2, 3):
                    f = f'{d}/slide-{i:02d}.jpg'
                    save(Image.open(os.path.join(ROOT, f'ambassadors/instagram/{AMB[pid]}-slide-{i}.png')), f)
                    files.append(f)
            else:
                cover = design(DES[pid], pid)
                if p['template'] == 'carousel':
                    files.append(f'{d}/slide-01.jpg'); save(cover, files[-1])
                    for k in range(2, len(p['slides']) + 1):
                        files.append(f'{d}/slide-{k:02d}.jpg')
                        save(Image.open(f'{tmp}/{pid}-slide-{k:02d}.png'), files[-1])
                elif p['template'] == 'reel':
                    files.append(f'{d}/reel-cover.jpg'); save(cover, files[-1])
                else:
                    files.append(f'{d}/post.jpg'); save(cover, files[-1])
            for f in files:
                assert Image.open(f).size in ((1080, 1350), (1080, 1920)), (f, Image.open(f).size)
            man['posts'][pid] = {'week': w['week'], 'date': p['date'], 'day': p['day'], 'format': p['format'],
                                 'title': p['title'], 'files': [rel(f) for f in files],
                                 'video_needed': p['template'] == 'reel'}
        for s in w['stories']:
            f = os.path.join(OUT, 'stories', f"{s['id']}.jpg")
            save(design(DES[s['id']], s['id']), f)
            man['stories'][s['id']] = {'week': w['week'], 'day': s['day'], 'type': s['type'],
                                      'text': s['text'], 'file': rel(f)}
    man['soft_photo'] = soft
    json.dump(man, open(os.path.join(H, 'buffer', 'media-manifest.json'), 'w'), ensure_ascii=False, indent=1)
    shutil.rmtree(tmp)
    print(len(man['posts']), 'posts,', sum(len(v['files']) for v in man['posts'].values()), 'files,',
          len(man['stories']), 'stories; canvas-only photo (softer):', ', '.join(soft) or 'none')


if __name__ == '__main__':
    main()
