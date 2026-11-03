"""Narração do "Qual você prefere: doce ou salgado?" — Edge pt-BR-AntonioNeural +20%.

Cria em assets/: intro, fase1..4, qN (pergunta), pN (escolha do Palito), outro. Textos em textos.json.
Uso: py -3 gerar_vozes.py            (gera só o que falta)
     py -3 gerar_vozes.py --tudo     (refaz tudo)
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


INTRO = ("Fala, pessoal! Bem-vindos a mais um Quiz Palito! Hoje é a batalha mais difícil do mundo: doce ou salgado! "
         "São quarenta escolhas, em quatro fases, e cada vez fica mais difícil escolher. "
         "E o Palito também vai escolher! Conta quantas vezes você concordou com ele. Valendo!")
FASES = {
    1: "Fase um: aquecimento!",
    2: "Fase dois: agora ficou difícil!",
    3: "Fase três: muito difícil! Pensa bem!",
    4: "Fase final: as escolhas impossíveis! Só os campeões aqui!",
}
OUTRO = ("E aí, você é do time doce ou do time salgado? E quantas vezes você concordou com o Palito? "
         "Conta aqui nos comentários! Deixa o like, se inscreve no Quiz Palito, e até o próximo quiz!")
EXTRA = {  # pedido de interação depois da escolha do Palito
    8: "Se você escolheu brownie, deixa o like! Se foi lasanha, comenta aí!",
    28: "Time paçoca deixa o like! Time amendoim comenta aí embaixo!",
}
ESCOLHA = ["O Palito vai de {x}!", "O Palito escolheu {x}!", "Pro Palito, {x}!", "O Palito fica com {x}!"]


def textos():
    esc = json.load(open(os.path.join(HERE, "escolhas.json"), encoding="utf-8"))
    reg = {"intro": INTRO, **{f"fase{k}": v for k, v in FASES.items()}, "outro": OUTRO}
    for e in esc:
        n = e["n"]
        a, b = e["doce"].lower(), e["salgado"].lower()
        reg[f"q{n}"] = f"Número {numero(n)}! {a} ou {b}?"
        x = (e["doce"], e["salgado"])[e["palito"]].lower()
        reg[f"p{n}"] = ESCOLHA[n % len(ESCOLHA)].format(x=x) + (" " + EXTRA[n] if n in EXTRA else "")
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
