"""13 email designs in the approved social style. Copy comes from calendar/extra.json; the per-email
choices (hook headline, highlight, photo, review) are set by hand in E below."""
import json, re, html, os, sys
OUT, EXTRA = sys.argv[1], sys.argv[2]
B = {'founders': '02e558eca951173a5ebb2af8f459a960', 'logo': '25197b28f4e73a8b274a5afe746a93c6', 'ankle': 'f607cd51a5bb2629d7f6c5893b16d228',
     'shoulder': '6c462ddd8d677371819572e77b5cec30', 'range': '274593319a3db54845362f5e4a374066', 'bush': 'ca1622b259e43296a606a6f48ca34f0a',
     'cricket': '11a7cd58a4080325358b6129ce7498e9', 'aoraki': '05eb395fa63417fa9b52a0a72b64d79a', 'bushwalk': '1e3be30ec195c75a250fcea6bebb2c8e',
     'hands': '2904a9a5b12644007408ef19c33a72f3', 'handsclose': '9ee689101ce237ac8bd2bc2c81fbc0a1', 'running': '812990ea70541643834c6b3b08c76d9e'}
G, L = '#0D441F', '#E0E64A'
HEAD = "'Poppins', Arial, Helvetica, sans-serif"
BODY = "Arial, Helvetica, sans-serif"
REV = {
 'maria': {'title': 'Rub it on and forget', 'quote': 'I have found the X-Zone Joints product easy to use. I use it both for relieving aches and pains in my joints and for prevention support prior to hiking/tramping. It has been really effective. I am on my second bottle.', 'name': 'Maria G., New Zealand', 'product': 'Joints Rub'},
 'james': {'title': 'I was sceptical, but wow!', 'quote': 'I’m a runner that runs long distances. This stuff post run provides instant relief to sore muscles and speeds up recovery. Totally recommend.', 'name': 'James H., New Zealand', 'product': 'Sports Rub'},
 'philippa': {'title': 'By far better than anything else I’ve used.', 'quote': 'Gives instant and long lasting pain relief for my arthritis and calcific tendonitis. I highly recommend it.', 'name': 'Philippa C., New Zealand', 'product': 'Sports Roll-On'},
}
# id: hero hook ([[highlight]]), hero subline, photo, crop, review key (None keeps the plan's quote)
E = {
 'w1-email':  ('The summer kit [[most baches]] are missing', 'Plus our old prices, held until [date]', 'cricket', '58% 50%', None),
 'w2-email':  ('Christmas gifts, [[sorted by person]]', 'For the tradie, the tramper, the touch player and the gardener', 'founders', '50% 25%', None),
 'w3-email':  ('Will it arrive [[before Christmas]]?', 'Our last order dates, plus what goes wrong on day two of a tramp', 'aoraki', '50% 60%', None),
 'w4-email':  ('What every [[bach cupboard]] should hold', '[Offer] in our pre-Christmas sale', 'ankle', '50% 45%', None),
 'w5-email':  ('[[Meri Kirihimete]] from our whānau', 'Thank you for every jar, every message and every story', 'founders', '50% 20%', None),
 'w6-email':  ('Stiff joints this summer? [[Here is what helps]]', 'Three habits, the 10% rule, then the Joints Rub', 'hands', '50% 50%', 'maria'),
 'w7-email':  ('Why day two [[hurts more]] than day one', 'DOMS in plain English, and what the lab found', 'running', '55% 45%', None),
 'w8-email':  ('Heat or ice? [[The honest answer]]', 'It depends on how new the pain is', 'ankle', '50% 40%', None),
 'w9-email':  ("Tennis elbow [[isn't just tennis]]", 'Gripping, drilling, pruning and scrolling all count', 'shoulder', '50% 35%', None),
 'w10-email': ("The best recovery tool is free, and [[it's your bed]]", 'Three sleep habits, and when a medicine is behind the aches', 'bushwalk', '50% 45%', 'philippa'),
 'w11-email': ('The five minutes that [[save your long weekend]]', 'First aid, a quick warm-up and the Sports Rub', 'running', '45% 40%', 'james'),
 'w12-email': ('What smart [[sideline parents]] keep in the car', 'What to pack, and when to sit them out', 'cricket', '40% 50%', None),
 'w13-email': ('Thank you for a summer of [[learning with us]]', 'Now help us choose what we cover this autumn', 'bush', '50% 50%', None),
}
DAY = r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday):'
def ph(s):  # {PLACEHOLDER} -> [placeholder]
    return re.sub(r'\{([A-Z_]+)\}', lambda m: '[' + m.group(1).replace('_', ' ').lower() + ']', s)
def esc(s): return html.escape(ph(s))
def hl(t, green):
    t = esc(t)
    if green: return re.sub(r'\[\[(.+?)\]\]', rf'<span style="color: {L}">\1</span>', t)
    return re.sub(r'\[\[(.+?)\]\]', rf'<span style="background: linear-gradient(transparent 58%, {L} 58%); padding: 0 2px">\1</span>', t)
def paras(b, color='#26352a'):
    out = []
    for p in ph(b).split('\n\n'):
        p = p.strip()
        if not p: continue
        out.append(f'<p style="margin: 0 0 14px 0; font-family: {BODY}; font-size: 16px; line-height: 1.6; color: {color}">{html.escape(p).replace(chr(10), "<br>")}</p>')
    return ''.join(out)
def button(label, green):
    bg, fg = (L, G) if green else (G, '#ffffff')
    return f'<div style="display: inline-block; background: {bg}; color: {fg}; font-family: {HEAD}; font-weight: 700; font-size: 17px; padding: 16px 30px; border-radius: 999px">{esc(label)}</div>'

def email(e):
    hook, sub, photo, crop, rk = E[e['id']]
    green = e['type'] == 'campaign'
    band_bg, band_fg, lab_c, sub_c = (G, '#ffffff', L, 'rgba(255,255,255,0.86)') if green else ('#ffffff', G, G, 'rgba(13,68,31,0.82)')
    kind = 'Campaign' if green else 'Newsletter'
    secs = []
    for s in e['sections']:
        if re.match(r'This week on', s['h']):
            parts = re.split(DAY, ph(s['b']))
            rows = ''.join(f'<div style="display: flex; gap: 14px; padding: 12px 0; border-top: 1px solid #dde3d8"><div style="flex: none; width: 92px; font-family: {HEAD}; font-weight: 700; font-size: 14px; color: {G}; text-transform: uppercase; letter-spacing: 1px">{parts[i][:3]}</div><div style="font-family: {BODY}; font-size: 15px; line-height: 1.55; color: #26352a">{html.escape(parts[i+1].strip()[:1].upper() + parts[i+1].strip()[1:])}</div></div>' for i in range(1, len(parts) - 1, 2))
            secs.append(f'<div style="margin: 8px 32px 28px; background: #f3f5ef; border-radius: 16px; padding: 22px 24px 10px"><div style="font-family: {HEAD}; font-weight: 700; font-size: 13px; letter-spacing: 3px; text-transform: uppercase; color: {G}; margin-bottom: 8px">{esc(s["h"])}</div>{rows}</div>')
        else:
            secs.append(f'<div style="padding: 0 32px 12px"><h2 style="margin: 0 0 10px 0; font-family: {HEAD}; font-weight: 800; font-size: 24px; line-height: 1.2; color: {G}">{esc(s["h"])}</h2>{paras(s["b"])}</div>')
    rbg, rfg, rlab, rsub, rnote = (('#f3f5ef', G, G, 'rgba(13,68,31,0.85)', 'rgba(13,68,31,0.55)') if green else (G, '#ffffff', L, 'rgba(255,255,255,0.88)', 'rgba(255,255,255,0.6)'))
    if rk:
        r = REV[rk]
        review = (f'<div style="margin: 12px 0 0; background: {rbg}; padding: 34px 32px"><div style="font-family: {HEAD}; font-weight: 700; font-size: 12px; letter-spacing: 3px; text-transform: uppercase; color: {rlab}">In their words · {r["product"]}</div>'
                  f'<div style="margin-top: 12px; font-family: {HEAD}; font-weight: 800; font-size: 26px; line-height: 1.2; color: {rfg}">“{html.escape(r["title"])}</div>'
                  f'<div style="margin-top: 10px; font-family: {BODY}; font-size: 16px; line-height: 1.6; color: {rsub}">{html.escape(r["quote"])}”</div>'
                  f'<div style="margin-top: 14px; font-family: {BODY}; font-size: 14px; font-weight: 700; color: {rfg}">{html.escape(r["name"])} <span style="font-weight: 400; color: {rnote}">· Verified Judge.me review</span></div></div>')
    else:
        rv = e.get('review') or {}
        review = (f'<div style="margin: 12px 0 0; background: {rbg}; padding: 34px 32px"><div style="font-family: {HEAD}; font-weight: 700; font-size: 12px; letter-spacing: 3px; text-transform: uppercase; color: {rlab}">In their words</div>'
                  f'<div style="margin-top: 12px; font-family: {HEAD}; font-weight: 800; font-size: 26px; line-height: 1.2; color: {rfg}">“{esc(rv.get("quote", ""))}”</div>'
                  f'<div style="margin-top: 14px; font-family: {BODY}; font-size: 14px; font-weight: 700; color: {rfg}">{esc(rv.get("name", ""))}</div>'
                  f'<div style="margin-top: 10px; font-family: {BODY}; font-size: 12px; color: {rnote}">[Swap for the full Judge.me review, word for word]</div></div>')
    cta = e.get('cta') or {}
    ps = f'<div style="padding: 26px 32px 30px"><p style="margin: 0; font-family: {BODY}; font-size: 15px; line-height: 1.6; color: #4a5a4e"><b style="color: {G}">PS</b> {esc(e["ps"])}</p></div>' if e.get('ps') else ''
    if photo == 'range':
        hero_img = f'<div style="height: 360px; background: #f3f5ef; display: flex; align-items: center; justify-content: center"><img src="/_blob/{B[photo]}" alt="The X-ZONE range" style="height: 280px; width: auto"></div>'
    else:
        hero_img = f'<img src="/_blob/{B[photo]}" alt="" style="display: block; width: 600px; height: 380px; object-fit: cover; object-position: {crop}">'
    body = f'''<div style="width: 640px; background: #e9ece6; padding: 20px; box-sizing: border-box; font-family: {BODY}">
  <div style="background: #ffffff; border-radius: 14px; padding: 14px 18px; margin-bottom: 16px; display: flex; gap: 12px; align-items: center">
    <div style="width: 40px; height: 40px; border-radius: 50%; background: {G}; color: {L}; display: flex; align-items: center; justify-content: center; font-family: {HEAD}; font-weight: 800; font-size: 15px; flex: none">X</div>
    <div style="min-width: 0"><div style="font-size: 13px; color: #111"><b>X-ZONE New Zealand</b> <span style="color: #6b6b6b">· {kind}, week {e["week"]} · {e["day"]}</span></div>
    <div style="font-size: 14px; font-weight: 700; color: #111; margin-top: 2px">{esc(e["subject"])}</div>
    <div style="font-size: 13px; color: #6b6b6b; margin-top: 2px">{esc(e["preheader"])}</div></div>
  </div>
  <div style="width: 600px; background: #ffffff; overflow: hidden">
    <div style="padding: 22px 0; text-align: center; border-bottom: 3px solid {G}"><img src="/_blob/{B["logo"]}" alt="X-ZONE New Zealand" style="height: 34px; width: auto"></div>
    {hero_img}
    <div style="background: {band_bg}; padding: 34px 32px 36px">
      <div style="font-family: {HEAD}; font-weight: 700; font-size: 12px; letter-spacing: 3px; text-transform: uppercase; color: {lab_c}">{esc(e["title"])}</div>
      <h1 style="margin: 12px 0 0 0; font-family: {HEAD}; font-weight: 800; font-size: 38px; line-height: 1.1; color: {band_fg}">{hl(hook, green)}</h1>
      <p style="margin: 12px 0 24px 0; font-family: {BODY}; font-size: 17px; line-height: 1.5; color: {sub_c}">{esc(sub)}</p>
      {button(cta.get("label", "Shop now"), green)}
    </div>
    <div style="height: 30px"></div>
    {''.join(secs)}
    <div style="padding: 6px 32px 30px">{button(cta.get("label", "Shop now"), False)}</div>
    {review}
    {ps}
    <div style="background: {G}; padding: 30px 32px; text-align: center">
      <div style="display: inline-block; background: #ffffff; border-radius: 999px; padding: 10px 22px"><img src="/_blob/{B["logo"]}" alt="X-ZONE New Zealand" style="height: 26px; width: auto; display: block"></div>
      <div style="margin-top: 14px; font-family: {HEAD}; font-weight: 800; font-size: 18px; color: #ffffff">Move Freely. <span style="color: {L}">Live Naturally.</span></div>
      <div style="margin-top: 10px; font-family: {BODY}; font-size: 13px; color: rgba(255,255,255,0.8)">Instagram · Facebook · xzone.nz</div>
      <div style="margin-top: 14px; font-family: {BODY}; font-size: 11px; line-height: 1.5; color: rgba(255,255,255,0.6)">[Business address] · You are getting this because you signed up at xzone.nz · Unsubscribe</div>
    </div>
  </div>
</div>'''
    return body

def page(title, body, h):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap">
<style>
body{{margin:0}}
a{{color:#0D441F}}a:hover{{color:#0a3318}}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":640,"height":{h}}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{}};
  }}
}}
</script>
</body>
</html>
'''
H = json.load(open(os.path.join(OUT, '_heights.json'))) if os.path.exists(os.path.join(OUT, '_heights.json')) else {}
emails = json.load(open(EXTRA))['emails']
for e in emails:
    n = 'Email-W%02d' % e['week']
    open(os.path.join(OUT, n + '.dc.html'), 'w').write(page(f"Week {e['week']} email: {e['title']}", email(e), H.get(n, 3000)))
print(len(emails), 'emails written')
