"""Quiz Palito — vídeo 38 "PAIS contra FILHOS: prova do 5º ano" (10 a 13 min, pensado para a TV/família).

32 perguntas próprias do 5º ano (português, matemática, ciências, geografia, história) em 3 rodadas (fácil, médio,
difícil). A imagem de cada pergunta é um cartão de caderno com a matéria (feito aqui, em cartoes/). 3 alternativas A/B/C.
Placar "PAIS x FILHOS" a cada 10 questões para a família marcar. Fundo roxo/azul (cara diferente dos últimos).
Layout `modelo-opcoes/opcoes.py` + ESTILO MAIS HUMANO `modelo-opcoes/humano.py`.
Uso: py -3 build_pais_filhos.py            (monta quiz-palito-pais-contra-filhos.mp4)
     py -3 build_pais_filhos.py --previa   (prancha em previa/)
     py -3 build_pais_filhos.py --duracao  (só calcula a duração pelo tamanho das falas)
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
op.CORES = [((120, 60, 200), (45, 20, 110)), ((30, 120, 220), (15, 45, 140)), ((0, 160, 170), (0, 80, 100)),
            ((150, 70, 200), (60, 25, 120)), ((230, 60, 90), (130, 20, 60)), ((40, 90, 200), (20, 30, 110))]
R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-pais-contra-filhos.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Wallpaper.mp3")
GANCHO = f"PAIS x FILHOS: {TOTAL} QUESTÕES!\nCADA UM MARCA OS PONTOS!"
SUB = {2: "SUBINDO O NÍVEL!", 3: "DERRUBA ATÉ ADULTO!"}
COR_MAT = {"PORTUGUÊS": (30, 120, 220), "MATEMÁTICA": (230, 60, 90), "CIÊNCIAS": (40, 170, 90),
           "GEOGRAFIA": (255, 140, 0), "HISTÓRIA": (150, 70, 200)}
COR_INTRO = [(230, 60, 90), (30, 120, 220), (40, 170, 90), (255, 140, 0)]
CURTIR_DEPOIS = 3
INICIO = {r["n"] for r in R if r["n"] > 1 and R[r["n"] - 2]["rodada"] != r["rodada"]}
INTRO = ["5º", "A+", "x", "?"]


# ---------- cartões ----------

def cartao(r, L=720):
    """Cartão de caderno com a palavra/frase bem grande."""
    img = Image.new("RGB", (L, L), (255, 255, 255))
    d = ImageDraw.Draw(img)
    for k in range(0, L, 40):   # papel quadriculado de caderno
        d.line([(k, 0), (k, L)], fill=(225, 235, 248), width=2)
        d.line([(0, k), (L, k)], fill=(225, 235, 248), width=2)
    linhas = r["cartao"]
    size = 140 if len(linhas) == 1 else 96
    fo = b.font(b.F_BLACK, size)
    while max(d.textlength(t, font=fo) for t in linhas) > L - 80 and fo.size > 40:
        fo = b.font(b.F_BLACK, fo.size - 4)
    y0 = L / 2 + 30 - (len(linhas) - 1) * fo.size * 0.6
    for i, t in enumerate(linhas):
        dica = t.startswith("(")
        f = b.font(b.F_BOLD, int(fo.size * 0.6)) if dica else fo
        d.text((L / 2, y0 + i * fo.size * 1.2), t, font=f, fill=(120, 130, 150) if dica else
               (b.RED if "_" in t else b.NAVY), anchor="mm")
    cor = COR_MAT[r["materia"]]
    fp = b.font(b.F_BLACK, 40)
    w = d.textlength(r["materia"], font=fp) / 2 + 40
    d.rounded_rectangle([L / 2 - w, 30, L / 2 + w, 100], 35, fill=cor)
    d.text((L / 2, 66), r["materia"], font=fp, fill=b.WHITE, anchor="mm")
    return img


def cartoes():
    pasta = op.FOTOS
    os.makedirs(pasta, exist_ok=True)
    for r in R:
        cartao(r).save(os.path.join(pasta, r["foto"]))
    for k, s in enumerate(INTRO):   # palavras da intro (não aparecem nas perguntas)
        img = Image.new("RGB", (300, 300), COR_INTRO[k])
        dd = ImageDraw.Draw(img)
        fo = b.font(b.F_BLACK, 200)
        while dd.textlength(s, font=fo) > 260:
            fo = b.font(b.F_BLACK, fo.size - 6)
        dd.text((150, 150), s, font=fo, fill=b.WHITE, anchor="mm")
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


def gancho(r):
    if r["n"] == 1:
        return GANCHO
    if r["n"] in INICIO:
        return f"RODADA {r['rodada']}!\n{SUB[r['rodada']]}"
    return None


def placar_frames(n, dur):
    """Placar da família: PAIS x FILHOS (cada um conta os seus pontos)."""
    c1, c2 = (120, 60, 200), (45, 20, 110)
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = nd.burst(c1, c2, t * 12).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.3)
        b.text_outline(d, (800, 170), f"{n} QUESTÕES!", b.font(b.F_BLACK, int(110 * (0.5 + 0.5 * s))), b.WHITE, w=11)
        b.text_outline(d, (800, 330), "QUEM TÁ GANHANDO?", b.font(b.F_BLACK, int(120 * (0.5 + 0.5 * s))), b.YELLOW, w=13)
        if s >= 1:
            for cx, nome, cor in ((480, "PAIS", (30, 120, 220)), (1120, "FILHOS", (230, 60, 90))):
                d.rounded_rectangle([cx - 260, 450, cx + 260, 800], 50, fill=(255, 255, 255, 245), outline=b.NAVY, width=8)
                d.rounded_rectangle([cx - 260, 450, cx + 260, 560], 50, fill=cor)
                d.text((cx, 505), nome, font=b.font(b.F_BLACK, 80), fill=b.WHITE, anchor="mm")
                d.text((cx, 690), f"__ / {n}", font=b.font(b.F_BLACK, 100), fill=b.NAVY, anchor="mm")
            b.text_outline(d, (800, 625), "x", b.font(b.F_BLACK, 130), b.YELLOW, w=12)
        b.selo(img, 800, 930, 1.0)
        b.put_palito(img, "apontando", 560, 1680, 1060 + int((1 - s) * 700), int(6 * math.sin(t * 5)))
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
    return op.intro_rapida("PAIS x FILHOS", "5º ANO!", d, fotos=[f"intro{k}.png" for k in range(len(INTRO))],
                          abertura=os.path.join(HERE, "abertura.jpg"))


def previa():
    cartoes()
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40]]
    for k in (0, 8, 14, 21, 26, 31):
        r = R[k]
        q = q_de(r)
        f = dur(A(f"q{r['n']}.mp3")) + 0.3
        pf = list(hu.pergunta_frames(q, TOTAL, f, r["count"], gancho(r)))
        fr += [pf[15],
               pf[min(len(pf) - 1, int((f + 2.5 + 0.6) * FPS))]]
        fr.append(list(hu.resposta_frames(q, TOTAL, 3.0))[-1])
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
    tmp = tempfile.mkdtemp(prefix="quiz_pais_filhos_")
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
