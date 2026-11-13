"""Gera itens.json, fotos/ e creditos.json do "Adivinhe o jogador pela foto" (vídeo 21).

Perguntas próprias: 38 craques (e 5 técnicos) do fácil ao difícil, foto real que começa com zoom e desfoque e vai
abrindo na contagem. Fotos reaproveitadas do vídeo 19 (Wikimedia Commons, licença livre; créditos na tela final).
Nenhuma resposta repete jogador do vídeo 02 (jogadores de A a Z).
Uso: py -3 itens.py
"""
import html, json, os, random, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(HERE)
ORIG = os.path.join(VID, "19-monte-seu-clube")
J, T = "QUEM É ESSE JOGADOR?", "QUEM É ESSE TÉCNICO?"
# pergunta, nome (em creditos do vídeo 19), arquivo em 19/fotos, certa (tela), [erradas], resposta falada
P = [
    (J, "Ronaldo Fenômeno", "lca-ronaldo-fenomeno.jpg", "Ronaldo", ["Romário", "Adriano"], "É o Fenômeno! Começou fácil, né?"),
    (J, "Roberto Carlos", "llat-roberto-carlos.jpg", "Roberto Carlos", ["Cafu", "Roque Júnior"], "Roberto Carlos, o rei da bomba!"),
    (J, "Raphinha", "pd-raphinha.jpg", "Raphinha", ["Antony", "Richarlison"], "É o Raphinha!"),
    (J, "Marcelo", "llat-marcelo.jpg", "Marcelo", ["Filipe Luís", "Alex Sandro"], "Marcelo! Esse cabelo não engana!"),
    (T, "Carlo Ancelotti", "tecnico-carlo-ancelotti.jpg", "Ancelotti", ["Tite", "Felipão"], "Ancelotti, o técnico da Seleção!"),
    (J, "Marquinhos", "zag1-marquinhos.jpg", "Marquinhos", ["Militão", "Gabriel"], "É o Marquinhos!"),
    (J, "Rodrygo", "pd-rodrygo.jpg", "Rodrygo", ["Vinícius Jr.", "Endrick"], "Rodrygo, do Real Madrid!"),
    (J, "Buffon", "lgol-buffon.jpg", "Buffon", ["Pirlo", "Totti"], "Buffon, lenda do gol da Itália!"),
    (J, "Daniel Alves", "llat-daniel-alves.jpg", "Daniel Alves", ["Maicon", "Cafu"], "É o Daniel Alves!"),
    (J, "Son", "pe-son.jpg", "Son", ["Kagawa", "Mitoma"], "É o Son, da Coreia do Sul!"),
    (T, "Pep Guardiola", "tecnico-pep-guardiola.jpg", "Guardiola", ["Luis Enrique", "Xabi Alonso"], "Pep Guardiola!"),
    (J, "Rogério Ceni", "lgol-rogerio-ceni.jpg", "Rogério Ceni", ["Marcos", "Dida"], "Rogério Ceni, o goleiro artilheiro!"),
    (J, "De Bruyne", "mei-de-bruyne.jpg", "De Bruyne", ["Hazard", "Haaland"], "Kevin De Bruyne!"),
    (J, "Courtois", "gol-courtois.jpg", "Courtois", ["De Gea", "Oblak"], "Courtois, o paredão da Bélgica!"),
    (J, "Paquetá", "dez-paqueta.jpg", "Paquetá", ["Coutinho", "Gerson"], "Lucas Paquetá!"),
    (J, "Neuer", "gol-neuer.jpg", "Neuer", ["Ter Stegen", "Oliver Kahn"], "Manuel Neuer!"),
    (J, "Bruno Guimarães", "vol-bruno-guimaraes.jpg", "Bruno Guimarães", ["Casemiro", "Fabinho"], "Bruno Guimarães!"),
    (T, "Jürgen Klopp", "tecnico-jurgen-klopp.jpg", "Klopp", ["Tuchel", "Simeone"], "Jürgen Klopp, com o boné de sempre!"),
    (J, "Lautaro", "ca-lautaro.jpg", "Lautaro", ["Julián Álvarez", "Di María"], "Lautaro Martínez!"),
    (J, "Rooney", "lca-rooney.jpg", "Rooney", ["Beckham", "Gerrard"], "Wayne Rooney!"),
    (J, "Ederson", "gol-ederson.jpg", "Ederson", ["Alisson", "Weverton"], "É o Ederson!"),
    (J, "Casillas", "lgol-casillas.jpg", "Casillas", ["Víctor Valdés", "Pepe Reina"], "Iker Casillas!"),
    (J, "Hakimi", "ld-hakimi.jpg", "Hakimi", ["Mazraoui", "Ziyech"], "Hakimi, do Marrocos!"),
    (T, "José Mourinho", "tecnico-jose-mourinho.jpg", "Mourinho", ["Jorge Jesus", "Conte"], "José Mourinho, o Special One!"),
    (J, "Rafael Leão", "pe-rafael-leao.jpg", "Rafael Leão", ["João Félix", "Nuno Mendes"], "Rafael Leão!"),
    (J, "Maldini", "lzag-maldini.jpg", "Maldini", ["Nesta", "Cannavaro"], "Paolo Maldini, lenda do Milan!"),
    (J, "Kimmich", "vol-kimmich.jpg", "Kimmich", ["Müller", "Goretzka"], "Joshua Kimmich!"),
    (J, "Puyol", "lzag-puyol.jpg", "Puyol", ["Sergio Ramos", "Piqué"], "Puyol! Esse cabelo é inconfundível!"),
    (J, "Saka", "pd-saka.jpg", "Saka", ["Rashford", "Sterling"], "Bukayo Saka!"),
    (J, "Estêvão", "joia-estevao.jpg", "Estêvão", ["Savinho", "Luiz Henrique"], "Estêvão, o Messinho!"),
    (J, "Rodri", "vol-rodri.jpg", "Rodri", ["Busquets", "Koke"], "Rodri, melhor do mundo em 2024!"),
    (T, "Abel Ferreira", "tecnico-abel-ferreira.jpg", "Abel Ferreira", ["Jorge Jesus", "Renato Gaúcho"], "Abel Ferreira, do Palmeiras!"),
    (J, "Ødegaard", "mei-degaard.jpg", "Ødegaard", ["Eriksen", "Haaland"], "Martin Ødegaard!"),
    (J, "Cole Palmer", "dez-cole-palmer.jpg", "Cole Palmer", ["Phil Foden", "Mason Mount"], "Cole Palmer!"),
    (J, "Musiala", "dez-musiala.jpg", "Musiala", ["Sané", "Gnabry"], "Jamal Musiala!"),
    (J, "Kvaratskhelia", "pe-kvaratskhelia.jpg", "Kvaratskhelia", ["Dzeko", "Vlahović"], "Kvaratskhelia! Esse nome é difícil até de falar!"),
    (J, "Lahm", "llat-lahm.jpg", "Philipp Lahm", ["Schweinsteiger", "Özil"], "Philipp Lahm, campeão do mundo em 2014!"),
    (J, "Cruyff", "ldez-cruyff.jpg", "Cruyff", ["Beckenbauer", "Van Basten"], "Johan Cruyff, a lenda da Holanda!"),
]
INTRO = [("Maracanã", "maracana.jpg"), ("Camp Nou", "estadio-camp-nou.jpg"), ("Bernabéu", "estadio-bernabeu.jpg"),
         ("Allianz Arena", "allianz-arena.jpg")]


def main():
    rnd = random.Random(21)
    cred19 = json.load(open(os.path.join(ORIG, "creditos.json"), encoding="utf-8"))
    os.makedirs(os.path.join(HERE, "fotos"), exist_ok=True)
    pos = [0, 1, 2] * 13
    rnd.shuffle(pos)
    R, cred = [], {}
    for n, (perg, nome, arq, certa, err, fala) in enumerate(P, 1):
        c = cred19[nome]
        shutil.copy(os.path.join(ORIG, "fotos", arq), os.path.join(HERE, "fotos", arq))
        cred[nome] = {**c, "arquivo": arq, "autor": html.unescape(c["autor"]).replace("\xa0", " ").strip()}
        ops = list(err)
        ops.insert(pos[n - 1], certa)
        assert len(set(ops)) == 3, (n, ops)
        R.append({"n": n, "pergunta": perg, "nome": nome, "foto": arq, "opcoes": ops, "certa": pos[n - 1],
                  "fala": fala})
    for nome, arq in INTRO:   # fotos só da intro rapidinha (não aparecem nas perguntas)
        shutil.copy(os.path.join(ORIG, "fotos", arq), os.path.join(HERE, "fotos", arq))
        cred[nome] = {**cred19[nome], "arquivo": arq}
    assert len({r["nome"] for r in R}) == len(R)
    json.dump(R, open(os.path.join(HERE, "itens.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(cred, open(os.path.join(HERE, "creditos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(R), "perguntas,", len(cred), "fotos")


if __name__ == "__main__":
    main()
