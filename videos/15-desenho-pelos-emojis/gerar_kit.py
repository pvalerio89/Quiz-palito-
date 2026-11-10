"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
"""
import importlib.util, json, os, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_desenhos as bd
from build_desenhos import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = f"ADIVINHE O DESENHO PELOS EMOJIS! 🧽 {bd.TOTAL} Desenhos e Filmes Animados | Quiz Palito"


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    spec = importlib.util.spec_from_file_location("kit05", os.path.join(bd.VIDEOS, "05-nao-diga-o-mesmo", "gerar_kit.py"))
    k5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k5)
    img = nd.burst((40, 190, 255), (150, 60, 220), 4).convert("RGBA")
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([380, 180, 1340, 1000], fill=150)
    img = Image.composite(Image.new("RGBA", (W, H), (210, 240, 255, 255)), img, glow.filter(ImageFilter.GaussianBlur(160)))
    vg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vg).ellipse([-350, -300, W + 350, H + 300], fill=255)
    img = Image.composite(img, Image.new("RGBA", (W, H), (30, 20, 110, 255)), vg.filter(ImageFilter.GaussianBlur(140)))
    # emojis gigantes recortados (adesivo)
    for ch, sz, x, y, rot in [("🧽", 330, 230, 690, 10), ("🍍", 300, 560, 650, -8), ("🦁", 300, 900, 690, 8),
                              ("👑", 230, 1180, 560, -14)]:
        e = k5.adesivo(bd.emoji(ch, sz), 14).rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, e, x, y)
    bal = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(bal)
    d.ellipse([0, 0, 290, 290], fill=b.YELLOW, outline=(20, 20, 40), width=12)
    d.text((145, 135), "?", font=b.font(b.F_BLACK, 230), fill=(20, 20, 40), anchor="mm")
    bal = k5.adesivo(bal, 14).rotate(-12, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(bal, (1040, 300))
    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 120), "QUE DESENHO É?", nd.fit(d, "QUE DESENHO É?", 170, 1180), b.WHITE, outline=(15, 15, 30), w=18, anchor="lm")
    b.text_outline(d, (50, 300), "PELOS EMOJIS!", nd.fit(d, "PELOS EMOJIS!", 200, 1180), b.YELLOW, outline=(15, 15, 30), w=20, anchor="lm")
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
    desc = f"""ADIVINHE O DESENHO PELOS EMOJIS! 🧽🍍🌊 São {bd.TOTAL} desenhos e filmes animados escondidos em 3 ou 4 emojis, do mais fácil ao mais difícil: Bob Esponja, Shrek, Frozen, Pokémon, Turma da Mônica, Rei Leão, clássicos das antigas e muito mais! Você tem 5 segundos e 3 alternativas para cada um. 📺

👇 Comenta quantos você acertou!
👥 Chama a família e os amigos pra ver quem lembra mais desenho!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Fluffing a Duck" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #desenhoanimado #emoji #quizpalito #adivinheodesenho
"""
    tags = ["adivinhe o desenho", "adivinhe o desenho pelos emojis", "quiz de desenhos", "quiz emoji", "desenho animado",
            "quiz de desenho animado", "quiz", "quiz palito", "quiz em português", "desafio emoji", "filmes animados",
            "quiz de filmes", "desenhos antigos", "teste de memória"]
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
