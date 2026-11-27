"""Gera itens.json do vídeo 57 "O vídeo ACABA quando você ERRAR a bandeira" (formato SOBREVIVÊNCIA).

36 bandeiras cada vez mais difíceis. Errou uma, fim de jogo: o espectador comenta até onde chegou.
Contador de SEQUÊNCIA na tela (no lugar das bolinhas de pontos) e tela "AINDA VIVO?" antes das perguntas 10, 19 e 28.
Nenhuma bandeira é resposta do vídeo 51 (bandeiras em 4 níveis); PNGs de domínio público do vídeo 03.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
FIM = " Errou alguma? Fim de jogo! Comenta até onde chegou!"

# código da bandeira, certa, [2 erradas], fala da pergunta (entrada), fala da resposta, extras
P = [
    ("br", "BRASIL", ["ARGENTINA", "COLÔMBIA"], "Pra aquecer, essa é a nossa! De qual país é?",
     "Brasil! Ordem e Progresso! Primeira de pé!", {"count": 4.0}),
    ("es", "ESPANHA", ["PORTUGAL", "MÉXICO"], "Agora vamos pra Europa! Que bandeira é essa?",
     "Espanha! Com o brasão do ladinho.", {"count": 4.0}),
    ("gb", "REINO UNIDO", ["AUSTRÁLIA", "ESTADOS UNIDOS"], "Olha essas cruzes! De onde é?",
     "Reino Unido! Ela junta as cruzes da Inglaterra, da Escócia e da Irlanda.", {"count": 5.0}),
    ("mx", "MÉXICO", ["ITÁLIA", "IRLANDA"], "Verde, branco e vermelho, com um bicho no meio. Qual país?",
     "México! A águia está comendo uma cobra em cima de um cacto.", {}),
    ("uy", "URUGUAI", ["ARGENTINA", "GRÉCIA"], "Listras azuis e um sol no canto. De onde é?",
     "Uruguai! Nove listras e o Sol de Maio." + FIM, {}),
    ("nl", "HOLANDA", ["FRANÇA", "RÚSSIA"], "Vermelho, branco e azul, deitadas. Qual é?",
     "Holanda! A da França tem as faixas em pé.", {}),
    ("jm", "JAMAICA", ["ÁFRICA DO SUL", "BRASIL"], "Que bandeira diferente! De qual país?",
     "Jamaica! Ela não tem nada de vermelho, branco ou azul.",
     {"sabia": "É A ÚNICA BANDEIRA SEM VERMELHO, BRANCO OU AZUL"}),
    ("ie", "IRLANDA", ["ITÁLIA", "COSTA DO MARFIM"], "Cuidado, que essa tem pegadinha! Verde, branco e laranja. Qual país?",
     "Irlanda! A da Costa do Marfim começa pelo laranja.", {"aviso": "TEM PEGADINHA!"}),
    ("dk", "DINAMARCA", ["SUÍÇA", "NORUEGA"], "Cruz branca no vermelho, mais pro lado. De onde é?",
     "Dinamarca! Dizem que é a bandeira mais antiga ainda em uso.", {}),
    # ---------- depois de 9 seguidas ----------
    ("fi", "FINLÂNDIA", ["SUÉCIA", "GRÉCIA"], "Cruz azul no branco. Que país é esse?",
     "Finlândia! O azul dos lagos e o branco da neve.", {}),
    ("py", "PARAGUAI", ["HOLANDA", "CROÁCIA"], "Vermelho, branco e azul, com um desenho no meio. Qual desses?",
     "Paraguai! E a frente e o verso dela são diferentes!",
     {"sabia": "A BANDEIRA DO PARAGUAI TEM FRENTE E VERSO DIFERENTES"}),
    ("ve", "VENEZUELA", ["COLÔMBIA", "EQUADOR"], "Um vizinho nosso! Repara nas estrelas. Qual é?",
     "Venezuela! As estrelinhas formam um arco.", {}),
    ("pl", "POLÔNIA", ["INDONÉSIA", "MÔNACO"], "Essa derruba muita gente! Branco em cima, vermelho embaixo. Qual país?",
     "Polônia! A da Indonésia e a de Mônaco são ao contrário.", {"aviso": "TEM PEGADINHA!"}),
    ("at", "ÁUSTRIA", ["PERU", "LETÔNIA"], "Vermelho, branco e vermelho, deitadas. De onde é?",
     "Áustria! A do Peru tem as faixas em pé.", {}),
    ("vn", "VIETNÃ", ["CHINA", "MARROCOS"], "Uma estrela amarela no vermelho. Qual desses?",
     "Vietnã! Uma estrela só, bem no meio.", {}),
    ("ma", "MARROCOS", ["TURQUIA", "VIETNÃ"], "Agora a estrela é verde! De qual país?",
     "Marrocos! Uma estrela verde de cinco pontas.", {}),
    ("cu", "CUBA", ["PORTO RICO", "CHILE"], "Listras azuis e um triângulo vermelho. Que país é esse?",
     "Cuba! A de Porto Rico tem as cores trocadas.", {"aviso": "TEM PEGADINHA!"}),
    ("sa", "ARÁBIA SAUDITA", ["PAQUISTÃO", "ARGÉLIA"], "Toda verde, com uma frase escrita. De onde é?",
     "Arábia Saudita! Embaixo da frase tem uma espada.", {}),
    # ---------- depois de 18 seguidas ----------
    ("ua", "UCRÂNIA", ["SUÉCIA", "CAZAQUISTÃO"], "Azul em cima, amarelo embaixo. Qual país?",
     "Ucrânia! O azul do céu e o amarelo do trigo.", {}),
    ("hr", "CROÁCIA", ["SÉRVIA", "ESLOVÁQUIA"], "Vermelho, branco e azul, com um escudo. Qual desses?",
     "Croácia! O xadrez vermelho e branco é a marca dela.",
     {"dica": ("Dica: repara no xadrezinho do escudo!", "OLHA O XADREZ NO ESCUDO!")}),
    ("ng", "NIGÉRIA", ["ARGÉLIA", "IRLANDA"], "Verde, branco e verde, em pé. De onde é?",
     "Nigéria! O país com mais gente da África.", {}),
    ("ke", "QUÊNIA", ["JAMAICA", "SUDÃO DO SUL"], "Preto, vermelho e verde, com um escudo. Qual país africano?",
     "Quênia! No meio tem um escudo e duas lanças.", {}),
    ("is", "ISLÂNDIA", ["NORUEGA", "FINLÂNDIA"], "Olha bem as cores dessa cruz! De onde é?",
     "Islândia! A da Noruega é vermelha com a cruz azul.", {"aviso": "TEM PEGADINHA!"}),
    ("bo", "BOLÍVIA", ["GANA", "LITUÂNIA"], "Vermelho, amarelo e verde, deitadas. Qual desses?",
     "Bolívia! A da Lituânia começa pelo amarelo." + FIM, {}),
    ("pk", "PAQUISTÃO", ["ARGÉLIA", "TURQUIA"], "Lua e estrela, com uma faixa branca do lado. Que país?",
     "Paquistão! A da Turquia é toda vermelha.", {}),
    ("ec", "EQUADOR", ["COLÔMBIA", "VENEZUELA"], "Amarelo, azul e vermelho, com um brasão. Qual é?",
     "Equador! A da Colômbia é igual, só que sem o brasão.", {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("bg", "BULGÁRIA", ["HUNGRIA", "ITÁLIA"], "Branco, verde e vermelho, deitadas. De onde é?",
     "Bulgária! A da Hungria começa pelo vermelho.", {}),
    # ---------- depois de 27 seguidas ----------
    ("ro", "ROMÊNIA", ["CHADE", "MOLDÁVIA"], "Azul, amarelo e vermelho, sem nada no meio. Qual país?",
     "Romênia! A do Chade tem o azul mais escuro.", {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("lu", "LUXEMBURGO", ["HOLANDA", "PARAGUAI"], "Lembra da Holanda? E essa aqui, de onde é?",
     "Luxemburgo! O azul é mais clarinho que o da Holanda.",
     {"dica": ("Dica: olha como o azul é clarinho!", "O AZUL É MAIS CLARO!")}),
    ("id", "INDONÉSIA", ["MÔNACO", "POLÔNIA"], "Vermelho em cima, branco embaixo. Qual desses?",
     "Indonésia! A de Mônaco é igualzinha, só que mais curtinha.", {"aviso": "TEM PEGADINHA!"}),
    ("np", "NEPAL", ["BUTÃO", "SRI LANKA"], "Olha o formato dessa! De qual país?",
     "Nepal! A única bandeira de país que não é um retângulo.",
     {"sabia": "É A ÚNICA BANDEIRA DE PAÍS QUE NÃO É RETANGULAR"}),
    ("mn", "MONGÓLIA", ["CAZAQUISTÃO", "QUIRGUISTÃO"], "Vermelho, azul e vermelho, com um símbolo amarelo. De onde é?",
     "Mongólia! Esse símbolo amarelo se chama soyombo.", {}),
    ("sn", "SENEGAL", ["CAMARÕES", "GUINÉ"], "Verde, amarelo e vermelho, com uma estrela verde. Qual país?",
     "Senegal! A de Camarões tem a estrela amarela.", {"suspense": True}),
    ("ee", "ESTÔNIA", ["FINLÂNDIA", "BOTSUANA"], "Azul, preto e branco. Qual desses?",
     "Estônia! Um país pequenininho do norte da Europa.", {}),
    ("kz", "CAZAQUISTÃO", ["PALAU", "UCRÂNIA"], "Um sol e uma águia no azul. De onde é?",
     "Cazaquistão! O maior país do mundo sem saída pro mar.", {"sabia": "É O MAIOR PAÍS DO MUNDO SEM SAÍDA PARA O MAR"}),
    ("ml", "MALI", ["GUINÉ", "SENEGAL"], "A mais difícil de todas! Verde, amarelo e vermelho, sem nada no meio. Qual país?",
     "Mali! A da Guiné é ao contrário: começa pelo vermelho. Se chegou até aqui sem errar, você é lenda!",
     {"final": True, "suspense": True}),
]
TOPO = ["DE QUAL PAÍS É ESSA BANDEIRA?", "QUE PAÍS É ESSE?", "DE ONDE É ESSA BANDEIRA?"]
USADAS_51 = set("jp ca ar it us pt de cn fr kr gr ch tr in se au il za ru no pe eg be hu co nz cl mc ci gn si lt ht bt ad td".split())


def main():
    assert len(P) == 36 and len({p[0] for p in P}) == 36
    assert not USADAS_51 & {p[0] for p in P}, USADAS_51 & {p[0] for p in P}
    rnd = random.Random(57)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    pos[0], pos[1], pos[2] = 2, 0, 1
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
        r = {"n": n, "code": code, "pergunta": TOPO[n % 3], "foto": f"{code}.png",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": f"{fq} {falas[0]}, {falas[1]} ou {falas[2]}?",
             "fala_r": fr, "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "E a resposta é..." if not ex.get("final") else "Valendo a sobrevivência... a resposta é..."
        R.append(r)
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
