"""Quiz Palito — "ALFABETO DOS TIMES DE A A Z" com os ESCUDOS (mais de 8 min, para anúncio no meio).

Para cada letra, escudos de times do Brasil e do mundo. O escudo aparece PIXELADO e vai ficando nítido nos 5 s
(assim o nome escrito no escudo não entrega a resposta logo); 3 alternativas com a MESMA letra.
Layout aprovado `videos/modelo-opcoes/opcoes.py` (sem tela de abertura, chamada por cima da 1ª pergunta,
placar de bolinhas, sons, transição). Escudos: imagem do artigo de cada clube na Wikipédia (escudos/, créditos na
tela final).
Uso: py -3 build_times.py            (monta quiz-palito-alfabeto-dos-times.mp4)
     py -3 build_times.py --previa   (prancha em previa/)
     py -3 build_times.py --duracao  (só calcula a duração pelo tamanho das falas)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
from opcoes import b, nd, W, H, FPS

R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-alfabeto-dos-times.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Carefree.mp3")
CRED = json.load(open(os.path.join(HERE, "creditos.json"), encoding="utf-8"))
GANCHO = "DE A A Z: SÓ CRAQUE\nACERTA TODOS!"
_cache = {}
PIX0, PIX1 = 46, 7        # tamanho do "pixel" no começo e no fim do tempo


def escudo(nome_arq, lado):
    im = Image.open(os.path.join(HERE, "escudos", nome_arq)).convert("RGBA")
    im.thumbnail((lado, lado), Image.LANCZOS)
    q = Image.new("RGBA", (lado, lado), (255, 255, 255, 255))
    q.alpha_composite(im, ((lado - im.width) // 2, (lado - im.height) // 2))
    return q


def pixelar(im, px):
    if px <= 1:
        return im
    w, h = im.size
    return im.resize((max(1, w // px), max(1, h // px)), Image.BILINEAR).resize((w, h), Image.NEAREST)


class Escudo:
    """Faz o papel do 'clipe' do modelo: cartão novo a cada quadro (pixelado -> nítido; nítido na resposta)."""

    def __init__(self, r, n_perg, fala):
        self.base = escudo(r["escudo"], op.CARD - 80)
        self.n_perg, self.fala, self.i = n_perg, fala, 0

    def cartao(self):
        t = self.i / FPS
        self.i += 1
        if self.i <= self.n_perg:
            p = min(1.0, max(0.0, (t - self.fala) / op.COUNT))
            im = pixelar(self.base, int(PIX0 + (PIX1 - PIX0) * p ** 0.7))
        else:
            im = self.base
        sp = op.moldura_sprite().copy()
        sp.alpha_composite(im, (70, 70))
        return sp

    def fechar(self):
        pass


def q_de(r, fala=0.0):
    q = {"n": r["n"], "pergunta": f"LETRA {r['letra']}: QUE TIME É ESSE?", "foto": r["escudo"], "clipe": True,
         "opcoes": r["opcoes"], "certa": r["certa"]}
    q["_clipe"] = Escudo(r, int((fala + op.COUNT) * FPS), fala)
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
    """Tela final: de onde vieram os escudos (artigo de cada clube na Wikipédia)."""
    img = Image.new("RGBA", (W, H), (20, 24, 48, 255))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 60), "ESCUDOS: marcas dos respectivos clubes (imagens da Wikipédia)", font=b.font(b.F_BOLD, 34),
           fill=b.YELLOW, anchor="mm")
    linhas = [f"{r['nome']}: {CRED[r['nome']]['file'][:38]}" for r in R]
    cols = 4
    por = math.ceil(len(linhas) / cols)
    passo = min(36, (H - 160) // por)
    f = b.font(b.F_BOLD, 17)
    for i, t in enumerate(linhas):
        while d.textlength(t, font=f) > W / cols - 24:
            t = t[:-2]
        d.text((16 + (i // por) * (W / cols), 110 + (i % por) * passo), t, font=f, fill=b.WHITE)
    d.text((W / 2, H - 34), "Vídeo de quiz sem ligação com os clubes.  •  Wikimedia / Wikipedia", font=b.font(b.F_BOLD, 22),
           fill=(180, 180, 200), anchor="mm")
    return img


dur = lambda p: b.duration(p) if os.path.exists(p) else 1.2
RESP = lambda n: max(1.6, dur(A(f"p{n}.mp3")) + 0.6)


def duracao():
    t = dur(A("q1.mp3")) + 0.2 + op.COUNT + RESP(1)
    for r in R[1:]:
        t += 0.6 + op.COUNT + RESP(r["n"])
    for n in range(10, TOTAL, 10):
        t += dur(A(f"placar{n}.mp3")) + 0.8
    return t + max(4.0, dur(A("outro.mp3")) + 1.8) + 5


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(op.pergunta_frames(q_de(R[0], 3.0), TOTAL, fala=3.0, gancho=GANCHO))[15]]
    for k in (3, 15, 30, 45, TOTAL - 1):
        pf = list(op.pergunta_frames(q_de(R[k]), TOTAL))
        fr += [pf[5], pf[int(op.COUNT * FPS * 0.8)]]
        q = q_de(R[k])
        q["_clipe"].i = 10 ** 6
        fr.append(list(op.resposta_frames(q, 1.0, TOTAL, t0=op.COUNT))[-1])
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
    print(out, f"duração estimada {duracao():.0f}s")


def main():
    tmp = tempfile.mkdtemp(prefix="quiz_times_")
    sfx = op.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    marcas = {}
    ultimo = None
    for r in R:
        n = r["n"]
        if n % 10 == 1:
            marcas[str(n)] = tl.t
        primeira = n == 1
        fala = 0.0
        if primeira:   # sem tela de abertura: apresentação falada por cima da 1ª pergunta
            tl.sound(A("q1.mp3"), at=0.1)
            fala = dur(A("q1.mp3")) + 0.2
        q = q_de(r, fala)
        if primeira:
            pass
        elif ultimo is not None:
            tl.sound(sfx["whoosh"], vol=0.7)
            for f in op.transicao_frames(ultimo, q, TOTAL):
                tl.frame(f)
        op.sons_pergunta(tl, sfx, tl.t, fala=fala, entrada=not primeira and ultimo is None)
        for f in op.pergunta_frames(q, TOTAL, fala=fala, gancho=GANCHO if primeira else None):
            tl.frame(f)
        tl.sound(A(f"p{n}.mp3"), at=tl.t + 0.25)
        for f in op.resposta_frames(q, RESP(n), TOTAL, t0=fala + op.COUNT):
            tl.frame(f)
            ultimo = f
        if n % 10 == 0 and n < TOTAL:
            v = A(f"placar{n}.mp3")
            tl.sound(sfx["whoosh"])
            tl.sound(v, at=tl.t + 0.3)
            for f in placar_frames(n, dur(v) + 0.8):
                tl.frame(f)
            ultimo = None
            print(f"{n}/{TOTAL} ({tl.t / 60:.1f} min)", flush=True)
    marcas["final"] = tl.t
    tl.sound(sfx["whoosh"])
    tl.sound(A("outro.mp3"), at=tl.t + 0.4)
    for f in nd.anima(outro_base().convert("RGBA"), "acenando", max(4.0, dur(A("outro.mp3")) + 1.8)):
        tl.frame(f)
    cr = creditos_base().convert("RGB")
    for _ in range(int(5 * FPS)):
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
