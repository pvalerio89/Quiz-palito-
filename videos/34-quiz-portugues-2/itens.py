"""Gera itens.json do vídeo 34 "Quiz de português do 3º ano, parte 2" (estilo mais humano, 2026-11-13).

30 perguntas próprias tiradas da matéria de Língua Portuguesa do 3º ano que o Patrick mandou em fotos (2026-11-15):
substantivo comum/próprio, adjetivo, verbo (ação, estado, fenômeno da natureza), pronomes pessoais, possessivos e
demonstrativos, sílaba tônica (oxítona, paroxítona, proparoxítona), separação de sílabas, S/SS/S com som de Z,
M antes de P e B, til (romã, vilã), O ou U / E ou I e sílaba que falta. 4 níveis (fácil → muito difícil).
Sem nomes do aluno/escola nem personagens de marca; Iara é lenda (domínio público).
A imagem de cada pergunta é um cartão de caderno com a palavra/frase (desenhado pelo build, em cartoes/).
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
TIPO = "QUE TIPO DE PALAVRA É?"
VERBO = "QUE TIPO DE VERBO?"
SIL = "QUANTAS SÍLABAS?"
TON = "COMO É A SÍLABA FORTE?"
COMP = "COMPLETE A PALAVRA:"
FRASE = "COMPLETE A FRASE:"
OXI = ["Oxítona", "Paroxítona", "Proparoxítona"]
SABIA_TON = "Oxítona: a sílaba forte é a última. Paroxítona: a penúltima. Proparoxítona: a antepenúltima."
# nível, pergunta (topo), cartão (linhas), certa, [erradas], fala da pergunta, fala da resposta, extras
P = [
    # ---------- FÁCIL ----------
    (1, "COMUM OU PRÓPRIO?", ["cachorro"], "Comum", ["Próprio", "Verbo"],
     "Pra aquecer: cachorro é substantivo comum ou próprio? Ou é verbo?",
     "Comum! Qualquer cachorro, com letra minúscula.", {"falar_ops": False, "count": 5.0}),
    (1, "QUAL PALAVRA É O VERBO?", ["A menina pedala", "a bicicleta."], "pedala", ["menina", "bicicleta"],
     "Na frase a menina pedala a bicicleta, qual palavra é o verbo?",
     "Pedala! É o que a menina está fazendo.", {"count": 6.0}),
    (1, "QUAL É O ADJETIVO?", ["A Caipora é", "muito forte."], "forte", ["Caipora", "muito"],
     "A Caipora é muito forte. Qual palavra é o adjetivo?",
     "Forte! Conta como a Caipora é.", {"sabia": "A Caipora é uma lenda brasileira: a protetora das matas e dos bichos."}),
    (1, SIL, ["ABACATE"], "4", ["3", "5"], "Quantas sílabas tem abacate?",
     "Quatro! A, ba, ca, te.", {"dica": ("Dica: bate palma em cada pedacinho!", "BATE PALMA!")}),
    (1, "QUAL SÍLABA FALTA?", ["MO _ _ LA", "(vai nas costas)"], "CHI", ["XI", "CHE"],
     "Ela vai nas suas costas até a escola. Mo, o quê, la? Chi com cê-agá, xi com xis, ou che?",
     "Chi, com cê-agá! Mochila.", {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (1, "QUAL PRONOME ENTRA?", ["Os meninos chegaram.", "___ estão felizes."], "Eles", ["Nós", "Ela"],
     "Pra não repetir os meninos, qual pronome entra?",
     "Eles! Vários meninos, então é eles.", {}),
    (1, COMP, ["_ APO", "(pula na lagoa)"], "S", ["Z", "C"],
     "Aquele bicho que pula na lagoa: sapo começa com esse, com zê ou com cê?",
     "Com esse! Sapo.", {"falar_ops": False}),
    (1, "QUAL É O NOME PRÓPRIO?", ["rio • Amazonas", "• lago"], "Amazonas", ["rio", "lago"],
     "Uma dessas palavras é substantivo próprio. Qual?",
     "Amazonas! É o nome de um rio específico, por isso tem letra maiúscula.", {}),
    # ---------- MÉDIO ----------
    (2, VERBO, ["TROVEJAR"], "Fenômeno", ["Ação", "Estado"],
     "Bora pro nível médio! Trovejar é verbo de ação, de estado ou de fenômeno da natureza?",
     "Fenômeno da natureza! Ninguém faz trovão, ele acontece.", {"falar_ops": False}),
    (2, VERBO, ["O cachorro", "CORREU muito."], "Ação", ["Estado", "Fenômeno"],
     "E na frase o cachorro correu muito, o verbo é de ação, de estado ou de fenômeno da natureza?",
     "Ação! Correr é fazer alguma coisa.", {"falar_ops": False}),
    (2, TON, ["SOFÁ"], "Oxítona", ["Paroxítona", "Proparoxítona"],
     "Hora da sílaba tônica! Sofá é oxítona, paroxítona ou proparoxítona?",
     "Oxítona! A sílaba forte é a última: fá.", {"falar_ops": False, "sabia": SABIA_TON}),
    (2, TON, ["MESA"], "Paroxítona", ["Oxítona", "Proparoxítona"],
     "E mesa? Oxítona, paroxítona ou proparoxítona?",
     "Paroxítona! Me, sa: a forte é a penúltima.", {"falar_ops": False,
                                                  "sabia": "A maioria das palavras do português é paroxítona!"}),
    (2, "M OU N?", ["PO _ TE"], "N", ["M", "NH"],
     "Ponte: antes do tê, vai eme ou ene?",
     "Ene! Eme só antes de pê e bê.", {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (2, FRASE, ["Nós temos uma casa.", "___ casa é azul."], "Nossa", ["Minha", "Sua"],
     "Nós temos uma casa. Qual pronome completa: a casa é de quem?",
     "Nossa! A casa é nossa. Pronome possessivo.", {}),
    (2, COMP, ["RO _ A", "(flor cheirosa)"], "S", ["Z", "SS"],
     "Rosa, a flor, se escreve com esse, com zê ou com dois esses?",
     "Com esse! Rosa tem som de zê, mas é com esse.", {"falar_ops": False,
                                                     "sabia": "S entre duas vogais tem som de Z: rosa, casa, mesa."}),
    (2, SIL, ["ASSUSTADO"], "4", ["5", "3"], "Quantas sílabas tem assustado?",
     "Quatro! As, sus, ta, do. Os dois esses se separam.", {"suspense": True}),
    # ---------- DIFÍCIL ----------
    (3, "ESTE, ESSE OU AQUELE?", ["___ livro aqui na", "minha mão é novo."], "Este", ["Esse", "Aquele"],
     "Subindo o nível! O livro está aqui, na mão de quem fala. Qual palavra completa?",
     "Este! Este é pro que está pertinho de quem fala.",
     {"sabia": "Este: perto de quem fala. Esse: perto de quem ouve. Aquele: longe dos dois."}),
    (3, "ISTO, ISSO OU AQUILO?", ["O que é ___ aí", "na sua mochila?"], "isso", ["isto", "aquilo"],
     "A coisa está aí, perto de você que está ouvindo. Qual palavra completa?",
     "Isso! Perto de quem ouve é esse, essa e isso.", {"aviso": "TEM PEGADINHA!"}),
    (3, "COMO SE ESCREVE?", ["Fruta vermelha", "e redondinha"], "Maçã", ["Massã", "Maçan"],
     "Aquela fruta vermelha e redondinha. Como se escreve?",
     "Maçã! Com cê-cedilha e til.", {"suspense": True}),
    (3, "O OU U?", ["C _ RUJA"], "O", ["U", "OU"],
     "A ave da noite: coruja se escreve com o ou com u?",
     "Com o! Coruja.", {"falar_ops": False}),
    (3, "E OU I?", ["M _ XERICA"], "E", ["I", "A"],
     "E mexerica, a fruta? É com é ou com i?",
     "Com é! Mexerica. Muita gente fala mixirica.", {"falar_ops": False, "aviso": "DERRUBA MUITA GENTE!"}),
    (3, "O OU U?", ["B _ EIRO"], "U", ["O", "OU"],
     "Aquele buraco da rua por onde a água da chuva desce: é com o ou com u?",
     "Com u! Bueiro.", {"falar_ops": False, "aviso": "TEM PEGADINHA!",
                        "dica": ("Dica: a gente escreve igual fala!", "ESCREVE IGUAL FALA")}),
    (3, TON, ["ÁRVORE"], "Proparoxítona", ["Paroxítona", "Oxítona"],
     "Árvore é oxítona, paroxítona ou proparoxítona?",
     "Proparoxítona! Ár é a antepenúltima sílaba.", {"falar_ops": False,
                                                    "sabia": "Toda proparoxítona tem acento!"}),
    (3, "QUAL SÍLABA FALTA?", ["GA _ _ TO", "(menino)"], "RO", ["LO", "RRO"],
     "Que sílaba falta? Ga, o quê, to? Um menino!",
     "Ro! Garoto, com um erre só.", {"falar_ops": False}),
    # ---------- MUITO DIFÍCIL ----------
    (4, TON, ["JABUTI"], "Oxítona", ["Paroxítona", "Proparoxítona"],
     "Agora o nível mais difícil! Jabuti é oxítona, paroxítona ou proparoxítona?",
     "Oxítona! Ja, bu, ti: a forte é a última. E não tem acento!", {"falar_ops": False, "suspense": True}),
    (4, TON, ["RUBRICA"], "Paroxítona", ["Proparoxítona", "Oxítona"],
     "Essa derruba até adulto! Rubrica é oxítona, paroxítona ou proparoxítona?",
     "Paroxítona! Ru, bri, ca. Se fosse proparoxítona, teria acento.", {"falar_ops": False,
                                                                       "aviso": "QUASE TODO MUNDO ERRA!",
                                                                       "dica": ("Dica: tem acento?", "TEM ACENTO?")}),
    (4, SIL, ["SAÚDE"], "3", ["2", "4"], "Quantas sílabas tem a palavra saúde?",
     "Três! Sa, ú, de. O acento separa o a do u.", {"aviso": "TEM PEGADINHA!"}),
    (4, COMP, ["PÊ _ EGO", "(fruta)"], "SS", ["S", "Ç"],
     "Pêssego, a fruta: é com um esse, com dois esses ou com cê-cedilha?",
     "Com dois esses! Pêssego.", {"falar_ops": False}),
    (4, "ISTO, ISSO OU AQUILO?", ["O que é ___", "lá no céu?"], "aquilo", ["isto", "isso"],
     "A coisa está lá longe, no céu. Qual palavra completa?",
     "Aquilo! Longe de todo mundo.", {}),
    (4, SIL, ["PARALELEPÍPEDO"], "7", ["6", "8"],
     "Valendo tudo! Quantas sílabas tem paralelepípedo?",
     "Sete! Pa, ra, le, le, pí, pe, do. Se você acertou essa, pode ensinar a turma!",
     {"count": 10.0, "suspense": True, "final": True}),
]

FALA = {"4": "quatro", "3": "três", "5": "cinco", "6": "seis", "7": "sete", "2": "dois", "8": "oito"}


def main():
    rnd = random.Random(34)
    pos = [0, 1, 2] * 10
    rnd.shuffle(pos)
    pos[0] = 0
    R = []
    for n, (nivel, perg, cartao, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        if ex.get("falar_ops", True):
            fo = [FALA.get(o, o) for o in ops]
            fq = f"{fq} {fo[0]}, {fo[1]} ou {fo[2]}?"
        r = {"n": n, "nivel": nivel, "pergunta": perg, "cartao": cartao, "foto": f"q{n}.png",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": fq, "fala_r": fr, "count": ex.get("count", 8.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo o boletim... a resposta é..."
        R.append(r)
    assert len(R) == 30 and len({tuple(r["cartao"]) for r in R}) == 30
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
