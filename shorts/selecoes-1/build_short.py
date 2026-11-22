"""Short "Seleções de A a Z" (selecoes-1), tirado do vídeo 39 (videos/39-selecoes-a-z; no ar 21/11).
Regra 2026-11-22 (Patrick): todo longo tem o Short do PRÓPRIO tema. Letra + pista em texto, opções com bandeira,
3 s por pergunta (molde shorts/do_longo.py).
Uso: py -3 build_short.py  |  py -3 build_short.py --previa
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import do_longo as L
from do_longo import QP, b

LONGO = os.path.join(QP, "videos", "39-selecoes-a-z")
BD = lambda *c: [os.path.join(LONGO, "bandeiras", x + ".png") if x else None for x in c]
T = "SELEÇÃO COM A LETRA"
PERG = [
    dict(titulo=T, destaque="J", texto=["Os SAMURAIS", "AZUIS"], opcoes=["JAMAICA", "JAPÃO", "JORDÂNIA"],
         bandeiras=BD("jm", "jp", "jo"), certa=1, fala="Letra J: os Samurais Azuis!", resp="Japão!",
         cores=((30, 110, 210), (15, 40, 130))),
    dict(titulo=T, destaque="H", texto=["A LARANJA", "MECÂNICA"], opcoes=["HUNGRIA", "HAITI", "HOLANDA"],
         bandeiras=BD("hu", "ht", "nl"), certa=2, fala="Letra H: a Laranja Mecânica!", resp="Holanda!",
         cores=((240, 130, 20), (170, 60, 0))),
    dict(titulo=T, destaque="G", texto=["As ESTRELAS", "NEGRAS"], opcoes=["GRÉCIA", "GANA", "GEÓRGIA"],
         bandeiras=BD("gr", "gh", "ge"), certa=1, fala="Letra G: as Estrelas Negras!", resp="Gana!",
         cores=((30, 110, 210), (15, 40, 130))),
    dict(titulo=T, destaque="V", texto=["A única da América", "do Sul que NUNCA", "foi à Copa"],
         opcoes=["VIETNÃ", "VANUATU", "VENEZUELA"], bandeiras=BD("vn", "vu", "ve"), certa=2,
         fala="Letra V: nunca foi à Copa!", resp="Venezuela!",
         cores=((240, 130, 20), (170, 60, 0))),
    dict(titulo=T, destaque="X", texto=["Que seleção", "começa com X?"], opcoes=["NENHUMA!", "XANGAI", "XINGU"],
         certa=0, fala="E a última: que seleção começa com X?", resp="Nenhuma! Era pegadinha!",
         cores=((235, 60, 50), (120, 15, 30))),
]
CFG = dict(count=3.0, nome="selecoes-1", here=HERE, rotulo="SELEÇÕES DE A a Z", cor_rotulo=(20, 60, 170),
           chamada="3 SEGUNDOS PRA CADA!", gancho="Três segundos pra cada!",
           final="O completo tá no canal!",
           musica=os.path.join(QP, "musicas", "Wallpaper.mp3"), creditos=[])

if __name__ == "__main__":
    L.rodar(CFG, PERG)
