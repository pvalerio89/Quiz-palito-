# Automação do Quiz Palito (GitHub Actions)

O render na nuvem usa os mesmos scripts do PC. Nenhum script de vídeo foi trocado.

## Fluxo de um vídeo novo

1. **Gerar vídeo** (aba Actions, modo `previa`): confira a prancha no artefato.
2. **Gerar vídeo** (modo `completo`): gera o mp4 + kit e guarda na Release `video-<pasta>`.
3. **Enviar ao YouTube** (padrão `publico`): sobe o vídeo da Release já público e grava o ID no `publicados.json`.
   Com `privado`, sobe só para você ver; depois publique no Studio e rode **Marcar publicado** (youtube, publicado).
4. **Enviar ao TikTok** (Shorts): posta pela API oficial o mp4 da Release com a legenda `youtube/tiktok.txt`
   e grava o ID no `publicados.json`. Enquanto o app do TikTok não passar na auditoria, sai como "somente eu".

## TikTok: configurar uma vez

1. Em developers.tiktok.com, entre com a conta @quizpalitos e crie um app (tipo Web).
   Produtos: **Login Kit** e **Content Posting API** (ligue **Direct Post**). Escopos: `user.info.basic`, `video.publish`.
   Redirect URI do Login Kit: `https://pvalerio89.github.io/quizpalito.github.io/tiktok.html`.
   Termos: `https://pvalerio89.github.io/quizpalito.github.io/termos.html` ; Privacidade: `https://pvalerio89.github.io/quizpalito.github.io/privacidade.html` (site no repo pvalerio89/quizpalito.github.io, GitHub Pages).
   No Sandbox, adicione a conta @quizpalitos como usuário de teste (Target users).
2. Variable (aba Variables) `TIKTOK_CLIENT_KEY` e Secret `TIKTOK_CLIENT_SECRET` (da página do app).
   A chave vai como Variable porque o GitHub esconde Secrets no resumo e o link de login sairia com `***`.
3. Rode **Autorizar TikTok** sem nada: o resumo mostra o link. Abra, autorize; a página do Quiz Palito abre com o botão **Copiar**.
   Rode de novo colando no campo. O resumo mostra o valor do Secret `TIKTOK_REFRESH_TOKEN` (vale 1 ano).
   Depois apague essa execução.
4. Peça a auditoria do app (Content Posting API) para os vídeos saírem públicos.

## 1 vídeo por dia, sozinho (fila)

- **Lista do Patrick:** links de referência em `fila/novos.txt` (um por linha) ou mandados no chat do projeto.
- **Rotina do Claude** (tarefa agendada no claude.ai, todo dia 4h43): segue `fila/ROTINA.md`. Passa os links para
  `fila/fila.json`, produz o próximo vídeo longo + Short (perguntas próprias, prévia conferida), marca `pronto`
  e faz o merge em `main` sozinha. Mantém até 2 itens prontos de estoque.
- **Publicar do dia** (workflow, todo dia 9h07 de Brasília, ou à mão em Actions): pega o 1º `pronto`, gera os dois,
  sobe o vídeo longo **público**, depois o Short **público** com o link do longo na descrição, e marca `publicado`.
  Se falhar, marca `erro` e no dia seguinte a rotina conserta. Sem item pronto, não faz nada.
- **TikTok:** o mp4 do Short fica na Release `video-shorts-<nome>` com a legenda pronta nas notas (postar pelo celular).
- **Parar tudo:** Actions > Publicar do dia > "Disable workflow" (e pausar a tarefa agendada no claude.ai).
- Ver a fila: `py -3 automacao/fila.py status`.

## Comentários do YouTube

- **Autorizar YouTube** (uma vez): libera ler e responder comentários (o token antigo só envia vídeos).
  Rode sem nada, abra o link do resumo, entre com a conta do Quiz Palito e aceite. A última página não abre
  (127.0.0.1): copie o endereço inteiro e rode de novo colando no campo. Troque o Secret `YT_REFRESH_TOKEN`
  pelo valor do resumo e apague a execução.
- **Comentários do YouTube**: lê todos os vídeos e grava `comentarios/pendentes.md` (sem resposta do canal).
  Com `RESPONDER`, publica antes as respostas aprovadas de `comentarios/respostas.json`
  (`[{"id": "...", "resposta": "..."}]`); nunca responde o mesmo comentário duas vezes (`respondidos.json`).
- Curtir/coração não existe na API do YouTube: só pelo app YouTube Studio.
- Vídeos fora do `publicados.json` entram em `comentarios/videos-extras.txt`.

## Registro `publicados.json`

Um status por plataforma: `pendente`, `privado_teste`, `publicado`, `nao_se_aplica`.
O envio para se o vídeo já está como `publicado` ou `privado_teste`, ou se o mesmo arquivo já foi enviado.
Para trocar um ID gravado de propósito: `py -3 automacao/marcar_publicado.py <pasta> <plataforma> --id X --corrigir`.

## Secrets (GitHub > Settings > Secrets and variables > Actions)

`YT_CLIENT_ID` e `TIKTOK_CLIENT_KEY` são identificadores públicos: cadastre na aba **Variables** (se ficarem como Secret, o link de login sai com `***`).

| Secret | Para quê |
| --- | --- |
| `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` (e a Variable `YT_CLIENT_ID`) | Envio ao YouTube e comentários. Refresh token novo pelo workflow **Autorizar YouTube**. |
| `GEMINI_API_KEY` | Só para refazer vozes dos vídeos 01 e 02. |
| `TIKTOK_CLIENT_SECRET`, `TIKTOK_REFRESH_TOKEN` (e a Variable `TIKTOK_CLIENT_KEY`) | Envio ao TikTok (veja "TikTok: configurar uma vez"). |

## Rodar no PC

`py -3 automacao/gerar.py shorts/brasil-1 --previa` faz o mesmo que a nuvem e põe o resultado em `saida/`.
