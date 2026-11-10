"""Narração do "Alfabeto dos times de A a Z" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro (intro rapidinha), q1 (1ª pergunta, falada por cima dela), p1..pN (resposta), placar10.., outro.
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))

INTRO = "Chegou o alfabeto dos times, de A a Z!"   # intro rapidinha (2 a 3 s)
Q1 = "Pelo escudo, valendo! Letra A: que time é esse?"
PLACAR = {
    10: "Dez já foram! Quantos escudos você acertou?",
    20: "Vinte! Tá indo bem? Continua contando!",
    30: "Trinta! Se acertou mais de vinte e cinco, você é craque!",
    40: "Quarenta! Agora vêm os gigantes da Europa e da América!",
    50: "Cinquenta! Faltam poucas letras, foco!",
    60: "Sessenta! Agora as letras mais difíceis do alfabeto!",
    70: "Setenta! Reta final!",
    80: "Oitenta! Só falta o fim do alfabeto!",
}
OUTRO = ("E aí, quantos escudos você acertou de A a Z? Comenta a sua nota e o seu time do coração aqui embaixo! "
         "Marca aquele amigo que se acha o rei do futebol, deixa o like e se inscreve no Quiz Palito! Até o próximo quiz!")
FRASES = ["{x}!", "É {x}!", "{x}! Acertou?", "{x}!", "Resposta: {x}!", "{x}! Acertou essa?"]


def textos():
    R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
    reg = {"intro": INTRO, "q1": Q1, **{f"placar{k}": v for k, v in PLACAR.items() if k < len(R)}, "outro": OUTRO}
    for r in R:
        reg[f"p{r['n']}"] = FRASES[r["n"] % len(FRASES)].format(x=r["fala"])
    return reg


def gerar(texto, destino):
    asyncio.run(edge_tts.Communicate(texto, "pt-BR-AntonioNeural", rate="+20%", pitch="+2Hz").save(destino))


def main():
    tudo = "--tudo" in sys.argv
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    reg = textos()
    json.dump(reg, open(os.path.join(HERE, "textos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for i, (k, t) in enumerate(reg.items(), 1):
        dst = os.path.join(HERE, "assets", f"{k}.mp3")
        if not tudo and os.path.exists(dst):
            continue
        for _ in range(4):
            try:
                gerar(t, dst)
                break
            except Exception as e:
                print("erro", k, e, flush=True)
                time.sleep(3)
        print(f"{i}/{len(reg)} {k}", flush=True)


if __name__ == "__main__":
    main()
