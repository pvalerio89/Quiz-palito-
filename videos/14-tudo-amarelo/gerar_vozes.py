"""Narração do "Quiz, mas tudo é amarelo" (fotos reais) — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro, p1..pN (nome do lugar/objeto/animal), placar10/20/..., outro.
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))

INTRO = ("Atenção, que hoje o desafio do Quiz Palito é diferente: tudo é amarelo! Lugares famosos, "
         "objetos e animais, todos pintados de amarelo. Sem a cor, você reconhece? Quatro segundos pra cada um. "
         "Conta quantos você acerta. Valendo!")
PLACAR = {
    10: "Dez já foram! Quantos você acertou? Sem cor fica mais difícil, né?",
    20: "Vinte! Agora começa a complicar. Continua contando!",
    30: "Trinta! Se você acertou mais de vinte e cinco, tá com olho de águia!",
    40: "Quarenta! Mais da metade! Agora vêm os objetos!",
    50: "Cinquenta! Esses aí são de enganar, presta atenção!",
    60: "Sessenta! Últimos, os mais difíceis! Foco!",
    70: "Setenta! Tá quase no fim!",
}
OUTRO = ("E aí, quantos você acertou só pelo amarelo? Comenta aqui embaixo a sua nota! Marca um amigo pra ver quem "
         "tem o olho melhor, deixa o like e se inscreve no Quiz Palito! Até o próximo quiz!")
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
