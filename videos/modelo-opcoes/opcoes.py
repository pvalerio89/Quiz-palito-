"""Quiz Palito — modelo de vídeo LONGO (16:9) com pergunta em formato de QUESTÃO: foto + opções A/B/C,
igual aos Shorts (pedido do Patrick, 2026-11-09).

Tela da pergunta: número + pergunta no topo, foto grande à esquerda, 3 opções empilhadas à direita,
Palito pensando no canto e a barra de tempo embaixo. Na resposta a opção certa fica verde com ✔,
as outras escurecem e o Palito comemora.

Uso num vídeo novo:
    sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes")); import opcoes as op
    op.FOTOS = os.path.join(HERE, "fotos")
    q = {"n": 1, "pergunta": "QUE LUGAR É ESSE?", "foto": "torre-eiffel.jpg",
         "opcoes": ["Big Ben", "Torre Eiffel", "Torre de Pisa"], "certa": 1}
    for f in op.pergunta_frames(q, total=60): tl.frame(f)
    for f in op.resposta_frames(q, dur, total=60): tl.frame(f)
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "05-nao-diga-o-mesmo"))
import build_naodiga as nd
from build_naodiga import b

W, H, FPS = b.W, b.H, b.FPS
FOTOS = HERE                       # pasta das fotos do vídeo (trocar no vídeo novo)
COUNT = 5.0                        # segundos para responder
VERDE = (60, 200, 90)
CORES = [((40, 170, 90), (10, 90, 60)), ((230, 60, 90), (130, 20, 60)), ((30, 120, 220), (15, 45, 140)),
         ((150, 70, 200), (60, 25, 120)), ((255, 150, 0), (200, 60, 0)), ((0, 160, 170), (0, 80, 100))]

# Posições (1920x1080)
CARD_C, CARD = (430, 545), 600      # centro e lado do cartão da foto
OPT_X, OPT_W, OPT_H = 1105, 700, 128
OPT_Y = (380, 545, 710)             # centro de cada opção
PAL_CX, PAL_BASE, PAL_H = 1700, 1000, 560
BAR = (130, 905, 1480, 950)
_cache = {}                         # só sprites de tamanho fixo


def fundo(n):
    c1, c2 = CORES[n % len(CORES)]
    img = b.gradient(c1, c2)
    img.paste(Image.new("RGB", (W, H), (255, 255, 255)), (0, 0), nd._mask())
    return img.convert("RGBA")


def foto(nome, size, filtro=None):
    k = ("foto", nome, size, filtro)
    if k in _cache:
        return _cache[k]
    im = Image.open(os.path.join(FOTOS, nome)).convert("RGB")
    im = ImageOps.fit(im, (size, size), Image.LANCZOS)
    if filtro == "amarela":
        im = ImageOps.colorize(im.convert("L"), black=(70, 45, 0), mid=(255, 205, 0), white=(255, 250, 200))
    im = im.convert("RGBA")
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1], int(size * 0.07), fill=255)
    im.putalpha(m)
    _cache[k] = im
    return im


def cartao_sprite(q, filtro=None):
    k = ("cartao", q["foto"], filtro)
    if k in _cache:
        return _cache[k]
    m = 30
    sp = Image.new("RGBA", (CARD + 2 * m, CARD + 2 * m), (0, 0, 0, 0))
    sh = Image.new("RGBA", sp.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([m, m + 14, m + CARD, m + CARD + 14], 50, fill=(0, 0, 40, 110))
    sp.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(sp).rounded_rectangle([m, m, m + CARD, m + CARD], 50, fill=b.WHITE, outline=b.NAVY, width=8)
    sp.alpha_composite(foto(q["foto"], CARD - 40, filtro), (m + 20, m + 20))
    _cache[k] = sp
    return sp


def opcao_sprite(i, txt, estado=None):
    """estado: None (normal), 'sim' (certa, verde com ✔) ou 'nao' (escurecida)."""
    k = ("op", i, txt, estado)
    if k in _cache:
        return _cache[k]
    cv = Image.new("RGBA", (OPT_W + 60, OPT_H + 60), (0, 0, 0, 0))
    x0, y0 = 30, 30
    if estado == "sim":
        glow = Image.new("RGBA", cv.size, (0, 0, 0, 0))
        ImageDraw.Draw(glow).rounded_rectangle([x0 - 18, y0 - 18, x0 + OPT_W + 18, y0 + OPT_H + 18], 70,
                                               fill=(255, 240, 120, 210))
        cv.alpha_composite(glow.filter(ImageFilter.GaussianBlur(14)))
    b.shadowed_round_rect(cv, (x0, y0, x0 + OPT_W, y0 + OPT_H), 64, VERDE if estado == "sim" else b.WHITE)
    d = ImageDraw.Draw(cv)
    d.rounded_rectangle([x0, y0, x0 + OPT_W, y0 + OPT_H], 64, outline=b.NAVY, width=7)
    d.ellipse([x0 + 14, y0 + 14, x0 + 114, y0 + 114], fill=b.WHITE if estado == "sim" else b.YELLOW,
              outline=b.NAVY, width=6)
    d.text((x0 + 64, y0 + 66), "ABC"[i], font=b.font(b.F_BLACK, 62), fill=b.NAVY, anchor="mm")
    t = txt.upper()
    fo = b.font(b.F_BLACK, 62)
    while d.textlength(t, font=fo) > OPT_W - 310 and fo.size > 34:
        fo = b.font(b.F_BLACK, fo.size - 2)
    sim = estado == "sim"
    d.text((x0 + OPT_W / 2 + 10, y0 + OPT_H / 2 + 2), t, font=fo, fill=b.WHITE if sim else b.NAVY, anchor="mm",
           stroke_width=4 if sim else 0, stroke_fill=b.NAVY)
    if sim:
        cx, cy = x0 + OPT_W - 66, y0 + OPT_H / 2
        d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], fill=b.WHITE, outline=b.NAVY, width=5)
        d.line([(cx - 21, cy), (cx - 5, cy + 17), (cx + 23, cy - 17)], fill=(40, 170, 70), width=11)
    if estado == "nao":
        sh = Image.new("RGBA", cv.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([x0, y0, x0 + OPT_W, y0 + OPT_H], 64, fill=(20, 30, 60, 150))
        cv.alpha_composite(sh)
    _cache[k] = cv
    return cv


def topo(img, q, total):
    d = ImageDraw.Draw(img)
    d.ellipse([40, 28, 190, 178], fill=b.ORANGE, outline=b.WHITE, width=8)
    d.text((115, 101), f"{q['n']:02d}", font=b.font(b.F_BLACK, 70), fill=b.WHITE, anchor="mm", stroke_width=3,
           stroke_fill=b.NAVY)
    t = q["pergunta"].upper()
    b.text_outline(d, (850, 92), t, nd.fit(d, t, 92, 1150), b.YELLOW, w=10)
    d.text((850, 168), f"PERGUNTA {q['n']} DE {total}", font=b.font(b.F_BLACK, 34), fill=b.WHITE, anchor="mm",
           stroke_width=4, stroke_fill=b.NAVY)
    b.selo(img, 1730, 100, 0.7)


def base(q, total):
    k = ("base", q["n"], total)
    if k not in _cache:
        img = fundo(q["n"])
        topo(img, q, total)
        _cache[k] = img
    return _cache[k].copy()


def colar(img, sp, cx, cy, sc=1.0):
    if sc <= 0.02:
        return
    if abs(sc - 1) > 1e-3:
        sp = sp.resize((max(1, int(sp.width * sc)), max(1, int(sp.height * sc))), Image.BILINEAR)
    img.alpha_composite(sp, (int(cx - sp.width / 2), int(cy - sp.height / 2)))


def pula(x):
    x = min(max(x, 0.0), 1.0)
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def barra(img, frac, count=COUNT):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = BAR
    d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 32, fill=b.WHITE)
    d.rounded_rectangle(BAR, 24, fill=(60, 70, 110))
    if frac > 0.002:
        xe = x0 + (x1 - x0) * frac
        d.rounded_rectangle([x0, y0, max(xe, x0 + 48), y1], 24, fill=b.ORANGE if frac > 0.34 else b.RED)
    s = math.ceil(frac * count)
    if s > 0:
        d.text(((x0 + x1) // 2, (y0 + y1) // 2), str(s), font=b.font(b.F_BLACK, 40), fill=b.WHITE, anchor="mm",
               stroke_width=4, stroke_fill=b.NAVY)


def pergunta_frames(q, total, count=COUNT, filtro=None):
    """Foto entra com pulinho, as opções entram uma a uma pela direita e a barra corre."""
    card = cartao_sprite(q, filtro)
    ops = [opcao_sprite(i, o) for i, o in enumerate(q["opcoes"])]
    n = int(count * FPS)
    for i in range(n):
        t = i / FPS
        frac = 1 - i / n
        img = base(q, total)
        colar(img, card, CARD_C[0], CARD_C[1] + 5 * math.sin(t * 2.5), pula(t / 0.35))
        for k, sp in enumerate(ops):
            a = min(max((t - 0.25 - 0.15 * k) / 0.3, 0.0), 1.0)
            if a > 0:
                colar(img, sp, OPT_X + (1 - pula(a)) * 300 if a < 1 else OPT_X, OPT_Y[k])
        barra(img, frac, count)
        pose = "pensando" if frac > 0.34 else "assustado"
        b.put_palito(img, pose, PAL_H, PAL_CX, PAL_BASE, int(7 * math.sin(t * (5 if pose == "pensando" else 18))))
        yield img.convert("RGB")


def resposta_frames(q, dur, total, filtro_antes=None):
    """A opção certa acende verde com ✔, as outras escurecem; foto volta à cor (se tinha filtro)."""
    am, cor = cartao_sprite(q, filtro_antes), cartao_sprite(q, None)
    ops = [opcao_sprite(i, o, "sim" if i == q["certa"] else "nao") for i, o in enumerate(q["opcoes"])]
    for i in range(int(dur * FPS)):
        tt = i / FPS
        img = base(q, total)
        a = min(1.0, tt / 0.45)
        card = cor if (a >= 1 or filtro_antes is None) else Image.blend(am, cor, a)
        colar(img, card, CARD_C[0], CARD_C[1])
        for k, sp in enumerate(ops):
            sc = 1.0 + (0.06 * math.sin(min(tt / 0.35, 1) * math.pi) if k == q["certa"] else 0)
            colar(img, sp, OPT_X, OPT_Y[k], sc)
        if tt < 0.2:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(120 * (1 - tt / 0.2)))))
        b.put_palito(img, "comemorando", PAL_H, PAL_CX, PAL_BASE, -int(abs(26 * math.sin(tt * 7))))
        yield img.convert("RGB")
