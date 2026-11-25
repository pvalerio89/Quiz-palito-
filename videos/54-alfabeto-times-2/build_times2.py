"""Quiz Palito — vídeo 54 "Alfabeto dos TIMES de A a Z — PARTE 2" (10 a 13 min).

36 times novos (nenhuma resposta da parte 1, vídeo 16): o ESCUDO aparece PIXELADO e vai ficando nítido durante a
contagem (o nome escrito no escudo não entrega logo); 3 alternativas A/B/C com a mesma letra. Na resposta o escudo
fica nítido com o nome numa faixa. Fundo verde-gramado/laranja/vermelho (cara diferente dos 52 roxo e 53 turquesa).
Layout `modelo-opcoes/opcoes.py` + ESTILO MAIS HUMANO `humano.py` + transição splash.
Uso: py -3 build_times2.py            (monta quiz-palito-alfabeto-times-2.mp4)
     py -3 build_times2.py --previa   (prancha em previa/)
     py -3 build_times2.py --duracao  (só calcula a duração pelo tamanho das falas)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
import humano as hu
from opcoes import b, nd, W, H, FPS

op.FOTOS = os.path.join(HERE, "cartoes")
op.CORES = [((40, 150, 70), (10, 75, 35)), ((235, 120, 25), (150, 55, 5)), ((200, 35, 50), (100, 10, 25)),
            ((30, 130, 60), (5, 60, 30))]   # gramado/laranja/vermelho (≠ 52 roxo, 53 turquesa)
COR = (40, 150, 70)
CRED = json.load(open(os.path.join(HERE, "creditos.json"), encoding="utf-8"))
R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-alfabeto-times-2.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Sneaky Snitch.mp3")
GANCHO = "36 ESCUDOS DE A A Z:\nO ÚLTIMO NINGUÉM ACERTA!"
CURTIR_DEPOIS = 3          # pedido de inscrição/like depois da 3ª resposta
INTRO_FOTOS = ["intro-1.png", "intro-2.png", "intro-3.png", "intro-4.png"]   # escudos que não são respostas
INTRO_SRC = ["fortaleza.png", "corinthians.png", "real-madrid.png", "flamengo.png"]   # (da parte 1)
PIX0, PIX1 = 48, 9        # tamanho do "pixel" no começo e no fim da contagem


def escudo_img(arq, lado):
    im = Image.open(os.path.join(HERE, "escudos", arq)).convert("RGBA")
    im.thumbnail((lado, lado), Image.LANCZOS)
    q = Image.new("RGBA", (lado, lado), (255, 255, 255, 255))
    q.alpha_composite(im, ((lado - im.width) // 2, (lado - im.height) // 2))
    return q


def pixelar(im, px):
    if px <= 1:
        return im
    w, h = im.size
    return im.resize((max(1, w // px), max(1, h // px)), Image.BILINEAR).resize((w, h), Image.NEAREST)


def selo_letra(sp, letra):
    d = ImageDraw.Draw(sp)
    d.rounded_rectangle([52, 52, 212, 212], 34, fill=COR, outline=b.WHITE, width=6)
    d.text((132, 134), letra, font=b.font(b.F_BLACK, 120), fill=b.WHITE, anchor="mm", stroke_width=5,
           stroke_fill=b.NAVY)


class Escudo:
    """Faz o papel do 'clipe' do modelo: pixelado -> quase nítido na contagem; nítido + nome na resposta."""

    def __init__(self, r):
        self.r = r
        self.base = escudo_img(r["escudo"], op.CARD - 120)
        self.i, self.fala, self.count, self.modo = 0, 1.0, 7.0, "espera"

    def iniciar(self, fala, count):
        self.i, self.fala, self.count, self.modo = 0, fala, count, "pergunta"

    def cartao(self):
        sp = op.moldura_sprite().copy()
        if self.modo == "resposta":
            sp.alpha_composite(self.base, (90, 70))
            d = ImageDraw.Draw(sp)
            nome = self.r["nome"]
            fo = b.font(b.F_BLACK, 70)
            while d.textlength(nome, font=fo) > op.CARD - 120 and fo.size > 34:
                fo = b.font(b.F_BLACK, fo.size - 3)
            y = op.CARD - 40
            d.rounded_rectangle([60, y - 130, op.CARD - 20, y - 20], 30, fill=b.NAVY)
            d.text(((op.CARD + 40) / 2, y - 75), nome, font=fo, fill=b.YELLOW, anchor="mm")
            return sp
        if self.modo == "pergunta":
            t = self.i / FPS
            self.i += 1
            p = min(1.0, max(0.0, (t - self.fala) / self.count))
        else:
            p = 1.0 if self.modo == "suspense" else 0.0
        sp.alpha_composite(pixelar(self.base, int(PIX0 + (PIX1 - PIX0) * p ** 0.7)), (90, 70))
        selo_letra(sp, self.r["letra"])
        return sp

    def fechar(self):
        pass


_pf, _sf, _rf = hu.pergunta_frames, hu.suspense_frames, hu.resposta_frames


def pergunta_frames(q, total, fala, count, gancho=None):
    q["_clipe"].iniciar(fala, count)
    yield from _pf(q, total, fala, count, gancho)
    q["_clipe"].modo = "suspense"


def resposta_frames(q, total, d):
    q["_clipe"].modo = "resposta"
    yield from _rf(q, total, d)


hu.pergunta_frames, hu.resposta_frames = pergunta_frames, resposta_frames


def q_de(r):
    q = {k: r[k] for k in ("n", "pergunta", "foto", "opcoes", "certa")}
    q["clipe"] = True
    q["_clipe"] = Escudo(r)
    if "dica_txt" in r:
        q["dica"] = (A(f"d{r['n']}.mp3"), r["dica_txt"], 2.5)
    if "fala_s" in r:
        q["suspense"] = A(f"s{r['n']}.mp3")
    for k in ("aviso", "sabia", "final"):
        if k in r:
            q[k] = r[k]
    return q


def cartoes():
    """Só as imagens da abertura (escudos da parte 1, que não são respostas aqui)."""
    os.makedirs(op.FOTOS, exist_ok=True)
    for nome, src in zip(INTRO_FOTOS, INTRO_SRC):
        p = os.path.join(VIDEOS, "16-alfabeto-times", "escudos", src)
        if os.path.exists(p):
            escudo_img_src = Image.open(p).convert("RGBA")
            escudo_img_src.thumbnail((260, 260), Image.LANCZOS)
            q = Image.new("RGBA", (300, 300), (255, 255, 255, 255))
            q.alpha_composite(escudo_img_src, ((300 - escudo_img_src.width) // 2, (300 - escudo_img_src.height) // 2))
            q.convert("RGB").save(os.path.join(op.FOTOS, nome))


def creditos_base():
    img = Image.new("RGBA", (W, H), (20, 40, 28, 255))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 46), "CRÉDITOS DAS IMAGENS", font=b.font(b.F_BLACK, 40), fill=b.YELLOW, anchor="mm")
    d.text((W / 2, 92), "Escudos: Wikipédia/Wikimedia Commons (autor, licença e arquivo). Marcas dos clubes.",
           font=b.font(b.F_BOLD, 22), fill=b.WHITE, anchor="mm")
    f = b.font(b.F_BOLD, 16)
    itens = [f"{k}: {c['autor'] or '-'} ({c['lic']}), {c['file'].replace('_', ' ')}" for k, c in CRED.items()]
    itens += ["Abertura: Fortaleza, Corinthians, Real Madrid, Flamengo (ver vídeo 'Alfabeto dos times')"]
    meio = (len(itens) + 1) // 2
    for col, parte in enumerate((itens[:meio], itens[meio:])):
        for i, t in enumerate(parte):
            while d.textlength(t, font=f) > W / 2 - 60:
                t = t[:-2]
            d.text((30 + col * W / 2, 125 + i * 25), t, font=f, fill=b.WHITE)
    d.text((W / 2, H - 28), "Perguntas: Quiz Palito.", font=b.font(b.F_BOLD, 22), fill=(180, 200, 180), anchor="mm")
    return img


def placar_frames(n, dur):
    c1, c2 = (40, 150, 70), (10, 75, 35)
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = nd.burst(c1, c2, t * 12).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.3)
        b.text_outline(d, (800, 230), f"{n} ESCUDOS!", b.font(b.F_BLACK, int(110 * (0.5 + 0.5 * s))), b.WHITE, w=11)
        b.text_outline(d, (800, 420), "QUANTOS VOCÊ", b.font(b.F_BLACK, int(140 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
        b.text_outline(d, (800, 580), "ACERTOU?", b.font(b.F_BLACK, int(140 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
        if s >= 1:
            d.rounded_rectangle([420, 680, 1180, 800], 60, fill=(255, 255, 255, 240), outline=b.NAVY, width=7)
            d.text((800, 740), f"__ / {n}", font=b.font(b.F_BLACK, 80), fill=b.NAVY, anchor="mm")
        b.selo(img, 800, 910, 1.1)
        b.put_palito(img, "apontando", 620, 1620 + int((1 - s) * 700), 1060, int(6 * math.sin(t * 5)))
        yield img.convert("RGB")


dur = lambda p: b.duration(p) if os.path.exists(p) else 1.2


def duracao():
    t = dur(A("intro.mp3")) + 0.4
    for r in R:
        n = r["n"]
        t += 0.6 + dur(A(f"q{n}.mp3")) + 0.3 + r["count"]
        if "fala_s" in r:
            t += dur(A(f"s{n}.mp3")) + 0.9
        dr = dur(A(f"p{n}.mp3")) + 0.3
        t += (max(dr, 5.5) if "sabia" in r else dr) + 0.7
        if n % 10 == 0 and n < TOTAL:
            t += dur(A(f"placar{n}.mp3")) + 0.8
    t += dur(A("curtir.mp3")) + 0.3 + 1.6 + dur(A("espero.mp3")) + 0.6
    t += dur(A("ultima.mp3")) + 0.8
    return t + dur(A("outro.mp3")) + 1.8 + 5


def intro_frames(d):
    return op.intro_rapida("TIMES DE A a Z", "PARTE 2", d, fotos=INTRO_FOTOS, cor=1,
                          abertura=os.path.join(HERE, "abertura.jpg"))


def previa():
    cartoes()
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40]]
    for k in (0, 7, 17, 30, 33, 35):
        r = R[k]
        q = q_de(r)
        f = dur(A(f"q{r['n']}.mp3")) + 0.3
        pf = list(hu.pergunta_frames(q, TOTAL, f, r["count"], GANCHO if k == 0 else None))
        fr += [pf[15], pf[min(len(pf) - 1, int((f + 2.5 + 0.6) * FPS))]]
        fr.append(list(hu.resposta_frames(q, TOTAL, 3.0))[-1])
    fr.append(list(op.transicao_frames(fr[-1], q_de(R[5]), TOTAL))[9])
    fr.append(list(placar_frames(10, 0.5))[-1])
    fr.append(list(hu.curtir_frames(3.0, 1.0))[-1])
    fr.append(list(hu.ultima_frames(1.0))[-1])
    fr.append(list(hu.inscreva_frames(1.0))[-1])
    fr.append(creditos_base().convert("RGB"))
    cols = 3
    th = [f.resize((640, 360), Image.LANCZOS) for f in fr]
    pr = Image.new("RGB", (cols * 650, math.ceil(len(th) / cols) * 370), "black")
    for i, f in enumerate(th):
        pr.paste(f, ((i % cols) * 650, (i // cols) * 370))
    pr.save(os.path.join(out, "prancha.jpg"), quality=88)
    th = []
    for r in R:
        im = escudo_img(r["escudo"], 200).convert("RGB")
        th.append((im, r))
    fo = Image.new("RGB", (6 * 270, math.ceil(len(th) / 6) * 300), "white")
    dd = ImageDraw.Draw(fo)
    for i, (im, r) in enumerate(th):
        x, y = (i % 6) * 270, (i // 6) * 300
        fo.paste(im, (x + 35, y + 5))
        dd.text((x + 135, y + 225), f"{r['n']}. {r['letra']}: {r['nome']}", font=b.font(b.F_BOLD, 15), fill="black", anchor="mm")
        dd.text((x + 135, y + 250), " / ".join(o[:12] for o in r["opcoes"]), font=b.font(b.F_BOLD, 11), fill=(90, 90, 90), anchor="mm")
    fo.save(os.path.join(out, "escudos.jpg"), quality=85)
    print(out, f"duração estimada {duracao():.0f}s")


def main():
    cartoes()
    tmp = tempfile.mkdtemp(prefix="quiz_times2_")
    sfx = hu.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    marcas = {}
    di = dur(A("intro.mp3")) + 0.4
    tl.sound(A("intro.mp3"), at=0.15)   # intro rapidinha (Patrick, 2026-11-10)
    ultimo = None
    for f in intro_frames(di):
        tl.frame(f)
        ultimo = f
    for r in R:
        n = r["n"]
        if n in (1, 13, 25):
            marcas[str(n)] = tl.t
        q = q_de(r)
        if q.get("final"):
            for f in hu.ultima(tl, sfx, A("ultima.mp3")):
                tl.frame(f)
                ultimo = f
        for f in hu.pergunta(tl, sfx, q, TOTAL, ultimo, A(f"q{n}.mp3"), A(f"p{n}.mp3"), count=r["count"],
                             gancho=GANCHO if n == 1 else None):
            tl.frame(f)
            ultimo = f
        if n == CURTIR_DEPOIS:
            for f in hu.curtir(tl, sfx, A("curtir.mp3"), A("espero.mp3")):
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
    for f in hu.inscreva(tl, sfx, A("outro.mp3")):
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
