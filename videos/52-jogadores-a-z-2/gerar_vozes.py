"""Narração do vídeo 52 "Jogadores de A a Z — parte 2" — Edge pt-BR-AntonioNeural +20%, pitch +2Hz.

Cria em assets/: intro, q1..qN (pergunta falada com as alternativas), p1..pN (resposta com reação), d<n> (dica),
s<n> (suspense), curtir/espero, placar10.., ultima, outro. O Palito não fala (Patrick, 2026-11-13).
Nomes estrangeiros vão escritos do jeito que se fala (PRONUNCIA) só no áudio; a tela mostra o nome certo.
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, re, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))

INTRO = "Atenção, boleiro! Chegou a parte dois dos craques!"      # intro rapidinha, saudação variada
Q1 = "Um jogador pra cada letra, com uma pista em cada. Trinta e duas letras, e a última ninguém acerta! "
CURTIR = "Ei, rapidinho... se inscreva no canal e deixe seu like!"
ESPERO = "Vai lá, eu espero!"
PLACAR = {
    10: "Dez craques! Quantos você acertou até agora?",
    20: "Vinte! Agora vêm as lendas e as letras difíceis!",
    30: "Trinta! Só faltam duas, e são as mais difíceis!",
}
ULTIMA = "Atenção... última pergunta! A letra Y, que quase ninguém acerta!"
OUTRO = "Quantas você acertou? Se inscreve no canal!"
PRONUNCIA = {"Ødegaard": "Ódegaard", "Petr Čech": "Pêtr Tchéc", "Kvaratskhelia": "Kvaratsquélia", "Xhaka": "Djáca",
             "Yashin": "Iáchin", "Wirtz": "Virtz", "Kimmich": "Kímix", "Gvardiol": "Gvárdiol", "Götze": "Gôtze",
             "Neuer": "Nóier", "Hummels": "Rúmels", "Hazard": "Azár", "De Bruyne": "De Bráine", "Isak": "Íssak",
             "Lineker": "Láineker", "Lingard": "Língard", "Frimpong": "Frímpong", "Yorke": "Iórk", "Yakin": "Iákin",
             "Khedira": "Quedíra", "Kolarov": "Kólarov", "Pickford": "Píkford", "Olise": "Olíse",
             "Alexander-Arnold": "Alexander Arnold", "Vini Jr.": "Vini Júnior", "Bierhoff": "Bírrof",
             "Beckenbauer": "Békenbauer", "Joelinton": "Djoelínton", "Cocu": "Cócu"}


def falar(t):
    for k in sorted(PRONUNCIA, key=len, reverse=True):
        t = re.sub(re.escape(k), PRONUNCIA[k], t, flags=re.I)
    return t


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
    return {k: falar(v) for k, v in reg.items()}


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
