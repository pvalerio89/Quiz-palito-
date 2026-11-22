"""Gera itens.json do vídeo 52 "Jogadores de A a Z — PARTE 2" (estilo mais humano, 2026-11-22).

32 perguntas próprias: o cartão mostra a LETRA gigante + uma pista (título, apelido, clube, Copa...) e as 3
alternativas são jogadores com a MESMA letra. Na resposta o cartão troca para a FOTO REAL do craque (fotos do
vídeo 19, Wikimedia Commons; créditos em creditos.json e na tela final). Nenhuma resposta repete os nomes do
vídeo 02 (parte 1). Letras I, X e Y não têm foto livre: a resposta mostra o nome num cartão.
Fáceis primeiro (craques do Brasil), letras e nomes difíceis no fim. Fatos conferidos em 2026-11-22.
Uso: py -3 itens.py   (copia as fotos e os créditos do vídeo 19)
"""
import json, os, random, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
V19 = os.path.join(VIDEOS, "19-monte-seu-clube")

# letra, pista (linhas do cartão), certa, [erradas], foto do vídeo 19 (None = cartão com o nome), chave em creditos,
# fala da pergunta (sem as alternativas), fala da resposta, extras
P = [
    ("R", ["O FENÔMENO,", "camisa 9 do PENTA"], "RONALDO", ["ROMÁRIO", "RICHARLISON"], "lca-ronaldo-fenomeno", "Ronaldo Fenômeno",
     "Começando fácil, letra R: o Fenômeno, camisa nove do Penta!", "Ronaldo Fenômeno! Oito gols na Copa de 2002. Começou bem?", {"count": 5.0}),
    ("M", ["Lateral do Brasil,", "5 CHAMPIONS", "no Real Madrid"], "MARCELO", ["MAICON", "MILITÃO"], "llat-marcelo", "Marcelo",
     "Letra M: o lateral brasileiro que ganhou cinco Champions pelo Real Madrid.", "Marcelo! O lateral do cabelão e do drible.", {"count": 5.0}),
    ("N", ["Goleiro ALEMÃO,", "campeão da", "Copa de 2014"], "NEUER", ["NAVAS", "NETO"], "gol-neuer", "Neuer",
     "Letra N: o goleiro alemão campeão da Copa de 2014.", "Neuer! Aquele que joga quase de líbero.", {}),
    ("D", ["Meia BELGA,", "10 anos no", "Manchester City"], "DE BRUYNE", ["DOKU", "DYBALA"], "mei-de-bruyne", "De Bruyne",
     "Letra D: o meia belga que passou dez anos no Manchester City.", "De Bruyne! O rei das assistências.", {}),
    ("E", ["Joia do Palmeiras,", "o \"MESSINHO\""], "ESTÊVÃO", ["ENDRICK", "EVERTON"], "joia-estevao", "Estêvão",
     "Agora uma joia do Brasil. Letra E: o garoto do Palmeiras apelidado de Messinho.", "Estêvão! Saiu do Palmeiras pro Chelsea.", {}),
    ("S", ["Atacante", "SUL-COREANO,", "ídolo do Tottenham"], "SON", ["SAKA", "SANÉ"], "pe-son", "Son",
     "Letra S: o atacante sul-coreano, ídolo do Tottenham.", "Son! Capitão da Coreia do Sul.", {}),
    ("B", ["Goleiro ITALIANO,", "campeão do mundo", "em 2006"], "BUFFON", ["BONUCCI", "BAGGIO"], "lgol-buffon", "Buffon",
     "Letra B: o goleiro italiano campeão do mundo em 2006.", "Buffon! Jogou até os quarenta e cinco anos.", {}),
    ("C", ["Goleiro ESPANHOL", "do Real Madrid,", "campeão em 2010"], "CASILLAS", ["COURTOIS", "CÉSAR"], "lgol-casillas", "Casillas",
     "Cuidado, que essa tem pegadinha! Letra C: o goleiro espanhol do Real Madrid, campeão do mundo em 2010.",
     "Casillas! O Courtois também jogou no Real, mas é belga e nunca ganhou Copa.", {"aviso": "TEM PEGADINHA!"}),
    ("H", ["Lateral", "MARROQUINO", "do PSG"], "HAKIMI", ["HAZARD", "HUMMELS"], "ld-hakimi", "Hakimi",
     "Letra H: o lateral marroquino do PSG.", "Hakimi! Um dos laterais mais rápidos do mundo.", {}),
    ("K", ["Volante ALEMÃO", "do Bayern,", "camisa 6"], "KIMMICH", ["KROOS", "KHEDIRA"], "vol-kimmich", "Kimmich",
     "Letra K: o volante alemão do Bayern, camisa seis.", "Kimmich! O Kroos era do Real Madrid.", {}),
    ("L", ["Maior ARTILHEIRO", "da história", "do Chelsea"], "LAMPARD", ["LINEKER", "LINGARD"], "lmei-lampard", "Lampard",
     "Letra L: o maior artilheiro da história do Chelsea. E ele era meia!", "Lampard! Duzentos e onze gols pelo Chelsea.",
     {"sabia": "Lampard fez 211 gols pelo Chelsea jogando no meio-campo."}),
    ("P", ["Capitão do Barça", "do CABELÃO", "enrolado"], "PUYOL", ["PIQUÉ", "PEDRI"], "lzag-puyol", "Puyol",
     "Letra P: o zagueiro capitão do Barcelona, aquele do cabelão enrolado.", "Puyol! Fez o gol que levou a Espanha à final de 2010.", {}),
    ("T", ["Goleiro do Brasil", "no TETRA, 1994"], "TAFFAREL", ["THIAGO SILVA", "TITE"], "lgol-taffarel", "Taffarel",
     "Letra T: o goleiro do Brasil no Tetra, em 1994.", "Taffarel! Sai que é sua, Taffarel!", {}),
    ("G", ["Zagueiro CROATA", "do Manchester City"], "GVARDIOL", ["GÖTZE", "GAVI"], "zag2-gvardiol", "Gvardiol",
     "Letra G: o zagueiro croata do Manchester City.", "Gvardiol! Aquele da máscara na Copa de 2022.", {}),
    ("R", ["Volante espanhol,", "BOLA DE OURO", "2024"], "RODRI", ["RAMOS", "RAÚL"], "vol-rodri", "Rodri",
     "Letra R de novo: o volante espanhol que ganhou a Bola de Ouro de 2024.", "Rodri! O Vini Júnior ficou em segundo.", {}),
    ("A", ["Lateral INGLÊS", "que trocou o Liverpool", "pelo Real Madrid"], "ALEXANDER-ARNOLD", ["ALABA", "ALBA"], "ld-alexander-arnold", "Alexander-Arnold",
     "Letra A: o lateral inglês que trocou o Liverpool pelo Real Madrid.", "Alexander-Arnold! Foi pro Real em 2025.", {}),
    ("O", ["Capitão", "NORUEGUÊS", "do Arsenal"], "ØDEGAARD", ["OLISE", "OBLAK"], "mei-degaard", "Ødegaard",
     "Letra O: o capitão norueguês do Arsenal.", "Ødegaard! Estreou na seleção com quinze anos.", {}),
    ("W", ["Meia ALEMÃO,", "contratado pelo", "Liverpool em 2025"], "WIRTZ", ["WERNER", "WALKER"], "dez-wirtz", "Wirtz",
     "Letra W: o meia alemão contratado pelo Liverpool em 2025.", "Wirtz! Veio do Bayer Leverkusen.", {}),
    ("J", ["Atacante do Brasil,", "campeão do Mundial", "2025 pelo Chelsea"], "JOÃO PEDRO", ["JORGINHO", "JOELINTON"], "joia-joao-pedro", "João Pedro",
     "Letra J: o atacante brasileiro campeão do Mundial de Clubes de 2025 pelo Chelsea.", "João Pedro! Fez gol na final contra o PSG.", {}),
    ("Z", ["Lateral ARGENTINO,", "ídolo da", "Inter de Milão"], "ZANETTI", ["ZAMORANO", "ZABALETA"], "llat-zanetti", "Zanetti",
     "Essa derruba muita gente! Letra Z: o lateral argentino, ídolo da Inter de Milão.",
     "Zanetti! O Zamorano também jogou na Inter, mas era atacante e chileno.", {"aviso": "DERRUBA MUITA GENTE!"}),
    ("F", ["Lateral FRANCÊS", "do Real Madrid"], "FERLAND MENDY", ["FRIMPONG", "FEKIR"], "le-ferland-mendy", "Ferland Mendy",
     "Letra F: o lateral francês do Real Madrid.", "Ferland Mendy! Lateral esquerdo do Real desde 2019.", {}),
    ("I", ["Atacante SUECO,", "contratação recorde", "do Liverpool"], "ISAK", ["IMMOBILE", "ICARDI"], None, None,
     "Letra I: o atacante sueco que virou a contratação recorde do Liverpool em 2025.", "Isak! A maior contratação da história do futebol inglês.",
     {"dica": ("Dica: ele jogava no Newcastle!", "JOGAVA NO NEWCASTLE!")}),
    ("V", ["Ex-Athletico, foi", "pro BARCELONA", "com 18 anos"], "VITOR ROQUE", ["VAGNER LOVE", "VINI JR."], "joia-vitor-roque", "Vitor Roque",
     "Letra V: o atacante que saiu do Athletico e foi pro Barcelona com dezoito anos.", "Vitor Roque! O Tigrinho.", {}),
    ("M", ["Zagueiro ITALIANO,", "25 anos só", "no Milan"], "MALDINI", ["MATERAZZI", "MARCHISIO"], "lzag-maldini", "Maldini",
     "Agora as lendas! Letra M: o zagueiro italiano que jogou vinte e cinco anos só no Milan.", "Maldini! Cinco Champions com a mesma camisa.",
     {"aviso": "AGORA SÓ LENDA!"}),
    ("R", ["GOLEIRO que fez", "mais de 100 GOLS"], "ROGÉRIO CENI", ["RAFAEL", "RENAN"], "lgol-rogerio-ceni", "Rogério Ceni",
     "Letra R: o goleiro que fez mais de cem gols na carreira!", "Rogério Ceni! Cento e trinta e um gols pelo São Paulo.",
     {"sabia": "Rogério Ceni fez 131 gols, quase todos de falta e pênalti."}),
    ("L", ["Atacante argentino,", "CAPITÃO da", "Inter de Milão"], "LAUTARO", ["LO CELSO", "LAMELA"], "ca-lautaro", "Lautaro",
     "Letra L: o atacante argentino, capitão da Inter de Milão.", "Lautaro Martínez! O Touro.", {}),
    ("C", ["Camisa 14 da", "LARANJA MECÂNICA", "de 1974"], "CRUYFF", ["COCU", "CLARENCE SEEDORF"], "ldez-cruyff", "Cruyff",
     "Letra C: o camisa quatorze da Laranja Mecânica de 1974.", "Cruyff! Inventou até um drible, o giro de Cruyff.", {"suspense": True}),
    ("B", ["O \"KAISER\": campeão", "do mundo como", "JOGADOR e TÉCNICO"], "BECKENBAUER", ["BALLACK", "BIERHOFF"], "lzag-beckenbauer", "Beckenbauer",
     "Letra B: o Kaiser, campeão do mundo como jogador e como técnico da Alemanha.", "Beckenbauer! Ganhou a Copa de 1974 jogando e a de 1990 como técnico.", {}),
    ("X", ["CAPITÃO da Suíça,", "ex-Arsenal"], "XHAKA", ["XISCO", "XABI"], None, None,
     "Letra xis, das difíceis: o capitão da Suíça, que jogou anos no Arsenal.", "Xhaka! Granit Xhaka, o volante da Suíça.", {"aviso": "LETRA DIFÍCIL!"}),
    ("K", ["Ponta GEORGIANO,", "o \"KVARADONA\""], "KVARATSKHELIA", ["KOLAROV", "KUBO"], "pe-kvaratskhelia", "Kvaratskhelia",
     "Letra K: o ponta da Geórgia, apelidado de Kvaradona.", "Kvaratskhelia! Ninguém consegue falar esse nome de primeira.", {}),
    ("P", ["Goleiro TCHECO", "que jogava", "de CAPACETE"], "PETR ČECH", ["PICKFORD", "PATRÍCIO"], "lgol-petr-cech", "Petr Čech",
     "Letra P: o goleiro tcheco que jogava de capacete.", "Petr Čech! Usava o capacete depois de uma pancada na cabeça.",
     {"suspense": True, "dica": ("Dica: foi ídolo do Chelsea!", "ÍDOLO DO CHELSEA!")}),
    ("Y", ["O ÚNICO goleiro", "BOLA DE OURO", "(1963)"], "YASHIN", ["YAKIN", "YORKE"], None, None,
     "Valendo o título de craque do alfabeto! Letra Y: o único goleiro da história que ganhou a Bola de Ouro, em 1963.",
     "Yashin! O Aranha Negra, da antiga União Soviética. Se acertou essa, você manja de futebol!",
     {"count": 10.0, "suspense": True, "final": True}),
]


def main():
    rnd = random.Random(52)
    pos = [0, 1, 2] * 11
    rnd.shuffle(pos)
    pos[0], pos[1] = 1, 2
    os.makedirs(os.path.join(HERE, "fotos"), exist_ok=True)
    cred19 = json.load(open(os.path.join(V19, "creditos.json"), encoding="utf-8"))
    cred = {}
    R = []
    for n, (letra, pista, certo, err, foto, ck, fq, fr, ex) in enumerate(P, 1):
        nomes = list(err)
        nomes.insert(pos[n - 1], certo)
        assert len(set(nomes)) == 3 and all(x[0] == letra or x.startswith("Ø") and letra == "O" for x in nomes), (n, nomes)
        r = {"n": n, "letra": letra, "pista": pista, "pergunta": f"JOGADOR COM A LETRA {letra}", "foto": f"q{n}.png",
             "opcoes": nomes, "certa": pos[n - 1], "fala_q": f"{fq} {nomes[0].title()}, {nomes[1].title()} ou {nomes[2].title()}?",
             "fala_r": fr, "count": ex.get("count", 7.0)}
        if foto:
            shutil.copy(os.path.join(V19, "fotos", foto + ".jpg"), os.path.join(HERE, "fotos", foto + ".jpg"))
            r["foto_jogador"] = foto + ".jpg"
            cred[ck] = cred19[ck]
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
    json.dump(cred, open(os.path.join(HERE, "creditos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], sorted({r["letra"] for r in R}), len(cred), "fotos")


if __name__ == "__main__":
    main()
