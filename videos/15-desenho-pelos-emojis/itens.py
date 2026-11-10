"""Gera itens.json: desenho (nome), emojis (pista) e alternativas A/B/C. Ordem: do fácil ao difícil."""
import json, random
D = [
    ("Bob Esponja", "🧽🍍🌊"), ("Peppa Pig", "🐷💦👢"), ("Pokémon", "⚡🐭🔴"), ("Frozen", "❄️👸⛄"),
    ("Toy Story", "🤠🚀🧸"), ("Carros", "🚗⚡🏁"), ("O Rei Leão", "🦁👑🌅"), ("Shrek", "👹🧅🏰"),
    ("Procurando Nemo", "🐠🔎🌊"), ("Tom e Jerry", "🐱🐭🧀"), ("Scooby-Doo", "🐶👻🚐"), ("Meu Malvado Favorito", "💛👓🍌"),
    ("Turma da Mônica", "👧🐰💪"), ("Os Simpsons", "🍩💛📺"), ("Moana", "🌊🛶🐔"), ("Divertida Mente", "😀😢😡🤢"),
    ("Up: Altas Aventuras", "🎈🏠👴"), ("Patrulha Canina", "🐶🚒🚓"), ("Branca de Neve", "🍎👸⛏️"), ("Cinderela", "👠🎃👸"),
    ("Madagascar", "🦁🦓🦒🦛"), ("A Era do Gelo", "🦣🐿️🌰"), ("Ratatouille", "🐀🍲🗼"), ("Dragon Ball", "🐉🟠⭐"),
    ("Naruto", "🍥🦊🥷"), ("Kung Fu Panda", "🐼🥋🥟"), ("Zootopia", "🐰🦊🚓"), ("Lilo & Stitch", "👧👽🌺"),
    ("Os Incríveis", "🦸💪🔥"), ("Ben 10", "⌚👦👽"), ("Miraculous: Ladybug", "🐞🐱🗼"), ("Pernalonga", "🐰🥕🕳️"),
    ("Garfield", "🐱🍝😴"), ("Sonic", "🦔💨💍"), ("Super Mario Bros.", "🍄⭐🐢"), ("A Pequena Sereia", "🧜🦀🐚"),
    ("Aladdin", "🧞🐒🕌"), ("Pinóquio", "🤥👃🦗"), ("Dumbo", "🐘👂🎪"), ("Monstros S.A.", "👁️🚪👧"),
    ("Wall-E", "🤖🌱🌎"), ("Hora de Aventura", "🐶👦🗡️"), ("Os Smurfs", "💙🍄🏠"), ("Popeye", "💪🥬⚓"),
    ("Viva: A Vida é uma Festa", "💀🎸🌼"), ("Encanto", "🦋🏠🕯️"), ("Enrolados", "💇🍳🏰"), ("Valente", "🏹🐻👸"),
    ("Luca", "🐟👦🛵"), ("Hércules", "💪⚡🏛️"), ("Tarzan", "🦍🌴🧔"), ("A Bela e a Fera", "🌹📚🕰️"),
    ("Mogli", "🐻🐯👦🌴"), ("Bambi", "🦌🐰🌸"), ("Mulan", "🏯⚔️👧"), ("Pocahontas", "🦝🍃🏹"),
    ("Papa-Léguas", "🐦💨🐺"), ("Snoopy", "🐶🏠🐤"), ("Os Flintstones", "🦖🏠🪨"), ("Os Jetsons", "🚀🤖🏙️"),
    ("Coragem, o Cão Covarde", "🐶😱🏚️"), ("Phineas e Ferb", "🔺👦🦆"), ("O Incrível Mundo de Gumball", "🐱🐟🏫"),
    ("Os Padrinhos Mágicos", "🧚⭐👑"), ("Galinha Pintadinha", "🐔🔵🎶"), ("Bananas de Pijamas", "🍌🍌🛏️"),
    ("O Show da Luna", "🌙👧🔬"), ("Pato Donald", "🦆😡⛵"),
]
FALA = {"Up: Altas Aventuras": "Up, Altas Aventuras", "Lilo & Stitch": "Lilo e Stitch",
        "Viva: A Vida é uma Festa": "Viva, a Vida é uma Festa", "Miraculous: Ladybug": "Miraculous, Ladybug",
        "Super Mario Bros.": "Super Mario", "Wall-E": "Wall-i", "Monstros S.A.": "Monstros S.A."}
CURTO = {"O Incrível Mundo de Gumball": "Gumball", "Viva: A Vida é uma Festa": "Viva", "Miraculous: Ladybug": "Miraculous",
         "Up: Altas Aventuras": "Up", "Coragem, o Cão Covarde": "Coragem", "Os Padrinhos Mágicos": "Padrinhos Mágicos"}
c = lambda x: CURTO.get(x, x)
rnd = random.Random(15)
nomes = [n for n, _ in D]
R = []
for i, (n, e) in enumerate(D, 1):
    perto = nomes[max(0, i - 15):i + 14]
    errados = rnd.sample([x for x in perto if x != n], 2)
    certa = (i * 7 + rnd.randint(0, 2)) % 3
    ops = [c(x) for x in errados]
    ops.insert(certa, c(n))
    R.append({"n": i, "nome": n, "emojis": e, "opcoes": ops, "certa": certa, "fala": FALA.get(n, n)})
json.dump(R, open("itens.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(R), [r["certa"] for r in R].count(0), [r["certa"] for r in R].count(1), [r["certa"] for r in R].count(2))
