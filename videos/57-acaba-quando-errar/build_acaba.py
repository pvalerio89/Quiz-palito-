"""Quiz Palito — vídeo 57 "O vídeo ACABA quando você ERRAR a bandeira" (formato SOBREVIVÊNCIA, 10 a 13 min).

36 bandeiras cada vez mais difíceis; errou uma, fim de jogo (o espectador comenta até onde chegou).
No lugar das bolinhas de pontos fica o contador "SEQUÊNCIA SEM ERRAR" (sobe a cada resposta) e o selo
"ACERTOU? SEGUE VIVO!". O cartão tem a placa "1 ERRO = FIM!" e a trilha das 36 bandeiras. O fundo vai escurecendo
(azul -> roxo -> vinho -> quase preto) e antes das perguntas 10, 19 e 28 entra a tela "AINDA VIVO?".
Bandeiras de domínio público (PNGs do vídeo 03); nenhuma é resposta do vídeo 51.
Layout `modelo-opcoes/opcoes.py` + ESTILO MAIS HUMANO `modelo-opcoes/humano.py` + transição splash.
Uso: py -3 build_acaba.py            (monta quiz-palito-acaba-quando-errar.mp4)
     py -3 build_acaba.py --previa   (prancha em previa/)
     py -3 build_acaba.py --duracao  (só calcula a duração pelo tamanho das falas)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
import humano as hu
import engaja as eg
from opcoes import b, nd, W, H, FPS

BANDEIRAS = os.path.join(VIDEOS, "03-bandeiras-195", "bandeiras")
op.FOTOS = os.path.join(HERE, "cartoes")      # gerados por cartoes() (fora do Git)
R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-acaba-quando-errar.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Fluffing a Duck.mp3")
GANCHO = "ERROU UMA?\nFIM DE JOGO!"
CURTIR_DEPOIS = 3
VIVO = (10, 19, 28)                          # tela "AINDA VIVO?" antes destas
INTRO_BAND = ["jp", "it", "ca", "fr"]        # não são resposta de nenhuma pergunta deste vídeo
# o fundo escurece a cada 9 perguntas: fica mais "perigoso"
op.CORES = [((30, 120, 230), (10, 45, 140)), ((120, 60, 210), (45, 15, 110)),
            ((190, 30, 70), (90, 5, 35)), ((70, 20, 40), (15, 5, 15))]
_fundo = op.fundo
op.fundo = lambda n, t=0.0: _fundo((n - 1) // 9 if 1 <= n <= TOTAL else n, t)
VERMELHO = (220, 30, 45)


def placar(img, q, total, t, respondida=False):
    """Contador SEQUÊNCIA SEM ERRAR (no lugar das bolinhas). Na resposta o número sobe com um pulinho."""
    seq = q["n"] - 1 + (1 if respondida else 0)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([520, 975, 1340, 1060], 42, fill=(20, 20, 40), outline=b.WHITE, width=6)
    d.text((860, 1018), "SEQUÊNCIA SEM ERRAR:", font=b.font(b.F_BLACK, 44), fill=b.WHITE, anchor="mm")
    sc = 1.0
    if respondida:
        sc = 1.0 + 0.35 * math.sin(min(max((t - 0.3) / 0.35, 0), 1) * math.pi)
    r = int(52 * sc)
    cx, cy = 1250, 1018
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=b.YELLOW, outline=VERMELHO, width=7)
    d.text((cx, cy + 2), str(seq), font=b.font(b.F_BLACK, int(62 * sc)), fill=b.NAVY, anchor="mm")


def vivo_selo(img, cx, cy, tt, size=46):
    """No lugar do '+1 SE ACERTOU!': 'ACERTOU? SEGUE VIVO!'."""
    sc = eg.pula((tt - 0.35) / 0.3)
    if sc <= 0.02:
        return
    sp = eg._faixa_sprite("ACERTOU? SEGUE VIVO!", int(size * 11), size, (40, 170, 70))
    eg._colar(img, sp, cx, cy + 4 * math.sin(tt * 6), sc)


op.placar = placar
eg.mais_um = vivo_selo


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
    """Placa '1 ERRO = FIM!' em cima + bandeira inteira (sem cortar) + trilha das 36 bandeiras embaixo."""
    img = Image.new("RGB", (L, L), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([110, 26, L - 110, 132], 40, fill=VERMELHO, outline=b.NAVY, width=6)
    d.text((L / 2, 79), "1 ERRO = FIM!", font=b.font(b.F_BLACK, 62), fill=b.WHITE, anchor="mm",
           stroke_width=5, stroke_fill=b.NAVY)
    bd = Image.open(os.path.join(BANDEIRAS, r["code"] + ".png")).convert("RGB")
    bd.thumbnail((L - 90, 420), Image.LANCZOS)
    x, y = (L - bd.width) // 2, 160 + (440 - bd.height) // 2
    d.rectangle([x - 6, y - 6, x + bd.width + 5, y + bd.height + 5], fill=b.NAVY)
    img.paste(bd, (x, y))
    # trilha: 36 tracinhos (feitas = amarelo, atual = vermelho, próximas = cinza)
    n = r["n"]
    x0, passo, w = 48, (L - 96) / 36, (L - 96) / 36 - 4
    for i in range(36):
        xi = x0 + i * passo
        cor = b.YELLOW if i < n - 1 else (VERMELHO if i == n - 1 else (215, 215, 225))
        d.rounded_rectangle([xi, 640, xi + w, 690], 5, fill=cor, outline=b.NAVY, width=2)
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


def coracao(d, cx, cy, s, cor):
    d.ellipse([cx - s, cy - s * 0.75, cx, cy + s * 0.25], fill=cor)
    d.ellipse([cx, cy - s * 0.75, cx + s, cy + s * 0.25], fill=cor)
    d.polygon([(cx - s * 0.97, cy - s * 0.1), (cx + s * 0.97, cy - s * 0.1), (cx, cy + s * 1.05)], fill=cor)


def vivo_frames(n, dur):
    """Tela 'AINDA VIVO?' (antes das perguntas 10, 19 e 28): sequência até aqui + coração batendo."""
    c1, c2 = op.CORES[(n - 1) // 9]
    feitas = n - 1
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = nd.burst(c1, c2, t * 12).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = max(0.15, min(1.0, t / 0.3))
        bat = 1 + 0.12 * abs(math.sin(t * 4.5))
        coracao(d, 400, 430, int(150 * s * bat), VERMELHO)
        d.text((400, 410), str(feitas), font=b.font(b.F_BLACK, int(150 * s * bat)), fill=b.WHITE, anchor="mm",
               stroke_width=8, stroke_fill=b.NAVY)
        b.text_outline(d, (1060, 300), "SEQUÊNCIA", b.font(b.F_BLACK, int(110 * (0.5 + 0.5 * s))), b.WHITE, w=11)
        b.text_outline(d, (1060, 440), f"DE {feitas}!", b.font(b.F_BLACK, int(140 * (0.5 + 0.5 * s))), b.YELLOW, w=14)
        if s >= 1:
            d.rounded_rectangle([170, 660, 1400, 790], 60, fill=(255, 255, 255, 240), outline=b.NAVY, width=7)
            tx = "AINDA VIVO? AGORA COMPLICA!"
            d.text((785, 725), tx, font=nd.fit(d, tx, 70, 1130), fill=VERMELHO, anchor="mm")
        b.selo(img, 785, 910, 1.1)
        b.put_palito(img, "comemorando", 560, 1640 + int((1 - s) * 700), 1060, -int(abs(18 * math.sin(t * 6))))
        yield img.convert("RGB")


dur = lambda p: b.duration(p) if os.path.exists(p) else 1.2


def duracao():
    t = dur(A("intro.mp3")) + 0.4
    for r in R:
        n = r["n"]
        if n in VIVO:
            t += dur(A(f"vivo{n}.mp3")) + 0.9
        t += 0.6 + dur(A(f"q{n}.mp3")) + 0.3 + r["count"]
        if "fala_s" in r:
            t += dur(A(f"s{n}.mp3")) + 0.9
        dr = dur(A(f"p{n}.mp3")) + 0.3
        t += (max(dr, 5.5) if "sabia" in r else dr) + 0.7
    t += dur(A("curtir.mp3")) + 0.3 + 1.6 + dur(A("espero.mp3")) + 0.6
    t += dur(A("ultima.mp3")) + 0.8
    return t + dur(A("outro.mp3")) + 1.8


def intro_frames(d):
    return op.intro_rapida("O VÍDEO ACABA", "1 ERRO = FIM!", d, fotos=[f"intro-{c}.png" for c in INTRO_BAND],
                          abertura=os.path.join(HERE, "abertura.jpg"))


def previa():
    cartoes()
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40]]
    for k in (0, 7, 19, 25, 30, 35):
        r = R[k]
        q = q_de(r)
        f = dur(A(f"q{r['n']}.mp3")) + 0.3
        pf = list(hu.pergunta_frames(q, TOTAL, f, r["count"], GANCHO if k == 0 else None))
        fr += [pf[15], pf[min(len(pf) - 1, int((f + 2.5 + 0.6) * FPS))]]
        fr.append(list(hu.resposta_frames(q, TOTAL, 3.0))[-1])
    fr.append(list(op.transicao_frames(fr[-1], q_de(R[5]), TOTAL))[9])
    fr.append(list(vivo_frames(19, 0.5))[-1])
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
    tmp = tempfile.mkdtemp(prefix="quiz_acaba_")
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
        if n in (1,) + VIVO:
            marcas[str(n)] = tl.t
        if n in VIVO:
            v = A(f"vivo{n}.mp3")
            tl.sound(sfx["whoosh"])
            tl.sound(sfx["acerto"], at=tl.t + 0.2, vol=0.6)
            tl.sound(v, at=tl.t + 0.3)
            for f in vivo_frames(n, dur(v) + 0.9):
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
