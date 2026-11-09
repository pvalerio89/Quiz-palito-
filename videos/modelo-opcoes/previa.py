"""Prévia do modelo com opções A/B/C (fotos do vídeo 14). Uso: py -3 previa.py -> previa/*.jpg"""
import os, sys
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
    fr.append(list(op.resposta_frames(a, 1.0, TOTAL))[-1])
    fr.append(list(op.pergunta_frames(c, TOTAL))[int(op.COUNT * op.FPS * 0.8)])
    fr.append(list(op.resposta_frames(c, 1.0, TOTAL))[-1])
    fr.append(list(op.pergunta_frames(p, TOTAL, filtro="amarela"))[int(op.COUNT * op.FPS * 0.5)])
    for i, f in enumerate(fr, 1):
        f.save(os.path.join(out, f"layout-{i}.jpg"), quality=90)
    print(out)


if __name__ == "__main__":
    main()
