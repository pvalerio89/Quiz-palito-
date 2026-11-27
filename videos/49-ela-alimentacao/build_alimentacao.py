"""Quiz Palito — vídeo 49 "COMIDA EM INGLÊS: FOOD RAINBOW" (mais de 8 min, para anúncio no meio).

44 perguntas da lição Mizzou Grade 3 ELA 5-3 "Eating Plants" que o Patrick mandou em foto (2026-11-19), do médio ao muito
difícil: legumes em inglês, singular/plural, Food Rainbow (cores e nutrientes), vocabulário (healthy, nutrition, rainbow).
Imagem de cada pergunta (feita aqui, em cartoes/): foto real (Wikimedia, do vídeo 12) ou cartão de caderno. 3 alternativas A/B/C.
Layout `modelo-opcoes/opcoes.py` + ESTILO MAIS HUMANO `modelo-opcoes/humano.py`.
Uso: py -3 build_alimentacao.py            (monta quiz-palito-food-rainbow.mp4)
     py -3 build_alimentacao.py --previa   (prancha em previa/)
     py -3 build_alimentacao.py --duracao  (só calcula a duração pelo tamanho das falas)
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
R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
TOTAL = len(R)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-food-rainbow.mp4")
CRED = json.load(open(os.path.join(HERE, "creditos.json"), encoding="utf-8"))
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Wallpaper.mp3")
GANCHO = f"{TOTAL} QUESTÕES DE INGLÊS!\nFOOD RAINBOW!"
SUB = {2: "SUBINDO O NÍVEL!", 3: "AGORA COMPLICA!", 4: "DERRUBA ATÉ ADULTO!"}
NIVEL = {1: "FÁCIL", 2: "MÉDIO", 3: "DIFÍCIL", 4: "MUITO DIFÍCIL"}
COR_NIVEL = {1: (30, 160, 120), 2: (40, 110, 210), 3: (240, 140, 0), 4: (200, 50, 120)}
CURTIR_DEPOIS = 3
INICIO = {r["n"] for r in R if r["n"] > 1 and R[r["n"] - 2]["nivel"] != r["nivel"]}
INTRO = ["tomate.jpg", "brocolis.jpg", "mirtilo.jpg"]


# ---------- cartões ----------

def nivel_pilula(img, nivel, L):
    d = ImageDraw.Draw(img)
    cor = COR_NIVEL[nivel]
    fp = b.font(b.F_BLACK, 40)
    w = d.textlength(NIVEL[nivel], font=fp) / 2 + 40
    d.rounded_rectangle([L / 2 - w, 30, L / 2 + w, 100], 35, fill=cor, outline=b.WHITE, width=4)
    d.text((L / 2, 66), NIVEL[nivel], font=fp, fill=b.WHITE, anchor="mm")


def papel(L):
    img = Image.new("RGB", (L, L), (255, 255, 255))
    d = ImageDraw.Draw(img)
    for k in range(0, L, 40):   # papel quadriculado de caderno
        d.line([(k, 0), (k, L)], fill=(225, 235, 248), width=2)
        d.line([(0, k), (L, k)], fill=(225, 235, 248), width=2)
    return img


def cartao_texto(r, L=720):
    """Cartão de caderno com a palavra/frase bem grande."""
    img = papel(L)
    d = ImageDraw.Draw(img)
    linhas = r["cartao"]
    size = 140 if len(linhas) == 1 else 96
    fo = b.font(b.F_BLACK, size)
    while max(d.textlength(t, font=fo) for t in linhas) > L - 80 and fo.size > 40:
        fo = b.font(b.F_BLACK, fo.size - 4)
    y0 = L / 2 + 30 - (len(linhas) - 1) * fo.size * 0.6
    for i, t in enumerate(linhas):
        dica = t.startswith("(")
        f = b.font(b.F_BOLD, int(fo.size * 0.75)) if dica else fo
        d.text((L / 2, y0 + i * fo.size * 1.2), t, font=f, fill=(90, 110, 140) if dica else
               (b.RED if "_" in t else b.NAVY), anchor="mm")
    return img


def cartao_foto(r, L=720):
    """Foto real cobrindo o cartão, com o nome em português numa faixa embaixo."""
    img = ImageOps.fit(Image.open(os.path.join(HERE, "fotos", r["foto"] + ".jpg")).convert("RGB"), (L, L), Image.LANCZOS)
    d = ImageDraw.Draw(img, "RGBA")
    if r.get("rotulo"):
        fo = b.font(b.F_BLACK, 64)
        while d.textlength(r["rotulo"], font=fo) > L - 140:
            fo = b.font(b.F_BLACK, fo.size - 4)
        w = d.textlength(r["rotulo"], font=fo) / 2 + 40
        d.rounded_rectangle([L / 2 - w, L - 130, L / 2 + w, L - 40], 40, fill=(255, 255, 255, 235), outline=b.NAVY, width=5)
        d.text((L / 2, L - 85), r["rotulo"], font=fo, fill=b.NAVY, anchor="mm")
    return img


PARTES = {"flower": (360, 215), "leaves": (215, 345), "stem": (372, 440), "roots": (330, 600)}


def cartao_planta(r, L=720):
    """Desenho próprio de uma planta (flor, folhas, caule, raízes) com uma seta vermelha numa parte."""
    img = papel(L)
    d = ImageDraw.Draw(img)
    ch = 520   # linha do chão
    d.rectangle([0, ch, L, L], fill=(150, 105, 65))
    for k in range(40):
        x, y = (k * 97) % L, ch + 20 + (k * 53) % (L - ch - 30)
        d.ellipse([x, y, x + 7, y + 7], fill=(115, 80, 45))
    raiz = (235, 215, 170)
    for ang, comp in [(-60, 150), (-30, 170), (0, 175), (30, 165), (60, 145), (-45, 110), (45, 110)]:
        a = math.radians(90 + ang)
        x1, y1 = 360 + comp * math.cos(a), ch + 5 + comp * math.sin(a) * 0.95
        d.line([(360, ch), ((360 + x1) / 2 + ang / 3, (ch + y1) / 2), (x1, y1)], fill=raiz, width=12, joint="curve")
        d.line([((360 + x1) / 2, (ch + y1) / 2), ((360 + x1) / 2 + 30 * math.copysign(1, ang or 1), (ch + y1) / 2 + 45)],
               fill=raiz, width=7)
    d.line([(360, ch + 5), (360, 230)], fill=(50, 140, 50), width=24)
    for lado in (-1, 1):   # folhas
        cx, cy = 360 + lado * 120, 380 - (20 if lado > 0 else 0)
        pts = []
        for k in range(41):
            u = k / 40 * 2 * math.pi
            x, y = 125 * math.cos(u), 52 * math.sin(u)
            rot = math.radians(-25 * lado)
            pts.append((cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot)))
        d.polygon(pts, fill=(70, 175, 70), outline=(30, 100, 30), width=5)
        d.line([(360, cy + 30 * lado * 0 + 25), (cx + lado * 110, cy - lado * lado * 50)], fill=(30, 100, 30), width=4)
    for k in range(8):   # pétalas
        u = k / 8 * 2 * math.pi
        x, y = 360 + 78 * math.cos(u), 185 + 78 * math.sin(u)
        d.ellipse([x - 52, y - 52, x + 52, y + 52], fill=(235, 80, 140), outline=(160, 30, 90), width=5)
    d.ellipse([360 - 50, 185 - 50, 360 + 50, 185 + 50], fill=(255, 205, 40), outline=(190, 130, 0), width=5)
    alvo = r.get("planta")
    if alvo:
        tx, ty = PARTES[alvo]
        sx, sy = (640, ty - 40) if alvo != "leaves" else (70, ty + 150)
        if alvo == "roots":
            sx, sy = 640, 680
        d.line([(sx, sy), (tx, ty)], fill=b.RED, width=12)
        ang = math.atan2(ty - sy, tx - sx)
        p1 = (tx - 45 * math.cos(ang - 0.45), ty - 45 * math.sin(ang - 0.45))
        p2 = (tx - 45 * math.cos(ang + 0.45), ty - 45 * math.sin(ang + 0.45))
        d.polygon([(tx, ty), p1, p2], fill=b.RED)
        d.ellipse([sx - 42, sy - 42, sx + 42, sy + 42], fill=b.WHITE, outline=b.RED, width=8)
        d.text((sx, sy), "?", font=b.font(b.F_BLACK, 60), fill=b.RED, anchor="mm")
    return img


def cartao(r, L=720):
    img = cartao_foto(r, L) if "foto" in r else cartao_planta(r, L) if "planta" in r else cartao_texto(r, L)
    nivel_pilula(img, r["nivel"], L)
    return img


def cartoes():
    pasta = op.FOTOS
    os.makedirs(pasta, exist_ok=True)
    for r in R:
        cartao(r).save(os.path.join(pasta, r["img"]))
    for s_ in INTRO:   # fotos da intro
        ImageOps.fit(Image.open(os.path.join(HERE, "fotos", s_)).convert("RGB"), (300, 300)).save(
            os.path.join(pasta, s_.replace(".jpg", ".png")))


def creditos_base():
    img = Image.new("RGBA", (W, H), (20, 24, 48, 255))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 70), "CRÉDITOS DAS IMAGENS", font=b.font(b.F_BLACK, 44), fill=b.YELLOW, anchor="mm")
    d.text((W / 2, 130), "Fotos: Wikimedia Commons (autor, licença e arquivo)", font=b.font(b.F_BOLD, 28),
           fill=b.WHITE, anchor="mm")
    f = b.font(b.F_BOLD, 26)
    for i, t in enumerate(CRED["fotos"]):
        while d.textlength(t, font=f) > W - 100:
            t = t[:-2]
        d.text((50, 190 + i * 52), t, font=f, fill=b.WHITE)
    d.text((W / 2, H - 50), "Perguntas e cartões: Quiz Palito.", font=b.font(b.F_BOLD, 24),
           fill=(180, 180, 200), anchor="mm")
    return img


# ---------- vídeo ----------

def q_de(r):
    q = {k: r[k] for k in ("n", "pergunta", "opcoes", "certa")}
    q["foto"] = r["img"]
    if "dica_txt" in r:
        q["dica"] = (A(f"d{r['n']}.mp3"), r["dica_txt"], 2.5)
    if "fala_s" in r:
        q["suspense"] = A(f"s{r['n']}.mp3")
    for k in ("aviso", "sabia", "final"):
        if k in r:
            q[k] = r[k]
    return q


def selo_serie(img, nivel):
    """Pílula com o nível embaixo do número da pergunta."""
    return img   # o nível já aparece no cartão (a pílula pequena ficava atrás dele)
    d = ImageDraw.Draw(img)
    t = NIVEL[nivel]
    fo = b.font(b.F_BLACK, 30)
    w = max(170, d.textlength(t, font=fo) + 44)
    d.rounded_rectangle([30, 192, 30 + w, 248], 28, fill=COR_NIVEL[nivel], outline=b.WHITE, width=5)
    d.text((30 + w / 2, 221), t, font=fo, fill=b.WHITE, anchor="mm", stroke_width=2, stroke_fill=b.NAVY)
    return img


def gancho(r):
    if r["n"] == 1:
        return GANCHO
    if r["n"] in INICIO:
        return f"NÍVEL {NIVEL[r['nivel']]}!\n{SUB[r['nivel']]}"
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
    return t + dur(A("outro.mp3")) + 1.8 + 5


def intro_frames(d):
    return op.intro_rapida("COMIDA EM INGLÊS", "FOOD RAINBOW!", d, fotos=[s_.replace(".jpg", ".png") for s_ in INTRO],
                          abertura=os.path.join(HERE, "abertura.jpg"))


def previa():
    cartoes()
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40]]
    for k in (0, 2, 15, 16, 31, 43):
        r = R[k]
        q = q_de(r)
        f = dur(A(f"q{r['n']}.mp3")) + 0.3
        pf = list(hu.pergunta_frames(q, TOTAL, f, r["count"], gancho(r)))
        fr += [selo_serie(pf[15], r["nivel"]),
               selo_serie(pf[min(len(pf) - 1, int((f + 2.5 + 0.6) * FPS))], r["nivel"])]
        fr.append(selo_serie(list(hu.resposta_frames(q, TOTAL, 3.0))[-1], r["nivel"]))
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
    fotos = [Image.open(os.path.join(op.FOTOS, r["img"])).resize((200, 200)) for r in R]
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
    tmp = tempfile.mkdtemp(prefix="food_rainbow_")
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
            f = selo_serie(f, r["nivel"])
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
