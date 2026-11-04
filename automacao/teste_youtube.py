"""Envio de TESTE ao YouTube: cópia de um vídeo já gerado, sempre PRIVADA e com título "[TESTE] ...".

Uso: py -3 automacao/teste_youtube.py <pasta> <arquivo.mp4> [--repetir]
Não lê nem grava o publicados.json: o registro dos vídeos reais e a trava contra duplicado ficam intactos.
O ID do teste vai para testes-youtube.json (na raiz), para você apagar o vídeo depois.
Sem --repetir, recusa enviar de novo um arquivo que já tem teste registrado e não marcado como apagado.
"""
import datetime, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import RAIZ, pasta_rel, sha256
from publicar_youtube import enviar_video, ler, tags_ok, token

TESTES = os.path.join(RAIZ, "testes-youtube.json")
PREFIXO = "[TESTE] "


def ler_testes():
    if not os.path.exists(TESTES):
        return {"_sobre": "Envios de teste ao YouTube (sempre privados). Apague o vídeo no Studio e mude "
                          "'apagado' para true. Este arquivo não interfere no publicados.json.", "testes": []}
    return json.load(open(TESTES, encoding="utf-8"))


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    pasta, mp4 = pasta_rel(sys.argv[1]), os.path.abspath(sys.argv[2])
    if not os.path.exists(mp4):
        sys.exit(f"ERRO: arquivo não encontrado: {mp4}")
    yt = os.path.join(os.path.dirname(mp4), "youtube")
    if not os.path.isdir(yt):
        yt = os.path.join(RAIZ, pasta, "youtube")

    reg = ler_testes()
    h = sha256(mp4)
    vivos = [t for t in reg["testes"] if t["sha256"] == h and not t.get("apagado")]
    if vivos and "--repetir" not in sys.argv:
        sys.exit(f"PARADO: já existe teste deste arquivo ({vivos[-1]['url']}). Apague-o ou use repetir.")

    titulo = (PREFIXO + ler(os.path.join(yt, "titulo.txt")).splitlines()[0])[:100]
    desc = ("Vídeo de TESTE da automação do Quiz Palito. Privado; será apagado.\n\n"
            + ler(os.path.join(yt, "descricao.txt")))[:5000]
    meta = {
        "snippet": {"title": titulo, "description": desc, "tags": tags_ok(ler(os.path.join(yt, "tags.txt"))),
                    "categoryId": "24", "defaultLanguage": "pt-BR", "defaultAudioLanguage": "pt-BR"},
        "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
                   "containsSyntheticMedia": False},
    }
    assert meta["status"]["privacyStatus"] == "private" and titulo.startswith(PREFIXO)
    vid = enviar_video(token(), mp4, meta)

    reg["testes"].append({"pasta": pasta, "id": vid, "url": f"https://youtu.be/{vid}", "titulo": titulo,
                          "privacidade": "private", "data": datetime.datetime.now().isoformat(timespec="seconds"),
                          "sha256": h, "apagado": False})
    with open(TESTES, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"OK teste enviado como PRIVADO: https://youtu.be/{vid}")
    print(f"Apagar depois: https://studio.youtube.com/video/{vid}/edit")


if __name__ == "__main__":
    main()
