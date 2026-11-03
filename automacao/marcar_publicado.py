"""Anota no publicados.json o que foi publicado fora da API (ex.: TikTok pelo navegador).

Uso: py -3 automacao/marcar_publicado.py <pasta> <youtube|tiktok> [--status publicado] [--id ID] [--url URL] [--corrigir]
  ex.: py -3 automacao/marcar_publicado.py shorts/brasil-1 tiktok --id 7702574023611305223
       py -3 automacao/marcar_publicado.py videos/07-novo youtube --status publicado   (depois de publicar no Studio)
Sem --corrigir, recusa sobrescrever um envio que já tem ID (evita apagar o histórico por engano).
Mudar de 'privado_teste' para 'publicado' na mesma plataforma é permitido e mantém o ID.
"""
import argparse, datetime, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import PLATAFORMAS, ler_registro, marcar, pasta_rel, salvar_registro, status

STATUS = ("publicado", "privado_teste", "pendente", "nao_se_aplica")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("plataforma", choices=PLATAFORMAS)
    ap.add_argument("--status", default="publicado", choices=STATUS)
    ap.add_argument("--id")
    ap.add_argument("--url")
    ap.add_argument("--corrigir", action="store_true")
    a = ap.parse_args()
    pasta = pasta_rel(a.pasta)
    doc = ler_registro()
    atual = dict(status(doc, pasta, a.plataforma))
    promocao = atual.get("status") == "privado_teste" and a.status == "publicado" and a.id in (None, atual.get("id"))
    if atual.get("id") and not promocao and not a.corrigir:
        sys.exit(f"PARADO: {pasta} já tem {a.plataforma} id {atual['id']} ({atual.get('status')}). "
                 "Use --corrigir se for mesmo para trocar.")
    vid = a.id or (atual.get("id") if promocao else None)
    url = (a.url or atual.get("url")) if promocao else a.url
    if not url and vid:
        url = (f"https://youtu.be/{vid}" if a.plataforma == "youtube"
               else f"https://www.tiktok.com/@quizpalitos/video/{vid}")
    novo = marcar(doc, pasta, a.plataforma, status=a.status, id=vid, url=url,
                  data=(atual.get("data") if atual.get("status") == a.status and atual.get("data")
                        else datetime.date.today().isoformat()),
                  origem=atual.get("origem", "navegador") if promocao else "navegador",
                  sha256=atual.get("sha256"))
    salvar_registro(doc)
    print(f"OK {pasta} / {a.plataforma}: {novo}")


if __name__ == "__main__":
    main()
