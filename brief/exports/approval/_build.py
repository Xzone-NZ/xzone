"""Approval page for the Move Freely emails: every email rendered live, with its subject, send date and the
points Jess and Dan need to confirm. Run from the repo root after brief/exports/shopify-emails/_build.py."""
import json, re, html, os, datetime
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
EM = os.path.join(ROOT, 'brief', 'exports', 'shopify-emails')
OUT = os.path.join(ROOT, 'brief', 'exports', 'approval', 'move-freely-approval.html')
emails = json.load(open(os.path.join(ROOT, 'calendar', 'extra.json')))['emails']

def ph(s): return re.sub(r'\{([A-Z_]+)\}', lambda m: '[' + m.group(1).replace('_', ' ').lower() + ']', s)
SKIP = ('UTM', "Review quotes are the plan", 'Instagram and Facebook links in the email footer')
def nice(d): d = datetime.date.fromisoformat(d); return f'{d.strftime("%a")} {d.day} {d.strftime("%b %Y")}'

rows, cards = [], []
for e in emails:
    n = '%02d' % e['week']
    src = open(f'{EM}/xzone-email-w{n}.html').read()
    src = re.sub(r'\{% comment %\}.*?\{% endcomment %\}\n?', '', src, flags=re.S)
    src = re.sub(r'\{%.*?%\}\n?', '', src)
    src = src.replace('{{ img }}', 'images/').replace('{{ unsubscribe_link }}', '#').replace('{{ open_tracking_block }}', '')
    src = src.replace('<head>', '<head><base target="_blank">', 1)
    flags = [ph(f) for f in e['flags'] if not any(s in f for s in SKIP)]
    if e['week'] == 9: flags.append("The review is Ben M's shortened quote until his full Judge.me review is found")
    kind = 'Campaign' if e['type'] == 'campaign' else 'Newsletter'
    rows.append(f'<tr><td class="num">No. {n}</td><td>{nice(e["date"])}</td><td><span class="pill {e["type"]}">{kind}</span></td>'
                f'<td><a href="#w{n}">{html.escape(ph(e["subject"]))}</a></td></tr>')
    fl = ''.join(f'<li>{html.escape(f)}</li>' for f in flags) or '<li>Nothing to confirm beyond the design.</li>'
    cards.append(f'''<section class="email" id="w{n}">
  <aside class="meta">
    <p class="eyebrow">Move Freely · No. {n}</p>
    <h3>{html.escape(ph(e["title"]))}</h3>
    <dl>
      <dt>Sends</dt><dd>{nice(e["date"])} <span class="pill {e["type"]}">{kind}</span></dd>
      <dt>Subject line</dt><dd class="strong">{html.escape(ph(e["subject"]))}</dd>
      <dt>Preview text</dt><dd>{html.escape(ph(e["preheader"]))}</dd>
      <dt>Button</dt><dd>{html.escape((e.get("cta") or {}).get("label", ""))}</dd>
    </dl>
    <div class="confirm"><p class="eyebrow">Please confirm</p><ul>{fl}</ul></div>
  </aside>
  <div class="frame"><iframe title="Email {n}: {html.escape(ph(e["subject"]))}" loading="lazy" srcdoc="{html.escape(src, quote=True)}"></iframe></div>
</section>''')

page = f'''<title>Move Freely emails</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600&display=swap">
<style>
/* Layout: a brand masthead, the schedule, then each email as a live render beside its approval notes. */
:root {{
  --bg: #F3F5EF; --surface: #ffffff; --fg: #1d2b21; --muted: #5d6f62; --line: #dde3d8;
  --green: #004F23; --lime: #E0E64A; --on-green: #ffffff; --chip: #e6ecd9; --chip-fg: #004F23;
  --display: 'Poppins', Arial, Helvetica, sans-serif; --body: 'Inter', Arial, Helvetica, sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #0d1a12; --surface: #13261a; --fg: #e4ece5; --muted: #9db0a2; --line: #24402d;
  --green: #0f5f31; --lime: #E0E64A; --on-green: #ffffff; --chip: #24402d; --chip-fg: #E0E64A; color-scheme: dark }} }}
:root[data-theme="dark"] {{
  --bg: #0d1a12; --surface: #13261a; --fg: #e4ece5; --muted: #9db0a2; --line: #24402d;
  --green: #0f5f31; --lime: #E0E64A; --on-green: #ffffff; --chip: #24402d; --chip-fg: #E0E64A; color-scheme: dark }}
* {{ box-sizing: border-box }}
body {{ background: var(--bg); color: var(--fg); font-family: var(--body); font-size: 15px; line-height: 1.6 }}
.wrap {{ max-width: 1120px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)) }}
h1, h2, h3 {{ font-family: var(--display); text-wrap: balance; margin: 0 }}
a {{ color: inherit }}
a:focus-visible {{ outline: 3px solid var(--lime); outline-offset: 2px }}
.eyebrow {{ font-family: var(--display); font-weight: 700; font-size: 11px; letter-spacing: .2em; text-transform: uppercase; color: var(--muted); margin: 0 }}
.mast {{ background: var(--green); color: var(--on-green); border-bottom: 6px solid var(--lime) }}
.mast .wrap {{ padding-block: 56px 48px; display: grid; gap: 14px }}
.mast .eyebrow {{ color: var(--lime) }}
.mast h1 {{ font-size: clamp(44px, 8vw, 84px); font-weight: 800; line-height: 1; letter-spacing: -.02em }}
.mast h1 span {{ color: var(--lime) }}
.mast p.lede {{ margin: 0; max-width: 62ch; font-size: 17px; color: #d5e0d8 }}
main .wrap {{ display: grid; grid-template-columns: minmax(0, 1fr); gap: 56px; padding-block: 48px 72px }}
.intro {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px }}
.panel {{ background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 24px; display: grid; gap: 10px; align-content: start; min-width: 0 }}
.panel h2 {{ font-size: 20px; color: var(--fg) }}
.panel p, .panel ul {{ margin: 0; color: var(--muted) }}
.panel ul {{ padding-left: 18px; display: grid; gap: 4px }}
.sched h2, .emails > h2 {{ font-size: 28px; margin-bottom: 16px }}
.tablewrap {{ overflow-x: auto; background: var(--surface); border: 1px solid var(--line); border-radius: 14px }}
table {{ border-collapse: collapse; width: 100%; min-width: 560px; font-variant-numeric: tabular-nums }}
th, td {{ text-align: left; padding: 12px 16px; border-bottom: 1px solid var(--line); vertical-align: middle }}
th {{ font-family: var(--display); font-size: 11px; letter-spacing: .15em; text-transform: uppercase; color: var(--muted) }}
tr:last-child td {{ border-bottom: 0 }}
td.num {{ font-family: var(--display); font-weight: 700; color: var(--muted); white-space: nowrap }}
td a {{ font-weight: 600; text-decoration-color: var(--lime); text-decoration-thickness: 2px; text-underline-offset: 3px }}
.pill {{ display: inline-block; font-family: var(--display); font-size: 11px; font-weight: 700; letter-spacing: .06em; padding: 2px 10px; border-radius: 999px; white-space: nowrap }}
.pill.campaign {{ background: var(--green); color: var(--lime) }}
.pill.newsletter {{ background: var(--chip); color: var(--chip-fg) }}
.emails {{ display: grid; gap: 40px }}
.email {{ display: grid; grid-template-columns: minmax(0, 340px) minmax(0, 640px); gap: 32px; align-items: start; justify-content: center; scroll-margin-top: 16px; padding-top: 40px; border-top: 1px solid var(--line) }}
.meta {{ position: sticky; top: 16px; display: grid; gap: 14px; min-width: 0 }}
.meta h3 {{ font-size: 24px; line-height: 1.2 }}
dl {{ margin: 0; display: grid; gap: 4px }}
dt {{ font-family: var(--display); font-size: 11px; font-weight: 700; letter-spacing: .15em; text-transform: uppercase; color: var(--muted); margin-top: 8px }}
dd {{ margin: 0 }}
dd.strong {{ font-weight: 600 }}
.confirm {{ background: var(--surface); border: 1px solid var(--line); border-left: 4px solid var(--lime); border-radius: 10px; padding: 16px 18px; display: grid; gap: 8px }}
.confirm ul {{ margin: 0; padding-left: 18px; display: grid; gap: 6px; font-size: 14px }}
.frame {{ min-width: 0; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0, 40, 18, .12) }}
iframe {{ display: block; width: 100%; height: 2400px; border: 0; background: #E9ECE6 }}
footer {{ border-top: 1px solid var(--line) }}
footer .wrap {{ padding-block: 28px; color: var(--muted); font-size: 13px }}
@media (max-width: 900px) {{ .email {{ grid-template-columns: minmax(0, 1fr) }} .meta {{ position: static }} }}
</style>

<header class="mast"><div class="wrap">
  <p class="eyebrow">X-ZONE New Zealand · Email plan for approval</p>
  <h1>Move <span>Freely</span></h1>
  <p class="lede">Our new email newsletter, named after your tagline. Thirteen emails from late November to mid-February: nine newsletters and four campaigns. Each one is shown below exactly as it will look in an inbox.</p>
</div></header>

<main><div class="wrap">
  <div class="intro">
    <div class="panel"><h2>Why "Move Freely"</h2><p>It is the first half of "Move Freely. Live Naturally.", so it reads as X-ZONE before anyone sees the logo. It also says what the emails are for: practical lessons that help people keep moving.</p></div>
    <div class="panel"><h2>What every email has</h2><ul><li>The Move Freely masthead, issue number and date</li><li>A hero photo, headline and one clear button</li><li>"In this issue", then short, numbered lessons</li><li>The week on Instagram and Facebook</li><li>Your sign-off with a photo of you both</li><li>A real Judge.me review, and the range</li></ul></div>
    <div class="panel"><h2>How to approve</h2><p>Scroll through each email. Under "Please confirm" are the facts only you can give us, such as dates, offers and stock. Reply with your yes, or with changes by email number (for example "No. 07: change the button to ...").</p></div>
  </div>

  <section class="sched"><h2>The schedule</h2>
    <div class="tablewrap"><table><thead><tr><th>Issue</th><th>Sends</th><th>Type</th><th>Subject line</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
  </section>

  <section class="emails"><h2>The emails</h2>{"".join(cards)}</section>
</div></main>
<footer><div class="wrap">Words in [square brackets] are filled in once you confirm them. Buttons go to xzone.nz for now and will point to the right pages before sending. Some hero photos are stand-ins until you approve them.</div></footer>
<script>
document.querySelectorAll('iframe').forEach(f => {{
  const fit = () => {{ try {{ const d = f.contentDocument; if (d && d.body) f.style.height = d.documentElement.scrollHeight + 'px'; }} catch (e) {{}} }};
  f.addEventListener('load', () => {{ fit(); setTimeout(fit, 600); setTimeout(fit, 2000); try {{ new ResizeObserver(fit).observe(f.contentDocument.body); }} catch (e) {{}} }});
}});
</script>
'''
open(OUT, 'w').write(page)
print(OUT, f'{len(page.encode())/1024:.0f} KB')

# A single self-contained file (images embedded) to send or open offline.
import base64
def data_uri(m):
    f = m.group(1); mime = 'image/png' if f.endswith('.png') else 'image/jpeg'
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(f'{EM}/images/{f}', 'rb').read()).decode())
solo = re.sub(r'images/(xzone-email-[a-z0-9-]+\.(?:jpg|png))', data_uri, page)
solo = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        + solo.replace('\n<header', '\n</head>\n<body style="margin:0">\n<header', 1) + '</body>\n</html>\n')
SOLO = OUT.replace('.html', '-standalone.html')
open(SOLO, 'w').write(solo)
print(SOLO, f'{len(solo.encode())/1024/1024:.1f} MB')
