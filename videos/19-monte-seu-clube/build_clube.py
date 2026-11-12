"""Quiz Palito — "MONTE O SEU CLUBE" (mais de 8 min, para anúncio no meio).

Vídeo de ESCOLHA, sem resposta certa e sem placar (formato da referência que o Patrick mandou, 2026-11-11):
o espectador monta o próprio clube em 24 etapas (cidade, cor da camisa, escudo, estádio, mascote, técnico, os 11
titulares e o banco com uma joia e lendas). Cada etapa mostra 6 opções numeradas com foto real e nome, a fala
apresenta as opções, a contagem "ESCOLHA O SEU!" corre e o Palito reage. No fim, campinho "MONTOU? COMENTA SEU TIME!".
Fundo, selo, sons e transição do modelo `videos/modelo-opcoes/opcoes.py`; intro rapidinha antes da 1ª etapa.
Uso: py -3 build_clube.py            (monta quiz-palito-monte-seu-clube.mp4)
     py -3 build_clube.py --previa   (prancha em previa/)
     py -3 build_clube.py --duracao  (só calcula a duração pelo tamanho das falas)
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
import engaja as eg
from opcoes import b, nd, W, H, FPS

E = json.load(open(os.path.join(HERE, "etapas.json"), encoding="utf-8"))
CRED = json.load(open(os.path.join(HERE, "creditos-tela.json"), encoding="utf-8"))
TOTAL = len(E)
A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "quiz-palito-monte-seu-clube.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Wallpaper.mp3")
CONTA = 10.0                                # segundos para escolher
GANCHO = "MONTE O SEU CLUBE:\nANOTA CADA NÚMERO!"
BANCO_APOS = "ca"                           # depois do centroavante: "time titular pronto"
FOTO, NOME_H = 280, 66                       # cartão: foto + faixa do nome
CX = (300, 650, 1000)
CY = (420, 805)
TIMER = (1390, 330)
_cache = {}


def foto(arq, lado=FOTO):
    k = ("foto", arq, lado)
    if k not in _cache:
        im = Image.open(os.path.join(HERE, "fotos", arq)).convert("RGBA").resize((lado, lado), Image.LANCZOS)
        m = Image.new("L", (lado, lado), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, lado - 1, lado - 1], 26, fill=255)
        im.putalpha(m)
        if len(_cache) > 60:
            _cache.clear()
        _cache[k] = im
    return _cache[k]


def cartao(i, o, lado=FOTO, nome_h=NOME_H, fonte=40):
    """Cartão branco: foto, nome embaixo e número da opção no canto."""
    k = ("cartao", o["foto"], i, lado)
    if k in _cache:
        return _cache[k]
    m = 22
    w, h = lado + 24, lado + nome_h + 30
    sp = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    sh = Image.new("RGBA", sp.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([m, m + 12, m + w, m + h + 12], 36, fill=(0, 0, 40, 110))
    sp.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
    d = ImageDraw.Draw(sp)
    d.rounded_rectangle([m, m, m + w, m + h], 36, fill=b.WHITE, outline=b.NAVY, width=7)
    sp.alpha_composite(foto(o["foto"], lado), (m + 12, m + 12))
    t = o["nome"].upper()
    f = b.font(b.F_BLACK, fonte)
    while d.textlength(t, font=f) > w - 30 and f.size > 20:
        f = b.font(b.F_BLACK, f.size - 2)
    d.text((m + w / 2, m + lado + 12 + (nome_h + 18) / 2), t, font=f, fill=b.NAVY, anchor="mm")
    r = int(lado * 0.15)
    d.ellipse([m - 6, m - 6, m - 6 + 2 * r, m - 6 + 2 * r], fill=b.YELLOW, outline=b.NAVY, width=6)
    d.text((m - 6 + r, m - 4 + r), str(i + 1), font=b.font(b.F_BLACK, int(r * 1.3)), fill=b.NAVY, anchor="mm")
    _cache[k] = sp
    return sp


def topo(img, k, e):
    d = ImageDraw.Draw(img)
    d.ellipse([40, 28, 190, 178], fill=b.ORANGE, outline=b.WHITE, width=8)
    d.text((115, 101), f"{k + 1:02d}", font=b.font(b.F_BLACK, 70), fill=b.WHITE, anchor="mm", stroke_width=3,
           stroke_fill=b.NAVY)
    b.text_outline(d, (830, 90), e["titulo"], nd.fit(d, e["titulo"], 92, 1150), b.YELLOW, w=10)
    d.text((830, 168), f"{e['sub']}   •   ETAPA {k + 1} DE {TOTAL}", font=b.font(b.F_BLACK, 34), fill=b.WHITE,
           anchor="mm", stroke_width=4, stroke_fill=b.NAVY)
    b.selo(img, 1730, 100, 0.7)


def base(k, e, t):
    key = ("topo", k)
    if key not in _cache:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        topo(lay, k, e)
        _cache[key] = lay
    img = op.fundo(k, t)
    img.alpha_composite(_cache[key])
    return img


def timer(img, frac, t, conta=CONTA, c=TIMER, raio=120, legenda=True):
    """Relógio redondo que esvazia + segundos que faltam + 'ESCOLHA O SEU!'."""
    d = ImageDraw.Draw(img)
    x, y = c
    d.ellipse([x - raio - 10, y - raio - 10, x + raio + 10, y + raio + 10], fill=b.WHITE)
    d.ellipse([x - raio, y - raio, x + raio, y + raio], fill=(60, 70, 110))
    if frac > 0:
        d.pieslice([x - raio, y - raio, x + raio, y + raio], -90, -90 + 360 * frac,
                   fill=b.ORANGE if frac > 0.3 else b.RED)
    d.ellipse([x - raio * 0.68, y - raio * 0.68, x + raio * 0.68, y + raio * 0.68], fill=b.WHITE)
    s = math.ceil(frac * conta)
    pulso = 1 + 0.08 * max(0, math.sin(t * 2 * math.pi)) if frac < 0.3 else 1
    d.text((x, y + 4), str(s) if s else "!", font=b.font(b.F_BLACK, int(raio * 0.95 * pulso)), fill=b.NAVY,
           anchor="mm")
    if legenda:
        b.text_outline(d, (x, y + raio + 60), "ESCOLHA O SEU!", b.font(b.F_BLACK, 50), b.YELLOW, w=7)


def grade(img, e, t, entrada=True, flut=True):
    for i, o in enumerate(e["opcoes"]):
        sc = op.pula((t - 0.25 - 0.22 * i) / 0.35) if entrada else 1.0
        dy = 5 * math.sin(t * 2.6 + i * 1.1) if flut else 0
        op.colar(img, cartao(i, o), CX[i % 3], CY[i // 3] + dy, sc)


def etapa_frames(k, e, fala, conta=CONTA, gancho=None):
    """Fala apresentando as opções (cartões entram um a um) e depois a contagem para escolher."""
    tot = fala + conta
    for i in range(int(tot * FPS)):
        t = i / FPS
        frac = 1.0 if t < fala else 1 - (t - fala) / conta
        img = base(k, e, t)
        grade(img, e, t)
        timer(img, frac, t)
        pose = "pensando" if frac > 0.3 else "assustado"
        b.put_palito(img, pose, 500, 1700, 1060, int(7 * math.sin(t * (5 if pose == "pensando" else 18))))
        if gancho:
            eg.faixa_gancho(img, 830, 122, gancho, t, max(fala, 2.5), larg=1350, size=78)
        yield op.zoom(img, 1.0 + 0.02 * t / tot).convert("RGB")


def reacao_frames(k, e, dur):
    """Tempo acabou: 'ESCOLHEU? ANOTA AÍ!' e o Palito comemora."""
    for i in range(int(dur * FPS)):
        tt = i / FPS
        img = base(k, e, CONTA + tt)
        grade(img, e, 10 + tt, entrada=False)
        d = ImageDraw.Draw(img)
        s = op.pula(tt / 0.35)
        f = b.font(b.F_BLACK, max(10, int(64 * s)))
        x, y = TIMER
        d.rounded_rectangle([x - 230 * s, y - 120 * s, x + 230 * s, y + 120 * s], int(40 * s) + 1, fill=b.RED,
                            outline=b.WHITE, width=8)
        d.text((x, y - 42 * s), "ESCOLHEU?", font=f, fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
        d.text((x, y + 44 * s), "ANOTA AÍ!", font=f, fill=b.YELLOW, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
        if tt < 0.2:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(110 * (1 - tt / 0.2)))))
        b.put_palito(img, "comemorando", 500, 1700, 1060, -int(abs(24 * math.sin(tt * 7))))
        yield op.zoom(img, 1.02).convert("RGB")


def transicao(antes, depois, dur=0.6):
    """Faixa diagonal amarela com o selo (igual à do modelo), trocando de etapa."""
    larg, incl = 520, 420
    n = int(dur * FPS)
    for i in range(n):
        p = (i + 1) / n
        p = p * p * (3 - 2 * p)
        x = -larg - incl + p * (W + 2 * larg + 2 * incl)
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).polygon([(-10, 0), (x - larg, 0), (x - larg - incl, H), (-10, H)], fill=255)
        img = antes.copy()
        img.paste(depois, (0, 0), m)
        img = img.convert("RGBA")
        d = ImageDraw.Draw(img)
        d.polygon([(x - larg, 0), (x, 0), (x - incl, H), (x - larg - incl, H)], fill=b.YELLOW)
        d.polygon([(x - larg, 0), (x - larg + 40, 0), (x - larg - incl + 40, H), (x - larg - incl, H)], fill=b.NAVY)
        d.polygon([(x - 40, 0), (x, 0), (x - incl, H), (x - incl - 40, H)], fill=b.NAVY)
        b.selo(img, int(x - larg / 2 - incl / 2), H // 2, 1.2)
        yield img.convert("RGB")


def primeiro(k, e):
    img = base(k, e, 0.0)
    timer(img, 1.0, 0)
    b.put_palito(img, "pensando", 500, 1700, 1060, 0)
    return img.convert("RGB")


POS = [("GOL", 0.5, 0.9), ("LD", 0.86, 0.68), ("ZAG", 0.62, 0.74), ("ZAG", 0.38, 0.74), ("LE", 0.14, 0.68),
       ("VOL", 0.5, 0.56), ("MEI", 0.3, 0.42), ("10", 0.7, 0.42), ("PD", 0.86, 0.22), ("PE", 0.14, 0.22),
       ("CA", 0.5, 0.12)]


def campinho(w=760, h=860):
    """Campo com as 11 posições e um '?' em cada (cada um põe o seu jogador nos comentários)."""
    if ("campo", w) in _cache:
        return _cache[("campo", w)]
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 40, fill=b.WHITE, outline=b.NAVY, width=8)
    for i in range(10):
        y0 = 20 + i * (h - 40) / 10
        d.rectangle([20, y0, w - 20, y0 + (h - 40) / 10], fill=(46, 160, 70) if i % 2 else (38, 145, 62))
    cor = (235, 255, 235)
    d.rectangle([40, 40, w - 40, h - 40], outline=cor, width=5)
    d.line([40, h / 2, w - 40, h / 2], fill=cor, width=5)
    d.ellipse([w / 2 - 80, h / 2 - 80, w / 2 + 80, h / 2 + 80], outline=cor, width=5)
    d.rectangle([w / 2 - 170, h - 40 - 120, w / 2 + 170, h - 40], outline=cor, width=5)
    d.rectangle([w / 2 - 170, 40, w / 2 + 170, 160], outline=cor, width=5)
    for rot, fx, fy in POS:
        x, y = 40 + fx * (w - 80), 40 + fy * (h - 80)
        d.ellipse([x - 40, y - 40, x + 40, y + 40], fill=b.YELLOW, outline=b.NAVY, width=6)
        d.text((x, y + 2), "?", font=b.font(b.F_BLACK, 50), fill=b.NAVY, anchor="mm")
        f = b.font(b.F_BLACK, 26)
        tw = d.textlength(rot, font=f)
        d.rounded_rectangle([x - tw / 2 - 12, y + 44, x + tw / 2 + 12, y + 80], 14, fill=b.NAVY)
        d.text((x, y + 62), rot, font=f, fill=b.WHITE, anchor="mm")
    _cache[("campo", w)] = img
    return img


def banco_frames(dur):
    """Depois do centroavante: 'TIME TITULAR PRONTO!' com o campinho."""
    cp = campinho()
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = nd.burst((40, 170, 90), (10, 90, 60), t * 10).convert("RGBA")
        op.colar(img, cp, 520, 560, 0.3 + 0.7 * op.pula(t / 0.4))
        d = ImageDraw.Draw(img)
        b.text_outline(d, (1400, 250), "TIME TITULAR", b.font(b.F_BLACK, 96), b.WHITE, w=11)
        b.text_outline(d, (1400, 370), "PRONTO!", b.font(b.F_BLACK, 120), b.YELLOW, w=12)
        b.text_outline(d, (1400, 520), "AGORA O BANCO:", b.font(b.F_BLACK, 64), b.WHITE, w=8)
        b.text_outline(d, (1400, 610), "JOIA + LENDAS!", b.font(b.F_BLACK, 76), b.YELLOW, w=9)
        b.put_palito(img, "comemorando", 380, 1400, 1080, -int(abs(20 * math.sin(t * 6))))
        yield img.convert("RGB")


def outro_frames(dur):
    cp = campinho()
    for i in range(int(dur * FPS)):
        t = i / FPS
        img = op.fundo(3, t)
        op.colar(img, cp, 470, 560, 0.3 + 0.7 * op.pula(t / 0.4))
        d = ImageDraw.Draw(img)
        b.text_outline(d, (1300, 170), "MONTOU?", b.font(b.F_BLACK, 130), b.YELLOW, w=13)
        b.text_outline(d, (1300, 300), "COMENTA SEU TIME!", b.font(b.F_BLACK, 84), b.WHITE, w=10)
        d.rounded_rectangle([890, 390, 1710, 500], 55, fill=b.RED, outline=b.WHITE, width=8)
        d.text((1300, 445), "OS NÚMEROS + NOME DO CLUBE", font=b.font(b.F_BLACK, 50), fill=b.WHITE, anchor="mm",
               stroke_width=3, stroke_fill=b.NAVY)
        b.text_outline(d, (1300, 590), "MARCA UM AMIGO E INSCREVA-SE NO", b.font(b.F_BLACK, 42), b.WHITE, w=6)
        b.selo(img, 1300, 680, 1.2)
        b.put_palito(img, "acenando", 340, 1300, 1075, int(6 * math.sin(t * 4)))
        yield img.convert("RGB")


def creditos_base():
    img = Image.new("RGBA", (W, H), (20, 24, 48, 255))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 36), "CRÉDITOS DAS IMAGENS — Wikimedia Commons (autor, licença e arquivo)",
           font=b.font(b.F_BLACK, 30), fill=b.YELLOW, anchor="mm")
    cols, f = 3, b.font(b.F_BOLD, 15)
    linhas = CRED["fotos"]
    por = math.ceil(len(linhas) / cols)
    for i, t in enumerate(linhas):
        while d.textlength(t, font=f) > W / cols - 24:
            t = t[:-2]
        d.text((16 + (i // por) * (W / cols), 66 + (i % por) * 21), t, font=f, fill=b.WHITE)
    esc = "Escudos (marcas dos clubes, imagens da Wikipédia): " + ", ".join(CRED["escudos"])
    fe = b.font(b.F_BOLD, 18)
    while d.textlength(esc, font=fe) > W - 40 and fe.size > 11:
        fe = b.font(b.F_BOLD, fe.size - 1)
    d.text((W / 2, H - 52), esc, font=fe, fill=b.WHITE, anchor="mm")
    d.text((W / 2, H - 22), "Vídeo de brincadeira sem ligação com clubes, jogadores ou técnicos.",
           font=b.font(b.F_BOLD, 18), fill=(180, 180, 200), anchor="mm")
    return img


dur = lambda p: b.duration(p) if os.path.exists(p) else 3.0
REAC = lambda k: A(f"r{k % 6}.mp3")


def duracao():
    t = dur(A("intro.mp3"))
    for k, e in enumerate(E):
        t += 0.6 + dur(A(f"e{k}.mp3")) + 0.3 + CONTA + dur(REAC(k)) + 0.6
        if e["chave"] == BANCO_APOS:
            t += dur(A("banco.mp3")) + 0.8
    return t + dur(A("outro.mp3")) + 1.5 + 6


INTRO_FOTOS = ["mascote-leao.jpg", "estadio-maracana.jpg", "ca-cristiano-ronaldo.jpg", "dez-messi.jpg",
               "pe-vinicius-jr.jpg"]


def intro_frames(d):
    return op.intro_rapida("MONTE O SEU", "CLUBE!", d,
                           fotos=[Image.open(os.path.join(HERE, "fotos", f)).convert("RGBA").resize((170, 170))
                                  for f in INTRO_FOTOS])


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = [list(intro_frames(2.5))[40], list(etapa_frames(0, E[0], 4.0, gancho=GANCHO))[30]]
    for k in (1, 3, 6, 13, 16, 22):
        pf = list(etapa_frames(k, E[k], 4.0))
        fr.append(pf[int(4 * FPS + CONTA * FPS * 0.75)])
    fr.append(list(reacao_frames(4, E[4], 1.0))[-1])
    fr.append(list(transicao(fr[-1], primeiro(5, E[5])))[9])
    fr.append(list(banco_frames(1.0))[-1])
    fr.append(list(outro_frames(1.0))[-1])
    fr.append(creditos_base().convert("RGB"))
    cols = 3
    th = [f.resize((640, 360), Image.LANCZOS) for f in fr]
    pr = Image.new("RGB", (cols * 650, math.ceil(len(th) / cols) * 370), "black")
    for i, f in enumerate(th):
        pr.paste(f, ((i % cols) * 650, (i // cols) * 370))
    pr.save(os.path.join(out, "prancha.jpg"), quality=88)
    print(out, f"duração estimada {duracao():.0f}s")


def main():
    tmp = tempfile.mkdtemp(prefix="quiz_clube_")
    sfx = op.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    marcas = {}
    tl.sound(A("intro.mp3"), at=0.15)   # intro rapidinha (Patrick, 2026-11-10)
    ultimo = None
    for f in intro_frames(dur(A("intro.mp3"))):
        tl.frame(f)
        ultimo = f
    for k, e in enumerate(E):
        marcas[e["chave"]] = tl.t
        if ultimo is not None:
            tl.sound(sfx["whoosh"], vol=0.7)
            for f in transicao(ultimo, primeiro(k, e)):
                tl.frame(f)
        v = A(f"e{k}.mp3")
        fala = dur(v) + 0.3
        t0 = tl.t
        tl.sound(v, at=t0 + 0.1)
        for i in range(6):                                   # cartões pulando
            tl.sound(sfx["pop"], at=t0 + 0.25 + 0.22 * i, vol=0.6)
        for s in range(int(CONTA)):                          # tique-taque, mais rápido no fim
            tl.sound(sfx["tick"], at=t0 + fala + s, vol=0.6)
            if s >= CONTA - 3:
                tl.sound(sfx["tique"], at=t0 + fala + s + 0.5, vol=0.5)
        tl.sound(sfx["acerto"], at=t0 + fala + CONTA, vol=0.7)
        for f in etapa_frames(k, e, fala, gancho=GANCHO if k == 0 else None):
            tl.frame(f)
        rv = REAC(k)
        tl.sound(rv, at=tl.t + 0.2)
        for f in reacao_frames(k, e, dur(rv) + 0.6):
            tl.frame(f)
            ultimo = f
        if e["chave"] == BANCO_APOS:
            tl.sound(sfx["whoosh"])
            tl.sound(A("banco.mp3"), at=tl.t + 0.3)
            for f in banco_frames(dur(A("banco.mp3")) + 0.8):
                tl.frame(f)
                ultimo = f
        print(f"{k + 1}/{TOTAL} ({tl.t / 60:.1f} min)", flush=True)
    marcas["final"] = tl.t
    tl.sound(sfx["whoosh"])
    tl.sound(A("outro.mp3"), at=tl.t + 0.4)
    for f in outro_frames(dur(A("outro.mp3")) + 1.5):
        tl.frame(f)
    cr = creditos_base().convert("RGB")
    for _ in range(int(6 * FPS)):
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
