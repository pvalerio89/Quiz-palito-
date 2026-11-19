"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
Miniatura principal: o Patrick gera no Google Flow com youtube/prompt-flow.txt; esta é a reserva.
"""
import importlib.util, json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_ingles_review as bd
from build_ingles_review import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = f"REVISÃO DE INGLÊS DO 3º ANO 📚 {bd.TOTAL} Questões do Médio ao Muito Difícil! Você Passaria? | Quiz Palito"


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    """Fundo azul liso + número grande + o desafio mostrado (miniaturas de maior CTR, 2026-11-19)."""
    spec = importlib.util.spec_from_file_location("kit05", os.path.join(bd.VIDEOS, "05-nao-diga-o-mesmo", "gerar_kit.py"))
    k5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k5)
    img = Image.new("RGBA", (W, H), (25, 110, 220, 255))
    vg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vg).ellipse([-350, -300, W + 350, H + 300], fill=255)
    img = Image.composite(img, Image.new("RGBA", (W, H), (10, 50, 140, 255)), vg.filter(ImageFilter.GaussianBlur(140)))
    for arq, sz, x, y, rot in [("morango.jpg", 300, 230, 720, 8), ("maca.jpg", 280, 560, 760, -7)]:
        e = ImageOps.fit(Image.open(os.path.join(HERE, "fotos", arq)).convert("RGB"), (sz, sz)).convert("RGBA")
        m = Image.new("L", (sz, sz), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, sz - 1, sz - 1], 40, fill=255)
        e.putalpha(m)
        e = k5.adesivo(e, 14).rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, e, x, y)
    # o desafio: watchs ou watches?
    c = Image.new("RGBA", (420, 230), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, 419, 229], 36, fill=b.WHITE, outline=b.NAVY, width=8)
    d.text((210, 70), "watchs", font=b.font(b.F_BLACK, 74), fill=b.RED, anchor="mm")
    d.line([(70, 72), (350, 72)], fill=b.RED, width=8)
    d.text((210, 165), "watches?", font=b.font(b.F_BLACK, 74), fill=(30, 150, 70), anchor="mm")
    c = k5.adesivo(c, 12).rotate(-6, expand=True, resample=Image.BICUBIC)
    nd.paste_c(img, c, 990, 640)
    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 200), "44", b.font(b.F_BLACK, 330), b.YELLOW, outline=(15, 15, 30), w=22, anchor="lm")
    b.text_outline(d, (500, 140), "QUESTÕES DE", nd.fit(d, "QUESTÕES DE", 130, 700), b.WHITE, outline=(15, 15, 30), w=14, anchor="lm")
    b.text_outline(d, (500, 290), "INGLÊS!", nd.fit(d, "INGLÊS!", 170, 700), b.WHITE, outline=(15, 15, 30), w=16, anchor="lm")
    b.put_palito(img, "assustado", 1080, 1610, 1200)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=(225, 20, 120))
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "VOCÊ CONSEGUE?", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    # a miniatura do Google Flow (thumbnail.jpg) manda; a feita aqui fica como reserva (thumbnail-codigo.jpg)
    nome = "thumbnail-codigo.jpg" if os.path.exists(os.path.join(OUT, "thumbnail-codigo.jpg")) else "thumbnail.jpg"
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, nome), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    nomes = {"1": "Nível médio", "16": "Nível difícil", "31": "Nível muito difícil"}
    linhas = [f"{mmss(t[k])} {v}" for k, v in nomes.items()]
    linhas[0] = "0:00" + linhas[0][linhas[0].index(" "):]   # o YouTube exige o 1º capítulo em 0:00
    linhas.append(f"{mmss(t['final'])} Quantos você acertou?")
    caps = "\n".join(linhas)
    desc = f"""REVISÃO DE INGLÊS DO 3º ANO! 📚 São {bd.TOTAL} questões de uma revisão de prova de inglês (Grade 3 ESL), do médio ao muito difícil: verbos no presente (com -s e -es), no passado (com -ed) e no futuro (com will), palavras de tempo como yesterday, tomorrow e every day, partes da planta (flower, leaves, stem e roots), frutas e legumes em inglês com fotos reais e plural (-s, -es e -ies). Cada uma tem 3 alternativas e tempo pra pensar. Ótimo pra estudar pra prova!

👇 Comenta quantas você acertou e qual te pegou!
👥 Desafia os amigos (e os pais!) pra ver quem tira 10!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Wallpaper" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

📚 Quiz de inglês do 5º ao 9º ano: https://youtu.be/-_mZQhLOJAI

#quiz #ingles #quizdeingles #escola #quizpalito
"""
    tags = ["quiz de inglês", "inglês 3º ano", "revisão de inglês", "prova de inglês", "verbos em inglês",
            "simple present", "simple past", "future will", "plural em inglês", "partes da planta em inglês",
            "frutas em inglês", "legumes em inglês", "quiz escolar", "quiz educativo", "quiz", "quiz palito",
            "quiz em português", "estudar para prova", "english quiz"]
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
