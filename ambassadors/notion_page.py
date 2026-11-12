"""Print the Notion page content (Notion-flavored Markdown) for one ambassador.

Usage: python3 ambassadors/notion_page.py <slug> [commit-sha]
The commit sha pins the image URLs (raw GitHub, repo is public); defaults to HEAD.
The skill pastes this output as the content of the ambassador's Output Log row.
"""
import json
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import QUESTIONS, SERIES_INTRO, nice_date  # noqa: E402

slug = sys.argv[1]
sha = sys.argv[2] if len(sys.argv) > 2 else subprocess.check_output(["git", "-C", HERE, "rev-parse", "HEAD"], text=True).strip()
path = glob.glob(os.path.join(HERE, "content", f"*-{slug}.json"))[0]
a = json.load(open(path, encoding="utf-8"))
raw = f"https://raw.githubusercontent.com/Xzone-NZ/xzone/{sha}/ambassadors"
readme = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
mock = next((l.split(": ", 1)[1].strip() for l in readme.splitlines() if l.startswith("Live mock-up:")), "")


def esc(t):
    return t.replace("<", "&lt;").replace(">", "&gt;")


def para(t):
    return "\n".join(esc(line) + ("\\" if i < len(t.split("\n")) - 1 and line else "") for i, line in enumerate(t.split("\n")))


out = []
out.append(f'<callout icon="📝" color="gray_bg">\nAmbassador {a["number"]}: {esc(a["name"])}, {esc(a["role"])}. Draft for Jess and Dan to approve. Mock-up: [{mock}]({mock})\n</callout>')
out.append("## Confirm before posting")
out += [f"- [ ] {esc(f)}" for f in a["flags"]]
out.append("## Instagram carousel")
for i in (1, 2, 3):
    out.append(f"![Slide {i}]({raw}/instagram/{slug}-slide-{i}.png)")
out.append("**Caption**")
out.append("```\n" + a["ig"]["caption"] + "\n\n" + a["ig"]["hashtags"] + "\n```")
out.append("## Facebook post")
out.append(f"![Facebook photo]({raw}/photos/{a['photos'][0]['file']})" if a["photos"][0].get("file") else "")
out.append("```\n" + a["fb"]["caption"] + "\n```")
out.append(f"## Blog post\n\n**Introducing: {esc(a['name'])}, {esc(a['sport'])}**\\\n{nice_date(a['date'])}")
out += [esc(p) for p in SERIES_INTRO]
out.append(f"**{a['number']}. {esc(a['name'])}, {esc(a['role'])}**")
for ans in a["answers"]:
    out.append(f"### {ans['q']}. {esc(QUESTIONS[ans['q']])}")
    out += [esc(p) for p in ans["paras"]]
out.append(f"{esc(a['more']['label'])}: [{a['more']['url']}]({a['more']['url']})")
if a.get("buffer"):
    out.append("## Buffer drafts")
    out += [f"- {k.title()}: draft `{v}` (not scheduled)" for k, v in a["buffer"].items()]
out.append("## What we changed from the draft")
out += [f"- {esc(x)}" for x in a["edits"]]
print("\n\n".join(x for x in out if x))
