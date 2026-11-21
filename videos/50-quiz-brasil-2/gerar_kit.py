"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
Miniatura principal: o Patrick gera no Google Flow com youtube/prompt-flow.txt; esta é a reserva.
"""
import importlib.util, json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_brasil2 as bd
from build_brasil2 import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = "QUIZ DO BRASIL 2 🇧🇷 Se você acertar 25 de 32, é brasileiro de verdade! | Quiz Palito"


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
    for arq, sz, x, y, rot in [("fotos/cristo.jpg", 300, 200, 640, 8), ("fotos/capivara.jpg", 260, 540, 700, -6),
                               ("fotos/tucano.jpg", 300, 880, 640, 5)]:
        e = Image.open(os.path.join(HERE, arq)).convert("RGBA")
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
    b.text_outline(d, (50, 120), "QUIZ DO", nd.fit(d, "QUIZ DO", 190, 1180), b.WHITE, outline=(15, 15, 30), w=18, anchor="lm")
    b.text_outline(d, (50, 310), "BRASIL 2", nd.fit(d, "BRASIL 2", 230, 1180), b.YELLOW, outline=(15, 15, 30), w=20, anchor="lm")
    b.put_palito(img, "apontando", 1080, 1610, 1200)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=(0, 150, 70))
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "VOCÊ CONSEGUE?", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    nomes = {"1": "As fáceis", "11": "Lugares e história", "21": "Ficando difícil", "31": "As mais difíceis"}
    linhas = [f"{mmss(t[k])} {v}" for k, v in nomes.items()]
    linhas[0] = "0:00" + linhas[0][linhas[0].index(" "):]   # o YouTube exige o 1º capítulo em 0:00
    linhas.append(f"{mmss(t['final'])} Quantos você acertou?")
    caps = "\n".join(linhas)
    desc = f"""QUIZ DO BRASIL 2 🇧🇷 Você conhece mesmo o seu país? São {bd.TOTAL} perguntas NOVAS sobre o Brasil, com fotos reais: lugares, bichos, comidas, história e cultura. Aparece a foto, você tem 7 segundos para escolher entre 3 alternativas, e as últimas são as mais difíceis!

👇 Comenta quantas você acertou!
👥 Chama a família pra jogar junto, dá pra ver na TV!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Fluffing a Duck" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #brasil #quizdobrasil #conhecimentosgerais #quizpalito
"""
    tags = ["quiz do brasil", "quiz sobre o brasil", "perguntas sobre o brasil", "conhecimentos gerais",
            "geografia do brasil", "história do brasil", "quiz de conhecimentos gerais", "quiz",
            "quiz palito", "quiz em português", "você conhece o brasil", "quiz em família"]
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
