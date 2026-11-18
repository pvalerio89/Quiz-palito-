"""Base da série de Shorts "DESAFIO DO PALITO" (2026-11-17).

Um enigma de palitos de fósforo por Short ("mova 1 palito e deixe a conta certa", "tire 1 palito"), 20 a 35 s:
a 1ª imagem já é o desafio, contagem, "comenta antes de ver", o palito se move sozinho na resposta, fala final curta.
Por que: na aba Pesquisa do Studio, Shorts de palitos fizeram de 1,5 a 6,8 milhões no nicho, e combina com a marca.

Cada Short (shorts/palito-N/build_short.py) só define a conta, o modo e as falas; tudo o resto vem daqui.
O solucionador confere sozinho que a conta está errada e que a resposta pedida é válida (e diz se há outras).
"""
import math, os, random, re, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import short_base as s
from short_base import b, W, H, FPS

# ---------------------------------------------------------------- solucionador (dígitos de 7 segmentos)
#  a = topo, b = alto direita, c = baixo direita, d = base, e = baixo esquerda, f = alto esquerda, g = meio
SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc",
       "7": "abc", "8": "abcdefg", "9": "abcdfg"}
INV = {frozenset(v): k for k, v in SEG.items()}
VAGAS = {"d": "abcdefg", "o": "hv", "e": ""}  # onde cabe palito: dígito, sinal (+/-: h e v), igual (fixo)


def pecas(conta):
    """'5+7=2' -> [('d', {...}), ('o', {'h','v'}), ...]"""
    out = []
    for c in conta:
        if c.isdigit():
            out.append(("d", frozenset(SEG[c])))
        elif c == "+":
            out.append(("o", frozenset("hv")))
        elif c == "-":
            out.append(("o", frozenset("h")))
        elif c == "=":
            out.append(("e", frozenset("ul")))
        else:
            raise ValueError(f"caractere inválido na conta: {c!r}")
    return out


def ler(ps):
    out = ""
    for t, sg in ps:
        if t == "d":
            k = INV.get(frozenset(sg))
            if k is None:
                return None
            out += k
        elif t == "o":
            out += {frozenset("h"): "-", frozenset("hv"): "+"}.get(frozenset(sg), "?")
            if out.endswith("?"):
                return None
        else:
            out += "="
    return out


def certa(conta):
    if not conta or conta.count("=") != 1:
        return False
    l, r = conta.split("=")
    if re.search(r"(^|[+-])0\d", l) or re.match(r"0\d", r) or not l or not r:
        return False
    try:
        return eval(l) == eval(r)  # só dígitos e + - (já conferido em ler)
    except Exception:
        return False


def mover1(conta):
    """Todas as jogadas de 1 palito que deixam a conta certa: [((i, seg), (j, seg2), nova_conta)]."""
    ps, sols = pecas(conta), []
    for i, (t, sg) in enumerate(ps):
        if t == "e":
            continue
        for seg in sg:
            for j, (t2, _) in enumerate(ps):
                for seg2 in VAGAS[t2]:
                    novo = list(ps)
                    novo[i] = (t, sg - {seg})
                    if seg2 in novo[j][1] or (i == j and seg2 == seg):
                        continue
                    novo[j] = (t2, novo[j][1] | {seg2})
                    n = ler(novo)
                    if certa(n):
                        sols.append(((i, seg), (j, seg2), n))
    return sols


def tirar1(conta):
    ps, sols = pecas(conta), []
    for i, (t, sg) in enumerate(ps):
        if t == "e":
            continue
        for seg in sg:
            novo = list(ps)
            novo[i] = (t, sg - {seg})
            n = ler(novo)
            if certa(n):
                sols.append(((i, seg), None, n))
    return sols


# ---------------------------------------------------------------- desenho
L = 170            # tamanho de um palito (lado do "quadradinho" do dígito)
GAP = 34           # espaço entre os caracteres
GROSS = 20         # grossura do palito
EQ_Y = 830         # centro vertical da conta
TEMAS = {  # fundo da mesa: (claro, escuro, veio)
    "madeira": ((170, 110, 60), (110, 65, 30), (90, 50, 20)),
    "lousa": ((40, 95, 70), (20, 55, 40), (70, 130, 100)),
    "azul": ((40, 110, 200), (15, 45, 120), (70, 140, 230)),
    "roxo": ((120, 60, 180), (50, 20, 100), (150, 100, 210)),
}


def geometria(conta, escala=None):
    """Retorna (escala, [x0 de cada caractere]) para a conta caber em ~960 px."""
    n = len(conta)
    larg = n * L + (n - 1) * GAP
    sc = escala or min(1.0, 960 / larg)
    x = W / 2 - larg * sc / 2
    xs = []
    for _ in conta:
        xs.append(x)
        x += (L + GAP) * sc
    return sc, xs


def ponta(tipo, seg, x0, sc):
    """Extremos (p0, p1) do palito `seg` no caractere que começa em x0. p1 = lado da cabeça."""
    l, y0, pad = L * sc, EQ_Y - L * sc, 9 * sc
    if tipo == "d":
        P = {"a": ((x0, y0), (x0 + l, y0)), "b": ((x0 + l, y0), (x0 + l, y0 + l)),
             "c": ((x0 + l, y0 + l), (x0 + l, y0 + 2 * l)), "d": ((x0, y0 + 2 * l), (x0 + l, y0 + 2 * l)),
             "e": ((x0, y0 + l), (x0, y0 + 2 * l)), "f": ((x0, y0), (x0, y0 + l)), "g": ((x0, y0 + l), (x0 + l, y0 + l))}
        (ax, ay), (bx, by) = P[seg]
        if ax == bx:  # vertical: cabeça em cima
            return (ax, by - pad), (ax, ay + pad)
        return (ax + pad, ay), (bx - pad, by)
    cx, cy, m = x0 + l / 2, EQ_Y, 0.42 * l
    if seg == "h":
        return (cx - m, cy), (cx + m, cy)
    if seg == "v":
        return (cx, cy + m), (cx, cy - m)
    if seg == "u":
        return (cx - m, cy - 0.24 * l), (cx + m, cy - 0.24 * l)
    return (cx - m, cy + 0.24 * l), (cx + m, cy + 0.24 * l)


def palito_poly(p0, p1, g):
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    n = math.hypot(dx, dy) or 1
    nx, ny = -dy / n * g / 2, dx / n * g / 2
    return [(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)]


def desenhar_palito(img, p0, p1, sc, brilho=0.0, cor_cabeca=(205, 40, 35), verde=False):
    g = GROSS * sc
    sombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sombra)
    off = 7 * sc
    ds.polygon(palito_poly((p0[0] + off, p0[1] + off), (p1[0] + off, p1[1] + off), g), fill=(0, 0, 0, 90))
    img.alpha_composite(sombra)
    d = ImageDraw.Draw(img)
    if brilho > 0:
        d.polygon(palito_poly(p0, p1, g + 22 * sc * brilho), fill=(255, 235, 60))
    d.polygon(palito_poly(p0, p1, g), fill=(120, 220, 120) if verde else (240, 205, 150), outline=(110, 70, 30))
    hx, hy = p1
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    n = math.hypot(dx, dy) or 1
    hx, hy = hx - dx / n * 4 * sc, hy - dy / n * 4 * sc
    r = g * 0.85
    d.ellipse([hx - r, hy - r * 1.0, hx + r, hy + r * 1.0], fill=cor_cabeca, outline=(90, 15, 10), width=max(2, int(3 * sc)))
    d.ellipse([hx - r * 0.45, hy - r * 0.55, hx - r * 0.05, hy - r * 0.15], fill=(255, 140, 120))


_cache = {}


def mesa(tema):
    if tema not in _cache:
        c1, c2, veio = TEMAS[tema]
        img = s.gradient(c1, c2).convert("RGBA")
        d = ImageDraw.Draw(img)
        rnd = random.Random(5)
        if tema == "madeira":
            for y in range(0, H, 160):  # tábuas
                d.line([(0, y), (W, y)], fill=(70, 38, 15), width=5)
                for _ in range(9):
                    yy = y + rnd.randint(10, 150)
                    d.arc([rnd.randint(-400, 600), yy - 30, rnd.randint(700, 1500), yy + 30], 180, 360,
                          fill=veio + (255,), width=2)
        else:
            for _ in range(70):
                x, y = rnd.randint(0, W), rnd.randint(0, H)
                d.line([(x, y), (x + rnd.randint(40, 200), y + rnd.randint(-6, 6))], fill=veio + (255,), width=2)
        # quadro claro onde fica a conta
        quadro = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(quadro).rounded_rectangle([50, EQ_Y - 260, W - 50, EQ_Y + 250], 50, fill=(255, 255, 255, 40),
                                                 outline=(255, 255, 255, 120), width=6)
        img.alpha_composite(quadro)
        _cache[tema] = img
    return _cache[tema].copy()


def cabecalho(img, linha1, linha2, numero, t=9.0, cor1=None):
    d = ImageDraw.Draw(img)
    s.pilula(d, 540, 205, f"DESAFIO DO PALITO #{numero}", (200, 40, 40), size=46, pad=36, h=90)
    e = min(1.0, t / 0.35)
    sc = 1 + 0.25 * (1 - e)
    s.texto(d, (540, 355), linha1, int(118 * sc), cor1 or b.YELLOW)
    s.texto(d, (540, 470), linha2, 64, b.WHITE)


def desenhar_conta(img, ps, xs, sc, esconder=None, extra=None, verde=False):
    """ps = peças; esconder = (i, seg) que não desenha (o que está voando); extra = [(p0, p1, brilho)]."""
    for i, ((t, sg), x0) in enumerate(zip(ps, xs)):
        for seg in sorted(sg):
            if esconder and (i, seg) == esconder:
                continue
            p0, p1 = ponta(t, seg, x0, sc)
            desenhar_palito(img, p0, p1, sc, verde=verde)
    for p0, p1, br in extra or []:
        desenhar_palito(img, p0, p1, sc, brilho=br, verde=verde)


def lerp(a, b_, k):
    return a + (b_ - a) * k


def suave(k):
    k = min(max(k, 0.0), 1.0)
    return k * k * (3 - 2 * k)


def voo(p0a, p1a, p0b, p1b, k):
    """Palito voando de (p0a,p1a) até (p0b,p1b): centro em arco, ângulo e tamanho interpolados."""
    ca = ((p0a[0] + p1a[0]) / 2, (p0a[1] + p1a[1]) / 2)
    cb = ((p0b[0] + p1b[0]) / 2, (p0b[1] + p1b[1]) / 2)
    aa = math.atan2(p1a[1] - p0a[1], p1a[0] - p0a[0])
    ab = math.atan2(p1b[1] - p0b[1], p1b[0] - p0b[0])
    da = (ab - aa + math.pi) % (2 * math.pi) - math.pi
    la, lb = math.hypot(p1a[0] - p0a[0], p1a[1] - p0a[1]), math.hypot(p1b[0] - p0b[0], p1b[1] - p0b[1])
    k = suave(k)
    cx, cy = lerp(ca[0], cb[0], k), lerp(ca[1], cb[1], k) - 170 * math.sin(math.pi * k)
    a, ln = aa + da * k, lerp(la, lb, k)
    dx, dy = math.cos(a) * ln / 2, math.sin(a) * ln / 2
    return (cx - dx, cy - dy), (cx + dx, cy + dy)


BAR = (140, 1110, 940, 1160)


def barra(img, frac, total):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = BAR
    d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 34, fill=b.WHITE)
    d.rounded_rectangle(BAR, 26, fill=(60, 70, 110))
    if frac > 0.002:
        d.rounded_rectangle([x0, y0, max(x0 + (x1 - x0) * frac, x0 + 52), y1], 26, fill=b.ORANGE if frac > 0.3 else b.RED)
    n = math.ceil(frac * total)
    if n > 0:
        d.text(((x0 + x1) // 2, (y0 + y1) // 2), str(n), font=b.font(b.F_BLACK, 42), fill=b.WHITE, anchor="mm",
               stroke_width=4, stroke_fill=b.NAVY)


def balao(img, txt, cx, cy, t, cor=b.RED, size=58, larg=760):
    e = min(1.0, t / 0.3)
    if e <= 0:
        return
    d = ImageDraw.Draw(img)
    f = b.font(b.F_BLACK, size)
    while d.textlength(txt, font=f) > larg - 60 and f.size > 30:
        f = b.font(b.F_BLACK, f.size - 3)
    w, h = (d.textlength(txt, font=f) + 70) * (0.6 + 0.4 * e), 120 * (0.6 + 0.4 * e)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 50, fill=cor, outline=b.WHITE, width=7)
    if e > 0.6:
        d.text((cx, cy), txt, font=f, fill=b.WHITE, anchor="mm", stroke_width=4, stroke_fill=b.NAVY)


def zoom(img, z):
    if abs(z - 1) < 1e-3:
        return img
    cw, ch = W / z, H / z
    x0, y0 = (W - cw) / 2, (H - ch) / 2
    return img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))


class Desafio:
    """Monta um Short da série. Campos (veja shorts/palito-1/build_short.py):
    conta, modo ("mover" | "tirar"), mostrar (lista de novas contas a revelar, na ordem), numero, tema,
    titulo (2 linhas da tela), falas {"q", "comenta", "r1", ["r2"], "final", ["dica"]}, count, dica_txt."""

    def __init__(self, here, conta, modo, mostrar, numero, tema, titulo, falas, count=8.0, dica_txt=None,
                 musica="Sneaky Snitch.mp3"):
        self.here, self.conta, self.modo, self.numero, self.tema = here, conta, modo, numero, tema
        self.titulo, self.falas, self.count, self.dica_txt = titulo, falas, count, dica_txt
        self.musica = os.path.join(s.QP, "musicas", musica)
        if certa(conta):
            sys.exit(f"ERRO: a conta {conta} já está certa.")
        todas = mover1(conta) if modo == "mover" else tirar1(conta)
        por_conta = {n: (de, para) for de, para, n in todas}
        faltam = [m for m in mostrar if m not in por_conta]
        if faltam:
            sys.exit(f"ERRO: {faltam} não sai de {conta} com 1 palito ({modo}). Possíveis: {sorted(por_conta)}")
        extras = sorted(set(por_conta) - set(mostrar))
        if extras:
            sys.exit(f"ERRO: {conta} também vira {extras}: mostre todas as respostas (mostrar=...) ou troque a conta.")
        self.sols = [(m,) + por_conta[m] for m in mostrar]
        self.ps = pecas(conta)
        self.sc, self.xs = geometria(conta)
        self.A = lambda n: os.path.join(here, "assets", n)

    # -------------------------------------------------- vozes
    def vozes(self):
        import asyncio, edge_tts
        if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
            import ssl, edge_tts.communicate as _c
            _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
        os.makedirs(os.path.join(self.here, "assets"), exist_ok=True)
        for k, txt in self.falas.items():
            p = self.A(f"{k}.mp3")
            if os.path.exists(p) and os.path.getsize(p) < 1000:
                os.remove(p)  # Edge TTS às vezes grava vazio
            for _ in range(3):
                if os.path.exists(p):
                    break
                try:
                    asyncio.run(edge_tts.Communicate(txt, "pt-BR-AntonioNeural", rate="+20%", pitch="+2Hz").save(p))
                    print("voz", k, "-", txt, flush=True)
                except Exception as e:
                    print("voz falhou, tentando de novo:", k, e, flush=True)

    # -------------------------------------------------- telas
    def base(self, t):
        img = mesa(self.tema)
        cabecalho(img, *self.titulo, self.numero, t)
        return img

    def pergunta_frames(self, fala, dica_em=None):
        total = fala + self.count
        for n in range(int(total * FPS)):
            t = n / FPS
            img = self.base(t)
            # palitos entram um por um bem rápido (0,6 s) e depois ficam parados
            desenhar_conta(img, self.ps, self.xs, self.sc)
            frac = 1.0 if t < fala else 1 - (t - fala) / self.count
            barra(img, frac, self.count)
            pose = "pensando" if frac > 0.3 else "assustado"
            b.put_palito(img, pose, 330, 230, 1570, int(7 * math.sin(t * (4 if pose == "pensando" else 15))))
            if self.dica_txt and dica_em is not None and t >= dica_em:
                balao(img, "DICA: " + self.dica_txt, 560, 1235, t - dica_em, cor=(40, 150, 70), size=50, larg=820)
            yield zoom(img, 1.0 + 0.025 * t / total).convert("RGB")

    def comenta_frames(self, dur):
        for n in range(int(dur * FPS)):
            t = n / FPS
            img = self.base(9)
            desenhar_conta(img, self.ps, self.xs, self.sc)
            balao(img, "COMENTA ANTES DE VER!", 540, 1180, t, cor=b.RED, size=60, larg=900)
            s.texto(ImageDraw.Draw(img), (620, 1360), "A RESPOSTA VEM AÍ...", 52, b.WHITE)
            b.put_palito(img, "apontando", 330, 230, 1570, int(6 * math.sin(t * 6)))
            yield img.convert("RGB")

    def resposta_frames(self, sol, dur, ps_antes):
        nova, de, para = sol
        (i, seg) = de
        p0a, p1a = ponta(ps_antes[i][0], seg, self.xs[i], self.sc)
        if para:
            j, seg2 = para
            p0b, p1b = ponta(ps_antes[j][0], seg2, self.xs[j], self.sc)
        depois = pecas(nova) if para else None
        for n in range(int(dur * FPS)):
            t = n / FPS
            img = self.base(9)
            brilho = 0.5 + 0.5 * math.sin(t * 14) if t < 0.7 else 1.0
            if para:
                k = (t - 0.7) / 1.1
                if k < 1:
                    q0, q1 = voo(p0a, p1a, p0b, p1b, max(k, 0))
                    desenhar_conta(img, ps_antes, self.xs, self.sc, esconder=de, extra=[(q0, q1, brilho)])
                else:
                    desenhar_conta(img, depois, self.xs, self.sc, verde=True)
            else:  # tirar: o palito sai voando para cima e some
                k = (t - 0.7) / 0.9
                if k < 1:
                    q0 = (p0a[0], p0a[1] - 900 * suave(max(k, 0)))
                    q1 = (p1a[0], p1a[1] - 900 * suave(max(k, 0)))
                    desenhar_conta(img, ps_antes, self.xs, self.sc, esconder=de, extra=[(q0, q1, brilho)])
                else:
                    novo = list(ps_antes)
                    novo[i] = (novo[i][0], novo[i][1] - {seg})
                    desenhar_conta(img, novo, self.xs, self.sc, verde=True)
            fim = (t - 1.8) if para else (t - 1.6)
            if fim > 0:
                d = ImageDraw.Draw(img)
                e = min(1.0, fim / 0.3)
                cx, cy, r = 540, 1210, 70 * (0.5 + 0.5 * e)
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 170, 70), outline=b.WHITE, width=7)
                d.line([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.35), (cx + r * 0.5, cy - r * 0.35)],
                       fill=b.WHITE, width=int(16 * e) + 1)
                s.texto(d, (540, 1350), nova.replace("-", " − ").replace("+", " + ").replace("=", " = "), 74, b.YELLOW)
                b.put_palito(img, "comemorando", 330, 230, 1570, int(10 * math.sin(t * 9)))
            else:
                b.put_palito(img, "pensando", 330, 230, 1570)
            yield zoom(img, 1.02).convert("RGB")

    def final_frames(self, dur):
        img = mesa(self.tema)
        d = ImageDraw.Draw(img)
        s.texto(d, (540, 420), "ACERTOU?", 150, b.YELLOW)
        d.rounded_rectangle([110, 540, 970, 690], 55, fill=b.RED, outline=b.WHITE, width=8)
        s.texto(d, (540, 615), "COMENTA \"EU\" AÍ!", 76, b.WHITE, max_w=820)
        s.texto(d, (540, 800), "AMANHÃ TEM OUTRO", 62, b.WHITE)
        b.selo(img, 540, 920, 1.3)
        b.put_palito(img, "comemorando", 420, 540, 1560)
        for n in range(int(dur * FPS)):
            yield zoom(img, 1.0 + 0.04 * n / FPS / dur).convert("RGB")

    # -------------------------------------------------- montagem
    def montar(self, saida):
        self.vozes()
        A, dur = self.A, s.duracao
        tmp = tempfile.mkdtemp(prefix="short_palito_")
        sfx = b.make_sfx(tmp)
        video = os.path.join(tmp, "video.mp4")
        tl = s.Timeline(video)
        tl.sound(A("q.mp3"), at=0.05, voz=True)
        fala = dur(A("q.mp3")) + 0.2
        dica_em = None
        if self.dica_txt and os.path.exists(A("dica.mp3")):
            dica_em = fala + self.count / 2
            tl.sound(A("dica.mp3"), at=dica_em, voz=True)
        for k in range(int(self.count)):
            tl.sound(sfx["tick"], at=fala + k, vol=0.8)
        for f in self.pergunta_frames(fala, dica_em):
            tl.frame(f)
        tl.sound(A("comenta.mp3"), at=tl.t + 0.05, voz=True)
        for f in self.comenta_frames(dur(A("comenta.mp3")) + 0.3):
            tl.frame(f)
        for n, sol in enumerate(self.sols, 1):
            tl.sound(sfx["whoosh"], at=tl.t + 0.7, vol=0.7)
            tl.sound(sfx["ding"], at=tl.t + 1.8, vol=0.8)
            tl.sound(A(f"r{n}.mp3"), at=tl.t + 1.9, voz=True)
            for f in self.resposta_frames(sol, 1.9 + dur(A(f"r{n}.mp3")) + 0.6, self.ps):
                tl.frame(f)
        tl.sound(A("final.mp3"), at=tl.t + 0.1, voz=True)
        for f in self.final_frames(dur(A("final.mp3")) + 0.7):
            tl.frame(f)
        tl.close()
        s.mixar(tl, video, self.musica, saida)
        print(f"OK {saida} ({tl.t:.1f}s)")

    def previa(self):
        out = os.path.join(self.here, "previa")
        os.makedirs(out, exist_ok=True)
        pf = list(self.pergunta_frames(2.5, 3.0 if self.dica_txt else None))
        rf = list(self.resposta_frames(self.sols[0], 4.0, self.ps))
        ims = [pf[2], pf[int(5.5 * FPS)], list(self.comenta_frames(1.0))[20], rf[int(1.2 * FPS)], rf[-1],
               list(self.final_frames(1.0))[10]]
        sheet = Image.new("RGB", (len(ims) * 370, 640), (25, 25, 25))
        for i, im in enumerate(ims):
            sheet.paste(im.resize((360, 640)), (i * 370, 0))
        sheet.save(os.path.join(out, "prancha.jpg"), quality=85)
        ims[0].save(os.path.join(out, "quadro1.jpg"), quality=85)
        print(os.path.join(out, "prancha.jpg"))
