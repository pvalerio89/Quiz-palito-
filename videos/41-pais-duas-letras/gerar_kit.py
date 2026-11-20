"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
Miniatura principal: o Patrick gera no Google Flow com youtube/prompt-flow.txt; esta é a reserva.
"""
import importlib.util, json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_duas_letras as bd
from build_duas_letras import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = "Adivinhe o PAÍS só com as 2 PRIMEIRAS LETRAS! 🌎 As últimas são impossíveis | Quiz Palito"


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    spec = importlib.util.spec_from_file_location("kit05", os.path.join(bd.VIDEOS, "05-nao-diga-o-mesmo", "gerar_kit.py"))
    k5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k5)
    img = nd.burst((40, 120, 235), (15, 50, 160), 4).convert("RGBA")   # azul (melhor CTR do canal, 19/11)
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([380, 180, 1340, 1000], fill=110)
    img = Image.composite(Image.new("RGBA", (W, H), (120, 190, 255, 255)), img, glow.filter(ImageFilter.GaussianBlur(160)))
    bd.cartoes()
    for arq, sz, x, y, rot in [("cartoes/q1.png", 470, 330, 640, -5), ("bandeiras/br.png", 230, 760, 560, 7),
                               ("bandeiras/ar.png", 210, 770, 800, -6)]:
        e = Image.open(os.path.join(HERE, arq)).convert("RGBA")
        e.thumbnail((sz, sz), Image.LANCZOS)
        e = k5.adesivo(e, 12).rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, e, x, y)
    bal = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(bal)
    d.ellipse([0, 0, 290, 290], fill=b.YELLOW, outline=(20, 20, 40), width=12)
    d.text((145, 135), "?", font=b.font(b.F_BLACK, 230), fill=(20, 20, 40), anchor="mm")
    bal = k5.adesivo(bal, 14).rotate(-12, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(bal, (950, 380))
    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 120), "36 PAÍSES", nd.fit(d, "36 PAÍSES", 200, 1180), b.WHITE, outline=(15, 15, 30), w=18, anchor="lm")
    b.text_outline(d, (50, 310), "SÓ COM 2 LETRAS!", nd.fit(d, "SÓ COM 2 LETRAS!", 200, 1180), b.YELLOW, outline=(15, 15, 30), w=20, anchor="lm")
    b.put_palito(img, "assustado", 1080, 1610, 1200)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=(225, 20, 120))
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "VOCÊ CONSEGUE?", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    nomes = {"1": "As fáceis", "11": "Bandeiras parecidas", "21": "Pegadinhas", "33": "As impossíveis"}
    linhas = [f"{mmss(t[k])} {v}" for k, v in nomes.items()]
    linhas[0] = "0:00" + linhas[0][linhas[0].index(" "):]   # o YouTube exige o 1º capítulo em 0:00
    linhas.append(f"{mmss(t['final'])} Quantas você acertou?")
    caps = "\n".join(linhas)
    desc = f"""Adivinhe o PAÍS só com as 2 PRIMEIRAS LETRAS! 🌎 Aparecem as duas letras e os quadradinhos das outras: conta quantas letras tem, descobre o país e escolhe a bandeira certa entre 3. São {bd.TOTAL} países, e as últimas bandeiras são quase iguais!

👇 Comenta quantas você acertou!
👥 Chama a família pra jogar junto na TV!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Fluffing a Duck" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #bandeiras #geografia #países #quizpalito
"""
    tags = ["quiz de países", "adivinhe o país", "quiz de bandeiras", "bandeiras", "países do mundo", "geografia",
            "quiz de geografia", "adivinhe a bandeira", "desafio de bandeiras", "duas primeiras letras",
            "quiz", "quiz palito", "quiz em português", "você conhece os países"]
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
