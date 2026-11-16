"""Gera itens.json do vídeo 35 "Prova de português do 3º ano" (estilo mais humano, 2026-11-13).

30 perguntas próprias tiradas do simulado de Língua Portuguesa do 3º ano que o Patrick mandou em PDF (2026-11-16):
interpretação do texto da prova (Clara, árvore genealógica), substantivo comum/próprio, adjetivo, verbos de ação/estado/
fenômeno, pronomes pessoais/possessivos/demonstrativos, G/GU, S/SS/S com som de Z, sílabas e sílaba tônica.
Nenhuma repete os vídeos 33 e 34 nem os Shorts portugues-2/3. Sem nome do aluno/escola. 4 níveis (fácil → muito difícil).
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
    (1, "COMUM OU PRÓPRIO?", ["Curitiba"], "Próprio", ["Comum", "Verbo"],
     "Primeira questão da prova: Curitiba é substantivo comum ou próprio? Ou é verbo?",
     "Próprio! É o nome de uma cidade, por isso tem letra maiúscula.", {"falar_ops": False, "count": 5.0}),
    (1, "QUANDO FOI?", ["No sábado, Clara", "achou uma caixa", "de fotos."], "No sábado", ["No domingo", "Na segunda"],
     "Leia: no sábado, Clara achou uma caixa de fotos. Quando ela achou as fotos?",
     "No sábado! Tá escrito logo no começo da frase.", {"count": 6.0}),
    (1, "QUAL PRONOME ENTRA?", ["Eu e minha avó:", "___ fizemos", "a pesquisa."], "Nós", ["Eles", "Ela"],
     "Eu e minha avó fizemos a pesquisa. Qual pronome entra no lugar de eu e minha avó?",
     "Nós! Eu mais alguém vira nós.", {}),
    (1, VERBO, ["Pedro CUIDA", "dos animais."], "Ação", ["Estado", "Fenômeno"],
     "Pedro cuida dos animais. Cuidar é verbo de ação, de estado ou de fenômeno da natureza?",
     "Ação! Cuidar é fazer alguma coisa.", {"falar_ops": False}),
    (1, COMP, ["O _ O", "(o cachorro adora)"], "SS", ["S", "Ç"],
     "O cachorro adora roer: o, o quê, o? Com um esse, com dois esses ou com cê-cedilha?",
     "Com dois esses! Osso.", {"falar_ops": False}),
    (1, SIL, ["CANETA"], "3", ["2", "4"], "Quantas sílabas tem caneta?",
     "Três! Ca, ne, ta.", {"dica": ("Dica: bate palma em cada pedacinho!", "BATE PALMA!")}),
    (1, "O QUE ROSA É DE PEDRO?", ["Pedro é neto", "de Rosa."], "Avó", ["Tia", "Irmã"],
     "Pedro é neto de Rosa. Então, o que Rosa é de Pedro?",
     "Avó! Se ele é neto, ela é a avó.", {}),
    (1, "QUE ÁRVORE É ESSA?", ["Sem terra nem", "semente, só com", "nomes da família"], "Genealógica",
     ["De Natal", "Frutífera"],
     "Uma árvore desenhada sem terra nem semente, só com os nomes da família. Que árvore é essa?",
     "Genealógica! A árvore da família.", {"sabia": "Na árvore genealógica, cada galho mostra os parentes: pais, avós, bisavós..."}),
    # ---------- MÉDIO ----------
    (2, VERBO, ["O cachorro", "PARECE cansado."], "Estado", ["Ação", "Fenômeno"],
     "Nível médio, valendo! O cachorro parece cansado. Parecer é verbo de ação, de estado ou de fenômeno da natureza?",
     "Estado! Parecer não é fazer nada, mostra como o cachorro está.", {"falar_ops": False}),
    (2, TON, ["PIPOCA"], "Paroxítona", ["Oxítona", "Proparoxítona"],
     "Pipoca é oxítona, paroxítona ou proparoxítona?",
     "Paroxítona! Pi, po, ca: a forte é a penúltima.", {"falar_ops": False, "sabia": SABIA_TON}),
    (2, TON, ["CORAÇÃO"], "Oxítona", ["Paroxítona", "Proparoxítona"],
     "E coração? Oxítona, paroxítona ou proparoxítona?",
     "Oxítona! Co, ra, ção: a forte é a última.", {"falar_ops": False}),
    (2, "G OU GU?", ["FO _ ETE", "(vai pro espaço)"], "GU", ["G", "J"],
     "Ele vai pro espaço: fo, o quê, ete? Com gê, com gê-u ou com jota?",
     "Com gê-u! Foguete. Sem o u, ia ler fojete.", {"falar_ops": False, "aviso": "TEM PEGADINHA!",
                                                  "sabia": "Antes de E e I, o GU deixa o G com som de gato: foguete, guerra."}),
    (2, "ESTA, ESSA OU AQUELA?", ["___ foto aí", "com você é antiga."], "Essa", ["Esta", "Aquela"],
     "A foto está aí, com você que está ouvindo. Qual palavra completa?",
     "Essa! Perto de quem ouve é esse e essa.", {}),
    (2, "QUAL É O ADJETIVO?", ["A árvore estava", "colorida."], "colorida", ["árvore", "estava"],
     "A árvore estava colorida. Qual palavra é o adjetivo?",
     "Colorida! Conta como a árvore estava.", {}),
    (2, "S COM SOM DE Z?", ["Em qual palavra", "o S tem som de Z?"], "Camisa", ["Sapo", "Sino"],
     "Em qual dessas palavras o esse tem som de zê?",
     "Camisa! O esse entre duas vogais tem som de zê.", {}),
    (2, "QUANTOS VERBOS?", ["Clara pesquisou", "e desenhou."], "2", ["1", "3"],
     "Clara pesquisou e desenhou. Quantos verbos tem nessa frase?",
     "Dois! Pesquisou e desenhou.", {"suspense": True}),
    # ---------- DIFÍCIL ----------
    (3, TIPO, ["RAIVA"], "Substantivo", ["Adjetivo", "Verbo"],
     "Agora complica! Raiva é substantivo, adjetivo ou verbo?",
     "Substantivo! Sentimento também é nome de coisa.", {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (3, "COMO SE ESCREVE?", ["Árvore que", "dá manga"], "Mangueira", ["Manguera", "Mangera"],
     "A árvore que dá manga. Como se escreve?",
     "Mangueira! Com gê-u e com e-i: man, guei, ra.", {"aviso": "DERRUBA MUITA GENTE!", "suspense": True}),
    (3, COMP, ["GIRA _ OL", "(flor amarela)"], "SS", ["S", "Ç"],
     "A flor amarela que segue o sol: gira, o quê, ol? Com um esse, com dois esses ou com cê-cedilha?",
     "Com dois esses! Girassol. Com um esse só, ia ler girasol, com som de zê.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (3, FRASE, ["Os livros são de nós.", "Eles são ___."], "nossos", ["nossas", "nosso"],
     "Os livros são de nós. Eles são o quê? Nossos, nossas ou nosso?",
     "Nossos! Livros, no plural e no masculino.", {"falar_ops": False}),
    (3, "QUE PRONOME É?", ["AQUELA caixa", "é antiga."], "Demonstrativo", ["Pessoal", "Possessivo"],
     "Aquela caixa é antiga. Aquela é pronome pessoal, possessivo ou demonstrativo?",
     "Demonstrativo! Mostra onde a caixa está: lá longe.",
     {"falar_ops": False, "sabia": "Pessoal: eu, ele, nós. Possessivo: meu, seu, nosso. Demonstrativo: este, esse, aquele."}),
    (3, "QUEM SÃO ELES?", ["Clara e Pedro", "conversaram.", "ELES trocaram fotos."], "Clara e Pedro",
     ["Rosa e Miguel", "Os avós"],
     "Clara e Pedro conversaram. Eles trocaram fotos. Quem são eles?",
     "Clara e Pedro! O pronome eles está no lugar dos dois.", {}),
    (3, "COMO SE SEPARA?", ["ARMAZÉM"], "ar-ma-zém", ["a-rma-zém", "arm-a-zém"],
     "Como se separa a palavra armazém em sílabas?",
     "Ar, ma, zém! O erre fica com o a.", {"falar_ops": False,
                                            "dica": ("Dica: fala bem devagar!", "FALA DEVAGAR!")}),
    (3, "QUAL TEM SEMPRE ACENTO?", ["Toda ___", "tem acento."], "Proparoxítona", ["Paroxítona", "Oxítona"],
     "Complete: toda o quê tem acento? Proparoxítona, paroxítona ou oxítona?",
     "Proparoxítona! Médico, lâmpada, árvore: toda proparoxítona tem acento.", {"falar_ops": False}),
    # ---------- MUITO DIFÍCIL ----------
    (4, TON, ["VETERINÁRIO"], "Paroxítona", ["Proparoxítona", "Oxítona"],
     "Agora a parte que reprova! Veterinário é oxítona, paroxítona ou proparoxítona?",
     "Paroxítona! Ve, te, ri, ná, rio: rio é uma sílaba só, então ná é a penúltima.",
     {"falar_ops": False, "aviso": "QUASE TODO MUNDO ERRA!", "suspense": True}),
    (4, "QUAL PRONOME ENTRA?", ["As ferramentas de", "Marina e Lucas =", "as ferramentas ___"], "deles",
     ["delas", "dele"],
     "Pra não repetir Marina e Lucas: as ferramentas o quê? Deles, delas ou dele?",
     "Deles! Menino e menina juntos fica deles.", {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (4, SIL, ["FOTOGRAFIA"], "5", ["4", "6"], "Quantas sílabas tem fotografia?",
     "Cinco! Fo, to, gra, fi, a.", {"aviso": "TEM PEGADINHA!"}),
    (4, "COMO SE ESCREVE?", ["Instrumento", "de cordas"], "Guitarra", ["Gitarra", "Guitara"],
     "Aquele instrumento de cordas do rock. Como se escreve?",
     "Guitarra! Com gê-u e dois erres.", {}),
    (4, VERBO, ["ANOITECER"], "Fenômeno", ["Estado", "Ação"],
     "Anoitecer é verbo de ação, de estado ou de fenômeno da natureza?",
     "Fenômeno da natureza! Ninguém faz a noite chegar.", {"falar_ops": False, "aviso": "DERRUBA MUITA GENTE!"}),
    (4, SIL, ["GENEALÓGICA"], "6", ["5", "7"],
     "Valendo a nota da prova! Lembra da árvore da Clara? Quantas sílabas tem genealógica?",
     "Seis! Ge, ne, a, ló, gi, ca. Se acertou essa, tirou dez na prova!",
     {"count": 10.0, "suspense": True, "final": True}),
]

FALA = {"1": "um", "4": "quatro", "3": "três", "5": "cinco", "6": "seis", "7": "sete", "2": "dois", "8": "oito"}


def main():
    rnd = random.Random(35)
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
