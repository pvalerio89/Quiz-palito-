import json, os, sys
from boneco import *
from boneco import _extras_outside
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
jobs = []
import re
def job(s, name, t=False):
    w,h=map(int,re.search(r'width="(\d+)" height="(\d+)"',s).groups()); jobs.append(dict(svg=s, out=f"{OUT}/{name}.png", w=w, h=h, transparent=t))
def label(x, y, txt, size=34):
    return f'<text x="{x}" y="{y}" font-family="Inter Display" font-weight="800" font-size="{size}" fill="{INK}" text-anchor="middle">{txt}</text>'
def sheet(body, labels, w, h, fundo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs>{WOBBLE.format(seed=7)}</defs>'
            f'<rect width="{w}" height="{h}" fill="{fundo}"/><g filter="url(#w)">{body}</g>{labels}</svg>')

# 1) vistas
vistas = [("frente", "Frente"), ("3/4", "3/4"), ("lado", "Lado"), ("costas", "Costas")]
body = labels = ""
for i, (v, n) in enumerate(vistas):
    x = 250 + i * 470
    body += f'<g transform="translate({x} 900) scale(1.0)">{desenhar(expressao="feliz", vista=v)}</g>'
    labels += label(x, 980, n, 44)
    job(svg(f'<g transform="translate(400 760)">{desenhar(expressao="feliz", vista=v)}</g>'), "vista-" + v.replace("/", "-"), t=True)
job(sheet(body, labels + label(1040, 70, "PALITO · vistas do personagem", 54), 2080, 1040, "#DFF4FF"), "folha-vistas")

# 2) expressões (só cabeça)
names = list(EXPRESSOES)
cols = 5; cw = 420; ch = 470
body = labels = ""
for i, n in enumerate(names):
    cx = 210 + (i % cols) * cw; cy = 330 + (i // cols) * ch
    body += f'<g transform="translate({cx} {cy})">{cabeca(n)}{_extras_outside(EXPRESSOES[n]["extras"], 0, 0, 0)}</g>'
    labels += label(cx, cy + 205, NOMES_PT[n], 38)
    job(svg(f'<g transform="translate(400 430)">{cabeca(n)}{_extras_outside(EXPRESSOES[n]["extras"], 0, 0, 0)}</g>'), "rosto-" + n, t=True)
W = cols * cw; H = 130 + 3 * ch
job(sheet(body, labels + label(W / 2, 80, "PALITO · 15 expressões", 54), W, H, "#DFF4FF"), "folha-expressoes")

# 3) expressões de lado e 3/4 (mostra que o rosto acompanha a cabeça)
sel = ["feliz", "desconfiado", "medo", "bravo", "rindo"]
body = labels = ""
for i, n in enumerate(sel):
    for j, yaw in enumerate((0.5, 1.0)):
        cx = 210 + i * 420; cy = 300 + j * 420
        body += f'<g transform="translate({cx} {cy})">{cabeca(n, yaw)}</g>'
    labels += label(210 + i * 420, 960, NOMES_PT[n], 38)
job(sheet(body, labels, 2100, 1010, "#DFF4FF"), "folha-expressoes-3-4-e-lado")

# 4) poses
poses = [("acenando", "feliz", "Acenando"), ("comemorando", "rindo", "Comemorando"), ("apontando", "convencido", "Apontando"),
         ("pensando", "pensativo", "Pensando"), ("maos_na_cintura", "bravo", "Mãos na cintura"), ("assustado", "medo", "Assustado")]
body = labels = ""
for i, (p, e, n) in enumerate(poses):
    x = 260 + i * 470
    body += f'<g transform="translate({x} 920)">{desenhar(p, e)}</g>'
    labels += label(x, 1000, n, 40)
    job(svg(f'<g transform="translate(400 760)">{desenhar(p, e)}</g>'), "pose-" + p, t=True)
job(sheet(body, labels + label(1410, 80, "PALITO · poses", 54), 2820, 1060, "#DFF4FF"), "folha-poses")
json.dump(jobs, open("jobs.json", "w"))
