"""Gera itens.json do "Capitais do Brasil e do mundo" (vídeo 22).

36 perguntas próprias, do fácil ao difícil, alternando estado do Brasil e país: "Qual é a capital de...?" com a
foto real de um lugar famoso da capital (Wikimedia Commons; baixadas com automacao/fotos_wiki.py baixar
escolhas.json, créditos em creditos.json e na tela final). Diferente do vídeo 07 (estado pelo mapa).
Uso: py -3 itens.py
"""
import json, os, random, unicodedata, re

HERE = os.path.dirname(os.path.abspath(__file__))


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


# lugar (tela), "de/da/do ..." falado, capital certa, [erradas], resposta falada (reação curta)
P = [
    ("BRASIL", "do Brasil", "Brasília", ["Rio de Janeiro", "São Paulo"], "Brasília! Essa foi pra aquecer!"),
    ("FRANÇA", "da França", "Paris", ["Lyon", "Marselha"], "Paris, a cidade da Torre Eiffel!"),
    ("BAHIA", "da Bahia", "Salvador", ["Ilhéus", "Feira de Santana"], "Salvador! A primeira capital do Brasil!"),
    ("ITÁLIA", "da Itália", "Roma", ["Milão", "Veneza"], "Roma! Essa é a Fontana di Trevi!"),
    ("AMAZONAS", "do Amazonas", "Manaus", ["Parintins", "Belém"], "Manaus, com o Teatro Amazonas!"),
    ("GRÉCIA", "da Grécia", "Atenas", ["Esparta", "Olímpia"], "Atenas, com o Partenon lá no alto!"),
    ("MINAS GERAIS", "de Minas Gerais", "Belo Horizonte", ["Uberlândia", "Juiz de Fora"], "Belo Horizonte, uai!"),
    ("INGLATERRA", "da Inglaterra", "Londres", ["Manchester", "Liverpool"], "Londres, com o Big Ben!"),
    ("PERNAMBUCO", "de Pernambuco", "Recife", ["Olinda", "Caruaru"], "Recife! Olinda é vizinha, mas não é a capital!"),
    ("JAPÃO", "do Japão", "Tóquio", ["Osaka", "Quioto"], "Tóquio! Quioto já foi capital, mas hoje é Tóquio!"),
    ("RIO GRANDE DO SUL", "do Rio Grande do Sul", "Porto Alegre", ["Pelotas", "Caxias do Sul"], "Porto Alegre, bah!"),
    ("PORTUGAL", "de Portugal", "Lisboa", ["Porto", "Coimbra"], "Lisboa, com a Torre de Belém!"),
    ("CEARÁ", "do Ceará", "Fortaleza", ["Sobral", "Juazeiro do Norte"], "Fortaleza, terra do humor!"),
    ("ESPANHA", "da Espanha", "Madri", ["Barcelona", "Sevilha"], "Madri! Barcelona é famosa, mas a capital é Madri!"),
    ("PARANÁ", "do Paraná", "Curitiba", ["Londrina", "Maringá"], "Curitiba, com o Jardim Botânico!"),
    ("ALEMANHA", "da Alemanha", "Berlim", ["Munique", "Frankfurt"], "Berlim, com o Portão de Brandemburgo!"),
    ("PARÁ", "do Pará", "Belém", ["Santarém", "Marabá"], "Belém, com o mercado Ver-o-Peso!"),
    ("EGITO", "do Egito", "Cairo", ["Alexandria", "Luxor"], "O Cairo!"),
    ("SANTA CATARINA", "de Santa Catarina", "Florianópolis", ["Joinville", "Blumenau"], "Florianópolis! Joinville é a maior cidade, mas não é a capital!"),
    ("ESTADOS UNIDOS", "dos Estados Unidos", "Washington", ["Nova York", "Los Angeles"], "Washington! Pegadinha: não é Nova York!"),
    ("GOIÁS", "de Goiás", "Goiânia", ["Anápolis", "Rio Verde"], "Goiânia!"),
    ("RÚSSIA", "da Rússia", "Moscou", ["São Petersburgo", "Kazan"], "Moscou, com a Praça Vermelha!"),
    ("MARANHÃO", "do Maranhão", "São Luís", ["Imperatriz", "Caxias"], "São Luís, a ilha do amor!"),
    ("CHINA", "da China", "Pequim", ["Xangai", "Hong Kong"], "Pequim!"),
    ("ESPÍRITO SANTO", "do Espírito Santo", "Vitória", ["Vila Velha", "Serra"], "Vitória, que fica numa ilha!"),
    ("PERU", "do Peru", "Lima", ["Cusco", "Arequipa"], "Lima! Cusco já foi a capital dos incas!"),
    ("MATO GROSSO DO SUL", "do Mato Grosso do Sul", "Campo Grande", ["Dourados", "Corumbá"], "Campo Grande!"),
    ("CANADÁ", "do Canadá", "Ottawa", ["Toronto", "Vancouver"], "Ottawa! Toronto é maior, mas a capital é Ottawa!"),
    ("PARAÍBA", "da Paraíba", "João Pessoa", ["Campina Grande", "Patos"], "João Pessoa!"),
    ("TURQUIA", "da Turquia", "Ancara", ["Istambul", "Antália"], "Ancara! Quase todo mundo chuta Istambul!"),
    ("MATO GROSSO", "do Mato Grosso", "Cuiabá", ["Rondonópolis", "Sinop"], "Cuiabá!"),
    ("AUSTRÁLIA", "da Austrália", "Camberra", ["Sydney", "Melbourne"], "Camberra! Não é Sydney, hein!"),
    ("TOCANTINS", "do Tocantins", "Palmas", ["Araguaína", "Gurupi"], "Palmas, a capital mais nova do Brasil!"),
    ("ÍNDIA", "da Índia", "Nova Délhi", ["Mumbai", "Calcutá"], "Nova Délhi, com o Portão da Índia!"),
    ("RORAIMA", "de Roraima", "Boa Vista", ["Caracaraí", "Pacaraima"], "Boa Vista!"),
    ("RONDÔNIA", "de Rondônia", "Porto Velho", ["Ji-Paraná", "Ariquemes"], "Porto Velho! Se acertou essa, você é fera!"),
]


def main():
    rnd = random.Random(22)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    R = []
    for n, (lugar, de, certa, err, fala) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        assert os.path.exists(os.path.join(HERE, "fotos", slug(certa) + ".jpg")), certa
        R.append({"n": n, "lugar": lugar, "de": de, "pergunta": f"QUAL É A CAPITAL {de.upper()}?",
                  "foto": slug(certa) + ".jpg", "opcoes": ops, "certa": pos[n - 1], "fala": fala})
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas")


if __name__ == "__main__":
    main()
