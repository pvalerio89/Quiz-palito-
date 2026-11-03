"""Short 1 — "Você acerta essas 6 bandeiras? Só 1% acerta a última!"

Reaproveita as bandeiras, os nomes narrados e a música do vídeo de 195 bandeiras.
Uso: py -3 build_short.py            (gera as vozes que faltam e monta o Short)
     py -3 build_short.py --previa   (só salva imagens das telas em previa/)
"""
import asyncio, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import short_base as s
from short_base import b, W, H, FPS

BAND = os.path.join(QP, "videos", "03-bandeiras-195")
A_BAND = lambda n: os.path.join(BAND, "assets", n)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "short-bandeiras-1.mp4")

COUNT, POP = 3.0, 0.3
VERDE, LARANJA, VERMELHO = (40, 190, 90), b.ORANGE, b.RED
# (código, nome, nº do áudio no vídeo de 195, nível, cor)
PERGUNTAS = [
    ("jp", "Japão", 10, "FÁCIL", VERDE),
    ("mx", "México", 12, "FÁCIL", VERDE),
    ("gr", "Grécia", 21, "MÉDIO", LARANJA),
    ("np", "Nepal", 62, "MÉDIO", LARANJA),
    ("lk", "Sri Lanka", 94, "DIFÍCIL", VERMELHO),
    ("bt", "Butão", 179, "IMPOSSÍVEL", (150, 40, 190)),
]
FALAS = {
    "gancho": "Você acerta essas seis bandeiras? Só um por cento acerta a última!",
    "ultima": "Agora a última! Só um por cento acerta!",
    "final": "Quantas você acertou? Comenta aí! E o desafio completo, com cento e noventa e cinco bandeiras, tá no canal!",
}
FLAG_C, FLAG_MAX = (540, 795), (900, 460)


def vozes():
    import edge_tts
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    for k, txt in FALAS.items():
        if not os.path.exists(A(f"{k}.mp3")):
            asyncio.run(edge_tts.Communicate(txt, "pt-BR-AntonioNeural", rate="+20%", pitch="+2Hz").save(A(f"{k}.mp3")))
            print("voz", k, flush=True)


def cartao(code, scale=1.0):
    fl = Image.open(os.path.join(BAND, "bandeiras", f"{code}.png")).convert("RGBA")
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
    return card


def put_card(img, card):
    img.alpha_composite(card, (FLAG_C[0] - card.width // 2, FLAG_C[1] - card.height // 2))


def topo(img, i, p, titulo):
    d = ImageDraw.Draw(img)
    b.selo(img, 540, 210, 1.1)
    d = ImageDraw.Draw(img)
    s.texto(d, (540, 345), titulo, 96, b.YELLOW)
    s.pilula(d, 540, 460, f"{i + 1}/6  •  {p[3]}", p[4], size=46)


def pergunta_frames(i, p):
    vazio = s.fundo().convert("RGBA")
    topo(vazio, i, p, "QUE PAÍS É ESSE?")
    s.trilho(vazio)
    for k in range(int(POP * FPS)):
        x = (k + 1) / (POP * FPS)
        sc = 0.6 + 0.48 * x if x < 0.8 else 1.08 - 0.08 * (x - 0.8) / 0.2
        img = vazio.copy()
        put_card(img, cartao(p[0], sc))
        yield s.barra(img, 1.0, COUNT, k / FPS)
    base = vazio.copy()
    put_card(base, cartao(p[0]))
    n = int(COUNT * FPS)
    for k in range(n):
        yield s.barra(base, 1 - k / n, COUNT, k / FPS)


def faixa(img, nome, pop):
    d = ImageDraw.Draw(img)
    f = b.font(b.F_BLACK, 110)
    while d.textlength(nome, font=f) > 820 and f.size > 50:
        f = b.font(b.F_BLACK, f.size - 4)
    full = max(620, int(d.textlength(nome, font=f)) + 130)
    bw = int(full * pop)
    if bw > 40:
        d.rounded_rectangle([540 - bw // 2, 1080, 540 + bw // 2, 1220], 44, fill=b.YELLOW, outline=b.NAVY, width=10)
        if pop >= 1.0:
            d.text((540, 1150), nome, font=f, fill=b.NAVY, anchor="mm")


def resposta_frames(i, p, dur):
    base = s.fundo().convert("RGBA")
    topo(base, i, p, "RESPOSTA")
    put_card(base, cartao(p[0]))
    for k in range(int(dur * FPS)):
        t = k / FPS
        pop = min(1.0, t / 0.25)
        img = base.copy()
        faixa(img, p[1], pop)
        sl = min(1.0, t / 0.3)
        b.put_palito(img, "comemorando", 280, 540, 1560, int((1 - sl) * 400 + 6 * math.sin(t * 8)))
        yield img.convert("RGB")


def gancho_base():
    img = s.gradient(b.TEAL, b.BLUE).convert("RGBA")
    b.selo(img, 540, 210, 1.1)
    d = ImageDraw.Draw(img)
    s.texto(d, (540, 380), "VOCÊ ACERTA", 110, b.WHITE)
    s.texto(d, (540, 520), "6 BANDEIRAS?", 140, b.YELLOW)
    for k, code in enumerate(["jp", "np", "bt"]):
        fl = Image.open(os.path.join(BAND, "bandeiras", f"{code}.png")).convert("RGBA")
        r = min(260 / fl.width, 175 / fl.height)
        fl = fl.resize((int(fl.width * r), int(fl.height * r)), Image.LANCZOS)
        cx = 220 + k * 320
        b.shadowed_round_rect(img, (cx - fl.width // 2 - 12, 700 - fl.height // 2 - 12,
                                    cx + fl.width // 2 + 12, 700 + fl.height // 2 + 12), 18, b.WHITE)
        img.alpha_composite(fl, (cx - fl.width // 2, 700 - fl.height // 2))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([90, 880, 990, 1040], 50, fill=b.RED, outline=b.WHITE, width=8)
    s.texto(d, (540, 960), "SÓ 1% ACERTA A ÚLTIMA!", 72, b.WHITE, max_w=840)
    s.texto(d, (540, 1130), "3 SEGUNDOS CADA", 70, b.WHITE)
    b.put_palito(img, "assustado", 360, 540, 1575)
    return img.convert("RGB")


def ultima_frames(dur):
    for k in range(int(dur * FPS)):
        t = k / FPS
        img = s.burst((240, 80, 80), (200, 30, 40), t * 14).convert("RGBA")
        d = ImageDraw.Draw(img)
        sc = min(1.0, t / 0.25)
        s.texto(d, (540, 620), "A ÚLTIMA!", int(170 * (0.5 + 0.5 * sc)), b.YELLOW)
        s.texto(d, (540, 820), "SÓ 1% ACERTA", int(110 * (0.5 + 0.5 * sc)), b.WHITE)
        b.selo(img, 540, 1010, 1.0)
        b.put_palito(img, "assustado", 360, 540 + int((1 - sc) * 600), 1575, int(6 * math.sin(t * 12)))
        yield img.convert("RGB")


def final_base():
    img = s.fundo(seed=3).convert("RGBA")
    b.selo(img, 540, 210, 1.1)
    d = ImageDraw.Draw(img)
    s.texto(d, (540, 390), "QUANTAS VOCÊ", 110, b.WHITE)
    s.texto(d, (540, 520), "ACERTOU?", 140, b.YELLOW)
    d.rounded_rectangle([140, 640, 940, 780], 50, fill=b.RED, outline=b.WHITE, width=8)
    s.texto(d, (540, 710), "COMENTA AÍ!", 80, b.WHITE)
    s.texto(d, (540, 900), "DESAFIO COMPLETO:", 64, b.WHITE)
    s.texto(d, (540, 1010), "195 BANDEIRAS", 104, b.YELLOW)
    s.texto(d, (540, 1110), "NO CANAL!", 72, b.WHITE)
    b.put_palito(img, "apontando", 360, 540, 1575)
    return img.convert("RGB")


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    gancho_base().save(os.path.join(out, "1_gancho.jpg"), quality=88)
    fr = list(pergunta_frames(0, PERGUNTAS[0]))
    fr[40].save(os.path.join(out, "2_pergunta.jpg"), quality=88)
    fr[-4].save(os.path.join(out, "2_pergunta_fim.jpg"), quality=88)
    list(resposta_frames(5, PERGUNTAS[5], 0.8))[-1].save(os.path.join(out, "3_resposta.jpg"), quality=88)
    list(ultima_frames(0.6))[-1].save(os.path.join(out, "4_ultima.jpg"), quality=88)
    final_base().save(os.path.join(out, "5_final.jpg"), quality=88)
    print(out)


def main():
    vozes()
    tmp = tempfile.mkdtemp(prefix="short_")
    sfx = b.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = s.Timeline(video)
    tl.sound(A("gancho.mp3"), at=0.1, voz=True)
    tl.hold(gancho_base(), s.duracao(A("gancho.mp3")) + 0.3)
    for i, p in enumerate(PERGUNTAS):
        if i == len(PERGUNTAS) - 1:
            tl.sound(sfx["whoosh"])
            tl.sound(A("ultima.mp3"), at=tl.t + 0.1, voz=True)
            for f in ultima_frames(s.duracao(A("ultima.mp3")) + 0.3):
                tl.frame(f)
        tl.sound(sfx["whoosh"], vol=0.6)
        st = tl.t + POP
        for k in range(int(COUNT)):
            tl.sound(sfx["tick"], at=st + k, vol=0.8)
        for f in pergunta_frames(i, p):
            tl.frame(f)
        aa = A_BAND(f"a{p[2]}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(aa, at=tl.t + 0.2, voz=True)
        for f in resposta_frames(i, p, max(1.6, s.duracao(aa) + 0.6)):
            tl.frame(f)
    tl.sound(sfx["whoosh"])
    tl.sound(A("final.mp3"), at=tl.t + 0.2, voz=True)
    tl.hold(final_base(), s.duracao(A("final.mp3")) + 0.8)
    tl.close()
    s.mixar(tl, video, A_BAND("musica.mp3"), SAIDA)
    print(f"OK {SAIDA} ({tl.t:.1f}s)")


if __name__ == "__main__":
    previa() if "--previa" in sys.argv else main()
