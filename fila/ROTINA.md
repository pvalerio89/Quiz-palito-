# Rotina diária do Claude: produzir o próximo vídeo da fila

Roda sozinha 3 vezes por dia (4h43, 9h43 e 18h43) (tarefa agendada no claude.ai). O Patrick **não aprova nada**: ele autorizou
(2026-11-06) publicar direto como público e apaga do YouTube se algo sair errado. Não pergunte, não espere.
Responda tudo em português do Brasil. Siga o `CLAUDE.md` e a memória do projeto.

São **2 envios por dia, em horários diferentes** (Patrick, 2026-11-17): o **vídeo longo às 18h00** e o **Short às 20h30**
de Brasília (pico do canal no Studio: 18h–21h todo dia). O workflow **Publicar do dia** agenda o 1º item `pronto`
(longo no horário de `HORARIOS`, Short `SHORT_DEPOIS` mais tarde, em `automacao/fila.py`). Esta rotina só deixa itens prontos.
(Antes, de 13/11 a 17/11, eram 3 longos + 3 Shorts por dia, e os vídeos novos pararam de ser distribuídos: ver "NOVO RITMO".)

## NOVO RITMO (análise do Studio, 2026-11-17 — vale mais que as regras antigas abaixo)

**Série DESAFIO DO PALITO** (Shorts de palitos de fósforo: `shorts/palito_base.py`, exemplos `shorts/palito-1..5`): um enigma
por Short ("mova 1 palito" / "tire 1 palito" / "tem 2 respostas"), 20 a 35 s. O build confere sozinho a resposta. Quando
os 5 primeiros saírem, compare as views do feed com os Shorts de tema; se ganharem, continue a série (palito-6 em diante,
contas novas, fundo variado) como Short dos próximos itens.

Desde 11/11 os vídeos novos quase não são mostrados (Shorts com 6–86 views; antes 900–1.800). Hipótese: muitos
vídeos por dia no mesmo molde ("produzido em massa"). Análise completa: doc "Quiz Palito: análise do canal e o que
copiar" (https://claude.ai/artifact/HpiLhDUBrcT8wjDEp8iUGJ). Regras:
- **Short de 30 a 50 s**, 4 ou 5 perguntas, e a **1ª imagem já é a pergunta** (sem abertura). O campeão (6 Bandeiras) tem 53 s.
- **Nunca "Só 1% acerta"** (nem no título, nem na tela, nem no TikTok). Títulos de desafio e VARIADOS, ex.:
  "Se você acertar 20 de 30…", "Fácil, médio, difícil e impossível", "As últimas são as mais difíceis",
  "Nenhum adulto passa…", "Pais contra filhos…", "Ninguém acerta a letra W", "O vídeo acaba quando você errar".
- **Cada vídeo com cara própria:** varie cor de fundo, ordem das telas, tipo de pergunta e frases. Dois vídeos
  seguidos não podem parecer o mesmo molde com outro tema.
- **Pensado para a TV** (61% do tempo assistido é na TV, família no sofá): letras grandes, placar na tela, 10 a 15 min.
- A regra "mais de 8 min por causa do anúncio" só vale depois da monetização (canal com 81/500 inscritos):
  a duração é escolhida pela retenção.
- **Google Flow (Patrick, 2026-11-17: "use o Flow para melhorar os vídeos"):** além da miniatura, grave em
  `youtube/prompt-flow-cena.txt` um prompt de **uma cena de abertura** do tema com o Palito (16:9; Short 9:16 se
  houver), no mesmo estilo da miniatura. A tarefa das miniaturas (`fila/MINIATURAS-FLOW.md`) gera no Flow pelo
  Chrome do PC e grava `abertura.jpg` na pasta do vídeo. No build do longo, passe
  `abertura=os.path.join(PASTA, "abertura.jpg")` para `op.intro_rapida(...)`: se a imagem existir, vira o fundo da intro
  (zoom lento); se ainda não existir, sai o fundo de sempre. Como o vídeo é gerado de novo na hora de publicar, a cena
  entra se ficar pronta antes do horário.

## Passos

1. Atualize `main` (`git fetch origin main && git checkout -B <sua branch> origin/main`).
2. **Novos links:** cada linha não comentada de `fila/novos.txt` vira um item no fim de `fila/fila.json`
   (`id` = `AAAA-MM-DD-tema-curto`, `referencia` = link, `tema` = o comentário do Patrick, `status` = `aguardando`).
   Depois deixe só o cabeçalho com `#` no `novos.txt`.
3. **Erros:** se algum item está `erro`, abra o último "Publicar do dia" (GitHub Actions) e conserte a causa.
   Se consertou, volte o item para `pronto` (o envio pula o que já foi publicado). Se não der, deixe `erro`
   com a explicação em `obs` e siga para o próximo.
4. **Estoque:** se já há 4 ou mais itens `pronto` (4 dias), pare aqui (só grave os passos 2 e 3).
5. **Repetido ou parecido:** antes de produzir, compare o item com tudo que já existe (`publicados.json`,
   pastas em `videos/` e `shorts/`, e os outros itens da fila). Se o tema/formato for **igual ou parecido**
   (ex.: outro "adivinhe a bandeira", mesmo assunto com outro nome), **não produza**: marque `status` = `parecido`,
   escreva em `obs` com qual vídeo ele se parece, avise o Patrick (ver "Avisos") e siga para o próximo item.
   Se já produziu e só percebeu depois, avise do mesmo jeito.
6. **Produzir** o 1º item `aguardando` (um por rodada; se o estoque estiver em 0 ou 1, faça mais um):
   - Item que já tem `short` preenchido (série **Desafio do Palito**, `shorts/palito-N`, 2026-11-17): faça **só o vídeo longo**;
     não crie Short do tema e não mexa no `short` do item.
   - Item `esperando` = falta o Patrick explicar algo (ver `obs`): **pule**. Item com `"so_short": true` = faça só o Short
     (sem vídeo longo; no item só `short`, `titulo` do Short e `status` = `pronto`).
   - Veja a referência leve: título pelo oembed, storyboard/miniaturas com `yt-dlp` (`-f sb0`), sem baixar o vídeo.
   - Faça a **versão Quiz Palito**: mesmo formato e ritmo, **perguntas próprias**, sem copiar arte, marca ou texto
     do outro canal, **sem parte de explicação/fonte**. Temas escolares/educativos para adolescentes quando der.
   - **Layout aprovado (Patrick, 2026-11-09): `videos/modelo-opcoes/opcoes.py`.** Toda pergunta do vídeo longo é
     QUESTÃO com 3 alternativas A/B/C (igual aos Shorts): foto à esquerda, alternativas animadas, Palito à direita,
     fundo com movimento, **efeitos sonoros** (`make_sfx` + `sons_pergunta`) e **transição** entre perguntas
     (`transicao_frames`). Em **algumas** perguntas (umas 1 a cada 5, quando houver clipe bom) troque a foto por um
     **vídeo curto** (`q["clipe"]`): ache .webm/.ogv nos artigos da Wikipédia, confira a licença (PD/CC0/CC BY de
     preferência) e baixe com `automacao/fotos_wiki.py clipes` pelo workflow "Fotos Wikimedia" (crédito vai na tela final).
     Alternativas erradas plausíveis e do mesmo tipo; a certa em posição variada. Exemplo completo: `previa.py` (`video()`).
     Só se o tema não couber em alternativas, use o modelo mais recente de `videos/`.
   - **ESTILO MAIS HUMANO (Patrick, 2026-11-13; vale para todo vídeo longo novo): `videos/modelo-opcoes/humano.py`**
     (amostra aprovada: `videos/amostra-humano/build_amostra.py`). Monte cada pergunta com `hu.pergunta(...)` em vez
     de chamar `pergunta_frames`/`resposta_frames` direto. Ele achou o formato antigo "muito robótico". Regras:
     - **Falas variadas:** nada de "Pergunta cinco!" em toda pergunta. Varie a entrada ("Agora uma do Nordeste...",
       "Bora pra Europa...", "Cuidado, que essa tem pegadinha!", "Essa aqui derruba muita gente.") e reaja de verdade
       na resposta ("Caiu na pegadinha, hein?", "Se acertou essa, você é fera!").
     - **Ritmo variado:** as 2 ou 3 primeiras fáceis e rápidas (contagem 4 a 5 s); depois 7 s.
     - Em umas **1 a cada 6** perguntas: **DICA** no meio da contagem (`q["dica"] = (voz, TEXTO, 2.5)`);
       **AVISO** na faixa do topo (`q["aviso"] = "TEM PEGADINHA!"`) quando a pergunta for pegadinha/difícil;
       **SUSPENSE** antes de revelar (`q["suspense"] = voz "A resposta é..."`) nas mais difíceis;
       **"VOCÊ SABIA?"** de 1 frase curta (`q["sabia"]`, a fala da resposta conta a mesma curiosidade).
     - **PEDIDO DE CURTIDA** uma vez, depois da 2ª ou 3ª resposta: `hu.curtir(tl, sfx, voz_pede, voz_espero)`.
       O narrador pede o coraçãozinho/curtida, tem uma pausa curta e fala "Eu espero!" (variar as duas frases, ex.:
       "Ei, antes da próxima... deixa o coraçãozinho e curte o vídeo aí!" / "Eu espero!" ou "Tô esperando, hein!").
     - **ÚLTIMA PERGUNTA:** antes dela, `hu.ultima(tl, sfx, voz)` (tela vermelha + coração) com a fala
       "Atenção... essa é a última pergunta! E é a mais difícil!" (variar); a pergunta tem `q["final"] = True`.
     - **FIM só com "se inscreva no canal":** `hu.inscreva(tl, sfx, voz)` com fala curta ("Gostou do quiz? Então se
       inscreve no canal!"), **sem** tela de nota/níveis. Depois só a tela de créditos das fotos, se houver.
     - **O Palito NÃO fala** (sem voz e sem balão de fala): o Patrick não gostou.
   - **Abertura RAPIDINHA (Patrick, 2026-11-10), no longo e no Short:** intro de 2 a 3 s (selo, nome do tema,
     3 a 5 imagens do tema que NÃO estão nas perguntas, Palito acenando) com só a saudação curta + o tema falados
     (`op.intro_rapida(...)` no longo, `s.intro_rapida(...)` no Short; fala "intro" de no máximo ~3 s, variar a
     saudação). Depois transição e a 1ª pergunta, com a chamada numa faixa vermelha por cima (`gancho=...` no
     longo; `CHAMADA` + "VALENDO!" no Short). Exemplos: `videos/16-alfabeto-times`, `shorts/times-1`.
     Placar na tela: bolinhas "CONTA SEUS PONTOS!"/"PONTOS:" + selo "+1 SE ACERTOU!" em cada resposta;
     no fim do longo só "INSCREVA-SE" (ver ESTILO MAIS HUMANO). Pasta nova `videos/NN-tema` (próximo número) e `shorts/tema-1`.
   - **O QUE SEGURA O PÚBLICO (Analytics do canal, 2026-11-12 — vale mais que o resto desta lista; detalhes em
     `estatisticas/analise-2026-11-12.md`):**
     - **Longo: ritmo de ~18 a 25 s por pergunta, com a PERGUNTA FALADA.** Os 3 melhores (Países sem vogais 46%,
       Estados 42%, Quiz do Brasil 41% assistido) falam a pergunta (no Brasil também as alternativas), dão 6 a 10 s
       de contagem e a resposta vem com uma reação curta ("É o Japão! Começou bem?"). Os "metralhadora" de 3 a 4 s
       com 60 a 100 itens (Tudo amarelo 12%, Fruta pela foto 17%, Logo 19%, Bandeiras 195 29%) perdem o público.
       No `opcoes.py`: gere `q{n}` falado em TODA pergunta (com entrada variada, ver ESTILO MAIS HUMANO; as
       alternativas faladas quando forem curtas), `COUNT` = 7 s e a fala da resposta com reação/curiosidade de
       1 frase (sem "explicação/fonte" longa).
     - **Longo: 10 a 13 minutos**, uns **30 a 40 perguntas** (não "o máximo que couber"). Os de 20 min caíram para
       10–19% no fim. Continua valendo: nunca abaixo de 8:10.
     - **Temas que seguram:** geografia, Brasil, matéria de escola (português, matemática, inglês), bandeiras,
       futebol com alternativas. Evitar tema "solto" (tudo de uma cor, logos, frutas em 3 s, conhecimentos gerais
       muito longos).
     - **Primeiro minuto:** todo longo perde 25–50% nos primeiros 5%. A 1ª pergunta tem que ser fácil e
       aparecer já (intro rapidinha), e a fala do gancho diz quantas perguntas são e que fica difícil no fim.
     - **Short: 30 a 50 s, 4 ou 5 perguntas** (2026-11-17; antes 45–60 s), contagem 3 a 5 s, pergunta falada. O mais curto
       (Bandeiras, 53 s) segurou mais. **Fala final de no máximo ~2 s** ("Comenta sua nota!"): hoje quase todos
       perdem 30–40 pontos no último quarto e terminam com 4–15%, por causa da tela final longa.
       1ª pergunta fácil (Estados, Logos e Times perderam ~25% logo nos primeiros 10%).
   - **Vídeo longo com MAIS DE 8 MINUTOS** (vale de novo depois da monetização; hoje a retenção manda, ver NOVO RITMO) (regra do Patrick, 2026-11-09: a partir de 8 min o YouTube deixa pôr
     anúncios no meio). Mire em **10 a 13 min** com **30 a 40 perguntas** no ritmo acima (não enrole com telas paradas). Depois de montar, confira a duração (`tempos.json` → `final` + fim ≥ 500 s, ou `ffprobe`); se
     ficar abaixo de 8:10, acrescente perguntas e monte de novo. Placar a cada 10 perguntas.
   - **Imagens reais quando o tema for de coisas reais** (frutas, legumes, animais, comidas, lugares, objetos,
     monumentos...): fotos de verdade, nunca emoji. Use `automacao/fotos_wiki.py` (Wikimedia Commons pelo artigo
     da Wikipédia; na nuvem o download dá 429, então use o workflow "Fotos Wikimedia": escreva os argumentos em
     `automacao/fotos-pedido.txt`, dê push na sua branch e espere o commit dele): prefira **domínio público/CC0**, depois **CC BY**; CC BY-SA só se não houver outra boa. Olhe a
     prancha de candidatas e escolha foto nítida, com o item inteiro e fácil de reconhecer. Créditos (autor +
     licença) só numa **tela curta no fim do vídeo** (modelo: `videos/12-fruta-fotos-reais`), nunca na descrição nem em comentário. Emoji/ícone só para
     temas abstratos (palavras, cores, sentimentos) ou bandeiras/logos (bandeiras SVG, simple-icons CC0).
   - Item sem `referencia` (tema próprio): produza direto pelo `tema`/`obs`, seguindo "O QUE SEGURA O PÚBLICO".
   - **Miniatura pelo Google Flow (Patrick, 2026-11-12):** além da miniatura por código (reserva), grave em
     `youtube/prompt-flow.txt` um prompt pronto para o Google Flow (Palito, boneco de palito, enorme em pânico;
     título grande; elementos do tema gigantes; fundo colorido com raios; faixa "VOCÊ CONSEGUE?"). Não precisa
     mandar ao Patrick: a rotina de hora em hora (`fila/MINIATURAS-FLOW.md`) gera no Flow assim que o PC ligar e troca.
   - Vídeo longo com kit completo em `youtube/`: título, descrição, tags e **miniatura** (título emocional grande,
     elementos recortados gigantes, **fundo colorido com raios**, Palito enorme em pânico, faixa "VOCÊ CONSEGUE?").
   - Short 9:16 com movimento: **copie o modelo `shorts/modelo/`** (sem abertura, placar, 3 opções), 6 perguntas do mesmo tema. Use as mesmas fotos reais do vídeo longo
     quando ele tiver fotos. **Frase de chamada variada** (nunca "Só 1% acerta"). Escolha uma frase de
     `CHAMADAS` em `shorts/short_base.py` (função `chamada()`) diferente das usadas nos últimos 3 Shorts
     (veja os títulos em `publicados.json`); "Só 1% acerta" não se usa mais (2026-11-17).
     A mesma frase vai na tela de abertura, no título e no `tiktok.txt`. Na descrição (YouTube):
     link do canal (https://www.youtube.com/channel/UCerGMTooT9vl4yVgW7Ggd3A) e o texto `LINK_DO_VIDEO_LONGO` no lugar do link do vídeo
     longo (o workflow troca pelo link certo na hora de publicar).
     **`tiktok.txt` (Patrick, 2026-11-14): NUNCA link nem menção ao YouTube** (o TikTok entrega menos).
     Formato: gancho (frase de chamada) / pedir para comentar a nota + marcar um amigo /
     "Segue o @quizpalitos pra quiz novo todo dia!" / hashtags `#quiz #quiztime #fyp #paravoce` + 2 do tema.
     Exemplo: `shorts/bandeiras-estados-1/youtube/tiktok.txt`.
   - **Abertura falada variada** (pedido do Patrick, 2026-11-09): não comece todo vídeo com "Fala, pessoal! Bem-vindos
     a mais um Quiz Palito!". Veja o `INTRO` dos últimos vídeos (`videos/*/gerar_vozes.py`) e use outra frase de entrada,
     ligada ao tema (ex.: "Ei, você aí! Será que conhece mesmo os bichos?", "Atenção, que hoje o desafio é diferente:",
     "Prepara o cérebro:", "Bora testar seu olho?", "Desafio rápido:", "Chegou mais um Quiz Palito!").
   - **Vídeo de anotar/escolher** (monte o seu clube, escolha 1 de cada, etc.; Patrick, 2026-11-12): logo no começo,
     antes da 1ª etapa, a fala chama para **clicar no coração e abrir os comentários para ir anotando; assim que
     terminar o vídeo, é só enviar**. Use `engaja.chamada_anotar(usadas=...)` (`videos/modelo-opcoes/engaja.py`),
     variando a frase em relação ao último vídeo desse tipo. Vale também para o Short (versão curta da frase).
   - Voz: Edge TTS pt-BR-AntonioNeural rate +20% pitch +2Hz. Música só do `musicas/` com o crédito de 1 linha.
   - Script de montagem precisa chamar `build_*.py` (o `automacao/gerar.py` acha sozinho).
   - **Confira** a prévia (`py automacao/gerar.py <pasta> --previa`, com as fontes substitutas descritas na memória):
     olhe a prancha, textos cortados, respostas certas, nenhuma pergunta repetida. Não precisa mostrar a ninguém.
   - No item: `video`, `short`, `titulo`, `status` = `pronto`.
7. **Gravar:** commit (autor `pvalerio89 <294259185+pvalerio89@users.noreply.github.com>`), push da sua branch, abra PR para `main`
   e faça o merge você mesmo (squash). Sem `.mp4` no Git.
8. Se a fila não tem `aguardando` nem `pronto`, não faça nada além dos passos 2 e 3.

## Avisos ao Patrick (sempre, na mensagem final)

Estes avisos valem **mesmo quando o pedido diz para terminar em silêncio**. Escreva-os no começo da mensagem final:

- **Faltando links:** como sai 1 item por dia, se depois do seu trabalho sobrar **3 ou menos** itens `aguardando`
  na fila, escreva: "⚠️ Só faltam N criações na fila: mande mais links de referência." (diga quantos `pronto` há.)
- **Repetido/parecido:** para cada item marcado `parecido`, escreva qual link e com qual vídeo do canal ele se parece.

## Nunca

- Publicar fora do workflow, mexer em vídeos já publicados ou apagar algo no YouTube.
- Trocar Secrets, workflows de autorização ou o `publicados.json` à mão (só o workflow grava IDs).
