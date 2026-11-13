"""Desenha o CONTORNO de cada país (silhueta) para o vídeo 23 "Adivinhe o país pelo mapa".

Fonte: Natural Earth 1:50m admin-0 (domínio público), recortada em mapas.json (só os países usados).
Uso: py -3 mapas.py --extrair ne_50m_admin_0_countries.geojson   (refaz mapas.json a partir do Natural Earth)
     py -3 mapas.py                                            (desenha mapas/<slug>.jpg)
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "mapas")
S = 1100                      # imagem quadrada (o cartão faz fit quadrado)

# slug -> código ISO A3 do Natural Earth
PAISES = {
    "brasil": "BRA", "italia": "ITA", "australia": "AUS", "chile": "CHL", "estados-unidos": "USA",
    "argentina": "ARG", "japao": "JPN", "india": "IND", "mexico": "MEX", "reino-unido": "GBR",
    "franca": "FRA", "espanha": "ESP", "china": "CHN", "africa-do-sul": "ZAF", "canada": "CAN",
    "portugal": "PRT", "egito": "EGY", "russia": "RUS", "madagascar": "MDG", "uruguai": "URY",
    "grecia": "GRC", "cuba": "CUB", "nova-zelandia": "NZL", "alemanha": "DEU", "peru": "PER",
    "turquia": "TUR", "noruega": "NOR", "colombia": "COL", "islandia": "ISL", "arabia-saudita": "SAU",
    "paraguai": "PRY", "vietna": "VNM", "bolivia": "BOL", "polonia": "POL", "mongolia": "MNG",
    "croacia": "HRV",
    # só na intro (não estão nas perguntas)
    "tailandia": "THA", "ucrania": "UKR", "irlanda": "IRL", "venezuela": "VEN",
}
# país -> (lon_min, lat_min, lon_max, lat_max) para tirar ilhas distantes (Alasca, Havaí, Svalbard...)
CAIXA = {
    "USA": (-126, 24, -66, 50), "NOR": (4, 57, 32, 72), "FRA": (-6, 41, 10, 52), "ESP": (-10, 35, 5, 44.5),
    "PRT": (-10, 36.8, -6, 42.3), "CHL": (-76, -56, -66, -17), "NZL": (165, -48, 179, -34),
    "RUS": (19, 41, 200, 82), "ECU": (-82, -5, -75, 2), "ITA": (6, 36, 19, 47.2), "GBR": (-9, 49.8, 2, 59),
    "CAN": (-142, 41, -52, 84), "ZAF": (16, -35, 33, -22), "COL": (-80, -5, -66, 13), "AUS": (112, -44, 154, -10),
    "JPN": (128, 30, 146, 46), "IND": (67, 6, 98, 37), "VEN": (-74, 0, -59, 13), "GRC": (19, 34.7, 29, 42),
}


def extrair(geo):
    d = json.load(open(geo, encoding="utf-8"))
    por = {f["properties"]["ADM0_A3"]: f["geometry"] for f in d["features"]}
    res = {"_fonte": "Natural Earth 1:50m admin-0 countries (domínio público), naturalearthdata.com"}
    for slug, a3 in PAISES.items():
        g = por[a3]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        res[slug] = [[[round(x, 2), round(y, 2)] for x, y in p[0]] for p in polys]   # só o anel externo
    json.dump(res, open(os.path.join(HERE, "mapas.json"), "w"), separators=(",", ":"))
    print(len(res) - 1, "países")


def area(r):
    return abs(sum(r[i][0] * r[i - 1][1] - r[i - 1][0] * r[i][1] for i in range(len(r)))) / 2


def desenhar(slug, aneis, cor=(255, 140, 0)):
    a3 = PAISES[slug]
    if a3 == "RUS":   # atravessa a linha de 180°
        aneis = [[[x + 360 if x < 0 else x, y] for x, y in r] for r in aneis]
    if a3 in CAIXA:
        x0, y0, x1, y1 = CAIXA[a3]
        aneis = [r for r in aneis if all(x0 <= x <= x1 and y0 <= y <= y1 for x, y in r)]
    maior = max(area(r) for r in aneis)
    aneis = [r for r in aneis if area(r) >= maior * 0.002]
    lat0 = sum(y for r in aneis for x, y in r) / sum(len(r) for r in aneis)
    k = math.cos(math.radians(lat0))
    pts = [[(x * k, -y) for x, y in r] for r in aneis]
    xs = [p[0] for r in pts for p in r]
    ys = [p[1] for r in pts for p in r]
    bx0, by0, bx1, by1 = min(xs), min(ys), max(xs), max(ys)
    m = 110
    esc = (S - 2 * m) / max(bx1 - bx0, by1 - by0)
    ox = (S - (bx1 - bx0) * esc) / 2
    oy = (S - (by1 - by0) * esc) / 2
    SS = 2   # desenha em 2x e reduz (borda lisa)
    mask = Image.new("L", (S * SS, S * SS), 0)
    dm = ImageDraw.Draw(mask)
    for r in pts:
        dm.polygon([((x - bx0) * esc * SS + ox * SS, (y - by0) * esc * SS + oy * SS) for x, y in r], fill=255)
    mask = mask.resize((S, S), Image.LANCZOS)
    img = Image.new("RGB", (S, S), (205, 235, 255))      # "mar" azul-claro
    d = ImageDraw.Draw(img)
    for i in range(0, S, 55):                             # quadriculado leve de mapa
        d.line([(i, 0), (i, S)], fill=(188, 222, 248), width=3)
        d.line([(0, i), (S, i)], fill=(188, 222, 248), width=3)
    borda = mask.filter(ImageFilter.MaxFilter(13))
    sombra = Image.new("L", (S, S), 0)
    sombra.paste(borda, (10, 14))
    img.paste((120, 160, 200), (0, 0), sombra.filter(ImageFilter.GaussianBlur(8)))
    img.paste((25, 30, 70), (0, 0), borda)
    img.paste(cor, (0, 0), mask)
    img.save(os.path.join(OUT, slug + ".jpg"), quality=90)


def main():
    if "--extrair" in sys.argv:
        extrair(sys.argv[sys.argv.index("--extrair") + 1])
        return
    os.makedirs(OUT, exist_ok=True)
    M = json.load(open(os.path.join(HERE, "mapas.json")))
    for slug in PAISES:
        desenhar(slug, M[slug])
    print(len(PAISES), "mapas em", OUT)


if __name__ == "__main__":
    main()
