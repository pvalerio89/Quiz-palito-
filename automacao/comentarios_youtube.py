"""Comentários do YouTube (canal Quiz Palito) pela nuvem.

Uso:
  python automacao/comentarios_youtube.py ler
      Lê os comentários de todos os vídeos do publicados.json (+ comentarios/videos-extras.txt).
      Com a permissão youtube.force-ssl usa a API oficial; sem ela usa o yt-dlp (só leitura).
      Grava comentarios/pendentes.json e comentarios/pendentes.md (comentários ainda sem resposta do canal).
  python automacao/comentarios_youtube.py responder comentarios/respostas.json
      Publica as respostas aprovadas: lista de {"id": <id do comentário>, "resposta": "texto"}.
      Não responde duas vezes o mesmo comentário (anota em comentarios/respondidos.json).
  python automacao/comentarios_youtube.py link | trocar <endereço>
      Nova autorização do YouTube com permissão para comentários (veja o workflow Autorizar YouTube).

Curtir comentário não existe na API do YouTube: só pelo Studio (app do celular ou navegador).
"""
import datetime, json, os, subprocess, sys, tempfile, urllib.error, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import RAIZ, ler_registro

CANAL = "UCerGMTooT9vl4yVgW7Ggd3A"
API = "https://www.googleapis.com/youtube/v3"
PASTA = os.path.join(RAIZ, "comentarios")
RESPONDIDOS = os.path.join(PASTA, "respondidos.json")
EXTRAS = os.path.join(PASTA, "videos-extras.txt")
ESCOPOS = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.force-ssl"
REDIRECT = "http://127.0.0.1:8765"


def env(*nomes):
    falta = [n for n in nomes if not os.environ.get(n)]
    if falta:
        sys.exit(f"ERRO: faltam os Secrets {', '.join(falta)}.")
    return [os.environ[n] for n in nomes]


def token():
    cid, cs, rt = env("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN")
    dados = urllib.parse.urlencode({"client_id": cid, "client_secret": cs, "refresh_token": rt,
                                    "grant_type": "refresh_token"}).encode()
    try:
        r = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", dados, timeout=30))
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO ao renovar o acesso ao YouTube (HTTP {e.code}).")
    return r["access_token"], r.get("scope", "")


def chamar(metodo, caminho, tk, params=None, corpo=None):
    url = f"{API}/{caminho}?" + urllib.parse.urlencode(params or {})
    req = urllib.request.Request(url, method=metodo, headers={"Authorization": f"Bearer {tk}"},
                                 data=json.dumps(corpo).encode() if corpo is not None else None)
    if corpo is not None:
        req.add_header("Content-Type", "application/json")
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO YouTube {caminho} (HTTP {e.code}): {e.read().decode(errors='replace')[:400]}")


def videos():
    lista = {}
    for pasta, e in ler_registro()["videos"].items():
        yt = e.get("youtube", {})
        if yt.get("status") == "publicado" and yt.get("id"):
            lista[yt["id"]] = e.get("titulo") or pasta
    if os.path.exists(EXTRAS):
        for linha in open(EXTRAS, encoding="utf-8"):
            p = linha.split("#", 1)
            vid = p[0].strip()
            if vid:
                lista.setdefault(vid, p[1].strip() if len(p) > 1 else vid)
    return lista


def ler_api(tk, titulos):
    """Todos os comentários do canal, com as respostas (API oficial)."""
    saida, pagina = [], None
    while True:
        p = {"part": "snippet,replies", "allThreadsRelatedToChannelId": CANAL, "maxResults": 100,
             "textFormat": "plainText", "order": "time"}
        if pagina:
            p["pageToken"] = pagina
        r = chamar("GET", "commentThreads", tk, p)
        for t in r.get("items", []):
            top = t["snippet"]["topLevelComment"]
            s = top["snippet"]
            respostas = t.get("replies", {}).get("comments", [])
            saida.append({
                "id": top["id"], "video": s.get("videoId"), "titulo": titulos.get(s.get("videoId"), s.get("videoId")),
                "autor": s.get("authorDisplayName"), "texto": s.get("textDisplay"),
                "data": s.get("publishedAt", "")[:10], "curtidas": s.get("likeCount", 0),
                "do_canal": s.get("authorChannelId", {}).get("value") == CANAL,
                "canal_respondeu": any(x["snippet"].get("authorChannelId", {}).get("value") == CANAL for x in respostas),
                "total_respostas": t["snippet"].get("totalReplyCount", 0)})
        pagina = r.get("nextPageToken")
        if not pagina:
            return saida


def ler_ytdlp(titulos):
    """Sem permissão de comentários: lê pelo yt-dlp, vídeo a vídeo."""
    saida = []
    with tempfile.TemporaryDirectory() as tmp:
        for vid, titulo in titulos.items():
            destino = os.path.join(tmp, vid)
            r = subprocess.run(["yt-dlp", "--skip-download", "--write-comments", "--no-warnings", "-q",
                                "--extractor-args", "youtube:max_comments=300,all,300,50;comment_sort=new",
                                "-o", destino, f"https://www.youtube.com/watch?v={vid}"],
                               capture_output=True, text=True)
            arq = destino + ".info.json"
            if not os.path.exists(arq):
                print(f"::warning::não li {vid}: {r.stderr.strip()[-300:]}")
                continue
            info = json.load(open(arq, encoding="utf-8"))
            todos = info.get("comments") or []
            for c in todos:
                if c.get("parent", "root") != "root":
                    continue
                filhos = [x for x in todos if x.get("parent") == c["id"]]
                saida.append({
                    "id": c["id"], "video": vid, "titulo": titulo, "autor": c.get("author"),
                    "texto": c.get("text"),
                    "data": datetime.datetime.fromtimestamp(c["timestamp"], datetime.UTC).date().isoformat()
                    if c.get("timestamp") else "",
                    "curtidas": c.get("like_count", 0), "coracao": bool(c.get("is_favorited")),
                    "do_canal": bool(c.get("author_is_uploader")),
                    "canal_respondeu": any(x.get("author_is_uploader") for x in filhos),
                    "total_respostas": len(filhos)})
    return saida


def ler():
    titulos = videos()
    modo = "yt-dlp"
    tk, escopo = token() if os.environ.get("YT_REFRESH_TOKEN") else (None, "")
    if tk and "youtube.force-ssl" in escopo:
        comentarios, modo = ler_api(tk, titulos), "API"
    else:
        comentarios = ler_ytdlp(titulos)
    ja = set(json.load(open(RESPONDIDOS, encoding="utf-8"))) if os.path.exists(RESPONDIDOS) else set()
    pend = [c for c in comentarios if not c["do_canal"] and not c["canal_respondeu"] and c["id"] not in ja]
    pend.sort(key=lambda c: (c["titulo"] or "", c["data"]), reverse=False)
    hoje = datetime.date.today().isoformat()
    os.makedirs(PASTA, exist_ok=True)
    json.dump({"data": hoje, "modo": modo, "total_lidos": len(comentarios), "pendentes": pend},
              open(os.path.join(PASTA, "pendentes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = [f"# Comentários sem resposta — {hoje}", "",
          f"Lidos {len(comentarios)} comentários em {len(titulos)} vídeos ({modo}). Sem resposta do canal: {len(pend)}.", ""]
    atual = None
    for c in pend:
        if c["titulo"] != atual:
            atual = c["titulo"]
            md += ["", f"## {atual}", f"https://youtu.be/{c['video']}", ""]
        md.append(f"- **{c['autor']}** ({c['data']}): {c['texto']}  \n  `id: {c['id']}`")
    open(os.path.join(PASTA, "pendentes.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"OK ({modo}): {len(comentarios)} comentários, {len(pend)} sem resposta.")


def responder(arquivo):
    tk, escopo = token()
    if "youtube.force-ssl" not in escopo:
        sys.exit("ERRO: o token do YouTube só tem permissão de envio. Rode o workflow 'Autorizar YouTube' "
                 "e troque o Secret YT_REFRESH_TOKEN.")
    ja = json.load(open(RESPONDIDOS, encoding="utf-8")) if os.path.exists(RESPONDIDOS) else []
    feitos = 0
    for item in json.load(open(arquivo, encoding="utf-8")):
        cid, texto = item["id"], item["resposta"].strip()
        if cid in ja or not texto:
            print(f"pulado (já respondido ou vazio): {cid}")
            continue
        chamar("POST", "comments", tk, {"part": "snippet"},
               {"snippet": {"parentId": cid, "textOriginal": texto}})
        ja.append(cid)
        json.dump(ja, open(RESPONDIDOS, "w", encoding="utf-8"), indent=1)  # grava a cada uma
        feitos += 1
        print(f"respondido: {cid} ({item.get('autor', '')})")
    print(f"OK: {feitos} respostas publicadas.")


def link():
    (cid,) = env("YT_CLIENT_ID")
    print("https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": cid, "redirect_uri": REDIRECT, "response_type": "code", "scope": ESCOPOS,
        "access_type": "offline", "prompt": "consent", "state": "quizpalito"}))


def trocar(endereco):
    cid, cs = env("YT_CLIENT_ID", "YT_CLIENT_SECRET")
    q = urllib.parse.parse_qs(urllib.parse.urlparse(endereco.strip()).query)
    code = (q.get("code") or [endereco.strip()])[0]
    try:
        r = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", urllib.parse.urlencode({
            "code": code, "client_id": cid, "client_secret": cs, "redirect_uri": REDIRECT,
            "grant_type": "authorization_code"}).encode(), timeout=30))
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO na troca do código (HTTP {e.code}): {e.read().decode(errors='replace')[:300]}")
    if "refresh_token" not in r:
        sys.exit("O Google não devolveu o token de longa duração. Gere o link de novo e autorize outra vez.")
    out = os.environ.get("GITHUB_STEP_SUMMARY")
    texto = ("### Copie este valor para o Secret `YT_REFRESH_TOKEN` (substitui o antigo)\n\n```\n"
             + r["refresh_token"] + "\n```\n\nPermissões: " + r.get("scope", "") +
             "\n\nDepois de salvar, apague esta execução.\n")
    if out:
        open(out, "a", encoding="utf-8").write(texto)
        # o app do GitHub no celular não mostra o resumo: repete no log do passo
        print("OK: copie a linha abaixo para o Secret YT_REFRESH_TOKEN e depois apague esta execução.")
        print(r["refresh_token"])
    else:
        print(texto)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "ler":
        ler()
    elif cmd == "responder" and len(sys.argv) > 2:
        responder(sys.argv[2])
    elif cmd == "link":
        link()
    elif cmd == "trocar" and len(sys.argv) > 2:
        trocar(sys.argv[2])
    else:
        sys.exit(__doc__)
