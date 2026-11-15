"""Gera itens.json do vídeo 33 "Quiz de português do 3º ano" (estilo mais humano, 2026-11-13).

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
    (1, "COMUM OU PRÓPRIO?", ["Brasil"], "Próprio", ["Comum", "Adjetivo"],
     "Pra começar fácil: Brasil é substantivo comum ou próprio? Ou é adjetivo?",
     "Próprio! Nome de lugar específico, com letra maiúscula.", {"falar_ops": False, "count": 5.0}),
    (1, "QUAL PALAVRA É O VERBO?", ["O gato pula", "o muro."], "pula", ["gato", "muro"],
     "Na frase o gato pula o muro, qual palavra é o verbo?",
     "Pula! Verbo é a ação, o que o gato faz.", {"count": 6.0}),
    (1, "QUAL É O ADJETIVO?", ["Que cachorro", "lindo!"], "lindo", ["cachorro", "que"],
     "Que cachorro lindo! Qual palavra é o adjetivo?",
     "Lindo! O adjetivo dá uma característica pro cachorro.", {}),
    (1, SIL, ["BORBOLETA"], "4", ["3", "5"], "Quantas sílabas tem a palavra borboleta?",
     "Quatro! Bor, bo, le, ta.", {"dica": ("Dica: bate palma em cada pedacinho!", "BATE PALMA!")}),
    (1, COMP, ["PÁ _ ARO"], "SS", ["S", "Ç"],
     "Pássaro se escreve com um esse, com dois esses ou com cê-cedilha?",
     "Com dois esses! Pássaro.", {"falar_ops": False,
                                  "sabia": "Entre duas vogais, pra ter som de S, a gente usa SS."}),
    (1, TIPO, ["AMOR"], "Substantivo", ["Verbo", "Adjetivo"], "Amor é um sentimento. Que tipo de palavra ele é?",
     "Substantivo! Sentimento também tem nome.",
     {"sabia": "Substantivo dá nome a tudo: pessoas, bichos, lugares, objetos e até sentimentos."}),
    (1, "QUAL SÍLABA FALTA?", ["PERI _ _ TO", "(ave verde que fala)"], "QUI", ["GUI", "CO"],
     "Que sílaba falta no nome daquele pássaro verde que fala? Peri, o quê, to?",
     "Qui! Periquito, com q, u, i.", {"falar_ops": False}),
    (1, "QUAL PRONOME ENTRA?", ["A menina chegou.", "___ gosta de ler."], "Ela", ["Nós", "Eles"],
     "Pra não repetir a menina, qual pronome entra no lugar?",
     "Ela! Pronome pessoal no lugar do nome.", {}),
    # ---------- MÉDIO ----------
    (2, VERBO, ["CHOVER"], "Fenômeno", ["Ação", "Estado"],
     "Bora pro nível médio! Chover é verbo de ação, de estado ou de fenômeno da natureza?",
     "Fenômeno da natureza! Chover, ventar, trovejar...", {"falar_ops": False}),
    (2, VERBO, ["A menina", "ESTÁ feliz."], "Estado", ["Ação", "Fenômeno"],
     "E na frase a menina está feliz, o verbo está é de ação, de estado ou de fenômeno da natureza?",
     "Estado! Ela não está fazendo nada, só está feliz.", {"falar_ops": False,
                                                        "dica": ("Dica: ela tá fazendo alguma coisa?", "ELA ESTÁ FAZENDO ALGO?")}),
    (2, TON, ["CAFÉ"], "Oxítona", ["Paroxítona", "Proparoxítona"],
     "Agora sílaba tônica, a sílaba mais forte! Café é oxítona, paroxítona ou proparoxítona?",
     "Oxítona! A sílaba forte é a última: fé.", {"falar_ops": False, "sabia": SABIA_TON}),
    (2, "M OU N?", ["BO _ BOM"], "M", ["N", "NH"],
     "Bombom: antes do bê, vai eme ou ene?",
     "Eme! Antes de pê e bê, sempre eme.", {"falar_ops": False, "aviso": "TEM REGRA!",
                                          "sabia": "Antes de P e B, sempre M: bombom, campo, tempo."}),
    (2, "QUAL É O VERBO?", ["COZINH..."], "Cozinhar", ["Cozinheiro", "Cozinha"],
     "São todas da mesma família. Qual delas é o verbo?",
     "Cozinhar! Cozinheiro é quem cozinha: é substantivo.", {}),
    (2, FRASE, ["Eu tenho um gato.", "___ gato é preto."], "Meu", ["Seu", "Nosso"],
     "Eu tenho um gato. Qual pronome completa: o quê gato é preto?",
     "Meu! O gato é meu. Pronome possessivo.", {}),
    (2, COMP, ["CA _ A"], "S", ["Z", "SS"],
     "Cuidado com essa! Casa se escreve com esse, com zê ou com dois esses?",
     "Com esse! Casa tem som de zê, mas é com esse.", {"falar_ops": False, "aviso": "TEM PEGADINHA!",
                                                      "sabia": "S entre duas vogais tem som de Z: casa, mesa, rosa."}),
    (2, "QUAL É O ADJETIVO?", ["A Iara tem", "cabelos longos."], "longos", ["cabelos", "tem"],
     "A Iara, a mãe d'água das lendas, tem cabelos longos. Qual é o adjetivo?",
     "Longos! Conta como são os cabelos.", {"sabia": "A Iara é uma lenda brasileira: a sereia dos rios."}),
    # ---------- DIFÍCIL ----------
    (3, "ESTE, ESSE OU AQUELE?", ["___ prédio lá", "longe é alto."], "Aquele", ["Este", "Esse"],
     "Subindo o nível! O prédio está lá longe. Qual palavra completa?",
     "Aquele! Aquele é pro que está longe de todo mundo.",
     {"sabia": "Este: perto de quem fala. Esse: perto de quem ouve. Aquele: longe dos dois."}),
    (3, "QUAL É A FRUTA?", ["ROMA", "ROMÃ"], "Romã", ["Roma", "As duas"],
     "Uma é cidade, a outra é fruta. Qual é a fruta?",
     "Romã, com til! O til deixa o som pelo nariz.", {"falar_ops": False}),
    (3, "QUAL É O BRINQUEDO?", ["Rodei o ___", "no chão."], "Pião", ["Peão", "Pilão"],
     "Aquele brinquedo que gira no chão: é pião, com i, ou peão, com é?",
     "Pião, com i! Peão é o trabalhador da fazenda.", {"falar_ops": False, "aviso": "TEM PEGADINHA!",
                                                       "suspense": True}),
    (3, TON, ["TRÂNSITO"], "Proparoxítona", ["Paroxítona", "Oxítona"],
     "Trânsito é oxítona, paroxítona ou proparoxítona?",
     "Proparoxítona! Trân é a antepenúltima sílaba.", {"falar_ops": False,
                                                     "dica": ("Dica: olha o acento circunflexo!", "OLHA O ACENTO!"),
                                                     "sabia": "Toda proparoxítona tem acento!"}),
    (3, "O OU U?", ["M _ SQUITO"], "O", ["U", "OU"],
     "A gente fala musquito... mas escreve com o ou com u?",
     "Com o! Mosquito.", {"falar_ops": False, "aviso": "DERRUBA MUITA GENTE!"}),
    (3, "E OU I?", ["_ LETRICISTA"], "E", ["I", "A"],
     "E eletricista? Começa com é ou com i?",
     "Com é! Vem de eletricidade.", {"falar_ops": False}),
    (3, "S OU SS?", ["CONVER _ A"], "S", ["SS", "Ç"],
     "Conversa: é com um esse, com dois esses ou com cê-cedilha?",
     "Com um esse só! Depois de consoante, nunca vai dois esses.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!", "suspense": True,
      "sabia": "Depois de consoante, o S sozinho já tem som de S: conversa, pensar."}),
    (3, "NO LUGAR DE VÓS...", ["VÓS"], "Vocês", ["Nós", "Eles"],
     "Hoje quase ninguém fala vós. No lugar de vós, a gente fala...",
     "Vocês! E no lugar de tu, muita gente fala você.", {}),
    # ---------- MUITO DIFÍCIL ----------
    (4, TON, ["RUIM"], "Oxítona", ["Paroxítona", "Proparoxítona"],
     "Agora o nível mais difícil! Ruim é oxítona, paroxítona ou proparoxítona?",
     "Oxítona! Ru, im: a sílaba forte é a última.", {"falar_ops": False, "aviso": "DERRUBA MUITA GENTE!",
                                                   "suspense": True}),
    (4, TON, ["GRATUITO"], "Paroxítona", ["Oxítona", "Proparoxítona"],
     "E gratuito? Oxítona, paroxítona ou proparoxítona?",
     "Paroxítona! Gra, tui, to: a forte é tui.", {"falar_ops": False, "aviso": "QUASE TODO MUNDO ERRA!"}),
    (4, TON, ["RECORDE"], "Paroxítona", ["Proparoxítona", "Oxítona"],
     "Bateu o recorde! Recorde é oxítona, paroxítona ou proparoxítona?",
     "Paroxítona! Re, cor, de. Se fosse proparoxítona, teria acento.", {"falar_ops": False,
                                                                       "dica": ("Dica: tem acento?", "TEM ACENTO?")}),
    (4, "QUAL SÍLABA FALTA?", ["JABU _ _ CABA", "(fruta roxinha)"], "TI", ["TE", "CHI"],
     "Que sílaba falta nessa fruta roxinha? Jabu, o quê, caba? Ti, te ou chi?",
     "Ti! Jabuticaba, com i.", {"falar_ops": False}),
    (4, FRASE, ["O vilão e a ___"], "vilã", ["vilona", "vilãe"],
     "O vilão e a... como fica o feminino de vilão?",
     "Vilã! Com til.", {}),
    (4, SIL, ["PROPAROXÍTONA"], "6", ["5", "7"], "Valendo tudo! Quantas sílabas tem a palavra proparoxítona?",
     "Seis! Pro, pa, ro, xí, to, na. Se você acertou essa, passou de ano!",
     {"count": 10.0, "suspense": True, "final": True}),
]

FALA = {"4": "quatro", "3": "três", "5": "cinco", "6": "seis", "7": "sete"}


def main():
    rnd = random.Random(33)
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
        r = {"n": n, "nivel": nivel, "pergunta": perg, "cartao": cartao, "foto": f"p{n}.png",
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
