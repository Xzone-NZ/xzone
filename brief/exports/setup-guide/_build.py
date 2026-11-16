"""PDF guide: setting up the Move Freely emails in Shopify. Run from the repo root."""
import json, re, html, os, datetime, base64
import subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
HERE = os.path.join(ROOT, 'brief', 'exports', 'setup-guide')
emails = json.load(open(os.path.join(ROOT, 'calendar', 'extra.json')))['emails']
def ph(s): return re.sub(r'\{([A-Z_]+)\}', lambda m: '[' + m.group(1).replace('_', ' ').lower() + ']', s)
def nice(d): d = datetime.date.fromisoformat(d); return f'{d.strftime("%a")} {d.day} {d.strftime("%b %Y")}'
def b64(p): return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
cover = b64(os.path.join(HERE, 'cover-email.png'))
logo = b64(os.path.join(ROOT, 'brief', 'exports', 'shopify-emails', 'images', 'xzone-email-logo.png'))
imgs = sorted(os.listdir(os.path.join(ROOT, 'brief', 'exports', 'shopify-emails', 'images')))

sched = ''.join(f'<tr><td class="n">{e["week"]:02d}</td><td class="nw">{nice(e["date"])}</td><td><span class="pill {e["type"]}">{"Campaign" if e["type"]=="campaign" else "Newsletter"}</span></td>'
                f'<td><b>{html.escape(ph(e["subject"]))}</b><br><span class="mut">{html.escape(ph(e["preheader"]))}</span></td><td class="mono">xzone-email-w{e["week"]:02d}.html</td></tr>' for e in emails)
def ph_list(e):
    found = sorted(set(re.findall(r'\[[a-z ]+\]', open(os.path.join(ROOT, 'brief/exports/shopify-emails', f'xzone-email-w{e["week"]:02d}.html')).read())) - {'[business address]', '[if mso]', '[endif]'})
    return ', '.join(found) or 'none'
fills = ''.join(f'<tr><td class="n">{e["week"]:02d}</td><td>{html.escape(ph_list(e))}</td><td>{html.escape((e.get("cta") or {}).get("label",""))}</td></tr>' for e in emails)

def step(n, title, body): return f'<section class="step"><div class="num">{n}</div><div class="sb"><h2>{title}</h2>{body}</div></section>'

doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Move Freely: Shopify setup guide</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap">
<style>
@page {{ size: A4; margin: 18mm 17mm 20mm; }}
@page :first {{ margin: 0; }}
:root {{ --g:#004F23; --l:#E0E64A; --ink:#1d2b21; --mut:#5d6f62; --sage:#F3F5EF; --line:#dde3d8; }}
* {{ box-sizing:border-box }}
body {{ margin:0; font-family:'Inter',Arial,sans-serif; font-size:10.5pt; line-height:1.55; color:var(--ink); -webkit-print-color-adjust:exact; print-color-adjust:exact }}
h1,h2,h3 {{ font-family:'Poppins',Arial,sans-serif; margin:0; color:var(--g) }}
p {{ margin:0 0 8px }}
.cover {{ height:297mm; background:var(--g); color:#fff; display:grid; grid-template-columns: 1.1fr .9fr; page-break-after:always; position:relative; overflow:hidden }}
.cover .txt {{ padding:22mm 10mm 20mm 18mm; display:flex; flex-direction:column; gap:14px }}
.cover .logo {{ background:#fff; border-radius:999px; padding:9px 18px; width:max-content }}
.cover .logo img {{ height:26px; display:block }}
.cover .eb {{ font-family:Poppins; font-weight:700; font-size:9pt; letter-spacing:.2em; text-transform:uppercase; color:var(--l); margin-top:40mm }}
.cover h1 {{ color:#fff; font-size:50pt; line-height:.98; letter-spacing:-.02em }}
.cover h1 span {{ color:var(--l) }}
.cover .sub {{ font-size:15pt; line-height:1.4; color:#d5e0d8; max-width:88mm }}
.cover .meta {{ margin-top:auto; font-size:9.5pt; color:#a9bcae }}
.cover .pic {{ padding:30mm 0 0 0 }}
.cover .pic img {{ width:100%; display:block; border-radius:10px 0 0 10px; box-shadow:0 20px 50px rgba(0,0,0,.35) }}
.cover .stripe {{ position:absolute; left:0; right:0; bottom:0; height:8px; background:var(--l) }}
.lead {{ font-size:12pt; color:var(--mut); margin-bottom:16px }}
h1.sec {{ font-size:22pt; margin:0 0 6px }}
.box {{ background:var(--sage); border-radius:10px; padding:14px 16px; margin:10px 0 }}
.box h3 {{ font-size:11pt; margin-bottom:6px }}
.tip {{ border-left:4px solid var(--l); background:var(--sage); padding:10px 14px; border-radius:0 8px 8px 0; margin:10px 0; font-size:10pt }}
.tip b:first-child {{ font-family:Poppins; color:var(--g) }}
.warn {{ border-left-color:#c9541f }}
ul, ol {{ margin:4px 0 8px; padding-left:20px }} li {{ margin:3px 0 }}
.step {{ display:grid; grid-template-columns:34px 1fr; gap:14px; padding:14px 0 10px; border-top:1px solid var(--line); break-inside:avoid-page }}
.num {{ width:34px; height:34px; border-radius:50%; background:var(--l); color:var(--g); font-family:Poppins; font-weight:800; font-size:14pt; display:flex; align-items:center; justify-content:center }}
.step h2 {{ font-size:14pt; margin:4px 0 6px }}
.path {{ font-family:Poppins; font-weight:600; color:var(--g); background:#e6ecd9; padding:1px 7px; border-radius:5px; white-space:nowrap }}
code, .mono {{ font-family:'SFMono-Regular',Menlo,Consolas,monospace; font-size:8.8pt }}
pre {{ background:#13261a; color:#e4ece5; border-radius:8px; padding:10px 12px; font-size:8.6pt; line-height:1.5; white-space:pre-wrap; word-break:break-all; margin:8px 0 }}
pre .hl {{ background:var(--l); color:var(--g); padding:0 3px; border-radius:3px }}
pre .dim {{ color:#8fa596 }}
table {{ width:100%; border-collapse:collapse; font-size:9pt; margin:8px 0 }}
th {{ text-align:left; font-family:Poppins; font-size:7.5pt; letter-spacing:.12em; text-transform:uppercase; color:var(--mut); border-bottom:2px solid var(--g); padding:6px 6px }}
td {{ padding:6px; border-bottom:1px solid var(--line); vertical-align:top }}
tr {{ break-inside:avoid }}
td.n {{ font-family:Poppins; font-weight:700; color:var(--g) }} .nw {{ white-space:nowrap }} .mut {{ color:var(--mut) }}
.pill {{ font-family:Poppins; font-size:7pt; font-weight:700; padding:2px 7px; border-radius:999px; white-space:nowrap }}
.pill.campaign {{ background:var(--g); color:var(--l) }} .pill.newsletter {{ background:#e6ecd9; color:var(--g) }}
.cols {{ display:grid; grid-template-columns:1fr 1fr; gap:12px }}
.check li {{ list-style:none; margin-left:-20px; padding-left:22px; position:relative }}
.check li::before {{ content:""; position:absolute; left:0; top:3px; width:12px; height:12px; border:1.5px solid var(--g); border-radius:3px }}
.pb {{ page-break-before:always }}
.files {{ columns:2; font-size:8.8pt; margin:6px 0 }}
</style></head><body>

<div class="cover">
  <div class="txt">
    <div class="logo"><img src="{logo}" alt="X-ZONE"></div>
    <p class="eb">Shopify setup guide</p>
    <h1>Move <span>Freely</span></h1>
    <p class="sub">How to load your 13 summer emails into Shopify, check them and schedule them.</p>
    <p class="meta">For Jess and Dan · X-ZONE New Zealand<br>Sends from 26 November 2026 to 18 February 2027</p>
  </div>
  <div class="pic"><img src="{cover}" alt=""></div>
  <div class="stripe"></div>
</div>

<h1 class="sec">Before you start</h1>
<p class="lead">Setting up the first email takes about 30 minutes. After that, each one takes about 10. Do it on a computer, not a phone: Shopify's code editor only works on a desktop.</p>
<div class="cols">
<div class="box"><h3>What you have</h3><ul>
<li><b>13 email files</b>, one per week: <code>xzone-email-w01.html</code> to <code>xzone-email-w13.html</code></li>
<li><b>An images folder</b> with {len(imgs)} pictures: the logo, 13 hero photos, your photo and the range photo</li>
<li><b>The approval page</b>, showing every email as it will look</li></ul></div>
<div class="box"><h3>What you need</h3><ul>
<li>Shopify admin access with <b>Shopify Email</b> (now called Shopify Messaging) installed</li>
<li>A plain text editor: <b>TextEdit</b> on a Mac or <b>Notepad</b> on Windows</li>
<li>Your <b>business address</b>, which the law requires in every marketing email</li>
<li>The dates and offers listed on the approval page under "Please confirm"</li></ul></div>
</div>
<div class="tip"><b>How it works.</b> Each email is a finished design written in code. You upload the pictures to Shopify once, tell each email where they are, fill in a few gaps such as dates, then import the file into Shopify. Shopify sends it to your subscribers.</div>

<h1 class="sec" style="margin-top:18px">Part 1: Do this once</h1>
{step(1, 'Upload the pictures to Shopify', f'''
<ol><li>In Shopify admin, go to <span class="path">Content</span> → <span class="path">Files</span>.</li>
<li>Click <b>Upload files</b> and select every picture in the <code>images</code> folder.</li>
<li><b>Keep the file names exactly as they are.</b> The emails look for these names.</li></ol>
<div class="files">{"".join(f"<div>{f}</div>" for f in imgs)}</div>''')}
{step(2, 'Find your Files folder address', '''
<p>Each email needs to know where your pictures live on Shopify. You find that address once and reuse it in every email.</p>
<ol><li>In <span class="path">Content</span> → <span class="path">Files</span>, find <code>xzone-email-logo.png</code> and click its <b>copy link</b> icon.</li>
<li>Paste the link somewhere you can edit it, for example a note. It will look like this:</li></ol>
<pre>https://cdn.shopify.com/s/files/1/0123/4567/8901/files/<span class="dim">xzone-email-logo.png?v=1732512345</span></pre>
<ol start="3"><li>Delete the file name and everything after it (the grey part). Keep the slash at the end:</li></ol>
<pre><span class="hl">https://cdn.shopify.com/s/files/1/0123/4567/8901/files/</span></pre>
<p>This is your <b>Files folder address</b>. Save it in your note. The numbers above are an example; yours will be different.</p>''')}

<h1 class="sec pb">Part 2: For each email</h1>
<p class="lead">Repeat these steps for each of the 13 emails, using the schedule on the last page. Start with No. 01.</p>
{step(3, 'Open the email file and add the folder address', '''
<ol><li>Right-click the email file (for example <code>xzone-email-w01.html</code>) and choose <b>Open With</b> → <b>TextEdit</b> (Mac) or <b>Notepad</b> (Windows). Don't double-click it, because that opens it in a browser.</li>
<li>Near the top, find this line:</li></ol>
<pre>{%% assign img = "<span class="hl">PASTE-SHOPIFY-FILES-FOLDER-URL-HERE/</span>" %%}</pre>
<ol start="3"><li>Replace the highlighted text with your Files folder address. Keep the quote marks. It should end up like this:</li></ol>
<pre>{%% assign img = "https://cdn.shopify.com/s/files/1/0123/4567/8901/files/" %%}</pre>
<div class="tip"><b>Mac users:</b> if TextEdit shows the email as a picture instead of code, go to <b>TextEdit</b> → <b>Settings</b> → <b>Open and Save</b> and tick <b>Display HTML files as HTML code instead of formatted text</b>. Then open the file again.</div>''').replace('%%', '%')}
{step(4, 'Fill in the gaps', '''
<p>Use <b>Find</b> (Cmd+F on a Mac, Ctrl+F on Windows) to search for <code>[</code> and replace every word in square brackets:</p>
<ul><li><code>[business address]</code> in the footer of every email</li>
<li>Dates and offers such as <code>[date]</code> or <code>[offer]</code> in some emails (listed on the last page)</li></ul>
<p><b>Button links.</b> Every button currently goes to <code>https://www.xzone.nz/</code>. Search for that address and replace it with the page you want, for example a product page. Adding tracking tags shows you which sales came from the email:</p>
<pre>https://www.xzone.nz/products/x-zone-joints-rub<span class="hl">?utm_source=shopify&amp;utm_medium=email&amp;utm_campaign=move-freely-06</span></pre>
<p>Change the number at the end to match the issue. Save the file when you're done (Cmd+S or Ctrl+S).</p>
<div class="tip warn"><b>Don't change</b> anything inside double curly brackets, such as <code>{{ unsubscribe_link }}</code> or <code>{{ open_tracking_block }}</code>. Shopify fills these in when it sends.</div>''')}
{step(5, 'Create the email in Shopify', '''
<ol><li>In Shopify admin, go to <span class="path">Marketing</span> → <span class="path">Create campaign</span> → <span class="path">Shopify Email</span>. (In some stores you'll find it under <span class="path">Apps</span> → <span class="path">Shopify Messaging</span>.)</li>
<li>When asked to choose a template, select <b>Code your own</b>.</li>
<li>Click <b>Import</b> and choose the email file you just saved. You can also copy everything in the file (Cmd+A, then Cmd+C) and paste it into the code box.</li>
<li>Check the preview. You should see the logo, the photo and the green and lime design.</li></ol>
<div class="tip"><b>No "Code your own" option?</b> Shopify is still rolling it out, so some stores don't have it yet. Contact Shopify Support and ask them to turn on custom-coded emails for Shopify Email.</div>''')}
{step(6, 'Add the subject line, preview text and audience', '''
<ol><li>Copy the <b>subject line</b> and <b>preview text</b> for this email from the schedule on the last page into Shopify's fields. The preview text is the short line people see next to the subject in their inbox.</li>
<li>Check the <b>sender name</b> reads <b>X-ZONE New Zealand</b> and the reply address is one you both read. The emails say "Reply to this email", so replies need to reach you.</li>
<li>Under <b>To</b>, choose your subscribers, for example <b>Email subscribers</b>.</li></ol>''')}
{step(7, 'Send yourself a test', '''
<ol><li>Click <b>Send test</b> and enter your own email addresses. You can add up to five.</li>
<li>Open the test on a computer and on a phone, and if you can, in both Gmail and Outlook.</li></ol>
<ul class="check"><li>The logo, photos, your photo and the range picture all show</li>
<li>No square brackets left anywhere</li>
<li>Every button goes to the right page</li>
<li>The subject line and preview text look right in the inbox</li>
<li>The Unsubscribe link at the bottom works</li></ul>
<p class="mut">In Outlook on Windows the headings show in Arial instead of Poppins. That's expected, because Outlook blocks web fonts.</p>''')}
{step(8, 'Schedule it', '''
<p>Click <b>Review</b>, then choose <b>Schedule</b> and set the date from the schedule on the last page. Pick a time when your customers usually read email, such as 7:30 am or 7:30 pm. Use the same time each week so people know when to expect Move Freely.</p>''')}

<h1 class="sec pb">If something goes wrong</h1>
<table><thead><tr><th style="width:34%">What you see</th><th>What to do</th></tr></thead><tbody>
<tr><td><b>Pictures are missing</b> or show as broken boxes</td><td>Check the folder address in step 3 ends with <code>/files/</code> and has no file name or <code>?v=</code> after it. Check the pictures are uploaded in Content → Files with their original names.</td></tr>
<tr><td>Shopify says <b>open_tracking_block</b> isn't valid</td><td>Search the file for <code>open_tracking_block</code> and change it to <code>open_tracking</code>, keeping the curly brackets. Shopify's help pages use both names.</td></tr>
<tr><td>Shopify says the <b>unsubscribe link is missing</b></td><td>Check the footer still contains <code>{{{{ unsubscribe_link }}}}</code>. Start again from the original file if it was deleted by mistake.</td></tr>
<tr><td>Shopify says the <b>code is too large</b></td><td>The limit is 50 KB, and each email is about 19 KB, so this shouldn't happen. Check you didn't paste the email in twice.</td></tr>
<tr><td>The email looks like <b>plain text</b> in the preview</td><td>The file was probably saved as rich text. Start again from the original file and use step 3's TextEdit tip.</td></tr>
<tr><td><b>Headings look plainer</b> in Outlook</td><td>Expected. Outlook uses Arial instead of Poppins. Everything else stays the same.</td></tr>
<tr><td>The email is <b>cut off in Gmail</b> with "View entire message"</td><td>Gmail clips emails over about 100 KB. Ours are about 19 KB, so check nothing was pasted in twice.</td></tr>
</tbody></table>

<h3 style="margin-top:16px">Before the very first send</h3>
<ul class="check">
<li>Approve all 13 emails on the approval page, including the stand-in hero photos</li>
<li>Your business address is ready to put in every footer</li>
<li>The reply address on your emails reaches you both</li>
<li>Courier last-order dates for Christmas (No. 03) and the old-price end date (Nos. 01 to 03)</li>
<li>The offer for the pre-Christmas sale (No. 04) and the survey link (No. 13)</li></ul>

<h1 class="sec pb">The schedule</h1>
<p class="lead">Copy the subject line and preview text into Shopify exactly as written. Replace anything in square brackets.</p>
<table><thead><tr><th>No.</th><th>Sends</th><th>Type</th><th>Subject line and preview text</th><th>File</th></tr></thead><tbody>{sched}</tbody></table>
<h3 style="margin-top:14px">Gaps to fill in each email</h3>
<p class="mut">Every email also needs [business address] in the footer and its button link.</p>
<table><thead><tr><th>No.</th><th>Square-bracket gaps</th><th>Button text</th></tr></thead><tbody>{fills}</tbody></table>
</body></html>'''
open(os.path.join(HERE, 'guide.html'), 'w').write(doc)
subprocess.run(['node', os.path.join(HERE, '_pdf.js'), HERE], check=True)
