# AP-940 — notas do mapa de votos

Mapa: `AP-940.psv` (15 linhas). Elaborado em 27/09/2026 por subagente (claude-opus-5-5), conforme `PROMPT_MAPA.md`.

Julgamento em sessão virtual (25/03 a 01/04/2022), unânime. Três ministros têm peça própria: Gilmar Mendes (Relator, p6-36), Ricardo Lewandowski (Revisor, p37-52) e Alexandre de Moraes (p53-71). No banco, os três aparecem como `lido`. Os outros 8 ministros (`deduzido` no banco) não têm peça e só são contados na ata (p72).

## (a) OCR
Acórdão eletrônico, com camada de texto nativa. Não há problema de OCR. Cada página traz no cabeçalho o rótulo da peça ("Voto - MIN. GILMAR MENDES", "Voto Vogal", "Extrato de Ata") e, no rodapé, o código de autenticação, que muda de uma peça para outra. Foi assim que separei Lewandowski (código CC3F-…, p37-52) de Moraes (código 19E3-…, p53-71), porque as duas peças têm o mesmo rótulo "Voto Vogal".

## (b) Peças anunciadas ausentes e outras questões de estrutura
- Nenhuma peça é anunciada sem estar no acórdão.
- O voto do Revisor está rotulado "Voto Vogal", não "Voto Revisor".
- A denúncia descreve três fatos, e os três votos com texto tratam os fatos em blocos separados (páginas na coluna `obs`). O banco registra uma linha por ministro, com a coluna `fato` vazia.

## (c) DIVERGE
Nenhuma.

## (d) Como li
Por navigação. Li na íntegra as p1-2, 5-6, 35-38, 52-53 e 70-72. Nas demais páginas, identifiquei as peças pelo rótulo do cabeçalho e pelo código de autenticação, e localizei os blocos de cada fato e das preliminares com `grep` (só para navegar). Os limites dos blocos de fatos nos votos de Lewandowski e Moraes são aproximados.
