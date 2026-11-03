"""Quiz Palito — "Adivinhe 195 países pela bandeira" (fácil, médio, difícil; 3 s por bandeira).

Reaproveita o build.py do quiz de países (Palito, selo, sons, barra, mixagem) com telas próprias.
Uso: py -3 build_bandeiras.py assets quiz-palito-bandeiras.mp4
     py -3 build_bandeiras.py --previa      (só salva imagens das telas em previa/)
"""
import json, math, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(QP, "videos", "01-paises-sem-vogais"))
import build as b

b.PERSONAGEM = os.path.join(QP, "personagem")
W, H, FPS = b.W, b.H, b.FPS
PAISES = json.load(open(os.path.join(HERE, "paises.json"), encoding="utf-8"))
TOTAL = len(PAISES)

COUNT = 3.0        # segundos para responder
POP = 0.3          # bandeira entrando
REVEAL_MIN = 2.4
b.COUNTDOWN = COUNT

NIVEL = {  # cor da faixa, fundo (topo, base), cores do "sol" da vinheta
    "FÁCIL": ((40, 190, 90), (0, 170, 150), (14, 60, 80), ((70, 210, 110), (30, 160, 70))),
    "MÉDIO": ((255, 140, 0), (34, 86, 196), (18, 32, 84), ((255, 170, 30), (245, 120, 0))),
    "DIFÍCIL": ((235, 50, 50), (120, 50, 170), (40, 16, 70), ((240, 80, 80), (200, 30, 40))),
}
FLAG_C = (860, 500)
FLAG_MAX = (1040, 560)

_bg = {}


def fundo(nivel):
    if nivel in _bg:
        return _bg[nivel].copy()
    _, c1, c2, _ = NIVEL[nivel]
    img = b.gradient(c1, c2)
    # mesmo padrão de "?" e globinhos do canal
    pat = b.pattern_bg().convert("L")
    base = b.gradient(b.BLUE, b.NAVY).convert("L")
    diff = Image.eval(Image.fromarray(__import__("numpy").clip(
        __import__("numpy").asarray(pat, dtype=int) - __import__("numpy").asarray(base, dtype=int), 0, 255).astype("uint8")),
        lambda v: min(255, v * 4))
    img.paste(Image.new("RGB", (W, H), (255, 255, 255)), (0, 0), diff.point(lambda v: v // 6))
    _bg[nivel] = img
    return img.copy()


def cartao(code, scale=1.0):
    """Bandeira com moldura branca, borda azul e sombra."""
    fl = Image.open(os.path.join(HERE, "bandeiras", f"{code}.png")).convert("RGBA")
    r = min(FLAG_MAX[0] / fl.width, FLAG_MAX[1] / fl.height) * scale
    fl = fl.resize((max(1, int(fl.width * r)), max(1, int(fl.height * r))), Image.LANCZOS)
    m = max(6, int(18 * scale))
    card = Image.new("RGBA", (fl.width + 2 * m + 40, fl.height + 2 * m + 50), (0, 0, 0, 0))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([20, 34, 20 + fl.width + 2 * m, 34 + fl.height + 2 * m], 24, fill=(0, 0, 0, 110))
    card.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([20, 20, 20 + fl.width + 2 * m, 20 + fl.height + 2 * m], 24, fill=b.WHITE,
                        outline=b.NAVY, width=max(3, int(6 * scale)))
    card.alpha_composite(fl, (20 + m, 20 + m))
    d.rectangle([20 + m, 20 + m, 20 + m + fl.width - 1, 20 + m + fl.height - 1], outline=(200, 205, 215), width=2)
    return card


def put_card(img, card):
    img.alpha_composite(card, (FLAG_C[0] - card.width // 2, FLAG_C[1] - card.height // 2 + 5))


def topo(img, p, titulo="QUE PAÍS É ESSE?"):
    d = ImageDraw.Draw(img)
    cor = NIVEL[p["nivel"]][0]
    d.rounded_rectangle([40, 40, 330, 150], 55, fill=b.ORANGE, outline=b.WHITE, width=7)
    d.text((185, 95), f"{p['n']}/{TOTAL}", font=b.font(b.F_BLACK, 58), fill=b.WHITE, anchor="mm",
           stroke_width=3, stroke_fill=b.NAVY)
    b.text_outline(d, (900, 95), titulo, b.font(b.F_BLACK, 84), b.YELLOW, w=10)
    b.selo(img, 1700, 85, 0.72)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([1555, 140, 1845, 205], 30, fill=cor, outline=b.WHITE, width=5)
    d.text((1700, 172), f"NÍVEL {p['nivel']}", font=b.font(b.F_BLACK, 40), fill=b.WHITE, anchor="mm",
           stroke_width=3, stroke_fill=b.NAVY)


def trilho(img):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = b.BAR
    d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 40, fill=b.WHITE)
    d.rounded_rectangle(b.BAR, 32, fill=(60, 70, 110))


def question_frames(p):
    """Bandeira entrando (POP) e depois a contagem de 3 s."""
    vazio = fundo(p["nivel"]).convert("RGBA")
    topo(vazio, p)
    trilho(vazio)
    for i in range(int(POP * FPS)):
        k = (i + 1) / (POP * FPS)
        s = 0.6 + 0.48 * k if k < 0.8 else 1.08 - 0.08 * (k - 0.8) / 0.2
        img = vazio.copy()
        put_card(img, cartao(p["code"], s))
        yield b.bar_frame(img.convert("RGB"), 1.0, i / FPS)
    base = vazio.copy()
    put_card(base, cartao(p["code"]))
    base = base.convert("RGB")
    n = int(COUNT * FPS)
    for i in range(n):
        yield b.bar_frame(base, 1 - i / n, i / FPS)


def reveal_base(p):
    img = fundo(p["nivel"]).convert("RGBA")
    topo(img, p, "RESPOSTA")
    put_card(img, cartao(p["code"]))
    return img


def faixa_nome(img, nome, pop):
    d = ImageDraw.Draw(img)
    f = b.font(b.F_BLACK, 110)
    while d.textlength(nome, font=f) > 1240 and f.size > 50:
        f = b.font(b.F_BLACK, f.size - 4)
    full = max(760, int(d.textlength(nome, font=f)) + 140)
    bw = int(full * pop)
    cx = FLAG_C[0]
    if bw > 40:
        d.rounded_rectangle([cx - bw // 2, 850, cx + bw // 2, 1010], 44, fill=b.YELLOW, outline=b.NAVY, width=10)
        if pop >= 1.0:
            d.text((cx, 928), nome, font=f, fill=b.NAVY, anchor="mm")


def reveal_frames(p, dur):
    base = reveal_base(p)
    cheia = base.copy()
    faixa_nome(cheia, p["nome"], 1.0)
    for i in range(int(dur * FPS)):
        t = i / FPS
        pop = min(1.0, t / 0.25)
        img = cheia.copy() if pop >= 1.0 else base.copy()
        if pop < 1.0:
            faixa_nome(img, p["nome"], pop)
        slide = min(1.0, t / 0.3)
        b.put_palito(img, "comemorando", 420, 1700, 1040, int((1 - slide) * 500 + 6 * math.sin(t * 8)))
        yield img.convert("RGB")


def nivel_frames(nivel, dur):
    cor, _, _, (c1, c2) = NIVEL[nivel]
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = Image.new("RGB", (W, H), c2)
        d = ImageDraw.Draw(img)
        cx, cy, R, rot = W / 2, H / 2, 2400, t * 12
        for k in range(24):
            a0, a1 = math.radians(k * 15 + rot), math.radians(k * 15 + 7.5 + rot)
            d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)),
                       (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=c1 if k % 2 else c2)
        s = min(1.0, t / 0.3)
        size = int(220 * (0.5 + 0.5 * s))
        b.text_outline(d, (820, 360), "NÍVEL", b.font(b.F_BLACK, int(size * 0.7)), b.WHITE, w=12)
        b.text_outline(d, (820, 580), nivel, b.font(b.F_BLACK, size), b.YELLOW, w=16)
        b.selo(img, 820, 840, 1.1)
        img = img.convert("RGBA")
        b.put_palito(img, "apontando", 620, 1600 + int((1 - s) * 700), 1050, int(6 * math.sin(t * 5)))
        yield img.convert("RGB")


def intro_base():
    img = b.gradient(b.TEAL, b.BLUE).convert("RGBA")
    b.selo(img, 800, 100, 1.2)
    d = ImageDraw.Draw(img)
    b.text_outline(d, (800, 270), "ADIVINHE 195 PAÍSES", b.font(b.F_BLACK, 120), b.WHITE, w=12)
    b.text_outline(d, (800, 420), "PELA BANDEIRA", b.font(b.F_BLACK, 150), b.YELLOW, w=14)
    for i, code in enumerate(["br", "jp", "ca", "kr"]):
        fl = Image.open(os.path.join(HERE, "bandeiras", f"{code}.png")).convert("RGB").resize((270, 180), Image.LANCZOS)
        x = 800 - 2 * 300 + i * 300 + 15
        b.shadowed_round_rect(img, (x - 10, 560, x + 280, 760), 18, b.WHITE)
        img.paste(fl, (x, 570))
    d = ImageDraw.Draw(img)
    for i, (txt, cor) in enumerate([("FÁCIL", NIVEL["FÁCIL"][0]), ("MÉDIO", NIVEL["MÉDIO"][0]), ("DIFÍCIL", NIVEL["DIFÍCIL"][0])]):
        x = 800 - 330 + i * 330
        d.rounded_rectangle([x - 140, 820, x + 140, 900], 36, fill=cor, outline=b.WHITE, width=6)
        d.text((x, 860), txt, font=b.font(b.F_BLACK, 50), fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
    b.text_outline(d, (800, 985), "3 SEGUNDOS POR BANDEIRA!", b.font(b.F_BLACK, 64), b.WHITE, w=7)
    b.put_palito(img, "acenando", 700, 1650, 1050)
    return img.convert("RGB")


def outro_base():
    img = b.gradient(b.BLUE, b.NAVY).convert("RGBA")
    d = ImageDraw.Draw(img)
    b.text_outline(d, (800, 260), "QUANTAS VOCÊ ACERTOU?", b.font(b.F_BLACK, 110), b.YELLOW, w=12)
    b.text_outline(d, (800, 410), "CONTA NOS COMENTÁRIOS!", b.font(b.F_BLACK, 86), b.WHITE, w=10)
    b.text_outline(d, (800, 530), "E MARCA UM AMIGO 👀".replace(" 👀", ""), b.font(b.F_BLACK, 70), b.WHITE, w=8)
    b.text_outline(d, (800, 690), "INSCREVA-SE NO", b.font(b.F_BLACK, 70), b.WHITE, w=8)
    b.selo(img, 800, 820, 1.4)
    b.put_palito(img, "acenando", 650, 1650, 1040)
    return img.convert("RGB")


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    intro_base().save(os.path.join(out, "1_intro.jpg"), quality=88)
    list(nivel_frames("DIFÍCIL", 0.5))[-1].save(os.path.join(out, "2_nivel.jpg"), quality=88)
    for p in (PAISES[0], PAISES[67], PAISES[150], PAISES[61]):
        fr = list(question_frames(p))
        fr[30].save(os.path.join(out, f"3_pergunta_{p['n']}.jpg"), quality=88)
        fr[-5].save(os.path.join(out, f"3_pergunta_{p['n']}_fim.jpg"), quality=88)
        list(reveal_frames(p, 1.0))[-1].save(os.path.join(out, f"4_resposta_{p['n']}.jpg"), quality=88)
    outro_base().save(os.path.join(out, "5_final.jpg"), quality=88)


def main():
    assets, out = sys.argv[1], sys.argv[2]
    tmp = tempfile.mkdtemp(prefix="quiz_band_")
    sfx = b.make_sfx(tmp)
    A = lambda name: os.path.join(assets, name)
    dur = lambda p: b.duration(p) if os.path.exists(p) else 2.0
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    marcas = {}

    tl.sound(A("intro.mp3"))
    tl.hold(intro_base(), dur(A("intro.mp3")) + 0.6)

    nivel_atual = None
    for p in PAISES:
        if p["nivel"] != nivel_atual:
            nivel_atual = p["nivel"]
            k = {"FÁCIL": 1, "MÉDIO": 2, "DIFÍCIL": 3}[nivel_atual]
            marcas[nivel_atual] = tl.t
            tl.sound(sfx["whoosh"])
            tl.sound(A(f"nivel{k}.mp3"), at=tl.t + 0.3)
            for f in nivel_frames(nivel_atual, dur(A(f"nivel{k}.mp3")) + 0.9):
                tl.frame(f)
        n = p["n"]
        tl.sound(sfx["whoosh"], vol=0.6)
        start = tl.t + POP
        for s in range(int(COUNT)):
            tl.sound(sfx["tick"], at=start + s, vol=0.8)
        for f in question_frames(p):
            tl.frame(f)
        aa = A(f"a{n}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(aa, at=tl.t + 0.25)
        for f in reveal_frames(p, max(REVEAL_MIN, dur(aa) + 0.75)):
            tl.frame(f)
        if n % 10 == 0:
            print(f"{n}/{TOTAL} ({tl.t / 60:.1f} min)", flush=True)

    marcas["FINAL"] = tl.t
    tl.sound(sfx["whoosh"])
    tl.sound(A("outro.mp3"), at=tl.t + 0.4)
    tl.hold(outro_base(), max(4.0, dur(A("outro.mp3")) + 1.5))
    total = tl.t
    tl.close()
    json.dump(marcas, open(os.path.join(HERE, "tempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # mixagem (igual ao build.py): narração + efeitos + música de fundo que abaixa quando o narrador fala
    import numpy as np
    sr = 44100
    buf = np.zeros((int((total + 1) * sr), 2), dtype=np.float32)
    voz = np.zeros(len(buf), dtype=np.float32)
    cache = {}
    for pth, at, vol in tl.audio:
        if pth not in cache:
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", pth, "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"],
                                 capture_output=True).stdout
            cache[pth] = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
        x = cache[pth] * vol
        i0 = int(at * sr)
        i1 = min(len(buf), i0 + len(x))
        buf[i0:i1] += x[: i1 - i0]
        if os.path.abspath(pth).startswith(os.path.abspath(assets)):
            voz[i0:i1] = 1.0
    buf = buf[: int(total * sr)]
    musica = A("musica.mp3")
    if os.path.exists(musica):
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", musica, "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"],
                             capture_output=True).stdout
        m = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
        n = len(buf)
        m = np.tile(m, (n // len(m) + 1, 1))[:n].copy()
        k = int(0.25 * sr)
        env = np.convolve(voz[:n], np.ones(k, dtype=np.float32) / k, mode="same")
        ganho = b.MUSICA_VOL * (1.0 - 0.55 * np.clip(env, 0, 1))
        fi, fo = int(1.5 * sr), int(3.0 * sr)
        ganho[:fi] *= np.linspace(0, 1, fi)
        ganho[-fo:] *= np.linspace(1, 0, fo)
        buf += m * ganho[:, None]
    peak = float(np.abs(buf).max()) or 1.0
    if peak > 0.98:
        buf *= 0.98 / peak
    wav = os.path.join(tmp, "mix.f32")
    buf.tofile(wav)
    b.run(["ffmpeg", "-y", "-i", video, "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", wav, "-map", "0:v", "-map", "1:a",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out])
    print(f"OK {out} ({total:.1f}s)")


if __name__ == "__main__":
    if "--previa" in sys.argv:
        previa()
    else:
        main()
