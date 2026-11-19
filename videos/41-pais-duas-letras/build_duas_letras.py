"""Quiz Palito — vídeo 41 "Adivinhe o PAÍS só com as 2 primeiras letras" (10 a 13 min).

36 perguntas próprias: o cartão mostra só as 2 primeiras letras do país e quadradinhos vazios no lugar das outras
(dá para contar as letras). As 3 alternativas A/B/C são só BANDEIRAS; na resposta o cartão completa o nome e cada
alternativa ganha o nome do país. Fundo azul e magenta (cara diferente dos vídeos 39 e 40).
Layout `modelo-opcoes/opcoes.py` + ESTILO MAIS HUMANO `humano.py`.
Uso: py -3 build_duas_letras.py            (monta quiz-palito-pais-duas-letras.mp4)
     py -3 build_duas_letras.py --previa   (prancha em previa/)
     py -3 build_duas_letras.py --duracao  (só calcula a duração pelo tamanho das falas)
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
op.CORES = [((30, 120, 220), (15, 45, 140)), ((200, 40, 140), (110, 15, 80)), ((40, 90, 210), (20, 30, 110)),
            ((150, 50, 200), (70, 20, 120))]
R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-pais-duas-letras.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Fluffing a Duck.mp3")
GANCHO = "SÓ 2 LETRAS:\nACHE A BANDEIRA CERTA!"
CURTIR_DEPOIS = 3          # pedido de curtida depois da 3ª resposta
INTRO_BAND = ["fi", "gh", "sa", "ph"]   # bandeiras que não estão nas perguntas
BANDEIRAS = os.path.join(HERE, "bandeiras")
BAND = {o: c for r in R for o, c in zip(r["opcoes"], r["bandeiras"])}   # nome do país -> código da bandeira
LARANJA, VERDE_T = (255, 140, 0), (40, 170, 90)


_opcao = op.opcao_sprite


def opcao_sprite(i, txt, estado=None):
    """Na pergunta, a alternativa é SÓ a bandeira (grande, no meio); na resposta ganha o nome do país."""
    k = ("opb", i, txt, estado)
    if k in op._cache:
        return op._cache[k]
    cv = _opcao(i, " ", estado).copy()
    d = ImageDraw.Draw(cv)
    x0, y0 = 30, 30
    bd = Image.open(os.path.join(BANDEIRAS, BAND[txt] + ".png")).convert("RGBA")
    if estado is None:
        bd.thumbnail((260, op.OPT_H - 22), Image.LANCZOS)
        bx = int(x0 + op.OPT_W / 2 + 40 - bd.width / 2)
    else:
        bd.thumbnail((130, 84), Image.LANCZOS)
        bx = x0 + 132
    by = int(y0 + op.OPT_H / 2 - bd.height / 2)
    d.rectangle([bx - 4, by - 4, bx + bd.width + 3, by + bd.height + 3], fill=b.NAVY)
    cv.alpha_composite(bd, (bx, by))
    if estado is not None:
        sim = estado == "sim"
        fim = x0 + op.OPT_W - (120 if sim else 30)
        ini = bx + bd.width + 20
        fo = b.font(b.F_BLACK, 56)
        while d.textlength(txt, font=fo) > fim - ini and fo.size > 26:
            fo = b.font(b.F_BLACK, fo.size - 2)
        d.text(((ini + fim) / 2, y0 + op.OPT_H / 2 + 2), txt, font=fo, fill=b.WHITE if sim else b.NAVY, anchor="mm",
               stroke_width=4 if sim else 0, stroke_fill=b.NAVY)
    if estado == "nao":
        sh = Image.new("RGBA", cv.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([x0, y0, x0 + op.OPT_W, y0 + op.OPT_H], 64, fill=(20, 30, 60, 110))
        cv.alpha_composite(sh)
    op._cache[k] = cv
    return cv


op.opcao_sprite = opcao_sprite
_resp = hu.resposta_frames


def resposta_frames(q, total, d):
    """Na resposta o cartão mostra o nome inteiro."""
    return _resp(dict(q, foto=q["foto_resposta"]), total, d)


hu.resposta_frames = resposta_frames


def q_de(r):
    q = {k: r[k] for k in ("n", "pergunta", "foto", "foto_resposta", "opcoes", "certa")}
    if "dica_txt" in r:
        q["dica"] = (A(f"d{r['n']}.mp3"), r["dica_txt"], 2.5)
    if "fala_s" in r:
        q["suspense"] = A(f"s{r['n']}.mp3")
    for k in ("aviso", "sabia", "final"):
        if k in r:
            q[k] = r[k]
    return q


def linhas_nome(nome, maxc=9):
    """Quebra o nome do país em linhas de no máximo `maxc` letras (palavra inteira)."""
    rows, cur = [], []
    for w in nome.split(" "):
        if cur and len(" ".join(cur + [w])) > maxc:
            rows.append(cur)
            cur = []
        cur.append(w)
    rows.append(cur)
    return rows


def cartao(r, L=720, cheio=False):
    """Cartão tipo forca: as 2 primeiras letras + quadradinhos; `cheio` = nome inteiro (resposta)."""
    img = Image.new("RGB", (L, L), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((L / 2, 62), "COMEÇA COM:" if not cheio else "É ELE!", font=b.font(b.F_BLACK, 64), fill=b.NAVY, anchor="mm")
    rows = linhas_nome(r["pais"])
    maxc = max(len(" ".join(w)) for w in rows)
    gap = 6
    t = min(140, int((L - 50) / maxc) - gap, int(470 / len(rows)) - 26)
    alt = t + 22
    y0 = 120 + (470 - len(rows) * alt) / 2
    k = 0
    for ri, ws in enumerate(rows):
        txt = " ".join(ws)
        x = L / 2 - (len(txt) * (t + gap) - gap) / 2
        y = y0 + ri * alt
        for ch in txt:
            if ch != " ":
                mostra = k < 2 or cheio
                cor = LARANJA if k < 2 else (VERDE_T if cheio else (225, 230, 240))
                d.rounded_rectangle([x, y, x + t, y + t], max(8, t // 6), fill=cor, outline=b.NAVY, width=5)
                if mostra:
                    d.text((x + t / 2, y + t / 2 + 2), ch, font=b.font(b.F_BLACK, int(t * 0.72)), fill=b.WHITE,
                           anchor="mm", stroke_width=max(3, t // 18), stroke_fill=b.NAVY)
                k += 1
            x += t + gap
    d.rounded_rectangle([L / 2 - 200, 610, L / 2 + 200, 695], 40, fill=b.NAVY)
    d.text((L / 2, 653), f"{r['letras']} LETRAS", font=b.font(b.F_BLACK, 58), fill=b.YELLOW, anchor="mm")
    return img


def cartoes():
    os.makedirs(op.FOTOS, exist_ok=True)
    for r in R:
        cartao(r).save(os.path.join(op.FOTOS, r["foto"]))
        cartao(r, cheio=True).save(os.path.join(op.FOTOS, r["foto_resposta"]))
    for c in INTRO_BAND:
        im = Image.open(os.path.join(VIDEOS, "03-bandeiras-195", "bandeiras", c + ".png")).convert("RGB")
        fundo = Image.new("RGB", (300, 300), (255, 255, 255))
        im.thumbnail((280, 280), Image.LANCZOS)
        fundo.paste(im, ((300 - im.width) // 2, (300 - im.height) // 2))
        fundo.save(os.path.join(op.FOTOS, f"intro-{c}.png"))


def placar_frames(n, dur):
    c1, c2 = (200, 40, 140), (110, 15, 80)
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = nd.burst(c1, c2, t * 12).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.3)
        b.text_outline(d, (800, 230), f"{n} PAÍSES!", b.font(b.F_BLACK, int(110 * (0.5 + 0.5 * s))), b.WHITE, w=11)
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
    return op.intro_rapida("ADIVINHE O PAÍS", "SÓ 2 LETRAS!", d, fotos=[f"intro-{c}.png" for c in INTRO_BAND],
                          abertura=os.path.join(HERE, "abertura.jpg"))


def previa():
    cartoes()
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40]]
    for k in (0, 6, 12, 20, 31, 35):
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
    cols = 3
    th = [f.resize((640, 360), Image.LANCZOS) for f in fr]
    pr = Image.new("RGB", (cols * 650, math.ceil(len(th) / cols) * 370), "black")
    for i, f in enumerate(th):
        pr.paste(f, ((i % cols) * 650, (i // cols) * 370))
    pr.save(os.path.join(out, "prancha.jpg"), quality=88)
    fotos = [Image.open(os.path.join(op.FOTOS, r["foto_resposta"])).resize((200, 200)) for r in R]
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
    tmp = tempfile.mkdtemp(prefix="quiz_duas_letras_")
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
        if n in (1, 11, 21, 33):
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
