# Automação do Quiz Palito (GitHub Actions)

O render na nuvem usa os mesmos scripts do PC. Nenhum script de vídeo foi trocado.

## Fluxo de um vídeo novo

1. **Gerar vídeo** (aba Actions, modo `previa`): confira a prancha no artefato.
2. **Gerar vídeo** (modo `completo`): gera o mp4 + kit e guarda na Release `video-<pasta>`.
3. **Enviar ao YouTube** (padrão `publico`): sobe o vídeo da Release já público e grava o ID no `publicados.json`.
   Com `privado`, sobe só para você ver; depois publique no Studio e rode **Marcar publicado** (youtube, publicado).
4. **TikTok** (Shorts): o Claude abre a Release no navegador, baixa o mp4 e posta no TikTok Studio
   com a legenda das notas da Release (`youtube/tiktok.txt`). Depois rode **Marcar publicado** (tiktok, com o ID).

## Registro `publicados.json`

Um status por plataforma: `pendente`, `privado_teste`, `publicado`, `nao_se_aplica`.
O envio para se o vídeo já está como `publicado` ou `privado_teste`, ou se o mesmo arquivo já foi enviado.
Para trocar um ID gravado de propósito: `py -3 automacao/marcar_publicado.py <pasta> <plataforma> --id X --corrigir`.

## Secrets (GitHub > Settings > Secrets and variables > Actions)

| Secret | Para quê |
| --- | --- |
| `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` | Envio ao YouTube. Gerados por `automacao/autorizar_youtube.py` no PC, uma vez. |
| `GEMINI_API_KEY` | Só para refazer vozes dos vídeos 01 e 02. |

## Rodar no PC

`py -3 automacao/gerar.py shorts/brasil-1 --previa` faz o mesmo que a nuvem e põe o resultado em `saida/`.
