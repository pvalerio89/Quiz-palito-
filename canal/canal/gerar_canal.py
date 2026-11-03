"""Imagens do canal Quiz Palito: banner 2048x1152 e foto de perfil 800x800.

Uso: py -3 gerar_canal.py
A área segura do banner (aparece em celular e computador) é o centro de 1235x338.
"""
import os, sys, shutil
from PIL import Image, ImageDraw

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(AQUI))
PAISES = os.path.join(QP, "videos", "01-paises-sem-vogais")
sys.path.insert(0, PAISES)
import build as b

b.PERSONAGEM = os.path.join(QP, "personagem")
BW, BH = 2048, 1152
SX0, SY0, SX1, SY1 = 406, 407, 1641, 745  # área segura


def banner(saida, guia=False):
    fundo = b.pattern_bg().resize((BW, BH))  # padrão de ? e globos
    img = fundo.convert("RGBA")
    d = ImageDraw.Draw(img)
    cx = BW // 2

    # nome do canal grande
    f = b.font(b.F_BLACK, 112)
    w1, w2 = d.textlength("QUIZ ", font=f), d.textlength("PALITO", font=f)
    x = cx - (w1 + w2) / 2
    b.text_outline(d, (x, 530), "QUIZ ", f, b.YELLOW, w=12, anchor="lm")
    b.text_outline(d, (x + w1, 530), "PALITO", f, b.WHITE, w=12, anchor="lm")

    # faixa com o slogan
    fs = b.font(b.F_BLACK, 42)
    txt = "QUIZ NOVO TODA SEMANA!"
    tw = d.textlength(txt, font=fs)
    y0 = 615
    d.rounded_rectangle([cx - tw / 2 - 36, y0, cx + tw / 2 + 36, y0 + 74], 42,
                        fill=b.RED, outline=b.WHITE, width=6)
    d.text((cx, y0 + 37), txt, font=fs, fill=b.WHITE, anchor="mm")

    # temas (fora da área segura: só aparecem em TV/computador grande)
    ft = b.font(b.F_BLACK, 46)
    temas = "GEOGRAFIA  •  BANDEIRAS  •  FUTEBOL  •  CURIOSIDADES"
    b.text_outline(d, (cx, 820), temas, ft, b.WHITE, w=7)

    # Palito dentro da área segura
    b.put_palito(img, "apontando", 300, SX0 + 115, SY1 - 5)
    b.put_palito(img, "comemorando", 300, SX1 - 105, SY1 - 5)
    # Palitos extras nas bordas (TV)
    b.put_palito(img, "pensando", 420, 190, BH - 40)
    b.put_palito(img, "acenando", 420, BW - 190, BH - 40)

    if guia:
        d.rectangle([SX0, SY0, SX1, SY1], outline=(255, 0, 0), width=4)
    img.convert("RGB").save(saida, quality=93)


if __name__ == "__main__":
    os.makedirs(AQUI, exist_ok=True)
    banner(os.path.join(AQUI, "banner.jpg"))
    banner(os.path.join(AQUI, "banner-com-guia.jpg"), guia=True)
    shutil.copy(os.path.join(b.PERSONAGEM, "logo.png"), os.path.join(AQUI, "foto-perfil.png"))
    print(AQUI)
