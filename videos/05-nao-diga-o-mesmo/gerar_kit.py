"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_naodiga as bn
from build_naodiga import b, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = "NÃO DIGA O MESMO QUE O PALITO 🤐 Só 5% Termina Com 8 Vidas! | Quiz Palito"
LIMA = (170, 255, 40)


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def adesivo(im, borda=18):
    """Recorte com borda branca grossa e sombra."""
    pad = borda + 20
    cv = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    cv.paste(im, (pad, pad), im)
    a = cv.getchannel("A").point(lambda v: 255 if v > 30 else 0)
    ol = a.filter(ImageFilter.MaxFilter(borda * 2 + 1)).filter(ImageFilter.GaussianBlur(1.5))
    sh = ol.filter(ImageFilter.GaussianBlur(12)).point(lambda v: v * 0.5)
    out = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    s = Image.new("RGBA", cv.size, (0, 0, 0, 255)); s.putalpha(sh)
    out.alpha_composite(s, (8, 12))
    w = Image.new("RGBA", cv.size, (255, 255, 255, 255)); w.putalpha(ol)
    out.alpha_composite(w)
    out.alpha_composite(cv)
    return out


def thumb():
    # fundo P&B com raios borrados
    raios = bn.burst((120, 120, 120), (60, 60, 60), 4).convert("L")
    tela = ImageOps.grayscale(bn.tela(bn.R[0], revelado=True).convert("RGB"))
    bg = Image.blend(raios, tela, 0.35).filter(ImageFilter.GaussianBlur(7))
    bg = ImageOps.autocontrast(bg, cutoff=2).point(lambda v: int(v * 0.8))
    img = bg.convert("RGBA")
    # vinheta escura nas bordas
    vg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vg).ellipse([-300, -250, W + 300, H + 250], fill=255)
    vg = vg.filter(ImageFilter.GaussianBlur(120))
    img = Image.composite(img, Image.new("RGBA", (W, H), (10, 10, 20, 255)), vg)

    # coração x8
    cor = Image.new("RGBA", (620, 330), (0, 0, 0, 0))
    cor.alpha_composite(bn.emoji("❤", 300), (0, 15))
    d = ImageDraw.Draw(cor)
    d.text((330, 170), "x8", font=b.font(b.F_BLACK, 230), fill=b.WHITE, anchor="lm", stroke_width=14, stroke_fill=(20, 20, 40))
    cor = adesivo(cor.crop(cor.getbbox()), 16).rotate(-6, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(cor, (40, 560))

    # balão ???
    bal = Image.new("RGBA", (560, 380), (0, 0, 0, 0))
    d = ImageDraw.Draw(bal)
    d.ellipse([0, 0, 560, 300], fill=b.YELLOW, outline=(20, 20, 40), width=12)
    d.polygon([(140, 250), (90, 375), (250, 280)], fill=b.YELLOW, outline=(20, 20, 40))
    d.ellipse([12, 12, 548, 288], fill=b.YELLOW)
    d.text((280, 145), "???", font=b.font(b.F_BLACK, 190), fill=(20, 20, 40), anchor="mm")
    bal = adesivo(bal, 14).rotate(8, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(bal, (620, 400))

    # título 2 linhas
    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 135), "NÃO DIGA", b.font(b.F_BLACK, 205), b.WHITE, outline=(15, 15, 30), w=22, anchor="lm")
    b.text_outline(d, (50, 355), "O MESMO!", b.font(b.F_BLACK, 215), LIMA, outline=(15, 15, 30), w=22, anchor="lm")

    # Palito enorme em pânico
    b.put_palito(img, "assustado", 1150, 1520, 1230)

    # faixa vermelha
    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=b.RED)
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "VOCÊ CONSEGUE?", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    caps = "\n".join([
        "0:00 Abertura: a regra das 8 vidas",
        f"{mmss(t['1'])} Rodadas 1 a 10",
        f"{mmss(t['11'])} Rodadas 11 a 20",
        f"{mmss(t['21'])} Rodadas 21 a 30",
        f"{mmss(t['31'])} Rodadas 31 a 40",
        f"{mmss(t['final'])} Com quantas vidas você terminou?",
    ])
    desc = f"""Você consegue NÃO pensar igual ao Palito? 🤐 Diga uma fruta… diga uma cor… diga um número de 1 a 10… Parece fácil, mas quase todo mundo pensa a mesma coisa! 😱

❤️ A regra: você começa com 8 VIDAS. Em cada uma das 40 rodadas aparece um pedido, você pensa na sua resposta antes do tempo acabar e depois o Palito revela a dele. Pensou igual ao Palito? Perde uma vida! Cuidado com as pegadinhas! 😈

👇 Comenta: com quantas vidas você terminou?
👥 Marca aquele amigo que sempre pensa igual a todo mundo!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo toda semana!

⏱️ Capítulos
{caps}

🎵 Música: "Carefree" e "Wallpaper" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #naodigaomesmo #quizpalito #desafio
"""
    tags = ["não diga o mesmo", "não diga o mesmo que eu", "quiz", "quiz palito", "desafio", "jogo de vidas",
            "8 vidas", "quiz em português", "teste de originalidade", "pense diferente", "quiz divertido",
            "desafio de raciocínio", "jogo para jogar com amigos", "quiz brasileiro"]
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
