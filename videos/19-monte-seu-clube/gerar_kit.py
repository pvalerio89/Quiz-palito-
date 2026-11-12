"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
"""
import importlib.util, json, os, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_clube as bd
from build_clube import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = "MONTE O SEU CLUBE ⚽ Escolha Estádio, Técnico, Craques e Lendas! Qual é o Seu Time? | Quiz Palito"


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    spec = importlib.util.spec_from_file_location("kit05", os.path.join(bd.VIDEOS, "05-nao-diga-o-mesmo", "gerar_kit.py"))
    k5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k5)
    img = nd.burst((40, 200, 90), (10, 110, 60), 4).convert("RGBA")
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([380, 180, 1340, 1000], fill=150)
    img = Image.composite(Image.new("RGBA", (W, H), (220, 255, 220, 255)), img, glow.filter(ImageFilter.GaussianBlur(160)))
    vg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vg).ellipse([-350, -300, W + 350, H + 300], fill=255)
    img = Image.composite(img, Image.new("RGBA", (W, H), (5, 60, 30, 255)), vg.filter(ImageFilter.GaussianBlur(140)))
    # fotos gigantes recortadas (adesivo)
    from PIL import ImageOps
    for arq, sz, x, y, rot in [("dez-messi.jpg", 330, 230, 690, 10), ("ca-cristiano-ronaldo.jpg", 310, 560, 660, -8),
                               ("pe-vinicius-jr.jpg", 300, 890, 700, 8)]:
        e = ImageOps.fit(Image.open(os.path.join(HERE, "fotos", arq)).convert("RGBA"), (sz, sz))
        m = Image.new("L", (sz, sz), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, sz - 1, sz - 1], 40, fill=255)
        e.putalpha(m)
        e = k5.adesivo(e, 14).rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, e, x, y)
    bal = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(bal)
    d.ellipse([0, 0, 290, 290], fill=b.YELLOW, outline=(20, 20, 40), width=12)
    d.text((145, 135), "?", font=b.font(b.F_BLACK, 230), fill=(20, 20, 40), anchor="mm")
    bal = k5.adesivo(bal, 14).rotate(-12, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(bal, (1040, 300))
    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 120), "MONTE O SEU", nd.fit(d, "MONTE O SEU", 170, 1180), b.WHITE, outline=(15, 15, 30), w=18, anchor="lm")
    b.text_outline(d, (50, 300), "CLUBE!", nd.fit(d, "CLUBE!", 200, 1180), b.YELLOW, outline=(15, 15, 30), w=20, anchor="lm")
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
        "0:00 O clube: cidade, camisa, escudo, estádio, mascote e técnico",
        f"{mmss(t['gol'])} Time titular: do goleiro ao centroavante",
        f"{mmss(t['joia'])} Banco: joia da base e lendas",
        f"{mmss(t['final'])} Comenta o seu time!",
    ])
    desc = f"""MONTE O SEU CLUBE! ⚽ Não tem resposta certa: em cada etapa aparecem 6 opções com foto e você escolhe a sua. Cidade, cor da camisa, escudo, estádio (Maracanã, Camp Nou, Bernabéu...), mascote, técnico, os 11 titulares (Messi, Cristiano Ronaldo, Vinícius Jr., Mbappé, Haaland...) e um banco cheio de lendas (Pelé, Ronaldo, Zidane, Ronaldinho...). Anota o número de cada escolha!

👇 Comenta os números que você escolheu e o nome do seu clube!
👥 Chama os amigos pra ver quem monta o melhor time!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Wallpaper" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#futebol #monteseutime #montesuaequipe #quiz #quizpalito
"""
    tags = ["monte seu time", "monte o seu clube", "escolha seu time", "monte seu time dos sonhos", "futebol",
            "messi", "cristiano ronaldo", "neymar", "vinicius jr", "lendas do futebol", "quiz de futebol",
            "quiz palito", "quiz em português", "desafio de futebol"]
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
