# Miniaturas pelo Google Flow (rotina de hora em hora)

Regra do Patrick (2026-11-13): **assim que o PC ligar, trocar a miniatura** dos vídeos novos pela do Google Flow.
A miniatura por código continua sendo feita pela rotina diária e sobe junto com o vídeo (reserva).

## Passo a passo
1. `python3 automacao/miniaturas_pendentes.py`. Se não imprimir nada: **pare aqui, sem mandar mensagem.**
2. Chrome: `list_connected_browsers`. Se nenhum navegador do PC (DESKTOP-S3UCD3C, Windows) estiver conectado:
   **pare aqui, sem mandar mensagem** (o PC está desligado; a próxima hora tenta de novo).
   Use o perfil pessoal do Patrick (`878f2588…`) **só para o Flow** (ele autorizou em 2026-11-13; o Flow está
   logado em p.valerio89). Se o perfil Quiz (`b745beaa…`) estiver conectado, pode usar ele se o Flow estiver logado lá.
3. Abra uma aba nova em https://flow.google.com → "Novo projeto". Configurações do agente (ícone de ajustes):
   16:9, x2, Nano Banana 2.1, "Nunca" pedir confirmação → Salvar.
4. Para cada pasta pendente, mande no chat do Flow o texto de `<pasta>/youtube/prompt-flow.txt`, começando com
   "Gere uma miniatura de YouTube 16:9 bem chamativa, que dá vontade de clicar:" e reforçando no fim:
   "À direita, ENORME (metade da altura da imagem), o Palito: boneco de palito (stickman) branco com contorno preto
   grosso, cabeça redonda, olhos arregalados, boca aberta em PÂNICO, as duas mãos na cabeça."
   Espere ~40 s e confira por screenshot: tem que ter o Palito grande, o título certo escrito sem erro e
   "VOCÊ CONSEGUE?". Se faltar algo, peça a correção no mesmo chat (no máximo 2 tentativas).
4b. **Cena de abertura** (2026-11-17, só quando a linha do passo 1 diz `cena`): no mesmo projeto, mande o texto de
   `<pasta>/youtube/prompt-flow-cena.txt` começando com "Gere uma cena 16:9 colorida, sem nenhum texto escrito:" e
   reforçando o Palito (mesmo desenho do passo 4, mas animado/feliz, não em pânico). Confira que não tem texto nem
   logo de outra marca. Baixe do mesmo jeito do passo 5 e grave como `<pasta>/abertura.jpg` (JPG 1920x1080, PIL
   `ImageOps.fit`, quality 88). O build usa sozinho como fundo da intro (`op.intro_rapida(..., abertura=...)`).
5. Baixe a melhor por JavaScript na aba do Flow (as `<img>` de 1376x768 cujo `alt` começa pelo prompt):
   `fetch(img.src)` → blob → `<a download="flow-<nome-da-pasta>.webp">` → click.
   O Chrome salva em `C:\Users\pvale\OneDrive\Desktop\Videos de IA\QuizPalito\zapi-img`.
   (Devolver a imagem em base64 pelo javascript_tool é bloqueado; não tente.)
6. `device_stage_files` desse arquivo → converta para JPG 1280x720 (PIL, quality 90, < 2 MB).
   Em `<pasta>/youtube/`: `git mv thumbnail.jpg thumbnail-codigo.jpg` e grave a nova como `thumbnail.jpg`.
7. Commit + push na branch da sessão, PR e merge no main (squash). Depois, para as pastas com status
   `publicado` (já subiram), rode o workflow **Trocar miniatura** com `pastas` = essas pastas e confira o log
   ("OK ... miniatura trocada"). Pastas `pronto` não precisam: o Publicar do dia já sobe com a nova.
8. Feche a aba que abriu. Mande ao Patrick 1 mensagem curta: quais vídeos ganharam miniatura do Flow (com link).
   Se algo falhar (Flow sem crédito, download não apareceu, workflow vermelho), avise na hora o que falhou.
