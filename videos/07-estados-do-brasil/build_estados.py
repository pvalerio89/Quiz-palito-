"""Quiz Palito — "QUE ESTADO É ESSE?" (27 estados do Brasil pelo mapa, 4 alternativas, 6 s cada).

Cada pergunta: vinheta -> mapa do Brasil com um estado em laranja + 4 alternativas + 6 s de barra
-> revelação (estado fica verde, alternativa certa verde e faixa com a capital).
Mapa: mapa_brasil.json (malha de estados do IBGE, simplificada). Reaproveita o 06 (alternativas, barra, placar, mixagem).
Uso: py -3 build_estados.py            (monta quiz-palito-estados-do-brasil.mp4)
     py -3 build_estados.py --previa   (só salva a prancha de prévia em previa/)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "06-quiz-brasil"))
import build_brasil as bb
from build_brasil import b, nd

W, H, FPS = b.W, b.H, b.FPS
R = json.load(open(os.path.join(HERE, "perguntas.json"), encoding="utf-8"))
MAPA = json.load(open(os.path.join(HERE, "mapa_brasil.json"), encoding="utf-8"))["estados"]
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-estados-do-brasil.mp4")
TITULO = "QUE ESTADO É ESSE?"
TOTAL = len(R)
COUNT = bb.COUNT
VERDE = bb.VERDE

# Layout: mapa à esquerda, alternativas empilhadas no meio, Palito à direita.
MAP_BOX = (50, 205, 830, 900)
bb.OPS = [(875, 210 + k * 172, 1530, 210 + k * 172 + 150) for k in range(4)]
PAL_CX, PAL_BASE, PAL_H = 1735, 1055, 540
CORES = [((20, 150, 80), (5, 80, 50)), ((30, 110, 210), (15, 45, 130)), ((0, 160, 170), (0, 80, 100)),
         ((40, 170, 90), (20, 90, 120)), ((70, 90, 220), (30, 30, 130)), ((10, 130, 110), (10, 60, 80))]
TERRA = (236, 240, 248)
LARANJA = (255, 140, 0)
MAR = (190, 225, 250)


def _proj():
    xs = [p[0] for pol in MAPA.values() for ring in pol for p in ring]
    ys = [p[1] for pol in MAPA.values() for ring in pol for p in ring]
    return min(xs), min(ys), max(xs), max(ys)


BX0, BY0, BX1, BY1 = _proj()


def mapa(alvo, cor, w, h, ss=2):
    """Mapa do Brasil (w x h) com o estado alvo pintado de `cor`. Desenha em 2x e reduz (bordas suaves)."""
    W2, H2 = w * ss, h * ss
    pad = 6 * ss
    esc = min((W2 - 2 * pad) / (BX1 - BX0), (H2 - 2 * pad) / (BY1 - BY0))
    ox = (W2 - (BX1 - BX0) * esc) / 2
    oy = (H2 - (BY1 - BY0) * esc) / 2
    P = lambda p: (ox + (p[0] - BX0) * esc, oy + (p[1] - BY0) * esc)
    # sombra do país (deslocada para baixo/direita)
    sh = Image.new("L", (W2, H2), 0)
    ds = ImageDraw.Draw(sh)
    Ps = lambda p: (P(p)[0] + 5 * ss, P(p)[1] + 8 * ss)
    for pol in MAPA.values():
        for ring in pol:
            ds.polygon([Ps(p) for p in ring], fill=110)
    im = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    im.putalpha(sh.filter(ImageFilter.GaussianBlur(6 * ss)))
    d = ImageDraw.Draw(im)
    for uf, pol in MAPA.items():
        for ring in pol:
            d.polygon([P(p) for p in ring], fill=cor if uf == alvo else TERRA)
    for uf, pol in MAPA.items():
        for ring in pol:
            pts = [P(p) for p in ring]
            d.line(pts + [pts[0]], fill=b.NAVY, width=(4 if uf == alvo else 2) * ss, joint="curve")
    # estados pequenos: anel em volta para achar fácil
    xs = [P(p)[0] for ring in MAPA[alvo] for p in ring]
    ys = [P(p)[1] for ring in MAPA[alvo] for p in ring]
    big = max(max(xs) - min(xs), max(ys) - min(ys))
    if big < 80 * ss:
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        r = max(34 * ss, big * 0.9)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=b.RED, width=7 * ss)
    return im.resize((w, h), Image.LANCZOS)


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
    b.text_outline(d, (760, 105), TITULO, nd.fit(d, TITULO, 104, 1050), b.YELLOW, w=10)
    b.selo(img, 1730, 105, 0.7)


def cartao_mapa(r, cor):
    """Cartão branco com o mapa (cor = laranja na pergunta, verde na resposta)."""
    x0, y0, x1, y1 = MAP_BOX
    w, h = x1 - x0, y1 - y0
    m = 30
    sp = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    sh = Image.new("RGBA", sp.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([m, m + 12, m + w, m + h + 12], 45, fill=(0, 0, 0, 100))
    sp.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(sp)
    d.rounded_rectangle([m, m, m + w, m + h], 45, fill=MAR, outline=b.NAVY, width=8)
    sp.alpha_composite(mapa(r["uf"], cor, w - 40, h - 40), (m + 20, m + 20))
    return sp


def tela(r, ops=True, revelado=False):
    img = fundo(r["n"])
    topo(img, r["n"])
    img.alpha_composite(cartao_mapa(r, VERDE if revelado else LARANJA), (MAP_BOX[0] - 30, MAP_BOX[1] - 30))
    if ops:
        for i, o in enumerate(r["op"]):
            bb.put_op(img, bb.opcao_sprite(i, o), i)
    return img


def faixa_capital(img, r, s=1.0):
    """Faixa amarela sobre o mapa: 'CAPITAL: CURITIBA'."""
    x0, y0, x1, y1 = MAP_BOX
    txt = f"CAPITAL: {r['capital'].upper()}"
    w, h = x1 - x0 - 60, 110
    sp = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(sp)
    d.rounded_rectangle([10, 14, w + 10, h + 14], 40, fill=(0, 0, 0, 110))
    d.rounded_rectangle([10, 10, w + 10, h + 10], 40, fill=b.YELLOW, outline=b.NAVY, width=7)
    d.text((w / 2 + 10, h / 2 + 10), txt, font=nd.fit(d, txt, 66, w - 60), fill=b.NAVY, anchor="mm")
    if s != 1.0:
        sp = sp.resize((max(1, int(sp.width * s)), max(1, int(sp.height * s))), Image.BILINEAR)
    nd.paste_c(img, sp, (x0 + x1) / 2, 975)  # no lugar da barra (que some na revelação)


def vinheta_frames(r):
    c1, c2 = CORES[r["n"] % len(CORES)]
    for i in range(int(nd.VINHETA * FPS)):
        t = i / FPS
        img = nd.burst(c1, c2, t * 30).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.25)
        b.text_outline(d, (W // 2, 250), "ESTADO", b.font(b.F_BLACK, int(110 * (0.4 + 0.6 * s))), b.WHITE, w=10)
        b.text_outline(d, (W // 2, 520), f"{r['n']:02d}", b.font(b.F_BLACK, int(330 * (0.4 + 0.6 * s))), b.YELLOW, w=18)
        b.text_outline(d, (W // 2, 820), TITULO, b.font(b.F_BLACK, int(80 * (0.4 + 0.6 * s))), b.WHITE, w=8)
        yield img.convert("RGB")


def pergunta_frames(r, fala):
    """Mapa entra, alternativas entram uma a uma, fala e 6 s de barra."""
    sem_ops = tela(r, ops=False)
    sps = [bb.opcao_sprite(i, o) for i, o in enumerate(r["op"])]
    n_in = int(0.7 * FPS)
    for i in range(n_in):
        t = i / FPS
        img = sem_ops.copy()
        for k, sp in enumerate(sps):
            tk = (t - 0.08 * k) / 0.25
            if tk <= 0:
                continue
            sc = 0.5 + 0.58 * tk if tk < 0.8 else (1.08 - 0.08 * min(1, (tk - 0.8) / 0.2))
            bb.put_op(img, sp, k, sc)
        bb.barra(img, 1.0)
        b.put_palito(img, "pensando", PAL_H, PAL_CX, PAL_BASE + int(max(0, 1 - t / 0.35) * 500))
        yield img.convert("RGB")
    base = sem_ops.copy()
    for k, sp in enumerate(sps):
        bb.put_op(base, sp, k)
    for i in range(max(0, int(fala * FPS) - n_in)):
        img = base.copy()
        bb.barra(img, 1.0)
        b.put_palito(img, "pensando", PAL_H, PAL_CX, PAL_BASE, int(6 * math.sin(i / FPS * 5)))
        yield img.convert("RGB")
    n = int(COUNT * FPS)
    for i in range(n):
        img = base.copy()
        frac = 1 - i / n
        bb.barra(img, frac)
        pose = "pensando" if frac > 0.17 else "assustado"
        b.put_palito(img, pose, PAL_H, PAL_CX, PAL_BASE, int(7 * math.sin(i / FPS * (5 if pose == "pensando" else 18))))
        yield img.convert("RGB")


def revela_frames(r, dur):
    c = r["certa"]
    base = tela(r, ops=False, revelado=True)
    for i, o in enumerate(r["op"]):
        if i != c:
            bb.put_op(base, bb.opcao_sprite(i, o, "apagada"), i)
    certa = bb.opcao_sprite(c, r["op"][c], "certa")
    for i in range(int(dur * FPS)):
        tt = i / FPS
        img = base.copy()
        if tt < 0.18:
            sc = 0.85 + 0.25 * tt / 0.18
        elif tt < 0.33:
            sc = 1.10 - 0.10 * (tt - 0.18) / 0.15
        else:
            sc = 1.0
        bb.put_op(img, certa, c, sc)
        fs = min(1.0, max(0.0, (tt - 0.25) / 0.2))
        if fs > 0:
            faixa_capital(img, r, 0.6 + 0.4 * fs)
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
        b.text_outline(d, (800, 230), f"{n} ESTADOS!", b.font(b.F_BLACK, int(110 * (0.5 + 0.5 * s))), b.WHITE, w=11)
        b.text_outline(d, (800, 420), "QUANTOS VOCÊ", b.font(b.F_BLACK, int(140 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
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
    b.text_outline(d, (540, 240), "QUE ESTADO", nd.fit(d, "QUE ESTADO", 140, 980), b.WHITE, w=13)
    b.text_outline(d, (540, 400), "É ESSE?", b.font(b.F_BLACK, 180), b.YELLOW, w=16)
    mp = mapa("PR", LARANJA, 400, 400)
    img.alpha_composite(mp, (1090, 150))
    passos = [(str(TOTAL), "ESTADOS DO BRASIL PELO MAPA"), ("4", "ALTERNATIVAS: A, B, C OU D"),
              ("6", "SEGUNDOS PARA RESPONDER")]
    d = ImageDraw.Draw(img)
    for k, (num, t) in enumerate(passos):
        y = 650 + k * 130
        d.ellipse([170, y - 55, 280, y + 55], fill=b.ORANGE, outline=b.WHITE, width=6)
        d.text((225, y), num, font=b.font(b.F_BLACK, 58), fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
        b.text_outline(d, (315, y), t, b.font(b.F_BLACK, 64), b.WHITE, w=8, anchor="lm")
    return img


def outro_base():
    img = fundo(3)
    d = ImageDraw.Draw(img)
    b.text_outline(d, (800, 200), "QUANTOS VOCÊ", b.font(b.F_BLACK, 120), b.WHITE, w=12)
    b.text_outline(d, (800, 345), "ACERTOU?", b.font(b.F_BLACK, 150), b.YELLOW, w=15)
    d.rounded_rectangle([450, 430, 1150, 545], 55, fill=(255, 255, 255, 240), outline=b.NAVY, width=7)
    d.text((800, 488), f"__ / {TOTAL}", font=b.font(b.F_BLACK, 80), fill=b.NAVY, anchor="mm")
    d.rounded_rectangle([290, 590, 1310, 710], 55, fill=b.RED, outline=b.WHITE, width=8)
    d.text((800, 650), "COMENTA SEU ESTADO!", font=b.font(b.F_BLACK, 64), fill=b.WHITE, anchor="mm",
           stroke_width=3, stroke_fill=b.NAVY)
    b.text_outline(d, (800, 790), "MANDA PRO AMIGO DA ESCOLA E INSCREVA-SE NO",
                   nd.fit(d, "MANDA PRO AMIGO DA ESCOLA E INSCREVA-SE NO", 54, 1400), b.WHITE, w=7)
    b.selo(img, 800, 910, 1.3)
    return img


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    quadros = [next(nd.anima(intro_base(), "acenando", 0.1)), list(vinheta_frames(R[2]))[-1]]
    for r in (R[0], R[9], R[16], R[26]):
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
    tmp = tempfile.mkdtemp(prefix="quiz_estados_")
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
        for f in revela_frames(r, max(2.8, dur(p) + 0.7)):
            tl.frame(f)
        if n in (10, 20):
            v = A(f"placar{n}.mp3")
            tl.sound(sfx["whoosh"])
            tl.sound(v, at=tl.t + 0.3)
            for f in placar_frames(n, dur(v) + 0.8):
                tl.frame(f)
        if n % 10 == 0:
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
