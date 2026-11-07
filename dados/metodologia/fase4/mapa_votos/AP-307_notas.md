# AP-307 — notas do mapa estrutural de votos

Mapa: `AP-307.psv` (64 peças). Feito em 18/10/2026 por claude-opus-5-5 (subagente), seguindo `PROMPT_MAPA.md`.

## (a) Problemas de OCR que pedem o PDF

- **pp.1-5 (ementa e acórdão):** a diagramação em colunas fragmentou as linhas, e há trechos lacunares (p.2 sobretudo; na p.4 a lista de vencidos do art. 317 aparece partida entre colunas). Para citar, usar o PDF.
- **p.6 e p.42:** os nomes dos réus no cabeçalho somem ou saem truncados (p.42: "PAULO COSAR CASAL ONDE FARIAS").
- **Títulos das peças:** "VOTO" sai como "VOI O", "VeIO", "VOIO", "VOID", "V °", e "Sr." sai como "SI." ou "Si.". Nenhum desses casos impediu de identificar a peça.
- **p.673 (ata de 12.12.94):** a lista de presentes e ausentes está embaralhada ("Ausente, justificadamente, o senior Aurélio e Velloso"). A cópia legível da mesma ata está na p.752.
- **p.696:** o título da peça diz "VOTO (S/ art, 292 do CP)". Pelo contexto (réus e ata) parece ser 299; conferir no PDF.
- **pp.640-664 (Néri da Silveira):** linhas como "7. Méri", "7. Vari" e "7. Mári" são a rubrica lida pelo OCR, não números de item.
- **p.751 e p.756:** os cabeçalhos das atas estão corrompidos ("AÇAO PENAL N." sem número; "upecao c'sievenné"). O conteúdo de cada uma foi identificado pela data da sessão.
- Os números de folha carimbados vêm misturados ao texto ("2431" para 2434 e assim por diante). A página usada no mapa é sempre o marcador `[página N/756]`.

## (b) Peças anunciadas que não estão no acórdão

- **Sustentações orais dos advogados (07.12.94):** a ata da p.510 as registra, mas não foram transcritas. Só a manifestação do Procurador-Geral está no acórdão (pp.44-64).
- **Manifestação oral do Revisor na sessão de 09.12.94:** o Relator a cita ao retificar o voto (p.511: "o Senhor Ministro Moreira Alves diz que o requerimento é mais amplo"), mas ela não foi transcrita.
- **Questão de ordem da defesa (p.695, 13.12.94):** não há resposta nem decisão transcrita logo depois dela.
- **Pena no art. 317:** Néri da Silveira (p.664) e Velloso (p.748) disseram que fixariam a pena se a condenação prevalecesse. Como ela não prevaleceu, nenhuma peça foi produzida.

## (c) Linhas DIVERGE

Nenhuma. Os dispositivos de todos os votos de mérito do art. 317 batem com o banco; isso vale também para Pertence, Néri e Velloso, que condenam R01 e R02 apenas no episódio Mercedes-Benz. Conferi só os dispositivos, sem ler cada voto por inteiro.

## Convenções usadas neste caso

- **`reus_abrangidos`:** traz os ids do banco só nas peças sobre o art. 317. Nas peças que tratam apenas dos arts. 305/343/344/299, o campo fica vazio, mesmo quando o réu (R02 ou R03) também responde por esses crimes.
- **`voto_banco` nas peças preliminares do art. 317:** copia o voto de mérito do banco, que não registra as preliminares (isso está dito na `obs`).
- **Ementa, acórdão, relatório, atas, debate e "outro":** ficaram sem `voto_banco`. O voto de cada ministro está na sua linha de voto.
- **`varia`** foi usado para Néri da Silveira, Sepúlveda Pertence e Carlos Velloso: Condena no episódio Mercedes-Benz para R01 e R02, Absolve no resto. Detalhe na `obs`.
- **Marco Aurélio (suspeição) e Francisco Rezek (ausente):** não votaram, mas ganharam uma linha `extrato_ata` cada, porque o banco tem registros para os dois.

## (d) Como li

Por navegação, sem ler o arquivo inteiro. Primeiro fiz busca de cabeçalhos (data da sessão, "TRIBUNAL PLENO", "EXTRATO DE ATA", marcas de locutor "O SENHOR MINISTRO", "O Sr. Ministro" e "O DR."). Depois li:
- as primeiras linhas de todas as 756 páginas;
- as páginas inteiras 1-6, 41-44, 64-65, 87-88, 212-213, 247-248, 328-331, 339, 358, 415, 457, 509-516, 533-558, 601-602, 624-626, 639-640, 663-706, 748-756;
- os pontos de transição internos dos votos do Relator e do Revisor (seções A/B/C e itens 1-7).

Usei busca textual só para navegar, por exemplo para achar onde cada voto do art. 317 menciona R03 e cada episódio. Os votos longos (pp.88-212, 329-509, 558-601, 602-625, 626-639, 640-664, 707-748) **não** foram lidos por inteiro.
