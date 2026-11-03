"""Baixa uma foto livre do Wikimedia Commons para cada comida do escolhas.json.

Grava fotos/<slug>.jpg e creditos.json (título, autor, licença).
Uso: py -3 fotos.py                 (baixa as que faltam)
     py -3 fotos.py "Coxinha" ...   (refaz essas, pulando a foto atual)
"""
import json, os, re, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request

UA = "QuizPalitoBuilder/1.0 (personal YouTube quiz project)"
OK_LIC = ("CC0", "Public domain", "CC BY", "CC BY-SA", "PD")
HERE = os.path.dirname(os.path.abspath(__file__))
RUIM = ("logo", "map", "diagram", "sign", "poster", "stamp", "signature", "autograph")


def slug(nome):
    s = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def fetch(req, timeout):
    for i in range(6):
        try:
            time.sleep(1.5)
            return urllib.request.urlopen(req, timeout=timeout)
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(15 * (i + 1))
    raise RuntimeError("Wikimedia continua com limite (429)")


def clean(s):
    return re.sub(r"\s+", " ", re.sub("<[^>]+>", "", s or "")).strip()


def search(q, pular=()):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"{q} filetype:bitmap",
        "gsrnamespace": 6, "gsrlimit": 30, "prop": "imageinfo", "iiprop": "url|size|extmetadata",
        "iiurlwidth": 1000})
    d = json.load(fetch(urllib.request.Request(url, headers={"User-Agent": UA}), 30))
    pages = sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    for p in pages:
        ii = p["imageinfo"][0]
        m = ii.get("extmetadata", {})
        lic = clean(m.get("LicenseShortName", {}).get("value"))
        w, h = ii["width"], ii["height"]
        t = p["title"]
        if not lic.startswith(OK_LIC) or "NC" in lic or "ND" in lic:
            continue
        if t in pular or any(k in t.lower() for k in RUIM) or t.lower().endswith((".png", ".gif", ".svg", ".tif", ".tiff")):
            continue
        if w < 900 or not (0.75 <= w / h <= 1.9):
            continue
        artist = clean(m.get("Artist", {}).get("value"))[:80] or "autor desconhecido"
        return {"url": ii.get("thumburl") or ii["url"], "title": t.replace("File:", ""), "lic": lic, "artist": artist}
    return None


def main():
    esc = json.load(open(os.path.join(HERE, "escolhas.json"), encoding="utf-8"))
    comidas = {}
    for e in esc:
        comidas.setdefault(e["doce"], e["busca_doce"])
        comidas.setdefault(e["salgado"], e["busca_salgado"])
    cred_path = os.path.join(HERE, "creditos.json")
    cred = json.load(open(cred_path, encoding="utf-8")) if os.path.exists(cred_path) else {}
    refazer = set(sys.argv[1:])
    os.makedirs(os.path.join(HERE, "fotos"), exist_ok=True)
    for nome, q in comidas.items():
        out = os.path.join(HERE, "fotos", slug(nome) + ".jpg")
        if os.path.exists(out) and nome not in refazer:
            continue
        pular = set(cred.get(nome, {}).get("pulados", []))
        if nome in refazer and nome in cred:
            pular.add("File:" + cred[nome]["title"])
        r = search(q, pular)
        if not r:
            print(f"{nome}: NADA para '{q}'", flush=True)
            continue
        open(out, "wb").write(fetch(urllib.request.Request(r["url"], headers={"User-Agent": UA}), 60).read())
        cred[nome] = {**{k: r[k] for k in ("title", "lic", "artist")}, "pulados": sorted(pular)}
        print(f"{nome}: {r['lic']} | {r['title'][:70]}", flush=True)
        json.dump(cred, open(cred_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
