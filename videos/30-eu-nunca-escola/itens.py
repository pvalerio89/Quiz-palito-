"""Gera itens.json do vídeo 30 "NA ESCOLA: EU JÁ ou EU NUNCA?" (formato de ESCOLHA, sem resposta certa; estilo humano).

Mesmo formato do vídeo 28, mas só coisas de ESCOLA (ref. Quiz Flash, frases próprias e leves para adolescentes):
"EU JÁ..." + a frase e dois botões, EU JÁ ✅ e EU NUNCA ❌. A pessoa escolhe na contagem e anota nos comentários;
depois aparece a % de quem disse "eu já" (números inventados, plausíveis) com uma reação curta.
Começa com as que quase todo mundo já fez e termina com as mais raras.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))

# emoji, frase (depois de "Eu já..."), % que disse "eu já", reação própria (opcional)
P = [
    # as que quase todo mundo já fez
    ("⏰", "cheguei atrasado na aula", 88, "Quem nunca, né?"),
    ("🎒", "esqueci o material em casa", 84, None),
    ("🔔", "comemorei porque faltou professor", 86, "Aula vaga é a melhor coisa!"),
    ("✏️", "pedi lápis emprestado e não devolvi", 76, "Esse lápis nunca mais voltou!"),
    ("🥱", "bocejei bem alto no meio da aula", 80, None),
    ("📝", "fiz a lição de casa cinco minutos antes da aula", 79, None),
    ("🤫", "conversei tanto que levei bronca", 73, None),
    ("🎨", "desenhei no caderno em vez de copiar a matéria", 77, None),
    ("🎤", "apresentei trabalho tremendo de nervoso", 71, None),
    ("🏃", "corri pra chegar antes do sinal", 70, None),
    # do dia a dia
    ("🍝", "repeti a merenda", 69, "A merenda tava boa, né?"),
    ("😂", "tive crise de riso no meio da aula", 68, None),
    ("🧮", "contei nos dedos durante a prova", 66, None),
    ("🚌", "fui numa excursão da escola", 65, None),
    ("🎂", "comemorei aniversário na sala de aula", 64, None),
    ("💯", "tirei dez numa prova", 63, "Parabéns, hein!"),
    ("🤥", "inventei uma desculpa por não ter feito a lição", 62, "Eu sabia!"),
    ("👩", "chamei a professora de mãe sem querer", 61, "Clássico demais!"),
    ("🤝", "fiz trabalho em grupo praticamente sozinho", 60, "Todo grupo tem um desses!"),
    ("🌧️", "cheguei na escola todo molhado de chuva", 58, None),
    # ficou dividido
    ("🍪", "comi lanche escondido na sala", 57, None),
    ("🏫", "troquei de escola", 56, None),
    ("🎭", "participei de uma peça de teatro da escola", 55, None),
    ("🙋", "levantei a mão e esqueci a pergunta", 54, None),
    ("🤒", "fui embora mais cedo porque passei mal", 50, None),
    ("🗣️", "travei lendo em voz alta pra turma", 48, None),
    ("📱", "levei bronca por mexer no celular na aula", 47, None),
    ("😳", "chamei o professor pelo nome errado", 46, None),
    ("📚", "esqueci que tinha prova", 44, "Que susto!"),
    ("🧃", "derrubei suco dentro da mochila", 43, None),
    # menos comuns
    ("📖", "li o livro inteiro que a professora pediu", 42, None),
    ("🏅", "fui o primeiro a terminar a prova", 37, None),
    ("🍎", "dei um presente pra um professor", 36, None),
    ("🏆", "ganhei medalha nos jogos da escola", 35, None),
    ("🧪", "fiz uma experiência de ciências que deu errado", 33, None),
    ("👟", "fui pra escola de chinelo", 31, None),
    ("📸", "saí de olho fechado na foto da turma", 30, None),
    ("🪑", "caí da cadeira na sala de aula", 29, "Todo mundo riu, né?"),
    ("⚽", "quebrei alguma coisa jogando bola na escola", 27, None),
    ("🚪", "entrei na sala errada", 25, None),
    # as mais raras
    ("💤", "acordei com o professor me chamando", 23, None),
    ("😬", "tirei zero numa prova", 21, None),
    ("🤯", "gabaritei uma prova de matemática", 19, "Se gabaritou, você é fera!"),
    ("🏛️", "fui parar na diretoria", 18, None),
    ("📢", "falei no microfone pra escola inteira", 15, None),
    ("📄", "entreguei a prova em branco", 14, None),
    ("🥇", "ganhei um campeonato representando a escola", 12, None),
    ("🐶", "disse que o cachorro comeu minha lição", 8, "Essa desculpa é das antigas!"),
    ("🎓", "fui o orador da formatura", 6, None),
    ("🌟", "ganhei prêmio por nunca faltar no ano inteiro", 5, "Se você já, você é lenda!"),
]

REACOES = [
    (80, ["Quase todo mundo já!", "Impossível nunca ter feito essa!", "Clássico de escola!"]),
    (60, ["A maioria já!", "Mais da metade já, hein!", "Muita gente já fez isso!"]),
    (40, ["Ficou bem dividido!", "Quase meio a meio!", "Empate técnico!"]),
    (20, ["A maioria nunca!", "Pouca gente já fez essa!", "Essa é mais rara!"]),
    (0, ["Quase ninguém já!", "Se você já, você é raro!", "Essa é raríssima!"]),
]
ENTRADAS = {4: "Agora seja sincero...", 9: "Essa dá frio na barriga...", 14: "Lembra disso?",
            21: "Bora pra próxima!", 26: "Essa é de dar vergonha...", 31: "Agora uma de aluno caprichoso...",
            38: "Essa foi engraçada...", 41: "Agora só as raras!", 46: "E essa?"}


def main():
    rnd = random.Random(30)
    R = []
    usadas = []
    for n, (em, frase, pct, reac) in enumerate(P, 1):
        if not reac:
            lista = next(l for lim, l in REACOES if pct >= lim)
            livres = [x for x in lista if x not in usadas[-3:]] or lista
            reac = rnd.choice(livres)
            usadas.append(reac)
        entrada = ENTRADAS.get(n, "")
        r = {"n": n, "emoji": em, "frase": frase, "pct": pct,
             "fala_q": f"{entrada} Eu já... {frase}?".strip(),
             "fala_r": f"{pct}% já! {reac}",
             "count": 3.0 if n <= 3 else 4.0}
        if n == len(P):
            r["final"] = True
            r["count"] = 5.0
        R.append(r)
    assert len({r["frase"] for r in R}) == len(R) == 50
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "frases")


if __name__ == "__main__":
    main()
