"""Short "Adivinhe o animal pela foto 2" (animais-2), do vídeo 55 (videos/55-animal-foto-2), feito a partir de shorts/modelo.

Sem abertura (NOVO RITMO, 2026-11-17): a 1ª imagem já é a pergunta, com a chamada na faixa vermelha.
5 perguntas do MESMO tema do longo (PLANO DE MONETIZAÇÃO, 2026-11-20), fotos reais do vídeo 55 (Wikimedia Commons,
créditos na tela final), 30 a 50 s, fala final curta. Descrição com o link do longo (LINK_DO_VIDEO_LONGO).
Uso: py -3 build_short.py            (gera vozes que faltam e monta o Short)
     py -3 build_short.py --previa   (prancha com quadros para conferir)
"""
import asyncio, json, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import short_base as s
from short_base import b, W, H, FPS
sys.path.insert(0, os.path.join(QP, "videos", "modelo-opcoes"))
import engaja as eg

A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "short-animais-2.mp4")
FOTOS = os.path.join(QP, "videos", "55-animal-foto-2")   # fotos do vídeo 55
CRED = json.load(open(os.path.join(FOTOS, "creditos.json"), encoding="utf-8"))
CHAMADA = "SERÁ QUE VOCÊ GABARITA?"   # s.CHAMADAS; diferente dos últimos 3 Shorts
MUSICA = os.path.join(QP, "musicas", "Wallpaper.mp3")
EMOJI = "C:/Windows/Fonts/seguiemj.ttf"
COUNT = 3.5
N = 5

# pergunta (tela), fala, foto (nome em creditos.json), opções A-C, índice certo, resposta falada, fundo (topo, base)
PERG = [
    ("Que animal é esse?
DE OLHOS GRANDES", "Que animal é esse?", "coruja",
     ["Gavião", "Coruja", "Águia"], 1, "Coruja!", ((0, 170, 170), (0, 75, 90))),
    ("Não confunda!
LHAMA OU ALPACA?", "Cuidado com a pegadinha! E esse?", "alpaca",
     ["Alpaca", "Lhama", "Ovelha"], 0, "Alpaca! A lhama é maior!", ((135, 65, 210), (55, 20, 110))),
    ("Esse filhote vira...
QUAL ANIMAL?", "Esse filhote vai virar qual animal?", "filhote-flamingo",
     ["Pato", "Ganso", "Flamingo"], 2, "Flamingo! Nasce cinzinha!", ((235, 95, 150), (135, 25, 80))),
    ("Bicho raro!
QUE ANIMAL É ESSE?", "Agora um raro! Que bicho é esse?", "quokka",
     ["Castor", "Quokka", "Marmota"], 1, "Quokka! O bicho mais feliz do mundo!", ((45, 60, 150), (10, 14, 55))),
    ("O mais estranho!
QUE BICHO É ESSE?", "A última! Que bicho é esse?", "aye-aye",
     ["Társio", "Lóris", "Aye-aye"], 2, "Aye-aye!", ((235, 60, 50), (120, 15, 30))),
]
FALAS = {
    "gancho": "Será que você gabarita?",   # falado por cima da 1ª pergunta (sem abertura)
    "final": "Os trinta e seis bichos tão no canal!",  # fala final curta (retenção) + chama para o longo
}
CARD = (90, 330, 990, 950)          # cartão da pergunta
OPT_Y = (1065, 1210, 1355)          # centro das opções
OPT_W, OPT_H = 820, 120
BAR = (110, 1468, 970, 1514)


def textos():
    t = dict(FALAS)
    for k, p in enumerate(PERG, 1):
        t[f"q{k}"] = p[1]
        t[f"a{k}"] = p[5]
    t["q1"] = f"{FALAS['gancho']} {PERG[0][1]}"   # chamada falada POR CIMA da 1ª pergunta, sem abertura
    t.pop("gancho")
    return t


def vozes():
    import edge_tts
    if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
        import ssl, edge_tts.communicate as _c
        _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    for k, txt in textos().items():
        if not os.path.exists(A(f"{k}.mp3")):
            asyncio.run(edge_tts.Communicate(txt, "pt-BR-AntonioNeural", rate="+20%", pitch="+2Hz").save(A(f"{k}.mp3")))
            print("voz", k, "-", txt, flush=True)


_cache = {}


def emoji(ch, size):
    key = ("emoji", ch, size)
    if key not in _cache:
        f = ImageFont.truetype(EMOJI, 109)
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((80, 80), ch, font=f, embedded_color=True, anchor="mm")
        im = im.crop(im.getbbox())
        r = size / max(im.size)
        _cache[key] = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    return _cache[key]


def foto(nome, size, amarela=False):   # amarela não se usa aqui
    key = ("foto", nome, size, amarela)
    if key not in _cache:
        im = Image.open(os.path.join(FOTOS, "fotos", CRED[nome]["arquivo"])).convert("RGBA").resize((size, size), Image.LANCZOS)
        if amarela:  # tudo amarelo: só luz e sombra
            im = ImageOps.colorize(im.convert("L"), black=(70, 45, 0), mid=(255, 205, 0), white=(255, 250, 200)).convert("RGBA")
        m = Image.new("L", (size, size), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1], 28, fill=255)
        im.putalpha(m)
        _cache[key] = im
    return _cache[key]


def cartao_sprite(k, p, amarela=False):
    """Cartão branco com número, pergunta e foto (amarela na pergunta, colorida na resposta)."""
    key = ("cartao", k, amarela)
    if key not in _cache:
        x0, y0, x1, y1 = CARD
        w, h = x1 - x0, y1 - y0
        cv = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
        b.shadowed_round_rect(cv, (30, 30, 30 + w, 30 + h), 44, b.WHITE)
        d = ImageDraw.Draw(cv)
        d.rounded_rectangle([30, 30, 30 + w, 30 + h], 44, outline=b.NAVY, width=7)
        linhas = p[0].split("\n")
        f1 = b.font(b.F_BOLD, 58)
        f2 = b.font(b.F_BLACK, 74)
        d.text((30 + w / 2, 105), f"{k}. {linhas[0]}", font=f1, fill=b.NAVY, anchor="mm")
        f = f2
        while d.textlength(linhas[1], font=f) > w - 80 and f.size > 40:
            f = b.font(b.F_BLACK, f.size - 4)
        d.text((30 + w / 2, 195), linhas[1], font=f, fill=(220, 40, 60), anchor="mm")
        em = foto(p[2], 380, amarela)
        cv.alpha_composite(em, (int(30 + w / 2 - em.width / 2), int(30 + h - 22 - em.height)))
        _cache[key] = cv
    return _cache[key]


def opcao_sprite(i, txt, estado=None):
    key = ("op", i, txt, estado)
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
        fo = b.font(b.F_BLACK, 62)
        while d.textlength(txt, font=fo) > OPT_W - 260 and fo.size > 36:
            fo = b.font(b.F_BLACK, fo.size - 2)
        d.text((x0 + OPT_W / 2 + 40, y0 + OPT_H / 2), txt, font=fo,
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


def topo(img, k):
    s.pilula(ImageDraw.Draw(img), 600, 205, "ANIMAL PELA FOTO 2", (0, 120, 120), size=50, pad=40, h=96)
    # a linha "PERGUNTA k/N" virou o placar de bolinhas (desenhado a cada quadro em placar())


def base(k, p):
    key = ("base", k)
    if key not in _cache:
        img = s.fundo(*p[6], seed=k).convert("RGBA")
        topo(img, k)
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
    n = math.ceil(frac * COUNT)
    if n > 0:
        d.text(((x0 + x1) // 2, (y0 + y1) // 2), str(n), font=b.font(b.F_BLACK, 40), fill=b.WHITE, anchor="mm",
               stroke_width=4, stroke_fill=b.NAVY)


CCX, CCY = (CARD[0] + CARD[2]) // 2, (CARD[1] + CARD[3]) // 2


def placar(img, k, t, respondida=False):
    eg.pontos(img, 660, 288, k - 1 + (1 if respondida else 0), N, t, raio=21, gap=14, rotulo="PONTOS:",
              rotulo_size=34, rotulo_acima=False)


def pergunta_frames(k, p, fala):
    total = fala + COUNT
    for n in range(int(total * FPS)):
        t = n / FPS
        frac = 1.0 if t < fala else 1 - (t - fala) / COUNT
        img = base(k, p)
        te = t + (1.0 if k == 1 else 0.0)   # 1ª pergunta já inteira no 1º quadro (sem abertura)
        colar(img, cartao_sprite(k, p), CCX, CCY + 5 * math.sin(t * 2.2), pula(te / 0.4))
        for i, op in enumerate(p[3]):
            ent = pula((te - 0.25 - 0.14 * i) / 0.35)
            dx = 4 * math.sin(t * 40 + i) if frac < 0.3 else 0
            colar(img, opcao_sprite(i, op), 540 + dx, OPT_Y[i] + 4 * math.sin(t * 3 + i), ent)
        barra(img, frac)
        placar(img, k, t)
        pose = "pensando" if frac > 0.3 else "assustado"
        b.put_palito(img, pose, 240, 140, 300, int(6 * math.sin(t * (5 if pose == "pensando" else 16))))
        if k == 1:  # chamada por cima da 1ª pergunta enquanto o gancho é falado
            eg.faixa_gancho(img, 620, 240, CHAMADA + "\nVALENDO!", t, max(2.5, fala), larg=820, size=64)
        yield zoom(img, 1.0 + 0.03 * t / total).convert("RGB")


def resposta_frames(k, p, dur):
    for n in range(int(dur * FPS)):
        t = n / FPS
        img = base(k, p)
        a = min(1.0, t / 0.45)
        card = cartao_sprite(k, p, False) if a >= 1 else Image.blend(cartao_sprite(k, p), cartao_sprite(k, p, False), a)
        colar(img, card, CCX, CCY, 1.0)
        for i, op in enumerate(p[3]):
            if i == p[4]:
                sc = 1.0 + 0.12 * math.sin(min(t / 0.4, 1.0) * math.pi) + 0.04 * min(t / 0.4, 1.0)
                colar(img, opcao_sprite(i, op, "sim"), 540, OPT_Y[i], sc)
            else:
                colar(img, opcao_sprite(i, op, "nao"), 540, OPT_Y[i], 1.0 - 0.05 * min(t / 0.25, 1.0))
        placar(img, k, t, respondida=True)
        eg.mais_um(img, 540, 900, t, size=50)
        sl = min(1.0, t / 0.3)
        b.put_palito(img, "comemorando", 240, 140, 300, int((1 - sl) * 120 + 6 * math.sin(t * 9)))
        yield zoom(img, 1.03 + 0.02 * t / dur).convert("RGB")


def final_base():
    img = s.fundo(seed=3).convert("RGBA")
    d = ImageDraw.Draw(img)
    s.texto(d, (540, 330), "QUANTAS VOCÊ", 110, b.WHITE)
    s.texto(d, (540, 460), "ACERTOU?", 150, b.YELLOW)
    d.rounded_rectangle([300, 545, 780, 655], 50, fill=b.WHITE, outline=b.NAVY, width=7)
    d.text((540, 600), f"__ / {N}", font=b.font(b.F_BLACK, 80), fill=b.NAVY, anchor="mm")
    d.rounded_rectangle([110, 690, 970, 830], 50, fill=b.RED, outline=b.WHITE, width=8)
    s.texto(d, (540, 760), "PAUSA E COMENTA SUA NOTA!", 62, b.WHITE, max_w=820)
    s.texto(d, (540, 900), "QUIZ COMPLETO NO CANAL:", 58, b.WHITE, max_w=900)
    b.selo(img, 540, 1000, 1.3)
    b.put_palito(img, "apontando", 380, 540, 1520)
    cred = "  •  ".join(f"{p[2]}: {CRED[p[2]]['autor']} ({CRED[p[2]]['lic']})" for p in PERG)
    f = b.font(b.F_BOLD, 22)
    linhas, cur = [], "Fotos (Wikimedia Commons): "
    for parte in cred.split("  •  "):
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
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = list(pergunta_frames(1, PERG[0], 3.0))
    ims = [fr[0], fr[8], fr[40], list(resposta_frames(1, PERG[0], 1.2))[-1],
           list(pergunta_frames(4, PERG[3], 1.0))[50], list(resposta_frames(5, PERG[4], 1.2))[-1],
           list(final_frames(1.0))[10]]
    sheet = Image.new("RGB", (len(ims) * 370, 640), (25, 25, 25))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((360, 640)), (i * 370, 0))
    sheet.save(os.path.join(out, "prancha.jpg"), quality=85)
    print(out)


def main():
    vozes()
    tmp = tempfile.mkdtemp(prefix="short_animais2_")
    sfx = b.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = s.Timeline(video)
    # sem abertura: a 1ª imagem já é a pergunta (NOVO RITMO, 2026-11-17)
    ultimo = None
    for k, p in enumerate(PERG, 1):
        q = A(f"q{k}.mp3")
        fala = s.duracao(q) + 0.2
        if ultimo is None:
            tl.sound(sfx["whoosh"], vol=0.6)
        else:   # transição SPLASH entre as perguntas (motion graphics, 2026-11-21)
            s.transicao(tl, sfx, ultimo, next(pergunta_frames(k, p, fala)), n=k, total=len(PERG))
        tl.sound(q, at=tl.t + 0.1, voz=True)
        for n in range(int(COUNT)):
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
    s.mixar(tl, video, MUSICA, SAIDA)
    print(f"OK {SAIDA} ({tl.t:.1f}s)")


if __name__ == "__main__":
    previa() if "--previa" in sys.argv else main()
