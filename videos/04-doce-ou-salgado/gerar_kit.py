"""Kit do YouTube: thumbnail 1280x720, título, descrição (com capítulos), tags e comentário de créditos.

Uso: py -3 gerar_kit.py   (depois de renderizar o vídeo; lê tempos.json)
"""
import json, os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_prefere as bp
from build_prefere import b

OUT = os.path.join(HERE, "youtube")
TITULO = "QUAL VOCÊ PREFERE? 🍫 DOCE ou SALGADO 🍕 40 Escolhas IMPOSSÍVEIS | Quiz Palito"


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def thumb():
    img = bp.fundo(0).convert("RGBA")
    # duas fotos grandes inclinadas
    for cx, nome, ang in ((470, "Brigadeiro", 6), (1450, "Coxinha", -6)):
        s = 600
        card = Image.new("RGBA", (s + 40, s + 40), (0, 0, 0, 0))
        ImageDraw.Draw(card).rounded_rectangle([0, 0, s + 39, s + 39], 40, fill=b.WHITE)
        card.paste(bp.foto(nome, s), (20, 20))
        card = card.rotate(ang, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(card, (cx - card.width // 2, 470 - card.height // 2))
    d = ImageDraw.Draw(img)
    b.text_outline(d, (470, 900), "DOCE", b.font(b.F_BLACK, 190), b.YELLOW, w=20)
    b.text_outline(d, (1450, 900), "SALGADO", b.font(b.F_BLACK, 170), b.WHITE, w=20)
    d.ellipse([960 - 130, 470 - 130, 960 + 130, 470 + 130], fill=b.RED, outline=b.WHITE, width=14)
    d.text((960, 462), "OU", font=b.font(b.F_BLACK, 130), fill=b.WHITE, anchor="mm", stroke_width=5, stroke_fill=b.NAVY)
    d.rounded_rectangle([560, 30, 1360, 150], 60, fill=b.NAVY, outline=b.WHITE, width=8)
    d.text((960, 88), "QUAL VOCÊ PREFERE?", font=b.font(b.F_BLACK, 76), fill=b.YELLOW, anchor="mm")
    b.put_palito(img, "assustado", 430, 960, 1075)
    b.selo(img, 1730, 80, 0.85)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def main():
    os.makedirs(OUT, exist_ok=True)
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    caps = "\n".join([
        "0:00 Abertura",
        f"{mmss(t['1'])} Fase 1: Aquecimento",
        f"{mmss(t['2'])} Fase 2: Ficou difícil",
        f"{mmss(t['3'])} Fase 3: Muito difícil",
        f"{mmss(t['4'])} Fase final: Escolhas impossíveis 🔥",
        f"{mmss(t['final'])} Resultado: time doce ou time salgado?",
    ])
    desc = f"""Doce ou salgado? 🍫🍕 Essa é a batalha mais difícil do mundo! São 40 escolhas em 4 fases, e cada vez fica mais difícil escolher. Brigadeiro ou coxinha? Pudim ou lasanha? 😱

🧠 O Palito também escolhe! Conta quantas vezes você concordou com ele.
👇 Comenta: você é do TIME DOCE ou do TIME SALGADO?
👥 Marca aquele amigo que nunca consegue escolher!
🔔 Inscreva-se no Quiz Palito e ative o sininho: quiz novo toda semana!

⏱️ Capítulos
{caps}

📸 Créditos das fotos no comentário fixado.
🎵 Música: "Carefree" e "Wallpaper" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#qualvoceprefere #docеousalgado #quiz #quizpalito #desafio
""".replace("docеousalgado", "doceousalgado")
    tags = ["qual você prefere", "doce ou salgado", "quiz", "quiz de comida", "escolhas impossíveis",
            "desafio das escolhas", "você prefere", "quiz palito", "teste de personalidade", "quiz em português",
            "comida", "brigadeiro ou coxinha"]
    open(os.path.join(OUT, "titulo.txt"), "w", encoding="utf-8").write(TITULO + "\n")
    open(os.path.join(OUT, "descricao.txt"), "w", encoding="utf-8").write(desc)
    open(os.path.join(OUT, "tags.txt"), "w", encoding="utf-8").write(", ".join(tags) + "\n")
    cred = json.load(open(os.path.join(HERE, "creditos.json"), encoding="utf-8"))
    usadas = []
    for e in bp.ESC:
        for k in ("doce", "salgado"):
            if e[k] not in usadas:
                usadas.append(e[k])
    linhas = ["📸 Créditos das fotos (Wikimedia Commons):"]
    for n in usadas:
        c = cred[n]
        linhas.append(f"{n}: \"{c['title'].rsplit('.', 1)[0]}\" de {c['artist']}, {c['lic']}")
    open(os.path.join(OUT, "comentario-creditos.txt"), "w", encoding="utf-8").write("\n".join(linhas) + "\n")
    thumb()
    print(OUT, len(desc), "caracteres; comentário", sum(len(l) + 1 for l in linhas))


if __name__ == "__main__":
    main()
