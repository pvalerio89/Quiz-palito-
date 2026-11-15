"""Short "Na escola: eu já ou eu nunca?" (escola-1), do vídeo 30. Formato de ESCOLHA (sem resposta certa).

Intro rapidinha, 1ª frase já com a chamada na faixa vermelha (anotar nos comentários, versão curta;
Patrick, 2026-11-12), 6 frases com os botões EU JÁ ✅ / EU NUNCA ❌, contagem de 3 s e a % de quem já fez.
Fala final curta (retenção, 2026-11-12).
Uso: py -3 build_short.py            (gera vozes que faltam e monta o Short)
     py -3 build_short.py --previa   (prancha com quadros para conferir)
"""
import asyncio, math, os, sys, tempfile
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import short_base as s
from short_base import b, W, H, FPS
sys.path.insert(0, os.path.join(QP, "videos", "modelo-opcoes"))
import engaja as eg

A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "short-escola-1.mp4")
CHAMADA = "SEJA SINCERO!"     # formato de escolha: as frases de s.CHAMADAS falam de "acertar"
MUSICA = os.path.join(QP, "musicas", "Carefree.mp3")
EMOJI = "C:/Windows/Fonts/seguiemj.ttf"
COUNT = 3.0
N = 6
VERDE, VERMELHO = (40, 175, 80), (225, 50, 60)

# emoji, frase, % "eu já", resposta falada, fundo (topo, base)
PERG = [
    ("⏰", "cheguei atrasado na aula", 88, "Quase todo mundo já!", ((20, 150, 80), (5, 70, 50))),
    ("👩", "chamei a professora de mãe sem querer", 61, "A maioria já!", ((30, 110, 210), (15, 40, 130))),
    ("📝", "fiz a lição de casa cinco minutos antes da aula", 79, "Setenta e nove por cento já!", ((150, 70, 200), (60, 25, 120))),
    ("🪑", "caí da cadeira na sala de aula", 29, "Pouca gente já!", ((0, 160, 170), (0, 70, 100))),
    ("🐶", "disse que o cachorro comeu minha lição", 8, "Quase ninguém já!", ((235, 60, 50), (120, 15, 30))),
    ("🎓", "fui o orador da formatura", 6, "Raríssima!", ((20, 150, 80), (5, 70, 50))),
]
FALAS = {
    "intro": "Na escola: eu já ou eu nunca?",                     # intro rapidinha (2 a 3 s)
    "gancho": "Seja sincero! Conta seus eu já e manda nos comentários!",
    "final": "Comenta quantos eu já!",                       # fala final curta (retenção)
}
CARD = (90, 340, 990, 940)
BTN_Y = (1075, 1235)
BTN_W, BTN_H = 780, 140
BAR = (110, 1370, 970, 1416)


def textos():
    t = dict(FALAS)
    for k, p in enumerate(PERG, 1):
        t[f"q{k}"] = f"Eu já... {p[1]}?"
        t[f"a{k}"] = p[3]
    t["q1"] = f"{FALAS['gancho']} Eu já... {PERG[0][1]}?"
    t.pop("gancho")
    return t


def vozes():
    import edge_tts
    if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
        import ssl, edge_tts.communicate as _c
        _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    for k, txt in textos().items():
        if not os.path.exists(A(f"{k}.mp3")):
            asyncio.run(edge_tts.Communicate(txt, "pt-BR-AntonioNeural", rate="+20%", pitch="+2Hz").save(A(f"{k}.mp3")))
            print("voz", k, "-", txt, flush=True)


_cache = {}


def emoji(ch, size):
    key = ("emoji", ch, size)
    if key not in _cache:
        f = ImageFont.truetype(EMOJI, 109)
        im = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((100, 100), ch, font=f, embedded_color=True, anchor="mm")
        im = im.crop(im.getbbox())
        r = size / max(im.size)
        _cache[key] = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    return _cache[key]


def cartao_sprite(k, p):
    key = ("cartao", k)
    if key not in _cache:
        x0, y0, x1, y1 = CARD
        w, h = x1 - x0, y1 - y0
        cv = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
        b.shadowed_round_rect(cv, (30, 30, 30 + w, 30 + h), 44, b.WHITE)
        d = ImageDraw.Draw(cv)
        d.rounded_rectangle([30, 30, 30 + w, 30 + h], 44, outline=b.NAVY, width=7)
        em = emoji(p[0], 220)
        cv.alpha_composite(em, (int(30 + w / 2 - em.width / 2), int(60 + 120 - em.height / 2)))
        d.text((30 + w / 2, 350), "EU JÁ...", font=b.font(b.F_BLACK, 78), fill=(220, 40, 60), anchor="mm")
        txt = p[1].upper()
        f = b.font(b.F_BLACK, 68)
        import build_naodiga as nd
        linhas = nd.wrap(d, txt, f, w - 80)
        while (len(linhas) > 3 or max(d.textlength(l, font=f) for l in linhas) > w - 80) and f.size > 36:
            f = b.font(b.F_BLACK, f.size - 3)
            linhas = nd.wrap(d, txt, f, w - 80)
        y = 505 - (len(linhas) - 1) * f.size * 0.6
        for i, l in enumerate(linhas):
            d.text((30 + w / 2, y + i * f.size * 1.2), l, font=f, fill=b.NAVY, anchor="mm")
        _cache[key] = cv
    return _cache[key]


def botao_sprite(lado, pct=None, frac=1.0, destaque=False):
    cor = VERDE if lado == 0 else VERMELHO
    rot = "EU JÁ" if lado == 0 else "EU NUNCA"
    key = ("btn", lado)
    if pct is None and key in _cache:
        return _cache[key]
    cv = Image.new("RGBA", (BTN_W + 60, BTN_H + 60), (0, 0, 0, 0))
    x0, y0, x1, y1 = 30, 30, 30 + BTN_W, 30 + BTN_H
    if destaque:
        g = Image.new("RGBA", cv.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).rounded_rectangle([x0 - 18, y0 - 18, x1 + 18, y1 + 18], 70, fill=(255, 240, 120, 220))
        cv.alpha_composite(g.filter(ImageFilter.GaussianBlur(14)))
    b.shadowed_round_rect(cv, (x0, y0, x1, y1), 64, cor if pct is None else (40, 45, 75))
    if pct is not None:
        v = pct if lado == 0 else 100 - pct
        xe = x0 + BTN_W * v / 100 * frac
        if xe > x0 + 4:
            m = Image.new("L", cv.size, 0)
            ImageDraw.Draw(m).rounded_rectangle([x0, y0, x1, y1], 64, fill=255)
            br = Image.new("L", cv.size, 0)
            ImageDraw.Draw(br).rectangle([x0, y0, xe, y1], fill=255)
            cv.paste(cor + (255,), (0, 0), ImageChops.multiply(m, br))
    d = ImageDraw.Draw(cv)
    d.rounded_rectangle([x0, y0, x1, y1], 64, outline=b.WHITE, width=8)
    if pct is None:
        e = emoji("✅" if lado == 0 else "❌", 84)
        cv.alpha_composite(e, (x0 + 36, int(y0 + BTN_H / 2 - e.height / 2)))
        d.text((x0 + 140 + (BTN_W - 160) / 2, y0 + BTN_H / 2), rot, font=b.font(b.F_BLACK, 76), fill=b.WHITE,
               anchor="mm", stroke_width=5, stroke_fill=b.NAVY)
        _cache[key] = cv
    else:
        v = pct if lado == 0 else 100 - pct
        d.text((x0 + 40, y0 + BTN_H / 2), rot, font=b.font(b.F_BLACK, 58), fill=b.WHITE, anchor="lm",
               stroke_width=4, stroke_fill=b.NAVY)
        d.text((x1 - 40, y0 + BTN_H / 2), f"{round(v * frac)}%", font=b.font(b.F_BLACK, 84), fill=b.YELLOW,
               anchor="rm", stroke_width=5, stroke_fill=b.NAVY)
    return cv


def base(k, p):
    key = ("base", k)
    if key not in _cache:
        img = s.fundo(*p[4], seed=k).convert("RGBA")
        s.pilula(ImageDraw.Draw(img), 600, 205, "NA ESCOLA: EU JÁ OU EU NUNCA?", (40, 60, 150), size=36, pad=30, h=92)
        _cache[key] = img
    return _cache[key].copy()


def colar(img, spr, cx, cy, sc):
    if sc <= 0.02:
        return
    w, h = max(1, int(spr.width * sc)), max(1, int(spr.height * sc))
    im = spr if abs(sc - 1) < 1e-3 else spr.resize((w, h), Image.BILINEAR)
    img.alpha_composite(im, (int(cx - w / 2), int(cy - h / 2)))


def zoom(img, z):
    if abs(z - 1) < 1e-3:
        return img
    w, h = img.size
    cw, ch = w / z, h / z
    x0, y0 = (w - cw) / 2, (h - ch) / 2
    return img.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))


pula = eg.pula


def barra(img, frac):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = BAR
    d.rounded_rectangle([x0 - 7, y0 - 7, x1 + 7, y1 + 7], 32, fill=b.WHITE)
    d.rounded_rectangle(BAR, 25, fill=(60, 70, 110))
    if frac > 0.002:
        d.rounded_rectangle([x0, y0, max(x0 + (x1 - x0) * frac, x0 + 50), y1], 25, fill=b.ORANGE if frac > 0.3 else b.RED)
    n = math.ceil(frac * COUNT)
    if n > 0:
        d.text(((x0 + x1) // 2, (y0 + y1) // 2), str(n), font=b.font(b.F_BLACK, 40), fill=b.WHITE, anchor="mm",
               stroke_width=4, stroke_fill=b.NAVY)


CCX, CCY = (CARD[0] + CARD[2]) // 2, (CARD[1] + CARD[3]) // 2


def placar(img, k, t, respondida=False):
    eg.pontos(img, 660, 288, k - 1 + (1 if respondida else 0), N, t, raio=21, gap=14, rotulo="FRASES:",
              rotulo_size=34, rotulo_acima=False)


def pergunta_frames(k, p, fala):
    total = fala + COUNT
    for n in range(int(total * FPS)):
        t = n / FPS
        frac = 1.0 if t < fala else 1 - (t - fala) / COUNT
        img = base(k, p)
        colar(img, cartao_sprite(k, p), CCX, CCY + 5 * math.sin(t * 2.2), pula(t / 0.4))
        for i in range(2):
            ent = pula((t - 0.25 - 0.14 * i) / 0.35)
            pulso = 1 + (0.05 * math.sin(t * 7 + i * math.pi) if t > fala else 0)
            dx = 4 * math.sin(t * 40 + i) if frac < 0.3 else 0
            colar(img, botao_sprite(i), 540 + dx, BTN_Y[i], ent * pulso)
        barra(img, frac)
        placar(img, k, t)
        pose = "pensando" if frac > 0.3 else "assustado"
        b.put_palito(img, pose, 240, 140, 300, int(6 * math.sin(t * (5 if pose == "pensando" else 16))))
        if k == 1:  # chamada por cima da 1ª frase enquanto o gancho é falado
            eg.faixa_gancho(img, 620, 240, "ANOTA NOS COMENTÁRIOS!\n" + CHAMADA, t, max(2.5, fala), larg=840, size=60)
        yield zoom(img, 1.0 + 0.03 * t / total).convert("RGB")


def resposta_frames(k, p, dur):
    maior = 0 if p[2] >= 50 else 1
    for n in range(int(dur * FPS)):
        t = n / FPS
        img = base(k, p)
        colar(img, cartao_sprite(k, p), CCX, CCY, 1.0)
        fr = min(1.0, t / 0.8)
        fr = fr * fr * (3 - 2 * fr)
        for i in range(2):
            sc = 1.0 + (0.08 * math.sin(min(t / 0.4, 1) * math.pi) + 0.03 if i == maior else 0)
            colar(img, botao_sprite(i, p[2], fr, destaque=(i == maior and t > 0.8)), 540, BTN_Y[i], sc)
        placar(img, k, t, respondida=True)
        sl = min(1.0, t / 0.3)
        b.put_palito(img, "comemorando", 240, 140, 300, int((1 - sl) * 120 + 6 * math.sin(t * 9)))
        yield zoom(img, 1.03 + 0.02 * t / dur).convert("RGB")


def final_base():
    img = s.fundo(seed=3).convert("RGBA")
    d = ImageDraw.Draw(img)
    s.texto(d, (540, 330), "QUANTOS \"EU JÁ\"", 100, b.WHITE)
    s.texto(d, (540, 460), "VOCÊ TEM?", 140, b.YELLOW)
    d.rounded_rectangle([300, 545, 780, 655], 50, fill=b.WHITE, outline=b.NAVY, width=7)
    d.text((540, 600), f"__ / {N}", font=b.font(b.F_BLACK, 80), fill=b.NAVY, anchor="mm")
    d.rounded_rectangle([110, 690, 970, 830], 50, fill=b.RED, outline=b.WHITE, width=8)
    s.texto(d, (540, 760), "COMENTA AÍ!", 70, b.WHITE, max_w=820)
    s.texto(d, (540, 900), "SEGUE O", 64, b.WHITE)
    b.selo(img, 540, 1000, 1.3)
    b.put_palito(img, "apontando", 380, 540, 1520)
    return img


def final_frames(dur):
    bs = final_base()
    for n in range(int(dur * FPS)):
        yield zoom(bs, 1.0 + 0.05 * n / FPS / dur).convert("RGB")


def intro_frames(dur):
    return s.intro_rapida("NA ESCOLA:", "EU JÁ OU NUNCA?", dur, [emoji(e, 200) for e in ("🏫", "✅", "❌")])


def previa():
    sys.path.insert(0, os.path.join(QP, "videos", "05-nao-diga-o-mesmo"))
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = list(pergunta_frames(1, PERG[0], 3.0))
    ims = [list(intro_frames(2.0))[40], fr[8], fr[100], list(resposta_frames(1, PERG[0], 1.2))[-1],
           list(pergunta_frames(3, PERG[2], 1.0))[50], list(resposta_frames(6, PERG[5], 1.2))[-1],
           list(final_frames(1.0))[10]]
    sheet = Image.new("RGB", (len(ims) * 370, 640), (25, 25, 25))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((360, 640)), (i * 370, 0))
    sheet.save(os.path.join(out, "prancha.jpg"), quality=85)
    print(out)


def main():
    sys.path.insert(0, os.path.join(QP, "videos", "05-nao-diga-o-mesmo"))
    vozes()
    tmp = tempfile.mkdtemp(prefix="short_escola_")
    sfx = b.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = s.Timeline(video)
    tl.sound(A("intro.mp3"), at=0.1, voz=True)
    for f in intro_frames(s.duracao(A("intro.mp3"))):
        tl.frame(f)
    for k, p in enumerate(PERG, 1):
        q = A(f"q{k}.mp3")
        tl.sound(sfx["whoosh"], vol=0.6)
        tl.sound(q, at=tl.t + 0.1, voz=True)
        fala = s.duracao(q) + 0.2
        for n in range(int(COUNT)):
            tl.sound(sfx["tick"], at=tl.t + fala + n, vol=0.8)
        for f in pergunta_frames(k, p, fala):
            tl.frame(f)
        a = A(f"a{k}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(a, at=tl.t + 0.15, voz=True)
        for f in resposta_frames(k, p, s.duracao(a) + 0.6):
            tl.frame(f)
    tl.sound(sfx["whoosh"])
    tl.sound(A("final.mp3"), at=tl.t + 0.2, voz=True)
    for f in final_frames(s.duracao(A("final.mp3")) + 0.8):
        tl.frame(f)
    tl.close()
    s.mixar(tl, video, MUSICA, SAIDA)
    print(f"OK {SAIDA} ({tl.t:.1f}s)")


if __name__ == "__main__":
    previa() if "--previa" in sys.argv else main()
