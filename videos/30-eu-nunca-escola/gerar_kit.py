"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
Miniatura principal: gerada no Google Flow com youtube/prompt-flow.txt; esta é a reserva.
"""
import importlib.util, json, os, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_escola as bd
from build_escola import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = f"VOCÊ JÁ FEZ ISSO NA ESCOLA? 🏫 EU JÁ ou EU NUNCA? {bd.TOTAL} Frases e NÃO VALE MENTIR! | Quiz Palito"


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    spec = importlib.util.spec_from_file_location("kit05", os.path.join(bd.VIDEOS, "05-nao-diga-o-mesmo", "gerar_kit.py"))
    k5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k5)
    img = nd.burst((30, 160, 90), (10, 80, 50), 4).convert("RGBA")
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([380, 180, 1340, 1000], fill=150)
    img = Image.composite(Image.new("RGBA", (W, H), (225, 255, 230, 255)), img, glow.filter(ImageFilter.GaussianBlur(160)))
    for ch, sz, x, y, rot in [("🎒", 300, 230, 660, 8), ("✅", 250, 600, 610, -6), ("❌", 250, 860, 720, 10)]:
        e = k5.adesivo(nd.emoji(ch, sz), 14).rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, e, x, y)
    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 120), "VOCÊ JÁ FEZ ISSO", nd.fit(d, "VOCÊ JÁ FEZ ISSO", 170, 1180), b.WHITE, outline=(15, 15, 30), w=18, anchor="lm")
    b.text_outline(d, (50, 310), "NA ESCOLA?", nd.fit(d, "NA ESCOLA?", 200, 1180), b.YELLOW, outline=(15, 15, 30), w=20, anchor="lm")
    b.put_palito(img, "assustado", 1080, 1610, 1200)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=(225, 20, 120))
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "VOCÊ CONSEGUE?", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    nomes = {"1": "As que todo mundo já fez", "11": "Do dia a dia", "21": "Ficou dividido", "31": "Menos comuns",
             "41": "As mais raras"}
    linhas = [f"{mmss(t[k])} {v}" for k, v in nomes.items()]
    linhas[0] = "0:00" + linhas[0][linhas[0].index(" "):]   # o YouTube exige o 1º capítulo em 0:00
    linhas.append(f"{mmss(t['final'])} Quantos \"eu já\" você tem?")
    caps = "\n".join(linhas)
    desc = f"""Você já fez isso NA ESCOLA? 🏫 EU JÁ ou EU NUNCA? São {bd.TOTAL} frases de escola: para cada uma, escolha um botão (e não vale mentir!). Depois aparece quantas pessoas já fizeram aquilo. Começa com as que todo aluno já fez e termina com as mais raras!

✍️ Vai anotando quantos "eu já" você tem e manda nos comentários!
👥 Joga com os amigos da sala e vê quem já fez mais coisa!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Carefree" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#eujaeununca #escola #quiz #escolhaumbotao #quizpalito
"""
    tags = ["eu já ou eu nunca", "eu nunca na escola", "você já fez isso na escola", "escola", "escolha um botão", "não vale mentir", "quiz", "quiz palito",
            "quiz em português", "brincadeira", "desafio", "quiz para jogar com amigos", "quiz divertido"]
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
