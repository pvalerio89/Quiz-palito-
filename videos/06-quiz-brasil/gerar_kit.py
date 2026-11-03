"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_brasil as bb
from build_brasil import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = "QUIZ DO BRASIL 🇧🇷 30 Perguntas Que Todo Brasileiro Deveria Acertar! | Quiz Palito"
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

    # figurinhas coloridas em volta
    for ch, sz, x, y, rot in [("🦜", 230, 130, 480, 10), ("⚽", 200, 1190, 880, -14)]:
        e = Image.new("RGBA", (sz + 40, sz + 40), (0, 0, 0, 0))
        nd.paste_c(e, nd.emoji(ch, sz), (sz + 40) / 2, (sz + 40) / 2)
        e = k5.adesivo(e.crop(e.getbbox()), 12).rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, e, x, y)

    # bandeira gigante recortada (colorida sobre o P&B)
    fl = Image.new("RGBA", (900, 900), (0, 0, 0, 0))
    bb.bandeira(fl, 450, 450, 560)
    fl = k5.adesivo(fl.crop(fl.getbbox()), 16)
    img.alpha_composite(fl, (470, 440))

    # balão "?" (fica atrás do 🎵)
    bal = Image.new("RGBA", (330, 330), (0, 0, 0, 0))
    d = ImageDraw.Draw(bal)
    d.ellipse([0, 0, 320, 320], fill=b.YELLOW, outline=(20, 20, 40), width=12)
    d.text((160, 150), "?", font=b.font(b.F_BLACK, 250), fill=(20, 20, 40), anchor="mm")
    bal = k5.adesivo(bal, 14).rotate(-12, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(bal, (40, 560))

    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 125), "VOCÊ SABE TUDO", nd.fit(d, "VOCÊ SABE TUDO", 170, 1180), b.WHITE, outline=(15, 15, 30), w=20, anchor="lm")
    b.text_outline(d, (50, 320), "DO BRASIL?", nd.fit(d, "DO BRASIL?", 230, 1180), b.YELLOW, outline=(15, 15, 30), w=22, anchor="lm")

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
        f"{mmss(t['final'])} Quantas você acertou?",
    ])
    desc = f"""Você conhece MESMO o Brasil? 🇧🇷 Bandeira, hino, estados, capitais, comidas típicas, história… São 30 perguntas com 4 alternativas e só 6 segundos para responder cada uma! ⏱️

👇 Comenta quantas você acertou e de qual cidade você é!
👥 Chama a família e os amigos pra ver quem sabe mais!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo toda semana!

⏱️ Capítulos
{caps}

🎵 Música: "Carefree" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #quizdobrasil #quizpalito #conhecimentosgerais
"""
    tags = ["quiz do brasil", "quiz brasil", "perguntas sobre o brasil", "conhecimentos gerais", "quiz",
            "quiz palito", "quiz em português", "perguntas e respostas", "quiz de geografia", "estados do brasil",
            "capitais do brasil", "quiz brasileiro", "teste seus conhecimentos", "quiz com alternativas"]
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
