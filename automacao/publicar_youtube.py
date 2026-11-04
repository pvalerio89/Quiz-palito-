"""Envia um vídeo ao YouTube pela API oficial, como PRIVADO (teste), e anota no publicados.json.

Uso: py -3 automacao/publicar_youtube.py <pasta> <arquivo.mp4>
Precisa das variáveis de ambiente (no GitHub vêm dos Secrets; nunca são impressas):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
Título, descrição, tags e miniatura vêm de <pasta>/youtube/ (titulo.txt, descricao.txt, tags.txt, thumbnail.jpg).
Não envia de novo se o registro já tiver esse vídeo como 'publicado' ou 'privado_teste'.
"""
import datetime, json, os, sys, urllib.error, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import RAIZ, checar_duplicado, ler_registro, marcar, pasta_rel, salvar_registro

API_UP = "https://www.googleapis.com/upload/youtube/v3"


def ler(p, padrao=""):
    return open(p, encoding="utf-8").read().strip() if os.path.exists(p) else padrao


def token():
    falta = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(k)]
    if falta:
        sys.exit(f"ERRO: faltam os Secrets {', '.join(falta)}.")
    dados = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    try:
        r = urllib.request.urlopen("https://oauth2.googleapis.com/token", dados, timeout=30)
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO ao renovar o acesso ao YouTube (HTTP {e.code}). Refaça automacao/autorizar_youtube.py.")
    return json.load(r)["access_token"]


def tags_ok(texto):
    tags, total = [], 0
    for t in [x.strip() for x in texto.replace("\n", ",").split(",") if x.strip()]:
        if total + len(t) + 1 > 480:  # limite do YouTube é 500 caracteres somando todas
            break
        tags.append(t)
        total += len(t) + 1
    return tags


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    pasta, mp4 = pasta_rel(sys.argv[1]), os.path.abspath(sys.argv[2])
    if not os.path.exists(mp4):
        sys.exit(f"ERRO: arquivo não encontrado: {mp4}")
    yt = os.path.join(RAIZ, pasta, "youtube")
    alt = os.path.join(os.path.dirname(mp4), "youtube")  # kit gerado junto do vídeo na nuvem
    if os.path.isdir(alt):
        yt = alt
    doc = ler_registro()
    h = checar_duplicado(doc, pasta, "youtube", mp4)

    titulo = ler(os.path.join(yt, "titulo.txt")).splitlines()[0][:100]
    meta = {
        "snippet": {"title": titulo, "description": ler(os.path.join(yt, "descricao.txt"))[:5000],
                    "tags": tags_ok(ler(os.path.join(yt, "tags.txt"))), "categoryId": "24",
                    "defaultLanguage": "pt-BR", "defaultAudioLanguage": "pt-BR"},
        "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
                   "containsSyntheticMedia": False},
    }
    tk = token()
    tam = os.path.getsize(mp4)
    req = urllib.request.Request(
        f"{API_UP}/videos?uploadType=resumable&part=snippet,status", data=json.dumps(meta).encode(),
        headers={"Authorization": f"Bearer {tk}", "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(tam)})
    try:
        destino = urllib.request.urlopen(req, timeout=60).headers["Location"]
        print(f"Enviando {os.path.basename(mp4)} ({tam / 1e6:.0f} MB) como privado...", flush=True)
        with open(mp4, "rb") as f:
            up = urllib.request.Request(destino, data=f, method="PUT",
                                        headers={"Authorization": f"Bearer {tk}", "Content-Type": "video/mp4",
                                                 "Content-Length": str(tam)})
            vid = json.load(urllib.request.urlopen(up, timeout=3600))["id"]
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO no envio (HTTP {e.code}): {e.read().decode(errors='replace')[:500]}")

    thumb = os.path.join(yt, "thumbnail.jpg")
    if os.path.exists(thumb) and not pasta.startswith("shorts/"):
        try:
            urllib.request.urlopen(urllib.request.Request(
                f"{API_UP}/thumbnails/set?videoId={vid}", data=open(thumb, "rb").read(),
                headers={"Authorization": f"Bearer {tk}", "Content-Type": "image/jpeg"}), timeout=120)
            print("Miniatura enviada.")
        except urllib.error.HTTPError as e:
            print(f"::warning::miniatura não foi aceita (HTTP {e.code}); suba pelo Studio.")

    marcar(doc, pasta, "youtube", status="privado_teste", id=vid, url=f"https://youtu.be/{vid}",
           data=datetime.date.today().isoformat(), origem="github-actions", sha256=h)
    salvar_registro(doc)
    print(f"OK enviado como PRIVADO: https://youtu.be/{vid}  (publique pelo YouTube Studio)")


if __name__ == "__main__":
    main()
