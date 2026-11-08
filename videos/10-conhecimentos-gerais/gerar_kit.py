"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_gerais as bb
from build_gerais import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = "50 PERGUNTAS DE CONHECIMENTOS GERAIS 🧠 Do Fácil ao Difícil! Você Consegue? | Quiz Palito"
LIMA = (170, 255, 40)


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    import importlib.util
    spec = importlib.util.spec_from_file_location("kit05", os.path.join(bb.VIDEOS, "05-nao-diga-o-mesmo", "gerar_kit.py"))
    k5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k5)
    # fundo colorido: raios laranja e roxo com brilho no centro
    img = nd.burst((255, 150, 0), (150, 40, 200), 4).convert("RGBA")
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([380, 180, 1340, 1000], fill=150)
    img = Image.composite(Image.new("RGBA", (W, H), (255, 230, 120, 255)), img, glow.filter(ImageFilter.GaussianBlur(160)))
    vg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vg).ellipse([-350, -300, W + 350, H + 300], fill=255)
    img = Image.composite(img, Image.new("RGBA", (W, H), (90, 20, 120, 255)), vg.filter(ImageFilter.GaussianBlur(140)))

    # figurinhas coloridas em volta
    for ch, sz, x, y, rot in [("🪐", 230, 1180, 560, 12), ("🔬", 200, 1230, 860, -14)]:
        e = Image.new("RGBA", (sz + 40, sz + 40), (0, 0, 0, 0))
        nd.paste_c(e, nd.emoji(ch, sz), (sz + 40) / 2, (sz + 40) / 2)
        e = k5.adesivo(e.crop(e.getbbox()), 12).rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, e, x, y)

    # cérebro gigante recortado no meio
    e = Image.new("RGBA", (560, 560), (0, 0, 0, 0))
    nd.paste_c(e, nd.emoji("🧠", 500), 280, 280)
    e = k5.adesivo(e.crop(e.getbbox()), 18).rotate(-6, expand=True, resample=Image.BICUBIC)
    nd.paste_c(img, e, 760, 650)


    # balão "?" (fica atrás do 🎵)
    bal = Image.new("RGBA", (330, 330), (0, 0, 0, 0))
    d = ImageDraw.Draw(bal)
    d.ellipse([0, 0, 320, 320], fill=b.YELLOW, outline=(20, 20, 40), width=12)
    d.text((160, 150), "?", font=b.font(b.F_BLACK, 250), fill=(20, 20, 40), anchor="mm")
    bal = k5.adesivo(bal, 14).rotate(-12, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(bal, (40, 560))

    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 125), "SÓ GÊNIOS", nd.fit(d, "SÓ GÊNIOS", 200, 1180), b.WHITE, outline=(15, 15, 30), w=20, anchor="lm")
    b.text_outline(d, (50, 320), "ACERTAM 50!", nd.fit(d, "ACERTAM 50!", 230, 1180), b.YELLOW, outline=(15, 15, 30), w=22, anchor="lm")

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
        f"{mmss(t['1'])} Perguntas 1 a 10 (nível fácil)",
        f"{mmss(t['11'])} Perguntas 11 a 20",
        f"{mmss(t['21'])} Perguntas 21 a 30 (nível médio)",
        f"{mmss(t['31'])} Perguntas 31 a 40",
        f"{mmss(t['41'])} Perguntas 41 a 50 (nível difícil)",
        f"{mmss(t['final'])} Quantas você acertou?",
    ])
    desc = f"""Teste seus conhecimentos gerais! 🧠 Planetas, animais, corpo humano, geografia, história e ciências: são 50 perguntas em 3 níveis (fácil, médio e difícil), com 4 alternativas e só 6 segundos para responder cada uma! ⏱️

👇 Comenta quantas você acertou!
👥 Chama a família e os amigos pra ver quem sabe mais!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Wallpaper" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #conhecimentosgerais #quizpalito #perguntaserespostas
"""
    tags = ["conhecimentos gerais", "quiz de conhecimentos gerais", "50 perguntas", "perguntas e respostas", "quiz",
            "quiz palito", "quiz em português", "quiz escolar", "teste seus conhecimentos", "quiz com alternativas",
            "quiz fácil médio difícil", "perguntas de ciências", "quiz de geografia", "desafio de perguntas"]
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
