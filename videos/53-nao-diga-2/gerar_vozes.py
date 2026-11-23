"""Narração do vídeo 53 "Não diga o mesmo que o Palito 2" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro, q1..q44 (pedido com entrada variada), p1..p44 (resposta do Palito com reação),
curtir/espero, vidas10/20/30, ultima, outro. O Palito não fala (Patrick, 2026-11-13): quem fala é o narrador.
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))

INTRO = "Ei, o Palito voltou pra revanche! Não diga o mesmo que ele, parte dois!"   # intro rapidinha, saudação nova
Q1 = ("Você tem oito vidas. Pensou igual ao Palito? Perde uma! São quarenta e quatro rodadas, "
      "e a última é a mais difícil. Valendo! ")
CURTIR = "Antes da próxima... se inscreva no canal e deixe seu like!"
ESPERO = "Vai lá, eu espero!"
VIDAS = {
    10: "Dez rodadas! Conta aí: quantas vidas ainda sobraram?",
    20: "Vinte rodadas! Se você ainda tem as oito vidas, você pensa muito diferente!",
    30: "Trinta! Agora vêm as pegadinhas. Segura essas vidas!",
}
ULTIMA = "Atenção... última rodada! E é a mais difícil de fugir do Palito!"
OUTRO = "Com quantas vidas você terminou? Comenta aí e se inscreve no canal!"


def textos():
    R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
    reg = {"intro": INTRO, "curtir": CURTIR, "espero": ESPERO, "ultima": ULTIMA, "outro": OUTRO,
           **{f"vidas{k}": v for k, v in VIDAS.items()}}
    for r in R:
        n = r["n"]
        reg[f"q{n}"] = (Q1 if n == 1 else "") + r["fala_q"]
        reg[f"p{n}"] = r["fala_r"]
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
        if os.path.exists(dst) and os.path.getsize(dst) < 1024:
            os.remove(dst)   # mp3 vazio (Edge falhou): refaz
        if not tudo and os.path.exists(dst):
            continue
        for _ in range(4):
            try:
                gerar(t, dst)
                if os.path.getsize(dst) >= 1024:
                    break
            except Exception as e:
                print("erro", k, e, flush=True)
            time.sleep(3)
        print(f"{i}/{len(reg)} {k}", flush=True)


if __name__ == "__main__":
    main()
