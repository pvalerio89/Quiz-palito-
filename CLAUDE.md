# Quiz Palito — contexto do projeto

Canal de quiz em português no **YouTube** (Quiz Palito, ID `UCerGMTooT9vl4yVgW7Ggd3A`) e **TikTok** (@quizpalitos). Mascote: **Palito**, boneco de palito (`personagem/`). Todo vídeo tem o Palito + selo "QUIZ PALITO". Responder sempre em português do Brasil, curto e simples.

## Pastas
- `videos/01..05` — vídeos longos 16:9. Base comum: `videos/01-paises-sem-vogais/build.py` (fontes, cores, Palito, selo, sons, Timeline). Modelo mais novo: `videos/04-doce-ou-salgado/` (build + gerar_vozes + gerar_kit).
- `shorts/` — Shorts 9:16 (`short_base.py`; modelo atual `shorts/portugues-1/`). Padrão **com movimento** (um arquivo serve YouTube Shorts e TikTok).
- `canal/` — banner, foto, kit de publicação. `musicas/` — Kevin MacLeod (CC BY 4.0, 1 linha de crédito).
- `envios/` — cópias ≤10 MB para subir pelo Chrome. `comentarios/` — respostas sugeridas da checagem diária.
- `COMO-PEDIR.md` — pedidos prontos do usuário.

## Regras principais
- Python: `py -3` (não `python`, não `-I`). Voz: Edge TTS **pt-BR-AntonioNeural rate +20% pitch +2Hz**.
- Prévia (prancha) antes de renderizar; depois conferir quadros e volume (~−26 dB). Não guardar em cache imagens de tamanho variável (estoura RAM).
- Miniatura: título emocional grande, elementos recortados gigantes, fundo P&B com raios, **Palito enorme em pânico**, faixa "VOCÊ CONSEGUE?".
- Fotos de terceiros: o usuário não quer créditos em comentário/descrição — preferir emojis/bandeiras; perguntar antes.
- Postar: **Chrome do perfil Quiz** (Claude in Chrome, deviceId `b745beaa-97ae-48fe-9320-d5797ce2f42d`; nunca o perfil Patrick `878f2588…`), aba na frente, conferir canal Quiz Palito. Subir com `file_upload`. Esperar verificações do YouTube antes de Publicar. TikTok: legenda só com clique real + teclado (nunca editar por JS).
- Economizar o plano: ler páginas por texto (não screenshot), /watch leve, não repetir ações falhas — perguntar ao usuário.
