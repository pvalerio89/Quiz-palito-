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
- Vídeo longo: sempre **mais de 8 min** (anúncio no meio); mirar **10–15 min** (Patrick 2026-11-20), 30–40 perguntas, ~20 s por pergunta com a pergunta falada (dados de retenção 2026-11-12, ver `fila/ROTINA.md`). Short: 30–50 s (2026-11-17), fala final curta. Ritmo (2026-11-27): 1 longo 18h + 1 Short 20h30 **dia sim, dia não**; sem mais vídeos de escola; regras novas em `fila/ROTINA.md` "PLANO DE MONETIZAÇÃO" (longo + Short do mesmo tema, Shorts campeões em parte 2, variar formato) e "NOVO RITMO".
- Tema de coisas reais (frutas, animais, comidas, lugares): **fotos reais** de licença livre (`automacao/fotos_wiki.py`, Wikimedia; preferir domínio público/CC0). Créditos só numa tela curta no fim do vídeo, nunca em comentário/descrição.
- Shorts: **todo longo sai com o Short DELE** (tirado do próprio longo; `shorts/do_longo.py`); Desafio do Palito só extra ocasional, nunca no lugar do Short do tema (Patrick 2026-11-22). Variar cartão, cor, música e frase de chamada (`s.chamada(s.usadas_recentes())` em `shorts/short_base.py`); nunca "Só 1% acerta" (2026-11-17).
- Postar: **Chrome do perfil Quiz** (Claude in Chrome, deviceId `b745beaa-97ae-48fe-9320-d5797ce2f42d`; nunca o perfil Patrick `878f2588…`), aba na frente, conferir canal Quiz Palito. Subir com `file_upload`. Esperar verificações do YouTube antes de Publicar. TikTok: legenda só com clique real + teclado (nunca editar por JS).
- Economizar o plano: ler páginas por texto (não screenshot), /watch leve, não repetir ações falhas — perguntar ao usuário.
