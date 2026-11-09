"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_frutas as bb
from build_frutas import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = f"ADIVINHE A FRUTA PELA FOTO EM 3 SEGUNDOS! 🍓 {bb.TOTAL} Frutas, Legumes e Verduras | Quiz Palito"
LIMA = (170, 255, 40)


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    import importlib.util
    spec = importlib.util.spec_from_file_location("kit05", os.path.join(bb.VIDEOS, "05-nao-diga-o-mesmo", "gerar_kit.py"))
    k5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k5)
    # fundo colorido: raios laranja e roxo com brilho no centro
    img = nd.burst((40, 200, 90), (255, 200, 0), 4).convert("RGBA")
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([380, 180, 1340, 1000], fill=150)
    img = Image.composite(Image.new("RGBA", (W, H), (255, 255, 190, 255)), img, glow.filter(ImageFilter.GaussianBlur(160)))
    vg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vg).ellipse([-350, -300, W + 350, H + 300], fill=255)
    img = Image.composite(img, Image.new("RGBA", (W, H), (0, 110, 60, 255)), vg.filter(ImageFilter.GaussianBlur(140)))

    # fotos reais gigantes (cartão branco inclinado)
    for nome, sz, x, y, rot in [("Melancia", 470, 330, 690, 8), ("Morango", 400, 790, 730, -9), ("Kiwi", 300, 1180, 600, 12)]:
        r = next(r for r in bb.R if r["nome"] == nome)
        c = Image.new("RGBA", (sz + 36, sz + 36), (0, 0, 0, 0))
        ImageDraw.Draw(c).rounded_rectangle([0, 0, sz + 35, sz + 35], 40, fill=b.WHITE, outline=(15, 15, 30), width=8)
        c.alpha_composite(bb.foto(r["foto"], sz), (18, 18))
        c = c.rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, c, x, y)

    # balão "?" (fica atrás do 🎵)
    bal = Image.new("RGBA", (330, 330), (0, 0, 0, 0))
    d = ImageDraw.Draw(bal)
    d.ellipse([0, 0, 320, 320], fill=b.YELLOW, outline=(20, 20, 40), width=12)
    d.text((160, 150), "?", font=b.font(b.F_BLACK, 250), fill=(20, 20, 40), anchor="mm")
    bal = k5.adesivo(bal, 14).rotate(-12, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(bal, (1000, 760))

    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 125), "QUE FRUTA É?", nd.fit(d, "QUE FRUTA É?", 200, 1180), b.WHITE, outline=(15, 15, 30), w=20, anchor="lm")
    b.text_outline(d, (50, 320), "SÓ 3 SEGUNDOS!", nd.fit(d, "SÓ 3 SEGUNDOS!", 230, 1180), b.YELLOW, outline=(15, 15, 30), w=22, anchor="lm")

    b.put_palito(img, "assustado", 1080, 1610, 1200)

    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=(225, 20, 120))
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "VOCÊ CONSEGUE?", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    nivel = ["fácil", "fácil", "médio", "médio", "difícil", "difícil", "muito difícil", "muito difícil", "nível mestre"]
    linhas = ["0:00 Abertura"]
    for k, ini in enumerate(range(1, bb.TOTAL + 1, 10)):
        fim = min(ini + 9, bb.TOTAL)
        linhas.append(f"{mmss(t[str(ini)])} {ini} a {fim} ({nivel[min(k, len(nivel) - 1)]})")
    linhas.append(f"{mmss(t['final'])} Quantas você acertou?")
    caps = "\n".join(linhas)
    desc = f"""Você consegue adivinhar a fruta, o legume ou a verdura pela FOTO em só 3 segundos? 🍓🥕🥦 São {bb.TOTAL} fotos de verdade, do mais fácil ao mais difícil, com frutas brasileiras como jabuticaba, caju e cupuaçu! ⏱️

👇 Comenta quantas você acertou!
👥 Chama a família e os amigos pra ver quem é mais rápido!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Fluffing a Duck" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #adivinheafruta #quizpalito #frutas #legumes
"""
    tags = ["adivinhe a fruta", "quiz de frutas", "frutas e legumes", "adivinhe em 3 segundos", "quiz", "quiz palito",
            "quiz em português", "quiz de verduras", "desafio de frutas", "quiz de alimentos", "frutas brasileiras",
            "adivinhe o legume", "quiz escolar", "adivinhe pela foto"]
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
