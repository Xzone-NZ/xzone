"""Build the X-ZONE team guides as branded A4 PDFs.

    python3 guides/build.py

Writes guides/<name>.html (source), then render.js prints guides/<name>.pdf with
Playwright Chromium (Node). Brand colours and type follow brief/06-brand-spec.md.
"""
import html, re, sys
from pathlib import Path
from guide_content import GUIDES

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def prompt(text, label="Copy this prompt"):
    """A copy-ready prompt box. [square brackets] become highlighted placeholders."""
    esc = html.escape(text.strip("\n"))
    esc = re.sub(r"\[([^\]]+)\]", r'<span class="ph">[\1]</span>', esc)
    return f'<div class="prompt"><span class="label">{label}</span>{esc}</div>'


def page(inner, n, title):
    return (f'<section class="page">{inner}'
            f'<div class="foot"><img src="../ambassadors/photos/logo-green.png" alt="X-ZONE">'
            f'<span>{title}</span><span class="pg">{n:02d}</span></div></section>')


def cover(c):
    return f'''<section class="page cover">
  <div class="photo" style="background-image:url('{c["photo"]}');background-position:{c.get("pos","center")}">
    <div class="logo"><img src="../ambassadors/photos/logo-green.png" alt="X-ZONE"></div>
  </div>
  <div class="body">
    <span class="pill">{c["pill"]}</span>
    <h1>{c["title"]}</h1>
    <div class="sub">{c["sub"]}</div>
  </div>
  <div class="meta"><span><b>For</b> {c["for"]}</span><span><b>Version</b> {c["version"]}</span></div>
</section>'''


def build_html(g):
    pages = [cover(g["cover"])]
    for i, body in enumerate(g["pages"], start=2):
        pages.append(page(body(prompt), i, g["footer"]))
    return f'''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8">
<title>{g["title"]}</title>
<link rel="stylesheet" href="fonts/poppins-local.css">
<link rel="stylesheet" href="style.css">
</head><body>
{"".join(pages)}
</body></html>'''


def main():
    import json, subprocess
    only = set(sys.argv[1:])
    jobs = []
    for g in GUIDES:
        if only and g["slug"] not in only:
            continue
        src = ROOT / f'{g["slug"]}.html'
        src.write_text(build_html(g), encoding="utf-8")
        jobs.append({"html": str(src), "pdf": str(ROOT / f'{g["slug"]}.pdf')})
    # Playwright ships as a Node package in this environment, so the PDF step runs in render.js.
    subprocess.run(["node", str(ROOT / "render.js"), json.dumps(jobs)], check=True)


if __name__ == "__main__":
    main()
