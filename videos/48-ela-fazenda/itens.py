"""Gera itens.json e junta as fotos do vídeo 48 "Inglês do 3º ano: a fazenda" (estilo mais humano, 2026-11-13).

44 perguntas próprias tiradas da lição "Places Where Plants Grow" (ELA, 3º ano, unidade 5, lição 5-2) que o Patrick
mandou em foto (2026-11-19): animais da fazenda em inglês e o plural deles (sheep, geese, cattle, turkeys), de onde vêm
os produtos (wool sweater, eggs, milk, socks, jam, sugar, orange juice), farmers market, nouns de pessoa ou coisa,
nouns e pronouns, maiúscula e pontuação, farm/grow/live/garden. Do MÉDIO ao MUITO DIFÍCIL ("do médio ao difícil").
Vídeo de 15 min pra cima. As fotos do livro NÃO vão para o vídeo nem para o repo: só fotos Wikimedia Commons
(reaproveitadas dos vídeos 12, 13 e 36, e novas em wiki/ pelo workflow Fotos Wikimedia).
Uso: py -3 itens.py
"""
import json, os, random, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
ORIGEM = {"12": "12-fruta-fotos-reais", "13": "13-animal-pela-foto", "36": "36-brasil-x-portugal",
          "14": "14-tudo-amarelo", "w": "48-ela-fazenda/wiki"}
NOME = "COMO SE DIZ EM INGLÊS?"
PLURAL = "QUAL É O PLURAL?"
VEM = "DE ONDE VEM?"
PT = "PERSON OU THING?"
PRON = "QUAL É O PRONOUN?"
COMPL = "QUAL PALAVRA COMPLETA?"
CERTA = "QUAL ESTÁ CERTA?"
TRAD = "O QUE SIGNIFICA?"
PONT = "QUAL SINAL VAI NO FIM?"
PONT_OPS = ["? (interrogação)", ". (ponto final)", ", (vírgula)"]
PEG = "TEM PEGADINHA!"


def t(*linhas):
    return {"cartao": list(linhas)}


def f(foto, rotulo=None):
    return {"foto": foto, **({"rotulo": rotulo} if rotulo else {})}


# nível (2 médio, 3 difícil, 4 muito difícil), pergunta (topo), imagem, certa, [erradas], fala pergunta, fala resposta, extras
P = [
    # ---------- MÉDIO ----------
    (2, NOME, f("13:porco"), "Pig", ["Cow", "Horse"],
     "Valendo! Como se diz porco em inglês?",
     "Pig! Começou tranquilo, né?", {"count": 6.0}),
    (2, NOME, f("13:ovelha"), "Sheep", ["Goat", "Llama"],
     "E a ovelha? Como é em inglês?",
     "Sheep! Guarda essa palavra, que ela vai voltar pra te pegar.", {"count": 6.0}),
    (2, NOME, f("13:burro"), "Donkey", ["Horse", "Monkey"],
     "E esse bichinho aqui?",
     "Donkey, o burro! Horse é o cavalo, e monkey é o macaco.", {}),
    (2, PLURAL, t("one horse", "two ______"), "horses", ["horsies", "horse"],
     "Um cavalo, one horse. E dois cavalos?",
     "Horses! Aqui é só colocar o S no final.", {"falar_ops": False}),
    (2, VEM, f("w:ovos", "EGGS"), "Chickens", ["Cows", "Pigs"],
     "Eggs, os ovos da feira. De onde eles vêm?",
     "Chickens! Quem bota os ovos é a galinha.", {}),
    (2, PT, t("farmer"), "Person", ["Thing", "Animal"],
     "Farmer é pessoa ou coisa? Person, thing ou animal?",
     "Person! Farmer é o fazendeiro, quem planta e cuida dos animais.", {"falar_ops": False}),
    (2, NOME, f("13:cabra"), "Goat", ["Sheep", "Pig"],
     "Agora essa, com chifrinho!",
     "Goat, a cabra! Sheep é a ovelha, não confunde.", {}),
    (2, VEM, f("w:leite", "MILK"), "Cows", ["Chickens", "Pigs"],
     "E o leite, milk? Vem de qual animal?",
     "Cows! O leite vem das vacas.", {}),
    (2, PT, t("paintings"), "Thing", ["Person", "Animal"],
     "Paintings é pessoa ou coisa?",
     "Thing! Paintings são as pinturas. Quem pinta é o artist.", {"falar_ops": False,
     "dica": ("Dica: paint é pintar.", "PAINT = PINTAR")}),
    (2, COMPL, t("The cow ______", "on the farm."), "lives", ["grows", "sells"],
     "Complete a frase: the cow, blank, on the farm.",
     "Lives! The cow lives on the farm: a vaca vive na fazenda.", {"falar_ops": False}),
    (2, NOME, f("13:pato"), "Duck", ["Goose", "Turkey"],
     "E essa ave que adora uma água?",
     "Duck, o pato! Goose é outra ave, o ganso. Ele aparece daqui a pouco.", {}),
    (2, COMPL, t("Plants ______", "on the farm."), "grow", ["swim", "play"],
     "E agora: plants, blank, on the farm.",
     "Grow! As plantas crescem na fazenda.", {"falar_ops": False}),
    (2, NOME, f("w:feira"), "Farmers market", ["Farm", "Garden"],
     "Barracas cheias de frutas, legumes e flores. Como se chama esse lugar em inglês?",
     "Farmers market, a feira! Onde os fazendeiros vendem o que plantam.", {"falar_ops": False,
     "sabia": "Farm é a fazenda, garden é o jardim e farmers market é a feira."}),
    (2, PT, f("w:padeiro", "BAKER"), "Person", ["Thing", "Food"],
     "Baker. É person, thing ou food?",
     "Person! Baker é o padeiro, quem faz os pães e os bolos.", {"falar_ops": False}),
    (2, NOME, f("13:galinha"), "Chicken", ["Turkey", "Duck"],
     "Última do nível médio: e essa ave?",
     "Chicken! A galinha, ou o frango.", {}),
    # ---------- DIFÍCIL ----------
    (3, NOME, f("w:peru"), "Turkey", ["Chicken", "Goose"],
     "Nível difícil! Como se diz peru em inglês?",
     "Turkey! E turkey também é o nome em inglês do país Turquia!", {
     "sabia": "Em inglês, turkey é o peru e Turkey, com T maiúsculo, é o país Turquia."}),
    (3, PLURAL, t("one sheep", "two ______"), "sheep", ["sheeps", "sheepes"],
     "Uma ovelha, one sheep. E duas ovelhas?",
     "Sheep! Não muda nada: one sheep, two sheep. Caiu?", {"falar_ops": False, "aviso": PEG}),
    (3, NOME, f("w:ganso"), "Goose", ["Duck", "Swan"],
     "E essa ave aqui? Não é o pato!",
     "Goose, o ganso!", {}),
    (3, PLURAL, t("one goose", "two ______"), "geese", ["gooses", "goosies"],
     "One goose, um ganso. E dois gansos?",
     "Geese! O O O vira E E. É igual tooth e teeth, dente e dentes.", {"falar_ops": False, "aviso": PEG,
     "dica": ("Dica: lembra de tooth e teeth?", "TOOTH → TEETH")}),
    (3, VEM, f("36:sueter", "WOOL SWEATER"), "Sheep", ["Cows", "Cotton farm"],
     "Esse é um wool sweater, um suéter de lã. De onde vem a lã?",
     "Sheep! A lã vem da ovelha. Cortam o pelo dela, e cresce de novo!", {
     "sabia": "A ovelha é tosquiada uma vez por ano. Não dói: é igual cortar o cabelo."}),
    (3, VEM, f("36:suco", "ORANGE JUICE"), "Orange grove", ["Apple tree", "Strawberry farm"],
     "Orange juice, suco de laranja. De onde vêm as laranjas?",
     "Orange grove! O laranjal, uma plantação cheia de pés de laranja.", {}),
    (3, PRON, t("An artist shows", "her paintings."), "her", ["artist", "paintings"],
     "An artist shows her paintings. Qual dessas palavras é o pronoun, o pronome?",
     "Her! O pronome fica no lugar do nome: her paintings, as pinturas dela.", {"falar_ops": False}),
    (3, "QUAL NÃO É NOUN?", t("Bands play music", "on stage."), "play", ["bands", "music"],
     "Bands play music on stage. Qual dessas palavras NÃO é noun, substantivo?",
     "Play! Play é verbo, tocar. Bands, music e stage são substantivos.", {"falar_ops": False, "aviso": PEG}),
    (3, PT, t("band"), "People", ["Thing", "Place"],
     "Band, a banda que toca na feira. É people, thing ou place?",
     "People! A band é um grupo de pessoas tocando música.", {"falar_ops": False}),
    (3, VEM, f("w:meias", "SOCKS"), "Cotton farm", ["Sugarcane", "Apple tree"],
     "Socks, as meias. Elas são feitas de algodão. De onde vêm?",
     "Cotton farm! Uma plantação de algodão.", {}),
    (3, VEM, f("w:queijo", "CHEESE"), "Milk", ["Eggs", "Sugar"],
     "Cheese, o queijo. É feito de quê?",
     "Milk! O queijo é feito de leite.", {}),
    (3, PONT, t("Where do eggs", "come from___"), PONT_OPS[0], PONT_OPS[1:],
     "Where do eggs come from. Qual sinal vai no final?",
     "Ponto de interrogação! Começa com where, onde: é uma pergunta.", {"falar_ops": False}),
    (3, CERTA, t(), "I can't wait!", ["i can't wait!", "I Can't Wait!"],
     "Qual dessas frases está escrita certinho? Olha bem as letras maiúsculas!",
     "I can't wait! O I, que quer dizer eu, é sempre maiúsculo em inglês.", {"falar_ops": False, "count": 9.0, "frases": True}),
    (3, VEM, f("w:geleia", "STRAWBERRY JAM"), "Strawberry farm", ["Orange grove", "Cotton farm"],
     "Strawberry jam, geleia de morango. De onde vêm os morangos?",
     "Strawberry farm! A fazenda de morangos.", {}),
    (3, NOME, f("13:lhama"), "Llama", ["Alpaca", "Goat"],
     "Última do nível difícil. E esse bicho, como se chama em inglês?",
     "Llama! Com dois L. A lhama é alta e tem orelhas compridas, tipo uma banana.", {"aviso": PEG,
     "sabia": "Llama se escreve com dois L. A lhama é maior que a alpaca e tem orelhas compridas."}),
    # ---------- MUITO DIFÍCIL ----------
    (4, NOME, f("w:alpaca"), "Alpaca", ["Llama", "Sheep"],
     "Muito difícil! Parece a de antes... mas e esse aqui?",
     "Alpaca! Menor que a lhama, com orelhinha curta e muito mais lã.", {"aviso": PEG}),
    (4, VEM, t("sugar", "for candy"), "Sugarcane", ["Cotton farm", "Apple tree"],
     "Sugar, o açúcar dos doces. De onde ele vem?",
     "Sugarcane! A cana-de-açúcar. E o Brasil é o maior produtor do mundo!", {
     "sabia": "O Brasil é o maior produtor de cana-de-açúcar do mundo."}),
    (4, NOME, f("w:guaxinim"), "Raccoon", ["Possum", "Fox"],
     "E esse mascarado aqui?",
     "Raccoon, o guaxinim! Olha a máscara preta no rosto.", {}),
    (4, NOME, f("w:gamba"), "Possum", ["Raccoon", "Rat"],
     "E esse? Não é rato, hein!",
     "Possum, o gambá! Quando ele leva um susto, finge que está morto.", {
     "sabia": "O gambá finge de morto quando sente perigo. Por isso em inglês existe a expressão play possum."}),
    (4, PLURAL, t("one turkey", "two ______"), "turkeys", ["turkies", "turkeyes"],
     "One turkey, um peru. E dois perus?",
     "Turkeys! Antes do Y tem vogal, então é só pôr o S. Igual donkeys.", {"falar_ops": False, "aviso": PEG,
     "dica": ("Dica: antes do Y tem uma vogal.", "VOGAL + Y")}),
    (4, "OUTRA PALAVRA PARA COWS?", t("many cows", "= ______"), "cattle", ["cats", "calves"],
     "Muitas vacas, many cows. Qual outra palavra quer dizer isso?",
     "Cattle! É o gado. Calves são os bezerros, e cats... são gatos!", {"falar_ops": False, "suspense": True}),
    (4, PRON, t("Do you want", "to go to the", "farmers market?"), "you", ["market", "want"],
     "Do you want to go to the farmers market? Qual é o pronoun?",
     "You! Você. Market é substantivo e want é verbo.", {"falar_ops": False}),
    (4, CERTA, t(), "Farmers bring fruits.", ["farmers bring fruits.", "Farmers bring fruits"],
     "Qual dessas está escrita certinho? Olha o começo e o fim!",
     "A que começa com maiúscula e termina com ponto final!", {"falar_ops": False, "count": 9.0, "frases": True}),
    (4, TRAD, t("gardener"), "Jardineiro", ["Jardim", "Garagem"],
     "Gardener. O que significa?",
     "Jardineiro! Garden é o jardim, e gardener é quem cuida dele.", {"falar_ops": False}),
    (4, "QUANTOS NOUNS?", t("The farmer sells", "eggs and milk."), "3", ["2", "4"],
     "The farmer sells eggs and milk. Quantos nouns, substantivos, tem nessa frase?",
     "Três! Farmer, eggs e milk. Sells é verbo.", {"falar_ops": False, "count": 9.0}),
    (4, "QUAL ESTÁ ERRADA?", t("Uma dessas", "está ERRADA!"), "two sheeps", ["two geese", "two horses"],
     "Uma dessas está errada. Qual?",
     "Two sheeps! Sheep não muda no plural: two sheep.", {"falar_ops": False, "aviso": PEG}),
    (4, VEM, f("w:mel", "HONEY"), "Bees", ["Flowers", "Sugarcane"],
     "Honey, o mel. Quem faz o mel?",
     "Bees! As abelhas fazem o mel com o néctar das flores.", {}),
    (4, CERTA, t("______ artist"), "an", ["a", "the an"],
     "Blank artist. Qual palavra vem antes de artist: an, a ou the an?",
     "An! Antes de som de vogal, usa an: an artist, an apple.", {"falar_ops": False, "suspense": True}),
    (4, "QUAL ESTÁ 100% CERTA?", t(), "Which baker sells cakes?",
     ["which baker sells cakes?", "Which baker sells cakes."],
     "Qual dessas frases está cem por cento certa?",
     "Which baker sells cakes, com W maiúsculo e ponto de interrogação! Se acertou, você é fera!",
     {"falar_ops": False, "count": 10.0, "final": True, "suspense": True, "frases": True}),
]

INTRO_FOTOS = ["w:celeiro", "w:fazenda", "14:trator"]   # intro e miniatura (não estão nas perguntas)


def copiar(ref, cred, rotulo):
    ori, nome = ref.split(":")
    pasta = os.path.join(VIDEOS, ORIGEM[ori])
    arq = nome + ".jpg"
    if not os.path.exists(os.path.join(pasta, "fotos", arq)):
        print("FALTA FOTO", ref)
        return arq
    shutil.copy2(os.path.join(pasta, "fotos", arq), os.path.join(HERE, "fotos", arq))
    c = json.load(open(os.path.join(pasta, "creditos.json"), encoding="utf-8"))
    por_arq = {v["arquivo"]: (k, v) for k, v in c.items()}
    k, v = por_arq[arq]
    cred[arq] = f"{rotulo}: {v['autor']}, {v['lic']}, {v['file']}"
    return arq


def main():
    rnd = random.Random(48)
    pos = [0, 1, 2] * 15
    rnd.shuffle(pos)
    pos[0] = 0
    R, cred = [], {}
    os.makedirs(os.path.join(HERE, "fotos"), exist_ok=True)
    for n, (nivel, perg, img, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        if ex.get("falar_ops", True):
            fq = f"{fq} {ops[0]}, {ops[1]} ou {ops[2]}?"
        img = dict(img)
        if ex.get("frases"):   # as opções ficam em MAIÚSCULAS no botão: a frase vai no cartão, o botão diz qual
            img["cartao"] = [f"{'ABC'[i]}) {o}" for i, o in enumerate(ops)]
            ops = [f"FRASE {'ABC'[i]}" for i in range(3)]
        if "foto" in img:
            img["foto"] = copiar(img["foto"], cred, img.get("rotulo") or certa)[:-4]
        r = {"n": n, "nivel": nivel, "pergunta": perg, **img, "img": f"q{n}.png",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": fq, "fala_r": fr, "count": ex.get("count", 8.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo a nota... a resposta é..."
        R.append(r)
    for ref in INTRO_FOTOS:
        copiar(ref, cred, ref.split(":")[1].capitalize())
    assert len(R) == 44
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"fotos": sorted(cred.values())}, open(os.path.join(HERE, "creditos.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], [sum(r["nivel"] == k for r in R) for k in (2, 3, 4)])


if __name__ == "__main__":
    main()
