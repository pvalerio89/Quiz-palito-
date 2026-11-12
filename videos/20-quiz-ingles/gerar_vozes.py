"""Narração do "Quiz de inglês do 5º ao 9º ano" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro (intro rapidinha), q1 (1ª pergunta, falada por cima dela), p1..pN (resposta), placar10.., outro.
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))

INTRO = "Bora testar seu inglês? Do quinto ao nono ano!"   # intro rapidinha (2 a 3 s)
SERIE = {
    5: "Valendo! Até onde você chega? Começando pelo quinto ano!",
    6: "Agora, sexto ano! Subindo o nível!",
    7: "Sétimo ano! Agora complica!",
    8: "Oitavo ano! Cuidado com as pegadinhas!",
    9: "Nono ano! O nível mais difícil!",
}
PLACAR = {
    10: "Dez perguntas! Quantas você acertou?",
    20: "Vinte! Continua contando os pontos!",
    30: "Trinta! Tá ficando difícil, hein?",
    40: "Quarenta! Se acertou mais de trinta, seu inglês é muito bom!",
    50: "Cinquenta! Agora só pergunta de nono ano!",
    60: "Sessenta! Só faltam cinco!",
}
OUTRO = ("E aí, até que série você chegou? Comenta a sua nota das sessenta e cinco aqui embaixo! "
         "Marca aquele amigo que diz que fala inglês, deixa o like e se inscreve no Quiz Palito! See you!")
FRASES = ["{x}", "{x}", "{x} Acertou?"]


def textos():
    R = json.load(open(os.path.join(HERE, "itens.json"), encoding="utf-8"))
    reg = {"intro": INTRO, **{f"placar{k}": v for k, v in PLACAR.items() if k < len(R)}, "outro": OUTRO}
    for i, r in enumerate(R):
        if i == 0 or R[i - 1]["serie"] != r["serie"]:
            reg[f"q{r['n']}"] = SERIE[r["serie"]]
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
