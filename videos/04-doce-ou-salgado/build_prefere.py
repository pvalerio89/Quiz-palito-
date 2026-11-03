"""Quiz Palito — "Qual você prefere: DOCE ou SALGADO?" (40 escolhas em 4 fases).

Cada escolha: vinheta com o número -> duas fotos com "OU" + 5 s de barra -> o Palito mostra a escolha dele.
Reaproveita o build.py do quiz de países (fontes, cores, Palito, selo, sons, mixagem).
Uso: py -3 build_prefere.py             (monta quiz-palito-doce-ou-salgado.mp4)
     py -3 build_prefere.py --previa    (só salva imagens das telas em previa/)
"""
import json, math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(QP, "videos", "01-paises-sem-vogais"))
import build as b
import re, unicodedata


def slug(nome):  # igual ao fotos.py desta pasta
    s = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


b.PERSONAGEM = os.path.join(QP, "personagem")
W, H, FPS = b.W, b.H, b.FPS
ESC = json.load(open(os.path.join(HERE, "escolhas.json"), encoding="utf-8"))
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-doce-ou-salgado.mp4")

COUNT = 5.0
VINHETA = 1.0
CARD = 520
CX = (560, 1360)   # centro dos dois cartões
CY = 530
BAR = (300, 945, W - 300, 995)
ROSA, LILAS = (236, 64, 150), (150, 70, 200)
# fundos que se alternam (topo, base)
CORES = [((236, 64, 150), (150, 30, 100)), ((235, 60, 50), (150, 20, 30)), ((40, 150, 230), (20, 60, 150)),
         ((255, 140, 0), (190, 70, 0)), ((40, 185, 110), (10, 100, 70)), ((150, 70, 200), (70, 30, 120))]
FASES = {1: ("AQUECIMENTO", (40, 190, 90)), 2: ("FICOU DIFÍCIL", (255, 140, 0)),
         3: ("MUITO DIFÍCIL", (235, 50, 50)), 4: ("IMPOSSÍVEL", (150, 40, 190))}

_cache = {}


def fundo(k):
    """Degradê colorido com o padrão de '?' e globinhos do canal."""
    if k in _cache:
        return _cache[k].copy()
    c1, c2 = CORES[k % len(CORES)]
    img = b.gradient(c1, c2)
    pat = np.asarray(b.pattern_bg().convert("L"), dtype=int) - np.asarray(b.gradient(b.BLUE, b.NAVY).convert("L"), dtype=int)
    mask = Image.fromarray(np.clip(pat * 4, 0, 255).astype("uint8")).point(lambda v: v // 5)
    img.paste(Image.new("RGB", (W, H), (255, 255, 255)), (0, 0), mask)
    _cache[k] = img
    return img.copy()


def foto(nome, size=CARD, apagada=False):
    key = ("f", nome, size, apagada)
    if key in _cache:
        return _cache[key]
    org = ("o", nome)
    if org not in _cache:  # original em 640x640, guardado uma vez só
        _cache[org] = ImageOps.fit(Image.open(os.path.join(HERE, "fotos", slug(nome) + ".jpg")).convert("RGB"),
                                   (640, 640), Image.LANCZOS)
    im = _cache[org].resize((size, size), Image.LANCZOS)
    if apagada:
        im = ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(0.25)).enhance(0.55)
    # só guarda os tamanhos fixos; os da animação de entrada mudam a cada quadro
    if size in (CARD, int(CARD * 1.06), int(CARD * 0.94)):
        _cache[key] = im
    return im


def cartao(img, cx, cy, nome, tipo, escala=1.0, estado=None):
    """Foto com moldura, etiqueta DOCE/SALGADO e nome embaixo. estado: None, 'sim' ou 'nao'."""
    s = int(CARD * escala)
    x0, y0 = cx - s // 2, cy - s // 2
    borda = (60, 220, 90) if estado == "sim" else b.WHITE
    if estado == "sim":  # brilho em volta
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(glow).rounded_rectangle([x0 - 40, y0 - 40, x0 + s + 40, y0 + s + 40], 60, fill=(255, 240, 120, 170))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(28)))
    b.shadowed_round_rect(img, (x0 - 14, y0 - 14, x0 + s + 14, y0 + s + 14), 34, borda)
    img.paste(foto(nome, s, estado == "nao"), (x0, y0))
    d = ImageDraw.Draw(img)
    # etiqueta do tipo
    cor = ROSA if tipo == "DOCE" else (255, 140, 0)
    ft = b.font(b.F_BLACK, 34)
    tw = d.textlength(tipo, font=ft)
    d.rounded_rectangle([cx - tw / 2 - 26, y0 - 40, cx + tw / 2 + 26, y0 + 18], 29, fill=cor, outline=b.WHITE, width=5)
    d.text((cx, y0 - 11), tipo, font=ft, fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
    # nome
    f = b.font(b.F_BLACK, 56)
    txt = nome.upper()
    while d.textlength(txt, font=f) > s + 40 and f.size > 30:
        f = b.font(b.F_BLACK, f.size - 3)
    nw = d.textlength(txt, font=f)
    ny = y0 + s + 58
    d.rounded_rectangle([cx - nw / 2 - 32, ny - 42, cx + nw / 2 + 32, ny + 42], 42,
                        fill=b.YELLOW if estado != "nao" else (170, 170, 170), outline=b.NAVY, width=7)
    d.text((cx, ny), txt, font=f, fill=b.NAVY, anchor="mm")


def topo(img, e):
    d = ImageDraw.Draw(img)
    d.ellipse([40, 30, 190, 180], fill=b.ORANGE, outline=b.WHITE, width=8)
    d.text((115, 103), f"{e['n']:02d}", font=b.font(b.F_BLACK, 70), fill=b.WHITE, anchor="mm", stroke_width=3,
           stroke_fill=b.NAVY)
    b.text_outline(d, (W // 2, 95), "QUAL VOCÊ PREFERE?", b.font(b.F_BLACK, 90), b.YELLOW, w=10)
    b.selo(img, 1730, 95, 0.7)
    nome, cor = FASES[e["fase"]]
    d = ImageDraw.Draw(img)
    f = b.font(b.F_BLACK, 34)
    t = f"FASE {e['fase']}  •  {nome}"
    tw = d.textlength(t, font=f)
    d.rounded_rectangle([W / 2 - tw / 2 - 30, 152, W / 2 + tw / 2 + 30, 204], 26, fill=cor, outline=b.WHITE, width=5)
    d.text((W / 2, 178), t, font=f, fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)


def ou(img, cy=CY):
    d = ImageDraw.Draw(img)
    d.ellipse([960 - 85, cy - 85, 960 + 85, cy + 85], fill=b.NAVY, outline=b.WHITE, width=10)
    d.text((960, cy - 6), "OU", font=b.font(b.F_BLACK, 80), fill=b.WHITE, anchor="mm")


def tela(e, estado=None, escala=(1.0, 1.0)):
    img = fundo(e["n"]).convert("RGBA")
    topo(img, e)
    est = (None, None) if estado is None else (("sim", "nao") if e["palito"] == 0 else ("nao", "sim"))
    cartao(img, CX[0], CY, e["doce"], "DOCE", escala[0], est[0])
    cartao(img, CX[1], CY, e["salgado"], "SALGADO", escala[1], est[1])
    ou(img)
    return img


def barra(img, frac):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = BAR
    d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 34, fill=b.WHITE)
    d.rounded_rectangle(BAR, 26, fill=(60, 70, 110))
    if frac > 0.002:
        xe = x0 + (x1 - x0) * frac
        d.rounded_rectangle([x0, y0, max(xe, x0 + 52), y1], 26, fill=b.ORANGE if frac > 0.3 else b.RED)
    s = math.ceil(frac * COUNT)
    if s > 0:
        d.text(((x0 + x1) // 2, (y0 + y1) // 2), str(s), font=b.font(b.F_BLACK, 42), fill=b.WHITE, anchor="mm",
               stroke_width=4, stroke_fill=b.NAVY)


def burst(c1, c2, rot):
    img = Image.new("RGB", (W, H), c2)
    d = ImageDraw.Draw(img)
    cx, cy, R = W / 2, H / 2, 2400
    for k in range(24):
        a0, a1 = math.radians(k * 15 + rot), math.radians(k * 15 + 7.5 + rot)
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)),
                   (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=c1 if k % 2 else c2)
    return img


def vinheta_frames(e):
    c1, c2 = CORES[e["n"] % len(CORES)]
    for i in range(int(VINHETA * FPS)):
        t = i / FPS
        img = burst(c1, c2, t * 30).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.25)
        b.text_outline(d, (W // 2, 430), f"{e['n']:02d}", b.font(b.F_BLACK, int(300 * (0.4 + 0.6 * s))), b.WHITE, w=18)
        b.text_outline(d, (W // 2, 700), "QUAL VOCÊ PREFERE?", b.font(b.F_BLACK, int(100 * (0.4 + 0.6 * s))), b.YELLOW, w=10)
        yield img.convert("RGB")


def pergunta_frames(e, fala):
    """Entrada dos cartões, fala da pergunta e 5 s de barra com o Palito pensando."""
    n_in = int(0.35 * FPS)
    for i in range(n_in):
        k = (i + 1) / n_in
        sc = 0.55 + 0.53 * k if k < 0.8 else 1.08 - 0.08 * (k - 0.8) / 0.2
        img = tela(e, escala=(sc, sc))
        barra(img, 1.0)
        yield img.convert("RGB")
    base = tela(e)
    barra(base, 1.0)
    for i in range(int(fala * FPS)):
        img = base.copy()
        b.put_palito(img, "pensando", 270, 960, 905, int(6 * math.sin(i / FPS * 5)))
        yield img.convert("RGB")
    vazio = tela(e)
    n = int(COUNT * FPS)
    for i in range(n):
        img = vazio.copy()
        frac = 1 - i / n
        barra(img, frac)
        pose = "pensando" if frac > 0.3 else "assustado"
        b.put_palito(img, pose, 270, 960, 905, int(7 * math.sin(i / FPS * (5 if pose == "pensando" else 18))))
        yield img.convert("RGB")


def escolha_frames(e, dur):
    lado = e["palito"]
    base = tela(e, estado=True, escala=(1.06, 0.94) if lado == 0 else (0.94, 1.06))
    d = ImageDraw.Draw(base)
    cx = CX[lado]
    f = b.font(b.F_BLACK, 44)
    t = "ESCOLHA DO PALITO!"
    tw = d.textlength(t, font=f)
    for i in range(int(dur * FPS)):
        tt = i / FPS
        img = base.copy()
        dd = ImageDraw.Draw(img)
        pop = min(1.0, tt / 0.2)
        y = 985
        w2 = (tw / 2 + 34) * pop
        if pop > 0.1:
            dd.rounded_rectangle([cx - w2, y - 38, cx + w2, y + 38], 38, fill=(60, 200, 90), outline=b.WHITE, width=6)
            if pop >= 1.0:
                dd.text((cx, y), t, font=f, fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
        sl = min(1.0, tt / 0.3)
        b.put_palito(img, "comemorando", 280, 960, 915, int((1 - sl) * 300 + 8 * math.sin(tt * 9)))
        yield img.convert("RGB")


def fase_frames(k, dur):
    nome, cor = FASES[k]
    c1 = tuple(min(255, int(v * 1.15) + 20) for v in cor)
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = burst(c1, cor, t * 12).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.3)
        b.text_outline(d, (820, 340), "FASE FINAL" if k == 4 else f"FASE {k}", b.font(b.F_BLACK, int(150 * (0.5 + 0.5 * s))), b.WHITE, w=12)
        b.text_outline(d, (820, 560), nome, b.font(b.F_BLACK, int(170 * (0.5 + 0.5 * s))), b.YELLOW, w=16)
        b.selo(img, 820, 800, 1.1)
        b.put_palito(img, "apontando", 620, 1600 + int((1 - s) * 700), 1050, int(6 * math.sin(t * 5)))
        yield img.convert("RGB")


def intro_base():
    img = fundo(0).convert("RGBA")
    b.selo(img, 960, 90, 1.1)
    d = ImageDraw.Draw(img)
    b.text_outline(d, (960, 235), "QUAL VOCÊ PREFERE?", b.font(b.F_BLACK, 120), b.WHITE, w=12)
    for cx, nome, tipo in ((520, "Bolo de chocolate", "DOCE"), (1400, "Pizza", "SALGADO")):
        s = 380
        x0, y0 = cx - s // 2, 360
        b.shadowed_round_rect(img, (x0 - 12, y0 - 12, x0 + s + 12, y0 + s + 12), 30, b.WHITE)
        img.paste(foto(nome, s), (x0, y0))
        d = ImageDraw.Draw(img)
        b.text_outline(d, (cx, 850), tipo, b.font(b.F_BLACK, 130), b.YELLOW if tipo == "DOCE" else b.WHITE, w=14)
    ou(img, 550)
    d = ImageDraw.Draw(img)
    b.text_outline(d, (960, 1000), "40 ESCOLHAS  •  4 FASES", b.font(b.F_BLACK, 56), b.WHITE, w=7)
    b.put_palito(img, "pensando", 360, 1825, 1065)
    return img.convert("RGB")


def outro_base():
    img = fundo(2).convert("RGBA")
    d = ImageDraw.Draw(img)
    b.text_outline(d, (800, 230), "TIME DOCE OU", b.font(b.F_BLACK, 120), b.WHITE, w=12)
    b.text_outline(d, (800, 380), "TIME SALGADO?", b.font(b.F_BLACK, 140), b.YELLOW, w=14)
    d.rounded_rectangle([340, 480, 1260, 600], 50, fill=b.RED, outline=b.WHITE, width=8)
    d.text((800, 540), "CONTA NOS COMENTÁRIOS!", font=b.font(b.F_BLACK, 64), fill=b.WHITE, anchor="mm",
           stroke_width=3, stroke_fill=b.NAVY)
    b.text_outline(d, (800, 700), "QUANTAS VEZES VOCÊ CONCORDOU COM O PALITO?", b.font(b.F_BLACK, 46), b.WHITE, w=6)
    b.text_outline(d, (800, 830), "INSCREVA-SE NO", b.font(b.F_BLACK, 64), b.WHITE, w=7)
    b.selo(img, 800, 940, 1.3)
    b.put_palito(img, "acenando", 650, 1650, 1040)
    return img.convert("RGB")


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    intro_base().save(os.path.join(out, "1_intro.jpg"), quality=88)
    list(fase_frames(4, 0.5))[-1].save(os.path.join(out, "2_fase.jpg"), quality=88)
    for e in (ESC[0], ESC[20], ESC[39]):
        list(vinheta_frames(e))[-1].save(os.path.join(out, f"3_vinheta_{e['n']}.jpg"), quality=88)
        fr = list(pergunta_frames(e, 0.3))
        fr[-int(COUNT * FPS * 0.5)].save(os.path.join(out, f"4_pergunta_{e['n']}.jpg"), quality=88)
        list(escolha_frames(e, 0.8))[-1].save(os.path.join(out, f"5_escolha_{e['n']}.jpg"), quality=88)
    outro_base().save(os.path.join(out, "6_final.jpg"), quality=88)
    print(out)


def main():
    tmp = tempfile.mkdtemp(prefix="quiz_pref_")
    sfx = b.make_sfx(tmp)
    dur = lambda p: b.duration(p) if os.path.exists(p) else 1.5
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    marcas = {}
    tl.sound(A("intro.mp3"))
    tl.hold(intro_base(), dur(A("intro.mp3")) + 0.6)
    fase = None
    for e in ESC:
        n = e["n"]
        if e["fase"] != fase:
            fase = e["fase"]
            marcas[fase] = tl.t
            tl.sound(sfx["whoosh"])
            tl.sound(A(f"fase{fase}.mp3"), at=tl.t + 0.3)
            for f in fase_frames(fase, dur(A(f"fase{fase}.mp3")) + 0.9):
                tl.frame(f)
        tl.sound(sfx["whoosh"], vol=0.7)
        for f in vinheta_frames(e):
            tl.frame(f)
        q = A(f"q{n}.mp3")
        tl.sound(q, at=tl.t + 0.35)
        fala = dur(q) + 0.15
        st = tl.t + 0.35 + fala
        for s in range(int(COUNT)):
            tl.sound(sfx["tick"], at=st + s, vol=0.8)
        for f in pergunta_frames(e, fala):
            tl.frame(f)
        p = A(f"p{n}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(p, at=tl.t + 0.2)
        for f in escolha_frames(e, max(2.2, dur(p) + 0.5)):
            tl.frame(f)
        if n % 10 == 0:
            print(f"{n}/40 ({tl.t / 60:.1f} min)", flush=True)
    marcas["final"] = tl.t
    tl.sound(sfx["whoosh"])
    tl.sound(A("outro.mp3"), at=tl.t + 0.4)
    tl.hold(outro_base(), max(4.0, dur(A("outro.mp3")) + 1.5))
    total = tl.t
    tl.close()
    json.dump(marcas, open(os.path.join(HERE, "tempos.json"), "w", encoding="utf-8"), indent=1)
    mixar(tl, video, total)
    print(f"OK {SAIDA} ({total:.1f}s)")


def mixar(tl, video, total):
    sr = 44100
    buf = np.zeros((int((total + 1) * sr), 2), dtype=np.float32)
    voz = np.zeros(len(buf), dtype=np.float32)
    dec = lambda p: np.frombuffer(subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"],
        capture_output=True).stdout, dtype=np.float32).reshape(-1, 2)
    cache = {}
    for pth, at, vol in tl.audio:
        x = cache.setdefault(pth, dec(pth)) * vol
        i0 = int(at * sr)
        i1 = min(len(buf), i0 + len(x))
        buf[i0:i1] += x[: i1 - i0]
        if os.path.abspath(pth).startswith(os.path.join(HERE, "assets")):
            voz[i0:i1] = 1.0
    n = int(total * sr)
    buf, voz = buf[:n], voz[:n]
    if os.path.exists(A("musica.mp3")):
        m = dec(A("musica.mp3"))
        m = np.tile(m, (n // len(m) + 1, 1))[:n].copy()
        k = int(0.25 * sr)
        env = np.convolve(voz, np.ones(k, dtype=np.float32) / k, mode="same")
        ganho = b.MUSICA_VOL * (1.0 - 0.55 * np.clip(env, 0, 1))
        fi, fo = int(1.5 * sr), int(3.0 * sr)
        ganho[:fi] *= np.linspace(0, 1, fi)
        ganho[-fo:] *= np.linspace(1, 0, fo)
        buf += m * ganho[:, None]
    peak = float(np.abs(buf).max()) or 1.0
    if peak > 0.98:
        buf *= 0.98 / peak
    raw = os.path.splitext(video)[0] + ".f32"
    buf.tofile(raw)
    b.run(["ffmpeg", "-y", "-i", video, "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", raw, "-map", "0:v",
           "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", SAIDA])


if __name__ == "__main__":
    previa() if "--previa" in sys.argv else main()
