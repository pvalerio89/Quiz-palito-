"""Gera itens.json e copia as fotos do vídeo 49 "Inglês: tempos verbais da viagem" (estilo mais humano, 2026-11-13).

44 perguntas PRÓPRIAS a partir do tema da unidade "Travel" de um livro de gramática em inglês que o Patrick mandou em
foto (2026-11-19): verbos no presente, passado (inclusive irregulares: swam, made, saw, took, flew, read...) e futuro
(will), corrigir o tempo verbal errado e achar o título (livros, filmes e programas de TV são sublinhados).
Frases, títulos e verbos inventados aqui (nada copiado do livro; as fotos do livro NÃO vão para o vídeo nem para o repo).
Diferente do vídeo 46 (que usou walk, cook, clean, watch, wash, open, play, study, help, jump, will visit, will swim).
Do MÉDIO ao MUITO DIFÍCIL. Vídeo de 15 min pra cima.
Imagem: foto real de lugar ou prato do mundo (Wikimedia Commons, reaproveitada dos vídeos 26 e 27) com a frase num
painel branco embaixo, ou cartão de caderno com a frase.
Uso: py -3 itens.py
"""
import json, os, random, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
ORIGENS = [os.path.join(VIDEOS, "26-pais-pelo-monumento"), os.path.join(VIDEOS, "27-paises-pelas-comidas")]
VERBO = "COMPLETE COM O VERBO:"
TEMPO = "QUE TEMPO VERBAL É ESSE?"
TEMPO_OPS = ["Presente", "Passado", "Futuro"]
PASSADO = "QUAL É O PASSADO?"
CORRIGE = "O VERBO ESTÁ NO TEMPO ERRADO! QUAL CORRIGE?"
TITULO = "QUAL É O TÍTULO? (O QUE SE SUBLINHA)"
PAL = "QUAL PALAVRA COMPLETA?"
INGLES = "COMO SE DIZ EM INGLÊS?"
ERRADA = "QUAL FRASE ESTÁ ERRADA?"
CERTA = "QUAL ESTÁ CERTA?"
SABIA_IRR = "Verbo irregular não ganha E D no passado: swim vira swam, see vira saw, make vira made."
SABIA_TIT = "Quando a gente escreve à mão, sublinha o título de livro, filme e programa de TV. No computador, usa itálico."
SABIA_DOBRA = "Verbo curto que termina em consoante, vogal, consoante dobra a última letra: plan, planned. Stop, stopped."
SABIA_WILL = "Depois do will, o verbo fica puro: sem S e sem E D. Will relax, will ride, will fly."
SABIA_IES = "Consoante mais Y no fim: troca o Y por I E S no presente e por I E D no passado. Fly, flies. Carry, carried."


def t(*linhas):
    return {"cartao": list(linhas)}


def f(foto, lugar, *linhas):
    return {"foto": foto, "lugar": lugar, "cartao": list(linhas)}


# nível (2 médio, 3 difícil, 4 muito difícil), pergunta (topo), imagem, certa, [erradas], fala pergunta, fala resposta, extras
P = [
    # ---------- MÉDIO ----------
    (2, VERBO, f("cristo-redentor", "RIO DE JANEIRO", "Every summer, we", "______ to Rio.", "(travel)"),
     "travel", ["traveled", "will travel"],
     "Primeira, valendo! Every summer, we... travel... to Rio. Qual a forma certa?",
     "Travel! Every summer é todo verão: é algo que se repete, então é presente.", {"falar_ops": False}),
    (2, TEMPO, t("swam"), "Passado", ["Presente", "Futuro"],
     "Swam. Que tempo verbal é esse? Presente, passado ou futuro?",
     "Passado! Swam é o passado de swim, nadar. Não tem E D, mas é passado!",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (2, VERBO, f("piramides-de-gize", "EGITO", "Last year, Leo", "______ the pyramids.", "(see)"),
     "saw", ["seed", "sees"],
     "Last year, Leo... see... the pyramids. Qual a forma certa?",
     "Saw! O passado de see é saw. Last year é ano passado.", {"falar_ops": False}),
    (2, TITULO, t("We watched the", "movie Lost in", "the Jungle."), "Lost in the Jungle", ["We watched", "the movie"],
     "We watched the movie Lost in the Jungle. Qual é o título do filme?",
     "Lost in the Jungle! É o nome do filme, então é o que a gente sublinha.", {"falar_ops": False}),
    (2, TEMPO, t("will pack"), "Futuro", ["Presente", "Passado"],
     "Will pack. Que tempo verbal é esse?", "Futuro! Will na frente do verbo: vai arrumar a mala.",
     {"falar_ops": False}),
    (2, VERBO, f("torre-de-pisa", "ITÁLIA", "Tomorrow, Bia", "______ the tower.", "(climb)"),
     "will climb", ["climbed", "climbs"],
     "Tomorrow, Bia... climb... the tower. Qual a forma certa?",
     "Will climb! Tomorrow é amanhã: futuro é will mais o verbo.", {"falar_ops": False}),
    (2, INGLES, t("MALA", "(de viagem)"), "Suitcase", ["Backpack", "Ticket"],
     "Mala de viagem. Como se diz em inglês?", "Suitcase! Backpack é mochila e ticket é passagem.", {}),
    (2, VERBO, f("coliseu", "ROMA", "Yesterday, they", "______ photos.", "(take)"),
     "took", ["taked", "takes"],
     "Yesterday, they... take... photos in Rome. Qual a forma certa?",
     "Took! Take é irregular: o passado é took. Taked não existe!", {"falar_ops": False}),
    (2, TEMPO, t("travels"), "Presente", ["Passado", "Futuro"],
     "Travels. Que tempo verbal é esse?", "Presente! O S no fim é do he, she e it: ela viaja.",
     {"falar_ops": False}),
    (2, PAL, f("petra", "JORDÂNIA", "______, I will", "ride a camel."), "Next week", ["Last week", "Yesterday"],
     "Qual palavra completa a frase: blank, I will ride a camel?",
     "Next week! Will ride é futuro, então é semana que vem.",
     {"falar_ops": False, "dica": ("Dica: olha o will...", "WILL = FUTURO")}),
    (2, VERBO, f("big-ben", "LONDRES", "Before every trip,", "Dad ______ a map.", "(read)"),
     "reads", ["readed", "will reads"],
     "Before every trip, Dad... read... a map. Qual a forma certa?",
     "Reads! Antes de toda viagem é algo que se repete: presente, e com he ganha S.", {"falar_ops": False}),
    (2, TITULO, t("My favorite book", "is The Secret Map."), "The Secret Map", ["My favorite book", "favorite"],
     "My favorite book is The Secret Map. Qual é o título do livro?",
     "The Secret Map! O mapa secreto. Nome de livro é título.", {"falar_ops": False}),
    (2, INGLES, t("PASSAPORTE"), "Passport", ["Luggage", "Airport"],
     "Passaporte. Como se diz em inglês?", "Passport! Luggage é bagagem e airport é aeroporto.", {}),
    (2, VERBO, f("muralha-da-china", "CHINA", "Next month, my class", "______ the Great Wall.", "(explore)"),
     "will explore", ["explored", "explores"],
     "Next month, my class... explore... the Great Wall. Qual a forma certa?",
     "Will explore! Next month é mês que vem: futuro.", {"falar_ops": False}),
    (2, CORRIGE, t("Yesterday, Mom", "WILL BUY", "the tickets."), "bought", ["buys", "buyed"],
     "Yesterday, Mom will buy the tickets. Essa frase está errada! Qual verbo corrige?",
     "Bought! Yesterday é ontem, então é passado. E o passado de buy é bought.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    # ---------- DIFÍCIL ----------
    (3, PASSADO, t("make", "(fazer)"), "made", ["maked", "makes"],
     "Nível difícil, valendo! Qual é o passado de make?",
     "Made! Make é irregular. Maked não existe.", {"falar_ops": False, "suspense": True, "sabia": SABIA_IRR}),
    (3, VERBO, f("opera-de-sydney", "AUSTRÁLIA", "Last week, we", "______ in the ocean.", "(swim)"),
     "swam", ["swimmed", "swims"],
     "Last week, we... swim... in the ocean. Como fica?",
     "Swam! O passado de swim é swam. Swimmed é o erro mais comum!",
     {"falar_ops": False, "aviso": "QUASE TODO MUNDO ERRA!", "suspense": True}),
    (3, CORRIGE, t("Tomorrow, Zoe", "RODE", "a horse."), "will ride", ["rides", "rided"],
     "Tomorrow, Zoe rode a horse. Tá errado! Qual verbo corrige?",
     "Will ride! Tomorrow pede futuro. Rode é o passado de ride.", {"falar_ops": False}),
    (3, TITULO, t("Let's watch", "Ocean Friends", "on TV tonight!"), "Ocean Friends", ["Let's watch", "on TV tonight"],
     "Let's watch Ocean Friends on TV tonight! Qual parte a gente sublinha?",
     "Ocean Friends! É o nome do programa de TV.", {"falar_ops": False, "sabia": SABIA_TIT}),
    (3, PASSADO, t("plan", "(planejar)"), "planned", ["planed", "planied"],
     "Qual é o passado de plan, planejar? Como se escreve?",
     "Planned, com dois N! Plan dobra o N antes do E D.",
     {"falar_ops": False, "sabia": SABIA_DOBRA, "aviso": "DERRUBA MUITA GENTE!"}),
    (3, VERBO, f("machu-picchu", "PERU", "Next summer, my", "cousins ______", "to Peru.", "(fly)"),
     "will fly", ["flew", "flies"],
     "Next summer, my cousins... fly... to Peru. Qual a forma certa?",
     "Will fly! Next summer é o verão que vem: futuro.", {"falar_ops": False}),
    (3, TEMPO, t("made"), "Passado", ["Presente", "Futuro"],
     "Made. Que tempo verbal é esse?", "Passado! Made é o passado de make: fez.", {"falar_ops": False}),
    (3, "DESEMBARALHE O VERBO:", t("D • E • K", "A • P • C"), "PACKED", ["PICKED", "PACKS"],
     "Desembaralha essas letras! D, E, K, A, P, C. Que verbo forma?",
     "Packed! Arrumou a mala. Picked tem I, e packs não tem D nem E.", {"falar_ops": False, "count": 10.0}),
    (3, VERBO, f("torre-de-belem", "LISBOA", "Every morning, Grandpa", "______ the bus.", "(catch)"),
     "catches", ["catchs", "caught"],
     "Every morning, Grandpa... catch... the bus. Como se escreve?",
     "Catches, com E S! Termina em C H, então ganha E S.", {"falar_ops": False, "suspense": True}),
    (3, CORRIGE, t("Last Sunday, we", "WILL DRIVE", "to the lake."), "drove", ["drives", "drived"],
     "Last Sunday, we will drive to the lake. Tá errado! Qual verbo corrige?",
     "Drove! Last Sunday é domingo passado. O passado de drive é drove.", {"falar_ops": False}),
    (3, "QUAL É O PRESENTE?", t("went  →  he ______"), "goes", ["gos", "go"],
     "Went é o passado de go. E no presente, com he, como fica?",
     "Goes! Go termina em O, então ganha E S: he goes.", {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (3, TITULO, t("I watch Tiny Chefs", "every Friday", "on TV."), "Tiny Chefs", ["every Friday", "on TV"],
     "I watch Tiny Chefs every Friday on TV. Qual é o título?",
     "Tiny Chefs! O nome do programa.", {"falar_ops": False}),
    (3, VERBO, f("sushi", "JAPÃO", "On our trip, we", "______ sushi.", "(eat)"),
     "ate", ["eated", "eats"],
     "On our trip, we... eat... sushi in Japan. Já foi! Qual a forma certa?",
     "Ate! O passado de eat é ate. Eated não existe.", {"falar_ops": False, "suspense": True}),
    (3, "QUAL É O FUTURO?", t("relaxes  →  ______"), "will relax", ["will relaxes", "relaxed"],
     "Relaxes. Como fica no futuro?", "Will relax! Depois do will, o verbo puro, sem o E S.",
     {"falar_ops": False, "sabia": SABIA_WILL}),
    (3, "QUANTOS ESTÃO NO FUTURO?", t("will hike • swam", "flies • will pack", "will eat • made"), "3", ["2", "4"],
     "Will hike, swam, flies, will pack, will eat e made. Quantos estão no futuro?",
     "Três! Will hike, will pack e will eat.", {"count": 10.0}),
    # ---------- MUITO DIFÍCIL ----------
    (4, PASSADO, t("read", "(ler)"), "read", ["readed", "reed"],
     "Agora é o nível que derruba até adulto! Qual é o passado de read, ler?",
     "Read! Escreve igual, mas no passado se fala réd. Readed não existe!",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!", "suspense": True}),
    (4, VERBO, f("estatua-da-liberdade", "NOVA YORK", "Last winter, Dad", "______ us to New York.", "(bring)"),
     "brought", ["bringed", "brang"],
     "Last winter, Dad... bring... us to New York. Qual a forma certa?",
     "Brought! O passado de bring é brought. Bringed e brang não existem.",
     {"falar_ops": False, "aviso": "QUASE TODO MUNDO ERRA!"}),
    (4, CORRIGE, t("Next year, my sister", "DROVE", "to Canada."), "will drive", ["drives", "drived"],
     "Next year, my sister drove to Canada. Qual verbo corrige?",
     "Will drive! Next year é ano que vem: futuro.", {"falar_ops": False}),
    (4, PASSADO, t("stop", "(parar)"), "stopped", ["stoped", "stopt"],
     "Qual é o passado de stop? Como se escreve?", "Stopped, com dois P! Igual planned.",
     {"falar_ops": False, "suspense": True}),
    (4, TITULO, t("My brother read", "The Dragon and Me", "on the plane."),
     "The Dragon and Me", ["The Dragon", "on the plane"],
     "My brother read The Dragon and Me on the plane. Qual é o título inteiro?",
     "The Dragon and Me! O título é o nome todo do livro, não só a primeira parte.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (4, VERBO, f("taj-mahal", "ÍNDIA", "Every year, many", "tourists ______", "the Taj Mahal.", "(visit)"),
     "visit", ["visits", "visited"],
     "Every year, many tourists... visit... the Taj Mahal. Qual a forma certa?",
     "Visit, sem S! Tourists é plural, e com they o verbo não ganha S.",
     {"falar_ops": False, "aviso": "QUASE TODO MUNDO ERRA!", "suspense": True}),
    (4, CORRIGE, t("Yesterday, the kids", "CARRY", "their bags."), "carried", ["carryed", "carries"],
     "Yesterday, the kids carry their bags. Qual verbo corrige?",
     "Carried! Consoante mais Y: troca por I E D.", {"falar_ops": False, "sabia": SABIA_IES}),
    (4, PASSADO, t("write", "(escrever)"), "wrote", ["writed", "writes"],
     "Qual é o passado de write, escrever?", "Wrote! Ontem eu escrevi um cartão-postal: I wrote a postcard.",
     {"falar_ops": False}),
    (4, VERBO, f("golden-gate", "SÃO FRANCISCO", "Tomorrow, we", "______ across", "the bridge.", "(ride)"),
     "will ride", ["rode", "will rode"],
     "Tomorrow, we... ride... across the bridge. Qual a forma certa?",
     "Will ride! Will rode não existe: depois do will, o verbo puro.",
     {"falar_ops": False, "aviso": "TEM PEGADINHA!"}),
    (4, "QUANTOS TÍTULOS TEM?", t("I read Space Cats", "and watched", "Pizza Planet on TV."), "2", ["1", "3"],
     "I read Space Cats and watched Pizza Planet on TV. Quantos títulos tem nessa frase?",
     "Dois! Space Cats, o livro, e Pizza Planet, o programa de TV.", {"falar_ops": False}),
    (4, VERBO, f("ponte-da-torre", "LONDRES", "The pilot ______", "to London", "every Monday.", "(fly)"),
     "flies", ["flys", "flew"],
     "The pilot... fly... to London every Monday. Como se escreve?",
     "Flies! Consoante mais Y: troca o Y por I E S.", {"falar_ops": False, "suspense": True}),
    (4, ERRADA, t("Uma dessas", "frases está", "ERRADA!"), "We swimmed.",
     ["They made tea.", "She will hike."],
     "Uma dessas frases está errada! Qual?", "We swimmed! O certo é we swam.",
     {"falar_ops": False}),
    (4, CERTA, t("Eu vou", "viajar."), "I will travel.",
     ["I will traveled.", "I traveled."],
     "Como se diz: eu vou viajar? Qual está certa?",
     "I will travel! Will mais o verbo puro. Traveled já é passado.",
     {"falar_ops": False, "aviso": "QUASE TODO MUNDO ERRA!"}),
    (4, "QUANTOS ESTÃO NO PASSADO?", t("made • will swim", "rode • flies", "saw • packs"), "3", ["2", "4"],
     "Valendo a nota! Made, will swim, rode, flies, saw e packs. Quantos estão no passado?",
     "Três! Made, rode e saw, todos irregulares. Se acertou essa, tirou dez em inglês!",
     {"count": 12.0, "suspense": True, "final": True}),
]
INTRO = ["torre-eiffel", "piramides-de-gize", "cristo-redentor"]


def main():
    rnd = random.Random(49)
    pos = [0, 1, 2] * 15
    rnd.shuffle(pos)
    pos[0] = 0
    R, cred = [], {}
    por_arq = {}
    for o in ORIGENS:
        for k, v in json.load(open(os.path.join(o, "creditos.json"), encoding="utf-8")).items():
            por_arq[v["arquivo"]] = (k, v, o)
    os.makedirs(os.path.join(HERE, "fotos"), exist_ok=True)

    def copiar(arq, rotulo):
        nome, c, o = por_arq[arq]
        shutil.copy2(os.path.join(o, "fotos", arq), os.path.join(HERE, "fotos", arq))
        cred[arq] = f"{nome}{rotulo}: {c['autor']}, {c['lic']}, {c['file']}"

    for n, (nivel, perg, img, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        if ex.get("falar_ops", True):
            fq = f"{fq} {ops[0]}, {ops[1]} ou {ops[2]}?"
        r = {"n": n, "nivel": nivel, "pergunta": perg, **img, "img": f"q{n}.png",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": fq, "fala_r": fr, "count": ex.get("count", 8.0)}
        if "foto" in img:
            copiar(img["foto"] + ".jpg", "")
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo a nota... a resposta é..."
        R.append(r)
    for extra in INTRO:   # intro e miniatura
        copiar(extra + ".jpg", "")
    assert len(R) == 44
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"fotos": sorted(cred.values())}, open(os.path.join(HERE, "creditos.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], [sum(r["nivel"] == k for r in R) for k in (2, 3, 4)],
          len(cred), "fotos")


if __name__ == "__main__":
    main()
