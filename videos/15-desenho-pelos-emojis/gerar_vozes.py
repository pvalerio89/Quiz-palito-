"""Narração do "Adivinhe o desenho pelos emojis" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: q1 (apresentação + 1ª pergunta, falada por cima dela), p1..pN (resposta), placar10.., outro.
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))

Q1 = "Ei, você que cresceu vendo desenho! Descubra qual é pelos emojis. Valendo! Que desenho é esse?"
PLACAR = {
    10: "Dez já foram! Quantos você acertou? Essas eram as fáceis!",
    20: "Vinte! Tá ficando bom, hein? Continua contando!",
    30: "Trinta! Agora vêm os filmes que todo mundo viu, mas ninguém lembra!",
    40: "Quarenta! Se acertou mais de trinta, você é fera em desenho!",
    50: "Cinquenta! Agora só os clássicos, os mais difíceis!",
    60: "Sessenta! Últimos! Esses só quem é das antigas acerta!",
}
OUTRO = ("E aí, quantos desenhos você acertou pelos emojis? Comenta a sua nota aqui embaixo! Marca aquele amigo "
         "que vivia vendo desenho, deixa o like e se inscreve no Quiz Palito! Até o próximo quiz!")
FRASES = ["{x}!", "É {x}!", "{x}! Acertou?", "{x}!", "Resposta: {x}!", "{x}! Fácil, né?"]


def textos():
    R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
    reg = {"q1": Q1, **{f"placar{k}": v for k, v in PLACAR.items() if k < len(R)}, "outro": OUTRO}
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
