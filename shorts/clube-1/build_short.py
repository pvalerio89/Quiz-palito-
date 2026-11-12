"""Short "Monte o seu time em 6 escolhas" (clube-1), do vídeo 19 (Monte o seu clube).

Sem resposta certa: 6 etapas (estádio, técnico, goleiro, camisa 10, ponta e centroavante), 4 opções numeradas com
foto real em cada, contagem de 5 s "ESCOLHA O SEU!" e no fim "COMENTA SEU TIME!". Fotos e créditos do vídeo 19.
Intro rapidinha + chamada na faixa da 1ª etapa (padrão dos Shorts, 2026-11-10).
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
V19 = os.path.join(QP, "videos", "19-monte-seu-clube")
sys.path.insert(0, V19)
import build_clube as bc
eg = bc.eg

A = lambda n: os.path.join(HERE, "assets", n)
SAIDA = os.path.join(HERE, "short-clube-1.mp4")
CHAMADA = "QUAL É O SEU TIME?"   # vídeo de escolha: chamada própria (sem "acertar")
MUSICA = os.path.join(QP, "musicas", "Wallpaper.mp3")
CONTA = 5.0
ETAPAS = ["estadio", "tecnico", "gol", "dez", "pe", "ca"]
E = [next(e for e in bc.E if e["chave"] == c) for c in ETAPAS]
for e in E:
    e["opcoes"] = e["opcoes"][:4]
FALA_E = {
    "estadio": "Monta o seu time em seis escolhas! Valendo! Primeiro, o estádio: Maracanã, Camp Nou, Bernabéu ou Old Trafford?",
    "tecnico": "O técnico: Guardiola, Ancelotti, Klopp ou Mourinho?",
    "gol": "O goleiro: Alisson, Ederson, Courtois ou Neuer?",
    "dez": "O camisa dez: Messi, Bruno Fernandes, Wirtz ou Mussiala?",
    "pe": "O ponta: Vinícius Júnior, Neymar, Kvaratskhélia ou Rafael Leão?",
    "ca": "E o centroavante: Haaland, Harry Kane, Mbappé ou Cristiano Ronaldo?",
}
FALAS = {"intro": "Monte o seu time!",
         "final": "Montou? Comenta os números que você escolheu! Segue o Quiz Palito! O vídeo completo, com vinte e quatro escolhas, tá no canal!",
         **{f"e{k}": FALA_E[c] for k, c in enumerate(ETAPAS)}}
REAC = ["Anotou?", "Escolheu?", "Boa!", "Anota aí!", "Difícil, né?", "Escolheu?"]
FALAS.update({f"r{k}": t for k, t in enumerate(REAC)})
GX, GY = (290, 790), (760, 1300)
LADO = 380
TIMER = (540, 1700)


def vozes():
    import edge_tts
    if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
        import ssl, edge_tts.communicate as _c
        _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    for k, txt in FALAS.items():
        if not os.path.exists(A(f"{k}.mp3")):
            asyncio.run(edge_tts.Communicate(txt, "pt-BR-AntonioNeural", rate="+20%", pitch="+2Hz").save(A(f"{k}.mp3")))
            print("voz", k, "-", txt, flush=True)


_cache = {}
CORES = [((30, 110, 210), (15, 40, 130)), ((20, 150, 80), (5, 70, 50)), ((150, 70, 200), (60, 25, 120)),
         ((0, 160, 170), (0, 70, 100)), ((235, 60, 50), (120, 15, 30)), ((255, 150, 0), (200, 60, 0))]


def base(k, e):
    key = ("base", k)
    if key not in _cache:
        img = s.fundo(*CORES[k], seed=k).convert("RGBA")
        d = ImageDraw.Draw(img)
        s.pilula(d, 600, 205, f"MONTE SEU TIME • {k + 1}/6", (40, 60, 150), size=46, pad=36, h=90)
        s.texto(d, (600, 330), e["titulo"], 92, b.YELLOW, max_w=820)
        _cache[key] = img
    return _cache[key].copy()


def grade(img, e, t, entrada=True):
    for i, o in enumerate(e["opcoes"]):
        sc = bc.op.pula((t - 0.25 - 0.22 * i) / 0.35) if entrada else 1.0
        bc.op.colar(img, bc.cartao(i, o, LADO, 70, 44), GX[i % 2], GY[i // 2] + 5 * math.sin(t * 2.6 + i), sc)


def etapa_frames(k, e, fala):
    tot = fala + CONTA
    for n in range(int(tot * FPS)):
        t = n / FPS
        frac = 1.0 if t < fala else 1 - (t - fala) / CONTA
        img = base(k, e)
        grade(img, e, t)
        bc.timer(img, frac, t, CONTA, TIMER, raio=100, legenda=False)
        s.texto(ImageDraw.Draw(img), (540, 1845), "ESCOLHA O SEU!", 60, b.YELLOW)
        pose = "pensando" if frac > 0.3 else "assustado"
        b.put_palito(img, pose, 240, 140, 300, int(6 * math.sin(t * (5 if pose == "pensando" else 16))))
        if k == 0:
            eg.faixa_gancho(img, 620, 240, CHAMADA + "\nVALENDO!", t, max(2.5, fala), larg=820, size=64)
        yield img.convert("RGB")


def reacao_frames(k, e, dur):
    for n in range(int(dur * FPS)):
        t = n / FPS
        img = base(k, e)
        grade(img, e, 10 + t, entrada=False)
        d = ImageDraw.Draw(img)
        sc = bc.op.pula(t / 0.35)
        x, y = TIMER
        d.rounded_rectangle([x - 330 * sc, y - 110 * sc, x + 330 * sc, y + 110 * sc], int(40 * sc) + 1, fill=b.RED,
                            outline=b.WHITE, width=8)
        f = b.font(b.F_BLACK, max(10, int(70 * sc)))
        d.text((x, y), "ANOTOU O Nº?", font=f, fill=b.WHITE, anchor="mm", stroke_width=3, stroke_fill=b.NAVY)
        b.put_palito(img, "comemorando", 240, 140, 300, int(6 * math.sin(t * 9)))
        yield img.convert("RGB")


def final_base():
    img = s.fundo(seed=3).convert("RGBA")
    d = ImageDraw.Draw(img)
    s.texto(d, (540, 330), "MONTOU?", 140, b.YELLOW)
    s.texto(d, (540, 470), "COMENTA SEU TIME!", 90, b.WHITE)
    d.rounded_rectangle([110, 560, 970, 690], 50, fill=b.RED, outline=b.WHITE, width=8)
    s.texto(d, (540, 625), "OS 6 NÚMEROS QUE VOCÊ ESCOLHEU", 50, b.WHITE, max_w=820)
    s.texto(d, (540, 800), "SEGUE O", 64, b.WHITE)
    b.selo(img, 540, 900, 1.3)
    b.put_palito(img, "apontando", 380, 540, 1460)
    cred = [c for c in bc.CRED["fotos"] if any(c.startswith(o["nome"] + ":") for e in E for o in e["opcoes"])]
    f = b.font(b.F_BOLD, 19)
    linhas, cur = [], "Fotos (Wikimedia Commons): "
    for parte in [c.split(", ")[0] for c in cred]:
        if d.textlength(cur + parte, font=f) > 1000:
            linhas.append(cur)
            cur = ""
        cur += parte + "  •  "
    linhas.append(cur.rstrip(" •"))
    for i, t in enumerate(linhas):
        d.text((540, 1520 + i * 26), t, font=f, fill=(235, 235, 245), anchor="mm")
    return img


def final_frames(dur):
    bs = final_base()
    for n in range(int(dur * FPS)):
        yield bs.convert("RGB")


def intro_frames(dur):
    ims = [Image.open(os.path.join(V19, "fotos", f)).convert("RGBA").resize((200, 200))
           for f in ["dez-messi.jpg", "ca-cristiano-ronaldo.jpg", "pe-vinicius-jr.jpg", "estadio-maracana.jpg"]]
    return s.intro_rapida("MONTE O SEU", "TIME!", dur, ims)


def previa():
    out = os.path.join(HERE, "previa")
    os.makedirs(out, exist_ok=True)
    fr = list(etapa_frames(0, E[0], 3.0))
    ims = [list(intro_frames(2.0))[40], fr[30], fr[110], list(reacao_frames(0, E[0], 1.0))[-1],
           list(etapa_frames(3, E[3], 1.0))[70], list(etapa_frames(5, E[5], 1.0))[40], list(final_frames(0.5))[5]]
    sheet = Image.new("RGB", (len(ims) * 370, 640), (25, 25, 25))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((360, 640)), (i * 370, 0))
    sheet.save(os.path.join(out, "prancha.jpg"), quality=85)
    print(out)


def main():
    vozes()
    tmp = tempfile.mkdtemp(prefix="short_clube_")
    sfx = bc.op.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = s.Timeline(video)
    tl.sound(A("intro.mp3"), at=0.1, voz=True)
    for f in intro_frames(s.duracao(A("intro.mp3"))):
        tl.frame(f)
    for k, e in enumerate(E):
        v = A(f"e{k}.mp3")
        tl.sound(sfx["whoosh"], vol=0.6)
        tl.sound(v, at=tl.t + 0.1, voz=True)
        fala = s.duracao(v) + 0.2
        for i in range(4):
            tl.sound(sfx["pop"], at=tl.t + 0.25 + 0.22 * i, vol=0.6)
        for n in range(int(CONTA)):
            tl.sound(sfx["tick"], at=tl.t + fala + n, vol=0.8)
        for f in etapa_frames(k, e, fala):
            tl.frame(f)
        r = A(f"r{k}.mp3")
        tl.sound(sfx["ding"], vol=0.8)
        tl.sound(r, at=tl.t + 0.15, voz=True)
        for f in reacao_frames(k, e, s.duracao(r) + 0.6):
            tl.frame(f)
    tl.sound(sfx["whoosh"])
    tl.sound(A("final.mp3"), at=tl.t + 0.2, voz=True)
    for f in final_frames(s.duracao(A("final.mp3")) + 0.7):
        tl.frame(f)
    tl.close()
    s.mixar(tl, video, MUSICA, SAIDA)
    print(f"OK {SAIDA} ({tl.t:.1f}s)")


if __name__ == "__main__":
    previa() if "--previa" in sys.argv else main()
