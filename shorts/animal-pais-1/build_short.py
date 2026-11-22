"""Short "Animal símbolo de cada país" (animal-pais-1), tirado do vídeo 40 (videos/40-animal-de-cada-pais; no ar 22/11).
Regra 2026-11-22 (Patrick): todo longo tem o Short do PRÓPRIO tema. Pergunta com a BANDEIRA, resposta troca
para a FOTO do animal (molde shorts/do_longo.py).
Uso: py -3 build_short.py  |  py -3 build_short.py --previa
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import do_longo as L
from do_longo import QP, b

LONGO = os.path.join(QP, "videos", "40-animal-de-cada-pais")
F = lambda n: os.path.join(LONGO, "fotos", n)
T = "QUAL É O ANIMAL SÍMBOLO?"
PERG = [
    dict(titulo=T, destaque="CHINA", foto=F("bandeira-cn.jpg"), foto_resp=F("panda-gigante.jpg"), contem=True,
         opcoes=["TIGRE", "MACACO", "PANDA"], certa=2, fala="Qual é o animal símbolo da China?", resp="Panda!",
         cores=((0, 160, 170), (0, 70, 100))),
    dict(titulo=T, destaque="FRANÇA", foto=F("bandeira-fr.jpg"), foto_resp=F("galo.jpg"), contem=True,
         opcoes=["LEÃO", "CAVALO", "GALO"], certa=2, fala="E o da França?", resp="O galo!",
         cores=((30, 110, 210), (15, 40, 130))),
    dict(titulo=T, destaque="INDONÉSIA", foto=F("bandeira-id.jpg"), foto_resp=F("dragao-de-komodo.jpg"), contem=True,
         opcoes=["DRAGÃO-DE-KOMODO", "ORANGOTANGO", "TIGRE"], certa=0, fala="E o da Indonésia?",
         resp="Dragão-de-Komodo!", cores=((0, 160, 170), (0, 70, 100))),
    dict(titulo=T, destaque="PAPUA-NOVA GUINÉ", foto=F("bandeira-pg.jpg"), foto_resp=F("ave-do-paraiso.jpg"), contem=True,
         opcoes=["PAPAGAIO", "AVE-DO-PARAÍSO", "TUCANO"], certa=1, fala="Essa é difícil! Papua-Nova Guiné?",
         resp="Ave-do-paraíso!", cores=((30, 110, 210), (15, 40, 130))),
    dict(titulo=T, destaque="ESCÓCIA", foto=F("bandeira-gb-sct.jpg"), foto_resp=F("unicornio.jpg"), contem=True,
         opcoes=["CAVALO", "OVELHA", "UNICÓRNIO"], certa=2, fala="A última é estranha: e o da Escócia?",
         resp="Unicórnio! Sério!", cores=((235, 60, 50), (120, 15, 30))),
]
CFG = dict(count=3.0, nome="animal-pais-1", here=HERE, rotulo="ANIMAL DE CADA PAÍS", cor_rotulo=(0, 110, 120),
           chamada="MARCA QUEM ERRARIA ESSA!", gancho="Marca aquele amigo que erraria essa!",
           final="Comenta sua nota! O completo tá no canal!",
           musica=os.path.join(QP, "musicas", "Carefree.mp3"),
           creditos=L.creditos(LONGO, [os.path.basename(p["foto_resp"]) for p in PERG]))

if __name__ == "__main__":
    L.rodar(CFG, PERG)
