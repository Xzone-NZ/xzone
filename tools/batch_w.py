import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_post as R
HERE = os.path.dirname(os.path.abspath(__file__))
OLD = sys.argv[1]; OUT = sys.argv[2]
P = {
 "w10-wed": ("The best recovery tool is free, and it’s your bed", "your bed", None, [("Same wake time","weekends too"),("Cool, dark, quiet","phone out of reach"),("Wind down","screens off, a slow massage")]),
 "w11-fri": ("The first 48 hours decide your long weekend", "48 hours", None, [("Rolled ankle","rest, ice, compress, raise"),("Bumps and bruises","cold first, then massage"),("Stiff after the drive","stop every two hours")]),
 "w12-fri": ("What smart sideline parents keep in the car", "parents", None, [("In the bag","water, ice pack, bandage"),("On the knock","cold first, then massage"),("Head knocks","off the field, see a doctor")]),
 "w13-wed": ("Your most-asked questions, answered", "questions", None, [("Which one?","Relief, Joints or Sports"),("How much?","1 to 5 ml, up to five times a day"),("Kids?","Relief from five, the others from seven")]),
 "w2-fri": ("Which jar is yours? Start here", "jar", None, [("Relief","bruises and bumps, your first-aid go-to"),("Joints","stiffness and long-term joint pain"),("Sports","our strongest, for warm-up and recovery")]),
 "w4-fri": ("What every bach cupboard should hold", "bach", None, [("First-aid tin","plasters, bandage, tweezers"),("Sun and bugs","sunscreen and repellent"),("Bumps and aches","a Relief Rub and a roll-on")]),
 "w5-mon": ("The herb your grandmother already knew", "grandmother", "Koromiko, in our Relief range.", None),
 "w5-sat": ("Is your Boxing Day ache actually thirst?", "thirst", None, [("Water first","a big glass, then sip all day"),("Then move","a gentle walk or a swim"),("Rub before bed","then let sleep do the work")]),
 "w6-fri": ("The 2027 recovery routine we actually stick to", "actually", None, [("Two easy days","walk, swim or stretch"),("Seven hours plus","when muscles repair"),("Massage sore spots","a few minutes, a little rub")]),
 "w7-wed": ("We sent our rubs to a lab. Here is what happened", "what happened", None, [("Tested","our three rubs, on cells linked to inflammation"),("Found","Sports 55%, Joints 49%, Relief 43% fewer"),("Means","a promising in-vitro result on cells")]),
 "w8-wed": ("Heat or ice? The honest answer", "honest answer", None, [("Ice","new knocks and swelling, first 48 hours"),("Heat","tight muscles and old aches"),("Joints","usually warm, unless hot and swollen")]),
 "w9-fri": ("The three injuries every worksite hands out", "worksite", None, [("Lower back","warm up, keep loads close"),("Tennis elbow","ease the grip, massage the forearm"),("Shoulders","break up overhead work")]),
}
for pid, (hook, key, sub, bl) in P.items():
    src = Image.open(os.path.join(OLD, pid + ".jpg")).convert("RGB").crop((0, 0, 1080, 600))
    tmp = f"/tmp/ph-{pid}.jpg"; src.save(tmp, quality=95)
    os.makedirs(os.path.join(OUT, pid), exist_ok=True)
    px = 70
    while True:
        try:
            R.render(tmp, hook, key, sub, os.path.join(HERE, "logo-white.png"), os.path.join(OUT, pid, "post.jpg"), headline_px=px, bullets=bl); break
        except AssertionError:
            px -= 4
    print(pid, "headline px", px)
