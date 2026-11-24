"""Rodadas do vídeo 53 "Não diga o mesmo que o Palito 2" -> itens.json.

Cada rodada: pedido curto, emoji do pedido, resposta do Palito (a mais comum), emoji da resposta (ou "" = número),
fala da resposta com reação. Nenhum pedido repete o vídeo 05 (rodadas.json de videos/05-nao-diga-o-mesmo).
Uso: py -3 itens.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

# pedido, emoji, resposta, emoji da resposta, fala da resposta (reação), extras
R = [
    ("DIGA UM ANIMAL DA FAZENDA", "🚜", "VACA", "🐄", "O Palito disse vaca! Disse vaca também? Tira uma vida!"),
    ("DIGA UMA FORMA GEOMÉTRICA", "📐", "QUADRADO", "🟦", "Quadrado! Se você pensou no quadrado, perdeu uma!"),
    ("DIGA UM NÚMERO DE 1 A 5", "🔢", "3", "", "Três! O número do meio é o que mais sai. Pensou igual? Menos uma vida!"),
    ("DIGA UMA FLOR", "🌸", "ROSA", "🌹", "Rosa! A flor que quase todo mundo fala primeiro."),
    ("DIGA UM PASSARINHO", "🐦", "PAPAGAIO", "🦜", "Papagaio! Falou papagaio? Tchau, uma vida!"),
    ("DIGA UMA COMIDA DO CAFÉ DA MANHÃ", "☕", "PÃO", "🍞", "Pão! Com manteiga, de preferência. Pensou igual? Perde uma!"),
    ("DIGA UM PERSONAGEM DA TURMA DA MÔNICA", "📖", "CEBOLINHA", "🐰", "Cebolinha! Se você disse Cebolinha, perdeu uma vida!"),
    ("DIGA UM ELETRODOMÉSTICO", "🔌", "GELADEIRA", "🧊", "Geladeira! Pensou na geladeira? Menos um coração!"),
    ("DIGA UMA PEÇA DE ROUPA", "👗", "CAMISETA", "👕", "Camiseta! Disse igual ao Palito? Perde uma!"),
    ("DIGA UM JOGO DE VIDEOGAME", "🎮", "MINECRAFT", "⛏️", "Minecraft! Esse é campeão. Falou igual? Tira uma vida!"),
    ("DIGA UM MEIO DE TRANSPORTE", "🚦", "CARRO", "🚗", "Carro! O mais óbvio de todos. Perdeu uma?"),
    ("DIGA UM DINOSSAURO", "🦕", "TIRANOSSAURO REX", "🦖", "Tiranossauro rex! Pensou no T-rex? Menos uma vida!"),
    ("DIGA UMA FRUTA VERMELHA", "🍒", "MORANGO", "🍓", "Morango! Se disse morango, perdeu uma!"),
    ("DIGA UM CALÇADO", "👞", "TÊNIS", "👟", "Tênis! Pensou igual ao Palito? Tchau, uma vida!"),
    ("DIGA UM ESPORTE... MAS NÃO VALE FUTEBOL!", "🚫", "VÔLEI", "🏐", "Vôlei! Sem o futebol, quase todo mundo vai no vôlei.", {"pegadinha": True}),
    ("DIGA UM ANIMAL DO PANTANAL", "🌿", "JACARÉ", "🐊", "Jacaré! Disse jacaré? Perde uma vida!"),
    ("DIGA UM MATERIAL ESCOLAR", "🎒", "LÁPIS", "✏️", "Lápis! Se você falou lápis, menos um coração!"),
    ("DIGA UM LANCHE", "🍟", "HAMBÚRGUER", "🍔", "Hambúrguer! Deu fome, né? Pensou igual? Perde uma!"),
    ("DIGA UMA BRINCADEIRA DE CRIANÇA", "🧒", "ESCONDE-ESCONDE", "🙈", "Esconde-esconde! Pensou nessa? Menos um coração!"),
    ("DIGA UM CÔMODO DA CASA", "🏠", "COZINHA", "🍳", "Cozinha! Disse cozinha? Tira uma vida!"),
    ("DIGA UMA CIDADE FORA DO BRASIL", "🌍", "PARIS", "🗼", "Paris! A cidade da Torre Eiffel. Falou igual? Perdeu uma!"),
    ("DIGA UM NÚMERO PAR MENOR QUE 10", "🔢", "4", "", "Quatro! Se você disse quatro, menos uma vida!"),
    ("DIGA UM FILME DE DESENHO", "🎬", "FROZEN", "❄", "Frozen! Livre estou... e você, perdeu uma vida?"),
    ("DIGA UM DOCE... MAS NÃO VALE BRIGADEIRO!", "🚫", "BEIJINHO", "🥥", "Beijinho! O irmão do brigadeiro. Pensou igual? Perde uma!", {"pegadinha": True}),
    ("DIGA UMA FERRAMENTA", "🧰", "MARTELO", "🔨", "Martelo! Disse martelo? Tchau, uma vida!"),
    ("DIGA UM ESTADO DO BRASIL", "🗺️", "RIO DE JANEIRO", "🏖", "Rio de Janeiro! Falou o Rio? Menos um coração!"),
    ("DIGA UM ANIMAL QUE PULA", "🌳", "CANGURU", "🦘", "Canguru! O campeão do pulo. Falou igual? Perdeu uma!"),
    ("DIGA UM PEIXE", "🎣", "SALMÃO", "🐟", "Salmão! Pensou no salmão? Perde uma vida!"),
    ("DIGA ALGO QUE CAI DO CÉU", "☁️", "CHUVA", "🌧", "Chuva! Quem disse chuva, perdeu uma!"),
    ("DIGA UM SABOR DE SUCO", "🍹", "LARANJA", "🍊", "Laranja! O suco mais pedido do Brasil. Disse igual? Tira uma vida!"),
    ("DIGA UMA COR DO ARCO-ÍRIS... MAS NÃO VALE VERMELHO!", "🌈", "AMARELO", "🟡", "Amarelo! Sem o vermelho, o amarelo é o que mais sai. Perdeu uma?", {"pegadinha": True}),
    ("DIGA UM INSETO BONITO", "🌼", "BORBOLETA", "🦋", "Borboleta! Disse borboleta? Tchau, uma vida!"),
    ("DIGA UM VILÃO", "😈", "CORINGA", "🃏", "Coringa! O vilão mais famoso. Pensou igual? Perde uma vida!"),
    ("DIGA UM ANIMAL COM A LETRA G", "🔤", "GATO", "🐱", "Gato! Se você disse gato, miau... menos uma vida!"),
    ("DIGA UMA POSIÇÃO DO FUTEBOL", "🥅", "ATACANTE", "⚽", "Atacante! Quem faz os gols. Disse igual? Perdeu uma!"),
    ("DIGA ALGO QUE TEM NO BANHEIRO", "🚿", "SABONETE", "🧼", "Sabonete! Pensou no sabonete? Tira uma vida!"),
    ("DIGA UMA SOBREMESA", "🍽", "PUDIM", "🍮", "Pudim! Aquele de leite condensado. Pensou igual? Perde uma!"),
    ("DIGA UM FERIADO", "📅", "NATAL", "🎄", "Natal! O feriado preferido de quase todo mundo. Perdeu uma?"),
    ("DIGA UM CONTINENTE", "🌎", "EUROPA", "🏰", "Europa! Falou Europa? Menos um coração!"),
    ("DIGA UMA PALAVRA EM INGLÊS", "🔠", "HELLO", "👋", "Hello! O famoso olá. Pensou igual? Perde uma vida!"),
    ("DIGA UM ANIMAL QUE VIVE NO GELO", "🧊", "PINGUIM", "🐧", "Pinguim! Disse pinguim? Tchau, uma vida!"),
    ("DIGA UM DINHEIRO DE OUTRO PAÍS", "💰", "DÓLAR", "💵", "Dólar! O mais conhecido do mundo. Falou igual? Perdeu uma!"),
    ("DIGA UM PLANETA... MAS NÃO VALE A TERRA!", "🪐", "MARTE", "🔴", "Marte! O planeta vermelho. Pensou igual? Menos uma vida!", {"pegadinha": True}),
    ("DIGA UMA COISA AMARELA... QUE NÃO SEJA FRUTA!", "🟨", "SOL", "☀️", "O Palito disse... o sol! Se você disse sol, perdeu mais uma vida!", {"pegadinha": True, "final": True}),
]
# falas do pedido quando o texto escrito não soa bem falado
FALA_Q = {"DIGA UM NÚMERO DE 1 A 5": "Diga um número de um a cinco!",
          "DIGA UM NÚMERO PAR MENOR QUE 10": "Diga um número par, menor que dez!",
          "DIGA UM PLANETA... MAS NÃO VALE A TERRA!": "Pegadinha! Diga um planeta... mas não vale a Terra!",
          "DIGA UMA COISA AMARELA... QUE NÃO SEJA FRUTA!": "A mais difícil: diga uma coisa amarela... que não seja fruta!",
          "DIGA UM ESPORTE... MAS NÃO VALE FUTEBOL!": "Pegadinha! Diga um esporte... mas não vale futebol!",
          "DIGA UM DOCE... MAS NÃO VALE BRIGADEIRO!": "Pegadinha! Diga um doce... mas não vale brigadeiro!",
          "DIGA UMA COR DO ARCO-ÍRIS... MAS NÃO VALE VERMELHO!": "Pegadinha! Diga uma cor do arco-íris... mas não vale vermelho!",
          "DIGA UM PERSONAGEM DA TURMA DA MÔNICA": "Diga um personagem da Turma da Mônica!",
          "DIGA UMA PALAVRA EM INGLÊS": "Agora em inglês: diga uma palavra em inglês!"}
# entradas variadas antes do pedido (sem "Rodada X!" em toda rodada)
ENTRADA = {2: "Agora:", 4: "Rápido!", 6: "Essa é fácil:", 8: "Pensa rápido!", 10: "Rodada dez!", 11: "Bora:",
           13: "Agora uma gostosa:", 18: "Deu fome?", 20: "Rodada vinte!",
           22: "Essa divide a família:", 25: "Agora:", 28: "Vamos pro mar:", 29: "Rápido!", 30: "Rodada trinta!",
           33: "Essa é difícil de fugir:", 35: "Pensa rápido!", 37: "Essa é boa:",
           41: "Vamos pro frio:", 42: "Quase acabando:"}


def main():
    out = []
    for n, r in enumerate(R, 1):
        ped, em, resp, er, fala = r[:5]
        ex = r[5] if len(r) > 5 else {}
        q = FALA_Q.get(ped) or (ped[0] + ped[1:].lower() + "!")
        ent = ENTRADA.get(n)
        if ent and not q.startswith(("Pegadinha", "Agora em", "A mais")):
            q = f"{ent} {q[0].lower()}{q[1:]}"
        for a, b in (("brasil", "Brasil"), ("letra g", "letra G"), ("pantanal", "Pantanal")):
            q = q.replace(a, b)
        item = {"n": n, "pedido": ped, "emoji": em, "resposta": resp, "er": er, "fala_q": q, "fala_r": fala, **ex}
        out.append(item)
    json.dump(out, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out), "rodadas")


if __name__ == "__main__":
    main()
