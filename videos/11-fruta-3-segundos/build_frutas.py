"""Quiz Palito — "ADIVINHE A FRUTA EM 3 SEGUNDOS" (33 frutas e legumes, ritmo rápido).

Cada item: cartão gigante com a fruta/legume (emoji grande com borda de adesivo) + 3 s de barra
-> o nome aparece numa etiqueta verde e o narrador fala. Sem alternativas, sem explicação.
Placar a cada 10. Reaproveita 05-nao-diga-o-mesmo (fundo, raios, emoji, mixagem) e 01 (Palito, sons, Timeline).
Uso: py -3 build_frutas.py            (monta quiz-palito-fruta-3-segundos.mp4)
     py -3 build_frutas.py --previa   (só salva a prancha de prévia em previa/)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "05-nao-diga-o-mesmo"))
import build_naodiga as nd
from build_naodiga import b

W, H, FPS = b.W, b.H, b.FPS
R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-fruta-3-segundos.mp4")
EMOJI_TTF = "C:/Windows/Fonts/seguiemj.ttf"

COUNT = 3.0
CX, CY, CARD = 800, 575, 600        # centro e lado do cartão
VERDE = (30, 175, 80)
PAL_CX, PAL_BASE, PAL_H = 1670, 1055, 600
CORES = [((255, 150, 0), (200, 60, 0)), ((40, 170, 90), (10, 90, 60)), ((230, 60, 90), (130, 20, 60)),
         ((30, 120, 220), (15, 45, 140)), ((150, 70, 200), (60, 25, 120)), ((0, 160, 170), (0, 80, 100))]
_cache = {}  # só sprites de tamanho fixo


def emoji_grande(ch, size):
    """Emoji nítido em tamanho grande (Segoe é vetorial; a Noto da nuvem só tem 109 px e é ampliada)."""
    k = ("eg", ch, size)
    if k in _cache:
        return _cache[k]
    try:
        f, px = ImageFont.truetype(EMOJI_TTF, 300), 300
    except OSError:
        f, px = ImageFont.truetype(EMOJI_TTF, 109), 109
    im = Image.new("RGBA", (px * 3, px * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((px * 1.5, px), ch, font=f, embedded_color=True, anchor="mm")
    im = im.crop(im.getbbox())
    r = size / max(im.size)
    im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
    # borda branca de adesivo + sombra
    m = 30
    a = Image.new("L", (im.width + 2 * m, im.height + 2 * m), 0)
    a.paste(im.getchannel("A"), (m, m))
    borda = a.filter(ImageFilter.MaxFilter(25)).point(lambda v: 255 if v > 40 else 0)
    out = Image.new("RGBA", a.size, (0, 0, 0, 0))
    sh = Image.new("RGBA", a.size, (0, 0, 0, 0))
    sh.putalpha(borda.filter(ImageFilter.GaussianBlur(10)).point(lambda v: v * 0.45))
    out.alpha_composite(sh, (0, 0))
    out.paste(Image.new("RGBA", a.size, (255, 255, 255, 255)), (0, 0), borda)
    out.alpha_composite(im, (m, m))
    _cache[k] = out
    return out


def fundo(n):
    c1, c2 = CORES[n % len(CORES)]
    img = b.gradient(c1, c2)
    img.paste(Image.new("RGB", (W, H), (255, 255, 255)), (0, 0), nd._mask())
    return img.convert("RGBA")


def pergunta_txt(r):
    return {"fruta": "QUE FRUTA É ESSA?", "legume": "QUE LEGUME É ESSE?"}.get(r["tipo"], "O QUE É ISSO?")


def topo(img, r):
    d = ImageDraw.Draw(img)
    d.ellipse([40, 30, 190, 180], fill=b.ORANGE, outline=b.WHITE, width=8)
    d.text((115, 103), f"{r['n']:02d}", font=b.font(b.F_BLACK, 70), fill=b.WHITE, anchor="mm", stroke_width=3,
           stroke_fill=b.NAVY)
    t = pergunta_txt(r)
    b.text_outline(d, (800, 105), t, nd.fit(d, t, 96, 1050), b.YELLOW, w=10)
    b.selo(img, 1730, 105, 0.7)


def cartao_sprite(r):
    k = ("cartao", r["n"])
    if k in _cache:
        return _cache[k]
    m = 30
    sp = Image.new("RGBA", (CARD + 2 * m, CARD + 2 * m), (0, 0, 0, 0))
    sh = Image.new("RGBA", sp.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([m, m + 14, m + CARD, m + CARD + 14], 60, fill=(0, 0, 40, 110))
    sp.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(sp)
    d.rounded_rectangle([m, m, m + CARD, m + CARD], 60, fill=b.WHITE, outline=b.NAVY, width=8)
    e = emoji_grande(r["emoji"], 430)
    sp.alpha_composite(e, (int(m + (CARD - e.width) / 2), int(m + (CARD - e.height) / 2)))
    _cache[k] = sp
    return sp


def etiqueta_sprite(nome):
    k = ("etq", nome)
    if k in _cache:
        return _cache[k]
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    f = nd.fit(d0, nome.upper(), 90, 820)
    w = int(d0.textlength(nome.upper(), font=f)) + 140
    h = 140
    sp = Image.new("RGBA", (w + 30, h + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(sp)
    d.rounded_rectangle([19, 25, 15 + w, 25 + h], 60, fill=(0, 0, 0, 100))
    d.rounded_rectangle([15, 15, 15 + w, 15 + h], 60, fill=VERDE, outline=b.WHITE, width=8)
    d.text((15 + w / 2, 15 + h / 2 + 3), nome.upper(), font=f, fill=b.WHITE, anchor="mm", stroke_width=4,
           stroke_fill=b.NAVY)
    _cache[k] = sp
    return sp


def barra(img, frac):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = nd.BAR
    d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 32, fill=b.WHITE)
    d.rounded_rectangle(nd.BAR, 24, fill=(60, 70, 110))
    if frac > 0.002:
        xe = x0 + (x1 - x0) * frac
        d.rounded_rectangle([x0, y0, max(xe, x0 + 48), y1], 24, fill=b.ORANGE if frac > 0.34 else b.RED)
    s = math.ceil(frac * COUNT)
    if s > 0:
        d.text(((x0 + x1) // 2, (y0 + y1) // 2), str(s), font=b.font(b.F_BLACK, 40), fill=b.WHITE, anchor="mm",
               stroke_width=4, stroke_fill=b.NAVY)


def base(r):
    k = ("base", r["n"])
    if k not in _cache:
        img = fundo(r["n"])
        topo(img, r)
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


def pergunta_frames(r):
    """Cartão entra com pulinho e a barra de 3 s corre."""
    card = cartao_sprite(r)
    n = int(COUNT * FPS)
    for i in range(n):
        t = i / FPS
        frac = 1 - i / n
        img = base(r)
        colar(img, card, CX, CY + 5 * math.sin(t * 2.5), pula(t / 0.35))
        barra(img, frac)
        pose = "pensando" if frac > 0.34 else "assustado"
        b.put_palito(img, pose, PAL_H, PAL_CX, PAL_BASE + int(max(0, 1 - t / 0.3) * 500) if r["n"] == 1 else PAL_BASE,
                     int(7 * math.sin(t * (5 if pose == "pensando" else 18))))
        yield img.convert("RGB")


def revela_frames(r, dur):
    card = cartao_sprite(r)
    etq = etiqueta_sprite(r["nome"])
    for i in range(int(dur * FPS)):
        tt = i / FPS
        img = base(r)
        colar(img, card, CX, CY, 1.0 + 0.03 * math.sin(min(tt / 0.3, 1) * math.pi))
        colar(img, etq, CX, 905, pula(tt / 0.3))
        if tt < 0.2:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(140 * (1 - tt / 0.2)))))
        b.put_palito(img, "comemorando", PAL_H, PAL_CX, PAL_BASE, -int(abs(28 * math.sin(tt * 7))))
        yield img.convert("RGB")


def placar_frames(n, dur):
    c1, c2 = (255, 170, 0), (215, 100, 0)
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = nd.burst(c1, c2, t * 12).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.3)
        b.text_outline(d, (800, 230), f"{n} JÁ FORAM!", b.font(b.F_BLACK, int(110 * (0.5 + 0.5 * s))), b.WHITE, w=11)
        b.text_outline(d, (800, 420), "QUANTAS VOCÊ", b.font(b.F_BLACK, int(140 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
        b.text_outline(d, (800, 580), "ACERTOU?", b.font(b.F_BLACK, int(140 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
        if s >= 1:
            d.rounded_rectangle([420, 680, 1180, 800], 60, fill=(255, 255, 255, 240), outline=b.NAVY, width=7)
            d.text((800, 740), f"__ / {n}", font=b.font(b.F_BLACK, 80), fill=b.NAVY, anchor="mm")
        b.selo(img, 800, 910, 1.1)
        b.put_palito(img, "apontando", 620, 1620 + int((1 - s) * 700), 1060, int(6 * math.sin(t * 5)))
        yield img.convert("RGB")


def intro_base():
    img = fundo(0)
    b.selo(img, 800, 80, 1.0)
    d = ImageDraw.Draw(img)
    b.text_outline(d, (800, 240), "ADIVINHE A FRUTA", nd.fit(d, "ADIVINHE A FRUTA", 130, 1400), b.WHITE, w=13)
    b.text_outline(d, (800, 410), "EM 3 SEGUNDOS!", nd.fit(d, "EM 3 SEGUNDOS!", 160, 1400), b.YELLOW, w=16)
    for k, ch in enumerate(["🍓", "🥕", "🍍", "🥦", "🍉"]):
        e = emoji_grande(ch, 170)
        img.alpha_composite(e, (int(260 + k * 270 - e.width / 2), int(600 - e.height / 2)))
    passos = [(str(TOTAL), "FRUTAS E LEGUMES"), ("3", "SEGUNDOS PARA CADA UM")]
    d = ImageDraw.Draw(img)
    for k, (num, t) in enumerate(passos):
        y = 800 + k * 135
        d.ellipse([170, y - 55, 280, y + 55], fill=b.ORANGE, outline=b.WHITE, width=6)
        d.text((225, y), num, font=b.font(b.F_BLACK, 58), fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
        b.text_outline(d, (315, y), t, b.font(b.F_BLACK, 64), b.WHITE, w=8, anchor="lm")
    return img


def outro_base():
    img = fundo(3)
    d = ImageDraw.Draw(img)
    b.text_outline(d, (800, 200), "QUANTAS VOCÊ", b.font(b.F_BLACK, 120), b.WHITE, w=12)
    b.text_outline(d, (800, 345), "ACERTOU?", b.font(b.F_BLACK, 150), b.YELLOW, w=15)
    d.rounded_rectangle([450, 430, 1150, 545], 55, fill=(255, 255, 255, 240), outline=b.NAVY, width=7)
    d.text((800, 488), f"__ / {TOTAL}", font=b.font(b.F_BLACK, 80), fill=b.NAVY, anchor="mm")
    d.rounded_rectangle([290, 590, 1310, 710], 55, fill=b.RED, outline=b.WHITE, width=8)
    d.text((800, 650), "COMENTA SUA NOTA!", font=b.font(b.F_BLACK, 64), fill=b.WHITE, anchor="mm",
           stroke_width=3, stroke_fill=b.NAVY)
    b.text_outline(d, (800, 790), "MARCA UM AMIGO E INSCREVA-SE NO", b.font(b.F_BLACK, 54), b.WHITE, w=7)
    b.selo(img, 800, 910, 1.3)
    return img


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    quadros = [next(nd.anima(intro_base(), "acenando", 0.1))]
    for r in (R[0], R[7], R[21], R[29]):
        quadros.append(list(pergunta_frames(r))[int(COUNT * FPS * 0.5)])
        quadros.append(list(revela_frames(r, 1.0))[-1])
    quadros.append(list(placar_frames(10, 0.5))[-1])
    quadros.append(next(nd.anima(outro_base(), "acenando", 0.1)))
    for i, q in enumerate(quadros):
        q.save(os.path.join(out, f"q{i:02d}.jpg"), quality=88)
    cols = 3
    th = [q.resize((640, 360), Image.LANCZOS) for q in quadros]
    pr = Image.new("RGB", (cols * 650, math.ceil(len(th) / cols) * 370), "black")
    for i, q in enumerate(th):
        pr.paste(q, ((i % cols) * 650, (i // cols) * 370))
    pr.save(os.path.join(out, "prancha.jpg"), quality=88)
    print(out)


def main():
    tmp = tempfile.mkdtemp(prefix="quiz_frutas_")
    sfx = b.make_sfx(tmp)
    dur = lambda p: b.duration(p) if os.path.exists(p) else 1.2
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    marcas = {}
    tl.sound(A("intro.mp3"), at=0.3)
    for f in nd.anima(intro_base(), "acenando", dur(A("intro.mp3")) + 0.8):
        tl.frame(f)
    for r in R:
        n = r["n"]
        if n % 10 == 1:
            marcas[str(n)] = tl.t
        tl.sound(sfx["whoosh"], vol=0.6)
        for s in range(int(COUNT)):
            tl.sound(sfx["tick"], at=tl.t + s, vol=0.8)
        for f in pergunta_frames(r):
            tl.frame(f)
        p = A(f"p{n}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(p, at=tl.t + 0.2)
        for f in revela_frames(r, max(1.6, dur(p) + 0.5)):
            tl.frame(f)
        if n % 10 == 0 and n < TOTAL:
            v = A(f"placar{n}.mp3")
            tl.sound(sfx["whoosh"])
            tl.sound(v, at=tl.t + 0.3)
            for f in placar_frames(n, dur(v) + 0.8):
                tl.frame(f)
            print(f"{n}/{TOTAL} ({tl.t / 60:.1f} min)", flush=True)
    marcas["final"] = tl.t
    tl.sound(sfx["whoosh"])
    tl.sound(A("outro.mp3"), at=tl.t + 0.4)
    for f in nd.anima(outro_base(), "acenando", max(4.0, dur(A("outro.mp3")) + 1.8)):
        tl.frame(f)
    total = tl.t
    tl.close()
    json.dump(marcas, open(os.path.join(HERE, "tempos.json"), "w", encoding="utf-8"), indent=1)
    nd.HERE, nd.A, nd.SAIDA = HERE, A, SAIDA
    nd.mixar(tl, video, total)
    print(f"OK {SAIDA} ({total:.1f}s)")


if __name__ == "__main__":
    previa() if "--previa" in sys.argv else main()
