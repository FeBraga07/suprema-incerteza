# L3 — build determinístico das 4 tabelas

> Executado em **09/08/2026**. Rege a leitura de `dados/derivados/1_casos.psv`,
> `2_casos_reus.psv` e `3_votos.psv`. `4_referencia_*.psv` já existiam antes deste
> build (ver `reconstrucao_4_referencia.md`) e não são regeneradas por
> `build_l3.py`.
>
> Script: `dados/metodologia/build_l3.py`. Roda sem argumentos, sem rede,
> ~1s. **As três PSVs não são editadas à mão.** Se uma regra de mapeamento
> mudar, muda-se o script e roda-se de novo — não a saída.

## Entradas

- `dados/derivados/casos/AP-*.json` — os 24 casos extraídos (L1), um por caso.
- `dados/derivados/classificacao_105.psv` — as 24 linhas com `decisao=incluir`, fonte de `regra_aplicada`, `merito_finalizado`, `lavagem_associada`, `organizacao_criminosa_associada`, `depende_dl201` e `justificativa_classificacao`.
- `dados/brutos/censo_ap_plenario_1991_2024.psv` — fonte de `numero_processo`, `data_julgamento`, `relator` e `sjur_id` (para `link_portal`). Esses campos de identificação **não estão nos JSONs por caso** (o L1 não os recoletou — não havia razão, já vinham corretos do censo).
- `dados/derivados/4_referencia_ministros.psv` — usada só para normalizar a grafia de `relator` e `ministro` contra `nome_padrao` (cruzamento informal, não uma FK executada).

Um `assert` no início do script trava se o conjunto de `id_caso` dos JSONs divergir do conjunto `decisao=incluir` da classificação — as duas fontes precisam concordar exatamente em 24 casos antes de gerar qualquer linha.

## Saídas — o que muda em relação ao esquema documentado antigo

`PLANO_EXTRACAO.md` §4 previa manter os nomes das colunas já documentadas em `DICIONARIO.md` e acrescentar as novas do CLAUDE.md/D-012/D-013. Na prática, três pontos precisaram de decisão de desenho que o plano não fechava — registrados aqui, não decididos em silêncio:

### 1. `instituto_juridico_1`/`instituto_juridico_2` — a coluna 2 fica sempre vazia

O schema de extração L1 (`caso.instituto_juridico`, um objeto único por caso) nunca previu um segundo instituto jurídico secundário — e é distinto do bloco de referência `4_referencia_temas_juridicos_ilustrativos.psv` (8 temas ilustrativos, catálogo, não por caso — ver a "colisão de nome" já registrada em `PLANO_EXTRACAO.md` §8 / `reconstrucao_4_referencia.md`). `instituto_juridico_1` recebe `caso.instituto_juridico.valor` integralmente; `instituto_juridico_2` fica **permanentemente vazio** por desenho, não por preenchimento pendente — mantida só para não quebrar quem já espera a coluna.

### 2. `3_votos` sem `reu`/`fato` explícitos → fan-out para todos os réus do caso

21 dos 24 casos têm placar homogêneo entre réus (o L1 não diferenciou voto por réu porque o resultado por ministro é o mesmo para todos). Nesses casos o array `votos[]` do JSON não carrega os campos `reu`/`fato` — uma linha por ministro, aplicável ao caso inteiro. Os outros 3 (`AP-565`, `AP-1025`, `AP-470`) têm placar heterogêneo (D-021) e cada linha de `votos[]` já nomeia `reu` e `fato` explicitamente.

O build trata os dois formatos: quando `reu` está ausente, replica a linha de voto para **todos** os réus de `2_casos_reus` daquele caso (fan-out); quando presente, usa o valor direto. Verificado antes de implementar: nos 21 casos sem `reu`/`fato`, o placar (`votos_condenacao`/`votos_absolvicao`/`unanime`) é de fato idêntico entre todos os réus do caso — o fan-out não inventa diferenciação que não existe na fonte.

### 3. `acompanhou_relator` é campo derivado, não extraído

Não existe no schema L1. Calculado por grupo `(id_caso_reu, fato)`: `Sim`/`Não` comparando `voto_resultado` de cada ministro ao do relator do mesmo grupo; `NA` quando a própria linha é do relator, quando o ministro não votou, ou quando o relator do grupo não votou. É aritmética sobre campos já evidenciados — não é dado novo, é a mesma classe de operação que `margem_votos`, `perc_vencedor` e `categoria_placar` já eram no desenho original.

## Regras de negócio aplicadas (decisões já registradas em `DECISOES.md`)

- **D-018** — `resultado` do réu é sempre o valor de mérito (`Condenação`/`Condenação parcial`/`Absolvição`); prescrição/processual entram só em `motivo` e `prescricao_pos_condenacao`. Os JSONs já vêm assim; o build não reinterpreta.
- **D-020/D-022** — réu sem nenhum crime no escopo Levcovitz não tem linha em `2_casos_reus`/`3_votos` (só afeta `AP-470`: `n_reus=37` na ficha do caso, 23 réus na tabela — checado e reportado pelo build, não é bug).
- **D-021** — granularidade de `3_votos` é `(ministro, id_caso_reu, fato)`, coberta pelo fan-out do item 2 acima.
- **Limiar de `categoria_placar`: 70%**, fixado em `4_referencia_categoria_placar.psv` (`Unânime` se `unanime=true`; `Folgado` se `perc_vencedor≥0,70`; `Apertado` caso contrário — `unanime` tem precedência, D-007).

## Achados do build — nenhum é erro de script, todos rastreáveis à fonte

Os `assert`s de integridade do script **passam** (0 PK duplicada, 0 FK órfã). As únicas duas "violações" que o build imprime são esperadas e documentadas na origem:

1. **`AP-470`: `n_reus=37` vs. 23 linhas em `2_casos_reus`.** Efeito direto e intencional de D-020 (14 réus sem crime de escopo Levcovitz ficam fora da tabela por réu, mas contam para `n_reus` do caso).
2. **`AP-409-R01`: `votos_condenacao(5) + votos_absolvicao(3) ≠ n_votantes(10)`.** Não é erro de soma do build — é a própria ata que registra o resultado dessa forma (2 ministros, Marco Aurélio e Cezar Peluso, votaram por condenar mas com pena que geraria prescrição; a ata trata esse voto como categoria à parte, não soma nem em "condena" nem em "absolve" na contagem oficial de 5×3). Documentado em detalhe nos `avisos` de `AP-409.json`. O build preserva o valor extraído tal como a ata registra, em vez de forçar a soma.

## Duplicidade em `4_referencia_ministros.psv` — RESOLVIDA em 22/08/2026

`4_referencia_ministros.psv` tinha **duas linhas para a mesma pessoa** (Carlos Augusto Ayres de Freitas Britto): `Carlos Britto` (posse 2003-06-26, saída 2012-07-14) e `Ayres Britto` (posse 2003-06-26, saída 2012-11-17). Nos JSONs de extração ele aparece sob três grafias: `Carlos Britto` (relator da `AP-447`, 2009), `Ayres Britto` (várias) e `Carlos Ayres Britto` (`AP-447`, campo `ministro` da própria linha em que ele é relator).

**Verificado contra fonte externa (STF/OABRJ, 22/08/2026):** Ayres Britto completou 70 anos em **18/11/2012**; a aposentadoria compulsória foi decretada em **17/11/2012**, véspera do aniversário. Não há registro de nenhum evento em julho/2012 — a linha `Carlos Britto` (`data_saida=2012-07-14`) era um erro de fonte/digitação, não uma licença real. **Decisão:** removida a linha `Carlos Britto`; mantida só `Ayres Britto`, `data_saida=2012-11-17`, com `Carlos Britto` dobrado em `nome_variantes`. O script (`RENOMEIA_MINISTRO`) ganhou a entrada `"Carlos Britto": "Ayres Britto"` e o lookup do campo `relator` (vindo do censo, fonte separada dos JSONs) passou a aplicar a mesma normalização — antes só o `ministro` de `3_votos` era normalizado, não o `relator` de `1_casos`, o que teria deixado a correção incompleta. 0 nomes fora do domínio depois do fix, checado pelo script a cada rodada.

## Resultado

| Tabela | Linhas | Observação |
|---|---|---|
| `1_casos.psv` | 24 | 1 por caso, id_caso único |
| `2_casos_reus.psv` | 63 | 1 por réu no escopo Levcovitz (D-020) |
| `3_votos.psv` | 877 | 1 por (ministro, réu, fato) |

Distribuição em `2_casos_reus` (63 réus): `Absolvição` 31, `Condenação` 24, `Condenação parcial` 8. `unanime`: 34 Sim / 29 Não. `motivo`: mérito 45, atipicidade 12, prescrição 4, processual 2 — `atipicidade` é um quarto valor de `motivo` que apareceu na extração e não estava listado em `PLANO_EXTRACAO.md` (que previa mérito/prescrição/processual); mantido como extraído, sem forçar em nenhuma das três categorias previstas.

Em `3_votos` (877 votos): `Condena` 486, `Absolve` 334, `Não votou` 57; `acompanhou_relator`: Sim 646, Não 94, NA 137.

## Pendências que este build **não** resolve (fora de escopo aqui)

- O valor `atipicidade` em `motivo` não estava previsto no vocabulário de `PLANO_EXTRACAO.md` — decidir se vira categoria própria formalmente documentada ou se é caso de `mérito` com essa nuance.
- Nenhuma das divergências de gabarito já registradas em `ESTADO.md` (AP-565, AP-372) foi tratada aqui — o build lê só os JSONs consolidados, que já são a versão pós-investigação; o gabarito em si (`GABARITO_VALIDACAO.md`) não foi editado.

---

## Adendo de 19/09/2026 — colunas novas (D-029, D-030, D-032, D-034)

Build reexecutado em 19/09/2026 (`claude-fable-5-1`) depois das decisões D-029 a D-034. Versão anterior do script preservada em `_build_l3_pre_D029.py.bak`.

**`1_casos`**
| Coluna | Derivação | Decisão |
|---|---|---|
| `relator` | ministro com `eh_relator = Sim` nos votos do JSON (relator originário, quem conduziu o voto). Antes vinha do censo do portal | D-032 |
| `redator_acordao` | valor do censo do portal (quem redigiu o acórdão; difere do relator quando este fica vencido) | D-032 |
| `relator_vencido` | `Sim` se `relator ≠ redator_acordao`. 4 casos: AP-433, AP-508, AP-973, AP-1025 | D-032 |

**`2_casos_reus`**
| Coluna | Derivação | Decisão |
|---|---|---|
| `votos_condenacao`, `votos_absolvicao`, `n_votantes`, `unanime` | em réu com mais de um fato com votos, passam a ser os do **fato mais apertado** (menor `perc_vencedor`), e `unanime` só é `Sim` se todos os fatos forem unânimes. Em réu com um fato, valores do JSON | D-029 |
| `placar_fato_ref` | qual fato deu o placar da linha (vazio quando há um só fato) | D-029 |
| `dissenso_fora_resultado` | `Sim` quando o JSON registrou `unanime = False` mas o placar não tem divergência de resultado (dissenso sobre crime fora do escopo ou sobre fundamento). Nesses casos `unanime` vira `Sim`. AP-396-R01, AP-465-R01 | D-029 |
| `observacoes` | texto gerado pelo build explicando a intervenção da D-029 na linha | D-029 |
| `categoria_placar` | inalterada na fórmula (Unânime / Folgado ≥ 0,70 / Apertado < 0,70); muda de valor onde o placar mudou (AP-470-R01: 9x2 Folgado → 5x6 Apertado; AP-409-R01: 5x3 Apertado → 7x3 Folgado) | D-029, D-030 |

**`3_votos`**
| Coluna | Derivação | Decisão |
|---|---|---|
| `acompanhou_maioria` | `Não` se `vencido = Sim`, `Sim` se votou e não foi vencido, `NA` se ausente/não votou. Distinto de `acompanhou_relator`, que mede deferência ao relator e, nos 4 casos de relator vencido, marca a corrente perdedora | D-032 |
| `fonte_voto` | `lido` (campo com evidência textual), `deduzido` (`fonte` contém "deducao", regra D-004), `sem_evidencia` (valor cru ou evidência vazia). Nos 820 votos efetivos (Condena/Absolve): 586 lidos, 83 deduzidos, 151 sem evidência (AP-565: 90; AP-441: 20; AP-447: 20; AP-508: 9; AP-396: 7; AP-503: 4; AP-465: 1) | D-034 |

**Alterações em JSON de origem (com `valor_extraido_original` e `nota_revisao`):** `AP-409.json` `votos_condenacao` 5 → 7 (D-030); `AP-365.json` e `AP-375.json` `motivo` do corréu `atipicidade` → `processual` (D-031). `4_referencia_ministros.psv`: Lewandowski saída 2023-04-11 (G-A05), Carlos Velloso saída 2006-01-19 (G-A06).
