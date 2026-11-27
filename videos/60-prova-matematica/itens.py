"""Gera itens.json do vídeo 60 "Prova de Matemática do 3º ano" (estilo mais humano).

44 perguntas feitas SÓ com o conteúdo dos 2 PDFs que o Patrick mandou (2026-11-27): Folha de Reforço e Simulado
do 3º trimestre do 3º ano (operações com "vai um", conferir a conta do colega, subtrações, multiplicações, divisões,
problemas de duas operações, tabela de preços das sacolinhas, dinheiro de cabeça, unidades de medida, instrumentos,
tempo, figuras espaciais, pilhas de caixas, tabela de livros, sequências, quadrado mágico e problemas para fechar).
Nada de fora das folhas: só reformulado e combinado; as alternativas erradas imitam o erro do "vai um" que a folha
aponta. Do MÉDIO ao MUITO DIFÍCIL (3 níveis). Nunca nome de aluno, professora ou escola.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
CE = ["Certa", "Errada"]
# nível, pergunta (topo), cartão (linhas), certa, [erradas], fala da pergunta, fala da resposta, extras
# extras: count (s), fig (cubo/bloco/piramide desenhado no cartão), fala_ops {opção: como falar}, falar_ops,
#         aviso, suspense, final
P = [
    # ---------- MÉDIO ----------
    (2, "QUANTO DÁ?", ["147 + 286"], "433", ["423", "333"],
     "Pra aquecer, uma adição com vai um! Quanto dá cento e quarenta e sete mais duzentos e oitenta e seis?",
     "Quatrocentos e trinta e três! Sete mais seis é treze: escreve três e vai um.", {"count": 10.0}),
    (2, "O QUE ELA MEDE?", ["Para que serve", "a BALANÇA?"], "Medir a massa", ["Medir o tempo", "Medir a temperatura"],
     "Pra que serve a balança?",
     "Medir a massa! Por exemplo, a massa de uma melancia.", {}),
    (2, "COMPLETE!", ["1 km = ? m"], "1000 metros", ["100 metros", "10 metros"],
     "Um quilômetro tem quantos metros?",
     "Mil metros! Quilo quer dizer mil.", {}),
    (2, "QUANTAS FACES?", ["O CUBO tem", "quantas faces?"], "6 faces", ["4 faces", "8 faces"],
     "Quantas faces tem o cubo?",
     "Seis faces! E todas são quadradas.", {"fig": "cubo"}),
    (2, "QUANTO DÁ?", ["625 - 424"], "201", ["211", "101"],
     "Agora uma subtração. Seiscentos e vinte e cinco menos quatrocentos e vinte e quatro?",
     "Duzentos e um!", {"count": 10.0}),
    (2, "VEM DE ONDE?", ["A palavra", "DÚZIA vem de..."], "Doze", ["Dez", "Cem"],
     "A palavra dúzia vem de qual número?",
     "Doze! Dúzia vem de doze, dezena vem de dez e centena vem de cem.", {}),
    (2, "COMPLETE!", ["1 hora =", "? minutos"], "60 minutos", ["100 minutos", "30 minutos"],
     "Uma hora tem quantos minutos?",
     "Sessenta minutos!", {}),
    (2, "O QUE ELE MEDE?", ["Para que serve", "o TERMÔMETRO?"], "Medir a temperatura", ["Medir a massa", "Medir o comprimento"],
     "E o termômetro, mede o quê?",
     "A temperatura! Em graus Celsius, como a temperatura do ar na rua.", {}),
    (2, "QUANTO DÁ?", ["92 ÷ 4"], "23", ["22", "24"],
     "Noventa e dois dividido por quatro?",
     "Vinte e três! Vinte e três vezes quatro dá noventa e dois.", {"count": 10.0}),
    (2, "DINHEIRO DE CABEÇA", ["R$ 1,00", "- R$ 0,40"], "R$ 0,60", ["R$ 0,50", "R$ 0,70"],
     "De cabeça: um real menos quarenta centavos?",
     "Sessenta centavos! Um real tem cem centavos.",
     {"fala_ops": {"R$ 0,60": "sessenta centavos", "R$ 0,50": "cinquenta centavos", "R$ 0,70": "setenta centavos"}}),
    (2, "O QUE É?", ["Nome do \"bico\"?"], "Vértice", ["Face", "Aresta"],
     "Nas figuras espaciais, como se chama o bico, onde as arestas se encontram?",
     "Vértice! Aresta é a linha entre duas faces, e face é cada lado chapado.", {"fig": "cubo"}),
    (2, "COMPLETE!", ["1 dia =", "? horas"], "24 horas", ["12 horas", "60 horas"],
     "Um dia inteiro tem quantas horas?",
     "Vinte e quatro horas!", {}),
    (2, "QUAL O PADRÃO?", ["0 · 15 · 30 · ?"], "45", ["40", "35"],
     "Começando do zero e aumentando sempre quinze: zero, quinze, trinta... qual vem depois?",
     "Quarenta e cinco! Sempre mais quinze.", {}),
    (2, "O QUE ELE MEDE?", ["Para que serve", "o COPO MEDIDOR?"], "Medir a capacidade", ["Medir o tempo", "Medir a massa"],
     "E o copo medidor, serve pra medir o quê?",
     "A capacidade! Como a quantidade de leite de uma receita de bolo.", {}),
    # ---------- DIFÍCIL ----------
    (3, "QUANTO DÁ?", ["358 + 275"], "633", ["623", "533"],
     "Trezentos e cinquenta e oito mais duzentos e setenta e cinco?",
     "Seiscentos e trinta e três! Essa tem vai um duas vezes.", {"count": 10.0, "aviso": "TEM VAI UM!"}),
    (3, "CONFIRA A CONTA!", ["O colega fez:", "136 × 7 = 962"], "Errada, é 952", ["Certa", "Errada, é 972"],
     "O colega fez cento e trinta e seis vezes sete e escreveu novecentos e sessenta e dois. A conta tá certa?",
     "Errada! O certo é novecentos e cinquenta e dois. O erro foi no vai um.",
     {"count": 10.0, "aviso": "PEGADINHA!",
      "fala_ops": {"Errada, é 952": "errada, é novecentos e cinquenta e dois",
                   "Errada, é 972": "errada, é novecentos e setenta e dois"}}),
    (3, "QUANTO DÁ?", ["28 × 9"], "252", ["253", "242"],
     "Vinte e oito vezes nove?",
     "Duzentos e cinquenta e dois! Oito vezes nove é setenta e dois: escreve dois e guarda sete.", {"count": 10.0}),
    (3, "QUANTOS VÉRTICES?", ["PIRÂMIDE de", "base quadrada"], "5 vértices", ["4 vértices", "8 vértices"],
     "Quantos vértices tem a pirâmide de base quadrada?",
     "Cinco vértices! Quatro embaixo, na base, e um lá em cima.", {"fig": "piramide"}),
    (3, "COMPLETE!", ["1 kg e 400 g", "= ? g"], "1400 g", ["1040 g", "140 g"],
     "Um quilo e quatrocentos gramas é o mesmo que quantos gramas?",
     "Mil e quatrocentos gramas! Um quilo tem mil gramas.",
     {"fala_ops": {"1400 g": "mil e quatrocentos", "1040 g": "mil e quarenta", "140 g": "cento e quarenta"}}),
    (3, "COMPLETE!", ["3 m e 48 cm", "= ? cm"], "348 cm", ["3048 cm", "3480 cm"],
     "Três metros e quarenta e oito centímetros é o mesmo que quantos centímetros?",
     "Trezentos e quarenta e oito! Um metro tem cem centímetros.",
     {"fala_ops": {"348 cm": "trezentos e quarenta e oito", "3048 cm": "três mil e quarenta e oito",
                   "3480 cm": "três mil quatrocentos e oitenta"}}),
    (3, "QUANTO SOBROU?", ["Tinha R$ 200", "Gastou R$ 67,", "R$ 48 e R$ 39"], "R$ 46,00",
     ["R$ 54,00", "R$ 56,00"],
     "A professora foi ao mercado com duzentos reais. Gastou sessenta e sete na padaria, quarenta e oito no açougue e trinta e nove na feira. Com quanto ela voltou pra casa?",
     "Quarenta e seis reais! Primeiro soma tudo que gastou: cento e cinquenta e quatro. Depois tira dos duzentos.",
     {"count": 12.0, "fala_ops": {"R$ 46,00": "quarenta e seis reais", "R$ 54,00": "cinquenta e quatro reais",
                                  "R$ 56,00": "cinquenta e seis reais"}}),
    (3, "QUANTO DÁ?", ["458 - 356"], "102", ["112", "202"],
     "Quatrocentos e cinquenta e oito menos trezentos e cinquenta e seis?",
     "Cento e dois!", {"count": 10.0}),
    (3, "DIVIDA OS BRIGADEIROS!", ["87 brigadeiros", "para 4 turmas"], "21 cada e sobram 3",
     ["22 cada e sobra 1", "20 cada e sobram 7"],
     "Oitenta e sete brigadeiros divididos igualmente entre quatro turmas. Quantos cada turma recebe e quantos sobram?",
     "Vinte e um pra cada turma, e sobram três! Vinte e um vezes quatro é oitenta e quatro, mais três dá oitenta e sete.",
     {"count": 10.0}),
    (3, "QUANTO TEMPO?", ["Almoço", "11h30 às 13h"], "90 minutos", ["30 minutos", "130 minutos"],
     "O Josué almoça das onze e meia até a uma da tarde. Quantos minutos ele tem pra almoçar?",
     "Noventa minutos! Uma hora e meia.", {}),
    (3, "QUANTO DINHEIRO?", ["6 moedas de", "25 centavos"], "R$ 1,50", ["R$ 1,25", "R$ 6,25"],
     "Quem tem seis moedas de vinte e cinco centavos tem quanto dinheiro?",
     "Um real e cinquenta! Seis vezes vinte e cinco dá cento e cinquenta centavos.",
     {"fala_ops": {"R$ 1,50": "um real e cinquenta", "R$ 1,25": "um real e vinte e cinco",
                   "R$ 6,25": "seis reais e vinte e cinco"}}),
    (3, "LENDO A TABELA", ["Set: 96 livros", "Out: 145 livros", "A mais?"], "49",
     ["51", "59"],
     "A tabela mostra os livros que o terceiro ano leu: noventa e seis em setembro e cento e quarenta e cinco em outubro. Quantos livros a mais em outubro?",
     "Quarenta e nove! Cento e quarenta e cinco menos noventa e seis.", {"count": 10.0}),
    (3, "QUANTO DÁ?", ["209 × 3"], "627", ["607", "637"],
     "Duzentos e nove vezes três?",
     "Seiscentos e vinte e sete! O zero do meio confunde: três vezes zero é zero, mais o dois guardado, dá dois.",
     {"count": 10.0, "aviso": "O ZERO CONFUNDE!"}),
    (3, "QUAL TEM ESSA FORMA?", ["BLOCO RETANGULAR"], "Caixa de creme dental",
     ["Casquinha de sorvete", "Balde"],
     "Qual desses tem forma parecida com a de um bloco retangular?",
     "A caixa de creme dental! A gaveta, o livro e o quarto também.", {"fig": "bloco"}),
    (3, "QUAL O PADRÃO?", ["1 · 2 · 4 · 8", "... 64 · ?"], "128", ["96", "100"],
     "Seguindo o padrão dos dobros: um, dois, quatro, oito... qual vem depois do sessenta e quatro?",
     "Cento e vinte e oito! O dobro de sessenta e quatro.", {}),
    (3, "COMPLETE!", ["2500 g = ?"], "2 kg e 500 g", ["25 kg", "2 kg e 50 g"],
     "Dois mil e quinhentos gramas é o mesmo que...",
     "Dois quilos e quinhentos gramas!",
     {"fala_ops": {"2 kg e 500 g": "dois quilos e quinhentos gramas", "25 kg": "vinte e cinco quilos",
                   "2 kg e 50 g": "dois quilos e cinquenta gramas"}}),
    # ---------- MUITO DIFÍCIL ----------
    (4, "QUANTO TEMPO?", ["Entra às 7h", "Almoço 11h30-13h", "Sai às 17h"],
     "8 horas e 30 minutos", ["10 horas", "9 horas e 30 minutos"],
     "O Josué entra às sete, almoça das onze e meia à uma e sai às cinco da tarde. Quantas horas ele trabalha no dia?",
     "Oito horas e meia! Quatro e meia de manhã e quatro à tarde.", {"count": 12.0, "aviso": "TIRA O ALMOÇO!"}),
    (4, "CONFIRA A CONTA!", ["O colega fez:", "207 + 149 = 446"], "Errada, é 356", ["Certa", "Errada, é 346"],
     "O colega fez duzentos e sete mais cento e quarenta e nove e escreveu quatrocentos e quarenta e seis. Tá certa?",
     "Errada! O certo é trezentos e cinquenta e seis.",
     {"count": 10.0, "fala_ops": {"Errada, é 356": "errada, é trezentos e cinquenta e seis",
                                  "Errada, é 346": "errada, é trezentos e quarenta e seis"}}),
    (4, "EMPILHE AS CAIXAS!", ["3 caixas de 12 cm", "empilhadas"], "36 cm",
     ["12 cm", "30 cm"],
     "Uma caixa tem doze centímetros de altura. Empilhando três caixas, uma em cima da outra, qual a altura da pilha?",
     "Trinta e seis centímetros! Empilhou pra cima, só muda a altura.", {"fig": "bloco"}),
    (4, "QUANTA MADEIRA?", ["Moldura", "75 cm × 36 cm"], "222 cm", ["111 cm", "150 cm"],
     "Pra trocar a moldura de um quadro de setenta e cinco centímetros de comprimento e trinta e seis de altura, quantos centímetros de madeira precisa?",
     "Duzentos e vinte e dois! A moldura dá a volta inteira: dois comprimentos e duas alturas.",
     {"count": 12.0, "aviso": "PEGADINHA!"}),
    (4, "QUANTO ELE GASTOU?", ["12 abacaxis", "a R$ 18 cada"], "R$ 216", ["R$ 72", "R$ 196"],
     "O Leo ia comprar abacaxis a dezoito reais cada. Se comprar doze abacaxis, quanto vai gastar?",
     "Duzentos e dezesseis reais! Doze vezes dezoito.",
     {"count": 12.0, "fala_ops": {"R$ 216": "duzentos e dezesseis reais", "R$ 72": "setenta e dois reais",
                                  "R$ 196": "cento e noventa e seis reais"}}),
    (4, "QUANTAS VOLTAS?", ["Pista: 250 m", "Caminha 1500 m"], "6 voltas", ["5 voltas", "7 voltas"],
     "A pista do parque tem duzentos e cinquenta metros. O Márcio caminha mil e quinhentos metros por dia. Quantas voltas ele dá?",
     "Seis voltas! E mil e quinhentos metros é um quilômetro e meio.", {"count": 10.0}),
    (4, "QUAL A DIFERENÇA?", ["Dois relógios:", "14:20 e 15:40"], "1 hora e 20 minutos",
     ["1 hora e 40 minutos", "2 horas e 20 minutos"],
     "Dois relógios marcam quatorze e vinte e quinze e quarenta. Qual a diferença entre eles?",
     "Uma hora e vinte minutos!", {}),
    (4, "QUANTAS LATINHAS?", ["Latinha: 350 mL", "Quantas = 1 L?"], "3 latinhas",
     ["2 latinhas", "4 latinhas"],
     "Uma latinha de suco tem trezentos e cinquenta mililitros. Quantas latinhas precisa pra ter mais ou menos um litro?",
     "Três latinhas! Dá mil e cinquenta mililitros, pouco mais de um litro.", {}),
    (4, "QUADRADO MÁGICO", ["8 · 36 · 16", "28 · 20 · 12", "24 · 4 · 32"], "60", ["48", "56"],
     "No quadrado mágico, todas as linhas, colunas e diagonais somam o mesmo valor. Quanto soma cada linha?",
     "Sessenta! Oito mais trinta e seis mais dezesseis dá sessenta.", {"count": 12.0}),
    (4, "QUAL O 10º NÚMERO?", ["0 · 15 · 30 · 45", "10º número?"], "135", ["150", "120"],
     "Na sequência que começa no zero e aumenta de quinze em quinze, qual é o décimo número?",
     "Cento e trinta e cinco! O zero é o primeiro: depois do cento e cinco vem cento e vinte, e depois cento e trinta e cinco.",
     {"count": 10.0, "aviso": "QUASE TODO MUNDO ERRA!"}),
    (4, "QUANTOS GRAMAS?", ["6 pacotes de", "arroz de 5 kg"], "30.000 g", ["3.000 g", "300 g"],
     "Um pacote de arroz de cinco quilos tem cinco mil gramas. Quantos gramas têm seis pacotes desses?",
     "Trinta mil gramas!",
     {"fala_ops": {"30.000 g": "trinta mil gramas", "3.000 g": "três mil gramas", "300 g": "trezentos gramas"}}),
    (4, "LENDO A TABELA", ["Ago 128 · Set 96", "Out 145 · Nov 87", "Total?"], "456", ["446", "466"],
     "Agosto, cento e vinte e oito. Setembro, noventa e seis. Outubro, cento e quarenta e cinco. Novembro, oitenta e sete. Quantos livros nos quatro meses juntos?",
     "Quatrocentos e cinquenta e seis livros!", {"count": 12.0}),
    (4, "QUAL A SEMANA?", ["8h30 por dia", "seg. a sexta"], "42 horas e 30 minutos",
     ["40 horas", "40 horas e 30 minutos"],
     "Se o Josué trabalha oito horas e meia por dia, de segunda a sexta, quantas horas ele trabalha na semana?",
     "Quarenta e duas horas e meia! Quarenta horas, mais cinco meias horas, que dão duas horas e meia.",
     {"count": 12.0, "suspense": True}),
    (4, "O QUE TÊM IGUAL?", ["CUBO e BLOCO", "RETANGULAR"], "Mesmos vértices, arestas e faces",
     ["Todas as faces quadradas", "Faces triangulares"],
     "O que o cubo e o bloco retangular têm igual?",
     "Os mesmos números! Oito vértices, doze arestas e seis faces.", {"fig": "cubo_bloco"}),
    (4, "QUANTO GASTOU?", ["28 × R$ 7", "35 × R$ 6", "9 × R$ 14"], "532 reais",
     ["522 reais", "432 reais"],
     "Valendo a nota da prova! A turma comprou vinte e oito adesivos de sete reais, trinta e cinco lápis de seis reais e nove caderninhos de quatorze reais. Quanto gastou ao todo?",
     "Quinhentos e trinta e dois reais! Cento e noventa e seis, mais duzentos e dez, mais cento e vinte e seis. Se acertou essa, tirou dez em matemática!",
     {"count": 15.0, "suspense": True, "final": True}),
]


def main():
    rnd = random.Random(81)
    pos = [0, 1, 2] * 16
    rnd.shuffle(pos)
    R = []
    for n, (nivel, perg, cartao, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        c = pos[n - 1]
        ops.insert(c, certa)
        assert len(set(ops)) == len(ops) and certa in ops, (n, ops)
        if ex.get("falar_ops", True):
            fo = [ex.get("fala_ops", {}).get(o, o) for o in ops]
            fq = f"{fq} {', '.join(fo[:-1])} ou {fo[-1]}?"
        r = {"n": n, "nivel": nivel, "pergunta": perg, "cartao": cartao, "foto": f"q{n}.png",
             "opcoes": ops, "certa": c, "fala_q": fq, "fala_r": fr, "count": ex.get("count", 8.0)}
        for k in ("fig", "aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo a nota... a resposta é..."
        R.append(r)
    assert len({tuple(r["cartao"]) for r in R}) == len(R), "cartão repetido"
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], [sum(r["nivel"] == k for r in R) for k in (2, 3, 4)])


if __name__ == "__main__":
    main()
