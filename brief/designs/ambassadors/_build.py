"""Ambassador carousels (Jasmine Marsters, Mollie Allison) in the approved social style. 3 slides each, 1080 x 1350."""
import sys, re, html
OUT = sys.argv[1]
G, L = '#0D441F', '#E0E64A'
LOGO = '/_blob/25197b28f4e73a8b274a5afe746a93c6'
PH = {'jas1': '/_blob/d2c897c75f5fcbc8a6cfd774ddbcdc20', 'jas2': '/_blob/7857f267843431270af02d3c5fd6a212',
      'mol1': '/_blob/d6f4ed7c106a6a841dd33259362017c8', 'mol2': '/_blob/fc32ab8f9a90be36adee1c41a420f62d'}
def hl(t, mode):
    if mode == 'lime': return re.sub(r'\[\[(.+?)\]\]', rf'<span style="color: {L}">\1</span>', t)
    return re.sub(r'\[\[(.+?)\]\]', rf'<span style="background: linear-gradient(transparent 58%, {L} 58%); padding: 0 4px">\1</span>', t)
def page(title, body, link=G):
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
a{{color:{link}}}a:hover{{color:#0a3318}}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1080,"height":1350}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{}};
  }}
}}
</script>
</body>
</html>
'''
def dots(n, on, green):
    a, b = (L, 'rgba(255,255,255,0.35)') if green else (G, 'rgba(13,68,31,0.25)')
    return '<div style="display: flex; gap: 12px">' + ''.join(f'<span style="width: 16px; height: 16px; border-radius: 50%; background: {a if i == on else b}"></span>' for i in range(n)) + '</div>'
def logo(green):
    if green: return f'<div style="background: #ffffff; border-radius: 999px; padding: 14px 28px; display: flex; align-items: center"><img src="{LOGO}" alt="X-ZONE New Zealand" style="height: 34px; width: auto"></div>'
    return f'<img src="{LOGO}" alt="X-ZONE New Zealand" style="height: 40px; width: auto">'

def cover(a):
    green = a['band'] == 'green'
    bg, fg, lab, sub = (G, '#ffffff', L, 'rgba(255,255,255,0.86)') if green else ('#ffffff', G, G, 'rgba(13,68,31,0.85)')
    arrow = L if green else G
    return page(f"{a['name']} carousel, slide 1", f'''<div style="position: relative; width: 1080px; height: 1350px; overflow: hidden; background: {bg}; font-family: 'Poppins', sans-serif; display: flex; flex-direction: column">
  <div style="position: relative; width: 1080px; height: 720px; flex-shrink: 0">
    <img src="{PH[a['p1']]}" alt="{a['alt1']}" style="width: 100%; height: 100%; object-fit: cover; object-position: {a['crop1']}">
    <div style="position: absolute; left: 64px; top: 56px; background: #ffffff; border-radius: 999px; padding: 16px 30px; display: flex; align-items: center"><img src="{LOGO}" alt="X-ZONE New Zealand" style="height: 36px; width: auto"></div>
  </div>
  <div style="flex: 1; padding: 52px 80px 50px 80px; display: flex; flex-direction: column; gap: 20px; box-sizing: border-box">
    <div style="color: {lab}; font-size: 26px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase">{a['label']}</div>
    <h1 style="margin: 0; color: {fg}; font-size: 80px; line-height: 1.06; font-weight: 800">{hl(a['hook'], 'lime' if green else 'hl')}</h1>
    <p style="margin: 0; color: {sub}; font-size: 32px; line-height: 1.45; font-weight: 500">{a['sub']}</p>
    <div style="margin-top: auto; display: flex; align-items: center; justify-content: space-between">
      <div style="display: flex; align-items: center; gap: 14px; color: {fg}; font-size: 26px; font-weight: 600"><span>Swipe</span><svg width="34" height="34" viewBox="0 0 36 36" fill="none" aria-hidden="true"><path d="M6 18h23M29 18l-9-9M29 18l-9 9" stroke="{arrow}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      {dots(3, 0, green)}
    </div>
  </div>
</div>''', L if green else G)

def quote(a):
    green = a['band'] != 'green'   # alternate with the cover
    bg, fg, mark, sub = (G, '#ffffff', L, 'rgba(255,255,255,0.8)') if green else ('#ffffff', G, G, 'rgba(13,68,31,0.75)')
    return page(f"{a['name']} carousel, slide 2", f'''<div style="position: relative; width: 1080px; height: 1350px; overflow: hidden; background: {bg}; font-family: 'Poppins', sans-serif; box-sizing: border-box; padding: 110px 90px 80px; display: flex; flex-direction: column">
  <div style="color: {mark}; font-size: 260px; line-height: 0.8; font-weight: 900; height: 170px">“</div>
  <div style="color: {fg}; font-size: 60px; line-height: 1.2; font-weight: 800; margin-top: 20px">{html.escape(a['quote'])}</div>
  <div style="margin-top: 56px; display: flex; flex-direction: column; gap: 6px">
    <div style="color: {fg}; font-size: 34px; font-weight: 700">{a['name']}</div>
    <div style="color: {sub}; font-size: 28px; font-weight: 500">{a['role']}</div>
  </div>
  <div style="margin-top: auto; display: flex; align-items: center; justify-content: space-between">{logo(green)}{dots(3, 1, green)}</div>
</div>''', L if green else G)

def story(a):
    if a['last'] == 'full':
        return page(f"{a['name']} carousel, slide 3", f'''<div style="position: relative; width: 1080px; height: 1350px; overflow: hidden; background: {G}; font-family: 'Poppins', sans-serif">
  <img src="{PH[a['p2']]}" alt="{a['alt2']}" style="position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; object-position: {a['crop2']}">
  <div style="position: absolute; left: 0; right: 0; bottom: 0; height: 820px; background: linear-gradient(180deg, rgba(13,68,31,0) 0%, rgba(13,68,31,0.6) 45%, rgba(13,68,31,0.96) 100%)"></div>
  <div style="position: absolute; left: 64px; top: 56px; background: #ffffff; border-radius: 999px; padding: 16px 30px; display: flex; align-items: center"><img src="{LOGO}" alt="X-ZONE New Zealand" style="height: 36px; width: auto"></div>
  <div style="position: absolute; left: 80px; right: 80px; bottom: 70px; display: flex; flex-direction: column; gap: 20px">
    <div style="align-self: flex-start; background: {L}; color: {G}; border-radius: 999px; padding: 12px 28px; font-size: 25px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase">{a['tag3']}</div>
    <h1 style="margin: 0; color: #ffffff; font-size: 84px; line-height: 1.06; font-weight: 800">{hl(a['h3'], 'lime')}</h1>
    <p style="margin: 0; color: rgba(255,255,255,0.88); font-size: 32px; line-height: 1.45; font-weight: 500">{a['s3']}</p>
    <div style="display: flex; justify-content: flex-end">{dots(3, 2, True)}</div>
  </div>
</div>''', L)
    return page(f"{a['name']} carousel, slide 3", f'''<div style="position: relative; width: 1080px; height: 1350px; overflow: hidden; background: {G}; font-family: 'Poppins', sans-serif; display: flex; flex-direction: column">
  <div style="position: relative; width: 1080px; height: 640px; flex-shrink: 0"><img src="{PH[a['p2']]}" alt="{a['alt2']}" style="width: 100%; height: 100%; object-fit: cover; object-position: {a['crop2']}"></div>
  <div style="flex: 1; padding: 56px 80px 50px 80px; display: flex; flex-direction: column; gap: 22px; box-sizing: border-box">
    <div style="align-self: flex-start; background: {L}; color: {G}; border-radius: 999px; padding: 12px 28px; font-size: 25px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase">{a['tag3']}</div>
    <h1 style="margin: 0; color: #ffffff; font-size: 84px; line-height: 1.06; font-weight: 800">{hl(a['h3'], 'lime')}</h1>
    <p style="margin: 0; color: rgba(255,255,255,0.86); font-size: 32px; line-height: 1.45; font-weight: 500">{a['s3']}</p>
    <div style="margin-top: auto; display: flex; align-items: center; justify-content: space-between">{logo(True)}{dots(3, 2, True)}</div>
  </div>
</div>''', L)

AMB = {
 'Amb-Jasmine': dict(name='Jasmine Marsters', role='NZ Strongman competitor', band='green',
    p1='jas1', crop1='50% 30%', alt1='Jasmine Marsters holding a pot of X-ZONE Sports Rub at the Strongman Series Easter Show',
    label='Ambassador 15 · NZ Strongman', hook='From 20 kg to [[75 kg]] overhead', sub='Meet Jasmine Marsters: South Auckland, mum of six, strongman.',
    quote="The instant relief I felt was unbelievable. Ever since then I've been hooked, and it's now a part of my training and recovery routine.",
    last='full', p2='jas2', crop2='50% 40%', alt2='Jasmine Marsters pulling a bus by rope at the Strongman Series Easter Show 2026',
    tag3='Ambassador 15 · link in bio', h3="Read Jasmine's [[full story]]", s3='Strongman, rugby with her eldest daughter, and the day she met Jess at the Easter Show.'),
 'Amb-Mollie': dict(name='Mollie Allison', role='NZ beach volleyball representative', band='white',
    p1='mol1', crop1='50% 22%', alt1='Mollie Allison serving on a sand court, in a New Zealand top',
    label='Ambassador 14 · NZ beach volleyball', hook='Top five on the [[NZ Beach Tour]]', sub='Meet Mollie Allison: Hamilton, NZ squad, coach and student.',
    quote='I love spending all my time on the courts, training hard myself but also giving back and teaching all I know to those around me.',
    last='band', p2='mol2', crop2='50% 50%', alt2='A New Zealand beach volleyball tour event by the sea',
    tag3='Ambassador 14 · link in bio', h3="Read Mollie's [[full story]]", s3='Training with few partners, funding it herself, and the goal of playing for New Zealand around the world.'),
}
for k, a in AMB.items():
    open(f'{OUT}/{k}-1.dc.html', 'w').write(cover(a))
    open(f'{OUT}/{k}-2.dc.html', 'w').write(quote(a))
    open(f'{OUT}/{k}-3.dc.html', 'w').write(story(a))
print('6 slides written')
