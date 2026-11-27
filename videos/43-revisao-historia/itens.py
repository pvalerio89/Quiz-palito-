"""Gera itens.json do vídeo 43 "Revisão da prova de História do 3º ano" (estilo mais humano, 2026-11-13).

45 perguntas próprias tiradas da Avaliação de Processo de História do 3º ano (3º trimestre) que o Patrick mandou em
foto (2026-11-19): nascimento e formação das cidades, nômades, litoral, fortes, povoado/vila/cidade, Salvador
(Cidade Alta e Baixa), capitais do Brasil, espaços públicos e deveres do cidadão. Sem nome do aluno/escola e sem
foto da prova. Do MÉDIO ao MUITO DIFÍCIL (Patrick: "do médio ao difícil", sem nível fácil). 15 min pra cima.
A imagem de cada pergunta é foto real do Wikimedia (fotos/, legenda por cima) ou cartão de caderno (cartoes/).
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
PVC = "POVOADO, VILA OU CIDADE?"
PVC_OPS = ["Povoado", "Vila", "Cidade"]
CAB = "CIDADE ALTA OU BAIXA?"
CAB_A = ["Cidade Baixa", "As duas"]
CAB_B = ["Cidade Alta", "As duas"]
JFC = "JÁ FOI CAPITAL DO BRASIL?"
EPP = "PÚBLICO OU PRIVADO?"
VF = "VERDADEIRO OU FALSO?"
COMP = "COMPLETE A FRASE!"
F = {"falar_ops": False}


def pvc(cartao, certa, fq, fr, **ex):
    return (cartao, certa, [o for o in PVC_OPS if o != certa], fq, fr, {"falar_ops": False, **ex})


# nível, pergunta (topo), cartão/legenda (linhas), certa, [erradas], fala da pergunta, fala da resposta, extras
# extras: img = foto real (fotos/<img>.jpg) no lugar do cartão, com as linhas do cartão como legenda
P = [
    # ---------- MÉDIO ----------
    (2, "COMO VIVIAM?", ["Antes das cidades,", "os humanos eram..."], "Nômades", ["Reis", "Marinheiros"],
     "Primeira questão da revisão! Antes das primeiras cidades, como viviam os seres humanos?",
     "Nômades! Mudavam de lugar o tempo todo, atrás de comida e água.", {"img": "nomades"}),
    (2, "O QUE FEZ NASCER AS CIDADES?", ["Há mais de", "10 mil anos..."], "Se fixar num lugar",
     ["Inventar o carro", "Fazer shoppings"],
     "Há mais de dez mil anos, o que permitiu que surgissem as primeiras cidades?",
     "Os grupos se fixaram num lugar! Ou seja, deixaram de ser nômades.", {}),
    (2, "POR QUE PARARAM DE ANDAR?", ["Plantar e criar", "animais"], "Agricultura", ["Televisão", "Eletricidade"],
     "O que ajudou os grupos a ficarem num lugar só, sem precisar sair atrás de comida?",
     "A agricultura! Plantando e criando animais, a comida estava ali pertinho.", {"img": "agricultura"}),
    (2, VF, ["Todas as cidades", "surgiram no", "mesmo período."], "Falso", ["Verdadeiro", "Depende"],
     "Verdadeiro ou falso: todas as cidades surgiram no mesmo período.",
     "Falso! Cada cidade surgiu num tempo diferente, e muitas começaram pequenininhas.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (2, "POR QUE NO LITORAL?", ["As primeiras vilas", "do Brasil ficavam", "no litoral"], "Navios e portos",
     ["Não tinha indígena", "Não sabiam fazer casa"],
     "As primeiras vilas do Brasil foram fundadas no litoral. Por quê?",
     "Para facilitar o transporte por navios nos portos! Tudo chegava e saía pelo mar.", {"img": "caravela"}),
    (2, "O QUE É ISSO?", ["Construção com", "canhões na", "beira do mar"], "Forte", ["Igreja", "Mercado"],
     "Olha essa construção na beira do mar, cheia de canhões. O que é?",
     "Um forte! Era comum no litoral do Brasil na época colonial.", {"img": "copacabana"}),
    (2, "PRA QUE SERVIA O FORTE?", ["Forte dos", "Reis Magos, Natal"], "Defender a cidade",
     ["Guardar comida", "Receber turistas"],
     "E pra que serviam os fortes, lá na época colonial?",
     "Para defender a vila e a cidade dos ataques que vinham pelo mar!", {"img": "reis-magos"}),
    (2, PVC, *pvc(["Pequeno grupo", "inicial de", "habitantes"], "Povoado",
                  "Pequeno grupo inicial de habitantes. Povoado, vila ou cidade?",
                  "Povoado! É o começo de tudo.")),
    (2, PVC, *pvc(["Tem Prefeitura e", "Câmara Municipal"], "Cidade",
                  "Tem população maior, Prefeitura e Câmara Municipal. Povoado, vila ou cidade?",
                  "Cidade! Prefeitura e Câmara só a cidade tem.")),
    (2, "QUE CIDADE É ESSA?", ["Foi a primeira", "capital do Brasil"], "Salvador", ["Recife", "São Paulo"],
     "Essa cidade foi a primeira capital do Brasil. Qual é?",
     "Salvador, na Bahia! Esse é o Elevador Lacerda.", {"img": "elevador"}),
    (2, "E A CAPITAL DE HOJE?", ["Capital atual", "do Brasil"], "Brasília", ["Rio de Janeiro", "São Paulo"],
     "E a capital do Brasil hoje, qual é?",
     "Brasília! Esse é o Congresso Nacional.", {"img": "congresso"}),
    (2, EPP, ["Parque"], "Público", ["Privado", "Nenhum dos dois"],
     "Parque é espaço público ou privado?",
     "Público! Parque, praça e rua de pedestres pertencem a todos os cidadãos.",
     {"falar_ops": False, "img": "ibirapuera"}),
    (2, "ATITUDE DE BOM CIDADÃO?", ["Jogar papel de bala", "no chão da praça"], "Não", ["Sim", "Só se ninguém vê"],
     "Jogar papel de bala no chão da praça é atitude de bom cidadão?",
     "Não! Lixo vai na lixeira. A praça é de todo mundo.", {"falar_ops": False, "img": "lixo"}),
    (2, "EM QUE ANO?", ["Salvador foi", "fundada em..."], "1549", ["1500", "1822"],
     "Em que ano a cidade de Salvador foi fundada?",
     "Mil quinhentos e quarenta e nove! Por ordem do rei de Portugal.", {"img": "salvador", "count": 9.0}),
    (2, "QUEM MANDOU FUNDAR?", ["Quem mandou", "fundar Salvador?"], "O rei de Portugal", ["O papa", "Os indígenas"],
     "Salvador foi fundada por ordem de quem?",
     "Do rei de Portugal!",
     {"sabia": "O rei era Dom João Terceiro. Quem veio fundar a cidade foi Tomé de Sousa, o primeiro governador-geral."}),
    # ---------- DIFÍCIL ----------
    (3, CAB, ["Prédios", "públicos"], "Cidade Alta", CAB_A,
     "Subindo o nível! Em Salvador, os prédios públicos ficavam na Cidade Alta ou na Cidade Baixa?",
     "Cidade Alta! Lá ficava o governo.", {"falar_ops": False, "img": "pelourinho"}),
    (3, CAB, ["Porto e", "armazéns"], "Cidade Baixa", CAB_B,
     "E o porto e os armazéns? Cidade Alta ou Cidade Baixa?",
     "Cidade Baixa! Pertinho do mar, onde chegavam os navios.", {"falar_ops": False}),
    (3, CAB, ["Moradias perto", "da praia"], "Cidade Baixa", CAB_B,
     "E as moradias perto da praia? Cidade Alta ou Cidade Baixa?",
     "Cidade Baixa! Porto, armazéns e moradias perto da praia.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!", "suspense": True}),
    (3, "O QUE LIGA AS DUAS?", ["Liga a Cidade Alta", "à Cidade Baixa"], "Elevador Lacerda",
     ["Ponte Rio-Niterói", "Cristo Redentor"],
     "Em Salvador, o que liga a Cidade Alta à Cidade Baixa até hoje?",
     "O Elevador Lacerda! Sobe e desce o tempo todo.", {"img": "elevador2"}),
    (3, COMP, ["Salvador foi a", "primeira ______", "do Brasil."], "Capital", ["Moradia", "Porto"],
     "Complete: Salvador foi a primeira o quê do Brasil?",
     "Capital! A primeira capital do Brasil.", {}),
    (3, COMP, ["Na Cidade Alta", "ficavam os", "______ públicos."], "Prédios", ["Portos", "Armazéns"],
     "Complete: na Cidade Alta ficavam os o quê públicos?",
     "Prédios públicos!", {}),
    (3, JFC, ["São Paulo"], "Nunca foi", ["Já foi", "É a de hoje"],
     "São Paulo já foi capital do Brasil?",
     "Nunca foi! É a maior cidade do Brasil, mas nunca foi capital.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!", "img": "sao-paulo"}),
    (3, JFC, ["Rio de Janeiro"], "Já foi", ["Nunca foi", "É a de hoje"],
     "E o Rio de Janeiro, já foi capital do Brasil?",
     "Já foi! O Rio foi capital por quase duzentos anos.", {"falar_ops": False, "img": "rio"}),
    (3, JFC, ["Curitiba"], "Nunca foi", ["Já foi", "É a de hoje"],
     "E Curitiba, já foi capital do Brasil?",
     "Nunca foi! Curitiba é capital do Paraná, mas não do Brasil.", {"falar_ops": False, "img": "curitiba"}),
    (3, "QUAL A ORDEM?", ["1ª, 2ª e 3ª", "capital do Brasil"], "Salvador, Rio, Brasília",
     ["Rio, Salvador, Brasília", "Brasília, Rio, Salvador"],
     "Qual é a ordem das capitais do Brasil, da primeira até a de hoje?",
     "Salvador, depois Rio de Janeiro, e agora Brasília!", {"count": 10.0}),
    (3, PVC, *pvc(["Maior que o povoado,", "com comércio", "e pelourinho"], "Vila",
                  "Maior que o povoado, com comércio e, na época colonial, com pelourinho. Povoado, vila ou cidade?",
                  "Vila! Na época colonial, toda vila tinha que ter pelourinho.", aviso="TEM PEGADINHA!")),
    (3, "O QUE ERA O PELOURINHO?", ["Coluna de pedra", "na praça da vila"], "Lugar de castigo",
     ["Poço de água", "Relógio"],
     "Na época colonial, o que era o pelourinho?",
     "Uma coluna na praça onde pessoas, principalmente as escravizadas, eram castigadas em público.",
     {"img": "pelourinho-coluna",
      "sabia": "Era também o símbolo de que o lugar era uma vila. Em Salvador, um bairro inteiro ganhou o nome de Pelourinho."}),
    (3, EPP, ["Shopping"], "Privado", ["Público", "Nenhum dos dois"],
     "Shopping é espaço público ou privado?",
     "Privado! Shopping tem dono. De todos mesmo são a praça, o parque e a rua de pedestres.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (3, COMP, ["Pessoas de diferentes", "idades, etnias e", "condições ______"], "Sociais",
     ["Climáticas", "Musicais"],
     "Complete: nas cidades se encontram pessoas de diferentes idades, etnias e condições o quê?",
     "Sociais! A cidade junta todo tipo de gente.", {}),
    (3, "QUAL É DEVER DO CIDADÃO?", ["Passeando com", "o cachorro na praça"], "Recolher o cocô",
     ["Deixar lá mesmo", "Soltar na rua"],
     "Passeando com o cachorro na praça, qual é o dever do bom cidadão?",
     "Recolher o cocô! Assim a praça fica limpa pra todo mundo.", {"img": "praca"}),
    # ---------- MUITO DIFÍCIL ----------
    (4, "ONDE NASCERAM AS PRIMEIRAS?", ["Entre dois rios:", "Tigre e Eufrates"], "Mesopotâmia",
     ["Amazônia", "Antártida"],
     "Agora é a parte que reprova! Algumas das primeiras cidades do mundo nasceram entre os rios Tigre e Eufrates. Que região é essa?",
     "Mesopotâmia! Quer dizer terra entre rios.", {"img": "ur", "aviso": "DERRUBA MUITA GENTE!"}),
    (4, "POR QUE PERTO DOS RIOS?", ["As primeiras cidades", "nasciam perto", "de rios"], "Água pra plantar",
     ["Pra nadar", "Pra ver baleia"],
     "Por que as primeiras cidades nasciam perto de rios?",
     "Água pra plantar e pra beber! Sem água não tem agricultura.", {"img": "nilo"}),
    (4, "UMA DAS MAIS ANTIGAS", ["Cidade com mais", "de 10 mil anos"], "Jericó", ["Brasília", "Curitiba"],
     "Qual destas é uma das cidades mais antigas do mundo, com mais de dez mil anos?",
     "Jericó! Fica no Oriente Médio, e tem gente morando lá há mais de dez mil anos.", {"img": "jerico"}),
    (4, "QUAL FOI A PRIMEIRA VILA?", ["Primeira vila", "do Brasil"], "São Vicente", ["Salvador", "Brasília"],
     "Qual foi a primeira vila do Brasil?",
     "São Vicente, no litoral de São Paulo, em mil quinhentos e trinta e dois!",
     {"img": "sao-vicente", "aviso": "QUASE TODO MUNDO ERRA!", "suspense": True}),
    (4, "QUEM FUNDOU SALVADOR?", ["Primeiro", "governador-geral"], "Tomé de Sousa",
     ["Pedro Álvares Cabral", "Dom Pedro I"],
     "Quem veio de Portugal para fundar Salvador?",
     "Tomé de Sousa, o primeiro governador-geral do Brasil!", {"img": "tome", "aviso": "TEM PEGADINHA!"}),
    (4, "QUANTO TEMPO?", ["Salvador foi capital", "por quanto tempo?"], "Mais de 200 anos", ["Só 10 anos", "Uns 50 anos"],
     "Salvador foi capital do Brasil por quanto tempo?",
     "Mais de duzentos anos! De mil quinhentos e quarenta e nove até mil setecentos e sessenta e três.", {}),
    (4, "EM QUE ANO?", ["Brasília virou", "capital em..."], "1960", ["1822", "1900"],
     "Em que ano Brasília virou a capital do Brasil?",
     "Mil novecentos e sessenta!",
     {"img": "planalto", "count": 9.0,
      "sabia": "Quem mandou construir Brasília foi o presidente Juscelino Kubitschek. A cidade ficou pronta em menos de quatro anos."}),
    (4, "POR QUE NO MEIO DO BRASIL?", ["Por que levar", "a capital pro", "centro do país?"], "Ocupar o interior",
     ["Fugir da praia", "Ficar perto da neve"],
     "Por que levaram a capital lá pro centro do Brasil?",
     "Para ocupar e desenvolver o interior do país! Antes, quase tudo ficava perto do mar.", {"img": "plano-piloto"}),
    (4, "PRA ONDE MIRAVAM?", ["Os canhões", "do forte", "miravam..."], "O mar", ["A floresta", "O céu"],
     "Os canhões dos fortes do litoral miravam pra onde?",
     "O mar! Os ataques de piratas e de outros povos europeus vinham de navio.", {"img": "farol-barra"}),
    (4, "ONDE FAZIAM OS FORTES?", ["Eram construídos", "em locais..."], "Estratégicos", ["Escondidos", "Qualquer um"],
     "Os fortes eram construídos em locais o quê?",
     "Estratégicos! Num lugar alto ou na entrada da baía, de onde dava pra ver o inimigo chegando.", {}),
    (4, "QUAL NÃO É DEVER?", ["Qual destes", "NÃO é dever", "do cidadão?"], "Pichar os muros",
     ["Cuidar das praças", "Respeitar as pessoas"],
     "Qual destes não é dever do bom cidadão?",
     "Pichar os muros! Isso suja a cidade de todos.", {"aviso": "TEM PEGADINHA!"}),
    (4, "QUEM FAZ AS LEIS?", ["Quem faz as leis", "da cidade?"], "Câmara Municipal", ["O porto", "O forte"],
     "Na cidade, quem faz as leis?",
     "A Câmara Municipal! É lá que trabalham os vereadores. E o prefeito cuida da cidade na Prefeitura.", {}),
    (4, "QUAL É A ORDEM?", ["Do menor", "para o maior"], "Povoado, vila, cidade",
     ["Cidade, vila, povoado", "Vila, povoado, cidade"],
     "Qual é a ordem do crescimento das ocupações humanas, do menor para o maior?",
     "Povoado, vila e cidade!", {"count": 10.0}),
    (4, "POR QUE LÁ NO ALTO?", ["Por que o governo", "ficava na", "Cidade Alta?"], "Mais fácil defender",
     ["Fugir do calor", "Ver o pôr do sol"],
     "Por que os prédios do governo de Salvador ficavam lá no alto?",
     "Mais fácil de defender! Lá de cima dava pra ver quem chegava pelo mar.",
     {"aviso": "DERRUBA MUITA GENTE!", "suspense": True}),
    (4, "QUANTAS JÁ FORAM?", ["São Paulo, Curitiba,", "Salvador, Brasília", "e Rio de Janeiro"], "2",
     ["3", "1"],
     "Valendo a nota da prova! Dessas cinco cidades: São Paulo, Curitiba, Salvador, Brasília e Rio de Janeiro. "
     "Quantas já foram capital do Brasil, mas não são mais?",
     "Duas! Salvador e Rio de Janeiro. Brasília é a de hoje, e São Paulo e Curitiba nunca foram. "
     "Se acertou essa, tirou dez na prova!",
     {"count": 12.0, "suspense": True, "final": True}),
]

def main():
    rnd = random.Random(43)
    pos = [0, 1, 2] * 15
    rnd.shuffle(pos)
    pos[0] = 0
    R = []
    for n, (nivel, perg, cartao, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        if ex.get("falar_ops", True):
            fq = f"{fq} {ops[0]}, {ops[1]} ou {ops[2]}?"
        r = {"n": n, "nivel": nivel, "pergunta": perg, "cartao": cartao, "foto": f"q{n}.png",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": fq, "fala_r": fr, "count": ex.get("count", 8.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final", "img"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo a nota... a resposta é..."
        R.append(r)
    assert len(R) == 45
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], [sum(r["nivel"] == k for r in R) for k in (2, 3, 4)])


if __name__ == "__main__":
    main()
