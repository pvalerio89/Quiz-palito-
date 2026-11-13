"""Narração do "Capitais do Brasil e do mundo" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro (intro rapidinha), q1..qN (pergunta FALADA com as alternativas), p1..pN (resposta com
reação curta), placar10.., outro. Regra de retenção (2026-11-12): toda pergunta falada, contagem de 7 s.
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = ("um dois três quatro cinco seis sete oito nove dez onze doze treze catorze quinze dezesseis dezessete "
       "dezoito dezenove vinte").split()


def extenso(n):
    if n <= 20:
        return NUM[n - 1]
    d, u = divmod(n, 10)
    return ["", "", "vinte", "trinta"][d] + (f" e {NUM[u - 1]}" if u else "")


INTRO = "Chegou mais um Quiz Palito! Capitais!"   # intro rapidinha (2 a 3 s)
PLACAR = {
    10: "Dez já foram! Quantas você acertou?",
    20: "Vinte! Agora começa a ficar difícil!",
    30: "Trinta! Só faltam seis, e são as mais difíceis!",
}
OUTRO = "Quantas você acertou das trinta e seis? Comenta sua nota e se inscreve no Quiz Palito!"


def textos():
    R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
    reg = {"intro": INTRO, **{f"placar{k}": v for k, v in PLACAR.items() if k < len(R)}, "outro": OUTRO}
    for r in R:
        n = r["n"]
        a, b_, c = r["opcoes"]
        if n == 1:
            reg["q1"] = (f"São {extenso(len(R))} capitais, e no final fica difícil! Pergunta um: qual é a capital "
                         f"{r['de']}? {a}, {b_} ou {c}?")
        elif n == len(R):
            reg[f"q{n}"] = f"Última pergunta, a mais difícil! Qual é a capital {r['de']}? {a}, {b_} ou {c}?"
        else:
            reg[f"q{n}"] = f"Pergunta {extenso(n)}! Qual é a capital {r['de']}? {a}, {b_} ou {c}?"
        reg[f"p{n}"] = r["fala"]
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
