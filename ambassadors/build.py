"""Build the ambassador posts mock-up.

Reads ambassadors/content/*.json (one file per ambassador, see
.claude/skills/brand-ambassador-posts/SKILL.md) and writes
ambassadors/xzone-ambassador-posts.html with photos embedded.

Run: python3 ambassadors/build.py
"""
import base64
import datetime
import glob
import html
import io
import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "photos")
OUT = os.path.join(HERE, "xzone-ambassador-posts.html")

QUESTIONS = {
    1: "Who are you? Your background, occupation and where you are based.",
    2: "What is your sport or passion, what drew you to it, and what are the pros and cons?",
    3: "What is your biggest achievement to date, and what is your ultimate goal?",
    4: "How does X-ZONE help?",
}
SERIES_INTRO = [
    "Welcome to our Ambassador blog series, where we celebrate the diverse passions and pursuits of ordinary Kiwis achieving the extraordinary. From athletes to artists and everything in between, they embody the spirit of New Zealand through their shared love for their respective sports, activities, passions and occupations.",
    "Join us in discovering their inspiring stories.",
]
# ground, accent, text on accent (brand spec range pairs)
RANGES = {
    "relief": ("#0D441F", "#E0E64A", "#0D441F"),
    "joints": ("#131D4A", "#F3AC3E", "#131D4A"),
    "sports": ("#1F1C1D", "#E44726", "#FFFFFF"),
}

e = html.escape
_cache = {}


def data_uri(name, max_w=900):
    """Embed a photo, resized, as a data URI. Returns None if missing."""
    if not name:
        return None
    path = os.path.join(PHOTOS, name)
    if not os.path.exists(path):
        return None
    if path in _cache:
        return _cache[path]
    im = Image.open(path)
    buf = io.BytesIO()
    if name.endswith(".png"):
        im.save(buf, "PNG", optimize=True)
        uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    else:
        im = im.convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        im.save(buf, "JPEG", quality=82, optimize=True)
        uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    _cache[path] = uri
    return uri


def photo(p, cls="", wrap=True):
    uri = data_uri(p.get("file"))
    if uri:
        return f'<img class="{cls}" src="{uri}" alt="{e(p["alt"])}">'
    return f'<div class="ph {cls}"><span><b>Photo to add</b>{e(p["note"])}</span></div>'


def nice_date(s):
    d = datetime.date.fromisoformat(s)
    return f"{d.day} {d.strftime('%B %Y')}"


def caption_html(name_handle, text):
    return f'<div class="caption"><b>{e(name_handle)}</b> {e(text)}</div>'


def section(a, logo_green, logo_white, icon):
    ground, accent, on_accent = RANGES[a["range"]]
    photos = a["photos"] + [{"file": None, "alt": "", "note": "Second photo"}] * (2 - len(a["photos"]))
    first = a["name"].split()[0]
    title = f'Introducing: {a["name"]}, {a["sport"]}'
    url = f'xzone.nz/blogs/ambassadors/introducing-{a["slug"]}'

    # article body
    body = []
    for ans in a["answers"]:
        body.append(f'<h3>{ans["q"]}. {e(QUESTIONS[ans["q"]])}</h3>')
        body += [f'<p class="a">{e(p)}</p>' for p in ans["paras"]]
        if ans["q"] == 2 and a.get("pull_quote"):
            body.append(f'<blockquote class="pull">{e(a["pull_quote"])}</blockquote>')
        if ans["q"] == 3:
            body.append(f'<figure class="inline-photo">{photo(photos[1])}<figcaption class="cap">{e(photos[1]["note"])}</figcaption></figure>')

    article = f"""
    <div class="browser">
      <div class="bar"><i></i><i></i><i></i><span>{e(url)}</span></div>
      <div class="site-nav"><img src="{logo_green}" alt="X-ZONE"><ul><li>Shop</li><li>Our herbs</li><li>Stockists</li><li class="on">Ambassadors</li></ul></div>
      <article class="article">
        <div class="series">Ambassador series</div>
        <h1>{e(title)}</h1>
        <div class="byline"><b>{nice_date(a["date"])}</b><span class="share">Share</span></div>
        <div class="intro">{''.join(f'<p>{e(p)}</p>' for p in SERIES_INTRO)}</div>
        <figure class="hero">{photo(photos[0])}<figcaption class="cap">{e(photos[0]["note"])}</figcaption></figure>
        <div class="amb-title">{a["number"]}. {e(a["name"])}, {e(a["role"])}</div>
        {''.join(body)}
        <p class="more">{e(a["more"]["label"])}: <a href="{e(a["more"]["url"])}">{e(a["more"]["url"].replace("https://", ""))}</a></p>
      </article>
    </div>"""

    ig = a["ig"]
    cov = photos[ig.get("cover_photo", 0)]
    fin = photos[ig.get("end_photo", 1)]
    cover = f"""
      <div class="slide cover">
        <div class="band"><img class="logo" src="{logo_white}" alt=""><h4>{e(ig["headline"])}</h4><p>{e(ig["subline"])}</p></div>{photo(cov, "bg")}
        <div class="pill" style="background:{accent};color:{on_accent}">{e(ig["pill"])}</div>
        <div class="foot"><span>@xzonenz</span><span>xzone.nz</span></div>
      </div>"""
    quote = f"""
      <div class="slide"><div class="quote-slide" style="background:{ground}">
        <div class="mark" style="color:{accent}" aria-hidden="true">&ldquo;</div>
        <blockquote>{e(ig["quote"])}</blockquote>
        <div class="who"><b>{e(a["name"])}</b>{e(a["role"])}</div>
        <img class="logo" src="{logo_white}" alt="">
      </div></div>"""
    end = f"""
      <div class="slide">{photo(fin, "bg")}<div class="wash"></div>
        <div class="end"><h4>Read {e(first)}'s full story</h4><p>Ambassador {a["number"]} &middot; link in bio</p></div>
        <div class="foot"><span>@xzonenz</span><span>xzone.nz</span></div>
      </div>"""
    social = f"""
    <div class="ig">
      <div class="ig-head"><span class="ava"><img src="{icon}" alt=""></span>xzonenz</div>
      <div class="slides" tabindex="0" aria-label="Instagram carousel, 3 slides, scroll sideways">{cover}{quote}{end}</div>
      <div class="dots"><i></i><i></i><i></i></div>
      <div class="ig-body">{caption_html("xzonenz", ig["caption"])}<div class="tags">{e(ig["hashtags"])}</div></div>
    </div>
    <p class="hint">Swipe or scroll the post sideways for slides 2 and 3.</p>
    <div class="fb">
      <div class="who"><span class="ava"><img src="{icon}" alt=""></span><div><b>X-ZONE New Zealand</b><small>Facebook &middot; link post</small></div></div>
      <div class="caption">{e(a["fb"]["caption"])}</div>
      <div class="link-card">{photo(photos[0])}<div class="t"><small>xzone.nz</small><b>{e(title)}</b></div></div>
    </div>"""

    checks = f"""
    <div class="checks">
      <div class="box edits"><h3>What we changed from the draft</h3><ul>{''.join(f'<li>{e(x)}</li>' for x in a["edits"])}</ul></div>
      <div class="box flags"><h3>Confirm before posting</h3><ul>{''.join(f'<li>{e(x)}</li>' for x in a["flags"])}</ul></div>
    </div>"""

    return f"""
<section class="amb" id="{a["slug"]}">
  <div class="amb-head"><span class="num">{a["number"]:02d}</span><h2>{e(a["name"])}</h2><span class="meta">{e(a["role"])} &middot; {e(a["range"].title())} range &middot; drafted for {nice_date(a["date"])}</span></div>
  <div class="grid">
    <div><div class="label col-title">Blog post</div>{article}</div>
    <div><div class="label col-title">Instagram carousel and Facebook</div>{social}</div>
  </div>
  {checks}
</section>"""


def main():
    items = [json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(HERE, "content", "*.json"))]
    items.sort(key=lambda a: -a["number"])
    logo_green = data_uri("logo-green.png")
    logo_white = data_uri("logo-white.png")
    icon = data_uri("../../calendar/small/icon.png")
    nav = "".join(f'<a href="#{a["slug"]}">{a["number"]}. {e(a["name"])}</a>' for a in items)
    sections = "".join(section(a, logo_green, logo_white, icon) for a in items)
    tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    out = tpl.replace("{{NAV}}", nav).replace("{{SECTIONS}}", sections).replace("{{LOGO_WHITE}}", logo_white)
    open(OUT, "w", encoding="utf-8").write(out)
    print(f"Wrote {OUT} ({len(out)//1024} KB, {len(items)} ambassadors)")


if __name__ == "__main__":
    main()
