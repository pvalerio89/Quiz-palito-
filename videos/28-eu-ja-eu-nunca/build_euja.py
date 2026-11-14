"""Quiz Palito — vídeo 28 "EU JÁ ou EU NUNCA?" (mais de 8 min, para anúncio no meio).

Formato de ESCOLHA (sem resposta certa): "EU JÁ..." + frase com emoji grande e dois botões, EU JÁ ✅ e
EU NUNCA ❌, pulsando na contagem. Na revelação os botões viram barras com a % de quem disse cada um.
Chamada de anotar nos comentários logo depois da intro (engaja; Patrick, 2026-11-12).
Fundo, transição, sons e telas de curtida/última/inscreva vêm de `modelo-opcoes/opcoes.py` e `humano.py`
(ESTILO MAIS HUMANO; o Palito não fala).
Uso: py -3 build_euja.py            (monta quiz-palito-eu-ja-eu-nunca.mp4)
     py -3 build_euja.py --previa   (prancha em previa/)
     py -3 build_euja.py --duracao  (só calcula a duração pelo tamanho das falas)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
import humano as hu
import engaja as eg
from opcoes import b, nd, W, H, FPS

R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-eu-ja-eu-nunca.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Fluffing a Duck.mp3")
GANCHO = f"{TOTAL} FRASES:\nNÃO VALE MENTIR!"
CURTIR_DEPOIS = 3
VERDE, VERMELHO = (40, 175, 80), (225, 50, 60)
CARD = (110, 215, 1470, 655)          # cartão da frase
BTN_W, BTN_H = 620, 165
BTN_C = ((470, 780), (1110, 780))    # centro dos botões EU JÁ / EU NUNCA
BAR = (130, 905, 1450, 950)
PAL_CX, PAL_BASE, PAL_H = 1715, 1040, 520
_cache = {}


def topo(img, r):
    d = ImageDraw.Draw(img)
    d.ellipse([40, 28, 190, 178], fill=b.ORANGE, outline=b.WHITE, width=8)
    d.text((115, 101), f"{r['n']:02d}", font=b.font(b.F_BLACK, 70), fill=b.WHITE, anchor="mm", stroke_width=3,
           stroke_fill=b.NAVY)
    b.text_outline(d, (790, 92), "EU JÁ OU EU NUNCA?", b.font(b.F_BLACK, 86), b.YELLOW, w=10)
    d.text((790, 168), f"FRASE {r['n']} DE {TOTAL}", font=b.font(b.F_BLACK, 34), fill=b.WHITE, anchor="mm",
           stroke_width=4, stroke_fill=b.NAVY)
    b.selo(img, 1730, 100, 0.7)


def base(r, t):
    k = ("topo", r["n"])
    if k not in _cache:
        for c in [c for c in _cache if c[0] == "topo"]:
            _cache.pop(c)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        topo(lay, r)
        _cache[k] = lay
    img = op.fundo(r["n"], t)
    img.alpha_composite(_cache[k])
    return img


def cartao_sprite(r):
    """Cartão branco: emoji grande à esquerda, 'EU JÁ...' e a frase à direita (só o da frase atual fica guardado)."""
    k = ("cartao", r["n"])
    if k not in _cache:
        for c in [c for c in _cache if c[0] == "cartao"]:
            _cache.pop(c)
        x0, y0, x1, y1 = CARD
        w, h = x1 - x0, y1 - y0
        sp = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
        b.shadowed_round_rect(sp, (30, 30, 30 + w, 30 + h), 56, b.WHITE)
        d = ImageDraw.Draw(sp)
        d.rounded_rectangle([30, 30, 30 + w, 30 + h], 56, outline=b.NAVY, width=8)
        em = nd.emoji(r["emoji"], 300)
        sp.alpha_composite(em, (int(30 + 210 - em.width / 2), int(30 + h / 2 - em.height / 2)))
        tx0, tw = 30 + 420, w - 450
        d.text((tx0, 95), "EU JÁ...", font=b.font(b.F_BLACK, 74), fill=(220, 40, 60), anchor="lm")
        txt = r["frase"].upper()
        f = b.font(b.F_BLACK, 76)
        linhas = nd.wrap(d, txt, f, tw)
        while (len(linhas) > 3 or max(d.textlength(l, font=f) for l in linhas) > tw) and f.size > 34:
            f = b.font(b.F_BLACK, f.size - 3)
            linhas = nd.wrap(d, txt, f, tw)
        cy = 30 + 95 + (h - 95) / 2 + 10
        y = cy - (len(linhas) - 1) * f.size * 0.6
        for i, l in enumerate(linhas):
            d.text((tx0, y + i * f.size * 1.2), l, font=f, fill=b.NAVY, anchor="lm")
        _cache[k] = sp
    return _cache[k]


def botao_sprite(lado, pct=None, frac=1.0, destaque=False):
    """lado 0 = EU JÁ (verde), 1 = EU NUNCA (vermelho). Com pct: barra enchendo até pct*frac e a % escrita."""
    cor = VERDE if lado == 0 else VERMELHO
    rot = "EU JÁ" if lado == 0 else "EU NUNCA"
    ic = "✅" if lado == 0 else "❌"
    key = ("btn", lado)
    if pct is None and key in _cache:
        return _cache[key]
    cv = Image.new("RGBA", (BTN_W + 60, BTN_H + 60), (0, 0, 0, 0))
    x0, y0, x1, y1 = 30, 30, 30 + BTN_W, 30 + BTN_H
    if destaque:
        g = Image.new("RGBA", cv.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).rounded_rectangle([x0 - 18, y0 - 18, x1 + 18, y1 + 18], 80, fill=(255, 240, 120, 220))
        cv.alpha_composite(g.filter(ImageFilter.GaussianBlur(14)))
    if pct is None:
        b.shadowed_round_rect(cv, (x0, y0, x1, y1), 70, cor)
    else:
        b.shadowed_round_rect(cv, (x0, y0, x1, y1), 70, (40, 45, 75))
        xe = x0 + BTN_W * pct / 100 * frac
        if xe > x0 + 4:
            m = Image.new("L", cv.size, 0)
            ImageDraw.Draw(m).rounded_rectangle([x0, y0, x1, y1], 70, fill=255)
            barra = Image.new("L", cv.size, 0)
            ImageDraw.Draw(barra).rectangle([x0, y0, xe, y1], fill=255)
            from PIL import ImageChops
            cv.paste(cor + (255,), (0, 0), ImageChops.multiply(m, barra))
    d = ImageDraw.Draw(cv)
    d.rounded_rectangle([x0, y0, x1, y1], 70, outline=b.WHITE, width=8)
    if pct is None:
        e = nd.emoji(ic, 92)
        cv.alpha_composite(e, (x0 + 40, int(y0 + BTN_H / 2 - e.height / 2)))
        f = nd.fit(d, rot, 84, BTN_W - 210)
        d.text((x0 + 150 + (BTN_W - 170) / 2, y0 + BTN_H / 2), rot, font=f, fill=b.WHITE, anchor="mm",
               stroke_width=5, stroke_fill=b.NAVY)
        _cache[key] = cv
    else:
        v = pct if lado == 0 else 100 - pct
        d.text((x0 + BTN_W / 2, y0 + 52), rot, font=b.font(b.F_BLACK, 46), fill=b.WHITE, anchor="mm",
               stroke_width=4, stroke_fill=b.NAVY)
        d.text((x0 + BTN_W / 2, y0 + 118), f"{round(v * frac)}%", font=b.font(b.F_BLACK, 80), fill=b.YELLOW,
               anchor="mm", stroke_width=5, stroke_fill=b.NAVY)
    return cv


def barra(img, frac, count):
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


def contador(img, r, t, respondida=False):
    bloco = (r["n"] - 1) // 10
    feitas = (r["n"] - 1) % 10 + (1 if respondida else 0)
    eg.pontos(img, 930, 1012, feitas, min(10, TOTAL - bloco * 10), t, raio=25, gap=18,
              rotulo="CONTA SEUS \"EU JÁ\"!", rotulo_size=38, rotulo_acima=False)


CC = ((CARD[0] + CARD[2]) // 2, (CARD[1] + CARD[3]) // 2)


def frase_frames(r, fala, count, gancho=None):
    d_total = fala + count
    for i in range(int(d_total * FPS)):
        t = i / FPS
        frac = 1.0 if t < fala else 1 - (t - fala) / count
        img = base(r, t)
        op.colar(img, cartao_sprite(r), CC[0], CC[1] + 6 * math.sin(t * 2.2), op.pula(t / 0.4))
        for k in range(2):
            ent = op.pula((t - 0.35 - 0.15 * k) / 0.35)
            pulso = 1 + (0.05 * math.sin(t * 7 + k * math.pi) if t > fala else 0)
            dx = 5 * math.sin(t * 40 + k) if frac < 0.3 else 0
            op.colar(img, botao_sprite(k), BTN_C[k][0] + dx, BTN_C[k][1], ent * pulso)
        barra(img, frac, count)
        contador(img, r, t)
        pose, mexe = ("pensando", 5) if frac > 0.3 else ("assustado", 18)
        b.put_palito(img, pose, PAL_H, PAL_CX, PAL_BASE, int(7 * math.sin(t * mexe)))
        if gancho:
            eg.faixa_gancho(img, 790, 122, gancho, t, max(fala, 2.5), larg=1350, size=78)
        yield op.zoom(img, 1.0 + 0.03 * t / d_total).convert("RGB")


def revela_frames(r, d):
    pct = r["pct"]
    maior = 0 if pct >= 50 else 1
    for i in range(int(d * FPS)):
        tt = i / FPS
        img = base(r, tt)
        op.colar(img, cartao_sprite(r), CC[0], CC[1])
        fr = min(1.0, tt / 0.8)
        fr = fr * fr * (3 - 2 * fr)
        for k in range(2):
            sc = 1.0 + (0.08 * math.sin(min(tt / 0.4, 1) * math.pi) + 0.03 if k == maior else 0)
            op.colar(img, botao_sprite(k, pct, fr, destaque=(k == maior and tt > 0.8)), BTN_C[k][0], BTN_C[k][1], sc)
        contador(img, r, tt, respondida=True)
        if tt > 0.8:
            eg.faixa_gancho(img, 790, 900, "E VOCÊ? ANOTA AÍ!", tt - 0.8, 99, larg=700, size=46,
                            cor=(40, 60, 150))
        b.put_palito(img, "comemorando" if pct >= 50 else "assustado", PAL_H, PAL_CX, PAL_BASE,
                     -int(abs(22 * math.sin(tt * 7))))
        if tt < 0.2:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(130 * (1 - tt / 0.2)))))
        z = 1.08 - 0.05 * min(1, tt / 0.5) if tt < 0.5 else 1.03 + 0.02 * tt / d
        yield op.zoom(img, z).convert("RGB")


def primeiro_quadro(r):
    img = base(r, 0.0)
    barra(img, 1.0, 4)
    contador(img, r, 0.0)
    b.put_palito(img, "pensando", PAL_H, PAL_CX, PAL_BASE, 0)
    return img.convert("RGB")


def transicao(antes, r):
    q = {"n": r["n"], "pergunta": "", "opcoes": [], "certa": 0}
    velho = op.primeiro_quadro
    op.primeiro_quadro = lambda q_, total: primeiro_quadro(r)
    try:
        yield from op.transicao_frames(antes, q, TOTAL)
    finally:
        op.primeiro_quadro = velho


def anotar_frames(d):
    """Chamada de anotar: coração, balão de comentário e lápis gigantes."""
    ems = [nd.emoji(e, 260) for e in ("❤️", "💬", "✍️")]
    for i in range(int(d * FPS)):
        t = i / FPS
        img = nd.burst((40, 110, 220), (15, 40, 140), t * 8).convert("RGBA")
        dd = ImageDraw.Draw(img)
        s = max(0.1, eg.pula(t / 0.4))
        b.text_outline(dd, (760, 150), "VAI ANOTANDO!", b.font(b.F_BLACK, int(140 * s)), b.WHITE, w=14)
        for j, e in enumerate(ems):
            ent = eg.pula((t - 0.3 - 0.35 * j) / 0.4)
            op.colar(img, e, 360 + j * 400, 500 + 12 * math.sin(t * 4 + j), ent * (1 + 0.05 * math.sin(t * 6 + j)))
        if t > 1.5:
            b.text_outline(dd, (760, 800), "CONTA QUANTOS \"EU JÁ\" VOCÊ TEM", b.font(b.F_BLACK, 66), b.YELLOW, w=8)
            b.text_outline(dd, (760, 900), "E MANDA NO FINAL!", b.font(b.F_BLACK, 66), b.WHITE, w=8)
        b.put_palito(img, "apontando", 600, 1660, 1060, int(6 * math.sin(t * 6)))
        yield img.convert("RGB")


def placar_frames(n, d):
    for i in range(int(d * FPS)):
        t = i / FPS
        img = nd.burst((255, 170, 0), (215, 100, 0), t * 12).convert("RGBA")
        dd = ImageDraw.Draw(img)
        s = 0.5 + 0.5 * min(1.0, t / 0.3)
        b.text_outline(dd, (800, 230), f"{n} FRASES!", b.font(b.F_BLACK, int(120 * s)), b.WHITE, w=11)
        b.text_outline(dd, (800, 420), "QUANTOS \"EU JÁ\"", b.font(b.F_BLACK, int(130 * s)), b.YELLOW, w=14)
        b.text_outline(dd, (800, 570), "VOCÊ TEM?", b.font(b.F_BLACK, int(140 * s)), b.YELLOW, w=14)
        if s >= 1:
            dd.rounded_rectangle([420, 680, 1180, 800], 60, fill=(255, 255, 255, 240), outline=b.NAVY, width=7)
            dd.text((800, 740), f"__ / {n}", font=b.font(b.F_BLACK, 80), fill=b.NAVY, anchor="mm")
        b.selo(img, 800, 910, 1.1)
        b.put_palito(img, "apontando", 620, 1620 + int((1 - min(1, t / 0.3)) * 700), 1060, int(6 * math.sin(t * 5)))
        yield img.convert("RGB")


def intro_frames(d):
    ims = [nd.emoji(e, 170) for e in ("✅", "❌", "🤔", "😱")]
    return op.intro_rapida("EU JÁ OU", "EU NUNCA?", d, fotos=ims)


dur = lambda p: b.duration(p) if os.path.exists(p) else 1.2


def duracao():
    t = dur(A("intro.mp3")) + 0.4 + dur(A("anotar.mp3")) + 0.8
    for r in R:
        n = r["n"]
        t += 0.6 + dur(A(f"q{n}.mp3")) + 0.3 + r["count"] + dur(A(f"p{n}.mp3")) + 1.1
        if n % 10 == 0 and n < TOTAL:
            t += dur(A(f"placar{n}.mp3")) + 0.8
    t += dur(A("curtir.mp3")) + 0.3 + 1.6 + dur(A("espero.mp3")) + 0.6
    t += dur(A("ultima.mp3")) + 0.8
    return t + dur(A("outro.mp3")) + 1.8


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40], list(anotar_frames(3.0))[-1]]
    for k in (0, 3, 15, 30, 44, 49):
        r = R[k]
        f = dur(A(f"q{r['n']}.mp3")) + 0.3
        pf = list(frase_frames(r, f, r["count"], GANCHO if k == 0 else None))
        fr += [pf[15], pf[min(len(pf) - 1, int((f + 2.5) * FPS))]]
        fr.append(list(revela_frames(r, 2.0))[-1])
    fr.append(list(transicao(fr[-1], R[5]))[9])
    fr.append(list(placar_frames(10, 0.5))[-1])
    fr.append(list(hu.curtir_frames(3.0, 1.0))[-1])
    fr.append(list(hu.ultima_frames(1.0))[-1])
    fr.append(list(hu.inscreva_frames(1.0))[-1])
    cols = 3
    th = [f.resize((640, 360), Image.LANCZOS) for f in fr]
    pr = Image.new("RGB", (cols * 650, math.ceil(len(th) / cols) * 370), "black")
    for i, f in enumerate(th):
        pr.paste(f, ((i % cols) * 650, (i // cols) * 370))
    pr.save(os.path.join(out, "prancha.jpg"), quality=88)
    print(out, f"duração estimada {duracao():.0f}s")


def main():
    tmp = tempfile.mkdtemp(prefix="quiz_euja_")
    sfx = hu.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    marcas = {}
    di = dur(A("intro.mp3")) + 0.4
    tl.sound(A("intro.mp3"), at=0.15)   # intro rapidinha (Patrick, 2026-11-10)
    ultimo = None
    for f in intro_frames(di):
        tl.frame(f)
        ultimo = f
    tl.sound(sfx["whoosh"])
    tl.sound(A("anotar.mp3"), at=tl.t + 0.2)   # chamada de anotar nos comentários (Patrick, 2026-11-12)
    for f in anotar_frames(dur(A("anotar.mp3")) + 0.8):
        tl.frame(f)
        ultimo = f
    for r in R:
        n = r["n"]
        if n in (1, 11, 21, 31, 41):
            marcas[str(n)] = tl.t
        if r.get("final"):
            for f in hu.ultima(tl, sfx, A("ultima.mp3")):
                tl.frame(f)
                ultimo = f
        tl.sound(sfx["whoosh"], vol=0.7)
        for f in transicao(ultimo, r):
            tl.frame(f)
        t0 = tl.t
        vq = A(f"q{n}.mp3")
        fala = dur(vq) + 0.3
        tl.sound(vq, at=t0 + 0.1)
        for k in range(2):
            tl.sound(sfx["pop"], at=t0 + 0.35 + 0.15 * k, vol=0.7)
        for s in range(int(r["count"])):
            tl.sound(sfx["tick"], at=t0 + fala + s, vol=0.7)
            if s >= r["count"] - 2:
                tl.sound(sfx["tique"], at=t0 + fala + s + 0.5, vol=0.6)
        if r.get("final"):
            for k in range(int((fala + r["count"]) / 0.8)):
                tl.sound(sfx["coracao"], at=t0 + k * 0.8, vol=0.6)
        for f in frase_frames(r, fala, r["count"], GANCHO if n == 1 else None):
            tl.frame(f)
        tl.sound(sfx["acerto"], vol=0.7)
        vr = A(f"p{n}.mp3")
        tl.sound(vr, at=tl.t + 0.3)
        for f in revela_frames(r, dur(vr) + 1.1):
            tl.frame(f)
            ultimo = f
        if n == CURTIR_DEPOIS:
            for f in hu.curtir(tl, sfx, A("curtir.mp3"), A("espero.mp3")):
                tl.frame(f)
                ultimo = f
        if n % 10 == 0 and n < TOTAL:
            v = A(f"placar{n}.mp3")
            tl.sound(sfx["whoosh"])
            tl.sound(v, at=tl.t + 0.3)
            for f in placar_frames(n, dur(v) + 0.8):
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
