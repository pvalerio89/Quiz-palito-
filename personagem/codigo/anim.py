"""teste de animação: Palito entra andando de lado, vira de frente, acena e muda de expressão."""
import json, math, os, sys
from boneco import *
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
FPS = 24; W = H = 720
jobs = []
frames = []
def lerp(a, b, t): return a + (b - a) * t
def ease(t): return t * t * (3 - 2 * t)
N = FPS * 7
for f in range(N):
    t = f / FPS
    expr = "feliz"; yaw = 1.0; pose = None; x = 360; tilt = 0
    if t < 2.5:   # andando de lado
        p = t * 2 * math.pi * 1.6
        s = math.sin(p)
        pose = dict(perna_d=(28 * s, -45 * max(0, math.sin(p - 1.2))), perna_e=(-28 * s, -45 * max(0, math.sin(p + math.pi - 1.2))),
                    braco_d=(-24 * s, 25), braco_e=(24 * s, 25), pulo=-6 + 8 * abs(math.cos(p)))
        x = lerp(-150, 360, t / 2.5); tilt = 4
    elif t < 3.1:  # vira de frente
        k = ease((t - 2.5) / 0.6); yaw = 1 - k
        a = POSES["parado_lado"]; b = POSES["parado_frente"]
        pose = {key: tuple(lerp(a[key][i], b[key][i], k) for i in range(2)) for key in a}
    elif t < 5.0:  # acena com piscadinha
        yaw = 0; expr = "piscando"
        w = math.sin((t - 3.1) * 2 * math.pi * 2.2)
        k = ease(min(1, (t - 3.1) / 0.3))
        base = POSES["parado_frente"]
        pose = dict(base, braco_d=(lerp(28, 95, k), lerp(14, 50 + 30 * w, k)))
    else:          # leva um susto
        yaw = 0
        k = ease(min(1, (t - 5.0) / 0.15))
        expr = "surpreso" if t < 5.4 else "medo"
        a = POSES["parado_frente"]; b = POSES["assustado"]
        pose = {key: (tuple(lerp(a[key][i], b[key][i], k) for i in range(2)) if key != "pulo" else 0) for key in b}
        pose["pulo"] = 40 * math.sin(min(1, (t - 5.0) / 0.4) * math.pi) if t < 5.4 else 0
        x = 360 + (4 * math.sin(t * 90) if t > 5.4 else 0)
    vista = "lado" if yaw > 0.8 else ("frente" if yaw == 0 else "3/4")
    body = f'<g transform="translate({x:.1f} 660) scale(0.82)">{desenhar(pose, expr, vista, yaw=yaw)}</g>'
    ground = f'<rect y="660" width="{W}" height="{H - 660}" fill="#BCE6FA"/>'
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs>{WOBBLE.format(seed=7 + (f // 3) % 3)}</defs>'
         f'<rect width="{W}" height="{H}" fill="#DFF4FF"/>{ground}<g filter="url(#w)">{body}</g></svg>')
    jobs.append(dict(svg=s, out=f"{OUT}/f{f:04d}.png", w=W, h=H))
json.dump(jobs, open("jobs_anim.json", "w"))
