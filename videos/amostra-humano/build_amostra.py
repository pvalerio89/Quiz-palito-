"""AMOSTRA "estilo mais humano" (Patrick, 2026-11-13: "esse formato está muito robótico").

Mesmo layout aprovado (`modelo-opcoes/opcoes.py`), 6 perguntas de capitais (fotos do vídeo 22), com:
  - frases variadas (sem "Pergunta cinco!" toda vez) e reação de verdade a cada resposta;
  - ritmo variado: a 1ª bem rápida, DICA no meio da contagem, SUSPENSE ("a resposta é...") antes de revelar;
  - "VOCÊ SABIA?" em algumas respostas (1 frase);
  - DESAFIO FINAL com tela própria e batida de coração;
  - NÍVEIS no fim ("mestre das capitais", "time do Palito");
  - mais vida na tela: zoom de impacto na revelação, tremida quando o Palito erra, poses trocando.
Uso: py -3 gerar_vozes.py && py -3 build_amostra.py [--previa]
"""
import json, math, os, sys, tempfile
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
from opcoes import b, nd, eg, W, H, FPS

op.FOTOS = os.path.join(VIDEOS, "22-capitais", "fotos")
A = lambda n: os.path.join(HERE, "assets", n + ".mp3")
SAIDA = os.path.join(HERE, "amostra-estilo-humano.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Sneaky Snitch.mp3")
dur = lambda k: b.duration(A(k))
TOTAL = 6

# Cada pergunta: narração (q), contagem, chute do Palito durante a contagem, dica, suspense, resposta,
# resposta do Palito e "você sabia?".
Q = [
    dict(n=1, pergunta="CAPITAL DO BRASIL?", foto="brasilia.jpg", opcoes=["Brasília", "Rio de Janeiro", "São Paulo"],
         certa=0, count=4.0, sabia="O Rio foi capital até 1960, quando Brasília foi inaugurada."),
    dict(n=2, pergunta="CAPITAL DA BAHIA?", foto="salvador.jpg", opcoes=["Ilhéus", "Feira de Santana", "Salvador"],
         certa=2, count=6.0,
         sabia="Salvador foi a primeira capital do Brasil, de 1549 a 1763."),
    dict(n=3, pergunta="CAPITAL DA GRÉCIA?", foto="atenas.jpg", opcoes=["Esparta", "Atenas", "Olímpia"],
         certa=1, count=7.0, dica=("n_d3", "O NOME LEMBRA UMA DEUSA GREGA", 2.5)),
    dict(n=4, pergunta="CAPITAL DOS EUA?", foto="washington.jpg", opcoes=["Nova York", "Washington", "Los Angeles"],
         certa=1, count=7.0,
         suspense="n_s4", aviso="TEM PEGADINHA!"),
    dict(n=5, pergunta="CAPITAL DA AUSTRÁLIA?", foto="camberra.jpg", opcoes=["Sydney", "Melbourne", "Camberra"],
         certa=2, count=7.0, aviso="DERRUBA MUITA GENTE!"),
    dict(n=6, pergunta="CAPITAL DE RONDÔNIA?", foto="porto-velho.jpg", opcoes=["Ji-Paraná", "Ariquemes", "Porto Velho"],
         certa=2, count=9.0, suspense="n_s6", final=True),
]


# ---------- desenhos novos ----------

def balao(img, txt, t, cx=1645, cy=255):
    """Balão de fala do Palito (canto de cima à direita, acima dele)."""
    s = eg.pula(t / 0.25)
    if s <= 0.02:
        return
    lw, lh = 440, 130
    lay = Image.new("RGBA", (lw + 40, lh + 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([20, 20, 20 + lw, 20 + lh], 40, fill=b.WHITE, outline=b.NAVY, width=6)
    d.polygon([(lw - 120, 20 + lh - 4), (lw - 60, 20 + lh - 4), (lw - 70, lh + 70)], fill=b.WHITE)
    d.line([(lw - 120, 20 + lh - 2), (lw - 70, lh + 70), (lw - 60, 20 + lh - 2)], fill=b.NAVY, width=6)
    f = b.font(b.F_BLACK, 46)
    linhas = nd.wrap(d, txt.upper(), f, lw - 40)
    while len(linhas) > 2 and f.size > 28:
        f = b.font(b.F_BLACK, f.size - 4)
        linhas = nd.wrap(d, txt.upper(), f, lw - 40)
    y0 = 20 + lh / 2 - (len(linhas) - 1) * f.size * 0.55
    for i, l in enumerate(linhas):
        d.text((20 + lw / 2, y0 + i * f.size * 1.1), l, font=f, fill=b.NAVY, anchor="mm")
    op.colar(img, lay, cx, cy, s)


def faixa_baixo(img, rotulo, txt, t, cor=b.YELLOW):
    """Cartão embaixo (no lugar da barra): 'VOCÊ SABIA?' ou 'DICA'."""
    s = eg.pula(t / 0.3)
    if s <= 0.02:
        return
    lay = Image.new("RGBA", (1420, 210), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([10, 40, 1410, 200], 40, fill=cor, outline=b.NAVY, width=7)
    d.rounded_rectangle([40, 8, 420, 72], 30, fill=b.RED, outline=b.WHITE, width=5)
    d.text((230, 41), rotulo, font=b.font(b.F_BLACK, 40), fill=b.WHITE, anchor="mm")
    f = b.font(b.F_BLACK, 44)
    linhas = nd.wrap(d, txt, f, 1320)
    while len(linhas) > 2:
        f = b.font(b.F_BLACK, f.size - 3)
        linhas = nd.wrap(d, txt, f, 1320)
    y0 = 125 - (len(linhas) - 1) * f.size * 0.55
    for i, l in enumerate(linhas):
        d.text((710, y0 + i * f.size * 1.1), l, font=f, fill=b.NAVY, anchor="mm")
    op.colar(img, lay, 805, 960, s)


def tremer(img, t, forca=14):
    """Tremida rápida da tela (quando o Palito erra)."""
    if forca <= 0:
        return img
    dx, dy = int(forca * math.sin(t * 90)), int(forca * 0.6 * math.cos(t * 77))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    out.alpha_composite(img, (dx, dy) if dx >= 0 and dy >= 0 else (0, 0))
    if dx < 0 or dy < 0:
        out = img.transform((W, H), Image.AFFINE, (1, 0, -dx, 0, 1, -dy))
    return out


def pergunta_frames(q, fala):
    ops_ = [op.opcao_sprite(i, o) for i, o in enumerate(q["opcoes"])]
    count = q["count"]
    d_total = fala + count
    ch = q.get("chute")
    dc = q.get("dica")
    for i in range(int(d_total * FPS)):
        t = i / FPS
        frac = 1.0 if t < fala else 1 - (t - fala) / count
        img = op.base(q, TOTAL, t)
        op.colar(img, op._cartao_agora(q, None), op.CARD_C[0], op.CARD_C[1] + 6 * math.sin(t * 2.2), op.pula(t / 0.4))
        for k, sp in enumerate(ops_):
            ent = op.pula((t - 0.3 - 0.15 * k) / 0.35)
            dx = 5 * math.sin(t * 40 + k) if frac < 0.3 else 0
            op.colar(img, sp, op.OPT_X + dx, op.OPT_Y[k] + 5 * math.sin(t * 3 + k * 1.3), ent)
        op.barra(img, frac, count)
        op.placar(img, q, TOTAL, t)
        pose, mexe = ("pensando", 5) if frac > 0.3 else ("assustado", 18)
        if ch and fala + ch[2] <= t < fala + ch[2] + dur(ch[0]) + 1.0:
            pose, mexe = "apontando", 9
        b.put_palito(img, pose, op.PAL_H, op.PAL_CX, op.PAL_BASE, int(7 * math.sin(t * mexe)))
        if ch and t >= fala + ch[2]:
            balao(img, ch[1], t - fala - ch[2])
        if dc and fala + dc[2] <= t:
            faixa_baixo(img, "DICA", dc[1], t - fala - dc[2], cor=(170, 230, 255))
        if q.get("aviso"):
            eg.faixa_gancho(img, 850, 122, q["aviso"], t, max(fala, 2.5), larg=1100, size=78)
        yield op.zoom(img, 1.0 + 0.03 * t / d_total).convert("RGB")


def suspense_frames(q, d):
    """'A resposta é...': alternativas acendendo uma a uma, tela fechando devagar."""
    for i in range(int(d * FPS)):
        t = i / FPS
        img = op.base(q, TOTAL, t)
        op.colar(img, op._cartao_agora(q, None), op.CARD_C[0], op.CARD_C[1])
        luz = int(t * 6) % 3
        for k, o in enumerate(q["opcoes"]):
            op.colar(img, op.opcao_sprite(k, o), op.OPT_X, op.OPT_Y[k], 1.06 if k == luz else 0.97)
        op.placar(img, q, TOTAL, t)
        b.put_palito(img, "assustado", op.PAL_H, op.PAL_CX, op.PAL_BASE, int(5 * math.sin(t * 25)))
        escuro = Image.new("RGBA", (W, H), (0, 0, 0, int(110 * min(1, t / d))))
        img.alpha_composite(escuro)
        yield op.zoom(img, 1.03 + 0.07 * t / d).convert("RGB")


def resposta_frames(q, d, falas):
    """Revela com zoom de impacto; o Palito comemora ou fica bravo (com tremida se errou)."""
    rp = q.get("resp_pal")
    t_pal = falas.get("t_pal", 99)
    for i in range(int(d * FPS)):
        tt = i / FPS
        img = op.base(q, TOTAL, tt)
        op.colar(img, op.cartao_sprite(q, None), op.CARD_C[0], op.CARD_C[1])
        for k, o in enumerate(q["opcoes"]):
            if k == q["certa"]:
                sc = 1.0 + 0.12 * math.sin(min(tt / 0.4, 1.0) * math.pi) + 0.04 * min(tt / 0.4, 1.0)
                op.colar(img, op.opcao_sprite(k, o, "sim"), op.OPT_X, op.OPT_Y[k], sc)
            else:
                op.colar(img, op.opcao_sprite(k, o, "nao"), op.OPT_X, op.OPT_Y[k], 0.94)
        op.placar(img, q, TOTAL, tt, respondida=True)
        if q.get("sabia") and tt > 1.2:
            faixa_baixo(img, "VOCÊ SABIA?", q["sabia"], tt - 1.2)
        else:
            eg.mais_um(img, op.OPT_X, 840, tt, size=42)
        if q.get("errou"):
            pose = "maos_na_cintura" if tt >= t_pal else "assustado"
            dy = int(4 * math.sin(tt * 20))
        else:
            pose, dy = "comemorando", -int(abs(26 * math.sin(tt * 7)))
        b.put_palito(img, pose, op.PAL_H, op.PAL_CX, op.PAL_BASE, dy)
        if rp and tt >= t_pal:
            balao(img, rp[1], tt - t_pal)
        if tt < 0.2:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(150 * (1 - tt / 0.2)))))
        if q.get("errou") and tt < 0.6:
            img = tremer(img, tt, int(16 * (1 - tt / 0.6)))
        z = 1.10 - 0.07 * min(1, tt / 0.5) if tt < 0.5 else 1.03 + 0.02 * tt / d   # "soco" de zoom
        yield op.zoom(img, z).convert("RGB")


def desafio_frames(d):
    for i in range(int(d * FPS)):
        t = i / FPS
        bate = abs(math.sin(t * math.pi * 1.25)) ** 6          # pulsa no ritmo do coração
        img = nd.burst((200, 20, 30), (90, 0, 10), t * 10).convert("RGBA")
        dd = ImageDraw.Draw(img)
        s = max(0.1, min(1.0, t / 0.35)) * (1 + 0.06 * bate)
        b.text_outline(dd, (800, 330), "ÚLTIMA", b.font(b.F_BLACK, int(190 * s)), b.YELLOW, w=16)
        b.text_outline(dd, (800, 540), "PERGUNTA", b.font(b.F_BLACK, int(200 * s)), b.WHITE, w=18)
        b.text_outline(dd, (800, 740), "A MAIS DIFÍCIL!", b.font(b.F_BLACK, 80), b.WHITE, w=8)
        b.selo(img, 800, 920, 1.0)
        b.put_palito(img, "assustado", 620, 1620, 1060 + int((1 - min(1, t / 0.4)) * 600), int(6 * math.sin(t * 30)))
        yield img.convert("RGB")


def intro_frames(d, t_pal):
    base = list(op.intro_rapida("QUIZ DE CAPITAIS", "VOCÊ CONSEGUE?", d,
                                fotos=["paris.jpg", "roma.jpg", "londres.jpg", "toquio.jpg", "lisboa.jpg"]))
    for i, f in enumerate(base):
        t = i / FPS
        if t >= t_pal:
            img = f.convert("RGBA")
            balao(img, "Eu vou ganhar de você!", t - t_pal, cx=1470, cy=430)
            f = img.convert("RGB")
        yield f


def niveis_frames(d, t_pal):
    niveis = [("6", "MESTRE DAS CAPITAIS", (60, 200, 90)), ("4-5", "MANDOU MUITO BEM", (255, 170, 0)),
              ("0-3", "BORA TREINAR!", (235, 50, 50))]
    for i in range(int(d * FPS)):
        t = i / FPS
        img = op.fundo(3, t).copy()
        dd = ImageDraw.Draw(img)
        b.text_outline(dd, (800, 120), "QUANTAS VOCÊ FEZ?", b.font(b.F_BLACK, 110), b.YELLOW, w=12)
        for k, (n, txt, cor) in enumerate(niveis):
            s = eg.pula((t - 1.2 - k * 1.6) / 0.35)
            if s <= 0.02:
                continue
            lay = Image.new("RGBA", (1200, 170), (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            ld.rounded_rectangle([10, 10, 1190, 160], 60, fill=b.WHITE, outline=b.NAVY, width=7)
            ld.rounded_rectangle([10, 10, 300, 160], 60, fill=cor, outline=b.NAVY, width=7)
            ld.text((155, 85), n, font=b.font(b.F_BLACK, 80), fill=b.WHITE, anchor="mm", stroke_width=4,
                    stroke_fill=b.NAVY)
            ld.text((745, 85), txt, font=b.font(b.F_BLACK, 66), fill=b.NAVY, anchor="mm")
            op.colar(img, lay, 800, 330 + k * 200, s)
        b.text_outline(dd, (800, 975), "COMENTA SUA NOTA!", b.font(b.F_BLACK, 70), b.WHITE, w=8)
        pose = "maos_na_cintura" if t >= t_pal else "acenando"
        b.put_palito(img, pose, 560, 1680, 1060, int(6 * math.sin(t * 6)))
        if t >= t_pal:
            balao(img, "Ei! Revanche!", t - t_pal, cx=1560, cy=330)
        yield img.convert("RGB")


def curtir_frames(d, t_clique):
    """Pedido de curtida: joinha e coração gigantes, o Palito aponta; em t_clique os dois 'apertam' e
    pulam corações (a pausa do 'eu espero!')."""
    joia = nd.emoji("\U0001F44D", 300)
    cor = nd.emoji("\u2764\ufe0f", 300)
    for i in range(int(d * FPS)):
        t = i / FPS
        img = nd.burst((255, 90, 120), (200, 30, 80), t * 8).convert("RGBA")
        dd = ImageDraw.Draw(img)
        s = max(0.1, eg.pula(t / 0.4))
        b.text_outline(dd, (760, 150), "CURTE AÍ!", b.font(b.F_BLACK, int(150 * s)), b.WHITE, w=14)
        aperta = t >= t_clique
        k = 1.0 + (0.25 * math.sin(min(1, (t - t_clique) / 0.35) * math.pi) if aperta else 0.04 * math.sin(t * 6))
        for j, sp in enumerate((joia, cor)):
            ent = eg.pula((t - 0.2 - 0.2 * j) / 0.4)
            op.colar(img, sp, 520 + j * 480, 520, ent * k)
        if aperta:   # coraçõezinhos subindo
            for c in range(8):
                tc = t - t_clique - c * 0.12
                if 0 < tc < 1.6:
                    x = 1000 + 180 * math.sin(c * 2.1) + 30 * math.sin(tc * 6 + c)
                    op.colar(img, nd.emoji("\u2764\ufe0f", 70), x, 420 - tc * 260, 1 - tc / 2)
            b.text_outline(dd, (760, 860), "EU ESPERO!", b.font(b.F_BLACK, 90), b.YELLOW, w=10)
        b.put_palito(img, "apontando", 600, 1640, 1060, int(6 * math.sin(t * 6)))
        yield img.convert("RGB")


def inscreva_frames(d):
    """Fim curto: só 'se inscreva no canal' (Patrick, 2026-11-13)."""
    for i in range(int(d * FPS)):
        t = i / FPS
        img = op.fundo(3, t).copy()
        dd = ImageDraw.Draw(img)
        s = max(0.1, eg.pula(t / 0.4))
        b.text_outline(dd, (800, 260), "GOSTOU?", b.font(b.F_BLACK, int(150 * s)), b.YELLOW, w=14)
        bate = 1 + 0.05 * math.sin(t * 6)
        w2, h2 = int(900 * s * bate), int(170 * s * bate)
        dd.rounded_rectangle([800 - w2 // 2, 520 - h2 // 2, 800 + w2 // 2, 520 + h2 // 2], 60, fill=b.RED,
                             outline=b.WHITE, width=9)
        dd.text((800, 522), "INSCREVA-SE", font=b.font(b.F_BLACK, max(8, int(100 * s * bate))), fill=b.WHITE,
                anchor="mm", stroke_width=4, stroke_fill=b.NAVY)
        b.text_outline(dd, (800, 720), "NO CANAL", b.font(b.F_BLACK, 80), b.WHITE, w=8)
        b.selo(img, 800, 880, 1.4)
        b.put_palito(img, "acenando", 600, 1640, 1060, int(6 * math.sin(t * 6)))
        yield img.convert("RGB")


# ---------- montagem ----------

def montar(tl, sfx, so_previa=False):
    """Agenda falas e sons e devolve os quadros (gerador). Na prévia só usa os tempos."""
    marcas = []
    # INTRO: narrador -> Palito -> narrador
    t1 = 99
    t2 = dur("n_intro") + 0.25
    di = t2 + dur("n_intro2") + 0.3
    tl.sound(A("n_intro"), at=tl.t + 0.15)
    tl.sound(A("n_intro2"), at=tl.t + t2)
    ultimo = None
    for f in intro_frames(di, t1):
        ultimo = f
        yield "intro", f
    for q in Q:
        n = q["n"]
        if q.get("final"):
            dd = dur("n_desafio") + 0.8
            tl.sound(sfx["whoosh"])
            tl.sound(A("n_desafio"), at=tl.t + 0.2)
            for k in range(int(dd / 0.8) + 1):
                tl.sound(sfx["coracao"], at=tl.t + k * 0.8, vol=0.9)
            for f in desafio_frames(dd):
                ultimo = f
                yield "desafio", f
        fala = dur(f"n_q{n}") + 0.3
        tl.sound(sfx["whoosh"], vol=0.7)
        for f in op.transicao_frames(ultimo, q, TOTAL):
            yield "trans", f
        t0 = tl.t
        tl.sound(A(f"n_q{n}"), at=t0 + 0.1)
        op.sons_pergunta(tl, sfx, t0, fala=fala, count=q["count"], entrada=False)
        if q.get("chute"):
            tl.sound(A(q["chute"][0]), at=t0 + fala + q["chute"][2])
        if q.get("dica"):
            tl.sound(sfx["pop"], at=t0 + fala + q["dica"][2])
            tl.sound(A(q["dica"][0]), at=t0 + fala + q["dica"][2] + 0.1)
        if q.get("final"):
            for k in range(int((fala + q["count"]) / 0.8)):
                tl.sound(sfx["coracao"], at=t0 + k * 0.8, vol=0.6)
        for f in pergunta_frames(q, fala):
            yield f"q{n}", f
        if q.get("suspense"):
            ds = dur(q["suspense"]) + 0.9
            tl.sound(A(q["suspense"]), at=tl.t + 0.05)
            tl.sound(sfx["rufar"], at=tl.t + 0.2, vol=0.8)
            for f in suspense_frames(q, ds):
                yield f"s{n}", f
        tr = tl.t
        tl.sound(sfx["acerto"], at=tr, vol=0.8)
        tl.sound(A(f"n_r{n}"), at=tr + 0.3)
        falas = {}
        dr = dur(f"n_r{n}") + 0.3
        if q.get("resp_pal"):
            falas["t_pal"] = dr + 0.15
            tl.sound(A(q["resp_pal"][0]), at=tr + falas["t_pal"])
            if q.get("errou"):
                tl.sound(sfx["buzina"], at=tr + falas["t_pal"] - 0.1, vol=0.6)
            dr = falas["t_pal"] + dur(q["resp_pal"][0])
        if q.get("sabia"):
            dr = max(dr, 5.5)
        dr += 0.7
        for f in resposta_frames(q, dr, falas):
            ultimo = f
            yield f"r{n}", f
        if n == 2:   # pedido de curtida depois da 2ª resposta
            c1 = dur("n_curtir") + 0.3
            pausa = 1.6                      # o "tempinho"
            tl.sound(sfx["whoosh"])
            tl.sound(A("n_curtir"), at=tl.t + 0.2)
            tl.sound(sfx["pop"], at=tl.t + c1 + pausa * 0.4, vol=0.9)
            tl.sound(sfx["acerto"], at=tl.t + c1 + pausa * 0.4 + 0.1, vol=0.5)
            tl.sound(A("n_espero"), at=tl.t + c1 + pausa)
            for f in curtir_frames(c1 + pausa + dur("n_espero") + 0.6, c1 + pausa * 0.4):
                ultimo = f
                yield "curtir", f
    # FIM: níveis
    tl.sound(sfx["whoosh"])
    tf = dur("n_fim") + 0.5
    tl.sound(A("n_fim"), at=tl.t + 0.3)
    for f in inscreva_frames(tf + 1.5):
        yield "fim", f


def make_sfx(tmp):
    sfx = op.make_sfx(tmp)
    novos = {
        # batida de coração (tum-tum)
        "coracao": "aevalsrc='0.9*sin(2*PI*55*t)*exp(-18*t)+0.7*sin(2*PI*50*(t-0.22))*exp(-20*(t-0.22))*gte(t,0.22)'"
                   ":s=44100:d=0.6",
        # rufar de tambor que cresce
        "rufar": "aevalsrc='0.5*(t/1.8)*sin(2*PI*90*t)*(0.5+0.5*sin(2*PI*28*t))':s=44100:d=1.8",
        # buzina de erro (wah-wah)
        "buzina": "aevalsrc='0.35*sin(2*PI*(220-60*t)*t)*(0.6+0.4*sin(2*PI*6*t))':s=44100:d=0.9",
    }
    for k, src in novos.items():
        sfx[k] = os.path.join(tmp, k + ".wav")
        b.run(["ffmpeg", "-y", "-f", "lavfi", "-i", src, sfx[k]])
    return sfx


class TLFalso:
    """Para a prévia: só conta o tempo."""
    def __init__(self):
        self.t, self.audio = 0.0, []

    def sound(self, *a, **k):
        pass


def previa():
    tmp = tempfile.mkdtemp(prefix="amostra_")
    sfx = make_sfx(tmp)
    tl = TLFalso()
    escolha, vistos, n = [], {}, 0
    for nome, f in montar(tl, sfx):
        n += 1
        tl.t = n / FPS
        vistos[nome] = vistos.get(nome, 0) + 1
        k = vistos[nome]
        if (nome in ("intro", "desafio", "fim") and k == 75) or (nome[0] in "qsr" and k == 70) \
                or (nome[0] == "r" and k == 150):
            escolha.append(f.resize((640, 360), Image.LANCZOS))
    cols = 4
    pr = Image.new("RGB", (cols * 650, math.ceil(len(escolha) / cols) * 370), "black")
    for i, f in enumerate(escolha):
        pr.paste(f, ((i % cols) * 650, (i // cols) * 370))
    os.makedirs(os.path.join(HERE, "previa"), exist_ok=True)
    pr.save(os.path.join(HERE, "previa", "prancha.jpg"), quality=88)
    print(f"prancha ok, duração {tl.t:.1f}s")


def main():
    tmp = tempfile.mkdtemp(prefix="amostra_")
    sfx = make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    for _, f in montar(tl, sfx):
        tl.frame(f)
    total = tl.t
    tl.close()
    nd.HERE, nd.SAIDA = HERE, SAIDA
    nd.A = lambda x: MUSICA if x == "musica.mp3" else os.path.join(HERE, "assets", x)
    nd.mixar(tl, video, total)
    print(f"OK {SAIDA} ({total:.1f}s)")


if __name__ == "__main__":
    previa() if "--previa" in sys.argv else main()
