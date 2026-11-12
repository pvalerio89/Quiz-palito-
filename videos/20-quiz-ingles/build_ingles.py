"""Quiz Palito — "QUIZ DE INGLÊS DO 5º AO 9º ANO" (mais de 8 min, para anúncio no meio).

65 perguntas próprias de inglês escolar, em 5 blocos (5º, 6º, 7º, 8º e 9º ano), do fácil ao difícil.
Cada pergunta tem 3 alternativas A/B/C; a imagem é foto real (objeto, animal, comida) ou um cartão com a
palavra/frase (feito aqui, em cartoes/). No começo de cada série, a faixa avisa o ano e a fala apresenta.
Layout aprovado `videos/modelo-opcoes/opcoes.py` (intro rapidinha, chamada na 1ª pergunta, placar, sons, transição).
Uso: py -3 build_ingles.py            (monta quiz-palito-quiz-ingles.mp4)
     py -3 build_ingles.py --previa   (prancha em previa/)
     py -3 build_ingles.py --duracao  (só calcula a duração pelo tamanho das falas)
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
SAIDA = os.path.join(HERE, "quiz-palito-quiz-ingles.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Sneaky Snitch.mp3")
CRED = json.load(open(os.path.join(HERE, "creditos.json"), encoding="utf-8"))
GANCHO = "DO 5º AO 9º ANO:\nATÉ ONDE VOCÊ CHEGA?"
SUB = {5: "COMEÇANDO FÁCIL!", 6: "SUBINDO O NÍVEL!", 7: "AGORA COMPLICA!", 8: "CUIDADO COM AS PEGADINHAS!",
       9: "O NÍVEL MAIS DIFÍCIL!"}
COR_SERIE = {5: (40, 170, 90), 6: (30, 120, 220), 7: (150, 70, 200), 8: (255, 150, 0), 9: (230, 60, 90)}


def cartoes():
    """Cartão branco com a palavra ou frase (o "___" em laranja) para as perguntas sem foto."""
    pasta = os.path.join(HERE, "cartoes")
    os.makedirs(pasta, exist_ok=True)
    L = 720
    for r in R:
        if not r["texto"]:
            continue
        img = Image.new("RGB", (L, L), (255, 255, 255))
        d = ImageDraw.Draw(img)
        linhas = r["texto"].split("\n")
        dica = linhas.pop() if len(linhas) > 1 and linhas[-1].startswith("(") else None
        curto = len(linhas) == 1 and len(linhas[0]) <= 14
        size = 200 if curto and len(linhas[0]) <= 6 else (130 if curto else 88)
        fo = b.font(b.F_BLACK, size)
        if not curto:   # frase: quebra em linhas para a letra ficar grande
            palavras, linhas, cur = " ".join(linhas).split(), [], ""
            for p in palavras:
                if cur and d.textlength(cur + " " + p.replace("___", "____"), font=fo) > L - 90:
                    linhas.append(cur)
                    cur = p
                else:
                    cur = (cur + " " + p).strip()
            linhas.append(cur)
        while max(d.textlength(l.replace("___", "____"), font=fo) for l in linhas) > L - 70 and fo.size > 40:
            fo = b.font(b.F_BLACK, fo.size - 4)
        alt = fo.size * 1.25
        y = L / 2 - alt * (len(linhas) - 1) / 2 - (30 if dica else 0)
        for l in linhas:
            partes = l.split("___")
            tw = d.textlength(l.replace("___", "____"), font=fo)
            x = L / 2 - tw / 2
            for i, p in enumerate(partes):
                d.text((x, y), p, font=fo, fill=b.NAVY, anchor="lm")
                x += d.textlength(p, font=fo)
                if i < len(partes) - 1:
                    bw = d.textlength("____", font=fo)
                    d.rounded_rectangle([x + 4, y - fo.size * 0.45, x + bw - 4, y + fo.size * 0.45], 14,
                                        fill=b.ORANGE)
                    d.text((x + bw / 2, y), "?", font=fo, fill=b.WHITE, anchor="mm")
                    x += bw
            y += alt
        if dica:
            d.text((L / 2, y + 10), dica, font=b.font(b.F_BOLD, 54), fill=(120, 120, 150), anchor="mm")
        d.rounded_rectangle([L / 2 - 150, 36, L / 2 + 150, 106], 35, fill=COR_SERIE[r["serie"]])
        d.text((L / 2, 72), "ENGLISH", font=b.font(b.F_BLACK, 40), fill=b.WHITE, anchor="mm")
        img.save(os.path.join(pasta, f"txt-{r['n']}.png"))


def q_de(r):
    return {"n": r["n"], "pergunta": r["pergunta"], "foto": r["foto"], "opcoes": r["opcoes"], "certa": r["certa"]}


def selo_serie(img, serie):
    """Pílula com a série embaixo do número da pergunta."""
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([30, 192, 200, 248], 28, fill=COR_SERIE[serie], outline=b.WHITE, width=5)
    d.text((115, 221), f"{serie}º ANO", font=b.font(b.F_BLACK, 32), fill=b.WHITE, anchor="mm",
           stroke_width=2, stroke_fill=b.NAVY)
    return img


def com_serie(frames, serie):
    for f in frames:
        yield selo_serie(f, serie)


def placar_frames(n, dur):
    c1, c2 = (255, 170, 0), (215, 100, 0)
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = nd.burst(c1, c2, t * 12).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.3)
        b.text_outline(d, (800, 230), f"{n} JÁ FORAM!", b.font(b.F_BLACK, int(110 * (0.5 + 0.5 * s))), b.WHITE, w=11)
        b.text_outline(d, (800, 420), "QUANTAS VOCÊ", b.font(b.F_BLACK, int(140 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
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
    b.text_outline(d, (800, 200), "QUANTAS VOCÊ", b.font(b.F_BLACK, 120), b.WHITE, w=12)
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
    d.text((W / 2, 70), "CRÉDITOS DAS IMAGENS", font=b.font(b.F_BLACK, 44), fill=b.YELLOW, anchor="mm")
    d.text((W / 2, 130), "Fotos: Wikimedia Commons (autor, licença e arquivo)", font=b.font(b.F_BOLD, 28),
           fill=b.WHITE, anchor="mm")
    f = b.font(b.F_BOLD, 24)
    for i, t in enumerate(CRED["fotos"]):
        while d.textlength(t, font=f) > W - 100:
            t = t[:-2]
        d.text((50, 190 + i * 38), t, font=f, fill=b.WHITE)
    d.text((W / 2, H - 50), "Perguntas e cartões: Quiz Palito.", font=b.font(b.F_BOLD, 24), fill=(180, 180, 200),
           anchor="mm")
    return img


dur = lambda p: b.duration(p) if os.path.exists(p) else 1.2
RESP = lambda n: max(1.6, dur(A(f"p{n}.mp3")) + 0.6)
INICIO = {r["n"] for r in R if r["n"] == 1 or R[r["n"] - 2]["serie"] != r["serie"]}


def duracao():
    t = dur(A("intro.mp3"))
    for r in R:
        t += 0.6 + op.COUNT + RESP(r["n"])
        if r["n"] in INICIO:
            t += dur(A(f"q{r['n']}.mp3")) + 0.2
    for n in range(10, TOTAL, 10):
        t += dur(A(f"placar{n}.mp3")) + 0.8
    return t + max(4.0, dur(A("outro.mp3")) + 1.8) + 5


def gancho(r):
    return GANCHO if r["n"] == 1 else f"{r['serie']}º ANO!\n{SUB[r['serie']]}"


INTRO_FOTOS = ["big-ben.jpg", "estatua-da-liberdade.jpg", "ponte-golden-gate.jpg"]


def intro_frames(d):
    return op.intro_rapida("QUIZ DE INGLÊS", "5º AO 9º ANO!", d, fotos=INTRO_FOTOS)


def previa():
    cartoes()
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40],
          selo_serie(list(op.pergunta_frames(q_de(R[0]), TOTAL, fala=3.0, gancho=GANCHO))[15], 5)]
    for k in (4, 13, 28, 32, 43, 52, 60):
        r = R[k]
        f = 3.0 if r["n"] in INICIO else 0.0
        pf = list(op.pergunta_frames(q_de(r), TOTAL, fala=f, gancho=gancho(r) if f else None))
        fr.append(selo_serie(pf[int(op.COUNT * FPS * 0.5)], r["serie"]))
        fr.append(selo_serie(list(op.resposta_frames(q_de(r), 1.0, TOTAL, t0=op.COUNT))[-1], r["serie"]))
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
    fo = Image.new("RGB", (12 * 205, math.ceil(len(fotos) / 12) * 235), "white")
    dd = ImageDraw.Draw(fo)
    for i, (f, r) in enumerate(zip(fotos, R)):
        x, y = (i % 12) * 205, (i // 12) * 235
        fo.paste(f, (x, y))
        dd.text((x + 100, y + 216), f"{r['n']}. {r['opcoes'][r['certa']]}"[:24], font=b.font(b.F_BOLD, 17),
                fill="black", anchor="mm")
    fo.save(os.path.join(out, "imagens.jpg"), quality=85)
    print(out, f"duração estimada {duracao():.0f}s")


def main():
    cartoes()
    tmp = tempfile.mkdtemp(prefix="quiz_ingles_")
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
        if n in INICIO:
            marcas[str(r["serie"])] = tl.t
        fala = dur(A(f"q{n}.mp3")) + 0.2 if n in INICIO else 0.0
        q = q_de(r)
        if ultimo is not None:
            tl.sound(sfx["whoosh"], vol=0.7)
            for f in op.transicao_frames(ultimo, q, TOTAL):
                tl.frame(f)
        if n in INICIO:   # série (e, na 1ª, a chamada) falada por cima da pergunta
            tl.sound(A(f"q{n}.mp3"), at=tl.t + 0.1)
        op.sons_pergunta(tl, sfx, tl.t, fala=fala, entrada=ultimo is None)
        for f in com_serie(op.pergunta_frames(q, TOTAL, fala=fala, gancho=gancho(r) if n in INICIO else None),
                           r["serie"]):
            tl.frame(f)
        tl.sound(A(f"p{n}.mp3"), at=tl.t + 0.25)
        for f in com_serie(op.resposta_frames(q, RESP(n), TOTAL, t0=fala + op.COUNT), r["serie"]):
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
