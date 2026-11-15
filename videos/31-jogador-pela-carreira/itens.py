"""Gera itens.json do vídeo 31 "De quem é essa carreira?" — adivinhe o jogador pelos clubes (estilo mais humano).

36 perguntas próprias, do fácil ao difícil (ref. BigFut, formato "quem é? pela carreira"): o cartão mostra a
SEQUÊNCIA DE CLUBES do jogador (escudos em ordem, com o ano em que chegou) e uma silhueta "?"; 3 jogadores como
alternativas; na resposta entra a foto real (Wikimedia Commons, as mesmas do vídeo 19; créditos na tela final).
Carreiras conferidas na caixa de informações da Wikipédia (2026-11-15). Clubes da base, times B e alguns
empréstimos curtos ficam de fora. Jogadores diferentes do vídeo 21 (jogador pela foto).
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
INTRO = ["ldez-pele.jpg", "lca-romario.jpg", "lmei-iniesta.jpg", "lmei-gerrard.jpg"]   # só na intro

# nome (como aparece), foto (videos/19/fotos), carreira [(escudo, ano)], [2 erradas], fala da pergunta,
# fala da resposta, extras
P = [
    ("Cristiano Ronaldo", "ca-cristiano-ronaldo.jpg",
     [("sporting", 2002), ("manchester-united", 2003), ("real-madrid", 2009), ("juventus", 2018),
      ("manchester-united", 2021), ("al-nassr", 2023)],
     ["Benzema", "Bale"], "Pra aquecer, uma bem famosa! De quem é essa carreira?",
     "Cristiano Ronaldo! Começou no Sporting e voltou duas vezes pro Manchester United!", {"count": 4.0}),
    ("Messi", "dez-messi.jpg",
     [("barcelona", 2004), ("psg", 2021), ("inter-miami", 2023)],
     ["Suárez", "Di María"], "Só três clubes nessa! Quem é?",
     "Messi! Dezessete anos de Barcelona!", {"count": 4.0}),
    ("Neymar", "pe-neymar.jpg",
     [("santos", 2009), ("barcelona", 2013), ("psg", 2017), ("al-hilal", 2023), ("santos", 2025)],
     ["Coutinho", "Gabigol"], "Agora um brasileiro que saiu e voltou pra casa!",
     "Neymar! Saiu do Santos e voltou pro Santos!", {"count": 5.0}),
    ("Mbappé", "ca-mbappe.jpg",
     [("monaco", 2015), ("psg", 2017), ("real-madrid", 2024)],
     ["Griezmann", "Giroud"], "Bora pra França! Quem fez esse caminho?",
     "Mbappé! Do Monaco pro PSG e depois pro Real Madrid!", {}),
    ("Haaland", "ca-haaland.jpg",
     [("molde", 2017), ("rb-salzburg", 2019), ("borussia-dortmund", 2020), ("manchester-city", 2022)],
     ["Ødegaard", "Sørloth"], "Esse é uma máquina de gols. Quem é?",
     "Haaland! O robô norueguês!", {}),
    ("Kaká", "lmei-kaka.jpg",
     [("sao-paulo", 2000), ("milan", 2003), ("real-madrid", 2009), ("milan", 2013), ("orlando-city", 2014)],
     ["Alexandre Pato", "Ronaldinho"], "Agora um craque das antigas, que foi o melhor do mundo!",
     "Kaká! Melhor do mundo em 2007, jogando pelo Milan!",
     {"sabia": "O Kaká ganhou a Bola de Ouro de 2007 jogando pelo Milan."}),
    ("Ibrahimović", "lca-ibrahimovic.jpg",
     [("ajax", 2001), ("juventus", 2004), ("inter-de-milao", 2006), ("barcelona", 2009), ("milan", 2010),
      ("psg", 2012), ("manchester-united", 2016), ("la-galaxy", 2018), ("milan", 2019)],
     ["Higuaín", "Van Persie"], "Olha o tamanho dessa carreira! Quem rodou tanto assim?",
     "Ibrahimović! Jogou em nove clubes grandes!", {}),
    ("Zidane", "ldez-zidane.jpg",
     [("cannes", 1989), ("bordeaux", 1992), ("juventus", 1996), ("real-madrid", 2001)],
     ["Figo", "Djorkaeff"], "Um francês que virou lenda. Quem é?",
     "Zidane! Craque da Juventus e do Real Madrid!", {}),
    ("Maradona", "ldez-maradona.jpg",
     [("argentinos-juniors", 1976), ("boca-juniors", 1981), ("barcelona", 1982), ("napoli", 1984),
      ("sevilla", 1992), ("newells-old-boys", 1993), ("boca-juniors", 1995)],
     ["Batistuta", "Riquelme"], "Esse aqui é ídolo em Nápoles até hoje!",
     "Maradona! O deus do Napoli!", {"sabia": "O estádio do Napoli hoje se chama Diego Armando Maradona."}),
    ("Donnarumma", "gol-donnarumma.jpg",
     [("milan", 2015), ("psg", 2021), ("manchester-city", 2025)],
     ["Buffon", "Courtois"], "Agora um goleiro! De quem é essa carreira?",
     "Donnarumma! Estreou no Milan com dezesseis anos!", {}),
    ("Alexander-Arnold", "ld-alexander-arnold.jpg",
     [("liverpool", 2016), ("real-madrid", 2025)],
     ["Robertson", "Joe Gomez"], "Cria da casa que trocou a Inglaterra pela Espanha. Quem é?",
     "Alexander-Arnold! Saiu do Liverpool direto pro Real Madrid!", {}),
    ("Lampard", "lmei-lampard.jpg",
     [("west-ham", 1995), ("chelsea", 2001), ("manchester-city", 2014), ("new-york-city", 2015)],
     ["Gerrard", "Terry"], "Um ídolo do Chelsea! Quem é?",
     "Lampard! O maior artilheiro da história do Chelsea!", {}),
    ("Henry", "lca-henry.jpg",
     [("monaco", 1994), ("juventus", 1999), ("arsenal", 1999), ("barcelona", 2007), ("new-york-red-bulls", 2010)],
     ["Trezeguet", "Anelka"], "Cuidado, que essa tem pegadinha! Dois clubes no mesmo ano!",
     "Thierry Henry! Ficou só meses na Juventus e virou lenda no Arsenal!", {"aviso": "TEM PEGADINHA!"}),
    ("Declan Rice", "vol-declan-rice.jpg",
     [("west-ham", 2015), ("arsenal", 2023)],
     ["Jarrod Bowen", "Mason Mount"], "Só dois clubes, mas um caminhão de dinheiro na troca. Quem é?",
     "Declan Rice! Saiu do West Ham pro Arsenal!", {}),
    ("Alisson", "gol-alisson.jpg",
     [("internacional", 2013), ("roma", 2016), ("liverpool", 2018)],
     ["Ederson", "Weverton"], "Agora um goleiro brasileiro!",
     "Alisson! Do Internacional pra Roma e depois pro Liverpool!", {}),
    ("Rüdiger", "zag1-rudiger.jpg",
     [("stuttgart", 2012), ("roma", 2015), ("chelsea", 2017), ("real-madrid", 2022)],
     ["Hummels", "Boateng"], "Um zagueiro alemão. Quem é?",
     "Rüdiger! Hoje no Real Madrid!", {}),
    ("Koundé", "ld-kounde.jpg",
     [("bordeaux", 2017), ("sevilla", 2019), ("barcelona", 2022)],
     ["Varane", "Upamecano"], "Essa aqui derruba muita gente.",
     "Koundé! Do Bordeaux pro Sevilla e depois pro Barcelona!", {}),
    ("Pirlo", "lmei-pirlo.jpg",
     [("brescia", 1995), ("inter-de-milao", 1998), ("milan", 2001), ("juventus", 2011), ("new-york-city", 2015)],
     ["Gattuso", "De Rossi"], "Um maestro italiano. Quem é?",
     "Pirlo! Jogou na Inter, no Milan e na Juventus!", {}),
    ("Tchouaméni", "vol-tchouameni.jpg",
     [("bordeaux", 2018), ("monaco", 2020), ("real-madrid", 2022)],
     ["Camavinga", "Kanté"], "Agora um volante francês!",
     "Tchouaméni! Hoje no Real Madrid!", {}),
    ("Theo Hernández", "le-theo-hernandez.jpg",
     [("atletico-de-madrid", 2015), ("real-madrid", 2017), ("real-sociedad", 2018), ("milan", 2019), ("al-hilal", 2025)],
     ["Lucas Hernández", "Ferland Mendy"], "Cuidado: essa tem irmão no meio!",
     "Theo Hernández! O Lucas é o irmão dele, que foi pro Bayern!",
     {"aviso": "TEM PEGADINHA!", "sabia": "Theo e Lucas Hernández são irmãos e começaram no Atlético de Madrid."}),
    ("Alphonso Davies", "le-alphonso-davies.jpg",
     [("vancouver-whitecaps", 2016), ("bayern-de-munique", 2019)],
     ["Jonathan David", "Achraf Hakimi"], "Esse veio do Canadá. Quem é?",
     "Alphonso Davies! O foguete do Bayern!", {}),
    ("Gvardiol", "zag2-gvardiol.jpg",
     [("dinamo-de-zagreb", 2019), ("rb-leipzig", 2020), ("manchester-city", 2023)],
     ["Dani Olmo", "Kramarić"], "Um croata! Mas qual deles?",
     "Gvardiol! O Dani Olmo também passou por Zagreb e Leipzig, mas foi pro Barcelona!", {}),
    ("Luis Díaz", "pe-luis-diaz.jpg",
     [("junior", 2017), ("porto", 2019), ("liverpool", 2022), ("bayern-de-munique", 2025)],
     ["James Rodríguez", "Cuadrado"], "Bora pra Colômbia!",
     "Luis Díaz! Do Porto pro Liverpool e depois pro Bayern!", {}),
    ("João Pedro", "joia-joao-pedro.jpg",
     [("fluminense", 2019), ("watford", 2020), ("brighton", 2023), ("chelsea", 2025)],
     ["Matheus Cunha", "Evanilson"], "Um brasileiro que foi cedo pra Inglaterra.",
     "João Pedro! Saiu do Fluminense pro Watford!", {}),
    ("Ferland Mendy", "le-ferland-mendy.jpg",
     [("le-havre", 2015), ("lyon", 2017), ("real-madrid", 2019)],
     ["Benjamin Mendy", "Lucas Digne"], "Pegadinha de sobrenome! Qual Mendy é esse?",
     "Ferland Mendy! O Benjamin Mendy foi do Monaco pro City!", {"aviso": "TEM PEGADINHA!"}),
    ("Beckenbauer", "lzag-beckenbauer.jpg",
     [("bayern-de-munique", 1964), ("new-york-cosmos", 1977), ("hamburgo", 1980), ("new-york-cosmos", 1983)],
     ["Gerd Müller", "Matthäus"], "Agora uma lenda alemã das antigas!",
     "Beckenbauer! O Kaiser! E jogou no Cosmos junto com o Pelé!",
     {"sabia": "No New York Cosmos, o Beckenbauer jogou ao lado do Pelé."}),
    ("Petr Čech", "lgol-petr-cech.jpg",
     [("sparta-praga", 2001), ("rennes", 2002), ("chelsea", 2004), ("arsenal", 2015)],
     ["Lloris", "Van der Sar"], "Um goleiro famoso pelo capacete!",
     "Petr Čech! Usava capacete depois de uma pancada na cabeça!", {}),
    ("Kyle Walker", "ld-kyle-walker.jpg",
     [("sheffield-united", 2008), ("tottenham", 2009), ("queens-park-rangers", 2010), ("aston-villa", 2011),
      ("manchester-city", 2017), ("milan", 2025), ("burnley", 2025)],
     ["Trippier", "Reece James"], "Lateral inglês que rodou bastante. Quem é?",
     "Kyle Walker! Campeão de tudo pelo City!", {}),
    ("Lisandro Martínez", "zag2-lisandro-martinez.jpg",
     [("newells-old-boys", 2017), ("defensa-y-justicia", 2017), ("ajax", 2019), ("manchester-united", 2022)],
     ["Otamendi", "Cuti Romero"], "Um zagueiro argentino!",
     "Lisandro Martínez! Brilhou no Ajax antes do United!", {}),
    ("Saliba", "zag1-saliba.jpg",
     [("saint-etienne", 2018), ("arsenal", 2019), ("saint-etienne", 2019), ("nice", 2021),
      ("olympique-de-marselha", 2021), ("arsenal", 2022)],
     ["Upamecano", "Konaté"], "Esse foi emprestado três vezes antes de vingar!",
     "Saliba! Hoje é paredão no Arsenal!", {}),
    ("Zanetti", "llat-zanetti.jpg",
     [("talleres", 1992), ("banfield", 1993), ("inter-de-milao", 1995)],
     ["Cambiasso", "Samuel"], "Esse ficou quase vinte anos no mesmo clube!",
     "Zanetti! Dezenove anos de Inter de Milão!", {"dica": ("Dica: ele foi o capitão da Inter por muitos anos.", "CAPITÃO DA INTER!")}),
    ("Gabriel Magalhães", "zag2-gabriel-magalhaes.jpg",
     [("avai", 2016), ("lille", 2017), ("troyes", 2017), ("dinamo-de-zagreb", 2018), ("arsenal", 2020)],
     ["Marquinhos", "Léo Ortiz"], "Agora um zagueiro brasileiro que começou em Santa Catarina!",
     "Gabriel Magalhães! Do Avaí pro Arsenal!", {}),
    ("Vitor Roque", "joia-vitor-roque.jpg",
     [("cruzeiro", 2021), ("athletico-paranaense", 2022), ("barcelona", 2023), ("betis", 2024), ("palmeiras", 2025)],
     ["Endrick", "Savinho"], "Essa é recente! Quem fez esse vai e volta?",
     "Vitor Roque! Foi pro Barcelona e voltou pro Brasil!", {"suspense": True}),
    ("Lúcio", "lzag-lucio.jpg",
     [("internacional", 1997), ("bayer-leverkusen", 2001), ("bayern-de-munique", 2004), ("inter-de-milao", 2009),
      ("juventus", 2012), ("sao-paulo", 2013), ("palmeiras", 2014), ("goa", 2015)],
     ["Juan", "Edmílson"], "Um zagueiro pentacampeão!",
     "Lúcio! Campeão da Champions com a Inter!", {"suspense": True}),
    ("Cannavaro", "lzag-cannavaro.jpg",
     [("napoli", 1991), ("parma", 1995), ("inter-de-milao", 2002), ("juventus", 2004), ("real-madrid", 2006),
      ("juventus", 2009), ("al-ahli-dubai", 2010)],
     ["Nesta", "Materazzi"], "Agora um zagueiro que foi eleito o melhor do mundo!",
     "Cannavaro! Melhor do mundo em 2006!", {"dica": ("Dica: ele foi capitão da Itália campeã em 2006.", "CAPITÃO DA ITÁLIA EM 2006!")}),
    ("Taffarel", "lgol-taffarel.jpg",
     [("internacional", 1985), ("parma", 1990), ("reggiana", 1993), ("atletico-mineiro", 1995),
      ("galatasaray", 1998), ("parma", 2001)],
     ["Dida", "Júlio César"], "Valendo o título de craque da bola: um goleiro tetracampeão!",
     "Taffarel! O goleiro do tetra! Se acertou essa, você é fera!", {"final": True, "suspense": True}),
]


def main():
    rnd = random.Random(31)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    pos[0], pos[1], pos[2] = 0, 2, 1
    R = []
    for n, (nome, foto, car, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], nome)
        assert len(set(ops)) == 3, (n, ops)
        assert 2 <= len(car) <= 9, nome
        r = {"n": n, "pergunta": "DE QUEM É ESSA CARREIRA?", "jogador": nome, "foto": foto,
             "carreira": [[c, a] for c, a in car], "opcoes": ops, "certa": pos[n - 1],
             "fala_q": f"{fq} {ops[0]}, {ops[1]} ou {ops[2]}?", "fala_r": fr, "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo o título de craque... a resposta é..."
        R.append(r)
    assert len({r["foto"] for r in R}) == len(R) == 36
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])
    print("escudos:", sorted({c for r in R for c, _ in r["carreira"]}))


if __name__ == "__main__":
    main()
