"""Short "Craques de A a Z 2" (craques-1), do vídeo 52 (videos/52-jogadores-a-z-2).

5 perguntas (30 a 50 s), sem abertura (NOVO RITMO, 2026-11-17): a 1ª imagem já é a pergunta, com a chamada na faixa
vermelha. O cartão mostra a LETRA + uma pista; na resposta vira a FOTO REAL do craque (Wikimedia Commons, as mesmas
do vídeo longo; créditos na tela final). Transição SPLASH entre as perguntas. Fala final curta + "o quiz completo tá
no canal". Descrição com o link do longo (LINK_DO_VIDEO_LONGO).
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
SAIDA = os.path.join(HERE, "short-craques-1.mp4")
V52 = os.path.join(QP, "videos", "52-jogadores-a-z-2")
CRED = json.load(open(os.path.join(V52, "creditos.json"), encoding="utf-8"))
CHAMADA = "QUASE NINGUÉM ACERTA A ÚLTIMA!"   # s.CHAMADAS; diferente dos últimos 3 Shorts
MUSICA = os.path.join(QP, "musicas", "Wallpaper.mp3")
COUNT = 2.5
N = 5
ROXO, AZUL, MAGENTA, VERMELHO = ((120, 50, 200), (50, 15, 110)), ((40, 60, 190), (15, 20, 90)), \
    ((170, 40, 160), (80, 10, 80)), ((200, 30, 60), (90, 5, 30))

# letra, pista (linhas), fala, foto (fotos do vídeo 52), crédito, opções A-C, índice certo, resposta falada, fundo
PERG = [
    ("R", ["O FENÔMENO,", "camisa 9 do PENTA"], "Letra R: o Fenômeno!", "lca-ronaldo-fenomeno.jpg",
     "Ronaldo Fenômeno", ["ROMÁRIO", "RONALDO", "RIVALDO"], 1, "Ronaldo Fenômeno!", ROXO),
    ("E", ["Joia do Palmeiras,", "o \"MESSINHO\""], "Letra E: o Messinho do Palmeiras!", "joia-estevao.jpg",
     "Estêvão", ["ENDRICK", "EVERTON", "ESTÊVÃO"], 2, "Estêvão!", AZUL),
    ("C", ["Goleiro ESPANHOL,", "campeão em 2010"], "Letra C: goleiro espanhol, campeão em 2010.",
     "lgol-casillas.jpg", "Casillas", ["CASILLAS", "COURTOIS", "CÉSAR"], 0, "Casillas!", MAGENTA),
    ("Z", ["Lateral ARGENTINO,", "ídolo da Inter"], "Letra Z: lateral argentino da Inter.",
     "llat-zanetti.jpg", "Zanetti", ["ZAMORANO", "ZANETTI", "ZABALETA"], 1, "Zanetti!", AZUL),
    ("P", ["Goleiro TCHECO que", "jogava de CAPACETE"], "A última! Letra P: o goleiro de capacete!",
     "lgol-petr-cech.jpg", "Petr Čech", ["PICKFORD", "PATRÍCIO", "PETR ČECH"], 2, "Pêtr Tchéc!", VERMELHO),
]
FALAS = {
    "gancho": "Quase ninguém acerta a última!",   # falado por cima da 1ª pergunta
    "final": "O quiz completo tá no canal!",  # fala final curta (retenção) + chama para o longo
}
CARD = (90, 330, 990, 950)          # cartão da pergunta
OPT_Y = (1065, 1210, 1355)          # centro das opções
OPT_W, OPT_H = 820, 120
BAR = (110, 1468, 970, 1514)
PRON = {"Ødegaard": "Ódegaard"}


def textos():
    t = dict(FALAS)
    for k, p in enumerate(PERG, 1):
        t[f"q{k}"] = p[2]
        t[f"a{k}"] = p[7]
    t["q1"] = f"{FALAS['gancho']} {PERG[0][2]}"   # chamada falada POR CIMA da 1ª pergunta, sem abertura
    t.pop("gancho")
    return t


def vozes():
    import edge_tts
    if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
        import ssl, edge_tts.communicate as _c
        _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    for k, txt in textos().items():
        if os.path.exists(A(f"{k}.mp3")) and os.path.getsize(A(f"{k}.mp3")) < 1024:
            os.remove(A(f"{k}.mp3"))
        if not os.path.exists(A(f"{k}.mp3")):
            asyncio.run(edge_tts.Communicate(txt, "pt-BR-AntonioNeural", rate="+20%", pitch="+2Hz").save(A(f"{k}.mp3")))
            print("voz", k, "-", txt, flush=True)


_cache = {}


def cartao_sprite(k, p, resposta=False):
    """Cartão branco: LETRA gigante + pista; na resposta, a foto do craque com o nome."""
    key = ("cartao", k, resposta)
    if key not in _cache:
        x0, y0, x1, y1 = CARD
        w, h = x1 - x0, y1 - y0
        cv = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
        b.shadowed_round_rect(cv, (30, 30, 30 + w, 30 + h), 44, b.WHITE)
        d = ImageDraw.Draw(cv)
        d.rounded_rectangle([30, 30, 30 + w, 30 + h], 44, outline=b.NAVY, width=7)
        d.text((30 + w / 2, 95), f"{k}. JOGADOR COM A LETRA", font=b.font(b.F_BOLD, 52), fill=b.NAVY, anchor="mm")
        if resposta:
            lado = h - 215
            im = ImageOps.fit(Image.open(os.path.join(V52, "fotos", p[3])).convert("RGBA"), (lado, lado), Image.LANCZOS,
                              centering=(0.5, 0.3))
            m = Image.new("L", (lado, lado), 0)
            ImageDraw.Draw(m).rounded_rectangle([0, 0, lado - 1, lado - 1], 28, fill=255)
            im.putalpha(m)
            cv.alpha_composite(im, (int(30 + w / 2 - lado / 2), 30 + 115))
            nome = p[5][p[6]]
            fo = b.font(b.F_BLACK, 72)
            while d.textlength(nome, font=fo) > w - 120 and fo.size > 36:
                fo = b.font(b.F_BLACK, fo.size - 3)
            d.rounded_rectangle([30 + 50, 30 + h - 190, 30 + w - 50, 30 + h - 105], 40, fill=b.NAVY)
            d.text((30 + w / 2, 30 + h - 148), nome, font=fo, fill=b.YELLOW, anchor="mm")
        else:
            cx = 30 + w / 2
            d.rounded_rectangle([cx - 150, 140, cx + 150, 390], 40, fill=p[8][0], outline=b.NAVY, width=6)
            d.text((cx, 265), p[0], font=b.font(b.F_BLACK, 210), fill=b.WHITE, anchor="mm", stroke_width=8,
                   stroke_fill=b.NAVY)
            fo = b.font(b.F_BLACK, 74)
            while max(d.textlength(t, font=fo) for t in p[1]) > w - 70 and fo.size > 36:
                fo = b.font(b.F_BLACK, fo.size - 3)
            y0 = 400 + (h + 30 - 400) / 2 - (len(p[1]) - 1) * fo.size * 0.6
            for i, t in enumerate(p[1]):
                d.text((cx, y0 + i * fo.size * 1.2), t, font=fo, fill=b.NAVY, anchor="mm")
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
    s.pilula(ImageDraw.Draw(img), 600, 205, "CRAQUES DE A a Z 2", (40, 15, 100), size=46, pad=36, h=96)


def base(k, p):
    key = ("base", k)
    if key not in _cache:
        img = s.fundo(*p[8], seed=k + 20).convert("RGBA")
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
        for i, op in enumerate(p[5]):
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
        card = cartao_sprite(k, p, True) if a >= 1 else Image.blend(cartao_sprite(k, p), cartao_sprite(k, p, True), a)
        colar(img, card, CCX, CCY, 1.0)
        for i, op in enumerate(p[5]):
            if i == p[6]:
                sc = 1.0 + 0.12 * math.sin(min(t / 0.4, 1.0) * math.pi) + 0.04 * min(t / 0.4, 1.0)
                colar(img, opcao_sprite(i, op, "sim"), 540, OPT_Y[i], sc)
            else:
                colar(img, opcao_sprite(i, op, "nao"), 540, OPT_Y[i], 1.0 - 0.05 * min(t / 0.25, 1.0))
        placar(img, k, t, respondida=True)
        eg.mais_um(img, 540, 905, t, size=50)
        sl = min(1.0, t / 0.3)
        b.put_palito(img, "comemorando", 240, 140, 300, int((1 - sl) * 120 + 6 * math.sin(t * 9)))
        yield zoom(img, 1.03 + 0.02 * t / dur).convert("RGB")


def final_base():
    img = s.fundo(*ROXO, seed=3).convert("RGBA")
    d = ImageDraw.Draw(img)
    s.texto(d, (540, 330), "QUANTOS VOCÊ", 110, b.WHITE)
    s.texto(d, (540, 460), "ACERTOU?", 150, b.YELLOW)
    d.rounded_rectangle([300, 545, 780, 655], 50, fill=b.WHITE, outline=b.NAVY, width=7)
    d.text((540, 600), f"__ / {N}", font=b.font(b.F_BLACK, 80), fill=b.NAVY, anchor="mm")
    d.rounded_rectangle([110, 690, 970, 830], 50, fill=b.RED, outline=b.WHITE, width=8)
    s.texto(d, (540, 760), "PAUSA E COMENTA SUA NOTA!", 62, b.WHITE, max_w=820)
    s.texto(d, (540, 900), "QUIZ COMPLETO NO CANAL:", 58, b.WHITE, max_w=900)
    b.selo(img, 540, 1000, 1.3)
    b.put_palito(img, "apontando", 380, 540, 1500)
    f = b.font(b.F_BOLD, 21)
    d.text((540, 1560), "Fotos: Wikimedia Commons", font=f, fill=(235, 235, 245), anchor="mm")
    for i, p in enumerate(PERG):
        c = CRED[p[4]]
        d.text((540, 1592 + i * 28), f"{p[4]}: {c['autor']} ({c['lic']})", font=f, fill=(235, 235, 245), anchor="mm")
    return img


def final_frames(dur):
    bs = final_base()
    for n in range(int(dur * FPS)):
        yield zoom(bs, 1.0 + 0.05 * n / FPS / dur).convert("RGB")


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = list(pergunta_frames(1, PERG[0], 3.0))
    ims = [fr[0], fr[40], list(resposta_frames(1, PERG[0], 1.2))[-1], list(pergunta_frames(3, PERG[2], 1.0))[50],
           list(resposta_frames(3, PERG[2], 1.2))[-1], list(pergunta_frames(5, PERG[4], 1.0))[50],
           list(resposta_frames(5, PERG[4], 1.2))[-1], list(final_frames(1.0))[10]]
    sheet = Image.new("RGB", (len(ims) * 370, 640), (25, 25, 25))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((360, 640)), (i * 370, 0))
    sheet.save(os.path.join(out, "prancha.jpg"), quality=85)
    print(out)


def main():
    vozes()
    tmp = tempfile.mkdtemp(prefix="short_craques1_")
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
