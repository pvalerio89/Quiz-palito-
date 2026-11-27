"""Peças de engajamento usadas nos vídeos longos e nos Shorts (pedido do Patrick, 2026-11-10):

- `faixa_gancho`: a chamada aparece numa faixa vermelha POR CIMA da 1ª pergunta, já no primeiro segundo
  (não existe mais tela de abertura parada antes do primeiro desafio);
- `pontos`: placar de bolinhas (quantas já foram / qual é a atual) + "CONTA SEUS PONTOS!";
- `mais_um`: selo "+1 SE ACERTOU!" que pula na resposta, para a pessoa ir somando e comentar a nota no fim;
- `chamada_anotar`: fala do início dos vídeos de ANOTAR/ESCOLHER ("Monte o seu clube" etc.): curtir e ir anotando
  nos comentários, para enviar no fim (Patrick, 2026-11-12). Varia a frase.
Funciona em 16:9 e 9:16 (as posições vêm de quem chama).
"""
import math, os, sys
from PIL import Image, ImageDraw

_V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_V, "01-paises-sem-vogais"))
import build as b

_cache = {}

# Vídeos de anotar/escolher: chamada no começo (Patrick, 2026-11-12). Sempre com as 3 ideias:
# deixar o like, abrir os comentários e ir anotando, enviar quando o vídeo acabar.
# 2026-11-19: Patrick não quer "coração"/"joinha" na fala; é "deixe seu like" (e "se inscreva no canal").
CHAMADAS_ANOTAR = [
    "Antes de começar: se inscreva no canal, deixe seu like e abre os comentários pra ir anotando. Terminou o vídeo, é só enviar!",
    "Já deixa seu like, abre os comentários e vai anotando cada escolha. Quando o vídeo acabar, é só enviar!",
    "Dica: deixe seu like e abre os comentários agora. Vai anotando aí e, no final, é só mandar!",
    "Deixe seu like, abre os comentários e vai escrevendo suas escolhas. Terminou o vídeo? É só enviar!",
    "Primeiro, o like! Depois abre os comentários e vai anotando. No fim do vídeo, é só apertar enviar!",
    "Abre os comentários e vai anotando junto comigo, e não esquece de deixar seu like! Acabou o vídeo, é só enviar!",
]


def chamada_anotar(usadas=(), seed=None):
    """Uma frase de CHAMADAS_ANOTAR que não esteja em `usadas` (as dos últimos vídeos)."""
    import random
    livres = [c for c in CHAMADAS_ANOTAR if c not in usadas] or CHAMADAS_ANOTAR
    return random.Random(seed).choice(livres)


def pula(x):
    x = min(max(x, 0.0), 1.0)
    return 1 + 2.9 * (x - 1) ** 3 + 1.9 * (x - 1) ** 2


def _colar(img, sp, cx, cy, sc=1.0):
    if sc <= 0.02:
        return
    if abs(sc - 1) > 1e-3:
        sp = sp.resize((max(1, int(sp.width * sc)), max(1, int(sp.height * sc))), Image.BILINEAR)
    img.alpha_composite(sp, (int(cx - sp.width / 2), int(cy - sp.height / 2)))


def _faixa_sprite(txt, larg, size, cor):
    k = ("faixa", txt, larg, size, cor)
    if k not in _cache:
        d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        linhas = txt.split("\n")
        f = b.font(b.F_BLACK, size)
        while max(d0.textlength(l, font=f) for l in linhas) > larg - 80 and f.size > 30:
            f = b.font(b.F_BLACK, f.size - 2)
        alt = int(f.size * 1.15 * len(linhas) + f.size * 0.9)
        sp = Image.new("RGBA", (larg + 40, alt + 40), (0, 0, 0, 0))
        d = ImageDraw.Draw(sp)
        d.rounded_rectangle([26, 30, larg + 26, alt + 30], 46, fill=(0, 0, 0, 110))
        d.rounded_rectangle([20, 20, larg + 20, alt + 20], 46, fill=cor, outline=b.WHITE, width=9)
        y0 = 20 + alt / 2 - (len(linhas) - 1) * f.size * 0.575
        for i, l in enumerate(linhas):
            d.text((20 + larg / 2, y0 + i * f.size * 1.15), l, font=f, fill=b.WHITE if i == 0 else b.YELLOW,
                   anchor="mm", stroke_width=max(4, f.size // 12), stroke_fill=b.NAVY)
        _cache[k] = sp
    return _cache[k]


def faixa_gancho(img, cx, cy, txt, t, dur, larg=1300, size=84, cor=b.RED):
    """Faixa da chamada sobre a 1ª pergunta: entra pulando, pulsa e sobe para fora no fim de `dur`."""
    if t >= dur:
        return
    sp = _faixa_sprite(txt, larg, size, cor)
    sc = pula(t / 0.35) * (1 + 0.03 * math.sin(t * 9))
    sai = max(0.0, (t - (dur - 0.3)) / 0.3)
    _colar(img, sp, cx, cy - sai * (cy + sp.height), sc)


def pontos(img, cx, cy, feitas, n, t=0.0, raio=22, gap=16, rotulo="CONTA SEUS PONTOS!", rotulo_size=34,
           rotulo_acima=True):
    """Bolinhas do bloco atual: já foram = amarelas com ✔, atual = branca pulsando, próximas = apagadas."""
    d = ImageDraw.Draw(img)
    passo = 2 * raio + gap
    x0 = cx - (n - 1) * passo / 2
    for i in range(n):
        x = x0 + i * passo
        r = raio
        if i < feitas:
            d.ellipse([x - r, cy - r, x + r, cy + r], fill=b.YELLOW, outline=b.NAVY, width=4)
            d.line([(x - r * 0.45, cy), (x - r * 0.1, cy + r * 0.38), (x + r * 0.5, cy - r * 0.38)],
                   fill=b.NAVY, width=max(3, r // 5))
        elif i == feitas:
            r = raio * (1.12 + 0.1 * math.sin(t * 8))
            d.ellipse([x - r, cy - r, x + r, cy + r], fill=b.WHITE, outline=b.ORANGE, width=6)
            d.text((x, cy + 1), str(i + 1), font=b.font(b.F_BLACK, int(raio * 1.1)), fill=b.NAVY, anchor="mm")
        else:
            d.ellipse([x - r, cy - r, x + r, cy + r], fill=None, outline=(230, 230, 240), width=4)
    if rotulo:
        y = cy - raio - rotulo_size * 0.9 if rotulo_acima else cy
        xr = cx if rotulo_acima else x0 - raio - 24
        d.text((xr, y), rotulo, font=b.font(b.F_BLACK, rotulo_size), fill=b.WHITE,
               anchor="mm" if rotulo_acima else "rm", stroke_width=4, stroke_fill=b.NAVY)


def mais_um(img, cx, cy, tt, size=46):
    """Selo '+1 SE ACERTOU!' que pula na resposta (a partir de 0,35 s)."""
    sc = pula((tt - 0.35) / 0.3)
    if sc <= 0.02:
        return
    sp = _faixa_sprite("+1 SE ACERTOU!", int(size * 9.2), size, (40, 170, 70))
    _colar(img, sp, cx, cy + 4 * math.sin(tt * 6), sc)


def intro_rapida_frames(fundo_fn, linhas, dur, W, H, cy0, passo, tamanhos, palito, selo, imagens=(), img_y=None,
                        img_lado=180):
    """Intro RAPIDINHA (2 a 3 s; Patrick, 2026-11-10): selo + título do tema pulando linha a linha, fotos do tema
    e o Palito acenando. Depois dela vem a transição direto para a 1ª pergunta.
    fundo_fn(t) -> imagem RGBA do fundo andando; linhas = [(texto, cor)]; tamanhos = fonte de cada linha;
    palito = (altura, cx, base); selo = (cx, cy, escala); imagens = fotos RGBA quadradas (já no tamanho)."""
    fs = [b.font(b.F_BLACK, s) for s in tamanhos]
    for i in range(int(dur * 30)):
        t = i / 30
        img = fundo_fn(t)
        d = ImageDraw.Draw(img)
        if pula(t / 0.3) > 0.1:
            b.selo(img, selo[0], selo[1], selo[2] * pula(t / 0.3))
        for k, (txt, cor) in enumerate(linhas):
            sc = pula((t - 0.1 - 0.12 * k) / 0.3)
            if sc <= 0.02:
                continue
            f = fs[k] if abs(sc - 1) < 0.02 else b.font(b.F_BLACK, max(8, int(fs[k].size * sc)))
            while d.textlength(txt, font=f) > W - 120 and f.size > 30:
                f = b.font(b.F_BLACK, f.size - 4)
            b.text_outline(d, (W // 2, cy0 + k * passo), txt,
                           f, cor, w=max(6, f.size // 10))
        n = len(imagens)
        for k, im in enumerate(imagens):
            sc = pula((t - 0.35 - 0.08 * k) / 0.3)
            if sc <= 0.02:
                continue
            x = W / 2 + (k - (n - 1) / 2) * (img_lado + 40)
            sp = Image.new("RGBA", (img_lado + 20, img_lado + 20), (0, 0, 0, 0))
            ImageDraw.Draw(sp).rounded_rectangle([0, 0, img_lado + 19, img_lado + 19], 26, fill=b.WHITE,
                                                 outline=b.NAVY, width=6)
            sp.alpha_composite(im.resize((img_lado, img_lado)), (10, 10))
            _colar(img, sp, x, img_y + 6 * math.sin(t * 4 + k), sc * (1 + 0.04 * math.sin(t * 5 + k)))
        ent = min(1.0, t / 0.35)
        b.put_palito(img, "acenando", palito[0], palito[1] + int((1 - pula(ent)) * 500), palito[2],
                     -int(abs(14 * math.sin(t * 6))))
        z = 1.0 + 0.04 * t / dur
        cw, ch = W / z, H / z
        x0, y0 = (W - cw) / 2, (H - ch) / 2
        yield img.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)).convert("RGB")
