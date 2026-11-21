"""Gera itens.json e copia as fotos do vídeo 49 "Comida em inglês: Food Rainbow" (estilo mais humano, 2026-11-13).

44 perguntas próprias tiradas da lição de inglês que o Patrick mandou em foto (2026-11-19): Mizzou Grade 3 ELA,
Lesson 5-3 "Eating Plants" (How are plants healthy for you?): vocabulário (healthy, nutrition, vitamin, rainbow),
legumes e verduras em inglês com singular/plural, Food Rainbow (cores e nutrientes: lycopene, lutein, carotenoids,
anthocyanins, anthoxanthins; laranja = vitamina C).
Do MÉDIO ao MUITO DIFÍCIL (pedido do Patrick). Vídeo de 15 min pra cima. As fotos do livro NÃO vão para o vídeo nem
para o repo: as fotos são reais da Wikimedia Commons, reaproveitadas do vídeo 12.
Não repete as perguntas do vídeo 46 (revisão de inglês): nada de morango, cenoura, alface, cebola, batata, pepino,
pimentão, pêssego, uva, melancia como foto; nada de tomatoes/potatoes/cherries.
Uso: py -3 itens.py
"""
import json, os, random, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
V12 = os.path.join(os.path.dirname(HERE), "12-fruta-fotos-reais")
FOTO = "COMO SE DIZ EM INGLÊS?"
COR = "QUAL COR NO FOOD RAINBOW?"
NUT = "ESSE NUTRIENTE É DE QUAL COR?"
PLURAL = "QUAL É O PLURAL?"
PAL = "QUAL PALAVRA COMPLETA?"
SIG = "O QUE SIGNIFICA?"
ERRADA = "QUAL ESTÁ ERRADA?"
CERTA = "QUAL ESTÁ CERTA?"
SABIA_RB = "O Food Rainbow tem 5 grupos: red, orange e yellow, green, blue e purple, e white. Coma um de cada!"
SABIA_ES = "Palavra que termina em S, SH, CH ou X ganha E S no plural: radishes, squashes, boxes."
SABIA_BR = "Na lição, broccoli, asparagus e spinach aparecem sem plural: a gente fala some broccoli."
SABIA_W = "No grupo white estão banana, couve-flor, alho, gengibre, cogumelo, cebola, batata e nabo."


def t(*linhas):
    return {"cartao": list(linhas)}


def f(arq, rotulo):
    return {"foto": arq, "rotulo": rotulo}


# nível (2 médio, 3 difícil, 4 muito difícil), pergunta (topo), imagem, certa, [erradas], fala pergunta, fala resposta, extras
P = [
    # ---------- MÉDIO ----------
    (2, FOTO, f("milho", "MILHO"), "Corn", ["Carrot", "Pea"],
     "Primeira, valendo! Como se diz milho em inglês?", "Corn! Carrot é cenoura e pea é ervilha.", {}),
    (2, SIG, t("healthy"), "Saudável", ["Pesado", "Feliz"],
     "Healthy. O que essa palavra significa?", "Saudável! Healthy é o que faz bem pra você: comida e hábitos bons.", {}),
    (2, COR, f("beterraba", "BEETS"), "Red", ["Green", "White"],
     "Beets, a beterraba. No arco-íris da comida, o Food Rainbow, ela fica em qual cor?",
     "Red! A beterraba é do grupo vermelho.", {"sabia": SABIA_RB}),
    (2, FOTO, f("ervilha", "ERVILHAS"), "Peas", ["Beans", "Nuts"],
     "Como se diz ervilhas em inglês?", "Peas! Uma ervilha é one pea, várias são peas.", {}),
    (2, PLURAL, t("one cucumber", "two ______"), "cucumbers", ["cucumberes", "cucumber's"],
     "One cucumber, two... qual é o plural?", "Cucumbers! Só ganha S, sem apóstrofo.", {"falar_ops": False}),
    (2, SIG, t("rainbow"), "Arco-íris", ["Chuva", "Nuvem"],
     "Rainbow. O que significa?", "Arco-íris! Um arco de luz colorida no céu. Rain é chuva, bow é arco.", {}),
    (2, FOTO, f("abobora", "ABÓBORA"), "Pumpkin", ["Melon", "Orange"],
     "Como se diz abóbora em inglês?", "Pumpkin! Melon é melão e orange é laranja.", {}),
    (2, COR, f("mirtilo", "BLUEBERRIES"), "Blue/Purple", ["Green", "Red"],
     "Blueberries, os mirtilos. Qual é a cor deles no Food Rainbow?", "Blue e purple! Azul e roxo, no mesmo grupo.",
     {}),
    (2, PAL, t("Carrots ______", "good for you."), "are", ["is", "am"],
     "Carrots... blank... good for you. Qual palavra completa?",
     "Are! Carrots é plural, mais de uma cenoura, então é are.", {"falar_ops": False}),
    (2, FOTO, f("vagem", "VAGENS"), "Green beans", ["Green peas", "Green peppers"],
     "Como se dizem as vagens em inglês?", "Green beans! Feijão verde. Green peppers são pimentões verdes.",
     {"aviso": "TEM PEGADINHA!"}),
    (2, COR, f("couve-flor", "CAULIFLOWER"), "White", ["Green", "Orange/Yellow"],
     "Cauliflower, a couve-flor. Fica em qual cor do Food Rainbow?", "White! O grupo branco.", {}),
    (2, "COMO SE DIZ EM INGLÊS?", t("ROXO"), "Purple", ["Pink", "Brown"],
     "Como se diz roxo em inglês?", "Purple! Pink é rosa e brown é marrom.", {}),
    (2, "QUAL É HEALTHY?", t("Qual faz", "bem pra você?"), "Spinach", ["Candy", "Soda"],
     "Qual desses é healthy, faz bem pra você?", "Spinach, o espinafre! Candy é bala e soda é refrigerante.", {}),
    (2, FOTO, f("berinjela", "BERINJELA"), "Eggplant", ["Plum", "Pepper"],
     "Como se diz berinjela em inglês?", "Eggplant! Planta ovo, porque tem uma berinjela branquinha que parece um ovo!",
     {}),
    (2, "DE ONDE VÊM?", t("Vegetables", "come from..."), "Plants", ["Animals", "Rocks"],
     "Vegetables come from... os legumes e verduras vêm de onde?",
     "Plants! Vegetable é um tipo de comida que vem das plantas.", {"falar_ops": False,
     "dica": ("Dica: o nome da lição é Eating Plants...", "EATING PLANTS")}),
    # ---------- DIFÍCIL ----------
    (3, PLURAL, t("one radish", "two ______"), "radishes", ["radishs", "radishies"],
     "Nível difícil, valendo! One radish, um rabanete. Two... como se escreve?",
     "Radishes, com E S! Termina em S H, então ganha E S.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!", "suspense": True, "sabia": SABIA_ES}),
    (3, FOTO, f("salsao", "SALSÃO"), "Celery", ["Lettuce", "Leek"],
     "Como se diz salsão, o aipo, em inglês?", "Celery! Lettuce é alface e leek é alho-poró.",
     {"aviso": "QUASE TODO MUNDO ERRA!"}),
    (3, COR, f("banana", "BANANA"), "White", ["Orange/Yellow", "Green"],
     "Banana! Ela fica em qual cor do Food Rainbow?",
     "White! Pegadinha: a casca é amarela, mas por dentro ela é branca. Na lição, banana está no grupo branco.",
     {"aviso": "TEM PEGADINHA!", "suspense": True, "sabia": SABIA_W}),
    (3, SIG, t("nutrition"), "Comer e usar os nutrientes", ["Fazer exercício", "Dormir bem"],
     "Nutrition. O que significa?", "Comer e usar os nutrientes! É o jeito que o corpo usa a comida.", {}),
    (3, PLURAL, t("one squash", "two ______"), "squashes", ["squashs", "squash's"],
     "One squash, uma abóbora menina. Two... como se escreve?", "Squashes! S H no fim: E S.", {"falar_ops": False}),
    (3, NUT, t("LUTEIN", "deixa os olhos", "saudáveis"), "Green", ["Red", "White"],
     "A lutein, a luteína, ajuda a deixar os olhos saudáveis. Ela está nos alimentos de qual cor?",
     "Green! Kiwi, espinafre, ervilha e brócolis.", {}),
    (3, FOTO, f("rabanete", "RABANETE"), "Radish", ["Beet", "Turnip"],
     "Como se diz rabanete em inglês?", "Radish! Beet é beterraba e turnip é nabo.", {}),
    (3, COR, f("kiwi", "KIWI"), "Green", ["Orange/Yellow", "White"],
     "Kiwi. Fica em qual cor do Food Rainbow?",
     "Green! Por fora é marrom, mas por dentro é verdinho.", {"aviso": "TEM PEGADINHA!"}),
    (3, FOTO, f("couve-de-bruxelas", "COUVE-DE-BRUXELAS"), "Brussels sprouts", ["Cabbage", "Broccoli"],
     "Como se diz couve-de-bruxelas em inglês?", "Brussels sprouts! Os brotos de Bruxelas. Cabbage é repolho.", {}),
    (3, CERTA, t("Como se escreve", "brócolis", "em inglês?"), "broccoli", ["brocoli", "brocolli"],
     "Como se escreve brócolis em inglês? Qual está certa?", "Broccoli! Dois C e um L só.",
     {"falar_ops": False, "aviso": "DERRUBA MUITA GENTE!", "suspense": True}),
    (3, "QUAL VITAMINA?", f("laranja", "ORANGE"), "Vitamin C", ["Vitamin A", "Vitamin K"],
     "A laranja, orange, é rica em qual vitamina?",
     "Vitamin C! E a lição avisa: laranja não é fonte de vitamina A, mas tem muita vitamina C.",
     {"aviso": "TEM PEGADINHA!"}),
    (3, COR, f("cogumelo", "MUSHROOMS"), "White", ["Green", "Blue/Purple"],
     "Mushrooms, os cogumelos. Qual é a cor deles no Food Rainbow?", "White! Grupo branco.", {}),
    (3, FOTO, f("abobrinha", "ABOBRINHA"), "Zucchini", ["Cucumber", "Pumpkin"],
     "Como se diz abobrinha em inglês?", "Zucchini! Cucumber é pepino, parece mas não é.",
     {"aviso": "DERRUBA MUITA GENTE!"}),
    (3, PAL, t("Spinach ______", "healthy."), "is", ["are", "am"],
     "Spinach... blank... healthy. Qual palavra completa?",
     "Is! Spinach, o espinafre, não tem plural: usa is, igual a broccoli is green.", {"falar_ops": False}),
    # ---------- MUITO DIFÍCIL ----------
    (4, NUT, t("LYCOPENE", "tomate e", "melancia têm"), "Red", ["Orange/Yellow", "Green"],
     "Agora é o nível que derruba até adulto! O lycopene, o licopeno, está no tomate e na melancia. É do grupo de qual cor?",
     "Red! O licopeno é do grupo vermelho.", {"suspense": True}),
    (4, FOTO, f("alcachofra", "ALCACHOFRA"), "Artichoke", ["Asparagus", "Cabbage"],
     "Como se diz alcachofra em inglês?", "Artichoke! Asparagus é aspargo.", {}),
    (4, PLURAL, t("one green bean", "two ______"), "green beans", ["greens bean", "greens beans"],
     "One green bean, uma vagem. Two... qual é o plural?",
     "Green beans! Só o bean ganha S. Green é cor, e cor nunca ganha S em inglês.",
     {"falar_ops": False, "aviso": "QUASE TODO MUNDO ERRA!", "suspense": True}),
    (4, COR, f("alho", "GARLIC"), "White", ["Green", "Orange/Yellow"],
     "Garlic, o alho. Fica em qual cor do Food Rainbow?", "White! O alho é do grupo branco.", {}),
    (4, NUT, t("ANTHOCYANINS", "protegem a", "memória"), "Blue/Purple", ["Green", "White"],
     "As anthocyanins, as antocianinas, ajudam a proteger a memória. Estão nos alimentos de qual cor?",
     "Blue e purple! Mirtilo, berinjela, ameixa e uva roxa.", {}),
    (4, ERRADA, t("Uma dessas", "está ERRADA!"), "two squashs", ["two peas", "two radishes"],
     "Uma dessas está errada! Qual?", "Two squashs está errado! O certo é squashes, com E S.",
     {"falar_ops": False}),
    (4, FOTO, f("roma", "ROMÃ"), "Pomegranate", ["Grapefruit", "Fig"],
     "Como se diz romã em inglês?", "Pomegranate! Grapefruit é toranja e fig é figo.",
     {"aviso": "DERRUBA MUITA GENTE!"}),
    (4, NUT, t("CAROTENOIDS", "dão a", "vitamina A"), "Orange/Yellow", ["Blue/Purple", "White"],
     "Os carotenoids, os carotenoides, dão a vitamina A e ajudam o sistema imune. São de qual cor?",
     "Orange e yellow! Cenoura, abóbora, manga e batata-doce.", {}),
    (4, FOTO, f("aspargo", "ASPARGOS"), "Asparagus", ["Celery", "Green beans"],
     "Como se diz aspargo em inglês?", "Asparagus! E é a mesma palavra pra um ou vários.", {"sabia": SABIA_BR}),
    (4, "QUANTAS CORES?", t("FOOD RAINBOW", "Quantos grupos", "de cor?"), "5", ["7", "4"],
     "O arco-íris do céu tem sete cores. E o Food Rainbow da lição? Quantos grupos de cor ele tem?",
     "Cinco! Red, orange e yellow, green, blue e purple, e white.", {"falar_ops": False, "aviso": "TEM PEGADINHA!",
     "suspense": True}),
    (4, CERTA, t("Qual frase", "está certa?"), "These carrots are healthy.",
     ["This carrots is healthy.", "These carrots is healthy."],
     "Qual dessas frases está certa?", "These carrots are healthy! Carrots é plural: these e are.",
     {"falar_ops": False}),
    (4, COR, f("nabo", "TURNIPS"), "White", ["Blue/Purple", "Red"],
     "Turnips, os nabos. Ficam em qual cor do Food Rainbow?",
     "White! Tem um pouco de roxo em cima, mas na lição o nabo está no grupo branco.", {"aviso": "TEM PEGADINHA!"}),
    (4, "QUAL É O CONTRÁRIO?", t("healthy", "↔", "?"), "unhealthy", ["unhappy", "healthier"],
     "Qual é o contrário de healthy?", "Unhealthy! U N na frente faz o contrário: o que não faz bem.",
     {"falar_ops": False}),
    (4, "QUAL NÃO TEM PLURAL?", t("Na lição, uma", "dessas fica igual", "no plural!"), "broccoli", ["carrot", "radish"],
     "Na lição, uma dessas palavras não muda no plural. Qual?",
     "Broccoli! Carrot vira carrots e radish vira radishes, mas broccoli fica broccoli.",
     {"falar_ops": False}),
    (4, "QUANTOS SÃO WHITE?", t("banana • garlic", "kiwi • onion", "corn • mushroom"), "4", ["3", "5"],
     "Valendo a nota! Banana, garlic, kiwi, onion, corn e mushroom. Quantos são do grupo white?",
     "Quatro! Banana, garlic, onion e mushroom. Kiwi é green e corn é yellow. Se acertou, tirou dez!",
     {"count": 12.0, "suspense": True, "final": True}),
]


def main():
    rnd = random.Random(49)
    pos = [0, 1, 2] * 15
    rnd.shuffle(pos)
    pos[0] = 1
    R, cred = [], {}
    c12 = json.load(open(os.path.join(V12, "creditos.json"), encoding="utf-8"))
    por_arq = {v["arquivo"]: (k, v) for k, v in c12.items()}
    os.makedirs(os.path.join(HERE, "fotos"), exist_ok=True)
    for n, (nivel, perg, img, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        if ex.get("falar_ops", True):
            fala = [o.replace("/", " ou ") for o in ops]
            fq = f"{fq} {fala[0]}, {fala[1]}, ou {fala[2]}?"
        r = {"n": n, "nivel": nivel, "pergunta": perg, **img, "img": f"q{n}.png",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": fq, "fala_r": fr, "count": ex.get("count", 8.0)}
        if "foto" in img:
            arq = img["foto"] + ".jpg"
            shutil.copy2(os.path.join(V12, "fotos", arq), os.path.join(HERE, "fotos", arq))
            nome, c = por_arq[arq]
            cred[arq] = f"{nome}: {c['autor']}, {c['lic']}, {c['file']}"
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo a nota... a resposta é..."
        R.append(r)
    for extra in ("tomate", "brocolis", "milho", "mirtilo", "beterraba"):   # intro e miniatura
        arq = extra + ".jpg"
        shutil.copy2(os.path.join(V12, "fotos", arq), os.path.join(HERE, "fotos", arq))
        nome, c = por_arq[arq]
        cred[arq] = f"{nome}: {c['autor']}, {c['lic']}, {c['file']}"
    assert len(R) == 44, len(R)
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"fotos": sorted(cred.values())}, open(os.path.join(HERE, "creditos.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], [sum(r["nivel"] == k for r in R) for k in (2, 3, 4)])


if __name__ == "__main__":
    main()
