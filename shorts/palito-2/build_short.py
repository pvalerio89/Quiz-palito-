"""Short "Desafio do Palito #2" (palito-2), SÓ SHORT: mover 1 palito, conta 7+1=0.

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
    conta="7+1=0",
    modo="mover",
    mostrar=['7-7=0'],
    numero=2,
    tema="lousa",
    titulo=('MOVA 1 PALITO', 'e deixe a conta CERTA!'),
    falas={
        "q": "Sete mais um, igual a zero? Mova só um palito e conserta essa conta!",
        "dica": "Dica: olha o número um!",
        "comenta": "Já sabe? Comenta antes de ver!",
        "r1": "Tira o palito do mais e faz um sete! Sete menos sete, zero!",
        "final": "E aí, achou? Comenta! A resposta tá nos comentários!",
    },
    dica_txt='OLHE O NÚMERO 1!',
    count=8.0,
)
SAIDA = os.path.join(HERE, "short-palito-2.mp4")

if __name__ == "__main__":
    D.previa() if "--previa" in sys.argv else D.montar(SAIDA)
