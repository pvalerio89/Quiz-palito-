"""Palito, o mascote do Quiz Palito: boneco montado em partes para animar.

desenhar(pose, expressao, vista) devolve o <g> SVG do boneco com os pés na origem (0,0).
- vista: "frente", "3/4", "lado", "costas"  (yaw 0, 0.5, 1, costas)
- pose: dict com ângulos (graus, 0 = apontando pra baixo, positivo = para a direita da tela)
- expressao: nome de EXPRESSOES ou dict próprio
"""
import math

INK = "#1B1B2F"
FAR = "#55566E"   # membros do lado de trás (vista lateral)
SKIN = "#FFFFFF"
BLUSH = "#FF8FA3"
TONGUE = "#FF6F7D"
MOUTH = "#7A1F2B"

# proporções (px)
HEAD_R = 140
TORSO = 150
UPPER_ARM, LOWER_ARM = 70, 68
THIGH, SHIN = 64, 64
FOOT = 34
HIP_Y = -(THIGH + SHIN)
NECK_Y = HIP_Y - TORSO
SHOULDER_Y = NECK_Y + 42
HEAD_Y = NECK_Y - HEAD_R + 4
LIMB_W, HEAD_W = 24, 22

POSES = {
    "parado_frente": dict(braco_d=(28, 14), braco_e=(-28, -14), perna_d=(13, 0), perna_e=(-13, 0)),
    "parado_lado": dict(braco_d=(6, 22), braco_e=(-4, 18), perna_d=(4, 0), perna_e=(-4, 0)),
    "acenando": dict(braco_d=(95, 50), braco_e=(-28, -14), perna_d=(13, 0), perna_e=(-13, 0)),
    "comemorando": dict(braco_d=(105, 20), braco_e=(-105, -20), perna_d=(18, 0), perna_e=(-18, 0), pulo=40),
    "apontando": dict(braco_d=(95, 0), braco_e=(-28, -14), perna_d=(13, 0), perna_e=(-13, 0)),
    "pensando": dict(braco_d=(35, 135), braco_e=(-35, 80), perna_d=(10, 0), perna_e=(-10, 0)),
    "maos_na_cintura": dict(braco_d=(55, -95), braco_e=(-55, 95), perna_d=(16, 0), perna_e=(-16, 0)),
    "assustado": dict(braco_d=(80, 70), braco_e=(-80, -70), perna_d=(20, -12), perna_e=(-20, 12), pulo=25),
}

# ---------- expressões ----------
def olho(t="aberto", ry=44, px=0, py=0, pr=19, lid=0.0, blid=0.0):
    return dict(t=t, ry=ry, px=px, py=py, pr=pr, lid=lid, blid=blid)

EXPRESSOES = {
    "feliz": dict(e=olho(px=4, py=8), d=olho(px=4, py=8), be=(0, -6), bd=(0, 6), boca="sorriso", extras=["bochecha"]),
    "piscando": dict(e=olho(px=10, py=10), d=olho("piscada"), be=(0, -12), bd=(6, 8), boca="lingua", extras=["bochecha"]),
    "desconfiado": dict(e=olho(px=20, py=4, lid=0.5, blid=0.15), d=olho(px=20, py=4, lid=0.5, blid=0.15),
                        be=(12, 10), bd=(-14, -18), boca="reta_lado", extras=[]),
    "medo": dict(e=olho(ry=50, px=0, py=0, pr=9), d=olho(ry=50, px=0, py=0, pr=9), be=(-22, -28), bd=(-22, 28),
                 boca="medo", extras=["suor", "suor2", "tremor"]),
    "surpreso": dict(e=olho(ry=50, pr=15), d=olho(ry=50, pr=15), be=(-34, 0), bd=(-34, 0), boca="o", extras=["bochecha"]),
    "bravo": dict(e=olho(py=6, lid=0.3), d=olho(py=6, lid=0.3), be=(16, 28), bd=(16, -28), boca="dentes", extras=["raiva"]),
    "triste": dict(e=olho(py=12, lid=0.2), d=olho(py=12, lid=0.2), be=(-10, -22), bd=(-10, 22), boca="triste", extras=["lagrima"]),
    "rindo": dict(e=olho("x_e"), d=olho("x_d"), be=(-12, -10), bd=(-12, 10), boca="gargalhada", extras=["lagrimas_riso", "bochecha"]),
    "apaixonado": dict(e=olho("coracao"), d=olho("coracao"), be=(-8, -6), bd=(-8, 6), boca="sorriso", extras=["bochecha", "coracoes"]),
    "confuso": dict(e=olho(ry=50, px=10, py=10, pr=20), d=olho(ry=36, px=8, py=8, pr=15), be=(-26, -14), bd=(8, 12),
                    boca="ondulada", extras=["interrogacao", "suor"]),
    "pensativo": dict(e=olho(px=14, py=-20), d=olho(px=14, py=-20), be=(-12, -6), bd=(2, 14), boca="hmm", extras=[]),
    "dormindo": dict(e=olho("fechado"), d=olho("fechado"), be=(4, 0), bd=(4, 0), boca="o_pequeno", extras=["zzz", "bochecha"]),
    "convencido": dict(e=olho(px=-8, py=6, lid=0.45), d=olho(px=-8, py=6, lid=0.45), be=(4, -14), bd=(-14, 8),
                       boca="sorrisinho", extras=["bochecha"]),
    "tonto": dict(e=olho("espiral"), d=olho("espiral"), be=(-14, -10), bd=(-14, 10), boca="lingua_tonta", extras=["estrelas"]),
    "chorando": dict(e=olho("fechado_triste"), d=olho("fechado_triste"), be=(-14, -24), bd=(-14, 24), boca="choro",
                     extras=["cascata"]),
}

NOMES_PT = {"feliz": "Feliz", "piscando": "Piscando", "desconfiado": "Desconfiado", "medo": "Medo",
            "surpreso": "Surpreso", "bravo": "Bravo", "triste": "Triste", "rindo": "Rindo", "apaixonado": "Apaixonado",
            "confuso": "Confuso", "pensativo": "Pensativo", "dormindo": "Dormindo", "convencido": "Convencido",
            "tonto": "Tonto", "chorando": "Chorando"}

EYE_POS = {"e": (-50, -18), "d": (54, -18)}
BROW_Y = -84
MOUTH_POS = (2, 58)

_uid = [0]
def _id():
    _uid[0] += 1
    return f"p{_uid[0]}"


def _fx(x, yaw):
    """posição horizontal de um traço do rosto quando a cabeça gira."""
    return x * (1 - 0.62 * abs(yaw)) + yaw * 82


def _eye_svg(o, side, yaw):
    bx, by = EYE_POS[side]
    x = _fx(bx, yaw)
    far = (side == "e" and yaw > 0) or (side == "d" and yaw < 0)
    if far and abs(yaw) > 0.8:
        return ""
    sx = 1 - (0.55 if far else 0.35) * abs(yaw)
    rx = 36
    t = o["t"]
    g = [f'<g transform="translate({x:.1f} {by}) scale({sx:.3f} 1)">']
    S = f'stroke="{INK}" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    if t == "aberto":
        ry = o["ry"]
        cid = _id()
        g.append(f'<clipPath id="{cid}"><ellipse rx="{rx}" ry="{ry}"/></clipPath>')
        g.append(f'<ellipse rx="{rx}" ry="{ry}" fill="#fff"/>')
        g.append(f'<g clip-path="url(#{cid})">')
        g.append(f'<circle cx="{o["px"]}" cy="{o["py"]}" r="{o["pr"]}" fill="{INK}"/>')
        g.append(f'<circle cx="{o["px"] - o["pr"] * .35:.1f}" cy="{o["py"] - o["pr"] * .4:.1f}" r="{max(3, o["pr"] * .3):.1f}" fill="#fff"/>')
        if o["lid"]:
            ly = -ry + 2 * ry * o["lid"]
            g.append(f'<rect x="-50" y="-60" width="100" height="{ly + 60:.1f}" fill="{SKIN}"/>')
            g.append(f'<line x1="-40" y1="{ly:.1f}" x2="40" y2="{ly:.1f}" stroke="{INK}" stroke-width="10"/>')
        if o["blid"]:
            ly = ry - 2 * ry * o["blid"]
            g.append(f'<rect x="-50" y="{ly:.1f}" width="100" height="60" fill="{SKIN}"/>')
            g.append(f'<line x1="-40" y1="{ly:.1f}" x2="40" y2="{ly:.1f}" stroke="{INK}" stroke-width="8"/>')
        g.append('</g>')
        g.append(f'<ellipse rx="{rx}" ry="{ry}" fill="none" stroke="{INK}" stroke-width="11"/>')
    elif t == "piscada":
        g.append(f'<path d="M-30 6 q30 -26 60 0" {S} stroke-width="13"/>')
    elif t == "fechado":
        g.append(f'<path d="M-28 0 q28 22 56 0" {S} stroke-width="12"/>')
    elif t == "fechado_triste":
        g.append(f'<path d="M-28 4 q28 -18 56 0" {S} stroke-width="12"/>')
    elif t in ("x_e", "x_d"):
        d = "M-24 -20 L22 0 L-24 20" if t == "x_e" else "M24 -20 L-22 0 L24 20"
        g.append(f'<path d="{d}" {S} stroke-width="14"/>')
    elif t == "coracao":
        g.append(f'<path d="M0 30 C-50 -5 -40 -45 -14 -38 C-4 -35 0 -26 0 -20 C0 -26 4 -35 14 -38 C40 -45 50 -5 0 30z" '
                 f'fill="#FF4D6D" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>')
        g.append('<ellipse cx="-16" cy="-22" rx="7" ry="5" fill="#fff" opacity=".8"/>')
    elif t == "espiral":
        pts = []
        for i in range(70):
            a = i * 0.32
            r = 2 + i * 0.5
            pts.append(f"{r * math.cos(a):.1f},{r * math.sin(a):.1f}")
        g.append(f'<ellipse rx="{rx}" ry="40" fill="#fff" stroke="{INK}" stroke-width="10"/>')
        g.append(f'<polyline points="{" ".join(pts)}" {S} stroke-width="6"/>')
    g.append('</g>')
    return "".join(g)


def _brow_svg(side, b, yaw):
    if b is None:
        return ""
    bx, _ = EYE_POS[side]
    far = (side == "e" and yaw > 0) or (side == "d" and yaw < 0)
    if far and abs(yaw) > 0.8:
        return ""
    x = _fx(bx, yaw)
    dy, ang = b
    sx = 1 - (0.55 if far else 0.35) * abs(yaw)
    return (f'<path transform="translate({x:.1f} {BROW_Y + dy}) rotate({ang}) scale({sx:.3f} 1)" d="M-30 6 Q0 -10 30 6" '
            f'stroke="{INK}" stroke-width="13" stroke-linecap="round" fill="none"/>')


def _mouth_svg(m, yaw):
    x = _fx(MOUTH_POS[0], yaw)
    sx = 1 - 0.5 * abs(yaw)
    S = f'stroke="{INK}" stroke-linecap="round" stroke-linejoin="round"'
    p = {
        "sorriso": f'<path d="M-46 -6 Q0 46 46 -8" {S} stroke-width="12" fill="none"/>',
        "lingua": f'<path d="M-62 -4 Q0 50 66 -12" {S} stroke-width="12" fill="none"/>'
                  f'<path d="M8 20 q4 40 30 36 q22 -4 12 -42" fill="{TONGUE}" {S} stroke-width="9"/>'
                  f'<path d="M28 22 l4 20" stroke="#C94457" stroke-width="5" stroke-linecap="round"/>',
        "reta_lado": f'<path d="M-6 6 L40 -2" {S} stroke-width="12" fill="none"/>',
        "medo": f'<path d="M-44 0 Q-22 -16 0 -4 Q22 -16 44 0 Q40 40 0 40 Q-40 40 -44 0z" fill="{MOUTH}" {S} stroke-width="11"/>'
                f'<path d="M-30 -2 l8 10 l8 -10 l8 10 l8 -10 l8 10 l8 -10" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/>',
        "o": f'<ellipse cx="0" cy="12" rx="20" ry="27" fill="{MOUTH}" {S} stroke-width="11"/>',
        "dentes": f'<rect x="-44" y="-6" width="88" height="34" rx="10" fill="#fff" {S} stroke-width="11"/>'
                  f'<path d="M-44 11 H44 M-22 -6 V28 M0 -6 V28 M22 -6 V28" {S} stroke-width="5" fill="none"/>',
        "triste": f'<path d="M-36 22 Q0 -12 36 22" {S} stroke-width="12" fill="none"/>',
        "gargalhada": f'<path d="M-62 -6 Q0 -4 62 -6 Q58 82 0 84 Q-58 82 -62 -6z" fill="{MOUTH}"/>'
                      f'<path d="M-52 0 L52 0 L48 18 L-48 18z" fill="#fff"/>'
                      f'<path d="M-30 70 Q0 40 30 70 Q0 86 -30 70z" fill="{TONGUE}"/>'
                      f'<path d="M-62 -6 Q0 -4 62 -6 Q58 82 0 84 Q-58 82 -62 -6z" fill="none" {S} stroke-width="12"/>',
        "ondulada": f'<path d="M-46 4 q12 -12 24 -2 q12 10 24 -2 q12 -12 24 -2 q12 10 20 0" {S} stroke-width="11" fill="none"/>',
        "hmm": f'<path d="M10 6 Q30 -4 46 4" {S} stroke-width="12" fill="none"/><circle cx="-18" cy="8" r="0"/>',
        "o_pequeno": f'<ellipse cx="0" cy="10" rx="10" ry="13" fill="{MOUTH}" {S} stroke-width="9"/>',
        "sorrisinho": f'<path d="M-30 10 Q10 22 44 -12" {S} stroke-width="12" fill="none"/>',
        "lingua_tonta": f'<path d="M-46 0 Q0 30 46 0" {S} stroke-width="12" fill="none"/>'
                        f'<path d="M-16 14 q-6 40 18 40 q20 -2 14 -36" fill="{TONGUE}" {S} stroke-width="9"/>',
        "choro": f'<path d="M-50 30 Q-30 -10 0 -6 Q30 -10 50 30 Q0 20 -50 30z" fill="{MOUTH}" {S} stroke-width="11"/>',
    }[m]
    return f'<g transform="translate({x:.1f} {MOUTH_POS[1]}) scale({sx:.3f} 1)">{p}</g>'


def _extras_in_head(ex, yaw):
    out = []
    S = f'stroke="{INK}" stroke-linecap="round" stroke-linejoin="round"'
    for k in ex:
        if k == "bochecha":
            for side, (bx, by) in (("e", (-92, 42)), ("d", (96, 38))):
                far = (side == "e" and yaw > 0) or (side == "d" and yaw < 0)
                if far and abs(yaw) > 0.4:
                    continue
                out.append(f'<ellipse cx="{_fx(bx, yaw):.1f}" cy="{by}" rx="{20 * (1 - .4 * abs(yaw)):.1f}" ry="11" fill="{BLUSH}" opacity=".85"/>')
        elif k == "lagrima":
            x = _fx(-56, yaw)
            out.append(f'<path d="M{x:.1f} 30 q14 26 0 34 q-14 -8 0 -34z" fill="#7FD3FF" {S} stroke-width="6"/>')
        elif k == "lagrimas_riso":
            for bx, s in ((-90, -1), (96, 1)):
                x = _fx(bx, yaw)
                out.append(f'<path d="M{x:.1f} -20 q{s * 18} 18 {s * 18} 46 q0 16 -{s * 12} 12 q-{s * 10} -6 -{s * 6} -34z" fill="#7FD3FF" {S} stroke-width="6"/>')
        elif k == "cascata":
            for bx in (-50, 54):
                x = _fx(bx, yaw)
                out.append(f'<path d="M{x - 14:.1f} -10 L{x + 14:.1f} -10 L{x + 18:.1f} 140 L{x - 18:.1f} 140z" fill="#7FD3FF" stroke="{INK}" stroke-width="6" opacity=".95"/>')
        elif k == "tremor":
            pass
    return "".join(out)


def _extras_outside(ex, yaw, hx, hy):
    out = []
    S = f'stroke="{INK}" stroke-linecap="round" stroke-linejoin="round"'
    for k in ex:
        if k in ("suor", "suor2"):
            x, y = (hx + 122, hy - 96) if k == "suor" else (hx - 128, hy - 70)
            out.append(f'<path d="M{x} {y} q18 30 4 42 q-16 10 -22 -8 q-2 -14 18 -34z" fill="#7FD3FF" {S} stroke-width="7"/>')
        elif k == "tremor":
            for s in (-1, 1):
                x = hx + s * 168
                out.append(f'<path d="M{x} {hy - 40} q{s * 10} 10 0 20 q{-s * 10} 10 0 20 q{s * 10} 10 0 20" fill="none" {S} stroke-width="8"/>')
        elif k == "raiva":
            x, y = hx + 92, hy - 112
            out.append(f'<g transform="translate({x} {y})" {S} stroke="#E63946" stroke-width="11" fill="none">'
                       '<path d="M-22 -6 q14 0 14 -16"/><path d="M6 -22 q0 14 16 14"/><path d="M22 6 q-14 0 -14 16"/><path d="M-6 22 q0 -14 -16 -14"/></g>')
        elif k == "coracoes":
            for (dx, dy, s, r) in ((150, -130, 0.8, 15), (-165, -100, 0.6, -15), (175, -40, 0.5, 20)):
                out.append(f'<path transform="translate({hx + dx} {hy + dy}) scale({s}) rotate({r})" d="M0 30 C-50 -5 -40 -45 -14 -38 C-4 -35 0 -26 0 -20 C0 -26 4 -35 14 -38 C40 -45 50 -5 0 30z" fill="#FF4D6D" {S} stroke-width="8"/>')
        elif k == "interrogacao":
            out.append(f'<text x="{hx + 150}" y="{hy - 90}" font-family="Inter Display" font-weight="900" font-size="110" fill="#6C3BFF" '
                       f'stroke="{INK}" stroke-width="8" paint-order="stroke" transform="rotate(16 {hx + 150} {hy - 120})">?</text>')
        elif k == "zzz":
            for i, (dx, dy, fs) in enumerate(((128, -95, 50), (158, -140, 62), (192, -190, 76))):
                out.append(f'<text x="{hx + dx}" y="{hy + dy}" font-family="Inter Display" font-weight="900" font-size="{fs}" fill="#fff" '
                           f'stroke="{INK}" stroke-width="7" paint-order="stroke">z</text>')
        elif k == "estrelas":
            for i in range(5):
                a = -math.pi / 2 + (i - 2) * 0.5
                x, y = hx + 175 * math.cos(a), hy - 40 + 120 * math.sin(a)
                pts = " ".join(f"{x + (16 if j % 2 == 0 else 7) * math.cos(j * math.pi / 5 - math.pi / 2):.1f},"
                               f"{y + (16 if j % 2 == 0 else 7) * math.sin(j * math.pi / 5 - math.pi / 2):.1f}" for j in range(10))
                out.append(f'<polygon points="{pts}" fill="#FFC928" {S} stroke-width="5"/>')
    return "".join(out)


def cabeca(expressao="piscando", yaw=0.0, costas=False, giro=0):
    """cabeça centrada em (0,0)."""
    ex = EXPRESSOES[expressao] if isinstance(expressao, str) else expressao
    cid = _id()
    g = [f'<g transform="rotate({giro})">']
    # topete: uma mecha enrolada que mostra pra onde ele está virado
    tx = -yaw * 18 if not costas else 0
    g.append(f'<path d="M{tx:.1f} -132 C{tx - 6:.1f} -175 {tx + 38:.1f} -192 {tx + 34:.1f} -162 C{tx + 30:.1f} -146 {tx + 12:.1f} -152 {tx + 16:.1f} -166" '
             f'stroke="{INK}" stroke-width="12" fill="none" stroke-linecap="round"/>')
    g.append(f'<circle r="{HEAD_R}" fill="{SKIN}" stroke="{INK}" stroke-width="{HEAD_W}"/>')
    if not costas:
        g.append(f'<clipPath id="{cid}"><circle r="{HEAD_R - 8}"/></clipPath><g clip-path="url(#{cid})">')
        g.append(_extras_in_head([e for e in ex["extras"] if e == "bochecha"], yaw))
        g.append(_eye_svg(ex["e"], "e", yaw) + _eye_svg(ex["d"], "d", yaw))
        g.append(_brow_svg("e", ex["be"], yaw) + _brow_svg("d", ex["bd"], yaw))
        g.append(_mouth_svg(ex["boca"], yaw))
        g.append(_extras_in_head([e for e in ex["extras"] if e != "bochecha"], yaw))
        g.append('</g>')
    g.append('</g>')
    return "".join(g)


def _limb(root, a1, a2, l1, l2, color, foot=None, mao=True):
    x0, y0 = root
    r1, r2 = math.radians(a1), math.radians(a1 + a2)
    x1, y1 = x0 + l1 * math.sin(r1), y0 + l1 * math.cos(r1)
    x2, y2 = x1 + l2 * math.sin(r2), y1 + l2 * math.cos(r2)
    cx, cy = 2 * x1 - (x0 + x2) / 2, 2 * y1 - (y0 + y2) / 2
    s = (f'<path d="M{x0:.1f} {y0:.1f} Q{cx:.1f} {cy:.1f} {x2:.1f} {y2:.1f}" stroke="{color}" stroke-width="{LIMB_W}" '
         f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    if foot is not None:
        s += (f'<path d="M{x2:.1f} {y2:.1f} L{x2 + foot * FOOT:.1f} {y2 + 2:.1f}" stroke="{color}" stroke-width="{LIMB_W}" '
              f'stroke-linecap="round"/>')
    elif mao:
        s += f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="15" fill="#fff" stroke="{color}" stroke-width="9"/>'
    return s


VISTAS = {"frente": 0.0, "3/4": 0.5, "lado": 1.0, "costas": 0.0}


def desenhar(pose=None, expressao="piscando", vista="frente", yaw=None, giro_cabeca=0, inclinar=0):
    """boneco inteiro, pés em (0,0)."""
    if pose is None:
        pose = POSES["parado_lado" if vista == "lado" else "parado_frente"]
    if isinstance(pose, str):
        pose = POSES[pose]
    if yaw is None:
        yaw = VISTAS[vista]
    costas = vista == "costas"
    lado = abs(yaw) > 0.8
    up = -pose.get("pulo", 0)
    hip = (0, HIP_Y + up)
    sh = (0, SHOULDER_Y + up)
    neck = (0, NECK_Y + up)
    far_col = FAR if lado else INK
    # pés: de frente apontam pra fora; de lado/3/4 apontam pra onde ele olha
    if lado or abs(yaw) > 0.3:
        fd = fe = (1 if yaw >= 0 else -1)
    else:
        fd, fe = 1, -1
    g = [f'<g transform="rotate({inclinar} 0 {HIP_Y + up})">']
    # membros de trás
    back = []
    front = []
    legs = [("perna_d", fd), ("perna_e", fe)]
    arms = ["braco_d", "braco_e"]
    for i, (k, f) in enumerate(legs):
        a1, a2 = pose[k]
        s = _limb(hip, a1, a2, THIGH, SHIN, far_col if (lado and i == 1) else INK, foot=f)
        (back if (lado and i == 1) else front).append(s)
    for i, k in enumerate(arms):
        a1, a2 = pose[k]
        s = _limb(sh, a1, a2, UPPER_ARM, LOWER_ARM, far_col if (lado and i == 1) else INK)
        (back if (lado and i == 1) else front).append(s)
    g += back
    g.append(f'<path d="M{neck[0]} {neck[1]} Q-4 {(neck[1] + hip[1]) / 2} {hip[0]} {hip[1]}" stroke="{INK}" stroke-width="{LIMB_W}" '
             f'stroke-linecap="round" fill="none"/>')
    if costas:
        g += front
        g.append(f'<g transform="translate(0 {HEAD_Y + up})">{cabeca(expressao, 0, True, giro_cabeca)}</g>')
    else:
        g += front[:2]
        g.append(f'<g transform="translate(0 {HEAD_Y + up})">{cabeca(expressao, yaw, False, giro_cabeca)}</g>')
        g += front[2:]
    ex = EXPRESSOES[expressao] if isinstance(expressao, str) else expressao
    if not costas:
        g.append(_extras_outside(ex["extras"], yaw, 0, HEAD_Y + up))
    g.append('</g>')
    return "".join(g)


WOBBLE = ('<filter id="w" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" '
          'baseFrequency="0.012" numOctaves="1" seed="{seed}"/><feDisplacementMap in="SourceGraphic" scale="4"/></filter>')


def svg(conteudo, w=800, h=800, fundo=None, seed=7, extra_defs=""):
    bg = f'<rect width="{w}" height="{h}" fill="{fundo}"/>' if fundo else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs>{WOBBLE.format(seed=seed)}{extra_defs}</defs>{bg}<g filter="url(#w)">{conteudo}</g></svg>')
