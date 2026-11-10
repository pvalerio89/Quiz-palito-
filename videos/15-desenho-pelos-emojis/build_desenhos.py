"""Quiz Palito — "ADIVINHE O DESENHO PELOS EMOJIS!" (mais de 8 min, para anúncio no meio).

Versão sem música de abertura do "adivinhe o desenho pela intro" (as aberturas têm direitos): cada desenho vira
uma pista de 3 ou 4 emojis num cartão + alternativas A/B/C. Layout aprovado `videos/modelo-opcoes/opcoes.py`
(sem tela de abertura, chamada por cima da 1ª pergunta, placar de bolinhas, sons, transição).
Uso: py -3 build_desenhos.py            (monta quiz-palito-desenho-pelos-emojis.mp4)
     py -3 build_desenhos.py --previa   (prancha em previa/)
     py -3 build_desenhos.py --duracao  (só calcula a duração pelo tamanho das falas)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
from opcoes import b, nd, W, H, FPS

R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-desenho-pelos-emojis.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Fluffing a Duck.mp3")
EMOJI_TTF = "C:/Windows/Fonts/seguiemj.ttf"
GANCHO = "SÓ QUEM VIU MUITO DESENHO\nACERTA TODAS!"
_cache = {}


def separar(s):
    """'❄️👸⛄' -> ['❄️', '👸', '⛄'] (junta o seletor de variação no emoji anterior)."""
    out = []
    for ch in s:
        if ch in "\ufe0f\u200d" and out:
            out[-1] += ch
        else:
            out.append(ch)
    return out


def emoji(ch, size):
    k = ("em", ch, size)
    if k in _cache:
        return _cache[k]
    try:
        f, px = ImageFont.truetype(EMOJI_TTF, 300), 300        # Segoe (Windows) é vetorial
    except OSError:
        f, px = ImageFont.truetype(EMOJI_TTF, 109), 109        # Noto (nuvem) só tem 109 px
    im = Image.new("RGBA", (px * 3, px * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((px * 1.5, px), ch, font=f, embedded_color=True, anchor="mm")
    bb = im.getbbox()
    im = im.crop(bb) if bb else im
    r = size / max(im.size)
    im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
    _cache[k] = im
    return im


def cartao_sprite(q, filtro=None):
    """Cartão branco com os emojis da pista (3 em triângulo ou 4 em quadrado) e um '+' entre eles."""
    k = ("cartao", q["n"])
    if k in _cache:
        return _cache[k]
    sp = op.moldura_sprite().copy()
    es = separar(q["emojis"])
    c = sp.width // 2
    if len(es) == 4:
        pos, sz = [(c - 135, c - 130), (c + 135, c - 130), (c - 135, c + 140), (c + 135, c + 140)], 215
    else:
        pos, sz = [(c - 140, c - 125), (c + 140, c - 125), (c, c + 150)], 230
    for (x, y), ch in zip(pos, es):
        e = emoji(ch, sz)
        sp.alpha_composite(e, (int(x - e.width / 2), int(y - e.height / 2)))
    _cache[k] = sp
    return sp


op.cartao_sprite = cartao_sprite      # o modelo chama op.cartao_sprite(q, filtro) para desenhar o cartão


def q_de(r):
    return {"n": r["n"], "pergunta": "QUE DESENHO É ESSE?", "foto": f"q{r['n']}", "opcoes": r["opcoes"],
            "certa": r["certa"], "emojis": r["emojis"]}


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


dur = lambda p: b.duration(p) if os.path.exists(p) else 1.2
RESP = lambda n: max(1.6, dur(A(f"p{n}.mp3")) + 0.6)


def duracao():
    t = dur(A("q1.mp3")) + 0.2 + op.COUNT + RESP(1)
    for r in R[1:]:
        t += 0.6 + op.COUNT + RESP(r["n"])
    for n in range(10, TOTAL, 10):
        t += dur(A(f"placar{n}.mp3")) + 0.8
    return t + max(4.0, dur(A("outro.mp3")) + 1.8)


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    q = [q_de(r) for r in R]
    fr = [list(op.pergunta_frames(q[0], TOTAL, fala=3.0, gancho=GANCHO))[15]]
    for k in (3, 15, 21, 33, TOTAL - 1):
        fr.append(list(op.pergunta_frames(q[k], TOTAL))[int(op.COUNT * FPS * 0.5)])
        fr.append(list(op.resposta_frames(q[k], 1.0, TOTAL, t0=op.COUNT))[-1])
    fr.append(list(op.transicao_frames(fr[-1], q[5], TOTAL))[9])
    fr.append(list(placar_frames(10, 0.5))[-1])
    fr.append(next(nd.anima(outro_base().convert("RGBA"), "acenando", 0.1)))
    cols = 3
    th = [f.resize((640, 360), Image.LANCZOS) for f in fr]
    pr = Image.new("RGB", (cols * 650, math.ceil(len(th) / cols) * 370), "black")
    for i, f in enumerate(th):
        pr.paste(f, ((i % cols) * 650, (i // cols) * 370))
    pr.save(os.path.join(out, "prancha.jpg"), quality=88)
    # todos os cartões numa folha, para conferir emojis
    t = 200
    fs = Image.new("RGB", (10 * t, math.ceil(TOTAL / 10) * (t + 26)), "white")
    dd = ImageDraw.Draw(fs)
    for i, r in enumerate(R):
        x, y = (i % 10) * t, (i // 10) * (t + 26)
        c = cartao_sprite(q[i]).resize((t - 8, t - 8))
        fs.paste(c, (x + 4, y + 4), c)
        dd.text((x + t / 2, y + t + 10), f"{r['n']} {r['nome']}"[:24], font=b.font(b.F_BOLD, 16), fill="black", anchor="mm")
    fs.save(os.path.join(out, "cartoes.jpg"), quality=85)
    print(out, f"duração estimada {duracao():.0f}s")


def main():
    tmp = tempfile.mkdtemp(prefix="quiz_desenhos_")
    sfx = op.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    marcas = {}
    ultimo = None
    for r in R:
        n, q = r["n"], q_de(r)
        if n % 10 == 1:
            marcas[str(n)] = tl.t
        primeira = n == 1
        fala = 0.0
        if primeira:   # sem tela de abertura: apresentação falada por cima da 1ª pergunta
            tl.sound(A("q1.mp3"), at=0.1)
            fala = dur(A("q1.mp3")) + 0.2
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
        _cache.pop(("cartao", n), None)
    marcas["final"] = tl.t
    tl.sound(sfx["whoosh"])
    tl.sound(A("outro.mp3"), at=tl.t + 0.4)
    for f in nd.anima(outro_base().convert("RGBA"), "acenando", max(4.0, dur(A("outro.mp3")) + 1.8)):
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
