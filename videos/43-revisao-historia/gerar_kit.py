"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
Miniatura principal: o Patrick gera no Google Flow com youtube/prompt-flow.txt; esta é a reserva.
"""
import importlib.util, json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_historia as bd
from build_historia import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = f"Quiz Revisão: Avaliação de Processo de História 3º Ano 🏰 {bd.TOTAL} Questões! Você Passaria? | Quiz Palito"


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    """Fundo azul liso + número grande + desafio literal (melhor CTR do canal, 2026-11-19)."""
    spec = importlib.util.spec_from_file_location("kit05", os.path.join(bd.VIDEOS, "05-nao-diga-o-mesmo", "gerar_kit.py"))
    k5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k5)
    img = Image.new("RGBA", (W, H), (25, 95, 200, 255))
    vg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vg).ellipse([-350, -300, W + 350, H + 300], fill=255)
    img = Image.composite(img, Image.new("RGBA", (W, H), (8, 40, 110, 255)), vg.filter(ImageFilter.GaussianBlur(160)))
    for arq, sz, x, y, rot in [("elevador.jpg", 400, 300, 700, 7), ("congresso.jpg", 360, 690, 720, -6)]:
        p = os.path.join(bd.FOTOS, arq)
        if not os.path.exists(p):
            continue
        e = ImageOps.fit(Image.open(p).convert("RGB"), (sz, sz)).convert("RGBA")
        m = Image.new("L", (sz, sz), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, sz - 1, sz - 1], 40, fill=255)
        e.putalpha(m)
        e = k5.adesivo(e, 14).rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, e, x, y)
    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 120), "REVISÃO DE HISTÓRIA", nd.fit(d, "REVISÃO DE HISTÓRIA", 170, 1180), b.WHITE, outline=(15, 15, 30), w=16, anchor="lm")
    b.text_outline(d, (50, 290), "3º ANO: VOCÊ PASSA?", nd.fit(d, "3º ANO: VOCÊ PASSA?", 180, 1180), b.YELLOW, outline=(15, 15, 30), w=18, anchor="lm")
    b.text_outline(d, (1050, 600), str(bd.TOTAL), b.font(b.F_BLACK, 330), b.YELLOW, outline=(15, 15, 30), w=22)
    b.text_outline(d, (1050, 790), "QUESTÕES", b.font(b.F_BLACK, 80), b.WHITE, outline=(15, 15, 30), w=10)
    b.put_palito(img, "apontando", 1530, 1610, 1100)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=(225, 20, 120))
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "VOCÊ CONSEGUE?", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    nomes = {"1": "Nível médio", "16": "Nível difícil", "31": "Nível muito difícil"}
    linhas = [f"{mmss(t[k])} {v}" for k, v in nomes.items()]
    linhas[0] = "0:00" + linhas[0][linhas[0].index(" "):]   # o YouTube exige o 1º capítulo em 0:00
    linhas.append(f"{mmss(t['final'])} Quantos você acertou?")
    caps = "\n".join(linhas)
    desc = f"""QUIZ REVISÃO DE HISTÓRIA DO 3º ANO! 🏰 São {bd.TOTAL} questões pra revisar a Avaliação de Processo de História (o nascimento e a formação das cidades), do médio ao muito difícil: nômades e as primeiras cidades, por que as primeiras vilas do Brasil ficavam no litoral, pra que serviam os fortes, povoado, vila ou cidade, o pelourinho, a fundação de Salvador (Cidade Alta e Cidade Baixa), as capitais do Brasil (Salvador, Rio de Janeiro e Brasília), espaços públicos e os deveres do bom cidadão. Cada uma tem 3 alternativas e tempo pra pensar. Ótimo pra estudar pra prova!

👇 Comenta quantas você acertou e qual te pegou!
👥 Desafia os amigos (e os pais!) pra ver quem tira 10!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Wallpaper" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

📚 Prova de geografia do 3º ano: https://youtu.be/S2X5K-jEREg

#quiz #historia #quizdehistoria #escola #quizpalito
"""
    tags = ["quiz de história", "história 3º ano", "revisão de história", "avaliação de história", "prova de história",
            "formação das cidades", "povoado vila e cidade", "fortes", "fundação de Salvador", "cidade alta e cidade baixa",
            "capitais do Brasil", "deveres do cidadão", "quiz escolar", "quiz educativo", "quiz", "quiz palito",
            "quiz em português", "estudar para prova"]
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
