"""Short "De qual país é esse jogador?" (jogador-pais-1), tirado do vídeo 37 (videos/37-jogador-qual-pais; no ar 19/11).
Regra 2026-11-22 (Patrick): todo longo tem o Short do PRÓPRIO tema. Foto do jogador, opções com bandeira e o
nome revelado na resposta (molde shorts/do_longo.py).
Uso: py -3 build_short.py  |  py -3 build_short.py --previa
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import do_longo as L
from do_longo import QP, b

LONGO = os.path.join(QP, "videos", "37-jogador-qual-pais")
F = lambda n: os.path.join(LONGO, "fotos", n)
BD = lambda *c: [os.path.join(LONGO, "bandeiras", x + ".png") for x in c]
T = "DE QUAL PAÍS É ELE?"
PERG = [
    dict(titulo=T, foto=F("ca-mbappe.jpg"), opcoes=["BÉLGICA", "CAMARÕES", "FRANÇA"], bandeiras=BD("be", "cm", "fr"),
         certa=2, revela="MBAPPÉ", fala="De qual país é esse craque?", resp="França, Mbappé!",
         cores=((30, 90, 200), (10, 35, 120)), j="Mbappé"),
    dict(titulo=T, foto=F("ca-haaland.jpg"), opcoes=["SUÉCIA", "DINAMARCA", "NORUEGA"], bandeiras=BD("se", "dk", "no"),
         certa=2, revela="HAALAND", fala="E esse artilheiro?", resp="Noruega, Haaland!",
         cores=((150, 70, 200), (60, 25, 120)), j="Haaland"),
    dict(titulo=T, foto=F("mei-modric.jpg"), opcoes=["CROÁCIA", "SÉRVIA", "ESLOVÊNIA"], bandeiras=BD("hr", "rs", "si"),
         certa=0, revela="MODRIĆ", fala="Esse aqui é meia, hein!", resp="Croácia, Modritch!",
         cores=((30, 90, 200), (10, 35, 120)), j="Modrić"),
    dict(titulo=T, foto=F("ld-hakimi.jpg"), opcoes=["ESPANHA", "FRANÇA", "MARROCOS"], bandeiras=BD("es", "fr", "ma"),
         certa=2, revela="HAKIMI", fala="Cuidado com essa!", resp="Marrocos! Nasceu na Espanha!",
         cores=((150, 70, 200), (60, 25, 120)), j="Hakimi"),
    dict(titulo=T, foto=F("lca-ibrahimovic.jpg"), opcoes=["BÓSNIA", "SUÉCIA", "CROÁCIA"], bandeiras=BD("ba", "se", "hr"),
         certa=1, revela="IBRAHIMOVIĆ", fala="A última! E esse gigante?", resp="Suécia, Ibrahimovic!",
         cores=((235, 60, 50), (120, 15, 30)), j="Ibrahimović"),
]
CFG = dict(count=3.0, nome="jogador-pais-1", here=HERE, rotulo="JOGADOR x PAÍS", cor_rotulo=(20, 60, 170),
           chamada="VOCÊ CHEGA NO 5 DE 5?", gancho="Será que você chega no cinco de cinco?",
           final="Tem trinta e seis no canal!",
           musica=os.path.join(QP, "musicas", "Sneaky Snitch.mp3"),
           creditos=L.creditos(LONGO, [p["j"] for p in PERG]))

if __name__ == "__main__":
    L.rodar(CFG, PERG)
