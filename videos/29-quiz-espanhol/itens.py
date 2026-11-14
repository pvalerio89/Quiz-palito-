"""Gera itens.json do vídeo 29 "Quiz de espanhol" (estilo mais humano, 2026-11-13).

36 perguntas próprias de espanhol de escola, em 4 níveis (fácil, médio, difícil e muito difícil): vocabulário,
números, dias, família, ser/estar, passado e as palavras traiçoeiras (falsos amigos do português).
A imagem de cada pergunta é um cartão com a palavra/frase em espanhol (desenhado pelo build, em cartoes/).
Pergunta falada com entrada variada, reação de verdade, dica/aviso/suspense/"você sabia?".
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
SIG = "O QUE SIGNIFICA?"
NUM = "QUE NÚMERO É ESSE?"
COMP = "COMPLETE A FRASE:"
COMO = "COMO SE DIZ EM ESPANHOL?"
TRAI = "PALAVRA TRAIÇOEIRA!"
# nível, pergunta (topo), cartão (linhas), certa, [erradas], fala da pergunta, fala da resposta, extras
P = [
    (1, SIG, ["HOLA"], "Olá", ["Tchau", "Obrigado"], "Pra começar fácil: o que significa hola?",
     "Olá! Começou bem?", {"count": 4.0}),
    (1, SIG, ["GRACIAS"], "Obrigado", ["Por favor", "Desculpa"], "E gracias, o que quer dizer?",
     "Obrigado! Essa foi rapidinha!", {"count": 4.0}),
    (1, SIG, ["PERRO"], "Cachorro", ["Gato", "Pássaro"], "Agora um bicho. O que é um perro?",
     "Cachorro! Au au!", {"count": 5.0}),
    (1, NUM, ["DIEZ"], "10", ["12", "2"], "Que número é diez?", "Dez!", {}),
    (1, "QUE COR É ESSA?", ["ROJO"], "Vermelho", ["Roxo", "Rosa"], "Cuidado, que essa tem pegadinha! Que cor é rojo?",
     "Vermelho! Rojo parece roxo, mas é vermelho. Caiu na pegadinha?", {"aviso": "TEM PEGADINHA!"}),
    (1, "QUE DIA É ESSE?", ["LUNES"], "Segunda-feira", ["Terça-feira", "Domingo"], "Que dia da semana é lunes?",
     "Segunda-feira! Vem de luna, a lua.", {"sabia": "Os dias em espanhol vêm dos astros: lunes é o dia da Lua."}),
    (1, SIG, ["MANZANA"], "Maçã", ["Laranja", "Banana"], "Hora do lanche! O que é uma manzana?",
     "Maçã!", {}),
    (1, SIG, ["LECHE"], "Leite", ["Suco", "Café"], "E leche, o que é?", "Leite! Leche con chocolate, que delícia.", {}),
    (1, NUM, ["CINCUENTA"], "50", ["15", "500"], "Que número é cincuenta?",
     "Cinquenta! Quase igual ao português.", {"dica": ("Dica: parece muito com o português!", "PARECE O PORTUGUÊS")}),
    (2, SIG, ["HERMANO"], "Irmão", ["Primo", "Tio"], "Bora pro nível médio! Família: quem é o seu hermano?",
     "Seu irmão!", {}),
    (2, COMP, ["Me ___ Pedro.", "(meu nome é)"], "llamo", ["llamas", "llama"],
     "Pra se apresentar: me, o quê, Pedro?", "Me llamo Pedro! Meu nome é Pedro.", {}),
    (2, "QUE DIA É ESSE?", ["MIÉRCOLES"], "Quarta-feira", ["Terça-feira", "Sexta-feira"],
     "Essa aqui derruba muita gente! Que dia é miércoles?", "Quarta-feira! E terça é martes.",
     {"aviso": "DERRUBA MUITA GENTE!"}),
    (2, COMO, ["AMARELO"], "Amarillo", ["Morado", "Marrón"], "Como se diz amarelo em espanhol?",
     "Amarillo! E morado é roxo.", {}),
    (2, SIG, ["CUMPLEAÑOS"], "Aniversário", ["Casamento", "Feriado"], "O que é um cumpleaños?",
     "Aniversário! Feliz cumpleaños é o parabéns de lá.", {"sabia": "Cumpleaños quer dizer, ao pé da letra, \"cumpre anos\"."}),
    (2, "QUE HORAS SÃO?", ["Son las tres", "y media."], "3:30", ["3:15", "2:30"], "Que horas são, se alguém diz son las tres y media?",
     "Três e meia!", {}),
    (2, SIG, ["CALCETÍN"], "Meia", ["Sapato", "Calça"], "Agora roupa. O que é um calcetín?",
     "Meia! Aquela do pé.", {"dica": ("Dica: vai no pé, antes do tênis!", "VAI NO PÉ")}),
    (2, COMP, ["Yo ___ brasileño."], "soy", ["estoy", "eres"], "Complete: eu, o quê, brasileiro?",
     "Yo soy brasileño! Nacionalidade é com o verbo ser.", {"aviso": "SER OU ESTAR?", "suspense": True}),
    (2, SIG, ["VENTANA"], "Janela", ["Porta", "Parede"], "O que é uma ventana?",
     "Janela! Por onde entra o vento.", {}),
    (3, SIG, ["EXQUISITO"], "Delicioso", ["Esquisito", "Caro"],
     "Agora as palavras traiçoeiras! Se um espanhol diz que a comida está exquisita, quer dizer que ela está...",
     "Deliciosa! Exquisito é elogio. Quem disse esquisito caiu direitinho!", {"aviso": TRAI}),
    (3, SIG, ["OFICINA"], "Escritório", ["Garagem", "Fábrica"], "O que é uma oficina, em espanhol?",
     "Escritório! O lugar onde se trabalha na mesa.", {}),
    (3, SIG, ["POLVO"], "Poeira", ["Peixe", "Pulga"], "Essa é clássica! O que significa polvo, em espanhol?",
     "Poeira! E o polvo, o bicho, lá se chama pulpo.", {"aviso": TRAI, "sabia": "O bicho polvo, em espanhol, é pulpo."}),
    (3, SIG, ["APELLIDO"], "Sobrenome", ["Apelido", "Nome do meio"], "Quando pedem o seu apellido, querem saber o quê?",
     "O sobrenome! Apellido não é apelido.", {"suspense": True}),
    (3, SIG, ["CENA"], "Jantar", ["Almoço", "Café da manhã"], "O que é a cena, pra um espanhol?",
     "Jantar! E o almoço é almuerzo.", {}),
    (3, SIG, ["PELADO"], "Careca", ["Cabeludo", "Barbudo"], "Cuidado! O que quer dizer pelado, em espanhol?",
     "Careca! Sem pelo na cabeça.", {"aviso": "TEM PEGADINHA!"}),
    (3, SIG, ["ZURDO"], "Canhoto", ["Surdo", "Cego"], "O que significa zurdo?",
     "Canhoto! Quem escreve com a mão esquerda.", {"dica": ("Dica: tem a ver com a mão!", "TEM A VER COM A MÃO")}),
    (3, SIG, ["TODAVÍA"], "Ainda", ["Sempre", "Nunca"], "E todavia, o que é em espanhol?",
     "Ainda! Todavía no, quer dizer ainda não.", {}),
    (3, SIG, ["BORRACHA"], "Bêbada", ["Cansada", "Brava"], "Essa aqui derruba muita gente! O que significa borracha?",
     "Bêbada! A borracha de apagar, lá, é goma.", {"aviso": TRAI, "suspense": True,
                                                   "sabia": "A borracha de apagar, em espanhol, é goma."}),
    (4, SIG, ["SALSA"], "Molho", ["Salsinha", "Sal"], "Agora o nível mais difícil! O que é salsa, na comida?",
     "Molho! E a salsinha é perejil.", {"aviso": "TEM PEGADINHA!"}),
    (4, COMP, ["Ayer yo ___", "al cine."], "fui", ["voy", "iré"], "Ontem eu fui ao cinema. Como fica a frase?",
     "Ayer yo fui al cine! Ayer é ontem, então é passado.", {"dica": ("Dica: ayer quer dizer ontem!", "AYER = ONTEM")}),
    (4, NUM, ["QUINIENTOS"], "500", ["5.000", "50"], "Que número é quinientos?",
     "Quinhentos! Igualzinho, só muda o jeito de falar.", {}),
    (4, SIG, ["EMBARAZADA"], "Grávida", ["Envergonhada", "Atrasada"], "Essa é famosa! O que significa embarazada?",
     "Grávida! Quem acha que é envergonhada passa um vexame!", {"aviso": TRAI, "suspense": True}),
    (4, SIG, ["UN RATO"], "Um tempinho", ["Um rato", "Um ladrão"], "Espera un rato, quer dizer espera o quê?",
     "Um tempinho! E o rato, o bicho, é ratón.", {"sabia": "O bicho rato, em espanhol, é ratón."}),
    (4, COMP, ["Mañana ___", "a llover."], "va", ["voy", "van"], "Amanhã vai chover. Complete a frase!",
     "Mañana va a llover!", {}),
    (4, SIG, ["SOBREMESA"], "Papo à mesa", ["Doce", "Toalha"], "Pegadinha! O que é a sobremesa, pra um espanhol?",
     "É aquele papo na mesa depois de comer! O doce, lá, é postre.", {"aviso": TRAI}),
    (4, SIG, ["LARGO"], "Comprido", ["Grosso", "Curto"], "Cuidado com essa! O que significa largo, em espanhol?",
     "Comprido! Uma estrada larga, pra eles, é uma estrada comprida.", {}),
    (4, SIG, ["ESCOBA"], "Vassoura", ["Escova", "Pente"], "Valendo tudo! O que é uma escoba?",
     "Vassoura! Se você acertou essa, você já fala espanhol!",
     {"count": 9.0, "suspense": True, "final": True}),
]

FALA = {"10": "dez", "12": "doze", "2": "dois", "50": "cinquenta", "15": "quinze", "500": "quinhentos",
        "5.000": "cinco mil", "3:30": "três e meia", "3:15": "três e quinze", "2:30": "duas e meia"}


def main():
    rnd = random.Random(29)
    pos = [0, 1, 2] * 12
    rnd.shuffle(pos)
    pos[0] = 1
    R = []
    for n, (nivel, perg, cartao, certa, err, fq, fr, ex) in enumerate(P, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        if ex.get("falar_ops", True):
            fo = [FALA.get(o, o) for o in ops]
            fq = f"{fq} {fo[0]}, {fo[1]} ou {fo[2]}?"
        r = {"n": n, "nivel": nivel, "pergunta": perg, "cartao": cartao, "foto": f"e{n}.png",
             "opcoes": ops, "certa": pos[n - 1], "fala_q": fq, "fala_r": fr, "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if n != len(P) else "Valendo o diploma de espanhol... a resposta é..."
        R.append(r)
    assert len(R) == 36 and len({tuple(r["cartao"]) for r in R}) == 36
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
