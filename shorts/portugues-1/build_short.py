"""Short — "Você passa no quiz de PORTUGUÊS do 5º ano?" (6 perguntas, 3 opções, padrão com movimento).

Perguntas próprias, ilustradas com emoji (fonte Segoe UI Emoji do Windows). Um arquivo só para TikTok e YouTube.
Uso: py -3 build_short.py            (gera vozes que faltam e monta o Short)
     py -3 build_short.py --previa   (prancha com quadros para conferir)
"""
import asyncio, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import short_base as s
from short_base import b, W, H, FPS

A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "short-portugues-1.mp4")
MUSICA = os.path.join(QP, "videos", "03-bandeiras-195", "assets", "musica.mp3")
EMOJI = "C:/Windows/Fonts/seguiemj.ttf"
COUNT = 5.0
N = 6

# pergunta (tela), fala, emoji, opções A-C, índice certo, resposta falada, fundo (topo, base)
PERG = [
    ("Qual é o plural de\n“PÃO”?", "Qual é o plural de pão?", "🍞", ["Pãos", "Pães", "Pãoes"], 1,
     "Pães!", ((0, 190, 200), (20, 70, 160))),
    ("Qual é o coletivo de\nLOBOS?", "Qual é o coletivo de lobos?", "🐺", ["Alcateia", "Cardume", "Enxame"], 0,
     "Alcateia!", ((150, 70, 200), (60, 25, 120))),
    ("Qual é o contrário de\n“ALEGRE”?", "Qual é o contrário de alegre?", "😄", ["Feliz", "Triste", "Contente"], 1,
     "Triste!", ((255, 170, 0), (210, 80, 0))),
    ("Qual é o feminino de\n“BODE”?", "Qual é o feminino de bode?", "🐐", ["Bodona", "Cabra", "Boda"], 1,
     "Cabra!", ((40, 190, 110), (10, 100, 80))),
    ("Quantas sílabas tem\n“BORBOLETA”?", "Quantas sílabas tem a palavra borboleta?", "🦋", ["3", "4", "5"], 1,
     "Quatro! Bor, bo, le, ta!", ((236, 64, 150), (130, 20, 90))),
    ("Qual está escrita\nCERTO?", "Agora a última! Só um por cento acerta! Qual está escrita certo?", "🦸",
     ["Heroi", "Herói", "Héroi"], 1, "Herói, com acento no o!", ((235, 60, 50), (120, 15, 30))),
]
FALAS = {
    "gancho": "Será que você passa no quiz de português do quinto ano? Valendo!",
    "final": "Quantas você acertou? Comenta aí, e segue o Quiz Palito pra mais desafios!",
}
CARD = (90, 330, 990, 950)          # cartão da pergunta
OPT_Y = (1065, 1210, 1355)          # centro das opções
OPT_W, OPT_H = 820, 120
BAR = (110, 1468, 970, 1514)


def textos():
    t = dict(FALAS)
    for k, p in enumerate(PERG, 1):
        t[f"q{k}"] = f"Pergunta {['um','dois','três','quatro','cinco','seis'][k-1]}! {p[1]}"
        t[f"a{k}"] = p[5]
    return t


def vozes():
    import edge_tts
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


def cartao_sprite(k, p):
    """Cartão branco com número, pergunta e emoji (imagem separada, para animar)."""
    key = ("cartao", k)
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
        em = emoji(p[2], 300)
        cv.alpha_composite(em, (int(30 + w / 2 - em.width / 2), int(30 + h - 40 - em.height)))
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
        d.text((x0 + OPT_W / 2 + 40, y0 + OPT_H / 2), txt, font=b.font(b.F_BLACK, 62),
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
    s.pilula(ImageDraw.Draw(img), 600, 205, "PORTUGUÊS • 5º ANO", (40, 60, 150), size=50, pad=40, h=96)
    d = ImageDraw.Draw(img)
    d.text((600, 270), f"PERGUNTA {k}/{N}", font=b.font(b.F_BLACK, 34), fill=b.WHITE, anchor="mm",
           stroke_width=4, stroke_fill=b.NAVY)


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


def pergunta_frames(k, p, fala):
    total = fala + COUNT
    for n in range(int(total * FPS)):
        t = n / FPS
        frac = 1.0 if t < fala else 1 - (t - fala) / COUNT
        img = base(k, p)
        colar(img, cartao_sprite(k, p), CCX, CCY + 5 * math.sin(t * 2.2), pula(t / 0.4))
        for i, op in enumerate(p[3]):
            ent = pula((t - 0.25 - 0.14 * i) / 0.35)
            dx = 4 * math.sin(t * 40 + i) if frac < 0.3 else 0
            colar(img, opcao_sprite(i, op), 540 + dx, OPT_Y[i] + 4 * math.sin(t * 3 + i), ent)
        barra(img, frac)
        pose = "pensando" if frac > 0.3 else "assustado"
        b.put_palito(img, pose, 240, 140, 300, int(6 * math.sin(t * (5 if pose == "pensando" else 16))))
        yield zoom(img, 1.0 + 0.03 * t / total).convert("RGB")


def resposta_frames(k, p, dur):
    for n in range(int(dur * FPS)):
        t = n / FPS
        img = base(k, p)
        colar(img, cartao_sprite(k, p), CCX, CCY, 1.0)
        for i, op in enumerate(p[3]):
            if i == p[4]:
                sc = 1.0 + 0.12 * math.sin(min(t / 0.4, 1.0) * math.pi) + 0.04 * min(t / 0.4, 1.0)
                colar(img, opcao_sprite(i, op, "sim"), 540, OPT_Y[i], sc)
            else:
                colar(img, opcao_sprite(i, op, "nao"), 540, OPT_Y[i], 1.0 - 0.05 * min(t / 0.25, 1.0))
        sl = min(1.0, t / 0.3)
        b.put_palito(img, "comemorando", 240, 140, 300, int((1 - sl) * 120 + 6 * math.sin(t * 9)))
        yield zoom(img, 1.03 + 0.02 * t / dur).convert("RGB")


def gancho_base():
    img = s.gradient((0, 190, 200), (20, 70, 160)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([90, 230, 990, 390], 60, fill=b.RED, outline=b.WHITE, width=10)
    s.texto(d, (540, 310), "SÓ 1% ACERTA TODAS!", 80, b.WHITE, max_w=840)
    s.texto(d, (540, 520), "VOCÊ PASSA NO", 100, b.WHITE)
    s.texto(d, (540, 650), "QUIZ DE PORTUGUÊS", 96, b.YELLOW)
    s.texto(d, (540, 780), "DO 5º ANO?", 110, b.WHITE)
    for i, ch in enumerate(["📚", "✏️", "🧠"]):
        em = emoji(ch, 170)
        img.alpha_composite(em, (int(250 + i * 290 - em.width / 2), int(980 - em.height / 2)))
    b.put_palito(img, "assustado", 380, 540, 1500)
    b.selo(img, 540, 1550, 0.8)
    return img


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
    return img


def gancho_frames(dur):
    bs = gancho_base()
    for n in range(int(dur * FPS)):
        t = n / FPS
        yield zoom(bs, max(1.0, 1.0 + 0.14 * (1 - pula(t / 0.5)) + 0.015 * math.sin(t * 6))).convert("RGB")


def final_frames(dur):
    bs = final_base()
    for n in range(int(dur * FPS)):
        yield zoom(bs, 1.0 + 0.05 * n / FPS / dur).convert("RGB")


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = list(pergunta_frames(1, PERG[0], 2.0))
    ims = [list(gancho_frames(1.0))[20], fr[8], fr[40], list(resposta_frames(1, PERG[0], 1.2))[-1],
           list(pergunta_frames(5, PERG[4], 1.0))[50], list(resposta_frames(6, PERG[5], 1.2))[-1],
           list(final_frames(1.0))[10]]
    sheet = Image.new("RGB", (len(ims) * 370, 640), (25, 25, 25))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((360, 640)), (i * 370, 0))
    sheet.save(os.path.join(out, "prancha.jpg"), quality=85)
    print(out)


def main():
    vozes()
    tmp = tempfile.mkdtemp(prefix="short_port_")
    sfx = b.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = s.Timeline(video)
    tl.sound(A("gancho.mp3"), at=0.1, voz=True)
    for f in gancho_frames(s.duracao(A("gancho.mp3")) + 0.3):
        tl.frame(f)
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
