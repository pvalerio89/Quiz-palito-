"""Gera toda a narração do Quiz Palito com a voz oficial: Gemini TTS, voz "Fenrir".

Cria assets/intro.mp3, assets/qN.mp3, assets/aN.mp3 e assets/outro.mp3.
A chave do Gemini fica em C:\\Users\\pvale\\.config\\watch\\.env (GEMINI_API_KEY=...).
Uso: py -3 gerar_vozes.py            (gera só o que falta)
     py -3 gerar_vozes.py --tudo     (refaz tudo)
"""
import json, os, subprocess, sys, tempfile, time
from gemini_voz import falar

HERE = os.path.dirname(os.path.abspath(__file__))
VOZ = "Fenrir"
ESTILO = "narrador brasileiro de quiz do YouTube, empolgado, sorridente, falando rápido e com energia"

INTRO = ("Fala, pessoal! Bem-vindos a mais um Quiz Palito! Hoje o desafio é adivinhar o nome de 40 países. "
         "Só que tem um detalhe: todas as vogais sumiram! Será que você consegue? "
         "Antes de começar, deixa o seu like, se inscreve no canal e ativa o sininho. Valendo!")
OUTRO = ("E aí, quantos países você acertou? Conta aqui nos comentários! "
         "Se curtiu, deixa o like, se inscreve no Quiz Palito e confere os outros quizzes. Até o próximo!")


def gerar(texto, destino):
    wav = os.path.join(tempfile.gettempdir(), "quiz_fala.wav")
    falar(texto, wav, voz=VOZ, estilo=ESTILO)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-b:a", "192k", destino], check=True)


def main():
    tudo = "--tudo" in sys.argv
    A = lambda nome: os.path.join(HERE, "assets", nome)
    qs = json.load(open(os.path.join(HERE, "perguntas.json"), encoding="utf-8"))
    tarefas = [(INTRO, A("intro.mp3"))]
    for q in qs:
        tarefas.append((q["q"], A(f"q{q['n']}.mp3")))
        tarefas.append((q["a"], A(f"a{q['n']}.mp3")))
    tarefas.append((OUTRO, A("outro.mp3")))
    for i, (texto, destino) in enumerate(tarefas, 1):
        if not tudo and os.path.exists(destino):
            continue
        gerar(texto, destino)
        print(f"{i}/{len(tarefas)} {os.path.basename(destino)}", flush=True)
        time.sleep(4)  # evita o limite de pedidos do plano grátis


if __name__ == "__main__":
    main()
