"""Quiz Palito — vídeo 51 "BANDEIRAS: fácil, médio, difícil e impossível" (10 a 13 min).

36 bandeiras em 4 NÍVEIS de 9. O cartão mostra a bandeira com a PLACA DO NÍVEL em cima; 3 alternativas A/B/C
(do difícil em diante, bandeiras parecidas). Cada nível tem cor de fundo própria (verde, azul, laranja, vermelho)
e uma TELA DE NÍVEL antes das perguntas 10, 19 e 28. Bandeiras de domínio público (PNGs do vídeo 03).
Layout `modelo-opcoes/opcoes.py` + ESTILO MAIS HUMANO `modelo-opcoes/humano.py`.
Uso: py -3 build_bandeiras_niveis.py            (monta quiz-palito-bandeiras-niveis.mp4)
     py -3 build_bandeiras_niveis.py --previa   (prancha em previa/)
     py -3 build_bandeiras_niveis.py --duracao  (só calcula a duração pelo tamanho das falas)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
import humano as hu
from opcoes import b, nd, W, H, FPS

BANDEIRAS = os.path.join(VIDEOS, "03-bandeiras-195", "bandeiras")
op.FOTOS = os.path.join(HERE, "cartoes")      # gerados por cartoes() (fora do Git)
R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-bandeiras-niveis.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Sneaky Snitch.mp3")
GANCHO = "36 BANDEIRAS, 4 NÍVEIS:\nATÉ ONDE VOCÊ CHEGA?"
CURTIR_DEPOIS = 3
INTRO_BAND = ["br", "es", "gb", "mx"]        # não são resposta de nenhuma pergunta
# nível -> (cor da placa, degradê do fundo)
NIVEL = {
    "FÁCIL": ((40, 170, 80), ((40, 170, 90), (10, 90, 50))),
    "MÉDIO": ((30, 110, 220), ((30, 110, 220), (10, 40, 130))),
    "DIFÍCIL": ((240, 130, 0), ((245, 140, 20), (160, 70, 0))),
    "IMPOSSÍVEL": ((210, 30, 50), ((200, 30, 60), (90, 5, 30))),
}
ORDEM = list(NIVEL)
op.CORES = [NIVEL[k][1] for k in ORDEM]
_fundo = op.fundo
op.fundo = lambda n, t=0.0: _fundo((n - 1) // 9 if 1 <= n <= TOTAL else n, t)   # cor pelo nível da pergunta


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


def cartao(r, L=720):
    """Placa do nível em cima + bandeira inteira (sem cortar) no meio + bolinhas dos 4 níveis."""
    img = Image.new("RGB", (L, L), (255, 255, 255))
    d = ImageDraw.Draw(img)
    cor = NIVEL[r["nivel"]][0]
    d.rounded_rectangle([60, 28, L - 60, 148], 40, fill=cor, outline=b.NAVY, width=6)
    fo = b.font(b.F_BLACK, 66)
    while d.textlength(f"NÍVEL {r['nivel']}", font=fo) > L - 180:
        fo = b.font(b.F_BLACK, fo.size - 2)
    d.text((L / 2, 90), f"NÍVEL {r['nivel']}", font=fo, fill=b.WHITE, anchor="mm",
           stroke_width=5, stroke_fill=b.NAVY)
    bd = Image.open(os.path.join(BANDEIRAS, r["code"] + ".png")).convert("RGB")
    bd.thumbnail((L - 90, 430), Image.LANCZOS)
    x, y = (L - bd.width) // 2, 175 + (450 - bd.height) // 2
    d.rectangle([x - 6, y - 6, x + bd.width + 5, y + bd.height + 5], fill=b.NAVY)
    img.paste(bd, (x, y))
    k = ORDEM.index(r["nivel"])
    for i, nv in enumerate(ORDEM):
        cx = L / 2 + (i - 1.5) * 70
        d.ellipse([cx - 22, 655 - 22, cx + 22, 655 + 22], fill=NIVEL[nv][0] if i <= k else (215, 215, 225),
                  outline=b.NAVY, width=4)
    return img


def cartoes():
    os.makedirs(op.FOTOS, exist_ok=True)
    for r in R:
        cartao(r).save(os.path.join(op.FOTOS, r["foto"]))
    for c in INTRO_BAND:
        im = Image.open(os.path.join(BANDEIRAS, c + ".png")).convert("RGB")
        fundo = Image.new("RGB", (300, 300), (255, 255, 255))
        im.thumbnail((280, 280), Image.LANCZOS)
        fundo.paste(im, ((300 - im.width) // 2, (300 - im.height) // 2))
        fundo.save(os.path.join(op.FOTOS, f"intro-{c}.png"))


def nivel_frames(n, dur):
    """Tela de nível (antes das perguntas 10, 19 e 28): 'NÍVEL MÉDIO' + quantas acertou até aqui."""
    nv = R[n - 1]["nivel"]
    cor, (c1, c2) = NIVEL[nv]
    feitas = n - 1
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = nd.burst(c1, c2, t * 12).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.3)
        b.text_outline(d, (800, 220), "PRÓXIMO:", b.font(b.F_BLACK, int(90 * (0.5 + 0.5 * s))), b.WHITE, w=10)
        b.text_outline(d, (800, 380), "NÍVEL", b.font(b.F_BLACK, int(130 * (0.5 + 0.5 * s))), b.WHITE, w=13)
        b.text_outline(d, (800, 550), nv, b.font(b.F_BLACK, int(170 * (0.5 + 0.5 * s))), b.YELLOW, w=16)
        if s >= 1:
            d.rounded_rectangle([380, 690, 1220, 800], 55, fill=(255, 255, 255, 240), outline=b.NAVY, width=7)
            d.text((800, 745), f"VOCÊ ACERTOU __ / {feitas}", font=b.font(b.F_BLACK, 62), fill=b.NAVY, anchor="mm")
        b.selo(img, 800, 910, 1.1)
        b.put_palito(img, "apontando", 620, 1620 + int((1 - s) * 700), 1060, int(6 * math.sin(t * 5)))
        yield img.convert("RGB")


dur = lambda p: b.duration(p) if os.path.exists(p) else 1.2


def duracao():
    t = dur(A("intro.mp3")) + 0.4
    for r in R:
        n = r["n"]
        if n in (10, 19, 28):
            t += dur(A(f"nivel{n}.mp3")) + 0.9
        t += 0.6 + dur(A(f"q{n}.mp3")) + 0.3 + r["count"]
        if "fala_s" in r:
            t += dur(A(f"s{n}.mp3")) + 0.9
        dr = dur(A(f"p{n}.mp3")) + 0.3
        t += (max(dr, 5.5) if "sabia" in r else dr) + 0.7
    t += dur(A("curtir.mp3")) + 0.3 + 1.6 + dur(A("espero.mp3")) + 0.6
    t += dur(A("ultima.mp3")) + 0.8
    return t + dur(A("outro.mp3")) + 1.8


def intro_frames(d):
    return op.intro_rapida("BANDEIRAS", "4 NÍVEIS!", d, fotos=[f"intro-{c}.png" for c in INTRO_BAND],
                          abertura=os.path.join(HERE, "abertura.jpg"))


def previa():
    cartoes()
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40]]
    for k in (0, 11, 15, 21, 27, 35):
        r = R[k]
        q = q_de(r)
        f = dur(A(f"q{r['n']}.mp3")) + 0.3
        pf = list(hu.pergunta_frames(q, TOTAL, f, r["count"], GANCHO if k == 0 else None))
        fr += [pf[15], pf[min(len(pf) - 1, int((f + 2.5 + 0.6) * FPS))]]
        fr.append(list(hu.resposta_frames(q, TOTAL, 3.0))[-1])
    fr.append(list(op.transicao_frames(fr[-1], q_de(R[5]), TOTAL))[9])
    fr.append(list(nivel_frames(19, 0.5))[-1])
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
    tmp = tempfile.mkdtemp(prefix="quiz_bandeiras_niveis_")
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
        if n in (1, 10, 19, 28):
            marcas[r["nivel"]] = tl.t
        if n in (10, 19, 28):
            v = A(f"nivel{n}.mp3")
            tl.sound(sfx["whoosh"])
            tl.sound(v, at=tl.t + 0.3)
            for f in nivel_frames(n, dur(v) + 0.9):
                tl.frame(f)
                ultimo = f
            print(f"{n}/{TOTAL} ({tl.t / 60:.1f} min)", flush=True)
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
