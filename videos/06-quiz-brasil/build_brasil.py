"""Quiz Palito — "QUIZ DO BRASIL" (30 perguntas, 4 alternativas, 6 s cada).

Cada pergunta: vinheta com o número -> cartão com a pergunta e as 4 alternativas + 6 s de barra com o Palito pensando
-> revelação (alternativa certa fica verde, as outras apagam). Sem explicação/fonte: direto ao ponto.
Reaproveita 01-paises-sem-vogais/build.py (fontes, cores, Palito, sons) e helpers do 05-nao-diga-o-mesmo.
Uso: py -3 build_brasil.py            (monta quiz-palito-quiz-do-brasil.mp4)
     py -3 build_brasil.py --previa   (só salva a prancha de prévia em previa/)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "05-nao-diga-o-mesmo"))
import build_naodiga as nd
from build_naodiga import b

W, H, FPS = b.W, b.H, b.FPS
R = json.load(open(os.path.join(HERE, "perguntas.json"), encoding="utf-8"))
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-quiz-do-brasil.mp4")
TITULO = "QUIZ DO BRASIL"

COUNT = 6.0
CARD = (90, 215, 1400, 470)
OPS = [(90, 510, 730, 690), (760, 510, 1400, 690), (90, 720, 730, 900), (760, 720, 1400, 900)]
LETRAS = "ABCD"
COR_LETRA = [(235, 60, 50), (40, 120, 220), (255, 140, 0), (150, 70, 200)]
VERDE = (30, 175, 80)
PAL_CX, PAL_BASE, PAL_H = 1670, 1055, 600
CORES = [((20, 150, 80), (5, 80, 50)), ((30, 110, 210), (15, 45, 130)), ((0, 160, 170), (0, 80, 100)),
         ((40, 170, 90), (20, 90, 120)), ((70, 90, 220), (30, 30, 130)), ((10, 130, 110), (10, 60, 80))]


def fundo(k):
    c1, c2 = CORES[k % len(CORES)]
    img = b.gradient(c1, c2)
    img.paste(Image.new("RGB", (W, H), (255, 255, 255)), (0, 0), nd._mask())
    return img.convert("RGBA")


def topo(img, n):
    d = ImageDraw.Draw(img)
    d.ellipse([40, 30, 190, 180], fill=b.ORANGE, outline=b.WHITE, width=8)
    d.text((115, 103), f"{n:02d}", font=b.font(b.F_BLACK, 70), fill=b.WHITE, anchor="mm", stroke_width=3,
           stroke_fill=b.NAVY)
    b.text_outline(d, (720, 105), TITULO, b.font(b.F_BLACK, 104), b.YELLOW, w=10)
    bandeira(img, 1265, 105, 120)
    b.selo(img, 1730, 105, 0.7)


def bandeira(img, cx, cy, w):
    """Bandeira do Brasil simplificada (verde, losango amarelo, círculo azul)."""
    h = int(w * 0.7)
    fl = Image.new("RGBA", (w, h), (0, 156, 59, 255))
    d = ImageDraw.Draw(fl)
    m = w * 0.08
    d.polygon([(w / 2, m), (w - m, h / 2), (w / 2, h - m), (m, h / 2)], fill=(255, 223, 0))
    r = h * 0.27
    d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=(0, 39, 118))
    d.arc([w / 2 - r * 1.6, h / 2 - r * 0.55, w / 2 + r * 1.4, h / 2 + r * 2.4], 235, 300, fill=b.WHITE, width=max(2, w // 40))
    out = Image.new("RGBA", (w + 16, h + 16), (0, 0, 0, 0))
    ImageDraw.Draw(out).rounded_rectangle([0, 0, w + 15, h + 15], 10, fill=b.WHITE)
    out.alpha_composite(fl, (8, 8))
    ImageDraw.Draw(out).rounded_rectangle([0, 0, w + 15, h + 15], 10, outline=b.NAVY, width=4)
    nd.paste_c(img, out.rotate(-6, expand=True, resample=Image.BICUBIC), cx, cy)


def cartao_sprite(r):
    x0, y0, x1, y1 = CARD
    w, h = x1 - x0, y1 - y0
    m = 30
    sp = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    sh = Image.new("RGBA", sp.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([m, m + 12, m + w, m + h + 12], 45, fill=(0, 0, 0, 100))
    sp.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(sp)
    d.rounded_rectangle([m, m, m + w, m + h], 45, fill=b.WHITE, outline=b.NAVY, width=8)
    ecx, ecy = m + 140, m + h // 2
    d.ellipse([ecx - 100, ecy - 100, ecx + 100, ecy + 100], fill=(255, 236, 160), outline=b.NAVY, width=6)
    nd.paste_c(sp, nd.emoji(r["emoji"], 130), ecx, ecy)
    tx0, tx1 = m + 270, m + w - 40
    maxw = tx1 - tx0
    size = 76
    while True:
        f = b.font(b.F_BLACK, size)
        lin = nd.wrap(d, r["pergunta"], f, maxw)
        lh = int(size * 1.15)
        if (len(lin) <= 3 and len(lin) * lh <= h - 40 and all(d.textlength(l, font=f) <= maxw for l in lin)) or size <= 40:
            break
        size -= 2
    cy = m + h / 2 - (len(lin) - 1) * lh / 2
    for i, l in enumerate(lin):
        d.text(((tx0 + tx1) / 2, cy + i * lh), l, font=f, fill=b.NAVY, anchor="mm")
    return sp


def opcao_sprite(i, txt, estado="normal"):
    """Caixa de alternativa. estado: normal | certa | apagada."""
    x0, y0, x1, y1 = OPS[i]
    w, h = x1 - x0, y1 - y0
    m = 24
    sp = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    d = ImageDraw.Draw(sp)
    d.rounded_rectangle([m + 4, m + 10, m + w + 4, m + h + 10], 40, fill=(0, 0, 0, 90))
    fill, fg, out = b.WHITE, b.NAVY, b.NAVY
    if estado == "certa":
        fill, fg, out = VERDE, b.WHITE, b.WHITE
    d.rounded_rectangle([m, m, m + w, m + h], 40, fill=fill, outline=out, width=7)
    lcx, lcy = m + 75, m + h // 2
    d.ellipse([lcx - 52, lcy - 52, lcx + 52, lcy + 52], fill=COR_LETRA[i] if estado != "certa" else b.WHITE,
              outline=b.WHITE if estado != "certa" else b.NAVY, width=5)
    d.text((lcx, lcy - 2), LETRAS[i], font=b.font(b.F_BLACK, 64),
           fill=b.WHITE if estado != "certa" else VERDE, anchor="mm", stroke_width=2,
           stroke_fill=b.NAVY if estado != "certa" else VERDE)
    tx0, tx1 = m + 145, m + w - (95 if estado == "certa" else 25)
    maxw = tx1 - tx0
    size = 60
    while True:
        f = b.font(b.F_BLACK, size)
        lin = nd.wrap(d, txt, f, maxw)
        lh = int(size * 1.12)
        if (len(lin) * lh <= h - 24 and all(d.textlength(l, font=f) <= maxw for l in lin)) or size <= 30:
            break
        size -= 2
    cy = m + h / 2 - (len(lin) - 1) * lh / 2
    for k, l in enumerate(lin):
        d.text((tx0, cy + k * lh), l, font=f, fill=fg, anchor="lm")
    if estado == "certa":
        nd.paste_c(sp, nd.emoji("✅", 70), m + w - 55, m + h // 2)
    if estado == "apagada":
        a = sp.getchannel("A").point(lambda v: int(v * 0.35))
        sp.putalpha(a)
    return sp


def put_op(img, sp, i, sc=1.0):
    x0, y0, x1, y1 = OPS[i]
    if sc != 1.0:
        sp = sp.resize((int(sp.width * sc), int(sp.height * sc)), Image.BILINEAR)
    nd.paste_c(img, sp, (x0 + x1) / 2, (y0 + y1) / 2)


def barra(img, frac):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = nd.BAR
    d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 32, fill=b.WHITE)
    d.rounded_rectangle(nd.BAR, 24, fill=(60, 70, 110))
    if frac > 0.002:
        xe = x0 + (x1 - x0) * frac
        d.rounded_rectangle([x0, y0, max(xe, x0 + 48), y1], 24, fill=b.ORANGE if frac > 0.3 else b.RED)
    s = math.ceil(frac * COUNT)
    if s > 0:
        d.text(((x0 + x1) // 2, (y0 + y1) // 2), str(s), font=b.font(b.F_BLACK, 40), fill=b.WHITE, anchor="mm",
               stroke_width=4, stroke_fill=b.NAVY)


def tela(r, ops=True):
    img = fundo(r["n"])
    topo(img, r["n"])
    img.alpha_composite(cartao_sprite(r), (CARD[0] - 30, CARD[1] - 30))
    if ops:
        for i, o in enumerate(r["op"]):
            put_op(img, opcao_sprite(i, o), i)
    return img


def vinheta_frames(r):
    c1, c2 = CORES[r["n"] % len(CORES)]
    for i in range(int(nd.VINHETA * FPS)):
        t = i / FPS
        img = nd.burst(c1, c2, t * 30).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.25)
        b.text_outline(d, (W // 2, 250), "PERGUNTA", b.font(b.F_BLACK, int(110 * (0.4 + 0.6 * s))), b.WHITE, w=10)
        b.text_outline(d, (W // 2, 520), f"{r['n']:02d}", b.font(b.F_BLACK, int(330 * (0.4 + 0.6 * s))), b.YELLOW, w=18)
        b.text_outline(d, (W // 2, 820), "QUIZ DO BRASIL", b.font(b.F_BLACK, int(80 * (0.4 + 0.6 * s))), b.WHITE, w=8)
        yield img.convert("RGB")


def pergunta_frames(r, fala):
    """Cartão entra com pulinho, alternativas entram uma a uma, fala e 6 s de barra."""
    sem_ops = tela(r, ops=False)
    sps = [opcao_sprite(i, o) for i, o in enumerate(r["op"])]
    n_in = int(0.7 * FPS)
    for i in range(n_in):
        t = i / FPS
        img = sem_ops.copy()
        for k, sp in enumerate(sps):
            tk = (t - 0.08 * k) / 0.25
            if tk <= 0:
                continue
            sc = 0.5 + 0.58 * tk if tk < 0.8 else (1.08 - 0.08 * min(1, (tk - 0.8) / 0.2))
            put_op(img, sp, k, sc)
        barra(img, 1.0)
        b.put_palito(img, "pensando", PAL_H, PAL_CX, PAL_BASE + int(max(0, 1 - t / 0.35) * 500))
        yield img.convert("RGB")
    base = sem_ops.copy()
    for k, sp in enumerate(sps):
        put_op(base, sp, k)
    for i in range(max(0, int(fala * FPS) - n_in)):
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
    c = r["certa"]
    base = tela(r, ops=False)
    for i, o in enumerate(r["op"]):
        if i != c:
            put_op(base, opcao_sprite(i, o, "apagada"), i)
    certa = opcao_sprite(c, r["op"][c], "certa")
    for i in range(int(dur * FPS)):
        tt = i / FPS
        img = base.copy()
        if tt < 0.18:
            sc = 0.85 + 0.25 * tt / 0.18
        elif tt < 0.33:
            sc = 1.10 - 0.10 * (tt - 0.18) / 0.15
        else:
            sc = 1.0
        put_op(img, certa, c, sc)
        if tt < 0.2:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(150 * (1 - tt / 0.2)))))
        b.put_palito(img, "comemorando", PAL_H, PAL_CX, PAL_BASE, -int(abs(28 * math.sin(tt * 7))))
        yield img.convert("RGB")


def placar_frames(n, dur):
    c1, c2 = (255, 170, 0), (215, 100, 0)
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = nd.burst(c1, c2, t * 12).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.3)
        b.text_outline(d, (800, 230), f"{n} PERGUNTAS!", b.font(b.F_BLACK, int(110 * (0.5 + 0.5 * s))), b.WHITE, w=11)
        b.text_outline(d, (800, 420), "QUANTAS VOCÊ", b.font(b.F_BLACK, int(140 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
        b.text_outline(d, (800, 580), "JÁ ACERTOU?", b.font(b.F_BLACK, int(140 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
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
    b.text_outline(d, (800, 240), "QUIZ DO", b.font(b.F_BLACK, 140), b.WHITE, w=13)
    b.text_outline(d, (720, 400), "BRASIL", b.font(b.F_BLACK, 180), b.YELLOW, w=16)
    bandeira(img, 1270, 400, 230)
    passos = [("30", "PERGUNTAS SOBRE O BRASIL"), ("4", "ALTERNATIVAS: A, B, C OU D"), ("6", "SEGUNDOS PARA RESPONDER")]
    d = ImageDraw.Draw(img)
    for k, (num, t) in enumerate(passos):
        y = 600 + k * 135
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
    d.text((800, 488), "__ / 30", font=b.font(b.F_BLACK, 80), fill=b.NAVY, anchor="mm")
    d.rounded_rectangle([290, 590, 1310, 710], 55, fill=b.RED, outline=b.WHITE, width=8)
    d.text((800, 650), "COMENTA SUA CIDADE!", font=b.font(b.F_BLACK, 64), fill=b.WHITE, anchor="mm",
           stroke_width=3, stroke_fill=b.NAVY)
    b.text_outline(d, (800, 790), "MARCA UM AMIGO E INSCREVA-SE NO", b.font(b.F_BLACK, 54), b.WHITE, w=7)
    b.selo(img, 800, 910, 1.3)
    return img


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    quadros = [next(nd.anima(intro_base(), "acenando", 0.1)), list(vinheta_frames(R[2]))[-1]]
    for r in (R[0], R[2], R[8], R[16]):
        fr = list(pergunta_frames(r, 0.8))
        quadros.append(fr[-int(COUNT * FPS * 0.5)])
        quadros.append(list(revela_frames(r, 1.2))[-1])
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
    tmp = tempfile.mkdtemp(prefix="quiz_brasil_")
    sfx = b.make_sfx(tmp)
    dur = lambda p: b.duration(p) if os.path.exists(p) else 1.5
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
        tl.sound(sfx["whoosh"], vol=0.7)
        for f in vinheta_frames(r):
            tl.frame(f)
        q = A(f"q{n}.mp3")
        tl.sound(q, at=tl.t + 0.3)
        fala = dur(q) + 0.15
        st = tl.t + max(fala, 0.7)
        for s in range(int(COUNT)):
            tl.sound(sfx["tick"], at=st + s, vol=0.8)
        for f in pergunta_frames(r, fala):
            tl.frame(f)
        p = A(f"p{n}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(p, at=tl.t + 0.25)
        for f in revela_frames(r, max(2.5, dur(p) + 0.6)):
            tl.frame(f)
        if n in (10, 20):
            v = A(f"placar{n}.mp3")
            tl.sound(sfx["whoosh"])
            tl.sound(v, at=tl.t + 0.3)
            for f in placar_frames(n, dur(v) + 0.8):
                tl.frame(f)
        if n % 10 == 0:
            print(f"{n}/30 ({tl.t / 60:.1f} min)", flush=True)
    marcas["final"] = tl.t
    tl.sound(sfx["whoosh"])
    tl.sound(A("outro.mp3"), at=tl.t + 0.4)
    for f in nd.anima(outro_base(), "acenando", max(4.0, dur(A("outro.mp3")) + 1.8)):
        tl.frame(f)
    total = tl.t
    tl.close()
    json.dump(marcas, open(os.path.join(HERE, "tempos.json"), "w", encoding="utf-8"), indent=1)
    # mixagem do 05, apontando para os assets deste vídeo
    nd.HERE, nd.A, nd.SAIDA = HERE, A, SAIDA
    nd.mixar(tl, video, total)
    print(f"OK {SAIDA} ({total:.1f}s)")


if __name__ == "__main__":
    previa() if "--previa" in sys.argv else main()
