"""Quiz Palito — ESTILO MAIS HUMANO dos vídeos longos (Patrick aprovou em 2026-11-13; amostra em
`videos/amostra-humano/`). Usa o layout de `opcoes.py` e acrescenta:

  - DICA no meio da contagem (faixa azul embaixo + fala curta);
  - AVISO na faixa vermelha do topo durante a fala ("TEM PEGADINHA!", "DERRUBA MUITA GENTE!");
  - SUSPENSE antes de revelar ("A resposta é...", rufar de tambor, tela escurecendo);
  - "VOCÊ SABIA?" (1 frase) em algumas respostas;
  - zoom de impacto na revelação;
  - PEDIDO DE INSCRIÇÃO + LIKE (Patrick, 2026-11-19): tela "INSCREVA-SE" + joinha, fala "Se inscreva no canal e
    deixe seu like!", pausa curta e "Vai lá, eu espero!" (frases em FRASES_CURTIR / FRASES_ESPERO; nada de
    "coraçãozinho"/"joinha" na fala);
  - tela "ÚLTIMA PERGUNTA, A MAIS DIFÍCIL!" com batida de coração antes da última;
  - FIM curto só com "INSCREVA-SE NO CANAL" (sem tela de nota/níveis).
O Palito NÃO fala (sem voz, sem balão): Patrick não gostou.

Uso (cada função agenda os sons no Timeline e devolve os quadros; consuma na hora com tl.frame):
    import opcoes as op, humano as hu
    sfx = hu.make_sfx(tmp)
    q = {"n": 4, "pergunta": "CAPITAL DOS EUA?", "foto": "washington.jpg",
         "opcoes": ["Nova York", "Washington", "Los Angeles"], "certa": 1,
         "aviso": "TEM PEGADINHA!",                         # opcional
         "dica": ("d4.mp3", "O NOME É DE UM PRESIDENTE", 2.5),  # opcional: voz, texto, segundos após a fala
         "suspense": "s4.mp3",                                # opcional: "A resposta é..."
         "sabia": "Washington foi planejada para ser a capital.",  # opcional
         "final": False}                                      # True só na última (batida de coração)
    for f in hu.pergunta(tl, sfx, q, TOTAL, ultimo, voz_q=A("q4.mp3"), voz_r=A("p4.mp3"), count=7):
        tl.frame(f); ultimo = f
    for f in hu.curtir(tl, sfx, A("curtir.mp3"), A("espero.mp3")): tl.frame(f); ultimo = f
    for f in hu.ultima(tl, sfx, A("ultima.mp3")): tl.frame(f); ultimo = f
    for f in hu.inscreva(tl, sfx, A("outro.mp3")): tl.frame(f)
"""
import math, os
from PIL import Image, ImageDraw

import opcoes as op
from opcoes import b, nd, eg, W, H, FPS

dur = b.duration

# Fala do pedido no meio do vídeo (Patrick, 2026-11-19): SEMPRE "se inscreva no canal" + "deixe seu like" e
# depois "vai lá, eu espero". Pode variar o começo; NÃO falar "coraçãozinho" nem "joinha".
FRASES_CURTIR = [
    "Ei, antes da próxima... se inscreva no canal e deixe seu like!",
    "Rapidinho: se inscreva no canal e deixe seu like!",
    "Pera aí, antes de continuar! Se inscreva no canal e deixe seu like!",
    "Ô, antes da próxima pergunta... se inscreva no canal e deixe seu like!",
    "Antes de seguir: se inscreva no canal e deixe seu like!",
]
FRASES_ESPERO = ["Vai lá, eu espero!", "Vai lá, que eu espero!", "Vai lá, eu espero aqui!"]


def frase_curtir(seed=None):
    """(pede, espero) para o pedido de inscrição + like, variando entre vídeos."""
    import random
    r = random.Random(seed)
    return r.choice(FRASES_CURTIR), r.choice(FRASES_ESPERO)


# ---------- desenhos ----------

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
    while len(linhas) > 2 and f.size > 24:
        f = b.font(b.F_BLACK, f.size - 3)
        linhas = nd.wrap(d, txt, f, 1320)
    y0 = 125 - (len(linhas) - 1) * f.size * 0.55
    for i, l in enumerate(linhas):
        d.text((710, y0 + i * f.size * 1.1), l, font=f, fill=b.NAVY, anchor="mm")
    op.colar(img, lay, 805, 960, s)


def pergunta_frames(q, total, fala, count, gancho=None):
    ops_ = [op.opcao_sprite(i, o) for i, o in enumerate(q["opcoes"])]
    d_total = fala + count
    dc = q.get("dica")
    faixa = gancho or q.get("aviso")
    for i in range(int(d_total * FPS)):
        t = i / FPS
        frac = 1.0 if t < fala else 1 - (t - fala) / count
        img = op.base(q, total, t)
        op.colar(img, op._cartao_agora(q, None), op.CARD_C[0], op.CARD_C[1] + 6 * math.sin(t * 2.2), op.pula(t / 0.4))
        for k, sp in enumerate(ops_):
            ent = op.pula((t - 0.3 - 0.15 * k) / 0.35)
            dx = 5 * math.sin(t * 40 + k) if frac < 0.3 else 0
            op.colar(img, sp, op.OPT_X + dx, op.OPT_Y[k] + 5 * math.sin(t * 3 + k * 1.3), ent)
        op.barra(img, frac, count)
        op.placar(img, q, total, t)
        pose, mexe = ("pensando", 5) if frac > 0.3 else ("assustado", 18)
        b.put_palito(img, pose, op.PAL_H, op.PAL_CX, op.PAL_BASE, int(7 * math.sin(t * mexe)))
        if dc and fala + dc[2] <= t:
            faixa_baixo(img, "DICA", dc[1], t - fala - dc[2], cor=(170, 230, 255))
        if faixa:
            eg.faixa_gancho(img, 850, 122, faixa, t, max(fala, 2.5), larg=1350 if gancho else 1100,
                            size=78)
        yield op.zoom(img, 1.0 + 0.03 * t / d_total).convert("RGB")


def suspense_frames(q, total, d):
    """'A resposta é...': alternativas acendendo uma a uma, tela fechando devagar."""
    for i in range(int(d * FPS)):
        t = i / FPS
        img = op.base(q, total, t)
        op.colar(img, op._cartao_agora(q, None), op.CARD_C[0], op.CARD_C[1])
        luz = int(t * 6) % 3
        for k, o in enumerate(q["opcoes"]):
            op.colar(img, op.opcao_sprite(k, o), op.OPT_X, op.OPT_Y[k], 1.06 if k == luz else 0.97)
        op.placar(img, q, total, t)
        b.put_palito(img, "assustado", op.PAL_H, op.PAL_CX, op.PAL_BASE, int(5 * math.sin(t * 25)))
        img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(110 * min(1, t / d)))))
        yield op.zoom(img, 1.03 + 0.07 * t / d).convert("RGB")


def resposta_frames(q, total, d):
    """Revela com zoom de impacto; 'VOCÊ SABIA?' se a pergunta tiver; senão '+1 SE ACERTOU!'."""
    clipe = bool(q.get("clipe"))
    for i in range(int(d * FPS)):
        tt = i / FPS
        img = op.base(q, total, tt)
        card = op._cartao_agora(q, None) if clipe else op.cartao_sprite(q, None)
        op.colar(img, card, op.CARD_C[0], op.CARD_C[1])
        for k, o in enumerate(q["opcoes"]):
            if k == q["certa"]:
                sc = 1.0 + 0.12 * math.sin(min(tt / 0.4, 1.0) * math.pi) + 0.04 * min(tt / 0.4, 1.0)
                op.colar(img, op.opcao_sprite(k, o, "sim"), op.OPT_X, op.OPT_Y[k], sc)
            else:
                op.colar(img, op.opcao_sprite(k, o, "nao"), op.OPT_X, op.OPT_Y[k], 0.94)
        op.placar(img, q, total, tt, respondida=True)
        if q.get("sabia") and tt > 1.2:
            faixa_baixo(img, "VOCÊ SABIA?", q["sabia"], tt - 1.2)
        else:
            eg.mais_um(img, op.OPT_X, 840, tt, size=42)
        b.put_palito(img, "comemorando", op.PAL_H, op.PAL_CX, op.PAL_BASE, -int(abs(26 * math.sin(tt * 7))))
        if tt < 0.2:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(150 * (1 - tt / 0.2)))))
        z = 1.10 - 0.07 * min(1, tt / 0.5) if tt < 0.5 else 1.03 + 0.02 * tt / d   # "soco" de zoom
        yield op.zoom(img, z).convert("RGB")
    if "_clipe" in q:
        q.pop("_clipe").fechar()


def ultima_frames(d):
    """Tela vermelha 'ÚLTIMA PERGUNTA, A MAIS DIFÍCIL!' pulsando no ritmo do coração."""
    for i in range(int(d * FPS)):
        t = i / FPS
        bate = abs(math.sin(t * math.pi * 1.25)) ** 6
        img = nd.burst((200, 20, 30), (90, 0, 10), t * 10).convert("RGBA")
        dd = ImageDraw.Draw(img)
        s = max(0.1, min(1.0, t / 0.35)) * (1 + 0.06 * bate)
        b.text_outline(dd, (800, 330), "ÚLTIMA", b.font(b.F_BLACK, int(190 * s)), b.YELLOW, w=16)
        b.text_outline(dd, (800, 540), "PERGUNTA", b.font(b.F_BLACK, int(200 * s)), b.WHITE, w=18)
        b.text_outline(dd, (800, 740), "A MAIS DIFÍCIL!", b.font(b.F_BLACK, 80), b.WHITE, w=8)
        b.selo(img, 800, 920, 1.0)
        b.put_palito(img, "assustado", 620, 1620, 1060 + int((1 - min(1, t / 0.4)) * 600), int(6 * math.sin(t * 30)))
        yield img.convert("RGB")


def curtir_frames(d, t_clique):
    """Pedido de inscrição + like: botão vermelho INSCREVA-SE e joinha gigante, o Palito aponta; em t_clique os
    dois 'apertam' (o botão vira INSCRITO) e sobem joinhas (a pausa antes do 'vai lá, eu espero!')."""
    joia = nd.emoji("\U0001F44D", 280)
    for i in range(int(d * FPS)):
        t = i / FPS
        img = nd.burst((255, 70, 70), (170, 20, 40), t * 8).convert("RGBA")
        dd = ImageDraw.Draw(img)
        s = max(0.1, eg.pula(t / 0.4))
        b.text_outline(dd, (760, 140), "SE INSCREVA", b.font(b.F_BLACK, int(130 * s)), b.WHITE, w=13)
        b.text_outline(dd, (760, 270), "E DEIXE SEU LIKE!", b.font(b.F_BLACK, int(80 * s)), b.YELLOW, w=9)
        aperta = t >= t_clique
        k = 1.0 + (0.22 * math.sin(min(1, (t - t_clique) / 0.35) * math.pi) if aperta else 0.04 * math.sin(t * 6))
        # botão INSCREVA-SE (vira INSCRITO cinza no clique)
        e1 = eg.pula((t - 0.2) / 0.4) * k
        if e1 > 0.02:
            bw, bh = int(560 * e1), int(150 * e1)
            cx, cy = 520, 560
            cor = (90, 90, 90) if aperta else b.RED
            dd.rounded_rectangle([cx - bw // 2, cy - bh // 2, cx + bw // 2, cy + bh // 2], int(40 * e1), fill=cor,
                                 outline=b.WHITE, width=8)
            dd.text((cx, cy + 2), "INSCRITO ✓" if aperta else "INSCREVA-SE",
                    font=b.font(b.F_BLACK, max(8, int(66 * e1))), fill=b.WHITE, anchor="mm")
        op.colar(img, joia, 1060, 540, eg.pula((t - 0.4) / 0.4) * k)
        if aperta:
            for c in range(8):
                tc = t - t_clique - c * 0.12
                if 0 < tc < 1.6:
                    x = 1060 + 180 * math.sin(c * 2.1) + 30 * math.sin(tc * 6 + c)
                    op.colar(img, nd.emoji("\U0001F44D", 70), x, 420 - tc * 260, 1 - tc / 2)
            b.text_outline(dd, (760, 860), "VAI LÁ, EU ESPERO!", b.font(b.F_BLACK, 90), b.YELLOW, w=10)
        b.put_palito(img, "apontando", 600, 1640, 1060, int(6 * math.sin(t * 6)))
        yield img.convert("RGB")


def inscreva_frames(d):
    """Fim curto: só 'se inscreva no canal'."""
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


# ---------- sons ----------

def make_sfx(tmp):
    sfx = op.make_sfx(tmp)
    novos = {
        "coracao": "aevalsrc='0.9*sin(2*PI*55*t)*exp(-18*t)+0.7*sin(2*PI*50*(t-0.22))*exp(-20*(t-0.22))*gte(t,0.22)'"
                   ":s=44100:d=0.6",
        "rufar": "aevalsrc='0.5*(t/1.8)*sin(2*PI*90*t)*(0.5+0.5*sin(2*PI*28*t))':s=44100:d=1.8",
    }
    for k, src in novos.items():
        sfx[k] = os.path.join(tmp, k + ".wav")
        b.run(["ffmpeg", "-y", "-f", "lavfi", "-i", src, sfx[k]])
    return sfx


# ---------- blocos prontos (agendam sons e devolvem quadros) ----------

def pergunta(tl, sfx, q, total, ultimo, voz_q, voz_r, count=7.0, gancho=None):
    """Transição + pergunta falada (com dica/aviso) + suspense opcional + resposta falada."""
    fala = dur(voz_q) + 0.3
    tl.sound(sfx["whoosh"], vol=0.7)
    for f in op.transicao_frames(ultimo, q, total):
        yield f
    t0 = tl.t
    tl.sound(voz_q, at=t0 + 0.1)
    op.sons_pergunta(tl, sfx, t0, fala=fala, count=count, entrada=False)
    if q.get("dica"):
        tl.sound(sfx["pop"], at=t0 + fala + q["dica"][2])
        tl.sound(q["dica"][0], at=t0 + fala + q["dica"][2] + 0.1)
    if q.get("final"):
        for k in range(int((fala + count) / 0.8)):
            tl.sound(sfx["coracao"], at=t0 + k * 0.8, vol=0.6)
    for f in pergunta_frames(q, total, fala, count, gancho):
        yield f
    if q.get("suspense"):
        ds = dur(q["suspense"]) + 0.9
        tl.sound(q["suspense"], at=tl.t + 0.05)
        tl.sound(sfx["rufar"], at=tl.t + 0.2, vol=0.8)
        for f in suspense_frames(q, total, ds):
            yield f
    tl.sound(sfx["acerto"], at=tl.t, vol=0.8)
    tl.sound(voz_r, at=tl.t + 0.3)
    dr = dur(voz_r) + 0.3
    if q.get("sabia"):
        dr = max(dr, 5.5)
    for f in resposta_frames(q, total, dr + 0.7):
        yield f


def curtir(tl, sfx, voz_pede, voz_espero, pausa=1.6):
    """Pede inscrição + like ('Se inscreva no canal e deixe seu like!'), dá um tempinho e fala 'Vai lá, eu
    espero!' (frases em FRASES_CURTIR / FRASES_ESPERO; variar)."""
    c1 = dur(voz_pede) + 0.3
    tl.sound(sfx["whoosh"])
    tl.sound(voz_pede, at=tl.t + 0.2)
    tl.sound(sfx["pop"], at=tl.t + c1 + pausa * 0.4, vol=0.9)
    tl.sound(sfx["acerto"], at=tl.t + c1 + pausa * 0.4 + 0.1, vol=0.5)
    tl.sound(voz_espero, at=tl.t + c1 + pausa)
    for f in curtir_frames(c1 + pausa + dur(voz_espero) + 0.6, c1 + pausa * 0.4):
        yield f


def ultima(tl, sfx, voz):
    """Antes da última pergunta: 'Atenção... essa é a última pergunta! E é a mais difícil!'."""
    d = dur(voz) + 0.8
    tl.sound(sfx["whoosh"])
    tl.sound(voz, at=tl.t + 0.2)
    for k in range(int(d / 0.8) + 1):
        tl.sound(sfx["coracao"], at=tl.t + k * 0.8, vol=0.9)
    for f in ultima_frames(d):
        yield f


def inscreva(tl, sfx, voz):
    """Fim: 'Gostou? Então se inscreve no canal!' (variar a frase), sem tela de nota."""
    tl.sound(sfx["whoosh"])
    tl.sound(voz, at=tl.t + 0.3)
    for f in inscreva_frames(dur(voz) + 1.8):
        yield f
