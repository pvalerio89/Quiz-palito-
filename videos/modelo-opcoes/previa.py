"""Prévia do modelo com opções A/B/C (fotos do vídeo 14).
Uso: py -3 previa.py          -> previa/layout-*.jpg
     py -3 previa.py --video  -> previa/amostra.mp4 (3 perguntas, sem som)"""
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
    out = os.path.join(HERE, "previa", "amostra.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{op.W}x{op.H}", "-r", str(op.FPS), "-i", "-", "-c:v", "libx264", "-crf", "23",
                           "-preset", "medium", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for q, filtro in ((Q[0], None), (Q[1], None), (Q[2], "amarela")):
        for f in op.pergunta_frames(q, TOTAL, filtro=filtro):
            pr.stdin.write(f.tobytes())
        for f in op.resposta_frames(q, 2.0, TOTAL, filtro_antes=filtro, t0=op.COUNT):
            pr.stdin.write(f.tobytes())
    pr.stdin.close()
    pr.wait()
    print(out)


if __name__ == "__main__":
    video() if "--video" in sys.argv else main()
