"""Gera itens.json do vídeo 42 "Prova de história do 3º ano: invasões europeias no Brasil" (estilo mais humano).

42 perguntas próprias tiradas da Unidade 5 do livro de História do 3º ano que o Patrick mandou em fotos (2026-11-19):
pau-brasil, franceses na Guanabara (1555, ilha de Villegagnon, França Antártica), Estácio de Sá e a fundação do Rio
(1565, Pão de Açúcar, expulsão em 1567 com alianças indígenas), franceses em São Luís (1612/1615), piratas e
Thomas Cavendish (Santos, 1591), fortes e fortalezas, holandeses (1624 Salvador, 1630 Pernambuco, 24 anos, açúcar,
Olinda incendiada), Maurício de Nassau (1637, Maurícia, Frans Post, Albert Eckhout, 1644, 1654) e a linha do tempo.
Patrick pediu (2026-11-19) "do médio ao difícil": sem nível fácil. 3 níveis (médio → muito difícil). ~15 min.
Sem nome de aluno/escola. A imagem de cada pergunta é uma foto real (Wikimedia, em fotos/) ou um cartão de caderno.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
ANO = "EM QUE ANO?"
QUEM = "QUEM É ELE?"
QUAL = "QUAL É A RESPOSTA?"
FD = "FORTE OU FORTALEZA?"
# nível, pergunta (topo), imagem ("foto:<slug>" ou linhas do cartão), certa, [erradas], fala da pergunta, fala da resposta, extras
P = [
    # ---------- MÉDIO ----------
    (1, "QUAL ERA A RIQUEZA?", "foto:paubrasil", "Pau-brasil", ["Ouro", "Café"],
     "Primeira questão: naquela época, qual era a principal riqueza do território do Brasil?",
     "Pau-brasil! Portugueses e franceses queriam vender a madeira dessa árvore.", {}),
    (1, "QUEM FUNDOU O RIO?", "foto:estacio", "Estácio de Sá", ["Pedro Álvares Cabral", "Maurício de Nassau"],
     "Esse militar português fundou a cidade do Rio de Janeiro. Quem é ele?",
     "Estácio de Sá! Ele fundou São Sebastião do Rio de Janeiro em 1565.", {}),
    (1, "PARA QUE SERVIAM?", "foto:santacruz", "Defender as cidades", ["Guardar comida", "Ser escola"],
     "Fortes e fortalezas cheios de canhões. Para que eles serviam?",
     "Para defender as vilas e cidades do litoral dos ataques!", {}),
    (1, "ONDE FICAVAM?", "foto:canhoes", "No litoral", ["No interior", "Nas montanhas"],
     "Onde ficava a maioria dos fortes e fortalezas do Brasil?",
     "No litoral! Era por ali, pelo mar, que os invasores chegavam.", {}),
    (1, QUEM, "foto:nassau", "Maurício de Nassau", ["Estácio de Sá", "Thomas Cavendish"],
     "Esse conde veio governar a colônia holandesa no Recife. Quem é ele?",
     "Maurício de Nassau! Ele chegou ao Recife em 1637.", {}),
    (1, "QUEM CHEGOU AQUI?", "foto:guanabara", "Franceses", ["Holandeses", "Ingleses"],
     "Em 1555, quem chegou à baía de Guanabara, no Rio de Janeiro, e se fixou numa ilha?",
     "Os franceses! Queriam criar uma colônia ali.", {}),
    (1, "QUEM FUNDOU SÃO LUÍS?", "foto:saoluis", "Franceses", ["Portugueses", "Holandeses"],
     "A cidade de São Luís, capital do Maranhão, foi fundada por quem?",
     "Pelos franceses! Depois os portugueses recuperaram a cidade.",
     {"aviso": "TEM PEGADINHA!", "suspense": True,
      "sabia": "Os sobrados de azulejo de São Luís são marca dos portugueses, mas quem fundou foram os franceses, em 1612."}),
    (1, "POR QUE ATACAVAM?", "foto:pirata", "Roubar riquezas", ["Fazer amizade", "Construir escolas"],
     "Navios piratas atacavam as vilas do litoral. Para quê?",
     "Para roubar riquezas: ouro, madeira e alimentos!", {}),
    (1, "O QUE PERNAMBUCO TINHA?", "foto:cana", "Açúcar", ["Café", "Chocolate"],
     "A capitania de Pernambuco tinha a maior produção do mundo de quê?",
     "Açúcar! Por isso os holandeses quiseram invadir.",
     {"dica": ("Dica: vem da cana!", "VEM DA CANA!")}),
    (1, "QUANTAS VEZES?", ["HOLANDESES", "INVADIRAM", "O BRASIL..."], "Duas", ["Uma", "Cinco"],
     "Quantas vezes os holandeses invadiram o Brasil? Uma, duas ou cinco?",
     "Duas! Em 1624 e em 1630.", {"falar_ops": False}),
    (1, "QUE CIDADE PEGOU FOGO?", "foto:olinda", "Olinda", ["Salvador", "São Luís"],
     "Na conquista, os holandeses incendiaram uma cidade bem pertinho do Recife. Qual?",
     "Olinda! E com isso o Recife cresceu e virou a capital de Pernambuco.", {}),
    (1, "QUAL FOI A PRIMEIRA?", "foto:rio", "Salvador", ["São Paulo", "Recife"],
     "O Rio de Janeiro foi a segunda cidade fundada no Brasil. Qual foi a primeira?",
     "Salvador! A primeira capital do país.", {}),
    (1, "QUEM NÃO ACEITAVA?", ["Holandeses e", "ingleses não", "aceitavam a posse..."], "Dos portugueses",
     ["Dos espanhóis", "Dos indígenas"],
     "Holandeses e ingleses não aceitavam a posse do território do Brasil por quem?",
     "Pelos portugueses! Eles também queriam as riquezas da América.", {}),
    (1, "QUEM ERA ELE?", "foto:cavendish", "Pirata inglês", ["Rei francês", "Padre jesuíta"],
     "Esse é Thomas Cavendish. Ele era o quê?",
     "Um pirata inglês! Ele atacou a vila de Santos.", {}),
    # ---------- DIFÍCIL ----------
    (2, ANO, ["FRANCESES NA", "BAÍA DE", "GUANABARA"], "1555", ["1500", "1654"],
     "Nível difícil, valendo! Em que ano os franceses chegaram à baía de Guanabara?",
     "Mil quinhentos e cinquenta e cinco!", {}),
    (2, "QUE ILHA É ESSA?", "foto:villegagnon", "Villegagnon", ["Itamaracá", "Fernando de Noronha"],
     "No Rio de Janeiro, os franceses se fixaram numa ilha. Como ela ficou conhecida?",
     "Ilha de Villegagnon! Lá eles fizeram um povoado e um forte.", {}),
    (2, "QUE NOME TERIA?", ["A colônia", "francesa no Rio", "se chamaria..."], "França Antártica",
     ["Nova Holanda", "Vila Rica"],
     "A colônia que os franceses queriam criar no Rio de Janeiro teria que nome?",
     "França Antártica!", {"aviso": "DERRUBA MUITA GENTE!"}),
    (2, "QUAL FOI A ESTRATÉGIA?", "foto:tupinamba", "Aliança com indígenas", ["Pagar piratas", "Fugir pro mar"],
     "Que estratégia os portugueses usaram para expulsar os franceses do Rio de Janeiro?",
     "Negociar e fazer alianças com os povos indígenas! Os Tupinambá e os Tupiniquim apoiavam os franceses.", {}),
    (2, "ENTRE QUAIS MORROS?", "foto:paoacucar", "Pão de Açúcar", ["Corcovado", "Morro do Chapéu"],
     "O Rio foi fundado entre o morro Cara de Cão e qual outro morro famoso?",
     "Pão de Açúcar! Em primeiro de março de 1565.", {}),
    (2, ANO, ["FRANCESES", "EXPULSOS", "DO RIO"], "1567", ["1555", "1630"],
     "Em que ano os portugueses expulsaram de vez os franceses do Rio de Janeiro?",
     "Mil quinhentos e sessenta e sete! Pouco mais de dez anos depois que eles chegaram.", {"suspense": True}),
    (2, "COMO ERA CONHECIDO?", ["Thomas", "Cavendish", "era o..."], "Ladrão dos mares", ["Rei do açúcar", "Herói da vila"],
     "Thomas Cavendish era conhecido como o quê?",
     "O franco ladrão dos mares!", {}),
    (2, ANO, ["Cavendish ataca", "Santos na", "missa de Natal"], "1591", ["1500", "1654"],
     "Cavendish chegou à vila de Santos e prendeu todo mundo na missa de Natal. Em que ano?",
     "Mil quinhentos e noventa e um! Ele saqueou a vila por dois meses.", {}),
    (2, "QUANTO TEMPO?", "foto:dutchbrazil", "24 anos", ["5 anos", "100 anos"],
     "Os holandeses dominaram quase todo o Nordeste durante quanto tempo?",
     "Vinte e quatro anos!", {}),
    (2, ANO, "foto:nassau2", "1637", ["1500", "1567"],
     "Em que ano Maurício de Nassau chegou ao Recife?",
     "Mil seiscentos e trinta e sete! Com uma comitiva de homens ilustres.", {}),
    (2, "QUE CIDADE ELE FUNDOU?", "foto:mauricia", "Maurícia", ["Olinda", "Holandinha"],
     "A comitiva de Nassau fundou até uma cidade nova. Como ela se chamava?",
     "Maurícia! O nome vem do próprio Maurício de Nassau.", {"aviso": "TEM PEGADINHA!"}),
    (2, "QUEM PINTOU?", "foto:eckhout", "Albert Eckhout", ["Estácio de Sá", "Thomas Cavendish"],
     "Esse quadro foi pintado por um artista holandês da comitiva de Nassau. Quem?",
     "Albert Eckhout! Ele pintou pessoas, frutas e plantas do Brasil.", {}),
    (2, FD, ["Mais simples", "e com menos", "poder de fogo"], "Forte", ["Fortaleza", "São iguais"],
     "Qual é mais simples e tem menos poder de fogo: forte ou fortaleza?",
     "Forte! A fortaleza é um conjunto de construções bem sólidas.", {"falar_ops": False}),
    (2, ANO, ["FRANCESES", "CHEGAM AO", "MARANHÃO"], "1612", ["1555", "1630"],
     "Em que ano os franceses chegaram ao Maranhão e fundaram o forte de São Luís?",
     "Mil seiscentos e doze!", {}),
    # ---------- MUITO DIFÍCIL ----------
    (3, "O QUE NASSAU PROIBIU?", ["Jogar lixo nas", "ruas e nos rios", "jogar..."], "Bagaço de cana",
     ["Peixe", "Moedas"],
     "Agora a parte que reprova! Nassau proibiu jogar lixo nas ruas. E proibiu jogar o quê nos rios?",
     "Bagaço de cana! Os peixes dos rios eram o alimento da população pobre.", {"aviso": "DERRUBA MUITA GENTE!"}),
    (3, ANO, "foto:guararapes", "1654", ["1644", "1624"],
     "Em que ano os portugueses e seus aliados indígenas expulsaram os holandeses de vez?",
     "Mil seiscentos e cinquenta e quatro! Fim do Brasil holandês.", {"suspense": True}),
    (3, ANO, ["NASSAU VOLTA", "PARA A", "EUROPA"], "1644", ["1654", "1637"],
     "E em que ano Nassau foi obrigado a voltar para a Europa?",
     "Mil seiscentos e quarenta e quatro! Aí começaram as guerras contra os holandeses.",
     {"aviso": "TEM PEGADINHA!"}),
    (3, "ONDE FOI EM 1624?", "foto:salvador", "Salvador", ["Recife", "Rio de Janeiro"],
     "Na primeira invasão, em 1624, os holandeses ocuparam qual cidade por um ano?",
     "Salvador! Só na segunda vez eles foram para Pernambuco.", {}),
    (3, ANO, ["FRANCESES", "EXPULSOS DO", "MARANHÃO"], "1615", ["1612", "1567"],
     "Os franceses foram expulsos do Maranhão por tropas portuguesas em que ano?",
     "Mil seiscentos e quinze! Só três anos depois de chegarem.", {"suspense": True}),
    (3, "QUE FORTE É ESSE?", "foto:orange", "Forte Orange", ["Reis Magos", "Santa Cruz"],
     "Os holandeses construíram esse forte em 1631 na ilha de Itamaracá. Qual é o nome dele?",
     "Forte Orange! Hoje ele é patrimônio histórico.", {}),
    (3, "EM QUE CIDADE?", "foto:mauritshuis", "Haia", ["Paris", "Lisboa"],
     "Nassau queria quadros do Brasil para decorar o palácio dele na Holanda. Em qual cidade?",
     "Haia! E esse palácio existe até hoje.", {}),
    (3, "QUANTOS MORAVAM?", ["O povoado", "do Recife", "por volta de 1600"], "200", ["2 mil", "20 mil"],
     "Por volta de 1600, o povoado do Recife tinha cerca de quantos habitantes?",
     "Só uns duzentos! Mas o porto já era o mais movimentado do Brasil.", {"aviso": "QUASE TODO MUNDO ERRA!"}),
    (3, "QUE FORTE É ESSE?", "foto:reismagos", "Reis Magos", ["Forte Orange", "Santa Cruz"],
     "Esse forte em forma de estrela fica em Natal e começou a ser construído em 1598. Qual é?",
     "Forte dos Reis Magos!", {}),
    (3, QUEM, "foto:franspost", "Frans Post", ["Albert Eckhout", "Estácio de Sá"],
     "Esse pintor da comitiva de Nassau pintou paisagens do Nordeste, como O carro de bois. Quem é?",
     "Frans Post! Ele pintou o Recife e a cidade Maurícia.", {}),
    (3, "TOLERÂNCIA DE QUÊ?", ["Nassau instituiu", "a tolerância..."], "Religiosa", ["Do açúcar", "Dos piratas"],
     "Nassau instituiu a tolerância o quê?",
     "Religiosa! Cada um podia seguir a sua religião.", {}),
    (3, "QUEM CONVIDOU NASSAU?", ["Nassau veio ao", "Recife a", "convite de..."], "Cia. das Índias",
     ["Rei de Portugal", "Estácio de Sá"],
     "Nassau veio governar o Recife a convite de quem?",
     "Da Companhia Holandesa das Índias Ocidentais!", {}),
    (3, "O QUE ELE FUNDOU?", ["Um museu de", "história natural", "e um..."], "Observatório",
     ["Shopping", "Estádio"],
     "Nassau fundou um museu de história natural e um o quê?",
     "Um observatório astronômico, para estudar as estrelas!", {}),
    (3, "QUAL VEIO PRIMEIRO?", ["Linha do tempo:", "qual invasão", "foi a primeira?"], "Franceses no Rio",
     ["Holandeses no Recife", "Franceses em São Luís"],
     "Valendo a nota da prova! Qual dessas invasões aconteceu primeiro?",
     "Franceses no Rio, em 1555! São Luís foi em 1612 e Recife em 1630. Se acertou, tirou dez em história!",
     {"count": 10.0, "suspense": True, "final": True}),
]


def main():
    rnd = random.Random(42)
    pos = [0, 1, 2] * 15
    rnd.shuffle(pos)
    R = []
    for n, (nivel, perg, img, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        if ex.get("falar_ops", True):
            fq = f"{fq} {ops[0]}, {ops[1]} ou {ops[2]}?"
        r = {"n": n, "nivel": nivel, "pergunta": perg, "foto": f"q{n}.png",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": fq, "fala_r": fr, "count": ex.get("count", 8.0)}
        if isinstance(img, str):
            r["img"] = img.split(":", 1)[1]
        else:
            r["cartao"] = img
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo a nota... a resposta é..."
        R.append(r)
    assert len(R) == 42, len(R)
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], [sum(r["nivel"] == k for r in R) for k in (1, 2, 3)],
          sorted({r["img"] for r in R if "img" in r}))


if __name__ == "__main__":
    main()
