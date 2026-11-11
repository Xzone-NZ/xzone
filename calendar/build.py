import json, base64, os, sys
H = os.path.dirname(os.path.abspath(__file__))
weeks = []
for f in ['content-a.json', 'content-b.json', 'content-c.json']:
    p = os.path.join(H, f)
    if os.path.exists(p):
        weeks += json.load(open(p))['weeks']
weeks.sort(key=lambda w: w['week'])
img = {}
for n in ['bush', 'founders', 'bruise', 'shoulder', 'ankle']:
    img[n] = 'data:image/jpeg;base64,' + base64.b64encode(open(f'{H}/small/{n}.jpg', 'rb').read()).decode()
for n in ['range', 'icon', 'logo']:
    img[n] = 'data:image/png;base64,' + base64.b64encode(open(f'{H}/small/{n}.png', 'rb').read()).decode()
data = json.dumps({'weeks': weeks}, ensure_ascii=False).replace('</', '<\\/')
t = open(f'{H}/template.html').read()
out = t.replace('__DATA__', data).replace('__IMG__', json.dumps(img))
open(f'{H}/xzone-summer-calendar.html', 'w').write(out)
print('weeks', len(weeks), 'posts', sum(len(w['posts']) for w in weeks), 'bytes', len(out))
