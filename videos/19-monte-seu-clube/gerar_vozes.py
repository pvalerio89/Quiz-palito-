"""Narração do "Monte o seu clube" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro (intro rapidinha), e0..e23 (etapa: o que escolher + as 6 opções), r0..r5 (reação depois da
escolha), banco (time titular pronto), outro.
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))

INTRO = "Hoje é diferente: monte o seu próprio clube!"   # intro rapidinha (2 a 3 s)
# antes da 1ª etapa: chamada de anotar nos comentários (Patrick, 2026-11-12; frases em engaja.CHAMADAS_ANOTAR)
GANCHO = ("Clica no coração e abre os comentários pra ir anotando o número de cada escolha. "
          "Assim que terminar o vídeo, é só enviar! Valendo!")
REACOES = ["Escolheu? Anota aí!", "Boa escolha! Bora pra próxima!", "Anotou o número? Próxima!",
           "Difícil, né? Vamos lá!", "Comenta qual você pegou!", "Essa foi rápida! Próxima!"]
BANCO = "Time titular pronto! Agora vamos montar o banco de reservas, com joia e lendas!"
OUTRO = ("Pronto! O seu clube está montado! Comenta aqui embaixo os números que você escolheu e o nome do seu clube! "
         "Marca um amigo pra ver quem montou o melhor time, deixa o like e se inscreve no Quiz Palito!")
FALA_NOME = {"Ødegaard": "Odegaard", "Modrić": "Modric", "Petr Čech": "Petr Tchéc", "Ibrahimović": "Ibrahimovic",
             "Kvaratskhelia": "Kvaratskhélia", "Vinícius Jr.": "Vinícius Júnior", "Eto'o": "Etô",
             "Rüdiger": "Rúdiguer", "Kimmich": "Kímich", "Musiala": "Mussiala", "Pirlo": "Pírlo"}


def nome_falado(n):
    return FALA_NOME.get(n, n.replace("Tipo ", ""))


def textos():
    E = json.load(open(os.path.join(HERE, "etapas.json"), encoding="utf-8"))
    reg = {"intro": INTRO}
    for i, e in enumerate(E):
        ns = [nome_falado(o["nome"]) for o in e["opcoes"]]
        pre = GANCHO + " " if i == 0 else ""
        reg[f"e{i}"] = f"{pre}{e['fala']} {', '.join(ns[:-1])} ou {ns[-1]}?"
    reg.update({f"r{i}": t for i, t in enumerate(REACOES)})
    reg["banco"] = BANCO
    reg["outro"] = OUTRO
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
