"""Gera itens.json do alfabeto de times: para cada letra, os times (escudo baixado em escudos/) e 3 alternativas
com a MESMA letra. Uso: py -3 itens.py  (só entra time cujo escudo existe)."""
import json, os, random, unicodedata, re

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = {
    "A": ["Avaí", "América-MG", "Atalanta", "Aston Villa"], "B": ["Bragantino", "Betis", "Basel"],
    "C": ["Criciúma", "Cuiabá", "CSA"], "D": ["Defensa y Justicia", "Derby County", "Danubio"],
    "E": ["Espanyol", "Emelec", "Elche"], "F": ["Figueirense", "Fulham", "Ferroviária"],
    "G": ["Guarani", "Getafe", "Gil Vicente"], "H": ["Hoffenheim", "Huracán", "Hull City"],
    "I": ["Ipatinga", "Ituano", "Ipswich"], "J": ["Joinville", "Junior Barranquilla", "Jaguares"],
    "K": ["Kashima Antlers", "Krasnodar", "Kawasaki Frontale"], "L": ["Londrina", "Lanús", "Lille"],
    "M": ["Málaga", "Mainz", "Millwall"], "N": ["Nottingham Forest", "Nantes", "Norwich"],
    "O": ["Oeste", "Osasuna", "Once Caldas"], "P": ["Paysandu", "Ponte Preta", "Paraná"],
    "Q": ["Querétaro", "Quilmes", "Qarabağ"], "R": ["Remo", "Rayo Vallecano", "Rennes"],
    "S": ["Schalke 04", "Southampton", "Sampdoria"], "T": ["Tigre", "Twente", "Toulouse"],
    "U": ["Universidad de Chile", "Unión Santa Fe", "Union Berlin"], "V": ["Vila Nova", "Vélez Sarsfield", "Verona"],
    "W": ["Watford", "Werder Bremen", "Wigan"], "X": ["Xelajú", "Xanthi", "Xavante"],
    "Y": ["Yokohama Marinos", "Yeovil", "Yverdon"], "Z": ["Zulte Waregem", "Zürich", "Zwolle"],
}
FALA = {"PSG": "Paris Saint-Germain", "PSV": "P S V", "Bayern de Munique": "Bayern de Munique"}


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def letra(n):
    return unicodedata.normalize("NFKD", n)[0].upper()


times = [l.split("\t")[0] for l in open(os.path.join(HERE, "escudos.tsv"), encoding="utf-8").read().splitlines() if l.strip()]
cred = json.load(open(os.path.join(HERE, "creditos.json"), encoding="utf-8"))
ok = [t for t in times if t in cred and os.path.exists(os.path.join(HERE, "escudos", slug(t) + ".png"))]
FORA = set(json.load(open(os.path.join(HERE, "fora.json"), encoding="utf-8"))) if os.path.exists(os.path.join(HERE, "fora.json")) else set()
ok = [t for t in ok if t not in FORA]
rnd = random.Random(16)
R = []
for i, t in enumerate(ok, 1):
    L = letra(t)
    pool = [x for x in times if letra(x) == L and x != t] + EXTRA[L]
    err = rnd.sample(pool, 2)
    certa = (i * 5 + rnd.randint(0, 2)) % 3
    err.insert(certa, t)
    R.append({"n": i, "nome": t, "letra": L, "escudo": slug(t) + ".png", "opcoes": err, "certa": certa,
              "fala": FALA.get(t, t)})
json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(R), "times;", "letras:", "".join(sorted({r["letra"] for r in R})))
