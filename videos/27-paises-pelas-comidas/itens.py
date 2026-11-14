"""Gera itens.json do vídeo 27 "Adivinhe o país pela comida" (estilo mais humano, 2026-11-13).

36 perguntas próprias, do fácil ao difícil: aparece a foto real do prato (Wikimedia Commons; créditos em
creditos.json e na tela final) e 3 países como alternativas. Pergunta falada com entrada variada, reação de
verdade, dica/aviso/suspense/"você sabia?".
Uso: py -3 itens.py
"""
import json, os, random, re, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
INTRO = ["Ramen", "Churros", "Cachorro-quente", "Macaron"]   # só na intro, não nas perguntas

# prato, certa, [erradas], fala da pergunta, fala da resposta, extras
P = [
    ("Feijoada", "Brasil", ["Portugal", "Argentina"], "Pra aquecer, essa é de casa! De que país é esse prato?",
     "Brasil! A nossa feijoada!", {"count": 4.0}),
    ("Pizza", "Itália", ["Estados Unidos", "Grécia"], "Essa todo mundo ama. De que país vem a pizza?",
     "Itália! A pizza nasceu em Nápoles!", {"count": 4.0}),
    ("Sushi", "Japão", ["China", "Coreia do Sul"], "Bora pra Ásia! De que país é o sushi?",
     "Japão! O sushi!", {"count": 5.0}),
    ("Tacos", "México", ["Espanha", "Peru"], "Agora uma bem apimentada! De que país são os tacos?",
     "México! Os tacos!", {}),
    ("Croissant", "França", ["Bélgica", "Suíça"], "Cuidado, que essa tem pegadinha! Esse pão é famoso em que país?",
     "França! Mas o pãozinho em forma de lua veio da Áustria!",
     {"aviso": "TEM PEGADINHA!", "sabia": "O croissant ficou famoso na França, mas a ideia veio da Áustria."}),
    ("Paella", "Espanha", ["Portugal", "Itália"], "Arroz com frutos do mar numa panela enorme. De que país?",
     "Espanha! A paella, de Valência!", {}),
    ("Pastel de nata", "Portugal", ["Brasil", "Espanha"], "Esse docinho é famoso em que país?",
     "Portugal! O pastel de nata, de Lisboa!", {"sabia": "O pastel de nata foi criado por monges de um mosteiro de Lisboa."}),
    ("Hambúrguer", "Estados Unidos", ["Alemanha", "Inglaterra"], "Esse lanche ficou famoso no mundo todo por qual país?",
     "Estados Unidos! Mas o nome vem da cidade de Hamburgo, na Alemanha!", {"aviso": "PENSA BEM!"}),
    ("Fish and chips", "Reino Unido", ["Irlanda", "Austrália"], "Peixe frito com batata frita. De que país é esse clássico?",
     "Reino Unido! O fish and chips!", {}),
    ("Biryani", "Índia", ["Tailândia", "Turquia"], "Arroz bem temperado com especiarias. De que país?",
     "Índia! O biryani!", {}),
    ("Kimchi", "Coreia do Sul", ["Japão", "China"], "Essa conserva de repolho apimentada é de que país?",
     "Coreia do Sul! O kimchi!", {"dica": ("Dica: é o país do kpop!", "É O PAÍS DO K-POP")}),
    ("Pad thai", "Tailândia", ["Vietnã", "Indonésia"], "Macarrão de arroz frito com amendoim. De que país?",
     "Tailândia! O pad thai!", {}),
    ("Asado", "Argentina", ["Uruguai", "Chile"], "Esse churrasco é a paixão de qual vizinho nosso?",
     "Argentina! O asado!", {}),
    ("Ceviche", "Peru", ["México", "Colômbia"], "Peixe cru temperado com limão. De que país é esse prato?",
     "Peru! O ceviche!", {"sabia": "No ceviche, o limão é que \"cozinha\" o peixe."}),
    ("Döner kebab", "Turquia", ["Grécia", "Índia"], "Carne assada num espeto que gira. De que país?",
     "Turquia! O döner kebab!", {}),
    ("Pato de Pequim", "China", ["Japão", "Tailândia"], "Esse pato assado leva o nome da capital de um país. Qual?",
     "China! O pato de Pequim!", {}),
    ("Fondue", "Suíça", ["França", "Áustria"], "Queijo derretido pra mergulhar o pão. De que país?",
     "Suíça! O fondue!", {"aviso": "DERRUBA MUITA GENTE!"}),
    ("Pho", "Vietnã", ["Japão", "Coreia do Sul"], "Essa sopa de macarrão é de que país?",
     "Vietnã! O pho!", {"suspense": True}),
    ("Moussaka", "Grécia", ["Itália", "Turquia"], "Berinjela, carne e molho branco no forno. De que país?",
     "Grécia! A moussaka!", {}),
    ("Waffle belga", "Bélgica", ["Holanda", "Alemanha"], "Pra respirar: de que país é esse waffle famoso?",
     "Bélgica! O waffle belga!", {}),
    ("Goulash", "Hungria", ["Polônia", "Rússia"], "Um ensopado de carne com páprica. De que país?",
     "Hungria! O goulash!", {"dica": ("Dica: a capital é Budapeste!", "A CAPITAL É BUDAPESTE")}),
    ("Pierogi", "Polônia", ["Ucrânia", "Alemanha"], "Esses pasteizinhos cozidos são símbolo de que país?",
     "Polônia! Os pierogi!", {}),
    ("Bratwurst", "Alemanha", ["Áustria", "Suíça"], "Essa linguiça famosa é de que país?",
     "Alemanha! A bratwurst!", {}),
    ("Strudel", "Áustria", ["Alemanha", "Hungria"], "Torta de massa fininha recheada de maçã. De que país?",
     "Áustria! O strudel de Viena!", {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("Poutine", "Canadá", ["Estados Unidos", "França"], "Batata frita com queijo e molho por cima. De que país?",
     "Canadá! A poutine!", {}),
    ("Cuscuz marroquino", "Marrocos", ["Egito", "Brasil"], "Agora a África. Esse cuscuz é de que país?",
     "Marrocos! O cuscuz marroquino! Diferente do nosso, né?", {"aviso": "PENSA BEM!"}),
    ("Nasi goreng", "Indonésia", ["Malásia", "Filipinas"], "Arroz frito com ovo por cima. De que país?",
     "Indonésia! O nasi goreng!", {}),
    ("Stroopwafel", "Holanda", ["Bélgica", "Dinamarca"], "Biscoito com calda de caramelo no meio. De que país?",
     "Holanda! O stroopwafel!", {}),
    ("Pelmeni", "Rússia", ["Polônia", "China"], "Bolinhos de massa recheados de carne. De que país?",
     "Rússia! Os pelmeni!", {}),
    ("Chivito", "Uruguai", ["Argentina", "Paraguai"], "Esse sanduíche enorme é de um vizinho nosso. Qual?",
     "Uruguai! O chivito!", {"dica": ("Dica: a capital é Montevidéu!", "A CAPITAL É MONTEVIDÉU")}),
    ("Lamington", "Austrália", ["Nova Zelândia", "Inglaterra"], "Bolinho com chocolate e coco. De que país?",
     "Austrália! O lamington!", {}),
    ("Smørrebrød", "Dinamarca", ["Suécia", "Noruega"], "Agora ficou difícil! Pão preto com coisas por cima. De que país?",
     "Dinamarca! O smørrebrød!", {"aviso": "DERRUBA MUITA GENTE!"}),
    ("Injera", "Etiópia", ["Quênia", "Egito"], "Essa panqueca grandona é de que país africano?",
     "Etiópia! A injera!", {}),
    ("Ackee and saltfish", "Jamaica", ["Cuba", "México"], "Um prato do Caribe. De que país?",
     "Jamaica! Ackee com bacalhau!", {}),
    ("Bobotie", "África do Sul", ["Nigéria", "Marrocos"], "Carne moída com ovo assado por cima. De que país?",
     "África do Sul! O bobotie!", {"suspense": True}),
    ("Mansaf", "Jordânia", ["Egito", "Turquia"], "De que país é esse prato de arroz com cordeiro?",
     "Jordânia! O mansaf! Se acertou essa, você é fera!", {"count": 9.0, "suspense": True, "final": True}),
]


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def main():
    rnd = random.Random(27)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    pos[0], pos[1], pos[2] = 0, 2, 1
    R = []
    for n, (prato, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        r = {"n": n, "pergunta": ex.get("pergunta", "DE QUE PAÍS É ESSE PRATO?"), "prato": prato, "foto": slug(prato) + ".jpg",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": f"{fq} {ops[0]}, {ops[1]} ou {ops[2]}?", "fala_r": fr,
             "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo o título de chef do mundo... a resposta é..."
        R.append(r)
    assert len({r["foto"] for r in R}) == len(R) == 36
    assert not set(INTRO) & {r["prato"] for r in R}
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
