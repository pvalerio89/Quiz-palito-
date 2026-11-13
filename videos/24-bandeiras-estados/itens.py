"""Gera itens.json do vídeo 24 "Bandeiras dos estados do Brasil" (estilo mais humano, 2026-11-13).

28 perguntas próprias (a do Brasil para aquecer + os 26 estados e o DF), do fácil ao difícil: aparece a bandeira
(SVG de domínio público do Wikimedia Commons, pelo pacote hata; créditos em creditos.json e na tela final) e
3 alternativas. Pergunta falada com entrada variada, reação de verdade, dica/aviso/suspense/"você sabia?".
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))

P = [
    ("br", "Brasil", ["Portugal", "Bolívia"], "Pra aquecer, essa é de graça! De que país é essa bandeira?",
     "Brasil! Essa é a nossa!", {"count": 4.0, "pergunta": "DE QUE PAÍS É ESSA BANDEIRA?"}),
    ("mg", "Minas Gerais", ["Goiás", "Bahia"], "Agora valendo, só estados! De qual estado é essa bandeira?",
     "Minas Gerais, uai! Com o triângulo dos inconfidentes!",
     {"count": 5.0, "sabia": "O lema em latim quer dizer: liberdade ainda que tardia."}),
    ("sp", "São Paulo", ["Paraná", "Rio de Janeiro"], "Olha essas listras pretas e brancas! Qual estado?",
     "São Paulo! Tem até o mapa do Brasil no cantinho!", {"count": 5.0}),
    ("rs", "Rio Grande do Sul", ["Santa Catarina", "Paraná"], "Bora pro Sul. Verde, vermelho e amarelo... qual é?",
     "Rio Grande do Sul, bah!", {"sabia": "A bandeira gaúcha vem da Revolução Farroupilha."}),
    ("ba", "Bahia", ["Sergipe", "Pernambuco"], "Agora uma do Nordeste. De qual estado é essa?",
     "Bahia! Com o triângulo branco no canto!", {}),
    ("pe", "Pernambuco", ["Paraíba", "Alagoas"], "Olha esse arco-íris! Qual estado é esse?",
     "Pernambuco! O arco-íris, o sol e a cruz!", {"sabia": "A bandeira de Pernambuco nasceu na revolução de 1817."}),
    ("pr", "Paraná", ["Santa Catarina", "São Paulo"], "Olha bem, que essa tem uma pista escondida! Qual é?",
     "Paraná! Tava escrito no meio da bola azul!", {}),
    ("rj", "Rio de Janeiro", ["Espírito Santo", "Minas Gerais"], "Azul e branco, com um brasão no meio. Qual estado?",
     "Rio de Janeiro! A Cidade Maravilhosa é a capital!", {}),
    ("am", "Amazonas", ["Pará", "Acre"], "Bora pra floresta. Muitas estrelinhas... qual estado é esse?",
     "Amazonas! O maior estado do Brasil!", {}),
    ("df", "Distrito Federal", ["Goiás", "Tocantins"], "Essa é a da capital do país! Qual é?",
     "Distrito Federal! Onde fica Brasília!", {}),
    ("ce", "Ceará", ["Piauí", "Maranhão"], "Essa lembra a bandeira do Brasil, hein! De qual estado é?",
     "Ceará! Muita gente confunde com a do Brasil!",
     {"dica": ("Dica: a capital é Fortaleza!", "A CAPITAL É FORTALEZA")}),
    ("go", "Goiás", ["Piauí", "Sergipe"], "Cuidado, que essa tem pegadinha! Listras verdes e amarelas...",
     "Goiás! Repara nas cinco estrelas do Cruzeiro do Sul!", {"aviso": "TEM PEGADINHA!", "suspense": True}),
    ("sc", "Santa Catarina", ["Rio Grande do Sul", "Paraná"], "Vermelho, branco e um losango verde. Qual estado?",
     "Santa Catarina! Terra de Florianópolis!", {}),
    ("es", "Espírito Santo", ["Rio de Janeiro", "Alagoas"], "Azul, branco e rosa! De qual estado é essa?",
     "Espírito Santo! A única com rosa!", {"sabia": "O lema TRABALHA E CONFIA está escrito na bandeira."}),
    ("pa", "Pará", ["Amapá", "Maranhão"], "Agora o Norte. Vermelho, branco e uma estrela azul. Qual é?",
     "Pará! Terra do açaí!", {}),
    ("ma", "Maranhão", ["Piauí", "Pará"], "Listras vermelhas, brancas e pretas. Qual estado é esse?",
     "Maranhão!", {"dica": ("Dica: a capital é São Luís!", "A CAPITAL É SÃO LUÍS")}),
    ("pb", "Paraíba", ["Pernambuco", "Rio Grande do Norte"], "Essa tem uma palavra escrita: nego! Qual estado é?",
     "Paraíba!", {"sabia": "O NEGO lembra o 'não' que a Paraíba disse em 1930."}),
    ("mt", "Mato Grosso", ["Mato Grosso do Sul", "Goiás"], "Azul, branco e uma estrela amarela no meio. Qual é?",
     "Mato Grosso! O do Pantanal!", {}),
    ("al", "Alagoas", ["Sergipe", "Pernambuco"], "Vermelho, branco e azul, com brasão. De qual estado é?",
     "Alagoas! Terra de praias lindas!", {}),
    ("pi", "Piauí", ["Goiás", "Maranhão"], "Pegadinha de novo! Listras verdes e amarelas, uma estrela só...",
     "Piauí! Não confunde com Goiás, hein!",
     {"aviso": "TEM PEGADINHA!", "suspense": True,
      "sabia": "A data na bandeira lembra a Batalha do Jenipapo, de 1823."}),
    ("ac", "Acre", ["Rondônia", "Amazonas"], "Amarelo, verde e uma estrela vermelha. Qual estado?",
     "Acre! Ele existe, sim!", {"dica": ("Dica: fica lá no extremo oeste!", "FICA NO EXTREMO OESTE")}),
    ("to", "Tocantins", ["Roraima", "Mato Grosso"], "Olha esse sol no meio! De qual estado é?",
     "Tocantins! O estado mais novo do Brasil!", {}),
    ("se", "Sergipe", ["Alagoas", "Goiás"], "Essa aqui derruba muita gente! Qual estado é esse?",
     "Sergipe! O menor estado do Brasil!", {"aviso": "DERRUBA MUITA GENTE!"}),
    ("ms", "Mato Grosso do Sul", ["Mato Grosso", "Tocantins"], "Verde, branco, azul e uma estrela. Qual é?",
     "Mato Grosso do Sul!", {"dica": ("Dica: a capital é Campo Grande!", "A CAPITAL É CAMPO GRANDE")}),
    ("rn", "Rio Grande do Norte", ["Paraíba", "Ceará"], "Verde, branco e um escudo amarelo. Qual estado é?",
     "Rio Grande do Norte! Terra de Natal!", {}),
    ("ro", "Rondônia", ["Roraima", "Acre"], "Agora ficou difícil! Azul, amarelo, verde e uma estrela branca...",
     "Rondônia! Se acertou essa, você manda bem!", {"aviso": "PENSA BEM!", "suspense": True}),
    ("ap", "Amapá", ["Roraima", "Pará"], "Essa tem um símbolo estranho no meio. Qual estado?",
     "Amapá!", {"dica": ("Dica: a capital é Macapá!", "A CAPITAL É MACAPÁ")}),
    ("rr", "Roraima", ["Rondônia", "Amapá"], "De qual estado é essa bandeira, com a estrela amarela gigante?",
     "Roraima! Se você acertou essa, você é fera de verdade!", {"count": 9.0, "suspense": True, "final": True}),
]


def main():
    rnd = random.Random(24)
    pos = [0, 1, 2] * 10
    rnd.shuffle(pos)
    pos[0] = 0   # a 1ª, de aquecimento, já na A
    R = []
    for n, (slug, certa, err, fq, fr, ex) in enumerate(P, 1):
        assert os.path.exists(os.path.join(HERE, "bandeiras", slug + ".jpg")), slug
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        r = {"n": n, "pergunta": ex.get("pergunta", "DE QUAL ESTADO É ESSA?"), "foto": slug + ".jpg", "opcoes": ops,
             "certa": pos[n - 1], "fala_q": f"{fq} {ops[0]}, {ops[1]} ou {ops[2]}?", "fala_r": fr,
             "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo o título de fera... a resposta é..."
        R.append(r)
    assert len({r["foto"] for r in R}) == len(R) == 28
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
