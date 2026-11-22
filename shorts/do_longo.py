"""Base dos Shorts TIRADOS DO PRÓPRIO VÍDEO LONGO (Patrick, 2026-11-22: "tem que fazer o Short do vídeo longo").

Cada Short `shorts/<tema>-N/build_short.py` só escolhe 4 ou 5 perguntas do longo (itens.json + fotos do longo)
e chama `rodar(CFG, PERG)`. O visual segue o molde de `shorts/brasil-2` (sem abertura, 1ª imagem já é a
pergunta, faixa da chamada, placar de bolinhas, +1 SE ACERTOU, transição SPLASH, tela final "quiz completo no
canal"), mas o CARTÃO muda conforme o longo, para os Shorts não saírem todos iguais:
  - "foto": título + destaque + foto (foto da resposta pode ser outra: ex. bandeira -> animal);
  - "texto": título + destaque + texto grande (conta, pista, frase), sem foto;
  - opções com bandeira (opcional) e nome revelado na resposta (ex.: jogador).

PERG = lista de dicts:
  titulo, destaque (opcional), foto (caminho) ou texto (lista de linhas), foto_resp (opcional),
  contem (True = foto inteira, ex. bandeira; False = recorta quadrado), opcoes [3], certa (0-2),
  bandeiras [3 caminhos ou None] (opcional), revela (texto na resposta, opcional), fala, resp, cores ((topo), (base)).
CFG = dict: nome (arquivo short-<nome>.mp4), here (pasta do Short), rotulo, cor_rotulo, chamada, gancho, final,
  musica, creditos (lista de "nome: autor (licença)"), count (s), final_titulo (2 linhas, opcional).
Uso no Short: py -3 build_short.py  |  py -3 build_short.py --previa
"""
import asyncio, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE0 = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE0)
import short_base as s
from short_base import b, QP
sys.path.insert(0, os.path.join(QP, "videos", "modelo-opcoes"))
import engaja as eg

FPS = s.FPS
CARD = (90, 330, 990, 950)          # cartão da pergunta
OPT_Y = (1065, 1210, 1355)          # centro das opções
OPT_W, OPT_H = 820, 120
BAR = (110, 1468, 970, 1514)
CCX, CCY = (CARD[0] + CARD[2]) // 2, (CARD[1] + CARD[3]) // 2

CFG, PERG = {}, []
_cache = {}


def A(n):
    return os.path.join(CFG["here"], "assets", n)


def textos():
    t = {"final": CFG["final"]}
    for k, p in enumerate(PERG, 1):
        t[f"q{k}"] = p["fala"]
        t[f"a{k}"] = p["resp"]
    t["q1"] = f"{CFG['gancho']} {PERG[0]['fala']}"   # chamada falada POR CIMA da 1ª pergunta (sem abertura)
    return t


def vozes():
    import edge_tts
    if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
        import ssl, edge_tts.communicate as _c
        _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
    os.makedirs(os.path.join(CFG["here"], "assets"), exist_ok=True)
    for k, txt in textos().items():
        p = A(f"{k}.mp3")
        if os.path.exists(p) and os.path.getsize(p) < 1000:   # Edge TTS às vezes grava vazio
            os.remove(p)
        if not os.path.exists(p):
            asyncio.run(edge_tts.Communicate(txt, "pt-BR-AntonioNeural", rate="+20%", pitch="+2Hz").save(p))
            print("voz", k, "-", txt, flush=True)


def foto(caminho, w, h, contem=False):
    """Foto arredondada: recorta para caber em w x h (ou inteira, centralizada, se contem=True)."""
    key = ("foto", caminho, w, h, contem)
    if key not in _cache:
        im = Image.open(caminho).convert("RGBA")
        if contem:
            r = min(w / im.width, h / im.height)
            im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
        else:
            im = ImageOps.fit(im, (w, h), Image.LANCZOS)
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], 28, fill=255)
        im.putalpha(m)
        _cache[key] = im
    return _cache[key]


def _ajusta(d, txt, fonte, tam, larg, minimo=36):
    f = b.font(fonte, tam)
    while d.textlength(txt, font=f) > larg and f.size > minimo:
        f = b.font(fonte, f.size - 4)
    return f


def cartao_sprite(k, p, resposta=False):
    """Cartão branco com número, título, destaque e foto OU texto grande."""
    key = ("cartao", k, resposta)
    if key not in _cache:
        x0, y0, x1, y1 = CARD
        w, h = x1 - x0, y1 - y0
        cv = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
        b.shadowed_round_rect(cv, (30, 30, 30 + w, 30 + h), 44, b.WHITE)
        d = ImageDraw.Draw(cv)
        d.rounded_rectangle([30, 30, 30 + w, 30 + h], 44, outline=b.NAVY, width=7)
        cx = 30 + w / 2
        titulo = f"{k}. {p['titulo']}"
        d.text((cx, 105), titulo, font=_ajusta(d, titulo, b.F_BOLD, 56, w - 80), fill=b.NAVY, anchor="mm")
        topo_img = 160
        dest, cor = p.get("destaque"), (220, 40, 60)
        if p.get("revela"):   # nome escondido na pergunta ("???") e revelado em verde na resposta (ex.: o jogador)
            dest, cor = (p["revela"], (30, 150, 60)) if resposta else ("? ? ?", (220, 40, 60))
        if dest:
            d.text((cx, 195), dest, font=_ajusta(d, dest, b.F_BLACK, 78, w - 80), fill=cor, anchor="mm")
            topo_img = 250
        area = (30 + h - 22) - topo_img
        if p.get("foto"):
            arq = p.get("foto_resp") if resposta and p.get("foto_resp") else p["foto"]
            contem = p.get("contem", False) and not (resposta and p.get("foto_resp"))
            im = foto(arq, min(560, w - 120) if contem or p.get("largo") else area, area, contem)
            cv.alpha_composite(im, (int(cx - im.width / 2), int(topo_img + (area - im.height) / 2)))
        else:   # texto grande (conta, pista, frase): linhas de caderno atrás
            for yy in range(topo_img + 20, 30 + h - 30, 62):
                d.line([(80, yy), (30 + w - 50, yy)], fill=(205, 225, 245), width=3)
            linhas = p.get("texto", [])
            tam = 104 if len(linhas) == 1 else 84 if len(linhas) == 2 else 70
            passo = tam * 1.22
            ym = topo_img + area / 2 - passo * (len(linhas) - 1) / 2
            for i, ln in enumerate(linhas):
                d.text((cx, ym + i * passo), ln, font=_ajusta(d, ln, b.F_BLACK, tam, w - 110), fill=b.NAVY,
                       anchor="mm")
        _cache[key] = cv
    return _cache[key]


def opcao_sprite(k, i, txt, estado=None):
    key = ("op", k, i, estado)
    if key not in _cache:
        cv = Image.new("RGBA", (OPT_W + 60, OPT_H + 60), (0, 0, 0, 0))
        x0, y0 = 30, 30
        if estado == "sim":
            glow = Image.new("RGBA", cv.size, (0, 0, 0, 0))
            ImageDraw.Draw(glow).rounded_rectangle([x0 - 18, y0 - 18, x0 + OPT_W + 18, y0 + OPT_H + 18], 70,
                                                   fill=(255, 240, 120, 210))
            cv.alpha_composite(glow.filter(ImageFilter.GaussianBlur(14)))
        fill = (60, 200, 90) if estado == "sim" else b.WHITE
        b.shadowed_round_rect(cv, (x0, y0, x0 + OPT_W, y0 + OPT_H), 60, fill)
        d = ImageDraw.Draw(cv)
        d.rounded_rectangle([x0, y0, x0 + OPT_W, y0 + OPT_H], 60, outline=b.NAVY, width=6)
        d.ellipse([x0 + 14, y0 + 12, x0 + 110, y0 + 108], fill=b.YELLOW if estado != "sim" else b.WHITE,
                  outline=b.NAVY, width=5)
        d.text((x0 + 62, y0 + 58), "ABC"[i], font=b.font(b.F_BLACK, 58), fill=b.NAVY, anchor="mm")
        ban = (PERG[k - 1].get("bandeiras") or [None] * 3)[i]
        esq = 0
        if ban and os.path.exists(ban):   # bandeira ao lado da letra
            bd = Image.open(ban).convert("RGBA")
            r = 66 / bd.height
            bd = bd.resize((max(1, int(bd.width * r)), 66), Image.LANCZOS)
            if bd.width > 110:
                bd = bd.resize((110, int(66 * 110 / bd.width)), Image.LANCZOS)
            cv.alpha_composite(bd, (x0 + 128, int(y0 + OPT_H / 2 - bd.height / 2)))
            d.rectangle([x0 + 128, y0 + OPT_H / 2 - bd.height / 2, x0 + 128 + bd.width,
                         y0 + OPT_H / 2 + bd.height / 2], outline=b.NAVY, width=2)
            esq = 70
        fo = _ajusta(d, txt, b.F_BLACK, 62, OPT_W - 260 - esq)
        d.text((x0 + OPT_W / 2 + 40 + esq, y0 + OPT_H / 2), txt, font=fo,
               fill=b.WHITE if estado == "sim" else b.NAVY, anchor="mm",
               stroke_width=3 if estado == "sim" else 0, stroke_fill=b.NAVY)
        if estado == "sim":  # ✔
            cx, cy = x0 + OPT_W - 62, y0 + OPT_H / 2
            d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=b.WHITE, outline=b.NAVY, width=4)
            d.line([(cx - 20, cy), (cx - 5, cy + 16), (cx + 22, cy - 16)], fill=(40, 170, 70), width=10)
        if estado == "nao":
            sombra = Image.new("RGBA", cv.size, (0, 0, 0, 0))
            ImageDraw.Draw(sombra).rounded_rectangle([x0, y0, x0 + OPT_W, y0 + OPT_H], 60, fill=(20, 30, 60, 140))
            cv.alpha_composite(sombra)
        _cache[key] = cv
    return _cache[key]


def base(k, p):
    key = ("base", k)
    if key not in _cache:
        img = s.fundo(*p["cores"], seed=k).convert("RGBA")
        s.pilula(ImageDraw.Draw(img), 600, 205, CFG["rotulo"], CFG["cor_rotulo"], size=50, pad=40, h=96)
        _cache[key] = img
    return _cache[key].copy()


def colar(img, spr, cx, cy, sc):
    if sc <= 0.02:
        return
    w, h = max(1, int(spr.width * sc)), max(1, int(spr.height * sc))
    im = spr if abs(sc - 1) < 1e-3 else spr.resize((w, h), Image.BILINEAR)
    img.alpha_composite(im, (int(cx - w / 2), int(cy - h / 2)))


def zoom(img, z):
    if abs(z - 1) < 1e-3:
        return img
    w, h = img.size
    cw, ch = w / z, h / z
    x0, y0 = (w - cw) / 2, (h - ch) / 2
    return img.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))


def pula(x):
    x = min(max(x, 0.0), 1.0)
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def barra(img, frac):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = BAR
    d.rounded_rectangle([x0 - 7, y0 - 7, x1 + 7, y1 + 7], 32, fill=b.WHITE)
    d.rounded_rectangle(BAR, 25, fill=(60, 70, 110))
    if frac > 0.002:
        d.rounded_rectangle([x0, y0, max(x0 + (x1 - x0) * frac, x0 + 50), y1], 25, fill=b.ORANGE if frac > 0.3 else b.RED)
    n = math.ceil(frac * CFG["count"])
    if n > 0:
        d.text(((x0 + x1) // 2, (y0 + y1) // 2), str(n), font=b.font(b.F_BLACK, 40), fill=b.WHITE, anchor="mm",
               stroke_width=4, stroke_fill=b.NAVY)


def placar(img, k, t, respondida=False):
    eg.pontos(img, 660, 288, k - 1 + (1 if respondida else 0), len(PERG), t, raio=21, gap=14, rotulo="PONTOS:",
              rotulo_size=34, rotulo_acima=False)


def pergunta_frames(k, p, fala):
    count = CFG["count"]
    total = fala + count
    for n in range(int(total * FPS)):
        t = n / FPS
        frac = 1.0 if t < fala else 1 - (t - fala) / count
        img = base(k, p)
        te = t + (1.0 if k == 1 else 0.0)   # 1ª pergunta já inteira no 1º quadro (sem abertura)
        colar(img, cartao_sprite(k, p), CCX, CCY + 5 * math.sin(t * 2.2), pula(te / 0.4))
        for i, op in enumerate(p["opcoes"]):
            ent = pula((te - 0.25 - 0.14 * i) / 0.35)
            dx = 4 * math.sin(t * 40 + i) if frac < 0.3 else 0
            colar(img, opcao_sprite(k, i, op), 540 + dx, OPT_Y[i] + 4 * math.sin(t * 3 + i), ent)
        barra(img, frac)
        placar(img, k, t)
        pose = "pensando" if frac > 0.3 else "assustado"
        b.put_palito(img, pose, 240, 140, 300, int(6 * math.sin(t * (5 if pose == "pensando" else 16))))
        if k == 1:  # chamada por cima da 1ª pergunta enquanto o gancho é falado
            eg.faixa_gancho(img, 620, 240, CFG["chamada"] + "\nVALENDO!", t, max(2.5, fala), larg=820, size=64)
        yield zoom(img, 1.0 + 0.03 * t / total).convert("RGB")


def resposta_frames(k, p, dur):
    for n in range(int(dur * FPS)):
        t = n / FPS
        img = base(k, p)
        a = min(1.0, t / 0.45)
        c0, c1 = cartao_sprite(k, p), cartao_sprite(k, p, True)
        colar(img, c1 if a >= 1 else Image.blend(c0, c1, a), CCX, CCY, 1.0)
        for i, op in enumerate(p["opcoes"]):
            if i == p["certa"]:
                sc = 1.0 + 0.12 * math.sin(min(t / 0.4, 1.0) * math.pi) + 0.04 * min(t / 0.4, 1.0)
                colar(img, opcao_sprite(k, i, op, "sim"), 540, OPT_Y[i], sc)
            else:
                colar(img, opcao_sprite(k, i, op, "nao"), 540, OPT_Y[i], 1.0 - 0.05 * min(t / 0.25, 1.0))
        placar(img, k, t, respondida=True)
        eg.mais_um(img, 540, 900, t, size=50)
        sl = min(1.0, t / 0.3)
        b.put_palito(img, "comemorando", 240, 140, 300, int((1 - sl) * 120 + 6 * math.sin(t * 9)))
        yield zoom(img, 1.03 + 0.02 * t / dur).convert("RGB")


def final_base():
    img = s.fundo(*CFG.get("cores_final", (b.BLUE, b.NAVY)), seed=3).convert("RGBA")
    d = ImageDraw.Draw(img)
    l1, l2 = CFG.get("final_titulo", ("QUANTAS VOCÊ", "ACERTOU?"))
    s.texto(d, (540, 330), l1, 110, b.WHITE)
    s.texto(d, (540, 460), l2, 150, b.YELLOW)
    d.rounded_rectangle([300, 545, 780, 655], 50, fill=b.WHITE, outline=b.NAVY, width=7)
    d.text((540, 600), f"__ / {len(PERG)}", font=b.font(b.F_BLACK, 80), fill=b.NAVY, anchor="mm")
    d.rounded_rectangle([110, 690, 970, 830], 50, fill=b.RED, outline=b.WHITE, width=8)
    s.texto(d, (540, 760), CFG.get("final_faixa", "PAUSA E COMENTA SUA NOTA!"), 62, b.WHITE, max_w=820)
    s.texto(d, (540, 900), "QUIZ COMPLETO NO CANAL:", 58, b.WHITE, max_w=900)
    b.selo(img, 540, 1000, 1.3)
    b.put_palito(img, "apontando", 380, 540, 1520)
    cred = CFG.get("creditos") or []
    if cred:
        f = b.font(b.F_BOLD, 22)
        linhas, cur = [], CFG.get("creditos_titulo", "Fotos (Wikimedia Commons): ")
        for parte in cred:
            if d.textlength(cur + parte, font=f) > 960:
                linhas.append(cur)
                cur = ""
            cur += parte + "  •  "
        linhas.append(cur.rstrip(" •"))
        for i, t in enumerate(linhas):
            d.text((540, 1600 + i * 30), t, font=f, fill=(235, 235, 245), anchor="mm")
    return img


def final_frames(dur):
    bs = final_base()
    for n in range(int(dur * FPS)):
        yield zoom(bs, 1.0 + 0.05 * n / FPS / dur).convert("RGB")


def previa():
    out = os.path.join(CFG["here"], "previa")
    os.makedirs(out, exist_ok=True)
    fr = list(pergunta_frames(1, PERG[0], 3.0))
    ims = [fr[8], list(resposta_frames(1, PERG[0], 1.2))[-1]]
    for k in range(2, len(PERG) + 1):
        ims.append(list(pergunta_frames(k, PERG[k - 1], 1.0))[50])
        ims.append(list(resposta_frames(k, PERG[k - 1], 1.2))[-1])
    ims.append(list(final_frames(1.0))[10])
    sheet = Image.new("RGB", (6 * 370, ((len(ims) + 5) // 6) * 650), (25, 25, 25))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((360, 640)), ((i % 6) * 370, (i // 6) * 650))
    sheet.save(os.path.join(out, "prancha.jpg"), quality=85)
    print(out)


def main():
    vozes()
    tmp = tempfile.mkdtemp(prefix=f"short_{CFG['nome']}_")
    sfx = b.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = s.Timeline(video)
    ultimo = None
    for k, p in enumerate(PERG, 1):   # sem abertura: a 1ª imagem já é a pergunta (NOVO RITMO, 2026-11-17)
        q = A(f"q{k}.mp3")
        fala = s.duracao(q) + 0.2
        if ultimo is None:
            tl.sound(sfx["whoosh"], vol=0.6)
        else:   # transição SPLASH entre as perguntas (motion graphics, 2026-11-21)
            s.transicao(tl, sfx, ultimo, next(pergunta_frames(k, p, fala)), n=k, total=len(PERG))
        tl.sound(q, at=tl.t + 0.1, voz=True)
        for n in range(int(CFG["count"])):
            tl.sound(sfx["tick"], at=tl.t + fala + n, vol=0.8)
        for f in pergunta_frames(k, p, fala):
            tl.frame(f)
        a = A(f"a{k}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(a, at=tl.t + 0.15, voz=True)
        for f in resposta_frames(k, p, s.duracao(a) + 0.7):
            tl.frame(f)
            ultimo = f
    tl.sound(sfx["whoosh"])
    tl.sound(A("final.mp3"), at=tl.t + 0.2, voz=True)
    for f in final_frames(s.duracao(A("final.mp3")) + 0.7):
        tl.frame(f)
    tl.close()
    saida = os.path.join(CFG["here"], f"short-{CFG['nome']}.mp4")
    s.mixar(tl, video, CFG["musica"], saida)
    print(f"OK {saida} ({tl.t:.1f}s)")


def creditos(pasta_longo, chaves):
    """Linhas de crédito das fotos usadas, a partir do creditos.json do longo. `chaves` = nomes (chave do json)
    ou arquivos (campo "arquivo"); o que não estiver lá (bandeiras, domínio público) fica de fora."""
    import json
    cj = json.load(open(os.path.join(pasta_longo, "creditos.json"), encoding="utf-8"))
    por_arq = {v.get("arquivo"): (k, v) for k, v in cj.items()}
    out = []
    for c in chaves:
        k, v = (c, cj[c]) if c in cj else por_arq.get(c, (None, None))
        if v and v.get("autor"):
            linha = f"{k}: {v['autor']} ({v.get('lic', '')})"
            if linha not in out:
                out.append(linha)
    return out


def rodar(cfg, perg):
    CFG.clear()
    CFG.update(cfg)
    CFG.setdefault("count", 3.5)
    PERG[:] = perg
    previa() if "--previa" in sys.argv else main()
