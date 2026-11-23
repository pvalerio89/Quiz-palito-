"""Kit do YouTube do vídeo 53: thumbnail 1280x720 (reserva), título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
Miniatura principal: a tarefa do Google Flow gera com youtube/prompt-flow.txt; esta é a reserva.
"""
import importlib.util, json, os, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_naodiga2 as bd
from build_naodiga2 import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = "NÃO DIGA O MESMO QUE O PALITO 2 🤐 Você tem 8 vidas: com quantas termina? | Quiz Palito"


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    spec = importlib.util.spec_from_file_location("kit05", os.path.join(bd.VIDEOS, "05-nao-diga-o-mesmo", "gerar_kit.py"))
    k5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k5)
    # fundo azul liso com brilho no centro (melhor CTR do canal, 2026-11-19)
    img = Image.new("RGBA", (W, H), (25, 80, 200, 255))
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([300, 150, 1400, 1050], fill=120)
    img = Image.composite(Image.new("RGBA", (W, H), (140, 200, 255, 255)), img, glow.filter(ImageFilter.GaussianBlur(170)))
    for ch, sz, x, y, rot in [("🐄", 230, 200, 640, 8), ("🍕", 210, 470, 700, -8), ("🎨", 200, 740, 650, 6)]:
        e = nd.emoji(ch, sz)
        e = k5.adesivo(e, 12).rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, e, x, y)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([920, 520, 1190, 790], 40, fill=b.WHITE, outline=(15, 15, 30), width=10)
    d.text((1055, 600), "8", font=b.font(b.F_BLACK, 150), fill=b.RED, anchor="mm", stroke_width=6, stroke_fill=(15, 15, 30))
    d.text((1055, 730), "VIDAS", font=b.font(b.F_BLACK, 56), fill=(15, 15, 30), anchor="mm")
    b.text_outline(d, (50, 120), "NÃO DIGA O MESMO", nd.fit(d, "NÃO DIGA O MESMO", 170, 1250), b.WHITE, outline=(15, 15, 30), w=18, anchor="lm")
    b.text_outline(d, (50, 300), "QUE O PALITO 2", nd.fit(d, "QUE O PALITO 2", 190, 1250), b.YELLOW, outline=(15, 15, 30), w=20, anchor="lm")
    b.put_palito(img, "apontando", 1060, 1610, 1200)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=(225, 20, 120))
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "VOCÊ CONSEGUE?", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    nomes = {"1": "Começando com 8 vidas", "11": "Rodadas 11 a 20", "21": "Rodadas 21 a 30",
             "31": "As pegadinhas e a última"}
    linhas = [f"{mmss(t[k])} {v}" for k, v in nomes.items()]
    linhas[0] = "0:00" + linhas[0][linhas[0].index(" "):]   # o YouTube exige o 1º capítulo em 0:00
    linhas.append(f"{mmss(t['final'])} Com quantas vidas você terminou?")
    caps = "\n".join(linhas)
    desc = f"""NÃO DIGA O MESMO QUE O PALITO – PARTE 2 🤐 Você começa com 8 vidas. Em cada rodada aparece um pedido ("diga uma flor", "diga um dinossauro"...) e você pensa rápido na sua resposta. Depois o Palito revela a dele: pensou igual, perde uma vida! São {bd.TOTAL} rodadas novas, com pegadinhas no fim. Joga com a família e vê quem pensa mais diferente!

👇 Comenta com quantas vidas você terminou!
👥 Chama a família e os amigos pra jogar junto!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Fluffing a Duck" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #desafio #naodigaomesmo #jogo #quizpalito
"""
    tags = ["não diga o mesmo", "não diga o mesmo que eu", "não diga o mesmo que o palito", "jogo de vidas", "desafio",
            "quiz", "quiz palito", "quiz em português", "jogo em família", "brincadeira", "parte 2", "pense rápido",
            "teste de originalidade"]
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
