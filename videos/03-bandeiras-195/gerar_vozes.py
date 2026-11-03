"""Narração do quiz "195 bandeiras" — voz Edge pt-BR-AntonioNeural +20% (grátis, sem limite).

Cria em assets/: intro.mp3, nivel1..3.mp3, aN.mp3 (nome do país) e outro.mp3; grava os textos em textos.json.
Uso: py -3 gerar_vozes.py            (gera só o que falta)
     py -3 gerar_vozes.py --tudo     (refaz tudo)
"""
import asyncio, json, os, sys, time
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))

INTRO = ("Fala, pessoal! Bem-vindos a mais um Quiz Palito! Hoje o desafio é gigante: "
         "adivinhar os cento e noventa e cinco países do mundo só pela bandeira! "
         "São três níveis: fácil, médio e difícil. E você tem só três segundos pra cada bandeira! "
         "Conta quantas você acertou e deixa aqui nos comentários. "
         "Deixa o like, se inscreve no canal, e bora começar!")
NIVEIS = {
    "nivel1": "Nível fácil! Que país é esse?",
    "nivel2": "Muito bem! Quantas você acertou até aqui? Agora vem o nível médio!",
    "nivel3": "Agora o bicho pega! Nível difícil! Só os gênios da geografia chegam até o fim!",
}
OUTRO = ("Ufa, chegamos ao fim! Foram cento e noventa e cinco bandeiras! "
         "Conta aqui nos comentários quantas você acertou, e marca aquele amigo que se acha o rei da geografia. "
         "Deixa o like, se inscreve no Quiz Palito, e até o próximo quiz!")
FALADO = {}  # ajustes de pronúncia, se precisar


def gerar(texto, destino):
    asyncio.run(edge_tts.Communicate(texto, "pt-BR-AntonioNeural", rate="+20%", pitch="+2Hz").save(destino))


def main():
    tudo = "--tudo" in sys.argv
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    A = lambda nome: os.path.join(HERE, "assets", nome)
    paises = json.load(open(os.path.join(HERE, "paises.json"), encoding="utf-8"))
    reg = {"intro": INTRO, **NIVEIS, "outro": OUTRO}
    for p in paises:
        reg[f"a{p['n']}"] = FALADO.get(p["nome"], p["nome"]) + "!"
    json.dump(reg, open(os.path.join(HERE, "textos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for i, (k, texto) in enumerate(reg.items(), 1):
        destino = A(f"{k}.mp3")
        if not tudo and os.path.exists(destino):
            continue
        for tent in range(4):
            try:
                gerar(texto, destino)
                break
            except Exception as e:
                print("erro", k, e, flush=True)
                time.sleep(3)
        print(f"{i}/{len(reg)} {k}", flush=True)
        time.sleep(0.2)


if __name__ == "__main__":
    main()
