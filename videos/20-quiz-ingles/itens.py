"""Gera itens.json, fotos/ e creditos.json do "Quiz de inglês do 5º ao 9º ano" (vídeo 20).

Perguntas próprias, do nível escolar: vocabulário (5º), to be/dias/família (6º), plural, presente e preposições (7º),
passado, comparativo e falsos cognatos (8º), present perfect, condicional, superlativo e phrasal verbs (9º).
Imagem de cada pergunta: foto real (reaproveitada dos vídeos 12, 13 e 14, Wikimedia Commons) quando é objeto,
animal ou comida; senão um cartão com a palavra/frase (feito pelo build, em cartoes/).
Uso: py -3 itens.py
"""
import json, os, random, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(HERE)
ORIG = {"fruta": "12-fruta-fotos-reais", "bicho": "13-animal-pela-foto", "obj": "14-tudo-amarelo"}
COMO, COR, SIG, COMP, PL, PAS = ("COMO SE DIZ EM INGLÊS?", "QUE COR É ESSA EM INGLÊS?", "O QUE SIGNIFICA?",
                                 "COMPLETE A FRASE:", "QUAL É O PLURAL?", "QUAL É O PASSADO?")
# série, pergunta, imagem (foto "bicho:Cachorro" ou texto "t:..."), certa, [erradas], resposta falada
P = [
    (5, COMO, "bicho:Cachorro", "Dog", ["Cat", "Duck"], "Dog! Cachorro!"),
    (5, COMO, "fruta:Maçã", "Apple", ["Pear", "Lemon"], "Apple! Maçã!"),
    (5, COMO, "bicho:Elefante", "Elephant", ["Giraffe", "Monkey"], "Elephant!"),
    (5, COR, "fruta:Morango", "Red", ["Blue", "Green"], "Red! Vermelho!"),
    (5, "QUE NÚMERO É ESSE EM INGLÊS?", "t:15", "Fifteen", ["Fifty", "Five"], "Fifteen! Quinze!"),
    (5, COMO, "obj:Cadeira", "Chair", ["Table", "Bed"], "Chair! Cadeira!"),
    (5, COMO, "bicho:Vaca", "Cow", ["Horse", "Pig"], "Cow! Vaca!"),
    (5, SIG, "t:BOOK", "Livro", ["Caderno", "Lápis"], "Book é livro!"),
    (5, COMO, "fruta:Uva", "Grape", ["Orange", "Cherry"], "Grape! Uva!"),
    (5, COR, "fruta:Banana", "Yellow", ["Purple", "Brown"], "Yellow! Amarelo!"),
    (5, COMO, "bicho:Gato", "Cat", ["Rabbit", "Mouse"], "Cat! Gato!"),
    (5, "QUE NÚMERO É ESSE EM INGLÊS?", "t:8", "Eight", ["Six", "Nine"], "Eight! Oito!"),
    (5, COMO, "bicho:Leão", "Lion", ["Tiger", "Bear"], "Lion! Leão!"),
    (6, COMP, "t:I ___ a student.", "am", ["is", "are"], "I am a student!"),
    (6, COMP, "t:She ___ my friend.", "is", ["are", "am"], "She is my friend!"),
    (6, "COMO SE DIZ SEGUNDA-FEIRA?", "t:SEGUNDA-FEIRA", "Monday", ["Sunday", "Tuesday"], "Monday!"),
    (6, SIG, "t:SISTER", "Irmã", ["Tia", "Prima"], "Sister é irmã!"),
    (6, "QUE NÚMERO É ESSE?", "t:TWENTY", "20", ["12", "2"], "Twenty é vinte!"),
    (6, COMP, "t:They ___ happy.", "are", ["is", "am"], "They are happy!"),
    (6, "COMO SE DIZ DEZEMBRO?", "t:DEZEMBRO", "December", ["November", "October"], "December!"),
    (6, COMO, "obj:Ônibus", "Bus", ["Car", "Train"], "Bus! Ônibus!"),
    (6, SIG, "t:KITCHEN", "Cozinha", ["Quarto", "Banheiro"], "Kitchen é cozinha!"),
    (6, COMO, "bicho:Abelha", "Bee", ["Fly", "Ant"], "Bee! Abelha!"),
    (6, "COMO SE DIZ PROFESSOR?", "t:PROFESSOR", "Teacher", ["Doctor", "Student"], "Teacher!"),
    (6, COMO, "bicho:Cavalo", "Horse", ["Donkey", "Zebra"], "Horse! Cavalo!"),
    (6, SIG, "t:HAND", "Mão", ["Pé", "Braço"], "Hand é mão!"),
    (7, PL, "t:CHILD", "Children", ["Childs", "Childes"], "Children! Criança vira children!"),
    (7, PL, "t:MOUSE", "Mice", ["Mouses", "Mices"], "Mice!"),
    (7, COMP, "t:He ___ soccer every day.", "plays", ["play", "playing"], "He plays soccer every day!"),
    (7, COMP, "t:She is ___ a book now.", "reading", ["read", "reads"], "She is reading a book now!"),
    (7, COMP, "t:There ___ two cats.", "are", ["is", "be"], "There are two cats!"),
    (7, COMO, "obj:Guarda-chuva", "Umbrella", ["Raincoat", "Hat"], "Umbrella! Guarda-chuva!"),
    (7, COMP, "t:This is ___ house.\n(minha)", "my", ["me", "I"], "This is my house!"),
    (7, PL, "fruta:Tomate", "Tomatoes", ["Tomatos", "Tomaties"], "Tomatoes!"),
    (7, SIG, "t:UNDER", "Embaixo", ["Em cima", "Dentro"], "Under é embaixo!"),
    (7, COMO, "obj:Coruja", "Owl", ["Eagle", "Parrot"], "Owl! Coruja!"),
    (7, COMP, "t:Can you ___ me?", "help", ["helps", "helping"], "Can you help me?"),
    (7, COMO, "obj:Bicicleta", "Bicycle", ["Motorcycle", "Skateboard"], "Bicycle! Bicicleta!"),
    (7, COMP, "t:I ___ like coffee.\n(não)", "don't", ["doesn't", "not"], "I don't like coffee!"),
    (8, PAS, "t:GO", "went", ["goed", "gone"], "Went!"),
    (8, PAS, "t:EAT", "ate", ["eated", "eaten"], "Ate!"),
    (8, COMP, "t:Yesterday I ___ a movie.\n(see)", "saw", ["see", "seen"], "Yesterday I saw a movie!"),
    (8, COMP, "t:An elephant is ___\nthan a mouse.", "bigger", ["big", "biggest"], "Bigger! Maior!"),
    (8, "O QUE SIGNIFICA NA PORTA?", "t:PUSH", "Empurrar", ["Puxar", "Pular"], "Push é empurrar! Puxar é pull!"),
    (8, SIG, "t:LIBRARY", "Biblioteca", ["Livraria", "Laboratório"], "Library é biblioteca! Pegadinha!"),
    (8, SIG, "t:PARENTS", "Pais", ["Parentes", "Primos"], "Parents são os pais!"),
    (8, COMP, "t:Did you ___ your homework?", "do", ["did", "done"], "Did you do your homework?"),
    (8, PAS, "t:BUY", "bought", ["buyed", "brought"], "Bought!"),
    (8, SIG, "t:PRETEND", "Fingir", ["Pretender", "Prender"], "Pretend é fingir!"),
    (8, PAS, "t:WRITE", "wrote", ["writed", "written"], "Wrote!"),
    (8, SIG, "t:COLLEGE", "Faculdade", ["Colégio", "Colega"], "College é faculdade!"),
    (8, COMP, "t:She ___ to school yesterday.", "walked", ["walks", "walking"], "She walked to school yesterday!"),
    (9, COMP, "t:I have ___ here since 2020.\n(live)", "lived", ["living", "live"], "I have lived here since 2020!"),
    (9, COMP, "t:If it rains, I ___ stay home.", "will", ["would", "am"], "If it rains, I will stay home!"),
    (9, COMP, "t:The blue whale is\nthe ___ animal.", "biggest", ["bigger", "most big"], "The biggest! O maior!"),
    (9, SIG, "t:TURN OFF", "Desligar", ["Ligar", "Virar"], "Turn off é desligar!"),
    (9, COMP, "t:You ___ smoke here.\nIt's forbidden!", "mustn't", ["must", "have to"], "You mustn't smoke here!"),
    (9, COMP, "t:She has never ___ sushi.", "eaten", ["ate", "eat"], "She has never eaten sushi!"),
    (9, SIG, "t:ALTHOUGH", "Embora", ["Portanto", "Porque"], "Although é embora!"),
    (9, SIG, "t:FIND OUT", "Descobrir", ["Perder", "Esconder"], "Find out é descobrir!"),
    (9, COMP, "t:The book ___ written\nin 1990.", "was", ["were", "is"], "The book was written in 1990!"),
    (9, COMP, "t:How long ___ you\nstudied English?", "have", ["did", "are"], "How long have you studied English?"),
    (9, SIG, "t:GIVE UP", "Desistir", ["Levantar", "Presentear"], "Give up é desistir!"),
    (9, COMP, "t:I'm looking forward\nto ___ you.", "seeing", ["see", "saw"], "Looking forward to seeing you!"),
    (9, COMP, "t:I wish I ___ fly.", "could", ["can", "will"], "I wish I could fly!"),
]

INTRO = ["Big Ben", "Estátua da Liberdade", "Ponte Golden Gate"]


def main():
    rnd = random.Random(20)
    os.makedirs(os.path.join(HERE, "fotos"), exist_ok=True)
    pos = [0, 1, 2] * 30
    rnd.shuffle(pos)
    R, cred = [], []
    for n, (serie, perg, img, certa, err, fala) in enumerate(P, 1):
        if img.startswith("t:"):
            foto, txt = f"../cartoes/txt-{n}.png", img[2:]
        else:
            k, nome = img.split(":")
            c = json.load(open(os.path.join(VID, ORIG[k], "creditos.json"), encoding="utf-8"))[nome]
            shutil.copy(os.path.join(VID, ORIG[k], "fotos", c["arquivo"]), os.path.join(HERE, "fotos", c["arquivo"]))
            foto, txt = c["arquivo"], None
            cred.append(f"{nome}: {c['autor']} ({c['lic']}), {c['file'].replace('_', ' ')}")
        ops = list(err)
        p = pos[n - 1]
        ops.insert(p, certa)
        assert len(set(ops)) == 3, (n, ops)
        R.append({"n": n, "serie": serie, "pergunta": perg, "foto": foto, "texto": txt, "opcoes": ops, "certa": p,
                  "fala": fala})
    for nome in INTRO:  # fotos só da intro rapidinha (não aparecem nas perguntas)
        c = json.load(open(os.path.join(VID, ORIG["obj"], "creditos.json"), encoding="utf-8"))[nome]
        shutil.copy(os.path.join(VID, ORIG["obj"], "fotos", c["arquivo"]), os.path.join(HERE, "fotos", c["arquivo"]))
        cred.append(f"{nome}: {c['autor']} ({c['lic']}), {c['file'].replace('_', ' ')}")
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"fotos": cred}, open(os.path.join(HERE, "creditos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas,", len(cred), "fotos")


if __name__ == "__main__":
    main()
