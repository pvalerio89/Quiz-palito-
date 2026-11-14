"""Narração do vídeo 28 "Eu já ou eu nunca?" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro, q1..qN (frase falada), p1..pN (% + reação), anotar (chamada de anotar nos comentários),
curtir/espero, placar10.., ultima, outro. O Palito não fala (Patrick, 2026-11-13).
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))

INTRO = "Hora da verdade! Eu já ou eu nunca?"      # intro rapidinha (2 a 3 s), saudação variada
# chamada de anotar (Patrick, 2026-11-12; engaja.CHAMADAS_ANOTAR, diferente da do vídeo 19)
ANOTAR = ("São cinquenta frases, e não vale mentir! Clica no coração, abre os comentários e vai anotando "
          "quantos eu já você tem. Terminou o vídeo? É só enviar!")
CURTIR = "Ei, rapidinho... se tá curtindo, deixa o like e o coraçãozinho aí!"
ESPERO = "Tô esperando, hein!"
PLACAR = {
    10: "Dez frases! Quantos eu já você tem até agora?",
    20: "Vinte! Vai contando aí nos comentários!",
    30: "Trinta! Agora começam as mais raras!",
    40: "Quarenta! Só faltam dez!",
}
ULTIMA = "Atenção... essa é a última! E quase ninguém já fez!"
OUTRO = "Curtiu? Então se inscreve no canal!"


def textos():
    R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
    reg = {"intro": INTRO, "anotar": ANOTAR, "curtir": CURTIR, "espero": ESPERO, "ultima": ULTIMA, "outro": OUTRO,
           **{f"placar{k}": v for k, v in PLACAR.items() if k < len(R)}}
    for r in R:
        n = r["n"]
        reg[f"q{n}"] = r["fala_q"]
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
