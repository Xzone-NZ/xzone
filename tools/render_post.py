#!/usr/bin/env python3
"""X-ZONE feed post in the approved 25 Nov look (1080 x 1350).
Photo on top (650 px), solid green #004F23 panel below, white Poppins ExtraBold hook
with a lime #E0E64A underline BEHIND the key word (descenders break through),
white Poppins Medium subline, white logo bottom right.

Usage:
  python3 render_post.py --photo photo.jpg --hook "Why we've held off." --key "held off" \
      --sub "One or two plain lines." --logo logo-white.png --out post.jpg
Fonts: Poppins_800ExtraBold.ttf and Poppins_500Medium.ttf in the same folder.
Rules baked in: logo bottom right in the green panel (never over a face);
one key word underlined; no highlighter block; no lime text.
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont

W, H, PHOTO_H = 1080, 1350, 650
GREEN, LIME, WHITE = (0, 79, 35), (224, 230, 74), (255, 255, 255)
MARGIN = 72
HERE = os.path.dirname(os.path.abspath(__file__))

def font(name, size): return ImageFont.truetype(os.path.join(HERE, name), size)

def wrap(draw, text, f, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))

def render(photo, hook, key, sub, logo, out, headline_px=70, sub_px=32, callout=None, button=None):
    canvas = Image.new("RGB", (W, H), GREEN)
    canvas.paste(cover(Image.open(photo).convert("RGB"), W, PHOTO_H), (0, 0))
    d = ImageDraw.Draw(canvas)
    hf, sf = font("Poppins_800ExtraBold.ttf", headline_px), font("Poppins_500Medium.ttf", sub_px)
    lines = wrap(d, hook, hf, W - 2 * MARGIN)
    assert len(lines) <= 2, "Hook must fit on two short lines"
    y = 700
    lh = int(headline_px * 1.12)
    # underline first, so the letters sit on top of it
    for i, ln in enumerate(lines):
        if key and key in ln:
            pre = ln[: ln.index(key)]
            x0 = MARGIN + d.textlength(pre, font=hf)
            x1 = x0 + d.textlength(key, font=hf)
            base = y + i * lh + hf.getmetrics()[0]
            d.rectangle([x0, base + 4, x1 + 6, base + 12], fill=LIME)
    for i, ln in enumerate(lines):
        d.text((MARGIN, y + i * lh), ln, font=hf, fill=WHITE)
    sy = y + len(lines) * lh + 28
    for i, ln in enumerate(wrap(d, sub, sf, W - 2 * MARGIN)):
        d.text((MARGIN, sy + i * 49), ln, font=sf, fill=WHITE)
    if callout:
        bf = font("Poppins_700Bold.ttf", 31)
        top, hgt = 1010, 160
        d.rounded_rectangle([MARGIN, top, W - MARGIN, top + hgt], radius=34, fill=LIME)
        cl = wrap(d, callout, bf, 430 if button else W - 2 * MARGIN - 90)
        ty = top + (hgt - len(cl) * 42) // 2
        for i, ln in enumerate(cl): d.text((MARGIN + 44, ty + i * 42), ln, font=bf, fill=(31, 28, 29))
        if button:
            bw = d.textlength(button, font=bf) + 110
            bx1 = W - MARGIN - 34; bx0 = bx1 - bw
            d.rounded_rectangle([bx0, top + 40, bx1, top + hgt - 40], radius=40, fill=(0, 79, 35))
            d.text((bx0 + 30, top + 80 - 20), button, font=bf, fill=WHITE)
            ax = bx1 - 62; ay = top + 80
            d.line([ax, ay, ax + 30, ay], fill=LIME, width=4); d.line([ax + 20, ay - 9, ax + 30, ay, ], fill=LIME, width=4); d.line([ax + 20, ay + 9, ax + 30, ay], fill=LIME, width=4)
    lg = Image.open(logo).convert("RGBA")
    canvas.paste(lg, (W - MARGIN - lg.width + 8, H - 57 - lg.height), lg)
    canvas.save(out, quality=95)

if __name__ == "__main__":
    a = argparse.ArgumentParser()
    for k in ("photo", "hook", "key", "sub", "logo", "out"): a.add_argument("--" + k, required=True)
    a.add_argument("--callout"); a.add_argument("--button")
    p = a.parse_args(); render(p.photo, p.hook, p.key, p.sub, p.logo, p.out, callout=p.callout, button=p.button)
