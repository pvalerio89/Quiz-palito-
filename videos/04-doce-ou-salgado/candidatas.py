"""Mostra até 8 fotos candidatas do Commons por comida, para escolher olhando.

Uso: py -3 candidatas.py busca.json      -> gera candidatas.jpg + candidatas.json
     py -3 candidatas.py --pegar escolhas_fotos.json   ({"Nome": índice}) baixa as escolhidas
busca.json = {"Nome": "termo de busca", ...}
"""
import io, json, os, sys, time, urllib.parse, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageOps
from fotos import UA, OK_LIC, RUIM, clean, fetch, slug

HERE = os.path.dirname(os.path.abspath(__file__))
N = 8


def candidatas(q):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"{q} filetype:bitmap",
        "gsrnamespace": 6, "gsrlimit": 40, "prop": "imageinfo", "iiprop": "url|size|extmetadata",
        "iiurlwidth": 1000})
    d = json.load(fetch(urllib.request.Request(url, headers={"User-Agent": UA}), 30))
    out = []
    for p in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99)):
        ii = p["imageinfo"][0]
        m = ii.get("extmetadata", {})
        lic = clean(m.get("LicenseShortName", {}).get("value"))
        w, h = ii["width"], ii["height"]
        t = p["title"]
        if not lic.startswith(OK_LIC) or "NC" in lic or "ND" in lic:
            continue
        if any(k in t.lower() for k in RUIM) or t.lower().endswith((".png", ".gif", ".svg", ".tif", ".tiff")):
            continue
        if w < 800 or not (0.7 <= w / h <= 2.0):
            continue
        out.append({"url": ii.get("thumburl") or ii["url"], "title": t.replace("File:", ""), "lic": lic,
                    "artist": clean(m.get("Artist", {}).get("value"))[:80] or "autor desconhecido"})
        if len(out) == N:
            break
    return out


def main():
    f = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
    if sys.argv[1] == "--pegar":
        cand = json.load(open(os.path.join(HERE, "candidatas.json"), encoding="utf-8"))
        cred = json.load(open(os.path.join(HERE, "creditos.json"), encoding="utf-8"))
        for nome, i in json.load(open(sys.argv[2], encoding="utf-8")).items():
            r = cand[nome][i]
            data = fetch(urllib.request.Request(r["url"], headers={"User-Agent": UA}), 60).read()
            open(os.path.join(HERE, "fotos", slug(nome) + ".jpg"), "wb").write(data)
            cred[nome] = {k: r[k] for k in ("title", "lic", "artist")}
            print("ok", nome, "-", r["title"][:60], flush=True)
        json.dump(cred, open(os.path.join(HERE, "creditos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return
    busca = json.load(open(sys.argv[1], encoding="utf-8"))
    cand, S = {}, 180
    img = Image.new("RGB", (220 + N * S, len(busca) * (S + 6)), (25, 25, 25))
    d = ImageDraw.Draw(img)
    for r, (nome, q) in enumerate(busca.items()):
        cand[nome] = candidatas(q)
        y = r * (S + 6)
        d.text((6, y + 70), nome, font=f, fill=(255, 230, 0))
        for i, c in enumerate(cand[nome]):
            try:
                th = c["url"].replace("/1000px-", "/330px-")
                time.sleep(0.4)
                im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(th, headers={"User-Agent": UA}), timeout=20).read()))
                img.paste(ImageOps.fit(im.convert("RGB"), (S - 6, S - 6)), (220 + i * S, y))
            except Exception as ex:
                print('  miniatura falhou', i, ex, flush=True)
            d.text((224 + i * S, y + 2), str(i), font=f, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
        print(nome, len(cand[nome]), flush=True)
    json.dump(cand, open(os.path.join(HERE, "candidatas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    img.save(os.path.join(HERE, "candidatas.jpg"), quality=80)


if __name__ == "__main__":
    main()
