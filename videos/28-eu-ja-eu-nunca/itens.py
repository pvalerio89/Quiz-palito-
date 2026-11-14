"""Gera itens.json do vídeo 28 "EU JÁ ou EU NUNCA?" (formato de ESCOLHA, sem resposta certa; estilo humano).

50 frases próprias e leves (para adolescentes): aparece "EU JÁ..." + a frase e dois botões, EU JÁ ✅ e
EU NUNCA ❌. A pessoa escolhe na contagem e anota nos comentários; depois aparece a % de quem disse "eu já"
(números inventados, plausíveis) com uma reação curta. Começa com as que quase todo mundo já fez e termina
com as mais raras.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))

# emoji, frase (depois de "Eu já..."), % que disse "eu já", reação própria (opcional)
P = [
    ("🎤", "cantei no chuveiro", 90, "Quase todo mundo é cantor de chuveiro!"),
    ("🦶", "bati o dedinho do pé na quina", 95, "Essa dói só de lembrar!"),
    ("📱", "deixei o celular cair na cara deitado", 78, None),
    ("😴", "cochilei na sala de aula", 48, None),
    ("🍕", "comi pizza no café da manhã", 55, "Pizza fria de manhã é outro nível!"),
    ("🧠", "esqueci o que ia falar no meio da frase", 92, None),
    ("🚌", "perdi o ônibus por um segundo", 70, None),
    ("🍫", "comi chocolate escondido", 74, None),
    ("😂", "ri numa hora que não podia rir", 87, None),
    ("🐶", "conversei com um bicho como se fosse gente", 83, "E ele entendeu tudo, né?"),
    ("📺", "assisti uma série inteira em um dia", 52, None),
    ("🤳", "tirei mais de vinte fotos pra postar uma só", 46, None),
    ("🎮", "joguei videogame até de madrugada", 61, None),
    ("🔑", "fiquei trancado do lado de fora de casa", 44, None),
    ("🧦", "saí de casa com uma meia de cada cor", 57, None),
    ("📞", "liguei pra alguém sem querer", 81, None),
    ("🙈", "mandei mensagem pra pessoa errada", 66, "Que vergonha!"),
    ("🍝", "sujei a roupa de molho de macarrão", 79, None),
    ("🌊", "vi o mar de pertinho", 72, None),
    ("🍳", "fiz uma refeição inteira sozinho", 58, None),
    ("🤧", "espirrei bem na hora da foto", 39, None),
    ("🎢", "andei de montanha-russa", 54, None),
    ("👻", "fiquei com medo do escuro depois de um filme de terror", 69, None),
    ("🎂", "esqueci o aniversário de um amigo", 51, None),
    ("🌙", "virei a noite acordado", 56, None),
    ("🎬", "chorei vendo desenho animado", 63, "Não precisa ter vergonha!"),
    ("🍋", "chupei limão puro", 64, None),
    ("🏃", "corri pra pegar o elevador", 68, None),
    ("🌶️", "comi pimenta e chorei", 59, None),
    ("🪞", "falei sozinho na frente do espelho", 71, None),
    ("✈️", "andei de avião", 49, None),
    ("🏆", "ganhei uma medalha", 45, None),
    ("🐟", "cuidei de um peixinho", 47, None),
    ("🎁", "abri um presente antes da hora", 38, None),
    ("🛹", "andei de skate", 36, None),
    ("🥶", "tomei banho gelado no inverno", 37, "Corajoso, hein!"),
    ("🚲", "andei de bicicleta sem as mãos", 34, None),
    ("🎸", "aprendi a tocar um instrumento", 33, None),
    ("🏕️", "dormi numa barraca de acampamento", 31, None),
    ("📚", "li um livro inteiro em um dia", 29, None),
    ("🐎", "andei a cavalo", 41, None),
    ("🤒", "fingi que estava doente pra não ir na aula", 42, "Eu sabia!"),
    ("🤿", "mergulhei com snorkel no mar", 22, None),
    ("🐍", "segurei uma cobra", 18, None),
    ("❄️", "vi neve de verdade", 12, "No Brasil é raro mesmo!"),
    ("🦈", "vi um tubarão de perto", 11, None),
    ("📸", "apareci na televisão", 9, None),
    ("🚁", "andei de helicóptero", 6, None),
    ("🐘", "fiz carinho num elefante", 5, None),
    ("🌋", "vi um vulcão de verdade", 4, "Se você já viu, conta nos comentários!"),
]

REACOES = [
    (80, ["Quase todo mundo já!", "Impossível nunca ter feito essa!", "Clássico! Quase todo mundo já!"]),
    (60, ["A maioria já!", "Mais da metade já, hein!", "Muita gente já fez isso!"]),
    (40, ["Ficou bem dividido!", "Quase meio a meio!", "Empate técnico!"]),
    (20, ["A maioria nunca!", "Pouca gente já fez essa!", "Essa é mais rara!"]),
    (0, ["Quase ninguém já!", "Se você já, você é raro!", "Essa é raríssima!"]),
]
ENTRADAS = {4: "Agora uma de escola...", 11: "E essa aqui?", 20: "Bora pra próxima!", 31: "Essa é de viagem...",
            37: "Pensa bem nessa...", 43: "Agora só as raras!", 47: "E essa?"}


def main():
    rnd = random.Random(28)
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
