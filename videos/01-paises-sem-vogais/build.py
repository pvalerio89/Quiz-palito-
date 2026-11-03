"""Gera o vídeo de teste do quiz "países sem vogais".

Uso: py -3 -I build.py <pasta_assets> <saida.mp4>
A pasta de assets deve ter: intro.mp3, q1.mp3, a1.mp3, ... e foto1.jpg ...
Se faltar algum arquivo, usa silêncio / foto de placeholder.
"""
import json, math, os, random, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
W, H, FPS = 1920, 1080, 30
FONTS = "C:/Windows/Fonts/"
F_BLACK = FONTS + "seguibl.ttf"   # Segoe UI Black
F_BOLD = FONTS + "segoeuib.ttf"

# Identidade visual própria
NAVY = (18, 32, 84)
BLUE = (34, 86, 196)
TEAL = (0, 190, 200)
ORANGE = (255, 140, 0)
YELLOW = (255, 206, 40)
RED = (235, 50, 50)
WHITE = (255, 255, 255)

PERSONAGEM = os.path.join(QP, "personagem")
_pcache = {}


def palito(pose, height):
    """Pose do Palito recortada, escalada e com borda branca de adesivo."""
    key = (pose, height)
    if key in _pcache:
        return _pcache[key]
    im = Image.open(os.path.join(PERSONAGEM, "poses", f"pose-{pose}.png")).convert("RGBA")
    im = im.crop(im.getbbox())
    r = height / im.height
    im = im.resize((int(im.width * r), height), Image.LANCZOS)
    pad = 22
    canvas = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    canvas.paste(im, (pad, pad), im)
    a = canvas.getchannel("A").point(lambda v: 255 if v > 20 else 0)
    outline = a.filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.GaussianBlur(1.5))
    shadow = outline.filter(ImageFilter.GaussianBlur(10)).point(lambda v: v * 0.45)
    out = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 255)); sh.putalpha(shadow)
    out.alpha_composite(sh, (0, 0))
    wh = Image.new("RGBA", canvas.size, (255, 255, 255, 255)); wh.putalpha(outline)
    out.alpha_composite(wh)
    out.alpha_composite(canvas)
    _pcache[key] = out
    return out


def put_palito(img, pose, height, cx, bottom, dy=0):
    p = palito(pose, height)
    img.paste(p, (int(cx - p.width / 2), int(bottom - p.height + dy)), p)


def selo(img, cx, cy, scale=1.0):
    """Selo do canal: QUIZ PALITO."""
    d = ImageDraw.Draw(img)
    f = font(F_BLACK, int(52 * scale))
    w1 = d.textlength("QUIZ ", font=f)
    w2 = d.textlength("PALITO", font=f)
    tw = w1 + w2
    pw, ph = tw + 70 * scale, 92 * scale
    x0, y0 = cx - pw / 2, cy - ph / 2
    d.rounded_rectangle([x0 + 6 * scale, y0 + 8 * scale, x0 + pw + 6 * scale, y0 + ph + 8 * scale], int(ph / 2), fill=NAVY)
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], int(ph / 2), fill=WHITE, outline=NAVY, width=max(3, int(6 * scale)))
    tx = cx - tw / 2
    d.text((tx, cy), "QUIZ ", font=f, fill=ORANGE, anchor="lm")
    d.text((tx + w1, cy), "PALITO", font=f, fill=NAVY, anchor="lm")


MUSICA_VOL = 0.14  # volume da música de fundo (0 a 1)
COUNTDOWN = 10.0   # segundos de contagem
REVEAL_MIN = 3.5   # duração mínima da revelação
VINHETA = 1.0

QUESTIONS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "perguntas.json"), encoding="utf-8"))


def font(path, size):
    return ImageFont.truetype(path, size)


def gradient(c1, c2, vertical=True):
    img = Image.new("RGB", (W, H), c1)
    d = ImageDraw.Draw(img)
    n = H if vertical else W
    for i in range(n):
        t = i / (n - 1)
        c = tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
        if vertical:
            d.line([(0, i), (W, i)], fill=c)
        else:
            d.line([(i, 0), (i, H)], fill=c)
    return img


def pattern_bg():
    """Fundo azul com padrão discreto de '?' e globinhos."""
    img = gradient(BLUE, NAVY)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = font(F_BLACK, 70)
    rnd = random.Random(7)
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


def text_outline(d, xy, text, f, fill, outline=NAVY, w=8, anchor="mm"):
    d.text(xy, text, font=f, fill=fill, anchor=anchor, stroke_width=w, stroke_fill=outline)


def shadowed_round_rect(img, box, radius, fill, shadow=(0, 0, 0, 90), off=10):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0, y0 + off, x1, y1 + off], radius, fill=shadow)
    layer = layer.filter(ImageFilter.GaussianBlur(6))
    img.paste(layer, (0, 0), layer)
    ImageDraw.Draw(img).rounded_rectangle(box, radius, fill=fill)


BAR = (140, 930, W - 140, 990)  # trilho da barra de tempo


def draw_tiles(img, tiles, cy, max_w=1380, max_size=190, cx=W // 2):
    words = tiles.split("/")
    n = sum(len(w) for w in words)
    gap, wgap = 0.16, 0.7  # proporções do tamanho da peça
    units = n + gap * (n - len(words)) + wgap * (len(words) - 1)
    size = int(min(max_size, max_w / units))
    total = size * units
    x = cx - total / 2
    ft = font(F_BLACK, int(size * 0.68))
    for wi, word in enumerate(words):
        for ch in word:
            x0, y0 = int(x), int(cy - size / 2)
            shadowed_round_rect(img, (x0, y0, x0 + size, y0 + size), int(size * 0.15), WHITE)
            d = ImageDraw.Draw(img)
            if ch == "_":
                m = int(size * 0.24)
                d.rounded_rectangle([x0 + m, y0 + size - int(size * 0.32), x0 + size - m, y0 + size - int(size * 0.22)],
                                    int(size * 0.04), fill=(170, 180, 200))
            else:
                d.text((x0 + size // 2, y0 + size // 2 - int(size * 0.04)), ch, font=ft, fill=NAVY, anchor="mm")
            x += size * (1 + gap)
        x += size * (wgap - gap)


def question_base(q):
    img = pattern_bg().convert("RGBA")
    d = ImageDraw.Draw(img)
    text_outline(d, (W // 2, 110), "QUE PAÍS É ESSE?", font(F_BLACK, 96), YELLOW, w=10)
    d.ellipse([50, 40, 200, 190], fill=ORANGE, outline=WHITE, width=8)
    d.text((125, 112), f"{q['n']:02d}", font=font(F_BLACK, 70), fill=WHITE, anchor="mm")
    selo(img, 1690, 112, 0.75)
    draw_tiles(img, q["tiles"].replace(" ", ""), 495, cx=860)
    d = ImageDraw.Draw(img)
    text_outline(d, (860, 720), "SEM AS VOGAIS!", font(F_BLACK, 60), WHITE, w=6)
    x0, y0, x1, y1 = BAR
    d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 40, fill=WHITE)
    d.rounded_rectangle(BAR, 32, fill=(60, 70, 110))
    return img.convert("RGB")


def bar_frame(base, frac, t=0.0):
    img = base.copy()
    pose = "pensando" if frac > 0.3 else "assustado"
    dy = int(8 * math.sin(t * 2 * math.pi * (0.8 if pose == "pensando" else 3)))
    put_palito(img, pose, 400, 1700, 900, dy)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = BAR
    if frac > 0.002:
        xe = x0 + (x1 - x0) * frac
        color = ORANGE if frac > 0.3 else RED
        d.rounded_rectangle([x0, y0, max(xe, x0 + 64), y1], 32, fill=color)
    secs = math.ceil(frac * COUNTDOWN)
    d.text((W // 2, (y0 + y1) // 2), str(secs) if secs > 0 else "", font=font(F_BLACK, 48), fill=WHITE,
           anchor="mm", stroke_width=4, stroke_fill=NAVY)
    return img


def burst_bg(rot):
    img = Image.new("RGB", (W, H), ORANGE)
    d = ImageDraw.Draw(img)
    cx, cy, R = W / 2, H / 2, 2400
    for i in range(24):
        a0 = math.radians(i * 15 + rot)
        a1 = math.radians(i * 15 + 7.5 + rot)
        col = (255, 170, 30) if i % 2 else (245, 120, 0)
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)),
                   (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=col)
    return img


def vinheta_frames(n):
    frames = int(VINHETA * FPS)
    for i in range(frames):
        t = i / frames
        img = burst_bg(t * 20)
        d = ImageDraw.Draw(img)
        # pop: cresce rápido e assenta
        s = min(1.0, t / 0.25)
        scale = 0.4 + 0.75 * s - 0.15 * max(0, s - 0.8) / 0.2 if t < 0.25 else 1.0
        size = int(380 * scale)
        text_outline(d, (W // 2, H // 2 - 40), f"{n:02d}", font(F_BLACK, size), WHITE, outline=NAVY, w=max(6, size // 18))
        selo(img, W // 2, 900, 0.9)
        img = img.convert("RGBA")
        put_palito(img, "apontando", 520, 420 - int((1 - s) * 600), 960)
        img = img.convert("RGB")
        d = ImageDraw.Draw(img)
        # saída: barra branca varrendo
        if t > 0.8:
            k = (t - 0.8) / 0.2
            d.rectangle([0, 0, int(W * k), H], fill=WHITE)
        yield img


def intro_base():
    img = gradient(TEAL, BLUE).convert("RGBA")
    d = ImageDraw.Draw(img)
    selo(img, 820, 120, 1.25)
    d = ImageDraw.Draw(img)
    text_outline(d, (820, 340), "ADIVINHE 40 PAÍSES", font(F_BLACK, 130), WHITE, w=12)
    text_outline(d, (820, 510), "SEM AS VOGAIS", font(F_BLACK, 150), YELLOW, w=14)
    draw_tiles(img, "BR_S_L", 760, max_size=150, cx=820)
    put_palito(img, "acenando", 700, 1640, 1050)
    return img.convert("RGB")


def reveal_frames(photo_path, answer, dur):
    if photo_path and os.path.exists(photo_path):
        ph = Image.open(photo_path).convert("RGB")
    else:
        ph = gradient((90, 160, 90), (30, 90, 140))
    # recorte 16:9 preenchendo a tela
    r = max(W / ph.width, H / ph.height)
    ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1), Image.LANCZOS)
    left, top = (ph.width - W) // 2, (ph.height - H) // 2
    ph = ph.crop((left, top, left + W, top + H))
    blurred = ph.filter(ImageFilter.GaussianBlur(30))
    frames = int(dur * FPS)
    fa = font(F_BLACK, 130)
    for i in range(frames):
        t = i / FPS
        k = min(1.0, t / 0.5)  # desfocado -> nítido em 0,5 s
        img = Image.blend(blurred, ph, k)
        # zoom lento
        z = 1.0 + 0.04 * (i / frames)
        zw, zh = int(W / z), int(H / z)
        img = img.crop(((W - zw) // 2, (H - zh) // 2, (W - zw) // 2 + zw, (H - zh) // 2 + zh)).resize((W, H))
        img = img.convert("RGBA")
        slide = min(1.0, t / 0.35)
        put_palito(img, "comemorando", 430, 230, 1060, int((1 - slide) * 500 + 6 * math.sin(t * 8)))
        selo(img, 1690, 90, 0.7)
        img = img.convert("RGB")
        d = ImageDraw.Draw(img)
        # faixa com o nome
        pop = min(1.0, t / 0.3)
        while d.textlength(answer, font=fa) > 1300 and fa.size > 60:
            fa = font(F_BLACK, fa.size - 6)
        full_w = max(900, int(d.textlength(answer, font=fa)) + 140)
        bw = int(full_w * pop)
        if bw > 40:
            d.rounded_rectangle([W // 2 - bw // 2, 820, W // 2 + bw // 2, 990], 40, fill=YELLOW, outline=NAVY, width=10)
            if pop >= 1.0:
                d.text((W // 2, 905), answer, font=fa, fill=NAVY, anchor="mm")
        yield img



# ---------- perguntas bônus ----------
GREEN = (40, 190, 90)

LEAF_R = [(0, -1), (0.13, -0.72), (0.3, -0.8), (0.25, -0.35), (0.45, -0.55), (0.52, -0.42), (0.78, -0.48),
          (0.68, -0.22), (0.85, -0.12), (0.5, 0.18), (0.56, 0.32), (0.08, 0.26), (0.06, 0.7)]
LEAF = LEAF_R + [(-x, y) for x, y in reversed(LEAF_R)]


def draw_flag(code, w, h):
    img = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(img)
    if code.startswith("jp"):
        bg, dot = {"jp": (WHITE, (188, 0, 45)), "jp_azul": (WHITE, (30, 80, 200)),
                   "jp_amarelo": ((255, 210, 0), (188, 0, 45))}[code]
        d.rectangle([0, 0, w, h], fill=bg)
        r = h * 0.3
        d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=dot)
    elif code.startswith("ca"):
        leaf = {"ca": (216, 6, 33), "ca_verde": (30, 150, 60), "ca_azul": (30, 80, 200)}[code]
        bar = (216, 6, 33)
        d.rectangle([0, 0, w / 4, h], fill=bar)
        d.rectangle([w * 3 / 4, 0, w, h], fill=bar)
        s = h * 0.36
        d.polygon([(w / 2 + x * s, h / 2 + y * s) for x, y in LEAF], fill=leaf)
    elif code == "de":
        for i, c in enumerate([(0, 0, 0), (221, 0, 0), (255, 206, 0)]):
            d.rectangle([0, h * i / 3, w, h * (i + 1) / 3], fill=c)
    return img


def framed(img, border=10, color=NAVY):
    out = Image.new("RGB", (img.width + 2 * border, img.height + 2 * border), color)
    out.paste(img, (border, border))
    return out


def bonus_base(q, reveal=False):
    img = pattern_bg().convert("RGBA")
    d = ImageDraw.Draw(img)
    d.ellipse([50, 40, 200, 190], fill=ORANGE, outline=WHITE, width=8)
    d.text((125, 112), f"{q['n']:02d}", font=font(F_BLACK, 70), fill=WHITE, anchor="mm")
    selo(img, 1690, 112, 0.75)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([W // 2 - 150, 40, W // 2 + 150, 110], 30, fill=YELLOW, outline=NAVY, width=6)
    d.text((W // 2, 75), "BÔNUS", font=font(F_BLACK, 50), fill=NAVY, anchor="mm")
    tf = font(F_BLACK, 74)
    while d.textlength(q["titulo"], font=tf) > 1500:
        tf = font(F_BLACK, tf.size - 4)
    text_outline(d, (W // 2, 190), q["titulo"], tf, WHITE, w=9)
    good = q["correct"]
    t = q["type"]
    if t == "bandeira":
        fw, fh, gap = 420, 280, 60
        x0 = (W - 3 * fw - 2 * gap) // 2 - 110
        for i, code in enumerate(q["flags"]):
            fl = framed(draw_flag(code, fw, fh))
            x = x0 + i * (fw + gap)
            if reveal and i != good:
                fl = Image.blend(fl, Image.new("RGB", fl.size, (40, 50, 90)), 0.6)
            if reveal and i == good:
                ImageDraw.Draw(img).rounded_rectangle([x - 18, 352, x + fl.width + 18, 372 + fl.height + 28], 26,
                                                      outline=GREEN, width=12)
            img.paste(fl, (x, 370))
            d = ImageDraw.Draw(img)
            cx = x + fl.width // 2
            d.ellipse([cx - 40, 700, cx + 40, 780], fill=GREEN if reveal and i == good else WHITE, outline=NAVY, width=6)
            d.text((cx, 740), str(i + 1), font=font(F_BLACK, 56), fill=NAVY, anchor="mm")
    elif t == "cores":
        fl = draw_flag(q["flag"], 600, 360)
        if not reveal:
            fl = fl.convert("L").convert("RGB")
        img.paste(framed(fl), (150, 330))
        d = ImageDraw.Draw(img)
        for i, cols in enumerate(q["options"]):
            y = 320 + i * 140
            ok = reveal and i == good
            dim = reveal and i != good
            d.rounded_rectangle([860, y, 1500, y + 115], 30, fill=GREEN if ok else (30, 40, 70), outline=WHITE, width=6)
            d.text((910, y + 57), "ABC"[i], font=font(F_BLACK, 64), fill=WHITE, anchor="mm")
            for k, c in enumerate(cols):
                rgb = tuple(int(c[j:j + 2], 16) for j in (1, 3, 5))
                if dim:
                    rgb = tuple(int(v * 0.4 + 40) for v in rgb)
                d.rounded_rectangle([980 + k * 170, y + 17, 980 + k * 170 + 140, y + 98], 14, fill=rgb,
                                    outline=WHITE, width=4)
    elif t == "opcoes":
        for i, txt in enumerate(q["options"]):
            y = 320 + i * 150
            ok = reveal and i == good
            d.rounded_rectangle([330, y, 1390, y + 120], 40, fill=GREEN if ok else WHITE, outline=NAVY, width=8)
            d.ellipse([350, y + 15, 440, y + 105], fill=ORANGE, outline=NAVY, width=5)
            d.text((395, y + 60), str(i + 1), font=font(F_BLACK, 54), fill=WHITE, anchor="mm")
            col = WHITE if ok else (NAVY if not reveal else (150, 160, 185))
            d.text((880, y + 60), txt, font=font(F_BLACK, 70), fill=col, anchor="mm")
    x0, y0, x1, y1 = BAR
    if not reveal:
        d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 40, fill=WHITE)
        d.rounded_rectangle(BAR, 32, fill=(60, 70, 110))
    return img.convert("RGB")


def bonus_reveal_frames(q, dur):
    base = bonus_base(q, reveal=True)
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = base.copy().convert("RGBA")
        slide = min(1.0, t / 0.35)
        put_palito(img, "comemorando", 430, 1700, 1060, int((1 - slide) * 500 + 6 * math.sin(t * 8)))
        yield img.convert("RGB")


def outro_base():
    img = gradient(BLUE, NAVY).convert("RGBA")
    d = ImageDraw.Draw(img)
    text_outline(d, (800, 300), "QUANTOS VOCÊ ACERTOU?", font(F_BLACK, 110), YELLOW, w=12)
    text_outline(d, (800, 450), "CONTA NOS COMENTÁRIOS!", font(F_BLACK, 86), WHITE, w=10)
    text_outline(d, (800, 640), "INSCREVA-SE NO", font(F_BLACK, 70), WHITE, w=8)
    selo(img, 800, 770, 1.4)
    put_palito(img, "acenando", 650, 1650, 1040)
    return img.convert("RGB")


# ---------- áudio ----------

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ERRO ffmpeg:\n" + r.stderr[-2000:])


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", path],
                       capture_output=True, text=True)
    return float(json.loads(r.stdout)["format"]["duration"])


def make_sfx(tmp):
    sfx = {}
    sfx["tick"] = os.path.join(tmp, "tick.wav")
    run(["ffmpeg", "-y", "-f", "lavfi", "-i",
         "aevalsrc='0.5*sin(2*PI*1800*t)*exp(-60*t)':s=44100:d=0.08", sfx["tick"]])
    sfx["ding"] = os.path.join(tmp, "ding.wav")
    run(["ffmpeg", "-y", "-f", "lavfi", "-i",
         "aevalsrc='0.35*(sin(2*PI*1319*t)+0.6*sin(2*PI*1976*t))*exp(-4*t)':s=44100:d=1.2", sfx["ding"]])
    sfx["whoosh"] = os.path.join(tmp, "whoosh.wav")
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anoisesrc=d=0.6:c=pink:a=0.6", "-af",
         "highpass=f=400,lowpass=f=3000,afade=t=in:d=0.25,afade=t=out:st=0.3:d=0.3", sfx["whoosh"]])
    return sfx


class Timeline:
    """Acumula frames de vídeo (pipe pro ffmpeg) e eventos de áudio (arquivo, início)."""

    def __init__(self, path):
        self.t = 0.0
        self.n = 0
        self.audio = []
        self.proc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
             "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)

    def frame(self, img):
        self.proc.stdin.write(img.tobytes())
        self.n += 1
        self.t = self.n / FPS

    def hold(self, img, secs):
        b = img.tobytes()
        for _ in range(int(round(secs * FPS))):
            self.proc.stdin.write(b)
            self.n += 1
        self.t = self.n / FPS

    def sound(self, path, at=None, vol=1.0):
        if path and os.path.exists(path):
            self.audio.append((path, self.t if at is None else at, vol))

    def close(self):
        self.proc.stdin.close()
        self.proc.wait()


def main():
    assets, out = sys.argv[1], sys.argv[2]
    tmp = tempfile.mkdtemp(prefix="quiz_")
    sfx = make_sfx(tmp)
    A = lambda name: os.path.join(assets, name)
    dur = lambda p: duration(p) if os.path.exists(p) else 2.0

    video = os.path.join(tmp, "video.mp4")
    tl = Timeline(video)

    # abertura
    tl.sound(A("intro.mp3"))
    tl.hold(intro_base(), dur(A("intro.mp3")) + 0.6)

    for q in QUESTIONS:
        n = q["n"]
        tl.sound(sfx["whoosh"])
        for f in vinheta_frames(n):
            tl.frame(f)
        base = bonus_base(q) if q.get("type") else question_base(q)
        # pergunta lida
        qa = A(f"q{n}.mp3")
        tl.sound(qa)
        tl.hold(bar_frame(base, 1.0), dur(qa) + 0.3)
        # contagem
        start = tl.t
        frames = int(COUNTDOWN * FPS)
        for s in range(int(COUNTDOWN)):
            tl.sound(sfx["tick"], at=start + s, vol=0.8)
        for i in range(frames):
            tl.frame(bar_frame(base, 1 - i / frames, i / FPS))
        # revelação
        aa = A(f"a{n}.mp3")
        tl.sound(sfx["ding"], vol=0.9)
        tl.sound(aa, at=tl.t + 0.35)
        rd = max(REVEAL_MIN, dur(aa) + 0.9)
        frames_r = bonus_reveal_frames(q, rd) if q.get("type") else reveal_frames(A(f"foto{n}.jpg"), q["answer"], rd)
        for f in frames_r:
            tl.frame(f)

    # final
    tl.sound(sfx["whoosh"])
    has_outro = os.path.exists(A("outro.mp3"))
    tl.sound(A("outro.mp3"), at=tl.t + 0.4)
    tl.hold(outro_base(), max(4.0, dur(A("outro.mp3")) + 1.5) if has_outro else 4.0)
    total = tl.t
    tl.close()

    # mixagem em numpy: decodifica cada som uma vez e soma no lugar certo
    import numpy as np
    sr = 44100
    buf = np.zeros((int((total + 1) * sr), 2), dtype=np.float32)
    voz = np.zeros(len(buf), dtype=np.float32)  # onde tem narração (para abaixar a música)
    cache = {}
    for p, at, vol in tl.audio:
        if p not in cache:
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"],
                                 capture_output=True).stdout
            cache[p] = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
        x = cache[p] * vol
        i0 = int(at * sr)
        i1 = min(len(buf), i0 + len(x))
        buf[i0:i1] += x[: i1 - i0]
        if os.path.abspath(p).startswith(os.path.abspath(assets)):
            voz[i0:i1] = 1.0
    buf = buf[: int(total * sr)]

    # música de fundo opcional: assets/musica.mp3 (em loop, baixinha, abaixa ainda mais quando o narrador fala)
    musica = A("musica.mp3")
    if os.path.exists(musica):
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", musica, "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"],
                             capture_output=True).stdout
        m = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
        n = len(buf)
        m = np.tile(m, (n // len(m) + 1, 1))[:n].copy()
        k = int(0.25 * sr)  # suaviza a entrada/saída do "abaixar"
        env = np.convolve(voz[:n], np.ones(k, dtype=np.float32) / k, mode="same")
        ganho = MUSICA_VOL * (1.0 - 0.55 * np.clip(env, 0, 1))
        fi, fo = int(1.5 * sr), int(3.0 * sr)
        ganho[:fi] *= np.linspace(0, 1, fi)
        ganho[-fo:] *= np.linspace(1, 0, fo)
        buf += m * ganho[:, None]
    peak = float(np.abs(buf).max()) or 1.0
    if peak > 0.98:
        buf *= 0.98 / peak
    wav = os.path.join(tmp, "mix.f32")
    buf.tofile(wav)
    run(["ffmpeg", "-y", "-i", video, "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", wav, "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out])
    print(f"OK {out} ({total:.1f}s)")


if __name__ == "__main__":
    main()
