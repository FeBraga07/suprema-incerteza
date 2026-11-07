# Teste-reteste da extração L1 — 27/09/2026

**Pergunta.** O mesmo modelo, com o mesmo prompt e o mesmo texto, rodado de novo e às cegas semanas depois, reproduz a extração de agosto?

**Por quê.** É a segunda das três lacunas do método apontadas pelo levantamento de 20/09. Foi declarada como limitação na D-035 e ficou pendente no `ESTADO.md`, item 4. Decidido com o Felipe em 27/09: 6 casos, `claude-sonnet-5`, prompts originais.

## Desenho

| Item | Escolha | Justificativa |
|---|---|---|
| Modelo | `claude-sonnet-5` | É o modelo das extrações A e B de agosto. Com outro modelo seria uma terceira extração, e não um reteste |
| Prompt | o da extração **A** de cada caso, recuperado byte a byte da transcrição do agente original | Os tamanhos batem com a tabela §3 do `REGISTRO_EXECUCAO.md` (6.980 · 6.868 · 5.540 · 5.584 · 6.544 · 12.350 caracteres) |
| Alterações no prompt | (1) caminho de saída `_dupla/AP-X_A.json` → `_reteste/AP-X_R.json`; (2) uma nota final proibindo abrir `derivados/` e `metodologia/` | (2) é necessária porque, em agosto, os JSONs consolidados ainda não existiam. Hoje eles estão em disco, e sem a nota a extração deixaria de ser cega |
| Entrega do prompt | o agente recebe a instrução de ler o arquivo `prompts/AP-X_reteste.md` e executá-lo | Garante o texto idêntico, sem risco de erro de transcrição. É a única diferença de forma em relação a agosto, quando o prompt ia inline |
| Casos | AP-375, AP-430, AP-503, AP-508, AP-973, AP-1025 | Cobrem os lotes 1, 3, 4 e 5; vão de curto (12 mil caracteres) a muito longo (AP-1025, ~2 milhões); incluem unânimes, divididos, relator vencido (AP-508, AP-973), resultado por inciso (AP-503) e réu recorrente (AP-1025, Collor). Todos têm dupla extração, o que permite comparar o reteste com A e com B |
| Casos excluídos de propósito | AP-426, AP-409, AP-416 | Estão sendo lidos pelo Felipe para o codebook da Fase 4 (D-033). Deixá-los fora evita qualquer interferência |

## Comparações

- **R × A.** É o reteste propriamente dito: mesmo prompt, mesmo modelo.
- **R × B.** Referência.
- **A × B.** Linha de base: a concordância de agosto nesses mesmos 6 casos.

Os campos e o alinhamento das unidades são os mesmos de `concordancia_kappa.py`. Script: `reteste_comparacao.py`. Saída: `reteste_2026-09-27.md`.

## Arquivos

- `prompts/AP-X_original_A.md`: prompt original, extraído da transcrição do agente de agosto
- `prompts/AP-X_reteste.md`: prompt do reteste
- `../../derivados/casos/_reteste/AP-X_R.json`: saídas do reteste. Não alimentam o banco: `build_l3.py` lê só `derivados/casos/AP-*.json`

## Execução

Agentes disparados pela sessão `2df6a3df` (`claude-opus-5-5`) em 27/09/2026, com o modelo fixado explicitamente em `sonnet`. O modelo efetivamente usado é conferido depois, na transcrição de cada subagente, e registrado no `REGISTRO_EXECUCAO.md`.

## Resultado (resumo; o porquê está na D-037)

R × A: **97,9%** (334/341), contra 99,1% de A × B. Voto individual, unanimidade e placar: **100%**. Das 7 divergências, 3 são convenção (`vencido` nulo × "Não" para ministro que não votou), 1 é violação de vocabulário (`merito_finalizado` respondido em parágrafo) e 3 são `resultado`/`motivo` de desfecho misto (AP-503, AP-508). Todas estão na fronteira que a D-035 já tinha localizado.

Correção de alinhamento feita no script depois da primeira rodada: "Carlos Britto" e "Ayres Britto" passaram a ser reconhecidos como o mesmo ministro (`nome_ministro()`). Sem isso, um voto da AP-430 aparecia como "sem par".
