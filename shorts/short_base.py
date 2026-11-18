"""Base dos Shorts do Quiz Palito (vertical 1080x1920).

Reaproveita o build.py do quiz de países (fontes, cores, Palito, selo, sons) com
linha do tempo e mixagem próprias para a tela em pé.
Área segura: evitar o topo (até ~150 px), a faixa de baixo (abaixo de ~1580 px)
e a coluna de botões da direita (x > 940 entre y 900 e 1600).
"""
import math, os, random, subprocess, sys
from PIL import Image, ImageDraw

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(QP, "videos", "01-paises-sem-vogais"))
import build as b

b.PERSONAGEM = os.path.join(QP, "personagem")
W, H, FPS = 1080, 1920, 30
BAR = (90, 1090, 990, 1150)
MUSICA_VOL = 0.14

# Frases de chamada da abertura/título. Variar entre Shorts (Patrick, 2026-11-09): não repetir as dos
# últimos 3 Shorts (títulos em publicados.json). "SÓ 1% ACERTA" saiu da lista (análise do canal, 2026-11-17).
CHAMADAS = [
    "DUVIDO VOCÊ ACERTAR TODAS!",
    "QUASE NINGUÉM ACERTA A ÚLTIMA!",
    "SÓ GÊNIO ACERTA TODAS!",
    "VALENDO! QUANTAS VOCÊ ACERTA?",
    "SERÁ QUE VOCÊ GABARITA?",
    "TESTE RÁPIDO: VOCÊ PASSA?",
    "A ÚLTIMA É MUITO DIFÍCIL!",
    "SEU AMIGO NÃO ACERTA ESSA!",
    "ACERTOU TODAS? COMENTA!",
    "SE ACERTAR 4, VOCÊ É FERA!",
    "SEU PAI ACERTA ESSAS?",
]


def chamada(usadas=(), seed=None):
    """Escolhe uma frase de CHAMADAS que não está em `usadas` (frases dos últimos Shorts)."""
    usadas = {u.upper() for u in usadas}
    livres = [c for c in CHAMADAS if c.upper() not in usadas] or CHAMADAS
    return random.Random(seed).choice(livres)


def gradient(c1, c2):
    img = Image.new("RGB", (W, H), c1)
    d = ImageDraw.Draw(img)
    for i in range(H):
        t = i / (H - 1)
        d.line([(0, i), (W, i)], fill=tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3)))
    return img


def fundo(c1=b.BLUE, c2=b.NAVY, seed=7):
    """Degradê com o padrão de '?' e globinhos do canal."""
    img = gradient(c1, c2)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = b.font(b.F_BLACK, 70)
    rnd = random.Random(seed)
    for y in range(-40, H, 150):
        for x in range(-40, W, 170):
            ox = x + (85 if (y // 150) % 2 else 0) + rnd.randint(-10, 10)
            if rnd.random() < 0.5:
                d.text((ox, y), "?", font=f, fill=(255, 255, 255, 28))
            else:
                d.ellipse([ox, y + 15, ox + 55, y + 70], outline=(255, 255, 255, 28), width=5)
                d.line([ox + 27, y + 15, ox + 27, y + 70], fill=(255, 255, 255, 28), width=4)
                d.line([ox, y + 42, ox + 55, y + 42], fill=(255, 255, 255, 28), width=4)
    img.paste(layer, (0, 0), layer)
    return img


def burst(c1, c2, rot):
    img = Image.new("RGB", (W, H), c2)
    d = ImageDraw.Draw(img)
    cx, cy, R = W / 2, H / 2, 2600
    for k in range(24):
        a0, a1 = math.radians(k * 15 + rot), math.radians(k * 15 + 7.5 + rot)
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)),
                   (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=c1 if k % 2 else c2)
    return img


def texto(d, xy, txt, size, cor, w=None, max_w=980):
    f = b.font(b.F_BLACK, size)
    while d.textlength(txt, font=f) > max_w and f.size > 30:
        f = b.font(b.F_BLACK, f.size - 4)
    b.text_outline(d, xy, txt, f, cor, w=w or max(5, f.size // 9))


def pilula(d, cx, cy, txt, cor, size=48, pad=40, h=None):
    f = b.font(b.F_BLACK, size)
    tw = d.textlength(txt, font=f)
    h = h or int(size * 1.7)
    d.rounded_rectangle([cx - tw / 2 - pad, cy - h / 2, cx + tw / 2 + pad, cy + h / 2], h // 2,
                        fill=cor, outline=b.WHITE, width=6)
    d.text((cx, cy), txt, font=f, fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)


def trilho(img):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = BAR
    d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 40, fill=b.WHITE)
    d.rounded_rectangle(BAR, 30, fill=(60, 70, 110))


def barra(base, frac, total, t=0.0, palito=True):
    """Barra de tempo + Palito pensando (assustado no fim)."""
    img = base.copy().convert("RGBA")
    if palito:
        pose = "pensando" if frac > 0.3 else "assustado"
        dy = int(8 * math.sin(t * 2 * math.pi * (0.8 if pose == "pensando" else 3)))
        b.put_palito(img, pose, 280, 540, 1560, dy)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = BAR
    if frac > 0.002:
        xe = x0 + (x1 - x0) * frac
        d.rounded_rectangle([x0, y0, max(xe, x0 + 60), y1], 30, fill=b.ORANGE if frac > 0.3 else b.RED)
    s = math.ceil(frac * total)
    if s > 0:
        d.text(((x0 + x1) // 2, (y0 + y1) // 2), str(s), font=b.font(b.F_BLACK, 48), fill=b.WHITE,
               anchor="mm", stroke_width=4, stroke_fill=b.NAVY)
    return img.convert("RGB")


class Timeline:
    def __init__(self, path):
        self.t, self.n, self.audio = 0.0, 0, []
        self.proc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)

    def frame(self, img):
        self.proc.stdin.write(img.convert("RGB").tobytes())
        self.n += 1
        self.t = self.n / FPS

    def hold(self, img, secs):
        raw = img.convert("RGB").tobytes()
        for _ in range(int(round(secs * FPS))):
            self.proc.stdin.write(raw)
            self.n += 1
        self.t = self.n / FPS

    def sound(self, path, at=None, vol=1.0, voz=False):
        if path and os.path.exists(path):
            self.audio.append((path, self.t if at is None else at, vol, voz))

    def close(self):
        self.proc.stdin.close()
        self.proc.wait()


def duracao(p):
    return b.duration(p) if os.path.exists(p) else 1.5


def mixar(tl, video, musica, out):
    """Narração + efeitos + música que abaixa quando o narrador fala."""
    import numpy as np
    sr, total = 44100, tl.t
    buf = np.zeros((int((total + 1) * sr), 2), dtype=np.float32)
    voz = np.zeros(len(buf), dtype=np.float32)
    dec = lambda p: np.frombuffer(subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"],
        capture_output=True).stdout, dtype=np.float32).reshape(-1, 2)
    cache = {}
    for pth, at, vol, eh_voz in tl.audio:
        x = cache.setdefault(pth, dec(pth)) * vol
        i0 = int(at * sr)
        i1 = min(len(buf), i0 + len(x))
        buf[i0:i1] += x[: i1 - i0]
        if eh_voz:
            voz[i0:i1] = 1.0
    n = int(total * sr)
    buf, voz = buf[:n], voz[:n]
    if musica and os.path.exists(musica):
        m = dec(musica)
        m = np.tile(m, (n // len(m) + 1, 1))[:n].copy()
        k = int(0.25 * sr)
        env = np.convolve(voz, np.ones(k, dtype=np.float32) / k, mode="same")
        ganho = MUSICA_VOL * (1.0 - 0.55 * np.clip(env, 0, 1))
        fi, fo = int(0.3 * sr), int(1.0 * sr)
        ganho[:fi] *= np.linspace(0, 1, fi)
        ganho[-fo:] *= np.linspace(1, 0, fo)
        buf += m * ganho[:, None]
    peak = float(np.abs(buf).max()) or 1.0
    if peak > 0.98:
        buf *= 0.98 / peak
    raw = os.path.splitext(video)[0] + ".f32"
    buf.tofile(raw)
    b.run(["ffmpeg", "-y", "-i", video, "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", raw, "-map", "0:v",
           "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out])


def intro_rapida(titulo, sub, dur, imagens=(), cores=((255, 150, 0), (200, 60, 0))):
    """Intro RAPIDINHA do Short (2 a 3 s; Patrick, 2026-11-10): selo, tema, até 4 fotos e o Palito acenando.
    Fale por cima só o tema, curtinho (FALAS["intro"]); a chamada vem na faixa da 1ª pergunta."""
    sys.path.insert(0, os.path.join(QP, "videos", "modelo-opcoes"))
    import engaja as eg
    bs = fundo(*cores, seed=11).convert("RGBA")
    linhas = [(titulo, b.WHITE)] + ([(sub, b.YELLOW)] if sub else [])
    return eg.intro_rapida_frames(lambda t: bs.copy(), linhas, dur, W, H, cy0=470, passo=150,
                                  tamanhos=[100, 130][:len(linhas)], palito=(640, 540, 1560), selo=(540, 250, 1.1),
                                  imagens=list(imagens)[:4], img_y=830, img_lado=200)
