"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_estados as be
from build_estados import b, nd, bb, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = "QUE ESTADO É ESSE? 🗺️ Acerte os 27 Estados do Brasil Pelo Mapa! | Quiz Palito"
LIMA = (170, 255, 40)


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    import importlib.util
    spec = importlib.util.spec_from_file_location("kit05", os.path.join(bb.VIDEOS, "05-nao-diga-o-mesmo", "gerar_kit.py"))
    k5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k5)
    # fundo colorido: raios verde e amarelo com brilho no centro
    img = nd.burst((0, 175, 75), (20, 95, 215), 4).convert("RGBA")
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([380, 180, 1340, 1000], fill=150)
    img = Image.composite(Image.new("RGBA", (W, H), (120, 230, 255, 255)), img, glow.filter(ImageFilter.GaussianBlur(160)))
    vg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vg).ellipse([-350, -300, W + 350, H + 300], fill=255)
    img = Image.composite(img, Image.new("RGBA", (W, H), (0, 60, 140, 255)), vg.filter(ImageFilter.GaussianBlur(140)))

    # mapa gigante recortado, um estado em laranja
    mp = be.mapa("MG", be.LARANJA, 780, 780)
    mp = k5.adesivo(mp.crop(mp.getbbox()), 16)
    img.alpha_composite(mp, (330, 330))

    # balão "?" em cima do estado
    bal = Image.new("RGBA", (330, 330), (0, 0, 0, 0))
    d = ImageDraw.Draw(bal)
    d.ellipse([0, 0, 320, 320], fill=b.YELLOW, outline=(20, 20, 40), width=12)
    d.text((160, 150), "?", font=b.font(b.F_BLACK, 250), fill=(20, 20, 40), anchor="mm")
    bal = k5.adesivo(bal, 14).rotate(-12, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(bal, (40, 520))

    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 125), "QUE ESTADO", nd.fit(d, "QUE ESTADO", 190, 1180), b.WHITE, outline=(15, 15, 30), w=20, anchor="lm")
    b.text_outline(d, (50, 320), "É ESSE?", nd.fit(d, "É ESSE?", 240, 1180), b.YELLOW, outline=(15, 15, 30), w=22, anchor="lm")

    b.put_palito(img, "assustado", 1080, 1610, 1200)

    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=(225, 20, 120))
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "VOCÊ CONSEGUE?", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    caps = "\n".join([
        "0:00 Abertura",
        f"{mmss(t['1'])} Perguntas 1 a 10",
        f"{mmss(t['11'])} Perguntas 11 a 20",
        f"{mmss(t['21'])} Perguntas 21 a 30",
        f"{mmss(t['final'])} Quantos você acertou?",
    ])
    caps = caps.replace("Perguntas 21 a 30", "Estados 21 a 27").replace("Perguntas", "Estados")
    desc = f"""Você consegue reconhecer os 27 estados do Brasil só pelo mapa? 🗺️ Um estado aparece pintado de laranja, você tem 4 alternativas e 6 segundos para responder. E na resposta tem a capital de cada um! Ótimo para estudar geografia para a prova. 📚

👇 Comenta quantos você acertou e de qual estado você é!
👥 Manda pro seu amigo da escola e vê quem sabe mais!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo toda semana!

⏱️ Capítulos
{caps}

🎵 Música: "Sneaky Snitch" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #geografia #estadosdobrasil #quizpalito
"""
    tags = ["estados do brasil", "quiz de geografia", "mapa do brasil", "capitais do brasil", "quiz estados",
            "geografia do brasil", "quiz palito", "quiz em português", "estudar geografia", "quiz escolar",
            "regiões do brasil", "teste seus conhecimentos", "quiz com alternativas", "que estado é esse"]
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
