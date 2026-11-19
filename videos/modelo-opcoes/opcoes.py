"""Quiz Palito — modelo de vídeo LONGO (16:9) com pergunta em formato de QUESTÃO: foto + opções A/B/C,
igual aos Shorts (pedido do Patrick, 2026-11-09). Fundo com movimento e alternativas animadas como no Short.

Tela da pergunta: número + pergunta no topo, foto grande à esquerda, 3 opções empilhadas à direita,
Palito pensando no canto e a barra de tempo embaixo. Na resposta a opção certa fica verde com ✔,
as outras escurecem e o Palito comemora.

Extras (aprovados pelo Patrick, 2026-11-09):
  - efeitos sonoros: `make_sfx(tmp)` + `sons_pergunta(...)` (whoosh, pop das alternativas, tique-taque,
    tique rápido no fim, acerto);
  - VÍDEO CURTO no lugar da foto em algumas perguntas (umas 1 a cada 5): q["clipe"] = "panda.mp4"
    (arquivo em CLIPES, baixado com `automacao/fotos_wiki.py clipes`), aparece com selo "VÍDEO";
  - transição entre perguntas: `transicao_frames(ultimo_quadro, q, total)` (faixa diagonal com o selo).
Intro RAPIDINHA (2026-11-10, 2º pedido): `intro_rapida(titulo, sub, dur, fotos)` de 2 a 3 s com saudação curta
falada, transição e já a 1ª pergunta. Mudanças de 2026-11-10 (Patrick): SEM tela de abertura longa — o vídeo já começa na 1ª pergunta, com a chamada numa
faixa por cima (`pergunta_frames(..., gancho="...")`, a saudação/apresentação é falada por cima dela);
placar de bolinhas "CONTA SEUS PONTOS!" embaixo da barra e selo "+1 SE ACERTOU!" em cada resposta.

Uso num vídeo novo (modelo completo em previa.py, função video()):
    sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes")); import opcoes as op
    op.FOTOS, op.CLIPES = os.path.join(HERE, "fotos"), os.path.join(HERE, "clipes")
    q = {"n": 1, "pergunta": "QUE LUGAR É ESSE?", "foto": "torre-eiffel.jpg",
         "opcoes": ["Big Ben", "Torre Eiffel", "Torre de Pisa"], "certa": 1}
    op.sons_pergunta(tl, sfx, tl.t, fala, op.COUNT)
    for f in op.pergunta_frames(q, total=60, fala=fala): tl.frame(f)
    for f in op.resposta_frames(q, dur, total=60, t0=fala + op.COUNT): tl.frame(f)
"""
import math, os, subprocess, sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "05-nao-diga-o-mesmo"))
import build_naodiga as nd
sys.path.insert(0, HERE)
import engaja as eg
from build_naodiga import b

W, H, FPS = b.W, b.H, b.FPS
FOTOS = HERE                       # pasta das fotos do vídeo (trocar no vídeo novo)
CLIPES = HERE                      # pasta dos vídeos curtos (clipes/<slug>.mp4)
COUNT = 5.0                        # segundos para responder
VERDE = (60, 200, 90)
CORES = [((40, 170, 90), (10, 90, 60)), ((230, 60, 90), (130, 20, 60)), ((30, 120, 220), (15, 45, 140)),
         ((150, 70, 200), (60, 25, 120)), ((255, 150, 0), (200, 60, 0)), ((0, 160, 170), (0, 80, 100))]

# Posições (1920x1080)
CARD_C, CARD = (430, 545), 600      # centro e lado do cartão da foto
OPT_X, OPT_W, OPT_H = 1105, 700, 128
OPT_Y = (380, 545, 710)             # centro de cada opção
PAL_CX, PAL_BASE, PAL_H = 1700, 1000, 560
BAR = (130, 905, 1480, 950)
_cache = {}                         # só sprites de tamanho fixo


def _padrao():
    """Ladrilho de '?' e globinhos que se repete sem emenda (240x216 cabe certinho em 1920x1080)."""
    if "padrao" not in _cache:
        tw, th = 240, 216
        tile = Image.new("L", (tw, th), 0)
        d = ImageDraw.Draw(tile)
        d.text((60, 54), "?", font=b.font(b.F_BLACK, 76), fill=255, anchor="mm")
        x, y = 180, 162
        d.ellipse([x - 30, y - 30, x + 30, y + 30], outline=255, width=6)
        d.line([x, y - 30, x, y + 30], fill=255, width=5)
        d.line([x - 30, y, x + 30, y], fill=255, width=5)
        m = Image.new("L", (W, H), 0)
        for yy in range(0, H, th):
            for xx in range(0, W, tw):
                m.paste(tile, (xx, yy))
        _cache["padrao"] = m.point(lambda v: v * 34 // 255)
    return _cache["padrao"]


def fundo(n, t=0.0):
    """Degradê da cor da pergunta + padrão andando na diagonal (fundo com movimento)."""
    k = ("grad", n % len(CORES))
    if k not in _cache:
        _cache[k] = b.gradient(*CORES[n % len(CORES)]).convert("RGBA")
    img = _cache[k].copy()
    m = ImageChops.offset(_padrao(), int(t * 40) % 240, int(t * 36) % 216)
    img.paste((255, 255, 255, 255), (0, 0, W, H), m)
    return img


def zoom(img, z):
    """Zoom lento na tela toda, igual ao Short."""
    if abs(z - 1) < 1e-3:
        return img
    cw, ch = W / z, H / z
    x0, y0 = (W - cw) / 2, (H - ch) / 2
    return img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))


def foto(nome, size, filtro=None):
    k = ("foto", nome, size, filtro)
    if k in _cache:
        return _cache[k]
    im = Image.open(os.path.join(FOTOS, nome)).convert("RGB")
    im = ImageOps.fit(im, (size, size), Image.LANCZOS)
    if filtro == "amarela":
        im = ImageOps.colorize(im.convert("L"), black=(70, 45, 0), mid=(255, 205, 0), white=(255, 250, 200))
    im = im.convert("RGBA")
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1], int(size * 0.07), fill=255)
    im.putalpha(m)
    _cache[k] = im
    return im


def moldura_sprite():
    """Cartão branco vazio com sombra (a foto ou o vídeo vai por cima)."""
    if "moldura" not in _cache:
        m = 30
        sp = Image.new("RGBA", (CARD + 2 * m, CARD + 2 * m), (0, 0, 0, 0))
        sh = Image.new("RGBA", sp.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([m, m + 14, m + CARD, m + CARD + 14], 50, fill=(0, 0, 40, 110))
        sp.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
        ImageDraw.Draw(sp).rounded_rectangle([m, m, m + CARD, m + CARD], 50, fill=b.WHITE, outline=b.NAVY, width=8)
        _cache["moldura"] = sp
    return _cache["moldura"]


def cartao_sprite(q, filtro=None):
    k = ("cartao", q["foto"], filtro)
    if k in _cache:
        return _cache[k]
    sp = moldura_sprite().copy()
    sp.alpha_composite(foto(q["foto"], CARD - 40, filtro), (50, 50))
    _cache[k] = sp
    return sp


class Clipe:
    """Lê um vídeo curto quadro a quadro (em loop), já no tamanho do cartão. Não guarda nada na memória."""

    def __init__(self, nome):
        self.s = CARD - 40
        self.p = subprocess.Popen(
            ["ffmpeg", "-loglevel", "error", "-stream_loop", "-1", "-i", os.path.join(CLIPES, nome), "-vf",
             f"scale={self.s}:{self.s}:force_original_aspect_ratio=increase,crop={self.s}:{self.s},fps={FPS}",
             "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        m = Image.new("L", (self.s, self.s), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, self.s - 1, self.s - 1], int(self.s * 0.07), fill=255)
        self.mask = m
        self.ult = None

    def cartao(self):
        raw = self.p.stdout.read(self.s * self.s * 3)
        if len(raw) == self.s * self.s * 3:
            self.ult = Image.frombytes("RGB", (self.s, self.s), raw)
        sp = moldura_sprite().copy()
        if self.ult is not None:
            im = self.ult.convert("RGBA")
            im.putalpha(self.mask)
            sp.alpha_composite(im, (50, 50))
        # selo "VÍDEO" no canto do cartão
        d = ImageDraw.Draw(sp)
        d.rounded_rectangle([62, 62, 262, 126], 32, fill=b.RED, outline=b.WHITE, width=5)
        d.polygon([(84, 78), (84, 110), (110, 94)], fill=b.WHITE)
        d.text((185, 95), "VÍDEO", font=b.font(b.F_BLACK, 36), fill=b.WHITE, anchor="mm")
        return sp

    def fechar(self):
        self.p.kill()
        self.p.wait()


def _cartao_agora(q, filtro):
    """Cartão da pergunta neste quadro: vídeo (se a pergunta tiver clipe) ou foto."""
    if q.get("clipe"):
        if "_clipe" not in q:
            q["_clipe"] = Clipe(q["clipe"])
        return q["_clipe"].cartao()
    return cartao_sprite(q, filtro)


def opcao_sprite(i, txt, estado=None):
    """estado: None (normal), 'sim' (certa, verde com ✔) ou 'nao' (escurecida)."""
    k = ("op", i, txt, estado)
    if k in _cache:
        return _cache[k]
    cv = Image.new("RGBA", (OPT_W + 60, OPT_H + 60), (0, 0, 0, 0))
    x0, y0 = 30, 30
    if estado == "sim":
        glow = Image.new("RGBA", cv.size, (0, 0, 0, 0))
        ImageDraw.Draw(glow).rounded_rectangle([x0 - 18, y0 - 18, x0 + OPT_W + 18, y0 + OPT_H + 18], 70,
                                               fill=(255, 240, 120, 210))
        cv.alpha_composite(glow.filter(ImageFilter.GaussianBlur(14)))
    b.shadowed_round_rect(cv, (x0, y0, x0 + OPT_W, y0 + OPT_H), 64, VERDE if estado == "sim" else b.WHITE)
    d = ImageDraw.Draw(cv)
    d.rounded_rectangle([x0, y0, x0 + OPT_W, y0 + OPT_H], 64, outline=b.NAVY, width=7)
    d.ellipse([x0 + 14, y0 + 14, x0 + 114, y0 + 114], fill=b.WHITE if estado == "sim" else b.YELLOW,
              outline=b.NAVY, width=6)
    d.text((x0 + 64, y0 + 66), "ABC"[i], font=b.font(b.F_BLACK, 62), fill=b.NAVY, anchor="mm")
    t = txt.upper()
    fo = b.font(b.F_BLACK, 62)
    while d.textlength(t, font=fo) > OPT_W - 310 and fo.size > 34:
        fo = b.font(b.F_BLACK, fo.size - 2)
    sim = estado == "sim"
    d.text((x0 + OPT_W / 2 + 10, y0 + OPT_H / 2 + 2), t, font=fo, fill=b.WHITE if sim else b.NAVY, anchor="mm",
           stroke_width=4 if sim else 0, stroke_fill=b.NAVY)
    if sim:
        cx, cy = x0 + OPT_W - 66, y0 + OPT_H / 2
        d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], fill=b.WHITE, outline=b.NAVY, width=5)
        d.line([(cx - 21, cy), (cx - 5, cy + 17), (cx + 23, cy - 17)], fill=(40, 170, 70), width=11)
    if estado == "nao":
        sh = Image.new("RGBA", cv.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([x0, y0, x0 + OPT_W, y0 + OPT_H], 64, fill=(20, 30, 60, 150))
        cv.alpha_composite(sh)
    _cache[k] = cv
    return cv


def topo(img, q, total):
    d = ImageDraw.Draw(img)
    d.ellipse([40, 28, 190, 178], fill=b.ORANGE, outline=b.WHITE, width=8)
    d.text((115, 101), f"{q['n']:02d}", font=b.font(b.F_BLACK, 70), fill=b.WHITE, anchor="mm", stroke_width=3,
           stroke_fill=b.NAVY)
    t = q["pergunta"].upper()
    b.text_outline(d, (850, 92), t, nd.fit(d, t, 92, 1150), b.YELLOW, w=10)
    d.text((850, 168), f"PERGUNTA {q['n']} DE {total}", font=b.font(b.F_BLACK, 34), fill=b.WHITE, anchor="mm",
           stroke_width=4, stroke_fill=b.NAVY)
    b.selo(img, 1730, 100, 0.7)


def base(q, total, t=0.0):
    """Fundo andando + topo (o topo fica numa camada transparente guardada; tamanho fixo)."""
    k = ("topo", q["n"], total)
    if k not in _cache:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        topo(lay, q, total)
        _cache.pop(next((c for c in _cache if c[0] == "topo"), None), None)  # guarda só o atual
        _cache[k] = lay
    img = fundo(q["n"], t)
    img.alpha_composite(_cache[k])
    return img


def colar(img, sp, cx, cy, sc=1.0):
    if sc <= 0.02:
        return
    if abs(sc - 1) > 1e-3:
        sp = sp.resize((max(1, int(sp.width * sc)), max(1, int(sp.height * sc))), Image.BILINEAR)
    img.alpha_composite(sp, (int(cx - sp.width / 2), int(cy - sp.height / 2)))


def pula(x):
    x = min(max(x, 0.0), 1.0)
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def barra(img, frac, count=COUNT):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = BAR
    d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 32, fill=b.WHITE)
    d.rounded_rectangle(BAR, 24, fill=(60, 70, 110))
    if frac > 0.002:
        xe = x0 + (x1 - x0) * frac
        d.rounded_rectangle([x0, y0, max(xe, x0 + 48), y1], 24, fill=b.ORANGE if frac > 0.34 else b.RED)
    s = math.ceil(frac * count)
    if s > 0:
        d.text(((x0 + x1) // 2, (y0 + y1) // 2), str(s), font=b.font(b.F_BLACK, 40), fill=b.WHITE, anchor="mm",
               stroke_width=4, stroke_fill=b.NAVY)


def placar(img, q, total, t, respondida=False):
    """Bolinhas do bloco de 10 atual embaixo da barra (o placar falado continua a cada 10)."""
    bloco = (q["n"] - 1) // 10
    feitas = (q["n"] - 1) % 10 + (1 if respondida else 0)
    eg.pontos(img, 930, 1012, feitas, min(10, total - bloco * 10), t, raio=25, gap=18,
              rotulo="CONTA SEUS PONTOS!", rotulo_size=38, rotulo_acima=False)


def pergunta_frames(q, total, count=COUNT, filtro=None, fala=0.0, gancho=None, gancho_dur=None):
    """Foto entra com pulinho, as alternativas pulam uma a uma e ficam flutuando; no fim do tempo tremem.
    `fala`: segundos de narração antes da barra começar a correr.
    `gancho`: só na 1ª pergunta — a chamada do vídeo ("CONSEGUE ACERTAR TODAS?\nVALENDO!") numa faixa por
    cima do título durante `gancho_dur` s (padrão: a fala). Não há tela de abertura antes da 1ª pergunta."""
    ops = [opcao_sprite(i, o) for i, o in enumerate(q["opcoes"])]
    dur = fala + count
    for i in range(int(dur * FPS)):
        t = i / FPS
        frac = 1.0 if t < fala else 1 - (t - fala) / count
        img = base(q, total, t)
        colar(img, _cartao_agora(q, filtro), CARD_C[0], CARD_C[1] + 6 * math.sin(t * 2.2), pula(t / 0.4))
        for k, sp in enumerate(ops):
            ent = pula((t - 0.3 - 0.15 * k) / 0.35)
            dx = 5 * math.sin(t * 40 + k) if frac < 0.3 else 0
            colar(img, sp, OPT_X + dx, OPT_Y[k] + 5 * math.sin(t * 3 + k * 1.3), ent)
        barra(img, frac, count)
        placar(img, q, total, t)
        pose = "pensando" if frac > 0.3 else "assustado"
        b.put_palito(img, pose, PAL_H, PAL_CX, PAL_BASE, int(7 * math.sin(t * (5 if pose == "pensando" else 18))))
        if gancho:
            eg.faixa_gancho(img, 850, 122, gancho, t, gancho_dur or max(fala, 2.5), larg=1350, size=78)
        yield zoom(img, 1.0 + 0.03 * t / dur).convert("RGB")


def resposta_frames(q, dur, total, filtro_antes=None, t0=0.0):
    """A certa cresce verde com ✔, as outras encolhem e escurecem; foto volta à cor (se tinha filtro)."""
    clipe = bool(q.get("clipe"))
    am, cor = (None, None) if clipe else (cartao_sprite(q, filtro_antes), cartao_sprite(q, None))
    for i in range(int(dur * FPS)):
        tt = i / FPS
        img = base(q, total, t0 + tt)
        a = min(1.0, tt / 0.45)
        if clipe:
            card = _cartao_agora(q, None)
        else:
            card = cor if (a >= 1 or filtro_antes is None) else Image.blend(am, cor, a)
        colar(img, card, CARD_C[0], CARD_C[1])
        for k, o in enumerate(q["opcoes"]):
            if k == q["certa"]:
                sc = 1.0 + 0.12 * math.sin(min(tt / 0.4, 1.0) * math.pi) + 0.04 * min(tt / 0.4, 1.0)
                colar(img, opcao_sprite(k, o, "sim"), OPT_X, OPT_Y[k], sc)
            else:
                colar(img, opcao_sprite(k, o, "nao"), OPT_X, OPT_Y[k], 1.0 - 0.06 * min(tt / 0.25, 1.0))
        placar(img, q, total, t0 + tt, respondida=True)
        eg.mais_um(img, OPT_X, 840, tt, size=42)
        if tt < 0.2:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(120 * (1 - tt / 0.2)))))
        b.put_palito(img, "comemorando", PAL_H, PAL_CX, PAL_BASE, -int(abs(26 * math.sin(tt * 7))))
        yield zoom(img, 1.03 + 0.02 * tt / dur).convert("RGB")
    if "_clipe" in q:
        q.pop("_clipe").fechar()


def primeiro_quadro(q, total):
    """Como a tela da pergunta começa (fundo, topo, barra cheia, Palito) — usado na transição."""
    img = base(q, total, 0.0)
    barra(img, 1.0)
    placar(img, q, total, 0.0)
    b.put_palito(img, "pensando", PAL_H, PAL_CX, PAL_BASE, 0)
    return img.convert("RGB")


def transicao_frames(antes, q, total, dur=0.6):
    """Faixa diagonal amarela com o selo varre a tela da esquerda para a direita, trocando de pergunta."""
    depois = primeiro_quadro(q, total)
    larg, incl = 520, 420                      # largura da faixa e inclinação
    n = int(dur * FPS)
    for i in range(n):
        p = (i + 1) / n
        p = p * p * (3 - 2 * p)
        x = -larg - incl + p * (W + 2 * larg + 2 * incl)   # borda da frente da faixa (no topo)
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


def make_sfx(tmp):
    """Sons do modelo: os de sempre (tick, ding, whoosh) + pop, tique rápido e acerto."""
    sfx = b.make_sfx(tmp)
    novos = {
        "pop": "aevalsrc='0.5*sin(2*PI*(500+2200*t)*t)*exp(-28*t)':s=44100:d=0.14",
        "tique": "aevalsrc='0.55*sin(2*PI*2400*t)*exp(-70*t)':s=44100:d=0.07",
        "acerto": "aevalsrc='0.3*(sin(2*PI*1047*t)*between(t,0,0.12)+sin(2*PI*1319*t)*between(t,0.09,0.21)"
                  "+sin(2*PI*1568*t)*between(t,0.18,0.3)+(sin(2*PI*2093*t)+0.5*sin(2*PI*3136*t))*gte(t,0.27)"
                  "*exp(-5*(t-0.27)))':s=44100:d=1.1",
    }
    for k, src in novos.items():
        sfx[k] = os.path.join(tmp, k + ".wav")
        b.run(["ffmpeg", "-y", "-f", "lavfi", "-i", src, sfx[k]])
    return sfx


def sons_pergunta(tl, sfx, t0, fala=0.0, count=COUNT, entrada=True):
    """Agenda os sons de uma pergunta que começa em t0 (antes de gerar os quadros dela)."""
    if entrada:
        tl.sound(sfx["whoosh"], at=t0, vol=0.6)
    for k in range(3):                                   # alternativas pulando
        tl.sound(sfx["pop"], at=t0 + 0.3 + 0.15 * k, vol=0.7)
    for s in range(int(count)):                          # tique-taque, mais rápido no fim
        tl.sound(sfx["tick"], at=t0 + fala + s, vol=0.7)
        if s >= count - 2:
            tl.sound(sfx["tique"], at=t0 + fala + s + 0.5, vol=0.6)
    tl.sound(sfx["acerto"], at=t0 + fala + count, vol=0.8)


def fundo_abertura(caminho, escurecer=0.35):
    """Fundo da intro a partir de uma imagem do Google Flow (`abertura.jpg` na pasta do vídeo; 2026-11-17):
    cobre a tela, escurece um pouco para o título ler bem e faz um zoom lento. Devolve fundo(t) ou None."""
    if not caminho or not os.path.exists(caminho):
        return None
    base = ImageOps.fit(Image.open(caminho).convert("RGB"), (W, H))
    base = Image.blend(base, Image.new("RGB", (W, H), (0, 0, 0)), escurecer)

    def f(t):
        z = 1.0 + 0.04 * min(t / 3.0, 1.0)
        w, h = int(W / z), int(H / z)
        x, y = (W - w) // 2, (H - h) // 2
        return base.crop((x, y, x + w, y + h)).resize((W, H)).convert("RGBA")
    return f


def intro_rapida(titulo, sub="", dur=2.6, fotos=(), filtro=None, cor=4, abertura=None):
    """Intro rapidinha 16:9 (2 a 3 s): selo, título do tema, até 5 fotos do tema e o Palito acenando.
    Fale por cima uma saudação CURTA e variada + o tema (ex.: "Chegou mais um Quiz Palito! Times de A a Z!").
    `abertura` = caminho da cena gerada no Google Flow (ex.: os.path.join(PASTA, "abertura.jpg")): se o arquivo
    existir, vira o fundo da intro; se não, usa o fundo colorido de sempre.
    Depois: `transicao_frames(ultimo_quadro_da_intro, q1, total)` e a 1ª pergunta (com `gancho`)."""
    linhas = [(titulo, b.WHITE)] + ([(sub, b.YELLOW)] if sub else [])
    ims = [f if isinstance(f, Image.Image) else foto(f, 170, filtro) for f in fotos[:5]]  # nome do arquivo ou imagem
    fa = fundo_abertura(abertura)
    return eg.intro_rapida_frames(fa or (lambda t: fundo(cor, t)), linhas, dur, W, H, cy0=300 if ims else 390, passo=165,
                                  tamanhos=[130, 150][:len(linhas)], palito=(600, 1660, 1060), selo=(800, 110, 1.0),
                                  imagens=ims, img_y=720, img_lado=170)
