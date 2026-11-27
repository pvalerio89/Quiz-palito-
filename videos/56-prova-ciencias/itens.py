"""Gera itens.json do vídeo 56 "Prova de Ciências do 3º ano: nosso planeta, a Terra" (estilo mais humano).

44 perguntas próprias da Unidade 2 "Nosso planeta, a Terra" (capítulos 4, 5 e 6) do 3º ano, a partir da folha de
reforço e do simulado trimestral que o Patrick mandou em PDF (2026-11-25): formato da Terra (geoide), cores da Terra
vista do espaço, globo, planisfério, imagens de satélite, corrida espacial (Sputnik 1, Gagarin, Apollo 11), satélites
(GPS, Amazônia 1, mosaico da África), estrelas e planetas, cintilar, estrela-d'alva, meteoro/meteorito/estrela
cadente, céu dos desanas (plêiades), relógio biológico, animais diurnos e noturnos, sono e telas.
Do MÉDIO ao MUITO DIFÍCIL (3 níveis), como as provas anteriores. Vídeo de 15 min pra cima.
Imagem de cada pergunta: foto real da Wikimedia (fotos/<img>.jpg, com a frase numa faixa embaixo) ou cartão de caderno.
Nunca nome de aluno ou escola.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
# nível, pergunta (topo), cartão (linhas), certa, [erradas], fala da pergunta, fala da resposta, extras
P = [
    # ---------- MÉDIO ----------
    (2, "O QUE É O AZUL?", ["O azul da Terra", "vista do espaço"], "Água", ["Florestas", "Solo"],
     "Na foto da Terra tirada do espaço, o que o azul representa?",
     "Água! Os oceanos e os mares cobrem a maior parte do planeta.", {"img": "terra"}),
    (2, "O QUE É ISSO?", ["Representa a Terra", "em tamanho menor"], "Globo terrestre", ["Planisfério", "Satélite"],
     "Essa bola representa a Terra em tamanho bem menor. Como ela se chama?",
     "Globo terrestre! Ele reproduz o formato arredondado do planeta.", {"img": "globo"}),
    (2, "QUEM TEM LUZ PRÓPRIA?", ["Quem produz", "a própria luz?"], "As estrelas", ["Os planetas", "A Lua"],
     "Qual desses corpos celestes produz a própria luz?",
     "As estrelas! Elas produzem luz e calor.", {"img": "estrelas"}),
    (2, "DIURNO OU NOTURNO?", ["Coruja"], "Noturno", ["Diurno", "Os dois"],
     "A coruja é um animal de hábito diurno ou noturno?",
     "Noturno! A coruja caça de noite e descansa de dia.", {"img": "coruja"}),
    (2, "COMO SE CHAMA?", ["A Terra inteira", "numa folha plana"], "Planisfério", ["Globo terrestre", "Maquete"],
     "Esse mapa mostra a superfície inteira da Terra numa folha plana. Como ele se chama?",
     "Planisfério, também chamado de mapa-múndi! Dá pra ver o planeta inteiro de uma vez.", {"img": "planisferio"}),
    (2, "O SOL É...", ["O Sol é um..."], "Estrela", ["Planeta", "Satélite"],
     "O Sol é um planeta, uma estrela ou um satélite?",
     "Uma estrela! Uma das inúmeras estrelas que existem.", {"img": "sol", "falar_ops": False}),
    (2, "E O BRANCO?", ["O branco da Terra", "vista do espaço"], "Nuvens e gelo", ["Areia", "Fumaça"],
     "E o branco que aparece na foto da Terra, o que é?",
     "Nuvens, ou o gelo das regiões polares!", {"img": "terra2"}),
    (2, "DIURNO OU NOTURNO?", ["Borboleta"], "Diurno", ["Noturno", "Os dois"],
     "E a borboleta? Diurna ou noturna?",
     "Diurno! A borboleta voa de flor em flor durante o dia.", {"img": "borboleta"}),
    (2, "VERDADE OU MENTIRA?", ["\"A Lua só aparece", "no céu à noite\""], "Mentira", ["Verdade", "Só na lua cheia"],
     "Verdade ou mentira: a Lua só aparece no céu à noite?",
     "Mentira! A Lua também aparece no céu durante o dia.", {"img": "lua", "aviso": "PEGADINHA!"}),
    (2, "QUANTO DORMIR?", ["Uma criança", "precisa dormir..."], "9 a 11 horas", ["5 a 6 horas", "14 a 16 horas"],
     "Quantas horas por noite uma criança precisa dormir?",
     "De nove a onze horas! Dormir bem ajuda a memória.", {}),
    (2, "E O VERDE?", ["O verde da Terra", "vista do espaço"], "Florestas", ["Oceanos", "Gelo polar"],
     "E o verde, na foto da Terra vista do espaço?",
     "As florestas!", {"img": "terra3"}),
    (2, "DIURNO OU NOTURNO?", ["Morcego"], "Noturno", ["Diurno", "Os dois"],
     "O morcego é diurno ou noturno?",
     "Noturno! Ele sai pra comer quando escurece.", {"img": "morcego"}),
    (2, "POR QUÊ?", ["Nunca olhe", "direto para o Sol!"], "Queima os olhos", ["Ele muda de cor", "Dá sono"],
     "Por que nunca devemos olhar diretamente para o Sol?",
     "Porque pode provocar queimaduras nos olhos! Nunca faça isso.", {"img": "sol2"}),
    (2, "DIURNO OU NOTURNO?", ["Esquilo"], "Diurno", ["Noturno", "Os dois"],
     "O esquilo é diurno ou noturno?",
     "Diurno! Ele procura comida durante o dia.", {"img": "esquilo"}),
    # ---------- DIFÍCIL ----------
    (3, "QUAL O NOME?", ["O primeiro satélite", "do mundo"], "Sputnik 1", ["Apollo 11", "Amazônia 1"],
     "Qual foi o primeiro satélite lançado ao espaço?",
     "Sputnik um! Ele abriu a corrida ao espaço.", {"img": "sputnik"}),
    (3, "EM QUE ANO?", ["O Sputnik 1", "foi lançado em..."], "1957", ["1969", "1961"],
     "Em que ano o Sputnik um foi lançado? Mil novecentos e cinquenta e sete, sessenta e nove ou sessenta e um?",
     "Mil novecentos e cinquenta e sete! No dia quatro de outubro.", {"falar_ops": False}),
    (3, "QUEM É ELE?", ["O 1º ser humano", "a ir ao espaço"], "Yuri Gagarin", ["Santos Dumont", "Neil Armstrong"],
     "Quem foi o primeiro ser humano a viajar para fora da Terra?",
     "Yuri Gagarin, astronauta soviético, a bordo da Vostok um!", {"img": "gagarin"}),
    (3, "O QUE ELE DISSE?", ["Gagarin olhou", "pela janela", "e disse..."], "A Terra é azul!", ["Que frio!", "Cheguei na Lua!"],
     "Da cabine da nave, Gagarin olhou o planeta e disse uma frase famosa. Qual foi?",
     "A Terra é azul! Foi o primeiro a ver isso com os próprios olhos.", {"img": "vostok"}),
    (3, "QUAL É O FORMATO?", ["O formato real", "da Terra"], "Geoide", ["Esfera perfeita", "Disco plano"],
     "De longe a Terra parece uma esfera perfeita. Mas qual é o formato real dela?",
     "Geoide! A superfície tem áreas mais altas e mais baixas.", {"img": "geoide", "aviso": "TEM PEGADINHA!"}),
    (3, "DE ONDE?", ["Apollo 11 (1969)", "fotografou a Terra..."], "Da Lua", ["De Marte", "Do Sol"],
     "Em mil novecentos e sessenta e nove, a missão Apollo onze fotografou a Terra de onde?",
     "Da Lua! Uma imagem do nosso planeta feita de lá.", {"img": "apollo"}),
    (3, "O QUE É?", ["Rocha do espaço", "que entra na", "atmosfera"], "Meteoro", ["Meteorito", "Cometa"],
     "Como se chama a rocha do espaço que entra na atmosfera da Terra?",
     "Meteoro! Ela entra rápido e pega fogo.", {"aviso": "CUIDADO!"}),
    (3, "E SE CAIR NO CHÃO?", ["A rocha chegou", "até o chão!"], "Meteorito", ["Meteoro", "Estrela cadente"],
     "E quando a rocha consegue atingir a superfície do planeta, vira o quê?",
     "Meteorito! A diferença é o chão.", {"img": "meteorito"}),
    (3, "QUAL O NOME POPULAR?", ["O rastro de luz", "do meteoro no céu"], "Estrela cadente",
     ["Arco-íris", "Estrela-d'alva"],
     "E o rastro luminoso que o meteoro deixa no céu, como a gente costuma chamar?",
     "Estrela cadente! Mas não é estrela de verdade.", {}),
    (3, "COMO SE CHAMA?", ["Vários meteoros", "ao mesmo tempo"], "Chuva de meteoros", ["Eclipse", "Tempestade solar"],
     "Quando vários meteoros entram na atmosfera ao mesmo tempo, os cientistas chamam de quê?",
     "Chuva de meteoros!", {"img": "chuva"}),
    (3, "QUAL PLANETA?", ["Estrela-d'alva", "ou estrela", "da manhã"], "Vênus", ["Marte", "Júpiter"],
     "Ele é chamado de estrela-d'alva ou estrela da manhã, mas é um planeta. Qual?",
     "Vênus! Aparece ao amanhecer ou ao anoitecer.", {"img": "venus", "aviso": "PEGADINHA!"}),
    (3, "O QUE É CINTILAR?", ["Cintilar é..."], "Brilhar piscando", ["Girar sem parar", "Esquentar"],
     "O que significa a palavra cintilar?",
     "Brilhar com rápida variação de cor e de intensidade! As estrelas cintilam.", {}),
    (3, "QUEM NÃO CINTILA?", ["Brilho fixo,", "sem piscar"], "Os planetas", ["As estrelas", "O Sol"],
     "Quem tem brilho fixo e não cintila no céu?",
     "Os planetas! Eles não têm luz própria, são iluminados pelo Sol.", {"img": "planetas"}),
    (3, "DIURNO OU NOTURNO?", ["Leão"], "Noturno", ["Diurno", "Os dois"],
     "E o leão? É diurno ou noturno?",
     "Noturno! De dia ele aparece dormindo; caça quando escurece.",
     {"img": "leao", "aviso": "DERRUBA MUITA GENTE!", "suspense": True}),
    (3, "E O MARROM?", ["O marrom da Terra", "vista do espaço"], "Solo exposto", ["Nuvens", "Rios"],
     "E o marrom, na foto da Terra vista do espaço?",
     "Solo exposto! Terra sem plantas por cima.", {"img": "terra"}),
    (3, "O QUE É?", ["Relógio", "biológico"], "Ritmo do dia e da noite", ["Relógio de pulso", "Um despertador"],
     "O que é o relógio biológico?",
     "É como o corpo dos seres vivos se adapta ao período claro e ao período escuro de cada dia!", {}),
    (3, "O QUE FAZ O GPS FUNCIONAR?", ["GPS"], "Satélites", ["Meteoros", "Estrelas"],
     "O GPS do celular funciona graças a quê?",
     "Aos satélites em órbita!", {"img": "gps"}),
    # ---------- MUITO DIFÍCIL ----------
    (4, "DIURNO OU NOTURNO?", ["Saí-azul"], "Diurno", ["Noturno", "Os dois"],
     "Esse passarinho é o saí-azul. Ele é diurno ou noturno?",
     "Diurno! Na foto tirada de dia, ele está acordado no galho.", {"img": "sai"}),
    (4, "QUE ESTRELAS?", ["Os desanas chamam", "de \"nekaturu\":", "sete estrelas"], "Plêiades",
     ["Cruzeiro do Sul", "Três Marias"],
     "Os indígenas desanas, da Amazônia, chamam de nekaturu, que quer dizer sete estrelas. Que estrelas são essas?",
     "As plêiades, também chamadas de Sete Irmãs!", {"img": "pleiades"}),
    (4, "O QUE ACONTECE?", ["Quando as plêiades", "somem no oeste..."], "Começam as chuvas",
     ["Começa o frio", "Vem a lua cheia"],
     "Para os desanas, o que acontece quando as plêiades somem no lado oeste do céu?",
     "Começa o período de chuvas! Eles montam o calendário pelo movimento dos astros.", {"suspense": True}),
    (4, "QUAL SATÉLITE?", ["O 1º satélite", "100% brasileiro"], "Amazônia 1", ["Sputnik 1", "Sentinel-2A"],
     "Qual é o primeiro satélite totalmente brasileiro?",
     "Amazônia um!", {"img": "amazonia1"}),
    (4, "EM QUE ANO?", ["O Amazônia 1", "foi lançado em..."], "2021", ["2016", "1969"],
     "Em que ano o Amazônia um foi lançado? Dois mil e vinte e um, dois mil e dezesseis ou mil novecentos e sessenta e nove?",
     "Dois mil e vinte e um!", {"falar_ops": False}),
    (4, "EM QUE PAÍS?", ["Lançamento", "do Amazônia 1"], "Índia", ["Brasil", "Rússia"],
     "O satélite é brasileiro. Mas em que país foi o lançamento do Amazônia um?",
     "Na Índia! Num foguete indiano.", {"img": "pslv", "aviso": "TEM PEGADINHA!", "suspense": True}),
    (4, "PRA QUE SERVE?", ["O Amazônia 1", "monitora..."], "O desmatamento", ["Os meteoros", "As marés"],
     "Uma das funções do Amazônia um é monitorar o quê?",
     "O desmatamento! E também a agricultura e os recursos hídricos.", {"img": "desmatamento"}),
    (4, "QUANTOS?", ["Satélites que", "o GPS precisa"], "Mais de 20", ["Só 1", "Exatamente 3"],
     "De quantos satélites em órbita o GPS precisa para funcionar?",
     "Mais de vinte satélites!", {"img": "satelite", "aviso": "QUASE TODO MUNDO ERRA!"}),
    (4, "QUANTAS IMAGENS?", ["Mosaico da África", "(satélite Sentinel-2A)"], "Quase 7 mil", ["Só 1", "Umas 50"],
     "A foto da África do satélite Sentinel-dois-A é um mosaico. Quantas imagens foram usadas?",
     "Quase sete mil imagens! Até achar tudo sem nuvens.", {"img": "sentinel"}),
    (4, "POR QUE ATRAPALHA?", ["Celular antes", "de dormir"], "Luz confunde o corpo", ["A tela é fria", "O peso do aparelho"],
     "Por que usar celular antes de dormir atrapalha o sono?",
     "A luz da tela entra pelos olhos e confunde o relógio biológico!", {}),
    (4, "QUANTO TEMPO?", ["Sem telas", "antes de dormir"], "30 minutos", ["5 minutos", "3 horas"],
     "Quanto tempo, pelo menos, a gente deve ficar sem telas antes de ir pra cama?",
     "Trinta minutos! Dá pra ler um livro ou tomar um banho morno.", {}),
    (4, "E OS ADULTOS?", ["Um adulto precisa", "dormir cerca de..."], "8 horas", ["4 horas", "12 horas"],
     "E os adultos, precisam dormir cerca de quantas horas seguidas?",
     "Oito horas seguidas!", {}),
    (4, "QUANTOS ANOS?", ["Sputnik 1 (1957)", "Amazônia 1 (2021)", "Diferença?"], "64 anos", ["54 anos", "74 anos"],
     "Valendo a nota da prova! O Sputnik um foi lançado em mil novecentos e cinquenta e sete. O Amazônia um, em dois mil e vinte e um. "
     "Quantos anos se passaram entre os dois?",
     "Sessenta e quatro anos! Dois mil e vinte e um menos mil novecentos e cinquenta e sete. Se acertou essa, tirou dez em ciências!",
     {"count": 12.0, "suspense": True, "final": True}),
]


def main():
    rnd = random.Random(56)
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
