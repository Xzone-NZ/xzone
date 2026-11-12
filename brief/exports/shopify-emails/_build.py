"""Email-safe HTML for Shopify's custom-coded emails: tables, inline styles, 600px, no flex or gradients.
Copy from calendar/extra.json; hooks, photos and reviews from the canvas email designs (emails.py)."""
import json, re, html, os, sys
from PIL import Image
EXTRA, OUT, SCR = sys.argv[1], sys.argv[2], sys.argv[3]
ns = {}
src = open(os.path.join(SCR, 'emails.py')).read()
exec(src.split("DAY = r'")[0].replace("OUT, EXTRA = sys.argv[1], sys.argv[2]", "OUT = EXTRA = None"), ns)
E, REV = ns['E'], ns['REV']
G, L, INK = '#0D441F', '#E0E64A', '#26352a'
HEAD = "'Poppins', Arial, Helvetica, sans-serif"
BODY = "Arial, Helvetica, sans-serif"
SMALL = '/home/user/xzone/calendar/small'; ORIG = os.path.join(SCR, '..', 'images')
PHOTO = {'cricket': f'{ORIG}/1.jpg', 'aoraki': f'{ORIG}/2.jpg', 'bushwalk': f'{ORIG}/3.jpg', 'hands': f'{ORIG}/4.jpg', 'handsclose': f'{ORIG}/5.jpg',
         'running': f'{SCR}/render/812990ea70541643834c6b3b08c76d9e.jpg', 'founders': f'{SMALL}/founders.jpg', 'shoulder': f'{SMALL}/shoulder.jpg',
         'ankle': f'{SMALL}/ankle.jpg', 'bush': f'{SMALL}/bush.jpg',
         'jess-dan-tees': '/tmp/claude-0/-home-user-xzone/86ea63bf-5758-5665-bc90-8e5f32934080/assets2/jess-dan-tees.jpg', 'jess-dan-garden': '/tmp/claude-0/-home-user-xzone/86ea63bf-5758-5665-bc90-8e5f32934080/assets2/jess-dan-garden.jpg', 'jess-dan-expo': '/tmp/claude-0/-home-user-xzone/86ea63bf-5758-5665-bc90-8e5f32934080/assets2/jess-dan-expo.jpg', 'relief-rollon-shoulder': '/tmp/claude-0/-home-user-xzone/86ea63bf-5758-5665-bc90-8e5f32934080/assets2/relief-rollon-shoulder.jpg', 'relief-rub-leg': '/tmp/claude-0/-home-user-xzone/86ea63bf-5758-5665-bc90-8e5f32934080/assets2/relief-rub-leg.jpg', 'sports-rub-gym': '/tmp/claude-0/-home-user-xzone/86ea63bf-5758-5665-bc90-8e5f32934080/assets2/sports-rub-gym.jpg', 'sports-spray-knee': '/tmp/claude-0/-home-user-xzone/86ea63bf-5758-5665-bc90-8e5f32934080/assets2/sports-spray-knee.jpg', 'sports-spray-arm': '/tmp/claude-0/-home-user-xzone/86ea63bf-5758-5665-bc90-8e5f32934080/assets2/sports-spray-arm.jpg', 'relief-rub-back': '/tmp/claude-0/-home-user-xzone/86ea63bf-5758-5665-bc90-8e5f32934080/assets2/relief-rub-back.jpg'}
os.makedirs(f'{OUT}/images', exist_ok=True)

def crop(src_path, pos, dst, w=1200, h=760):
    im = Image.open(src_path).convert('RGB')
    px, py = [float(v.strip('%')) / 100 for v in pos.split()]
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - w) * px); y = round((im.height - h) * py)
    im.crop((x, y, x + w, y + h)).save(dst, quality=82, optimize=True, progressive=True)

Image.open(f'{SMALL}/logo.png').save(f'{OUT}/images/xzone-email-logo.png', optimize=True)

def ph(s): return re.sub(r'\{([A-Z_]+)\}', lambda m: '[' + m.group(1).replace('_', ' ').lower() + ']', s)
def esc(s): return html.escape(ph(s), quote=False)
def hl(t, green):
    t = esc(t)
    if green: return re.sub(r'\[\[(.+?)\]\]', rf'<span style="color:{L};">\1</span>', t)
    return re.sub(r'\[\[(.+?)\]\]', rf'<span style="background-color:{L};">\1</span>', t)
def p(text, size=16, color=INK, mb=14):
    return f'<p style="margin:0 0 {mb}px 0;font-family:{BODY};font-size:{size}px;line-height:1.6;color:{color};">{text}</p>'
def paras(b): return ''.join(p(html.escape(x.strip(), quote=False).replace('\n', '<br>')) for x in ph(b).split('\n\n') if x.strip())
def button(label, href, green):
    bg, fg = (L, G) if green else (G, '#ffffff')
    return (f'<table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td bgcolor="{bg}" style="border-radius:999px;background-color:{bg};">'
            f'<a href="{href}" target="_blank" style="display:inline-block;padding:16px 30px;font-family:{HEAD};font-size:17px;font-weight:700;color:{fg};text-decoration:none;border-radius:999px;">{esc(label)}</a></td></tr></table>')
def row(inner, bg='#ffffff', pad='0 32px 12px'):
    return f'<tr><td class="px" bgcolor="{bg}" style="background-color:{bg};padding:{pad};">{inner}</td></tr>'
DAY = r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday):'

def build(e):
    n = 'w%02d' % e['week']
    hook, sub, photo, pos, rk = E[e['id']]
    green = e['type'] == 'campaign'
    hero_file = f'xzone-email-{n}-hero.jpg'
    crop(PHOTO[photo], pos, f'{OUT}/images/{hero_file}')
    href = 'https://www.xzone.nz/'
    cta = (e.get('cta') or {}).get('label', 'Shop now')
    if e['id'] == 'w13-email': href = 'https://www.xzone.nz/'  # survey link goes here
    bbg, bfg, blab, bsub = (G, '#ffffff', L, '#d5e0d8') if green else ('#ffffff', G, G, '#3d5a46')
    rows = []
    rows.append(f'<tr><td align="center" style="padding:22px 0;border-bottom:3px solid {G};"><img src="{{{{ img }}}}xzone-email-logo.png" width="116" alt="X-ZONE New Zealand" style="display:block;width:116px;height:auto;border:0;"></td></tr>')
    rows.append(f'<tr><td><img class="fluid" src="{{{{ img }}}}{hero_file}" width="600" alt="" style="display:block;width:600px;max-width:100%;height:auto;border:0;"></td></tr>')
    rows.append(row(f'<p style="margin:0;font-family:{HEAD};font-size:12px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{blab};">{esc(e["title"])}</p>'
                    f'<h1 class="h1" style="margin:12px 0 0 0;font-family:{HEAD};font-size:36px;line-height:1.12;font-weight:800;color:{bfg};">{hl(hook, green)}</h1>'
                    f'<p style="margin:12px 0 24px 0;font-family:{BODY};font-size:17px;line-height:1.5;color:{bsub};">{esc(sub)}</p>{button(cta, href, green)}', bbg, '34px 32px 36px'))
    rows.append('<tr><td style="height:30px;line-height:30px;font-size:0;">&nbsp;</td></tr>')
    for s in e['sections']:
        if re.match(r'This week on', s['h']):
            parts = re.split(DAY, ph(s['b']))
            items = ''.join(f'<tr><td valign="top" width="80" style="padding:12px 0;border-top:1px solid #dde3d8;font-family:{HEAD};font-size:13px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:{G};">{parts[i][:3]}</td>'
                            f'<td valign="top" style="padding:12px 0;border-top:1px solid #dde3d8;font-family:{BODY};font-size:15px;line-height:1.55;color:{INK};">{html.escape(parts[i+1].strip()[:1].upper() + parts[i+1].strip()[1:], quote=False)}</td></tr>' for i in range(1, len(parts) - 1, 2))
            box = (f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="#f3f5ef" style="background-color:#f3f5ef;border-radius:16px;"><tr><td style="padding:22px 24px 10px;">'
                   f'<p style="margin:0 0 8px 0;font-family:{HEAD};font-size:12px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{G};">{esc(s["h"])}</p>'
                   f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0">{items}</table></td></tr></table>')
            rows.append(row(box, pad='8px 32px 28px'))
        else:
            rows.append(row(f'<h2 style="margin:0 0 10px 0;font-family:{HEAD};font-size:23px;line-height:1.25;font-weight:800;color:{G};">{esc(s["h"])}</h2>{paras(s["b"])}'))
    rows.append(row(button(cta, href, False), pad='6px 32px 30px'))
    rbg, rfg, rlab, rsub, rnote = ('#f3f5ef', G, G, '#3d5a46', '#6b7d70') if green else (G, '#ffffff', L, '#d5e0d8', '#a9bcae')
    if rk:
        r = REV[rk]
        qp = (f'<p style="margin:10px 0 0 0;font-family:{BODY};font-size:16px;line-height:1.6;color:{rsub};">{html.escape(r["quote"], quote=False).replace(chr(10), "<br>")}&rdquo;</p>' if r['quote'] else '')
        rv = (f'<p style="margin:0;font-family:{HEAD};font-size:12px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{rlab};">In their words &middot; {r["product"]}</p>'
              f'<p style="margin:12px 0 0 0;font-family:{HEAD};font-size:25px;line-height:1.2;font-weight:800;color:{rfg};">&ldquo;{html.escape(r["title"], quote=False)}{"" if r["quote"] else "&rdquo;"}</p>'
              f'{qp}'
              f'<p style="margin:14px 0 0 0;font-family:{BODY};font-size:14px;font-weight:700;color:{rfg};">{html.escape(r["name"])} <span style="font-weight:400;color:{rnote};">&middot; {"Verified Judge.me review" if r.get("verified") else "Judge.me review"}</span></p>')
    else:
        q = e.get('review') or {}
        rv = (f'<p style="margin:0;font-family:{HEAD};font-size:12px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{rlab};">In their words</p>'
              f'<p style="margin:12px 0 0 0;font-family:{HEAD};font-size:25px;line-height:1.2;font-weight:800;color:{rfg};">&ldquo;{esc(q.get("quote", ""))}&rdquo;</p>'
              f'<p style="margin:14px 0 0 0;font-family:{BODY};font-size:14px;font-weight:700;color:{rfg};">{esc(q.get("name", ""))}</p>')
    rows.append(row(rv, rbg, '34px 32px'))
    if e.get('ps'):
        rows.append(row(p(f'<b style="color:{G};">PS</b> {esc(e["ps"])}', 15, '#4a5a4e', 0), pad='26px 32px 30px'))
    rows.append(f'''<tr><td class="px" align="center" bgcolor="{G}" style="background-color:{G};padding:30px 32px;">
<table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td bgcolor="#ffffff" style="background-color:#ffffff;border-radius:999px;padding:10px 22px;"><img src="{{{{ img }}}}xzone-email-logo.png" width="90" alt="X-ZONE New Zealand" style="display:block;width:90px;height:auto;border:0;"></td></tr></table>
<p style="margin:14px 0 0 0;font-family:{HEAD};font-size:18px;font-weight:800;color:#ffffff;">Move Freely. <span style="color:{L};">Live Naturally.</span></p>
<p style="margin:10px 0 0 0;font-family:{BODY};font-size:13px;color:#c4d3c8;"><a href="https://www.xzone.nz/" target="_blank" style="color:#c4d3c8;text-decoration:underline;">xzone.nz</a></p>
<p style="margin:14px 0 0 0;font-family:{BODY};font-size:11px;line-height:1.5;color:#a9bcae;">[Business address] &middot; You are getting this because you signed up at xzone.nz.<br><a href="{{{{ unsubscribe_link }}}}" target="_blank" style="color:#a9bcae;text-decoration:underline;">Unsubscribe</a></p>
</td></tr>''')
    pre = esc(e['preheader'])
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<title>{esc(e["subject"])}</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@700;800&amp;display=swap" rel="stylesheet">
<style>
body {{ margin:0; padding:0; -webkit-text-size-adjust:100%; }}
table {{ border-collapse:collapse; }}
img {{ -ms-interpolation-mode:bicubic; }}
@media only screen and (max-width:620px) {{
  .w {{ width:100% !important; }}
  .px {{ padding-left:20px !important; padding-right:20px !important; }}
  .h1 {{ font-size:30px !important; }}
  img.fluid {{ width:100% !important; height:auto !important; }}
}}
</style>
</head>
<body style="margin:0;padding:0;background-color:#e9ece6;">
{{% comment %}} Paste your Shopify Files folder address between the quotes below, ending with a slash. Settings > Files: copy any uploaded image's link and delete the file name. {{% endcomment %}}
{{% assign img = "PASTE-SHOPIFY-FILES-FOLDER-URL-HERE/" %}}
<div style="display:none;font-size:1px;color:#e9ece6;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">{pre}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="#e9ece6" style="background-color:#e9ece6;">
<tr><td align="center" style="padding:20px 10px;">
<table role="presentation" class="w" width="600" border="0" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="width:600px;max-width:600px;background-color:#ffffff;">
{chr(10).join(rows)}
</table>
</td></tr>
</table>
{{{{ open_tracking_block }}}}
</body>
</html>
'''
    open(f'{OUT}/xzone-email-{n}.html', 'w').write(doc)
    return n, len(doc.encode())

emails = json.load(open(EXTRA))['emails']
for e in emails:
    n, size = build(e)
    print(n, f'{size/1024:.1f} KB')
