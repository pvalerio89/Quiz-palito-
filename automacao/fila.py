"""Fila de publicação diária (fila/fila.json). Usado pelo workflow "Publicar do dia".

Uso:
  py -3 automacao/fila.py proximo            -> escolhe o 1º item 'pronto' e escreve id/video/short
                                                (no GitHub vai para GITHUB_OUTPUT)
  py -3 automacao/fila.py fechar <id> <ok|erro> [motivo]
                                             -> marca o item como publicado ou erro e põe o link
                                                do vídeo longo na descrição/legenda do Short
  py -3 automacao/fila.py status             -> mostra a fila
"""
import datetime, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import RAIZ, ler_registro, status

FILA = os.path.join(RAIZ, "fila", "fila.json")
MARCA = "LINK_DO_VIDEO_LONGO"


def ler():
    with open(FILA, encoding="utf-8") as f:
        return json.load(f)


def salvar(doc):
    with open(FILA, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")


def saida(**campos):
    destino = os.environ.get("GITHUB_OUTPUT")
    for k, v in campos.items():
        print(f"{k}={v}")
        if destino:
            with open(destino, "a", encoding="utf-8") as f:
                f.write(f"{k}={v}\n")


def feito(reg, pasta):
    return bool(pasta) and status(reg, pasta, "youtube").get("status") == "publicado"


def proximo():
    doc, reg = ler(), ler_registro()
    for it in doc["itens"]:
        if it.get("status") != "pronto":
            continue
        video, short = it.get("video") or "", it.get("short") or ""
        for p in (video, short):
            if p and not os.path.isdir(os.path.join(RAIZ, p)):
                sys.exit(f"ERRO: item {it['id']}: pasta {p} não existe no repositório.")
        saida(id=it["id"], video=video, short=short,
              video_feito=str(feito(reg, video)).lower(), short_feito=str(feito(reg, short)).lower())
        return
    print("Nenhum item 'pronto' na fila. Nada para publicar hoje.")
    saida(id="", video="", short="", video_feito="false", short_feito="false")


def trocar_link(pasta_short, url):
    trocados = []
    yt = os.path.join(RAIZ, pasta_short, "youtube")
    for nome in ("descricao.txt", "tiktok.txt"):
        p = os.path.join(yt, nome)
        if os.path.exists(p):
            t = open(p, encoding="utf-8").read()
            if MARCA in t:
                open(p, "w", encoding="utf-8").write(t.replace(MARCA, url))
                trocados.append(nome)
    return trocados


def fechar(ident, resultado, motivo=""):
    doc, reg = ler(), ler_registro()
    it = next((i for i in doc["itens"] if i["id"] == ident), None)
    if not it:
        sys.exit(f"ERRO: item {ident} não está na fila.")
    url = status(reg, it.get("video") or "", "youtube").get("url") if it.get("video") else None
    if url and it.get("short"):
        t = trocar_link(it["short"], url)
        if t:
            print(f"Link do vídeo longo posto em {it['short']}/youtube: {', '.join(t)}")
    links = {k: status(reg, it[k], "youtube").get("url") for k in ("video", "short") if it.get(k)}
    if resultado == "ok":
        it["status"] = "publicado"
        it["publicado_em"] = datetime.date.today().isoformat()
        it.pop("erro", None)
    else:
        it["status"] = "erro"
        it["erro"] = f"{datetime.date.today().isoformat()}: {motivo or 'falhou no Publicar do dia'}"
    it["links"] = {k: v for k, v in links.items() if v}
    salvar(doc)
    print(f"{ident}: {it['status']} {json.dumps(it['links'], ensure_ascii=False)}")


def mostrar():
    for it in ler()["itens"]:
        print(f"{it['status']:10} {it['id']:28} {it.get('video') or '-'} | {it.get('short') or '-'}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "proximo":
        proximo()
    elif cmd == "fechar" and len(sys.argv) >= 4:
        fechar(sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))
    elif cmd == "status":
        mostrar()
    else:
        sys.exit(__doc__)
