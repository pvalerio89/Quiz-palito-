"""Quiz Palito — vídeo 25 "QUIZ DE MATEMÁTICA DO 6º AO 9º ANO" (mais de 8 min, para anúncio no meio).

36 perguntas próprias de matemática escolar, em 4 blocos (6º, 7º, 8º e 9º ano), do fácil ao difícil. A imagem
de cada pergunta é um cartão com a conta ou a figura (feito aqui, em cartoes/). 3 alternativas A/B/C.
Layout `modelo-opcoes/opcoes.py` + ESTILO MAIS HUMANO `modelo-opcoes/humano.py`.
Uso: py -3 build_matematica.py            (monta quiz-palito-quiz-matematica.mp4)
     py -3 build_matematica.py --previa   (prancha em previa/)
     py -3 build_matematica.py --duracao  (só calcula a duração pelo tamanho das falas)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
import humano as hu
from opcoes import b, nd, W, H, FPS

op.FOTOS = os.path.join(HERE, "cartoes")
R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-quiz-matematica.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Sneaky Snitch.mp3")
GANCHO = f"{TOTAL} PERGUNTAS:\nNO FIM FICA DIFÍCIL!"
SUB = {7: "AGORA COM NEGATIVOS!", 8: "SUBINDO O NÍVEL!", 9: "O NÍVEL MAIS DIFÍCIL!"}
COR_SERIE = {6: (40, 170, 90), 7: (30, 120, 220), 8: (255, 150, 0), 9: (230, 60, 90)}
CURTIR_DEPOIS = 3
INICIO = {r["n"] for r in R if r["n"] > 1 and R[r["n"] - 2]["serie"] != r["serie"]}
INTRO = ["+", "÷", "π", "√"]


# ---------- cartões ----------

def texto_exp(d, xy, txt, fo, cor, medir=False):
    """Escreve o texto com "^" como expoente (menor e mais alto). Devolve a largura."""
    partes = txt.split("^")
    fe = b.font(b.F_BLACK, int(fo.size * 0.55))
    larg = d.textlength(partes[0], font=fo) + sum(d.textlength(p[:1], font=fe) + d.textlength(p[1:], font=fo)
                                                  for p in partes[1:])
    if medir:
        return larg
    x, y = xy[0] - larg / 2, xy[1]
    d.text((x, y), partes[0], font=fo, fill=cor, anchor="lm")
    x += d.textlength(partes[0], font=fo)
    for p in partes[1:]:
        d.text((x + 2, y - fo.size * 0.42), p[:1], font=fe, fill=cor, anchor="lm")
        x += d.textlength(p[:1], font=fe) + 6
        d.text((x, y), p[1:], font=fo, fill=cor, anchor="lm")
        x += d.textlength(p[1:], font=fo)
    return larg


def forma(d, tipo, L, cor=(30, 120, 220)):
    """Figura geométrica na metade de cima do cartão."""
    lw, f = 12, b.font(b.F_BLACK, 52)
    cx, cy = L / 2, L * 0.40
    if tipo == "quadrado":
        s = 260
        d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], outline=cor, width=lw, fill=(225, 240, 255))
        d.text((cx, cy + s / 2 + 40), "5 cm", font=f, fill=b.NAVY, anchor="mm")
        d.text((cx + s / 2 + 22, cy), "5 cm", font=f, fill=b.NAVY, anchor="lm")
    elif tipo == "retangulo":
        w, h = 400, 150
        d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], outline=cor, width=lw, fill=(225, 240, 255))
        d.text((cx, cy + h / 2 + 40), "8 cm", font=f, fill=b.NAVY, anchor="mm")
        d.text((cx + w / 2 + 20, cy), "3 cm", font=f, fill=b.NAVY, anchor="lm")
    elif tipo == "triangulo":
        pts = [(cx - 230, cy + 140), (cx + 230, cy + 140), (cx - 40, cy - 170)]
        d.polygon(pts, outline=cor, width=lw, fill=(225, 240, 255))
        for (x, y), t in zip(pts, "abc"):
            d.text((x + (cx - x) * 0.28, y + (cy + 30 - y) * 0.28), t, font=f, fill=b.RED, anchor="mm")
    elif tipo == "pitagoras":
        p0, p1, p2 = (cx - 160, cy + 150), (cx + 160, cy + 150), (cx - 160, cy - 150)
        d.polygon([p0, p1, p2], outline=cor, width=lw, fill=(225, 240, 255))
        d.rectangle([p0[0] + 6, p0[1] - 50, p0[0] + 50, p0[1] - 6], outline=b.NAVY, width=5)
        d.text((cx, cy + 195), "4", font=f, fill=b.NAVY, anchor="mm")
        d.text((cx - 205, cy), "3", font=f, fill=b.NAVY, anchor="mm")
        d.text((cx + 40, cy - 30), "?", font=b.font(b.F_BLACK, 80), fill=b.RED, anchor="mm")
    elif tipo == "angulo":
        o = (cx - 150, cy + 150)
        d.line([o, (cx + 200, cy + 150)], fill=cor, width=lw + 4)
        d.line([o, (cx - 150, cy - 200)], fill=cor, width=lw + 4)
        d.rectangle([o[0] + 8, o[1] - 80, o[0] + 80, o[1] - 8], outline=b.RED, width=8)
        d.text((cx + 60, cy - 40), "?°", font=b.font(b.F_BLACK, 90), fill=b.RED, anchor="mm")
    elif tipo == "hexagono":
        r = 180
        pts = [(cx + r * math.cos(math.radians(60 * k)), cy + r * math.sin(math.radians(60 * k))) for k in range(6)]
        d.polygon(pts, outline=cor, width=lw, fill=(225, 240, 255))
        d.text((cx, cy), "6 lados", font=f, fill=b.NAVY, anchor="mm")


def cartao(r, L=720):
    img = Image.new("RGB", (L, L), (255, 255, 255))
    d = ImageDraw.Draw(img)
    # papel quadriculado de caderno
    for k in range(0, L, 40):
        d.line([(k, 0), (k, L)], fill=(225, 235, 248), width=2)
        d.line([(0, k), (L, k)], fill=(225, 235, 248), width=2)
    linhas = r["cartao"]
    if r["forma"]:
        forma(d, r["forma"], L)
        if r["forma"] in ("hexagono", "angulo"):
            linhas = []
        y0, size = L * 0.84, 70
    else:
        size = 150 if len(linhas) == 1 else 110
        y0 = L / 2 + 20 - (len(linhas) - 1) * size * 0.6
    fo = b.font(b.F_BLACK, size)
    while linhas and max(texto_exp(d, (0, 0), t, fo, b.NAVY, medir=True) for t in linhas) > L - 80 and fo.size > 40:
        fo = b.font(b.F_BLACK, fo.size - 4)
    for i, t in enumerate(linhas):
        texto_exp(d, (L / 2, y0 + i * fo.size * 1.2), t, fo, b.RED if "?" in t else b.NAVY)
    d.rounded_rectangle([L / 2 - 190, 30, L / 2 + 190, 100], 35, fill=COR_SERIE[r["serie"]])
    d.text((L / 2, 66), f"{r['serie']}º ANO", font=b.font(b.F_BLACK, 42), fill=b.WHITE, anchor="mm")
    return img


def cartoes():
    pasta = op.FOTOS
    os.makedirs(pasta, exist_ok=True)
    for r in R:
        cartao(r).save(os.path.join(pasta, r["foto"]))
    for k, s in enumerate(INTRO):   # símbolos da intro (não aparecem nas perguntas assim)
        img = Image.new("RGB", (300, 300), COR_SERIE[6 + k])
        ImageDraw.Draw(img).text((150, 140), s, font=b.font(b.F_BLACK, 200), fill=b.WHITE, anchor="mm")
        img.save(os.path.join(pasta, f"intro{k}.png"))


# ---------- vídeo ----------

def q_de(r):
    q = {k: r[k] for k in ("n", "pergunta", "foto", "opcoes", "certa")}
    if "dica_txt" in r:
        q["dica"] = (A(f"d{r['n']}.mp3"), r["dica_txt"], 2.5)
    if "fala_s" in r:
        q["suspense"] = A(f"s{r['n']}.mp3")
    for k in ("aviso", "sabia", "final"):
        if k in r:
            q[k] = r[k]
    return q


def selo_serie(img, serie):
    """Pílula com a série embaixo do número da pergunta."""
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([30, 192, 200, 248], 28, fill=COR_SERIE[serie], outline=b.WHITE, width=5)
    d.text((115, 221), f"{serie}º ANO", font=b.font(b.F_BLACK, 32), fill=b.WHITE, anchor="mm",
           stroke_width=2, stroke_fill=b.NAVY)
    return img


def gancho(r):
    if r["n"] == 1:
        return GANCHO
    if r["n"] in INICIO:
        return f"{r['serie']}º ANO!\n{SUB[r['serie']]}"
    return None


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
    return t + dur(A("outro.mp3")) + 1.8


def intro_frames(d):
    return op.intro_rapida("QUIZ DE", "MATEMÁTICA!", d, fotos=[f"intro{k}.png" for k in range(len(INTRO))])


def previa():
    cartoes()
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40]]
    for k in (0, 8, 15, 23, 27, 35):
        r = R[k]
        q = q_de(r)
        f = dur(A(f"q{r['n']}.mp3")) + 0.3
        pf = list(hu.pergunta_frames(q, TOTAL, f, r["count"], gancho(r)))
        fr += [selo_serie(pf[15], r["serie"]),
               selo_serie(pf[min(len(pf) - 1, int((f + 2.5 + 0.6) * FPS))], r["serie"])]
        fr.append(selo_serie(list(hu.resposta_frames(q, TOTAL, 3.0))[-1], r["serie"]))
    fr.append(list(op.transicao_frames(fr[-1], q_de(R[5]), TOTAL))[9])
    fr.append(list(placar_frames(10, 0.5))[-1])
    fr.append(list(hu.curtir_frames(3.0, 1.0))[-1])
    fr.append(list(hu.ultima_frames(1.0))[-1])
    fr.append(list(hu.inscreva_frames(1.0))[-1])
    cols = 3
    th = [f.resize((640, 360), Image.LANCZOS) for f in fr]
    pr = Image.new("RGB", (cols * 650, math.ceil(len(th) / cols) * 370), "black")
    for i, f in enumerate(th):
        pr.paste(f, ((i % cols) * 650, (i // cols) * 370))
    pr.save(os.path.join(out, "prancha.jpg"), quality=88)
    fotos = [Image.open(os.path.join(op.FOTOS, r["foto"])).resize((200, 200)) for r in R]
    fo = Image.new("RGB", (9 * 205, math.ceil(len(fotos) / 9) * 235), "white")
    dd = ImageDraw.Draw(fo)
    for i, (f, r) in enumerate(zip(fotos, R)):
        x, y = (i % 9) * 205, (i // 9) * 235
        fo.paste(f, (x, y))
        dd.text((x + 100, y + 216), f"{r['n']}. {r['opcoes'][r['certa']]}"[:24], font=b.font(b.F_BOLD, 17),
                fill="black", anchor="mm")
    fo.save(os.path.join(out, "imagens.jpg"), quality=85)
    print(out, f"duração estimada {duracao():.0f}s")


def main():
    cartoes()
    tmp = tempfile.mkdtemp(prefix="quiz_matematica_")
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
        if n == 1 or n in INICIO:
            marcas[str(n)] = tl.t
        q = q_de(r)
        if q.get("final"):
            for f in hu.ultima(tl, sfx, A("ultima.mp3")):
                tl.frame(f)
                ultimo = f
        for f in hu.pergunta(tl, sfx, q, TOTAL, ultimo, A(f"q{n}.mp3"), A(f"p{n}.mp3"), count=r["count"],
                             gancho=gancho(r)):
            f = selo_serie(f, r["serie"])
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
