"""Narração do quiz "Jogadores de A a Z" com a voz oficial do Quiz Palito (Gemini, Fenrir).

Cria assets/intro.mp3, assets/qN.mp3, assets/aN.mp3 e assets/outro.mp3 e grava os textos em textos.json.
Uso: py -3 gerar_vozes.py            (gera só o que falta)
     py -3 gerar_vozes.py --tudo     (refaz tudo)
"""
import json, os, subprocess, sys, tempfile, time
from gemini_voz import falar

HERE = os.path.dirname(os.path.abspath(__file__))
VOZ = "Fenrir"
ESTILO = "narrador brasileiro de quiz de futebol no YouTube, empolgado, sorridente, falando rápido e com energia"

INTRO = ("Fala, pessoal! Bem-vindos a mais um Quiz Palito! Hoje o desafio é de futebol: "
         "você consegue lembrar um jogador para cada letra, de A até Z? "
         "Vale craque de hoje e lenda das antigas! Antes de começar, deixa o seu like, "
         "se inscreve no canal e ativa o sininho. Valendo!")
OUTRO = ("E aí, chegou até o Z? Conta aqui nos comentários quantas letras você completou! "
         "Se curtiu, deixa o like, se inscreve no Quiz Palito e confere os outros quizzes. Até o próximo!")

NUM = ["", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez", "onze", "doze",
       "treze", "catorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove", "vinte", "vinte e um",
       "vinte e dois", "vinte e três", "vinte e quatro", "vinte e cinco", "vinte e seis"]
LETRA = {"A": "A", "B": "bê", "C": "cê", "D": "dê", "E": "é", "F": "éfe", "G": "gê", "H": "agá", "I": "i",
         "J": "jota", "K": "cá", "L": "éle", "M": "ême", "N": "êne", "O": "ó", "P": "pê", "Q": "quê",
         "R": "érre", "S": "ésse", "T": "tê", "U": "u", "V": "vê", "W": "dáblio", "X": "xis", "Y": "ípsilon",
         "Z": "zê"}
PERGUNTA = ["Um jogador que começa com a letra {l}!", "Fala aí um jogador com a letra {l}!",
            "E com a letra {l}, quem você lembra?", "Agora a letra {l}!"]
RESPOSTA = ["Algumas respostas: {a}, {b} e {c}!", "Valeu {a}, {b} ou {c}!", "Pode ser {a}, {b} ou {c}!",
            "Acertou quem falou {a}, {b} ou {c}!"]
FALADO = {"VINI JR.": "Vini Júnior", "ETO'O": "Etoo"}


def falado(nome):
    return FALADO.get(nome, nome.title())


def textos(q):
    i = q["n"]
    l = LETRA[q["letra"]]
    if q["letra"] in ("K", "W", "X", "Y", "Q"):
        pq = f"Número {NUM[i]}. Essa é difícil! Letra {l}!"
    else:
        pq = f"Número {NUM[i]}. " + PERGUNTA[i % len(PERGUNTA)].format(l=l)
    a, b, c = (falado(n) for n in q["nomes"])
    ra = RESPOSTA[i % len(RESPOSTA)].format(a=a, b=b, c=c)
    if q.get("extra"):
        ra += " " + q["extra"]
    return pq, ra


MOTOR = "edge"  # "edge" (Antonio, grátis e sem limite) ou "gemini" (Fenrir, 10 falas/dia no plano grátis)


def gerar(texto, destino):
    if MOTOR == "edge":
        import asyncio, edge_tts
        asyncio.run(edge_tts.Communicate(texto, "pt-BR-AntonioNeural", rate="+20%", pitch="+2Hz").save(destino))
        return
    wav = os.path.join(tempfile.gettempdir(), "quiz_fala.wav")
    falar(texto, wav, voz=VOZ, estilo=ESTILO)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-b:a", "192k", destino], check=True)


def main():
    tudo = "--tudo" in sys.argv
    A = lambda nome: os.path.join(HERE, "assets", nome)
    qs = json.load(open(os.path.join(HERE, "perguntas.json"), encoding="utf-8"))
    tarefas = [(INTRO, A("intro.mp3"))]
    registro = {"intro": INTRO, "outro": OUTRO}
    for q in qs:
        pq, ra = textos(q)
        registro[f"q{q['n']}"], registro[f"a{q['n']}"] = pq, ra
        tarefas += [(pq, A(f"q{q['n']}.mp3")), (ra, A(f"a{q['n']}.mp3"))]
    tarefas.append((OUTRO, A("outro.mp3")))
    json.dump(registro, open(os.path.join(HERE, "textos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "--so-textos" in sys.argv:
        return
    for i, (texto, destino) in enumerate(tarefas, 1):
        if not tudo and os.path.exists(destino):
            continue
        gerar(texto, destino)
        print(f"{i}/{len(tarefas)} {os.path.basename(destino)}", flush=True)
        time.sleep(0.3 if MOTOR == "edge" else 4)


if __name__ == "__main__":
    main()
