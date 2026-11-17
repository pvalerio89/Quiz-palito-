"""Muda a hora em que vídeos JÁ agendados no YouTube entram no ar (publishAt).

Uso: py -3 automacao/reagendar.py <DE>=<PARA> [<DE>=<PARA> ...]
  DE e PARA em UTC, no formato AAAA-MM-DDTHH:MM:SSZ (ex.: 2026-11-13T21:00:00Z=2026-11-13T22:14:00Z).
DE também pode ser o id do item (ex.: 2026-11-15-jogador-pela-carreira=2026-11-17T23:30:00Z).
Para cada item de fila/fila.json com no_ar_em (ou agendar_em, se falhou no meio) == DE, troca o publishAt do vídeo longo e do Short no YouTube
e grava o novo horário em fila/fila.json e publicados.json. Vídeo que já está público é pulado.
Precisa dos Secrets YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN.
"""
import datetime, json, os, sys, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import ler_registro, salvar_registro, status
from fila import BRASILIA, ler, salvar
from publicar_youtube import token

API = "https://www.googleapis.com/youtube/v3/videos"


def chamar(tk, url, corpo=None):
    req = urllib.request.Request(url, data=json.dumps(corpo).encode() if corpo else None,
                                 method="PUT" if corpo else "GET",
                                 headers={"Authorization": f"Bearer {tk}", "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO no YouTube (HTTP {e.code}): {e.read().decode(errors='replace')[:500]}")


def trocar_no_youtube(tk, vid, para):
    itens = chamar(tk, f"{API}?part=status&id={vid}").get("items", [])
    if not itens:
        sys.exit(f"ERRO: vídeo {vid} não encontrado no canal.")
    st = itens[0]["status"]
    if st.get("privacyStatus") != "private" or not st.get("publishAt"):
        print(f"  {vid}: já está {st.get('privacyStatus')} (sem agendamento), não mexi.")
        return False
    novo = {k: st[k] for k in ("privacyStatus", "embeddable", "license", "publicStatsViewable",
                               "selfDeclaredMadeForKids", "containsSyntheticMedia") if k in st}
    novo["publishAt"] = para
    r = chamar(tk, f"{API}?part=status", {"id": vid, "status": novo})
    print(f"  {vid}: {st['publishAt']} -> {r['status'].get('publishAt')}")
    return True


def main():
    trocas = dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a)
    if not trocas:
        sys.exit(__doc__)
    agora = datetime.datetime.now(datetime.timezone.utc)
    for de, para in trocas.items():
        if datetime.datetime.fromisoformat(para.replace("Z", "+00:00")) < agora + datetime.timedelta(minutes=20):
            sys.exit(f"ERRO: {para} está no passado ou perto demais (o YouTube precisa de folga).")
    doc, reg, tk = ler(), ler_registro(), token()
    achou = 0
    for it in doc["itens"]:
        campo = "agendar_em" if it.get("agendar_em") and not it.get("no_ar_em") else "no_ar_em"
        para = trocas.get(it["id"]) or trocas.get(it.get(campo) or "")  # DE = horário ou id do item
        if not para:
            continue
        achou += 1
        print(f"{it['id']}: {it.get(campo)} -> {para}")
        for k in ("video", "short"):
            pasta = it.get(k)
            yt = status(reg, pasta, "youtube") if pasta else {}
            if not yt.get("id"):
                continue
            if trocar_no_youtube(tk, yt["id"], para):
                reg["videos"][pasta]["youtube"]["no_ar_em"] = para
        it[campo] = para
        if campo == "agendar_em":  # item com 'erro': a nova tentativa do Short usa o mesmo horário
            continue
        it["no_ar_brasilia"] = datetime.datetime.fromisoformat(para.replace("Z", "+00:00")) \
            .astimezone(BRASILIA).strftime("%d/%m %Hh%M")
    if not achou:
        sys.exit("Nenhum item da fila tem esses horários. Nada mudou.")
    salvar(doc)
    salvar_registro(reg)


if __name__ == "__main__":
    main()
