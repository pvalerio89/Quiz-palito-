"""Narração do vídeo 51 "Bandeiras: fácil, médio, difícil e impossível" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro, q1..qN (pergunta falada com as alternativas), p1..pN (resposta com reação), d<n> (dica),
s<n> (suspense), curtir/espero, placar10.., ultima, outro. O Palito não fala (Patrick, 2026-11-13).
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))

INTRO = "Ei! Bora pro desafio das bandeiras?"      # intro rapidinha (2 a 3 s), saudação variada
Q1 = "Trinta e seis bandeiras, quatro níveis. Conta quantas você acerta! "   # gancho falado na 1ª pergunta
CURTIR = "Antes de continuar... se inscreva no canal e deixe seu like!"
ESPERO = "Vai lá, eu espero!"
PLACAR = {   # telas de nível (antes das perguntas 10, 19 e 28)
    10: "Acabou o fácil! Agora é nível médio!",
    19: "Nível difícil! Agora aparecem as bandeiras parecidas!",
    28: "Chegou o nível impossível! Boa sorte!",
}
ULTIMA = "Atenção... última bandeira! E é a mais difícil do vídeo!"
OUTRO = "Até qual nível você chegou? Se inscreve no canal!"


def textos():
    R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
    reg = {"intro": INTRO, "curtir": CURTIR, "espero": ESPERO, "ultima": ULTIMA, "outro": OUTRO,
           **{f"nivel{k}": v for k, v in PLACAR.items()}}
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
