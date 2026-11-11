"""Narração do "Monte o time" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro, q<n> (1ª pergunta de cada time, com o nome do time), p1..pN (resposta), completo0..5, outro.
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from dados import TIMES

INTRO = "Desafio rápido: monte o time campeão!"   # intro rapidinha (2 a 3 s)
ORD = ["um", "dois", "três", "quatro", "cinco", "seis"]
COMPLETO = [
    "Time completo! Quantos do penta você acertou?",
    "Time completo! Quantos desse Real Madrid você lembrou?",
    "Time completo! Acertou os campeões do mundo?",
    "Time completo! Esse Barça jogava demais! Quantos você acertou?",
    "Time completo! Agora a mais difícil: o Brasil de 1970!",
    "Time completo! Esse é o tri! Quantos você sabia?",
]
OUTRO = ("E aí, quantos jogadores você acertou nos seis times? Comenta a sua nota e qual time você quer no próximo! "
         "Marca aquele amigo que se acha o rei do futebol, deixa o like e se inscreve no Quiz Palito! Até o próximo quiz!")
FRASES = ["{x}!", "Era o {x}!", "{x}! Acertou?", "{x}!", "Resposta: {x}!"]


def textos():
    R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
    reg = {"intro": INTRO, **{f"completo{i}": t for i, t in enumerate(COMPLETO)}, "outro": OUTRO}
    for r in R:
        if r["slot"] == 0:
            tm = TIMES[r["time"]]
            pre = "Valendo! " if r["n"] == 1 else ""
            reg[f"q{r['n']}"] = f"{pre}Time {ORD[r['time']]}: {tm['fala']}. Quem era o goleiro?"
        reg[f"p{r['n']}"] = FRASES[r["n"] % len(FRASES)].format(x=r["nome"])
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
