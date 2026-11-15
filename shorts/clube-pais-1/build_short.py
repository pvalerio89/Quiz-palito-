"""Short "Quem jogou aqui?" (clube-pais-1), do vídeo 32 (feito a partir do carreira-1).

Intro rapidinha, 1ª pergunta já com a chamada na faixa vermelha, placar "PONTOS:" e "+1 SE ACERTOU!".
O cartão mostra a BANDEIRA do país + o ESCUDO de um clube onde o jogador já jogou; na resposta vira a foto real
(Wikimedia Commons, as mesmas do vídeo 32; créditos na tela final). Fala final curta (2026-11-12).
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
SAIDA = os.path.join(HERE, "short-clube-pais-1.mp4")
FOTOS = os.path.join(QP, "videos", "32-jogador-clube-pais")   # fotos, escudos e bandeiras do vídeo 32
CRED = json.load(open(os.path.join(FOTOS, "creditos.json"), encoding="utf-8"))
ITENS = {r["jogador"]: r for r in json.load(open(os.path.join(FOTOS, "itens.json"), encoding="utf-8"))}
CHAMADA = "SEU AMIGO NÃO ACERTA ESSA!"   # s.CHAMADAS; diferente dos últimos 3 Shorts
MUSICA = os.path.join(QP, "musicas", "Sneaky Snitch.mp3")
EMOJI = "C:/Windows/Fonts/seguiemj.ttf"
COUNT = 4.0
N = 6

# pergunta (tela), fala, foto (nome em CRED), opções A-C, índice certo, resposta falada, fundo (topo, base)
PERG = [
    ("Quem é?", "Brasileiro que já jogou no Real Madrid. Quem é?", "Vinícius Jr",
     ["Neymar", "Vinícius Jr", "Mbappé"], 1, "Vinícius Júnior!", ((20, 150, 80), (5, 70, 50))),
    ("Quem é?", "Egípcio que já jogou no Liverpool?", "Salah",
     ["Salah", "Mané", "Firmino"], 0, "Salah!", ((30, 110, 210), (15, 40, 130))),
    ("Quem é?", "Brasileiro que já jogou no PSG? Cuidado!", "Ronaldinho",
     ["Kaká", "Beckham", "Ronaldinho"], 2, "Ronaldinho!", ((150, 70, 200), (60, 25, 120))),
    ("Quem é?", "Português que já jogou no Benfica?", "Rúben Dias",
     ["Cristiano Ronaldo", "Rúben Dias", "Di María"], 1, "Rúben Dias! O Cristiano nunca jogou lá!", ((0, 160, 170), (0, 70, 100))),
    ("Quem é?", "Brasileiro que já jogou no PSV?", "Romário",
     ["Romário", "Bebeto", "Van Nistelrooy"], 0, "Romário!", ((235, 60, 50), (120, 15, 30))),
    ("Quem é?", "A última, a mais difícil! Espanhol que já jogou no Leverkusen?", "Carvajal",
     ["Xabi Alonso", "Sergio Ramos", "Carvajal"], 2, "Carvajal!", ((20, 150, 80), (5, 70, 50))),
]
FALAS = {
    "intro": "Quem jogou aqui?",                # intro rapidinha (2 a 3 s)
    "gancho": "Seu amigo não acerta essa! Valendo!",            # falado por cima da 1ª pergunta
    "final": "Comenta sua nota!",                          # fala final curta (retenção)
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
    t["q1"] = f"{FALAS['gancho']} {PERG[0][1]}"   # chamada falada POR CIMA da 1ª pergunta, logo depois da intro
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


def foto(nome, size, rev=1.0):
    """rev = 0 (zoom 2,2x e borrada) .. 1 (inteira e nítida). Só a nítida fica guardada (tamanho fixo)."""
    key = ("foto", nome, size)
    if rev >= 1 and key in _cache:
        return _cache[key]
    src = Image.open(os.path.join(FOTOS, "fotos", ITENS[nome]["foto"])).convert("RGB")
    z = 1 + 1.2 * (1 - rev) ** 1.5
    w = src.width / z
    x0 = min(max(src.width * 0.5 - w / 2, 0), src.width - w)
    y0 = min(max(src.height * 0.40 - w / 2, 0), src.height - w)
    im = src.resize((size, size), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + w))
    r = 22 * (1 - rev) ** 1.4
    if r > 0.3:
        im = im.filter(ImageFilter.GaussianBlur(r))
    im = im.convert("RGBA")
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1], 28, fill=255)
    im.putalpha(m)
    if rev >= 1:
        _cache[key] = im
    return im


def grade(nome, w, h):
    """Bandeira do país + escudo do clube, com os nomes."""
    r = ITENS[nome]
    cv = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(cv)
    bd = Image.open(os.path.join(FOTOS, "bandeiras", r["bandeira"] + ".png")).convert("RGBA")
    bd.thumbnail((300, 150), Image.LANCZOS)
    by = 10
    d.rectangle([w / 2 - bd.width / 2 - 5, by - 5, w / 2 + bd.width / 2 + 4, by + bd.height + 4], fill=b.NAVY)
    cv.alpha_composite(bd, (int(w / 2 - bd.width / 2), by))
    d.text((w / 2, by + bd.height + 30), r["pais"], font=b.font(b.F_BLACK, 40), fill=b.NAVY, anchor="mm")
    cy = by + bd.height + 80
    d.ellipse([w / 2 - 30, cy - 30, w / 2 + 30, cy + 30], fill=b.ORANGE, outline=b.WHITE, width=4)
    d.text((w / 2, cy - 3), "+", font=b.font(b.F_BLACK, 56), fill=b.WHITE, anchor="mm")
    es = Image.open(os.path.join(FOTOS, "escudos", r["clube"] + ".png")).convert("RGBA")
    es.thumbnail((150, 150), Image.LANCZOS)
    ey = cy + 30
    cv.alpha_composite(es, (int(w / 2 - es.width / 2), int(ey + (150 - es.height) / 2)))
    d.text((w / 2, ey + 150 + 28), r["clube_nome"], font=b.font(b.F_BLACK, 40), fill=b.NAVY, anchor="mm")
    return cv


def cartao_sprite(k, p, rev=0):
    """Cartão branco: na pergunta (rev=0) os escudos em ordem; na resposta (rev=1) a foto real."""
    key = ("cartao", k, rev)
    if key not in _cache:
        x0, y0, x1, y1 = CARD
        w, h = x1 - x0, y1 - y0
        cv = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
        b.shadowed_round_rect(cv, (30, 30, 30 + w, 30 + h), 44, b.WHITE)
        d = ImageDraw.Draw(cv)
        d.rounded_rectangle([30, 30, 30 + w, 30 + h], 44, outline=b.NAVY, width=7)
        if rev:
            tt, fo = f"É O {p[2].upper()}!", b.font(b.F_BLACK, 60)
            while d.textlength(tt, font=fo) > w - 80 and fo.size > 30:
                fo = b.font(b.F_BLACK, fo.size - 2)
            d.text((30 + w / 2, 95), tt, font=fo, fill=(220, 40, 60), anchor="mm")
            em = foto(p[2], 440)
            cv.alpha_composite(em, (int(30 + w / 2 - em.width / 2), int(30 + h - 22 - em.height)))
        else:
            d.text((30 + w / 2, 95), f"{k}. PAÍS + CLUBE", font=b.font(b.F_BLACK, 56), fill=b.NAVY, anchor="mm")
            g = grade(p[2], w - 40, h - 150)
            cv.alpha_composite(g, (50, 170))
        _for = [c for c in _cache if c[0] == "cartao" and c[1] != k]
        for c in _for:
            _cache.pop(c)
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
    s.pilula(ImageDraw.Draw(img), 600, 205, "QUEM É?", (40, 60, 150), size=50, pad=40, h=96)
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
        rev = 1.0
        colar(img, cartao_sprite(k, p, 0), CCX, CCY + 5 * math.sin(t * 2.2), pula(t / 0.4))
        for i, op in enumerate(p[3]):
            ent = pula((t - 0.25 - 0.14 * i) / 0.35)
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
        card = cartao_sprite(k, p, 1)
        if a < 1:
            card = Image.blend(cartao_sprite(k, p, 0), card, a)
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
    s.texto(d, (540, 900), "SEGUE O", 64, b.WHITE)
    b.selo(img, 540, 1000, 1.3)
    b.put_palito(img, "apontando", 380, 540, 1520)
    cred = "  •  ".join(f"{p[2]}: {CRED[p[2]]['autor']} ({CRED[p[2]]['lic']})" for p in PERG) + "  •  Escudos: marcas dos clubes"
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


def intro_frames(dur):
    return s.intro_rapida("QUEM JOGOU", "AQUI?", dur,
                          [esc(n, 200) for n in ["barcelona", "chelsea", "juventus"]])


def esc(clube, size):
    im = Image.open(os.path.join(FOTOS, "escudos", clube + ".png")).convert("RGBA")
    im.thumbnail((size, size), Image.LANCZOS)
    return im


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = list(pergunta_frames(1, PERG[0], 3.0))
    ims = [list(intro_frames(2.0))[40], fr[8], fr[40], list(resposta_frames(1, PERG[0], 1.2))[-1], list(pergunta_frames(4, PERG[3], 1.0))[50],
           list(pergunta_frames(5, PERG[4], 1.0))[50], list(resposta_frames(6, PERG[5], 1.2))[-1],
           list(final_frames(1.0))[10]]
    sheet = Image.new("RGB", (len(ims) * 370, 640), (25, 25, 25))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((360, 640)), (i * 370, 0))
    sheet.save(os.path.join(out, "prancha.jpg"), quality=85)
    print(out)


def main():
    vozes()
    tmp = tempfile.mkdtemp(prefix="short_clube_pais_")
    sfx = b.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = s.Timeline(video)
    # intro rapidinha (2 a 3 s) e logo a 1ª pergunta (Patrick, 2026-11-10)
    tl.sound(A("intro.mp3"), at=0.1, voz=True)
    for f in intro_frames(s.duracao(A("intro.mp3"))):
        tl.frame(f)
    for k, p in enumerate(PERG, 1):
        q = A(f"q{k}.mp3")
        tl.sound(sfx["whoosh"], vol=0.6)
        tl.sound(q, at=tl.t + 0.1, voz=True)
        fala = s.duracao(q) + 0.2
        for n in range(int(COUNT)):
            tl.sound(sfx["tick"], at=tl.t + fala + n, vol=0.8)
        for f in pergunta_frames(k, p, fala):
            tl.frame(f)
        a = A(f"a{k}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(a, at=tl.t + 0.15, voz=True)
        for f in resposta_frames(k, p, s.duracao(a) + 0.7):
            tl.frame(f)
    tl.sound(sfx["whoosh"])
    tl.sound(A("final.mp3"), at=tl.t + 0.2, voz=True)
    for f in final_frames(s.duracao(A("final.mp3")) + 1.2):
        tl.frame(f)
    tl.close()
    s.mixar(tl, video, MUSICA, SAIDA)
    print(f"OK {SAIDA} ({tl.t:.1f}s)")


if __name__ == "__main__":
    previa() if "--previa" in sys.argv else main()
