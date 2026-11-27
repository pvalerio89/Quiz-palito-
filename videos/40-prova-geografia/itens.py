"""Gera itens.json do vídeo 40 "Prova de geografia do 3º ano" (estilo mais humano, 2026-11-13).

44 perguntas próprias tiradas do simulado e da folha de reforço de Geografia do 3º ano (capítulos 8 e 9: as paisagens
e o ambiente) que o Patrick mandou em PDF (2026-11-18): paisagem, elementos naturais e culturais, paisagem natural e
cultural, quem transforma a paisagem, mudança rápida ou lenta, superfície terrestre, desigualdade social, maquete e
legenda, ambiente, tipos de poluição, tudo está ligado, desperdício de água, ajuda ou prejudica, governo ou cidadão.
Sem nome do aluno/escola. 4 níveis (fácil → muito difícil). Vídeo de 15 min pra cima (Patrick, 2026-11-18).
A imagem de cada pergunta é um cartão de caderno com a palavra/frase (desenhado pelo build, em cartoes/).
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
NC = "NATURAL OU CULTURAL?"
NC_OPS = ["Cultural", "Nenhum dos dois"]
CN_OPS = ["Natural", "Nenhum dos dois"]
POL = "QUE POLUIÇÃO É ESSA?"
QUEM = "QUEM MUDOU A PAISAGEM?"
QUEM_N = ["Ser humano", "Ninguém"]
QUEM_H = ["Natureza", "Ninguém"]
RL = "RÁPIDA OU LENTA?"
AP = "AJUDA OU PREJUDICA?"
GT = "GOVERNO OU TODOS NÓS?"
PNC = "PAISAGEM NATURAL OU CULTURAL?"
VF = "VERDADEIRO OU FALSO?"
ECO = "QUANTO ECONOMIZA?"
SABIA_POL = "Poluição sonora é o barulho que atrapalha. Poluição visual é o excesso de cartazes e letreiros que cansa a vista."
SABIA_AMB = "Ambiente é tudo junto: seres vivos, ar, água, solo, luz do Sol, o que o ser humano constrói e as relações entre eles."
# nível, pergunta (topo), cartão (linhas), certa, [erradas], fala da pergunta, fala da resposta, extras
P = [
    # ---------- FÁCIL ----------
    (1, NC, ["RIO"], "Natural", NC_OPS,
     "Primeira questão da prova: rio é elemento natural ou cultural?",
     "Natural! O rio já estava lá, ninguém construiu.", {"falar_ops": False, "count": 5.0}),
    (1, NC, ["PRÉDIO"], "Cultural", CN_OPS,
     "E prédio? Natural ou cultural?",
     "Cultural! Quem construiu foi o ser humano.", {"falar_ops": False, "count": 6.0}),
    (1, POL, ["Uma fábrica solta", "fumaça o dia", "inteiro."], "Do ar", ["Da água", "Sonora"],
     "Uma fábrica solta fumaça o dia inteiro. Que poluição é essa?",
     "Poluição do ar! A fumaça suja o ar que a gente respira.", {}),
    (1, "O QUE É PAISAGEM?", ["Paisagem", "é..."], "Tudo que se vê", ["Só lugar bonito", "Só cidade grande"],
     "O que é paisagem? Tudo que se vê, só lugar bonito ou só cidade grande?",
     "Tudo o que vemos e percebemos num local, em determinado momento!",
     {"falar_ops": False, "sabia": "As palavras-chave são local e momento: a paisagem é sempre de um lugar e de um instante."}),
    (1, QUEM, ["Construíram uma", "ponte sobre", "o rio."], "Ser humano", QUEM_H,
     "Construíram uma ponte sobre o rio. Quem mudou a paisagem?",
     "O ser humano! Ponte é construção.", {}),
    (1, QUEM, ["Um terremoto", "rachou a estrada", "ao meio."], "Natureza", QUEM_N,
     "Um terremoto rachou a estrada ao meio. Quem mudou a paisagem?",
     "A natureza! Ninguém manda no terremoto.", {}),
    (1, POL, ["Esgoto sem", "tratamento jogado", "no rio."], "Da água", ["Do ar", "Visual"],
     "Esgoto sem tratamento é jogado no rio. Que poluição é essa?",
     "Poluição da água! O rio fica sujo.", {}),
    (1, AP, ["Jogar lixo", "no rio"], "Prejudica", ["Ajuda", "Tanto faz"],
     "Jogar lixo no rio ajuda ou prejudica o ambiente?",
     "Prejudica! Suja a água e faz mal aos peixes.", {"falar_ops": False}),
    (1, AP, ["Fechar a torneira", "ao escovar", "os dentes"], "Ajuda", ["Prejudica", "Tanto faz"],
     "Fechar a torneira ao escovar os dentes ajuda ou prejudica o ambiente?",
     "Ajuda! Economiza muita água.", {"falar_ops": False}),
    (1, NC, ["LUZ SOLAR"], "Natural", NC_OPS,
     "Luz solar é elemento natural ou cultural?",
     "Natural! O Sol ninguém fabricou.", {"falar_ops": False}),
    (1, RL, ["Começou", "a chover."], "Rápida", ["Lenta", "Não muda nada"],
     "Começou a chover. Essa mudança na paisagem é rápida ou lenta?",
     "Rápida! Acontece no mesmo dia, em minutos.", {"falar_ops": False,
     "dica": ("Dica: isso muda no mesmo dia ou leva anos?", "MESMO DIA?")}),
    # ---------- MÉDIO ----------
    (2, NC, ["PLANTAÇÃO"], "Cultural", CN_OPS,
     "Nível médio, valendo! Plantação é elemento natural ou cultural?",
     "Cultural! Tem planta, mas quem plantou foi o ser humano.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!", "suspense": True}),
    (2, POL, ["Som do vizinho", "alto a noite", "toda."], "Sonora", ["Do ar", "Visual"],
     "O som do vizinho fica muito alto a noite toda. Que poluição é essa?",
     "Poluição sonora! Barulho demais também é poluição.", {}),
    (2, POL, ["Rua coberta de", "cartazes, letreiros", "e faixas."], "Visual", ["Do solo", "Sonora"],
     "A rua está coberta de cartazes, letreiros e faixas. Que poluição é essa?",
     "Poluição visual! Cansa a vista.", {"sabia": SABIA_POL}),
    (2, QUEM, ["A floresta foi", "derrubada para", "virar pasto."], "Ser humano", QUEM_H,
     "A floresta foi derrubada para virar pasto. Quem mudou a paisagem?",
     "O ser humano! Foi gente que derrubou a mata.", {}),
    (2, QUEM, ["No inverno, a cidade", "amanheceu coberta", "de neve."], "Natureza", QUEM_N,
     "No inverno, a cidade amanheceu coberta de neve. Quem mudou a paisagem?",
     "A natureza! A neve cai sozinha.", {}),
    (2, RL, ["A cidade cresceu", "e ganhou", "prédios altos."], "Lenta", ["Rápida", "Não muda nada"],
     "A cidade cresceu e ganhou prédios altos. Mudança rápida ou lenta?",
     "Lenta! Prédio e bairro novo levam anos.", {"falar_ops": False}),
    (2, PNC, ["Centro da cidade:", "prédios, carros", "e lojas"], "Cultural", ["Natural", "Nenhuma"],
     "O centro de uma cidade, cheio de prédios, carros e lojas. É paisagem natural ou cultural?",
     "Cultural! Quase tudo ali foi feito pelo ser humano.", {"falar_ops": False}),
    (2, PNC, ["Cachoeira no meio", "da mata, sem", "construções"], "Natural", ["Cultural", "Nenhuma"],
     "Uma cachoeira no meio da mata, sem nenhuma construção por perto. Paisagem natural ou cultural?",
     "Natural! Só tem elementos da natureza.", {"falar_ops": False}),
    (2, GT, ["Multar empresas", "que poluem o ar", "ou a água"], "Governo", ["Todos nós", "Ninguém"],
     "Multar empresas que poluem o ar ou a água. Isso é ação do governo ou de todos nós?",
     "Do governo! Só o governo pode multar.", {"falar_ops": False}),
    (2, GT, ["Comprar só", "o necessário"], "Todos nós", ["Governo", "Ninguém"],
     "E comprar só o necessário? Governo ou todos nós?",
     "Todos nós! Cada um pode fazer isso em casa.", {"falar_ops": False}),
    (2, ECO, ["Banho com", "desperdício: 45 L", "sem: 15 L"], "30 litros", ["60 litros", "20 litros"],
     "Tomar banho com desperdício gasta quarenta e cinco litros. Sem desperdício, quinze. Quanto economiza?",
     "Trinta litros! Quarenta e cinco menos quinze.",
     {"dica": ("Dica: é conta de menos!", "CONTA DE MENOS!"), "count": 10.0}),
    # ---------- DIFÍCIL ----------
    (3, NC, ["ÁRVORE NATIVA"], "Natural", NC_OPS,
     "Agora complica! Árvore nativa é natural ou cultural?",
     "Natural! A árvore nativa nasceu sozinha, ninguém plantou.", {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (3, POL, ["Produtos químicos", "contaminam a terra", "da plantação."], "Do solo", ["Da água", "Do ar"],
     "Produtos químicos contaminam a terra da plantação. Que poluição é essa?",
     "Poluição do solo! A terra fica contaminada.", {}),
    (3, QUEM, ["Faltou chuva", "e o rio secou."], "Natureza", QUEM_N,
     "Faltou chuva e o rio secou. Quem mudou a paisagem?",
     "A natureza! A seca é da natureza, mesmo que o ser humano possa piorar.",
     {"aviso": "DERRUBA MUITA GENTE!", "suspense": True}),
    (3, "ONDE ESTÃO AS PAISAGENS?", ["Todas as paisagens", "se encontram", "na..."], "Superfície",
     ["Embaixo da terra", "Lua"],
     "Complete: todas as paisagens se encontram na o quê?",
     "Na superfície terrestre! É onde o ser humano vive e faz suas atividades.", {}),
    (3, VF, ["O ambiente é", "formado só pelos", "seres vivos."], "Falso", ["Verdadeiro", "Depende"],
     "Verdadeiro ou falso: o ambiente é formado só pelos seres vivos.",
     "Falso! O ambiente tem muito mais coisa.", {"falar_ops": False, "sabia": SABIA_AMB}),
    (3, VF, ["A água de beber", "é inesgotável e", "nunca vai acabar."], "Falso", ["Verdadeiro", "Depende"],
     "Verdadeiro ou falso: a água boa para beber é inesgotável e nunca vai acabar.",
     "Falso! Ela pode acabar. A maior parte da água do planeta é salgada.", {"falar_ops": False}),
    (3, "COMO SE CHAMA ISSO?", ["Pessoas do mesmo", "lugar vivendo em", "condições diferentes"],
     "Desigualdade", ["Paisagem natural", "Poluição visual"],
     "Quando as pessoas de um mesmo lugar vivem em condições muito diferentes, como se chama isso?",
     "Desigualdade social! Dá até para perceber olhando a paisagem.", {}),
    (3, ECO, ["Lavar o carro com", "desperdício: 216 L", "sem: 40 L"], "176 litros", ["186 litros", "256 litros"],
     "Lavar o carro com desperdício gasta duzentos e dezesseis litros. Sem desperdício, quarenta. Quanto economiza?",
     "Cento e setenta e seis litros! Usa balde, não mangueira.", {"count": 10.0}),
    (3, AP, ["Trocar brinquedos", "em vez de", "comprar novos"], "Ajuda", ["Prejudica", "Tanto faz"],
     "Trocar brinquedos em vez de comprar novos ajuda ou prejudica o ambiente?",
     "Ajuda! Reaproveitar gera menos lixo.", {"falar_ops": False}),
    (3, AP, ["Lavar a calçada", "com mangueira"], "Prejudica", ["Ajuda", "Tanto faz"],
     "Lavar a calçada com mangueira ajuda ou prejudica o ambiente?",
     "Prejudica! Desperdiça muita água. Melhor vassoura e balde.", {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (3, "COMO OLHAR A MAQUETE?", ["Pra desenhar a", "maquete no papel,", "olhe de..."], "Cima para baixo",
     ["Lado", "Baixo para cima"],
     "Para desenhar a representação plana de uma maquete, a gente olha de onde?",
     "De cima para baixo! Como um pássaro voando sobre o bairro.", {}),
    # ---------- MUITO DIFÍCIL ----------
    (4, "COMO SE CHAMA?", ["Quadrinho que", "explica cada", "símbolo do desenho"], "Legenda", ["Título", "Escala"],
     "Agora a parte que reprova! Como se chama o quadrinho que explica o que cada símbolo do desenho representa?",
     "Legenda! É ela que diz, por exemplo, que o quadradinho verde é uma praça.", {"aviso": "DERRUBA MUITA GENTE!"}),
    (4, "O QUE MAIS TEM HOJE?", ["No planeta, hoje,", "a maioria das", "paisagens é..."], "Cultural",
     ["Natural", "Metade de cada"],
     "No planeta, hoje, a maioria das paisagens é natural, cultural ou metade de cada?",
     "Cultural! O ser humano já mudou quase todos os lugares. Paisagem natural virou coisa rara.",
     {"falar_ops": False, "aviso": "QUASE TODO MUNDO ERRA!", "suspense": True}),
    (4, GT, ["Implantar a", "coleta seletiva", "na cidade"], "Governo", ["Todos nós", "Ninguém"],
     "Implantar a coleta seletiva na cidade. Governo ou todos nós?",
     "Governo! Separar o lixo é com a gente, mas implantar a coleta na cidade só o governo consegue.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (4, ECO, ["Lavar a louça com", "desperdício: 117 L", "sem: 20 L"], "97 litros", ["107 litros", "87 litros"],
     "Lavar a louça com desperdício gasta cento e dezessete litros. Sem desperdício, vinte. Quanto economiza?",
     "Noventa e sete litros! Cento e dezessete menos vinte.", {"count": 10.0, "suspense": True}),
    (4, "E OS PEIXES?", ["Uma fábrica jogou", "esgoto sem", "tratamento no rio."], "Podem morrer",
     ["Ficam maiores", "Nada muda"],
     "Uma fábrica jogou esgoto sem tratamento no rio. O que acontece com os peixes?",
     "Podem morrer, ou ter que procurar outro lugar para viver!",
     {"sabia": "Na natureza tudo depende de tudo, como as peças de um quebra-cabeça: mexeu numa peça, as outras sentem."}),
    (4, "E AS AVES?", ["A vegetação da", "floresta foi", "destruída."], "Perdem a casa",
     ["Ficam felizes", "Nada muda"],
     "A vegetação de uma floresta foi destruída. O que pode acontecer com as aves?",
     "Perdem a casa e a comida! Podem ir embora ou até desaparecer.", {}),
    (4, "QUAL NÃO É CULTURAL?", ["Ponte, asfalto", "ou cachoeira?"], "Cachoeira", ["Ponte", "Asfalto"],
     "Ponte, asfalto ou cachoeira: qual desses não é elemento cultural?",
     "Cachoeira! Ela é natural. Ponte e asfalto o ser humano fez.", {"falar_ops": False}),
    (4, "O QUE NÃO PODE FALTAR?", ["Seres vivos, ar,", "água, solo e as", "___ entre eles"], "Relações",
     ["Estrelas", "Placas"],
     "O ambiente é formado pelos seres vivos, o ar, a água, o solo e as o quê entre eles?",
     "Relações! O ambiente não é só a lista de coisas, é como tudo se liga.", {"aviso": "DERRUBA MUITA GENTE!"}),
    (4, RL, ["A mata virou", "plantação."], "Lenta", ["Rápida", "Não muda nada"],
     "A mata virou plantação. Mudança rápida ou lenta?",
     "Lenta! Derrubar, preparar a terra e plantar leva meses.", {"falar_ops": False}),
    (4, VF, ["Mexer numa parte", "do ambiente afeta", "as outras partes."], "Verdadeiro", ["Falso", "Depende"],
     "Verdadeiro ou falso: mexer numa parte do ambiente afeta as outras partes.",
     "Verdadeiro! Tudo está ligado.", {"falar_ops": False}),
    (4, "QUANTO ECONOMIZA NO TOTAL?", ["Dentes: 12 L → 1 L", "Banho: 45 L → 15 L", "Total?"], "41 litros",
     ["31 litros", "57 litros"],
     "Valendo a nota da prova! Escovar os dentes: de doze para um litro. Banho: de quarenta e cinco para quinze. "
     "Quanto economiza juntando os dois?",
     "Quarenta e um litros! Onze dos dentes mais trinta do banho. Se acertou essa, tirou dez na prova!",
     {"count": 12.0, "suspense": True, "final": True}),
]


def main():
    rnd = random.Random(40)
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
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo a nota... a resposta é..."
        R.append(r)
    assert len(R) == 44 and len({tuple(r["cartao"]) for r in R}) == 44
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], [sum(r["nivel"] == k for r in R) for k in (1, 2, 3, 4)])


if __name__ == "__main__":
    main()
