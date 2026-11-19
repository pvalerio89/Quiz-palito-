"""Gera itens.json do vídeo 47 "Quiz de inglês: All About Plants" (estilo mais humano, 2026-11-13).

44 perguntas próprias de inglês de escola (3º ano, unidade "All About Plants", lição 5-1 "How are plants useful?"),
do MÉDIO ao MUITO DIFÍCIL (Patrick, 2026-11-19: "quero do médio ao difícil"): nome em inglês pela foto real,
palavras embaralhadas, plural/singular, o que significa, qual parte da planta a gente come, para que servem as
plantas e o action verb da frase. Nada copiado do livro (sem fotos, textos ou nomes da escola/aluno).
Fotos reais: as do vídeo 12 (Wikimedia Commons, créditos em creditos.json, tela final). As outras perguntas têm
cartão de caderno desenhado pelo build (fotos/q<n>.png, fora do Git).
Para não repetir o vídeo 46 (English Review Worksheet), ficam de fora peach, watermelon e os plurais
cherries/peaches/potatoes/strawberries/leaves.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
EN = "COMO SE DIZ EM INGLÊS?"
EMB = "DESEMBARALHE A PALAVRA!"
PL = "QUAL É O PLURAL?"
SG = "QUAL É O SINGULAR?"
SIG = "O QUE SIGNIFICA?"
PARTE = "QUE PARTE DA PLANTA A GENTE COME?"
USO = "PARA QUE SERVE?"
VERB = "QUAL É O ACTION VERB?"
ESC = "QUAL ESTÁ ESCRITO CERTO?"


# nível (1 médio, 2 difícil, 3 muito difícil), pergunta (topo), imagem (foto .jpg OU linhas do cartão), certa,
# [erradas], fala da pergunta, fala da resposta, extras
P = [
    # ---------- MÉDIO ----------
    (1, EN, "cereja.jpg", "Cherry", ["Berry", "Grape"],
     "Pra começar: como se diz essa fruta em inglês?",
     "Cherry! Cereja em inglês é cherry. Começou bem?", {"falar_ops": False, "count": 5.0}),
    (1, EN, "abobora.jpg", "Pumpkin", ["Potato", "Pepper"],
     "E essa, que aparece muito no Halloween?",
     "Pumpkin! A abóbora do Halloween.", {"falar_ops": False, "count": 6.0}),
    (1, EN, "milho.jpg", "Corn", ["Bean", "Pea"],
     "Agora essa aqui, que vira pipoca!",
     "Corn! Milho em inglês é corn. E pipoca é popcorn!", {"falar_ops": False}),
    (1, SIG, ["RIPE"], "Maduro", ["Podre", "Verde"],
     "O que significa ripe? Maduro, podre ou verde?",
     "Maduro! Fruta ripe tá pronta pra comer.", {"falar_ops": False}),
    (1, EMB, ["S N A E B"], "Beans", ["Bones", "Beets"],
     "Desembaralha essas cinco letras! Que palavra é?",
     "Beans! Feijões. O prato do brasileiro em inglês!", {"falar_ops": False}),
    (1, EN, "repolho.jpg", "Cabbage", ["Lettuce", "Broccoli"],
     "Essa verdura redondinha, como é que se fala em inglês?",
     "Cabbage! Repolho. Cuidado pra não confundir com lettuce, que é alface.", {"falar_ops": False}),
    (1, PL, ["ONE CABBAGE", "TWO ..."], "Cabbages", ["Cabbagies", "Cabbagees"],
     "Um repolho é one cabbage. E dois?",
     "Cabbages! É só colocar o s.", {"falar_ops": False}),
    (1, PARTE, "mandioca.jpg", "Root", ["Stem", "Leaf"],
     "Mandioca! Que parte da planta a gente come: root, stem ou leaf?",
     "Root! A mandioca é a raiz da planta.", {"falar_ops": False}),
    (1, SIG, ["USEFUL"], "Útil", ["Usado", "Inútil"],
     "O que significa useful?",
     "Útil! Plants are useful: as plantas são úteis.", {"falar_ops": False}),
    (1, EN, "framboesa.jpg", "Raspberry", ["Strawberry", "Blueberry"],
     "Cuidado que tem três berries! Qual é essa?",
     "Raspberry! Framboesa. Strawberry é o morango.", {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (1, VERB, ["MY DAD PICKS", "THE APPLES."], "Picks", ["Dad", "Apples"],
     "Ache o action verb, a palavra da ação: my dad picks the apples.",
     "Picks! Colhe. É o que o pai está fazendo.", {"falar_ops": False}),
    (1, EN, "beterraba.jpg", "Beet", ["Bean", "Radish"],
     "Essa raiz roxinha, como é em inglês?",
     "Beet! Beterraba é beet.", {"falar_ops": False}),
    (1, PL, ["ONE BUNCH", "TWO ..."], "Bunches", ["Bunchs", "Bunchies"],
     "Um cacho de uvas é a bunch of grapes. E dois cachos?",
     "Bunches! Palavra que termina em ch ganha es.", {"falar_ops": False}),
    (1, USO, ["COTTON", "(algodão)"], "Clothes", ["Glass", "Metal"],
     "A planta do algodão, cotton, serve pra fazer o quê?",
     "Clothes! Roupas. A sua camiseta pode ter vindo de uma planta!", {"falar_ops": False}),
    (1, EMB, ["T L A N P S"], "Plants", ["Planets", "Pants"],
     "Desembaralha essa! Seis letras.",
     "Plants! Plantas. Planets tem uma letra a mais.", {"falar_ops": False}),
    # ---------- DIFÍCIL ----------
    (2, EMB, ["K P M U N I P S"], "Pumpkins", ["Napkins", "Muffins"],
     "Agora complica! Oito letras embaralhadas.",
     "Pumpkins! Abóboras.", {"falar_ops": False}),
    (2, SIG, ["FALL"], "Outono", ["Inverno", "Primavera"],
     "Fall é uma estação do ano. Qual?",
     "Outono! Fall também quer dizer cair, porque é quando as folhas caem.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!",
      "sabia": "Nos Estados Unidos o outono é fall porque é quando as folhas caem das árvores."}),
    (2, PARTE, "salsao.jpg", "Stem", ["Root", "Seed"],
     "Salsão, que em inglês é celery. A gente come qual parte?",
     "Stem! O talo do salsão é o caule.", {"falar_ops": False}),
    (2, EN, "coco.jpg", "Coconut", ["Walnut", "Peanut"],
     "Essa é peluda! Como é em inglês?",
     "Coconut! Coco. Peanut é amendoim.", {"falar_ops": False}),
    (2, PL, ["ONE DAISY", "TWO ..."], "Daisies", ["Daisys", "Daisyes"],
     "Daisy é a margarida, uma flor. E duas margaridas?",
     "Daisies! O y vira i e ganha es.", {"falar_ops": False, "dica": ("Dica: o y some!", "O Y SOME!")}),
    (2, SIG, ["SEED"], "Semente", ["Folha", "Caule"],
     "O que significa seed?",
     "Semente! Tudo começa com uma seed.", {"falar_ops": False}),
    (2, VERB, ["THE GIRLS WATER", "THE GARDEN."], "Water", ["Girls", "Garden"],
     "The girls water the garden. Qual é o action verb?",
     "Water! Aqui water é regar: as meninas regam o jardim.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (2, EN, "ameixa.jpg", "Plum", ["Prune", "Pear"],
     "E essa fruta roxa?",
     "Plum! Ameixa fresca. Prune é a ameixa seca!",
     {"falar_ops": False, "sabia": "Prune é a ameixa seca, aquela escurinha. A fresca é plum."}),
    (2, EMB, ["G A B C A S E B"], "Cabbages", ["Sausages", "Bandages"],
     "Oito letras de novo! Que palavra é essa?",
     "Cabbages! Repolhos.", {"falar_ops": False}),
    (2, PARTE, "couve-flor.jpg", "Flower", ["Leaf", "Root"],
     "Couve-flor! A gente come qual parte da planta?",
     "Flower! A flor. Tá até no nome: cauliflower!", {"falar_ops": False}),
    (2, USO, ["TREES", "GIVE US..."], "Wood", ["Glass", "Stone"],
     "Trees give us... O que as árvores dão pra gente?",
     "Wood! Madeira, pra fazer mesa, cadeira e casa.", {"falar_ops": False}),
    (2, EN, "amora.jpg", "Blackberry", ["Blueberry", "Cranberry"],
     "Mais uma berry! Qual é essa pretinha?",
     "Blackberry! Amora. Black é preto.", {"falar_ops": False}),
    (2, SIG, ["GREENHOUSE"], "Estufa", ["Casa verde", "Jardim"],
     "O que significa greenhouse?",
     "Estufa! Aquela casa de vidro onde as plantas crescem.", {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (2, PL, ["ONE RADISH", "TWO ..."], "Radishes", ["Radishs", "Radishies"],
     "Radish é rabanete. E dois rabanetes?",
     "Radishes! Termina em sh, ganha es.", {"falar_ops": False}),
    (2, VERB, ["WE GROW TOMATOES", "AT HOME."], "Grow", ["Tomatoes", "Home"],
     "We grow tomatoes at home. Cadê o action verb?",
     "Grow! Plantar, cultivar. A gente cultiva tomates em casa.", {"falar_ops": False}),
    # ---------- MUITO DIFÍCIL ----------
    (3, SIG, ["EDIBLE"], "Comestível", ["Venenosa", "Cozida"],
     "Muito difícil agora! Edible plants. O que é edible?",
     "Comestível! Edible plants são as plantas que a gente pode comer.", {"falar_ops": False}),
    (3, PARTE, "ervilha.jpg", "Seed", ["Stem", "Root"],
     "Ervilha, que é pea. A gente come qual parte?",
     "Seed! A ervilha é a semente da planta.", {"falar_ops": False}),
    (3, EMB, ["S T O P A E T O"], "Potatoes", ["Tomatoes", "Teapots"],
     "Oito letras. Cuidado, que tem pegadinha!",
     "Potatoes! Tomatoes tem um m, e teapots tem uma letra a menos.",
     {"falar_ops": False, "aviso": "CONFERE AS LETRAS!", "suspense": True}),
    (3, EN, "mirtilo.jpg", "Blueberry", ["Blackberry", "Gooseberry"],
     "Essa bolinha azul, como é em inglês?",
     "Blueberry! Mirtilo. Blue é azul.", {"falar_ops": False}),
    (3, SIG, ["HARVEST"], "Colheita", ["Plantio", "Rega"],
     "O que significa harvest?",
     "Colheita! Harvest é quando se colhe o que plantou.", {"falar_ops": False}),
    (3, USO, ["ALOE VERA", "IS USED AS..."], "Medicine", ["Wood", "Glass"],
     "A babosa, aloe vera, é usada como o quê?",
     "Medicine! Remédio, por exemplo pra queimadura.", {"falar_ops": False}),
    (3, PL, ["ONE BUSH", "TWO ..."], "Bushes", ["Bushs", "Bushies"],
     "Bush é arbusto. E dois arbustos?",
     "Bushes! Sh ganha es.", {"falar_ops": False}),
    (3, PARTE, "batata.jpg", "Stem", ["Root", "Seed"],
     "Essa derruba muita gente! A batata é qual parte da planta?",
     "Stem! A batata é um caule que cresce debaixo da terra. Muita gente acha que é raiz!",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!", "suspense": True,
      "sabia": "A batata é um caule que cresce debaixo da terra, chamado tubérculo. Não é raiz!"}),
    (3, VERB, ["THE SUN HELPS", "PLANTS."], "Helps", ["Sun", "Plants"],
     "The sun helps plants. Qual é o action verb?",
     "Helps! Ajuda. O sol ajuda as plantas.", {"falar_ops": False}),
    (3, SG, ["BERRIES"], "Berry", ["Berrie", "Berrys"],
     "Agora ao contrário: berries é plural. Qual é o singular?",
     "Berry! O ies volta a ser y.", {"falar_ops": False}),
    (3, SIG, ["SPROUT"], "Brotar", ["Murchar", "Florescer"],
     "O que significa sprout?",
     "Brotar! É quando a semente começa a crescer.", {"falar_ops": False, "dica": ("Dica: acontece com a semente!", "SEMENTE!")}),
    (3, EN, "castanha-do-para.jpg", "Brazil nuts", ["Peanuts", "Walnuts"],
     "Essa é brasileira! Como se diz em inglês?",
     "Brazil nuts! Castanha-do-pará. Tem até Brasil no nome!", {"falar_ops": False}),
    (3, ESC, ["BRÓCOLIS", "EM INGLÊS"], "Broccoli", ["Brocoli", "Brocolli"],
     "Como se escreve brócolis em inglês? Olha bem as letras!",
     "Broccoli! Com dois c e um l só.", {"falar_ops": False, "suspense": True}),
    (3, EMB, ["S E B L A T", "G E V E"], "Vegetables", ["Beanstalks", "Greenhouse"],
     "Valendo tudo! Dez letras embaralhadas. Que palavra é essa?",
     "Vegetables! Legumes e verduras. Se acertou essa, seu inglês é de primeira!",
     {"falar_ops": False, "count": 12.0, "suspense": True, "final": True}),
]

EMBARALHADAS = {"S N A E B": "BEANS", "T L A N P S": "PLANTS", "K P M U N I P S": "PUMPKINS",
                "G A B C A S E B": "CABBAGES", "S T O P A E T O": "POTATOES", "S E B L A T G E V E": "VEGETABLES"}


def main():
    for k, v in EMBARALHADAS.items():   # confere as letras das embaralhadas
        assert sorted(k.replace(" ", "")) == sorted(v), (k, v)
    rnd = random.Random(47)
    pos = [0, 1, 2] * 15
    rnd.shuffle(pos)
    pos[0] = 0
    R = []
    for n, (nivel, perg, img, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        if perg == EMB:
            assert sorted("".join(img).replace(" ", "")) == sorted(certa.upper()), (n, img)
        if ex.get("falar_ops", True):
            fq = f"{fq} {ops[0]}, {ops[1]} ou {ops[2]}?"
        r = {"n": n, "nivel": nivel, "pergunta": perg, "opcoes": ops, "certa": pos[n - 1], "fala_q": fq,
             "fala_r": fr, "count": ex.get("count", 10.0 if nivel > 1 else 8.0)}
        if isinstance(img, str):
            assert os.path.exists(os.path.join(HERE, "fotos", img)), img
            r["foto"] = img
        else:
            r["cartao"], r["foto"] = img, f"q{n}.png"
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo tudo... a resposta é..."
        R.append(r)
    assert len(R) == 44 and len({r["foto"] for r in R}) == 44
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], [sum(r["nivel"] == k for r in R) for k in (1, 2, 3)])


if __name__ == "__main__":
    main()
