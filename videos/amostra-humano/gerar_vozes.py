"""Vozes da AMOSTRA "estilo mais humano" (capitais, 6 perguntas).

Só o narrador (Edge pt-BR-AntonioNeural +20%, +2Hz). O Palito NÃO fala (Patrick, 2026-11-13: não gostou).
Uso: py -3 gerar_vozes.py   (gera só o que falta; --tudo refaz)
"""
import asyncio, json, os, subprocess, sys, time
import edge_tts

if os.path.exists("/root/.ccr/ca-bundle.crt"):  # só na nuvem do Claude (proxy)
    import ssl, edge_tts.communicate as _c
    _c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

HERE = os.path.dirname(os.path.abspath(__file__))

# n_* = narrador, pal_* = Palito
FALAS = {
    "n_intro": "E aí, tudo certo? Hoje é dia de quiz de capitais!",
    "n_intro2": "Seis perguntas, e a última é bem difícil. Conta seus pontos!",

    "n_q1": "Pra aquecer, essa é de graça: qual é a capital do Brasil?",
    "n_r1": "Brasília! Quem respondeu Rio caiu: ele deixou de ser capital em mil novecentos e sessenta.",

    "n_q2": "Agora uma do Nordeste. Qual é a capital da Bahia? Ilhéus, Feira de Santana... ou Salvador?",
    "n_r2": "Salvador! E sabia que ela foi a primeira capital do Brasil?",

    "n_q3": "Bora pra Europa. Olha esse templo lá no alto... Qual é a capital da Grécia?",
    "n_d3": "Dica: o nome lembra uma deusa grega!",
    "n_r3": "Atenas! Esparta era a cidade dos guerreiros, mas a capital é Atenas.",

    "n_q4": "Cuidado, que essa tem pegadinha! Qual é a capital dos Estados Unidos?",
    "n_s4": "A resposta é...",
    "n_r4": "Washington! Caiu na pegadinha, hein? Muita gente chuta Nova York.",

    "n_q5": "Essa aqui derruba muita gente. Capital da Austrália: Sydney, Melbourne ou Camberra?",
    "n_r5": "Camberra! Quase todo mundo chuta Sydney. Se você acertou, comenta: eu sabia!",

    "n_desafio": "Atenção... essa é a última pergunta! E é a mais difícil!",
    "n_q6": "Qual é a capital de Rondônia? Ji-Paraná, Ariquemes ou Porto Velho?",
    "n_s6": "Valendo o título de mestre... a resposta é...",
    "n_r6": "Porto Velho! Se acertou essa, você é fera mesmo!",

    "n_fim": "Gostou do quiz? Então se inscreve no canal!",
}


def gerar(chave, texto, destino):
    if chave.startswith("pal_"):
        tmp = destino + ".raw.mp3"
        asyncio.run(edge_tts.Communicate(texto, "pt-BR-AntonioNeural", rate="+25%", pitch="+35Hz").save(tmp))
        # voz de desenho: mais aguda, sem ficar rápida demais
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-af",
                        "asetrate=24000*1.22,aresample=24000,atempo=0.92", destino], check=True)
        os.remove(tmp)
    else:
        asyncio.run(edge_tts.Communicate(texto, "pt-BR-AntonioNeural", rate="+20%", pitch="+2Hz").save(destino))


def main():
    tudo = "--tudo" in sys.argv
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    json.dump(FALAS, open(os.path.join(HERE, "textos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for i, (k, t) in enumerate(FALAS.items(), 1):
        dst = os.path.join(HERE, "assets", f"{k}.mp3")
        if not tudo and os.path.exists(dst):
            continue
        for _ in range(4):
            try:
                gerar(k, t, dst)
                break
            except Exception as e:
                print("erro", k, e, flush=True)
                time.sleep(3)
        print(f"{i}/{len(FALAS)} {k}", flush=True)


if __name__ == "__main__":
    main()
