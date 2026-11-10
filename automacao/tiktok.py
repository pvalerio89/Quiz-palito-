"""TikTok pela API oficial (Content Posting API, Direct Post).

Uso:
  python automacao/tiktok.py link                       -> mostra o link de login (1 vez, para autorizar)
  python automacao/tiktok.py trocar "<endereço colado>" -> troca o código do login pelo refresh token
  python automacao/tiktok.py publicar <pasta> <arquivo.mp4> [legenda.txt]
Variáveis de ambiente (Secrets do GitHub; nunca são impressas):
  TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_REFRESH_TOKEN (este só para publicar)
  TIKTOK_REDIRECT (opcional; padrão abaixo, tem que ser igual ao cadastrado no app do TikTok)
Enquanto o app não passar na auditoria do TikTok, ele só publica como "somente eu" (SELF_ONLY).
"""
import datetime, json, os, sys, time, urllib.error, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import checar_duplicado, ler_registro, marcar, pasta_rel, salvar_registro

API = "https://open.tiktokapis.com/v2"
REDIRECT = os.environ.get("TIKTOK_REDIRECT") or "https://pvalerio89.github.io/quizpalito.github.io/tiktok.html"
ESCOPOS = "user.info.basic,video.publish"
LIMITE_UM_PEDACO = 64 * 1024 * 1024  # até 64 MB o vídeo vai inteiro numa parte só
PEDACO = 10 * 1024 * 1024


def env(*nomes):
    falta = [n for n in nomes if not os.environ.get(n)]
    if falta:
        sys.exit(f"ERRO: faltam os Secrets {', '.join(falta)}.")
    return [os.environ[n] for n in nomes]


def chamar(url, dados=None, token=None, form=False, metodo="POST"):
    h = {}
    if token:
        h["Authorization"] = f"Bearer {token}"
    if form:
        corpo = urllib.parse.urlencode(dados).encode()
        h["Content-Type"] = "application/x-www-form-urlencoded"
    else:
        corpo = json.dumps(dados or {}).encode()
        h["Content-Type"] = "application/json; charset=UTF-8"
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, data=corpo, headers=h, method=metodo), timeout=60)
        resp = json.load(r)
    except urllib.error.HTTPError as e:
        try:
            resp = json.loads(e.read().decode())
        except Exception:
            sys.exit(f"ERRO HTTP {e.code} em {url.split('?')[0]}")
    erro = resp.get("error")
    if isinstance(erro, dict) and erro.get("code") not in (None, "ok"):
        sys.exit(f"ERRO do TikTok: {erro.get('code')} - {erro.get('message')}")
    if "error" in resp and isinstance(erro, str):  # formato do /oauth/token/
        sys.exit(f"ERRO do TikTok: {erro} - {resp.get('error_description')}")
    return resp


def link():
    (ck,) = env("TIKTOK_CLIENT_KEY")
    q = urllib.parse.urlencode({"client_key": ck, "scope": ESCOPOS, "response_type": "code",
                                "redirect_uri": REDIRECT, "state": "quizpalito"})
    print(f"https://www.tiktok.com/v2/auth/authorize/?{q}")


def trocar(endereco):
    ck, cs = env("TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET")
    q = urllib.parse.parse_qs(urllib.parse.urlparse(endereco.strip()).query)
    code = (q.get("code") or [endereco.strip()])[0]
    r = chamar(f"{API}/oauth/token/", {"client_key": ck, "client_secret": cs, "code": code,
                                         "grant_type": "authorization_code", "redirect_uri": REDIRECT}, form=True)
    if "video.publish" not in r.get("scope", ""):
        print("::warning::o login não liberou video.publish; confira os escopos do app.")
    return r["refresh_token"], r.get("refresh_expires_in")


def acesso():
    ck, cs, rt = env("TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET", "TIKTOK_REFRESH_TOKEN")
    r = chamar(f"{API}/oauth/token/", {"client_key": ck, "client_secret": cs, "grant_type": "refresh_token",
                                         "refresh_token": rt}, form=True)
    if r.get("refresh_token") and r["refresh_token"] != rt:
        print("::warning::o TikTok trocou o refresh token. Rode 'Autorizar TikTok' de novo quando der.")
    return r["access_token"]


def publicar(pasta, mp4, legenda_txt=None):
    pasta = pasta_rel(pasta)
    doc = ler_registro()
    h = checar_duplicado(doc, pasta, "tiktok", mp4)
    legenda = open(legenda_txt, encoding="utf-8").read().strip() if legenda_txt and os.path.exists(legenda_txt) else ""
    tk = acesso()

    info = chamar(f"{API}/post/publish/creator_info/query/", token=tk)["data"]
    opcoes = info.get("privacy_level_options", [])
    priv = "PUBLIC_TO_EVERYONE" if "PUBLIC_TO_EVERYONE" in opcoes else "SELF_ONLY"
    print(f"Conta: @{info.get('creator_username')} | privacidade: {priv} (opções: {', '.join(opcoes)})")
    dur = info.get("max_video_post_duration_sec")

    tam = os.path.getsize(mp4)
    pedaco = tam if tam <= LIMITE_UM_PEDACO else PEDACO
    partes = 1 if pedaco == tam else tam // pedaco  # a última parte leva o resto
    ini = chamar(f"{API}/post/publish/video/init/", {
        "post_info": {"title": legenda[:2200], "privacy_level": priv, "disable_duet": False,
                      "disable_comment": False, "disable_stitch": False, "video_cover_timestamp_ms": 1000},
        "source_info": {"source": "FILE_UPLOAD", "video_size": tam, "chunk_size": pedaco,
                        "total_chunk_count": partes}}, token=tk)["data"]
    pid, url = ini["publish_id"], ini["upload_url"]
    print(f"Enviando {os.path.basename(mp4)} ({tam / 1e6:.0f} MB, {partes} parte(s)); limite da conta: {dur}s", flush=True)
    with open(mp4, "rb") as f:
        for i in range(partes):
            a = i * pedaco
            b = tam - 1 if i == partes - 1 else a + pedaco - 1
            f.seek(a)
            dados = f.read(b - a + 1)
            req = urllib.request.Request(url, data=dados, method="PUT", headers={
                "Content-Type": "video/mp4", "Content-Length": str(len(dados)),
                "Content-Range": f"bytes {a}-{b}/{tam}"})
            try:
                urllib.request.urlopen(req, timeout=600)
            except urllib.error.HTTPError as e:
                sys.exit(f"ERRO no envio da parte {i + 1} (HTTP {e.code})")

    post_id, st = None, "?"
    for _ in range(60):  # até ~10 min processando
        time.sleep(10)
        d = chamar(f"{API}/post/publish/status/fetch/", {"publish_id": pid}, token=tk)["data"]
        st = d.get("status")
        print("status:", st, flush=True)
        if st == "FAILED":
            sys.exit(f"ERRO: o TikTok recusou o vídeo ({d.get('fail_reason')}).")
        if st == "PUBLISH_COMPLETE":
            ids = d.get("publicaly_available_post_id") or d.get("publicly_available_post_id") or []
            post_id = str(ids[0]) if ids else None
            break
    publico = priv == "PUBLIC_TO_EVERYONE"
    marcar(doc, pasta, "tiktok", status="publicado" if publico else "privado_teste", id=post_id or pid,
           url=f"https://www.tiktok.com/@{info.get('creator_username')}/video/{post_id}" if post_id else None,
           data=datetime.date.today().isoformat(), origem="github-actions", sha256=h)
    salvar_registro(doc)
    if not publico:
        print("::warning::O TikTok só liberou 'somente eu' (app ainda sem auditoria). O vídeo ficou privado.")
    print(f"OK TikTok ({st}, {priv}): {post_id or pid}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "link":
        link()
    elif cmd == "trocar" and len(sys.argv) >= 3:
        rt, exp = trocar(sys.argv[2])
        out = os.environ.get("GITHUB_STEP_SUMMARY")
        if out:  # aparece só no resumo da execução; o log não mostra
            with open(out, "a", encoding="utf-8") as f:
                f.write("### Copie este valor para o Secret `TIKTOK_REFRESH_TOKEN`\n\n```\n" + rt + "\n```\n\n"
                        f"Vale por {int(exp or 0) // 86400} dias. Depois de salvar, peça para apagar esta execução.\n")
            print("OK: refresh token no resumo da execução (aba Summary).")
        else:
            print(rt)
    elif cmd == "publicar" and len(sys.argv) >= 4:
        publicar(sys.argv[2], os.path.abspath(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else None)
    else:
        sys.exit(__doc__)
