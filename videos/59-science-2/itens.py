"""Gera itens.json do vídeo 59 "Prova de Science do 3º ano, " (estilo mais humano).

Perguntas feitas SÓ com o conteúdo dos 2 PDFs que o Patrick mandou em 2026-11-26 (Science Review Sheet e Science
Practice Test, Grade 3, Book B, Unit 3 lessons 1-3 e Unit 4 lesson 4, com gabarito): as 3 atividades de casa que mais
gastam água (descarga, banho, lavar roupa), Direct Use x Virtual Use, litros para produzir comida (tomate 13, batata 25,
pão 40, maçã 70, ovo 135, leite 200, hambúrguer 2400), litro, adaptação, adaptações do camelo (corcova, cílios e
sobrancelhas, narinas, pés, lábios, pelo, pernas longas, beber muita água de uma vez), healthy x unhealthy.
Números da tabela dos PDFs (diferentes da folha do vídeo 58; o próprio PDF diz que variam por fonte).
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
DV = ["Direct Use", "Virtual Use", "Neither"]
VF = ["True", "False"]
HU = ["Healthy", "Unhealthy"]
SN = ["Yes", "No"]
# level, title (top), card (lines), right, [wrong], question (spoken), answer (spoken), extras  -- ALL IN ENGLISH (Patrick 2026-11-26)
P = [
    # ---------- MEDIUM ----------
    (2, "WHICH ONE?", ["One of the 3 home", "activities that use", "the MOST water"], "Flushing the toilet",
     ["Drinking a glass of water", "Brushing your teeth"],
     "Which one is one of the three home activities that use the most water?",
     "Flushing the toilet!", {}),
    (2, "DIRECT OR VIRTUAL?", ["Taking a shower"], "Direct Use", DV[1:],
     "Taking a shower. Is it Direct Use or Virtual Use?",
     "Direct Use! We can see the water being used.", {"img": "chuveiro", "falar_ops": False}),
    (2, "HEALTHY OR UNHEALTHY?", ["Broccoli"], "Healthy", ["Unhealthy"],
     "Broccoli. Healthy or unhealthy?",
     "Healthy!", {"img": "brocolis", "falar_ops": False}),
    (2, "DIRECT OR VIRTUAL?", ["Eating a hamburger"], "Virtual Use", [DV[0], DV[2]],
     "Eating a hamburger. Direct Use or Virtual Use?",
     "Virtual Use! The water was used to make the hamburger.", {"img": "hamburguer", "falar_ops": False}),
    (2, "TRUE OR FALSE?", ["\"A camel keeps water", "inside its hump\""], "False", ["True"],
     "True or false? A camel keeps water inside its hump.",
     "False! The hump stores fat, not water.",
     {"img": "dromedario", "aviso": "TRICK QUESTION!", "falar_ops": False}),
    (2, "HEALTHY OR UNHEALTHY?", ["Soda"], "Unhealthy", ["Healthy"],
     "Soda. Healthy or unhealthy?",
     "Unhealthy! It has a lot of sugar.", {"img": "refri", "falar_ops": False}),
    (2, "DIRECT OR VIRTUAL?", ["Washing clothes"], "Direct Use", DV[1:],
     "Washing clothes. Direct Use or Virtual Use?",
     "Direct Use!", {"img": "maquina", "falar_ops": False}),
    (2, "WHAT UNIT?", ["We measure the", "water to produce", "food in..."], "Liters", ["Kilograms", "Meters"],
     "What unit do we use to measure the water used to produce food?",
     "Liters!", {}),
    (2, "HEALTHY OR UNHEALTHY?", ["Fish"], "Healthy", ["Unhealthy"],
     "Fish. Healthy or unhealthy?",
     "Healthy!", {"img": "peixe", "falar_ops": False}),
    (2, "WHAT DO THEY DO?", ["Wide, padded feet"], "Stop it sinking in sand",
     ["Let it eat thorny plants", "Store fat"],
     "What do the camel's wide, padded feet do?",
     "They stop the camel from sinking into the sand!", {"img": "dromedario2"}),
    (2, "HEALTHY OR UNHEALTHY?", ["Potato chips"], "Unhealthy", ["Healthy"],
     "Potato chips. Healthy or unhealthy?",
     "Unhealthy! A lot of salt and fat.", {"img": "chips", "falar_ops": False}),
    (2, "DIRECT OR VIRTUAL?", ["Brushing your teeth"], "Direct Use", DV[1:],
     "Brushing your teeth. Direct Use or Virtual Use?",
     "Direct Use!", {"img": "escova", "falar_ops": False}),
    (2, "HEALTHY OR UNHEALTHY?", ["Rice and beans"], "Healthy", ["Unhealthy"],
     "Rice and beans. Healthy or unhealthy?",
     "Healthy!", {"img": "arrozfeijao", "falar_ops": False}),
    # ---------- HARD ----------
    (3, "WHICH ONE?", ["Another one of the", "3 activities that use", "the MOST water"], "Washing clothes",
     ["Watering the plants", "Brushing your teeth"],
     "Which one is also one of the three home activities that use the most water?",
     "Washing clothes! The three are: flushing the toilet, taking a shower or a bath, and washing clothes.",
     {"img": "maquina"}),
    (3, "DIRECT OR VIRTUAL?", ["Drinking a", "glass of milk"], "Virtual Use", [DV[0], DV[2]],
     "Drinking a glass of milk. Direct Use or Virtual Use?",
     "Virtual Use! The water that counts was used to produce the milk.",
     {"img": "leite", "aviso": "TRICK QUESTION!", "suspense": True, "falar_ops": False}),
    (3, "WHAT DO THEY DO?", ["Nostrils that close"], "Keep sand out of the nose",
     ["Keep sand out of the eyes", "Store fat"],
     "What do the camel's nostrils that close do?",
     "They keep the sand out of the nose!", {"img": "camelorosto"}),
    (3, "DIRECT OR VIRTUAL?", ["Using a sheet", "of paper"], "Virtual Use", [DV[0], DV[2]],
     "Using a sheet of paper. Direct Use or Virtual Use?",
     "Virtual Use! Water was used to make the paper.", {"img": "papel", "falar_ops": False}),
    (3, "WHAT DO THEY DO?", ["Thick lips"], "Eat thorny plants",
     ["Stop it sinking in sand", "Keep water"],
     "What do the camel's thick lips do?",
     "They let the camel eat thorny desert plants without pain!", {"img": "camelo"}),
    (3, "DIRECT OR VIRTUAL?", ["Watering", "the plants"], "Direct Use", DV[1:],
     "Watering the plants. Direct Use or Virtual Use?",
     "Direct Use!", {"falar_ops": False}),
    (3, "THE MOST WATER?", ["Which food needs", "the MOST water", "to be produced?"], "Hamburger",
     ["Egg", "Glass of milk"],
     "Which food needs the most water to be produced?",
     "The hamburger! About two thousand four hundred liters.", {"img": "hamburguer"}),
    (3, "DIRECT OR VIRTUAL?", ["Buying a pair", "of shoes"], "Virtual Use", [DV[0], DV[2]],
     "Buying a pair of shoes. Direct Use or Virtual Use?",
     "Virtual Use! It is a ready product.", {"img": "sapato", "falar_ops": False}),
    (3, "THE LEAST WATER?", ["Which food needs", "the LEAST water?"], "Tomato", ["Potato", "Apple"],
     "Which food needs the least water?",
     "The tomato! About thirteen liters.", {"img": "tomate"}),
    (3, "WHAT IS IT?", ["An adaptation is..."], "A feature to survive",
     ["A kind of food", "Water we cannot see"],
     "What is an adaptation?",
     "A special feature that helps an animal survive where it lives!", {}),
    (3, "HOW MANY LITERS?", ["1 slice of bread"], "About 40 liters", ["About 4 liters", "About 400 liters"],
     "How many liters of water to produce one slice of bread?",
     "About forty liters!", {"img": "pao"}),
    (3, "HEALTHY OR UNHEALTHY?", ["Chocolate cake"], "Unhealthy", ["Healthy"],
     "Chocolate cake. Healthy or unhealthy?",
     "Unhealthy! A lot of sugar and fat.", {"img": "bolo", "falar_ops": False}),
    (3, "WHICH NEEDS MORE?", ["Food from animals", "or food from plants?"], "Food from animals",
     ["Food from plants", "The same"],
     "Which usually needs more water: food from animals or food from plants?",
     "Food from animals! It needs much more water.", {"img": "ovo", "falar_ops": False}),
    (3, "HOW MANY LITERS?", ["1 egg"], "About 135 liters", ["About 13 liters", "About 70 liters"],
     "How many liters of water to produce one egg?",
     "About one hundred thirty-five liters!", {"img": "ovo"}),
    (3, "WHAT DO THEY DO?", ["Long eyelashes and", "thick eyebrows"], "Keep sand out of the eyes",
     ["Keep sand out of the nose", "Give energy"],
     "What do the camel's long eyelashes and thick eyebrows do?",
     "They keep the sand out of the eyes and shade them from the sun!", {"img": "bactriano2"}),
    # ---------- VERY HARD ----------
    (4, "HOW MANY LITERS?", ["1 glass of milk"], "About 200 liters", ["About 20 liters", "About 2,000 liters"],
     "How many liters of water to produce one glass of milk?",
     "About two hundred liters!", {"img": "leite", "aviso": "ALMOST EVERYBODY MISSES IT!"}),
    (4, "WHAT IS THE ORDER?", ["From the LEAST", "to the MOST water"], "Tomato, apple, egg",
     ["Apple, tomato, egg", "Egg, apple, tomato"],
     "Which is the right order, from the least water to the most?",
     "Tomato, apple, egg! Thirteen, seventy and one hundred thirty-five liters.", {"suspense": True}),
    (4, "HOW MANY LITERS?", ["1 hamburger"], "About 2,400 liters", ["About 240 liters", "About 24 liters"],
     "How many liters of water to produce one hamburger?",
     "About two thousand four hundred liters!", {"img": "hamburguer"}),
    (4, "UNHEALTHY FOOD HAS...", ["Unhealthy food", "has a lot of..."], "Sugar, salt or fat",
     ["Water and milk", "Fruit and vegetables"],
     "Unhealthy food has a lot of what?",
     "Sugar, salt or fat!", {"img": "batatafrita"}),
    (4, "HOW MUCH MORE?", ["Egg: 135 liters", "Apple: 70 liters", "Difference?"], "65 liters",
     ["55 liters", "75 liters"],
     "An egg needs about one hundred thirty-five liters. An apple, seventy. How many more liters does the egg need?",
     "Sixty-five liters! One hundred thirty-five minus seventy.", {"falar_ops": False}),
    (4, "HEALTHY OR UNHEALTHY?", ["Milk"], "Healthy", ["Unhealthy"],
     "And milk? Healthy or unhealthy?",
     "Healthy!", {"img": "leite", "falar_ops": False}),
    (4, "WHAT DO THEY DO?", ["Long legs"], "Keep the body off hot sand",
     ["Run from lions", "Store fat"],
     "What do the camel's long legs do?",
     "They keep the body away from the hot sand!", {"img": "dromedario"}),
    (4, "TRUE OR FALSE?", ["\"A camel can drink a lot", "of water at once and", "go many days without\""],
     "True", ["False"],
     "True or false? A camel can drink a lot of water at once and go many days without drinking.",
     "True! Another adaptation for the desert.", {"img": "deserto", "falar_ops": False, "suspense": True}),
    (4, "WHY IS IT USEFUL?", ["The fat in", "the hump..."], "Gives energy with no food",
     ["Cools the body", "Stores water"],
     "This one is worth the grade! The hump stores fat. Why is the fat useful in the desert?",
     "It gives energy when there is no food! The hump stores fat, not water. If you got this one, you are ready for the test!",
     {"img": "camelo", "count": 12.0, "suspense": True, "final": True}),
]

# Sheet 1 (6 photos, Science Review Activity): Tommy, direct x virtual, liters, hose, camel. Interleaved by level in main().
P1 = [
    (2, "WHAT DOES HE EAT?", ["Tommy's breakfast:", "a banana and..."], "Whole-grain bread",
     ["Chocolate cake", "Candy"],
     "Tommy loves to eat. For breakfast, he eats a banana and what?",
     "Whole-grain bread! A banana and whole-grain bread, a healthy breakfast.", {"img": "pao"}),
    (2, "WHAT DOES HE DRINK?", ["During the day,", "Tommy drinks..."], "Water", ["Soda", "Nothing"],
     "And what does Tommy drink during the day to help his body?",
     "Water! He drinks water during the day.", {"img": "copo"}),
    (2, "ONLY ONCE IN A WHILE!", ["What should Tommy", "NOT eat every day?"], "Candy and soda",
     ["Rice and beans", "Banana and bread"],
     "Tommy loves candy and soda too. But what should he NOT eat every day?",
     "Candy and soda! Only once in a while.", {"img": "doces"}),
    (2, "COMPLETE!", ["Fruits and vegetables", "are examples of", "________ foods"], "Healthy",
     ["Virtual", "Desert"],
     "Complete the sentence: fruits and vegetables are examples of what foods?",
     "Healthy foods!", {"img": "verduras"}),
    (2, "WHICH USES MORE?", ["Which one uses", "MORE water?"], "Washing the car with a hose",
     ["Using a watering can", "Drinking a glass of water"],
     "Which one of these uses more water?",
     "Washing the car with a hose! The water keeps running.", {"img": "mangueira"}),
    (3, "DIRECT OR VIRTUAL?", ["A farmer uses water", "to grow tomatoes"], "Virtual Use", [DV[0], DV[2]],
     "A farmer uses water to grow tomatoes. Direct Use or Virtual Use?",
     "Virtual Use! The water is used to produce food.",
     {"img": "tomateiro", "falar_ops": False, "aviso": "TRICK QUESTION!"}),
    (3, "DIRECT OR VIRTUAL?", ["A factory uses water", "to make a T-shirt"], "Virtual Use", [DV[0], DV[2]],
     "A factory uses water to make a T-shirt. Direct Use or Virtual Use?",
     "Virtual Use! It counts for products too, not only food.", {"img": "camiseta", "falar_ops": False}),
    (3, "HOW MANY LITERS?", ["1 banana"], "About 160 liters", ["About 16 liters", "About 1,600 liters"],
     "How many liters of water to produce one banana?",
     "About one hundred sixty liters!", {"img": "banana"}),
    (3, "WHAT DOES IT DO?", ["The camel's", "thick fur"], "Protects from sun and cold",
     ["Stores fat", "Keeps sand out of the eyes"],
     "What does the camel's thick fur do?",
     "It protects the camel from the hot sun and also from the cold desert nights!",
     {"img": "camelorosto", "suspense": True}),
    (3, "COMPLETE!", ["Healthy foods", "help Tommy..."], "Grow and stay strong",
     ["Eat more candy", "Sleep in class"],
     "According to the text, healthy food helps Tommy do what?",
     "Grow, stay strong and have energy to play soccer with his friends!", {}),
    (4, "HOW MANY LITERS?", ["Beef:", "liters per kilogram"], "15,000 liters", ["1,500 liters", "150 liters"],
     "How many liters of water to produce one kilogram of beef?",
     "Fifteen thousand liters per kilogram! Much more than everything else.",
     {"img": "carne2", "aviso": "ALMOST NOBODY GETS IT!", "falar_ops": False}),
    (4, "COMPLETE!", ["We need ________", "to survive"], "Water", ["Soda", "Candy"],
     "Complete the sentence: we need what to survive?",
     "Water! We need water to survive.", {"img": "torneira"}),
]


def merged():
    out = []
    for lv in (2, 3, 4):
        a = [p for p in P if p[0] == lv and not p[7].get("final")]
        b = [p for p in P1 if p[0] == lv]
        step = max(1, round(len(a) / (len(b) + 1)))
        for i, x in enumerate(b):
            a.insert(min(len(a), (i + 1) * step + i), x)
        out += a
    return out + [p for p in P if p[7].get("final")]


def main():
    Q = merged()
    rnd = random.Random(59)
    pos = [0, 1, 2] * 20
    rnd.shuffle(pos)
    R = []
    for n, (nivel, perg, cartao, certa, err, fq, fr, ex) in enumerate(Q, 1):
        ops = list(err)
        if len(ops) == 1:   # 2 opções, ordem fixa
            ops = next(p for p in (VF, HU, SN) if certa in p)[:]
            c = ops.index(certa)
        elif certa in DV:   # direta/virtual: ordem fixa (direta, virtual, nenhuma)
            ops = DV[:]
            c = ops.index(certa)
        else:
            c = pos[n - 1]
            ops.insert(c, certa)
        assert len(set(ops)) == len(ops) and certa in ops, (n, ops)
        if ex.get("falar_ops", True):
            fq = f"{fq} {', '.join(ops[:-1])} or {ops[-1]}?"
        r = {"n": n, "nivel": nivel, "pergunta": perg, "cartao": cartao, "foto": f"q{n}.png",
             "opcoes": ops, "certa": c, "fala_q": fq, "fala_r": fr, "count": ex.get("count", 8.0)}
        if "img" in ex:
            r["img"] = ex["img"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "The answer is..." if n != len(Q) else "For the grade... the answer is..."
        R.append(r)
    assert len({tuple(r["cartao"]) for r in R}) == len(R), "cartão repetido"
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R], [sum(r["nivel"] == k for r in R) for k in (2, 3, 4)],
          sorted({r["img"] for r in R if "img" in r}))


if __name__ == "__main__":
    main()
