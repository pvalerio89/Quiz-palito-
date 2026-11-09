"""Prévia do modelo com opções A/B/C (fotos do vídeo 14).
Uso: py -3 previa.py          -> previa/layout-*.jpg
     py -3 previa.py --video  -> previa/amostra.mp4 (4 perguntas com som, 2 com vídeo)"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import opcoes as op

op.FOTOS = os.path.join(os.path.dirname(HERE), "14-tudo-amarelo", "fotos")
TOTAL = 60
Q = [
    {"n": 1, "pergunta": "Que lugar é esse?", "foto": "torre-eiffel.jpg",
     "opcoes": ["Big Ben", "Torre Eiffel", "Torre de Pisa"], "certa": 1},
    {"n": 8, "pergunta": "Que lugar é esse?", "foto": "piramides-do-egito.jpg",
     "opcoes": ["Pirâmides do Egito", "Chichén Itzá", "Petra"], "certa": 0},
    {"n": 23, "pergunta": "Que animal é esse?", "foto": "panda.jpg",
     "opcoes": ["Urso-polar", "Coala", "Panda"], "certa": 2},
]


def main():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = []
    a, c, p = Q
    fr.append(list(op.pergunta_frames(a, TOTAL))[int(op.COUNT * op.FPS * 0.4)])
    fr.append(list(op.resposta_frames(a, 1.0, TOTAL, t0=op.COUNT))[-1])
    fr.append(list(op.pergunta_frames(c, TOTAL))[int(op.COUNT * op.FPS * 0.8)])
    fr.append(list(op.resposta_frames(c, 1.0, TOTAL, t0=op.COUNT))[-1])
    fr.append(list(op.pergunta_frames(p, TOTAL, filtro="amarela"))[int(op.COUNT * op.FPS * 0.5)])
    for i, f in enumerate(fr, 1):
        f.save(os.path.join(out, f"layout-{i}.jpg"), quality=90)
    print(out)


def video():
    """Amostra com som: 4 perguntas (2 com vídeo curto), transições, efeitos e música."""
    import tempfile
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "05-nao-diga-o-mesmo"))
    import build_naodiga as nd
    b = op.b
    op.CLIPES = os.path.join(HERE, "clipes")
    qs = [
        dict(Q[0]),
        {"n": 2, "pergunta": "Que animal é esse?", "foto": "panda.jpg", "clipe": "panda.mp4",
         "opcoes": ["Panda", "Urso-pardo", "Guaxinim"], "certa": 0},
        dict(Q[1], n=3),
        {"n": 4, "pergunta": "Que animal é esse?", "foto": "panda.jpg", "clipe": "guepardo.mp4",
         "opcoes": ["Leopardo", "Onça-pintada", "Guepardo"], "certa": 2},
    ]
    tmp = tempfile.mkdtemp(prefix="opcoes_")
    sfx = op.make_sfx(tmp)
    v = os.path.join(tmp, "v.mp4")
    tl = b.Timeline(v)
    ultimo = None
    for q in qs:
        if ultimo is not None:
            tl.sound(sfx["whoosh"], vol=0.7)
            for f in op.transicao_frames(ultimo, q, TOTAL):
                tl.frame(f)
        op.sons_pergunta(tl, sfx, tl.t, entrada=ultimo is None)
        for f in op.pergunta_frames(q, TOTAL):
            tl.frame(f)
        for f in op.resposta_frames(q, 2.0, TOTAL, t0=op.COUNT):
            tl.frame(f)
            ultimo = f
    total = tl.t
    tl.close()
    out = os.path.join(HERE, "previa", "amostra.mp4")
    nd.A = lambda n: os.path.join(os.path.dirname(os.path.dirname(HERE)), "musicas", "Sneaky Snitch.mp3")
    nd.SAIDA = out
    nd.mixar(tl, v, total)
    print(out, f"{total:.1f}s")


if __name__ == "__main__":
    video() if "--video" in sys.argv else main()
