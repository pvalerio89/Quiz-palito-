"""Gera itens.json do vídeo 38 "PAIS contra FILHOS: prova do 5º ano" (estilo mais humano, 2026-11-18).

32 perguntas próprias do 5º ano (português, matemática, ciências, geografia, história) em 3 rodadas (fácil, médio,
difícil). Pensado para a TV/família: placar "PAIS x FILHOS" a cada 10 questões. A imagem de cada pergunta é um
cartão de caderno com a matéria no topo (desenhado pelo build, em cartoes/). Nenhuma repete os vídeos 25 e 33-35.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
POR, MAT, CIE, GEO, HIS = "PORTUGUÊS", "MATEMÁTICA", "CIÊNCIAS", "GEOGRAFIA", "HISTÓRIA"
Q = "QUANTO É?"
# rodada, matéria, pergunta (topo), cartão (linhas), certa, [erradas], fala da pergunta, fala da resposta, extras
P = [
    # ---------- RODADA 1 (fácil) ----------
    (1, MAT, Q, ["9 × 6"], "54", ["56", "45"], "Pra esquentar: quanto é nove vezes seis?",
     "Cinquenta e quatro! Começou bem?", {"count": 5.0}),
    (1, GEO, "CAPITAL DO BRASIL?", ["Capital do", "Brasil"], "Brasília", ["Rio de Janeiro", "São Paulo"],
     "Essa é pra todo mundo acertar: qual é a capital do Brasil?",
     "Brasília! Quem disse Rio de Janeiro voltou pro tempo antigo!", {"count": 5.0}),
    (1, CIE, "QUANTOS PLANETAS?", ["Planetas do", "Sistema Solar"], "8", ["9", "7"],
     "Quantos planetas tem o Sistema Solar?",
     "Oito! Plutão virou planeta-anão em 2006. Pai e mãe que disseram nove aprenderam na escola antiga!",
     {"aviso": "PAIS, CUIDADO!", "sabia": "Plutão deixou de ser planeta em 2006: hoje é um planeta-anão."}),
    (1, POR, "QUAL É O PLURAL?", ["PÃO"], "Pães", ["Pãos", "Pões"],
     "Qual é o plural de pão?", "Pães! Um pão, dois pães.", {}),
    (1, HIS, "EM QUE ANO?", ["Os portugueses", "chegam ao Brasil"], "1500", ["1822", "1889"],
     "Em que ano os portugueses chegaram ao Brasil?", "Mil e quinhentos! Com a esquadra de Pedro Álvares Cabral.", {}),
    (1, CIE, "QUAL É MAMÍFERO?", ["Qual desses", "é mamífero?"], "Baleia", ["Tubarão", "Pinguim"],
     "Qual desses animais é mamífero?", "A baleia! O filhote mama, e ela respira ar, igual a gente.", {}),
    (1, MAT, "QUANTOS LADOS?", ["HEXÁGONO"], "6", ["5", "8"],
     "Quantos lados tem um hexágono?", "Seis! Igual aos buraquinhos do favo de mel.", {}),
    (1, GEO, "QUANTAS REGIÕES?", ["Regiões do", "Brasil"], "5", ["4", "6"],
     "O Brasil é dividido em quantas regiões?", "Cinco! Norte, Nordeste, Centro-Oeste, Sudeste e Sul.",
     {"dica": ("Dica: Norte, Sul... e conta o resto!", "CONTA NOS DEDOS!")}),
    # ---------- RODADA 2 (médio) ----------
    (2, POR, "QUAL É O ANTÔNIMO?", ["GENEROSO"], "Egoísta", ["Bondoso", "Gentil"],
     "Rodada dois, valendo! Antônimo é o contrário. Qual é o antônimo de generoso?",
     "Egoísta! Bondoso e gentil são sinônimos, quase a mesma coisa.", {}),
    (2, MAT, Q, ["3,50 + 1,75"], "5,25", ["4,80", "5,15"],
     "Conta com vírgula, igual dinheiro: três e cinquenta mais um e setenta e cinco?",
     "Cinco e vinte e cinco! Quem faz compra no mercado matou essa.", {"falar_ops": False}),
    (2, CIE, "ÁGUA VIRANDO VAPOR?", ["ÁGUA → VAPOR"], "Evaporação", ["Condensação", "Solidificação"],
     "Quando a água vira vapor, como isso se chama?",
     "Evaporação! Condensação é o contrário: o vapor virando água.", {}),
    (2, HIS, "QUEM PROCLAMOU?", ["Independência", "7 de setembro", "de 1822"], "Dom Pedro I",
     ["Tiradentes", "Dom Pedro II"],
     "Sete de setembro de 1822. Quem proclamou a independência do Brasil? Dom Pedro primeiro, Tiradentes ou Dom Pedro segundo?",
     "Dom Pedro primeiro! Às margens do riacho Ipiranga.", {"falar_ops": False}),
    (2, GEO, "MAIOR ESTADO?", ["Maior estado", "do Brasil"], "Amazonas", ["Pará", "Mato Grosso"],
     "Qual é o maior estado do Brasil?", "Amazonas! É maior que muitos países da Europa.",
     {"sabia": "O Amazonas é quase 3 vezes maior que a França."}),
    (2, MAT, Q, ["25% de 80"], "20", ["25", "40"], "Quanto é vinte e cinco por cento de oitenta?",
     "Vinte! Vinte e cinco por cento é a quarta parte.", {}),
    (2, POR, "QUAL COMPLETA?", ["Eu quis ir,", "___ choveu."], "mas", ["mais", "más"],
     "Qual palavra completa a frase do cartão? Mas sem i, mais com i, ou más com acento?",
     "Mas, sem i! Mais com i é de quantidade, o contrário de menos.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (2, CIE, "O QUE AS PLANTAS SOLTAM?", ["FOTOSSÍNTESE"], "Oxigênio", ["Gás carbônico", "Nitrogênio"],
     "Na fotossíntese, que gás as plantas soltam no ar?",
     "Oxigênio! Elas pegam gás carbônico e devolvem oxigênio.",
     {"dica": ("Dica: é o gás que a gente respira!", "A GENTE RESPIRA ELE!")}),
    (2, GEO, "ONDE O SOL NASCE?", ["O Sol nasce", "no..."], "Leste", ["Oeste", "Norte"],
     "De que lado o Sol nasce?", "No leste! E se põe no oeste.", {"count": 6.0}),
    (2, HIS, "QUEM ASSINOU?", ["Lei Áurea", "1888"], "Princesa Isabel", ["Dom Pedro I", "Tiradentes"],
     "Em 1888, quem assinou a Lei Áurea? Princesa Isabel, Dom Pedro primeiro ou Tiradentes?",
     "Princesa Isabel! A lei acabou com a escravidão no Brasil.", {"falar_ops": False}),
    (2, MAT, "QUANTOS CENTÍMETROS?", ["1,5 m = ? cm"], "150", ["15", "1500"],
     "Um metro e meio tem quantos centímetros?", "Cento e cinquenta! Um metro tem cem centímetros.", {}),
    (2, POR, "QUAL É O SUJEITO?", ["Os meninos", "jogaram bola."], "Os meninos", ["jogaram", "bola"],
     "Os meninos jogaram bola. Qual é o sujeito da frase?",
     "Os meninos! Sujeito é quem faz a ação.", {}),
    # ---------- RODADA 3 (difícil) ----------
    (3, CIE, "MAIOR ÓRGÃO DO CORPO?", ["Maior órgão", "do corpo humano"], "Pele", ["Fígado", "Intestino"],
     "Agora complica! Qual é o maior órgão do corpo humano?",
     "A pele! Ela também é um órgão, e é o maior de todos.", {"aviso": "TEM PEGADINHA!", "suspense": True}),
    (3, MAT, Q, ["2 + 3 × 4"], "14", ["20", "24"], "Essa aqui derruba muito adulto! Dois mais três vezes quatro?",
     "Catorze! Primeiro a multiplicação, depois a soma. Quem fez na ordem deu vinte.",
     {"aviso": "DERRUBA ATÉ ADULTO!"}),
    (3, GEO, "MAIOR OCEANO?", ["Maior oceano", "do mundo"], "Pacífico", ["Atlântico", "Índico"],
     "Qual é o maior oceano do mundo?", "Pacífico! Ele é maior que todos os continentes juntos.",
     {"sabia": "O Pacífico sozinho é maior que toda a terra do planeta junta."}),
    (3, HIS, "1ª CAPITAL DO BRASIL?", ["Primeira", "capital do", "Brasil"], "Salvador", ["Rio de Janeiro", "São Paulo"],
     "Antes de Brasília e do Rio, qual foi a primeira capital do Brasil?",
     "Salvador! Depois veio o Rio, e só em 1960 Brasília.",
     {"dica": ("Dica: fica no Nordeste!", "FICA NO NORDESTE!")}),
    (3, POR, "QUANTAS SÍLABAS?", ["PARALELEPÍPEDO"], "7", ["6", "8"], "Quantas sílabas tem paralelepípedo?",
     "Sete! Pa, ra, le, le, pí, pe, do.", {"aviso": "CONTA DEVAGAR!"}),
    (3, CIE, "MAIS PERTO DO SOL?", ["Planeta mais", "perto do Sol"], "Mercúrio", ["Vênus", "Marte"],
     "Qual planeta fica mais perto do Sol?", "Mercúrio! Vênus vem logo depois.", {}),
    (3, MAT, Q, ["0,5 × 0,5"], "0,25", ["2,5", "1"],
     "Cuidado! Zero vírgula cinco vezes zero vírgula cinco?",
     "Zero vírgula vinte e cinco! Metade da metade é um quarto.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!", "suspense": True}),
    (3, GEO, "QUE RIO É ESSE?", ["Apelido:", "VELHO CHICO"], "São Francisco", ["Tietê", "Paraná"],
     "Ele tem o apelido de Velho Chico. Que rio é esse?",
     "Rio São Francisco! Nasce em Minas Gerais e chega no mar entre Alagoas e Sergipe.", {}),
    (3, HIS, "O QUE ERA?", ["PAU-BRASIL"], "Uma árvore", ["Um rio", "Uma moeda"],
     "O pau-brasil, que deu nome ao país, era o quê?",
     "Uma árvore! A madeira soltava uma tinta vermelha, cor de brasa.", {}),
    (3, POR, "QUAL É O COLETIVO?", ["Coletivo de", "LOBOS"], "Alcateia", ["Cardume", "Matilha"],
     "Qual é o coletivo de lobos?", "Alcateia! Matilha é de cães, cardume é de peixes.",
     {"aviso": "DERRUBA ATÉ ADULTO!"}),
    (3, CIE, "QUANTOS OSSOS?", ["Ossos do corpo", "de um adulto"], "206", ["106", "306"],
     "Quantos ossos tem o corpo de um adulto?", "Duzentos e seis! O bebê nasce com mais, e eles vão se juntando.",
     {"suspense": True}),
    (3, MAT, Q, ["1/3 + 1/6"], "1/2", ["2/9", "1/9"],
     "Valendo a nota da família! Um terço mais um sexto? Um meio, dois nonos ou um nono?",
     "Um meio! Um terço é dois sextos, mais um sexto dá três sextos, que é a metade. Se acertou, passou de ano!",
     {"falar_ops": False, "count": 10.0, "suspense": True, "final": True}),
]

FALA = {"1": "um", "4": "quatro", "3": "três", "5": "cinco", "6": "seis", "7": "sete", "2": "dois", "8": "oito",
        "9": "nove"}


def main():
    rnd = random.Random(38)
    pos = [0, 1, 2] * 11
    rnd.shuffle(pos)
    pos[0] = 0
    R = []
    for n, (rod, mat, perg, cartao, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        if ex.get("falar_ops", True):
            fo = [FALA.get(o, o) for o in ops]
            fq = f"{fq} {fo[0]}, {fo[1]} ou {fo[2]}?"
        r = {"n": n, "rodada": rod, "materia": mat, "pergunta": perg, "cartao": cartao, "foto": f"q{n}.png",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": fq, "fala_r": fr, "count": ex.get("count", 8.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Pais ou filhos... a resposta é..."
        R.append(r)
    assert len(R) == 32 and len({tuple(r["cartao"]) for r in R}) == 32
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
