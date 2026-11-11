"""Quiz Palito — "MONTE O TIME" (mais de 8 min, para anúncio no meio).

6 times de finais famosas (Brasil 2002, Real Madrid 2017, Argentina 2022, Barcelona 2011, Espanha 2010, Brasil 1970).
Posição por posição: "Quem era o goleiro?" com 3 alternativas A/B/C; o campinho do cartão vai se completando com a
escalação. No fim de cada time, tela "TIME COMPLETO!" com os 11. Dados em dados.py, perguntas em itens.json.
Layout aprovado `videos/modelo-opcoes/opcoes.py` (intro rapidinha, chamada na 1ª pergunta, placar, sons, transição).
Uso: py -3 build_monte.py            (monta quiz-palito-monte-o-time.mp4)
     py -3 build_monte.py --previa   (prancha em previa/)
     py -3 build_monte.py --duracao  (só calcula a duração pelo tamanho das falas)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
sys.path.insert(0, HERE)
import opcoes as op
from opcoes import b, nd, W, H, FPS
from dados import TIMES

R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-monte-o-time.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Carefree.mp3")
GANCHO = "MONTE O TIME CAMPEÃO:\nSÓ CRAQUE SABE TODOS!"
LADO = op.CARD - 40
_cache = {}


def icone(ti, lado):
    tipo, k = TIMES[ti]["img"].split(":")
    im = Image.open(os.path.join(HERE, "fotos", f"{tipo}-{k}.png")).convert("RGBA")
    im.thumbnail((lado, lado), Image.LANCZOS)
    return im


def slot_xy(x, y, lado):
    return 34 + x * (lado - 68), 118 + y * (lado - 168)


def campo_base(ti, k, revelado, lado=LADO, todos=False):
    """Campo com cabeçalho do time e os jogadores já descobertos (o slot atual é desenhado à parte).
    `todos`: mostra todos menos o slot atual (Short "quem falta?")."""
    key = ("campo", ti, k, revelado, lado, todos)
    if key in _cache:
        return _cache[key]
    tm = TIMES[ti]
    img = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, lado, 92], fill=tm["cor"])
    ic = icone(ti, 72)
    img.alpha_composite(ic, (14 + (72 - ic.width) // 2, 10 + (72 - ic.height) // 2))
    b.text_outline(d, (100, 30), tm["nome"], b.font(b.F_BLACK, 36), b.WHITE, w=4, anchor="lm")
    b.text_outline(d, (100, 68), tm["sub"], b.font(b.F_BLACK, 26), b.YELLOW, w=4, anchor="lm")
    for i in range(8):                       # gramado listrado
        y0 = 92 + i * (lado - 92) / 8
        d.rectangle([0, y0, lado, y0 + (lado - 92) / 8], fill=(46, 160, 70) if i % 2 else (38, 145, 62))
    m, top, bot = 14, 104, lado - 12
    cor = (235, 255, 235)
    d.rectangle([m, top, lado - m, bot], outline=cor, width=4)
    my = (top + bot) / 2
    d.line([m, my, lado - m, my], fill=cor, width=4)
    d.ellipse([lado / 2 - 56, my - 56, lado / 2 + 56, my + 56], outline=cor, width=4)
    for yy, s in ((top, 1), (bot, -1)):
        y0, y1 = sorted([yy, yy + s * 70])
        d.rectangle([lado / 2 - 130, y0, lado / 2 + 130, y1], outline=cor, width=4)
    f = b.font(b.F_BLACK, max(21, lado // 24))
    for i, j in enumerate(tm["jog"]):
        cx, cy = slot_xy(j[4], j[5], lado)
        if i < k or (todos and i != k) or (i == k and revelado):
            d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=b.WHITE, outline=tm["cor"], width=7)
            tw = d.textlength(j[2], font=f)
            d.rounded_rectangle([cx - tw / 2 - 9, cy + 20, cx + tw / 2 + 9, cy + 22 + f.size * 1.3], 12, fill=b.WHITE,
                                outline=b.NAVY, width=3)
            d.text((cx, cy + 22 + f.size * 0.65), j[2], font=f, fill=b.NAVY, anchor="mm")
        elif i != k:
            d.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], fill=(255, 255, 255, 70), outline=(255, 255, 255, 200), width=3)
    if len(_cache) > 40:
        _cache.clear()
    _cache[key] = img
    return img


def campo(ti, k, revelado, t, lado=LADO, todos=False):
    img = campo_base(ti, k, revelado, lado, todos).copy()
    if not revelado and k < 11:
        j = TIMES[ti]["jog"][k]
        cx, cy = slot_xy(j[4], j[5], lado)
        r = 24 + 4 * math.sin(t * 8)
        d = ImageDraw.Draw(img)
        d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], fill=(255, 240, 120, 110))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=b.YELLOW, outline=b.NAVY, width=5)
        d.text((cx, cy + 1), "?", font=b.font(b.F_BLACK, 34), fill=b.NAVY, anchor="mm")
    return img


class Campo:
    """Faz o papel do 'clipe' do modelo: campo com o slot atual piscando; na resposta, o nome aparece."""

    def __init__(self, r, n_perg):
        self.r, self.n_perg, self.i = r, n_perg, 0

    def cartao(self):
        t = self.i / FPS
        self.i += 1
        sp = op.moldura_sprite().copy()
        sp.alpha_composite(campo(self.r["time"], self.r["slot"], self.i > self.n_perg, t), (50, 50))
        return sp

    def fechar(self):
        pass


def q_de(r, fala=0.0):
    q = {"n": r["n"], "pergunta": r["pergunta"], "foto": None, "clipe": True, "opcoes": r["opcoes"], "certa": r["certa"]}
    q["_clipe"] = Campo(r, int((fala + op.COUNT) * FPS))
    return q


def completo_frames(ti, dur):
    """Fim de cada time: o campo inteiro grande + 'QUANTOS VOCÊ ACERTOU? __ / 11'."""
    tm = TIMES[ti]
    cp = campo(ti, 11, True, 0, 820)
    fr = Image.new("RGBA", (860, 860), (0, 0, 0, 0))
    ImageDraw.Draw(fr).rounded_rectangle([0, 0, 859, 859], 40, fill=b.WHITE, outline=b.NAVY, width=8)
    fr.alpha_composite(cp, (20, 20))
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = nd.burst(tm["cor"], tuple(int(c * 0.5) for c in tm["cor"]), t * 10).convert("RGBA")
        s = min(1.0, t / 0.35)
        op.colar(img, fr, 520, 545, 0.3 + 0.7 * op.pula(s))
        d = ImageDraw.Draw(img)
        b.text_outline(d, (1420, 250), "TIME COMPLETO!", b.font(b.F_BLACK, 76), b.YELLOW, w=10)
        b.text_outline(d, (1420, 380), "QUANTOS VOCÊ", b.font(b.F_BLACK, 72), b.WHITE, w=9)
        b.text_outline(d, (1420, 470), "ACERTOU?", b.font(b.F_BLACK, 90), b.WHITE, w=10)
        d.rounded_rectangle([1180, 550, 1660, 660], 55, fill=b.WHITE, outline=b.NAVY, width=7)
        d.text((1420, 605), "__ / 11", font=b.font(b.F_BLACK, 76), fill=b.NAVY, anchor="mm")
        b.put_palito(img, "comemorando", 400, 1420, 1080, -int(abs(20 * math.sin(t * 6))))
        yield img.convert("RGB")


def outro_base():
    img = op.fundo(3).copy()
    d = ImageDraw.Draw(img)
    b.text_outline(d, (800, 200), "QUANTOS VOCÊ", b.font(b.F_BLACK, 120), b.WHITE, w=12)
    b.text_outline(d, (800, 345), "ACERTOU?", b.font(b.F_BLACK, 150), b.YELLOW, w=15)
    d.rounded_rectangle([450, 430, 1150, 545], 55, fill=(255, 255, 255, 240), outline=b.NAVY, width=7)
    d.text((800, 488), f"__ / {TOTAL}", font=b.font(b.F_BLACK, 80), fill=b.NAVY, anchor="mm")
    d.rounded_rectangle([250, 590, 1350, 710], 55, fill=b.RED, outline=b.WHITE, width=8)
    d.text((800, 650), "PAUSA E COMENTA SUA NOTA!", font=b.font(b.F_BLACK, 62), fill=b.WHITE, anchor="mm",
           stroke_width=3, stroke_fill=b.NAVY)
    b.text_outline(d, (800, 790), "MARCA UM AMIGO E INSCREVA-SE NO", b.font(b.F_BLACK, 54), b.WHITE, w=7)
    b.selo(img, 800, 910, 1.3)
    return img


def creditos_base():
    img = Image.new("RGBA", (W, H), (20, 24, 48, 255))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 380), "CRÉDITOS DAS IMAGENS", font=b.font(b.F_BLACK, 50), fill=b.YELLOW, anchor="mm")
    d.text((W / 2, 480), "Bandeiras: domínio público (Wikimedia Commons).", font=b.font(b.F_BOLD, 36), fill=b.WHITE, anchor="mm")
    d.text((W / 2, 545), "Escudos: Real_Madrid_CF.svg e FC_Barcelona_(crest).svg — marcas dos clubes (Wikipédia).",
           font=b.font(b.F_BOLD, 30), fill=b.WHITE, anchor="mm")
    d.text((W / 2, 660), "Vídeo de quiz sem ligação com clubes, seleções ou jogadores.", font=b.font(b.F_BOLD, 28),
           fill=(180, 180, 200), anchor="mm")
    return img


dur = lambda p: b.duration(p) if os.path.exists(p) else 1.2
RESP = lambda n: max(1.6, dur(A(f"p{n}.mp3")) + 0.6)


def duracao():
    t = dur(A("intro.mp3"))
    for r in R:
        t += 0.6 + op.COUNT + RESP(r["n"])
        if r["slot"] == 0:
            t += dur(A(f"q{r['n']}.mp3")) + 0.2
        if r["slot"] == 10:
            t += dur(A(f"completo{r['time']}.mp3")) + 1.0
    return t + max(4.0, dur(A("outro.mp3")) + 1.8) + 5


def gancho(r):
    tm = TIMES[r["time"]]
    if r["n"] == 1:
        return GANCHO
    return f"TIME {r['time'] + 1}: {tm['nome']}\n{tm['sub']}"


INTRO_TIMES = [0, 1, 2, 3, 4]


def intro_frames(d):
    return op.intro_rapida("MONTE O TIME", "CAMPEÃO!", d, fotos=[icone(i, 170) for i in (0, 1, 2, 3, 4)])


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40], list(op.pergunta_frames(q_de(R[0], 3.0), TOTAL, fala=3.0, gancho=GANCHO))[15]]
    for k in (5, 11, 27, 40, 52, 65):
        f = 3.0 if R[k]["slot"] == 0 else 0.0
        pf = list(op.pergunta_frames(q_de(R[k], f), TOTAL, fala=f, gancho=gancho(R[k]) if f else None))
        fr.append(pf[20])
        q = q_de(R[k], f)
        q["_clipe"].i = 10 ** 6
        fr.append(list(op.resposta_frames(q, 1.0, TOTAL, t0=op.COUNT))[-1])
    fr.append(list(op.transicao_frames(fr[-1], q_de(R[6]), TOTAL))[9])
    for ti in range(len(TIMES)):
        fr.append(list(completo_frames(ti, 0.5))[-1])
    fr.append(next(nd.anima(outro_base().convert("RGBA"), "acenando", 0.1)))
    fr.append(creditos_base().convert("RGB"))
    cols = 3
    th = [f.resize((640, 360), Image.LANCZOS) for f in fr]
    pr = Image.new("RGB", (cols * 650, math.ceil(len(th) / cols) * 370), "black")
    for i, f in enumerate(th):
        pr.paste(f, ((i % cols) * 650, (i // cols) * 370))
    pr.save(os.path.join(out, "prancha.jpg"), quality=88)
    print(out, f"duração estimada {duracao():.0f}s")


def main():
    tmp = tempfile.mkdtemp(prefix="quiz_monte_")
    sfx = op.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    marcas = {}
    tl.sound(A("intro.mp3"), at=0.15)     # intro rapidinha (Patrick, 2026-11-10)
    ultimo = None
    for f in intro_frames(dur(A("intro.mp3"))):
        tl.frame(f)
        ultimo = f
    for r in R:
        n = r["n"]
        novo_time = r["slot"] == 0
        if novo_time:
            marcas[str(r["time"])] = tl.t
        fala = dur(A(f"q{n}.mp3")) + 0.2 if novo_time else 0.0
        q = q_de(r, fala)
        if ultimo is not None:
            tl.sound(sfx["whoosh"], vol=0.7)
            for f in op.transicao_frames(ultimo, q_de(r), TOTAL):
                tl.frame(f)
        if novo_time:   # nome do time (e, na 1ª, a chamada) falado por cima da pergunta
            tl.sound(A(f"q{n}.mp3"), at=tl.t + 0.1)
        op.sons_pergunta(tl, sfx, tl.t, fala=fala, entrada=ultimo is None)
        for f in op.pergunta_frames(q, TOTAL, fala=fala, gancho=gancho(r) if novo_time else None):
            tl.frame(f)
        tl.sound(A(f"p{n}.mp3"), at=tl.t + 0.25)
        for f in op.resposta_frames(q, RESP(n), TOTAL, t0=fala + op.COUNT):
            tl.frame(f)
            ultimo = f
        if r["slot"] == 10:
            v = A(f"completo{r['time']}.mp3")
            tl.sound(sfx["whoosh"])
            tl.sound(v, at=tl.t + 0.3)
            for f in completo_frames(r["time"], dur(v) + 1.0):
                tl.frame(f)
            ultimo = None
            print(f"{n}/{TOTAL} ({tl.t / 60:.1f} min)", flush=True)
    marcas["final"] = tl.t
    tl.sound(sfx["whoosh"])
    tl.sound(A("outro.mp3"), at=tl.t + 0.4)
    for f in nd.anima(outro_base().convert("RGBA"), "acenando", max(4.0, dur(A("outro.mp3")) + 1.8)):
        tl.frame(f)
    cr = creditos_base().convert("RGB")
    for _ in range(int(4 * FPS)):
        tl.frame(cr)
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
