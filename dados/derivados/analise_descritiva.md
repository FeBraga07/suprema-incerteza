# Estatística descritiva — banco de casos STF (25 casos, 66 réus, 927 votos)

> Gerado por `dados/metodologia/analise_descritiva.py` a partir de `dados/derivados/{1_casos,2_casos_reus,3_votos}.psv`. Não editar à mão.

> Estatística descritiva pura (D-006 — sem econometria, sem teste de significância). Nenhum número aqui é causal.


## 1. Panorama geral

- **25 casos**, **66 réus** no escopo Levcovitz (D-020), **927 votos** individuais.
- `resultado`: Absolvição 34 (52%), Condenação 24 (36%), Condenação parcial 8 (12%)
- `unanime`: Sim 37 (56%), Não 29 (44%)
- `categoria_placar`: Unânime 37 (56%), Folgado 16 (24%), Apertado 13 (20%)
- Janela temporal: 1994–2023, com o vazio institucional 2014–2021 já documentado (D-011, Emenda Regimental 49/2014).

## 2. Unanimidade ao longo do tempo

Por ano de julgamento (nível réu, não caso — réus do mesmo caso têm o mesmo ano):

| Ano | N réus | Unânime | % unânime |
|---|---|---|---|
| 1994 | 3 | 1 | 33% |
| 2004 | 2 | 2 | 100% |
| 2006 | 3 | 3 | 100% |
| 2008 | 2 | 2 | 100% |
| 2009 | 2 | 0 | 0% |
| 2010 | 8 | 4 | 50% |
| 2012 | 26 | 13 | 50% |
| 2013 | 10 | 5 | 50% |
| 2014 | 1 | 1 | 100% |
| 2021 | 2 | 1 | 50% |
| 2022 | 3 | 3 | 100% |
| 2023 | 4 | 2 | 50% |

Em dois blocos (pré/pós vazio institucional 2014-2021, D-011):

| Bloco | N réus | Unânime | % unânime |
|---|---|---|---|
| 1994–2014 (pré-migração) | 57 | 31 | 54% |
| 2021–2023 (pós-retorno ao Plenário) | 9 | 6 | 67% |

## 3. Unanimidade por composição da corte (proxy: `n_votantes`)

`n_votantes` varia por ausências/impedimentos pontuais, não só por vacância formal — é proxy grosseiro de composição, não uma reconstrução da Corte por data. Ver `4_referencia_ministros.psv` para a composição exata em qualquer data.

| n_votantes | N réus | Unânime | % unânime |
|---|---|---|---|
| 7 | 3 | 2 | 67% |
| 8 | 8 | 5 | 62% |
| 9 | 6 | 6 | 100% |
| 10 | 36 | 17 | 47% |
| 11 | 13 | 7 | 54% |

## 4. Unanimidade por modalidade Levcovitz

Um réu pode estar em caso com mais de uma modalidade (`modalidade_levcovitz` é do caso, não do réu) — as contagens por código somam mais que 66.

| Código | Rótulo | N réus | Unânime | % unânime |
|---|---|---|---|---|
| 1 | Peculato (art. 312, CP, ou equivalente via DL 201/67) | 35 | 22 | 63% |
| 5 | Emprego irregular de verbas ou rendas públicas (art. 315, CP, ou equivalente via DL 201/67) | 8 | 3 | 38% |
| 8 | Corrupção passiva (art. 317, CP) | 34 | 19 | 56% |
| 10 | Prevaricação (art. 319, CP) | 3 | 1 | 33% |
| 15 | Corrupção ativa (art. 333, CP) | 24 | 13 | 54% |
| 18 | Crimes previstos na Lei 8.666/93 (licitações) | 18 | 10 | 56% |
| 19 | Improbidade administrativa (Lei 8.429/92) | 3 | 1 | 33% |

## 5. Unanimidade por cargo do réu (categorização automática — confirmada em 22/08/2026, D-025/D-026; cargo à época dos fatos)

| Categoria | N réus | Unânime | % unânime | Condenação | Absolvição | Cond. parcial |
|---|---|---|---|---|---|---|
| Particular / setor privado | 18 | 6 | 33% | 6 | 11 | 1 |
| Prefeito Municipal | 16 | 9 | 56% | 3 | 10 | 3 |
| Servidor/agente público (outro cargo) | 7 | 7 | 100% | 2 | 3 | 2 |
| Não determinado | 7 | 4 | 57% | 5 | 2 | 0 |
| Deputado Federal | 6 | 5 | 83% | 5 | 1 | 0 |
| Presidente da República | 2 | 1 | 50% | 0 | 2 | 0 |
| Secretário (Estado/Município) | 2 | 1 | 50% | 0 | 2 | 0 |
| Ministro de Estado / Chefia de órgão federal | 2 | 1 | 50% | 1 | 1 | 0 |
| Dirigente partidário | 2 | 1 | 50% | 2 | 0 | 0 |
| Deputado Estadual | 2 | 2 | 100% | 0 | 2 | 0 |
| Deputado Federal (Presidência da Câmara) | 1 | 0 | 0% | 0 | 0 | 1 |
| Senador da República | 1 | 0 | 0% | 0 | 0 | 1 |

## 6. Distribuição do `motivo`

Geral (todos os 66 réus):

| Motivo | N | % |
|---|---|---|
| mérito | 48 | 73% |
| atipicidade | 12 | 18% |
| prescrição | 4 | 6% |
| processual | 2 | 3% |

Só entre os 34 réus com `resultado = Absolvição` ("motivo da absolvição", D-008):

| Motivo | N | % das absolvições |
|---|---|---|
| mérito | 20 | 59% |
| atipicidade | 12 | 35% |
| processual | 2 | 6% |

## 7. Cluster de comparabilidade — réus por equivalência ao DL 201/67 (D-013)

É o grupo de "mesmo instituto jurídico" mais limpo do corpus: 7 casos entraram só porque o STF processou o art. 1º do DL 201/67 (crime de prefeito) como equivalente ao peculato/emprego irregular de verbas do CP (D-013). Mesmo instituto de fundo, réus julgados em anos diferentes — o recorte que a definição de "casos comparáveis" do `CLAUDE.md` pede.

| id_caso | Ano | Relator | Réu | Resultado | Unânime | Categoria placar |
|---|---|---|---|---|---|---|
| AP-426 | 2008 | Marco Aurélio | Cássio Taniguchi | Absolvição | Sim | Unânime |
| AP-409 | 2010 | Ayres Britto | José Gerardo Oliveira de Arruda Filho | Condenação | Não | Folgado |
| AP-503 | 2010 | Celso de Mello | Cássio Taniguchi | Condenação parcial | Não | Folgado |
| AP-416 | 2012 | Luiz Fux | Sérgio Ivan Moraes | Absolvição | Sim | Unânime |
| AP-441 | 2012 | Dias Toffoli | José Abelardo Guimarães Camarinha | Condenação | Não | Folgado |
| AP-441 | 2012 | Dias Toffoli | Walter Miosi | Condenação | Não | Folgado |
| AP-432 | 2013 | Luiz Fux | Jairo Ataíde Vieira | Condenação parcial | Não | Apertado |
| AP-973 | 2021 | Gilmar Mendes | André Luiz Dantas Ferreira (André Moura) | Condenação | Não | Apertado |

**7 casos, 8 réus, 6 condenações (75%), 2 unânimes (25%).** Nenhum teste de significância (D-006) — é descrição do grupo, não prova de instabilidade. Ver a tabela linha a linha acima para inspeção qualitativa (é isso que a hipótese do trabalho precisa examinar: mesmo instituto, resultados e placares comparados caso a caso).

## 7.1 Réus recorrentes — o mesmo réu em mais de um caso do corpus

Achado do build, não previsto no plano original: alguns réus aparecem em mais de um dos 25 casos. É comparabilidade de tipo mais forte que "mesmo instituto jurídico" — é o **mesmo réu**, o que isola quase tudo que poderia explicar uma diferença de resultado que não seja o próprio padrão decisório do STF. Chave de agrupamento normalizada por acento (ver `nome_normalizado()` no script — sem isso, 'Cássio Taniguchi' e 'Cassio Taniguchi', grafados de forma diferente em casos diferentes, não seriam reconhecidos como a mesma pessoa).

| Réu | Casos (ano — resultado — unânime) |
|---|---|
| Cássio Taniguchi | AP-426 (2008 — Absolvição — Sim); AP-430 (2008 — Absolvição — Sim); AP-503 (2010 — Condenação parcial — Não) |
| Fernando Affonso Collor de Mello | AP-307 (1994 — Absolvição — Não); AP-465 (2014 — Absolvição — Sim); AP-1025 (2023 — Condenação parcial — Não) |
| Jackson Barreto de Lima | AP-375 (2004 — Absolvição — Sim); AP-365 (2006 — Absolvição — Sim); AP-372 (2010 — Absolvição — Sim) |
| Sérgio Ivan Moraes | AP-447 (2009 — Absolvição — Não); AP-416 (2012 — Absolvição — Sim) |

**Dois casos com resultado diferente entre julgamentos do mesmo réu:**
- **Cássio Taniguchi** (ex-Prefeito de Curitiba): absolvido na AP-426 (2008) e na AP-430 (2008, mesmo ano, incisos diferentes do DL 201/67), depois **condenação parcial** na AP-503 (2010) — incisos IV e V do art. 1º condenados, inciso XIV absolvido. Não são os mesmos fatos exatos (incisos diferentes em cada ação), mas é o mesmo instituto (DL 201/67, equivalência D-013), o mesmo cargo, a mesma pessoa, em uma janela de 2 anos.
- **Fernando Affonso Collor de Mello** (ex-Presidente da República, depois Senador): absolvido na AP-307 (1994) e na AP-465 (2014, fatos de 1991-1992, corrupção passiva/peculato) e **condenação parcial** na AP-1025 (2023, fatos de 2010-2014, corrupção passiva/lavagem) — 9 anos de intervalo, fatos e período distintos, mesma pessoa, mesmo tipo penal central (corrupção passiva).

Nenhuma das duas comparações isola "mudança de posição do STF sobre o mesmo fato" no sentido mais estrito que `CLAUDE.md` define (fatos diferentes em cada ação, mesmo para o mesmo réu) — mas são o material bruto mais concreto do corpus para a seção de resultados examinar caso a caso. **Não incluído como prova de instabilidade aqui** — é só o achado de que o material existe e onde está.

## 8. Julgamento em sessão única vs. múltiplas sessões

7 dos 25 casos em múltiplas sessões, 18 em sessão única.
