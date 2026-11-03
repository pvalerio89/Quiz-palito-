"""Baixa fotos do Wikimedia Commons para cada país do perguntas.json.

Escolhe a primeira foto horizontal, grande e com licença livre.
Grava assets/fotoN.jpg e atualiza creditos-fotos.txt.
Uso: py -3 fotos.py [n1 n2 ...]   (sem números = todas que faltam)
"""
import json, os, re, sys, urllib.error, urllib.parse, urllib.request

UA = "QuizPalitoBuilder/1.0 (personal YouTube quiz project)"
OK_LIC = ("CC0", "Public domain", "CC BY", "CC BY-SA", "PD")
HERE = os.path.dirname(os.path.abspath(__file__))


def fetch(req, timeout):
    import time
    for i in range(6):
        try:
            time.sleep(2)
            return urllib.request.urlopen(req, timeout=timeout)
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(15 * (i + 1))
    raise RuntimeError("Wikimedia continua com limite (429)")


def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return json.load(fetch(req, 30))


def clean(s):
    return re.sub(r"\s+", " ", re.sub("<[^>]+>", "", s or "")).strip()


def search(q, skip=()):
    d = api({"action": "query", "format": "json", "generator": "search",
             "gsrsearch": f"{q} filetype:bitmap", "gsrnamespace": 6, "gsrlimit": 20,
             "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1920})
    pages = sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    for p in pages:
        ii = p["imageinfo"][0]
        m = ii.get("extmetadata", {})
        lic = clean(m.get("LicenseShortName", {}).get("value"))
        w, h = ii["width"], ii["height"]
        if not lic.startswith(OK_LIC) or "NC" in lic or "ND" in lic:
            continue
        if any(k.lower() in p['title'].lower() for k in skip):
            continue
        if w < 1600 or not (1.3 <= w / h <= 2.2):
            continue
        artist = clean(m.get("Artist", {}).get("value"))[:80] or "autor desconhecido"
        return {"url": ii.get("thumburl") or ii["url"], "title": p["title"].replace("File:", ""),
                "lic": lic, "artist": artist}
    return None


def main():
    qs = json.load(open(os.path.join(HERE, "perguntas.json"), encoding="utf-8"))
    want = {int(a) for a in sys.argv[1:]}
    cred_path = os.path.join(HERE, "creditos.json")
    cred = json.load(open(cred_path, encoding="utf-8")) if os.path.exists(cred_path) else {}
    for q in qs:
        if "foto" not in q:
            continue
        n = q["n"]
        out = os.path.join(HERE, "assets", f"foto{n}.jpg")
        if want and n not in want:
            continue
        if not want and os.path.exists(out):
            continue
        r = search(q["foto"], q.get("skip", ()))
        if not r:
            print(f"{n:2d} {q['answer']}: NADA ENCONTRADO para '{q['foto']}'")
            continue
        req = urllib.request.Request(r["url"], headers={"User-Agent": UA})
        open(out, "wb").write(fetch(req, 60).read())
        cred[str(n)] = {"pais": q["answer"], **{k: r[k] for k in ("title", "lic", "artist")}}
        print(f"{n:2d} {q['answer']}: {r['lic']} | {r['artist'][:40]} | {r['title'][:60]}", flush=True)
        json.dump(cred, open(cred_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(cred, open(cred_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # texto pra descrição do YouTube
    lines = ["Créditos das fotos (cole na descrição do vídeo do YouTube)", ""]
    for k in sorted(cred, key=int):
        c = cred[k]
        lines.append(f"{c['pais'].title()}: \"{c['title'].rsplit('.', 1)[0]}\" de {c['artist']}, {c['lic']}, via Wikimedia Commons")
    open(os.path.join(HERE, "creditos-fotos.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
