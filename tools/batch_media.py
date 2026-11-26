import os, sys, json, glob, re
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_post as R
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CAL = os.path.join(ROOT, "calendar"); P = lambda *a: os.path.join(ROOT, *a)
LOGO = os.path.join(HERE, "logo-white.png")
POOL = {
 "bush": ["brief/photos/bush-clear.jpg", "calendar/small/bushwalk.jpg", "calendar/small/aoraki.jpg"],
 "horopito": ["brief/photos/horopito.jpg", "brief/photos/koromiko.jpg"],
 "koromiko": ["brief/photos/koromiko.jpg", "brief/photos/horopito.jpg"],
 "kumarahou": ["brief/photos/kumarahou.jpg", "brief/photos/bush-clear.jpg"],
 "bushwalk": ["brief/photos/stock-hikers-coast-path-iStock-2245937776.jpg", "brief/photos/stock-hiker-snowy-mountain-iStock-2290792761.jpg", "calendar/small/bushwalk.jpg", "calendar/small/aoraki.jpg", "brief/photos/bush-clear.jpg"],
 "bruise": ["calendar/small/bruise.jpg", "brief/photos/relief-rub-knee.jpg", "brief/photos/relief-rub-leg.jpg"],
 "ankle": ["calendar/small/ankle.jpg", "brief/photos/relief-rub-leg.jpg"],
 "aoraki": ["brief/photos/stock-hiker-snowy-mountain-iStock-2290792761.jpg", "calendar/small/aoraki.jpg", "calendar/small/bushwalk.jpg", "brief/photos/bush-clear.jpg"],
 "running": ["brief/photos/stock-couple-jogging-pier-iStock-1842243532.jpg", "brief/photos/stock-trail-runner-hillside-iStock-471234605.jpg", "calendar/small/running.jpg", "brief/photos/sports-rub-gym.jpg", "brief/photos/sports-spray-gym.jpg"],
 "handsclose": ["calendar/small/handsclose.jpg", "calendar/small/hands.jpg"],
 "shoulder": ["calendar/small/shoulder.jpg", "brief/photos/relief-rollon-shoulder.jpg", "brief/photos/sports-spray-arm.jpg"],
 "founders": ["calendar/small/founders.jpg", "brief/photos/jess-dan-tees.jpg", "brief/photos/jess-dan-garden.jpg"],
 "range": ["calendar/small/range.png", "brief/photos/relief-rub-leg.jpg"],
 "cricket": ["calendar/small/cricket.jpg", "brief/photos/stock-family-ball-lawn-iStock-2247111861.jpg"], "family": ["brief/photos/stock-family-ball-lawn-iStock-2247111861.jpg", "calendar/small/cricket.jpg"], "bikers": ["brief/photos/stock-mountain-bikers-iStock-1134311384.jpg"], "hands": ["calendar/small/hands.jpg"],
}
STOP = set("the and for that this with what why your you are our one not but from have about when then than into every most more some their they them been will just only also".split())
def auto_key(h):
    ws = [re.sub(r"[^\wĀ-ſ'’-]", "", w) for w in h.split()]
    ws = [w for w in ws if len(w) >= 4 and w.lower() not in STOP and not w[0].isdigit()]
    return max(ws, key=len) if ws else None
def variant(path, k, out):
    im = Image.open(path)
    if im.mode in ("P", "LA", "RGBA"):
        im = im.convert("RGBA"); bg = Image.new("RGBA", im.size, (244, 243, 236, 255)); bg.alpha_composite(im); im = bg
    im = im.convert("RGB"); w, h = im.size
    z = [1.0, 1.35, 1.35, 1.7, 1.2][k % 5]
    if any(t in path for t in ("founders","jess-dan","running","stock-")): z = [1.0, 1.12][k % 2]
    ax = [0.5, 0.15, 0.85, 0.5, 0.3][k % 5]; ay = [0.5, 0.4, 0.4, 0.3, 0.6][k % 5]
    cw, ch = w / z, h / z
    x0 = (w - cw) * ax; y0 = (h - ch) * ay
    im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).save(out, quality=95); return out
KEYS = {"w1-tue": "wrong", "w10-tue": "nobody", "w5-tue": "warm-up", "w7-tue": "lights"}
def render_any(photo, hook, key, sub, out, **kw):
    px = 70
    while True:
        try: R.render(photo, hook, key, sub, LOGO, out, headline_px=px, **kw); return px
        except AssertionError:
            px -= 4
            if px < 40: raise
def content():
    sel = json.load(open(os.path.join(CAL, "selection.json")))["weeks"]
    ids = {p for w in sel.values() for p, _ in w}; out = {}
    for f in sorted(glob.glob(os.path.join(CAL, "content-*.json"))):
        for w in json.load(open(f))["weeks"]:
            for p in w["posts"]:
                if p["id"] in ids: out[p["id"]] = p
    return out
def story_media(OUT):
    import csv
    rows = list(csv.DictReader(open(os.path.join(CAL, "buffer", "buffer-stories.csv"))))
    def pool_for(t):
        t = t.lower()
        for kws, key in [(("jess","dan","thank you","kirihimete","waitangi","whānau"), "founders"), (("stockist",), "range"), (("sleep","recovery","routine","sports range","mollie"), "running"),
                         (("tramp","hike","track"), "bushwalk"), (("overdo","warm-up","training"), "bikers"), (("parents","kids","sideline"), "family"), (("bruise",), "bruise"), (("herb","native","kūmarahou","harakeke"), "bush"), (("kit","sale","gift","prices"), "range")]:
            if any(k in t for k in kws): return key
        return "bush"
    for r in rows:
        t = r["text"]
        t = re.sub(r"find us at \{STOCKIST\}, (\w+)", r"find us in \1", t)
        t = t.replace("Old prices held until 31 December 2026", "Today\u2019s prices until 30 December 2026").replace(": {OFFER}", "")
        t = t.replace("'", "\u2019")
        sents = re.split(r"(?<=[.?!])\s+", t.strip())
        hook = sents[0].rstrip(".")
        sub = " ".join(sents[1:]) or None
        pool = [P(x) for x in POOL[pool_for(r["text"])]]
        ph = variant(pool[0], 0, f"/tmp/st-{r['story']}.jpg") if pool_for(r["text"]) not in ("founders","running") else pool[0]
        px = 76
        while True:
            try:
                R.render(ph, hook, auto_key(hook), sub, LOGO, os.path.join(OUT, r["story"] + ".jpg"), headline_px=px, canvas_h=1920, photo_h=1000, text_y=1060, logo_y=1590, max_bottom=1540, sub_px=36, max_lines=4); break
            except AssertionError: px -= 4
    print("stories", len(rows))
if __name__ == "__main__":
    OUT = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "stories":
        os.makedirs(OUT, exist_ok=True); story_media(OUT); sys.exit()
    C = content(); made = []
    for pid, p in C.items():
        pool = [P(x) for x in POOL.get(p["photo"], POOL["bush"])]
        if p["format"] == "Carousel":
            n = len(p["slides"])
            for i, s in enumerate(p["slides"]):
                ph = variant(pool[i % len(pool)], i if i < 5 else i + 1, f"/tmp/cv-{pid}-{i}.jpg")
                o = os.path.join(OUT, pid); os.makedirs(o, exist_ok=True)
                body = p["subline"] if (i == 0 and False) else s["b"]
                render_any(ph, s["h"], auto_key(s["h"]), body, os.path.join(o, f"slide-{i+1:02d}.jpg"), swipe=(i == 0), sub_px=38)
            made.append((pid, n))
        elif p["format"] == "Reel":
            ph = variant(pool[0], 0, f"/tmp/cv-{pid}.jpg")
            o = os.path.join(OUT, pid); os.makedirs(o, exist_ok=True)
            render_any(ph, p["headline"], KEYS.get(pid) or auto_key(p["headline"]), p["subline"], os.path.join(o, "reel-image.jpg"), sub_px=36)
            made.append((pid, "reel-image"))
    tp = [P(x) for x in POOL["bushwalk"]]
    o = os.path.join(OUT, "w3-testimonial"); os.makedirs(o, exist_ok=True)
    quote = "I have found the X-Zone Joints product easy to use. I use it both for relieving aches and pains in my joints and for prevention support prior to hiking/tramping. It has been really effective. I am on my second bottle."
    render_any(variant(tp[0], 0, "/tmp/cv-testi.jpg"), "\u201cRub it on and forget\u201d", "forget", "\u201c" + quote + "\u201d", os.path.join(o, "post.jpg"), foot="Maria G., New Zealand \u00b7 Verified review \u00b7 Joints Rub", sub_px=34, max_bottom=1190)
    print(made)
