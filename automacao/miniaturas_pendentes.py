"""Lista os vídeos longos que ainda estão com a miniatura feita por código (sem a do Google Flow).

Uso: py -3 automacao/miniaturas_pendentes.py
  Olha os itens 'pronto' e os 'publicado' que ainda não entraram no ar (no_ar_em no futuro) do fila/fila.json.
  Pendente = <video>/youtube/ tem prompt-flow.txt mas NÃO tem thumbnail-codigo.jpg
  (quando a miniatura do Flow entra, a de código vira thumbnail-codigo.jpg).
  Imprime uma pasta por linha: "<pasta> <status> <no_ar_em>". Nada impresso = nada a fazer.
"""
import datetime, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import RAIZ


def main():
    doc = json.load(open(os.path.join(RAIZ, "fila", "fila.json"), encoding="utf-8"))
    agora = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for it in doc.get("itens", []):
        pasta, st, quando = it.get("video"), it.get("status"), it.get("no_ar_em") or ""
        if not pasta or st not in ("pronto", "publicado"):
            continue
        if st == "publicado" and (not quando or quando <= agora):
            continue
        yt = os.path.join(RAIZ, pasta, "youtube")
        if os.path.exists(os.path.join(yt, "prompt-flow.txt")) and not os.path.exists(os.path.join(yt, "thumbnail-codigo.jpg")):
            print(pasta, st, quando or "-")


if __name__ == "__main__":
    main()
