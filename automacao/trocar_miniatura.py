"""Troca a miniatura de vídeos que JÁ estão no YouTube (agendados ou públicos).

Uso: py -3 automacao/trocar_miniatura.py <pasta> [<pasta> ...]
  Envia <pasta>/youtube/thumbnail.jpg para o vídeo gravado no publicados.json (chave youtube.id).
  Uso típico: miniatura feita no Google Flow depois do vídeo já ter subido.
Precisa dos Secrets YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN.
"""
import os, sys, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import RAIZ, ler_registro, pasta_rel, status
from publicar_youtube import API_UP, token


def main():
    pastas = [pasta_rel(p) for p in sys.argv[1:]]
    if not pastas:
        sys.exit(__doc__)
    doc, tk, erros = ler_registro(), token(), 0
    for pasta in pastas:
        vid = status(doc, pasta, "youtube").get("id")
        thumb = os.path.join(RAIZ, pasta, "youtube", "thumbnail.jpg")
        if not vid or not os.path.exists(thumb):
            print(f"::error::{pasta}: falta o id no publicados.json ou o youtube/thumbnail.jpg")
            erros += 1
            continue
        dados = open(thumb, "rb").read()
        if len(dados) > 2 * 1024 * 1024:
            print(f"::error::{pasta}: miniatura passa de 2 MB (limite do YouTube)")
            erros += 1
            continue
        try:
            urllib.request.urlopen(urllib.request.Request(
                f"{API_UP}/thumbnails/set?videoId={vid}", data=dados,
                headers={"Authorization": f"Bearer {tk}", "Content-Type": "image/jpeg"}), timeout=120)
            print(f"OK {pasta}: miniatura trocada em https://youtu.be/{vid}")
        except urllib.error.HTTPError as e:
            print(f"::error::{pasta}: YouTube recusou (HTTP {e.code}): {e.read().decode(errors='replace')[:300]}")
            erros += 1
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
