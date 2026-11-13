"""Gera itens.json do vídeo 23 "Adivinhe o PAÍS pelo contorno do mapa" (estilo mais humano, 2026-11-13).

36 perguntas próprias, do fácil ao difícil: aparece o contorno do país (Natural Earth, domínio público,
desenhado por mapas.py) e 3 alternativas. Pergunta falada com entrada variada, reação de verdade na resposta,
dica/aviso/suspense/"você sabia?" em algumas (ver videos/modelo-opcoes/humano.py).
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))

# slug, certa, [erradas], fala da pergunta (entrada variada; as alternativas entram no fim), resposta falada, extras
P = [
    ("brasil", "Brasil", ["Argentina", "Colômbia"], "Pra aquecer, essa é de graça! Que país é esse?",
     "Brasil! Esse você conhece de olho fechado!", {"count": 4.0, "sabia": "O Brasil é o 5º maior país do mundo."}),
    ("italia", "Itália", ["Grécia", "Croácia"], "Agora olha essa bota! Que país é esse?",
     "Itália! A famosa bota da Europa!", {"count": 4.0}),
    ("australia", "Austrália", ["Nova Zelândia", "Madagascar"], "Esse aqui é um país inteiro e também um continente!",
     "Austrália! Terra dos cangurus!", {"count": 5.0}),
    ("chile", "Chile", ["Peru", "Equador"], "Bora pra América do Sul. Esse fininho aqui, qual é?",
     "Chile! O país mais comprido e fininho do mundo!", {"sabia": "O Chile tem mais de 4 mil km de norte a sul."}),
    ("estados-unidos", "Estados Unidos", ["Canadá", "México"], "Esse aparece em todo filme. Que país é esse?",
     "Estados Unidos! Sem o Alasca e o Havaí, pra ficar justo!", {}),
    ("argentina", "Argentina", ["Chile", "Paraguai"], "Vizinho nosso, hein! Qual é esse?",
     "Argentina! O rival do futebol!", {}),
    ("japao", "Japão", ["Coreia do Sul", "Filipinas"], "Agora uma da Ásia. Um monte de ilhas em fila... que país é esse?",
     "Japão! A terra do sol nascente!", {}),
    ("india", "Índia", ["Paquistão", "Bangladesh"], "Esse tem formato de triângulo pra baixo. Qual país é esse?",
     "Índia! O país com mais gente no mundo!", {}),
    ("mexico", "México", ["Guatemala", "Colômbia"], "Olha esse rabinho lá embaixo! Que país é esse?",
     "México! Tacos e mariachis!", {"dica": (None, "Dica: fica colado nos Estados Unidos!", "FICA COLADO NOS ESTADOS UNIDOS")}),
    ("reino-unido", "Reino Unido", ["Irlanda", "Islândia"], "Cuidado, que essa tem pegadinha! Que país é esse?",
     "Reino Unido! A ilha do lado, que fica de fora, é a Irlanda!", {"aviso": "TEM PEGADINHA!"}),
    ("franca", "França", ["Bélgica", "Alemanha"], "Esse aqui parece um hexágono. Qual país é?",
     "França! Os franceses chamam o país de hexágono mesmo!", {}),
    ("espanha", "Espanha", ["Portugal", "França"], "Agora o vizinho de Portugal. Que país é esse?",
     "Espanha! Ele fica com quase toda a península!", {}),
    ("china", "China", ["Mongólia", "Rússia"], "Esse é gigante e parece uma galinha! Que país é esse?",
     "China! Repara que parece mesmo uma galinha!", {}),
    ("africa-do-sul", "África do Sul", ["Namíbia", "Moçambique"], "Bora pra África. Esse fica lá na pontinha. Qual é?",
     "África do Sul! Lá teve a Copa de 2010!", {}),
    ("canada", "Canadá", ["Rússia", "Estados Unidos"], "Esse é o segundo maior país do mundo. Qual é?",
     "Canadá! Cheio de ilhas lá no norte gelado!", {}),
    ("portugal", "Portugal", ["Espanha", "Uruguai"], "Esse aqui é um retangulozinho na beira do mar. Que país é esse?",
     "Portugal! De onde veio a nossa língua!", {}),
    ("egito", "Egito", ["Líbia", "Sudão"], "Esse aqui é quase um quadrado. Que país é esse?",
     "Egito! A terra das pirâmides!", {"dica": (None, "Dica: lá tem as pirâmides!", "LÁ TEM AS PIRÂMIDES")}),
    ("russia", "Rússia", ["Canadá", "Cazaquistão"], "Esse aqui é o maior de todos. Qual é?",
     "Rússia! O maior país do planeta!", {"sabia": "A Rússia tem 11 fusos horários diferentes."}),
    ("madagascar", "Madagascar", ["Sri Lanka", "Cuba"], "Uma ilha enorme perto da África. Que país é esse?",
     "Madagascar! Igual o filme!", {}),
    ("uruguai", "Uruguai", ["Paraguai", "Bolívia"], "Essa aqui derruba muita gente! Vizinho do Rio Grande do Sul.",
     "Uruguai! Quem chutou Paraguai caiu!", {"aviso": "DERRUBA MUITA GENTE!", "suspense": True}),
    ("grecia", "Grécia", ["Turquia", "Croácia"], "Esse tem um montão de ilhas. Que país é esse?",
     "Grécia! São mais de seis mil ilhas!", {}),
    ("cuba", "Cuba", ["Jamaica", "República Dominicana"], "Bora pro Caribe. Que ilha é essa?",
     "Cuba! A maior ilha do Caribe!", {"dica": (None, "Dica: a capital é Havana!", "A CAPITAL É HAVANA")}),
    ("nova-zelandia", "Nova Zelândia", ["Filipinas", "Islândia"], "Duas ilhas compridas lá no fim do mundo. Qual é?",
     "Nova Zelândia! Vizinha da Austrália!", {"sabia": "Na Nova Zelândia tem mais ovelhas do que gente."}),
    ("alemanha", "Alemanha", ["Polônia", "Áustria"], "Agora uma do coração da Europa. Que país é esse?",
     "Alemanha! A do sete a um, né...", {}),
    ("peru", "Peru", ["Bolívia", "Equador"], "Vizinho do Brasil, lá do lado do Pacífico. Qual é?",
     "Peru! A terra de Machu Picchu!", {}),
    ("turquia", "Turquia", ["Irã", "Grécia"], "Esse é comprido, meio na Europa e meio na Ásia. Que país é?",
     "Turquia! Um pedacinho dela fica na Europa!", {"aviso": "PENSA BEM!"}),
    ("noruega", "Noruega", ["Suécia", "Finlândia"], "Olha esse litoral todo picotado! Que país é esse?",
     "Noruega! Esse picotado são os fiordes!", {"dica": (None, "Dica: é a terra dos fiordes!", "É A TERRA DOS FIORDES")}),
    ("colombia", "Colômbia", ["Venezuela", "Equador"], "Esse tem mar dos dois lados. Que país é esse?",
     "Colômbia! É o único da América do Sul com Pacífico e Caribe!", {}),
    ("islandia", "Islândia", ["Irlanda", "Nova Zelândia"], "Uma ilha gelada perto do Polo Norte. Qual é?",
     "Islândia! Terra de vulcões e geleiras!", {"suspense": True}),
    ("arabia-saudita", "Arábia Saudita", ["Irã", "Iraque"], "Agora uma do Oriente Médio. Que país é esse?",
     "Arábia Saudita! Quase tudo deserto!", {"sabia": "A Arábia Saudita não tem nenhum rio permanente."}),
    ("paraguai", "Paraguai", ["Uruguai", "Bolívia"], "Esse é vizinho do Paraná. Que país é esse?",
     "Paraguai! Um dos dois países da América do Sul sem mar!",
     {"dica": (None, "Dica: não tem mar!", "NÃO TEM MAR")}),
    ("vietna", "Vietnã", ["Laos", "Tailândia"], "Esse é comprido e curvado, lá na Ásia. Qual é?",
     "Vietnã! Parece um S, né?", {}),
    ("bolivia", "Bolívia", ["Paraguai", "Peru"], "Tem pegadinha de novo! Vizinho do Brasil, sem mar. Qual é?",
     "Bolívia! O outro país sem mar da América do Sul!", {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("polonia", "Polônia", ["Ucrânia", "Alemanha"], "Agora ficou difícil! Que país europeu é esse?",
     "Polônia! Se acertou essa, você manda bem!",
     {"dica": (None, "Dica: a capital é Varsóvia!", "A CAPITAL É VARSÓVIA")}),
    ("mongolia", "Mongólia", ["Cazaquistão", "China"], "Esse fica entre a China e a Rússia. Qual é?",
     "Mongólia! Terra de Gengis Khan!", {"sabia": "A Mongólia é o país com menos gente por quilômetro do mundo."}),
    ("croacia", "Croácia", ["Eslovênia", "Sérvia"], "Que país é esse, em forma de bumerangue?",
     "Croácia! Se você acertou essa, você é fera de verdade!", {"count": 9.0, "suspense": True, "final": True}),
]


def main():
    rnd = random.Random(23)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    pos[0] = 0   # a 1ª, de aquecimento, já na A
    R = []
    for n, (slug, certa, err, fq, fr, ex) in enumerate(P, 1):
        assert os.path.exists(os.path.join(HERE, "mapas", slug + ".jpg")), slug
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        r = {"n": n, "pergunta": "QUE PAÍS É ESSE?", "foto": slug + ".jpg", "opcoes": ops, "certa": pos[n - 1],
             "fala_q": f"{fq} {ops[0]}, {ops[1]} ou {ops[2]}?", "fala_r": fr, "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"][1], ex["dica"][2]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo o título de fera... a resposta é..."
        R.append(r)
    assert len({r["foto"] for r in R}) == len(R)
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas")


if __name__ == "__main__":
    main()
