"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
"""
import importlib.util, json, os, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_times as bd
from build_times import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = f"ALFABETO DOS TIMES DE A a Z ⚽ Adivinhe {bd.TOTAL} Times Pelo Escudo! | Quiz Palito"


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
    for nome, sz, x, y, rot in [("Flamengo", 330, 230, 690, 10), ("Real Madrid", 300, 560, 650, -8),
                                ("Corinthians", 300, 890, 700, 8)]:
        r = next(r for r in bd.R if r["nome"] == nome)
        e = Image.open(os.path.join(HERE, "escudos", r["escudo"])).convert("RGBA")
        e = e.crop(e.getbbox())
        e.thumbnail((sz, sz), Image.LANCZOS)
        e = k5.adesivo(e, 14).rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, e, x, y)
    bal = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(bal)
    d.ellipse([0, 0, 290, 290], fill=b.YELLOW, outline=(20, 20, 40), width=12)
    d.text((145, 135), "?", font=b.font(b.F_BLACK, 230), fill=(20, 20, 40), anchor="mm")
    bal = k5.adesivo(bal, 14).rotate(-12, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(bal, (1040, 300))
    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 120), "TIMES DE A a Z", nd.fit(d, "TIMES DE A a Z", 170, 1180), b.WHITE, outline=(15, 15, 30), w=18, anchor="lm")
    b.text_outline(d, (50, 300), "PELO ESCUDO!", nd.fit(d, "PELO ESCUDO!", 200, 1180), b.YELLOW, outline=(15, 15, 30), w=20, anchor="lm")
    b.put_palito(img, "assustado", 1080, 1610, 1200)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=(225, 20, 120))
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "VOCÊ CONSEGUE?", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    nivel = ["fácil", "fácil", "médio", "médio", "difícil", "difícil", "muito difícil"]
    linhas = []
    for k, ini in enumerate(range(1, bd.TOTAL + 1, 10)):
        fim = min(ini + 9, bd.TOTAL)
        linhas.append(f"{mmss(t[str(ini)])} {ini} a {fim} ({nivel[min(k, len(nivel) - 1)]})")
    linhas.append(f"{mmss(t['final'])} Quantos você acertou?")
    caps = "\n".join(linhas)
    desc = f"""ALFABETO DOS TIMES DE A a Z! ⚽ São {bd.TOTAL} times do Brasil e do mundo, um alfabeto inteiro de escudos: Flamengo, Corinthians, Real Madrid, Barcelona, Liverpool e até as letras mais difíceis como K, Q, X e Y! O escudo aparece pixelado e vai ficando nítido: você tem 5 segundos e 3 alternativas com a mesma letra.

👇 Comenta quantos você acertou e qual é o seu time!
👥 Chama os amigos pra ver quem manja mais de futebol!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Carefree" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #futebol #quizdefutebol #escudos #quizpalito
"""
    tags = ["alfabeto dos times", "times de a a z", "adivinhe o time pelo escudo", "quiz de futebol", "escudos de times",
            "quiz de escudos", "futebol", "quiz", "quiz palito", "quiz em português", "times brasileiros",
            "times europeus", "desafio de futebol", "adivinhe o escudo"]
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
