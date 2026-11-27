"""Quiz Palito — MOTION GRAPHICS nas transições entre perguntas (pedido do Patrick, 2026-11-21).

Serve para vídeo longo (1920x1080) e Short (1080x1920): tudo é medido pelo tamanho do quadro.

    import motion
    for f in motion.transicao(ultimo_quadro, primeiro_quadro_da_proxima, estilo="raios", n=5, total=36):
        tl.frame(f)
    motion.sons(tl, sfx, estilo)          # agenda os sons da transição (antes de gerar os quadros)

Estilos:
  "raios"  — EXPLOSÃO: a tela dá um zoom rápido, um círculo amarelo com raios girando explode do centro,
             o número da pergunta pula grande no meio e o círculo fecha revelando a próxima.
  "faixas" — CORTINA DE CORES: 4 faixas diagonais (amarelo, laranja, azul, azul-escuro) entram em cascata,
             o selo + "PERGUNTA 5" passam no meio, formas (círculos, triângulos, ?) voam e as faixas saem.
  "cartao" — CARTÃO VOADOR: a tela encolhe num cartão que gira e voa para fora, o Palito atravessa
             correndo no fundo de '?', e a próxima pergunta entra girando como cartão e cresce.
"""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "05-nao-diga-o-mesmo"))
from build_naodiga import b

FPS = b.FPS
ESTILOS = ("raios", "faixas", "cartao", "splash")
DUR = {"raios": 1.0, "faixas": 1.0, "cartao": 1.1, "splash": 1.0}
AMARELO, LARANJA, AZUL, MARINHO, BRANCO = b.YELLOW, b.ORANGE, b.BLUE, b.NAVY, b.WHITE
ROSA = (235, 70, 120)


# ---------- curvas de movimento ----------

def _clamp(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def ease_out(x):
    x = _clamp(x)
    return 1 - (1 - x) ** 3


def ease_in(x):
    x = _clamp(x)
    return x ** 3


def ease_io(x):
    x = _clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def back_out(x, s=1.9):
    """Passa um pouco do ponto e volta (efeito 'mola')."""
    x = _clamp(x) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


# ---------- peças ----------

def _zoom(img, z, blur=0):
    w, h = img.size
    cw, ch = int(w / z), int(h / z)
    x, y = (w - cw) // 2, (h - ch) // 2
    out = img.crop((x, y, x + cw, y + ch)).resize((w, h), Image.BILINEAR)
    if blur > 0.5:
        out = out.filter(ImageFilter.GaussianBlur(blur))
    return out


def _numero(img, cx, cy, n, total, sc, u):
    """'PERGUNTA' pequeno + número gigante com contorno (sc = escala da mola)."""
    if sc <= 0.02 or n is None:
        return
    d = ImageDraw.Draw(img)
    fs = max(10, int(300 * u * sc))
    f = b.font(b.F_BLACK, fs)
    txt = str(n)
    sw = max(4, int(fs * 0.07))
    d.text((cx + int(10 * u * sc), cy + int(14 * u * sc)), txt, font=f, fill=MARINHO, anchor="mm",
           stroke_width=sw, stroke_fill=MARINHO)
    d.text((cx, cy), txt, font=f, fill=BRANCO, anchor="mm", stroke_width=sw, stroke_fill=MARINHO)
    f2 = b.font(b.F_BLACK, max(8, int(70 * u * sc)))
    import engaja
    rot = engaja.TXT["pergunta"]
    d.text((cx, cy - int(205 * u * sc)), rot, font=f2, fill=MARINHO, anchor="mm",
           stroke_width=max(2, int(8 * u * sc)), stroke_fill=BRANCO)


def _raios(w, h, cx, cy, ang, n=16, c1=AMARELO, c2=LARANJA, r=None):
    r = r or int(math.hypot(w, h))
    img = Image.new("RGB", (w, h), c1)
    d = ImageDraw.Draw(img)
    for k in range(n):
        a0 = ang + k * 2 * math.pi / n
        a1 = a0 + math.pi / n
        d.polygon([(cx, cy), (cx + r * math.cos(a0), cy + r * math.sin(a0)),
                   (cx + r * math.cos(a1), cy + r * math.sin(a1))], fill=c2)
    return img


def _forma(d, kind, x, y, s, rot, cor, u):
    if kind == 0:
        d.ellipse([x - s, y - s, x + s, y + s], fill=cor)
    elif kind == 1:
        pts = [(x + s * math.cos(rot + k * 2.094), y + s * math.sin(rot + k * 2.094)) for k in range(3)]
        d.polygon(pts, fill=cor)
    elif kind == 2:
        d.ellipse([x - s, y - s, x + s, y + s], outline=cor, width=max(3, int(s * 0.35)))
    else:
        f = b.font(b.F_BLACK, max(10, int(s * 2.4)))
        d.text((x, y), "?", font=f, fill=cor, anchor="mm", stroke_width=max(2, int(6 * u)), stroke_fill=MARINHO)


# ---------- estilo 1: explosão de raios ----------

def _raios_frames(antes, depois, n, total, dur):
    w, h = antes.size
    u = min(w, h) / 1080
    cx, cy = w // 2, int(h * (0.5 if w > h else 0.45))
    R = math.hypot(w, h) / 2 + 40
    N = int(dur * FPS)
    for i in range(N):
        t = (i + 1) / N
        # 0-0.35: tela antiga dá zoom e o círculo cresce | 0.35-0.65: número | 0.65-1: círculo fecha revelando
        if t < 0.5:
            fundo = _zoom(antes, 1 + 0.25 * ease_in(t / 0.5), blur=8 * ease_in(t / 0.5))
            r = R * ease_out(t / 0.38)
        else:
            fundo = _zoom(depois, 1.18 - 0.18 * ease_out((t - 0.5) / 0.5))
            r = R * (1 - ease_in((t - 0.62) / 0.38))
        img = fundo.copy()
        if r > 2:
            disco = _raios(w, h, cx, cy, t * 2.4)
            m = Image.new("L", (w, h), 0)
            md = ImageDraw.Draw(m)
            md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
            img.paste(disco, (0, 0), m)
            d = ImageDraw.Draw(img)
            borda = max(6, int(18 * u))
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=MARINHO, width=borda)
            if r > 20 * u:   # anel branco que vem atrás
                r2 = r * 0.82
                d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=BRANCO, width=max(3, int(8 * u)))
            sc = back_out((t - 0.18) / 0.3) * (1 - ease_in((t - 0.68) / 0.22))
            _numero(img, cx, cy + int(30 * u), n, total, sc, u)
        yield img


def _raios_sons(tl, sfx, at):
    tl.sound(sfx["whoosh"], at=at, vol=0.7)
    if "pop" in sfx:
        tl.sound(sfx["pop"], at=at + 0.25, vol=0.9)
    if "boom" in sfx:
        tl.sound(sfx["boom"], at=at + 0.2, vol=0.8)


# ---------- estilo 2: cortina de faixas coloridas ----------

def _faixas_frames(antes, depois, n, total, dur):
    w, h = antes.size
    u = min(w, h) / 1080
    cores = [AMARELO, LARANJA, AZUL, MARINHO]
    incl = 0.38 * h                       # inclinação das faixas
    span = w + incl + 200 * u
    rnd = random.Random(n or 7)
    formas = [(rnd.randrange(4), rnd.uniform(0, w), rnd.uniform(0.1, 0.9) * h, rnd.uniform(18, 46) * u,
               rnd.uniform(0, 6.28), rnd.choice([BRANCO, ROSA, AMARELO, (0, 190, 200)]), rnd.uniform(0.6, 1.4))
              for _ in range(14)]
    N = int(dur * FPS)
    for i in range(N):
        t = (i + 1) / N
        img = (antes if t < 0.5 else depois).copy()
        d = ImageDraw.Draw(img)
        bw = w + incl + 100 * u
        for k, cor in enumerate(cores):
            # entra pela direita em cascata (0,1,2,3) e sai pela esquerda na ordem inversa (3,2,1,0)
            a = ease_out((t - 0.07 * k) / 0.36)
            s = ease_in((t - 0.52 - 0.06 * (3 - k)) / 0.3)
            if a <= 0 or s >= 1:
                continue
            x0 = (w + incl) + a * (-50 * u - (w + incl)) + s * (-bw - incl + 50 * u)
            d.polygon([(x0, 0), (x0 + bw, 0), (x0 + bw - incl, h), (x0 - incl, h)], fill=cor)
        # selo + número no meio, entre a entrada e a saída
        cob = ease_io((t - 0.15) / 0.42) * (1 - ease_io((t - 0.6) / 0.35))
        if cob > 0.02:
            img = img.convert("RGBA")
            for kind, fx, fy, fs, fr, fc, vel in formas:
                x = fx - (t * 900 * vel * u) % (w + 200 * u) + 100 * u
                if x < -100 * u:
                    x += w + 200 * u
                _forma(ImageDraw.Draw(img), kind, x, fy, fs * cob, fr + t * 6 * vel, fc, u)
            dx = (1 - back_out((t - 0.2) / 0.35)) * w * 0.6 - ease_in((t - 0.68) / 0.25) * w
            cx, cy = w / 2 + dx, h / 2
            if w > h:
                b.selo(img, int(cx), int(cy - 330 * u), 1.3 * u)
            else:
                b.selo(img, int(cx), int(cy - 330 * u), 1.3 * u)
            _numero(img, int(cx), int(cy + 60 * u), n, total, 1.0, u)
            img = img.convert("RGB")
        yield img


def _faixas_sons(tl, sfx, at):
    tl.sound(sfx["whoosh"], at=at, vol=0.7)
    if "pop" in sfx:
        tl.sound(sfx["pop"], at=at + 0.3, vol=0.8)
    tl.sound(sfx["whoosh"], at=at + 0.55, vol=0.5)


# ---------- estilo 3: cartão voador + Palito correndo ----------

_fundo_cache = {}


def _fundo_interrogacao(w, h, t, u):
    key = (w, h)
    if key not in _fundo_cache:
        tile = int(240 * u)
        base = Image.new("RGB", (w + tile, h + tile), AZUL)
        d = ImageDraw.Draw(base)
        f = b.font(b.F_BLACK, int(120 * u))
        for yy in range(0, h + tile, tile):
            for xx in range(0, w + tile, tile):
                off = tile // 2 if (yy // tile) % 2 else 0
                d.text((xx + off, yy + tile // 2), "?", font=f, fill=(48, 104, 214), anchor="mm")
        _fundo_cache[key] = (base, tile)
    base, tile = _fundo_cache[key]
    o = int(t * 400 * u) % tile
    return base.crop((o, o, o + w, o + h))


def _cartao(img, sc, ang, u):
    w, h = img.size
    cw, ch = max(2, int(w * sc)), max(2, int(h * sc))
    c = img.resize((cw, ch), Image.BILINEAR).convert("RGBA")
    bd = max(2, int(14 * u * sc / 0.6))
    framed = Image.new("RGBA", (cw + 2 * bd, ch + 2 * bd), BRANCO + (255,))
    framed.paste(c, (bd, bd))
    m = Image.new("L", framed.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, framed.width - 1, framed.height - 1], int(40 * u * sc / 0.6), fill=255)
    framed.putalpha(m)
    return framed.rotate(ang, expand=True, resample=Image.BICUBIC)


def _cartao_frames(antes, depois, n, total, dur):
    w, h = antes.size
    u = min(w, h) / 1080
    N = int(dur * FPS)
    pal_h = int((420 if w > h else 520) * u)
    for i in range(N):
        t = (i + 1) / N
        img = _fundo_interrogacao(w, h, t, u).convert("RGBA")
        # tela antiga: encolhe (0-0.25) e voa girando para a esquerda (0.2-0.5)
        if t < 0.5:
            sc = 1 - 0.42 * ease_out(t / 0.25)
            fx = -ease_in((t - 0.18) / 0.32) * w * 1.1
            ang = 14 * ease_in((t - 0.18) / 0.32) + 3 * ease_out(t / 0.25)
            c = _cartao(antes, sc, ang, u)
            img.alpha_composite(_sombra(c, u), (int(w / 2 + fx - c.width / 2 + 16 * u), int(h / 2 - c.height / 2 + 22 * u)))
            img.alpha_composite(c, (int(w / 2 + fx - c.width / 2), int(h / 2 - c.height / 2)))
        # nova: entra da direita girando (0.5-0.8) e cresce até a tela cheia (0.8-1)
        if t >= 0.45:
            e = back_out((t - 0.45) / 0.33, 1.2)
            fx = (1 - e) * w * 1.1
            ang = -12 * (1 - ease_out((t - 0.45) / 0.33))
            sc = 0.58 + 0.42 * ease_io((t - 0.8) / 0.2)
            if t >= 0.999:
                yield depois.copy()
                continue
            c = _cartao(depois, sc, ang, u)
            img.alpha_composite(_sombra(c, u), (int(w / 2 + fx - c.width / 2 + 16 * u), int(h / 2 - c.height / 2 + 22 * u)))
            img.alpha_composite(c, (int(w / 2 + fx - c.width / 2), int(h / 2 - c.height / 2)))
        # Palito atravessa correndo (pulinhos) da direita para a esquerda, na frente
        pt = (t - 0.12) / 0.7
        if 0 <= pt <= 1:
            pose = "comemorando" if (i // 3) % 2 else "acenando"
            px = w + pal_h * 0.6 - pt * (w + pal_h * 1.2)
            dy = -abs(math.sin(pt * math.pi * 5)) * 70 * u
            b.put_palito(img, pose, pal_h, int(px), int(h * 0.97), int(dy))
        yield img.convert("RGB")


def _sombra(c, u):
    a = c.getchannel("A").filter(ImageFilter.GaussianBlur(max(2, int(14 * u)))).point(lambda v: int(v * 0.45))
    s = Image.new("RGBA", c.size, (0, 0, 0, 255))
    s.putalpha(a)
    return s


def _cartao_sons(tl, sfx, at):
    tl.sound(sfx["whoosh"], at=at, vol=0.7)
    if "pop" in sfx:
        tl.sound(sfx["pop"], at=at + 0.35, vol=0.8)
    tl.sound(sfx["whoosh"], at=at + 0.5, vol=0.6)


# ---------- estilo 4: SPLASH (respingo de tinta; pedido do Patrick 2026-11-21) ----------

def _splat_forma(rnd, pontas=9, gotas=14):
    """Forma de respingo (raio 1): borda ondulada, pontas finas que terminam em gota e gotinhas soltas."""
    ondas = [(rnd.randint(3, 11), rnd.uniform(0, 6.28), rnd.uniform(0.03, 0.08)) for _ in range(5)]
    ang_p = [(rnd.uniform(0, 6.28), rnd.uniform(1.25, 1.75), rnd.uniform(0.05, 0.09)) for _ in range(pontas)]
    soltas = [(rnd.uniform(0, 6.28), rnd.uniform(1.15, 1.9), rnd.uniform(0.025, 0.07)) for _ in range(gotas)]
    return ondas, ang_p, soltas


def _splat(m, cx, cy, R, forma, cor=255, rot=0.0):
    """Desenha o respingo de raio R em (cx, cy) na máscara/imagem m."""
    if R < 1:
        return
    ondas, pontas, soltas = forma
    d = ImageDraw.Draw(m)
    pts = []
    for k in range(120):
        a = k * 2 * math.pi / 120
        r = 1 + sum(amp * math.sin(f * a + ph) for f, ph, amp in ondas)
        pts.append((cx + R * r * math.cos(a + rot), cy + R * r * math.sin(a + rot)))
    d.polygon(pts, fill=cor)
    for a, L, lw in pontas:              # pontas: triângulo fino + gota na ponta
        a += rot
        ca, sa = math.cos(a), math.sin(a)
        px, py = -sa, ca
        base = R * 0.85
        bw = R * lw * 2.2
        tx, ty = cx + R * L * ca, cy + R * L * sa
        d.polygon([(cx + base * ca + px * bw, cy + base * sa + py * bw),
                   (cx + base * ca - px * bw, cy + base * sa - py * bw), (tx, ty)], fill=cor)
        gr = R * lw
        d.ellipse([tx - gr, ty - gr, tx + gr, ty + gr], fill=cor)
    for a, L, gr in soltas:
        a += rot
        x, y = cx + R * L * math.cos(a), cy + R * L * math.sin(a)
        d.ellipse([x - R * gr, y - R * gr, x + R * gr, y + R * gr], fill=cor)


def _splash_frames(antes, depois, n, total, dur):
    """3 respingos de tinta (amarelo, laranja, azul) estouram e cobrem a tela, o número pula no meio
    e a próxima pergunta aparece de dentro de um último respingo que cresce."""
    w, h = antes.size
    u = min(w, h) / 1080
    rnd = random.Random(1000 + (n or 0))
    D = math.hypot(w, h)
    horiz = w > h
    # (cor, centro, início, raio final)
    # 5 respingos menores, um atrás do outro, em lugares diferentes (cor, centro, início, raio, forma, giro)
    cent = [(0.22, 0.3), (0.78, 0.7), (0.7, 0.22), (0.28, 0.75), (0.5, 0.5)]
    if not horiz:
        cent = [(y, x) for x, y in cent]
    cores = [AMARELO, ROSA, LARANJA, (0, 190, 200), AZUL]
    manchas = [(cor, (w * fx, h * fy), 0.06 * k, D * (0.2 + 0.05 * k), _splat_forma(rnd), rnd.uniform(-1, 1))
               for k, (cor, (fx, fy)) in enumerate(zip(cores, cent))]
    revela = _splat_forma(rnd, pontas=11, gotas=18)
    sombra = lambda c: tuple(int(v * 0.6) for v in c)
    N = int(dur * FPS)
    for i in range(N):
        t = (i + 1) / N
        if t >= 0.999:
            yield depois.copy()
            continue
        img = _zoom(antes, 1 + 0.06 * ease_out(t / 0.4))
        for cor, (cx, cy), t0, rf, forma, rot in manchas:
            p = (t - t0) / 0.2
            if p <= 0:
                continue
            R = rf * back_out(p, 1.6)
            _splat(img, cx + 10 * u, cy + 14 * u, R, forma, sombra(cor), rot)   # sombra (volume)
            _splat(img, cx, cy, R, forma, cor, rot)
            hl = R * 0.1                                                       # brilho
            ImageDraw.Draw(img).ellipse([cx - R * 0.5 - hl, cy - R * 0.5 - hl * 0.6, cx - R * 0.5 + hl,
                                         cy - R * 0.5 + hl * 0.6], fill=tuple(min(255, v + 70) for v in cor))
        if t >= 0.52:                          # a próxima pergunta "espirra" por cima, do centro
            p = (t - 0.52) / 0.44
            R = D * 0.8 * ease_out(p)
            borda = Image.new("L", (w, h), 0)
            _splat(borda, w / 2, h / 2, R * 1.04 + 12 * u, revela, 255, 0.3)
            img.paste(BRANCO, (0, 0), borda)
            m = Image.new("L", (w, h), 0)
            _splat(m, w / 2, h / 2, R, revela, 255, 0.3)
            img.paste(depois, (0, 0), m.filter(ImageFilter.GaussianBlur(1.2)))
        sc = back_out((t - 0.22) / 0.2) * (1 - ease_in((t - 0.5) / 0.14))
        if sc > 0.02:
            img = img.convert("RGBA")
            _numero(img, w // 2, int(h / 2 + 40 * u), n, total, sc, u)
            img = img.convert("RGB")
        yield img


def _splash_sons(tl, sfx, at):
    for k in range(3):
        tl.sound(sfx.get("splash", sfx["whoosh"]), at=at + 0.08 * k, vol=0.9 - 0.15 * k)
    if "pop" in sfx:
        tl.sound(sfx["pop"], at=at + 0.33, vol=0.8)
    tl.sound(sfx.get("splash", sfx["whoosh"]), at=at + 0.6, vol=0.7)


# ---------- uso ----------

_FRAMES = {"raios": _raios_frames, "faixas": _faixas_frames, "cartao": _cartao_frames, "splash": _splash_frames}
_SONS = {"raios": _raios_sons, "faixas": _faixas_sons, "cartao": _cartao_sons, "splash": _splash_sons}


def transicao(antes, depois, estilo="raios", n=None, total=None, dur=None):
    """Quadros RGB da transição de `antes` (último quadro da resposta) para `depois` (1º quadro da pergunta)."""
    antes, depois = antes.convert("RGB"), depois.convert("RGB")
    for f in _FRAMES[estilo](antes, depois, n, total, dur or DUR[estilo]):
        yield f.convert("RGB")


def sons(tl, sfx, estilo="raios", at=None):
    """Agenda os sons da transição que começa em `at` (padrão: agora)."""
    _SONS[estilo](tl, sfx, tl.t if at is None else at)


def make_sfx(tmp, sfx):
    """Acrescenta 'boom' (impacto grave) e 'pop' ao dicionário de sons, se faltarem."""
    novos = {"boom": "aevalsrc='0.9*sin(2*PI*(110-60*t)*t)*exp(-7*t)':s=44100:d=0.5",
             # 'splash': chiado molhado curto + batida grave (respingo de tinta)
             "splash": "aevalsrc='0.7*(random(0)*2-1)*exp(-14*t)*(0.6+0.4*sin(2*PI*35*t))+0.6*sin(2*PI*(160-90*t)*t)*exp(-18*t)':s=44100:d=0.35"}
    if "pop" not in sfx:
        novos["pop"] = "aevalsrc='0.5*sin(2*PI*(500+2200*t)*t)*exp(-28*t)':s=44100:d=0.14"
    for k, src in novos.items():
        sfx[k] = os.path.join(tmp, k + ".wav")
        b.run(["ffmpeg", "-y", "-f", "lavfi", "-i", src, sfx[k]])
    return sfx
