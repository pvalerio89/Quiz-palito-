"""Short "Desafio do Palito #4" (palito-4), SÓ SHORT: tirar 1 palito, conta 8-7=2.

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
    conta="8-7=2",
    modo="tirar",
    mostrar=['9-7=2'],
    numero=4,
    tema="roxo",
    titulo=('TIRE 1 PALITO', 'e deixe a conta CERTA!'),
    falas={
        "q": "Agora é diferente: tire só um palito pra conta ficar certa!",
        "dica": "Dica: olha o oito!",
        "comenta": "Comenta qual palito você tira!",
        "r1": "Tira o palito de baixo do oito! Vira nove! Nove menos sete, dois!",
        "final": "Acertou? Comenta eu!",
    },
    dica_txt='OLHE O OITO!',
    count=8.0,
)
SAIDA = os.path.join(HERE, "short-palito-4.mp4")

if __name__ == "__main__":
    D.previa() if "--previa" in sys.argv else D.montar(SAIDA)
