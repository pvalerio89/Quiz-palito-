# Rotina diária do Claude: produzir o próximo vídeo da fila

Roda sozinha 3 vezes por dia (4h43, 9h43 e 18h43) (tarefa agendada no claude.ai). O Patrick **não aprova nada**: ele autorizou
(2026-11-06) publicar direto como público e apaga do YouTube se algo sair errado. Não pergunte, não espere.
Responda tudo em português do Brasil. Siga o `CLAUDE.md` e a memória do projeto.

São **3 vídeos por dia** (longo + Short cada; desde 2026-11-13): o workflow **Publicar do dia** agenda o 1º item `pronto` no próximo horário livre (12h09, 17h30 ou 20h30 de Brasília). Esta rotina só deixa itens prontos.

## Passos

1. Atualize `main` (`git fetch origin main && git checkout -B <sua branch> origin/main`).
2. **Novos links:** cada linha não comentada de `fila/novos.txt` vira um item no fim de `fila/fila.json`
   (`id` = `AAAA-MM-DD-tema-curto`, `referencia` = link, `tema` = o comentário do Patrick, `status` = `aguardando`).
   Depois deixe só o cabeçalho com `#` no `novos.txt`.
3. **Erros:** se algum item está `erro`, abra o último "Publicar do dia" (GitHub Actions) e conserte a causa.
   Se consertou, volte o item para `pronto` (o envio pula o que já foi publicado). Se não der, deixe `erro`
   com a explicação em `obs` e siga para o próximo.
4. **Estoque:** se já há 6 ou mais itens `pronto` (2 dias), pare aqui (só grave os passos 2 e 3).
5. **Repetido ou parecido:** antes de produzir, compare o item com tudo que já existe (`publicados.json`,
   pastas em `videos/` e `shorts/`, e os outros itens da fila). Se o tema/formato for **igual ou parecido**
   (ex.: outro "adivinhe a bandeira", mesmo assunto com outro nome), **não produza**: marque `status` = `parecido`,
   escreva em `obs` com qual vídeo ele se parece, avise o Patrick (ver "Avisos") e siga para o próximo item.
   Se já produziu e só percebeu depois, avise do mesmo jeito.
6. **Produzir** o 1º item `aguardando` (um por rodada; se o estoque estiver em 0, 1 ou 2, faça mais um):
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
   - **Abertura RAPIDINHA (Patrick, 2026-11-10), no longo e no Short:** intro de 2 a 3 s (selo, nome do tema,
     3 a 5 imagens do tema que NÃO estão nas perguntas, Palito acenando) com só a saudação curta + o tema falados
     (`op.intro_rapida(...)` no longo, `s.intro_rapida(...)` no Short; fala "intro" de no máximo ~3 s, variar a
     saudação). Depois transição e a 1ª pergunta, com a chamada numa faixa vermelha por cima (`gancho=...` no
     longo; `CHAMADA` + "VALENDO!" no Short). Exemplos: `videos/16-alfabeto-times`, `shorts/times-1`.
     Placar na tela: bolinhas "CONTA SEUS PONTOS!"/"PONTOS:" + selo "+1 SE ACERTOU!" em cada resposta;
     no fim, "__ / N" e "PAUSA E COMENTA SUA NOTA!". Pasta nova `videos/NN-tema` (próximo número) e `shorts/tema-1`.
   - **O QUE SEGURA O PÚBLICO (Analytics do canal, 2026-11-12 — vale mais que o resto desta lista; detalhes em
     `estatisticas/analise-2026-11-12.md`):**
     - **Longo: ritmo de ~18 a 25 s por pergunta, com a PERGUNTA FALADA.** Os 3 melhores (Países sem vogais 46%,
       Estados 42%, Quiz do Brasil 41% assistido) falam a pergunta (no Brasil também as alternativas), dão 6 a 10 s
       de contagem e a resposta vem com uma reação curta ("É o Japão! Começou bem?"). Os "metralhadora" de 3 a 4 s
       com 60 a 100 itens (Tudo amarelo 12%, Fruta pela foto 17%, Logo 19%, Bandeiras 195 29%) perdem o público.
       No `opcoes.py`: gere `q{n}` falado em TODA pergunta ("Pergunta cinco! Qual é a capital da Bahia?"; as
       alternativas faladas quando forem curtas), `COUNT` = 7 s e a fala da resposta com reação/curiosidade de
       1 frase (sem "explicação/fonte" longa).
     - **Longo: 10 a 13 minutos**, uns **30 a 40 perguntas** (não "o máximo que couber"). Os de 20 min caíram para
       10–19% no fim. Continua valendo: nunca abaixo de 8:10.
     - **Temas que seguram:** geografia, Brasil, matéria de escola (português, matemática, inglês), bandeiras,
       futebol com alternativas. Evitar tema "solto" (tudo de uma cor, logos, frutas em 3 s, conhecimentos gerais
       muito longos).
     - **Primeiro minuto:** todo longo perde 25–50% nos primeiros 5%. A 1ª pergunta tem que ser fácil e
       aparecer já (intro rapidinha), e a fala do gancho diz quantas perguntas são e que fica difícil no fim.
     - **Short: 45 a 60 s, 5 ou 6 perguntas**, contagem 3 a 5 s, pergunta falada (já é assim). O mais curto
       (Bandeiras, 53 s) segurou mais. **Fala final de no máximo ~2 s** ("Comenta sua nota!"): hoje quase todos
       perdem 30–40 pontos no último quarto e terminam com 4–15%, por causa da tela final longa.
       1ª pergunta fácil (Estados, Logos e Times perderam ~25% logo nos primeiros 10%).
   - **Vídeo longo com MAIS DE 8 MINUTOS** (regra do Patrick, 2026-11-09: a partir de 8 min o YouTube deixa pôr
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
     quando ele tiver fotos. **Frase de chamada variada:** não use sempre "Só 1% acerta". Escolha uma frase de
     `CHAMADAS` em `shorts/short_base.py` (função `chamada()`) diferente das usadas nos últimos 3 Shorts
     (veja os títulos em `publicados.json`); "Só 1% acerta" pode aparecer de vez em quando, nunca em 2 seguidos.
     A mesma frase vai na tela de abertura, no título e no `tiktok.txt`. Na descrição e no `tiktok.txt`:
     link do canal (https://www.youtube.com/channel/UCerGMTooT9vl4yVgW7Ggd3A) e o texto `LINK_DO_VIDEO_LONGO` no lugar do link do vídeo
     longo (o workflow troca pelo link certo na hora de publicar).
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

- **Faltando links:** como saem 3 vídeos por dia, se depois do seu trabalho sobrar **3 ou menos** itens `aguardando`
  na fila, escreva: "⚠️ Só faltam N criações na fila: mande mais links de referência." (diga quantos `pronto` há.)
- **Repetido/parecido:** para cada item marcado `parecido`, escreva qual link e com qual vídeo do canal ele se parece.

## Nunca

- Publicar fora do workflow, mexer em vídeos já publicados ou apagar algo no YouTube.
- Trocar Secrets, workflows de autorização ou o `publicados.json` à mão (só o workflow grava IDs).
