"""Gera itens.json do vídeo 36 "Brasil x Portugal: como se diz em Portugal?" (estilo mais humano).

O cartão mostra a FOTO REAL do objeto (Wikimedia Commons; créditos na tela final) com a palavra do Brasil embaixo;
as 3 alternativas são palavras do português de Portugal (só uma quer dizer a mesma coisa; as erradas são palavras de
Portugal para outras coisas ou parecidas). Das fáceis às bizarras. Palavras conferidas em 2026-11-18.
Uso: py -3 itens.py
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))

# palavra no Brasil (= nome na lista de fotos), certa em Portugal, [2 erradas], entrada falada, fala da resposta, extras
P = [
    ("ônibus", "AUTOCARRO", ["COMBOIO", "ELÉTRICO"], "Pra começar, uma fácil!",
     "Autocarro! Em Portugal, o ônibus é o autocarro!", {"count": 4.0}),
    ("trem", "COMBOIO", ["AUTOCARRO", "CAMIÃO"], "Agora mais um transporte!",
     "Comboio! Lá ninguém pega o trem, pega o comboio!", {"count": 4.0}),
    ("celular", "TELEMÓVEL", ["ECRÃ", "AUSCULTADOR"], "Essa todo mundo usa!",
     "Telemóvel! O celular em Portugal é o telemóvel!", {"count": 5.0}),
    ("geladeira", "FRIGORÍFICO", ["ARCA", "DESPENSA"], "Agora uma da cozinha!",
     "Frigorífico! Em Portugal a geladeira é o frigorífico!", {}),
    ("sorvete", "GELADO", ["NATAS", "GELATINA"], "Bora pra sobremesa!",
     "Gelado! Em Portugal você pede um gelado!", {}),
    ("suco", "SUMO", ["BATIDO", "NÉCTAR"], "Agora uma bebida!",
     "Sumo! E batido lá é o nosso milk-shake!", {}),
    ("café da manhã", "PEQUENO-ALMOÇO", ["LANCHE", "MERENDA"], "Essa é a primeira refeição do dia!",
     "Pequeno-almoço! O almoço deles é o almoço mesmo, e o café da manhã é o pequeno-almoço!", {}),
    ("banheiro", "CASA DE BANHO", ["LAVABO", "SANITA"], "Agora um cômodo da casa!",
     "Casa de banho! Lá você pergunta: onde fica a casa de banho?", {}),
    ("caminhão", "CAMIÃO", ["CARRINHA", "CAMIONETA"], "Cuidado, que essa engana!",
     "Camião! E camioneta lá é ônibus de viagem!", {"aviso": "TEM PEGADINHA!"}),
    ("mouse", "RATO", ["CURSOR", "TECLA"], "Agora uma do computador!",
     "Rato! Em Portugal o mouse virou rato mesmo!", {}),
    ("tela", "ECRÃ", ["VISOR", "PAINEL"], "Mais uma do computador!",
     "Ecrã! Tela de computador ou de televisão, lá é ecrã!", {}),
    ("grama", "RELVA", ["PASTO", "MATO"], "Essa tem em todo campo de futebol!",
     "Relva! O gramado do estádio lá é o relvado!", {}),
    ("xícara", "CHÁVENA", ["TAÇA", "CANECA"], "Agora uma da hora do café!",
     "Chávena! Uma chávena de café, por favor!", {"dica": ("Dica: começa com a letra C!", "COMEÇA COM C")}),
    ("cardápio", "EMENTA", ["RECEITA", "TABELA"], "Bora pro restaurante!",
     "Ementa! No restaurante, você pede a ementa!", {}),
    ("garçom", "EMPREGADO DE MESA", ["MORDOMO", "PAQUETE"], "Ainda no restaurante!",
     "Empregado de mesa! E paquete lá é navio grande!", {}),
    ("terno", "FATO", ["CASACO", "BLAZER"], "Agora uma roupa chique!",
     "Fato! Em Portugal o noivo casa de fato!", {}),
    ("suéter", "CAMISOLA", ["CAMISA DE LÃ", "BLUSÃO"], "Essa aqui confunde muito brasileiro!",
     "Camisola! Aqui camisola é roupa de dormir, mas lá é o nosso suéter!",
     {"aviso": "TEM PEGADINHA!", "suspense": True, "sabia": "CAMISOLA LÁ É BLUSA DE FRIO"}),
    ("fila", "BICHA", ["CAUDA", "RENQUE"], "Essa aqui é famosa!",
     "Bicha! Em Portugal você entra na bicha do autocarro!", {}),
    ("pedestre", "PEÃO", ["ANDARILHO", "CAMINHANTE"], "Agora uma da rua!",
     "Peão! Quem anda a pé lá é peão, igual no xadrez!", {}),
    ("faixa de pedestres", "PASSADEIRA", ["ZEBRA", "TRAVESSIA"], "Ainda na rua!",
     "Passadeira! O peão atravessa na passadeira!", {}),
    ("ponto de ônibus", "PARAGEM", ["APEADEIRO", "ESTAÇÃO"], "Onde você espera o autocarro?",
     "Paragem! E apeadeiro é uma paradinha pequena de comboio!", {}),
    ("bonde", "ELÉTRICO", ["FUNICULAR", "COMBOIO"], "Esse é famoso em Lisboa!",
     "Elétrico! O amarelinho de Lisboa é o elétrico!", {}),
    ("goleiro", "GUARDA-REDES", ["DEFESA", "GUARDA-BALIZA"], "Agora uma de futebol!",
     "Guarda-redes! E o gol, lá, é a baliza!", {}),
    ("abacaxi", "ANANÁS", ["PAPAIA", "MARACUJÁ"], "Agora uma fruta!",
     "Ananás! Em Portugal o abacaxi é ananás!", {}),
    ("bala", "REBUÇADO", ["GOMA", "PASTILHA"], "Bora pros doces!",
     "Rebuçado! A bala lá é rebuçado!", {"dica": ("Dica: começa com a letra R!", "COMEÇA COM R")}),
    ("chiclete", "PASTILHA ELÁSTICA", ["REBUÇADO", "GOMA DOCE"], "Mais um doce!",
     "Pastilha elástica! O chiclete lá estica até no nome!", {}),
    ("presunto", "FIAMBRE", ["CHOURIÇO", "PAIO"], "Agora uma do lanche!",
     "Fiambre! O presunto do sanduíche lá é fiambre!", {}),
    ("misto-quente", "TOSTA MISTA", ["PREGO", "SANDES QUENTE"], "Essa aqui dá fome!",
     "Tosta mista! E prego lá é sanduíche de bife!", {"sabia": "PREGO LÁ É SANDUÍCHE DE BIFE"}),
    ("açougue", "TALHO", ["MERCEARIA", "TASCA"], "Agora uma loja!",
     "Talho! Em Portugal a carne se compra no talho!", {}),
    ("vaso sanitário", "SANITA", ["LAVATÓRIO", "BIDÉ"], "De volta pra casa de banho!",
     "Sanita! E lavatório lá é a pia!", {}),
    ("curativo", "PENSO RÁPIDO", ["LIGADURA", "ADESIVO"], "Machucou? Usa um...",
     "Penso rápido! O band-aid lá é penso rápido!", {}),
    ("grampeador", "AGRAFADOR", ["FURADOR", "CLIPE"], "Agora uma da escola!",
     "Agrafador! O grampo lá é agrafo!", {}),
    ("fita adesiva", "FITA-COLA", ["FITA-GOMA", "DUREX"], "Mais uma do material escolar!",
     "Fita-cola! Lá ela cola até no nome!", {}),
    ("fone de ouvido", "AUSCULTADORES", ["ESCUTADORES", "OUVIDEIROS"], "Essa é bem difícil!",
     "Auscultadores! Parece coisa de médico, mas é o fone!", {"suspense": True}),
    ("encanador", "CANALIZADOR", ["TUBISTA", "CANOEIRO"], "Agora uma profissão!",
     "Canalizador! Quem conserta o cano lá é o canalizador!", {}),
    ("aeromoça", "HOSPEDEIRA DE BORDO", ["GUIA DE BORDO", "AJUDANTE DE VOO"], "Mais uma profissão!",
     "Hospedeira de bordo! É a aeromoça de Portugal!", {}),
    ("salva-vidas", "NADADOR-SALVADOR", ["BANHISTA", "GUARDA-MAR"], "Bora pra praia!",
     "Nadador-salvador! E banhista é quem vai tomar banho de mar!", {}),
    ("placa do carro", "MATRÍCULA", ["CHAPA", "ALVARÁ"],
     "Valendo o título de mestre da língua: como se diz placa do carro em Portugal?",
     "Matrícula! Em Portugal o carro tem matrícula! Se acertou essa, você é fera!",
     {"final": True, "suspense": True}),
]


def main():
    FOTOS = json.load(open(os.path.join(HERE, "fotos.json"), encoding="utf-8"))   # palavra -> foto (as que vieram)
    itens = [p for p in P if p[0] in FOTOS]
    rnd = random.Random(36)
    pos = [0, 1, 2] * 14
    rnd.shuffle(pos)
    pos[0], pos[1], pos[2] = 2, 0, 1
    R = []
    for n, (br, certa, err, fq, fr, ex) in enumerate(itens, 1):
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        falas = [o.lower() for o in ops]
        r = {"n": n, "pergunta": "COMO SE DIZ EM PORTUGAL?", "br": br.upper(), "foto": FOTOS[br],
             "opcoes": ops, "certa": pos[n - 1],
             "fala_q": f"{fq} {br.capitalize()}, em Portugal, é... {falas[0]}, {falas[1]} ou {falas[2]}?"
             if not ex.get("final") else f"{fq} {falas[0]}, {falas[1]} ou {falas[2]}?",
             "fala_r": fr, "count": ex.get("count", 7.0)}
        if "dica" in ex:
            r["fala_d"], r["dica_txt"] = ex["dica"]
        for k in ("aviso", "sabia", "final"):
            if k in ex:
                r[k] = ex[k]
        if ex.get("suspense"):
            r["fala_s"] = "A resposta é..." if not ex.get("final") else "Valendo o título... a resposta é..."
        R.append(r)
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas", [r["certa"] for r in R])


if __name__ == "__main__":
    main()
