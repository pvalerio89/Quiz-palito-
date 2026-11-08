"""Narração do "Que estado é esse?" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro, q1..q27 (pergunta + alternativas), p1..p27 (resposta), placar10/20, outro.
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez", "onze", "doze",
       "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove", "vinte"]


def numero(n):
    if n <= 20:
        return NUM[n]
    d, u = divmod(n, 10)
    dez = {2: "vinte", 3: "trinta"}[d]
    return dez if u == 0 else f"{dez} e {NUM[u]}"


INTRO = ("Fala, pessoal! Bem-vindos a mais um Quiz Palito! Hoje é aula de geografia: você consegue reconhecer "
         "os vinte e sete estados do Brasil só pelo mapa? Um estado vai aparecer pintado de laranja. "
         "Você tem quatro alternativas e seis segundos pra responder. E na resposta eu ainda falo a capital! "
         "Pega papel e caneta, conta quantos você acerta e chama os amigos. Valendo!")
PLACAR = {
    10: "Dez estados! Quantos você já acertou? Guarda esse número, que agora começa a ficar difícil!",
    20: "Vinte estados! Faltam só sete, e são os mais difíceis. Atenção no mapa!",
}
OUTRO = ("E aí, quantos você acertou dos vinte e sete? Comenta aqui embaixo e diz de qual estado você é! "
         "Se acertou todos, você tá pronto pra prova de geografia! Manda esse vídeo pro seu amigo da escola, "
         "deixa o like e se inscreve no Quiz Palito! Até o próximo quiz!")
FRASES = [
    "Letra {L}! É {x}! E a capital é {c}!",
    "Resposta certa: {x}! Capital: {c}!",
    "É {x}, letra {L}! A capital é {c}!",
    "Letra {L}: {x}! A capital? {c}!",
    "É {x}! Capital: {c}! Acertou?",
]
LETRA = ["A", "B", "C", "D"]
LETRA_FALA = ["á", "bê", "cê", "dê"]


def textos():
    R = json.load(open(os.path.join(HERE, "perguntas.json"), encoding="utf-8"))
    reg = {"intro": INTRO, **{f"placar{k}": v for k, v in PLACAR.items()}, "outro": OUTRO}
    for r in R:
        n = r["n"]
        ops = r.get("falaop") or r["op"]
        alt = " ".join(f"{LETRA_FALA[i]}: {o}." for i, o in enumerate(ops))
        reg[f"q{n}"] = f"Estado {numero(n)}! {r.get('falap') or 'Que estado é esse?'} {alt}"
        x = r.get("fala") or (r.get("falaop") or r["op"])[r["certa"]]
        reg[f"p{n}"] = FRASES[n % len(FRASES)].format(L=LETRA_FALA[r["certa"]], x=x, c=r["capital"])
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
