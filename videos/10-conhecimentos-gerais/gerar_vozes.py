"""Narração do "Conhecimentos gerais" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro, q1..q50 (pergunta + alternativas), p1..p50 (resposta), placar10/20/30/40, outro.
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez", "onze", "doze",
       "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove", "vinte"]


def numero(n):
    if n <= 20:
        return NUM[n]
    d, u = divmod(n, 10)
    dez = {2: "vinte", 3: "trinta", 4: "quarenta", 5: "cinquenta"}[d]
    return dez if u == 0 else f"{dez} e {NUM[u]}"


INTRO = ("Fala, pessoal! Bem-vindos a mais um Quiz Palito! Hoje é conhecimentos gerais: cinquenta perguntas de tudo um pouco, "
         "do nível fácil ao difícil! Cada pergunta tem quatro alternativas e você tem seis segundos pra responder. "
         "Conta quantas você acerta e chama a família pra jogar junto. Valendo!")
PLACAR = {
    10: "Dez perguntas! Quantas você já acertou? Guarda esse número e bora pra próxima!",
    20: "Vinte perguntas! Acabou o nível fácil. Agora começa o nível médio. Será que você continua acertando?",
    30: "Trinta perguntas! Já passou da metade! Continua contando os seus pontos!",
    40: "Quarenta perguntas! Agora vem o nível difícil: só os gênios acertam essas dez!",
}
OUTRO = ("E aí, quantas você acertou das cinquenta? Comenta aqui embaixo a sua nota! "
         "Se acertou mais de quarenta, você é um gênio! Marca um amigo pra ver quem sabe mais, "
         "deixa o like e se inscreve no Quiz Palito! Até o próximo quiz!")
FRASES = [
    "Resposta certa: letra {L}! {x}!",
    "É a letra {L}: {x}!",
    "Letra {L}! {x}! Acertou?",
    "A resposta é {x}! Letra {L}!",
    "Letra {L}: {x}! Valeu ponto?",
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
        reg[f"q{n}"] = f"Pergunta {numero(n)}! {r.get('falap') or r['pergunta']} {alt}"
        x = r.get("fala") or (r.get("falaop") or r["op"])[r["certa"]]
        reg[f"p{n}"] = FRASES[n % len(FRASES)].format(L=LETRA_FALA[r["certa"]], x=x)
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
