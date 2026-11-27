"""Narração do vídeo 59 "Science Review, 3rd grade" — TODA EM INGLÊS (Patrick 2026-11-26): Edge en-US-AndrewMultilingualNeural.

Cria em assets/: intro, q1..qN (pergunta falada com as alternativas), p1..pN (resposta com reação), s<n> (suspense),
curtir/espero, placar10.., ultima, outro. O Palito não fala (Patrick, 2026-11-13).
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))
VOZ = "en-US-AndrewMultilingualNeural"   # vídeo em inglês

INTRO = "Science test is coming! Let's review water, food and the amazing camel!"   # intro rapidinha, saudação variada
Q1 = "Forty-nine review questions, from medium to very hard, and the last one is worth the grade! "   # gancho falado na 1ª pergunta
CURTIR = "Before we keep going... subscribe to the channel and leave a like!"
ESPERO = "Go ahead, I'll wait!"
PLACAR = {
    10: "Ten questions done! Do you remember everything?",
    20: "Twenty done! How many did you get right?",
    30: "Thirty! Get ready, the very hard level is coming!",
    40: "Forty! Only nine to go!",
}
ULTIMA = "Last question! This one is worth the grade!"
OUTRO = "So, are you ready for the science test? Subscribe to the channel!"


def textos():
    R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
    reg = {"intro": INTRO, "curtir": CURTIR, "espero": ESPERO, "ultima": ULTIMA, "outro": OUTRO,
           **{f"placar{k}": v for k, v in PLACAR.items() if k < len(R)}}
    for r in R:
        n = r["n"]
        reg[f"q{n}"] = (Q1 if n == 1 else "") + r["fala_q"]
        reg[f"p{n}"] = r["fala_r"]
        if "fala_d" in r:
            reg[f"d{n}"] = r["fala_d"]
        if "fala_s" in r:
            reg[f"s{n}"] = r["fala_s"]
    return reg


def gerar(texto, destino):
    asyncio.run(edge_tts.Communicate(texto, VOZ, rate="+8%").save(destino))


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
