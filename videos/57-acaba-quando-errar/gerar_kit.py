"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
Miniatura principal: o Patrick gera no Google Flow com youtube/prompt-flow.txt; esta é a reserva.
"""
import importlib.util, json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_acaba as bd
from build_acaba import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = "O vídeo ACABA quando você ERRAR a bandeira 🚩 36 bandeiras: até onde você chega? | Quiz Palito"


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    spec = importlib.util.spec_from_file_location("kit05", os.path.join(bd.VIDEOS, "05-nao-diga-o-mesmo", "gerar_kit.py"))
    k5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k5)
    img = nd.burst((30, 90, 210), (10, 35, 120), 4).convert("RGBA")
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([380, 180, 1340, 1000], fill=150)
    img = Image.composite(Image.new("RGBA", (W, H), (220, 235, 255, 255)), img, glow.filter(ImageFilter.GaussianBlur(160)))
    vg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vg).ellipse([-350, -300, W + 350, H + 300], fill=255)
    img = Image.composite(img, Image.new("RGBA", (W, H), (5, 25, 80, 255)), vg.filter(ImageFilter.GaussianBlur(140)))
    for arq, sz, x, y, rot in [("br", 300, 200, 650, 8), ("is", 240, 540, 700, -6), ("ml", 300, 880, 650, 5)]:
        e = Image.open(os.path.join(bd.BANDEIRAS, arq + ".png")).convert("RGBA")
        e.thumbnail((sz, sz), Image.LANCZOS)
        e = k5.adesivo(e, 12).rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, e, x, y)
    bal = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(bal)
    d.ellipse([0, 0, 290, 290], fill=b.YELLOW, outline=(20, 20, 40), width=12)
    d.text((145, 135), "?", font=b.font(b.F_BLACK, 230), fill=(20, 20, 40), anchor="mm")
    bal = k5.adesivo(bal, 14).rotate(-12, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(bal, (900, 330))
    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 120), "ERROU UMA?", nd.fit(d, "ERROU UMA?", 190, 1180), b.WHITE, outline=(15, 15, 30), w=18, anchor="lm")
    b.text_outline(d, (50, 310), "ACABOU!", nd.fit(d, "ACABOU!", 230, 1180), b.YELLOW, outline=(15, 15, 30), w=20, anchor="lm")
    b.put_palito(img, "apontando", 1080, 1610, 1200)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=(0, 150, 70))
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "VOCÊ CONSEGUE?", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    nomes = {"1": "Começo (aquecimento)", "10": "Sequência de 9: agora complica", "19": "Sequência de 18: as parecidas",
             "28": "Sequência de 27: a parte mais cruel", "final": "Até onde você chegou?"}
    linhas = [f"{mmss(t[k])} {v}" for k, v in nomes.items()]
    linhas[0] = "0:00" + linhas[0][linhas[0].index(" "):]   # o YouTube exige o 1º capítulo em 0:00
    caps = "\n".join(linhas)
    desc = f"""O vídeo ACABA quando você ERRAR a bandeira 🚩 São {bd.TOTAL} bandeiras, cada vez mais difíceis: aparece a bandeira, você tem 7 segundos para escolher entre 3 alternativas e, no primeiro erro, acabou o jogo pra você. No começo é aquecimento, depois vêm as bandeiras parecidas (Polônia x Indonésia, Islândia x Noruega, Romênia x Chade...). Até qual bandeira você chega sem errar?

👇 Comenta até onde você chegou!
👥 Chama a família pra jogar junto, dá pra ver na TV!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Fluffing a Duck" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #bandeiras #quizdebandeiras #geografia #quizpalito
"""
    tags = ["quiz de bandeiras", "adivinhe a bandeira", "bandeiras do mundo", "bandeiras parecidas",
            "quiz de geografia", "geografia", "países do mundo", "o vídeo acaba quando você errar", "quiz sobrevivência", "quiz",
            "quiz palito", "quiz em português", "quiz em família"]
    open(os.path.join(OUT, "titulo.txt"), "w", encoding="utf-8").write(TITULO + "\n")
    open(os.path.join(OUT, "descricao.txt"), "w", encoding="utf-8").write(desc)
    open(os.path.join(OUT, "tags.txt"), "w", encoding="utf-8").write(", ".join(tags) + "\n")
    print(caps)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    thumb()
    if "--thumb" not in sys.argv:
        textos()
    print(OUT)
