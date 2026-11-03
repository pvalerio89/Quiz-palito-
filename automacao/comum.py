"""Funções usadas pelos scripts de automação (GitHub Actions e PC).

O registro `publicados.json` (na raiz) guarda o status de cada vídeo em cada plataforma.
"""
import hashlib, json, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRO = os.path.join(RAIZ, "publicados.json")
PLATAFORMAS = ("youtube", "tiktok")
BLOQUEIA = ("publicado", "privado_teste")  # status que impedem um novo envio


def pasta_rel(pasta):
    """Normaliza 'videos\\06-quiz-brasil/' -> 'videos/06-quiz-brasil' e confere se existe."""
    p = os.path.relpath(os.path.abspath(os.path.join(RAIZ, pasta)), RAIZ).replace("\\", "/").strip("/")
    if p.startswith("..") or not os.path.isdir(os.path.join(RAIZ, p)):
        sys.exit(f"ERRO: pasta não encontrada no projeto: {pasta}")
    return p


def slug(pasta):
    return pasta_rel(pasta).replace("/", "-")


def ler_registro():
    with open(REGISTRO, encoding="utf-8") as f:
        return json.load(f)


def salvar_registro(doc):
    with open(REGISTRO, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")


def status(doc, pasta, plataforma):
    return doc["videos"].get(pasta, {}).get(plataforma, {"status": "pendente"})


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def checar_duplicado(doc, pasta, plataforma, arquivo=None):
    """Para com erro se este vídeo já foi enviado para a plataforma."""
    st = status(doc, pasta, plataforma)
    if st.get("status") in BLOQUEIA:
        sys.exit(f"PARADO: {pasta} já está como '{st['status']}' no {plataforma} "
                 f"(id {st.get('id')}). Nada foi enviado.")
    if arquivo:
        h = sha256(arquivo)
        for p, e in doc["videos"].items():
            if e.get(plataforma, {}).get("sha256") == h:
                sys.exit(f"PARADO: este mesmo arquivo já foi enviado ao {plataforma} como {p}. Nada foi enviado.")
        return h
    return None


def marcar(doc, pasta, plataforma, **campos):
    e = doc["videos"].setdefault(pasta, {})
    if "titulo" not in e:
        t = os.path.join(RAIZ, pasta, "youtube", "titulo.txt")
        if os.path.exists(t):
            e["titulo"] = open(t, encoding="utf-8").readline().strip()
    e.setdefault("youtube", {"status": "pendente"})
    e.setdefault("tiktok", {"status": "pendente"})
    e[plataforma] = {k: v for k, v in campos.items() if v is not None}
    return e[plataforma]
