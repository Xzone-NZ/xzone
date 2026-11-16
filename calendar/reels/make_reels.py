"""Build motion Reels from footage and photos we already have (no new filming needed).

Each Reel in specs.json is a list of segments shown in the 1080 x 1350 video window:
  {"clip": [src, in], "dur": s}               a clip from a source video, played from `in`
  {"img": path, "dur": s, "kb": "kbIn"}         a photo with a slow camera move (kbIn kbOut kbL kbR kbUp)
  {"hold": [src, in, play], "dur": s}           play a short clip, then hold its last frame with a slow zoom
plus "text" (caption, [[words]] get the lime highlighter), "sub", "small" and "timer" per segment,
and an end card. Captions, bands, progress bar and end card are drawn by overlay.html.
Writes buffer/media/<id>/reel.mp4 (1080 x 1920, 30 fps, H.264, silent AAC track) and reel-cover.jpg.
Run: python3 reels/make_reels.py [reel ids...]
"""
import json, os, shutil, subprocess, sys, tempfile

H = os.path.dirname(os.path.abspath(__file__))
CAL = os.path.dirname(H)
ROOT = os.path.dirname(CAL)
FPS = 30
SOURCES = {'promo': 'brief/source/drive/videos/xzone-promo-reel-1080x1920.mp4'}  # 4:5 picture at y 285
CROP = 'crop=1080:1350:0:285'


def run(*a):
    subprocess.run(a, check=True)


def src_path(s):
    return os.path.join(ROOT, SOURCES.get(s, s))


def build(rid, spec, tmp):
    segs = spec['segments']
    parts, page_segs = [], []
    for i, s in enumerate(segs):
        frames = round(s['dur'] * FPS)
        out = f'{tmp}/seg{i:02d}.mp4'
        seg = {k: v for k, v in s.items() if k not in ('clip', 'hold', 'img')}
        if 'clip' in s:          # straight clip
            src, t_in = s['clip']
            run('ffmpeg', '-v', 'error', '-y', '-ss', str(t_in), '-i', src_path(src), '-vf', f'{CROP},fps={FPS}',
                '-frames:v', str(frames), '-an', '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', out)
        elif 'hold' in s:        # play, then hold the last frame (the overlay page zooms the held frame)
            src, t_in, play = s['hold']
            pf = round(play * FPS)
            still = f'{tmp}/hold{i:02d}.png'
            run('ffmpeg', '-v', 'error', '-y', '-ss', str(t_in + (pf - 1) / FPS), '-i', src_path(src), '-vf', CROP,
                '-frames:v', '1', still)
            run('ffmpeg', '-v', 'error', '-y', '-ss', str(t_in), '-i', src_path(src), '-vf',
                f'{CROP},fps={FPS},tpad=stop_mode=clone:stop_duration={s["dur"]}', '-frames:v', str(frames),
                '-an', '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', out)
            seg.update(img='file://' + still, clip=play, kb=s.get('kb', 'kbIn'))
        else:                    # photo: the overlay draws it; the clip track is plain green underneath
            run('ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=c=0x004F23:s=1080x1350:r={FPS}',
                '-frames:v', str(frames), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', out)
            seg['img'] = 'file://' + os.path.join(ROOT, s['img'])
        parts.append(out)
        page_segs.append(seg)
    total = sum(s['dur'] for s in segs) + spec['end'].get('dur', 2.5)
    # clip track
    lst = f'{tmp}/list.txt'
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    track = f'{tmp}/track.mp4'
    run('ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', track)
    # overlay frames
    reel = {'total': total, 'eyebrow': spec.get('eyebrow', ''), 'segments': page_segs, 'end': spec['end']}
    page = open(os.path.join(H, 'overlay.html')).read()
    page = page.replace('__REEL__', json.dumps(reel, ensure_ascii=False)) \
               .replace('__LOGO__', 'file://' + os.path.join(CAL, 'small', 'logo.png'))
    html = f'{tmp}/overlay.html'
    open(html, 'w').write(page)
    frames_dir = f'{tmp}/frames'
    os.makedirs(frames_dir)
    run('node', os.path.join(H, 'render.js'), html, frames_dir, str(total), str(FPS))
    # composite: green ground, clip track in the window, overlay on top, silent audio
    out_dir = os.path.join(CAL, 'buffer', 'media', rid)
    os.makedirs(out_dir, exist_ok=True)
    mp4 = os.path.join(out_dir, 'reel.mp4')
    run('ffmpeg', '-v', 'error', '-y',
        '-f', 'lavfi', '-i', f'color=c=0x004F23:s=1080x1920:r={FPS}:d={total}',
        '-i', track, '-framerate', str(FPS), '-i', f'{frames_dir}/%05d.png',
        '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
        '-filter_complex', '[0][1]overlay=0:285:eof_action=pass[a];[a][2]overlay=0:0[v]',
        '-map', '[v]', '-map', '3', '-t', str(total), '-c:v', 'libx264', '-preset', 'slow', '-crf', '19',
        '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', str(FPS), '-c:a', 'aac', '-b:a', '128k',
        '-movflags', '+faststart', mp4)
    # cover = a frame from the first segment once its caption is in
    cover_t = min(1.6, segs[0]['dur'] - 0.4)
    run('ffmpeg', '-v', 'error', '-y', '-ss', str(cover_t), '-i', mp4, '-frames:v', '1', '-q:v', '2',
        os.path.join(out_dir, 'reel-cover-frame.jpg'))
    return mp4, total


def main():
    specs = json.load(open(os.path.join(H, 'specs.json')))
    ids = sys.argv[1:] or list(specs)
    for rid in ids:
        tmp = tempfile.mkdtemp(prefix=f'reel-{rid}-')
        try:
            mp4, total = build(rid, specs[rid], tmp)
            print(rid, f'{total:.1f}s', os.path.relpath(mp4, CAL), f'{os.path.getsize(mp4) / 1e6:.1f} MB')
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
