"""Quiz Palito — vídeo 36 "BRASIL x PORTUGAL: COMO SE DIZ EM PORTUGAL?" (10 a 13 min).

37 palavras, das fáceis às bizarras: o cartão mostra a FOTO REAL do objeto (Wikimedia Commons; créditos em
creditos.json e na tela final) com a palavra do Brasil embaixo; as 3 alternativas A/B/C são palavras de Portugal.
Layout `modelo-opcoes/opcoes.py` + ESTILO MAIS HUMANO `modelo-opcoes/humano.py`.
Uso: py -3 build_brasil_portugal.py            (monta quiz-palito-quem-jogou-aqui.mp4)
     py -3 build_brasil_portugal.py --previa   (prancha em previa/)
     py -3 build_brasil_portugal.py --duracao  (só calcula a duração pelo tamanho das falas)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
import humano as hu
from opcoes import b, nd, W, H, FPS

op.FOTOS = os.path.join(HERE, "fotos")
CRED = json.load(open(os.path.join(HERE, "creditos.json"), encoding="utf-8"))
R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-brasil-x-portugal.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Fluffing a Duck.mp3")
GANCHO = f"{TOTAL} PALAVRAS:\nAS ÚLTIMAS SÃO BIZARRAS!"
CURTIR_DEPOIS = 3          # pedido de curtida depois da 3ª resposta
INTRO_FOTOS = ["intro-br.png", "intro-pt.png"]   # não estão nas perguntas
BANDEIRAS = os.path.join(HERE, "bandeiras")


_cartao = op.cartao_sprite
BR_PALAVRA = {r["foto"]: r["br"] for r in R}


def cartao_sprite(q, filtro=None):
    """Foto real com a palavra do BRASIL numa faixa embaixo (bandeirinha + palavra)."""
    k = ("cartao_br", q["foto"])
    if k in op._cache:
        return op._cache[k]
    sp = _cartao(q, filtro).copy()
    d = ImageDraw.Draw(sp)
    x0, x1, y1 = 50, 50 + op.CARD - 40, 50 + op.CARD - 40
    y0 = y1 - 110
    d.rounded_rectangle([x0, y0, x1, y1], 34, fill=(0, 120, 60))
    d.rectangle([x0, y0, x1, y0 + 40], fill=(0, 120, 60))
    bd = Image.open(os.path.join(BANDEIRAS, "br.png")).convert("RGBA")
    bd.thumbnail((96, 66), Image.LANCZOS)
    by = int((y0 + y1) / 2 - bd.height / 2)
    d.rectangle([x0 + 22, by - 3, x0 + 24 + bd.width, by + bd.height + 2], fill=b.WHITE)
    sp.alpha_composite(bd, (x0 + 23, by))
    t = BR_PALAVRA[q["foto"]]
    ini, fim = x0 + 40 + bd.width, x1 - 20
    fo = b.font(b.F_BLACK, 60)
    while d.textlength(t, font=fo) > fim - ini and fo.size > 28:
        fo = b.font(b.F_BLACK, fo.size - 2)
    d.text(((ini + fim) / 2, (y0 + y1) / 2), t, font=fo, fill=b.YELLOW, anchor="mm", stroke_width=4, stroke_fill=b.NAVY)
    op._cache[k] = sp
    return sp


op.cartao_sprite = cartao_sprite


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


def creditos_base():
    img = Image.new("RGBA", (W, H), (20, 24, 48, 255))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 50), "CRÉDITOS DAS IMAGENS", font=b.font(b.F_BLACK, 40), fill=b.YELLOW, anchor="mm")
    d.text((W / 2, 98), "Fotos: Wikimedia Commons (autor, licença e arquivo). Bandeiras: domínio público.", font=b.font(b.F_BOLD, 24),
           fill=b.WHITE, anchor="mm")
    f = b.font(b.F_BOLD, 18)
    itens = [f"{k}: {c['autor']} ({c['lic']}), {c['file'].replace('_', ' ')}" for k, c in CRED.items()]
    meio = (len(itens) + 1) // 2
    for col, parte in enumerate((itens[:meio], itens[meio:])):
        for i, t in enumerate(parte):
            while d.textlength(t, font=f) > W / 2 - 60:
                t = t[:-2]
            d.text((30 + col * W / 2, 130 + i * 44), t, font=f, fill=b.WHITE)
    d.text((W / 2, H - 30), "Perguntas: Quiz Palito.", font=b.font(b.F_BOLD, 22), fill=(180, 180, 200), anchor="mm")
    return img


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
    return t + dur(A("outro.mp3")) + 1.8 + 5


def intro_frames(d):
    return op.intro_rapida("BRASIL x PORTUGAL", "COMO SE DIZ?", d, fotos=INTRO_FOTOS, abertura=os.path.join(HERE, "abertura.jpg"))


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40]]
    for k in (0, 4, 12, 19, 26, 35):
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
    fotos = [Image.open(os.path.join(op.FOTOS, r["foto"])).resize((200, 200)) for r in R]
    fo = Image.new("RGB", (9 * 205, math.ceil(len(fotos) / 9) * 235), "white")
    dd = ImageDraw.Draw(fo)
    for i, (f, r) in enumerate(zip(fotos, R)):
        x, y = (i % 9) * 205, (i // 9) * 235
        fo.paste(f, (x, y))
        dd.text((x + 100, y + 216), f"{r['n']}. {r['br']}"[:24], font=b.font(b.F_BOLD, 17),
                fill="black", anchor="mm")
    fo.save(os.path.join(out, "imagens.jpg"), quality=85)
    print(out, f"duração estimada {duracao():.0f}s")


def main():
    tmp = tempfile.mkdtemp(prefix="quiz_brasil_portugal_")
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
        if n in (1, 11, 21, 31):
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
