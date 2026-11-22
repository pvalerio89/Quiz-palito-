"""Quiz Palito — vídeo 52 "Jogadores de A a Z — PARTE 2" (10 a 13 min).

32 perguntas próprias: o cartão mostra a LETRA gigante + uma pista e as 3 alternativas A/B/C são jogadores com essa
letra. Na resposta o cartão troca para a FOTO REAL do craque (Wikimedia Commons, fotos do vídeo 19; créditos na tela
final). Nenhuma resposta repete a parte 1 (vídeo 02). Fundo roxo/noite de estádio (cara diferente dos últimos).
Layout `modelo-opcoes/opcoes.py` + ESTILO MAIS HUMANO `humano.py` + transição splash.
Uso: py -3 build_jogadores2.py            (monta quiz-palito-jogadores-a-z-2.mp4)
     py -3 build_jogadores2.py --previa   (prancha em previa/)
     py -3 build_jogadores2.py --duracao  (só calcula a duração pelo tamanho das falas)
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
op.CORES = [((120, 50, 200), (50, 15, 110)), ((40, 60, 190), (15, 20, 90)), ((170, 40, 160), (80, 10, 80)),
            ((90, 40, 210), (30, 10, 100))]   # roxo/azul de estádio à noite (≠ 39 verde, 40 savana, 51 níveis)
COR_LETRA = (120, 50, 200)
CRED = json.load(open(os.path.join(HERE, "creditos.json"), encoding="utf-8"))
R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-jogadores-a-z-2.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Wallpaper.mp3")
GANCHO = "UM CRAQUE POR LETRA:\nA ÚLTIMA NINGUÉM ACERTA!"
CURTIR_DEPOIS = 3          # pedido de inscrição/like depois da 3ª resposta
V19 = os.path.join(VIDEOS, "19-monte-seu-clube", "fotos")
INTRO_FOTOS = ["intro-1.png", "intro-2.png", "intro-3.png", "intro-4.png"]   # fotos que não são respostas
INTRO_SRC = ["pe-vinicius-jr", "dez-messi", "ca-mbappe", "ca-haaland"]       # (já foram da parte 1)
_resp = hu.resposta_frames


def resposta_frames(q, total, d):
    """Na resposta o cartão troca a letra pela foto do craque (ou pelo nome, se não houver foto livre)."""
    return _resp(dict(q, foto=q["foto_resposta"]), total, d)


hu.resposta_frames = resposta_frames


def q_de(r):
    q = {k: r[k] for k in ("n", "pergunta", "foto", "opcoes", "certa")}
    q["foto_resposta"] = f"r{r['n']}.png"
    if "dica_txt" in r:
        q["dica"] = (A(f"d{r['n']}.mp3"), r["dica_txt"], 2.5)
    if "fala_s" in r:
        q["suspense"] = A(f"s{r['n']}.mp3")
    for k in ("aviso", "sabia", "final"):
        if k in r:
            q[k] = r[k]
    return q


def cartao(r, L=720):
    """Cartão com a LETRA gigante e a pista embaixo."""
    img = Image.new("RGB", (L, L), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([L / 2 - 190, 30, L / 2 + 190, 330], 40, fill=COR_LETRA)
    d.text((L / 2, 185), r["letra"], font=b.font(b.F_BLACK, 250), fill=b.WHITE, anchor="mm",
           stroke_width=8, stroke_fill=b.NAVY)
    linhas = r["pista"]
    fo = b.font(b.F_BLACK, 70)
    while max(d.textlength(t, font=fo) for t in linhas) > L - 60 and fo.size > 34:
        fo = b.font(b.F_BLACK, fo.size - 3)
    y0 = 360 + (L - 360) / 2 - (len(linhas) - 1) * fo.size * 0.6
    for i, t in enumerate(linhas):
        d.text((L / 2, y0 + i * fo.size * 1.2), t, font=fo, fill=b.NAVY, anchor="mm")
    return img


def cartao_resposta(r, L=720):
    """Foto do craque com o nome numa faixa embaixo; sem foto livre: o nome gigante no cartão."""
    nome = r["opcoes"][r["certa"]]
    if r.get("foto_jogador"):
        img = ImageOps.fit(Image.open(os.path.join(HERE, "fotos", r["foto_jogador"])).convert("RGB"), (L, L),
                           Image.LANCZOS, centering=(0.5, 0.3))
    else:
        img = Image.new("RGB", (L, L), COR_LETRA)
        d = ImageDraw.Draw(img)
        d.text((L / 2, 250), r["letra"], font=b.font(b.F_BLACK, 330), fill=(255, 255, 255), anchor="mm",
               stroke_width=10, stroke_fill=b.NAVY)
    d = ImageDraw.Draw(img)
    fo = b.font(b.F_BLACK, 76)
    while d.textlength(nome, font=fo) > L - 60 and fo.size > 34:
        fo = b.font(b.F_BLACK, fo.size - 3)
    d.rectangle([0, L - 130, L, L], fill=b.NAVY)
    d.text((L / 2, L - 65), nome, font=fo, fill=b.YELLOW, anchor="mm")
    return img


def cartoes():
    os.makedirs(op.FOTOS, exist_ok=True)
    for r in R:
        cartao(r).save(os.path.join(op.FOTOS, r["foto"]))
        cartao_resposta(r).save(os.path.join(op.FOTOS, f"r{r['n']}.png"))
    for nome, src in zip(INTRO_FOTOS, INTRO_SRC):
        p = os.path.join(V19, src + ".jpg")
        if os.path.exists(p):
            ImageOps.fit(Image.open(p).convert("RGB"), (300, 300), Image.LANCZOS, centering=(0.5, 0.3)).save(
                os.path.join(op.FOTOS, nome))


def creditos_base():
    img = Image.new("RGBA", (W, H), (20, 24, 48, 255))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 50), "CRÉDITOS DAS IMAGENS", font=b.font(b.F_BLACK, 40), fill=b.YELLOW, anchor="mm")
    d.text((W / 2, 98), "Fotos: Wikimedia Commons (autor, licença e arquivo).", font=b.font(b.F_BOLD, 22),
           fill=b.WHITE, anchor="mm")
    f = b.font(b.F_BOLD, 17)
    itens = [f"{k}: {c['autor']} ({c['lic']}), {c['file'].replace('_', ' ')}" for k, c in CRED.items()]
    itens += [f"Abertura: {c}" for c in ("Vinícius Jr., Messi, Mbappé e Haaland: ver vídeo 'Monte o seu clube'",)]
    meio = (len(itens) + 1) // 2
    for col, parte in enumerate((itens[:meio], itens[meio:])):
        for i, t in enumerate(parte):
            while d.textlength(t, font=f) > W / 2 - 60:
                t = t[:-2]
            d.text((30 + col * W / 2, 135 + i * 29), t, font=f, fill=b.WHITE)
    d.text((W / 2, H - 30), "Perguntas: Quiz Palito.", font=b.font(b.F_BOLD, 22), fill=(180, 180, 200), anchor="mm")
    return img


def placar_frames(n, dur):
    c1, c2 = (120, 50, 200), (50, 15, 110)
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = nd.burst(c1, c2, t * 12).convert("RGBA")
        d = ImageDraw.Draw(img)
        s = min(1.0, t / 0.3)
        b.text_outline(d, (800, 230), f"{n} CRAQUES!", b.font(b.F_BLACK, int(110 * (0.5 + 0.5 * s))), b.WHITE, w=11)
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
    return op.intro_rapida("CRAQUES A-Z", "PARTE 2", d, fotos=INTRO_FOTOS, cor=1,
                          abertura=os.path.join(HERE, "abertura.jpg"))


def previa():
    cartoes()
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40]]
    for k in (0, 7, 15, 21, 28, 31):
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
    fotos = [Image.open(os.path.join(op.FOTOS, f"r{r['n']}.png")).resize((200, 200)) for r in R]
    fo = Image.new("RGB", (8 * 205, math.ceil(len(fotos) / 8) * 235), "white")
    dd = ImageDraw.Draw(fo)
    for i, (f, r) in enumerate(zip(fotos, R)):
        x, y = (i % 8) * 205, (i // 8) * 235
        fo.paste(f, (x, y))
        dd.text((x + 100, y + 216), f"{r['n']}. {r['letra']} {' / '.join(r['pista'])}"[:26], font=b.font(b.F_BOLD, 14),
                fill="black", anchor="mm")
    fo.save(os.path.join(out, "imagens.jpg"), quality=85)
    print(out, f"duração estimada {duracao():.0f}s")


def main():
    cartoes()
    tmp = tempfile.mkdtemp(prefix="quiz_jogadores2_")
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
        if n in (1, 11, 24):
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
