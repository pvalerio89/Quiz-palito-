"""Short "Desafio do Palito #5" (palito-5), SÓ SHORT: mover 1 palito, conta 2+3=7.

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
    conta="2+3=7",
    modo="mover",
    mostrar=['2+5=7'],
    numero=5,
    tema="madeira",
    titulo=('MOVA 1 PALITO', '2 + 3 = 7 está ERRADO!'),
    falas={
        "q": "Dois mais três, sete? Tá errado! Mova um palito e conserta!",
        "dica": "Dica: o resultado tá certo!",
        "comenta": "Comenta tua resposta antes de ver!",
        "r1": "O palito do três muda de lado e vira cinco! Dois mais cinco, sete!",
        "final": "Comenta como você resolveu! A resposta tá nos comentários!",
    },
    dica_txt='O 7 ESTÁ CERTO!',
    count=8.0,
)
SAIDA = os.path.join(HERE, "short-palito-5.mp4")

if __name__ == "__main__":
    D.previa() if "--previa" in sys.argv else D.montar(SAIDA)
