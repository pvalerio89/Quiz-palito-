"""Quiz Palito — vídeo 53 "NÃO DIGA O MESMO QUE O PALITO 2" (44 rodadas, 8 vidas, 10 a 13 min).

Mesmo jogo do vídeo 05 (o Palito tem uma resposta escondida; quem pensar igual perde uma vida), com pedidos NOVOS
e curtos (itens.py), placa de VIDAS grande à direita (TV), fundo turquesa/roxo/coral (cara diferente do 05),
intro rapidinha, transição SPLASH, pedido de inscrição/like, tela de última rodada e fim só com "inscreva-se"
(ESTILO MAIS HUMANO). O Palito não fala.
Uso: py -3 build_naodiga2.py            (monta quiz-palito-nao-diga-2.mp4)
     py -3 build_naodiga2.py --previa   (prancha em previa/)
     py -3 build_naodiga2.py --duracao  (só calcula a duração pelo tamanho das falas)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
import humano as hu
import motion
import engaja as eg
from opcoes import b, nd, W, H, FPS

R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-nao-diga-2.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Fluffing a Duck.mp3")
TITULO = "NÃO DIGA O MESMO QUE O PALITO"
GANCHO = "8 VIDAS: PENSOU IGUAL\nAO PALITO? PERDE UMA!"
CURTIR_DEPOIS = 3
VIDAS = 8
CORES = [((0, 170, 170), (0, 80, 110)), ((110, 60, 200), (45, 20, 110)), ((255, 110, 80), (190, 40, 70)),
         ((30, 140, 220), (15, 50, 130)), ((0, 160, 110), (0, 80, 70)), ((200, 60, 160), (100, 20, 90))]
CARD = (70, 215, 1310, 715)
FAIXA = (70, 750, 1310, 880)
BAR = (90, 925, 1290, 975)
VIDAS_BOX = (1345, 195, 1885, 515)
PAL_CX, PAL_BASE, PAL_H = 1615, 1065, 520


def count_de(r):
    return 5.0 if r["n"] <= 3 else 6.0


def dur(p):
    return b.duration(p) if os.path.exists(p) else 1.5


_cache = {}


def _mask():
    if "mask" not in _cache:
        _cache["mask"] = nd._mask()
    return _cache["mask"]


def fundo(k):
    key = ("fundo", k % len(CORES))
    if key not in _cache:
        c1, c2 = CORES[k % len(CORES)]
        img = b.gradient(c1, c2)
        img.paste(Image.new("RGB", (W, H), (255, 255, 255)), (0, 0), _mask())
        _cache[key] = img.convert("RGBA")
    return _cache[key].copy()


def placa_vidas(img, pulso=0.0):
    """Placa grande 'SUAS VIDAS' com 8 corações em 2 fileiras (lembrete para o público contar)."""
    x0, y0, x1, y1 = VIDAS_BOX
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0 + 6, y0 + 12, x1 + 6, y1 + 12], 36, fill=(0, 0, 0, 90))
    d.rounded_rectangle([x0, y0, x1, y1], 36, fill=(255, 255, 255, 245), outline=b.NAVY, width=7)
    d.text(((x0 + x1) / 2, y0 + 48), "SUAS VIDAS", font=b.font(b.F_BLACK, 52), fill=b.NAVY, anchor="mm")
    sz = int(84 * (1 + 0.08 * pulso))
    for fila in range(2):
        nd.coracoes(img, (x0 + x1) / 2, y0 + 128 + fila * 94, 4, sz, 26)
    d = ImageDraw.Draw(img)
    d.text(((x0 + x1) / 2, y1 - 30), "PENSOU IGUAL? TIRA 1!", font=b.font(b.F_BLACK, 30), fill=b.RED, anchor="mm")


def topo(img, n):
    d = ImageDraw.Draw(img)
    d.ellipse([30, 30, 170, 170], fill=b.ORANGE, outline=b.WHITE, width=8)
    d.text((100, 100), f"{n:02d}", font=b.font(b.F_BLACK, 66), fill=b.WHITE, anchor="mm", stroke_width=3,
           stroke_fill=b.NAVY)
    f = nd.fit(d, TITULO, 78, 1000)
    b.text_outline(d, (720, 100), TITULO, f, b.YELLOW, w=9)
    d.rounded_rectangle([1270, 62, 1500, 138], 38, fill=b.RED, outline=b.WHITE, width=6)
    d.text((1385, 100), "PARTE 2", font=b.font(b.F_BLACK, 44), fill=b.WHITE, anchor="mm", stroke_width=3,
           stroke_fill=b.NAVY)
    b.selo(img, 1730, 100, 0.65)


def cartao_sprite(r, revelado=False):
    key = ("cartao", r["n"], revelado)
    if key in _cache:
        return _cache[key]
    x0, y0, x1, y1 = CARD
    w, h = x1 - x0, y1 - y0
    m = 30
    sp = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    sh = Image.new("RGBA", sp.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([m, m + 12, m + w, m + h + 12], 50, fill=(0, 0, 0, 100))
    sp.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(sp)
    d.rounded_rectangle([m, m, m + w, m + h], 50, fill=b.WHITE, outline=b.NAVY, width=8)
    ecx, ecy = m + 240, m + h // 2
    d.ellipse([ecx - 180, ecy - 180, ecx + 180, ecy + 180], fill=(255, 220, 90) if revelado else (200, 240, 240),
              outline=b.NAVY, width=6)
    nd.paste_c(sp, nd.icone(r, 240, revelado), ecx, ecy)
    tx0, tx1 = m + 460, m + w - 50
    maxw = tx1 - tx0
    size = 104
    while True:
        f = b.font(b.F_BLACK, size)
        lin = nd.wrap(d, r["pedido"], f, maxw)
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
    _cache[key] = sp
    return sp


def faixa(img, r, revelado, pop=1.0):
    x0, y0, x1, y1 = FAIXA
    d = ImageDraw.Draw(img)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hw, hh = (x1 - x0) / 2 * pop, (y1 - y0) / 2 * pop
    d.rounded_rectangle([cx - hw + 6, cy - hh + 10, cx + hw + 6, cy + hh + 10], 55, fill=(0, 0, 0, 90))
    if not revelado:
        d.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh], 55, fill=b.NAVY, outline=b.WHITE, width=7)
        d.text((cx, cy - 4), "O PALITO PENSOU EM:  ? ? ?", font=b.font(b.F_BLACK, int(64 * pop)), fill=b.WHITE,
               anchor="mm")
        return
    d.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh], 55, fill=b.YELLOW, outline=b.WHITE, width=8)
    if pop >= 0.98:
        lbl = "PALITO DISSE:"
        fl = b.font(b.F_BLACK, 38)
        lw = d.textlength(lbl, font=fl)
        f = nd.fit(d, r["resposta"], 96, (x1 - x0) - lw - 140)
        aw = d.textlength(r["resposta"], font=f)
        x = cx - (lw + 30 + aw) / 2
        d.text((x, cy), lbl, font=fl, fill=b.NAVY, anchor="lm")
        d.text((x + lw + 30, cy - 4), r["resposta"], font=f, fill=b.NAVY, anchor="lm", stroke_width=2,
               stroke_fill=b.NAVY)


def barra(img, frac, count):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = BAR
    d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 32, fill=b.WHITE)
    d.rounded_rectangle(BAR, 24, fill=(60, 70, 110))
    if frac > 0.002:
        xe = x0 + (x1 - x0) * frac
        d.rounded_rectangle([x0, y0, max(xe, x0 + 48), y1], 24, fill=(0, 190, 170) if frac > 0.3 else b.RED)
    s = math.ceil(frac * count)
    if s > 0:
        d.text(((x0 + x1) // 2, (y0 + y1) // 2), str(s), font=b.font(b.F_BLACK, 40), fill=b.WHITE, anchor="mm",
               stroke_width=4, stroke_fill=b.NAVY)


def aviso_vida(img, k=1.0):
    d = ImageDraw.Draw(img)
    t = "PENSOU IGUAL? PERDEU 1 VIDA!"
    f = b.font(b.F_BLACK, 52)
    tw = d.textlength(t, font=f)
    cx = (BAR[0] + BAR[2]) / 2 - 30
    y = 952 + int((1 - k) * 140)
    d.rounded_rectangle([cx - tw / 2 - 30, y - 40, cx + tw / 2 + 100, y + 40], 40, fill=b.RED, outline=b.WHITE, width=6)
    d.text((cx - 4, y), t, font=f, fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
    nd.paste_c(img, nd.emoji("❤", 54), cx + tw / 2 + 50, y)


def tela(r, revelado=None, com_cartao=True):
    img = fundo(r["n"])
    topo(img, r["n"])
    placa_vidas(img)
    if com_cartao:
        img.alpha_composite(cartao_sprite(r, bool(revelado)), (CARD[0] - 30, CARD[1] - 30))
    return img


def primeiro_quadro(r):
    img = tela(r)
    faixa(img, r, False)
    barra(img, 1.0, count_de(r))
    b.put_palito(img, "pensando", PAL_H, PAL_CX, PAL_BASE)
    return img.convert("RGB")


def pergunta_frames(r, fala, gancho=None):
    count = count_de(r)
    base = tela(r)
    faixa(base, r, False)
    t_g = max(3.0, fala - 1.5)
    for i in range(int(fala * FPS)):
        t = i / FPS
        img = base.copy()
        barra(img, 1.0, count)
        b.put_palito(img, "pensando", PAL_H, PAL_CX, PAL_BASE, int(6 * math.sin(t * 5)))
        if gancho:
            eg.faixa_gancho(img, 690, 470, gancho, t, t_g, larg=1180, size=72)
        yield img.convert("RGB")
    n = int(count * FPS)
    for i in range(n):
        img = base.copy()
        frac = 1 - i / n
        barra(img, frac, count)
        pose = "pensando" if frac > 0.17 else "assustado"
        b.put_palito(img, pose, PAL_H, PAL_CX, PAL_BASE, int(7 * math.sin(i / FPS * (5 if pose == "pensando" else 18))))
        yield img.convert("RGB")


def revela_frames(r, d):
    base = tela(r, revelado=True)
    for i in range(int(d * FPS)):
        tt = i / FPS
        img = base.copy()
        pop = min(1.0, tt / 0.18)
        pop = 0.6 + 0.48 * pop if pop < 1 else max(1.0, 1.08 - (tt - 0.18) / 0.15 * 0.08)
        faixa(img, r, True, min(pop, 1.08) if tt < 0.33 else 1.0)
        if tt > 0.35:
            aviso_vida(img, min(1.0, (tt - 0.35) / 0.2))
        if tt < 0.2:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(160 * (1 - tt / 0.2)))))
        b.put_palito(img, "comemorando", PAL_H, PAL_CX, PAL_BASE, -int(abs(28 * math.sin(tt * 7))))
        z = 1.08 - 0.06 * min(1, tt / 0.5) if tt < 0.5 else 1.02
        yield op.zoom(img, z).convert("RGB")


def vidas_frames(n, d):
    c1, c2 = CORES[(n // 10) % len(CORES)]
    for i in range(int(d * FPS)):
        t = i / FPS
        img = nd.burst(c1, c2, t * 12).convert("RGBA")
        dd = ImageDraw.Draw(img)
        s = min(1.0, t / 0.3)
        b.text_outline(dd, (800, 220), f"{n} RODADAS!", b.font(b.F_BLACK, int(100 * (0.5 + 0.5 * s))), b.WHITE, w=10)
        b.text_outline(dd, (800, 380), "QUANTAS VIDAS", b.font(b.F_BLACK, int(130 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
        b.text_outline(dd, (800, 530), "AINDA SOBRARAM?", b.font(b.F_BLACK, int(120 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
        if s >= 1:
            dd.rounded_rectangle([230, 640, 1370, 790], 70, fill=(255, 255, 255, 240), outline=b.NAVY, width=7)
            nd.coracoes(img, 800, 715, VIDAS, 100, 30)
        b.selo(img, 800, 900, 1.1)
        b.put_palito(img, "apontando", 620, 1620 + int((1 - s) * 700), 1060, int(6 * math.sin(t * 5)))
        yield img.convert("RGB")


def curtir_frames(d, t_clique):
    """Pedido no meio: INSCREVA-SE + LIKE (Patrick, 2026-11-19: nada de 'coraçãozinho'/'joinha' na fala)."""
    like = nd.emoji("\U0001F44D", 260)
    for i in range(int(d * FPS)):
        t = i / FPS
        img = nd.burst((0, 170, 170), (0, 80, 110), t * 8).convert("RGBA")
        dd = ImageDraw.Draw(img)
        s = max(0.1, eg.pula(t / 0.4))
        aperta = t >= t_clique
        k = 1.0 + (0.18 * math.sin(min(1, (t - t_clique) / 0.35) * math.pi) if aperta else 0.04 * math.sin(t * 6))
        w2, h2 = int(820 * s * k), int(170 * s * k)
        cor = (150, 150, 150) if aperta else b.RED
        dd.rounded_rectangle([700 - w2 // 2, 300 - h2 // 2, 700 + w2 // 2, 300 + h2 // 2], 60, fill=cor,
                             outline=b.WHITE, width=9)
        dd.text((700, 302), "INSCRITO ✔" if aperta else "INSCREVA-SE", font=b.font(b.F_BLACK, max(8, int(96 * s * k))),
                fill=b.WHITE, anchor="mm", stroke_width=4, stroke_fill=b.NAVY)
        ent = eg.pula((t - 0.3) / 0.4)
        op.colar(img, like, 700, 600, ent * k)
        b.text_outline(dd, (700, 820), "DEIXA SEU LIKE!", b.font(b.F_BLACK, 80), b.WHITE, w=9)
        if aperta:
            b.text_outline(dd, (700, 960), "EU ESPERO!", b.font(b.F_BLACK, 90), b.YELLOW, w=10)
        b.put_palito(img, "apontando", 600, 1640, 1060, int(6 * math.sin(t * 6)))
        yield img.convert("RGB")


def curtir(tl, sfx, pausa=1.6):
    c1 = dur(A("curtir.mp3")) + 0.3
    tl.sound(sfx["whoosh"])
    tl.sound(A("curtir.mp3"), at=tl.t + 0.2)
    tl.sound(sfx["pop"], at=tl.t + c1 + pausa * 0.4, vol=0.9)
    tl.sound(sfx["acerto"], at=tl.t + c1 + pausa * 0.4 + 0.1, vol=0.5)
    tl.sound(A("espero.mp3"), at=tl.t + c1 + pausa)
    yield from curtir_frames(c1 + pausa + dur(A("espero.mp3")) + 0.6, c1 + pausa * 0.4)


def intro_frames(d):
    ims = [nd.emoji(e, 109).resize((150, 150)) for e in ("🍕", "🐶", "🎨", "⚽")]   # temas que não são respostas
    return op.intro_rapida("NÃO DIGA O MESMO", "QUE O PALITO!", d, fotos=ims, cor=2,
                          abertura=os.path.join(HERE, "abertura.jpg"))


def duracao():
    t = dur(A("intro.mp3")) + 0.4
    for r in R:
        n = r["n"]
        t += 1.0 + dur(A(f"q{n}.mp3")) + 0.35 + count_de(r) + max(2.6, dur(A(f"p{n}.mp3")) + 0.5)
        if n in (10, 20, 30):
            t += dur(A(f"vidas{n}.mp3")) + 0.8
    t += dur(A("curtir.mp3")) + 0.3 + 1.6 + dur(A("espero.mp3")) + 0.6
    t += dur(A("ultima.mp3")) + 0.8
    return t + dur(A("outro.mp3")) + 1.8 + 3


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[45]]
    for k in (0, 6, 14, 30, 43):
        r = R[k]
        f = dur(A(f"q{r['n']}.mp3")) + 0.35
        pf = list(pergunta_frames(r, f, GANCHO if k == 0 else None))
        fr.append(pf[20 if k == 0 else int((f + 2) * FPS)])
        fr.append(list(revela_frames(r, 1.2))[-1])
    fr.append(list(motion.transicao(fr[-1], primeiro_quadro(R[5]), "splash", n=6, total=TOTAL))[12])
    fr.append(list(vidas_frames(20, 0.5))[-1])
    fr.append(list(curtir_frames(3.0, 1.0))[-1])
    fr.append(list(hu.ultima_frames(1.0))[-1])
    fr.append(list(hu.inscreva_frames(1.0))[-1])
    cols = 3
    th = [f.resize((640, 360), Image.LANCZOS) for f in fr]
    pr = Image.new("RGB", (cols * 650, math.ceil(len(th) / cols) * 370), "black")
    for i, f in enumerate(th):
        pr.paste(f, ((i % cols) * 650, (i // cols) * 370))
    pr.save(os.path.join(out, "prancha.jpg"), quality=88)
    # todas as cartas reveladas, para conferir textos e emojis
    cs = [tela(r, True).convert("RGB").resize((480, 270)) for r in R]
    fo = Image.new("RGB", (4 * 485, math.ceil(len(cs) / 4) * 275), "black")
    for i, c in enumerate(cs):
        fo.paste(c, ((i % 4) * 485, (i // 4) * 275))
    fo.save(os.path.join(out, "cartas.jpg"), quality=80)
    print(out, f"duração estimada {duracao():.0f}s")


def main():
    tmp = tempfile.mkdtemp(prefix="quiz_naodiga2_")
    sfx = hu.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    marcas = {}
    di = dur(A("intro.mp3")) + 0.4
    tl.sound(A("intro.mp3"), at=0.15)
    ultimo = None
    for f in intro_frames(di):
        tl.frame(f)
        ultimo = f
    for r in R:
        n = r["n"]
        if n in (1, 11, 21, 31):
            marcas[str(n)] = tl.t
        if r.get("final"):
            for f in hu.ultima(tl, sfx, A("ultima.mp3")):
                tl.frame(f)
                ultimo = f
        motion.sons(tl, sfx, "splash")
        for f in motion.transicao(ultimo, primeiro_quadro(r), "splash", n=n, total=TOTAL):
            tl.frame(f)
        q = A(f"q{n}.mp3")
        fala = dur(q) + 0.35
        count = count_de(r)
        t0 = tl.t
        tl.sound(q, at=t0 + 0.1)
        for s in range(int(count)):
            tl.sound(sfx["tick"], at=t0 + fala + s, vol=0.8)
            if s >= count - 2:
                tl.sound(sfx["tique"], at=t0 + fala + s + 0.5, vol=0.6)
        if r.get("final"):
            for k in range(int((fala + count) / 0.8)):
                tl.sound(sfx["coracao"], at=t0 + k * 0.8, vol=0.6)
        for f in pergunta_frames(r, fala, GANCHO if n == 1 else None):
            tl.frame(f)
        p = A(f"p{n}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(p, at=tl.t + 0.25)
        for f in revela_frames(r, max(2.6, dur(p) + 0.5)):
            tl.frame(f)
            ultimo = f
        if n == CURTIR_DEPOIS:
            for f in curtir(tl, sfx):
                tl.frame(f)
                ultimo = f
        if n in (10, 20, 30):
            v = A(f"vidas{n}.mp3")
            tl.sound(sfx["whoosh"])
            tl.sound(v, at=tl.t + 0.3)
            for f in vidas_frames(n, dur(v) + 0.8):
                tl.frame(f)
                ultimo = f
            print(f"{n}/{TOTAL} ({tl.t / 60:.1f} min)", flush=True)
    marcas["final"] = tl.t
    for f in hu.inscreva(tl, sfx, A("outro.mp3")):
        tl.frame(f)
    total = tl.t
    tl.close()
    json.dump(marcas, open(os.path.join(HERE, "tempos.json"), "w", encoding="utf-8"), indent=1)
    nd.HERE, nd.SAIDA = HERE, SAIDA
    nd.A = lambda x: MUSICA if x == "musica.mp3" else A(x)
    nd.mixar(tl, video, total)
    print(f"OK {SAIDA} ({total:.1f}s)")


if __name__ == "__main__":
    if "--duracao" in sys.argv:
        print(f"{duracao():.1f}s")
    elif "--previa" in sys.argv:
        previa()
    else:
        main()
