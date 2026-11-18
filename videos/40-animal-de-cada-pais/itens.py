"""Gera itens.json do vídeo 40 "Qual é o ANIMAL símbolo de cada PAÍS?" (estilo mais humano).

36 perguntas próprias, do fácil ao impossível: o cartão mostra a BANDEIRA do país (domínio público, as do vídeo 03)
e as 3 alternativas A/B/C são animais, cada uma com a FOTO REAL (Wikimedia Commons: as do vídeo 13 + as novas em
fotos/). Na resposta, o cartão troca a bandeira pela foto do animal certo. Só casos com fonte clara (animal ou ave
nacional na Wikipédia "List of national animals" / brasão / bandeira); as alternativas erradas não são símbolo
daquele país. Última: Escócia = UNICÓRNIO (desenho, emoji Noto, Apache 2.0). Fatos conferidos em 2026-11-18.
Uso: py -3 itens.py   (copia fotos e bandeiras que faltarem e monta os cartões das bandeiras)
"""
import json, os, random, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
V13 = os.path.join(VIDEOS, "13-animal-pela-foto")

# código da bandeira: (nome na tela, nome falado)
PAISES = {
    "au": ("AUSTRÁLIA", "Austrália"), "cn": ("CHINA", "China"), "us": ("ESTADOS UNIDOS", "Estados Unidos"),
    "in": ("ÍNDIA", "Índia"), "ca": ("CANADÁ", "Canadá"), "ru": ("RÚSSIA", "Rússia"),
    "nz": ("NOVA ZELÂNDIA", "Nova Zelândia"), "fr": ("FRANÇA", "França"), "th": ("TAILÂNDIA", "Tailândia"),
    "mx": ("MÉXICO", "México"), "gb-eng": ("INGLATERRA", "Inglaterra"), "it": ("ITÁLIA", "Itália"),
    "id": ("INDONÉSIA", "Indonésia"), "tz": ("TANZÂNIA", "Tanzânia"), "za": ("ÁFRICA DO SUL", "África do Sul"),
    "pe": ("PERU", "Peru"), "cl": ("CHILE", "Chile"), "ar": ("ARGENTINA", "Argentina"),
    "cr": ("COSTA RICA", "Costa Rica"), "gt": ("GUATEMALA", "Guatemala"), "pg": ("PAPUA-NOVA GUINÉ", "Papua-Nova Guiné"),
    "br": ("BRASIL", "Brasil"), "np": ("NEPAL", "Nepal"), "pa": ("PANAMÁ", "Panamá"), "mn": ("MONGÓLIA", "Mongólia"),
    "cd": ("CONGO", "República Democrática do Congo"), "bz": ("BELIZE", "Belize"), "kr": ("COREIA DO SUL", "Coreia do Sul"),
    "ug": ("UGANDA", "Uganda"), "dk": ("DINAMARCA", "Dinamarca"), "jp": ("JAPÃO", "Japão"), "bt": ("BUTÃO", "Butão"),
    "pk": ("PAQUISTÃO", "Paquistão"), "bw": ("BOTSUANA", "Botsuana"), "qa": ("CATAR", "Catar"), "gb-sct": ("ESCÓCIA", "Escócia"),
}

# animal na tela -> foto (do vídeo 13 se existir lá; senão fotos/ deste vídeo)
FOTO = {
    "CANGURU": "canguru", "LEÃO": "leao", "GIRAFA": "girafa", "PANDA": "panda-gigante", "TIGRE": "tigre",
    "MACACO": "macaco", "ÁGUIA-CARECA": "aguia", "URSO-PARDO": "urso-pardo", "CAVALO": "cavalo", "VACA": "vaca",
    "RINOCERONTE": "rinoceronte", "CASTOR": "castor", "ALCE": "alce", "URSO-POLAR": "urso-polar", "LOBO": "lobo",
    "KIWI": "kiwi", "EMU": "emu", "GALO": "galo", "ELEFANTE": "elefante", "ÁGUIA-REAL": "aguia-real",
    "TUCANO": "tucano", "IGUANA": "iguana", "RAPOSA": "raposa", "JAVALI": "javali", "DRAGÃO-DE-KOMODO": "dragao-de-komodo",
    "ORANGOTANGO": "orangotango", "ZEBRA": "zebra", "SPRINGBOK": "springbok", "VICUNHA": "vicunha", "LHAMA": "lhama",
    "CAPIVARA": "capivara", "CONDOR": "condor-andino", "HARPIA": "gaviao-real", "JOÃO-DE-BARRO": "joao-de-barro",
    "EMA": "ema", "BEIJA-FLOR": "beija-flor", "BICHO-PREGUIÇA": "bicho-preguica", "QUETZAL": "quetzal",
    "ARARA": "arara", "AVE-DO-PARAÍSO": "ave-do-paraiso", "PAPAGAIO": "papagaio", "SABIÁ-LARANJEIRA": "sabia-laranjeira",
    "PANDA-VERMELHO": "panda-vermelho", "CAMELO": "camelo", "OCAPI": "ocapi", "ANTA": "anta", "ONÇA-PINTADA": "onca-pintada",
    "GROU-COROADO": "grou-coroado", "AVESTRUZ": "avestruz", "CISNE": "cisne-branco", "PATO": "pato",
    "FAISÃO-VERDE": "faisao-verde", "TAKIN": "takin", "BISÃO": "bisao", "CABRA": "cabra", "MARKHOR": "markhor",
    "ÓRIX": "orix-da-arabia", "UNICÓRNIO": "unicornio", "OVELHA": "ovelha",
}
PREP = {"us": "dos", "za": "da", "pa": "do", "cd": "da", "bz": "de", "ug": "de", "pg": "de", "qa": "do", "bw": "de", "kr": "da"}

# país, animal certo, [2 errados], entrada falada, fala da resposta, extras
P = [
    ("au", "CANGURU", ["LEÃO", "GIRAFA"], "Pra começar, uma bem fácil!",
     "Canguru! Ele está até no brasão da Austrália!", {"count": 4.0}),
    ("cn", "PANDA", ["TIGRE", "MACACO"], "Essa aqui todo mundo sabe!",
     "Panda! O panda-gigante é o grande símbolo da China!", {"count": 4.0}),
    ("us", "ÁGUIA-CARECA", ["URSO-PARDO", "CAVALO"], "Mais uma pra aquecer!",
     "Águia-careca! Ela aparece no selo oficial dos Estados Unidos!", {"count": 5.0}),
    ("in", "TIGRE", ["VACA", "RINOCERONTE"], "Agora um gigante da Ásia!",
     "Tigre! O tigre-de-bengala é o animal nacional da Índia!", {}),
    ("ca", "CASTOR", ["ALCE", "URSO-POLAR"], "Bora pro país do frio!",
     "Castor! Ele está até na moeda de cinco centavos do Canadá!", {}),
    ("ru", "URSO-PARDO", ["LOBO", "TIGRE"], "Agora o maior país do mundo!",
     "Urso-pardo! O urso é o símbolo mais famoso da Rússia!", {}),
    ("nz", "KIWI", ["EMU", "CANGURU"], "Essa é do outro lado do mundo!",
     "Kiwi! É um passarinho que não voa, e os neozelandeses são chamados de kiwis!",
     {"sabia": "OS NEOZELANDESES SÃO CHAMADOS DE KIWIS"}),
    ("fr", "GALO", ["LEÃO", "CAVALO"], "Bora pra Europa!",
     "Galo! O galo aparece até no uniforme da seleção francesa!", {}),
    ("th", "ELEFANTE", ["TIGRE", "MACACO"], "Agora um país da Ásia!",
     "Elefante! Na Tailândia ele é sagrado e tem até feriado!", {}),
    ("mx", "ÁGUIA-REAL", ["TUCANO", "IGUANA"], "Olha bem a bandeira, que tem uma dica nela!",
     "Águia-real! Ela está no meio da bandeira do México, comendo uma cobra!", {}),
    ("gb-eng", "LEÃO", ["RAPOSA", "CAVALO"], "Agora a terra do futebol!",
     "Leão! Por isso a seleção inglesa é chamada de Três Leões!", {"sabia": "A SELEÇÃO É CHAMADA DE 'TRÊS LEÕES'"}),
    ("it", "LOBO", ["URSO-PARDO", "JAVALI"], "Agora a terra da pizza!",
     "Lobo! Na lenda, uma loba criou os fundadores de Roma!", {}),
    ("id", "DRAGÃO-DE-KOMODO", ["ORANGOTANGO", "TIGRE"], "Esse aqui parece de filme!",
     "Dragão-de-komodo! O maior lagarto do mundo só vive na Indonésia!",
     {"dica": ("Dica: é um réptil!", "É UM RÉPTIL")}),
    ("tz", "GIRAFA", ["ZEBRA", "LEÃO"], "Bora pra África!",
     "Girafa! A girafa é o animal nacional da Tanzânia!", {}),
    ("za", "SPRINGBOK", ["LEÃO", "ZEBRA"], "Essa tem a ver com esporte!",
     "Springbok! É uma gazela, e a seleção de rúgbi do país se chama Springboks!",
     {"sabia": "A SELEÇÃO DE RÚGBI SE CHAMA SPRINGBOKS"}),
    ("pe", "VICUNHA", ["LHAMA", "CAPIVARA"], "Cuidado, que essa tem pegadinha!",
     "Vicunha! Não é a lhama! A vicunha está no brasão do Peru!", {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("cl", "CONDOR", ["HARPIA", "LHAMA"], "Agora o país mais comprido do mundo!",
     "Condor! O condor-dos-Andes está no brasão do Chile!", {}),
    ("ar", "JOÃO-DE-BARRO", ["EMA", "BEIJA-FLOR"], "Agora os nossos vizinhos!",
     "João-de-barro! Na Argentina ele se chama hornero, e é a ave nacional!",
     {"dica": ("Dica: ele faz a casa de barro!", "FAZ A CASA DE BARRO")}),
    ("cr", "BICHO-PREGUIÇA", ["IGUANA", "TUCANO"], "Essa aqui é bem devagarinho!",
     "Bicho-preguiça! Virou símbolo nacional da Costa Rica em dois mil e vinte e um!", {}),
    ("gt", "QUETZAL", ["ARARA", "BEIJA-FLOR"], "Agora uma ave linda!",
     "Quetzal! Ele é tão importante que a moeda da Guatemala se chama quetzal!",
     {"sabia": "A MOEDA DA GUATEMALA SE CHAMA QUETZAL"}),
    ("pg", "AVE-DO-PARAÍSO", ["PAPAGAIO", "TUCANO"], "Olha a bandeira de novo!",
     "Ave-do-paraíso! Ela aparece em amarelo na bandeira!", {}),
    ("br", "SABIÁ-LARANJEIRA", ["TUCANO", "ARARA"], "Agora a mais importante: a ave símbolo do Brasil!",
     "Sabiá-laranjeira! Muita gente chuta tucano ou arara, mas a ave símbolo do Brasil é o sabiá!",
     {"aviso": "TEM PEGADINHA!", "suspense": True, "pergunta": "QUAL É A AVE SÍMBOLO DO BRASIL?"}),
    ("np", "VACA", ["TIGRE", "PANDA-VERMELHO"], "Olha essa bandeira diferente!",
     "Vaca! No Nepal, a vaca é o animal nacional e é sagrada!", {"aviso": "TEM PEGADINHA!"}),
    ("pa", "HARPIA", ["ÁGUIA-REAL", "CONDOR"], "Agora uma ave gigante!",
     "Harpia! É o gavião-real, uma das águias mais fortes do mundo!",
     {"dica": ("Dica: também vive na Amazônia!", "TAMBÉM VIVE NA AMAZÔNIA")}),
    ("mn", "CAVALO", ["CAMELO", "LOBO"], "Essa é do país de Gengis Khan!",
     "Cavalo! Na Mongólia tem mais cavalo do que gente!", {"sabia": "TEM MAIS CAVALO DO QUE GENTE"}),
    ("cd", "OCAPI", ["GIRAFA", "ZEBRA"], "Esse bicho é muito estranho!",
     "Ocapi! Parece uma zebra, mas é parente da girafa!", {"suspense": True}),
    ("bw", "ZEBRA", ["GIRAFA", "SPRINGBOK"], "Mais uma da África!",
     "Zebra! A zebra é o animal nacional de Botsuana, e as cores da bandeira lembram as listras dela!",
     {"sabia": "A BANDEIRA LEMBRA AS LISTRAS DA ZEBRA"}),
    ("bz", "ANTA", ["ONÇA-PINTADA", "CAPIVARA"], "Agora um país pequenininho!",
     "Anta! A anta é o animal nacional de Belize!", {}),
    ("kr", "TIGRE", ["PANDA", "URSO-PARDO"], "Essa é da terra do K-pop!",
     "Tigre! O tigre foi até mascote das Olimpíadas na Coreia!", {}),
    ("ug", "GROU-COROADO", ["AVESTRUZ", "TUCANO"], "A bandeira dá uma dica!",
     "Grou-coroado! Ele aparece no meio da bandeira de Uganda!", {}),
    ("dk", "CISNE", ["PATO", "GALO"], "Agora um país gelado da Europa!",
     "Cisne! O cisne-branco é a ave nacional da Dinamarca!", {}),
    ("jp", "FAISÃO-VERDE", ["GALO", "PAPAGAIO"], "Essa derruba muita gente!",
     "Faisão-verde! É a ave nacional do Japão!", {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("bt", "TAKIN", ["BISÃO", "CABRA"], "Agora um bicho que quase ninguém conhece!",
     "Takin! Ele só vive nas montanhas do Himalaia!",
     {"dica": ("Dica: parece uma mistura de vaca com cabra!", "MISTURA DE VACA COM CABRA")}),
    ("pk", "MARKHOR", ["CAMELO", "ALCE"], "Essa é pra quem manja de bicho!",
     "Markhor! É uma cabra selvagem com chifres em espiral!", {"suspense": True}),
    ("qa", "ÓRIX", ["CAMELO", "CABRA"], "Agora o país da Copa de dois mil e vinte e dois!",
     "Órix! O órix-da-arábia é o animal nacional do Catar!", {}),
    ("gb-sct", "UNICÓRNIO", ["CAVALO", "OVELHA"], "Valendo o título de mestre dos bichos!",
     "Unicórnio! É sério! O animal símbolo da Escócia é o unicórnio! Se acertou, você é fera!",
     {"final": True, "suspense": True, "aviso": "TEM PEGADINHA!"}),
]


def cartao_bandeira(cod, dst):
    """Cartão quadrado: bandeira grande no meio, com borda, sobre fundo branco."""
    from PIL import Image, ImageDraw
    S = 720
    img = Image.new("RGB", (S, S), (255, 255, 255))
    bd = Image.open(os.path.join(VIDEOS, "03-bandeiras-195", "bandeiras", cod + ".png")
                    if os.path.exists(os.path.join(VIDEOS, "03-bandeiras-195", "bandeiras", cod + ".png"))
                    else os.path.join(VIDEOS, "37-jogador-qual-pais", "bandeiras", cod + ".png")).convert("RGBA")
    bd.thumbnail((640, 560), Image.LANCZOS)
    x, y = (S - bd.width) // 2, (S - bd.height) // 2
    d = ImageDraw.Draw(img)
    if cod != "np":     # bandeira do Nepal não é retângulo
        d.rectangle([x - 5, y - 5, x + bd.width + 4, y + bd.height + 4], fill=(30, 40, 80))
    img.paste(bd, (x, y), bd)
    img.save(dst, quality=92)


def main():
    rnd = random.Random(40)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    pos[0], pos[1], pos[2] = 1, 2, 0
    fotos = os.path.join(HERE, "fotos")
    os.makedirs(fotos, exist_ok=True)
    cred13 = json.load(open(os.path.join(V13, "creditos.json"), encoding="utf-8"))
    por_arq13 = {c["arquivo"]: (k, c) for k, c in cred13.items()}
    arq_cred = os.path.join(HERE, "creditos.json")
    cred = json.load(open(arq_cred, encoding="utf-8")) if os.path.exists(arq_cred) else {}
    usados = set()
    R = []
    for n, (cod, certo, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certo)
        assert len(set(ops)) == 3, (n, ops)
        for a in ops:
            arq = FOTO[a] + ".jpg"
            usados.add(arq)
            if not os.path.exists(os.path.join(fotos, arq)) and arq in por_arq13:
                shutil.copy(os.path.join(V13, "fotos", arq), os.path.join(fotos, arq))
            if arq in por_arq13:
                k, c = por_arq13[arq]
                cred[k] = c
            if not os.path.exists(os.path.join(fotos, arq)):
                print("FALTA FOTO", a, arq, file=sys.stderr)
        band = f"bandeira-{cod}.jpg"
        cartao_bandeira(cod, os.path.join(fotos, band))
        nome, falado = PAISES[cod]
        fal = [o.lower() for o in ops]
        prep = PREP.get(cod, "do" if falado[-1] not in "a" else "da")
        r = {"n": n, "pergunta": ex.get("pergunta", "QUAL É O ANIMAL SÍMBOLO DESTE PAÍS?"), "pais": nome,
             "cod": cod, "foto": band, "foto_resposta": FOTO[certo] + ".jpg",
             "opcoes": ops, "fotos_opcoes": [FOTO[o] + ".jpg" for o in ops], "certa": pos[n - 1],
             "fala_q": f"{fq} Qual é o animal símbolo {prep} {falado}? "
                       f"{fal[0]}, {fal[1]} ou {fal[2]}?" if "pergunta" not in ex else
                       f"{fq} {fal[0]}, {fal[1]} ou {fal[2]}?",
             "fala_r": fr, "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo o título... o animal símbolo da Escócia é..."
        R.append(r)
    assert len(R) == 36 and len({r["cod"] for r in R}) == 36
    cred = {k: v for k, v in cred.items() if v["arquivo"] in usados}
    cred["Unicórnio"] = {"file": "Noto Color Emoji (Google)", "arquivo": "unicornio.jpg", "autor": "Google",
                         "lic": "Apache 2.0"}
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(cred, open(arq_cred, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
