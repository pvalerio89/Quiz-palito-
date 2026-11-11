"""Gera itens.json (uma pergunta por posição) e as imagens do cabeçalho em fotos/. Uso: py -3 itens.py"""
import json, os, random
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(HERE))
from dados import TIMES

rnd = random.Random(18)
R = []
n = 0
pos = [0, 1, 2] * 30
rnd.shuffle(pos)
os.makedirs(os.path.join(HERE, "fotos"), exist_ok=True)
for ti, tm in enumerate(TIMES):
    tipo, k = tm["img"].split(":")
    src = (os.path.join(RAIZ, "videos", "03-bandeiras-195", "bandeiras", k + ".png") if tipo == "band"
           else os.path.join(RAIZ, "videos", "16-alfabeto-times", "escudos", k + ".png"))
    im = Image.open(src).convert("RGBA")
    im = im.crop(im.getbbox())
    im.thumbnail((200, 200), Image.LANCZOS)
    im.save(os.path.join(HERE, "fotos", f"{tipo}-{k}.png"))
    for si, (perg, certa, rot, err, x, y) in enumerate(tm["jog"]):
        n += 1
        ops = list(err)
        p = pos[n - 1]
        ops.insert(p, certa)
        assert len(set(ops)) == 3, (tm["sub"], certa)
        R.append({"n": n, "time": ti, "slot": si, "pergunta": perg, "opcoes": ops, "certa": p, "nome": certa})
json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(R), "perguntas")
