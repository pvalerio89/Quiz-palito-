import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
sys.path.insert(0, ".")
from fotos import slug
esc = json.load(open("escolhas.json", encoding="utf-8"))
nomes = []
for e in esc:
    for k in ("doce", "salgado"):
        if e[k] not in nomes: nomes.append(e[k])
f = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
C, S = 10, 200
rows = (len(nomes) + C - 1) // C
img = Image.new("RGB", (C * S, rows * (S + 26)), (25, 25, 25))
d = ImageDraw.Draw(img)
for i, n in enumerate(nomes):
    x, y = (i % C) * S, (i // C) * (S + 26)
    p = os.path.join("fotos", slug(n) + ".jpg")
    if os.path.exists(p):
        img.paste(ImageOps.fit(Image.open(p).convert("RGB"), (S - 6, S - 6)), (x + 3, y + 3))
    else:
        d.rectangle([x + 3, y + 3, x + S - 3, y + S - 3], outline=(255, 0, 0), width=3)
    d.text((x + 4, y + S), f"{i+1}. {n}", font=f, fill=(255, 230, 0))
img.save("prancha-fotos.jpg", quality=80)
