"""Short "Brasil x Portugal" (portugal-1), tirado do vídeo 36 (videos/36-brasil-x-portugal; no ar 18/11).
Regra 2026-11-22 (Patrick): todo longo tem o Short do PRÓPRIO tema. Cartão com foto (molde shorts/do_longo.py).
Uso: py -3 build_short.py  |  py -3 build_short.py --previa
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import do_longo as L
from do_longo import QP, b

LONGO = os.path.join(QP, "videos", "36-brasil-x-portugal")
F = lambda n: os.path.join(LONGO, "fotos", n)
T = "COMO SE DIZ EM PORTUGAL?"
PERG = [
    dict(titulo=T, destaque="ÔNIBUS", foto=F("onibus.jpg"), opcoes=["COMBOIO", "ELÉTRICO", "AUTOCARRO"], certa=2,
         fala="Ônibus, em Portugal, é?", resp="Autocarro!", cores=((20, 150, 70), (5, 80, 40))),
    dict(titulo=T, destaque="MOUSE", foto=F("mouse.jpg"), opcoes=["CURSOR", "TECLA", "RATO"], certa=2,
         fala="E o mouse do computador?", resp="Rato!", cores=((235, 60, 50), (120, 15, 30))),
    dict(titulo=T, destaque="FILA", foto=F("fila.jpg"), opcoes=["CAUDA", "BICHA", "RENQUE"], certa=1,
         fala="E a fila do banco?", resp="Bicha!", cores=((20, 150, 70), (5, 80, 40))),
    dict(titulo=T, destaque="CHICLETE", foto=F("chiclete.jpg"), opcoes=["REBUÇADO", "GOMA DOCE", "PASTILHA ELÁSTICA"],
         certa=2, fala="E chiclete?", resp="Pastilha elástica!", cores=((235, 60, 50), (120, 15, 30))),
    dict(titulo=T, destaque="CURATIVO", foto=F("curativo.jpg"), opcoes=["LIGADURA", "ADESIVO", "PENSO RÁPIDO"], certa=2,
         fala="A última é difícil! Curativo?", resp="Penso rápido!", cores=((20, 150, 70), (5, 80, 40))),
]
CFG = dict(count=3.0, nome="portugal-1", here=HERE, rotulo="BRASIL x PORTUGAL", cor_rotulo=(0, 110, 50),
           chamada="APOSTO QUE VOCÊ ERRA UMA!", gancho="Aposto que você erra uma!",
           final="Comenta sua nota! O completo tá no canal!",
           musica=os.path.join(QP, "musicas", "Fluffing a Duck.mp3"),
           creditos=L.creditos(LONGO, [os.path.basename(p["foto"]) for p in PERG]))

if __name__ == "__main__":
    L.rodar(CFG, PERG)
