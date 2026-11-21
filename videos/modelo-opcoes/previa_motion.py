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
        fr = list(motion.transicao(a, d, e, n=5, total=TOTAL))
        pick = [fr[int(k * (len(fr) - 1) / 5)] for k in range(6)]
        linhas.append(pick)
    tw, th = 480, 270
    sheet = Image.new("RGB", (6 * (tw + 8), len(linhas) * (th + 8)), (25, 25, 25))
    for y, ln in enumerate(linhas):
        for x, f in enumerate(ln):
            sheet.paste(f.resize((tw, th)), (x * (tw + 8), y * (th + 8)))
    sheet.save(os.path.join(OUT, "motion-prancha.jpg"), quality=85)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    if "--prancha" in sys.argv:
        prancha()
    else:
        for e in (args or motion.ESTILOS):
            amostra(e)
