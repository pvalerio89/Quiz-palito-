"""Gera itens.json, fotos/ e creditos.json do "Super quiz de futebol mundial" (vídeo 17).

Imagens reaproveitadas do próprio repositório (todas reais e já usadas no canal):
  escudo:<slug>  -> videos/16-alfabeto-times/escudos/<slug>.png (imagem do artigo do clube na Wikipédia)
  band:<código>  -> videos/03-bandeiras-195/bandeiras/<código>.png (ou shorts/qual-joga-1/bandeiras)
  foto:<slug>    -> shorts/qual-joga-1/fotos/<slug>.jpg (Wikimedia Commons, autor e licença em creditos.json)
Uso: py -3 itens.py
"""
import json, os, random
from PIL import Image, ImageDraw, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(HERE))
ESC = os.path.join(RAIZ, "videos", "16-alfabeto-times")
BAND = [os.path.join(RAIZ, "videos", "03-bandeiras-195", "bandeiras"), os.path.join(RAIZ, "shorts", "qual-joga-1", "bandeiras")]
JOG = os.path.join(RAIZ, "shorts", "qual-joga-1")
LADO = 600

PAIS_T, PAIS_J, CRAQUE, ESTADIO, APELIDO, CIDADE = ("DE QUE PAÍS É ESSE TIME?", "DE QUE PAÍS É ESSE CRAQUE?",
    "QUAL CRAQUE É DESSE PAÍS?", "QUAL É O ESTÁDIO DESSE TIME?", "QUAL É O APELIDO DESSE TIME?",
    "EM QUE CIDADE FICA ESSE TIME?")
COPA = "COPA DE {}, AQUI: QUEM GANHOU?"
COMECOU = "EM QUE TIME ELE COMEÇOU?"
# imagem, pergunta, certa, [erradas], resposta falada   (do fácil ao difícil)
P = [
    ("foto:messi", PAIS_J, "Argentina", ["Uruguai", "Espanha"], "Argentina! É o Messi!"),
    ("escudo:barcelona", PAIS_T, "Espanha", ["Itália", "Portugal"], "Espanha! É o Barcelona!"),
    ("band:pt", CRAQUE, "Cristiano Ronaldo", ["Messi", "Neymar"], "Cristiano Ronaldo, de Portugal!"),
    ("escudo:flamengo", ESTADIO, "Maracanã", ["Morumbi", "Mineirão"], "Maracanã!"),
    ("band:qa", COPA.format(2022), "Argentina", ["França", "Croácia"], "Argentina, no Catar!"),
    ("escudo:corinthians", APELIDO, "Timão", ["Verdão", "Peixe"], "Timão!"),
    ("foto:mbappe", PAIS_J, "França", ["Bélgica", "Holanda"], "França! É o Mbappé!"),
    ("escudo:juventus", PAIS_T, "Itália", ["Espanha", "França"], "Itália! É a Juventus!"),
    ("band:ar", CRAQUE, "Maradona", ["Pelé", "Zidane"], "Maradona, da Argentina!"),
    ("escudo:real-madrid", ESTADIO, "Santiago Bernabéu", ["Camp Nou", "Old Trafford"], "Santiago Bernabéu!"),
    ("escudo:boca-juniors", PAIS_T, "Argentina", ["Uruguai", "Chile"], "Argentina! É o Boca Juniors!"),
    ("band:fr", CRAQUE, "Zidane", ["Ronaldinho", "Beckham"], "Zidane, da França!"),
    ("foto:salah", PAIS_J, "Egito", ["Marrocos", "Argélia"], "Egito! É o Salah!"),
    ("escudo:palmeiras", APELIDO, "Verdão", ["Timão", "Tricolor"], "Verdão!"),
    ("band:ru", COPA.format(2018), "França", ["Croácia", "Bélgica"], "França, na Rússia!"),
    ("escudo:liverpool", ESTADIO, "Anfield", ["Old Trafford", "Stamford Bridge"], "Anfield!"),
    ("escudo:bayern-de-munique", PAIS_T, "Alemanha", ["Áustria", "Holanda"], "Alemanha! É o Bayern de Munique!"),
    ("foto:haaland", PAIS_J, "Noruega", ["Suécia", "Dinamarca"], "Noruega! É o Haaland!"),
    ("escudo:santos", ESTADIO, "Vila Belmiro", ["Pacaembu", "São Januário"], "Vila Belmiro!"),
    ("band:za", COPA.format(2010), "Espanha", ["Holanda", "Alemanha"], "Espanha, na África do Sul!"),
    ("escudo:arsenal", APELIDO, "Gunners", ["Reds", "Blues"], "Gunners, os artilheiros!"),
    ("foto:kane", PAIS_J, "Inglaterra", ["Escócia", "País de Gales"], "Inglaterra! É o Harry Kane!"),
    ("escudo:ajax", PAIS_T, "Holanda", ["Bélgica", "Alemanha"], "Holanda! É o Ajax!"),
    ("band:nl", CRAQUE, "Cruyff", ["Beckenbauer", "Puskás"], "Johan Cruyff, da Holanda!"),
    ("escudo:manchester-united", ESTADIO, "Old Trafford", ["Anfield", "Etihad"], "Old Trafford!"),
    ("band:us", COPA.format(1994), "Brasil", ["Itália", "Suécia"], "Brasil, o tetra nos Estados Unidos!"),
    ("escudo:benfica", PAIS_T, "Portugal", ["Espanha", "Brasil"], "Portugal! É o Benfica!"),
    ("escudo:cruzeiro", APELIDO, "Raposa", ["Galo", "Coelho"], "Raposa!"),
    ("foto:son", PAIS_J, "Coreia do Sul", ["Japão", "China"], "Coreia do Sul! É o Son!"),
    ("escudo:chelsea", ESTADIO, "Stamford Bridge", ["Emirates", "Anfield"], "Stamford Bridge!"),
    ("band:de", COPA.format(2006), "Itália", ["França", "Alemanha"], "Itália, na Alemanha!"),
    ("escudo:atletico-mineiro", APELIDO, "Galo", ["Raposa", "Coelho"], "Galo!"),
    ("band:sn", CRAQUE, "Sadio Mané", ["Salah", "Drogba"], "Sadio Mané, do Senegal!"),
    ("escudo:galatasaray", PAIS_T, "Turquia", ["Grécia", "Rússia"], "Turquia! É o Galatasaray!"),
    ("foto:modric", PAIS_J, "Croácia", ["Sérvia", "Bósnia"], "Croácia! É o Modric!"),
    ("escudo:sao-paulo", ESTADIO, "Morumbi", ["Pacaembu", "Maracanã"], "Morumbi!"),
    ("band:kr", COPA.format(2002), "Brasil", ["Alemanha", "Turquia"], "Brasil, o penta na Coreia e no Japão!"),
    ("escudo:atletico-de-madrid", APELIDO, "Colchoneros", ["Merengues", "Culés"], "Colchoneros!"),
    ("escudo:penarol", PAIS_T, "Uruguai", ["Argentina", "Paraguai"], "Uruguai! É o Peñarol!"),
    ("foto:vinicius-jr", COMECOU, "Flamengo", ["Fluminense", "Vasco"], "Flamengo! É o Vini Júnior!"),
    ("band:ci", CRAQUE, "Drogba", ["Eto'o", "Weah"], "Didier Drogba, da Costa do Marfim!"),
    ("escudo:vasco", ESTADIO, "São Januário", ["Engenhão", "Maracanã"], "São Januário!"),
    ("band:mx", COPA.format(1970), "Brasil", ["Itália", "Alemanha"], "Brasil, o tri no México!"),
    ("escudo:celtic", PAIS_T, "Escócia", ["Irlanda", "Inglaterra"], "Escócia! É o Celtic!"),
    ("escudo:inter-de-milao", APELIDO, "Nerazzurri", ["Rossoneri", "Bianconeri"], "Nerazzurri, os azul e preto!"),
    ("foto:lewandowski", PAIS_J, "Polônia", ["República Tcheca", "Ucrânia"], "Polônia! É o Lewandowski!"),
    ("band:se", CRAQUE, "Ibrahimović", ["Haaland", "Eriksen"], "Ibrahimović, da Suécia!"),
    ("escudo:borussia-dortmund", ESTADIO, "Signal Iduna Park", ["Allianz Arena", "Olympiastadion"], "Signal Iduna Park!"),
    ("escudo:psg", PAIS_T, "França", ["Bélgica", "Suíça"], "França! É o PSG!"),
    ("band:it", COPA.format(1990), "Alemanha", ["Argentina", "Itália"], "Alemanha, na Itália!"),
    ("escudo:internacional", ESTADIO, "Beira-Rio", ["Arena do Grêmio", "Couto Pereira"], "Beira-Rio!"),
    ("band:hu", CRAQUE, "Puskás", ["Eusébio", "Cruyff"], "Ferenc Puskás, da Hungria!"),
    ("foto:cristiano-ronaldo", "EM QUE ILHA ELE NASCEU?", "Madeira", ["Açores", "Sicília"], "Ilha da Madeira, em Portugal!"),
    ("escudo:zenit", PAIS_T, "Rússia", ["Ucrânia", "Polônia"], "Rússia! É o Zenit!"),
    ("band:es", COPA.format(1982), "Itália", ["Alemanha", "Brasil"], "Itália, na Espanha!"),
    ("escudo:bahia", APELIDO, "Esquadrão de Aço", ["Leão da Barra", "Vozão"], "Esquadrão de Aço!"),
    ("escudo:milan", ESTADIO, "San Siro", ["Estádio Olímpico", "Allianz Stadium"], "San Siro!"),
    ("band:be", CRAQUE, "De Bruyne", ["Modric", "Kroos"], "Kevin De Bruyne, da Bélgica!"),
    ("escudo:nautico", CIDADE, "Recife", ["Salvador", "Natal"], "Recife!"),
    ("foto:raphinha", COMECOU, "Avaí", ["Figueirense", "Grêmio"], "Avaí, de Florianópolis!"),
    ("band:se", COPA.format(1958), "Brasil", ["Suécia", "França"], "Brasil, o primeiro título, na Suécia!"),
    ("escudo:olimpia", PAIS_T, "Paraguai", ["Bolívia", "Uruguai"], "Paraguai! É o Olimpia!"),
    ("band:cm", CRAQUE, "Eto'o", ["Drogba", "Weah"], "Samuel Eto'o, de Camarões!"),
    ("foto:bellingham", COMECOU, "Birmingham", ["Aston Villa", "Leeds"], "Birmingham City!"),
    ("escudo:dinamo-de-zagreb", PAIS_T, "Croácia", ["Sérvia", "Eslovênia"], "Croácia! É o Dínamo de Zagreb!"),
    ("band:uy", "EM QUE ANO FOI A 1ª COPA, AQUI?", "1930", ["1950", "1924"], "Mil novecentos e trinta, no Uruguai!"),
    ("escudo:juventude", CIDADE, "Caxias do Sul", ["Porto Alegre", "Pelotas"], "Caxias do Sul!"),
    ("band:lr", CRAQUE, "George Weah", ["Eto'o", "Okocha"], "George Weah, da Libéria!"),
    ("foto:haaland", "ELE NASCEU EM QUE PAÍS?", "Inglaterra", ["Noruega", "Alemanha"], "Inglaterra! O Haaland nasceu em Leeds!"),
    ("escudo:estudiantes", CIDADE, "La Plata", ["Buenos Aires", "Córdoba"], "La Plata!"),
    ("band:gb-eng", COPA.format(1966), "Inglaterra", ["Alemanha", "Portugal"], "Inglaterra, em casa!"),
    ("band:ro", CRAQUE, "Hagi", ["Stoichkov", "Nedved"], "Gheorghe Hagi, da Romênia!"),
]
INTRO = ["escudo:gremio", "band:br", "escudo:manchester-city", "escudo:botafogo", "band:jp"]
NOME_JOG = {"messi": "Messi", "mbappe": "Mbappé", "salah": "Salah", "haaland": "Haaland", "kane": "Kane", "son": "Son",
            "modric": "Modric", "vinicius-jr": "Vinícius Jr", "lewandowski": "Lewandowski",
            "cristiano-ronaldo": "Cristiano Ronaldo", "raphinha": "Raphinha", "bellingham": "Bellingham"}


def quadrado(im, fundo=(255, 255, 255)):
    q = Image.new("RGB", (LADO, LADO), fundo)
    q.paste(im, ((LADO - im.width) // 2, (LADO - im.height) // 2), im if im.mode == "RGBA" else None)
    return q


def preparar(spec):
    tipo, k = spec.split(":")
    os.makedirs(os.path.join(HERE, "fotos"), exist_ok=True)
    nome = f"{tipo}-{k}.jpg"
    dst = os.path.join(HERE, "fotos", nome)
    if tipo == "escudo":
        im = Image.open(os.path.join(ESC, "escudos", k + ".png")).convert("RGBA")
        im = im.crop(im.getbbox())
        im.thumbnail((LADO - 110, LADO - 110), Image.LANCZOS)
        out = quadrado(im)
    elif tipo == "band":
        src = next(os.path.join(p, k + ".png") for p in BAND if os.path.exists(os.path.join(p, k + ".png")))
        im = Image.open(src).convert("RGBA")
        im.thumbnail((LADO - 60, LADO - 60), Image.LANCZOS)
        fl = Image.new("RGBA", (im.width + 8, im.height + 8), (60, 60, 80, 255))
        fl.alpha_composite(im, (4, 4))
        out = quadrado(fl, (235, 240, 250))
    else:   # foto vertical de jogador: quadrado puxado para cima (rosto)
        im = Image.open(os.path.join(JOG, "fotos", k + ".jpg")).convert("RGB")
        w, h = im.size
        s = min(w, h)
        top = max(0, min(h - s, int(h * 0.30 - s / 2)))
        out = im.crop(((w - s) // 2, top, (w - s) // 2 + s, top + s)).resize((LADO, LADO), Image.LANCZOS)
    out.save(dst, quality=92)
    return nome


def main():
    rnd = random.Random(17)
    R, usadas = [], set()
    posicoes = [0, 1, 2] * (len(P) // 3 + 1)
    rnd.shuffle(posicoes)
    for n, (spec, perg, certa, err, fala) in enumerate(P, 1):
        ops = list(err)
        pos = posicoes[n - 1]
        ops.insert(pos, certa)
        R.append({"n": n, "img": spec, "foto": preparar(spec), "pergunta": perg, "opcoes": ops, "certa": pos,
                  "fala": fala})
        usadas.add(spec)
    for spec in INTRO:   # imagens da intro rapidinha (não aparecem nas perguntas)
        preparar(spec)
        usadas.add(spec)
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # créditos (tela final): fotos dos jogadores com autor e licença; escudos = marcas dos clubes; bandeiras = PD
    cj = json.load(open(os.path.join(JOG, "creditos.json"), encoding="utf-8"))
    ce = json.load(open(os.path.join(ESC, "creditos.json"), encoding="utf-8"))
    por_arq = {v["arquivo"]: (k, v) for k, v in ce.items()}
    cred = {"fotos": [], "escudos": []}
    for spec in sorted(usadas):
        tipo, k = spec.split(":")
        if tipo == "foto":
            c = cj[NOME_JOG[k]]
            cred["fotos"].append(f"{NOME_JOG[k]}: {c['artist']} ({c['lic']}), {c['title']}")
        elif tipo == "escudo":
            nome, c = por_arq[k + ".png"]
            cred["escudos"].append(f"{nome}: {c['file']}")
    json.dump(cred, open(os.path.join(HERE, "creditos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(R), "perguntas; posição da certa:", Counter(r["certa"] for r in R))


if __name__ == "__main__":
    main()
