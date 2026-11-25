"""Gera itens.json do vídeo 55 "Adivinhe o ANIMAL pela FOTO 2" (estilo mais humano, layout modelo-opcoes).

36 animais NOVOS (nenhum é resposta do vídeo 13 nem do 40, menos na fase dos filhotes, que mostra o bebê),
em 4 FASES de 9: CONHECIDOS -> PARECIDOS (pegadinhas: alpaca x lhama, crocodilo x jacaré...) -> FILHOTES
(o filhote vira qual animal?) -> RAROS. Foto real inteira (Wikimedia Commons; créditos na tela final) e 3
alternativas. Fatos conferidos em 2026-11-25.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))

FASES = ["CONHECIDOS", "PARECIDOS", "FILHOTES", "RAROS"]
PERG = {"CONHECIDOS": ("QUE ANIMAL É ESSE?", "Que animal é esse?"),
        "PARECIDOS": ("NÃO CONFUNDA: QUEM É?", "Que animal é esse?"),
        "FILHOTES": ("ESSE FILHOTE VIRA QUAL ANIMAL?", "Esse filhote vai virar qual animal?"),
        "RAROS": ("QUE BICHO RARO É ESSE?", "Que bicho é esse?")}

# slug da foto, fase, certa, [2 erradas], entrada falada, fala da resposta, extras
P = [
    ("pinguim", "CONHECIDOS", "PINGUIM", ["PATO", "GAIVOTA"], "Pra começar, bem fácil!",
     "Pinguim! Ele não voa, mas nada rapidinho! Começou bem?", {"count": 4.0}),
    ("flamingo", "CONHECIDOS", "FLAMINGO", ["GARÇA", "CISNE"], "Essa é moleza!",
     "Flamingo! E ele fica rosa por causa do que come!", {"count": 4.0}),
    ("coruja", "CONHECIDOS", "CORUJA", ["GAVIÃO", "ÁGUIA"], "Mais uma pra aquecer!",
     "Coruja! Ela vira a cabeça quase de costas!", {"count": 5.0}),
    ("polvo", "CONHECIDOS", "POLVO", ["LULA", "ÁGUA-VIVA"], "Bora pro fundo do mar!",
     "Polvo! Oito braços e três corações!", {"sabia": "O POLVO TEM 3 CORAÇÕES!"}),
    ("pavao", "CONHECIDOS", "PAVÃO", ["PERU", "FAISÃO"], "Olha que cauda!",
     "Pavão! E quem tem essa cauda colorida é o macho!", {}),
    ("joaninha", "CONHECIDOS", "JOANINHA", ["VAGALUME", "CIGARRA"], "Agora um bichinho do jardim!",
     "Joaninha! Ela come os pulgões das plantas!", {}),
    ("morcego", "CONHECIDOS", "MORCEGO", ["RATO", "ESQUILO-VOADOR"], "Esse aqui só sai de noite!",
     "Morcego! O único mamífero que voa de verdade!", {}),
    ("camaleao", "CONHECIDOS", "CAMALEÃO", ["IGUANA", "LAGARTIXA"], "Repara nos olhos dele!",
     "Camaleão! Cada olho olha pra um lado!", {}),
    ("cavalo-marinho", "CONHECIDOS", "CAVALO-MARINHO", ["ENGUIA", "PEIXE-AGULHA"], "Agora um peixe diferentão!",
     "Cavalo-marinho! E quem fica grávido é o papai!", {"sabia": "O PAPAI É QUE FICA GRÁVIDO!"}),

    ("pelicano", "PARECIDOS", "PELICANO", ["CEGONHA", "GARÇA"], "Olha o tamanho desse bico!",
     "Pelicano! O bico dele vira uma rede de pesca!", {}),
    ("alpaca", "PARECIDOS", "ALPACA", ["LHAMA", "OVELHA"], "Cuidado, que essa engana muita gente!",
     "Alpaca! A lhama é maior e tem orelhas compridas, tipo banana!",
     {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("crocodilo", "PARECIDOS", "CROCODILO", ["JACARÉ", "LAGARTO"], "Olha o focinho dele!",
     "Crocodilo! O focinho é fino, e os dentes de baixo aparecem com a boca fechada!",
     {"aviso": "TEM PEGADINHA!", "dica": ("Dica: repara nos dentes de baixo!", "OLHA OS DENTES!")}),
    ("puma", "PARECIDOS", "PUMA", ["ONÇA-PINTADA", "LEOA"], "Agora um gatão das Américas!",
     "Puma! Também chamado de onça-parda!", {}),
    ("ourico", "PARECIDOS", "OURIÇO", ["PORCO-ESPINHO", "TATU"], "Esse aqui é espinhudo!",
     "Ouriço! O porco-espinho é bem maior e tem espinhos compridos!", {"aviso": "TEM PEGADINHA!"}),
    ("texugo", "PARECIDOS", "TEXUGO", ["GAMBÁ", "GUAXINIM"], "Olha a listra na cara!",
     "Texugo! Ele passa a vida cavando tocas!", {}),
    ("gnu", "PARECIDOS", "GNU", ["BÚFALO", "BISÃO"], "Esse vive na savana africana!",
     "Gnu! Eles atravessam a savana aos milhões!", {}),
    ("jaguatirica", "PARECIDOS", "JAGUATIRICA", ["ONÇA-PINTADA", "GUEPARDO"], "Agora um felino brasileiro!",
     "Jaguatirica! Ela é bem menor que a onça!", {"suspense": True}),
    ("lince", "PARECIDOS", "LINCE", ["PUMA", "GATO-DO-MATO"], "Repara nas orelhas!",
     "Lince! Olha os tufinhos pretos nas orelhas!", {}),

    ("girino", "FILHOTES", "SAPO", ["PEIXE", "SALAMANDRA"], "Começou a fase dos filhotes!",
     "Sapo! O girino perde o rabo e ganha perninhas!", {}),
    ("lagarta", "FILHOTES", "BORBOLETA", ["ABELHA", "MINHOCA"], "Essa é clássica!",
     "Borboleta! Depois do casulo, ela ganha asas!", {}),
    ("filhote-flamingo", "FILHOTES", "FLAMINGO", ["PATO", "GANSO"], "Essa aqui derruba muita gente!",
     "Flamingo! O filhote nasce cinzinha e só fica rosa depois!",
     {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("filhote-pinguim", "FILHOTES", "PINGUIM", ["CORUJA", "GAIVOTA"], "Olha que fofura!",
     "Pinguim! É um filhote de pinguim-imperador!", {}),
    ("filhote-foca", "FILHOTES", "FOCA", ["URSO-POLAR", "LONTRA"], "Esse nasceu na neve!",
     "Foca! O filhote nasce branquinho pra se esconder no gelo!", {}),
    ("filhote-cisne", "FILHOTES", "CISNE", ["PATO", "GANSO"], "Pensa bem nessa!",
     "Cisne! O patinho feio da história era um filhote de cisne!",
     {"dica": ("Dica: lembra da história do patinho feio?", "O PATINHO FEIO!")}),
    ("filhote-coruja", "FILHOTES", "CORUJA", ["GAVIÃO", "POMBO"], "Esse tá todo arrepiado!",
     "Coruja! Filhote de coruja-das-torres!", {}),
    ("filhote-canguru", "FILHOTES", "CANGURU", ["COALA", "RATO"], "Olha onde ele tá escondido!",
     "Canguru! O filhote se chama joey e mora na bolsa da mãe!", {"sabia": "O FILHOTE SE CHAMA JOEY!"}),
    ("filhote-avestruz", "FILHOTES", "AVESTRUZ", ["GALINHA", "PERU"], "Esse vai ficar enorme!",
     "Avestruz! A maior ave do mundo, e bota o maior ovo também!", {}),

    ("bico-de-sapato", "RAROS", "BICO-DE-SAPATO", ["PELICANO", "GARÇA"], "Agora só os raros! Olha a cara dele!",
     "Bico-de-sapato! Ele fica parado igual estátua pra pescar!", {}),
    ("macaco-narigudo", "RAROS", "MACACO-NARIGUDO", ["ORANGOTANGO", "BABUÍNO"], "Que nariz é esse?",
     "Macaco-narigudo! Ele só existe na ilha de Bornéu!", {}),
    ("quokka", "RAROS", "QUOKKA", ["MARMOTA", "CASTOR"], "Esse vive sorrindo!",
     "Quokka! Dizem que é o bicho mais feliz do mundo!", {}),
    ("dugongo", "RAROS", "DUGONGO", ["PEIXE-BOI", "FOCA"], "Cuidado com essa!",
     "Dugongo! Parente do peixe-boi, mas com o rabo igual de golfinho!",
     {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("saiga", "RAROS", "SAIGA", ["CABRA", "CERVO"], "Olha esse narigão!",
     "Saiga! Esse nariz filtra a poeira da estepe!", {}),
    ("caracal", "RAROS", "CARACAL", ["LINCE", "GATO-DO-MATO"], "Parece o lince, mas será?",
     "Caracal! Ele pula alto pra pegar passarinho no ar!", {"aviso": "TEM PEGADINHA!"}),
    ("peixe-lua", "RAROS", "PEIXE-LUA", ["ARRAIA", "BAIACU"], "Esse é gigante!",
     "Peixe-lua! Pode pesar mais que um carro!", {}),
    ("gerenuk", "RAROS", "GERENUK", ["GAZELA", "IMPALA"], "Repara no pescoço!",
     "Gerenuk! Ele fica em pé nas patas de trás pra comer folhas!",
     {"dica": ("Dica: o nome dele parece nome de robô!", "NOME ESQUISITO!")}),
    ("casuar", "RAROS", "CASUAR", ["EMA", "AVESTRUZ"], "Olha o capacete dele!",
     "Casuar! Uma das aves mais perigosas do mundo!", {}),
    ("fossa", "RAROS", "FOSSA", ["PUMA", "MANGUSTO"], "Esse vive em Madagascar!",
     "Fossa! O maior caçador de Madagascar!", {}),
    ("numbat", "RAROS", "NUMBAT", ["ESQUILO", "GAMBÁ"], "Esse come cupim!",
     "Numbat! Ele come até vinte mil cupins por dia!", {}),
    ("aye-aye", "RAROS", "AYE-AYE", ["TÁRSIO", "LÓRIS"], "",
     "Aye-aye! Ele bate na madeira com o dedo comprido pra achar larva! Se acertou essa, você é fera!",
     {"final": True, "suspense": True}),
]


def main():
    FOTOS = json.load(open(os.path.join(HERE, "fotos.json"), encoding="utf-8"))   # slug -> foto (as que vieram)
    itens = [p for p in P if p[0] in FOTOS]
    por_fase = {f: [p for p in itens if p[1] == f] for f in FASES}
    # 9 por fase; nos raros fica sempre o aye-aye no fim (última pergunta)
    raros = [p for p in por_fase["RAROS"] if p[0] != "aye-aye"][:8] + [p for p in por_fase["RAROS"] if p[0] == "aye-aye"]
    itens = por_fase["CONHECIDOS"][:9] + por_fase["PARECIDOS"][:9] + por_fase["FILHOTES"][:9] + raros
    rnd = random.Random(55)
    pos = [0, 1, 2] * 13
    rnd.shuffle(pos)
    pos[0], pos[1], pos[2] = 1, 2, 0
    R = []
    for n, (slug, fase, certa, err, ent, fr, ex) in enumerate(itens, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        falas = [o.lower() for o in ops]
        txt, falada = PERG[fase]
        if ex.get("final"):
            falada = "Que bicho é esse? Pouca gente no mundo já viu um!"
        r = {"n": n, "fase": fase, "pergunta": txt, "foto": FOTOS[slug], "opcoes": ops, "certa": pos[n - 1],
             "fala_q": f"{ent} {falada} {falas[0]}, {falas[1]} ou {falas[2]}?".strip(), "fala_r": fr,
             "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if not ex.get("final") else "Valendo o título de mestre dos bichos... a resposta é..."
        R.append(r)
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], {f: sum(r["fase"] == f for r in R) for f in FASES})


if __name__ == "__main__":
    main()
