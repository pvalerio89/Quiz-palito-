"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
Miniatura principal: o Patrick gera no Google Flow com youtube/prompt-flow.txt; esta é a reserva.
"""
import importlib.util, json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_monumentos as bd
from build_monumentos import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = f"ADIVINHE O PAÍS PELO MONUMENTO 🌍 {bd.TOTAL} Lugares Famosos do Fácil ao Impossível! Quiz de Geografia | Quiz Palito"


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    spec = importlib.util.spec_from_file_location("kit05", os.path.join(bd.VIDEOS, "05-nao-diga-o-mesmo", "gerar_kit.py"))
    k5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k5)
    img = nd.burst((40, 170, 90), (10, 90, 60), 4).convert("RGBA")
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([380, 180, 1340, 1000], fill=150)
    img = Image.composite(Image.new("RGBA", (W, H), (220, 235, 255, 255)), img, glow.filter(ImageFilter.GaussianBlur(160)))
    vg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vg).ellipse([-350, -300, W + 350, H + 300], fill=255)
    img = Image.composite(img, Image.new("RGBA", (W, H), (5, 25, 80, 255)), vg.filter(ImageFilter.GaussianBlur(140)))
    for arq, sz, x, y, rot, blur in [("torre-eiffel.jpg", 340, 240, 690, 8, 0),
                                     ("moai.jpg", 330, 600, 680, -7, 0)]:
        e = ImageOps.fit(Image.open(os.path.join(HERE, "fotos", arq)).convert("RGB"), (sz, sz))
        if blur:
            e = e.filter(ImageFilter.GaussianBlur(blur))
        e = e.convert("RGBA")
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
    img.alpha_composite(bal, (880, 420))
    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 120), "EM QUE PAÍS", nd.fit(d, "EM QUE PAÍS", 190, 1180), b.WHITE, outline=(15, 15, 30), w=18, anchor="lm")
    b.text_outline(d, (50, 300), "FICA ISSO?", nd.fit(d, "FICA ISSO?", 200, 1180), b.YELLOW, outline=(15, 15, 30), w=20, anchor="lm")
    b.put_palito(img, "assustado", 1080, 1610, 1200)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=(225, 20, 120))
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "VOCÊ CONSEGUE?", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    nomes = {"1": "As fáceis", "11": "Subindo o nível", "21": "As mais difíceis"}
    linhas = [f"{mmss(t[k])} {v}" for k, v in nomes.items()]
    linhas[0] = "0:00" + linhas[0][linhas[0].index(" "):]   # o YouTube exige o 1º capítulo em 0:00
    linhas.append(f"{mmss(t['final'])} Quantos você acertou?")
    caps = "\n".join(linhas)
    desc = f"""ADIVINHE O PAÍS PELO MONUMENTO! 🌍 São {bd.TOTAL} lugares famosos do mundo, do fácil ao impossível: Cristo Redentor, pirâmides, castelos, templos e torres. Cada um tem 3 países como alternativa e 7 segundos. Tem dica, pegadinha e curiosidade no caminho. Ótimo para treinar geografia para a escola!

👇 Comenta quantos você acertou!
👥 Desafia os amigos da escola!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Sneaky Snitch" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #geografia #monumentos #paises #quizpalito
"""
    tags = ["adivinhe o país", "monumentos do mundo", "lugares famosos", "quiz de geografia", "geografia",
            "quiz de países", "pontos turísticos", "quiz escolar", "quiz educativo", "quiz", "quiz palito",
            "quiz em português", "você sabe geografia"]
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
