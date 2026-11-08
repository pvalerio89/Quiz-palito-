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
   Redirect URI do Login Kit: `https://github.com/quizpalito/quiz-palito`.
2. Secrets: `TIKTOK_CLIENT_KEY` e `TIKTOK_CLIENT_SECRET` (da página do app).
3. Rode **Autorizar TikTok** sem nada: o resumo mostra o link. Abra, autorize, copie o endereço da página onde caiu
   e rode de novo colando no campo. O resumo mostra o valor do Secret `TIKTOK_REFRESH_TOKEN` (vale 1 ano).
   Depois apague essa execução.
4. Peça a auditoria do app (Content Posting API) para os vídeos saírem públicos.

## Registro `publicados.json`

Um status por plataforma: `pendente`, `privado_teste`, `publicado`, `nao_se_aplica`.
O envio para se o vídeo já está como `publicado` ou `privado_teste`, ou se o mesmo arquivo já foi enviado.
Para trocar um ID gravado de propósito: `py -3 automacao/marcar_publicado.py <pasta> <plataforma> --id X --corrigir`.

## Secrets (GitHub > Settings > Secrets and variables > Actions)

| Secret | Para quê |
| --- | --- |
| `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` | Envio ao YouTube. Gerados por `automacao/autorizar_youtube.py` no PC, uma vez. |
| `GEMINI_API_KEY` | Só para refazer vozes dos vídeos 01 e 02. |
| `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, `TIKTOK_REFRESH_TOKEN` | Envio ao TikTok (veja "TikTok: configurar uma vez"). |
| `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, `TIKTOK_REFRESH_TOKEN` | Envio ao TikTok (veja "TikTok: configurar uma vez"). |

## Rodar no PC

`py -3 automacao/gerar.py shorts/brasil-1 --previa` faz o mesmo que a nuvem e põe o resultado em `saida/`.
