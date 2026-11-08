# Rotina diária do Claude: produzir o próximo vídeo da fila

Roda sozinha todo dia de madrugada (4h43) (tarefa agendada no claude.ai). O Patrick **não aprova nada**: ele autorizou
(2026-11-06) publicar direto como público e apaga do YouTube se algo sair errado. Não pergunte, não espere.
Responda tudo em português do Brasil. Siga o `CLAUDE.md` e a memória do projeto.

O workflow **Publicar do dia** (9h07 de Brasília, no ar antes do meio-dia) publica o 1º item `pronto`. Esta rotina só deixa itens prontos.

## Passos

1. Atualize `main` (`git fetch origin main && git checkout -B <sua branch> origin/main`).
2. **Novos links:** cada linha não comentada de `fila/novos.txt` vira um item no fim de `fila/fila.json`
   (`id` = `AAAA-MM-DD-tema-curto`, `referencia` = link, `tema` = o comentário do Patrick, `status` = `aguardando`).
   Depois deixe só o cabeçalho com `#` no `novos.txt`.
3. **Erros:** se algum item está `erro`, abra o último "Publicar do dia" (GitHub Actions) e conserte a causa.
   Se consertou, volte o item para `pronto` (o envio pula o que já foi publicado). Se não der, deixe `erro`
   com a explicação em `obs` e siga para o próximo.
4. **Estoque:** se já há 2 ou mais itens `pronto`, pare aqui (só grave os passos 2 e 3).
5. **Repetido ou parecido:** antes de produzir, compare o item com tudo que já existe (`publicados.json`,
   pastas em `videos/` e `shorts/`, e os outros itens da fila). Se o tema/formato for **igual ou parecido**
   (ex.: outro "adivinhe a bandeira", mesmo assunto com outro nome), **não produza**: marque `status` = `parecido`,
   escreva em `obs` com qual vídeo ele se parece, avise o Patrick (ver "Avisos") e siga para o próximo item.
   Se já produziu e só percebeu depois, avise do mesmo jeito.
6. **Produzir** o 1º item `aguardando` (um por dia; se sobrar tempo e o estoque estiver 0, faça mais um):
   - Veja a referência leve: título pelo oembed, storyboard/miniaturas com `yt-dlp` (`-f sb0`), sem baixar o vídeo.
   - Faça a **versão Quiz Palito**: mesmo formato e ritmo, **perguntas próprias**, sem copiar arte, marca ou texto
     do outro canal, **sem parte de explicação/fonte**. Temas escolares/educativos para adolescentes quando der.
   - Use o modelo de vídeo mais novo do repositório (o mais recente em `videos/`; estilo em `videos/modelo-cartao/`
     se existir). Pasta nova `videos/NN-tema` (próximo número) e `shorts/tema-1`.
   - Vídeo longo com kit completo em `youtube/`: título, descrição, tags e **miniatura** (título emocional grande,
     elementos recortados gigantes, **fundo colorido com raios**, Palito enorme em pânico, faixa "VOCÊ CONSEGUE?").
   - Short 9:16 com movimento (`shorts/short_base.py`), 6 perguntas do mesmo tema. Na descrição e no `tiktok.txt`:
     link do canal (https://www.youtube.com/channel/UCerGMTooT9vl4yVgW7Ggd3A) e o texto `LINK_DO_VIDEO_LONGO` no lugar do link do vídeo
     longo (o workflow troca pelo link certo na hora de publicar).
   - Fotos/logos de terceiros: prefira emojis, bandeiras ou ícones livres (simple-icons CC0); nada de créditos.
   - Voz: Edge TTS pt-BR-AntonioNeural rate +20% pitch +2Hz. Música só do `musicas/` com o crédito de 1 linha.
   - Script de montagem precisa chamar `build_*.py` (o `automacao/gerar.py` acha sozinho).
   - **Confira** a prévia (`py automacao/gerar.py <pasta> --previa`, com as fontes substitutas descritas na memória):
     olhe a prancha, textos cortados, respostas certas, nenhuma pergunta repetida. Não precisa mostrar a ninguém.
   - No item: `video`, `short`, `titulo`, `status` = `pronto`.
7. **Gravar:** commit (autor `Quiz Palito <quizpalito@gmail.com>`), push da sua branch, abra PR para `main`
   e faça o merge você mesmo (squash). Sem `.mp4` no Git.
8. Se a fila não tem `aguardando` nem `pronto`, não faça nada além dos passos 2 e 3.

## Avisos ao Patrick (sempre, na mensagem final)

Estes avisos valem **mesmo quando o pedido diz para terminar em silêncio**. Escreva-os no começo da mensagem final:

- **Faltando links:** se depois do seu trabalho sobrar **1 ou 0** itens `aguardando` na fila, escreva:
  "⚠️ Só falta 1 criação na fila (ou nenhuma): mande mais links de referência." (diga quantos `pronto` há.)
- **Repetido/parecido:** para cada item marcado `parecido`, escreva qual link e com qual vídeo do canal ele se parece.

## Nunca

- Publicar fora do workflow, mexer em vídeos já publicados ou apagar algo no YouTube.
- Trocar Secrets, workflows de autorização ou o `publicados.json` à mão (só o workflow grava IDs).
