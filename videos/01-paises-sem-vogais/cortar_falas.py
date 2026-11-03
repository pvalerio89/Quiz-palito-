"""Corta raw/qaN.mp3 (pergunta + pausa + resposta) em assets/qN.mp3 e assets/aN.mp3.

Escolhe a pausa mais longa perto do ponto esperado (proporção de letras da pergunta).
Uso: py -3 cortar_falas.py
"""
import json, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def silences(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "silencedetect=n=-35dB:d=0.2", "-f", "null", "-"],
                       capture_output=True, text=True)
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    dur = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).group(3)) + \
        60 * int(re.search(r"Duration: (\d+):(\d+)", r.stderr).group(2))
    return list(zip(st, en)), dur


def cut(src, dst, a, b):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                    "-af", "afade=t=in:d=0.02", dst], check=True)


def main():
    qs = json.load(open(os.path.join(HERE, "perguntas.json"), encoding="utf-8"))
    for q in qs:
        n = q["n"]
        raw = os.path.join(HERE, "raw", f"qa{n}.mp3")
        if not os.path.exists(raw):
            continue
        sil, dur = silences(raw)
        inner = [(s, e) for s, e in sil if s > 0.3 and e < dur - 0.2]
        if not inner:
            print(f"{n}: SEM PAUSA — conferir"); continue
        expected = dur * len(q["q"]) / (len(q["q"]) + len(q["a"]))
        longest = max(e - s for s, e in inner)
        cands = [(s, e) for s, e in inner if e - s >= 0.6 * longest]
        s, e = min(cands, key=lambda x: abs((x[0] + x[1]) / 2 - expected))
        cut(raw, os.path.join(HERE, "assets", f"q{n}.mp3"), 0, s + 0.08)
        cut(raw, os.path.join(HERE, "assets", f"a{n}.mp3"), max(0, e - 0.08), dur)
        print(f"{n:2d}: corte em {s:.2f}-{e:.2f}s de {dur:.2f}s (esperado ~{expected:.2f})")


if __name__ == "__main__":
    main()
