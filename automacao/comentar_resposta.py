"""Posta a RESPOSTA dos Shorts de desafio num comentário do canal (Patrick, 2026-11-17).

O Short "Desafio do Palito" não mostra a resposta: termina pedindo o palpite e diz que a certa está nos
comentários. Quando o Short já está PÚBLICO no YouTube, este script posta o texto de <short>/youtube/comentario.txt
como comentário do canal (uma vez só; anota em comentarios/respostas-shorts.json).
Fixar o comentário não existe na API do YouTube: se quiser, fixe pelo app (opcional).

Uso: python automacao/comentar_resposta.py      (roda em toda rodada do "Publicar do dia")
Precisa do token com youtube.force-ssl (o mesmo dos comentários). Sem ele, só avisa e não falha.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import RAIZ, ler_registro, status

FEITOS = os.path.join(RAIZ, "comentarios", "respostas-shorts.json")


def main():
    if not all(os.environ.get(k) for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN")):
        print("Sem Secrets do YouTube: nada a fazer.")
        return
    reg = ler_registro()
    feitos = json.load(open(FEITOS, encoding="utf-8")) if os.path.exists(FEITOS) else {}
    pend = []
    for pasta in sorted(reg.get("videos", {})):
        txt = os.path.join(RAIZ, pasta, "youtube", "comentario.txt")
        vid = status(reg, pasta, "youtube").get("id")
        if vid and os.path.exists(txt) and pasta not in feitos:
            pend.append((pasta, vid, open(txt, encoding="utf-8").read().strip()))
    if not pend:
        print("Nenhum Short com resposta para comentar.")
        return
    import comentarios_youtube as cy
    try:
        tk, escopo = cy.token()
    except SystemExit as e:
        print(f"AVISO: {e}")
        return
    if "youtube.force-ssl" not in escopo:
        print("AVISO: o token não tem youtube.force-ssl; rode 'Autorizar YouTube'. Respostas não postadas.")
        return
    try:
        st = cy.chamar("GET", "videos", tk, {"part": "status", "id": ",".join(v for _, v, _ in pend)})
    except SystemExit as e:
        print(f"AVISO: {e}")
        return
    publico = {i["id"] for i in st.get("items", []) if i["status"].get("privacyStatus") == "public"}
    for pasta, vid, texto in pend:
        if vid not in publico:
            print(f"{pasta}: ainda não está público; comento na próxima rodada.")
            continue
        try:
            r = cy.chamar("POST", "commentThreads", tk, {"part": "snippet"},
                          {"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": texto}}}})
        except SystemExit as e:
            print(f"AVISO: {pasta}: {e}")
            continue
        feitos[pasta] = {"video": vid, "comentario": r.get("id")}
        print(f"{pasta}: resposta comentada em https://youtube.com/shorts/{vid}")
    os.makedirs(os.path.dirname(FEITOS), exist_ok=True)
    with open(FEITOS, "w", encoding="utf-8") as f:
        json.dump(feitos, f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
