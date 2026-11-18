"""Gera itens.json do vídeo 39 "Uma SELEÇÃO para cada LETRA" (estilo mais humano, 2026-11-18).

32 perguntas próprias: o cartão mostra a LETRA gigante + uma pista (título, apelido, Copa...), e as 3 alternativas
são seleções com a MESMA letra, cada uma com a bandeira (domínio público: as do vídeo 03; Inglaterra/Escócia do
vídeo 37; País de Gales e Kosovo do pacote npm flag-icons, MIT). Fáceis primeiro; letras difíceis (K, O, Q, W, X, Y, Z)
no fim com aviso. Alternativa que não é país (Oceania, Xangai...) aparece com um "?" no lugar da bandeira.
Fatos conferidos em 2026-11-18.
Uso: py -3 itens.py   (copia as bandeiras que faltarem)
"""
import json, os, random, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)

# código da bandeira: (nome na tela, nome falado). Código começando com "-" = sem bandeira (não é país).
PAISES = {
    "br": ("BRASIL", "Brasil"), "be": ("BÉLGICA", "Bélgica"), "bo": ("BOLÍVIA", "Bolívia"),
    "ar": ("ARGENTINA", "Argentina"), "de": ("ALEMANHA", "Alemanha"), "au": ("AUSTRÁLIA", "Austrália"),
    "pt": ("PORTUGAL", "Portugal"), "py": ("PARAGUAI", "Paraguai"), "pe": ("PERU", "Peru"),
    "fr": ("FRANÇA", "França"), "fi": ("FINLÂNDIA", "Finlândia"), "fj": ("FIJI", "Fiji"),
    "es": ("ESPANHA", "Espanha"), "ec": ("EQUADOR", "Equador"), "gb-sct": ("ESCÓCIA", "Escócia"),
    "it": ("ITÁLIA", "Itália"), "gb-eng": ("INGLATERRA", "Inglaterra"), "ir": ("IRÃ", "Irã"),
    "jp": ("JAPÃO", "Japão"), "jm": ("JAMAICA", "Jamaica"), "jo": ("JORDÂNIA", "Jordânia"),
    "uy": ("URUGUAI", "Uruguai"), "ua": ("UCRÂNIA", "Ucrânia"), "uz": ("UZBEQUISTÃO", "Uzbequistão"),
    "mx": ("MÉXICO", "México"), "ma": ("MARROCOS", "Marrocos"), "ml": ("MALI", "Mali"),
    "mz": ("MOÇAMBIQUE", "Moçambique"),
    "hr": ("CROÁCIA", "Croácia"), "co": ("COLÔMBIA", "Colômbia"), "cm": ("CAMARÕES", "Camarões"),
    "nl": ("HOLANDA", "Holanda"), "hu": ("HUNGRIA", "Hungria"), "ht": ("HAITI", "Haiti"),
    "dz": ("ARGÉLIA", "Argélia"), "at": ("ÁUSTRIA", "Áustria"),
    "se": ("SUÉCIA", "Suécia"), "ch": ("SUÍÇA", "Suíça"), "rs": ("SÉRVIA", "Sérvia"),
    "gh": ("GANA", "Gana"), "gr": ("GRÉCIA", "Grécia"), "ge": ("GEÓRGIA", "Geórgia"),
    "ng": ("NIGÉRIA", "Nigéria"), "no": ("NORUEGA", "Noruega"), "nz": ("NOVA ZELÂNDIA", "Nova Zelândia"),
    "ru": ("RÚSSIA", "Rússia"), "ro": ("ROMÊNIA", "Romênia"), "rw": ("RUANDA", "Ruanda"),
    "tr": ("TURQUIA", "Turquia"), "tn": ("TUNÍSIA", "Tunísia"), "tg": ("TOGO", "Togo"),
    "cl": ("CHILE", "Chile"), "cr": ("COSTA RICA", "Costa Rica"), "ca": ("CANADÁ", "Canadá"), "qa": ("CATAR", "Catar"),
    "dk": ("DINAMARCA", "Dinamarca"), "dj": ("DJIBUTI", "Djibuti"), "dm": ("DOMINICA", "Dominica"),
    "ie": ("IRLANDA", "Irlanda"), "is": ("ISLÂNDIA", "Islândia"), "il": ("ISRAEL", "Israel"),
    "ve": ("VENEZUELA", "Venezuela"), "vn": ("VIETNÃ", "Vietnã"), "vu": ("VANUATU", "Vanuatu"),
    "lr": ("LIBÉRIA", "Libéria"), "ly": ("LÍBIA", "Líbia"), "lu": ("LUXEMBURGO", "Luxemburgo"),
    "zm": ("ZÂMBIA", "Zâmbia"), "zw": ("ZIMBÁBUE", "Zimbábue"), "-zaire": ("ZAIRE", "Zaire"),
    "kw": ("KUWAIT", "Kuwait"), "xk": ("KOSOVO", "Kosovo"), "ki": ("KIRIBATI", "Kiribati"),
    "om": ("OMÃ", "Omã"), "-oceania": ("OCEANIA", "Oceania"), "-oriente": ("ORIENTE MÉDIO", "Oriente Médio"),
    "ke": ("QUÊNIA", "Quênia"), "kg": ("QUIRGUISTÃO", "Quirguistão"), "-quebec": ("QUEBEC", "Quebec"),
    "ye": ("IÊMEN", "Iêmen"),
    "-nenhuma": ("NENHUMA!", "nenhuma"), "-xangai": ("XANGAI", "Xangai"), "-xingu": ("XINGU", "Xingu"),
    "gb-wls": ("PAÍS DE GALES", "País de Gales"),
}

# letra, pista (linhas do cartão), certa, [erradas], fala da pergunta (sem as alternativas), fala da resposta, extras
P = [
    ("B", ["A única", "PENTACAMPEÃ"], "br", ["be", "bo"], "Começando fácil, letra B: a única seleção pentacampeã do mundo!",
     "Brasil! Cinco estrelas na camisa. Começou bem?", {"count": 5.0}),
    ("A", ["Campeã do mundo", "em 2022"], "ar", ["de", "au"], "Letra A: quem foi campeã do mundo em 2022?",
     "Argentina! Com Messi levantando a taça.", {"count": 5.0}),
    ("P", ["A seleção do", "Cristiano Ronaldo"], "pt", ["py", "pe"], "Letra P: a seleção do Cristiano Ronaldo!",
     "Portugal! O maior artilheiro de seleções da história.", {}),
    ("F", ["Campeã do mundo", "em 2018"], "fr", ["fi", "fj"], "Letra F: a campeã do mundo de 2018, na Rússia.",
     "França! Com o Mbappé ainda novinho.", {}),
    ("E", ["Campeã do mundo", "em 2010"], "es", ["ec", "gb-sct"], "Letra E: quem ganhou a Copa de 2010, na África do Sul?",
     "Espanha! Gol do Iniesta na prorrogação da final.", {}),
    ("I", ["A AZZURRA,", "tetracampeã"], "it", ["gb-eng", "ir"], "Letra I: a Azzurra, tetracampeã do mundo.",
     "Itália! Quatro títulos, igual à Alemanha.", {}),
    ("J", ["Os SAMURAIS", "AZUIS"], "jp", ["jm", "jo"], "Letra J: a seleção conhecida como Samurais Azuis.",
     "Japão! A torcida ainda limpa o estádio depois do jogo.", {}),
    ("U", ["A 1ª campeã", "do mundo (1930)"], "uy", ["ua", "uz"], "Letra U: a primeira campeã do mundo, em 1930.",
     "Uruguai! E ainda foi a dona da casa.", {"sabia": "O Uruguai também ganhou a Copa de 1950, no Maracanã."}),
    ("M", ["Sede das Copas", "de 1970, 1986", "e 2026"], "mx", ["ma", "ml"],
     "Letra M: o país que recebeu as Copas de 1970, 1986 e 2026.",
     "México! O primeiro país a receber três Copas.", {}),
    ("C", ["Vice em 2018,", "camisa XADREZ"], "hr", ["co", "cm"],
     "Letra C: a vice-campeã de 2018, a da camisa xadrez.", "Croácia! Com o Modrić no meio-campo.", {}),
    ("H", ["A LARANJA", "MECÂNICA"], "nl", ["hu", "ht"], "Letra H: a famosa Laranja Mecânica.",
     "Holanda! Três finais de Copa e nenhum título.", {}),
    ("A", ["Os SOCCEROOS", "(a dos cangurus)"], "au", ["dz", "at"], "Letra A de novo: a seleção dos Socceroos, a dos cangurus.",
     "Austrália! Socceroos mistura soccer, futebol, com kangaroo, canguru.", {}),
    ("S", ["Perdeu a final", "de 1958", "para o Brasil"], "se", ["ch", "rs"],
     "Cuidado, que essa tem pegadinha! Letra S: quem perdeu a final da Copa de 1958 para o Brasil?",
     "Suécia! A primeira Copa do Brasil, com Pelé de dezessete anos.", {"aviso": "TEM PEGADINHA!"}),
    ("G", ["As ESTRELAS", "NEGRAS"], "gh", ["gr", "ge"], "Letra G: as Estrelas Negras, da África.",
     "Gana! A estrela preta tá até na bandeira.", {}),
    ("N", ["As SUPER", "ÁGUIAS"], "ng", ["no", "nz"], "Letra N: a seleção das Super Águias.",
     "Nigéria! Campeã olímpica em 1996.", {}),
    ("R", ["Sede da Copa", "de 2018"], "ru", ["ro", "rw"], "Letra R: o país-sede da Copa de 2018.",
     "Rússia! A Copa da final França contra Croácia.", {}),
    ("T", ["3º lugar na", "Copa de 2002"], "tr", ["tn", "tg"], "Letra T: quem ficou em terceiro lugar na Copa de 2002?",
     "Turquia! E perdeu a semifinal justo pro Brasil.", {"suspense": True}),
    ("C", ["Campeã da Copa", "América em", "2015 e 2016"], "cl", ["co", "cr"],
     "Letra C de novo: a campeã da Copa América em 2015 e em 2016.",
     "Chile! Ganhou as duas na final contra a Argentina, nos pênaltis.",
     {"dica": ("Dica: é a do Alexis Sánchez!", "ALEXIS SÁNCHEZ!")}),
    ("M", ["1ª africana na", "SEMIFINAL", "(2022)"], "ma", ["ml", "mz"],
     "Letra M: a primeira seleção africana a chegar numa semifinal de Copa, em 2022.",
     "Marrocos! Eliminou Espanha e Portugal no caminho.", {}),
    ("D", ["Campeã da", "EUROCOPA 1992"], "dk", ["dj", "dm"], "Letra D: a campeã da Eurocopa de 1992.",
     "Dinamarca! E ela nem tinha se classificado, entrou de última hora.",
     {"sabia": "A Dinamarca entrou na Euro 92 no lugar da Iugoslávia, 10 dias antes."}),
    ("I", ["Campeã do mundo", "em casa, 1966"], "gb-eng", ["ie", "is"],
     "Letra I: campeã do mundo em casa, em 1966.", "Inglaterra! O único título deles.", {}),
    ("V", ["A ÚNICA da", "América do Sul que", "NUNCA foi à Copa"], "ve", ["vn", "vu"],
     "Essa derruba muita gente! Letra V: a única seleção da América do Sul que nunca jogou uma Copa.",
     "Venezuela! Bateu na trave de novo nas eliminatórias de 2026.", {"aviso": "DERRUBA MUITA GENTE!"}),
    ("C", ["Os LEÕES", "INDOMÁVEIS"], "cm", ["ca", "qa"], "Letra C, a última com C: os Leões Indomáveis.",
     "Camarões! A do Roger Milla dançando na bandeirinha de escanteio.", {}),
    ("L", ["Seleção do único", "africano BOLA", "DE OURO"], "lr", ["ly", "lu"],
     "Agora as letras difíceis! Letra L: a seleção do George Weah, o único africano Bola de Ouro.",
     "Libéria! E o Weah depois virou presidente do país.",
     {"aviso": "AGORA SÓ LETRA DIFÍCIL!", "dica": ("Dica: fica na África!", "FICA NA ÁFRICA!")}),
    ("I", ["O grito viking", "\"UH!\" na Euro 2016"], "is", ["ie", "il"],
     "Letra I: a seleção do grito viking, uh, na Eurocopa de 2016.",
     "Islândia! Um país com menos gente que muita cidade brasileira.", {}),
    ("Z", ["Campeã africana", "em 2012"], "zm", ["zw", "-zaire"], "Letra Z: a campeã da Copa Africana de 2012.",
     "Zâmbia! E Zaire é o nome antigo do Congo.", {"aviso": "TEM PEGADINHA!"}),
    ("K", ["Jogou a Copa", "de 1982"], "kw", ["xk", "ki"], "Ninguém lembra dessa! Letra K: a seleção que jogou a Copa de 1982.",
     "Kuwait! Jogou na Espanha, contra França, Inglaterra e Tchecoslováquia.", {"aviso": "NINGUÉM LEMBRA!", "suspense": True}),
    ("O", ["A ÚNICA seleção", "com O"], "om", ["-oceania", "-oriente"], "Letra O: qual é a única seleção com O?",
     "Omã! Oceania é continente, e Oriente Médio é região.", {"aviso": "TEM PEGADINHA!"}),
    ("Q", ["Terra dos campeões", "de MARATONA"], "ke", ["kg", "-quebec"], "Letra Q: o país africano dos campeões de maratona.",
     "Quênia! Quebec é uma província do Canadá.", {}),
    ("Y", ["Em inglês: YEMEN.", "E em português?"], "ye", ["om", "qa"],
     "Letra Y! Em português não tem seleção com Y. Mas em inglês tem: Yemen. Que país é esse?",
     "Iêmen! No Brasil a gente escreve com I.", {"aviso": "TEM PEGADINHA!"}),
    ("X", ["Que seleção", "começa com X?"], "-nenhuma", ["-xangai", "-xingu"],
     "E a letra xis? Que seleção começa com xis?",
     "Nenhuma! Não existe país com xis. Xangai é cidade da China e Xingu é rio do Brasil.",
     {"aviso": "PEGADINHA!", "suspense": True}),
    ("W", ["Em inglês: WALES,", "a do Gareth Bale"], "gb-wls", ["gb-sct", "ie"],
     "Valendo o título de craque das seleções! Letra W: Wales, a seleção do Gareth Bale. Como é em português?",
     "País de Gales! Em inglês é Wales, com W. Se acertou essa, você manja de seleção!",
     {"count": 10.0, "suspense": True, "final": True}),
]


def main():
    rnd = random.Random(39)
    pos = [0, 1, 2] * 11
    rnd.shuffle(pos)
    pos[0], pos[1] = 0, 2
    os.makedirs(os.path.join(HERE, "bandeiras"), exist_ok=True)
    R = []
    for n, (letra, pista, certo, err, fq, fr, ex) in enumerate(P, 1):
        cods = list(err)
        cods.insert(pos[n - 1], certo)
        assert len(set(cods)) == 3, (n, cods)
        for c in cods:
            if c.startswith("-"):
                continue
            dst = os.path.join(HERE, "bandeiras", c + ".png")
            if not os.path.exists(dst):
                src = os.path.join(VIDEOS, "03-bandeiras-195", "bandeiras", c + ".png")
                if not os.path.exists(src):
                    src = os.path.join(VIDEOS, "37-jogador-qual-pais", "bandeiras", c + ".png")
                shutil.copy(src, dst)
        fal = [PAISES[c][1] for c in cods]
        r = {"n": n, "letra": letra, "pista": pista, "pergunta": f"SELEÇÃO COM A LETRA {letra}",
             "foto": f"q{n}.png", "bandeiras": cods, "opcoes": [PAISES[c][0] for c in cods], "certa": pos[n - 1],
             "fala_q": f"{fq} {fal[0]}, {fal[1]} ou {fal[2]}?", "fala_r": fr, "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo o título... a resposta é..."
        R.append(r)
    assert len(R) == 32 and len({tuple(r["pista"]) for r in R}) == 32
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], sorted({r["letra"] for r in R}))


if __name__ == "__main__":
    main()
