"""Monta paises.json: 195 países (193 membros da ONU + Vaticano e Palestina) em 3 níveis.

Uso: py -3 montar_lista.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))

NOMES = {
    "af": "Afeganistão", "za": "África do Sul", "al": "Albânia", "de": "Alemanha", "ad": "Andorra", "ao": "Angola",
    "ag": "Antígua e Barbuda", "sa": "Arábia Saudita", "dz": "Argélia", "ar": "Argentina", "am": "Armênia",
    "au": "Austrália", "at": "Áustria", "az": "Azerbaijão", "bs": "Bahamas", "bh": "Bahrein", "bd": "Bangladesh",
    "bb": "Barbados", "by": "Belarus", "be": "Bélgica", "bz": "Belize", "bj": "Benin", "bo": "Bolívia",
    "ba": "Bósnia e Herzegovina", "bw": "Botsuana", "br": "Brasil", "bn": "Brunei", "bg": "Bulgária",
    "bf": "Burkina Faso", "bi": "Burundi", "bt": "Butão", "cv": "Cabo Verde", "cm": "Camarões", "kh": "Camboja",
    "ca": "Canadá", "qa": "Catar", "kz": "Cazaquistão", "td": "Chade", "cl": "Chile", "cn": "China", "cy": "Chipre",
    "co": "Colômbia", "km": "Comores", "cg": "Congo", "kp": "Coreia do Norte", "kr": "Coreia do Sul",
    "ci": "Costa do Marfim", "cr": "Costa Rica", "hr": "Croácia", "cu": "Cuba", "dk": "Dinamarca", "dj": "Djibuti",
    "dm": "Dominica", "eg": "Egito", "sv": "El Salvador", "ae": "Emirados Árabes Unidos", "ec": "Equador",
    "er": "Eritreia", "sk": "Eslováquia", "si": "Eslovênia", "es": "Espanha", "us": "Estados Unidos",
    "ee": "Estônia", "sz": "Essuatíni", "et": "Etiópia", "fj": "Fiji", "ph": "Filipinas", "fi": "Finlândia",
    "fr": "França", "ga": "Gabão", "gm": "Gâmbia", "gh": "Gana", "ge": "Geórgia", "gd": "Granada", "gr": "Grécia",
    "gt": "Guatemala", "gy": "Guiana", "gn": "Guiné", "gq": "Guiné Equatorial", "gw": "Guiné-Bissau", "ht": "Haiti",
    "hn": "Honduras", "hu": "Hungria", "ye": "Iêmen", "mh": "Ilhas Marshall", "sb": "Ilhas Salomão", "in": "Índia",
    "id": "Indonésia", "ir": "Irã", "iq": "Iraque", "ie": "Irlanda", "is": "Islândia", "il": "Israel", "it": "Itália",
    "jm": "Jamaica", "jp": "Japão", "jo": "Jordânia", "ki": "Kiribati", "kw": "Kuwait", "la": "Laos",
    "ls": "Lesoto", "lv": "Letônia", "lb": "Líbano", "lr": "Libéria", "ly": "Líbia", "li": "Liechtenstein",
    "lt": "Lituânia", "lu": "Luxemburgo", "mk": "Macedônia do Norte", "mg": "Madagascar", "my": "Malásia",
    "mw": "Malawi", "mv": "Maldivas", "ml": "Mali", "mt": "Malta", "ma": "Marrocos", "mu": "Maurício",
    "mr": "Mauritânia", "mx": "México", "mm": "Mianmar", "fm": "Micronésia", "mz": "Moçambique", "md": "Moldávia",
    "mc": "Mônaco", "mn": "Mongólia", "me": "Montenegro", "na": "Namíbia", "nr": "Nauru", "np": "Nepal",
    "ni": "Nicarágua", "ne": "Níger", "ng": "Nigéria", "no": "Noruega", "nz": "Nova Zelândia", "om": "Omã",
    "nl": "Países Baixos", "pw": "Palau", "ps": "Palestina", "pa": "Panamá", "pg": "Papua-Nova Guiné",
    "pk": "Paquistão", "py": "Paraguai", "pe": "Peru", "pl": "Polônia", "pt": "Portugal", "ke": "Quênia",
    "kg": "Quirguistão", "gb": "Reino Unido", "cf": "República Centro-Africana", "cd": "República Democrática do Congo",
    "do": "República Dominicana", "cz": "República Tcheca", "ro": "Romênia", "rw": "Ruanda", "ru": "Rússia",
    "ws": "Samoa", "sm": "San Marino", "lc": "Santa Lúcia", "kn": "São Cristóvão e Névis", "st": "São Tomé e Príncipe",
    "vc": "São Vicente e Granadinas", "sc": "Seicheles", "sn": "Senegal", "sl": "Serra Leoa", "rs": "Sérvia",
    "sg": "Singapura", "sy": "Síria", "so": "Somália", "lk": "Sri Lanka", "sd": "Sudão", "ss": "Sudão do Sul",
    "se": "Suécia", "ch": "Suíça", "sr": "Suriname", "th": "Tailândia", "tj": "Tajiquistão", "tz": "Tanzânia",
    "tl": "Timor-Leste", "tg": "Togo", "to": "Tonga", "tt": "Trinidad e Tobago", "tn": "Tunísia",
    "tm": "Turcomenistão", "tr": "Turquia", "tv": "Tuvalu", "ua": "Ucrânia", "ug": "Uganda", "uy": "Uruguai",
    "uz": "Uzbequistão", "vu": "Vanuatu", "va": "Vaticano", "ve": "Venezuela", "vn": "Vietnã", "zm": "Zâmbia",
    "zw": "Zimbábue",
}

FACIL = ("br ar us fr it de pt es gb jp ca mx cn au ru kr in za ch nl gr se no dk fi ie be at tr sa eg ma ng uy cl "
         "co pe py bo ec ve cu jm pa cr nz is pl ua hr th vn id ph sg il ps va qa ae ke np gh cm sn").split()
MEDIO = ("ao ro cd hu rs sk si bg cz kz uz pk ir iq sy jo lb dz tn ly sd ci et tz ug zm zw bd lk mm kp mn ge am "
         "az cy lu mt by lt lv ee md al gt hn sv ni do ht bh om kw mg mu mz kh la bn fj tt so my mc ba").split()


def main():
    assert len(NOMES) == 195, len(NOMES)
    for c in FACIL + MEDIO:
        assert c in NOMES, c
    assert len(set(FACIL + MEDIO)) == len(FACIL + MEDIO)
    dificil = [c for c in NOMES if c not in FACIL and c not in MEDIO]
    random.Random(28).shuffle(dificil)
    lista, n = [], 0
    for nivel, codes in (("FÁCIL", FACIL), ("MÉDIO", MEDIO), ("DIFÍCIL", dificil)):
        for c in codes:
            n += 1
            lista.append({"n": n, "nivel": nivel, "code": c, "nome": NOMES[c]})
    json.dump(lista, open(os.path.join(HERE, "paises.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(FACIL), len(MEDIO), len(dificil))


if __name__ == "__main__":
    main()
