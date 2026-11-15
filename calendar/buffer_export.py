"""Export the 39 scheduled posts (selection.json) as Buffer-ready drafts.

Writes buffer/buffer-posts.json and buffer/buffer-posts.csv: one row per post per
channel (Instagram, Facebook), with the scheduled time in NZ time, the caption with
hashtags, and the media and confirm notes to sort before each goes live.
Each row lists its upload-ready files (from export_media.py) as repo paths and raw GitHub URLs.
Stories go to buffer/buffer-stories.csv.
Run: python3 build.py && python3 export_media.py && python3 buffer_export.py
"""
import json, os, csv, datetime
H = os.path.dirname(os.path.abspath(__file__))
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
TIME = '19:00'            # 7pm NZT, from the summer plan's posting times
TZ = 'Pacific/Auckland'
CHANNELS = ['Instagram', 'Facebook']
# raw file URLs on the repo's default branch (the repo is public, so Buffer can fetch them)
RAW = 'https://raw.githubusercontent.com/Xzone-NZ/xzone/claude/jolly-ptolemy-s3u3e9/calendar/buffer/'
MAN = json.load(open(os.path.join(H, 'buffer', 'media-manifest.json')))

weeks = []
for f in ['content-a.json', 'content-b.json', 'content-c.json']:
    weeks += json.load(open(os.path.join(H, f)))['weeks']
posts = {p['id']: p for w in weeks for p in w['posts']}
for p in json.load(open(os.path.join(H, 'extra.json'))).get('posts', []):
    posts[p['id']] = p
sel = json.load(open(os.path.join(H, 'selection.json')))['weeks']

def flags(p):
    f = p.get('flags') or []
    if isinstance(f, str):
        try: f = json.loads(f)
        except ValueError: f = [f]
    return f

rows = []
for w in sorted(weeks, key=lambda w: w['week']):
    first = w['posts'][0]
    monday = datetime.date.fromisoformat(first['date']) - datetime.timedelta(days=DAYS.index(first['day']))
    for pid, day in sel[str(w['week'])]:
        p = posts[pid]
        date = (monday + datetime.timedelta(days=DAYS.index(day))).isoformat()
        text = p['caption'].strip()
        if p.get('hashtags'):
            text += '\n\n' + p['hashtags'].strip()
        media = {'Carousel': f"{len(p.get('slides') or [])} slides", 'Reel': 'video'}.get(p['format'], 'image')
        files = MAN['posts'][pid]['files']
        if p['format'] == 'Reel':
            media = 'video (film from the shot list); cover image ready'
        if pid in MAN['soft_photo']:
            media += '; photo is a 540px preview, swap for the design-canvas export'
        for ch in CHANNELS:
            rows.append({
                'id': f"{pid}-{ch[:2].lower()}", 'post': pid, 'week': w['week'], 'date': date,
                'time': TIME, 'timezone': TZ, 'channel': ch, 'format': p['format'],
                'title': p['title'], 'text': text, 'media': media,
                'files': files, 'file_urls': [RAW + f for f in files],
                'shoot': p.get('shoot', ''), 'placeholders': '{' in text, 'confirm': flags(p),
            })

os.makedirs(os.path.join(H, 'buffer'), exist_ok=True)
json.dump(rows, open(os.path.join(H, 'buffer', 'buffer-posts.json'), 'w'), ensure_ascii=False, indent=1)
with open(os.path.join(H, 'buffer', 'buffer-posts.csv'), 'w', newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    wr.writeheader()
    for r in rows:
        wr.writerow({**r, 'confirm': ' | '.join(r['confirm']), 'files': ' | '.join(r['files']), 'file_urls': ' | '.join(r['file_urls'])})
print(len(rows), 'drafts,', len({r['post'] for r in rows}), 'posts,',
      sum(r['placeholders'] for r in rows) // len(CHANNELS), 'with {PLACEHOLDERS} still to fill')

with open(os.path.join(H, 'buffer', 'buffer-stories.csv'), 'w', newline='') as fh:
    wr = csv.writer(fh)
    wr.writerow(['story', 'week', 'day', 'type', 'text', 'file', 'file_url', 'note'])
    for sid, s in MAN['stories'].items():
        wr.writerow([sid, s['week'], s['day'], s['type'], s['text'], s['file'], RAW + s['file'],
                     'photo is a 540px preview, swap for the design-canvas export' if sid in MAN['soft_photo'] else ''])
print(len(MAN['stories']), 'stories in buffer-stories.csv')
