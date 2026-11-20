"""Gera itens.json do vídeo 41 "Adivinhe o PAÍS só com as 2 primeiras letras" (estilo mais humano, 2026-11-19).

36 perguntas próprias: o cartão mostra só as DUAS primeiras letras do país e os quadradinhos das outras
(tipo forca: dá para contar quantas letras tem). As 3 alternativas A/B/C são só BANDEIRAS (sem nome); na resposta
o cartão completa o nome e cada alternativa ganha o nome do país. Nas mais difíceis, as 3 bandeiras são de países
que começam com as mesmas letras (aí é contar os quadradinhos) ou bandeiras parecidas (Irlanda x Costa do Marfim).
Bandeiras: as do vídeo 03 (domínio público). Fáceis primeiro.
Uso: py -3 itens.py   (copia as bandeiras que faltarem)
"""
import json, os, random, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)

# código da bandeira: (nome na tela, nome falado)
PAISES = {
    "br": ("BRASIL", "Brasil"), "ar": ("ARGENTINA", "Argentina"), "pt": ("PORTUGAL", "Portugal"),
    "jp": ("JAPÃO", "Japão"), "cn": ("CHINA", "China"), "kr": ("COREIA DO SUL", "Coreia do Sul"),
    "it": ("ITÁLIA", "Itália"), "ie": ("IRLANDA", "Irlanda"), "mx": ("MÉXICO", "México"),
    "us": ("ESTADOS UNIDOS", "Estados Unidos"), "gb": ("REINO UNIDO", "Reino Unido"), "ca": ("CANADÁ", "Canadá"),
    "dz": ("ARGÉLIA", "Argélia"), "am": ("ARMÊNIA", "Armênia"), "pl": ("POLÔNIA", "Polônia"), "es": ("ESPANHA", "Espanha"),
    "qa": ("CATAR", "Catar"), "cm": ("CAMARÕES", "Camarões"), "de": ("ALEMANHA", "Alemanha"), "al": ("ALBÂNIA", "Albânia"),
    "at": ("ÁUSTRIA", "Áustria"), "co": ("COLÔMBIA", "Colômbia"), "pe": ("PERU", "Peru"), "fr": ("FRANÇA", "França"),
    "nl": ("HOLANDA", "Holanda"), "ru": ("RÚSSIA", "Rússia"), "cl": ("CHILE", "Chile"), "vn": ("VIETNÃ", "Vietnã"),
    "eg": ("EGITO", "Egito"), "iq": ("IRAQUE", "Iraque"), "ye": ("IÊMEN", "Iêmen"), "sn": ("SENEGAL", "Senegal"),
    "ml": ("MALI", "Mali"), "gn": ("GUINÉ", "Guiné"), "au": ("AUSTRÁLIA", "Austrália"), "nz": ("NOVA ZELÂNDIA", "Nova Zelândia"),
    "ec": ("EQUADOR", "Equador"), "ve": ("VENEZUELA", "Venezuela"), "gr": ("GRÉCIA", "Grécia"), "uy": ("URUGUAI", "Uruguai"),
    "il": ("ISRAEL", "Israel"), "si": ("ESLOVÊNIA", "Eslovênia"), "sk": ("ESLOVÁQUIA", "Eslováquia"),
    "ma": ("MARROCOS", "Marrocos"), "mg": ("MADAGASCAR", "Madagascar"), "ne": ("NÍGER", "Níger"),
    "ni": ("NICARÁGUA", "Nicarágua"), "ng": ("NIGÉRIA", "Nigéria"), "se": ("SUÉCIA", "Suécia"), "ch": ("SUÍÇA", "Suíça"),
    "sd": ("SUDÃO", "Sudão"), "ci": ("COSTA DO MARFIM", "Costa do Marfim"), "tr": ("TURQUIA", "Turquia"),
    "tn": ("TUNÍSIA", "Tunísia"), "jm": ("JAMAICA", "Jamaica"), "za": ("ÁFRICA DO SUL", "África do Sul"),
    "ke": ("QUÊNIA", "Quênia"), "cu": ("CUBA", "Cuba"), "pa": ("PANAMÁ", "Panamá"), "no": ("NORUEGA", "Noruega"),
    "is": ("ISLÂNDIA", "Islândia"), "dk": ("DINAMARCA", "Dinamarca"), "hu": ("HUNGRIA", "Hungria"),
    "bg": ("BULGÁRIA", "Bulgária"), "kg": ("QUIRGUISTÃO", "Quirguistão"), "mw": ("MALAWI", "Malawi"),
    "th": ("TAILÂNDIA", "Tailândia"), "cr": ("COSTA RICA", "Costa Rica"), "tj": ("TADJIQUISTÃO", "Tadjiquistão"),
    "lu": ("LUXEMBURGO", "Luxemburgo"), "hr": ("CROÁCIA", "Croácia"), "rs": ("SÉRVIA", "Sérvia"),
    "py": ("PARAGUAI", "Paraguai"), "np": ("NEPAL", "Nepal"), "bt": ("BUTÃO", "Butão"), "in": ("ÍNDIA", "Índia"),
    "uz": ("UZBEQUISTÃO", "Uzbequistão"), "kz": ("CAZAQUISTÃO", "Cazaquistão"), "tm": ("TURCOMENISTÃO", "Turcomenistão"),
    "kp": ("COREIA DO NORTE", "Coreia do Norte"), "mz": ("MOÇAMBIQUE", "Moçambique"), "zw": ("ZIMBÁBUE", "Zimbábue"),
    "ao": ("ANGOLA", "Angola"), "ir": ("IRÃ", "Irã"),
}

# nome falado de cada letra (o Edge lê melhor assim)
LETRA = {"A": "á", "B": "bê", "C": "cê", "E": "é", "É": "é", "F": "éfe", "G": "gê", "H": "agá", "I": "i", "J": "jota",
         "L": "éle", "M": "ême", "N": "êne", "O": "ó", "P": "pê", "Q": "quê", "R": "érre", "S": "ésse", "T": "tê",
         "U": "u", "Ú": "u", "V": "vê", "Z": "zê", "X": "xis"}
NUM = {4: "quatro", 5: "cinco", 6: "seis", 7: "sete", 8: "oito", 9: "nove", 10: "dez", 11: "onze", 12: "doze",
       13: "treze"}

# certa, [erradas], entrada falada (antes das letras), fala da resposta, extras
P = [
    ("br", ["ar", "pt"], "Começando fácil!", "Brasil! Começou bem?", {"count": 5.0}),
    ("jp", ["cn", "kr"], "Agora uma da Ásia.", "Japão! A bolinha vermelha é o sol nascente.", {"count": 5.0}),
    ("it", ["ie", "mx"], "Essa é de comer pizza!", "Itália! Verde, branco e vermelho, em pé.", {"count": 6.0}),
    ("pt", ["pl", "es"], "Bora pra Europa.", "Portugal! O nosso irmão do outro lado do mar.", {}),
    ("ar", ["dz", "am"], "Olha aí três países com as mesmas letras!",
     "Argentina! Argélia e Armênia têm só sete letras.", {}),
    ("ca", ["qa", "cm"], "Conta os quadradinhos nessa!", "Canadá! A da folha de bordo.", {}),
    ("us", ["gb", "ca"], "Agora tem duas palavras!", "Estados Unidos! Cinquenta estrelas, uma por estado.", {}),
    ("de", ["al", "at"], "Mais uma da Europa.", "Alemanha! Preto, vermelho e amarelo.", {}),
    ("mx", ["ir", "it"], "Atenção nas cores!", "México! Parecida com a Itália, mas com a águia no meio.",
     {"aviso": "OLHA AS CORES!"}),
    ("fr", ["nl", "ru"], "Três bandeiras azul, branco e vermelho...", "França! A dela é em pé, as outras deitadas.", {}),
    ("cn", ["cl", "vn"], "Cuidado, que essa tem pegadinha!", "China! Chile também tem cinco letras, mas fica na América.",
     {"aviso": "TEM PEGADINHA!", "dica": ("Dica: fica na Ásia!", "FICA NA ÁSIA!")}),
    ("eg", ["iq", "ye"], "Agora uma da África.", "Egito! A águia dourada no meio é a de Saladino.", {}),
    ("au", ["nz", "at"], "Essa derruba muita gente!",
     "Austrália! Áustria tem só sete letras. E a da Nova Zelândia tem estrelas vermelhas.",
     {"aviso": "DERRUBA MUITA GENTE!", "suspense": True}),
    ("co", ["ec", "ve"], "Três vizinhos com as mesmas cores!", "Colômbia! Sem estrelas e sem brasão.",
     {"sabia": "A faixa amarela da Colômbia ocupa metade da bandeira."}),
    ("pe", ["ca", "at"], "Uma curtinha agora.", "Peru! Vermelho, branco e vermelho, em pé.", {}),
    ("gr", ["uy", "il"], "Listras azuis e brancas...", "Grécia! Nove listras e uma cruz no canto.", {}),
    ("ru", ["si", "sk"], "Essa é de gente grande!", "Rússia! Sem brasão. As outras duas têm escudo.",
     {"aviso": "OLHA O BRASÃO!"}),
    ("ma", ["ml", "mg"], "Mais três com as mesmas letras!", "Marrocos! Mali tem quatro letras, Madagascar tem dez.", {}),
    ("ng", ["ne", "ni"], "Vai, conta os quadradinhos!", "Nigéria! Verde, branco e verde.", {}),
    ("se", ["ch", "sd"], "Agora uma lá do norte.", "Suécia! Azul com a cruz amarela.", {}),
    ("ie", ["ci", "it"], "Cuidado, essa tem pegadinha!",
     "Irlanda! A da Costa do Marfim é igualzinha, mas com as cores ao contrário.",
     {"aviso": "TEM PEGADINHA!", "suspense": True,
      "sabia": "Na bandeira da Irlanda, o verde fica do lado do mastro."}),
    ("tr", ["tn", "cn"], "Essa é difícil, olha a dica!", "Turquia! A Tunísia tem o mesmo número de letras, mas fica na África.",
     {"aviso": "MESMO NÚMERO DE LETRAS!", "dica": ("Dica: fica entre a Europa e a Ásia!", "ENTRE A EUROPA E A ÁSIA!")}),
    ("jm", ["za", "ke"], "Agora uma do Caribe!", "Jamaica! A única bandeira sem vermelho, branco ou azul.",
     {"sabia": "A Jamaica é uma das poucas bandeiras sem vermelho, branco ou azul."}),
    ("cu", ["cl", "pa"], "Mais uma curtinha.", "Cuba! Listras azuis e o triângulo vermelho.", {}),
    ("no", ["is", "dk"], "Três cruzes parecidas... cuidado!", "Noruega! Vermelha com a cruz azul.",
     {"aviso": "TEM PEGADINHA!"}),
    ("hu", ["it", "bg"], "Faixas deitadas agora.", "Hungria! Vermelho, branco e verde.", {}),
    ("vn", ["cn", "ma"], "Uma estrela só...", "Vietnã! Vermelha com uma estrela amarela.", {}),
    ("ke", ["kg", "mw"], "Bora pra África!", "Quênia! Com o escudo e as duas lanças.", {}),
    ("th", ["cr", "tj"], "Faixas parecidas nessa!", "Tailândia! Na da Costa Rica, a faixa do meio é vermelha.", {}),
    ("hr", ["rs", "py"], "Essa tem xadrez!", "Croácia! O xadrez vermelho e branco tá no escudo.", {}),
    ("np", ["bt", "in"], "Uma bem diferente agora.", "Nepal! A única bandeira do mundo que não é retangular.",
     {"sabia": "O Nepal tem a única bandeira nacional que não é retângulo."}),
    ("kr", ["kp", "jp"], "Pegadinha! Olha quantas palavras!",
     "Coreia do Sul! A do Norte tem treze letras. Se acertou essa, você é fera!",
     {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("uz", ["kz", "tm"], "Agora as impossíveis! Três países da Ásia Central.",
     "Uzbequistão! A lua branca e as estrelas no azul.", {"aviso": "AGORA SÓ AS DIFÍCEIS!"}),
    ("lu", ["nl", "ru"], "Essa derruba quase todo mundo!",
     "Luxemburgo! O azul dele é mais clarinho que o da Holanda.",
     {"aviso": "QUASE IGUAIS!", "suspense": True,
      "sabia": "Luxemburgo e Holanda têm bandeiras quase iguais: só muda o tom do azul."}),
    ("sn", ["ml", "gn"], "Três bandeiras verde, amarelo e vermelho!",
     "Senegal! A dele tem a estrela verde no meio.",
     {"dica": ("Dica: a certa tem uma estrela!", "A CERTA TEM ESTRELA!")}),
    ("mz", ["zw", "ao"], "Valendo o título de mestre das bandeiras!",
     "Moçambique! A única bandeira com um fuzil. Se acertou, você manja muito de bandeira!",
     {"count": 10.0, "suspense": True, "final": True}),
]


def letras(nome):
    return [c for c in nome if c != " "]


def main():
    rnd = random.Random(41)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    pos[0], pos[1] = 1, 2
    os.makedirs(os.path.join(HERE, "bandeiras"), exist_ok=True)
    R = []
    for n, (certo, err, entrada, fr, ex) in enumerate(P, 1):
        cods = list(err)
        cods.insert(pos[n - 1], certo)
        assert len(set(cods)) == 3, (n, cods)
        for c in cods:
            dst = os.path.join(HERE, "bandeiras", c + ".png")
            if not os.path.exists(dst):
                shutil.copy(os.path.join(VIDEOS, "03-bandeiras-195", "bandeiras", c + ".png"), dst)
        nome = PAISES[certo][0]
        le = letras(nome)
        tam = len(le)
        palavras = nome.count(" ") + 1
        extra = f", em {'três' if palavras > 2 else 'duas'} palavras" if palavras > 1 else ""
        fq = (f"{entrada} Começa com {LETRA[le[0]]}, {LETRA[le[1]]}... e tem {NUM[tam]} letras{extra}. "
              f"Qual é a bandeira?")
        r = {"n": n, "pais": nome, "inicio": le[0] + le[1], "letras": tam, "pergunta": "QUE PAÍS É? ACHE A BANDEIRA!",
             "foto": f"q{n}.png", "foto_resposta": f"r{n}.png", "bandeiras": cods,
             "opcoes": [PAISES[c][0] for c in cods], "certa": pos[n - 1],
             "fala_q": fq, "fala_r": fr, "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "E a resposta é..." if n != len(P) else "Valendo o título... a resposta é..."
        R.append(r)
    assert len(R) == 36 and len({r["pais"] for r in R}) == 36
    # nenhuma resposta repetida, e a certa começa mesmo com as letras do cartão
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
