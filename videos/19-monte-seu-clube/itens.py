"""Gera etapas.json, fotos/ e creditos.json do "Monte o seu clube" (vídeo 19).

Vídeo de ESCOLHA (sem resposta certa): o espectador monta o próprio clube etapa por etapa (cidade, camisa, escudo,
estádio, mascote, técnico, os 11 titulares e um banco de lendas). Em cada etapa 6 opções com foto real.
Fotos: escudos/<slug>.png = imagem da caixa de informações do artigo da Wikipédia (fotos_wiki.py escudos, licença em
creditos.json); fotos/<slug>.jpg baixadas com fotos_wiki.py baixar; cidades e bichos reaproveitados dos vídeos 13 e 14;
escudos dos clubes do vídeo 16.
Uso: py -3 itens.py
"""
import json, os, re, unicodedata
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(HERE)
LADO = 420

# etapa: (chave, título na tela, subtítulo, fala, [(nome na tela, origem)])
#   origem: "p:Nome" (pessoas.tsv/escolhas.json deste vídeo), "obj:Nome" (vídeo 14), "bicho:Nome" (vídeo 13),
#           "esc:slug" (escudo do vídeo 16), "camisa:Nome" (recorte do peito na foto da pessoa)
P = lambda *ns: [(n, "p:" + n) for n in ns]
ETAPAS = [
    ("cidade", "A CIDADE DO SEU CLUBE", "ONDE ELE VAI NASCER?", "Primeiro: em que cidade nasce o seu clube?",
     [("Rio de Janeiro", "obj:Cristo Redentor"), ("Londres", "obj:Big Ben"), ("Barcelona", "obj:Sagrada Família"),
      ("Paris", "obj:Torre Eiffel"), ("Roma", "obj:Coliseu"), ("Nova York", "obj:Estátua da Liberdade")]),
    ("camisa", "A COR DA CAMISA", "QUAL VAI SER O UNIFORME?", "Agora a cor da camisa!",
     [("Amarela", "camisa:Marquinhos"), ("Celeste e branca", "camisa:Messi"), ("Laranja", "camisa:Van Dijk"),
      ("Azul", "camisa:Koundé"), ("Vermelha", "camisa:Rodri"), ("Branca", "camisa:Bellingham")]),
    ("escudo", "O ESTILO DO ESCUDO", "SE INSPIRA EM QUAL?", "O escudo! Vai se inspirar em qual?",
     [("Tipo Flamengo", "esc:flamengo"), ("Tipo Corinthians", "esc:corinthians"), ("Tipo Palmeiras", "esc:palmeiras"),
      ("Tipo Real Madrid", "esc:real-madrid"), ("Tipo Barcelona", "esc:barcelona"), ("Tipo Juventus", "esc:juventus")]),
    ("estadio", "O ESTÁDIO", "ONDE O SEU TIME JOGA?", "Onde o seu time vai jogar?", P("Maracanã", "Camp Nou", "Bernabéu",
     "Old Trafford", "Allianz Arena", "La Bombonera")),
    ("mascote", "O MASCOTE", "QUAL BICHO REPRESENTA?", "E o mascote do clube?",
     [("Urubu", "p:Urubu"), ("Porco", "bicho:Porco"), ("Raposa", "bicho:Raposa"), ("Leão", "bicho:Leão"),
      ("Águia", "bicho:Águia"), ("Tigre", "bicho:Tigre")]),
    ("tecnico", "O TÉCNICO", "QUEM COMANDA O TIME?", "Quem vai ser o técnico?", P("Pep Guardiola", "Carlo Ancelotti",
     "Jürgen Klopp", "José Mourinho", "Abel Ferreira", "Luis Enrique")),
    ("gol", "O GOLEIRO", "QUEM FECHA O GOL?", "Agora o time titular! O goleiro!", P("Alisson", "Ederson", "Courtois",
     "Neuer", "Donnarumma", "Dibu Martínez")),
    ("ld", "O LATERAL DIREITO", "QUEM CORRE PELA DIREITA?", "Lateral direito!", P("Hakimi", "Alexander-Arnold",
     "Carvajal", "Koundé", "Reece James", "Kyle Walker")),
    ("zag1", "O 1º ZAGUEIRO", "O XERIFE DA DEFESA!", "O primeiro zagueiro, o xerife!", P("Van Dijk", "Marquinhos",
     "Rúben Dias", "Rüdiger", "Saliba", "Militão")),
    ("zag2", "O 2º ZAGUEIRO", "QUEM FAZ DUPLA COM ELE?", "Agora a dupla de zaga!", P("Gabriel Magalhães", "Gvardiol",
     "Ronald Araújo", "Lisandro Martínez", "Bastoni", "Cubarsí")),
    ("le", "O LATERAL ESQUERDO", "QUEM CORRE PELA ESQUERDA?", "Lateral esquerdo!", P("Alphonso Davies",
     "Theo Hernández", "Nuno Mendes", "Grimaldo", "Robertson", "Ferland Mendy")),
    ("vol", "O VOLANTE", "QUEM PROTEGE A DEFESA?", "O volante!", P("Rodri", "Casemiro", "Declan Rice",
     "Bruno Guimarães", "Kimmich", "Tchouaméni")),
    ("mei", "O MEIA", "QUEM ARMA AS JOGADAS?", "O meia que arma o jogo!", P("De Bruyne", "Modrić", "Pedri",
     "Bellingham", "Ødegaard", "Valverde")),
    ("dez", "O CAMISA 10", "O CRAQUE DO TIME!", "O camisa dez, o craque!", P("Messi", "Bruno Fernandes", "Wirtz",
     "Musiala", "Cole Palmer", "Paquetá")),
    ("pd", "O PONTA DIREITA", "DRIBLE PELA DIREITA!", "Ponta direita!", P("Salah", "Lamine Yamal", "Saka", "Raphinha",
     "Rodrygo", "Dembélé")),
    ("pe", "O PONTA ESQUERDA", "DRIBLE PELA ESQUERDA!", "Ponta esquerda!", P("Vinícius Jr.", "Neymar",
     "Kvaratskhelia", "Rafael Leão", "Luis Díaz", "Son")),
    ("ca", "O CENTROAVANTE", "QUEM FAZ OS GOLS?", "E o centroavante, o homem gol!", P("Haaland", "Harry Kane",
     "Mbappé", "Cristiano Ronaldo", "Lewandowski", "Lautaro")),
    ("joia", "A JOIA DA BASE", "UM BRASILEIRO PROMESSA!", "Agora o banco! Primeiro, uma joia brasileira!",
     P("Endrick", "Estêvão", "Martinelli", "João Pedro", "Savinho", "Vitor Roque")),
    ("lgol", "GOLEIRO LENDA", "PARA O BANCO DE LENDAS!", "Um goleiro lenda!", P("Buffon", "Casillas", "Taffarel",
     "Rogério Ceni", "Oliver Kahn", "Petr Čech")),
    ("llat", "LATERAL LENDA", "PARA O BANCO DE LENDAS!", "Um lateral lenda!", P("Cafu", "Roberto Carlos", "Marcelo",
     "Daniel Alves", "Lahm", "Zanetti")),
    ("lzag", "ZAGUEIRO LENDA", "PARA O BANCO DE LENDAS!", "Um zagueiro lenda!", P("Maldini", "Puyol", "Lúcio",
     "Cannavaro", "Thiago Silva", "Beckenbauer")),
    ("lmei", "MEIO-CAMPO LENDA", "PARA O BANCO DE LENDAS!", "Um meio-campo lenda!", P("Xavi", "Iniesta", "Pirlo",
     "Gerrard", "Lampard", "Kaká")),
    ("ldez", "CAMISA 10 LENDA", "PARA O BANCO DE LENDAS!", "Um camisa dez lendário!", P("Pelé", "Maradona", "Zico",
     "Zidane", "Ronaldinho", "Cruyff")),
    ("lca", "ATACANTE LENDA", "O ÚLTIMO DO BANCO!", "E o último: um atacante lenda!", P("Ronaldo Fenômeno", "Romário",
     "Henry", "Ibrahimović", "Eto'o", "Rooney")),
]
ORIG = {"obj": "14-tudo-amarelo", "bicho": "13-animal-pela-foto"}


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


ZOOM = {"Xavi": (0.45, 0.3, 0.55), "Zico": (0.47, 0.55, 0.62), "Luis Enrique": (0.6, 0.18, 0.45)}  # cx, cy, lado


def quadrado(im, cy=0.5, fr=1.0, cx=0.5):
    """Recorte quadrado: em foto em pé, mais para cima (rosto)."""
    w, h = im.size
    s = min(w, h) * fr
    x0 = min(max(w * cx - s / 2, 0), w - s)
    y0 = min(max(h * cy - s / 2, 0), h - s)
    return im.crop((int(x0), int(y0), int(x0 + s), int(y0 + s))).resize((LADO, LADO), Image.LANCZOS)


def main():
    cred_aqui = json.load(open(os.path.join(HERE, "creditos.json"), encoding="utf-8"))
    os.makedirs(os.path.join(HERE, "fotos"), exist_ok=True)
    out, cred, escudos = [], [], []
    for chave, tit, sub, fala, ops in ETAPAS:
        lst = []
        for nome, org in ops:
            tipo, k = org.split(":", 1)
            arq = f"{chave}-{slug(nome)}.jpg"
            dst = os.path.join(HERE, "fotos", arq)
            if tipo in ("p", "camisa"):
                c = cred_aqui[k]
                src = os.path.join(HERE, "escudos" if c["arquivo"].endswith(".png") else "fotos", c["arquivo"])
                im = Image.open(src).convert("RGBA")
                if im.getchannel("A").getbbox():
                    im = im.crop(im.getchannel("A").getbbox())
                fundo = Image.new("RGBA", im.size, (255, 255, 255, 255))
                fundo.alpha_composite(im)
                im = fundo.convert("RGB")
                if tipo == "camisa":
                    im = quadrado(im, 0.62, 0.62)
                elif k in ZOOM:
                    im = quadrado(im, ZOOM[k][1], ZOOM[k][2], ZOOM[k][0])
                else:
                    im = quadrado(im, 0.3 if im.height > im.width * 1.05 else 0.5)
                im.save(dst, quality=88)
                linha = f"{k}: {c['autor'] or 'Wikimedia Commons'} ({c['lic']}), {c['file'].replace('_', ' ')}"
            elif tipo == "esc":
                c = json.load(open(os.path.join(VID, "16-alfabeto-times", "creditos.json"), encoding="utf-8"))
                c = next(v for v in c.values() if v["arquivo"] == k + ".png")
                e = Image.open(os.path.join(VID, "16-alfabeto-times", "escudos", k + ".png")).convert("RGBA")
                e = e.crop(e.getbbox())
                e.thumbnail((LADO - 60, LADO - 60), Image.LANCZOS)
                q = Image.new("RGBA", (LADO, LADO), (255, 255, 255, 255))
                q.alpha_composite(e, ((LADO - e.width) // 2, (LADO - e.height) // 2))
                q.convert("RGB").save(dst, quality=90)
                linha = None
                escudos.append(c["file"].replace("_", " "))
            else:
                c = json.load(open(os.path.join(VID, ORIG[tipo], "creditos.json"), encoding="utf-8"))[k]
                Image.open(os.path.join(VID, ORIG[tipo], "fotos", c["arquivo"])).convert("RGB").resize(
                    (LADO, LADO), Image.LANCZOS).save(dst, quality=88)
                linha = f"{k}: {c['autor']} ({c['lic']}), {c['file'].replace('_', ' ')}"
            if linha and linha not in cred:
                cred.append(linha)
            lst.append({"nome": nome, "foto": arq})
        out.append({"chave": chave, "titulo": tit, "sub": sub, "fala": fala, "opcoes": lst})
    json.dump(out, open(os.path.join(HERE, "etapas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"fotos": cred, "escudos": escudos}, open(os.path.join(HERE, "creditos-tela.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(len(out), "etapas,", len(cred), "créditos")


if __name__ == "__main__":
    main()
