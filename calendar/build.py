"""Build xzone-summer-calendar.html from content-*.json, extra.json and selection.json."""
import json, base64, os, datetime
H = os.path.dirname(os.path.abspath(__file__))
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

weeks = []
for f in ['content-a.json', 'content-b.json', 'content-c.json']:
    weeks += json.load(open(os.path.join(H, f)))['weeks']
weeks.sort(key=lambda w: w['week'])
posts = {p['id']: p for w in weeks for p in w['posts']}

extra = {'posts': [], 'emails': []}
if os.path.exists(os.path.join(H, 'extra.json')):
    extra = json.load(open(os.path.join(H, 'extra.json')))
for p in extra.get('posts', []):
    posts[p['id']] = p          # new pieces and replacements win
story_over = {x['id']: x for x in extra.get('stories', [])}
for w in weeks:
    w['stories'] = [story_over.get(x['id'], x) for x in w['stories']]
emails = {}
for e in extra.get('emails', []):
    emails.setdefault(int(e['week']), []).append(e)

sel = json.load(open(os.path.join(H, 'selection.json')))['weeks']
STORY_PRI = ['greeting', 'question', 'link', 'quiz', 'poll', 'countdown', 'testimonial', 'prompt', 'explainer', 'bts', 'recap']

out_weeks = []
for w in weeks:
    monday = datetime.date.fromisoformat(w['posts'][0]['date']) - datetime.timedelta(days=DAYS.index(w['posts'][0]['day']))
    chosen = []
    for pid, day in sel[str(w['week'])]:
        p = dict(posts[pid])
        p['day'] = day
        p['date'] = (monday + datetime.timedelta(days=DAYS.index(day))).isoformat()
        p['where'] = 'IG + FB'
        chosen.append(p)
    st = list(w['stories'])
    st.sort(key=lambda s: STORY_PRI.index(s['type']) if s['type'] in STORY_PRI else 99)
    keep = st[:2]
    keep.sort(key=lambda s: DAYS.index(s['day']) if s['day'] in DAYS else 9)
    out_weeks.append({**{k: w[k] for k in ('week', 'theme', 'dates')}, 'posts': chosen,
                      'stories': keep, 'emails': emails.get(w['week'], [])})

img = {}
for n in ['bush', 'founders', 'bruise', 'shoulder', 'ankle']:
    img[n] = 'data:image/jpeg;base64,' + base64.b64encode(open(f'{H}/small/{n}.jpg', 'rb').read()).decode()
for n in ['range', 'icon', 'logo']:
    img[n] = 'data:image/png;base64,' + base64.b64encode(open(f'{H}/small/{n}.png', 'rb').read()).decode()
data = json.dumps({'weeks': out_weeks}, ensure_ascii=False).replace('</', '<\\/')
t = open(f'{H}/template.html').read()
out = t.replace('__DATA__', data).replace('__IMG__', json.dumps(img))
open(f'{H}/xzone-summer-calendar.html', 'w').write(out)
print('weeks', len(out_weeks), 'posts', sum(len(w['posts']) for w in out_weeks),
      'stories', sum(len(w['stories']) for w in out_weeks),
      'emails', sum(len(w['emails']) for w in out_weeks), 'bytes', len(out))
