"""Short — "Qual desses joga no Barcelona?" (6 perguntas fáceis, times da temporada 2025/26).

Formato inspirado no "Qual o correto?": 4 cartas (A–D) com bandeira + nome, 4 s de barra,
revelação com o time de cada jogador. Bandeiras livres (flagcdn), sem fotos.
Uso: py -3 build_short.py            (gera vozes que faltam e monta o Short com movimento, para TikTok e YouTube)
     py -3 build_short.py --previa   (só salva imagens das telas em previa/)
"""
import asyncio, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import short_base as s
from short_base import b, W, H, FPS

A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "short-qual-joga-1.mp4")
MUSICA = os.path.join(QP, "videos", "03-bandeiras-195", "assets", "musica.mp3")
COUNT = 4.0

# jogador: (bandeira, time em 2025/26)
JOG = {
    "Lamine Yamal": ("es", "Barcelona"), "Mbappé": ("fr", "Real Madrid"), "Haaland": ("no", "Man. City"),
    "Messi": ("ar", "Inter Miami"), "Raphinha": ("br", "Barcelona"), "Salah": ("eg", "Liverpool"),
    "Vinícius Jr": ("br", "Real Madrid"), "Cristiano Ronaldo": ("pt", "Al-Nassr"),
    "Bellingham": ("gb-eng", "Real Madrid"), "Pedri": ("es", "Barcelona"), "Dembélé": ("fr", "PSG"),
    "Lewandowski": ("pl", "Barcelona"), "Lautaro Martínez": ("ar", "Inter de Milão"), "Kane": ("gb-eng", "Bayern"),
    "Modric": ("hr", "Milan"), "Son": ("kr", "LAFC"), "Bruno Fernandes": ("pt", "Man. United"),
}
PAIS = {"es": "Espanha", "fr": "França", "no": "Noruega", "ar": "Argentina", "br": "Brasil", "eg": "Egito",
        "pt": "Portugal", "gb-eng": "Inglaterra", "pl": "Polônia", "hr": "Croácia", "kr": "Coreia do Sul"}
# tipo, alvo (time ou bandeira), texto na tela, como falar, cor, fundo (topo, base), opções A–D
PERG = [
    ("clube", "Barcelona", "BARCELONA", "joga no Barcelona", (165, 0, 68), ((120, 20, 80), (0, 60, 140)),
     ["Mbappé", "Lamine Yamal", "Haaland", "Messi"]),
    ("clube", "Real Madrid", "REAL MADRID", "joga no Real Madrid", (215, 170, 30), ((190, 150, 40), (20, 30, 80)),
     ["Raphinha", "Salah", "Vinícius Jr", "Cristiano Ronaldo"]),
    ("selecao", "ar", "ARGENTINA", "é da seleção da Argentina", (90, 170, 230), ((110, 180, 235), (20, 50, 110)),
     ["Lewandowski", "Salah", "Kane", "Lautaro Martínez"]),
    ("clube", "Man. City", "MANCHESTER CITY", "joga no Manchester City", (90, 160, 215), ((108, 171, 221), (28, 44, 91)),
     ["Haaland", "Bellingham", "Pedri", "Dembélé"]),
    ("clube", "PSG", "PSG", "joga no Paris Saint-Germain", (0, 65, 112), ((0, 65, 112), (150, 20, 40)),
     ["Pedri", "Vinícius Jr", "Messi", "Dembélé"]),
    ("selecao", "pt", "PORTUGAL", "é da seleção de Portugal", (200, 30, 45), ((0, 120, 60), (170, 20, 40)),
     ["Kane", "Bruno Fernandes", "Modric", "Son"]),
    ("clube", "Inter Miami", "INTER MIAMI", "joga no Inter Miami", (235, 110, 165), ((240, 140, 180), (35, 31, 32)),
     ["Cristiano Ronaldo", "Messi", "Mbappé", "Lewandowski"]),
    ("clube", "Al-Nassr", "AL-NASSR", "joga no Al Nassr", (0, 50, 140), ((230, 180, 0), (0, 40, 120)),
     ["Salah", "Raphinha", "Cristiano Ronaldo", "Bellingham"]),
]
N = len(PERG)
COR_TIME = {"Barcelona": (165, 0, 68), "Real Madrid": (205, 160, 20), "Man. City": (90, 160, 215),
            "PSG": (0, 65, 112), "Inter Miami": (235, 110, 165), "Al-Nassr": (0, 50, 140), "Liverpool": (200, 16, 46),
            "Inter de Milão": (0, 80, 160), "Bayern": (220, 5, 45), "Milan": (190, 20, 30), "LAFC": (30, 30, 30),
            "Man. United": (210, 20, 30)}
FALAS = {
    "gancho": "Só craque acerta as oito! Qual desses joga no time, ou na seleção? Valendo!",
    "final": "Quantas você acertou? Comenta aí, e segue o Quiz Palito pra mais desafios!",
}
CW, CH = 380, 400
COLS = (285, 735)
ROWS = (790, 1215)  # centro das linhas
BAR = (95, 1440, 925, 1488)


def certo(p):
    k = 1 if p[0] == "clube" else 0
    ok = [i for i, n in enumerate(p[6]) if JOG[n][k] == p[1]]
    assert len(ok) == 1, (p[2], ok)
    return ok[0]


def textos():
    t = dict(FALAS)
    for k, p in enumerate(PERG, 1):
        t[f"q{k}"] = f"Qual desses {p[3]}?"
        t[f"a{k}"] = f"Acertou quem disse {p[6][certo(p)]}!"
    return t


def vozes():
    import edge_tts
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    for k, txt in textos().items():
        if not os.path.exists(A(f"{k}.mp3")):
            asyncio.run(edge_tts.Communicate(txt, "pt-BR-AntonioNeural", rate="+20%", pitch="+2Hz").save(A(f"{k}.mp3")))
            print("voz", k, "-", txt, flush=True)


_cache = {}


def bandeira(code, w, h):
    key = (code, w, h)
    if key not in _cache:
        fl = Image.open(os.path.join(HERE, "bandeiras", f"{code}.png")).convert("RGB")
        r = min(w / fl.width, h / fl.height)
        _cache[key] = fl.resize((int(fl.width * r), int(fl.height * r)), Image.LANCZOS)
    return _cache[key]


def foto(nome, w, h):
    key = ("foto", nome, w, h)
    if key not in _cache:
        import re, unicodedata
        slug = lambda s_: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s_).encode("ascii", "ignore")
                                 .decode().lower()).strip("-")
        p = os.path.join(HERE, "fotos", slug(nome) + ".jpg")
        if not os.path.exists(p):  # foto ainda não baixada
            return Image.new("RGB", (w, h), (170, 178, 198))
        im = Image.open(p).convert("RGB")
        # recorte mais para cima, onde fica o rosto
        fx, fy, z = ZOOM.get(nome, (0.5, 0.5, 1.0))
        big = ImageOps.fit(im, (int(w * z), int(h * z)), Image.LANCZOS, centering=(0.5, 0.2))
        # janela w x h centrada no rosto (fx, fy em fração do recorte inicial)
        x = min(max(0, int(fx * big.width - w / 2)), big.width - w)
        y = min(max(0, int(fy * big.height - h / 2)), big.height - h)
        _cache[key] = big.crop((x, y, x + w, y + h))
    return _cache[key]


def mascara(w, h):
    key = ("mask", w, h)
    if key not in _cache:
        m = Image.new("L", (w, h), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 24, fill=255)
        _cache[key] = m
    return _cache[key]


# zoom no rosto: (x, y do rosto no recorte normal, aumento)
ZOOM = {"Haaland": (0.51, 0.22, 2.4), "Bellingham": (0.5, 0.22, 2.6), "Dembélé": (0.465, 0.27, 4.0),
        "Modric": (0.5, 0.36, 3.2), "Raphinha": (0.5, 0.3, 1.5), "Salah": (0.62, 0.35, 1.4),
        "Lautaro Martínez": (0.5, 0.32, 1.8), "Messi": (0.5, 0.38, 1.25), "Bruno Fernandes": (0.5, 0.33, 1.7),
        "Lewandowski": (0.72, 0.22, 1.9), "Vinícius Jr": (0.45, 0.5, 1.25)}


def carta(img, cx, cy, letra, nome, estado=None, mostra_time=False, tipo="clube"):
    """estado: None, 'sim' ou 'nao'."""
    x0, y0 = cx - CW // 2, cy - CH // 2
    if estado == "sim":
        glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(glow).rounded_rectangle([x0 - 26, y0 - 26, x0 + CW + 26, y0 + CH + 26], 50, fill=(255, 240, 120, 200))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(20)))
    borda = (60, 210, 90) if estado == "sim" else b.NAVY
    b.shadowed_round_rect(img, (x0, y0, x0 + CW, y0 + CH), 36, b.WHITE)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x0 + CW, y0 + CH], 36, outline=borda, width=10 if estado == "sim" else 6)
    # foto do jogador (recorte no rosto) com cantos arredondados
    px0, py0, pw, ph = x0 + 16, y0 + 16, CW - 32, 244
    img.paste(foto(nome, pw, ph), (px0, py0), mascara(pw, ph))
    d = ImageDraw.Draw(img)
    # nome
    f = b.font(b.F_BLACK, 50)
    txt = nome.upper()
    while d.textlength(txt, font=f) > CW - 40 and f.size > 26:
        f = b.font(b.F_BLACK, f.size - 2)
    d.text((cx, y0 + 290), txt, font=f, fill=b.NAVY, anchor="mm")
    # time (na revelação)
    if mostra_time:
        time = JOG[nome][1] if tipo == "clube" else PAIS[JOG[nome][0]]
        ft = b.font(b.F_BLACK, 36)
        tw = d.textlength(time.upper(), font=ft)
        d.rounded_rectangle([cx - tw / 2 - 22, y0 + 330, cx + tw / 2 + 22, y0 + 382], 26, fill=COR_TIME.get(time, b.NAVY),
                            outline=b.WHITE, width=4)
        d.text((cx, y0 + 356), time.upper(), font=ft, fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
    # letra
    d.ellipse([x0 - 18, y0 - 18, x0 + 62, y0 + 62], fill=b.YELLOW, outline=b.NAVY, width=5)
    d.text((x0 + 22, y0 + 20), letra, font=b.font(b.F_BLACK, 46), fill=b.NAVY, anchor="mm")
    if estado == "nao":  # apaga a carta errada
        sombra = Image.new("RGBA", (CW, CH), (20, 30, 60, 150))
        m = Image.new("L", (CW, CH), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, CW - 1, CH - 1], 36, fill=150)
        sombra.putalpha(m)
        img.alpha_composite(sombra, (x0, y0))
        d = ImageDraw.Draw(img)
        if mostra_time:  # mantém o time legível por cima
            time = JOG[nome][1] if tipo == "clube" else PAIS[JOG[nome][0]]
            ft = b.font(b.F_BLACK, 36)
            tw = d.textlength(time.upper(), font=ft)
            d.rounded_rectangle([cx - tw / 2 - 22, y0 + 330, cx + tw / 2 + 22, y0 + 382], 26,
                                fill=COR_TIME.get(time, b.NAVY), outline=b.WHITE, width=4)
            d.text((cx, y0 + 356), time.upper(), font=ft, fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
    if estado == "sim":
        d.ellipse([x0 + CW - 70, y0 - 24, x0 + CW + 24, y0 + 70], fill=(60, 200, 90), outline=b.WHITE, width=6)
        d.line([(x0 + CW - 43, y0 + 24), (x0 + CW - 27, y0 + 42), (x0 + CW + 2, y0 + 4)], fill=b.WHITE, width=11)


def topo(img, k, p):
    d = ImageDraw.Draw(img)
    s.texto(d, (620, 225), "QUAL DESSES", 84, b.WHITE, max_w=720)
    s.texto(d, (620, 315), "JOGA NO..." if p[0] == "clube" else "É DA SELEÇÃO...", 84, b.WHITE, max_w=720)
    if p[0] == "selecao":  # bandeira do país na pergunta, ao lado do nome
        fl = bandeira(p[1], 132, 88)
        f = b.font(b.F_BLACK, 72)
        tw = d.textlength(p[2], font=f)
        larg = fl.width + 26 + tw
        x0 = 540 - larg / 2
        d.rounded_rectangle([x0 - 44, 435 - 62, x0 + larg + 44, 435 + 62], 62, fill=p[4], outline=b.WHITE, width=6)
        fy = 435 - fl.height // 2
        d.rounded_rectangle([x0 - 4, fy - 4, x0 + fl.width + 4, fy + fl.height + 4], 8, fill=b.WHITE)
        img.paste(fl, (int(x0), fy))
        d.text((x0 + fl.width + 26 + tw / 2, 435), p[2], font=f, fill=b.WHITE, anchor="mm", stroke_width=3,
               stroke_fill=b.NAVY)
    else:
        s.pilula(d, 540, 435, p[2], p[4], size=72, pad=50, h=118)
    d = ImageDraw.Draw(img)
    d.text((540, 527), f"{k}/{N}  •  TEMPORADA 2025/26", font=b.font(b.F_BLACK, 34), fill=b.WHITE, anchor="mm",
           stroke_width=4, stroke_fill=b.NAVY)


def base_pergunta(k, p, revela=False):
    img = s.fundo(*p[5], seed=k).convert("RGBA")
    topo(img, k, p)
    c = certo(p)
    for i, nome in enumerate(p[6]):
        est = None if not revela else ("sim" if i == c else "nao")
        carta(img, COLS[i % 2], ROWS[i // 2], "ABCD"[i], nome, est, revela, p[0])
    b.selo(img, 540, 1555, 0.7)
    return img


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


def pergunta_frames(k, p, fala):
    base = base_pergunta(k, p)
    total = fala + COUNT
    for i in range(int(total * FPS)):
        t = i / FPS
        frac = 1.0 if t < fala else 1 - (t - fala) / COUNT
        img = base.copy()
        barra(img, frac)
        pose = "pensando" if frac > 0.3 else "assustado"
        b.put_palito(img, pose, 270, 165, 375, int(6 * math.sin(t * (5 if pose == "pensando" else 16))))
        yield img.convert("RGB")


def resposta_frames(k, p, dur):
    base = base_pergunta(k, p, revela=True)
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = base.copy()
        sl = min(1.0, t / 0.3)
        b.put_palito(img, "comemorando", 270, 165, 375, int((1 - sl) * 120 + 6 * math.sin(t * 9)))
        yield img.convert("RGB")


def gancho_base():
    img = s.gradient(b.TEAL, b.BLUE).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([80, 230, 1000, 400], 60, fill=b.RED, outline=b.WHITE, width=10)
    s.texto(d, (540, 315), "SÓ CRAQUE ACERTA AS 8!", 78, b.WHITE, max_w=860)
    s.texto(d, (540, 520), "QUAL DESSES", 120, b.WHITE)
    s.texto(d, (540, 650), "JOGA ONDE?", 120, b.YELLOW)
    for i, code in enumerate(["br", "ar", "pt", "es"]):
        fl = bandeira(code, 200, 134)
        cx = 180 + i * 240
        b.shadowed_round_rect(img, (cx - fl.width // 2 - 12, 860 - 12 - fl.height // 2, cx + fl.width // 2 + 12,
                                    860 + 12 + fl.height // 2), 16, b.WHITE)
        img.paste(fl, (cx - fl.width // 2, 860 - fl.height // 2))
    d = ImageDraw.Draw(img)
    s.texto(d, (540, 1030), "CLUBES E SELEÇÕES  •  2025/26", 46, b.WHITE)
    b.put_palito(img, "assustado", 400, 540, 1500)
    b.selo(img, 540, 1550, 0.8)
    return img.convert("RGB")


def final_base():
    img = s.fundo(seed=3).convert("RGBA")
    d = ImageDraw.Draw(img)
    s.texto(d, (540, 330), "QUANTAS VOCÊ", 110, b.WHITE)
    s.texto(d, (540, 460), "ACERTOU?", 150, b.YELLOW)
    d.rounded_rectangle([170, 590, 910, 730], 50, fill=b.RED, outline=b.WHITE, width=8)
    s.texto(d, (540, 660), "COMENTA AÍ!", 84, b.WHITE)
    s.texto(d, (540, 860), "SEGUE O", 70, b.WHITE)
    b.selo(img, 540, 980, 1.3)
    b.put_palito(img, "apontando", 380, 540, 1520)
    return img.convert("RGB")


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    ims = [gancho_base()]
    fr = list(pergunta_frames(1, PERG[0], 0.5))
    fr3 = list(pergunta_frames(3, PERG[2], 0.5))
    ims += [fr[int(2.5 * FPS)], list(resposta_frames(1, PERG[0], 0.6))[-1],
            fr3[int(2.5 * FPS)], list(resposta_frames(3, PERG[2], 0.6))[-1], final_base()]
    for i, im in enumerate(ims):
        im.save(os.path.join(out, f"{i}.jpg"), quality=88)
    sheet = Image.new("RGB", (len(ims) * 370, 640), (25, 25, 25))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((360, 640)), (i * 370, 0))
    sheet.save(os.path.join(out, "prancha.jpg"), quality=85)
    print(out)


# ---------- versão TikTok: mais movimento (cartas entrando, balançando, zoom lento, selo só no começo/fim) ----------
SAIDA_TK = os.path.join(HERE, "short-qual-joga-1-tiktok.mp4")
SP = 60  # margem do sprite da carta (para o brilho)


def sprite(k, i, nome, est, revela, tipo):
    key = ("sprite", k, i, est, revela)
    if key not in _cache:
        cv = Image.new("RGBA", (CW + 2 * SP, CH + 2 * SP), (0, 0, 0, 0))
        carta(cv, cv.width // 2, cv.height // 2, "ABCD"[i], nome, est, revela, tipo)
        _cache[key] = cv
    return _cache[key]


def base_tk(k, p):
    key = ("base_tk", k)
    if key not in _cache:
        img = s.fundo(*p[5], seed=k).convert("RGBA")
        topo(img, k, p)
        _cache[key] = img
    return _cache[key].copy()


def colar(img, spr, cx, cy, sc):
    if sc <= 0.02:
        return
    w, h = max(1, int(spr.width * sc)), max(1, int(spr.height * sc))
    im = spr if sc == 1 else spr.resize((w, h), Image.BILINEAR)
    img.alpha_composite(im, (int(cx - w / 2), int(cy - h / 2)))


def zoom(img, z):
    if abs(z - 1) < 1e-3:
        return img
    w, h = img.size
    cw, ch = w / z, h / z
    x0, y0 = (w - cw) / 2, (h - ch) / 2
    return img.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))


def pula(x):  # 0 -> 1 com um pequeno "estouro" (ease-out-back)
    x = min(max(x, 0.0), 1.0)
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def pergunta_tk(k, p, fala):
    total = fala + COUNT
    for n in range(int(total * FPS)):
        t = n / FPS
        frac = 1.0 if t < fala else 1 - (t - fala) / COUNT
        img = base_tk(k, p)
        for i, nome in enumerate(p[6]):
            ent = pula((t - 0.05 - 0.13 * i) / 0.38)
            dy = 7 * math.sin(2 * math.pi * 0.6 * t + i * 1.3)
            treme = 4 * math.sin(t * 40 + i) if frac < 0.3 else 0  # tremidinha no fim do tempo
            colar(img, sprite(k, i, nome, None, False, p[0]), COLS[i % 2] + treme, ROWS[i // 2] + dy, ent)
        barra(img, frac)
        pose = "pensando" if frac > 0.3 else "assustado"
        b.put_palito(img, pose, 270, 165, 375, int(6 * math.sin(t * (5 if pose == "pensando" else 16))))
        yield zoom(img, 1.0 + 0.035 * t / total).convert("RGB")


def resposta_tk(k, p, dur):
    c = certo(p)
    for n in range(int(dur * FPS)):
        t = n / FPS
        img = base_tk(k, p)
        for i, nome in enumerate(p[6]):
            est = "sim" if i == c else "nao"
            if i == c:
                sc = 1.0 + 0.16 * math.sin(min(t / 0.4, 1.0) * math.pi) + 0.05 * min(t / 0.4, 1.0)
            else:
                sc = 1.0 - 0.06 * min(t / 0.25, 1.0)
            colar(img, sprite(k, i, nome, est, True, p[0]), COLS[i % 2], ROWS[i // 2], sc)
        sl = min(1.0, t / 0.3)
        b.put_palito(img, "comemorando", 270, 165, 375, int((1 - sl) * 120 + 6 * math.sin(t * 9)))
        yield zoom(img, 1.035 + 0.02 * t / dur).convert("RGB")


def gancho_tk(dur):
    base = gancho_base()
    for n in range(int(dur * FPS)):
        t = n / FPS
        z = 1.0 + 0.14 * (1 - pula(t / 0.5)) + 0.015 * math.sin(t * 6)
        yield zoom(base, max(1.0, z))


def final_tk(dur):
    base = final_base()
    for n in range(int(dur * FPS)):
        t = n / FPS
        yield zoom(base, 1.0 + 0.05 * t / dur)


def main_tiktok():
    vozes()
    tmp = tempfile.mkdtemp(prefix="short_joga_tk_")
    sfx = b.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = s.Timeline(video)
    tl.sound(A("gancho.mp3"), at=0.1, voz=True)
    for f in gancho_tk(s.duracao(A("gancho.mp3")) + 0.3):
        tl.frame(f)
    for k, p in enumerate(PERG, 1):
        q = A(f"q{k}.mp3")
        tl.sound(sfx["whoosh"], vol=0.6)
        tl.sound(q, at=tl.t + 0.1, voz=True)
        fala = s.duracao(q) + 0.2
        for n in range(int(COUNT)):
            tl.sound(sfx["tick"], at=tl.t + fala + n, vol=0.8)
        for f in pergunta_tk(k, p, fala):
            tl.frame(f)
        a = A(f"a{k}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(a, at=tl.t + 0.15, voz=True)
        for f in resposta_tk(k, p, s.duracao(a) + 0.6):
            tl.frame(f)
        print(f"{k}/{N}", flush=True)
    tl.sound(sfx["whoosh"])
    tl.sound(A("final.mp3"), at=tl.t + 0.2, voz=True)
    for f in final_tk(s.duracao(A("final.mp3")) + 0.7):
        tl.frame(f)
    tl.close()
    s.mixar(tl, video, MUSICA, SAIDA_TK)
    print(f"OK {SAIDA_TK} ({tl.t:.1f}s)")


def main():
    vozes()
    tmp = tempfile.mkdtemp(prefix="short_joga_")
    sfx = b.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = s.Timeline(video)
    tl.sound(A("gancho.mp3"), at=0.1, voz=True)
    tl.hold(gancho_base(), s.duracao(A("gancho.mp3")) + 0.3)
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
        for f in resposta_frames(k, p, s.duracao(a) + 0.6):
            tl.frame(f)
    tl.sound(sfx["whoosh"])
    tl.sound(A("final.mp3"), at=tl.t + 0.2, voz=True)
    tl.hold(final_base(), s.duracao(A("final.mp3")) + 0.7)
    tl.close()
    s.mixar(tl, video, MUSICA, SAIDA)
    print(f"OK {SAIDA} ({tl.t:.1f}s)")


if __name__ == "__main__":
    if "--previa-tiktok" in sys.argv:  # tira alguns quadros da versão TikTok para conferir o movimento
        out = os.path.join(HERE, "previa")
        os.makedirs(out, exist_ok=True)
        fr = list(pergunta_tk(1, PERG[0], 2.0))
        rs = list(resposta_tk(1, PERG[0], 1.5))
        ims = [list(gancho_tk(1.0))[3], fr[6], fr[14], fr[40], fr[-3], rs[6], rs[-1]]
        sheet = Image.new("RGB", (len(ims) * 370, 640), (25, 25, 25))
        for i, im in enumerate(ims):
            sheet.paste(im.convert("RGB").resize((360, 640)), (i * 370, 0))
        sheet.save(os.path.join(out, "prancha-tiktok.jpg"), quality=85)
        print(out)
    elif "--tiktok" in sys.argv:
        main_tiktok()
    elif "--previa" in sys.argv:
        previa()
    elif "--parado" in sys.argv:  # versão antiga, telas paradas (o TikTok marcou como baixa qualidade)
        main()
    else:  # padrão: versão com movimento, serve para TikTok e YouTube Shorts
        main_tiktok()
