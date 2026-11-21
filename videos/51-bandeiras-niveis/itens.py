"""Gera itens.json do vídeo 51 "BANDEIRAS: fácil, médio, difícil e impossível" (estilo mais humano, layout modelo-opcoes).

36 bandeiras em 4 NÍVEIS de 9 (placa do nível no cartão e tela de nível entre eles). 3 alternativas A/B/C;
do nível difícil em diante as erradas são bandeiras PARECIDAS (Chade x Romênia, Mônaco x Indonésia...).
Bandeiras: domínio público (PNGs do vídeo 03). Ordem e escolhas diferentes do vídeo 03 (195 bandeiras).
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
NIVEIS = ["FÁCIL", "MÉDIO", "DIFÍCIL", "IMPOSSÍVEL"]

# código da bandeira, certa, [2 erradas], fala da pergunta (entrada), fala da resposta, extras
P = [
    # ---------- FÁCIL ----------
    ("jp", "JAPÃO", ["CHINA", "COREIA DO SUL"], "Pra começar, essa é moleza! De qual país é essa bandeira?",
     "Japão! A bolinha vermelha é o sol nascente. Começou bem?", {"count": 4.0}),
    ("ca", "CANADÁ", ["ESTADOS UNIDOS", "SUÍÇA"], "Olha essa folha! Que país é esse?",
     "Canadá! A folha é de bordo, o símbolo deles.", {"count": 4.0}),
    ("ar", "ARGENTINA", ["URUGUAI", "GRÉCIA"], "Essa é dos nossos vizinhos! Que bandeira é essa?",
     "Argentina! Com o Sol de Maio no meio.", {"count": 5.0}),
    ("it", "ITÁLIA", ["MÉXICO", "IRLANDA"], "Verde, branco e vermelho... de qual país?",
     "Itália! Terra da pizza e do macarrão!", {}),
    ("us", "ESTADOS UNIDOS", ["REINO UNIDO", "LIBÉRIA"], "Cinquenta estrelinhas! Que país é esse?",
     "Estados Unidos! Uma estrela para cada estado.", {}),
    ("pt", "PORTUGAL", ["ESPANHA", "BRASIL"], "Essa tem tudo a ver com a gente! De qual país é?",
     "Portugal! Olha a esfera armilar no meio.", {}),
    ("de", "ALEMANHA", ["BÉLGICA", "ESPANHA"], "Preto, vermelho e amarelo! Qual é?",
     "Alemanha! Tetracampeã do mundo.", {}),
    ("cn", "CHINA", ["VIETNÃ", "JAPÃO"], "Vermelha com estrelas amarelas... que país é esse?",
     "China! Uma estrela grande e quatro pequenas.", {"sabia": "SÃO 5 ESTRELAS: 1 GRANDE E 4 PEQUENAS"}),
    ("fr", "FRANÇA", ["HOLANDA", "RÚSSIA"], "Última do nível fácil! De qual país é essa?",
     "França! Azul, branco e vermelho, em pé.", {}),
    # ---------- MÉDIO ----------
    ("kr", "COREIA DO SUL", ["JAPÃO", "COREIA DO NORTE"], "Essa tem um símbolo bem diferente no meio. Que país é?",
     "Coreia do Sul! O círculo do meio é o yin-yang deles.", {}),
    ("gr", "GRÉCIA", ["URUGUAI", "ISRAEL"], "Listras azuis e brancas com uma cruz. De onde é?",
     "Grécia! São nove listras.", {}),
    ("ch", "SUÍÇA", ["DINAMARCA", "ÁUSTRIA"], "Cuidado, que essa tem pegadinha! Cruz branca no vermelho. Qual país?",
     "Suíça! E ela é quadrada!", {"aviso": "TEM PEGADINHA!", "sabia": "A BANDEIRA DA SUÍÇA É QUADRADA"}),
    ("tr", "TURQUIA", ["TUNÍSIA", "PAQUISTÃO"], "Lua e estrela no vermelho. Que país é esse?",
     "Turquia! A da Tunísia tem a lua dentro de um círculo branco.", {}),
    ("in", "ÍNDIA", ["NÍGER", "IRLANDA"], "Laranja, branco e verde, com uma rodinha azul. De onde é?",
     "Índia! O país com mais gente no mundo.", {}),
    ("se", "SUÉCIA", ["NORUEGA", "FINLÂNDIA"], "Bora pra Escandinávia! Que bandeira é essa?",
     "Suécia! Cruz amarela no azul.", {}),
    ("au", "AUSTRÁLIA", ["NOVA ZELÂNDIA", "REINO UNIDO"], "Essa derruba muita gente! Estrelas no azul... qual é?",
     "Austrália! A da Nova Zelândia tem estrelas vermelhas.",
     {"aviso": "TEM PEGADINHA!", "dica": ("Dica: repara que as estrelas são brancas!", "ESTRELAS BRANCAS!")}),
    ("il", "ISRAEL", ["GRÉCIA", "ARGENTINA"], "Uma estrela azul no meio. De qual país?",
     "Israel! É a Estrela de Davi.", {}),
    ("za", "ÁFRICA DO SUL", ["JAMAICA", "QUÊNIA"], "A mais colorida até agora! De onde é essa?",
     "África do Sul! Seis cores numa bandeira só!", {}),
    # ---------- DIFÍCIL ----------
    ("ru", "RÚSSIA", ["SÉRVIA", "ESLOVÁQUIA"], "Branco, azul e vermelho, sem nenhum desenho. Qual país?",
     "Rússia! A maior do mundo em tamanho.", {}),
    ("no", "NORUEGA", ["ISLÂNDIA", "DINAMARCA"], "Olha bem essa cruz! Que país é?",
     "Noruega! A da Islândia é ao contrário: azul com cruz vermelha.", {"aviso": "TEM PEGADINHA!"}),
    ("pe", "PERU", ["CANADÁ", "ÁUSTRIA"], "Vermelho, branco e vermelho, em pé. De onde é?",
     "Peru! A da Áustria tem as faixas deitadas.", {}),
    ("eg", "EGITO", ["IRAQUE", "SÍRIA"], "Vermelho, branco e preto... qual desses?",
     "Egito! O desenho do meio é uma águia dourada.",
     {"dica": ("Dica: olha o pássaro dourado no meio!", "UMA ÁGUIA DOURADA!")}),
    ("be", "BÉLGICA", ["ALEMANHA", "ROMÊNIA"], "Preto, amarelo e vermelho, em pé. Qual país?",
     "Bélgica! As cores da Alemanha, só que em pé.", {}),
    ("hu", "HUNGRIA", ["BULGÁRIA", "ITÁLIA"], "Vermelho, branco e verde, deitadas. De qual país?",
     "Hungria! Vermelho em cima, verde embaixo.", {}),
    ("co", "COLÔMBIA", ["EQUADOR", "VENEZUELA"], "Agora um vizinho da América do Sul! Qual é?",
     "Colômbia! A do Equador tem um brasão no meio.", {}),
    ("nz", "NOVA ZELÂNDIA", ["AUSTRÁLIA", "FIJI"], "Lembra da Austrália? E essa aqui, de onde é?",
     "Nova Zelândia! Quatro estrelas vermelhas.", {}),
    ("cl", "CHILE", ["CUBA", "PANAMÁ"], "Uma estrela só, no cantinho azul. Que país?",
     "Chile! O país mais comprido do mundo.", {}),
    # ---------- IMPOSSÍVEL ----------
    ("mc", "MÔNACO", ["INDONÉSIA", "POLÔNIA"], "Começou o impossível! Vermelho em cima, branco embaixo. Qual é?",
     "Mônaco! A da Indonésia é igualzinha, só é mais comprida!", {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("ci", "COSTA DO MARFIM", ["IRLANDA", "NÍGER"], "Laranja, branco e verde, em pé. De onde é?",
     "Costa do Marfim! A da Irlanda começa pelo verde.", {}),
    ("gn", "GUINÉ", ["MALI", "SENEGAL"], "Vermelho, amarelo e verde. Qual país africano?",
     "Guiné! A do Mali é ao contrário: começa pelo verde.", {}),
    ("si", "ESLOVÊNIA", ["ESLOVÁQUIA", "RÚSSIA"], "Branco, azul e vermelho com um escudo. Qual desses?",
     "Eslovênia! O escudo tem uma montanha com três picos.", {"aviso": "TEM PEGADINHA!"}),
    ("lt", "LITUÂNIA", ["BOLÍVIA", "GANA"], "Amarelo, verde e vermelho. De onde é?",
     "Lituânia! A da Bolívia começa pelo vermelho.", {}),
    ("ht", "HAITI", ["LIECHTENSTEIN", "PANAMÁ"], "Azul e vermelho com um brasão. Que país é?",
     "Haiti! A de Liechtenstein tem uma coroa no lugar do brasão.", {}),
    ("bt", "BUTÃO", ["NEPAL", "SRI LANKA"], "Olha o bicho no meio dessa! De qual país?",
     "Butão! Um dragão branco no meio.", {"sabia": "BUTÃO SIGNIFICA TERRA DO DRAGÃO"}),
    ("ad", "ANDORRA", ["MOLDÁVIA", "ROMÊNIA"], "Azul, amarelo e vermelho com brasão. Qual é?",
     "Andorra! A da Moldávia tem uma águia no brasão.", {"suspense": True}),
    ("td", "CHADE", ["ROMÊNIA", "MOLDÁVIA"], "A mais difícil de todas! Azul, amarelo e vermelho, sem nada no meio. Qual país?",
     "Chade! Ela é quase igual à da Romênia, só o azul é mais escuro. Se acertou, você é fera!",
     {"final": True, "suspense": True}),
]
TOPO = ["DE QUAL PAÍS É ESSA BANDEIRA?", "QUE PAÍS É ESSE?", "DE ONDE É ESSA BANDEIRA?"]


def main():
    assert len(P) == 36 and len({p[0] for p in P}) == 36
    rnd = random.Random(51)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    pos[0], pos[1], pos[2] = 1, 0, 2
    for i in range(2, len(pos)):          # nunca 3 seguidas na mesma letra
        if pos[i] == pos[i - 1] == pos[i - 2]:
            j = next(j for j in range(i + 1, len(pos)) if pos[j] != pos[i])
            pos[i], pos[j] = pos[j], pos[i]
    R = []
    for n, (code, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        falas = [o.title().replace(" Do ", " do ").replace(" De ", " de ") for o in ops]
        r = {"n": n, "nivel": NIVEIS[(n - 1) // 9], "code": code, "pergunta": TOPO[n % 3], "foto": f"{code}.png",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": f"{fq} {falas[0]}, {falas[1]} ou {falas[2]}?",
             "fala_r": fr, "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if not ex.get("final") else "Valendo o título de mestre das bandeiras... a resposta é..."
        R.append(r)
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
