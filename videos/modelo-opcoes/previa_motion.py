"""Amostras das transições em motion graphics (motion.py), com as perguntas e vozes do vídeo 50.
Uso: py -3 previa_motion.py               -> previa/motion-<estilo>.mp4 (os 3 estilos) + previa/motion-prancha.jpg
     py -3 previa_motion.py raios         -> só um estilo
     py -3 previa_motion.py --short raios -> amostra 9:16 com as perguntas do Short brasil-2"""
import json, os, sys, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import opcoes as op
import humano as hu
import motion
from opcoes import b, nd, FPS

V50 = os.path.join(VIDEOS, "50-quiz-brasil-2")
op.FOTOS = os.path.join(V50, "fotos")
op.CORES = [((20, 150, 70), (5, 80, 40)), ((30, 90, 200), (10, 35, 120)), ((225, 165, 10), (150, 95, 0))]
R = json.load(open(os.path.join(V50, "itens.json"), encoding="utf-8"))
A = lambda n: os.path.join(V50, "assets", n)
TOTAL = len(R)
OUT = os.path.join(HERE, "previa")
ESTILOS_PRANCHA = ("splash",)


def q_de(r):
    return {k: r[k] for k in ("n", "pergunta", "foto", "opcoes", "certa")}


def amostra(estilo):
    tmp = tempfile.mkdtemp(prefix="motion_")
    sfx = motion.make_sfx(tmp, hu.make_sfx(tmp))
    v = os.path.join(tmp, "v.mp4")
    tl = b.Timeline(v)
    ultimo = None
    for idx, r in enumerate(R[3:6]):
        q = q_de(r)
        if ultimo is not None:
            motion.sons(tl, sfx, estilo)
            for f in motion.transicao(ultimo, op.primeiro_quadro(q, TOTAL), estilo, n=q["n"], total=TOTAL):
                tl.frame(f)
        vq = A(f"q{r['n']}.mp3")
        fala = hu.dur(vq) + 0.3
        t0 = tl.t
        tl.sound(vq, at=t0 + 0.1)
        cnt = 2.0
        op.sons_pergunta(tl, sfx, t0, fala=fala, count=cnt, entrada=False)
        for f in hu.pergunta_frames(q, TOTAL, fala, cnt):
            tl.frame(f)
        tl.sound(sfx["acerto"], at=tl.t, vol=0.8)
        vr = A(f"p{r['n']}.mp3")
        tl.sound(vr, at=tl.t + 0.3)
        for f in hu.resposta_frames(q, TOTAL, hu.dur(vr) + 0.8):
            tl.frame(f)
            ultimo = f
    total = tl.t
    tl.close()
    out = os.path.join(OUT, f"motion-{estilo}.mp4")
    nd.HERE, nd.SAIDA = V50, out
    nd.A = lambda x: os.path.join(os.path.dirname(VIDEOS), "musicas", "Fluffing a Duck.mp3") if x == "musica.mp3" else A(x)
    nd.mixar(tl, v, total)
    print(out, f"{total:.1f}s")


def prancha():
    """6 quadros de cada estilo (uma linha por estilo)."""
    a = list(hu.resposta_frames(q_de(R[3]), TOTAL, 1.0))[-1]
    d = op.primeiro_quadro(q_de(R[4]), TOTAL)
    linhas = []
    for e in motion.ESTILOS:
        if e not in ESTILOS_PRANCHA:
            linhas.append(None)
            continue
        fr = list(motion.transicao(a, d, e, n=5, total=TOTAL))
        pick = [fr[int(k * (len(fr) - 1) / 9)] for k in range(10)]
        linhas.append(pick)
    if ESTILOS_PRANCHA != motion.ESTILOS:
        linhas = [ln for e, ln in zip(motion.ESTILOS, linhas) if e in ESTILOS_PRANCHA]
    tw, th = 480, 270
    sheet = Image.new("RGB", (10 * (tw + 8), len(linhas) * (th + 8)), (25, 25, 25))
    for y, ln in enumerate(linhas):
        for x, f in enumerate(ln):
            sheet.paste(f.resize((tw, th)), (x * (tw + 8), y * (th + 8)))
    sheet.save(os.path.join(OUT, "motion-prancha-" + "-".join(ESTILOS_PRANCHA) + ".jpg"), quality=85)


def amostra_short(estilo):
    """Short 9:16 (brasil-2, 3 primeiras perguntas) com a transição entre as perguntas."""
    sys.path.insert(0, os.path.join(os.path.dirname(VIDEOS), "shorts", "brasil-2"))
    import build_short as bs
    s = bs.s
    tmp = tempfile.mkdtemp(prefix="motion_short_")
    sfx = motion.make_sfx(tmp, b.make_sfx(tmp))
    v = os.path.join(tmp, "v.mp4")
    tl = s.Timeline(v)
    ultimo = None
    for k, p in enumerate(bs.PERG[:3], 1):
        q = bs.A(f"q{k}.mp3")
        fala = s.duracao(q) + 0.2
        if ultimo is not None:
            motion.sons(tl, sfx, estilo)
            for f in motion.transicao(ultimo, next(bs.pergunta_frames(k, p, fala)), estilo, n=k, total=len(bs.PERG)):
                tl.frame(f)
        tl.sound(q, at=tl.t + 0.1, voz=True)
        for c in range(int(bs.COUNT)):
            tl.sound(sfx["tick"], at=tl.t + fala + c, vol=0.8)
        for f in bs.pergunta_frames(k, p, fala):
            tl.frame(f)
        a = bs.A(f"a{k}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(a, at=tl.t + 0.15, voz=True)
        for f in bs.resposta_frames(k, p, s.duracao(a) + 0.7):
            tl.frame(f)
            ultimo = f
    tl.close()
    out = os.path.join(OUT, f"motion-short-{estilo}.mp4")
    s.mixar(tl, v, bs.MUSICA, out)
    print(out, f"{tl.t:.1f}s")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    if "--prancha" in sys.argv:
        prancha()
    elif "--short" in sys.argv:
        for e in (args or ["splash"]):
            amostra_short(e)
    else:
        for e in (args or motion.ESTILOS):
            amostra(e)
