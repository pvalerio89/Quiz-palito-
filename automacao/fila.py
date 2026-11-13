"""Fila de publicação diária (fila/fila.json). Usado pelo workflow "Publicar do dia".

Uso:
  py -3 automacao/fila.py proximo            -> escolhe o 1º item 'pronto' e o próximo horário livre
                                                (HORARIOS) e escreve id/video/short/agendar
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

# Horários em que os vídeos entram no ar (Brasília, UTC-3, sem horário de verão).
# O workflow sobe o vídeo antes e o YouTube solta na hora certa (publishAt), então o atraso do GitHub não importa.
HORARIOS = ((12, 9), (17, 30), (20, 30))  # 3 por dia (Patrick, 2026-11-13)
BRASILIA = datetime.timezone(datetime.timedelta(hours=-3))
MARGEM = datetime.timedelta(hours=2)  # tempo para gerar e subir antes do horário
JANELA = datetime.timedelta(hours=24)  # só agenda horários das próximas 24 h


def agora():
    a = os.environ.get("FILA_AGORA")  # só para testar: "2026-11-10T20:00:00-03:00"
    return datetime.datetime.fromisoformat(a) if a else datetime.datetime.now(datetime.timezone.utc)


def horario_livre(doc, ref=None):
    """Próximo horário de HORARIOS (>= agora + MARGEM, dentro da JANELA) que nenhum item já ocupa."""
    ref = ref or agora()
    ocupados = {i["no_ar_em"] for i in doc["itens"] if i.get("no_ar_em")}
    dia = ref.astimezone(BRASILIA).date()
    for d in range(3):
        for h, m in HORARIOS:
            t = datetime.datetime.combine(dia + datetime.timedelta(days=d), datetime.time(h, m), BRASILIA)
            iso = t.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            if ref + MARGEM <= t <= ref + JANELA and iso not in ocupados:
                return iso
    return ""


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
    sem_agendar = os.environ.get("SEM_AGENDAR") == "true"  # "Publicar JÁ" pedido à mão
    quando = "" if sem_agendar else horario_livre(doc)
    if not quando and not sem_agendar:
        print("Os horários das próximas 24 h já têm vídeo agendado. Nada a fazer agora.")
        saida(id="", video="", short="", video_feito="false", short_feito="false", agendar="")
        return
    for it in doc["itens"]:
        if it.get("status") != "pronto":
            continue
        video, short = it.get("video") or "", it.get("short") or ""
        for p in (video, short):
            if p and not os.path.isdir(os.path.join(RAIZ, p)):
                sys.exit(f"ERRO: item {it['id']}: pasta {p} não existe no repositório.")
        # Item que já tinha horário (falhou no meio) mantém o dele se ainda der tempo.
        antes = it.get("agendar_em", "")
        if antes and not sem_agendar and datetime.datetime.fromisoformat(antes.replace("Z", "+00:00")) >= agora() + MARGEM:
            quando = antes
        saida(id=it["id"], video=video, short=short, agendar=quando,
              video_feito=str(feito(reg, video)).lower(), short_feito=str(feito(reg, short)).lower())
        return
    print("Nenhum item 'pronto' na fila. Nada para publicar agora.")
    saida(id="", video="", short="", video_feito="false", short_feito="false", agendar="")


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


def fechar(ident, resultado, motivo="", quando=""):
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
        if quando:
            it["no_ar_em"] = quando
            it["no_ar_brasilia"] = datetime.datetime.fromisoformat(quando.replace("Z", "+00:00")) \
                .astimezone(BRASILIA).strftime("%d/%m %Hh%M")
        it.pop("erro", None)
        it.pop("agendar_em", None)
    else:
        it["status"] = "erro"
        it["erro"] = f"{datetime.date.today().isoformat()}: {motivo or 'falhou no Publicar do dia'}"
        if quando:  # se uma parte já subiu agendada, a nova tentativa usa o mesmo horário
            it["agendar_em"] = quando
    it["links"] = {k: v for k, v in links.items() if v}
    salvar(doc)
    print(f"{ident}: {it['status']} {json.dumps(it['links'], ensure_ascii=False)}")


def mostrar():
    for it in ler()["itens"]:
        print(f"{it['status']:10} {it['id']:28} {it.get('video') or '-'} | {it.get('short') or '-'}"
              f"{'  (no ar ' + it['no_ar_brasilia'] + ')' if it.get('no_ar_brasilia') else ''}")
    print(f"Próximo horário livre: {horario_livre(ler()) or 'nenhum nas próximas 24 h'}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "proximo":
        proximo()
    elif cmd == "fechar" and len(sys.argv) >= 4:
        fechar(sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]), os.environ.get("AGENDAR", ""))
    elif cmd == "status":
        mostrar()
    else:
        sys.exit(__doc__)
