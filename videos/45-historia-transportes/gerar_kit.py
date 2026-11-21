"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py           (depois do render; lê tempos.json)
     py -3 gerar_kit.py --thumb   (só a thumbnail)
Miniatura principal: a tarefa do Google Flow gera com youtube/prompt-flow.txt; esta é a reserva.
"""
import importlib.util, json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_historia as bd
from build_historia import b, nd, W, H

OUT = os.path.join(HERE, "youtube")
TITULO = f"PROVA DE HISTÓRIA DO 3º ANO 🚂 {bd.TOTAL} Questões de Transportes, do Médio ao Difícil! | Quiz Palito"


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    spec = importlib.util.spec_from_file_location("kit05", os.path.join(bd.VIDEOS, "05-nao-diga-o-mesmo", "gerar_kit.py"))
    k5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k5)
    # fundo azul LISO (sem raios): melhor CTR do canal (19/11), número grande e o desafio literal
    img = Image.new("RGBA", (W, H), (25, 90, 210, 255))
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([300, 150, 1400, 1050], fill=140)
    img = Image.composite(Image.new("RGBA", (W, H), (90, 170, 255, 255)), img, glow.filter(ImageFilter.GaussianBlur(200)))
    for arq, sz, x, y, rot in [("vapor", 400, 280, 700, -6), ("14bis", 360, 700, 690, 7)]:
        fp = os.path.join(HERE, "fotos", arq + ".jpg")
        if not os.path.exists(fp):
            continue
        e = ImageOps.fit(Image.open(fp).convert("RGB"), (sz, sz)).convert("RGBA")
        m = Image.new("L", (sz, sz), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, sz - 1, sz - 1], 40, fill=255)
        e.putalpha(m)
        e = k5.adesivo(e, 14).rotate(rot, expand=True, resample=Image.BICUBIC)
        nd.paste_c(img, e, x, y)
    d = ImageDraw.Draw(img)
    b.text_outline(d, (50, 130), "44 QUESTÕES", nd.fit(d, "44 QUESTÕES", 210, 1180), b.YELLOW, outline=(15, 15, 30), w=20, anchor="lm")
    b.text_outline(d, (50, 320), "DE HISTÓRIA 3º ANO", nd.fit(d, "DE HISTÓRIA 3º ANO", 150, 1180), b.WHITE, outline=(15, 15, 30), w=16, anchor="lm")
    b.put_palito(img, "pensando", 1080, 1610, 1200)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 935), (1130, 915), (1100, 1080), (0, 1080)], fill=(225, 20, 120))
    d.line([(0, 935), (1130, 915)], fill=b.WHITE, width=10)
    b.text_outline(d, (560, 1000), "NENHUMA FÁCIL!", b.font(b.F_BLACK, 112), b.WHITE, outline=(15, 15, 30), w=10)
    b.selo(img, 1755, 1025, 0.62)
    # a miniatura do Google Flow (youtube/thumbnail.jpg) não pode ser sobrescrita: esta vira a reserva
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail-codigo.jpg"), quality=92)
    if not os.path.exists(os.path.join(OUT, "thumbnail.jpg")):
        img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def textos():
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    nomes = {"1": "Nível médio", "15": "Nível difícil", "30": "Nível muito difícil"}
    linhas = [f"{mmss(t[k])} {v}" for k, v in nomes.items()]
    linhas[0] = "0:00" + linhas[0][linhas[0].index(" "):]   # o YouTube exige o 1º capítulo em 0:00
    linhas.append(f"{mmss(t['final'])} Quantas você acertou?")
    caps = "\n".join(linhas)
    desc = f"""PROVA DE HISTÓRIA DO 3º ANO: TRANSPORTES! 🚂✈️⛵ São {bd.TOTAL} questões, todas do médio ao muito difícil: meios de transporte do passado, do presente e do futuro. Tem tropas e tropeiros (gravuras de Debret e Rugendas), cadeiras de arruar, a primeira ferrovia do Brasil (Estrada de Ferro Mauá, 1854) e a maria-fumaça, a evolução dos trens até o TGV e o Maglev, os bondes e ônibus elétricos, o gráfico do Ipea sobre transporte nas cidades, trânsito e congestionamento, o 14-Bis de Santos Dumont, as embarcações do Brasil e a canoa caiçara, que é patrimônio imaterial. Cada uma tem 3 alternativas e tempo pra pensar. Ótimo pra estudar pra prova!

👇 Comenta quantas você acertou e qual te pegou!
👥 Desafia os amigos (e os pais!) pra ver quem tira 10!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo todo dia!

⏱️ Capítulos
{caps}

🎵 Música: "Wallpaper" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #história #quizdehistoria #escola #quizpalito
"""
    tags = ["quiz de história", "história 3º ano", "prova de história", "meios de transporte", "transportes",
            "tropeiros", "maria-fumaça", "estrada de ferro mauá", "santos dumont", "14-bis", "canoa caiçara",
            "patrimônio imaterial", "quiz escolar", "quiz educativo", "quiz", "quiz palito", "quiz em português",
            "estudar para prova"]
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
