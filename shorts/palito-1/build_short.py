"""Short "Desafio do Palito #1" (palito-1), SÓ SHORT: mova 1 palito e deixe a conta 5 + 7 = 2 certa.

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
    conta="5+7=2",
    modo="mover",
    mostrar=["9-7=2"],
    numero=1,
    tema="madeira",
    titulo=("MOVA 1 PALITO", "e deixe a conta CERTA!"),
    falas={
        "q": "Mova só um palito pra essa conta ficar certa! Valendo!",
        "dica": "Dica: o sinal também é palito!",
        "comenta": "Comenta tua resposta antes de ver!",
        "r1": "Tira o palito do mais e põe no cinco! Nove menos sete, dois!",
        "final": "Acertou? Comenta eu!",
    },
    dica_txt="O SINAL TAMBÉM CONTA!",
    count=8.0,
)
SAIDA = os.path.join(HERE, "short-palito-1.mp4")

if __name__ == "__main__":
    D.previa() if "--previa" in sys.argv else D.montar(SAIDA)
