"""Gera itens.json do vídeo 45 "Prova de História do 3º ano: Transportes" (estilo mais humano, 2026-11-13).

44 perguntas próprias da Unidade 7 "Transportes: passado, presente e futuro" (livro de História do 3º ano que o Patrick
mandou em fotos, 2026-11-19): meios de transporte, transporte rodoviário e seus problemas, Av. Presidente Vargas
1958/2024, gráfico do Ipea 2010, bondes e ônibus elétricos de Belo Horizonte, leis de trânsito, tropas e tropeiros
(Debret, Rugendas, cadeiras de arruar), a chegada da ferrovia (Estrada de Ferro Mauá, maria-fumaça), evolução das
locomotivas, transporte aquático (embarcações, pesca artesanal), transporte aéreo (14-Bis, Santos Dumont),
transporte sustentável e canoa caiçara (patrimônio imaterial).
Patrick pediu só do MÉDIO ao DIFÍCIL: 3 níveis (médio, difícil, muito difícil). Vídeo de 15 min pra cima.
Imagem de cada pergunta: foto real da Wikimedia (fotos/<img>.jpg, com a frase numa faixa embaixo) ou cartão de caderno.
Nunca as fotos do caderno da criança.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
# nível, pergunta (topo), cartão (linhas), certa, [erradas], fala da pergunta, fala da resposta, extras
P = [
    # ---------- MÉDIO ----------
    (2, "QUE TRANSPORTE É ESSE?", ["Há uns 200 anos..."], "Tropa de mulas", ["Carro de boi", "Trem"],
     "Há uns duzentos anos, era assim que as mercadorias viajavam pelo Brasil, por matas e caminhos difíceis. "
     "Que transporte é esse?",
     "Tropa de mulas! Era o transporte de mercadorias mais usado naquela época.", {"img": "mula"}),
    (2, "COMO SE CHAMAVAM?", ["Os homens que", "guiavam as", "tropas de mulas"], "Tropeiros",
     ["Bandeirantes", "Maquinistas"],
     "Como se chamavam os homens que guiavam as tropas de mulas?",
     "Tropeiros! Eles viajavam de vila em vila.", {"img": "tropeiro"}),
    (2, "O QUE ELES LEVAVAM?", ["Além das mercadorias,", "os tropeiros", "levavam..."], "Notícias",
     ["Eletricidade", "Gasolina"],
     "Além de vender mercadorias, o que mais os tropeiros levavam de uma vila para outra?",
     "Notícias! Sem internet, sem telefone, a notícia chegava no lombo da mula.", {"img": "mula2"}),
    (2, "QUE APELIDO ELA TINHA?", ["Locomotiva a vapor"], "Maria-fumaça", ["Maria-chuva", "Zé-faísca"],
     "A primeira locomotiva do Brasil era movida a vapor. Que apelido ela tinha?",
     "Maria-fumaça! Por causa da nuvem de fumaça que ela soltava.", {"img": "vapor", "falar_ops": True}),
    (2, "QUEM VOOU NELE?", ["14-Bis, 1906"], "Santos Dumont", ["Dom Pedro II", "Tiradentes"],
     "Esse é o 14-Bis, em mil novecentos e seis. Quem voou nele?",
     "Santos Dumont! O brasileiro conhecido como pai da aviação.", {"img": "14bis"}),
    (2, "QUEM DEVE RESPEITAR?", ["Quem deve respeitar", "as leis de", "trânsito?"], "Todos",
     ["Só os motoristas", "Só os pedestres"],
     "Quem deve respeitar as leis de trânsito?",
     "Todos! Motorista, ciclista e pedestre.", {"aviso": "TEM PEGADINHA!"}),
    (2, "QUE PROBLEMA É ESSE?", ["Carros parados", "na avenida"], "Congestionamento",
     ["Enchente", "Poluição visual"],
     "Carros e mais carros parados na avenida. Que problema é esse?",
     "Congestionamento! Excesso de veículos faz as pessoas perderem muito tempo.", {"img": "transito"}),
    (2, "QUE BARCO É ESSE?", ["Rio Negro, Manaus"], "Chalana", ["Jangada", "Submarino"],
     "No rio Negro, em Manaus, esse barco leva passageiros e carga. Que barco é esse?",
     "Chalana! Muito usada nos rios da Amazônia.", {}),
    (2, "O QUE É ISSO?", ["Rio de Janeiro"], "Bonde", ["Metrô", "Ônibus"],
     "Ele anda sobre trilhos pelas ruas do Rio de Janeiro. O que é isso?",
     "Bonde! Há uns setenta anos era o principal transporte público de muitas cidades.", {"img": "bonde"}),
    (2, "QUE TIPO DE TRANSPORTE?", ["Navio, ônibus,", "avião e trem", "levam muita gente"], "Coletivo",
     ["Individual", "Particular"],
     "Navio, ônibus, avião e trem levam muita gente junta. Que tipo de transporte eles são?",
     "Coletivos! Transportam muitas pessoas de uma vez.", {"img": "transatlantico"}),
    (2, "QUANTO TEMPO DURAVA?", ["Europa → Brasil", "de navio,", "antigamente"], "Meses",
     ["Horas", "Minutos"],
     "Antigamente, quanto tempo durava uma viagem de navio da Europa até o Brasil?",
     "Meses! Hoje, de avião, leva só algumas horas.", {"falar_ops": True}),
    (2, "QUE PESCA É ESSA?", ["Pesca feita com o", "trabalho das mãos", "do ser humano"], "Artesanal",
     ["Industrial", "Elétrica"],
     "A pesca feita com o trabalho das mãos do ser humano, como nessa canoa, se chama pesca o quê?",
     "Artesanal! Como a pesca de canoa na Reserva Mamirauá, no Amazonas.", {"img": "pesca"}),
    (2, "POR QUE POLUI MENOS?", ["Ônibus elétrico"], "Não solta gases", ["É mais rápido", "É mais bonito"],
     "Por que o ônibus elétrico polui menos o ar?",
     "Porque não solta gases poluentes! Ele funciona com bateria.", {"img": "trolebus"}),
    (2, "ONDE SE RECARREGAM?", ["Carros elétricos", "funcionam com", "baterias"], "Postos especiais",
     ["Na chuva", "No posto de gasolina"],
     "Carros e ônibus elétricos funcionam com baterias. Onde elas são recarregadas?",
     "Em postos especiais de recarga!", {"img": "onibus-eletrico"}),
    # ---------- DIFÍCIL ----------
    (3, "EM QUE ANO?", ["Primeira ferrovia", "do Brasil:", "30 de abril de..."], "1854", ["1822", "1889"],
     "Agora complica! A primeira ferrovia do Brasil foi inaugurada em trinta de abril de que ano?",
     "Mil oitocentos e cinquenta e quatro! Na Estrada de Ferro Mauá, com a locomotiva Baroneza, essa da foto.", {"img": "maua", "falar_ops": True}),
    (3, "ATÉ ONDE ELA IA?", ["Estrada de Ferro Mauá:", "do Porto de Mauá", "até..."], "Fragoso",
     ["Petrópolis", "Santos"],
     "A Estrada de Ferro Mauá ligava o Porto de Mauá até onde?",
     "Até Fragoso, no Rio de Janeiro! O nome da companhia falava de Petrópolis, mas o primeiro trecho ia até Fragoso.",
     {"aviso": "TEM PEGADINHA!", "suspense": True}),
    (3, "QUANTOS QUILÔMETROS?", ["Tamanho da", "Estrada de", "Ferro Mauá"], "14,5 km", ["145 km", "1.450 km"],
     "Quantos quilômetros tinha a Estrada de Ferro Mauá?",
     "Catorze quilômetros e meio! Bem curtinha.", {"falar_ops": True}),
    (3, "QUANTOS ANOS DEPOIS?", ["Locomotiva a vapor:", "inventada em 1814,", "chegou aqui em 1854"], "40 anos",
     ["30 anos", "50 anos"],
     "A locomotiva a vapor foi inventada em mil oitocentos e catorze e chegou ao Brasil em mil oitocentos e cinquenta "
     "e quatro. Quantos anos depois?",
     "Quarenta anos! Cinquenta e quatro menos catorze.",
     {"dica": ("Dica: é conta de menos!", "CONTA DE MENOS!"), "count": 10.0}),
    (3, "QUAL A VELOCIDADE?", ["Uma das primeiras", "locomotivas a vapor"], "6,4 km/h", ["64 km/h", "100 km/h"],
     "A primeira locomotiva a vapor, de mil oitocentos e catorze, andava a quantos quilômetros por hora?",
     "Seis vírgula quatro! Quase a velocidade de uma pessoa andando rápido.",
     {"img": "vapor2", "falar_ops": True, "aviso": "DERRUBA MUITA GENTE!"}),
    (3, "QUAL A VELOCIDADE?", ["Locomotiva", "a diesel (1902)"], "100 km/h", ["13 km/h", "400 km/h"],
     "E a locomotiva a diesel, que surgiu em mil novecentos e dois, chegava a quanto?",
     "Cem quilômetros por hora! E aos poucos substituiu as outras.", {"img": "diesel", "falar_ops": True}),
    (3, "COMO ESSE TREM ANDA?", ["Trem de levitação", "magnética (Maglev)"], "Flutua nos trilhos",
     ["Com vapor", "Puxado por cavalos"],
     "Esse é o Maglev, o trem de levitação magnética. Como ele anda?",
     "Flutua sobre os trilhos! E passa de quatrocentos quilômetros por hora.", {"img": "maglev"}),
    (3, "QUAL É ESSE TREM?", ["Trem de grande", "velocidade, sem", "locomotiva"], "TGV",
     ["Maria-fumaça", "Bonde"],
     "Trem de grande velocidade, elétrico e sem locomotiva, que chega a trezentos e vinte quilômetros por hora. Qual é?",
     "TGV! O primeiro modelo começou a funcionar em mil novecentos e setenta e dois.", {"img": "tgv"}),
    (3, "DE ONDE ELE ERA?", ["Gravura de", "Jean-Baptiste Debret"], "França", ["Portugal", "Brasil"],
     "O pintor Jean-Baptiste Debret desenhou muito o Brasil antigo. De que país ele era?",
     "Da França! Ele veio com a Missão Artística Francesa.", {"img": "debret", "falar_ops": True}),
    (3, "QUEM CARREGAVA?", ["Cadeira de arruar"], "Pessoas escravizadas", ["Cavalos", "Bois"],
     "Nas cidades antigas, a elite andava em cadeiras de arruar. Quem carregava essas cadeiras?",
     "Pessoas escravizadas! Esse transporte era só para poucos.", {"img": "liteira"}),
    (3, "E A MAIORIA?", ["Na época das tropas,", "a maioria das", "pessoas andava..."], "A pé",
     ["De cadeirinha", "A cavalo"],
     "E na época das tropas, como andava a maioria das pessoas?",
     "A pé! Cadeirinha era só para a elite.", {"aviso": "TEM PEGADINHA!", "suspense": True}),
    (3, "QUANTO É UM SÉCULO?", ["Século é", "um período de..."], "100 anos", ["10 anos", "1.000 anos"],
     "O livro diz que as tropas existiam há uns dois séculos. Mas quanto tempo é um século?",
     "Cem anos! Então dois séculos são duzentos anos.", {"falar_ops": True}),
    (3, "O MAIS USADO", ["Cidades do Brasil", "(Ipea, 2010):", "o mais usado é..."], "Transporte público",
     ["Carro", "Moto"],
     "Num gráfico do Ipea, de dois mil e dez, qual é o transporte mais usado nas cidades brasileiras?",
     "Transporte público! Quarenta e quatro por cento.", {"img": "brt"}),
    (3, "QUANTAS PESSOAS?", ["De cada 100", "pessoas, quantas", "vão de carro?"], "24", ["44", "13"],
     "No mesmo gráfico, de cada cem pessoas, quantas usam o carro?",
     "Vinte e quatro! Quarenta e quatro é o transporte público, e treze é a moto.",
     {"falar_ops": True, "sabia": "Ipea 2010: transporte público 44%, carro 24%, moto 13%, a pé 12% e bicicleta 7%."}),
    (3, "O MENOS USADO", ["Cidades do Brasil", "(Ipea, 2010):", "o MENOS usado é..."], "Bicicleta",
     ["A pé", "Moto"],
     "E qual é o meio de transporte menos usado nas cidades?",
     "Bicicleta! Só sete por cento. Faltam ciclovias em muitas cidades.",
     {"img": "bicicleta", "aviso": "DERRUBA MUITA GENTE!"}),
    # ---------- MUITO DIFÍCIL ----------
    (4, "QUANTOS ANOS?", ["Bondes em", "Belo Horizonte:", "de 1902 a 1963"], "61 anos", ["51 anos", "71 anos"],
     "Agora a parte que reprova! Em Belo Horizonte, os bondes elétricos rodaram de mil novecentos e dois a mil "
     "novecentos e sessenta e três. Por quantos anos?",
     "Sessenta e um anos! Sessenta e três menos dois.",
     {"falar_ops": True, "count": 12.0, "dica": ("Dica: faz 63 menos 2!", "63 − 2")}),
    (4, "QUANTOS ANOS?", ["Ônibus elétricos", "em BH:", "de 1953 a 1969"], "16 anos", ["26 anos", "6 anos"],
     "E os ônibus elétricos de Belo Horizonte: de mil novecentos e cinquenta e três a mil novecentos e sessenta e nove. "
     "Quantos anos?",
     "Dezesseis anos! Bem menos que os bondes.", {"falar_ops": True, "count": 12.0}),
    (4, "QUANTOS ANOS?", ["Av. Presidente Vargas:", "foto de 1958 e", "foto de 2024"], "66 anos",
     ["56 anos", "76 anos"],
     "A avenida Presidente Vargas, no Rio, foi fotografada em mil novecentos e cinquenta e oito e em dois mil e vinte "
     "e quatro. Quantos anos se passaram?",
     "Sessenta e seis anos! E o número de carros aumentou muito.",
     {"img": "vargas", "falar_ops": True, "count": 12.0}),
    (4, "HÁ QUANTOS ANOS?", ["O 14-Bis voou", "em 1906. Hoje", "estamos em 2026."], "120 anos",
     ["100 anos", "110 anos"],
     "O 14-Bis voou em mil novecentos e seis. Estamos em dois mil e vinte e seis. Há quantos anos foi esse voo?",
     "Cento e vinte anos!", {"falar_ops": True, "count": 10.0}),
    (4, "EM QUE CIDADE?", ["Primeiro voo", "do 14-Bis"], "Paris", ["Rio de Janeiro", "São Paulo"],
     "Santos Dumont era brasileiro. Mas em que cidade o 14-Bis fez seu voo famoso?",
     "Em Paris, na França! No dia vinte e três de outubro de mil novecentos e seis.",
     {"img": "dumont", "falar_ops": True, "aviso": "TEM PEGADINHA!", "suspense": True}),
    (4, "O QUE É?", ["Patrimônio", "imaterial é..."], "Saberes e fazeres", ["Prédios antigos", "Dinheiro guardado"],
     "O que é patrimônio imaterial?",
     "Saberes e fazeres passados de geração em geração!",
     {"sabia": "Patrimônio imaterial: o modo de construir um objeto, as danças, as festas e as receitas tradicionais."}),
    (4, "QUAL É IMATERIAL?", ["Qual destes é", "patrimônio", "imaterial?"], "O modo de fazer canoa",
     ["Uma ponte velha", "Um navio"],
     "Qual destes é patrimônio imaterial?",
     "O modo de fazer a canoa caiçara! É um saber, não um objeto.", {"aviso": "DERRUBA MUITA GENTE!"}),
    (4, "QUANTOS TRONCOS?", ["A canoa caiçara", "é feita de..."], "Um tronco só", ["Dois troncos", "Dez tábuas"],
     "A canoa caiçara é feita de quantos troncos de árvore?",
     "Um tronco só! Esculpido inteirinho, de cedro ou guapuruvu.", {"img": "canoa"}),
    (4, "QUEM FAZ A CANOA?", ["Quem esculpe", "a canoa caiçara?"], "Mestre canoeiro",
     ["Maquinista", "Tropeiro"],
     "Quem esculpe a canoa caiçara e ensina a técnica aos mais jovens?",
     "O mestre canoeiro!", {}),
    (4, "O QUE QUER DIZER?", ["Na fala caiçara,", "\"tirar uma canoa\"", "significa..."], "Construir a canoa",
     ["Afundar a canoa", "Pescar"],
     "Na linguagem caiçara, o que significa tirar uma canoa?",
     "Construir a canoa! Tirar ela de dentro do tronco.", {"aviso": "QUASE TODO MUNDO ERRA!", "suspense": True}),
    (4, "ONDE ELA É USADA?", ["Canoa caiçara", "(Paraty, RJ)"], "Litoral sudeste", ["Sertão nordestino", "Pampa gaúcho"],
     "Em que região do Brasil a canoa caiçara é mais usada?",
     "No litoral sudeste! Na pesca, no esporte e no transporte de pessoas.", {"img": "paraty"}),
    (4, "QUAL A VELOCIDADE?", ["Locomotiva", "elétrica (1879)"], "13 km/h", ["130 km/h", "1,3 km/h"],
     "A locomotiva elétrica, lançada em mil oitocentos e setenta e nove, andava a quanto?",
     "Treze quilômetros por hora! O dobro da maria-fumaça.", {"img": "eletrica", "falar_ops": True}),
    (4, "POR QUE TROCARAM?", ["Por volta de 1950,", "os ônibus", "substituíram os bondes"],
     "Não precisam de trilhos", ["Eram mais antigos", "Andavam na água"],
     "Por volta de mil novecentos e cinquenta, os ônibus começaram a substituir os bondes. Por quê?",
     "Porque não precisam de trilhos! Podem ir por qualquer rua.", {}),
    (4, "QUEM FALTA?", ["Nossas embarcações:", "indígenas,", "africanos e..."], "Europeus",
     ["Japoneses", "Australianos"],
     "A variedade de embarcações do Brasil vem da influência de indígenas, africanos e de quem mais?",
     "Europeus! Os povos que formaram o Brasil.", {"img": "jangada", "falar_ops": True}),
    (4, "QUANTO MAIS RÁPIDO?", ["TGV: 320 km/h", "Diesel: 100 km/h", "Diferença?"], "220 km/h",
     ["120 km/h", "420 km/h"],
     "Valendo a nota da prova! O TGV chega a trezentos e vinte quilômetros por hora. A locomotiva a diesel, a cem. "
     "Quantos quilômetros por hora o TGV anda a mais?",
     "Duzentos e vinte! Trezentos e vinte menos cem. Se acertou essa, tirou dez em história!",
     {"falar_ops": True, "count": 12.0, "suspense": True, "final": True}),
]


def main():
    rnd = random.Random(45)
    pos = [0, 1, 2] * 15
    rnd.shuffle(pos)
    R = []
    for n, (nivel, perg, cartao, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        if ex.get("falar_ops", True):
            fq = f"{fq} {ops[0]}, {ops[1]} ou {ops[2]}?"
        r = {"n": n, "nivel": nivel, "pergunta": perg, "cartao": cartao, "foto": f"q{n}.png",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": fq, "fala_r": fr, "count": ex.get("count", 8.0)}
        if "img" in ex:
            r["img"] = ex["img"]
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo a nota... a resposta é..."
        R.append(r)
    assert len(R) == 44 and len({tuple(r["cartao"]) for r in R}) == 44, len(R)
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], [sum(r["nivel"] == k for r in R) for k in (2, 3, 4)],
          sorted({r["img"] for r in R if "img" in r}))


if __name__ == "__main__":
    main()
