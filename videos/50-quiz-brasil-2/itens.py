"""Gera itens.json do vídeo 50 "QUIZ DO BRASIL 2" (estilo mais humano, layout modelo-opcoes).

32 perguntas NOVAS sobre o Brasil (nenhuma igual às do vídeo 06): lugares, bichos, comidas, história, cultura.
Cada pergunta tem uma FOTO REAL (Wikimedia Commons; créditos em creditos.json e na tela final) e 3 alternativas.
Das fáceis às difíceis. Fatos conferidos em 2026-11-20.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))

# foto, texto curto do topo, certa, [2 erradas], fala da pergunta (entrada + pergunta + alternativas), fala da resposta, extras
P = [
    ("cristo", "ONDE FICA ESSE MONUMENTO?", "RIO DE JANEIRO", ["SÃO PAULO", "SALVADOR"],
     "Pra esquentar! Em qual cidade fica o Cristo Redentor?",
     "Rio de Janeiro! Lá no alto do Corcovado. Começou bem?", {"count": 4.0}),
    ("brigadeiro", "QUAL É O NOME DESSE DOCE?", "BRIGADEIRO", ["BEIJINHO", "CAJUZINHO"],
     "Agora uma de festa de aniversário! Qual é o nome desse docinho?",
     "Brigadeiro! O rei da festa!", {"count": 4.0}),
    ("tucano", "QUE AVE É ESSA?", "TUCANO", ["ARARA", "PAPAGAIO"],
     "Olha esse bico! Que ave é essa?",
     "Tucano! Aquele bico enorme é levinho, viu?", {"count": 5.0}),
    ("maracana", "QUE ESTÁDIO É ESSE?", "MARACANÃ", ["MINEIRÃO", "MORUMBI"],
     "Bora pro futebol! Que estádio famoso é esse, no Rio?",
     "Maracanã! Palco de duas finais de Copa do Mundo!", {}),
    ("onca", "MAIOR FELINO DAS AMÉRICAS?", "ONÇA-PINTADA", ["JAGUATIRICA", "PUMA"],
     "Agora um bicho bravo! Qual é o maior felino das Américas?",
     "Onça-pintada! E ela adora nadar!", {}),
    ("capivara", "MAIOR ROEDOR DO MUNDO?", "CAPIVARA", ["PACA", "CUTIA"],
     "Esse aqui é o queridinho da internet! Qual é o maior roedor do mundo?",
     "Capivara! A mais tranquila do Brasil!", {}),
    ("pao-de-queijo", "DE QUAL ESTADO É ESSE PETISCO?", "MINAS GERAIS", ["GOIÁS", "PARANÁ"],
     "Hora do lanche! O pão de queijo é típico de qual estado?",
     "Minas Gerais! Com um cafezinho, uai!", {}),
    ("cataratas", "ONDE FICAM AS CATARATAS?", "PARANÁ", ["SANTA CATARINA", "MATO GROSSO DO SUL"],
     "Olha que lugar lindo! As Cataratas do Iguaçu ficam em qual estado?",
     "Paraná! Lá em Foz do Iguaçu, na divisa com a Argentina!", {}),
    ("chimarrao", "DE QUAL REGIÃO É ESSA TRADIÇÃO?", "SUL", ["NORDESTE", "NORTE"],
     "Agora uma tradição! O chimarrão é a cara de qual região?",
     "Sul! O gaúcho não larga a cuia, tchê!", {}),
    ("acai", "DE ONDE VEM O AÇAÍ?", "REGIÃO NORTE", ["REGIÃO SUL", "CENTRO-OESTE"],
     "E o açaí, vem de qual região do Brasil?",
     "Região Norte! Lá no Pará se come açaí com peixe!", {"sabia": "NO PARÁ, AÇAÍ SE COME COM PEIXE"}),
    ("pelourinho", "PRIMEIRA CAPITAL DO BRASIL?", "SALVADOR", ["RIO DE JANEIRO", "RECIFE"],
     "Agora uma de história! Qual foi a primeira capital do Brasil?",
     "Salvador! Foi capital por mais de duzentos anos!", {}),
    ("tiradentes", "QUANDO É O FERIADO DELE?", "21 DE ABRIL", ["7 DE SETEMBRO", "15 DE NOVEMBRO"],
     "Esse é o Tiradentes! Em que dia cai o feriado de Tiradentes?",
     "Vinte e um de abril! Quem acertou merece um dia de folga!", {}),
    ("frevo", "DE QUAL ESTADO É O FREVO?", "PERNAMBUCO", ["BAHIA", "CEARÁ"],
     "Bora pro Carnaval! O frevo, com essas sombrinhas coloridas, é de qual estado?",
     "Pernambuco! O frevo nasceu em Recife!", {}),
    ("lencois", "ONDE FICA ESSE PARQUE?", "MARANHÃO", ["CEARÁ", "PIAUÍ"],
     "Parece deserto, mas tem lagoa! Os Lençóis Maranhenses ficam em qual estado?",
     "Maranhão! Tava até no nome, hein?", {"aviso": "TÁ NA CARA!"}),
    ("pedro-i", "QUEM PROCLAMOU A INDEPENDÊNCIA?", "DOM PEDRO I", ["DOM PEDRO II", "TIRADENTES"],
     "Cuidado, que essa engana! Quem proclamou a Independência do Brasil?",
     "Dom Pedro primeiro! O segundo era o filho dele!", {"aviso": "TEM PEGADINHA!"}),
    ("taca", "QUANTAS COPAS O BRASIL TEM?", "5", ["4", "6"],
     "Essa todo brasileiro tem que saber! Quantas Copas do Mundo o Brasil já ganhou?",
     "Cinco! Ninguém ganhou mais que o Brasil!", {}),
    ("ouro-preto", "EM QUAL ESTADO FICA OURO PRETO?", "MINAS GERAIS", ["GOIÁS", "BAHIA"],
     "Agora uma cidade histórica! Ouro Preto fica em qual estado?",
     "Minas Gerais! Cheia de igrejas da época do ouro!", {}),
    ("pantanal", "ONDE FICA O PANTANAL?", "MT E MS", ["GO E TO", "PA E AM"],
     "Bora pro Centro-Oeste! O Pantanal fica principalmente em quais estados?",
     "Mato Grosso e Mato Grosso do Sul! A maior planície alagada do mundo!", {}),
    ("encontro-aguas", "ONDE É O ENCONTRO DAS ÁGUAS?", "MANAUS", ["BELÉM", "PORTO VELHO"],
     "Olha essa água de duas cores! Em qual cidade acontece o Encontro das Águas?",
     "Manaus! Os rios correm lado a lado por quilômetros sem se misturar!",
     {"sabia": "RIOS LADO A LADO POR KM SEM MISTURAR"}),
    ("pau-brasil", "QUAL É A ÁRVORE SÍMBOLO DO BRASIL?", "PAU-BRASIL", ["IPÊ-AMARELO", "JABUTICABEIRA"],
     "Agora uma árvore! Qual é a árvore símbolo nacional do Brasil?",
     "Pau-brasil! Foi ela que deu nome ao país!",
     {"dica": ("Dica: tem o nome do país!", "TEM O NOME DO PAÍS")}),
    ("machado", "QUEM ESCREVEU DOM CASMURRO?", "MACHADO DE ASSIS", ["JOSÉ DE ALENCAR", "MONTEIRO LOBATO"],
     "Agora uma de escola! Quem escreveu o livro Dom Casmurro?",
     "Machado de Assis! O da Capitu!", {}),
    ("guarana", "DE ONDE VEM O GUARANÁ?", "AMAZÔNIA", ["CAATINGA", "PAMPA"],
     "Essa fruta parece um olho! O guaraná é nativo de qual bioma?",
     "Amazônia! E o refrigerante veio dela!", {}),
    ("senna", "QUANTOS TÍTULOS ELE GANHOU?", "3", ["2", "4"],
     "Esse é o Ayrton Senna! Quantos títulos de Fórmula 1 ele ganhou?",
     "Três! Em oitenta e oito, noventa e noventa e um!", {}),
    ("isabel", "QUE LEI ELA ASSINOU EM 1888?", "LEI ÁUREA", ["VENTRE LIVRE", "SEXAGENÁRIOS"],
     "Essa é a Princesa Isabel! Qual lei ela assinou em 1888, acabando com a escravidão?",
     "Lei Áurea! Treze de maio de 1888!", {}),
    ("congresso", "QUEM PROJETOU ESSE PRÉDIO?", "OSCAR NIEMEYER", ["LÚCIO COSTA", "BURLE MARX"],
     "Essa aqui derruba muita gente! Quem foi o arquiteto desse prédio, o Congresso Nacional?",
     "Oscar Niemeyer! O Lúcio Costa fez o plano da cidade!", {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("republica", "QUANDO O BRASIL VIROU REPÚBLICA?", "1889", ["1822", "1888"],
     "Mais uma de história! Em que ano o Brasil virou República?",
     "1889! Quinze de novembro!", {}),
    ("sao-francisco", "RIO DA INTEGRAÇÃO NACIONAL?", "SÃO FRANCISCO", ["TIETÊ", "PARANÁ"],
     "Agora um rio! Qual é o maior rio que nasce e corre só dentro do Brasil?",
     "São Francisco! O Velho Chico, rio da integração nacional!", {}),
    ("mandacaru", "QUAL É O NOME DESSE CACTO?", "MANDACARU", ["CARNAÚBA", "BABAÇU"],
     "Bora pro sertão! Qual é o nome desse cacto?",
     "Mandacaru! Quando ele floresce, dizem que vem chuva!", {}),
    ("noronha", "NORONHA É DE QUAL ESTADO?", "PERNAMBUCO", ["RIO GRANDE DO NORTE", "BAHIA"],
     "Cuidado! Fernando de Noronha pertence a qual estado?",
     "Pernambuco! Mesmo ficando mais perto do Rio Grande do Norte!",
     {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("neblina", "PONTO MAIS ALTO DO BRASIL?", "PICO DA NEBLINA", ["PICO DA BANDEIRA", "MONTE RORAIMA"],
     "Lá em cima! Qual é o ponto mais alto do Brasil?",
     "Pico da Neblina! Quase três mil metros, no Amazonas!",
     {"dica": ("Dica: fica na Amazônia!", "FICA NA AMAZÔNIA")}),
    ("profetas", "QUEM ESCULPIU OS PROFETAS?", "ALEIJADINHO", ["MESTRE VALENTIM", "BRECHERET"],
     "Essa é pra quem manja de arte! Quem esculpiu os Profetas de Congonhas?",
     "Aleijadinho! Ele esculpia mesmo doente!", {}),
    ("roraima", "ESTADO COM MENOS GENTE?", "RORAIMA", ["AMAPÁ", "ACRE"],
     "Qual é o estado brasileiro com menos habitantes?",
     "Roraima! Se você acertou essa, você é brasileiro de verdade!",
     {"final": True, "suspense": True}),
]


def main():
    FOTOS = json.load(open(os.path.join(HERE, "fotos.json"), encoding="utf-8"))   # slug -> foto (as que vieram)
    itens = [p for p in P if p[0] in FOTOS]
    rnd = random.Random(50)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    pos[0], pos[1], pos[2] = 1, 2, 0
    R = []
    for n, (slug, perg, certa, err, fq, fr, ex) in enumerate(itens, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        falas = [o.lower().replace("mt e ms", "Mato Grosso e Mato Grosso do Sul").replace("go e to", "Goiás e Tocantins")
                 .replace("pa e am", "Pará e Amazonas") for o in ops]
        r = {"n": n, "pergunta": perg, "foto": FOTOS[slug], "opcoes": ops, "certa": pos[n - 1],
             "fala_q": f"{fq} {falas[0]}, {falas[1]} ou {falas[2]}?", "fala_r": fr, "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if not ex.get("final") else "Valendo o título de brasileiro raiz... a resposta é..."
        R.append(r)
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
