"""Gera itens.json do vídeo 26 "Adivinhe o país pelo monumento" (estilo mais humano, 2026-11-13).

32 perguntas próprias, do fácil ao difícil: aparece a foto real do monumento (Wikimedia Commons; créditos em
creditos.json e na tela final) e 3 países como alternativas. Pergunta falada com entrada variada, reação de
verdade, dica/aviso/suspense/"você sabia?".
Uso: py -3 itens.py
"""
import json, os, random, re, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
INTRO = ["Ponte da Torre", "Abu Simbel", "Templo do Céu", "Portal da Índia"]   # só na intro, não nas perguntas

# monumento, certa, [erradas], fala da pergunta, fala da resposta, extras
P = [
    ("Cristo Redentor", "Brasil", ["Portugal", "Argentina"], "Pra aquecer, essa é de casa! Em que país fica esse monumento?",
     "Brasil! O Cristo Redentor, no Rio de Janeiro!", {"count": 4.0}),
    ("Torre Eiffel", "França", ["Itália", "Inglaterra"], "Essa todo mundo conhece. Em que país fica essa torre?",
     "França! A Torre Eiffel, em Paris!", {"count": 4.0}),
    ("Pirâmides de Gizé", "Egito", ["México", "Peru"], "Bora pro deserto! Em que país ficam essas pirâmides?",
     "Egito! As pirâmides de Gizé, com mais de quatro mil anos!", {"count": 5.0}),
    ("Coliseu", "Itália", ["Grécia", "Espanha"], "Aqui lutavam os gladiadores! Em que país fica?",
     "Itália! O Coliseu, em Roma!", {}),
    ("Estátua da Liberdade", "Estados Unidos", ["França", "Canadá"], "Cuidado, que essa tem pegadinha! Em que país fica essa estátua?",
     "Estados Unidos! Ela fica em Nova York, mas foi um presente da França!",
     {"aviso": "TEM PEGADINHA!", "sabia": "A Estátua da Liberdade foi um presente da França aos Estados Unidos."}),
    ("Big Ben", "Reino Unido", ["Irlanda", "Austrália"], "Olha esse relógio famoso! Em que país ele fica?",
     "Reino Unido! O Big Ben, em Londres!", {}),
    ("Taj Mahal", "Índia", ["Turquia", "Irã"], "Agora a Ásia. Em que país fica esse palácio branco?",
     "Índia! O Taj Mahal!", {"sabia": "O Taj Mahal foi construído por um imperador em homenagem à esposa."}),
    ("Muralha da China", "China", ["Japão", "Coreia do Sul"], "Essa aqui é enorme! Em que país fica?",
     "China! A Grande Muralha!", {}),
    ("Torre de Pisa", "Itália", ["França", "Espanha"], "Olha essa torre tortinha! Em que país ela fica?",
     "Itália! A Torre de Pisa!", {}),
    ("Ópera de Sydney", "Austrália", ["Nova Zelândia", "Reino Unido"], "Parece um monte de velas de barco! Em que país fica?",
     "Austrália! A Ópera de Sydney!", {}),
    ("Machu Picchu", "Peru", ["Bolívia", "México"], "Uma cidade antiga lá no alto das montanhas. Em que país?",
     "Peru! Machu Picchu, a cidade dos incas!", {}),
    ("Sagrada Família", "Espanha", ["Portugal", "Itália"], "Essa igreja tá em obra há mais de cem anos! Em que país fica?",
     "Espanha! A Sagrada Família, em Barcelona!", {"sabia": "A Sagrada Família começou a ser construída em 1882."}),
    ("Chichén Itzá", "México", ["Peru", "Egito"], "Pirâmide de novo... mas cuidado! Em que país fica essa?",
     "México! Chichén Itzá, dos maias! Quem disse Egito caiu na pegadinha!",
     {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("Portão de Brandemburgo", "Alemanha", ["Áustria", "Grécia"], "Agora a Europa. Em que país fica esse portão?",
     "Alemanha! O Portão de Brandemburgo, em Berlim!", {}),
    ("Partenon", "Grécia", ["Itália", "Turquia"], "Um templo antigo lá no alto. Em que país fica?",
     "Grécia! O Partenon, em Atenas!", {}),
    ("Torre de Belém", "Portugal", ["Brasil", "Espanha"], "Essa aqui derruba muita gente! Em que país fica a Torre de Belém?",
     "Portugal! Fica em Lisboa, não no Pará!", {"aviso": "DERRUBA MUITA GENTE!"}),
    ("Catedral de São Basílio", "Rússia", ["Turquia", "Ucrânia"], "Olha essas cúpulas coloridas! Em que país?",
     "Rússia! A Catedral de São Basílio, em Moscou!", {}),
    ("Petra", "Jordânia", ["Egito", "Arábia Saudita"], "Uma cidade inteira esculpida na pedra. Em que país?",
     "Jordânia! Petra!", {"dica": ("Dica: fica do lado de Israel!", "FICA DO LADO DE ISRAEL")}),
    ("Burj Khalifa", "Emirados Árabes", ["Catar", "Arábia Saudita"], "O prédio mais alto do mundo! Em que país fica?",
     "Emirados Árabes! O Burj Khalifa, em Dubai!", {"sabia": "O Burj Khalifa tem mais de 800 metros de altura."}),
    ("Obelisco de Buenos Aires", "Argentina", ["Uruguai", "Chile"], "Aqui pertinho do Brasil. Em que país fica esse obelisco?",
     "Argentina! O Obelisco de Buenos Aires!", {}),
    ("Moai", "Chile", ["Peru", "Nova Zelândia"], "Essas cabeças de pedra são famosas. Em que país elas ficam?",
     "Chile! Na Ilha de Páscoa, no meio do Pacífico!", {"aviso": "PENSA BEM!", "suspense": True}),
    ("Torre CN", "Canadá", ["Estados Unidos", "Austrália"], "Uma torre altíssima na América do Norte. Em que país?",
     "Canadá! A Torre CN, em Toronto!", {}),
    ("Santa Sofia", "Turquia", ["Grécia", "Egito"], "Já foi igreja e mesquita. Em que país fica?",
     "Turquia! Santa Sofia, em Istambul!", {"dica": ("Dica: a cidade é Istambul!", "A CIDADE É ISTAMBUL")}),
    ("Angkor Wat", "Camboja", ["Tailândia", "Vietnã"], "Um templo gigante no meio da floresta. Em que país?",
     "Camboja! Angkor Wat! Está até na bandeira de lá!", {"sabia": "Angkor Wat aparece desenhado na bandeira do Camboja."}),
    ("Alhambra", "Espanha", ["Marrocos", "Portugal"], "Um palácio antigo dos mouros. Em que país fica?",
     "Espanha! A Alhambra, em Granada!", {"aviso": "TEM PEGADINHA!"}),
    ("Golden Gate", "Estados Unidos", ["Canadá", "Reino Unido"], "Pra respirar: em que país fica essa ponte vermelha?",
     "Estados Unidos! A Golden Gate, em São Francisco!", {}),
    ("Torres Petronas", "Malásia", ["Singapura", "Indonésia"], "Duas torres gêmeas ligadas por uma ponte. Em que país?",
     "Malásia! As Torres Petronas!", {"dica": ("Dica: a capital é Kuala Lumpur!", "A CAPITAL É KUALA LUMPUR")}),
    ("Castelo de Neuschwanstein", "Alemanha", ["Áustria", "Suíça"], "Parece castelo de desenho animado! Em que país fica?",
     "Alemanha! Esse castelo inspirou o castelo da Cinderela!", {}),
    ("Atomium", "Bélgica", ["Holanda", "França"], "Olha essas bolas gigantes de metal! Em que país fica?",
     "Bélgica! O Atomium, em Bruxelas!", {"aviso": "DERRUBA MUITA GENTE!", "suspense": True}),
    ("Mont Saint-Michel", "França", ["Inglaterra", "Bélgica"], "Uma ilha com um castelo que a maré cerca. Em que país?",
     "França! O Mont Saint-Michel!", {}),
    ("Ponte Carlos", "República Tcheca", ["Hungria", "Polônia"], "Agora ficou difícil! Em que país fica essa ponte de pedra?",
     "República Tcheca! A Ponte Carlos, em Praga!", {}),
    ("Borobudur", "Indonésia", ["Índia", "Tailândia"], "Em que país fica esse templo gigante de pedra?",
     "Indonésia! Borobudur, o maior templo budista do mundo! Se acertou essa, você é fera!",
     {"count": 9.0, "suspense": True, "final": True}),
]


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def main():
    rnd = random.Random(26)
    pos = [0, 1, 2] * 11
    rnd.shuffle(pos)
    pos[0], pos[1], pos[2] = 0, 2, 1
    R = []
    for n, (mon, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        r = {"n": n, "pergunta": ex.get("pergunta", "EM QUE PAÍS FICA?"), "monumento": mon, "foto": slug(mon) + ".jpg",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": f"{fq} {ops[0]}, {ops[1]} ou {ops[2]}?", "fala_r": fr,
             "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo o título de fera da geografia... a resposta é..."
        R.append(r)
    assert len({r["foto"] for r in R}) == len(R) == 32
    assert not set(INTRO) & {r["monumento"] for r in R}
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
