"""Gera itens.json do vídeo 32 "Quem jogou aqui?" — adivinhe o jogador pelo PAÍS + CLUBE (estilo mais humano).

36 perguntas próprias, do fácil ao difícil (ref. NaTraveQuiz, formato "jogador que já jogou"): o cartão mostra a
BANDEIRA do país do jogador + o ESCUDO de um clube onde ele já jogou; 3 jogadores como alternativas, e só um
deles é desse país E já jogou nesse clube (as erradas são do mesmo país OU do mesmo clube). Na resposta entra a
foto real (Wikimedia Commons, as mesmas do vídeo 19; créditos na tela final). Jogadores diferentes dos vídeos 21
e 31. Carreiras conferidas em 2026-11-15.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))

# nome, foto, (bandeira, país na tela, gentílico), (escudo, clube na tela, "no clube"), [2 erradas],
# entrada falada, fala da resposta, extras
P = [
    ("Vinícius Jr", "pe-vinicius-jr.jpg", ("br", "BRASIL", "brasileiro"), ("real-madrid", "REAL MADRID", "no Real Madrid"),
     ["Neymar", "Mbappé"], "Pra aquecer, uma bem fácil!",
     "Vinícius Júnior! O Neymar nunca jogou no Real, e o Mbappé é francês!", {"count": 4.0}),
    ("Salah", "pd-salah.jpg", ("eg", "EGITO", "egípcio"), ("liverpool", "LIVERPOOL", "no Liverpool"),
     ["Mané", "Firmino"], "Bora pra mais uma!",
     "Salah! O Rei do Egito!", {"count": 4.0}),
    ("Harry Kane", "ca-harry-kane.jpg", ("gb-eng", "INGLATERRA", "inglês"), ("bayern-de-munique", "BAYERN", "no Bayern de Munique"),
     ["Sterling", "Musiala"], "Agora um centroavante!",
     "Harry Kane! Saiu do Tottenham direto pro Bayern!", {"count": 5.0}),
    ("Lamine Yamal", "pd-lamine-yamal.jpg", ("es", "ESPANHA", "espanhol"), ("barcelona", "BARCELONA", "no Barcelona"),
     ["Nico Williams", "Raphinha"], "Essa é da nova geração!",
     "Lamine Yamal! A joia do Barcelona!", {}),
    ("Casemiro", "vol-casemiro.jpg", ("br", "BRASIL", "brasileiro"), ("manchester-united", "MAN. UNITED", "no Manchester United"),
     ["Fabinho", "Rashford"], "Agora um volante!",
     "Casemiro! Saiu do Real Madrid pro United!", {}),
    ("Van Dijk", "zag1-van-dijk.jpg", ("nl", "HOLANDA", "holandês"), ("liverpool", "LIVERPOOL", "no Liverpool"),
     ["De Ligt", "Konaté"], "Um paredão na defesa!",
     "Van Dijk! O capitão do Liverpool!", {}),
    ("Bellingham", "mei-bellingham.jpg", ("gb-eng", "INGLATERRA", "inglês"), ("borussia-dortmund", "DORTMUND", "no Borussia Dortmund"),
     ["Foden", "Haaland"], "Esse foi cedo pra Alemanha!",
     "Bellingham! Do Dortmund pro Real Madrid!", {}),
    ("Lewandowski", "ca-lewandowski.jpg", ("pl", "POLÔNIA", "polonês"), ("borussia-dortmund", "DORTMUND", "no Borussia Dortmund"),
     ["Szczęsny", "Reus"], "Mesmo clube, outro país!",
     "Lewandowski! Antes do Bayern e do Barça, ele brilhou no Dortmund!", {}),
    ("Martinelli", "joia-martinelli.jpg", ("br", "BRASIL", "brasileiro"), ("arsenal", "ARSENAL", "no Arsenal"),
     ["Antony", "Saka"], "Agora um ponta brasileiro!",
     "Gabriel Martinelli! Saiu do Ituano direto pro Arsenal!",
     {"sabia": "O Martinelli foi pro Arsenal sem nunca jogar num time grande do Brasil."}),
    ("Thiago Silva", "lzag-thiago-silva.jpg", ("br", "BRASIL", "brasileiro"), ("chelsea", "CHELSEA", "no Chelsea"),
     ["Marquinhos", "Lampard"], "Um zagueiro que jogou até depois dos quarenta!",
     "Thiago Silva! Campeão da Champions com o Chelsea!", {}),
    ("Ronaldinho", "ldez-ronaldinho.jpg", ("br", "BRASIL", "brasileiro"), ("psg", "PSG", "no PSG"),
     ["Kaká", "Beckham"], "Cuidado, que essa tem pegadinha!",
     "Ronaldinho! Antes do Barcelona, ele jogou no PSG!", {"aviso": "TEM PEGADINHA!"}),
    ("Pelé", "ldez-pele.jpg", ("br", "BRASIL", "brasileiro"), ("new-york-cosmos", "NY COSMOS", "no New York Cosmos"),
     ["Garrincha", "Beckenbauer"], "Agora um time dos Estados Unidos!",
     "Pelé! O Rei terminou a carreira no Cosmos!",
     {"sabia": "O Pelé jogou no New York Cosmos de 1975 a 1977."}),
    ("Oliver Kahn", "lgol-oliver-kahn.jpg", ("de", "ALEMANHA", "alemão"), ("bayern-de-munique", "BAYERN", "no Bayern de Munique"),
     ["Lehmann", "Robben"], "Agora um goleiro das antigas!",
     "Oliver Kahn! O Lehmann nunca jogou no Bayern!", {}),
    ("Eto'o", "lca-eto-o.jpg", ("cm", "CAMARÕES", "camaronês"), ("barcelona", "BARCELONA", "no Barcelona"),
     ["Drogba", "Henry"], "Bora pra África!",
     "Samuel Eto'o! Artilheiro do Barça!", {}),
    ("Savinho", "joia-savinho.jpg", ("br", "BRASIL", "brasileiro"), ("manchester-city", "MAN. CITY", "no Manchester City"),
     ["Richarlison", "Grealish"], "Essa é recente!",
     "Savinho! Brilhou no Girona e foi pro City!", {}),
    ("Bruno Fernandes", "dez-bruno-fernandes.jpg", ("pt", "PORTUGAL", "português"), ("sporting", "SPORTING", "no Sporting"),
     ["Bernardo Silva", "Gyökeres"], "Agora Portugal!",
     "Bruno Fernandes! Foi do Sporting pro Manchester United!", {}),
    ("Endrick", "joia-endrick.jpg", ("br", "BRASIL", "brasileiro"), ("palmeiras", "PALMEIRAS", "no Palmeiras"),
     ["Rodrygo", "Gustavo Gómez"], "Um time brasileiro agora!",
     "Endrick! Saiu do Palmeiras pro Real Madrid!", {}),
    ("Militão", "zag1-militao.jpg", ("br", "BRASIL", "brasileiro"), ("porto", "PORTO", "no Porto"),
     ["Gabriel Magalhães", "Luis Díaz"], "Essa aqui derruba muita gente.",
     "Éder Militão! Foi do São Paulo pro Porto antes do Real!", {}),
    ("Rúben Dias", "zag1-ruben-dias.jpg", ("pt", "PORTUGAL", "português"), ("benfica", "BENFICA", "no Benfica"),
     ["Cristiano Ronaldo", "Di María"], "Cuidado: tem português famoso aí no meio!",
     "Rúben Dias! O Cristiano Ronaldo nunca jogou no Benfica!", {"aviso": "TEM PEGADINHA!"}),
    ("Wirtz", "dez-wirtz.jpg", ("de", "ALEMANHA", "alemão"), ("bayer-leverkusen", "LEVERKUSEN", "no Bayer Leverkusen"),
     ["Kimmich", "Xhaka"], "Agora um meia alemão!",
     "Florian Wirtz! Campeão invicto com o Leverkusen!", {}),
    ("Modrić", "mei-modric.jpg", ("hr", "CROÁCIA", "croata"), ("tottenham", "TOTTENHAM", "no Tottenham"),
     ["Kovačić", "Son"], "Antes de ser lenda no Real, ele jogou na Inglaterra!",
     "Luka Modrić! Jogou quatro anos no Tottenham!", {}),
    ("Hakimi", "ld-hakimi.jpg", ("ma", "MARROCOS", "marroquino"), ("inter-de-milao", "INTER", "na Inter de Milão"),
     ["Ziyech", "Lautaro"], "Bora pra Itália!",
     "Hakimi! Foi campeão italiano com a Inter antes do PSG!", {}),
    ("Cafu", "llat-cafu.jpg", ("br", "BRASIL", "brasileiro"), ("roma", "ROMA", "na Roma"),
     ["Roberto Carlos", "Totti"], "Um lateral pentacampeão!",
     "Cafu! O capitão do penta jogou na Roma e no Milan!", {}),
    ("Bastoni", "zag2-bastoni.jpg", ("it", "ITÁLIA", "italiano"), ("inter-de-milao", "INTER", "na Inter de Milão"),
     ["Chiellini", "Çalhanoğlu"], "Um zagueiro italiano!",
     "Bastoni! O Chiellini foi ídolo da rival Juventus!", {}),
    ("Dibu Martínez", "gol-dibu-martinez.jpg", ("ar", "ARGENTINA", "argentino"), ("aston-villa", "ASTON VILLA", "no Aston Villa"),
     ["Dybala", "Watkins"], "Agora um goleiro campeão do mundo!",
     "Dibu Martínez! O goleiro da Argentina campeã de 2022!", {}),
    ("Nuno Mendes", "le-nuno-mendes.jpg", ("pt", "PORTUGAL", "português"), ("psg", "PSG", "no PSG"),
     ["Cancelo", "Mbappé"], "Um lateral português!",
     "Nuno Mendes! Do Sporting pro PSG!", {}),
    ("Romário", "lca-romario.jpg", ("br", "BRASIL", "brasileiro"), ("psv", "PSV", "no PSV"),
     ["Bebeto", "Van Nistelrooy"], "Agora a Holanda... mas o jogador é brasileiro!",
     "Romário! Fez chover de gol no PSV!", {"dica": ("Dica: ele foi o craque da Copa de 94.", "CRAQUE DA COPA DE 94!")}),
    ("Reece James", "ld-reece-james.jpg", ("gb-eng", "INGLATERRA", "inglês"), ("chelsea", "CHELSEA", "no Chelsea"),
     ["Alexander-Arnold", "Enzo Fernández"], "Um lateral inglês!",
     "Reece James! Cria da base do Chelsea!", {}),
    ("Robertson", "le-robertson.jpg", ("gb-sct", "ESCÓCIA", "escocês"), ("liverpool", "LIVERPOOL", "no Liverpool"),
     ["Tierney", "Mac Allister"], "Atenção pra bandeira, que essa é diferente!",
     "Andy Robertson! O escocês do Liverpool!", {"sabia": "A Escócia tem seleção própria, separada da Inglaterra."}),
    ("Ronald Araújo", "zag2-ronald-araujo.jpg", ("uy", "URUGUAI", "uruguaio"), ("barcelona", "BARCELONA", "no Barcelona"),
     ["Giménez", "Koundé"], "Bora pro Uruguai!",
     "Ronald Araújo! O xerife uruguaio do Barça!", {}),
    ("Valverde", "mei-valverde.jpg", ("uy", "URUGUAI", "uruguaio"), ("penarol", "PEÑAROL", "no Peñarol"),
     ["Bentancur", "Suárez"], "Mais uma do Uruguai, mas agora o clube é de lá!",
     "Fede Valverde! Começou no Peñarol! O Suárez é do rival Nacional!",
     {"dica": ("Dica: hoje ele joga no Real Madrid.", "HOJE NO REAL MADRID!")}),
    ("Grimaldo", "le-grimaldo.jpg", ("es", "ESPANHA", "espanhol"), ("benfica", "BENFICA", "no Benfica"),
     ["Jordi Alba", "Otamendi"], "Agora só pra quem entende de futebol!",
     "Grimaldo! Sete anos de Benfica antes do Leverkusen!", {"suspense": True}),
    ("Gerrard", "lmei-gerrard.jpg", ("gb-eng", "INGLATERRA", "inglês"), ("la-galaxy", "LA GALAXY", "no LA Galaxy"),
     ["Lampard", "Ibrahimović"], "Um ídolo inglês que foi pros Estados Unidos!",
     "Steven Gerrard! Saiu do Liverpool pro Galaxy! O Lampard foi pro New York City!", {"suspense": True}),
    ("Dembélé", "pd-dembele.jpg", ("fr", "FRANÇA", "francês"), ("rennes", "RENNES", "no Rennes"),
     ["Griezmann", "Mbappé"], "Essa é bem difícil!",
     "Dembélé! Começou no Rennes, antes do Dortmund!", {}),
    ("Carvajal", "ld-carvajal.jpg", ("es", "ESPANHA", "espanhol"), ("bayer-leverkusen", "LEVERKUSEN", "no Bayer Leverkusen"),
     ["Xabi Alonso", "Sergio Ramos"], "Cuidado, que essa tem pegadinha das grandes!",
     "Carvajal! Jogou um ano no Leverkusen! O Xabi Alonso foi técnico de lá, mas nunca jogou!",
     {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("Zico", "ldez-zico.jpg", ("br", "BRASIL", "brasileiro"), ("udinese", "UDINESE", "na Udinese"),
     ["Sócrates", "Falcão"], "Valendo o título de craque da bola: um brasileiro num time pequeno da Itália!",
     "Zico! O Galinho jogou duas temporadas na Udinese! Se acertou essa, você é fera!",
     {"final": True, "suspense": True}),
]


def main():
    rnd = random.Random(32)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    pos[0], pos[1], pos[2] = 2, 0, 1
    R = []
    for n, (nome, foto, pais, clube, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], nome)
        assert len(set(ops)) == 3, (n, ops)
        assert os.path.exists(os.path.join(HERE, "bandeiras", pais[0] + ".png")), pais
        assert os.path.exists(os.path.join(HERE, "escudos", clube[0] + ".png")), clube
        r = {"n": n, "pergunta": "QUEM JÁ JOGOU AQUI?", "jogador": nome, "foto": foto,
             "bandeira": pais[0], "pais": pais[1], "clube": clube[0], "clube_nome": clube[1],
             "opcoes": ops, "certa": pos[n - 1],
             "fala_q": f"{fq} Qual {pais[2]} já jogou {clube[2]}? {ops[0]}, {ops[1]} ou {ops[2]}?",
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
    assert len({(r["bandeira"], r["clube"]) for r in R}) == 36, "cartão repetido"
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
