"""Kit do YouTube do quiz de bandeiras: youtube/thumbnail.jpg, titulo.txt, descricao.txt, tags.txt.

Uso: py -3 gerar_kit.py            (precisa do vídeo pronto e do tempos.json para os capítulos)
     py -3 gerar_kit.py --so-thumb
"""
import json, os, re, subprocess, sys
from PIL import Image, ImageDraw

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(QP, "videos", "01-paises-sem-vogais"))
import build as b

b.PERSONAGEM = os.path.join(QP, "personagem")
OUT = os.path.join(HERE, "youtube")
VIDEO = os.path.join(HERE, "quiz-palito-bandeiras.mp4")


def thumb():
    img = b.gradient(b.TEAL, b.NAVY).convert("RGBA")
    d = ImageDraw.Draw(img)
    b.text_outline(d, (780, 165), "195 PAÍSES", b.font(b.F_BLACK, 170), b.WHITE, w=16)
    b.text_outline(d, (700, 355), "PELA BANDEIRA", b.font(b.F_BLACK, 132), b.YELLOW, w=16)
    codes = ["br", "kp", "np", "bt"]
    for i, code in enumerate(codes):
        fl = Image.open(os.path.join(HERE, "bandeiras", f"{code}.png")).convert("RGBA")
        fl.thumbnail((290, 200), Image.LANCZOS)
        cx = 690 - 1.5 * 310 + i * 310
        x0, y0 = int(cx - fl.width / 2), int(620 - fl.height / 2)
        b.shadowed_round_rect(img, (x0 - 12, y0 - 12, x0 + fl.width + 12, y0 + fl.height + 12), 18, b.WHITE)
        img.alpha_composite(fl, (x0, y0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([250, 830, 1270, 1000], 50, fill=b.RED, outline=b.WHITE, width=10)
    d.text((760, 915), "VOCÊ CONSEGUE?", font=b.font(b.F_BLACK, 110), fill=b.WHITE, anchor="mm")
    b.put_palito(img, "assustado", 900, 1600, 1075)
    b.selo(img, 1640, 90, 1.0)
    # selo "3 SEG"
    d = ImageDraw.Draw(img)
    d.ellipse([30, 30, 230, 230], fill=b.YELLOW, outline=b.NAVY, width=10)
    d.text((130, 112), "3", font=b.font(b.F_BLACK, 110), fill=b.NAVY, anchor="mm")
    d.text((130, 192), "SEG", font=b.font(b.F_BLACK, 46), fill=b.NAVY, anchor="mm")
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "thumbnail.jpg"), quality=92)


def cenas(a, z):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{a:.2f}", "-t", f"{z - a:.2f}", "-i", VIDEO, "-vf",
                        "select='gt(scene,0.35)',showinfo", "-f", "null", "-"], capture_output=True, text=True)
    return [a + float(x) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)]


def ajusta(est):
    ts = cenas(max(0, est - 3), est + 4)
    return min(ts, key=lambda x: abs(x - est)) if ts else est


def main():
    os.makedirs(OUT, exist_ok=True)
    thumb()
    if "--so-thumb" in sys.argv:
        return
    t = json.load(open(os.path.join(HERE, "tempos.json"), encoding="utf-8"))
    mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
    caps = "\n".join([
        "0:00 Abertura",
        f"{mmss(ajusta(t['FÁCIL']))} Nível fácil (1 a 65)",
        f"{mmss(ajusta(t['MÉDIO']))} Nível médio (66 a 130)",
        f"{mmss(ajusta(t['DIFÍCIL']))} Nível difícil (131 a 195) 🔥",
        f"{mmss(ajusta(t['FINAL']))} Resultado final",
    ])
    titulo = "ADIVINHE os 195 PAÍSES pela BANDEIRA em 3 SEGUNDOS! 🌍 Fácil, Médio e Difícil | Quiz Palito"
    descricao = f"""
Você conhece as bandeiras do MUNDO INTEIRO? 🌍😱 São 195 países e só 3 segundos para cada um!

Começa tranquilo com Brasil, Japão e Canadá… mas no nível difícil aparecem Butão, Kiribati e Tuvalu. 🤯 Será que você chega até o fim?

🎯 Desafio: jogue sem pausar o vídeo e conte quantas bandeiras você acertou! Deixa seu placar nos comentários: fácil, médio e difícil.
👥 Marca aquele amigo que se acha o rei da geografia e desafia ele!
🔔 Inscreva-se no Quiz Palito e ative o sininho: tem quiz novo toda semana!

⏱️ Capítulos
{caps}

🎵 Música: "Carefree" e "Wallpaper" Kevin MacLeod (incompetech.com) – CC BY 4.0 https://creativecommons.org/licenses/by/4.0/

#quiz #bandeiras #geografia #quizpalito #desafio
"""
    tags = ["quiz", "quiz de bandeiras", "adivinhe a bandeira", "195 países", "bandeiras do mundo",
            "quiz de geografia", "geografia", "países do mundo", "adivinhe o país", "desafio", "quiz palito",
            "teste seus conhecimentos", "quiz em português", "quiz fácil médio difícil"]
    open(os.path.join(OUT, "titulo.txt"), "w", encoding="utf-8").write(titulo + "\n")
    open(os.path.join(OUT, "descricao.txt"), "w", encoding="utf-8").write(descricao.strip() + "\n")
    open(os.path.join(OUT, "tags.txt"), "w", encoding="utf-8").write(", ".join(tags) + "\n")
    print(caps.encode("ascii", "replace").decode())


if __name__ == "__main__":
    main()
