"""Gera itens.json do vídeo 25 "Quiz de matemática do 6º ao 9º ano" (estilo mais humano, 2026-11-13).

36 perguntas próprias de matemática da escola, em 4 blocos (6º, 7º, 8º e 9º ano), do fácil ao difícil:
contas, frações, porcentagem, equações, potências, raízes, geometria. A imagem de cada pergunta é um cartão
com a conta/figura (desenhado pelo build, em cartoes/). Pergunta falada com entrada variada, reação de verdade,
dica/aviso/suspense/"você sabia?".
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
Q = "QUANTO É?"
X = "QUANTO VALE O X?"
# série, pergunta (topo), cartão (linhas; "^" = expoente), forma (figura opcional), certa, [erradas],
# fala da pergunta, fala da resposta, extras
P = [
    (6, Q, ["7 × 8"], None, "56", ["54", "63"], "Pra aquecer: quanto é sete vezes oito?",
     "Cinquenta e seis! Começou bem?", {"count": 4.0}),
    (6, Q, ["125 + 75"], None, "200", ["190", "210"], "Agora de cabeça: cento e vinte e cinco mais setenta e cinco?",
     "Duzentos! Essa foi rapidinha!", {"count": 4.0}),
    (6, Q, ["100 − 37"], None, "63", ["73", "67"], "Cem menos trinta e sete?",
     "Sessenta e três!", {"count": 5.0}),
    (6, Q, ["144 ÷ 12"], None, "12", ["14", "11"], "Cento e quarenta e quatro dividido por doze?",
     "Doze! Doze vezes doze dá cento e quarenta e quatro!", {}),
    (6, Q, ["2^3"], None, "8", ["6", "9"], "Cuidado, que essa tem pegadinha! Quanto é dois ao cubo?",
     "Oito! Dois vezes dois vezes dois. Quem disse seis caiu na pegadinha!", {"aviso": "TEM PEGADINHA!"}),
    (6, "QUAL É O MAIOR?", ["0,5   0,25   0,8"], None, "0,8", ["0,5", "0,25"],
     "Qual desses números é o maior?", "Zero vírgula oito! Oitenta centavos é mais que cinquenta!", {}),
    (6, "QUANTOS MINUTOS?", ["2 h 30 min", "= ? min"], None, "150", ["130", "230"],
     "Duas horas e meia têm quantos minutos?", "Cento e cinquenta minutos!",
     {"sabia": "Um dia inteiro tem 1.440 minutos."}),
    (6, "MENOR MÚLTIPLO COMUM", ["MMC (4, 6)"], None, "12", ["24", "10"],
     "Qual é o menor número que é múltiplo de quatro e de seis ao mesmo tempo?", "Doze! Quatro vezes três e seis vezes dois!",
     {"dica": ("Dica: é menor que vinte!", "É MENOR QUE 20")}),
    (6, "QUAL É O PERÍMETRO?", ["lado = 5 cm"], "quadrado", "20 cm", ["25 cm", "10 cm"],
     "Esse quadrado tem cinco centímetros de lado. Qual é o perímetro?",
     "Vinte centímetros! Perímetro é a volta toda. Vinte e cinco seria a área!", {"aviso": "PERÍMETRO OU ÁREA?"}),
    (7, Q, ["−3 + 8"], None, "5", ["−5", "11"], "Agora o sétimo ano, com números negativos! Menos três mais oito?",
     "Cinco positivo!", {}),
    (7, Q, ["(−4) × (−5)"], None, "20", ["−20", "−9"], "Essa aqui derruba muita gente! Menos quatro vezes menos cinco?",
     "Vinte positivo! Menos com menos dá mais!", {"aviso": "DERRUBA MUITA GENTE!"}),
    (7, X, ["x + 7 = 15"], None, "8", ["22", "7"], "Achou o xis? Xis mais sete igual a quinze.",
     "Xis vale oito! Oito mais sete, quinze!", {}),
    (7, Q, ["10% de 250"], None, "25", ["50", "15"], "Quanto é dez por cento de duzentos e cinquenta?",
     "Vinte e cinco! Dez por cento é só dividir por dez.", {}),
    (7, X, ["2x = 18"], None, "9", ["16", "36"], "Dois xis igual a dezoito. Quanto vale xis?",
     "Nove!", {}),
    (7, "SOMA DOS ÂNGULOS?", ["a + b + c = ?"], "triangulo", "180°", ["360°", "90°"],
     "Quanto dá a soma dos três ângulos de um triângulo?", "Cento e oitenta graus! Em qualquer triângulo!",
     {"sabia": "No quadrado e no retângulo, a soma dos ângulos dá 360°."}),
    (7, Q, ["1/2 + 1/4"], None, "3/4", ["2/6", "2/4"], "Fração! Um meio mais um quarto?",
     "Três quartos! Um meio é a mesma coisa que dois quartos. Quem somou em cima e embaixo errou!",
     {"aviso": "TEM PEGADINHA!", "suspense": True}),
    (7, "QUANTO CUSTAM 5?", ["3 lápis = R$ 6", "5 lápis = ?"], None, "R$ 10", ["R$ 8", "R$ 12"],
     "Se três lápis custam seis reais, quanto custam cinco lápis?", "Dez reais! Cada lápis custa dois.", {}),
    (7, Q, ["−10 − 5"], None, "−15", ["−5", "15"], "Menos dez menos cinco?",
     "Menos quinze! Quem deve dez e gasta mais cinco, fica devendo quinze!",
     {"dica": ("Dica: pensa em dinheiro devendo!", "PENSA EM DÍVIDA")}),
    (8, Q, ["√81"], None, "9", ["8", "18"], "Bora pro oitavo ano! Qual é a raiz quadrada de oitenta e um?",
     "Nove! Nove vezes nove, oitenta e um.", {}),
    (8, Q, ["(−2)^2"], None, "4", ["−4", "−2"], "Olha os parênteses! Menos dois, ao quadrado?",
     "Quatro positivo! Com parênteses, o sinal também vai ao quadrado.", {"aviso": "TEM PEGADINHA!"}),
    (8, X, ["3x − 4 = 11"], None, "5", ["3", "7"], "Três xis menos quatro igual a onze. Quanto vale xis?",
     "Xis vale cinco! Três vezes cinco, quinze, menos quatro, onze!",
     {"dica": ("Dica: primeiro passa o quatro pro outro lado!", "PASSA O 4 PRO OUTRO LADO")}),
    (8, "QUE FRAÇÃO É ESSA?", ["0,25"], None, "1/4", ["1/25", "2/5"], "Zero vírgula vinte e cinco é igual a que fração?",
     "Um quarto! Tipo vinte e cinco centavos de um real.", {}),
    (8, "QUAL É A ÁREA?", ["8 cm × 3 cm"], "retangulo", "24 cm²", ["22 cm²", "11 cm²"],
     "Um retângulo de oito por três centímetros. Qual é a área?",
     "Vinte e quatro centímetros quadrados! Vinte e dois seria o perímetro.", {}),
    (8, Q, ["10^0"], None, "1", ["0", "10"], "Essa parece fácil, mas não é. Quanto é dez elevado a zero?",
     "Um! Todo número, menos o zero, elevado a zero dá um!",
     {"aviso": "PARECE FÁCIL...", "suspense": True, "sabia": "Qualquer número diferente de zero elevado a zero dá 1."}),
    (8, "PRODUTO NOTÁVEL", ["(x + 3)^2"], None, "x² + 6x + 9", ["x² + 9", "x² + 3x + 9"],
     "Produto notável! Xis mais três, tudo ao quadrado. Qual é a resposta?",
     "Xis ao quadrado, mais seis xis, mais nove! Não esquece o dobro do primeiro vezes o segundo!",
     {"aviso": "TEM PEGADINHA!", "falar_ops": False}),
    (8, "QUAL É A MÉDIA?", ["6, 7 e 8"], None, "7", ["21", "6,5"], "Qual é a média de seis, sete e oito?",
     "Sete! Soma tudo, vinte e um, e divide por três.", {}),
    (8, "QUANTOS GRAUS?", ["ângulo reto"], "angulo", "90°", ["180°", "45°"], "Pra respirar: um ângulo reto mede quantos graus?",
     "Noventa graus! Igual o canto de uma folha de caderno.", {}),
    (9, X, ["x^2 = 49"], None, "7 e −7", ["Só 7", "24,5"],
     "Agora o nono ano, o mais difícil! Xis ao quadrado igual a quarenta e nove. Quanto vale xis?",
     "Sete ou menos sete! Os dois, ao quadrado, dão quarenta e nove.",
     {"suspense": True, "falar_ops": False}),
    (9, "QUANTO MEDE A HIPOTENUSA?", ["catetos 3 e 4"], "pitagoras", "5", ["7", "6"],
     "Triângulo retângulo com catetos três e quatro. Quanto mede a hipotenusa?", "Cinco! O famoso três, quatro, cinco!",
     {"sabia": "É o Teorema de Pitágoras: a² + b² = c²."}),
    (9, "QUE TIPO DE NÚMERO É?", ["√2"], None, "Irracional", ["Racional", "Inteiro"],
     "A raiz quadrada de dois é um número de que tipo?",
     "Irracional! As casas depois da vírgula nunca acabam e nunca se repetem.",
     {"dica": ("Dica: as casas depois da vírgula nunca acabam!", "AS CASAS DECIMAIS NUNCA ACABAM")}),
    (9, Q, ["2^5"], None, "32", ["10", "25"], "Dois elevado a cinco?",
     "Trinta e dois! Quem fez dois vezes cinco caiu na pegadinha!", {}),
    (9, "QUAIS SÃO AS RAÍZES?", ["x² − 5x + 6 = 0"], None, "2 e 3", ["1 e 6", "−2 e −3"],
     "Equação do segundo grau! Quais são as raízes dessa equação?",
     "Dois e três! Eles somam cinco e multiplicados dão seis.",
     {"dica": ("Dica: dois números que somam cinco e multiplicados dão seis!", "SOMAM 5 E MULTIPLICADOS DÃO 6"),
      "falar_ops": False}),
    (9, "QUANTO VALE O Y?", ["y = 2x + 1", "x = 4"], None, "9", ["7", "10"],
     "Na função y igual a dois xis mais um, quanto vale y quando xis é quatro?", "Nove! Dois vezes quatro, oito, mais um.", {}),
    (9, Q, ["0,1 × 0,1"], None, "0,01", ["0,1", "1"], "Cuidado! Zero vírgula um vezes zero vírgula um?",
     "Zero vírgula zero um! Um décimo de um décimo é um centésimo.", {"aviso": "TEM PEGADINHA!", "suspense": True}),
    (9, "QUANTO VALE O PI?", ["π ≈ ?"], None, "3,14", ["3,41", "2,71"], "Quanto vale o pi, mais ou menos?",
     "Três vírgula catorze!", {"sabia": "Em inglês, 14 de março se escreve 3/14: é o Dia do Pi!"}),
    (9, "SOMA DOS ÂNGULOS?", ["hexágono"], "hexagono", "720°", ["360°", "540°"],
     "Quanto dá a soma dos ângulos internos de um hexágono, que tem seis lados?",
     "Setecentos e vinte graus! Se você acertou essa, você é fera em matemática!",
     {"count": 9.0, "suspense": True, "final": True}),
]

FRACOES = {"3/4": "três quartos", "2/6": "dois sextos", "2/4": "dois quartos", "1/4": "um quarto",
           "1/25": "um vinte e cinco avos", "2/5": "dois quintos"}


def falar(o):
    """Como a voz fala a alternativa (o Edge lê "3/4" como data e "−5" sem o menos)."""
    if o in FRACOES:
        return FRACOES[o]
    o = o.replace("R$ ", "").replace("−", "menos ").replace(",", " vírgula ")
    if o.endswith("°"):
        return o[:-1] + " graus"
    if o.endswith(" cm²"):
        return o[:-4] + " centímetros quadrados"
    if o.endswith(" cm"):
        return o[:-3] + " centímetros"
    return o + (" reais" if o.isdigit() and "R$" in o else "")


def main():
    rnd = random.Random(25)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    pos[0] = 1
    R = []
    for n, (serie, perg, cartao, forma, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        if ex.get("falar_ops", True):
            fo = [("R$ " in o and o.replace("R$ ", "") + " reais") or falar(o) for o in ops]
            fq = f"{fq} {fo[0]}, {fo[1]} ou {fo[2]}?"
        r = {"n": n, "serie": serie, "pergunta": perg, "cartao": cartao, "forma": forma, "foto": f"m{n}.png",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": fq, "fala_r": fr, "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo o título de gênio da matemática... a resposta é..."
        R.append(r)
    assert len(R) == 36 and len({tuple(r["cartao"]) for r in R}) == 36
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
