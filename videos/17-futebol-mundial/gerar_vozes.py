"""Narração do "Super quiz de futebol mundial" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro (intro rapidinha), q1 (1ª pergunta, falada por cima dela), p1..pN (resposta), placar10.., outro.
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))

INTRO = "Prepara a chuteira: super quiz de futebol!"   # intro rapidinha (2 a 3 s)
Q1 = "Só quem entende de futebol gabarita! Valendo! De que país é esse craque?"
PLACAR = {
    10: "Dez perguntas! Quantas você acertou?",
    20: "Vinte! Continua contando os pontos!",
    30: "Trinta! Agora começa a ficar difícil!",
    40: "Quarenta! Se acertou mais de trinta, você manja muito!",
    50: "Cinquenta! Agora só pergunta de quem acompanha futebol de verdade!",
    60: "Sessenta! Reta final, as mais difíceis!",
    70: "Setenta! Só faltam duas!",
}
OUTRO = ("E aí, quantas você acertou das setenta e duas? Comenta a sua nota aqui embaixo! "
         "Marca aquele amigo que se acha o rei do futebol, deixa o like e se inscreve no Quiz Palito! Até o próximo quiz!")
FRASES = ["{x}", "{x}", "{x} Acertou?"]


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
