"""Narração do "Não diga o mesmo que o Palito" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro, q1..q40 (pedido), p1..p40 (resposta do Palito), vidas10/20/30, outro.
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
    dez = {2: "vinte", 3: "trinta", 4: "quarenta"}[d]
    return dez if u == 0 else f"{dez} e {NUM[u]}"


INTRO = ("Fala, pessoal! Bem-vindos a mais um Quiz Palito! Hoje o jogo é: não diga o mesmo que o Palito! "
         "Você começa com oito vidas. Em cada rodada aparece um pedido, tipo: diga uma fruta. "
         "Pensa rápido na sua resposta antes do tempo acabar! Depois o Palito revela a resposta dele. "
         "Se você pensou igual ao Palito, perde uma vida! São quarenta rodadas. Valendo!")
VIDAS = {
    10: "Dez rodadas! Quantas vidas você ainda tem? Conta aí e bora pra próxima!",
    20: "Metade do jogo! Se você ainda tem as oito vidas, você é muito original!",
    30: "Trinta rodadas! Faltam só dez. Segura essas vidas!",
}
OUTRO = ("E aí, com quantas vidas você terminou? Comenta aqui embaixo! Se terminou com as oito, você é um gênio da "
         "originalidade! Marca um amigo pra ver se ele termina com mais vidas que você, deixa o like e se inscreve "
         "no Quiz Palito! Até o próximo quiz!")
FRASES = [
    "O Palito disse {x}! Se você disse {x}, perde uma vida!",
    "Palito: {x}! Pensou igual? Menos uma vida!",
    "A resposta do Palito é {x}! Se você falou {x}, perdeu uma vida!",
    "{X}! Se você também disse {x}, tchau, uma vida!",
    "O Palito escolheu {x}! Disse igual? Perde uma vida!",
    "O Palito foi de {x}! Se você foi de {x}, menos um coração!",
]


def textos():
    R = json.load(open(os.path.join(HERE, "rodadas.json"), encoding="utf-8"))
    reg = {"intro": INTRO, **{f"vidas{k}": v for k, v in VIDAS.items()}, "outro": OUTRO}
    for r in R:
        n = r["n"]
        ped = r.get("falap") or (r["pedido"].capitalize() + "!")
        reg[f"q{n}"] = f"Rodada {numero(n)}! {ped}"
        x = r["fala"]
        reg[f"p{n}"] = r.get("falar") or FRASES[n % len(FRASES)].format(x=x, X=x[0].upper() + x[1:])
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
