"""Quiz Palito — "SUPER QUIZ DE FUTEBOL MUNDIAL" (mais de 8 min, para anúncio no meio).

72 perguntas de futebol do mundo todo, do fácil ao difícil: país do time pelo escudo, craque pela bandeira,
estádios, apelidos, campeões das Copas (até 2022) e onde os craques começaram. Cada pergunta tem imagem real
(escudo, bandeira ou foto do jogador, preparadas por itens.py em fotos/) e 3 alternativas A/B/C.
Layout aprovado `videos/modelo-opcoes/opcoes.py` (intro rapidinha, chamada na 1ª pergunta, placar, sons, transição).
Uso: py -3 build_futebol.py            (monta quiz-palito-futebol-mundial.mp4)
     py -3 build_futebol.py --previa   (prancha em previa/)
     py -3 build_futebol.py --duracao  (só calcula a duração pelo tamanho das falas)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
from opcoes import b, nd, W, H, FPS

op.FOTOS = os.path.join(HERE, "fotos")
R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-futebol-mundial.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Carefree.mp3")
CRED = json.load(open(os.path.join(HERE, "creditos.json"), encoding="utf-8"))
GANCHO = "SÓ QUEM ENTENDE DE\nFUTEBOL GABARITA!"


def q_de(r):
    return {"n": r["n"], "pergunta": r["pergunta"], "foto": r["foto"], "opcoes": r["opcoes"], "certa": r["certa"]}


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
    """Tela final curta: de onde vieram as imagens."""
    img = Image.new("RGBA", (W, H), (20, 24, 48, 255))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 55), "CRÉDITOS DAS IMAGENS", font=b.font(b.F_BLACK, 40), fill=b.YELLOW, anchor="mm")
    y = 110
    f = b.font(b.F_BOLD, 22)
    d.text((40, y), "Fotos (Wikimedia Commons):", font=b.font(b.F_BOLD, 26), fill=b.YELLOW)
    y += 38
    for t in CRED["fotos"]:
        while d.textlength(t, font=f) > W - 80:
            t = t[:-2]
        d.text((40, y), t, font=f, fill=b.WHITE)
        y += 30
    y += 14
    d.text((40, y), "Escudos: marcas dos respectivos clubes (imagens da Wikipédia):", font=b.font(b.F_BOLD, 26),
           fill=b.YELLOW)
    y += 40
    cols, fe = 3, b.font(b.F_BOLD, 18)
    por = math.ceil(len(CRED["escudos"]) / cols)
    for i, t in enumerate(CRED["escudos"]):
        while d.textlength(t, font=fe) > W / cols - 30:
            t = t[:-2]
        d.text((40 + (i // por) * (W / cols), y + (i % por) * 26), t, font=fe, fill=b.WHITE)
    d.text((W / 2, H - 70), "Bandeiras: domínio público (Wikimedia Commons).", font=b.font(b.F_BOLD, 24),
           fill=b.WHITE, anchor="mm")
    d.text((W / 2, H - 32), "Vídeo de quiz sem ligação com clubes, jogadores ou a FIFA.", font=b.font(b.F_BOLD, 22),
           fill=(180, 180, 200), anchor="mm")
    return img


dur = lambda p: b.duration(p) if os.path.exists(p) else 1.2
RESP = lambda n: max(1.6, dur(A(f"p{n}.mp3")) + 0.6)


def duracao():
    t = dur(A("intro.mp3")) + 0.6 + dur(A("q1.mp3")) + 0.2 + op.COUNT + RESP(1)
    for r in R[1:]:
        t += 0.6 + op.COUNT + RESP(r["n"])
    for n in range(10, TOTAL, 10):
        t += dur(A(f"placar{n}.mp3")) + 0.8
    return t + max(4.0, dur(A("outro.mp3")) + 1.8) + 5


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40], list(op.pergunta_frames(q_de(R[0]), TOTAL, fala=3.0, gancho=GANCHO))[15]]
    for k in (2, 12, 21, 39, 52, 64, 68):
        pf = list(op.pergunta_frames(q_de(R[k]), TOTAL))
        fr += [pf[int(op.COUNT * FPS * 0.5)]]
        fr.append(list(op.resposta_frames(q_de(R[k]), 1.0, TOTAL, t0=op.COUNT))[-1])
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
    # todas as imagens com a resposta, para conferir
    fotos = [Image.open(os.path.join(op.FOTOS, r["foto"])).resize((200, 200)) for r in R]
    fo = Image.new("RGB", (12 * 205, math.ceil(len(fotos) / 12) * 235), "white")
    dd = ImageDraw.Draw(fo)
    for i, (f, r) in enumerate(zip(fotos, R)):
        x, y = (i % 12) * 205, (i // 12) * 235
        fo.paste(f, (x, y))
        dd.text((x + 100, y + 216), f"{r['n']}. {r['opcoes'][r['certa']]}"[:24], font=b.font(b.F_BOLD, 17), fill="black", anchor="mm")
    fo.save(os.path.join(out, "imagens.jpg"), quality=85)
    print(out, f"duração estimada {duracao():.0f}s")


INTRO_FOTOS = ["escudo-gremio.jpg", "band-br.jpg", "escudo-manchester-city.jpg", "escudo-botafogo.jpg", "band-jp.jpg"]


def intro_frames(d):
    return op.intro_rapida("SUPER QUIZ", "DE FUTEBOL!", d, fotos=INTRO_FOTOS)


def main():
    tmp = tempfile.mkdtemp(prefix="quiz_futebol_")
    sfx = op.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    marcas = {}
    # intro rapidinha (Patrick, 2026-11-10): título + imagens do tema + Palito acenando, depois transição
    tl.sound(A("intro.mp3"), at=0.15)
    ultimo = None
    for f in intro_frames(dur(A("intro.mp3"))):
        tl.frame(f)
        ultimo = f
    for r in R:
        n = r["n"]
        if n % 10 == 1:
            marcas[str(n)] = tl.t
        primeira = n == 1
        fala = 0.0
        q = q_de(r)
        if ultimo is not None:
            tl.sound(sfx["whoosh"], vol=0.7)
            for f in op.transicao_frames(ultimo, q, TOTAL):
                tl.frame(f)
        if primeira:   # chamada por cima da 1ª pergunta, logo depois da intro rapidinha
            tl.sound(A("q1.mp3"), at=tl.t + 0.1)
            fala = dur(A("q1.mp3")) + 0.2
        op.sons_pergunta(tl, sfx, tl.t, fala=fala, entrada=ultimo is None)
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
