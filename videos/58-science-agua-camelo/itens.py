"""Gera itens.json do vídeo 58 "Prova de Science do 3º ano: alimentação, água e o camelo" (estilo mais humano).

40 perguntas feitas SÓ com o conteúdo da Science Review Activity do 3º ano (3º trimestre) que o Patrick mandou
em 6 fotos (2026-11-26): o texto "Eating Well Every Day" (Tommy), água direta x água virtual, litros de água para
produzir cada alimento (maçã 70 L, batata 25 L, carne 15.000 L/kg, tomate 50 L, banana 160 L), atividades que
desperdiçam água, adaptações do camelo (corcovas, cílios, pés largos, pelo), verdadeiro/falso sobre camelos e
completar frases (energy, virtual, healthy, desert, direct, water). Nada de fora das folhas: só reformulado e
combinado (ex.: somar os litros de dois alimentos da folha). Palavras em inglês da folha aparecem nos cartões.
Do MÉDIO ao MUITO DIFÍCIL (3 níveis). Nunca nome de aluno ou escola.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
DV = ["Água direta", "Água virtual", "Nenhuma das duas"]
VF = ["Verdade", "Mentira"]
# nível, pergunta (topo), cartão (linhas), certa, [erradas], fala da pergunta, fala da resposta, extras
P = [
    # ---------- MÉDIO ----------
    (2, "O QUE ELE COME?", ["Café da manhã", "do Tommy: banana e..."], "Pão integral", ["Bolo de chocolate", "Bala"],
     "O Tommy adora comer de tudo. No café da manhã, ele come uma banana e o quê?",
     "Pão integral! Banana e pão integral, um café da manhã saudável.", {"img": "pao"}),
    (2, "DIRETA OU VIRTUAL?", ["Maria toma banho", "antes da escola"], "Água direta", DV[1:],
     "A Maria toma banho antes de ir pra escola. Isso é água direta ou água virtual?",
     "Água direta! É a água que a gente usa nas atividades do dia a dia.", {"img": "chuveiro", "falar_ops": False}),
    (2, "O QUE ELE BEBE?", ["Durante o dia,", "Tommy bebe..."], "Água", ["Refrigerante", "Nada"],
     "E durante o dia, o que o Tommy bebe pra ajudar o corpo dele?",
     "Água! Ele bebe água durante o dia.", {}),
    (2, "ONDE VIVEM?", ["Camels live in", "the ________"], "Deserto (desert)", ["Fazenda (farm)", "Supermercado"],
     "Complete a frase: os camelos vivem no... Deserto, fazenda ou supermercado?",
     "No deserto! Desert, em inglês.", {"img": "deserto", "falar_ops": False}),
    (2, "SÓ DE VEZ EM QUANDO!", ["O que o Tommy", "NÃO deve comer", "todo dia?"], "Doce e refrigerante",
     ["Arroz e feijão", "Banana e pão"],
     "O Tommy ama doce e refrigerante também. Mas o que ele NÃO deve comer todo dia?",
     "Doce e refrigerante! Candy and soda, só de vez em quando.", {"img": "doces"}),
    (2, "DIRETA OU VIRTUAL?", ["Pedro bebe", "um copo de água"], "Água direta", DV[1:],
     "O Pedro bebe um copo de água. Água direta ou água virtual?",
     "Água direta! Ele usou a água ali, na hora.", {"img": "copo", "falar_ops": False}),
    (2, "QUAL USA MAIS ÁGUA?", ["Para ser produzido,", "quem gasta", "MAIS água?"], "Carne (beef)", ["Maçã", "Batata"],
     "Cada alimento precisa de uma quantidade de água pra ser produzido. Qual desses gasta MAIS água? Carne, maçã ou batata?",
     "A carne! Beef: quinze mil litros por quilo.", {"img": "carne", "falar_ops": False}),
    (2, "PRA QUE SERVEM?", ["Cílios longos", "(long eyelashes)", "do camelo"], "Proteger os olhos da areia",
     ["Andar na areia fofa", "Guardar gordura"],
     "Pra que servem os cílios longos do camelo?",
     "Proteger os olhos da areia! Long eyelashes.", {"img": "camelorosto"}),
    (2, "VERDADE OU MENTIRA?", ["\"Camelos nunca", "precisam de água\""], "Mentira", ["Verdade"],
     "Verdade ou mentira: os camelos nunca precisam de água?",
     "Mentira! Camelo também precisa de água.", {"img": "dromedario", "aviso": "PEGADINHA!", "falar_ops": False}),
    (2, "DIRETA OU VIRTUAL?", ["Uma família", "lava a louça"], "Água direta", DV[1:],
     "Uma família usa água pra lavar a louça. Água direta ou virtual?",
     "Água direta! Lavar a louça é atividade do dia a dia.", {"img": "louca", "falar_ops": False}),
    (2, "COMPLETE!", ["Fruits and vegetables", "are examples of", "________ foods"], "Saudáveis (healthy)",
     ["Virtuais (virtual)", "Do deserto (desert)"],
     "Frutas e verduras são exemplos de alimentos o quê?",
     "Saudáveis! Healthy foods.", {"img": "verduras"}),
    (2, "QUEM DESPERDIÇA MAIS?", ["Qual gasta", "MAIS água?"], "Lavar o carro com mangueira",
     ["Regar com regador", "Beber um copo de água"],
     "Qual dessas atividades gasta MAIS água?",
     "Lavar o carro com a mangueira! A água sai sem parar.", {"img": "mangueira"}),
    # ---------- DIFÍCIL ----------
    (3, "DIRETA OU VIRTUAL?", ["O fazendeiro usa água", "para plantar tomates"], "Água virtual", [DV[0], DV[2]],
     "Um fazendeiro usa água pra plantar tomates. Água direta ou virtual?",
     "Água virtual! É água usada pra produzir um alimento.", {"img": "tomateiro", "falar_ops": False,
                                                                 "aviso": "TEM PEGADINHA!"}),
    (3, "E O ALMOÇO?", ["Almoço do Tommy:", "arroz, feijão,", "verduras e às vezes..."], "Carne",
     ["Chocolate", "Bala"],
     "No almoço, o Tommy come arroz, feijão, verduras e, às vezes, o quê?",
     "Carne! Arroz, feijão, verduras e às vezes carne.", {"img": "arrozfeijao"}),
    (3, "QUAL USA MENOS ÁGUA?", ["Para ser produzido,", "quem gasta", "MENOS água?"], "Batata", ["Tomate", "Maçã"],
     "E qual desses gasta MENOS água pra ser produzido?",
     "A batata! Só vinte e cinco litros.", {"img": "batata"}),
    (3, "DIRETA OU VIRTUAL?", ["Uma fábrica usa água", "para fazer", "uma camiseta"], "Água virtual", [DV[0], DV[2]],
     "Uma fábrica usa água pra fazer uma camiseta. Água direta ou virtual?",
     "Água virtual! Também vale pra produtos, não só comida.", {"img": "camiseta", "falar_ops": False}),
    (3, "QUANTOS LITROS?", ["Para produzir", "uma maçã (apple)"], "70 litros", ["25 litros", "160 litros"],
     "Quantos litros de água são usados pra produzir uma maçã?",
     "Setenta litros!", {"img": "maca"}),
    (3, "PRA QUE SERVEM?", ["Corcovas", "(humps)", "do camelo"], "Guardar gordura que dá energia",
     ["Proteger os olhos", "Andar na areia fofa"],
     "E as corcovas do camelo, servem pra quê?",
     "Guardam gordura, que dá energia pro camelo!", {"img": "bactriano"}),
    (3, "O QUE TEM DENTRO?", ["O camelo guarda", "na corcova..."], "Gordura", ["Água", "Areia"],
     "E o que o camelo guarda dentro da corcova?",
     "Gordura! Muita gente acha que é água, mas a folha diz: camels store fat in their humps.",
     {"img": "camelo", "aviso": "DERRUBA MUITA GENTE!", "suspense": True}),
    (3, "DIRETA OU VIRTUAL?", ["A água usada para", "produzir o chocolate", "do supermercado"], "Água virtual",
     [DV[0], DV[2]],
     "A água usada pra produzir o chocolate que a gente compra no supermercado é direta ou virtual?",
     "Virtual! Você nem vê essa água, mas ela foi usada.", {"img": "chocolate", "falar_ops": False}),
    (3, "PRA QUE SERVEM?", ["Pés grandes", "e largos", "(big, wide feet)"], "Andar na areia sem afundar",
     ["Guardar gordura", "Proteger do sol"],
     "Pra que servem os pés grandes e largos do camelo?",
     "Pra andar na areia fofa sem afundar!", {"img": "dromedario2"}),
    (3, "QUANTOS LITROS?", ["Para produzir", "um tomate (tomato)"], "50 litros", ["70 litros", "25 litros"],
     "Quantos litros de água pra produzir um tomate?",
     "Cinquenta litros!", {"img": "tomate"}),
    (3, "O QUE É?", ["Direct water", "(água direta) é..."], "Água do dia a dia",
     ["Água para produzir", "Água do deserto"],
     "O que é água direta? Água que a gente usa no dia a dia, água usada pra produzir coisas, ou água do deserto?",
     "A água que a gente usa nas atividades do dia a dia!", {"falar_ops": False}),
    (3, "QUEM DESPERDIÇA MAIS?", ["E agora? Qual", "desperdiça MAIS água?"], "Lavar a calçada com mangueira",
     ["Regar com regador", "Consertar a torneira"],
     "Qual dessas gasta MAIS água?",
     "Lavar a calçada com a mangueira! É um dos maiores desperdícios.", {}),
    (3, "PRA QUE SERVE?", ["O pelo", "(fur)", "do camelo"], "Proteger do sol e do frio da noite",
     ["Guardar gordura", "Proteger os olhos"],
     "E o pelo do camelo, serve pra quê?",
     "Protege do sol quente e também das noites frias do deserto!",
     {"img": "bactriano2", "aviso": "TEM PEGADINHA!", "suspense": True}),
    (3, "VERDADE OU MENTIRA?", ["\"Camelos não", "sobrevivem em", "lugares quentes\""], "Mentira", ["Verdade"],
     "Verdade ou mentira: os camelos não sobrevivem em lugares quentes?",
     "Mentira! Eles vivem no deserto, que é quente.", {"img": "deserto2", "falar_ops": False}),
    (3, "QUANTOS LITROS?", ["Para produzir", "uma banana"], "160 litros", ["50 litros", "70 litros"],
     "Quantos litros de água pra produzir uma banana?",
     "Cento e sessenta litros!", {"img": "banana"}),
    (3, "O QUE É?", ["Virtual water", "(água virtual) é..."], "Água para produzir",
     ["Água do dia a dia", "Água de beber"],
     "E água virtual, o que é?",
     "A água usada pra produzir alimentos e outros produtos!", {}),
    (3, "COMPLETE!", ["Healthy foods", "give our bodies", "________"], "Energia (energy)",
     ["Água virtual", "Deserto"],
     "Complete: alimentos saudáveis dão ao nosso corpo...",
     "Energia! Energy.", {}),
    # ---------- MUITO DIFÍCIL ----------
    (4, "QUANTOS LITROS?", ["Carne (beef):", "litros por quilo"], "15.000 litros", ["1.500 litros", "150 litros"],
     "Quantos litros de água são usados pra produzir um quilo de carne?",
     "Quinze mil litros por quilo! Muito mais que todos os outros.", {"img": "carne2", "aviso": "QUASE TODO MUNDO ERRA!",
                                                                     "falar_ops": False}),
    (4, "QUAL NÃO?", ["Qual NÃO usa", "menos de 200 litros?"], "Carne", ["Banana", "Maçã"],
     "Qual desses alimentos NÃO usa menos de duzentos litros de água?",
     "A carne! Banana, maçã, tomate e batata ficam abaixo de duzentos litros.", {"aviso": "PEGADINHA!"}),
    (4, "PRA QUE SERVE?", ["Healthy foods", "help Tommy..."], "Crescer e ficar forte",
     ["Comer mais doce", "Dormir na aula"],
     "Segundo o texto, a comida saudável ajuda o corpo do Tommy a fazer o quê?",
     "Crescer, ficar forte e ter energia pra jogar futebol com os amigos!", {}),
    (4, "O QUE SIGNIFICA?", ["\"Humps\""], "Corcovas", ["Cílios", "Pés largos"],
     "Em inglês, o que significa humps?",
     "Corcovas! Humps são as corcovas do camelo.", {}),
    (4, "QUAL A ORDEM?", ["Do que gasta MENOS", "para o que gasta MAIS"], "Batata, tomate, maçã",
     ["Tomate, batata, maçã", "Maçã, tomate, batata"],
     "Qual está na ordem certa, do que gasta menos água pro que gasta mais?",
     "Batata, tomate e maçã! Vinte e cinco, cinquenta e setenta litros.", {"suspense": True}),
    (4, "O QUE SIGNIFICA?", ["\"Long eyelashes\""], "Cílios longos", ["Pelo grosso", "Corcovas"],
     "E long eyelashes, o que significa?",
     "Cílios longos! Protegem os olhos da areia.", {}),
    (4, "QUANTO A MAIS?", ["Banana: 160 L", "Maçã: 70 L", "Diferença?"], "90 litros", ["80 litros", "100 litros"],
     "A banana usa cento e sessenta litros de água. A maçã, setenta. Quantos litros a banana usa a mais?",
     "Noventa litros! Cento e sessenta menos setenta.", {"falar_ops": False}),
    (4, "COMPLETE!", ["We need ________", "to survive"], "Água (water)", ["Refrigerante", "Doce"],
     "Complete: nós precisamos de... pra sobreviver.",
     "Água! We need water to survive.", {"img": "torneira"}),
    (4, "QUAL ESTÁ CERTA?", ["Qual frase sobre", "camelos é", "VERDADEIRA?"], "Têm pés largos pra areia",
     ["Nunca precisam de água", "Não vivem no calor"],
     "Qual dessas frases sobre camelos é verdadeira?",
     "Camelos têm pés largos pra andar na areia! As outras duas são mentira.", {}),
    (4, "QUANTOS LITROS?", ["Tommy comeu", "1 maçã + 1 banana", "Total de água?"], "230 litros",
     ["210 litros", "330 litros"],
     "Valendo a nota da prova! O Tommy comeu uma maçã e uma banana. Quantos litros de água foram usados pra produzir as duas?",
     "Duzentos e trinta litros! Setenta da maçã mais cento e sessenta da banana. Se acertou essa, tirou dez em science!",
     {"count": 12.0, "suspense": True, "final": True}),
]


def main():
    rnd = random.Random(58)
    pos = [0, 1, 2] * 15
    rnd.shuffle(pos)
    R = []
    for n, (nivel, perg, cartao, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        if len(ops) == 1:   # verdade ou mentira: 2 opções, ordem fixa
            ops = VF[:]
            c = ops.index(certa)
        elif certa in DV:   # direta/virtual: ordem fixa (direta, virtual, nenhuma)
            ops = DV[:]
            c = ops.index(certa)
        else:
            c = pos[n - 1]
            ops.insert(c, certa)
        assert len(set(ops)) == len(ops) and certa in ops, (n, ops)
        if ex.get("falar_ops", True):
            fq = f"{fq} {', '.join(ops[:-1])} ou {ops[-1]}?"
        r = {"n": n, "nivel": nivel, "pergunta": perg, "cartao": cartao, "foto": f"q{n}.png",
             "opcoes": ops, "certa": c, "fala_q": fq, "fala_r": fr, "count": ex.get("count", 8.0)}
        if "img" in ex:
            r["img"] = ex["img"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo a nota... a resposta é..."
        R.append(r)
    assert len({tuple(r["cartao"]) for r in R}) == len(R), "cartão repetido"
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], [sum(r["nivel"] == k for r in R) for k in (2, 3, 4)],
          sorted({r["img"] for r in R if "img" in r}))


if __name__ == "__main__":
    main()
