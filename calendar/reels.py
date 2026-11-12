"""Stitch each Reel's shot frames (from render.js) into media/<id>/reel.mp4.

Each shot is held for its shot-list timing with a slow push-in, 1080x1920, 30 fps,
H.264 + silent AAC (Instagram and Facebook both accept it). Frames are then deleted.
"""
import json, os, re, shutil, subprocess, tempfile

H = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(H, 'media')
FPS = 30

posts = {}
for f in ['content-a.json', 'content-b.json', 'content-c.json']:
    for w in json.load(open(os.path.join(H, f)))['weeks']:
        for p in w['posts']:
            posts[p['id']] = p
for p in json.load(open(os.path.join(H, 'extra.json'))).get('posts', []):
    posts[p['id']] = p


def secs(t):
    m, s = t.split(':')
    return int(m) * 60 + float(s)


def durations(p):
    out = []
    for i, s in enumerate(p['shots']):
        a, b = re.split(r'\s*[-–]\s*', s['t'].strip())
        out.append(max(1.5, secs(b) - secs(a)))
    return out


for entry in json.load(open(os.path.join(M, 'manifest.json'))):
    if entry['template'] != 'reel':
        continue
    pid = entry['id']
    frames = sorted(os.listdir(os.path.join(M, pid, 'frames')))
    durs = durations(posts[pid])
    assert len(frames) == len(durs), pid
    with tempfile.TemporaryDirectory() as tmp:
        parts = []
        for i, (fr, d) in enumerate(zip(frames, durs)):
            n = int(round(d * FPS))
            z = f"1+0.06*on/{n}" if i % 2 == 0 else f"1.06-0.06*on/{n}"
            out = os.path.join(tmp, f'{i:02d}.mp4')
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', os.path.join(M, pid, 'frames', fr),
                            '-vf', f"scale=2160:3840,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps={FPS},format=yuv420p",
                            '-frames:v', str(n), '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', out], check=True)
            parts.append(out)
        lst = os.path.join(tmp, 'list.txt')
        open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
        dst = os.path.join(M, pid, 'reel.mp4')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst,
                        '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', dst], check=True)
    # keep the first frame as the cover image, drop the rest
    shutil.copy(os.path.join(M, pid, 'frames', frames[0]), os.path.join(M, pid, 'cover.png'))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(M, pid, 'cover.png'), '-q:v', '3', os.path.join(M, pid, 'cover.jpg')], check=True)
    os.remove(os.path.join(M, pid, 'cover.png'))
    shutil.rmtree(os.path.join(M, pid, 'frames'))
    print(pid, round(sum(durs), 1), 's', os.path.getsize(dst) // 1024, 'KB')
