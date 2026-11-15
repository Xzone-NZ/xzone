"""Export Instagram slides at 1080 x 1350. Run after build.py: python3 ambassadors/export_instagram.py"""
import glob, os, subprocess
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__))
subprocess.run(["node", os.path.join(here, "export_instagram.js")], check=True)
for f in sorted(glob.glob(os.path.join(here, "instagram", "*.png"))):
    im = Image.open(f).convert("RGB").resize((1080, 1350), Image.LANCZOS)
    im.save(f, optimize=True)
    print(os.path.relpath(f, here), im.size)
