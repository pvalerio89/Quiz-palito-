"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
"""
import importlib.util, json, os, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_monte as bd
from build_monte import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = "MONTE O TIME CAMPEÃO ⚽ Você Lembra a Escalação do Penta, do Tri e do Barça? | Quiz Palito"


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
    # escudos gigantes recortados (adesivo)
    cp = bd.campo(0, 10, False, 0.2, 560)   # sem entregar o centroavante (o "?")
    cp = k5.adesivo(cp, 14).rotate(6, expand=True, resample=Image.BICUBIC)
    nd.paste_c(img, cp, 470, 690)
    for ti, sz, x, y, rot in [(3, 230, 960, 780, -10), (1, 210, 140, 560, 12)]:
        e = bd.icone(ti, sz)
        e = k5.adesivo(e, 12).rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, e, x, y)
    bal = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(bal)
    d.ellipse([0, 0, 290, 290], fill=b.YELLOW, outline=(20, 20, 40), width=12)
    d.text((145, 135), "?", font=b.font(b.F_BLACK, 230), fill=(20, 20, 40), anchor="mm")
    bal = k5.adesivo(bal, 14).rotate(-12, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(bal, (1040, 300))
    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 120), "MONTE O TIME", nd.fit(d, "MONTE O TIME", 170, 1180), b.WHITE, outline=(15, 15, 30), w=18, anchor="lm")
    b.text_outline(d, (50, 300), "CAMPEÃO!", nd.fit(d, "CAMPEÃO!", 200, 1180), b.YELLOW, outline=(15, 15, 30), w=20, anchor="lm")
    b.put_palito(img, "assustado", 1080, 1610, 1200)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=(225, 20, 120))
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "VOCÊ CONSEGUE?", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    linhas = [f"{mmss(t[str(i)])} Time {i + 1}: {tm['nome'].title()} ({tm['sub'].lower().replace('copa', 'Copa').replace('champions', 'Champions')})"
              for i, tm in enumerate(bd.TIMES)]
    linhas[0] = "0:00" + linhas[0][linhas[0].index(" "):]   # o YouTube exige o 1º capítulo em 0:00
    linhas.append(f"{mmss(t['final'])} Quantos você acertou?")
    caps = "\n".join(linhas)
    desc = f"""MONTE O TIME CAMPEÃO! ⚽ Você lembra a escalação titular das finais mais famosas do futebol? Posição por posição, do goleiro ao atacante: Brasil do penta (2002), Real Madrid (Champions 2017), Argentina (Copa 2022), Barcelona (Champions 2011), Espanha (Copa 2010) e o Brasil do tri (1970). São {bd.TOTAL} perguntas, 5 segundos e 3 alternativas em cada uma!

👇 Comenta quantos você acertou e qual time você quer no próximo!
👥 Chama os amigos pra ver quem manja mais de futebol!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Carefree" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #futebol #quizdefutebol #escalação #quizpalito
"""
    tags = ["monte o time", "monte seu time", "escalação", "quiz de futebol", "brasil 2002", "brasil 1970", "penta",
            "barcelona 2011", "argentina 2022", "real madrid", "futebol", "quiz", "quiz palito", "quiz em português",
            "desafio de futebol"]
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
