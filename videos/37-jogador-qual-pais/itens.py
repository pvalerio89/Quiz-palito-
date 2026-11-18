"""Gera itens.json do vídeo 37 "De qual PAÍS é esse JOGADOR?" (estilo mais humano).

36 perguntas próprias, do fácil ao impossível: o cartão mostra a FOTO REAL do jogador (Wikimedia Commons, as mesmas
do vídeo 19; créditos na tela final) e as 3 alternativas são PAÍSES, cada uma com a bandeira (domínio público, as do
vídeo 03). As difíceis são as "pegadinhas": jogador que nasceu num país e joga por outro (Hakimi, Musiala, Rüdiger,
Alphonso Davies, Declan Rice, Ibrahimović). Fatos conferidos em 2026-11-18.
Uso: py -3 itens.py   (copia fotos e bandeiras que faltarem)
"""
import json, os, random, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)

# código da bandeira: (nome na tela, nome falado)
PAISES = {
    "br": ("BRASIL", "Brasil"), "ar": ("ARGENTINA", "Argentina"), "pt": ("PORTUGAL", "Portugal"),
    "fr": ("FRANÇA", "França"), "eg": ("EGITO", "Egito"), "sa": ("ARÁBIA SAUDITA", "Arábia Saudita"),
    "no": ("NORUEGA", "Noruega"), "se": ("SUÉCIA", "Suécia"), "dk": ("DINAMARCA", "Dinamarca"),
    "kr": ("COREIA DO SUL", "Coreia do Sul"), "jp": ("JAPÃO", "Japão"), "cn": ("CHINA", "China"),
    "pl": ("POLÔNIA", "Polônia"), "de": ("ALEMANHA", "Alemanha"), "cz": ("REP. TCHECA", "República Tcheca"),
    "hr": ("CROÁCIA", "Croácia"), "rs": ("SÉRVIA", "Sérvia"), "si": ("ESLOVÊNIA", "Eslovênia"),
    "be": ("BÉLGICA", "Bélgica"), "nl": ("HOLANDA", "Holanda"), "co": ("COLÔMBIA", "Colômbia"),
    "ve": ("VENEZUELA", "Venezuela"), "ec": ("EQUADOR", "Equador"), "uy": ("URUGUAI", "Uruguai"),
    "py": ("PARAGUAI", "Paraguai"), "ma": ("MARROCOS", "Marrocos"), "es": ("ESPANHA", "Espanha"),
    "cm": ("CAMARÕES", "Camarões"), "ca": ("CANADÁ", "Canadá"), "gh": ("GANA", "Gana"),
    "us": ("ESTADOS UNIDOS", "Estados Unidos"), "sl": ("SERRA LEOA", "Serra Leoa"), "ng": ("NIGÉRIA", "Nigéria"),
    "ie": ("IRLANDA", "Irlanda"), "it": ("ITÁLIA", "Itália"), "ba": ("BÓSNIA", "Bósnia"),
    "ci": ("COSTA DO MARFIM", "Costa do Marfim"), "sn": ("SENEGAL", "Senegal"), "ch": ("SUÍÇA", "Suíça"),
    "at": ("ÁUSTRIA", "Áustria"), "ge": ("GEÓRGIA", "Geórgia"), "ru": ("RÚSSIA", "Rússia"),
    "ua": ("UCRÂNIA", "Ucrânia"), "sk": ("ESLOVÁQUIA", "Eslováquia"), "cl": ("CHILE", "Chile"),
    "gb-eng": ("INGLATERRA", "Inglaterra"), "gb-sct": ("ESCÓCIA", "Escócia"),
}

# jogador (nome do crédito), foto, país certo, [2 erradas], entrada falada, fala da resposta, extras
P = [
    ("Neymar", "pe-neymar.jpg", "br", ["ar", "pt"], "Pra começar, uma bem fácil!",
     "Brasil, claro! É o Neymar, o maior artilheiro da história da Seleção!", {"count": 4.0}),
    ("Messi", "dez-messi.jpg", "ar", ["es", "uy"], "Essa aqui todo mundo sabe!",
     "Argentina! É o Messi, campeão do mundo em dois mil e vinte e dois!", {"count": 4.0}),
    ("Cristiano Ronaldo", "ca-cristiano-ronaldo.jpg", "pt", ["es", "br"], "Mais uma pra aquecer!",
     "Portugal! O Cristiano Ronaldo nasceu na Ilha da Madeira!", {"count": 5.0}),
    ("Mbappé", "ca-mbappe.jpg", "fr", ["be", "cm"], "Agora um velocista!",
     "França! É o Mbappé, campeão do mundo em dois mil e dezoito!", {}),
    ("Salah", "pd-salah.jpg", "eg", ["ma", "sa"], "Esse aqui é rei no país dele!",
     "Egito! É o Mohamed Salah, o Rei do Egito!", {}),
    ("Haaland", "ca-haaland.jpg", "no", ["se", "dk"], "Agora um centroavante gigante!",
     "Noruega! É o Haaland, uma máquina de fazer gol!", {}),
    ("Harry Kane", "ca-harry-kane.jpg", "gb-eng", ["gb-sct", "ie"], "Bora pra Europa!",
     "Inglaterra! O Harry Kane é o maior artilheiro da história da seleção inglesa!", {}),
    ("Son", "pe-son.jpg", "kr", ["jp", "cn"], "Cuidado pra não confundir os vizinhos!",
     "Coreia do Sul! É o Son, ídolo do Tottenham!", {"dica": ("Dica: a capital é Seul!", "CAPITAL: SEUL")}),
    ("Lewandowski", "ca-lewandowski.jpg", "pl", ["de", "cz"], "Mais um matador!",
     "Polônia! Muita gente acha que ele é alemão, porque brilhou no Bayern!", {}),
    ("Modrić", "mei-modric.jpg", "hr", ["rs", "si"], "Esse aqui já foi o melhor do mundo!",
     "Croácia! É o Modric, o maestro croata!", {}),
    ("De Bruyne", "mei-de-bruyne.jpg", "be", ["nl", "de"], "Agora um gênio do passe!",
     "Bélgica! É o De Bruyne!", {}),
    ("Luis Díaz", "pe-luis-diaz.jpg", "co", ["ve", "ec"], "Bora pra América do Sul!",
     "Colômbia! É o Luis Díaz, que saiu do Liverpool pro Bayern!",
     {"dica": ("Dica: a capital é Bogotá!", "CAPITAL: BOGOTÁ")}),
    ("Valverde", "mei-valverde.jpg", "uy", ["ar", "py"], "Mais um sul-americano!",
     "Uruguai! É o Federico Valverde, do Real Madrid!", {}),
    ("Hakimi", "ld-hakimi.jpg", "ma", ["es", "fr"], "Cuidado, que essa tem pegadinha: ele nasceu em Madri!",
     "Marrocos! O Hakimi nasceu na Espanha, mas escolheu jogar por Marrocos!",
     {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("Lamine Yamal", "pd-lamine-yamal.jpg", "es", ["ma", "pt"], "Agora a joia da nova geração!",
     "Espanha! O Lamine Yamal foi campeão da Eurocopa com só dezessete anos!", {}),
    ("Bellingham", "mei-bellingham.jpg", "gb-eng", ["gb-sct", "us"], "Esse joga no Real Madrid!",
     "Inglaterra! É o Jude Bellingham!", {}),
    ("Kimmich", "vol-kimmich.jpg", "de", ["at", "ch"], "Agora um volante!",
     "Alemanha! É o Kimmich, do Bayern de Munique!", {}),
    ("Pedri", "mei-pedri.jpg", "es", ["pt", "it"], "Esse é baixinho, mas joga muito!",
     "Espanha! O Pedri é das Ilhas Canárias!", {}),
    ("Lautaro", "ca-lautaro.jpg", "ar", ["uy", "cl"], "Um artilheiro da Inter de Milão!",
     "Argentina! É o Lautaro Martínez!", {}),
    ("Van Dijk", "zag1-van-dijk.jpg", "nl", ["be", "de"], "Agora um paredão na defesa!",
     "Holanda! É o Van Dijk, capitão do Liverpool!", {}),
    ("Kvaratskhelia", "pe-kvaratskhelia.jpg", "ge", ["ru", "ua"], "Esse nome é difícil até de falar!",
     "Geórgia! O Kvaratskhelia é o grande craque da Geórgia!",
     {"dica": ("Dica: o país fica entre a Europa e a Ásia!", "ENTRE EUROPA E ÁSIA")}),
    ("Alphonso Davies", "le-alphonso-davies.jpg", "ca", ["gh", "us"], "Essa aqui engana muita gente!",
     "Canadá! O Alphonso Davies nasceu num campo de refugiados em Gana e cresceu no Canadá!",
     {"aviso": "TEM PEGADINHA!", "sabia": "NASCEU EM GANA, CRESCEU NO CANADÁ", "suspense": True}),
    ("Robertson", "le-robertson.jpg", "gb-sct", ["gb-eng", "ie"], "Agora um lateral do Liverpool!",
     "Escócia! O Robertson é o capitão da Escócia!", {}),
    ("Rüdiger", "zag1-rudiger.jpg", "de", ["sl", "fr"], "Olha a pegadinha de novo!",
     "Alemanha! O Rüdiger nasceu em Berlim, e a mãe dele é de Serra Leoa!", {"aviso": "TEM PEGADINHA!"}),
    ("Musiala", "dez-musiala.jpg", "de", ["gb-eng", "ng"], "Essa aqui derruba muita gente!",
     "Alemanha! O Musiala jogou na base da Inglaterra, mas escolheu a Alemanha!",
     {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("Declan Rice", "vol-declan-rice.jpg", "gb-eng", ["ie", "gb-sct"], "Mais uma pegadinha!",
     "Inglaterra! O Declan Rice chegou a jogar pela Irlanda antes de trocar pela Inglaterra!",
     {"aviso": "TEM PEGADINHA!"}),
    ("Tchouaméni", "vol-tchouameni.jpg", "fr", ["cm", "be"], "Mais um do Real Madrid!",
     "França! O Tchouaméni nasceu na França, filho de pais de Camarões!", {}),
    ("Gvardiol", "zag2-gvardiol.jpg", "hr", ["rs", "ba"], "Um zagueiro do Manchester City!",
     "Croácia! É o Gvardiol!", {}),
    ("Ødegaard", "mei-degaard.jpg", "no", ["dk", "se"], "Agora o capitão do Arsenal!",
     "Noruega! O Odegaard estreou na seleção com só quinze anos!",
     {"sabia": "ESTREOU NA SELEÇÃO COM 15 ANOS"}),
    ("Bastoni", "zag2-bastoni.jpg", "it", ["es", "ar"], "Um zagueiro canhoto da Inter!",
     "Itália! É o Bastoni!", {}),
    ("Eto'o", "lca-eto-o.jpg", "cm", ["ci", "sn"], "Agora só lendas do futebol!",
     "Camarões! O Samuel Eto'o foi eleito quatro vezes o melhor jogador da África!", {}),
    ("Ibrahimović", "lca-ibrahimovic.jpg", "se", ["ba", "hr"], "Essa lenda tem pegadinha!",
     "Suécia! O Ibrahimovic nasceu na Suécia, e os pais dele vieram da antiga Iugoslávia!",
     {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("Petr Čech", "lgol-petr-cech.jpg", "cz", ["sk", "pl"], "Um goleiro que jogava de capacete!",
     "República Tcheca! O Petr Cech usava capacete depois de uma lesão grave na cabeça!",
     {"dica": ("Dica: a capital é Praga!", "CAPITAL: PRAGA"), "sabia": "JOGAVA DE CAPACETE"}),
    ("Cruyff", "ldez-cruyff.jpg", "nl", ["be", "de"], "Uma lenda das antigas!",
     "Holanda! É o Johan Cruyff, o gênio do Carrossel Holandês!", {}),
    ("Zanetti", "llat-zanetti.jpg", "ar", ["it", "uy"], "Esse foi ídolo na Itália!",
     "Argentina! O Zanetti foi capitão da Inter por muitos anos, mas é argentino!", {}),
    ("Ronald Araújo", "zag2-ronald-araujo.jpg", "uy", ["br", "py"],
     "Valendo o título de craque: um zagueiro do Barcelona!",
     "Uruguai! É o Ronald Araújo! Muita gente acha que ele é brasileiro por causa do nome! Se acertou, você é fera!",
     {"final": True, "suspense": True}),
]


def main():
    rnd = random.Random(37)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    pos[0], pos[1], pos[2] = 1, 2, 0
    os.makedirs(os.path.join(HERE, "fotos"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "bandeiras"), exist_ok=True)
    cred19 = json.load(open(os.path.join(VIDEOS, "19-monte-seu-clube", "creditos.json"), encoding="utf-8"))
    cred, R = {}, []
    for n, (nome, foto, certo, err, fq, fr, ex) in enumerate(P, 1):
        src = os.path.join(VIDEOS, "19-monte-seu-clube", "fotos", foto)
        if not os.path.exists(os.path.join(HERE, "fotos", foto)):
            shutil.copy(src, os.path.join(HERE, "fotos", foto))
        cred[nome] = cred19[nome]
        cods = list(err)
        cods.insert(pos[n - 1], certo)
        for c in cods:
            dst = os.path.join(HERE, "bandeiras", c + ".png")
            if not os.path.exists(dst):
                shutil.copy(os.path.join(VIDEOS, "03-bandeiras-195", "bandeiras", c + ".png"), dst)
        ops = [PAISES[c][0] for c in cods]
        fal = [PAISES[c][1] for c in cods]
        assert len(set(cods)) == 3, (n, cods)
        r = {"n": n, "pergunta": "DE QUAL PAÍS É ESSE JOGADOR?", "jogador": nome, "foto": foto,
             "bandeiras": cods, "opcoes": ops, "certa": pos[n - 1],
             "fala_q": f"{fq} {fal[0]}, {fal[1]} ou {fal[2]}?",
             "fala_r": fr, "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo o título de craque... a resposta é..."
        R.append(r)
    assert len({r["foto"] for r in R}) == len(R) == 36
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(cred, open(os.path.join(HERE, "creditos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
