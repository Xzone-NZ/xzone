"""Email-safe HTML for Shopify's custom-coded emails: tables, inline styles, 600px, no flex or gradients.

Copy comes from calendar/extra.json. Hooks, photos and reviews come from the canvas email designs
(brief/designs/emails/_build.py, tables E and REV). Hero photos are the crops already in images/.

Run from the repo root:  python3 brief/exports/shopify-emails/_build.py
"""
import json, re, html, os, datetime
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'brief', 'exports', 'shopify-emails')
EXTRA = os.path.join(ROOT, 'calendar', 'extra.json')
SMALL = os.path.join(ROOT, 'calendar', 'small')

ns = {}
src = open(os.path.join(ROOT, 'brief', 'designs', 'emails', '_build.py')).read()
exec(src.split("DAY = r'")[0].replace("OUT, EXTRA = sys.argv[1], sys.argv[2]", "OUT = EXTRA = None"), ns)
E, REV = ns['E'], ns['REV']

G, L, INK, SAGE, MUTED, PAGE = '#004F23', '#E0E64A', '#26352a', '#F3F5EF', '#5d6f62', '#E9ECE6'
HEAD = "'Poppins', Arial, Helvetica, sans-serif"
BODY = "Arial, Helvetica, sans-serif"
SITE = 'https://www.xzone.nz/'
SIGNOFF = 'Ngā mihi, Jess and Dan'
NAME = 'Move Freely'  # the newsletter's name, shown under the logo

# ---- shared images (the hero crops are already in images/) ----
os.makedirs(f'{OUT}/images', exist_ok=True)
Image.open(f'{SMALL}/logo.png').save(f'{OUT}/images/xzone-email-logo.png', optimize=True)
f = Image.open(f'{SMALL}/founders.jpg').convert('RGB')  # square crop on the two faces
f.crop((150, 40, 750, 640)).resize((192, 192), Image.LANCZOS).save(f'{OUT}/images/xzone-email-founders.jpg', quality=85, optimize=True)
r = Image.open(f'{SMALL}/range.png').convert('RGBA')
bg = Image.new('RGBA', r.size, SAGE); bg.alpha_composite(r)
bg.convert('RGB').save(f'{OUT}/images/xzone-email-range.jpg', quality=85, optimize=True, progressive=True)

def ph(s): return re.sub(r'\{([A-Z_]+)\}', lambda m: '[' + m.group(1).replace('_', ' ').lower() + ']', s)
def esc(s): return html.escape(ph(s), quote=False)
def hl(t, green):
    t = esc(t)
    if green: return re.sub(r'\[\[(.+?)\]\]', rf'<span style="color:{L};">\1</span>', t)
    return re.sub(r'\[\[(.+?)\]\]', rf'<span style="background-color:{L};padding:0 4px;">\1</span>', t)
def p(text, size=16, color=INK, mb=16):
    return f'<p style="margin:0 0 {mb}px 0;font-family:{BODY};font-size:{size}px;line-height:1.65;color:{color};">{text}</p>'
def eyebrow(text, color=G, mb=0):
    return f'<p style="margin:0 0 {mb}px 0;font-family:{HEAD};font-size:12px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{color};">{text}</p>'
def button(label, href, bg=G, fg='#ffffff', align='left'):
    return (f'<table role="presentation" border="0" cellpadding="0" cellspacing="0" align="{align}" style="margin:0 auto 0 0;"><tr><td bgcolor="{bg}" style="border-radius:999px;background-color:{bg};">'
            f'<a href="{href}" target="_blank" style="display:inline-block;padding:16px 32px;font-family:{HEAD};font-size:16px;font-weight:700;color:{fg};text-decoration:none;border-radius:999px;">{esc(label)} &rarr;</a></td></tr></table>')
def row(inner, bg='#ffffff', pad='0 40px 12px', extra=''):
    return f'<tr><td class="px" bgcolor="{bg}" style="background-color:{bg};padding:{pad};{extra}">{inner}</td></tr>'
def spacer(h, bg='#ffffff'):
    return f'<tr><td bgcolor="{bg}" style="height:{h}px;line-height:{h}px;font-size:0;background-color:{bg};">&nbsp;</td></tr>'
def rule():  # short lime bar above each section
    return f'<table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td bgcolor="{L}" style="width:36px;height:4px;line-height:4px;font-size:0;background-color:{L};border-radius:2px;">&nbsp;</td></tr></table>'
DAY = r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday):'

def signature():
    return (f'<table role="presentation" border="0" cellpadding="0" cellspacing="0" style="margin:8px 0 0 0;"><tr>'
            f'<td valign="middle" width="72" style="width:72px;padding:0 16px 0 0;"><img src="{{{{ img }}}}xzone-email-founders.jpg" width="72" height="72" alt="Jess and Dan" style="display:block;width:72px;height:72px;border:0;border-radius:50%;"></td>'
            f'<td valign="middle"><p style="margin:0;font-family:{BODY};font-size:15px;color:{MUTED};">Ngā mihi,</p>'
            f'<p style="margin:2px 0 0 0;font-family:{HEAD};font-size:19px;font-weight:800;color:{G};">Jess and Dan</p>'
            f'<p style="margin:2px 0 0 0;font-family:{BODY};font-size:13px;color:{MUTED};">Founders, X-ZONE New Zealand</p></td></tr></table>')

def build(e):
    n = 'w%02d' % e['week']
    hook, sub, photo, pos, rk = E[e['id']]
    green = e['type'] == 'campaign'
    kind = 'Campaign' if green else 'Newsletter'
    hero_file = f'xzone-email-{n}-hero.jpg'
    assert os.path.exists(f'{OUT}/images/{hero_file}'), hero_file
    href = SITE
    cta = (e.get('cta') or {}).get('label', 'Shop now')
    lessons = [s for s in e['sections'] if not re.match(r'This week on', s['h'])]
    rows = []

    # brand stripe + logo
    rows.append(f'<tr><td bgcolor="{G}" style="height:6px;line-height:6px;font-size:0;background-color:{G};">&nbsp;</td></tr>')
    rows.append(f'<tr><td bgcolor="{L}" style="height:3px;line-height:3px;font-size:0;background-color:{L};">&nbsp;</td></tr>')
    rows.append(f'<tr><td align="center" style="padding:26px 0 14px;"><a href="{SITE}" target="_blank"><img src="{{{{ img }}}}xzone-email-logo.png" width="132" alt="X-ZONE New Zealand" style="display:block;width:132px;height:auto;border:0;"></a></td></tr>')
    d = datetime.date.fromisoformat(e['date'])
    rows.append(f'<tr><td align="center" style="padding:0 20px 22px;"><p style="margin:0;font-family:{HEAD};font-size:20px;line-height:1.2;font-weight:800;color:{G};">{NAME}</p>'
                f'<p style="margin:6px 0 0 0;font-family:{HEAD};font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{MUTED};">No. {e["week"]:02d} &nbsp;<span style="color:{L};">&#9679;</span>&nbsp; {d.day} {d.strftime("%B %Y")}</p></td></tr>')
    # hero
    rows.append(f'<tr><td><a href="{href}" target="_blank"><img class="fluid" src="{{{{ img }}}}{hero_file}" width="600" alt="{esc(hook.replace("[[", "").replace("]]", ""))}" style="display:block;width:600px;max-width:100%;height:auto;border:0;"></a></td></tr>')
    # headline band
    bbg, bfg, blab, bsub = (G, '#ffffff', L, '#d5e0d8') if green else ('#ffffff', G, G, '#3d5a46')
    rows.append(row(eyebrow(esc(e['title']), blab)
                    + f'<h1 class="h1" style="margin:14px 0 0 0;font-family:{HEAD};font-size:38px;line-height:1.12;font-weight:800;color:{bfg};">{hl(hook, green)}</h1>'
                    + f'<p style="margin:14px 0 28px 0;font-family:{BODY};font-size:18px;line-height:1.5;color:{bsub};">{esc(sub)}</p>'
                    + button(cta, href, *((L, G) if green else (G, '#ffffff'))), bbg, '40px 40px 44px'))
    # in this issue
    if len(lessons) > 1:
        items = ''.join(
            f'<tr><td valign="top" width="40" style="width:40px;padding:8px 0;"><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr>'
            f'<td align="center" bgcolor="{L}" style="width:28px;height:28px;border-radius:50%;background-color:{L};font-family:{HEAD};font-size:12px;font-weight:800;color:{G};">{i}</td></tr></table></td>'
            f'<td valign="middle" style="padding:8px 0;font-family:{HEAD};font-size:16px;font-weight:700;color:{G};">{esc(s["h"])}</td></tr>'
            for i, s in enumerate(lessons, 1))
        box = (f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="{SAGE}" style="background-color:{SAGE};border-radius:16px;"><tr><td style="padding:22px 26px 16px;">'
               + eyebrow('In this issue', G, 6) + f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0">{items}</table></td></tr></table>')
        rows.append(row(box, pad=('36px' if green else '0') + ' 40px 8px'))
    rows.append(spacer(28))
    # sections
    num = 0
    for s in e['sections']:
        if re.match(r'This week on', s['h']):
            parts = re.split(DAY, ph(s['b']))
            items = ''.join(
                f'<tr><td valign="top" width="64" style="width:64px;padding:12px 0;border-top:1px solid #2a6b45;">'
                f'<span style="display:inline-block;background-color:{L};color:{G};font-family:{HEAD};font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;padding:4px 9px;border-radius:999px;">{parts[i][:3]}</span></td>'
                f'<td valign="top" style="padding:12px 0;border-top:1px solid #2a6b45;font-family:{BODY};font-size:15px;line-height:1.55;color:#e6eee8;">{html.escape(parts[i+1].strip()[:1].upper() + parts[i+1].strip()[1:], quote=False)}</td></tr>'
                for i in range(1, len(parts) - 1, 2))
            box = (f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="{G}" style="background-color:{G};border-radius:16px;"><tr><td style="padding:24px 26px 12px;">'
                   + eyebrow(esc(s['h']), L, 4)
                   + f'<p style="margin:0 0 12px 0;font-family:{BODY};font-size:14px;color:#c4d3c8;">Follow along for the full lessons, slide by slide.</p>'
                   + f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0">{items}</table></td></tr></table>')
            rows.append(row(box, pad='8px 40px 36px'))
            continue
        num += 1
        body, sign = ph(s['b']), False
        if SIGNOFF in body:
            body, sign = body.replace(SIGNOFF, '').strip(), True
        paras = ''.join(p(html.escape(x.strip(), quote=False).replace('\n', '<br>')) for x in body.split('\n\n') if x.strip())
        head = (rule() + f'<p style="margin:14px 0 6px 0;font-family:{HEAD};font-size:12px;font-weight:700;letter-spacing:2px;color:{MUTED};">{num:02d}</p>') if len(lessons) > 1 else rule() + '<div style="height:14px;line-height:14px;font-size:0;">&nbsp;</div>'
        rows.append(row(head + f'<h2 style="margin:0 0 12px 0;font-family:{HEAD};font-size:25px;line-height:1.25;font-weight:800;color:{G};">{esc(s["h"])}</h2>{paras}'
                        + (signature() if sign else ''), pad='0 40px 26px'))
    # main CTA
    rows.append(row(button(cta, href), pad='4px 40px 44px'))
    # review
    rbg, rfg, rlab, rsub, rnote = (SAGE, G, G, '#3d5a46', '#6b7d70') if green else (G, '#ffffff', L, '#d5e0d8', '#a9bcae')
    stars = f'<p style="margin:0 0 4px 0;font-family:Arial, Helvetica, sans-serif;font-size:20px;letter-spacing:4px;color:{L if not green else "#c9b400"};">&#9733;&#9733;&#9733;&#9733;&#9733;</p>'
    mark = f'<p style="margin:0;font-family:Georgia, serif;font-size:72px;line-height:56px;height:44px;color:{L if not green else G};">&ldquo;</p>'
    if rk:
        rv = REV[rk]
        qp = (f'<p style="margin:12px 0 0 0;font-family:{BODY};font-size:17px;line-height:1.65;color:{rsub};">{html.escape(rv["quote"], quote=False).replace(chr(10), "<br>")}</p>' if rv['quote'] else '')
        inner = (eyebrow(f'In their words &middot; {rv["product"]}', rlab, 14) + stars + mark
                 + f'<p style="margin:0;font-family:{HEAD};font-size:26px;line-height:1.25;font-weight:800;color:{rfg};">{html.escape(rv["title"], quote=False)}</p>{qp}'
                 + f'<p style="margin:18px 0 0 0;font-family:{BODY};font-size:14px;font-weight:700;color:{rfg};">{html.escape(rv["name"])} <span style="font-weight:400;color:{rnote};">&middot; {"Verified Judge.me review" if rv.get("verified") else "Judge.me review"}</span></p>')
    else:
        q = e.get('review') or {}
        inner = (eyebrow('In their words', rlab, 14) + stars + mark
                 + f'<p style="margin:0;font-family:{HEAD};font-size:26px;line-height:1.25;font-weight:800;color:{rfg};">{esc(q.get("quote", ""))}</p>'
                 + f'<p style="margin:18px 0 0 0;font-family:{BODY};font-size:14px;font-weight:700;color:{rfg};">{esc(q.get("name", ""))}</p>')
    rows.append(row(inner, rbg, '44px 40px 46px'))
    # range card
    rows.append(spacer(36))
    rows.append(row(f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="{SAGE}" style="background-color:{SAGE};border-radius:16px;">'
                    f'<tr><td align="center" style="padding:30px 26px 6px;">' + eyebrow('The X-ZONE range', G, 8)
                    + f'<p style="margin:0;font-family:{HEAD};font-size:22px;line-height:1.3;font-weight:800;color:{G};">Relief, Joints and Sports</p>'
                    + f'<p style="margin:8px 0 0 0;font-family:{BODY};font-size:15px;line-height:1.55;color:{MUTED};">Rubs, sprays and roll-ons. Find the one that suits you.</p></td></tr>'
                    f'<tr><td align="center" style="padding:14px 20px 4px;"><a href="{SITE}" target="_blank"><img class="fluid" src="{{{{ img }}}}xzone-email-range.jpg" width="440" alt="The X-ZONE range of rubs, sprays and roll-ons" style="display:block;width:440px;max-width:100%;height:auto;border:0;"></a></td></tr>'
                    f'<tr><td align="center" style="padding:10px 26px 30px;"><a href="{SITE}" target="_blank" style="font-family:{HEAD};font-size:15px;font-weight:700;color:{G};text-decoration:underline;">Shop the range &rarr;</a></td></tr></table>',
                    pad='0 40px 8px'))
    # PS
    if e.get('ps'):
        rows.append(row(f'<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0"><tr><td style="border-left:4px solid {L};padding:4px 0 4px 18px;">'
                        + p(f'<b style="font-family:{HEAD};color:{G};">PS</b>&nbsp; {esc(e["ps"])}', 15, '#4a5a4e', 0) + '</td></tr></table>', pad='28px 40px 40px'))
    else:
        rows.append(spacer(32))
    # footer
    rows.append(f'''<tr><td class="px" align="center" bgcolor="{G}" style="background-color:{G};padding:40px 40px 36px;">
<table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td bgcolor="#ffffff" style="background-color:#ffffff;border-radius:999px;padding:11px 24px;"><img src="{{{{ img }}}}xzone-email-logo.png" width="96" alt="X-ZONE New Zealand" style="display:block;width:96px;height:auto;border:0;"></td></tr></table>
<p style="margin:18px 0 0 0;font-family:{HEAD};font-size:20px;font-weight:800;color:#ffffff;">Move Freely. <span style="color:{L};">Live Naturally.</span></p>
<p style="margin:10px 0 0 0;font-family:{BODY};font-size:14px;line-height:1.55;color:#c4d3c8;">Questions? Reply to this email. Jess and Dan read every one.</p>
<p style="margin:16px 0 0 0;font-family:{HEAD};font-size:14px;font-weight:700;"><a href="{SITE}" target="_blank" style="color:{L};text-decoration:none;">xzone.nz</a></p>
<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" style="margin:24px 0 0 0;"><tr><td style="border-top:1px solid #2a6b45;font-size:0;line-height:0;">&nbsp;</td></tr></table>
<p style="margin:18px 0 0 0;font-family:{BODY};font-size:11px;line-height:1.6;color:#a9bcae;">[Business address]<br>You are getting this because you signed up at xzone.nz. &middot; <a href="{{{{ unsubscribe_link }}}}" target="_blank" style="color:#a9bcae;text-decoration:underline;">Unsubscribe</a></p>
</td></tr>''')
    rows.append(f'<tr><td bgcolor="{L}" style="height:6px;line-height:6px;font-size:0;background-color:{L};">&nbsp;</td></tr>')

    pre = esc(e['preheader'])
    doc = f'''<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">
<title>{esc(e["subject"])}</title>
<!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@700;800&amp;display=swap" rel="stylesheet">
<style>
body {{ margin:0; padding:0; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; }}
table {{ border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; }}
img {{ -ms-interpolation-mode:bicubic; }}
a {{ color:{G}; }}
@media only screen and (max-width:620px) {{
  .w {{ width:100% !important; }}
  .px {{ padding-left:22px !important; padding-right:22px !important; }}
  .h1 {{ font-size:31px !important; }}
  img.fluid {{ width:100% !important; height:auto !important; }}
}}
</style>
</head>
<body style="margin:0;padding:0;background-color:{PAGE};">
{{% comment %}} Paste your Shopify Files folder address between the quotes below, ending with a slash. Content > Files: copy any uploaded image's link and delete the file name. {{% endcomment %}}
{{% assign img = "PASTE-SHOPIFY-FILES-FOLDER-URL-HERE/" %}}
<div style="display:none;font-size:1px;color:{PAGE};line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">{pre}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<table role="presentation" width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="{PAGE}" style="background-color:{PAGE};">
<tr><td align="center" style="padding:18px 10px 28px;">
<table role="presentation" class="w" width="600" border="0" cellpadding="0" cellspacing="0" style="width:600px;max-width:600px;">
<tr><td class="px" style="padding:0 4px 12px;font-family:{BODY};font-size:12px;color:{MUTED};">{NAME} &middot; No. {e["week"]:02d}</td>
<td class="px" align="right" style="padding:0 4px 12px;font-family:{BODY};font-size:12px;"><a href="{SITE}" target="_blank" style="color:{MUTED};text-decoration:underline;">xzone.nz</a></td></tr>
</table>
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

if __name__ == '__main__':
    for e in json.load(open(EXTRA))['emails']:
        n, size = build(e)
        print(n, f'{size/1024:.1f} KB')
