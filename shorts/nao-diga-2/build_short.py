"""Short — "NÃO DIGA O MESMO QUE O PALITO 2" (nao-diga-2), do vídeo 53 (videos/53-nao-diga-2).

4 rodadas do longo, 3 vidas, 30 a 50 s, sem abertura (NOVO RITMO, 2026-11-17): a 1ª imagem já é a rodada 1, com a
chamada na faixa vermelha. Transição SPLASH entre as rodadas. Fala final curta + "o jogo completo tá no canal".
Descrição com o link do longo (LINK_DO_VIDEO_LONGO). Um arquivo só para YouTube Shorts e TikTok.
Uso: py -3 build_short.py            (gera vozes que faltam e monta o Short)
     py -3 build_short.py --previa   (prancha com quadros para conferir)
"""
import asyncio, json, math, os, sys, tempfile
from PIL import Image, ImageDraw

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import short_base as s
from short_base import b, W, H, FPS

sys.path.insert(0, os.path.join(QP, "videos", "05-nao-diga-o-mesmo"))
import build_naodiga as bn
sys.path.insert(0, os.path.join(QP, "videos", "modelo-opcoes"))
import engaja as eg

A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "short-nao-diga-2.mp4")
MUSICA = os.path.join(QP, "musicas", "Fluffing a Duck.mp3")
COUNT = 3.0
CHAMADA = "VOCÊ TEM SÓ 3 VIDAS!"
POR_N = {r["n"]: r for r in json.load(open(os.path.join(QP, "videos", "53-nao-diga-2", "itens.json"), encoding="utf-8"))}
RODADAS = [POR_N[k] for k in (4, 18, 24, 44)]   # flor, lanche, doce (pegadinha), amarela (a última)
N = len(RODADAS)
VIDAS = 3
CORES = [((0, 170, 170), (0, 80, 110)), ((110, 60, 200), (45, 20, 110)), ((255, 110, 80), (190, 40, 70)),
         ((30, 140, 220), (15, 50, 130)), ((200, 30, 60), (90, 5, 30))]
FALAS = {
    "gancho": "Só três vidas! Pensou igual ao Palito, perde uma!",   # falado por cima da 1ª rodada
    "final": "O jogo completo tá no canal!",   # fala final curta (retenção) + chama para o longo
}
FALA_Q = ["Diga uma flor!", "Diga um lanche!",
          "Pegadinha! Um doce, sem ser brigadeiro!",
          "A última: algo amarelo que não é fruta!"]
FALA_A = ["Rosa! Perdeu uma?", "Hambúrguer! Tchau, uma vida!", "Beijinho! Caiu?", "O sol! Perdeu?"]
CARD = (90, 380, 990, 1010)
FAIXA = (110, 1050, 970, 1170)
BAR = (130, 1215, 950, 1258)


def textos():
    t = dict(FALAS)
    for k, r in enumerate(RODADAS, 1):
        t[f"q{k}"] = FALA_Q[k - 1]
        t[f"a{k}"] = FALA_A[k - 1]
    t["q1"] = f"{FALAS['gancho']} {t['q1']}"
    t.pop("gancho")
    return t


def vozes():
    import edge_tts
    if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
        import ssl, edge_tts.communicate as _c
        _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    for k, txt in textos().items():
        if os.path.exists(A(f"{k}.mp3")) and os.path.getsize(A(f"{k}.mp3")) < 1024:
            os.remove(A(f"{k}.mp3"))
        if not os.path.exists(A(f"{k}.mp3")):
            asyncio.run(edge_tts.Communicate(txt, "pt-BR-AntonioNeural", rate="+20%", pitch="+2Hz").save(A(f"{k}.mp3")))
            print("voz", k, flush=True)


_cache = {}


def cartao_sprite(k, r, revelado):
    key = ("c", k, revelado)
    if key not in _cache:
        x0, y0, x1, y1 = CARD
        w, h = x1 - x0, y1 - y0
        cv = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
        b.shadowed_round_rect(cv, (30, 30, 30 + w, 30 + h), 50, b.WHITE)
        d = ImageDraw.Draw(cv)
        d.rounded_rectangle([30, 30, 30 + w, 30 + h], 50, outline=b.NAVY, width=8)
        ecx, ecy = 30 + w / 2, 30 + 200
        d.ellipse([ecx - 160, ecy - 160, ecx + 160, ecy + 160], fill=(255, 220, 90) if revelado else (255, 236, 160),
                  outline=b.NAVY, width=6)
        bn.paste_c(cv, bn.icone(r, 220, revelado), ecx, ecy)
        size = 84
        while True:
            f = b.font(b.F_BLACK, size)
            lin = bn.wrap(d, r["pedido"], f, w - 90)
            lh = int(size * 1.12)
            if (len(lin) * lh <= 200 and all(d.textlength(l, font=f) <= w - 90 for l in lin)) or size <= 44:
                break
            size -= 4
        cy = 30 + 505 - (len(lin) - 1) * lh / 2
        for i, l in enumerate(lin):
            d.text((ecx, cy + i * lh), l, font=f, fill=b.NAVY, anchor="mm")
        if r.get("pegadinha"):
            ft = b.font(b.F_BLACK, 34)
            tw = d.textlength("PEGADINHA!", font=ft)
            px = 60 + tw / 2 + 24
            d.rounded_rectangle([60, 56, px + tw / 2 + 24, 120], 32, fill=b.RED, outline=b.WHITE, width=6)
            d.text((px, 88), "PEGADINHA!", font=ft, fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
        _cache[key] = cv
    return _cache[key]


def faixa_sprite(r, revelado):
    key = ("f", r["n"], revelado)
    if key not in _cache:
        x0, y0, x1, y1 = FAIXA
        w, h = x1 - x0, y1 - y0
        cv = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
        d = ImageDraw.Draw(cv)
        d.rounded_rectangle([26, 30, 26 + w, 30 + h], 55, fill=(0, 0, 0, 90))
        if revelado:
            d.rounded_rectangle([20, 20, 20 + w, 20 + h], 55, fill=b.YELLOW, outline=b.WHITE, width=8)
            f = bn.fit(d, r["resposta"], 88, w - 80)
            d.text((20 + w / 2, 20 + h / 2 - 4), r["resposta"], font=f, fill=b.NAVY, anchor="mm", stroke_width=2,
                   stroke_fill=b.NAVY)
        else:
            d.rounded_rectangle([20, 20, 20 + w, 20 + h], 55, fill=b.NAVY, outline=b.WHITE, width=7)
            d.text((20 + w / 2, 20 + h / 2 - 4), "? ? ?", font=b.font(b.F_BLACK, 86), fill=b.WHITE, anchor="mm")
        _cache[key] = cv
    return _cache[key]


def topo(img, k):
    d = ImageDraw.Draw(img)
    s.pilula(d, 540, 205, "NÃO DIGA O MESMO QUE O PALITO 2", (20, 40, 110), size=42, pad=34, h=88)
    d.text((540, 272), f"RODADA {k}/{N}", font=b.font(b.F_BLACK, 40), fill=b.WHITE, anchor="mm",
           stroke_width=4, stroke_fill=b.NAVY)
    bn.coracoes(img, 540, 337, VIDAS, 44, 14)


def base(k):
    key = ("b", k)
    if key not in _cache:
        img = s.fundo(*CORES[(k - 1) % len(CORES)], seed=k).convert("RGBA")
        topo(img, k)
        _cache[key] = img
    return _cache[key].copy()


def colar(img, spr, cx, cy, sc):
    if sc <= 0.02:
        return
    w, h = max(1, int(spr.width * sc)), max(1, int(spr.height * sc))
    im = spr if abs(sc - 1) < 1e-3 else spr.resize((w, h), Image.BILINEAR)
    img.alpha_composite(im, (int(cx - w / 2), int(cy - h / 2)))


def zoom(img, z):
    if abs(z - 1) < 1e-3:
        return img
    w, h = img.size
    cw, ch = w / z, h / z
    x0, y0 = (w - cw) / 2, (h - ch) / 2
    return img.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))


def pula(x):
    x = min(max(x, 0.0), 1.0)
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def barra(img, frac):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = BAR
    d.rounded_rectangle([x0 - 7, y0 - 7, x1 + 7, y1 + 7], 30, fill=b.WHITE)
    d.rounded_rectangle(BAR, 23, fill=(60, 70, 110))
    if frac > 0.002:
        d.rounded_rectangle([x0, y0, max(x0 + (x1 - x0) * frac, x0 + 46), y1], 23, fill=b.ORANGE if frac > 0.3 else b.RED)
    n = math.ceil(frac * COUNT)
    if n > 0:
        d.text(((x0 + x1) // 2, (y0 + y1) // 2), str(n), font=b.font(b.F_BLACK, 38), fill=b.WHITE, anchor="mm",
               stroke_width=4, stroke_fill=b.NAVY)


CCX, CCY = (CARD[0] + CARD[2]) // 2, (CARD[1] + CARD[3]) // 2
FCX, FCY = (FAIXA[0] + FAIXA[2]) // 2, (FAIXA[1] + FAIXA[3]) // 2


def pergunta_frames(k, r, fala):
    total = fala + COUNT
    for n in range(int(total * FPS)):
        t = n / FPS
        frac = 1.0 if t < fala else 1 - (t - fala) / COUNT
        img = base(k)
        te = t + (1.0 if k == 1 else 0.0)   # 1ª rodada já inteira no 1º quadro (sem abertura)
        colar(img, cartao_sprite(k, r, False), CCX, CCY + 5 * math.sin(t * 2.2), pula(te / 0.4))
        dx = 4 * math.sin(t * 40) if frac < 0.3 else 0
        colar(img, faixa_sprite(r, False), FCX + dx, FCY + 4 * math.sin(t * 3), pula((te - 0.25) / 0.35))
        barra(img, frac)
        pose = "pensando" if frac > 0.3 else "assustado"
        ent = pula((te - 0.4) / 0.4)
        b.put_palito(img, pose, 270, 540, 1575 + int((1 - ent) * 400),
                     int(6 * math.sin(t * (5 if pose == "pensando" else 16))))
        if k == 1:  # chamada por cima da 1ª rodada enquanto o gancho é falado
            eg.faixa_gancho(img, 540, 640, CHAMADA + "\nVALENDO!", t, max(2.5, fala - 1.0), larg=860, size=66)
        yield zoom(img, 1.0 + 0.03 * t / total).convert("RGB")


def resposta_frames(k, r, dur):
    for n in range(int(dur * FPS)):
        t = n / FPS
        img = base(k)
        colar(img, cartao_sprite(k, r, True), CCX, CCY, 1.0 + 0.04 * math.sin(min(t / 0.35, 1) * math.pi))
        colar(img, faixa_sprite(r, True), FCX, FCY, pula(t / 0.3) * 1.0 + 0.0)
        if t > 0.3:
            d = ImageDraw.Draw(img)
            sc = pula((t - 0.3) / 0.3)
            if sc > 0.3:
                s.pilula(d, 540, 1238, "PENSOU IGUAL? -1 VIDA!", b.RED, size=int(44 * min(sc, 1.1)), pad=34)
        if t < 0.2:
            img.alpha_composite(Image.new("RGBA", img.size, (255, 255, 255, int(150 * (1 - t / 0.2)))))
        b.put_palito(img, "comemorando", 270, 540, 1575, -int(abs(24 * math.sin(t * 7))))
        yield zoom(img, 1.03 + 0.02 * t / dur).convert("RGB")


def final_base():
    img = s.fundo(*CORES[0], seed=3).convert("RGBA")
    d = ImageDraw.Draw(img)
    s.texto(d, (540, 330), "COM QUANTAS VIDAS", 90, b.WHITE)
    s.texto(d, (540, 460), "VOCÊ TERMINOU?", 104, b.YELLOW)
    d.rounded_rectangle([170, 590, 910, 730], 50, fill=b.RED, outline=b.WHITE, width=8)
    s.texto(d, (540, 660), "COMENTA AÍ!", 84, b.WHITE)
    s.texto(d, (540, 860), "JOGO COMPLETO NO CANAL:", 58, b.WHITE, max_w=900)
    b.selo(img, 540, 980, 1.3)
    b.put_palito(img, "apontando", 380, 540, 1520)
    return img


def final_frames(dur):
    bs = final_base()
    for n in range(int(dur * FPS)):
        yield zoom(bs, 1.0 + 0.05 * n / FPS / dur).convert("RGB")


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = list(pergunta_frames(1, RODADAS[0], 2.0))
    ims = [fr[0], fr[30], fr[100], list(resposta_frames(1, RODADAS[0], 1.2))[-1],
           list(pergunta_frames(4, RODADAS[3], 1.0))[50], list(resposta_frames(5, RODADAS[4], 1.2))[-1],
           list(final_frames(1.0))[10]]
    sheet = Image.new("RGB", (len(ims) * 370, 640), (25, 25, 25))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((360, 640)), (i * 370, 0))
    sheet.save(os.path.join(out, "prancha.jpg"), quality=85)
    print(out)


def main():
    vozes()
    tmp = tempfile.mkdtemp(prefix="short_naodiga2_")
    sfx = b.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = s.Timeline(video)
    ultimo = None   # sem abertura: a 1ª imagem já é a rodada 1 (NOVO RITMO, 2026-11-17)
    for k, r in enumerate(RODADAS, 1):
        q = A(f"q{k}.mp3")
        fala = s.duracao(q) + 0.2
        if ultimo is None:
            tl.sound(sfx["whoosh"], vol=0.6)
        else:   # transição SPLASH entre as rodadas (motion graphics, 2026-11-21)
            s.transicao(tl, sfx, ultimo, next(pergunta_frames(k, r, fala)), n=k, total=N)
        tl.sound(q, at=tl.t + 0.1, voz=True)
        for n in range(int(COUNT)):
            tl.sound(sfx["tick"], at=tl.t + fala + n, vol=0.8)
        for f in pergunta_frames(k, r, fala):
            tl.frame(f)
        a = A(f"a{k}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(a, at=tl.t + 0.15, voz=True)
        for f in resposta_frames(k, r, s.duracao(a) + 0.5):
            tl.frame(f)
            ultimo = f
    tl.sound(sfx["whoosh"])
    tl.sound(A("final.mp3"), at=tl.t + 0.2, voz=True)
    for f in final_frames(s.duracao(A("final.mp3")) + 0.7):
        tl.frame(f)
    tl.close()
    s.mixar(tl, video, MUSICA, SAIDA)
    print(f"OK {SAIDA} ({tl.t:.1f}s)")


if __name__ == "__main__":
    previa() if "--previa" in sys.argv else main()
