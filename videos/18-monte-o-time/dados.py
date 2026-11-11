"""Times do "MONTE O TIME" (vídeo 18): escalação titular de finais famosas, posição por posição.

Cada jogador: (pergunta, nome certo, rótulo curto no campo, [2 erradas], x, y)  — x,y de 0 a 1 no campo
(y = 0 ataque, 1 = gol). As erradas nunca são titulares daquela final.
Imagem do cabeçalho: bandeira (videos/03-bandeiras-195/bandeiras) ou escudo (videos/16-alfabeto-times/escudos).
"""
GOL, LD, LE = "QUEM ERA O GOLEIRO?", "E O LATERAL DIREITO?", "E O LATERAL ESQUERDO?"
Z1, Z2, Z3 = "QUEM ERA UM DOS ZAGUEIROS?", "E O OUTRO ZAGUEIRO?", "E O TERCEIRO ZAGUEIRO?"
VOL, VOL2 = "QUEM ERA O VOLANTE?", "E O OUTRO VOLANTE?"
MEI, MEI2, MEI3 = "QUEM ERA UM DOS MEIAS?", "E O OUTRO MEIA?", "E O ÚLTIMO MEIA?"
ATA, ATA2 = "QUEM ERA UM DOS ATACANTES?", "E O OUTRO ATACANTE?"

TIMES = [
    {"nome": "BRASIL", "sub": "FINAL DA COPA 2002", "fala": "Brasil do penta, na final da Copa de 2002", "img": "band:br",
     "cor": (0, 150, 70), "jog": [
        (GOL, "Marcos", "Marcos", ["Dida", "Taffarel"], 0.5, 0.92),
        (Z1, "Lúcio", "Lúcio", ["Juan", "Aldair"], 0.28, 0.76),
        (Z2, "Edmílson", "Edmílson", ["Juan", "Júnior Baiano"], 0.5, 0.79),
        (Z3, "Roque Júnior", "R. Júnior", ["Aldair", "Anderson Polga"], 0.72, 0.76),
        ("QUEM ERA O LATERAL DIREITO E CAPITÃO?", "Cafu", "Cafu", ["Belletti", "Jorginho"], 0.12, 0.5),
        (VOL, "Gilberto Silva", "Gilberto", ["Emerson", "Mauro Silva"], 0.38, 0.58),
        (VOL2, "Kléberson", "Kléberson", ["Juninho Paulista", "Dunga"], 0.62, 0.58),
        (LE, "Roberto Carlos", "R. Carlos", ["Júnior", "Branco"], 0.88, 0.5),
        ("QUEM ERA O CAMISA 11?", "Ronaldinho", "Ronaldinho", ["Kaká", "Denílson"], 0.33, 0.32),
        ("QUEM ERA O CAMISA 10?", "Rivaldo", "Rivaldo", ["Kaká", "Edílson"], 0.67, 0.32),
        ("QUEM ERA O CENTROAVANTE?", "Ronaldo", "Ronaldo", ["Luizão", "Romário"], 0.5, 0.12)]},
    {"nome": "REAL MADRID", "sub": "FINAL DA CHAMPIONS 2017", "fala": "Real Madrid, na final da Champions de 2017",
     "img": "escudo:real-madrid", "cor": (230, 180, 30), "jog": [
        (GOL, "Keylor Navas", "Navas", ["Casillas", "Courtois"], 0.5, 0.92),
        (LD, "Carvajal", "Carvajal", ["Arbeloa", "Míchel Salgado"], 0.13, 0.66),
        (Z1, "Varane", "Varane", ["Hierro", "Cannavaro"], 0.37, 0.76),
        (Z2, "Sergio Ramos", "S. Ramos", ["Hierro", "Cannavaro"], 0.63, 0.76),
        (LE, "Marcelo", "Marcelo", ["Roberto Carlos", "Míchel Salgado"], 0.87, 0.66),
        (VOL, "Casemiro", "Casemiro", ["Makélélé", "Xabi Alonso"], 0.5, 0.56),
        (MEI, "Kroos", "Kroos", ["Özil", "Guti"], 0.3, 0.46),
        (MEI2, "Modric", "Modric", ["Özil", "Guti"], 0.7, 0.46),
        (MEI3, "Isco", "Isco", ["Kaká", "Özil"], 0.5, 0.33),
        (ATA, "Benzema", "Benzema", ["Higuaín", "Raúl"], 0.34, 0.14),
        (ATA2, "Cristiano Ronaldo", "Cristiano", ["Raúl", "Figo"], 0.66, 0.14)]},
    {"nome": "ARGENTINA", "sub": "FINAL DA COPA 2022", "fala": "Argentina campeã, na final da Copa de 2022",
     "img": "band:ar", "cor": (90, 170, 230), "jog": [
        (GOL, "Emiliano Martínez", "Dibu", ["Armani", "Sergio Romero"], 0.5, 0.92),
        (LD, "Molina", "Molina", ["Zabaleta", "Mercado"], 0.13, 0.66),
        (Z1, "Cuti Romero", "Romero", ["Demichelis", "Garay"], 0.37, 0.76),
        (Z2, "Otamendi", "Otamendi", ["Demichelis", "Garay"], 0.63, 0.76),
        (LE, "Tagliafico", "Tagliafico", ["Rojo", "Heinze"], 0.87, 0.66),
        (MEI, "De Paul", "De Paul", ["Mascherano", "Banega"], 0.25, 0.48),
        (VOL, "Enzo Fernández", "Enzo", ["Biglia", "Gago"], 0.5, 0.55),
        (MEI2, "Mac Allister", "Mac Allister", ["Lo Celso", "Banega"], 0.75, 0.48),
        ("QUEM ERA O PONTA QUE FEZ GOL?", "Di María", "Di María", ["Lavezzi", "Agüero"], 0.82, 0.22),
        (ATA, "Julián Álvarez", "Julián", ["Higuaín", "Agüero"], 0.5, 0.12),
        ("E O CAMISA 10 E CAPITÃO?", "Messi", "Messi", ["Riquelme", "Tévez"], 0.18, 0.22)]},
    {"nome": "BARCELONA", "sub": "FINAL DA CHAMPIONS 2011", "fala": "Barcelona, na final da Champions de 2011",
     "img": "escudo:barcelona", "cor": (165, 0, 68), "jog": [
        (GOL, "Víctor Valdés", "Valdés", ["Pinto", "Bravo"], 0.5, 0.92),
        (LD, "Daniel Alves", "D. Alves", ["Belletti", "Zambrotta"], 0.13, 0.66),
        (Z1, "Piqué", "Piqué", ["Márquez", "Thuram"], 0.37, 0.76),
        (Z2, "Mascherano", "Mascherano", ["Márquez", "Milito"], 0.63, 0.76),
        (LE, "Abidal", "Abidal", ["Maxwell", "Sylvinho"], 0.87, 0.66),
        (VOL, "Busquets", "Busquets", ["Yaya Touré", "Keita"], 0.5, 0.56),
        (MEI, "Xavi", "Xavi", ["Fàbregas", "Deco"], 0.3, 0.44),
        (MEI2, "Iniesta", "Iniesta", ["Thiago", "Deco"], 0.7, 0.44),
        ("QUEM ERA O PONTA DIREITA?", "Pedro", "Pedro", ["Afellay", "Giuly"], 0.18, 0.2),
        ("QUEM ERA O CAMISA 10?", "Messi", "Messi", ["Eto'o", "Ibrahimović"], 0.5, 0.12),
        ("E O PONTA ESQUERDA?", "David Villa", "Villa", ["Henry", "Bojan"], 0.82, 0.2)]},
    {"nome": "ESPANHA", "sub": "FINAL DA COPA 2010", "fala": "Espanha campeã, na final da Copa de 2010",
     "img": "band:es", "cor": (200, 30, 40), "jog": [
        (GOL, "Casillas", "Casillas", ["Zubizarreta", "De Gea"], 0.5, 0.92),
        (LD, "Sergio Ramos", "S. Ramos", ["Míchel Salgado", "Carvajal"], 0.13, 0.66),
        (Z1, "Piqué", "Piqué", ["Hierro", "Nadal"], 0.37, 0.76),
        (Z2, "Puyol", "Puyol", ["Hierro", "Nadal"], 0.63, 0.76),
        (LE, "Capdevila", "Capdevila", ["Jordi Alba", "Reguilón"], 0.87, 0.66),
        (VOL, "Busquets", "Busquets", ["Rodri", "Senna"], 0.37, 0.56),
        (VOL2, "Xabi Alonso", "X. Alonso", ["Rodri", "Senna"], 0.63, 0.56),
        (MEI, "Xavi", "Xavi", ["Pedri", "Gavi"], 0.5, 0.4),
        ("QUEM FEZ O GOL DO TÍTULO?", "Iniesta", "Iniesta", ["Pedri", "Gavi"], 0.8, 0.3),
        ("QUEM ERA O PONTA?", "Pedro", "Pedro", ["Joaquín", "Lamine Yamal"], 0.2, 0.3),
        ("E O ATACANTE?", "David Villa", "Villa", ["Raúl", "Morata"], 0.5, 0.13)]},
    {"nome": "BRASIL", "sub": "FINAL DA COPA 1970", "fala": "Brasil do tri, na final da Copa de 1970", "img": "band:br",
     "cor": (0, 150, 70), "jog": [
        (GOL, "Félix", "Félix", ["Leão", "Gilmar"], 0.5, 0.92),
        ("QUEM ERA O LATERAL DIREITO E CAPITÃO?", "Carlos Alberto", "C. Alberto", ["Djalma Santos", "Zé Maria"], 0.13, 0.66),
        (Z1, "Brito", "Brito", ["Bellini", "Mauro Ramos"], 0.37, 0.76),
        (Z2, "Piazza", "Piazza", ["Bellini", "Orlando"], 0.63, 0.76),
        (LE, "Everaldo", "Everaldo", ["Nílton Santos", "Júnior"], 0.87, 0.66),
        (VOL, "Clodoaldo", "Clodoaldo", ["Zito", "Falcão"], 0.37, 0.54),
        ("E O MEIA CANHOTINHA?", "Gérson", "Gérson", ["Didi", "Zico"], 0.63, 0.54),
        ("QUEM ERA O PONTA QUE MARCOU EM TODOS OS JOGOS?", "Jairzinho", "Jairzinho", ["Garrincha", "Edu"], 0.15, 0.25),
        ("E O CENTROAVANTE?", "Tostão", "Tostão", ["Vavá", "Careca"], 0.4, 0.13),
        ("QUEM ERA O CAMISA 10?", "Pelé", "Pelé", ["Zico", "Sócrates"], 0.62, 0.2),
        ("E O DONO DA PATADA ATÔMICA?", "Rivelino", "Rivelino", ["Zagallo", "Éder"], 0.85, 0.3)]},
]
