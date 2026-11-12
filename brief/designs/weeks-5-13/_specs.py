"""Weeks 5-13 designs, one spec per piece (copy, highlight, photo, crop and look chosen by hand).
Layouts are the same markup as the approved Round 2 pieces and the weeks 1-4 designs."""
import os, re, sys, html
OUT = sys.argv[1]
B = {'founders': '02e558eca951173a5ebb2af8f459a960', 'logo': '25197b28f4e73a8b274a5afe746a93c6', 'ankle': 'f607cd51a5bb2629d7f6c5893b16d228',
     'shoulder': '6c462ddd8d677371819572e77b5cec30', 'bruise': '596e0c6c60466b5fd12b38c0f20574e2', 'range': '274593319a3db54845362f5e4a374066',
     'bush': 'ca1622b259e43296a606a6f48ca34f0a', 'cricket': '11a7cd58a4080325358b6129ce7498e9', 'aoraki': '05eb395fa63417fa9b52a0a72b64d79a',
     'bushwalk': '1e3be30ec195c75a250fcea6bebb2c8e', 'hands': '2904a9a5b12644007408ef19c33a72f3', 'handsclose': '9ee689101ce237ac8bd2bc2c81fbc0a1',
     'running': '812990ea70541643834c6b3b08c76d9e',
     'jess-dan-tees': '2e0053c0b4994ed2020b08b26ac36ac4', 'jess-dan-garden': '5de84cca1ac1924820cfab3106c42c36', 'relief-rub-back': '9f42f545745a082ee90e54e2cc819e60', 'relief-rub-knee': 'ca3321f82a43b6dc05a049d31167d483', 'relief-rub-leg': '7c4dc8163ed84ea819baf23ffaaaa973', 'sports-rub-gym': '687c3ea396d216bafa56dd82643c01fb', 'sports-spray-arm': 'a26ba0467a35ce72edfcbec2cb642c42', 'sports-spray-knee': 'ab98e6ec43549b66058b8cdfea34bb44', 'elder-mountains': '8caed02fc06dd4ddf8d2e1dee55131bd', 'couple-waterfront': 'd0b2e8e3b820d5b039531894ca213520', 'family-deck': 'b6548a31b3bdb9010a2488b8d3d6a66e', 'mollie': 'd6f4ed7c106a6a841dd33259362017c8'}
ALT = {'founders': 'Jess and Dan sitting by a stream in the bush', 'ankle': 'A roll-on being applied to a sore ankle', 'shoulder': 'Hands massaging rub into a sore shoulder',
       'bruise': 'A bruised knee', 'range': 'The X-ZONE range of rubs, sprays and roll-ons', 'bush': 'A waterfall and river through native bush',
       'cricket': 'A family playing backyard cricket', 'aoraki': 'A walker on the Hooker Valley track below Aoraki', 'bushwalk': 'Walkers on a boardwalk through mossy native bush',
       'hands': 'An older man rubbing the joints of his hand', 'handsclose': 'Older hands massaging a stiff thumb joint', 'running': 'Two people running on the Auckland waterfront',
       'jess-dan-tees': 'Jess and Dan in X-ZONE t-shirts', 'jess-dan-garden': 'Jess and Dan with native plants in their garden', 'relief-rub-back': 'Relief Rub being massaged into a lower back', 'relief-rub-knee': 'Relief Rub on a grazed knee', 'relief-rub-leg': 'Relief Rub being applied to a leg', 'sports-rub-gym': 'Sports Rub being massaged into a thigh at the gym', 'sports-spray-arm': 'Sports Spray on a forearm', 'sports-spray-knee': 'Sports Spray on a knee', 'elder-mountains': 'An older man in a beanie with mountains behind', 'couple-waterfront': 'A couple resting on the waterfront after a run', 'family-deck': 'A family playing with a rugby ball on their deck', 'mollie': 'Mollie Allison serving on a sand court, in a New Zealand top'}
G, L, N = '#0D441F', '#E0E64A', '#131D4A'
def src(k): return f'/_blob/{B[k]}'
def hl(text, mode):
    def rep(m):
        t = m.group(1)
        if mode == 'lime': return f'<span style="color: {L}">{t}</span>'
        if mode == 'white': return f'<span style="background: linear-gradient(transparent 58%, #ffffff 58%); padding: 0 4px">{t}</span>'
        return f'<span style="background: linear-gradient(transparent 58%, {L} 58%); padding: 0 4px">{t}</span>'
    return re.sub(r'\[\[(.+?)\]\]', rep, text)
def page(title, w, h, body, link='#0D441F', hover='#0a3318'):
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
a{{color:{link}}}a:hover{{color:{hover}}}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{}};
  }}
}}
</script>
</body>
</html>
'''
LOGO_PILL = lambda top, left, hgt=36, pad='16px 30px': f'<div style="position: absolute; left: {left}px; top: {top}px; background: #ffffff; border-radius: 999px; padding: {pad}; display: flex; align-items: center"><img src="{src("logo")}" alt="X-ZONE New Zealand" style="height: {hgt}px; width: auto"></div>'
PLAY = lambda c: f'<svg width="56" height="56" viewBox="0 0 56 56" fill="none" aria-hidden="true"><circle cx="28" cy="28" r="26.5" stroke="{c}" stroke-width="3"/><path d="M23 18.5 39 28l-16 9.5v-19Z" fill="{c}"/></svg>'
LINK_ICON = f'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1" stroke="{G}" stroke-width="2.4" stroke-linecap="round"/></svg>'

def band_colors(band, ink=G):
    if band == 'green': return G, '#ffffff', L, 'rgba(255,255,255,0.86)', 'lime'
    if band == 'lime': return L, G, G, 'rgba(13,68,31,0.88)', 'white'
    return '#ffffff', ink, ink, ('rgba(19,29,74,0.8)' if ink == N else 'rgba(13,68,31,0.85)'), 'hl'

def footer(band, ink, left=''):
    logo = (f'<div style="background: #ffffff; border-radius: 999px; padding: 14px 28px; display: flex; align-items: center"><img src="{src("logo")}" alt="X-ZONE New Zealand" style="height: 34px; width: auto"></div>'
            if band == 'green' else f'<img src="{src("logo")}" alt="X-ZONE New Zealand" style="height: 40px; width: auto">')
    return f'<div style="margin-top: auto; display: flex; align-items: center; justify-content: {"space-between" if left else "flex-end"}">{left}{logo}</div>'

def pill(text, bg, fg):
    return f'<div style="background: {bg}; color: {fg}; border-radius: 999px; padding: 12px 26px; font-size: 24px; font-weight: 700">{html.escape(text)}</div>'

def photo_block(k, crop, h, logo=False):
    if k == 'range':
        inner = f'<img src="{src(k)}" alt="{ALT[k]}" style="height: {int(h*0.7)}px; width: auto">'
        return f'<div style="position: relative; width: 1080px; height: {h}px; flex-shrink: 0; background: #f3f5ef; display: flex; align-items: center; justify-content: center">{inner}{LOGO_PILL(56,64) if logo else ""}</div>'
    return f'<div style="position: relative; width: 1080px; height: {h}px; flex-shrink: 0"><img src="{src(k)}" alt="{ALT[k]}" style="width: 100%; height: 100%; object-fit: cover; object-position: {crop}">{LOGO_PILL(56,64) if logo else ""}</div>'

def carousel(s):
    bg, fg, labc, subc, mode = band_colors(s['band'], s.get('ink', G))
    on, off = (L, 'rgba(255,255,255,0.35)') if s['band'] == 'green' else (fg, 'rgba(13,68,31,0.25)')
    dots = ''.join(f'<span style="width: 16px; height: 16px; border-radius: 50%; background: {on if i == 0 else off}"></span>' for i in range(s['dots']))
    arrow = L if s['band'] == 'green' else fg
    swipe = f'<div style="display: flex; align-items: center; gap: 14px; color: {fg}; font-size: 26px; font-weight: 600"><span>Swipe</span><svg width="34" height="34" viewBox="0 0 36 36" fill="none" aria-hidden="true"><path d="M6 18h23M29 18l-9-9M29 18l-9 9" stroke="{arrow}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
    body = f'''<div style="position: relative; width: 1080px; height: 1350px; overflow: hidden; background: {bg}; font-family: 'Poppins', sans-serif; box-sizing: border-box; display: flex; flex-direction: column">
  {photo_block(s['photo'], s.get('crop', '50% 50%'), 700, logo=True)}
  <div style="flex: 1; padding: 56px 80px 52px 80px; display: flex; flex-direction: column; gap: 22px; box-sizing: border-box">
    <div style="color: {labc}; font-size: 26px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase">{s['label']}</div>
    <h1 style="margin: 0; color: {fg}; font-size: {s.get('size', 78)}px; line-height: 1.06; font-weight: 800">{hl(s['h'], mode)}</h1>
    <p style="margin: 0; color: {subc}; font-size: 33px; line-height: 1.45; font-weight: 500">{s['sub']}</p>
    <div style="margin-top: auto; display: flex; align-items: center; justify-content: space-between">{swipe}<div style="display: flex; gap: 12px">{dots}</div></div>
  </div>
</div>'''
    return page(s['title'], 1080, 1350, body, L if s['band'] == 'green' else fg)

def single(s):
    bg, fg, labc, subc, mode = band_colors(s['band'], s.get('ink', G))
    rows = s.get('rows')
    ph = 600 if rows else 700
    mid = ''
    if rows:
        bar = L if s['band'] == 'green' else fg
        mid = '<div style="display: flex; flex-direction: column; gap: 16px; margin-top: 6px">' + ''.join(
            f'<div style="border-left: 6px solid {bar}; padding-left: 22px; color: {fg}; font-size: 30px; line-height: 1.35; font-weight: 500"><b style="font-weight: 700">{b}</b> · {t}</div>' for b, t in rows) + '</div>'
    else:
        mid = f'<p style="margin: 0; color: {subc}; font-size: 33px; line-height: 1.45; font-weight: 500">{s["sub"]}</p>'
    left = ''
    if s.get('pill'):
        left = pill(s['pill'], L if s['band'] == 'green' else G, G if s['band'] == 'green' else L)
    body = f'''<div style="position: relative; width: 1080px; height: 1350px; overflow: hidden; background: {bg}; font-family: 'Poppins', sans-serif; box-sizing: border-box; display: flex; flex-direction: column">
  {photo_block(s['photo'], s.get('crop', '50% 50%'), ph)}
  <div style="flex: 1; padding: {"52px 80px 50px" if rows else "56px 80px 52px"} 80px; display: flex; flex-direction: column; gap: 22px; box-sizing: border-box">
    <div style="color: {labc}; font-size: 26px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase">{s['label']}</div>
    <h1 style="margin: 0; color: {fg}; font-size: {s.get('size', 76)}px; line-height: 1.06; font-weight: 800">{hl(s['h'], mode)}</h1>
    {mid}
    {footer(s['band'], fg, left)}
  </div>
</div>'''
    return page(s['title'], 1080, 1350, body, L if s['band'] == 'green' else fg)

def reel_a(s):
    body = f'''<div style="position: relative; width: 1080px; height: 1920px; overflow: hidden; background: {G}; font-family: 'Poppins', sans-serif; box-sizing: border-box">
  <img src="{src(s['photo'])}" alt="{ALT[s['photo']]}" style="position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; object-position: {s.get('crop', '50% 50%')}">
  <div style="position: absolute; left: 0; right: 0; bottom: 0; height: 1150px; background: linear-gradient(180deg, rgba(13,68,31,0) 0%, rgba(13,68,31,0.55) 45%, rgba(13,68,31,0.96) 100%)"></div>
  {LOGO_PILL(150, 72, 42, '18px 34px')}
  <div style="position: absolute; left: 72px; right: 72px; bottom: 400px; display: flex; flex-direction: column; align-items: flex-start; gap: 34px">
    <div style="background: {L}; color: {G}; border-radius: 999px; padding: 14px 30px; font-size: 27px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase">{s['tag']}</div>
    <h1 style="margin: 0; color: #ffffff; font-size: {s.get('size', 98)}px; line-height: 1.07; font-weight: 800">{hl(s['h'], 'lime')}</h1>
    <p style="margin: 0; color: rgba(255,255,255,0.88); font-size: 37px; line-height: 1.4; font-weight: 500">{s['sub']}</p>
    <div style="display: flex; align-items: center; gap: 20px; color: #ffffff; font-size: 30px; font-weight: 600; margin-top: 6px">{PLAY(L)}<span>{s['watch']}</span></div>
  </div>
</div>'''
    return page(s['title'], 1080, 1920, body, L, '#ffffff')

def reel_b(s):
    ink = s.get('ink', G)
    body = f'''<div style="position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #ffffff; font-family: 'Poppins', sans-serif; box-sizing: border-box; display: flex; flex-direction: column">
  <div style="position: relative; width: 1080px; height: 1000px; flex-shrink: 0">
    <img src="{src(s['photo'])}" alt="{ALT[s['photo']]}" style="width: 100%; height: 100%; object-fit: cover; object-position: {s.get('crop', '50% 50%')}">
    {LOGO_PILL(150, 72, 42, '18px 34px')}
  </div>
  <div style="padding: 64px 72px 0 72px; display: flex; flex-direction: column; align-items: flex-start; gap: 30px">
    <div style="background: {ink}; color: {L}; border-radius: 999px; padding: 14px 30px; font-size: 27px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase">{s['tag']}</div>
    <h1 style="margin: 0; color: {ink}; font-size: {s.get('size', 90)}px; line-height: 1.08; font-weight: 800">{hl(s['h'], 'hl')}</h1>
    <p style="margin: 0; color: rgba(13,68,31,0.8); font-size: 36px; line-height: 1.4; font-weight: 500">{s['sub']}</p>
    <div style="display: flex; align-items: center; gap: 20px; color: {ink}; font-size: 30px; font-weight: 600; margin-top: 4px">{PLAY(ink)}<span>{s['watch']}</span></div>
  </div>
</div>'''
    return page(s['title'], 1080, 1920, body, ink)

def sticker(st, shadow=False):
    if not st: return ''
    sh = 'box-shadow: 0 24px 60px rgba(13,68,31,0.22); ' if shadow else ''
    kind = st[0]
    if kind == 'q':
        return f'<div style="width: 780px; {sh}background: #ffffff; border-radius: 36px; padding: 40px 48px; box-sizing: border-box; display: flex; flex-direction: column; gap: 18px; text-align: center"><div style="font-size: 36px; font-weight: 700; color: {G}">{st[1]}</div><div style="background: #f1f3ef; border-radius: 20px; padding: 26px; font-size: 32px; font-weight: 500; color: #5f6b62">Type your question</div></div>'
    if kind == 'poll':
        opts = st[1]
        rows = ''.join(f'<div style="padding: 34px 48px; font-size: 38px; font-weight: 600; color: {G}; {"border-bottom: 2px solid #E8E8E8; " if i < len(opts) - 1 else ""}text-align: center">{o}</div>' for i, o in enumerate(opts))
        return f'<div style="width: 760px; {sh}background: #ffffff; border-radius: 36px; overflow: hidden; display: flex; flex-direction: column">{rows}</div>'
    if kind == 'link':
        return f'<div style="{sh}background: #ffffff; border-radius: 999px; padding: 26px 48px; display: flex; align-items: center; gap: 18px; color: {G}; font-size: 36px; font-weight: 700; white-space: nowrap">{LINK_ICON}<span>{st[1]}</span></div>'
    return ''

def story_a(s):
    body = f'''<div style="position: relative; width: 1080px; height: 1920px; overflow: hidden; background: {G}; font-family: 'Poppins', sans-serif; box-sizing: border-box">
  <img src="{src(s['photo'])}" alt="{ALT[s['photo']]}" style="position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; object-position: {s.get('crop', '50% 50%')}">
  <div style="position: absolute; left: 0; right: 0; top: 0; height: 440px; background: linear-gradient(180deg, rgba(13,68,31,0.8) 0%, rgba(13,68,31,0) 100%)"></div>
  <div style="position: absolute; left: 0; right: 0; bottom: 0; height: 1250px; background: linear-gradient(180deg, rgba(13,68,31,0) 0%, rgba(13,68,31,0.72) 55%, rgba(13,68,31,0.96) 100%)"></div>
  <div style="position: absolute; left: 0; right: 0; top: 130px; display: flex; justify-content: center"><div style="background: #ffffff; border-radius: 999px; padding: 16px 32px; display: flex; align-items: center"><img src="{src("logo")}" alt="X-ZONE New Zealand" style="height: 38px; width: auto"></div></div>
  <div style="position: absolute; left: 90px; right: 90px; bottom: 220px; display: flex; flex-direction: column; align-items: center; gap: 52px">
    <h1 style="margin: 0; color: #ffffff; font-size: {s.get('size', 92)}px; line-height: 1.1; font-weight: 800; text-align: center">{hl(s['h'], 'lime')}</h1>
    {sticker(s.get('st'))}
    {f'<p style="margin: 0; color: rgba(255,255,255,0.9); font-size: 31px; line-height: 1.45; font-weight: 500; text-align: center; max-width: 780px">{s["line"]}</p>' if s.get('line') else ''}
  </div>
</div>'''
    return page(s['title'], 1080, 1920, body, L, '#ffffff')

def story_c(s):
    k = s['photo']
    if k == 'range':
        card = f'<div style="width: 920px; height: 900px; border-radius: 40px; overflow: hidden; background: #f3f5ef; display: flex; align-items: center; justify-content: center"><img src="{src(k)}" alt="{ALT[k]}" style="width: 820px; height: auto"></div>'
    else:
        card = f'<div style="width: 920px; height: 900px; border-radius: 40px; overflow: hidden"><img src="{src(k)}" alt="{ALT[k]}" style="width: 100%; height: 100%; object-fit: cover; object-position: {s.get("crop", "50% 50%")}"></div>'
    st = s.get('st')
    if st and st[0] == 'poll':
        over = f'<div style="position: absolute; left: 80px; bottom: 0">{sticker(st, True)}</div>'
        boxh = 900 + 60 + 130 * len(st[1]) // 2
    elif st:
        over = f'<div style="position: absolute; left: 50%; bottom: 40px; transform: translateX(-50%)">{sticker(st, True)}</div>'
        boxh = 1000
    else:
        over, boxh = '', 900
    body = f'''<div style="position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #ffffff; font-family: 'Poppins', sans-serif; box-sizing: border-box; padding: 140px 80px 0 80px; display: flex; flex-direction: column; gap: 48px">
  <div style="display: flex; align-items: center; justify-content: space-between">
    <img src="{src("logo")}" alt="X-ZONE New Zealand" style="height: 46px; width: auto">
    <div style="background: {G}; color: #ffffff; border-radius: 999px; padding: 14px 30px; font-size: 26px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase">{s['tag']}</div>
  </div>
  <h1 style="margin: 20px 0 0 0; color: {G}; font-size: {s.get('size', 96)}px; line-height: 1.07; font-weight: 800">{hl(s['h'], 'hl')}</h1>
  <div style="position: relative; width: 920px; height: {boxh}px; flex-shrink: 0">{card}{over}</div>
  {f'<p style="margin: 10px 0 0 0; color: rgba(13,68,31,0.8); font-size: 33px; line-height: 1.45; font-weight: 500; text-align: center">{s["line"]}</p>' if s.get('line') else ''}
</div>'''
    return page(s['title'], 1080, 1920, body)

SPECS = {
 # ---------------- week 5: Christmas, koromiko
 'W5-Mon': (single, dict(title='Week 5 Monday post: koromiko', band='white', photo='bushwalk', crop='35% 50%', label='Herb 5 of 11 · Koromiko', size=82,
            h='The herb your [[grandmother]] already knew', sub='Koromiko, in our Relief range.')),
 'W5-Wed': (reel_b, dict(title='Week 5 Wednesday Reel: Christmas cricket warm-up', photo='cricket', crop='60% 50%', tag='Christmas cricket',
            h='The Christmas cricket [[warm-up]] nobody does', sub='Twenty seconds before you bowl your first over.', watch='Watch the 20-second warm-up')),
 'W5-Fri': (single, dict(title='Week 5 Saturday post: Boxing Day recovery', band='green', photo='relief-rub-back', crop='50% 45%', label='Boxing Day · Recovery guide', size=74,
            h='Is your Boxing Day ache actually [[thirst]]?', rows=[('Water first', 'a big glass, then sip all day'), ('Then move', 'a gentle walk or a swim'), ('Rub before bed', 'then let sleep do the work')])),
 'W5-Story-1': (story_a, dict(title='Week 5 story: Meri Kirihimete', photo='jess-dan-tees', crop='50% 22%', h='[[Meri Kirihimete]] from our whānau to yours', size=96,
            line='Thank you for a big year. Ngā mihi, Jess and Dan.')),
 'W5-Story-2': (story_c, dict(title='Week 5 story: Boxing Day guide link', photo='running', crop='55% 50%', tag='Boxing Day', h='Water, movement, [[sleep]]. In that order.',
            st=('link', 'Read the recovery guide'), line='Our Boxing Day recovery guide is on the feed.')),
 # ---------------- week 6: New Year, pūriri
 'W6-Mon': (carousel, dict(title='Week 6 Monday carousel: January injuries', band='green', photo='aoraki', crop='50% 60%', label='New year, new start', dots=7,
            h='Why so many of us get [[hurt in January]]', sub='Too much, too soon. Swipe for the 10% rule.')),
 'W6-Wed': (reel_a, dict(title='Week 6 Wednesday Reel: pūriri', photo='bush', crop='20% 50%', tag='Herb 6 of 11 · Pūriri',
            h="The tree New Zealand's [[biggest moth]] calls home", sub='Pūriri, in our Sports range.', watch='Watch · 20 seconds')),
 'W6-Fri': (single, dict(title='Week 6 Friday post: recovery routine', band='lime', photo='running', crop='55% 45%', label='Recovery · Three habits', size=72,
            h='The 2027 recovery routine we [[actually stick to]]', rows=[('Two easy days', 'walk, swim or stretch'), ('Seven hours plus', 'when muscles repair'), ('Massage sore spots', 'a few minutes, a little rub')])),
 'W6-Story-1': (story_c, dict(title='Week 6 story: stockist of the week, Nelson', photo='range', tag='Stockist of the week', h='Find us in [[Nelson]]',
            st=('link', '[Stockist name], Nelson'), line='Over 200 stockists across Aotearoa.')),
 'W6-Story-2': (story_a, dict(title='Week 6 story: recovery routine link', photo='couple-waterfront', crop='45% 50%', h='Three habits for a [[better 2027]]',
            st=('link', 'See the routine'), line='Small, steady and free.')),
 # ---------------- week 7: DOMS, rātā
 'W7-Mon': (carousel, dict(title='Week 7 Monday carousel: DOMS', band='white', photo='sports-rub-gym', crop='50% 50%', label='Sports range · Recovery science', dots=7, size=84,
            h='Why you hurt [[two days later]]', sub='DOMS explained, without the jargon.')),
 'W7-Wed': (reel_b, dict(title='Week 7 Wednesday Reel: rātā', photo='bushwalk', crop='70% 40%', tag='Herb 7 of 11 · Rātā',
            h='The [[red tree]] that lights up the summer forest', sub='Rātā, in our Relief range.', watch='Watch · 20 seconds')),
 'W7-Fri': (single, dict(title='Week 7 Friday post: the lab results', band='green', photo='range', label='Independent lab tests · Trinity Bioactives', size=70,
            h='We sent our rubs to a lab. Here is [[what happened]]', rows=[('Tested', 'our three rubs, on cells linked to inflammation'), ('Found', 'Sports 54%, Joints 48%, Relief 43% fewer'), ('Means', 'a promising lab result, not a clinical trial')])),
 'W7-Story-1': (story_a, dict(title='Week 7 story: what hurts this week', photo='jess-dan-garden', crop='50% 30%', h='What hurts [[this week]]?',
            st=('q', 'Ask Jess and Dan'), line='Back at work, back at training. Ask away.')),
 'W7-Story-2': (story_c, dict(title='Week 7 story: stockist of the week, Dunedin', photo='range', tag='Stockist of the week', h='Find us in [[Dunedin]]',
            st=('link', '[Stockist name], Dunedin'), line='Over 200 stockists across Aotearoa.')),
 # ---------------- week 8: joints, pukatea
 'W8-Mon': (carousel, dict(title='Week 8 Monday carousel: the stiff-joint duo', band='white', ink='#131D4A', photo='handsclose', crop='45% 50%', label='Joints range', dots=7, size=78,
            h='The stiff-joint duo: [[one inside, one outside]]', sub='Turmeric in the kitchen, the Joints Rub on the joint.')),
 'W8-Wed': (reel_b, dict(title='Week 8 Wednesday Reel: pukatea', photo='bush', crop='80% 50%', tag='Herb 8 of 11 · Pukatea',
            h='The swamp giant with [[roots like walls]]', sub='Pukatea, in our Joints and Sports ranges.', watch='Watch · 20 seconds')),
 'W8-Fri': (single, dict(title='Week 8 Friday post: heat or ice', band='green', photo='ankle', crop='50% 45%', label='First aid', size=80,
            h='Heat or ice? [[The honest answer]]', rows=[('Ice', 'new knocks and swelling, first 48 hours'), ('Heat', 'tight muscles and old aches'), ('Joints', 'usually warm, unless hot and swollen')])),
 'W8-Story-1': (story_a, dict(title='Week 8 story: joint questions', photo='hands', crop='50% 50%', h='Stiff knees? [[Sore hands]]?',
            st=('q', 'Ask us about joints, heat or ice'), line='Jess and Dan read every question.')),
 'W8-Story-2': (story_c, dict(title='Week 8 story: stockist of the week, Christchurch', photo='range', tag='Stockist of the week', h='Find us in [[Christchurch]]',
            st=('link', '[Stockist name], Christchurch'), line='Over 200 stockists across Aotearoa.')),
 # ---------------- week 9: tradies, kahikatea
 'W9-Mon': (carousel, dict(title="Week 9 Monday carousel: a tradie's back", band='green', photo='relief-rub-back', crop='50% 40%', label='Tradie week', dots=7, size=78,
            h="Five free habits that save a [[tradie's back]]", sub='None of them cost a cent.')),
 'W9-Wed': (reel_a, dict(title='Week 9 Wednesday Reel: kahikatea', photo='aoraki', crop='45% 50%', tag='Herb 9 of 11 · Kahikatea',
            h="Why New Zealand's [[tallest tree]] is in our Relief range", sub='Kahikatea, the white pine.', watch='Watch · 22 seconds', size=92)),
 'W9-Fri': (single, dict(title='Week 9 Friday post: worksite injuries', band='white', photo='sports-spray-arm', crop='50% 50%', label='Tradie week · Sports range', size=74,
            h='The three injuries every [[worksite]] hands out', rows=[('Lower back', 'warm up, keep loads close'), ('Tennis elbow', 'ease the grip, massage the forearm'), ('Shoulders', 'break up overhead work')])),
 'W9-Story-1': (story_a, dict(title='Week 9 story: worksite questions', photo='sports-spray-arm', crop='45% 50%', h='What hurts [[on your worksite]]?',
            st=('q', 'Ask Jess and Dan'), line='Backs, shoulders, knees. Ask away.')),
 'W9-Story-2': (story_c, dict(title='Week 9 story: site injuries link', photo='relief-rub-back', crop='50% 45%', tag='Tradie week', h='Three site injuries, [[sorted]]',
            st=('link', 'See what to do'), line='On the feed now.')),
 # ---------------- week 10: medication, tūpākihi
 'W10-Mon': (carousel, dict(title='Week 10 Monday carousel: medicines and muscle aches', band='white', photo='jess-dan-tees', crop='50% 25%', label='From the blog', dots=7, size=74,
            h='Could your medicine be making your [[muscles ache]]?', sub='Seven to know. Never stop one without your GP.')),
 'W10-Wed': (reel_a, dict(title='Week 10 Wednesday Reel: tūpākihi', photo='bush', crop='50% 50%', tag='Herb 10 of 11 · Tūpākihi',
            h='The native herb [[almost nobody]] has heard of', sub='Tūpākihi, in our Joints Rub.', watch='Watch · 23 seconds')),
 'W10-Fri': (single, dict(title='Week 10 Friday post: sleep', band='lime', photo='bushwalk', crop='50% 40%', label='Recovery science', size=72,
            h="The best recovery tool is free, and [[it's your bed]]", rows=[('Same wake time', 'weekends too'), ('Cool, dark, quiet', 'phone out of reach'), ('Wind down', 'screens off, a slow massage')])),
 'W10-Story-1': (story_a, dict(title='Week 10 story: sleep poll', photo='aoraki', crop='50% 50%', h='How many hours did you [[sleep]] last night?',
            st=('poll', ['Under 7', '7 or more']), line='On Friday: why sleep beats any product.')),
 'W10-Story-2': (story_a, dict(title="Week 10 story: Mollie's story link", photo='mollie', crop='50% 25%', h="Mollie's story, and the [[Sports range]]",
            st=('link', "Read Mollie's story"), line='')),
 # ---------------- week 11: Waitangi, karaeo
 'W11-Mon': (carousel, dict(title='Week 11 Monday carousel: all eleven herbs', band='green', photo='bush', crop='35% 50%', label='Herb 11 of 11 · Karaeo', dots=7, size=78,
            h='Herb eleven, and the [[full set]] in one swipe', sub='Karaeo, plus where each of the eleven lives.')),
 'W11-Wed': (reel_a, dict(title='Week 11 Wednesday Reel: walk the bush', photo='bushwalk', crop='40% 55%', tag='Founders',
            h='Walk the bush with us and [[name every herb]]', sub='Jess names the herbs as she walks.', watch='Watch · 30 seconds')),
 'W11-Fri': (single, dict(title='Week 11 Friday post: long weekend first aid', band='white', photo='ankle', crop='50% 40%', label='Long weekend · Relief range', size=76,
            h='The [[first 48 hours]] decide your long weekend', rows=[('Rolled ankle', 'rest, ice, compress, raise'), ('Bumps and bruises', 'cold first, then massage'), ('Stiff after the drive', 'stop every two hours')])),
 'W11-Story-1': (story_a, dict(title='Week 11 story: herb questions', photo='jess-dan-garden', crop='45% 30%', h='Curious about [[our eleven herbs]]?',
            st=('q', 'Ask Jess and Dan'), line='Where they grow, and why we use them.')),
 'W11-Story-2': (story_a, dict(title='Week 11 story: Waitangi Day', photo='aoraki', crop='55% 40%', h='Ngā mihi o [[Te Rā o Waitangi]]', size=96,
            line='From Jess, Dan and the X-ZONE whānau.')),
 # ---------------- week 12: school and sidelines
 'W12-Mon': (carousel, dict(title='Week 12 Monday carousel: every herb in one post', band='white', photo='jess-dan-garden', crop='50% 30%', label='Herb guide', dots=7, size=82,
            h='Every native herb we use, [[in one post]]', sub='All eleven, and where you will find them. Save it.')),
 'W12-Wed': (reel_b, dict(title='Week 12 Wednesday Reel: 20-second warm-up', photo='sports-spray-knee', crop='50% 50%', tag='Warm-up',
            h='Twenty seconds your [[ankles]] will thank you for', sub='Netball and rugby. Ankles and knees first.', watch='Watch the 20-second warm-up')),
 'W12-Fri': (single, dict(title='Week 12 Friday post: the sideline kit', band='green', photo='family-deck', crop='55% 50%', label='Back to school · Relief range', size=72,
            h='What smart [[sideline parents]] keep in the car', rows=[('In the bag', 'water, ice pack, bandage'), ('On the knock', 'cold first, then massage'), ('Head knocks', 'off the field, see a doctor')])),
 'W12-Story-1': (story_c, dict(title='Week 12 story: name all eleven herbs', photo='bush', crop='40% 50%', tag='Challenge', h='Can you name [[all eleven]] of our native herbs?', size=88,
            st=('poll', ['Easy', "I'll need the post"]), line="Monday's post has every one.")),
 'W12-Story-2': (story_a, dict(title='Week 12 story: sideline kit link', photo='ankle', crop='50% 40%', h='The [[sideline kit]] for Saturday',
            st=('link', 'See the kit list'), line='Pack it once. Keep it in the car.')),
 # ---------------- week 13: review week
 'W13-Mon': (carousel, dict(title='Week 13 Monday carousel: most-saved posts', band='green', photo='range', label='Summer recap', dots=6, size=78,
            h='The twelve posts [[you saved most]] this summer', sub='The ones you kept, all in one place.')),
 'W13-Wed': (reel_a, dict(title="Week 13 Wednesday Reel: summer's most-watched", photo='bush', crop='65% 50%', tag='Summer recap',
            h='[[New hook for the most-watched Reel]]', sub='Our most-watched Reel of the summer.', watch='Watch it again', size=90)),
 'W13-Fri': (single, dict(title='Week 13 Friday post: most-asked questions', band='white', photo='jess-dan-tees', crop='50% 25%', label='Ask Jess and Dan', size=72,
            h='Your [[most-asked questions]], answered', rows=[('Which one?', 'Relief, Joints or Sports'), ('How much?', '1 to 5 ml, up to five times a day'), ('Kids?', 'Relief from five, the others from seven')])),
 'W13-Story-1': (story_c, dict(title='Week 13 story: autumn questions', photo='elder-mountains', crop='62% 45%', tag='Coming this autumn', h='What should we answer [[this autumn]]?',
            st=('q', 'Ask Jess and Dan'), line='Tell us what to cover next.')),
 'W13-Story-2': (story_c, dict(title='Week 13 story: thank you', photo='jess-dan-garden', crop='50% 35%', tag='Ngā mihi', h='Thank you for a summer of [[learning with us]]', size=92,
            line='Jess and Dan')),
}
for name, (fn, spec) in SPECS.items():
    open(os.path.join(OUT, f'{name}.dc.html'), 'w').write(fn(spec))
print(len(SPECS), 'designs written')
