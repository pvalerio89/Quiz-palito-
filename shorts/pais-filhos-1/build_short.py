"""Short "Pais contra filhos" (pais-filhos-1), tirado do vídeo 38 (videos/38-pais-contra-filhos; no ar 20/11).
Regra 2026-11-22 (Patrick): todo longo tem o Short do PRÓPRIO tema. Cartão de TEXTO (conta/pergunta em letra
grande, linhas de caderno), sem foto (molde shorts/do_longo.py).
Uso: py -3 build_short.py  |  py -3 build_short.py --previa
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import do_longo as L
from do_longo import QP, b

PERG = [
    dict(titulo="QUANTO É?", destaque="MATEMÁTICA", texto=["2 + 3 × 4"], opcoes=["20", "14", "24"], certa=1,
         fala="Quanto é dois mais três vezes quatro?", resp="Quatorze!",
         cores=((240, 130, 20), (170, 60, 0))),
    dict(titulo="EM QUE ANO?", destaque="HISTÓRIA", texto=["Os portugueses", "chegam ao Brasil"],
         opcoes=["1822", "1500", "1889"], certa=1, fala="Em que ano os portugueses chegaram ao Brasil?",
         resp="Mil e quinhentos!", cores=((20, 150, 70), (5, 80, 40))),
    dict(titulo="QUAL É?", destaque="GEOGRAFIA", texto=["Maior estado", "do Brasil"], opcoes=["Pará", "Amazonas", "Mato Grosso"],
         certa=1, fala="Qual é o maior estado do Brasil?", resp="Amazonas!", cores=((240, 130, 20), (170, 60, 0))),
    dict(titulo="QUAL É O COLETIVO?", destaque="PORTUGUÊS", texto=["Coletivo de", "LOBOS"],
         opcoes=["Cardume", "Matilha", "Alcateia"], certa=2, fala="Coletivo de lobos?", resp="Alcateia!",
         cores=((20, 150, 70), (5, 80, 40))),
    dict(titulo="QUANTO É?", destaque="MATEMÁTICA", texto=["0,5 × 0,5"], opcoes=["2,5", "1", "0,25"], certa=2,
         fala="A última! Quanto dá essa?", resp="Zero vírgula vinte e cinco!",
         cores=((235, 60, 50), (120, 15, 30))),
]
CFG = dict(count=3.0, nome="pais-filhos-1", here=HERE, rotulo="PAIS x FILHOS", cor_rotulo=(200, 70, 0),
           chamada="PAIS OU FILHOS: QUEM GANHA?", gancho="Pais ou filhos, quem ganha essa?",
           final="Quem ganhou? Comenta aí!",
           final_titulo=("QUEM GANHOU:", "PAIS OU FILHOS?"), final_faixa="COMENTA QUEM GANHOU!",
           musica=os.path.join(QP, "musicas", "Carefree.mp3"), creditos=[])

if __name__ == "__main__":
    L.rodar(CFG, PERG)
