"""Quiz Palito — "ADIVINHE O JOGADOR PELA FOTO" (mais de 8 min, para anúncio no meio).

38 perguntas próprias (craques e 5 técnicos), do fácil ao difícil. A foto real começa com ZOOM e DESFOQUE e vai
abrindo durante a contagem; na resposta aparece inteira. 3 alternativas A/B/C, pergunta falada com as
alternativas, contagem de 7 s, resposta com reação curta (regras de retenção, 2026-11-12).
Layout aprovado `videos/modelo-opcoes/opcoes.py` (intro rapidinha, chamada na 1ª pergunta, placar, sons, transição).
Uso: py -3 build_jogador.py            (monta quiz-palito-jogador-pela-foto.mp4)
     py -3 build_jogador.py --previa   (prancha em previa/)
     py -3 build_jogador.py --duracao  (só calcula a duração pelo tamanho das falas)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
from opcoes import b, nd, W, H, FPS

op.FOTOS = os.path.join(HERE, "fotos")
R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-jogador-pela-foto.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Sneaky Snitch.mp3")
CRED = json.load(open(os.path.join(HERE, "creditos.json"), encoding="utf-8"))
COUNT = 7.0
GANCHO = f"{TOTAL} CRAQUES:\nNO FIM FICA DIFÍCIL!"


class Revela:
    """Cartão da foto que começa com zoom + desfoque e vai abrindo na contagem (usa o encaixe de clipe do
    opcoes: q["_clipe"].cartao() a cada quadro). Depois da pergunta (na resposta) fica nítida."""

    def __init__(self, nome, fala, count=COUNT):
        self.src = Image.open(os.path.join(op.FOTOS, nome)).convert("RGB")
        self.s = op.CARD - 40
        self.fala, self.count, self.i = fala, count, 0
        self.n1 = int((fala + count) * FPS)
        m = Image.new("L", (self.s, self.s), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, self.s - 1, self.s - 1], int(self.s * 0.07), fill=255)
        self.mask = m

    def imagem(self, p):
        """p = 0 (escondida: zoom 2,2x e bem borrada) .. 1 (inteira e nítida)."""
        z = 1 + 1.2 * (1 - p) ** 1.5
        w = self.src.width / z
        cx, cy = self.src.width * 0.5, self.src.height * 0.40
        x0 = min(max(cx - w / 2, 0), self.src.width - w)
        y0 = min(max(cy - w / 2, 0), self.src.height - w)
        im = self.src.resize((self.s, self.s), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + w))
        r = 26 * (1 - p) ** 1.4
        return im.filter(ImageFilter.GaussianBlur(r)) if r > 0.3 else im

    def cartao(self):
        t = self.i / FPS
        self.i += 1
        if self.i <= self.n1:
            p = 0.82 * min(1.0, max(0.0, (t - self.fala) / self.count))   # nunca fica 100% antes da resposta
        else:
            p = min(1.0, 0.82 + (self.i - self.n1) / (0.3 * FPS))
        im = self.imagem(p).convert("RGBA")
        im.putalpha(self.mask)
        sp = op.moldura_sprite().copy()
        sp.alpha_composite(im, (50, 50))
        if p < 1:
            d = ImageDraw.Draw(sp)
            d.rounded_rectangle([62, 62, 322, 126], 32, fill=b.RED, outline=b.WHITE, width=5)
            d.text((192, 95), "REVELANDO...", font=b.font(b.F_BLACK, 30), fill=b.WHITE, anchor="mm")
        return sp

    def fechar(self):
        pass


def q_de(r, fala=None):
    q = {"n": r["n"], "pergunta": r["pergunta"], "foto": r["foto"], "opcoes": r["opcoes"], "certa": r["certa"]}
    if fala is not None:
        q["clipe"] = r["foto"]
        q["_clipe"] = Revela(r["foto"], fala)
    return q


def placar_frames(n, dur):
    c1, c2 = (255, 170, 0), (215, 100, 0)
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = nd.burst(c1, c2, t * 12).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.3)
        b.text_outline(d, (800, 230), f"{n} JÁ FORAM!", b.font(b.F_BLACK, int(110 * (0.5 + 0.5 * s))), b.WHITE, w=11)
        b.text_outline(d, (800, 420), "QUANTOS VOCÊ", b.font(b.F_BLACK, int(140 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
        b.text_outline(d, (800, 580), "ACERTOU?", b.font(b.F_BLACK, int(140 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
        if s >= 1:
            d.rounded_rectangle([420, 680, 1180, 800], 60, fill=(255, 255, 255, 240), outline=b.NAVY, width=7)
            d.text((800, 740), f"__ / {n}", font=b.font(b.F_BLACK, 80), fill=b.NAVY, anchor="mm")
        b.selo(img, 800, 910, 1.1)
        b.put_palito(img, "apontando", 620, 1620 + int((1 - s) * 700), 1060, int(6 * math.sin(t * 5)))
        yield img.convert("RGB")


def outro_base():
    img = op.fundo(3).copy()
    d = ImageDraw.Draw(img)
    b.text_outline(d, (800, 200), "QUANTOS VOCÊ", b.font(b.F_BLACK, 120), b.WHITE, w=12)
    b.text_outline(d, (800, 345), "ACERTOU?", b.font(b.F_BLACK, 150), b.YELLOW, w=15)
    d.rounded_rectangle([450, 430, 1150, 545], 55, fill=(255, 255, 255, 240), outline=b.NAVY, width=7)
    d.text((800, 488), f"__ / {TOTAL}", font=b.font(b.F_BLACK, 80), fill=b.NAVY, anchor="mm")
    d.rounded_rectangle([250, 590, 1350, 710], 55, fill=b.RED, outline=b.WHITE, width=8)
    d.text((800, 650), "PAUSA E COMENTA SUA NOTA!", font=b.font(b.F_BLACK, 62), fill=b.WHITE, anchor="mm",
           stroke_width=3, stroke_fill=b.NAVY)
    b.text_outline(d, (800, 790), "MARCA UM AMIGO E INSCREVA-SE NO", b.font(b.F_BLACK, 54), b.WHITE, w=7)
    b.selo(img, 800, 910, 1.3)
    return img


def creditos_base():
    img = Image.new("RGBA", (W, H), (20, 24, 48, 255))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 50), "CRÉDITOS DAS IMAGENS", font=b.font(b.F_BLACK, 40), fill=b.YELLOW, anchor="mm")
    d.text((W / 2, 98), "Fotos: Wikimedia Commons (autor, licença e arquivo)", font=b.font(b.F_BOLD, 24),
           fill=b.WHITE, anchor="mm")
    f = b.font(b.F_BOLD, 19)
    itens = [f"{k}: {c['autor']} ({c['lic']}), {c['file'].replace('_', ' ')}" for k, c in CRED.items()]
    meio = (len(itens) + 1) // 2
    for col, parte in enumerate((itens[:meio], itens[meio:])):
        for i, t in enumerate(parte):
            while d.textlength(t, font=f) > W / 2 - 60:
                t = t[:-2]
            d.text((30 + col * W / 2, 135 + i * 41), t, font=f, fill=b.WHITE)
    d.text((W / 2, H - 30), "Perguntas: Quiz Palito.", font=b.font(b.F_BOLD, 22), fill=(180, 180, 200), anchor="mm")
    return img


dur = lambda p: b.duration(p) if os.path.exists(p) else 1.2
RESP = lambda n: max(1.8, dur(A(f"p{n}.mp3")) + 0.6)
FALA = lambda n: dur(A(f"q{n}.mp3")) + 0.2


def duracao():
    t = dur(A("intro.mp3"))
    for r in R:
        t += 0.6 + FALA(r["n"]) + COUNT + RESP(r["n"])
    for n in range(10, TOTAL, 10):
        t += dur(A(f"placar{n}.mp3")) + 0.8
    return t + max(4.0, dur(A("outro.mp3")) + 1.8) + 6


INTRO_FOTOS = ["maracana.jpg", "estadio-camp-nou.jpg", "estadio-bernabeu.jpg", "allianz-arena.jpg"]


def intro_frames(d):
    return op.intro_rapida("ADIVINHE O JOGADOR", "PELA FOTO!", d, fotos=INTRO_FOTOS)


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40]]
    for k in (0, 4, 12, 23, 37):
        r = R[k]
        f = FALA(r["n"])
        q = q_de(r, f)
        pf = list(op.pergunta_frames(q, TOTAL, count=COUNT, fala=f, gancho=GANCHO if k == 0 else None))
        fr += [pf[15], pf[int((f + COUNT * 0.6) * FPS)]]
        fr.append(list(op.resposta_frames(q, 1.0, TOTAL, t0=f + COUNT))[-1])
    fr.append(list(op.transicao_frames(fr[-1], q_de(R[5]), TOTAL))[9])
    fr.append(list(placar_frames(10, 0.5))[-1])
    fr.append(next(nd.anima(outro_base().convert("RGBA"), "acenando", 0.1)))
    fr.append(creditos_base().convert("RGB"))
    cols = 3
    th = [f.resize((640, 360), Image.LANCZOS) for f in fr]
    pr = Image.new("RGB", (cols * 650, math.ceil(len(th) / cols) * 370), "black")
    for i, f in enumerate(th):
        pr.paste(f, ((i % cols) * 650, (i // cols) * 370))
    pr.save(os.path.join(out, "prancha.jpg"), quality=88)
    fotos = [Image.open(os.path.join(op.FOTOS, r["foto"])).resize((200, 200)) for r in R]
    fo = Image.new("RGB", (10 * 205, math.ceil(len(fotos) / 10) * 235), "white")
    dd = ImageDraw.Draw(fo)
    for i, (f, r) in enumerate(zip(fotos, R)):
        x, y = (i % 10) * 205, (i // 10) * 235
        fo.paste(f, (x, y))
        dd.text((x + 100, y + 216), f"{r['n']}. {r['opcoes'][r['certa']]}"[:24], font=b.font(b.F_BOLD, 17),
                fill="black", anchor="mm")
    fo.save(os.path.join(out, "imagens.jpg"), quality=85)
    print(out, f"duração estimada {duracao():.0f}s")


def main():
    tmp = tempfile.mkdtemp(prefix="quiz_jogador_")
    sfx = op.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    marcas = {}
    tl.sound(A("intro.mp3"), at=0.15)   # intro rapidinha (Patrick, 2026-11-10)
    ultimo = None
    for f in intro_frames(dur(A("intro.mp3"))):
        tl.frame(f)
        ultimo = f
    for r in R:
        n = r["n"]
        if n in (1, 11, 21, 31):
            marcas[str(n)] = tl.t
        fala = FALA(n)
        q = q_de(r, fala)
        tl.sound(sfx["whoosh"], vol=0.7)
        for f in op.transicao_frames(ultimo, q_de(r), TOTAL):
            tl.frame(f)
        tl.sound(A(f"q{n}.mp3"), at=tl.t + 0.1)   # pergunta falada com as alternativas
        op.sons_pergunta(tl, sfx, tl.t, fala=fala, count=COUNT, entrada=False)
        for f in op.pergunta_frames(q, TOTAL, count=COUNT, fala=fala, gancho=GANCHO if n == 1 else None):
            tl.frame(f)
        tl.sound(A(f"p{n}.mp3"), at=tl.t + 0.25)
        for f in op.resposta_frames(q, RESP(n), TOTAL, t0=fala + COUNT):
            tl.frame(f)
            ultimo = f
        if n % 10 == 0 and n < TOTAL:
            v = A(f"placar{n}.mp3")
            tl.sound(sfx["whoosh"])
            tl.sound(v, at=tl.t + 0.3)
            for f in placar_frames(n, dur(v) + 0.8):
                tl.frame(f)
                ultimo = f
            print(f"{n}/{TOTAL} ({tl.t / 60:.1f} min)", flush=True)
    marcas["final"] = tl.t
    tl.sound(sfx["whoosh"])
    tl.sound(A("outro.mp3"), at=tl.t + 0.4)
    for f in nd.anima(outro_base().convert("RGBA"), "acenando", max(4.0, dur(A("outro.mp3")) + 1.8)):
        tl.frame(f)
    cr = creditos_base().convert("RGB")
    for _ in range(int(6 * FPS)):
        tl.frame(cr)
    total = tl.t
    tl.close()
    json.dump(marcas, open(os.path.join(HERE, "tempos.json"), "w", encoding="utf-8"), indent=1)
    nd.HERE, nd.SAIDA = HERE, SAIDA
    nd.A = lambda x: MUSICA if x == "musica.mp3" else A(x)
    nd.mixar(tl, video, total)
    print(f"OK {SAIDA} ({total:.1f}s)")


if __name__ == "__main__":
    if "--duracao" in sys.argv:
        print(f"{duracao():.1f}s")
    elif "--previa" in sys.argv:
        previa()
    else:
        main()
