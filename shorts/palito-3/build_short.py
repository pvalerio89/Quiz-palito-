"""Short "Desafio do Palito #3" (palito-3), SÓ SHORT: mover 1 palito, conta 6+4=4.

Série nova (2026-11-17, análise do canal): ver shorts/palito_base.py.
Uso: py -3 build_short.py            (gera vozes que faltam e monta o Short)
     py -3 build_short.py --previa   (prancha com quadros para conferir)
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import palito_base as pb

D = pb.Desafio(
    HERE,
    conta="6+4=4",
    modo="mover",
    mostrar=['8-4=4', '0+4=4'],
    numero=3,
    tema="azul",
    titulo=('TEM 2 RESPOSTAS!', 'mova 1 palito e ache as DUAS'),
    falas={
        "q": "Essa conta tem duas respostas! Mova um palito e ache as duas!",
        "comenta": "Achou as duas? Comenta antes de ver!",
        "r1": "Primeira: o palito do mais vai pro seis! Oito menos quatro, quatro!",
        "r2": "Segunda: o meio do seis sobe! Zero mais quatro, quatro!",
        "final": "Achou as duas? Comenta!",
    },
    dica_txt=None,
    count=8.0,
)
SAIDA = os.path.join(HERE, "short-palito-3.mp4")

if __name__ == "__main__":
    D.previa() if "--previa" in sys.argv else D.montar(SAIDA)
