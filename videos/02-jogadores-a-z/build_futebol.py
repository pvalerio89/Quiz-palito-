"""Quiz Palito — "Jogadores de A a Z". Reaproveita o build.py e troca as telas por um tema de futebol.

Uso: py -3 build_futebol.py assets saida.mp4
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFilter
import build as b

QP = next(p for p in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * k)) for k in range(1, 6)] if os.path.basename(p) == "Quiz Palito")  # pasta raiz do projeto
HERE = os.path.dirname(os.path.abspath(__file__))
b.PERSONAGEM = os.path.join(QP, "personagem")
QS = json.load(open(os.path.join(HERE, "perguntas.json"), encoding="utf-8"))
BY_N = {q["n"]: q for q in QS}
for q in QS:
    q["answer"] = str(q["n"])  # o build passa isso pro reveal; usamos pra achar a pergunta
b.QUESTIONS = QS

W, H = b.W, b.H
G1, G2 = (46, 140, 62), (38, 120, 52)
LINE = (255, 255, 255, 70)
_bg = None


def campo():
    """Gramado com faixas e linhas do campo."""
    global _bg
    if _bg is not None:
        return _bg.copy()
    img = Image.new("RGB", (W, H), G1)
    d = ImageDraw.Draw(img)
    stripe = 160
    for i in range(0, W, stripe * 2):
        d.rectangle([i + stripe, 0, i + 2 * stripe, H], fill=G2)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rectangle([40, 40, W - 40, H - 40], outline=LINE, width=8)
    ld.line([W // 2, 40, W // 2, H - 40], fill=LINE, width=8)
    ld.ellipse([W // 2 - 190, H // 2 - 190, W // 2 + 190, H // 2 + 190], outline=LINE, width=8)
    ld.rectangle([40, H // 2 - 260, 300, H // 2 + 260], outline=LINE, width=8)
    ld.rectangle([W - 300, H // 2 - 260, W - 40, H // 2 + 260], outline=LINE, width=8)
    img = img.convert("RGBA")
    img.alpha_composite(lay)
    # escurece as bordas para o texto aparecer melhor
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).rectangle([0, 0, W, H], fill=0)
    ImageDraw.Draw(vig).ellipse([-300, -250, W + 300, H + 250], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(160))
    dark = Image.new("RGBA", (W, H), (0, 30, 10, 150))
    dark.putalpha(Image.eval(vig, lambda v: int((255 - v) * 0.6)))
    img.alpha_composite(dark)
    _bg = img.convert("RGB")
    return _bg.copy()


def topo(img, n):
    d = ImageDraw.Draw(img)
    d.ellipse([50, 40, 200, 190], fill=b.ORANGE, outline=b.WHITE, width=8)
    d.text((125, 112), f"{n:02d}", font=b.font(b.F_BLACK, 70), fill=b.WHITE, anchor="mm")
    b.selo(img, 1690, 112, 0.75)


def letra_tile(img, letra, cx, cy, size):
    b.shadowed_round_rect(img, (cx - size // 2, cy - size // 2, cx + size // 2, cy + size // 2), int(size * 0.14), b.WHITE)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - size // 2 + 14, cy - size // 2 + 14, cx + size // 2 - 14, cy + size // 2 - 14],
                        int(size * 0.11), outline=b.YELLOW, width=10)
    d.text((cx, cy - int(size * 0.03)), letra, font=b.font(b.F_BLACK, int(size * 0.72)), fill=b.NAVY, anchor="mm")


def question_base(q):
    img = campo().convert("RGBA")
    topo(img, q["n"])
    d = ImageDraw.Draw(img)
    b.text_outline(d, (900, 230), "UM JOGADOR QUE COMECE COM…", b.font(b.F_BLACK, 80), b.YELLOW, w=10)
    letra_tile(img, q["letra"], 860, 560, 400)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = b.BAR
    d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 40, fill=b.WHITE)
    d.rounded_rectangle(b.BAR, 32, fill=(60, 70, 110))
    return img.convert("RGB")


def reveal_base(q):
    img = campo().convert("RGBA")
    topo(img, q["n"])
    d = ImageDraw.Draw(img)
    b.text_outline(d, (900, 215), "ALGUMAS RESPOSTAS:", b.font(b.F_BLACK, 84), b.YELLOW, w=10)
    letra_tile(img, q["letra"], 250, 620, 230)
    d = ImageDraw.Draw(img)
    for i, nome in enumerate(q["nomes"]):
        y = 340 + i * 175
        d.rounded_rectangle([440, y + 8, 1520, y + 148], 46, fill=b.NAVY)
        d.rounded_rectangle([430, y, 1510, y + 140], 46, fill=b.GREEN, outline=b.WHITE, width=8)
        d.ellipse([452, y + 22, 548, y + 118], fill=b.WHITE, outline=b.NAVY, width=6)
        d.text((500, y + 70), str(i + 1), font=b.font(b.F_BLACK, 60), fill=b.NAVY, anchor="mm")
        f = b.font(b.F_BLACK, 76)
        while d.textlength(nome, font=f) > 860:
            f = b.font(b.F_BLACK, f.size - 4)
        b.text_outline(d, (1025, y + 70), nome, f, b.WHITE, outline=b.NAVY, w=6)
    return img.convert("RGB")


def reveal_frames(_photo, answer, dur):
    q = BY_N[int(answer)]
    base = reveal_base(q)
    for i in range(int(dur * b.FPS)):
        t = i / b.FPS
        img = base.copy()
        # nomes aparecem um por um (cobre com o fundo os que ainda não entraram)
        shown = 1 + int(t / 0.35)
        if shown < 3:
            bg = campo()
            for k in range(shown, 3):
                y = 340 + k * 175
                img.paste(bg.crop((420, y - 4, 1530, y + 160)), (420, y - 4))
        img = img.convert("RGBA")
        slide = min(1.0, t / 0.35)
        b.put_palito(img, "comemorando", 430, 1730, 1060, int((1 - slide) * 500 + 6 * math.sin(t * 8)))
        yield img.convert("RGB")


def burst_bg(rot):
    img = Image.new("RGB", (W, H), G1)
    d = ImageDraw.Draw(img)
    cx, cy, R = W / 2, H / 2, 2400
    for i in range(24):
        a0, a1 = math.radians(i * 15 + rot), math.radians(i * 15 + 7.5 + rot)
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)),
                   (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=(70, 175, 85) if i % 2 else (40, 130, 55))
    return img


def intro_base():
    img = campo().convert("RGBA")
    b.selo(img, 820, 120, 1.25)
    d = ImageDraw.Draw(img)
    b.text_outline(d, (780, 330), "VOCÊ LEMBRA UM JOGADOR", b.font(b.F_BLACK, 92), b.WHITE, w=11)
    b.text_outline(d, (820, 490), "DE A ATÉ Z?", b.font(b.F_BLACK, 150), b.YELLOW, w=14)
    b.draw_tiles(img, "ABC/Z", 760, max_size=150, cx=820)
    b.put_palito(img, "acenando", 700, 1640, 1050)
    return img.convert("RGB")


def outro_base():
    img = campo().convert("RGBA")
    d = ImageDraw.Draw(img)
    b.text_outline(d, (800, 300), "CHEGOU ATÉ O Z?", b.font(b.F_BLACK, 120), b.YELLOW, w=12)
    b.text_outline(d, (800, 450), "CONTA NOS COMENTÁRIOS!", b.font(b.F_BLACK, 86), b.WHITE, w=10)
    b.text_outline(d, (800, 640), "INSCREVA-SE NO", b.font(b.F_BLACK, 70), b.WHITE, w=8)
    b.selo(img, 800, 770, 1.4)
    b.put_palito(img, "acenando", 650, 1650, 1040)
    return img.convert("RGB")


b.question_base = question_base
b.reveal_frames = reveal_frames
b.burst_bg = burst_bg
b.intro_base = intro_base
b.outro_base = outro_base

if __name__ == "__main__":
    b.main()
