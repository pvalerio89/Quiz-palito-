"""Gera itens.json e copia as fotos do vídeo 46 "Revisão de inglês do 3º ano" (estilo mais humano, 2026-11-13).

44 perguntas próprias tiradas da folha de revisão de inglês (Grade 3 ESL) que o Patrick mandou em foto (2026-11-19):
verbos no presente (-s/-es), passado (-ed) e futuro (will), palavras de tempo (yesterday, tomorrow, every day),
partes da planta (flower, leaves, stem, roots), frutas e legumes em inglês e plural (-s, -es, -ies).
Do MÉDIO ao MUITO DIFÍCIL (pedido do Patrick: "do médio ao difícil"). Vídeo de 15 min pra cima.
Sem nome do aluno/escola; as fotos da folha NÃO vão para o vídeo nem para o repo.
Imagem de cada pergunta: foto real (Wikimedia Commons, reaproveitada do vídeo 12) para fruta/legume, desenho da planta
com seta (feito pelo build) ou cartão de caderno com a frase. Tudo vai para cartoes/ pelo build.
Uso: py -3 itens.py
"""
import json, os, random, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
V12 = os.path.join(os.path.dirname(HERE), "12-fruta-fotos-reais")
VERBO = "COMPLETE COM O VERBO:"
TEMPO = "QUE TEMPO VERBAL É ESSE?"
TEMPO_OPS = ["Presente", "Passado", "Futuro"]
FOTO = "COMO SE DIZ EM INGLÊS?"
PLANTA = "QUE PARTE DA PLANTA É ESSA?"
PARTE = "QUE PARTE DA PLANTA FAZ ISSO?"
PLURAL = "QUAL É O PLURAL?"
PAL = "QUAL PALAVRA COMPLETA?"
FV = "FRUIT OU VEGETABLE?"
ERRADA = "QUAL ESTÁ ERRADA?"
CERTA = "QUAL ESTÁ CERTA?"
SABIA_ES = "Verbo que termina em S, SH, CH, X ou O ganha E S com he, she e it: watches, washes, goes."
SABIA_IES = "Consoante + Y no fim: troca o Y por I E S. Strawberry vira strawberries. Mas vogal + Y só ganha S: plays."
SABIA_O = "Muitas palavras terminadas em O ganham E S no plural: tomatoes, potatoes, mangoes."
SABIA_PL = "Roots são as raízes, stem é o caule, leaves são as folhas e flower é a flor."


def t(*linhas):
    return {"cartao": list(linhas)}


# nível (2 médio, 3 difícil, 4 muito difícil), pergunta (topo), imagem, certa, [erradas], fala pergunta, fala resposta, extras
# imagem: {"cartao": [...]} | {"foto": "<arquivo do vídeo 12 sem .jpg>", "rotulo": ...} | {"planta": "flower"/...}
P = [
    # ---------- MÉDIO ----------
    (2, VERBO, t("Every morning,", "Lucas ______", "to school.", "(walk)"), "walks", ["walked", "will walk"],
     "Primeira, valendo! Every morning, Lucas... walk... to school. Qual a forma certa?",
     "Walks! Every morning é todo dia, então é presente. E com ele, he, ganha S.", {"falar_ops": False}),
    (2, FOTO, {"foto": "morango", "rotulo": "MORANGO"}, "Strawberry", ["Raspberry", "Cherry"],
     "Como se diz morango em inglês?", "Strawberry! Raspberry é framboesa e cherry é cereja.", {}),
    (2, PLANTA, {"planta": "flower"}, "Flower", ["Leaves", "Roots"],
     "A seta está apontando para qual parte da planta?", "Flower! A flor.", {}),
    (2, TEMPO, t("jumped"), "Passado", ["Presente", "Futuro"],
     "Jumped. Que tempo verbal é esse? Presente, passado ou futuro?",
     "Passado! Terminou com E D, é passado. Jumped é pulou.", {"falar_ops": False}),
    (2, PLURAL, t("one apple", "two ______"), "apples", ["applees", "apple's"],
     "One apple, two... qual é o plural de apple?", "Apples! A maioria das palavras só ganha S.", {"falar_ops": False}),
    (2, FOTO, {"foto": "cenoura", "rotulo": "CENOURA"}, "Carrot", ["Potato", "Onion"],
     "E cenoura? Como se diz em inglês?", "Carrot! Potato é batata e onion é cebola.", {}),
    (2, VERBO, t("Tomorrow, Dad", "______ dinner.", "(cook)"), "will cook", ["cooked", "cooks"],
     "Tomorrow, Dad... cook... dinner. Qual a forma certa?",
     "Will cook! Tomorrow é amanhã: futuro é will mais o verbo.", {"falar_ops": False}),
    (2, FV, {"foto": "brocolis", "rotulo": "BRÓCOLIS"}, "Vegetable", ["Fruit", "Flower"],
     "Brócolis é fruit ou vegetable?", "Vegetable! Fruit é fruta, vegetable é legume e verdura.", {"falar_ops": False}),
    (2, TEMPO, t("will visit"), "Futuro", ["Presente", "Passado"],
     "Will visit. Que tempo verbal é esse?", "Futuro! Will na frente do verbo é futuro: vai visitar.",
     {"falar_ops": False}),
    (2, FOTO, {"foto": "melancia", "rotulo": "MELANCIA"}, "Watermelon", ["Melon", "Pumpkin"],
     "Como se diz melancia em inglês?", "Watermelon! Melon é melão. Water melon: o melão de água!",
     {"aviso": "TEM PEGADINHA!"}),
    (2, PLANTA, {"planta": "roots"}, "Roots", ["Stem", "Leaves"],
     "E agora? A seta aponta para qual parte?", "Roots! As raízes, embaixo da terra.", {}),
    (2, VERBO, t("Last night, I", "______ my room.", "(clean)"), "cleaned", ["cleans", "will clean"],
     "Last night, I... clean... my room. Qual a forma certa?",
     "Cleaned! Last night é ontem à noite: passado, com E D.", {"falar_ops": False}),
    (2, FOTO, {"foto": "uva", "rotulo": "UVAS"}, "Grapes", ["Plums", "Cherries"],
     "Como se diz uvas em inglês?", "Grapes! Plums são ameixas.", {}),
    (2, PLURAL, t("one banana", "two ______"), "bananas", ["bananes", "bananies"],
     "One banana, two... qual é o plural?", "Bananas! Só ganha S.", {"falar_ops": False}),
    (2, PAL, t("______, we played", "in the park."), "Yesterday", ["Tomorrow", "Every day"],
     "Qual palavra completa a frase: blank, we played in the park?",
     "Yesterday! Played está no passado, então é ontem.", {"falar_ops": False,
     "dica": ("Dica: played termina com E D...", "ED = PASSADO")}),
    # ---------- DIFÍCIL ----------
    (3, VERBO, t("Leo ______ TV", "after school", "every day.", "(watch)"), "watches", ["watchs", "watched"],
     "Nível difícil, valendo! Leo... watch... TV after school every day. Como se escreve?",
     "Watches, com E S! Watch termina em C H, então ganha E S.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!", "suspense": True, "sabia": SABIA_ES}),
    (3, PLANTA, {"planta": "stem"}, "Stem", ["Leaves", "Roots"],
     "A seta está no meio da planta. Que parte é essa?", "Stem! O caule.", {"sabia": SABIA_PL}),
    (3, PLURAL, t("one tomato", "two ______"), "tomatoes", ["tomatos", "tomatoies"],
     "One tomato, two... como se escreve o plural?", "Tomatoes, com E S! Termina em O, ganha E S.",
     {"falar_ops": False, "sabia": SABIA_O}),
    (3, FOTO, {"foto": "alface", "rotulo": "ALFACE"}, "Lettuce", ["Cabbage", "Broccoli"],
     "Como se diz alface em inglês?", "Lettuce! Cabbage é repolho.", {"aviso": "QUASE TODO MUNDO ERRA!"}),
    (3, PAL, t("______, the children", "will dance at school."), "Tomorrow", ["Yesterday", "Last night"],
     "Qual palavra completa: blank, the children will dance at school?",
     "Tomorrow! Will dance é futuro, então é amanhã.", {"falar_ops": False}),
    (3, TEMPO, t("helps"), "Presente", ["Passado", "Futuro"],
     "Helps. Que tempo verbal é esse?", "Presente! O S no fim é do he, she e it no presente.", {"falar_ops": False}),
    (3, FOTO, {"foto": "cebola", "rotulo": "CEBOLA"}, "Onion", ["Garlic", "Potato"],
     "Como se diz cebola em inglês?", "Onion! Garlic é alho.", {}),
    (3, PLURAL, t("one strawberry", "two ______"), "strawberries", ["strawberrys", "strawberryes"],
     "One strawberry, two... como se escreve o plural?",
     "Strawberries! Termina em consoante mais Y: troca o Y por I E S.",
     {"falar_ops": False, "sabia": SABIA_IES, "suspense": True}),
    (3, VERBO, t("Sam ______ his", "hands every day.", "(wash)"), "washes", ["washs", "washed"],
     "Sam... wash... his hands every day. Como se escreve?", "Washes! Termina em S H, ganha E S.",
     {"falar_ops": False}),
    (3, PARTE, t("Pega a água", "e os nutrientes", "do solo."), "Roots", ["Leaves", "Flower"],
     "Que parte da planta pega a água e os nutrientes do solo?", "Roots! As raízes.", {}),
    (3, FOTO, {"foto": "batata", "rotulo": "BATATA"}, "Potato", ["Tomato", "Carrot"],
     "Como se diz batata em inglês?", "Potato! Cuidado: tomato é tomate.", {"aviso": "TEM PEGADINHA!"}),
    (3, VERBO, t("Yesterday, Dad", "______ the door.", "(open)"), "opened", ["openned", "opens"],
     "Yesterday, Dad... open... the door. Como se escreve?", "Opened, com um N só! Open mais E D.",
     {"falar_ops": False, "suspense": True}),
    (3, PLURAL, t("one potato", "two ______"), "potatoes", ["potatos", "potatoe"],
     "One potato, two... como se escreve o plural?", "Potatoes! Igual tomatoes: O mais E S.", {"falar_ops": False}),
    (3, FOTO, {"foto": "pepino", "rotulo": "PEPINO"}, "Cucumber", ["Pepper", "Zucchini"],
     "Como se diz pepino em inglês?", "Cucumber! Pepper é pimentão, e zucchini é abobrinha.",
     {"aviso": "DERRUBA MUITA GENTE!"}),
    (3, PARTE, t("Segura a planta", "em pé e leva", "a água."), "Stem", ["Roots", "Flower"],
     "Que parte segura a planta em pé e leva a água até as folhas?", "Stem! O caule.", {}),
    # ---------- MUITO DIFÍCIL ----------
    (4, PLURAL, t("one peach", "two ______"), "peaches", ["peachs", "peachies"],
     "Agora é o nível que derruba até adulto! One peach, two... como se escreve?",
     "Peaches! Termina em C H, ganha E S.", {"falar_ops": False, "suspense": True}),
    (4, ERRADA, t("Uma dessas", "está ERRADA!"), "two tomatos", ["two onions", "two grapes"],
     "Uma dessas está errada! Qual?", "Two tomatos está errado! O certo é tomatoes, com E S.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (4, VERBO, t("My brother ______", "soccer on", "Saturdays.", "(play)"), "plays", ["plaies", "played"],
     "My brother... play... soccer on Saturdays. Como se escreve?",
     "Plays! Vogal mais Y só ganha S. Nada de I E S.", {"falar_ops": False, "aviso": "QUASE TODO MUNDO ERRA!"}),
    (4, PLURAL, t("one cherry", "two ______"), "cherries", ["cherrys", "cherryes"],
     "One cherry, two... como se escreve?", "Cherries! Consoante mais Y: I E S.", {"falar_ops": False}),
    (4, PARTE, t("Faz o alimento", "da planta com", "a luz do Sol."), "Leaves", ["Roots", "Stem"],
     "Que parte faz o alimento da planta usando a luz do Sol?", "Leaves! As folhas.", {}),
    (4, VERBO, t("Next week, they", "______ the zoo.", "(visit)"), "will visit", ["visited", "visits"],
     "Next week, they... visit... the zoo. Qual a forma certa?", "Will visit! Next week é semana que vem: futuro.",
     {"falar_ops": False}),
    (4, FOTO, {"foto": "pimentao", "rotulo": "PIMENTÃO"}, "Pepper", ["Pumpkin", "Eggplant"],
     "Como se diz pimentão em inglês?", "Pepper! Pumpkin é abóbora e eggplant é berinjela.", {}),
    (4, PLURAL, t("one leaf", "two ______"), "leaves", ["leafs", "leafes"],
     "One leaf, uma folha. Two... qual é o plural?",
     "Leaves! O F vira V E S. É a mesma palavra das folhas da planta!",
     {"falar_ops": False, "aviso": "DERRUBA MUITA GENTE!", "suspense": True}),
    (4, CERTA, t("Tomorrow, we", "______ our teacher.", "(help)"), "will help", ["will helps", "will helped"],
     "Tomorrow, we... help... our teacher. Qual está certa?",
     "Will help! Depois do will, o verbo fica do jeito que é, sem S e sem E D.", {"falar_ops": False}),
    (4, FOTO, {"foto": "pessego", "rotulo": "PÊSSEGO"}, "Peach", ["Pear", "Plum"],
     "Como se diz pêssego em inglês?", "Peach! Pear é pera e plum é ameixa.", {}),
    (4, VERBO, t("Every day, Ana", "______ English.", "(study)"), "studies", ["studys", "studyes"],
     "Every day, Ana... study... English. Como se escreve?",
     "Studies! Consoante mais Y: troca por I E S, igual strawberries.", {"falar_ops": False}),
    (4, ERRADA, t("Uma dessas", "frases está", "ERRADA!"), "She watchs TV.", ["He plays soccer.", "It rains a lot."],
     "Uma dessas frases está errada! Qual?", "She watchs TV! O certo é watches, com E S.",
     {"falar_ops": False}),
    (4, CERTA, t("Eu gosto de", "comer bananas."), "I like to eat bananas.",
     ["I'm like to eat bananas.", "I likes to eat bananas."],
     "Como se diz: eu gosto de comer bananas? Qual está certa?",
     "I like to eat bananas! Não tem I'm, e com I o verbo não ganha S.",
     {"falar_ops": False, "aviso": "QUASE TODO MUNDO ERRA!", "suspense": True}),
    (4, "QUANTOS ESTÃO NO PASSADO?", t("plays • jumped", "will help • cleaned", "opened • walks"), "3", ["2", "4"],
     "Valendo a nota! Plays, jumped, will help, cleaned, opened e walks. Quantos estão no passado?",
     "Três! Jumped, cleaned e opened. Se acertou essa, tirou dez em inglês!",
     {"count": 12.0, "suspense": True, "final": True}),
]


def main():
    rnd = random.Random(46)
    pos = [0, 1, 2] * 15
    rnd.shuffle(pos)
    pos[0] = 0
    R, cred = [], {}
    c12 = json.load(open(os.path.join(V12, "creditos.json"), encoding="utf-8"))
    por_arq = {v["arquivo"]: (k, v) for k, v in c12.items()}
    os.makedirs(os.path.join(HERE, "fotos"), exist_ok=True)
    for n, (nivel, perg, img, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        if ex.get("falar_ops", True):
            fq = f"{fq} {ops[0]}, {ops[1]} ou {ops[2]}?"
        r = {"n": n, "nivel": nivel, "pergunta": perg, **img, "img": f"q{n}.png",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": fq, "fala_r": fr, "count": ex.get("count", 8.0)}
        if "foto" in img:
            arq = img["foto"] + ".jpg"
            shutil.copy2(os.path.join(V12, "fotos", arq), os.path.join(HERE, "fotos", arq))
            nome, c = por_arq[arq]
            cred[arq] = f"{nome} ({certa}): {c['autor']}, {c['lic']}, {c['file']}"
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo a nota... a resposta é..."
        R.append(r)
    for extra in ("maca", "banana", "laranja"):   # intro e miniatura
        arq = extra + ".jpg"
        shutil.copy2(os.path.join(V12, "fotos", arq), os.path.join(HERE, "fotos", arq))
        nome, c = por_arq[arq]
        cred[arq] = f"{nome}: {c['autor']}, {c['lic']}, {c['file']}"
    assert len(R) == 44
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"fotos": sorted(cred.values())}, open(os.path.join(HERE, "creditos.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], [sum(r["nivel"] == k for r in R) for k in (2, 3, 4)])


if __name__ == "__main__":
    main()
