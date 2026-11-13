"""AMOSTRA "estilo mais humano" (Patrick, 2026-11-13: "esse formato está muito robótico").

Mesmo layout aprovado (`modelo-opcoes/opcoes.py`), 6 perguntas de capitais (fotos do vídeo 22), com:
  - frases variadas (sem "Pergunta cinco!" toda vez) e reação de verdade a cada resposta;
  - ritmo variado: a 1ª bem rápida, DICA no meio da contagem, SUSPENSE ("a resposta é...") antes de revelar;
  - "VOCÊ SABIA?" em algumas respostas (1 frase);
  - pedido de curtida com pausa e "Eu espero!";
  - tela ÚLTIMA PERGUNTA com batida de coração; fim só com INSCREVA-SE;
  - zoom de impacto na revelação. O Palito não fala (Patrick não gostou).
Tudo isso vive em `modelo-opcoes/humano.py` (esta amostra só monta as perguntas com ele).
Uso: py -3 gerar_vozes.py && py -3 build_amostra.py
"""
import os, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VIDEOS, "modelo-opcoes"))
import opcoes as op
import humano as hu
from opcoes import b, nd

op.FOTOS = os.path.join(VIDEOS, "22-capitais", "fotos")
A = lambda n: os.path.join(HERE, "assets", n + ".mp3")
SAIDA = os.path.join(HERE, "amostra-estilo-humano.mp4")
MUSICA = os.path.join(os.path.dirname(VIDEOS), "musicas", "Sneaky Snitch.mp3")
dur = lambda k: b.duration(A(k))
TOTAL = 6

# Cada pergunta: contagem, dica, aviso, suspense e "você sabia?" (ver humano.py).
Q = [
    dict(n=1, pergunta="CAPITAL DO BRASIL?", foto="brasilia.jpg", opcoes=["Brasília", "Rio de Janeiro", "São Paulo"],
         certa=0, count=4.0, sabia="O Rio foi capital até 1960, quando Brasília foi inaugurada."),
    dict(n=2, pergunta="CAPITAL DA BAHIA?", foto="salvador.jpg", opcoes=["Ilhéus", "Feira de Santana", "Salvador"],
         certa=2, count=6.0,
         sabia="Salvador foi a primeira capital do Brasil, de 1549 a 1763."),
    dict(n=3, pergunta="CAPITAL DA GRÉCIA?", foto="atenas.jpg", opcoes=["Esparta", "Atenas", "Olímpia"],
         certa=1, count=7.0, dica=(A("n_d3"), "O NOME LEMBRA UMA DEUSA GREGA", 2.5)),
    dict(n=4, pergunta="CAPITAL DOS EUA?", foto="washington.jpg", opcoes=["Nova York", "Washington", "Los Angeles"],
         certa=1, count=7.0,
         suspense=A("n_s4"), aviso="TEM PEGADINHA!"),
    dict(n=5, pergunta="CAPITAL DA AUSTRÁLIA?", foto="camberra.jpg", opcoes=["Sydney", "Melbourne", "Camberra"],
         certa=2, count=7.0, aviso="DERRUBA MUITA GENTE!"),
    dict(n=6, pergunta="CAPITAL DE RONDÔNIA?", foto="porto-velho.jpg", opcoes=["Ji-Paraná", "Ariquemes", "Porto Velho"],
         certa=2, count=9.0, suspense=A("n_s6"), final=True),
]


def intro_frames(d):
    return op.intro_rapida("QUIZ DE CAPITAIS", "VOCÊ CONSEGUE?", d,
                           fotos=["paris.jpg", "roma.jpg", "londres.jpg", "toquio.jpg", "lisboa.jpg"])


def main():
    tmp = tempfile.mkdtemp(prefix="amostra_")
    sfx = hu.make_sfx(tmp)
    video = os.path.join(tmp, "video.mp4")
    tl = b.Timeline(video)
    t2 = dur("n_intro") + 0.25
    di = t2 + dur("n_intro2") + 0.3
    tl.sound(A("n_intro"), at=0.15)
    tl.sound(A("n_intro2"), at=t2)
    ultimo = None
    for f in intro_frames(di):
        tl.frame(f)
        ultimo = f
    for q in Q:
        n = q["n"]
        if q.get("final"):
            for f in hu.ultima(tl, sfx, A("n_desafio")):
                tl.frame(f)
                ultimo = f
        for f in hu.pergunta(tl, sfx, q, TOTAL, ultimo, A(f"n_q{n}"), A(f"n_r{n}"), count=q["count"]):
            tl.frame(f)
            ultimo = f
        if n == 2:   # pedido de curtida depois da 2ª resposta
            for f in hu.curtir(tl, sfx, A("n_curtir"), A("n_espero")):
                tl.frame(f)
                ultimo = f
    for f in hu.inscreva(tl, sfx, A("n_fim")):
        tl.frame(f)
    total = tl.t
    tl.close()
    nd.HERE, nd.SAIDA = HERE, SAIDA
    nd.A = lambda x: MUSICA if x == "musica.mp3" else os.path.join(HERE, "assets", x)
    nd.mixar(tl, video, total)
    print(f"OK {SAIDA} ({total:.1f}s)")


if __name__ == "__main__":
    main()
