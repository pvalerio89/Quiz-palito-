"""Fotos reais de licença livre (Wikimedia Commons) para os quizzes.

A nuvem do Claude não abre commons.wikimedia.org nem a API, mas abre as páginas da Wikipédia em inglês
(en.wikipedia.org/wiki/...) e os arquivos em upload.wikimedia.org (só miniaturas 500/960/1280 px).

1) Buscar candidatas (fotos do artigo da Wikipédia + licença e autor de cada uma):
     py -3 automacao/fotos_wiki.py buscar lista.tsv saida/         (lista: nome<TAB>tipo<TAB>Artigo_em_ingles)
   Grava saida/cand.json e saida/folha_*.jpg (fundo branco = licença boa: domínio público, CC0 ou CC BY;
   rosa = CC BY-SA/GFDL, usar só se não houver outra; nunca foto só GFDL, sem CC).
2) Escolher: escolhas.json  {"Banana": {"file": "Banana-Single.jpg", "crop": [0.5, 0.5, 1.0]}, ...}
   crop = centro x, centro y (0..1) e lado do quadrado (fração do lado menor). Sem crop = centro.
   crop = "fit" põe a foto inteira num quadrado branco (bom para foto comprida com fundo branco).
3) Baixar as escolhidas já recortadas em quadrado + creditos.json (autor e licença para a tela final):
     py -3 automacao/fotos_wiki.py baixar escolhas.json videos/NN-tema/   (grava fotos/<slug>.jpg)
   (folhas de novo a partir de um cand.json: py -3 automacao/fotos_wiki.py folhas cand.json saida/)
Vídeos curtos (para trocar a foto por um clipe em algumas perguntas):
     py -3 automacao/fotos_wiki.py clipes clipes.json videos/NN-tema/   (grava clipes/<slug>.mp4, quadrado, sem som)
   clipes.json  {"Panda": {"file": "Pandas_playing_640x480.ogv", "inicio": 5, "dur": 10, "crop": [0.5, 0.5, 1.0]}}
   Ache os clipes nos artigos da Wikipédia (links .webm/.ogv de commons/transcoded). Créditos vão no mesmo creditos.json.
Escudos/logos (imagem da caixa de informações do artigo, ex.: escudo do time):
     py -3 automacao/fotos_wiki.py escudos lista.tsv videos/NN-tema/   (lista: nome<TAB>Artigo_em_ingles)
   Grava escudos/<slug>.png (fundo transparente, 512 px), creditos.json e escudos/folha.jpg para conferir.
Na nuvem do Claude o upload.wikimedia.org dá 429 (IP compartilhado): rode pelo workflow "Fotos Wikimedia"
(escreva os argumentos em automacao/fotos-pedido.txt e dê push numa branch claude/...; ele grava o resultado na branch).
Créditos: só na tela final do vídeo (o Patrick não quer em descrição nem comentário).
"""
import hashlib, html, json, os, re, subprocess, sys, threading, time, unicodedata, urllib.parse
from concurrent.futures import ThreadPoolExecutor

UA = "QuizPalitoBot/1.0 (https://github.com/pvalerio89/quiz-palito-; educational quiz video)"
LIC_BOA = re.compile(r"public domain|pdm|cc0|^cc by \d|^cc by$", re.I)
_lk = threading.Lock()


def get(url, out=None):
    for k in range(3):
        cmd = ["curl", "-s", "-L", "-m", "60", "-A", UA, "-w", "%{http_code}", url] + (["-o", out] if out else [])
        txt = subprocess.run(cmd, capture_output=True).stdout.decode("utf-8", "replace")
        code = txt[-3:]
        if code == "200":
            return True if out else txt[:-3]
        if code in ("404", "400"):
            return None
        time.sleep(3 * (k + 1))
    return None


def url_arquivo(fn, px=None):
    n = fn.replace(" ", "_")
    h = hashlib.md5(n.encode()).hexdigest()
    q = urllib.parse.quote(n)
    if px:
        return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/{px}px-{q}"
    return f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{q}"


def licenca(fn):
    p = get(f"https://en.wikipedia.org/wiki/File:{urllib.parse.quote(fn)}")
    if not p:
        return None
    lic = [l.strip() for l in re.findall(r'licensetpl_short"[^>]*>([^<]*)<', p)]
    m = re.search(r'id="fileinfotpl_aut"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>', p, re.S)
    autor = re.sub(r"<style.*?</style>", "", m.group(1), flags=re.S) if m else ""  # Creator: traz CSS junto
    autor = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", autor)).strip()[:80]
    return {"file": fn, "lic": lic, "autor": autor}


def buscar(lista, saida, n_cand=10):
    os.makedirs(saida, exist_ok=True)
    arq = os.path.join(saida, "cand.json")
    res = json.load(open(arq, encoding="utf-8")) if os.path.exists(arq) else {}

    def um(linha):
        nome, tipo, art = linha.split("\t")[:3]
        if nome in res:
            return
        html = get(f"https://en.wikipedia.org/wiki/{urllib.parse.quote(art)}")
        if not html:
            print("artigo não achado:", nome, art, flush=True)
            return
        files = []
        for m in re.finditer(r'href="(?:https://en.wikipedia.org)?/wiki/File:([^"#?]+)"', html):
            f = urllib.parse.unquote(m.group(1))
            if f not in files and re.search(r"\.(jpe?g|png)$", f, re.I) and \
                    not re.search(r"\bmap|\brange|production|logo|flag|diagram|chart|symbol", f, re.I):
                files.append(f)
        cs = [c for c in (licenca(f) for f in files[:n_cand]) if c]
        with _lk:
            res[nome] = {"tipo": tipo, "art": art, "cand": cs}
            json.dump(res, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(nome, len(cs), flush=True)

    linhas = [l for l in open(lista, encoding="utf-8").read().splitlines() if l.strip() and not l.startswith("#")]
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(um, linhas))
    folhas(res, saida)


def folhas(res, saida, por_folha=8):
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(os.path.join(saida, "thumbs"), exist_ok=True)
    try:
        f = ImageFont.truetype("DejaVuSans-Bold.ttf", 16)
        fg = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
    except OSError:
        f = fg = ImageFont.load_default()
    TS, cols = 230, 11
    nomes = list(res)
    for a in range(0, len(nomes), por_folha):
        sheet = Image.new("RGB", (cols * (TS + 4), por_folha * (TS + 4)), (40, 40, 40))
        d = ImageDraw.Draw(sheet)
        for r, nome in enumerate(nomes[a:a + por_folha]):
            y = r * (TS + 4)
            d.text((6, y + 100), nome, font=fg, fill="yellow")
            k = 0
            for i, c in enumerate(res[nome]["cand"]):
                out = os.path.join(saida, "thumbs", hashlib.md5(c["file"].encode()).hexdigest() + ".jpg")
                if not (os.path.exists(out) and os.path.getsize(out) > 2000):
                    time.sleep(0.3)
                    if not get(url_arquivo(c["file"], 500), out):
                        continue
                try:
                    im = Image.open(out).convert("RGB")
                except Exception:
                    continue
                im.thumbnail((TS, TS - 30))
                ok = any(LIC_BOA.search(l) for l in c["lic"])
                t = Image.new("RGB", (TS, TS), "white" if ok else (255, 200, 200))
                t.paste(im, ((TS - im.width) // 2, 0))
                ImageDraw.Draw(t).text((4, TS - 26), f"{i} {(c['lic'] or ['?'])[-1][:16]}", font=f, fill="black")
                k += 1
                if k < cols:
                    sheet.paste(t, (k * (TS + 4), y))
        sheet.save(os.path.join(saida, f"folha_{a // por_folha + 1:02d}.jpg"), quality=80)
    print("folhas em", saida)


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def baixar(escolhas, pasta, lado=720):
    from PIL import Image
    esc = json.load(open(escolhas, encoding="utf-8"))
    os.makedirs(os.path.join(pasta, "fotos"), exist_ok=True)
    arq = os.path.join(pasta, "creditos.json")
    cred = json.load(open(arq, encoding="utf-8")) if os.path.exists(arq) else {}
    tmp = os.path.join(pasta, "fotos", "_tmp.jpg")
    for nome, e in esc.items():
        dst = os.path.join(pasta, "fotos", slug(nome) + ".jpg")
        c = cred.get(nome, {})
        if os.path.exists(dst) and c.get("file") == e["file"] and c.get("crop") == e.get("crop"):
            continue
        if not any(get(url_arquivo(e["file"], px), tmp) for px in (1280, 960, 500)):
            print("falhou", nome, e["file"])
            continue
        im = Image.open(tmp).convert("RGB")
        if e.get("crop") == "fit":  # foto inteira num quadrado branco (bom para foto de fundo branco)
            s = max(im.size)
            q = Image.new("RGB", (s, s), (255, 255, 255))
            q.paste(im, ((s - im.width) // 2, (s - im.height) // 2))
            im = q
        cx, cy, fr = (0.5, 0.5, 1.0) if e.get("crop") in (None, "fit") else e["crop"]
        s = min(im.size) * fr
        x0 = min(max(im.width * cx - s / 2, 0), im.width - s)
        y0 = min(max(im.height * cy - s / 2, 0), im.height - s)
        im.crop((int(x0), int(y0), int(x0 + s), int(y0 + s))).resize((lado, lado), Image.LANCZOS).save(dst, quality=88)
        info = e.get("lic") and e or (licenca(e["file"]) or {})
        lic = [l for l in info.get("lic", []) if not l.upper().startswith("GFDL")] or info.get("lic", ["?"])
        autor = re.sub(r"\s+", " ", html.unescape(info.get("autor") or "")).strip()
        autor = re.sub(r"(?i)^self,?\s*|\s*\(?talk\)?$|[¡!]?שיחת!?\u200e?", "", autor).strip()
        autor = re.sub(r"(?i)^no machine-readable author provided\.\s*|~\w+$|^\S+\.(jpe?g|png):\s*|^English:\s*", "", autor).strip()
        autor = re.split(r"\s{2,}|Alternative names", autor)[0].strip() or "autor no Wikimedia Commons"
        cred[nome] = {"file": e["file"], "crop": e.get("crop"), "arquivo": os.path.basename(dst),
                      "autor": autor[:60], "lic": lic[0]}
        print("ok", nome, cred[nome]["lic"], flush=True)
        json.dump(cred, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if os.path.exists(tmp):
        os.remove(tmp)


def clipes(escolhas, pasta, lado=600):
    """Baixa vídeos do Commons (versão 480p/720p já convertida), corta o trecho e grava mp4 quadrado sem som."""
    esc = json.load(open(escolhas, encoding="utf-8"))
    os.makedirs(os.path.join(pasta, "clipes"), exist_ok=True)
    arq = os.path.join(pasta, "creditos.json")
    cred = json.load(open(arq, encoding="utf-8")) if os.path.exists(arq) else {}
    tmp = os.path.join(pasta, "clipes", "_tmp.webm")
    for nome, e in esc.items():
        dst = os.path.join(pasta, "clipes", slug(nome) + ".mp4")
        n = e["file"].replace(" ", "_")
        h = hashlib.md5(n.encode()).hexdigest()
        q = urllib.parse.quote(n)
        urls = [f"https://upload.wikimedia.org/wikipedia/commons/transcoded/{h[0]}/{h[:2]}/{q}/{q}.{r}.vp9.webm"
                for r in ("720p", "480p", "360p")] + [url_arquivo(e["file"])]
        if not any(get(u, tmp) for u in urls):
            print("falhou", nome, e["file"])
            continue
        cx, cy, fr = e.get("crop") or (0.5, 0.5, 1.0)
        lado_f = f"min(iw\\,ih)*{fr}"
        vf = (f"crop={lado_f}:{lado_f}:min(max(iw*{cx}-{lado_f}/2\\,0)\\,iw-{lado_f}):"
              f"min(max(ih*{cy}-{lado_f}/2\\,0)\\,ih-{lado_f}),scale={lado}:{lado},fps=30")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(e.get("inicio", 0)), "-i", tmp,
                        "-t", str(e.get("dur", 10)), "-vf", vf, "-an", "-c:v", "libx264", "-crf", "20",
                        "-pix_fmt", "yuv420p", dst], check=True)
        info = licenca(e["file"]) or {}
        lic = [l for l in info.get("lic", []) if not l.upper().startswith("GFDL")] or info.get("lic", ["?"])
        autor = re.sub(r"\s+", " ", html.unescape(info.get("autor") or "")).strip()
        autor = re.split(r"\s{2,}|\(", autor)[0].strip() or "autor no Wikimedia Commons"
        cred[nome] = {"file": e["file"], "arquivo": os.path.basename(dst), "autor": autor[:60], "lic": lic[0],
                      "video": True}
        print("ok", nome, cred[nome]["lic"], flush=True)
        json.dump(cred, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if os.path.exists(tmp):
        os.remove(tmp)


def escudos(lista, pasta, lado=512):
    """Imagem principal da caixa de informações do artigo (escudo do time, logo...) em PNG transparente."""
    from PIL import Image, ImageDraw
    os.makedirs(os.path.join(pasta, "escudos"), exist_ok=True)
    arq = os.path.join(pasta, "creditos.json")
    cred = json.load(open(arq, encoding="utf-8")) if os.path.exists(arq) else {}
    tmp = os.path.join(pasta, "escudos", "_tmp")
    linhas = [l for l in open(lista, encoding="utf-8").read().splitlines() if l.strip() and not l.startswith("#")]
    for linha in linhas:
        nome, art = linha.split("\t")[:2]
        dst = os.path.join(pasta, "escudos", slug(nome) + ".png")
        if os.path.exists(dst) and nome in cred:
            continue
        time.sleep(0.5)
        pg = get(f"https://en.wikipedia.org/wiki/{urllib.parse.quote(art)}")
        m = pg and re.search(r'<table class="infobox.*?</table>', pg, re.S)
        im_m = m and re.search(r'href="/wiki/File:([^"#?]+)"[^>]*>\s*<img[^>]*?src="([^"]+)"', m.group(0), re.S)
        if not im_m:
            print("sem escudo:", nome, art, flush=True)
            continue
        fn, src = urllib.parse.unquote(im_m.group(1)), html.unescape(im_m.group(2))
        src = "https:" + src if src.startswith("//") else src
        urls = [re.sub(r"/\d+px-", f"/{px}px-", src) for px in (500, 330)] if "/thumb/" in src else []
        if not any(get(u, tmp) for u in urls + [src]):
            print("falhou download:", nome, src, flush=True)
            continue
        im = Image.open(tmp).convert("RGBA")
        bb = im.getchannel("A").getbbox()
        if bb:
            im = im.crop(bb)
        r = (lado - 16) / max(im.size)
        im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
        q = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
        q.alpha_composite(im, ((lado - im.width) // 2, (lado - im.height) // 2))
        q.save(dst)
        info = licenca(fn) or {}
        cred[nome] = {"file": fn, "arquivo": os.path.basename(dst), "autor": (info.get("autor") or "")[:60],
                      "lic": (info.get("lic") or ["logo do clube"])[0], "artigo": art}
        print("ok", nome, fn, cred[nome]["lic"], flush=True)
        json.dump(cred, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if os.path.exists(tmp):
        os.remove(tmp)
    # folha para conferir
    nomes = [l.split("\t")[0] for l in linhas]
    th, cols = 150, 10
    fs = Image.new("RGB", (cols * th, -(-len(nomes) // cols) * (th + 20)), (200, 200, 210))
    d = ImageDraw.Draw(fs)
    for i, n in enumerate(nomes):
        x, y = (i % cols) * th, (i // cols) * (th + 20)
        p = os.path.join(pasta, "escudos", slug(n) + ".png")
        if os.path.exists(p):
            e = Image.open(p)
            e.thumbnail((th - 10, th - 10))
            fs.paste(e, (x + 5, y + 5), e)
        d.text((x + 4, y + th + 2), n[:22], fill="black")
    fs.save(os.path.join(pasta, "escudos", "folha.jpg"), quality=85)


if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[1] not in ("buscar", "baixar", "folhas", "clipes", "escudos"):
        sys.exit(__doc__)
    if sys.argv[1] == "folhas":  # refaz só as folhas a partir de um cand.json
        folhas(json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3])
    else:
        {"buscar": buscar, "baixar": baixar, "clipes": clipes, "escudos": escudos}[sys.argv[1]](sys.argv[2], sys.argv[3])
