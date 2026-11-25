"""Gera itens.json do vídeo 54 "Alfabeto dos TIMES de A a Z — PARTE 2" (estilo mais humano, 2026-11-24).

36 times NOVOS (nenhum é resposta do vídeo 16, a parte 1): o escudo aparece PIXELADO e vai ficando nítido na
contagem; 3 alternativas com a MESMA letra. Mais times do Brasil (Série B/C e tradicionais) e da Europa média.
Escudos: imagem da infobox da en.wikipedia (workflow Fotos Wikimedia, pasta novos/) + escudos já baixados para os
vídeos 16, 19, 31 e 32. Créditos em creditos.json e na tela final.
Uso: py -3 itens.py   (copia os escudos para escudos/ e grava itens.json + creditos.json)
"""
import json, os, random, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
FONTES = [os.path.join(HERE, "novos")] + [os.path.join(VIDEOS, p) for p in
                                           ("16-alfabeto-times", "19-monte-seu-clube", "31-jogador-pela-carreira",
                                            "32-jogador-clube-pais")]

# letra, certo (como aparece), escudo, [erradas], fala da pergunta (sem alternativas), fala da resposta, extras
P = [
    ("A", "ATHLETICO-PR", "athletico-paranaense.png", ["AVAÍ", "ATLÉTICO-GO"],
     "Começando pelo A, bem fácil: que time é esse?", "Athletico Paranaense, o Furacão! Começou bem?", {"count": 5.0}),
    ("A", "AMÉRICA-MG", "america-mineiro.png", ["ATLÉTICO-MG", "ASTON VILLA"],
     "Mais um com A. Cuidado, que esse tem pegadinha!", "América Mineiro, o Coelho! Não é o Galo, hein?",
     {"count": 5.0, "aviso": "TEM PEGADINHA!"}),
    ("A", "ASTON VILLA", "aston-villa.png", ["ARSENAL", "ATALANTA"],
     "Agora um inglês com a letra A.", "Aston Villa! O leão de Birmingham.", {}),
    ("B", "BRAGANTINO", "red-bull-bragantino.png", ["BOTAFOGO", "BAHIA"],
     "Letra B: esse é do interior de São Paulo.", "Red Bull Bragantino! O Massa Bruta.", {}),
    ("B", "LEVERKUSEN", "bayer-leverkusen.png", ["DORTMUND", "BAYERN"],
     "Ainda no B... ou quase! Time alemão.", "Bayer Leverkusen! Campeão alemão invicto em 2024.",
     {"sabia": "O Leverkusen ganhou a Bundesliga de 2024 sem perder nenhum jogo."}),
    ("B", "BETIS", "betis.png", ["BARCELONA", "BENFICA"],
     "Letra B, agora na Espanha: verde e branco.", "Real Betis, de Sevilha! O Antony brilhou lá.", {}),
    ("C", "CHAPECOENSE", "chapecoense.png", ["CORITIBA", "CRICIÚMA"],
     "Vamos pro C! Time de Santa Catarina.", "Chapecoense, a Chape! Campeã da Sul-Americana de 2016.",
     {"sabia": "A Chape foi declarada campeã da Sul-Americana de 2016."}),
    ("C", "CUIABÁ", "cuiaba.png", ["CEARÁ", "CORITIBA"],
     "Letra C, lá do Mato Grosso.", "Cuiabá, o Dourado!", {}),
    ("C", "CRYSTAL PALACE", "crystal-palace.png", ["CHELSEA", "CELTIC"],
     "Mais um C, agora de Londres. Que time é esse?", "Crystal Palace! A águia de Londres.", {}),
    ("D", "LA CORUÑA", "deportivo-la-coruna.png", ["DÍNAMO DE KIEV", "DEFENSA Y JUSTICIA"],
     "Letra D: esse foi campeão espanhol com os brasileiros Djalminha e Mauro Silva.",
     "Deportivo La Coruña! O Super Depor.", {}),
    ("E", "EINTRACHT", "eintracht-frankfurt.png", ["EVERTON", "ESPANYOL"],
     "Letra E: tem uma águia no escudo e é da Alemanha.", "Eintracht Frankfurt! Campeão da Liga Europa em 2022.", {}),
    ("E", "ESTUDIANTES", "estudiantes.png", ["EMELEC", "EVERTON"],
     "Mais um E, esse é argentino e já foi campeão do mundo.", "Estudiantes de La Plata! O time do Verón.", {}),
    ("F", "FIORENTINA", "fiorentina.png", ["FLUMINENSE", "FULHAM"],
     "Letra F: o time roxo da Itália!", "Fiorentina, a Viola de Florença!", {}),
    ("F", "FIGUEIRENSE", "figueirense.png", ["FORTALEZA", "FERROVIÁRIA"],
     "Outro F, alvinegro e de Florianópolis.", "Figueirense, o Furacão do Estreito!", {}),
    ("G", "GUARANI", "guarani.png", ["GRÊMIO", "GOIÁS"],
     "Letra G: campeão brasileiro de 1978, lá de Campinas.", "Guarani, o Bugre! Campeão brasileiro em 78.", {}),
    ("G", "GETAFE", "getafe.png", ["GIRONA", "GRANADA"],
     "Mais um G, esse é da Espanha, pertinho de Madri.", "Getafe! Time da região de Madri.", {}),
    ("H", "HERTHA BERLIM", "hertha-berlim.png", ["HAMBURGO", "HOFFENHEIM"],
     "Letra H, da capital da Alemanha.", "Hertha Berlim! O time azul e branco de Berlim.", {}),
    ("I", "INTER MIAMI", "inter-miami.png", ["INTERNACIONAL", "INDEPENDIENTE"],
     "Letra I: o time cor-de-rosa de um certo argentino famoso!", "Inter Miami, o time do Messi!",
     {"dica": ("Dica: é dos Estados Unidos!", "É DOS ESTADOS UNIDOS!")}),
    ("K", "KASHIMA ANTLERS", "kashima-antlers.png", ["KAWASAKI", "KAISERSLAUTERN"],
     "Letra K, lá do Japão, onde o Zico virou ídolo.", "Kashima Antlers! O Zico é rei lá.",
     {"sabia": "O Zico jogou e foi dirigente no Kashima: tem até estátua dele lá."}),
    ("L", "LEICESTER", "leicester.png", ["LIVERPOOL", "LILLE"],
     "Letra L: o time que foi campeão inglês contra todas as apostas!", "Leicester! Campeão inglês em 2016, a maior zebra.", {}),
    ("M", "MALLORCA", "mallorca.png", ["MÁLAGA", "MONACO"],
     "Letra M: time de uma ilha da Espanha.", "Mallorca! Lá da ilha de Maiorca.", {}),
    ("N", "NOTTINGHAM FOREST", "nottingham-forest.png", ["NEWCASTLE", "NORWICH"],
     "Letra N: esse inglês já ganhou duas Champions!", "Nottingham Forest! Bicampeão da Europa em 79 e 80.", {}),
    ("N", "NÁUTICO", "nautico.png", ["NACIONAL", "NOVORIZONTINO"],
     "Mais um N, lá de Recife.", "Náutico, o Timbu!", {}),
    ("O", "OLYMPIACOS", "olympiacos.png", ["OLIMPIA", "OSASUNA"],
     "Letra O: o maior campeão da Grécia.", "Olympiacos! Campeão da Conference League em 2024.", {}),
    ("P", "PAYSANDU", "paysandu.png", ["PALMEIRAS", "PONTE PRETA"],
     "Letra P, lá de Belém do Pará!", "Paysandu, o Papão da Curuzu!", {}),
    ("P", "PONTE PRETA", "ponte-preta.png", ["PORTUGUESA", "PARANÁ"],
     "Outro P, esse é de Campinas, rival do Guarani.", "Ponte Preta, a Macaca!", {}),
    ("P", "PEÑAROL", "penarol.png", ["PORTO", "PALESTINO"],
     "Mais um P, agora do Uruguai: cinco Libertadores!", "Peñarol! Cinco vezes campeão da Libertadores.", {}),
    ("R", "REMO", "remo.png", ["RIVER PLATE", "ROMA"],
     "Letra R, de novo em Belém: o rival do Paysandu!", "Remo, o Leão Azul! Rival do Paysandu no Re-Pa.", {}),
    ("S", "SANTA CRUZ", "santa-cruz.png", ["SPORT", "SANTOS"],
     "Letra S: time tricolor de Recife.", "Santa Cruz, a Cobra Coral!", {}),
    ("S", "SCHALKE 04", "schalke-04.png", ["STUTTGART", "SEVILLA"],
     "Mais um S, esse é alemão e azul.", "Schalke zero quatro! O Rafinha e o Naldo jogaram lá.", {}),
    ("S", "SHAKHTAR", "shakhtar.png", ["SPARTAK MOSCOU", "SPORTING"],
     "Letra S: o time da Ucrânia que adora contratar brasileiros!", "Shakhtar Donetsk! Já teve mais de dez brasileiros no elenco.",
     {"suspense": True}),
    ("U", "UNION BERLIN", "union-berlin.png", ["UDINESE", "UTRECHT"],
     "Letra U, das difíceis!", "Union Berlin! O outro time de Berlim.", {"aviso": "LETRA DIFÍCIL!"}),
    ("V", "VÉLEZ SARSFIELD", "velez-sarsfield.png", ["VALENCIA", "VILLARREAL"],
     "Letra V: argentino, campeão do mundo em 1994.", "Vélez Sarsfield! Ganhou do Milan no Mundial de 94.", {}),
    ("W", "WERDER BREMEN", "werder-bremen.png", ["WOLFSBURG", "WOLVERHAMPTON"],
     "Letra W: tem um W verde no escudo, mas cuidado!", "Werder Bremen! O Wolfsburg também é verde, mas o escudo é redondo.",
     {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("Y", "YOKOHAMA MARINOS", "yokohama-marinos.png", ["YOUNG BOYS", "YEOVIL TOWN"],
     "Letra Y! Esse é do Japão.", "Yokohama Marinos! Time de Yokohama, no Japão.",
     {"dica": ("Dica: tem uma âncora no escudo!", "TEM UMA ÂNCORA!")}),
    ("Z", "ZULTE WAREGEM", "zulte-waregem.png", ["ZENIT", "ZARAGOZA"],
     "Valendo o título de mestre do alfabeto! A letra Z, que ninguém acerta.",
     "Zulte Waregem, da Bélgica! Se acertou essa, você é fera demais!",
     {"count": 10.0, "suspense": True, "final": True}),
]


def achar(arq):
    for d in FONTES:
        p = os.path.join(d, "escudos", arq)
        if os.path.exists(p):
            return d, p
    raise FileNotFoundError(arq)


def credito(d, arq):
    for nome in ("creditos.json", "creditos-escudos.json"):
        p = os.path.join(d, nome)
        if os.path.exists(p):
            for k, c in json.load(open(p, encoding="utf-8")).items():
                if c.get("arquivo") == arq:
                    return k, c
    raise KeyError(arq)


def main():
    rnd = random.Random(54)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    pos[0], pos[1] = 1, 0
    os.makedirs(os.path.join(HERE, "escudos"), exist_ok=True)
    parte1 = {r["escudo"] for r in json.load(open(os.path.join(VIDEOS, "16-alfabeto-times", "itens.json"), encoding="utf-8"))}
    cred, R = {}, []
    for n, (letra, certo, esc, err, fq, fr, ex) in enumerate(P, 1):
        assert esc not in parte1, esc
        d, src = achar(esc)
        shutil.copy(src, os.path.join(HERE, "escudos", esc))
        k, c = credito(d, esc)
        cred[k] = c
        nomes = list(err)
        nomes.insert(pos[n - 1], certo)
        ok = lambda x: x[0] == letra or (letra == "B" and x in ("LEVERKUSEN", "DORTMUND", "BAYERN")) or \
            (letra == "D" and x == "LA CORUÑA")
        assert len(set(nomes)) == 3 and all(ok(x) for x in nomes), (n, nomes)
        r = {"n": n, "letra": letra, "nome": certo, "escudo": esc, "pergunta": f"LETRA {letra}: QUE TIME É ESSE?",
             "foto": esc, "opcoes": nomes, "certa": pos[n - 1],
             "fala_q": f"{fq} {nomes[0].title()}, {nomes[1].title()} ou {nomes[2].title()}?",
             "fala_r": fr, "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for kk in ("aviso", "sabia", "final"):
            if kk in ex:
                r[kk] = ex[kk]
        if ex.get("suspense"):
            r["fala_s"] = "E a resposta é..." if n != len(P) else "Valendo o título... a resposta é..."
        R.append(r)
    assert len(R) == 36 and len({r["escudo"] for r in R}) == 36
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(cred, open(os.path.join(HERE, "creditos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], len(cred), "créditos")


if __name__ == "__main__":
    main()
