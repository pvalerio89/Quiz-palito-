"""Desempenho do canal Quiz Palito no YouTube (pela nuvem).

Uso: python automacao/estatisticas_youtube.py
  Grava estatisticas/AAAA-MM-DD.md e estatisticas/ultimo.json:
  inscritos, views, vídeos longos e Shorts (melhores/piores) e, se o token tiver a
  permissão yt-analytics.readonly, views/inscritos por dia dos últimos 28 dias.
"""
import datetime, json, os, re, sys, urllib.error, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import RAIZ
from comentarios_youtube import CANAL, token

API = "https://www.googleapis.com/youtube/v3"
ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"
PASTA = os.path.join(RAIZ, "estatisticas")


def get(url, tk, params):
    req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params),
                                 headers={"Authorization": f"Bearer {tk}"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60)), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}"


def segundos(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    return sum(int(v or 0) * k for v, k in zip(m.groups(), (3600, 60, 1))) if m else 0


def main():
    tk, escopo = token()
    print("Permissões do token:", escopo)
    ch, erro = get(f"{API}/channels", tk, {"part": "snippet,statistics,contentDetails", "id": CANAL})
    if erro:
        sys.exit(f"ERRO ao ler o canal ({erro}). O token precisa de youtube.force-ssl ou youtube.readonly.")
    c = ch["items"][0]
    est = c["statistics"]
    uploads = c["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, pg = [], None
    while True:
        p = {"part": "contentDetails", "playlistId": uploads, "maxResults": 50}
        if pg:
            p["pageToken"] = pg
        r, erro = get(f"{API}/playlistItems", tk, p)
        if erro:
            sys.exit(f"ERRO playlist: {erro}")
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        pg = r.get("nextPageToken")
        if not pg:
            break
    vids = []
    for i in range(0, len(ids), 50):
        r, erro = get(f"{API}/videos", tk, {"part": "snippet,statistics,contentDetails,status",
                                             "id": ",".join(ids[i:i + 50])})
        if erro:
            sys.exit(f"ERRO vídeos: {erro}")
        for v in r["items"]:
            s = v["statistics"]
            dur = segundos(v["contentDetails"]["duration"])
            vids.append({"id": v["id"], "titulo": v["snippet"]["title"],
                         "publicado": v["snippet"]["publishedAt"][:10],
                         "privacidade": v["status"]["privacyStatus"],
                         "tipo": "short" if dur <= 180 else "longo", "duracao": dur,
                         "views": int(s.get("viewCount", 0)), "likes": int(s.get("likeCount", 0)),
                         "comentarios": int(s.get("commentCount", 0))})

    # Analytics (opcional): por dia nos últimos 28 dias + retenção por vídeo
    hoje = datetime.date.today()
    ini = (hoje - datetime.timedelta(days=28)).isoformat()
    diario, por_video, aviso = [], {}, None
    r, erro = get(ANALYTICS, tk, {"ids": "channel==MINE", "startDate": ini, "endDate": hoje.isoformat(),
                                  "metrics": "views,estimatedMinutesWatched,subscribersGained,subscribersLost",
                                  "dimensions": "day", "sort": "day"})
    if erro:
        aviso = f"Analytics indisponível ({erro[:120]}). Falta autorizar yt-analytics.readonly."
    else:
        diario = r.get("rows", [])
        r2, e2 = get(ANALYTICS, tk, {"ids": "channel==MINE", "startDate": "2020-01-01", "endDate": hoje.isoformat(),
                                     "metrics": "views,averageViewDuration,averageViewPercentage,subscribersGained",
                                     "dimensions": "video", "sort": "-views", "maxResults": 200})
        if not e2:
            for row in r2.get("rows", []):
                por_video[row[0]] = {"dur_media": row[2], "pct_media": row[3], "inscritos": row[4]}
    for v in vids:
        v.update(por_video.get(v["id"], {}))

    # Curva de retenção (fração do vídeo -> % de quem ainda assiste), só com Analytics
    curvas = {}
    if not aviso:
        for v in vids:
            if v["privacidade"] != "public":
                continue
            r3, e3 = get(ANALYTICS, tk, {"ids": "channel==MINE", "startDate": "2020-01-01",
                                         "endDate": hoje.isoformat(), "metrics": "audienceWatchRatio",
                                         "dimensions": "elapsedVideoTimeRatio", "filters": f"video=={v['id']}"})
            if not e3 and r3.get("rows"):
                curvas[v["id"]] = [[round(a, 2), round(b, 3)] for a, b in r3["rows"]]
        json.dump({v["id"]: {"titulo": v["titulo"], "duracao": v["duracao"], "curva": curvas[v["id"]]}
                   for v in vids if v["id"] in curvas},
                  open(os.path.join(PASTA, "retencao.json"), "w", encoding="utf-8"), ensure_ascii=False)

    os.makedirs(PASTA, exist_ok=True)
    json.dump({"data": hoje.isoformat(), "canal": est, "videos": vids, "diario": diario, "aviso": aviso},
              open(os.path.join(PASTA, "ultimo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    L = [f"# Quiz Palito — {hoje.isoformat()}", "",
         f"Inscritos: **{est.get('subscriberCount')}** · Views totais: **{est.get('viewCount')}** · "
         f"Vídeos: **{est.get('videoCount')}**", ""]
    if aviso:
        L += [f"_{aviso}_", ""]
    if diario:
        L += ["## Últimos 28 dias (por dia)", "", "| dia | views | min assistidos | +insc | -insc |", "|---|---|---|---|---|"]
        L += [f"| {d[0]} | {d[1]} | {d[2]} | {d[3]} | {d[4]} |" for d in diario]
        L += [""]
    for tipo in ("longo", "short"):
        g = sorted([v for v in vids if v["tipo"] == tipo], key=lambda v: -v["views"])
        L += [f"## {'Vídeos longos' if tipo == 'longo' else 'Shorts'} ({len(g)})", "",
              "| views | likes | coment. | % assistido | publicado | título |", "|---|---|---|---|---|---|"]
        for v in g:
            pct = f"{v['pct_media']:.0f}%" if "pct_media" in v else "-"
            priv = "" if v["privacidade"] == "public" else f" ({v['privacidade']})"
            L.append(f"| {v['views']} | {v['likes']} | {v['comentarios']} | {pct} | {v['publicado']} | "
                     f"[{v['titulo']}](https://youtu.be/{v['id']}){priv} |")
        L += [""]
    if curvas:
        marcas = (0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.99)
        L += ["## Retenção (% de quem ainda assiste em cada ponto do vídeo)", "",
              "| tipo | dur | " + " | ".join(f"{int(m*100)}%" for m in marcas) + " | título |",
              "|---|---|" + "---|" * len(marcas) + "---|"]
        for v in sorted(vids, key=lambda v: (v["tipo"], -v.get("pct_media", 0))):
            c = curvas.get(v["id"])
            if not c:
                continue
            val = [min(c, key=lambda p: abs(p[0] - m))[1] for m in marcas]
            L.append(f"| {v['tipo']} | {v['duracao']//60}:{v['duracao']%60:02d} | "
                     + " | ".join(f"{x*100:.0f}" for x in val) + f" | {v['titulo'][:50]} |")
        L += [""]
    md = "\n".join(L)
    open(os.path.join(PASTA, f"{hoje.isoformat()}.md"), "w", encoding="utf-8").write(md)
    print(md)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8").write(md)


if __name__ == "__main__":
    main()
