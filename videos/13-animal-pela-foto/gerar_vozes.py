"""Narração do "Adivinhe o animal pelo zoom" (fotos reais) — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro, p1..pN (nome do animal), placar10/20/..., outro.
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))

INTRO = ("Fala, pessoal! Bem-vindos a mais um Quiz Palito! Hoje é o desafio dos animais pelo zoom: a foto começa "
         "bem de pertinho e vai abrindo. Você tem quatro segundos pra adivinhar o animal! Começa fácil e vai ficando "
         "difícil. Conta quantos você acerta. Valendo!")
PLACAR = {
    10: "Dez já foram! Quantos você acertou? Até aqui tava fácil, né?",
    20: "Vinte! Agora começa a ficar difícil. Continua contando!",
    30: "Trinta! Se você acertou mais de vinte e cinco, tá mandando muito bem!",
    40: "Quarenta! Quase metade! Bora que tem muito bicho ainda!",
    50: "Cinquenta! Agora vêm os animais do Brasil e os mais raros!",
    60: "Sessenta! Essa parte é só pra quem ama a natureza!",
    70: "Setenta! Tá chegando a parte mais difícil de todas!",
    80: "Oitenta! Últimos animais, os mais difíceis! Foco!",
}
OUTRO = ("E aí, quantos animais você acertou? Comenta aqui embaixo a sua nota! Marca um amigo pra ver quem conhece mais "
         "bicho, deixa o like e se inscreve no Quiz Palito! Até o próximo quiz!")
FRASES = ["{x}!", "É {x}!", "{x}! Acertou?", "{x}!", "Resposta: {x}!"]


def textos():
    R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
    reg = {"intro": INTRO, **{f"placar{k}": v for k, v in PLACAR.items() if k < len(R)}, "outro": OUTRO}
    for r in R:
        reg[f"p{r['n']}"] = FRASES[r["n"] % len(FRASES)].format(x=r.get("fala") or r["nome"])
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
