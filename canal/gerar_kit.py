"""Kit de publicação do Quiz Palito: thumbnail 1280x720 + título, descrição (com capítulos) e tags.

Uso: py -3 gerar_kit.py
Cria a pasta "youtube" dentro de cada projeto de vídeo.
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAISES = os.path.join(QP, "videos", "01-paises-sem-vogais")
JOGADORES = os.path.join(QP, "videos", "02-jogadores-a-z")
sys.path.insert(0, PAISES)
import build as b  # reaproveita fontes, cores, Palito e selo

b.PERSONAGEM = os.path.join(QP, "personagem")
TW, TH = 1280, 720


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def capitulos(pasta, perguntas, grupos, rotulo):
    """Recalcula os tempos exatamente como o build.py monta o vídeo."""
    A = lambda n: os.path.join(pasta, "assets", n)
    t = round((dur(A("intro.mp3")) + 0.6) * 30) / 30
    inicio = {}
    for q in perguntas:
        n = q["n"]
        inicio[n] = t
        t += 1.0 + round((dur(A(f"q{n}.mp3")) + 0.3) * 30) / 30 + 10.0
        t += int(max(3.5, dur(A(f"a{n}.mp3")) + 0.9) * 30) / 30
    fim = t
    video = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith(".mp4") and f.startswith("quiz-palito")][0]

    def ajusta(est):
        """Procura no vídeo a troca de cena (início da vinheta) mais próxima da estimativa."""
        a = max(0, est - 3)
        r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{a:.2f}", "-t", "9", "-i", video, "-vf",
                            "select='gt(scene,0.35)',showinfo", "-f", "null", "-"], capture_output=True, text=True)
        ts = [a + float(x) for x in __import__("re").findall(r"pts_time:([0-9.]+)", r.stderr)]
        return min(ts, key=lambda x: abs(x - est)) if ts else est

    inicio = {n: ajusta(v) for n, v in inicio.items()}
    fim = ajusta(fim)
    mmss = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
    linhas = ["0:00 Abertura"]
    for a, z in grupos:
        linhas.append(f"{mmss(inicio[a])} {rotulo(a, z)}")
    linhas.append(f"{mmss(fim)} Resultado final")
    return "\n".join(linhas)


def fundo_azul():
    return b.gradient(b.TEAL, b.NAVY).convert("RGBA")


def fundo_campo():
    sys.path.insert(0, JOGADORES)
    import importlib
    bf = importlib.import_module("build_futebol")
    return bf.campo().convert("RGBA")


def thumb(fundo, linha1, linha2, tiles, pose, saida):
    img = fundo.resize((1920, 1080))
    d = ImageDraw.Draw(img)
    b.text_outline(d, (760, 170), linha1, b.font(b.F_BLACK, 150), b.WHITE, w=16)
    b.text_outline(d, (760, 360), linha2, b.font(b.F_BLACK, 170), b.YELLOW, w=18)
    b.draw_tiles(img, tiles, 640, max_w=1250, max_size=230, cx=760)
    # faixa "VOCÊ CONSEGUE?"
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([250, 830, 1270, 1000], 50, fill=b.RED, outline=b.WHITE, width=10)
    d.text((760, 915), "VOCÊ CONSEGUE?", font=b.font(b.F_BLACK, 110), fill=b.WHITE, anchor="mm")
    b.put_palito(img, pose, 900, 1600, 1075)
    b.selo(img, 1640, 90, 1.0)
    img = img.convert("RGB").resize((TW, TH), Image.LANCZOS)
    img.save(saida, quality=92)


def salvar(pasta, titulo, descricao, tags):
    out = os.path.join(pasta, "youtube")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "titulo.txt"), "w", encoding="utf-8").write(titulo + "\n")
    open(os.path.join(out, "descricao.txt"), "w", encoding="utf-8").write(descricao.strip() + "\n")
    open(os.path.join(out, "tags.txt"), "w", encoding="utf-8").write(", ".join(tags) + "\n")
    return out


def kit_paises():
    qs = json.load(open(os.path.join(PAISES, "perguntas.json"), encoding="utf-8"))
    caps = capitulos(PAISES, qs, [(1, 10), (11, 20), (21, 30), (31, 40), (41, 44)],
                     lambda a, z: f"Perguntas {a} a {z}" + (" (desafio final)" if a == 41 else ""))
    creditos = [l.replace(", via Wikimedia Commons", "") for l in open(os.path.join(PAISES, "creditos-fotos.txt"), encoding="utf-8").read().splitlines()[2:] if l.strip()]
    titulo = "Adivinhe 40 PAÍSES Sem as VOGAIS 🌍 Quiz de Geografia | Quiz Palito"
    descricao = f"""
Será que você consegue adivinhar 40 países só pelas consoantes? 🌍 As vogais sumiram e o Palito quer saber quantos você acerta! Ainda tem 4 perguntas bônus de bandeiras e capitais.

👇 Conta nos comentários quantos países você acertou!
🔔 Se inscreve no Quiz Palito e ativa o sininho para mais quizzes.

⏱️ Capítulos
{caps}

📸 Fotos: Wikimedia Commons (título, autor e licença)
""" + "\n".join(creditos) + """

#quiz #geografia #quizpalito #paises #desafio
"""
    tags = ["quiz", "quiz de geografia", "adivinhe o país", "países sem vogais", "quiz de países",
            "geografia", "bandeiras", "capitais", "desafio", "quiz palito", "teste seus conhecimentos",
            "quiz em português"]
    out = salvar(PAISES, titulo, descricao, tags)
    thumb(fundo_azul(), "40 PAÍSES", "SEM VOGAIS", "BR_S_L", "assustado", os.path.join(out, "thumbnail.jpg"))
    return out


def kit_jogadores():
    qs = json.load(open(os.path.join(JOGADORES, "perguntas.json"), encoding="utf-8"))
    L = {q["n"]: q["letra"] for q in qs}
    caps = capitulos(JOGADORES, qs, [(1, 6), (7, 12), (13, 18), (19, 24), (25, 26)],
                     lambda a, z: f"Letras {L[a]} a {L[z]}")
    titulo = "Você Lembra um JOGADOR de A até Z? ⚽ Quiz de Futebol | Quiz Palito"
    descricao = f"""
Você consegue lembrar um jogador de futebol para cada letra do alfabeto? ⚽ De A até Z, vale craque de hoje e lenda das antigas! O Palito duvida que você chega no Z sem travar.

👇 Conta nos comentários até que letra você chegou!
🔔 Se inscreve no Quiz Palito e ativa o sininho para mais quizzes.

⏱️ Capítulos
{caps}

#quiz #futebol #quizdefutebol #quizpalito #desafio
"""
    tags = ["quiz", "quiz de futebol", "jogadores de a a z", "futebol", "desafio de futebol",
            "craques do futebol", "seleção brasileira", "quiz palito", "teste seus conhecimentos",
            "quiz em português"]
    out = salvar(JOGADORES, titulo, descricao, tags)
    thumb(fundo_campo(), "JOGADORES", "DE A ATÉ Z", "A/Z", "assustado", os.path.join(out, "thumbnail.jpg"))
    return out


if __name__ == "__main__":
    print(kit_paises())
    print(kit_jogadores())
