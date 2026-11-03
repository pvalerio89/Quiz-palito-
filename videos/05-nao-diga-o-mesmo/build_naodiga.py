"""Quiz Palito — "NÃO DIGA O MESMO QUE O PALITO" (40 rodadas, 8 vidas).

Cada rodada: vinheta com o número -> cartão com o pedido + 6 s de barra com o Palito pensando
-> revelação da resposta do Palito (faixa amarela). Reaproveita quiz-paises/build.py (fontes, cores, Palito, sons).
Uso: py -3 build_naodiga.py            (monta quiz-palito-nao-diga-o-mesmo.mp4)
     py -3 build_naodiga.py --previa   (só salva a prancha de prévia em previa/)
"""
import json, math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(QP, "videos", "01-paises-sem-vogais"))
import build as b

b.PERSONAGEM = os.path.join(QP, "personagem")
W, H, FPS = b.W, b.H, b.FPS
R = json.load(open(os.path.join(HERE, "rodadas.json"), encoding="utf-8"))
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-nao-diga-o-mesmo.mp4")
TITULO = "NÃO DIGA O MESMO QUE O PALITO"

COUNT = 6.0
VINHETA = 1.0
CARD = (90, 230, 1400, 740)
FAIXA = (90, 775, 1400, 905)
BAR = (110, 945, 1380, 993)
VIDAS_BOX = (1450, 215, 1890, 345)
PAL_CX, PAL_BASE, PAL_H = 1670, 1055, 600
VERDE = (40, 190, 90)
CORES = [((236, 64, 150), (150, 30, 100)), ((40, 150, 230), (20, 60, 150)), ((255, 140, 0), (190, 70, 0)),
         ((40, 185, 110), (10, 100, 70)), ((150, 70, 200), (70, 30, 120)), ((235, 60, 50), (150, 20, 30)),
         ((0, 170, 180), (0, 90, 110)), ((90, 100, 230), (40, 40, 140)), ((230, 110, 40), (160, 40, 60)),
         ((60, 160, 70), (20, 80, 90))]

_sprites = {}   # só sprites de tamanho fixo
EMOJI = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", 109)


def emoji(ch, size):
    key = ("e", ch, size)
    if key not in _sprites:
        im = Image.new("RGBA", (300, 200), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((150, 100), ch, font=EMOJI, embedded_color=True, anchor="mm")
        im = im.crop(im.getbbox())
        r = size / max(im.size)
        _sprites[key] = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
    return _sprites[key]


def numero_sprite(txt, size):
    key = ("n", txt, size)
    if key not in _sprites:
        im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([4, 4, size - 4, size - 4], size // 5, fill=(40, 150, 230), outline=b.WHITE, width=size // 25)
        d.text((size / 2, size / 2), txt, font=b.font(b.F_BLACK, int(size * 0.72)), fill=b.WHITE, anchor="mm",
               stroke_width=size // 30, stroke_fill=b.NAVY)
        _sprites[key] = im
    return _sprites[key]


def icone(r, size, revelado):
    if revelado:
        return emoji(r["er"], size) if r["er"] else numero_sprite(r["resposta"], size)
    return emoji(r["emoji"], size)


def paste_c(img, sp, cx, cy):
    img.alpha_composite(sp, (int(cx - sp.width / 2), int(cy - sp.height / 2)))


def _mask():
    if "mask" not in _sprites:
        pat = np.asarray(b.pattern_bg().convert("L"), dtype=int) - np.asarray(b.gradient(b.BLUE, b.NAVY).convert("L"), dtype=int)
        _sprites["mask"] = Image.fromarray(np.clip(pat * 4, 0, 255).astype("uint8")).point(lambda v: v // 5)
    return _sprites["mask"]


def fundo(k):
    c1, c2 = CORES[k % len(CORES)]
    img = b.gradient(c1, c2)
    img.paste(Image.new("RGB", (W, H), (255, 255, 255)), (0, 0), _mask())
    return img.convert("RGBA")


def fit(d, txt, size, maxw, minsize=30):
    f = b.font(b.F_BLACK, size)
    while d.textlength(txt, font=f) > maxw and f.size > minsize:
        f = b.font(b.F_BLACK, f.size - 2)
    return f


def wrap(d, txt, f, maxw):
    linhas, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            linhas.append(cur)
            cur = w
    linhas.append(cur)
    return linhas


def coracoes(img, cx, cy, n=8, size=44, gap=8):
    sp = emoji("❤", size)
    tot = n * size + (n - 1) * gap
    x = cx - tot / 2 + size / 2
    for i in range(n):
        paste_c(img, sp, x + i * (size + gap), cy)


def topo(img, n):
    d = ImageDraw.Draw(img)
    d.ellipse([40, 30, 190, 180], fill=b.ORANGE, outline=b.WHITE, width=8)
    d.text((115, 103), f"{n:02d}", font=b.font(b.F_BLACK, 70), fill=b.WHITE, anchor="mm", stroke_width=3,
           stroke_fill=b.NAVY)
    f = fit(d, TITULO, 84, 1290)
    b.text_outline(d, (880, 105), TITULO, f, b.YELLOW, w=9)
    b.selo(img, 1730, 105, 0.7)
    # lembrete das vidas
    x0, y0, x1, y1 = VIDAS_BOX
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x1, y1], 30, fill=(255, 255, 255, 235), outline=b.NAVY, width=5)
    d.text(((x0 + x1) / 2, y0 + 32), "SUAS VIDAS", font=b.font(b.F_BLACK, 32), fill=b.NAVY, anchor="mm")
    coracoes(img, (x0 + x1) / 2, y0 + 90, 8, 42, 9)


def cartao_sprite(r, revelado=False):
    """Cartão branco com emoji grande + pedido (sprite do tamanho do cartão, com sombra)."""
    x0, y0, x1, y1 = CARD
    w, h = x1 - x0, y1 - y0
    m = 30
    sp = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    sh = Image.new("RGBA", sp.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([m, m + 12, m + w, m + h + 12], 50, fill=(0, 0, 0, 100))
    sp.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(sp)
    d.rounded_rectangle([m, m, m + w, m + h], 50, fill=b.WHITE, outline=b.NAVY, width=8)
    ecx, ecy = m + 250, m + h // 2
    tint = (255, 236, 160) if not revelado else (255, 220, 90)
    d.ellipse([ecx - 185, ecy - 185, ecx + 185, ecy + 185], fill=tint, outline=b.NAVY, width=6)
    paste_c(sp, icone(r, 250, revelado), ecx, ecy)
    # texto do pedido
    tx0, tx1 = m + 480, m + w - 50
    maxw = tx1 - tx0
    size = 100
    while True:
        f = b.font(b.F_BLACK, size)
        lin = wrap(d, r["pedido"], f, maxw)
        lh = int(size * 1.12)
        if (len(lin) <= 3 and len(lin) * lh <= h - 120 and all(d.textlength(l, font=f) <= maxw for l in lin)) or size <= 44:
            break
        size -= 4
    cy = m + h / 2 - (len(lin) - 1) * lh / 2
    for i, l in enumerate(lin):
        d.text(((tx0 + tx1) / 2, cy + i * lh), l, font=f, fill=b.NAVY, anchor="mm")
    if r.get("pegadinha"):
        ft = b.font(b.F_BLACK, 40)
        t = "PEGADINHA!"
        tw = d.textlength(t, font=ft)
        cx = (tx0 + tx1) / 2
        d.rounded_rectangle([cx - tw / 2 - 30, m - 30, cx + tw / 2 + 30, m + 34], 32, fill=b.RED, outline=b.WHITE, width=6)
        d.text((cx, m + 2), t, font=ft, fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
    return sp


def faixa(img, r, revelado, pop=1.0):
    x0, y0, x1, y1 = FAIXA
    d = ImageDraw.Draw(img)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hw, hh = (x1 - x0) / 2 * pop, (y1 - y0) / 2 * pop
    d.rounded_rectangle([cx - hw + 6, cy - hh + 10, cx + hw + 6, cy + hh + 10], 55, fill=(0, 0, 0, 90))
    if not revelado:
        d.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh], 55, fill=b.NAVY, outline=b.WHITE, width=7)
        d.text((cx, cy - 4), "? ? ?", font=b.font(b.F_BLACK, 90), fill=b.WHITE, anchor="mm")
        return
    d.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh], 55, fill=b.YELLOW, outline=b.WHITE, width=8)
    if pop >= 0.98:
        lbl = "PALITO DISSE:"
        fl = b.font(b.F_BLACK, 36)
        lw = d.textlength(lbl, font=fl)
        f = fit(d, r["resposta"], 92, (x1 - x0) - lw - 140)
        aw = d.textlength(r["resposta"], font=f)
        x = cx - (lw + 30 + aw) / 2
        d.text((x, cy), lbl, font=fl, fill=b.NAVY, anchor="lm")
        d.text((x + lw + 30, cy - 4), r["resposta"], font=f, fill=b.NAVY, anchor="lm", stroke_width=2, stroke_fill=b.NAVY)


def barra(img, frac):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = BAR
    d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 32, fill=b.WHITE)
    d.rounded_rectangle(BAR, 24, fill=(60, 70, 110))
    if frac > 0.002:
        xe = x0 + (x1 - x0) * frac
        d.rounded_rectangle([x0, y0, max(xe, x0 + 48), y1], 24, fill=b.ORANGE if frac > 0.3 else b.RED)
    s = math.ceil(frac * COUNT)
    if s > 0:
        d.text(((x0 + x1) // 2, (y0 + y1) // 2), str(s), font=b.font(b.F_BLACK, 40), fill=b.WHITE, anchor="mm",
               stroke_width=4, stroke_fill=b.NAVY)


def aviso_vida(img, k=1.0):
    """Texto embaixo na revelação: 'PENSOU IGUAL? -1 ❤'."""
    d = ImageDraw.Draw(img)
    t = "PENSOU IGUAL? PERDEU 1 VIDA!"
    f = b.font(b.F_BLACK, 50)
    tw = d.textlength(t, font=f)
    cx = (BAR[0] + BAR[2]) / 2 - 30
    y = 970 + int((1 - k) * 120)
    d.rounded_rectangle([cx - tw / 2 - 30, y - 38, cx + tw / 2 + 100, y + 38], 38, fill=b.RED, outline=b.WHITE, width=6)
    d.text((cx - 4, y), t, font=f, fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
    paste_c(img, emoji("❤", 52), cx + tw / 2 + 50, y)


def tela(r, revelado=False, com_cartao=True):
    img = fundo(r["n"])
    topo(img, r["n"])
    if com_cartao:
        sp = cartao_sprite(r, revelado)
        img.alpha_composite(sp, (CARD[0] - 30, CARD[1] - 30))
    return img


def burst(c1, c2, rot):
    img = Image.new("RGB", (W, H), c2)
    d = ImageDraw.Draw(img)
    cx, cy, Rr = W / 2, H / 2, 2400
    for k in range(24):
        a0, a1 = math.radians(k * 15 + rot), math.radians(k * 15 + 7.5 + rot)
        d.polygon([(cx, cy), (cx + Rr * math.cos(a0), cy + Rr * math.sin(a0)),
                   (cx + Rr * math.cos(a1), cy + Rr * math.sin(a1))], fill=c1 if k % 2 else c2)
    return img


def vinheta_frames(r):
    c1, c2 = CORES[r["n"] % len(CORES)]
    for i in range(int(VINHETA * FPS)):
        t = i / FPS
        img = burst(c1, c2, t * 30).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.25)
        b.text_outline(d, (W // 2, 250), "RODADA", b.font(b.F_BLACK, int(110 * (0.4 + 0.6 * s))), b.WHITE, w=10)
        b.text_outline(d, (W // 2, 520), f"{r['n']:02d}", b.font(b.F_BLACK, int(330 * (0.4 + 0.6 * s))), b.YELLOW, w=18)
        if r.get("pegadinha"):
            b.text_outline(d, (W // 2, 820), "PEGADINHA!",
                           b.font(b.F_BLACK, int(110 * (0.4 + 0.6 * s))), b.RED, outline=b.WHITE, w=10)
        else:
            b.text_outline(d, (W // 2, 820), TITULO, b.font(b.F_BLACK, int(70 * (0.4 + 0.6 * s))), b.WHITE, w=8)
        yield img.convert("RGB")


def pergunta_frames(r, fala):
    """Cartão entra com pulinho, fala do pedido e 6 s de barra com o Palito pensando."""
    fundo_t = tela(r, com_cartao=False)
    sp = cartao_sprite(r)
    n_in = int(0.35 * FPS)
    for i in range(n_in):
        k = (i + 1) / n_in
        sc = 0.5 + 0.58 * k if k < 0.8 else 1.08 - 0.08 * (k - 0.8) / 0.2
        img = fundo_t.copy()
        s2 = sp.resize((int(sp.width * sc), int(sp.height * sc)), Image.BILINEAR)
        paste_c(img, s2, (CARD[0] + CARD[2]) / 2, (CARD[1] + CARD[3]) / 2)
        faixa(img, r, False, min(1.0, k * 1.2))
        barra(img, 1.0)
        b.put_palito(img, "pensando", PAL_H, PAL_CX, PAL_BASE + int((1 - k) * 500))
        yield img.convert("RGB")
    base = tela(r)
    faixa(base, r, False)
    for i in range(int(fala * FPS)):
        img = base.copy()
        barra(img, 1.0)
        b.put_palito(img, "pensando", PAL_H, PAL_CX, PAL_BASE, int(6 * math.sin(i / FPS * 5)))
        yield img.convert("RGB")
    n = int(COUNT * FPS)
    for i in range(n):
        img = base.copy()
        frac = 1 - i / n
        barra(img, frac)
        pose = "pensando" if frac > 0.17 else "assustado"
        b.put_palito(img, pose, PAL_H, PAL_CX, PAL_BASE, int(7 * math.sin(i / FPS * (5 if pose == "pensando" else 18))))
        yield img.convert("RGB")


def revela_frames(r, dur):
    base = tela(r, revelado=True)
    for i in range(int(dur * FPS)):
        tt = i / FPS
        img = base.copy()
        pop = min(1.0, tt / 0.18)
        pop = 0.6 + 0.48 * pop if pop < 1 else max(1.0, 1.08 - (tt - 0.18) / 0.15 * 0.08)
        faixa(img, r, True, min(pop, 1.08) if tt < 0.33 else 1.0)
        if tt > 0.35:
            aviso_vida(img, min(1.0, (tt - 0.35) / 0.2))
        if tt < 0.2:  # flash
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(160 * (1 - tt / 0.2)))))
        b.put_palito(img, "comemorando", PAL_H, PAL_CX, PAL_BASE, -int(abs(28 * math.sin(tt * 7))))
        yield img.convert("RGB")


def vidas_frames(n, dur):
    """Parada a cada 10 rodadas: quantas vidas ainda restam?"""
    c1, c2 = (255, 90, 120), (200, 30, 70)
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = burst(c1, c2, t * 12).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.3)
        b.text_outline(d, (800, 220), f"RODADA {n} CONCLUÍDA!", b.font(b.F_BLACK, int(90 * (0.5 + 0.5 * s))), b.WHITE, w=10)
        b.text_outline(d, (800, 380), "QUANTAS VIDAS", b.font(b.F_BLACK, int(130 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
        b.text_outline(d, (800, 530), "VOCÊ AINDA TEM?", b.font(b.F_BLACK, int(130 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
        if s >= 1:
            d.rounded_rectangle([230, 640, 1370, 790], 70, fill=(255, 255, 255, 240), outline=b.NAVY, width=7)
            coracoes(img, 800, 715, 8, 100, 30)
        b.selo(img, 800, 900, 1.1)
        b.put_palito(img, "apontando", 620, 1620 + int((1 - s) * 700), 1060, int(6 * math.sin(t * 5)))
        yield img.convert("RGB")


def intro_base():
    img = fundo(0)
    b.selo(img, 960, 80, 1.0)
    d = ImageDraw.Draw(img)
    b.text_outline(d, (800, 220), "NÃO DIGA O MESMO", b.font(b.F_BLACK, 130), b.WHITE, w=13)
    b.text_outline(d, (800, 360), "QUE O PALITO!", b.font(b.F_BLACK, 140), b.YELLOW, w=14)
    d.rounded_rectangle([200, 450, 1400, 620], 60, fill=(255, 255, 255, 240), outline=b.NAVY, width=8)
    d.text((800, 490), "VOCÊ COMEÇA COM 8 VIDAS", font=b.font(b.F_BLACK, 44), fill=b.NAVY, anchor="mm")
    coracoes(img, 800, 565, 8, 70, 22)
    passos = [("1", "LEIA O PEDIDO"), ("2", "PENSE NA SUA RESPOSTA"), ("3", "PENSOU IGUAL AO PALITO? -1 VIDA!")]
    d = ImageDraw.Draw(img)
    for k, (num, t) in enumerate(passos):
        y = 690 + k * 115
        d.ellipse([200, y - 45, 290, y + 45], fill=b.ORANGE, outline=b.WHITE, width=6)
        d.text((245, y), num, font=b.font(b.F_BLACK, 56), fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
        b.text_outline(d, (320, y), t, b.font(b.F_BLACK, 62), b.WHITE, w=8, anchor="lm")
    return img


def outro_base():
    img = fundo(3)
    d = ImageDraw.Draw(img)
    b.text_outline(d, (800, 200), "COM QUANTAS VIDAS", b.font(b.F_BLACK, 110), b.WHITE, w=12)
    b.text_outline(d, (800, 340), "VOCÊ TERMINOU?", b.font(b.F_BLACK, 130), b.YELLOW, w=14)
    d.rounded_rectangle([250, 420, 1350, 540], 60, fill=(255, 255, 255, 240), outline=b.NAVY, width=7)
    coracoes(img, 800, 480, 8, 80, 26)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([340, 590, 1260, 710], 55, fill=b.RED, outline=b.WHITE, width=8)
    d.text((800, 650), "COMENTA AQUI EMBAIXO!", font=b.font(b.F_BLACK, 64), fill=b.WHITE, anchor="mm",
           stroke_width=3, stroke_fill=b.NAVY)
    b.text_outline(d, (800, 790), "MARCA UM AMIGO E INSCREVA-SE NO", b.font(b.F_BLACK, 54), b.WHITE, w=7)
    b.selo(img, 800, 910, 1.3)
    return img


def anima(base, pose, dur, h=640, cx=1660, bottom=1060):
    for i in range(int(dur * FPS)):
        img = base.copy()
        b.put_palito(img, pose, h, cx, bottom, int(8 * math.sin(i / FPS * 4)))
        yield img.convert("RGB")


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    quadros = [next(anima(intro_base(), "acenando", 0.1)), list(vinheta_frames(R[16]))[-1]]
    for r in (R[0], R[16], R[13], R[37]):
        fr = list(pergunta_frames(r, 0.3))
        quadros.append(fr[-int(COUNT * FPS * 0.5)])
        quadros.append(list(revela_frames(r, 1.2))[-1])
    quadros.append(list(vidas_frames(20, 0.5))[-1])
    quadros.append(next(anima(outro_base(), "acenando", 0.1)))
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
    tmp = tempfile.mkdtemp(prefix="quiz_naodiga_")
    sfx = b.make_sfx(tmp)
    dur = lambda p: b.duration(p) if os.path.exists(p) else 1.5
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    marcas = {}
    tl.sound(A("intro.mp3"), at=0.3)
    for f in anima(intro_base(), "acenando", dur(A("intro.mp3")) + 0.8):
        tl.frame(f)
    for r in R:
        n = r["n"]
        if n % 10 == 1:
            marcas[str(n)] = tl.t
        tl.sound(sfx["whoosh"], vol=0.7)
        for f in vinheta_frames(r):
            tl.frame(f)
        q = A(f"q{n}.mp3")
        tl.sound(q, at=tl.t + 0.3)
        fala = dur(q) + 0.05
        st = tl.t + 0.35 + fala
        for s in range(int(COUNT)):
            tl.sound(sfx["tick"], at=st + s, vol=0.8)
        for f in pergunta_frames(r, fala):
            tl.frame(f)
        p = A(f"p{n}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(p, at=tl.t + 0.25)
        for f in revela_frames(r, max(2.5, dur(p) + 0.45)):
            tl.frame(f)
        if n in (10, 20, 30):
            v = A(f"vidas{n}.mp3")
            tl.sound(sfx["whoosh"])
            tl.sound(v, at=tl.t + 0.3)
            for f in vidas_frames(n, dur(v) + 0.8):
                tl.frame(f)
        if n % 10 == 0:
            print(f"{n}/40 ({tl.t / 60:.1f} min)", flush=True)
    marcas["final"] = tl.t
    tl.sound(sfx["whoosh"])
    tl.sound(A("outro.mp3"), at=tl.t + 0.4)
    for f in anima(outro_base(), "acenando", max(4.0, dur(A("outro.mp3")) + 1.8)):
        tl.frame(f)
    total = tl.t
    tl.close()
    json.dump(marcas, open(os.path.join(HERE, "tempos.json"), "w", encoding="utf-8"), indent=1)
    mixar(tl, video, total)
    print(f"OK {SAIDA} ({total:.1f}s)")


def mixar(tl, video, total):
    sr = 44100
    buf = np.zeros((int((total + 1) * sr), 2), dtype=np.float32)
    voz = np.zeros(len(buf), dtype=np.float32)
    dec = lambda p: np.frombuffer(subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"],
        capture_output=True).stdout, dtype=np.float32).reshape(-1, 2)
    cache = {}
    for pth, at, vol in tl.audio:
        x = cache.setdefault(pth, dec(pth)) * vol
        i0 = int(at * sr)
        i1 = min(len(buf), i0 + len(x))
        buf[i0:i1] += x[: i1 - i0]
        if os.path.abspath(pth).startswith(os.path.join(HERE, "assets")):
            voz[i0:i1] = 1.0
    n = int(total * sr)
    buf, voz = buf[:n], voz[:n]
    m = dec(A("musica.mp3"))
    m = np.tile(m, (n // len(m) + 1, 1))[:n].copy()
    k = int(0.25 * sr)
    env = np.convolve(voz, np.ones(k, dtype=np.float32) / k, mode="same")
    ganho = b.MUSICA_VOL * (1.0 - 0.55 * np.clip(env, 0, 1))
    fi, fo = int(1.5 * sr), int(3.0 * sr)
    ganho[:fi] *= np.linspace(0, 1, fi)
    ganho[-fo:] *= np.linspace(1, 0, fo)
    buf += m * ganho[:, None]
    peak = float(np.abs(buf).max()) or 1.0
    if peak > 0.98:
        buf *= 0.98 / peak
    raw = os.path.splitext(video)[0] + ".f32"
    buf.tofile(raw)
    b.run(["ffmpeg", "-y", "-i", video, "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", raw, "-map", "0:v",
           "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", SAIDA])


if __name__ == "__main__":
    previa() if "--previa" in sys.argv else main()
