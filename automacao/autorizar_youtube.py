"""Roda UMA vez no seu PC para dar ao GitHub permissão de subir vídeos no canal Quiz Palito.

Uso: py -3 automacao/autorizar_youtube.py C:\\caminho\\client_secret.json
  1. Abre o login do Google no navegador. Entre com a conta do canal Quiz Palito e aceite.
  2. Salva o token em %USERPROFILE%\\.config\\quiz-palito\\youtube-token.json (fora do projeto e fora do Git).
  3. Você copia os 3 valores desse arquivo para os Secrets do GitHub e depois apaga o arquivo.
O token nunca é mostrado na tela. Permissão pedida: só enviar vídeos (youtube.upload).
"""
import http.server, json, os, secrets, sys, urllib.parse, urllib.request, webbrowser

ESCOPO = "https://www.googleapis.com/auth/youtube.upload"
DESTINO = os.path.join(os.path.expanduser("~"), ".config", "quiz-palito", "youtube-token.json")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    cfg = cfg.get("installed") or cfg.get("web")
    cid, csec = cfg["client_id"], cfg["client_secret"]
    estado = secrets.token_urlsafe(16)
    recebido = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(self.path).query))
            if q.get("state") == estado:
                recebido.update(q)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("Pronto! Pode fechar esta aba e voltar ao terminal.".encode())

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    volta = f"http://127.0.0.1:{srv.server_port}"
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": cid, "redirect_uri": volta, "response_type": "code", "scope": ESCOPO,
        "access_type": "offline", "prompt": "consent", "state": estado})
    print("Abrindo o login do Google. Use a conta do canal Quiz Palito.")
    webbrowser.open(url)
    while "code" not in recebido and "error" not in recebido:
        srv.handle_request()
    if "error" in recebido:
        sys.exit(f"Autorização cancelada: {recebido['error']}")
    r = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", urllib.parse.urlencode({
        "code": recebido["code"], "client_id": cid, "client_secret": csec, "redirect_uri": volta,
        "grant_type": "authorization_code"}).encode(), timeout=30))
    if "refresh_token" not in r:
        sys.exit("O Google não devolveu o token de longa duração. Remova o acesso do app na conta e rode de novo.")
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    json.dump({"YT_CLIENT_ID": cid, "YT_CLIENT_SECRET": csec, "YT_REFRESH_TOKEN": r["refresh_token"]},
              open(DESTINO, "w", encoding="utf-8"), indent=1)
    print(f"OK. Token salvo em {DESTINO}")
    print("Copie os 3 valores para GitHub > Settings > Secrets and variables > Actions e depois apague o arquivo.")


if __name__ == "__main__":
    main()
