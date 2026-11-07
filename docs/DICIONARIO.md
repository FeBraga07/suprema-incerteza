# Dicionário de dados

Todas as tabelas são texto UTF-8 separado por barra vertical (`|`), com cabeçalho na primeira linha. Linhas iniciadas por `#` são comentário. Valores lógicos são `Sim`/`Não` nas tabelas do banco e `Sim`/`Nao` nas da leitura da fundamentação. Campo vazio significa que não se aplica ou que a fonte não diz.

As tabelas do banco (`dados/derivados/`) são geradas por `dados/metodologia/build_l3.py` a partir dos arquivos de caso (`dados/derivados/casos/*.json`); as da leitura da fundamentação (`dados/metodologia/fase4/consolidado/`), por `dados/metodologia/fase4/consolidar_fase4.py` a partir das leituras A e B. Nenhuma é editada à mão.

## Chaves

| Chave | Forma | Exemplo |
|---|---|---|
| `id_caso` | `AP-` + número da ação penal | `AP-470` |
| `id_caso_reu` | `id_caso` + `-R` + ordem do réu | `AP-470-R05` |
| `id_unidade` | `id_caso_reu` + `-I` + ordem da imputação, com letra quando a unidade foi desdobrada por fato | `AP-1025-R01-I01a` |

---

## 1. Banco de casos, réus e votos

### `1_casos.psv` — uma linha por ação penal (25)

| Campo | Definição |
|---|---|
| `id_caso`, `numero_processo` | Identificação da ação penal |
| `nome_popular` | Nome pelo qual o caso é conhecido, quando há (só a AP 470, "Mensalão") |
| `link_portal` | Endereço do acórdão no portal de jurisprudência do STF |
| `data_julgamento`, `ano_julgamento` | Data (AAAA-MM-DD) e ano da sessão que concluiu o julgamento |
| `multiplas_sessoes` | Se o julgamento se estendeu por mais de uma sessão |
| `relator` | Ministro que relatou o processo e proferiu o primeiro voto |
| `redator_acordao` | Ministro que redigiu o acórdão (o portal o informa como relator) |
| `relator_vencido` | Se o relator ficou vencido no resultado de ao menos um réu ou fato do escopo (3 casos) |
| `modalidade_corrupcao`, `modalidade_levcovitz` | Modalidade(s) de corrupção, por extenso e pelo número da lista de Levcovitz (2014, Quadro 1.1) |
| `instituto_juridico_1`, `instituto_juridico_2` | Instituto jurídico central do caso, em texto |
| `n_reus` | Número de réus julgados na ação, dentro e fora do escopo |
| `merito_finalizado` | Se houve julgamento de mérito (critério de inclusão; sempre `Sim`) |
| `lavagem_associada`, `organizacao_criminosa_associada` | Se o caso inclui imputação de lavagem de dinheiro ou de associação ou organização criminosa (não são critério de inclusão) |
| `depende_dl201`, `regra_aplicada` | Se o caso entrou pela equivalência do Decreto-Lei 201/1967 (`inclusao_dl201`, 7 casos) ou diretamente pela lista (`inclusao_direta`, 18) |
| `justificativa_classificacao` | Razão da inclusão, com o dispositivo imputado |
| `observacoes` | Observações do build |

### `2_casos_reus.psv` — uma linha por réu com ao menos uma imputação no escopo (66)

| Campo | Definição |
|---|---|
| `nome_reu`, `cargo_funcao` | Nome e cargo, em texto livre, como constam do acórdão; o cargo relevante é o da época dos fatos |
| `resultado` | `Condenação`, `Condenação parcial` ou `Absolvição`, pelo mérito dos crimes do escopo. Condenação seguida de prescrição pela pena em concreto continua `Condenação` |
| `resultado_binario` | 1 = condenação (total ou parcial); 0 = absolvição |
| `motivo` | Razão dominante do desfecho: `mérito`, `atipicidade`, `prescrição` ou `processual` |
| `prescricao_pos_condenacao` | Se a punibilidade foi extinta pela prescrição depois da condenação |
| `crimes` | Dispositivos imputados ao réu no escopo |
| `n_votantes`, `votos_condenacao`, `votos_absolvicao` | Placar. Votos que julgam procedente a ação com pena que leva à prescrição contam como condenação |
| `margem_votos`, `perc_vencedor` | Diferença entre os lados e proporção de votos do lado vencedor |
| `unanime` | Se todos os votantes chegaram ao mesmo resultado em todos os fatos do escopo imputados ao réu |
| `categoria_placar` | `Unânime`; `Folgado` (vencedor com 70% ou mais); `Apertado` (menos de 70%) |
| `placar_fato_ref` | Em réu com vários fatos de placar diferente, o fato cujo placar a linha carrega: o mais apertado |
| `dissenso_fora_resultado` | Dissenso restrito a crime fora do escopo ou a fundamento que não altera o resultado (não quebra a unanimidade) |
| `observacoes` | Registro das regras do build aplicadas à linha |

### `3_votos.psv` — uma linha por voto de ministro sobre um réu e um fato (927)

| Campo | Definição |
|---|---|
| `id_voto` | Número sequencial |
| `fato` | Imputação com placar próprio dentro do réu; vazio quando o réu tem placar único |
| `ministro` | Nome padronizado (ver `4_referencia_ministros.psv`) |
| `eh_relator` | Se o ministro é o relator |
| `voto_resultado`, `voto_binario` | `Condena` (1), `Absolve` (0) ou `Não votou` (vazio) |
| `acompanhou_relator` | Se votou como o relator do mesmo grupo; `NA` para o próprio relator e para quem não votou |
| `acompanhou_maioria` | Inverso de `vencido` para quem votou; `NA` para quem não votou |
| `vencido` | Se ficou vencido no resultado |
| `ausente`, `motivo_ausencia` | Ausência, impedimento ou suspeição registrados na ata, e o motivo |
| `fonte_voto` | Origem do registro: `lido` (com evidência textual), `deduzido` (ministro em exercício, não listado como ausente nem vencido, votou com a maioria) ou `sem_evidencia` |

### Tabelas de referência e auxiliares

| Arquivo | Conteúdo |
|---|---|
| `4_referencia_ministros.psv` | Os 32 ministros do período: nome padronizado e variantes, posse, saída, quem indicou e afastamentos temporários. Usada para saber quem estava em exercício em cada sessão |
| `4_referencia_categoria_placar.psv` | Limiares das categorias de placar |
| `4_referencia_temas_juridicos_ilustrativos.psv` | Temas jurídicos usados como ilustração, com a indicação de mudança formal de regra relevante |
| `classificacao_105.psv` | As 105 ações penais do censo classificadas uma a uma: decisão (`incluir`/`excluir`), modalidade, regra aplicada, fonte da decisão (ementa, ata, legislação citada) e justificativa |
| `classificacao_complemento_2026-10-18.psv` | Classificação do complemento do censo (APs catalogadas como julgamento de Turma), que trouxe a AP 307 |
| `cargo_categoria_auditoria.psv` | Categoria do cargo de cada réu, ao lado do texto livre, para auditoria da categorização |
| `analise_descritiva.md` | Estatística descritiva do banco, gerada por `analise_descritiva.py` |

### Arquivos de caso (`derivados/casos/`)

Um JSON por caso, saída da extração. Todo campo tem quatro partes: `valor`, `evidencia` (trecho literal da fonte), `fonte` (ementa, ata, página do acórdão ou legislação citada) e `confianca` (`alta`, `media`, `baixa`). `_dupla/` guarda as duas extrações independentes (A e B) dos casos com dupla extração; `_reteste/`, a repetição cega de seis extrações semanas depois (ver `metodologia/reteste/`).

---

## 2. Leitura da fundamentação dos votos (`metodologia/fase4/consolidado/`)

Base congelada em 24/10/2026; o conteúdo de cada arquivo está registrado em `metodologia/fase4/CONGELAMENTO_2026-10-24.md`. As categorias e regras estão em `docs/CODEBOOK.md`.

### `fase4_unidades.psv` — uma linha por unidade réu × imputação (105)

| Campo | Definição |
|---|---|
| `unidade_origem` | Para unidades desdobradas ou fundidas, a unidade de que se originam |
| `fato` | Fato da unidade, quando a imputação foi desdobrada por fato |
| `escopo_levcovitz` | Se a imputação está no escopo de corrupção (74 das 94 ativas) |
| `status` | `ativa` (94); `desdobrada`, `fundida` ou `excluida`, quando substituída na consolidação; `pendente_leitura` |
| `motivo_status` | Código do item de revisão que alterou a unidade e o que mudou |
| `voto_condutor` | Ministro que fundamenta a razão de decidir |
| `n_questoes_ativas`, `n_principais` | Número de questões decisivas e de questões principais |

### `fase4_questoes.psv` — uma linha por questão decisiva (179; 174 ativas)

| Campo | Definição |
|---|---|
| `indice` | Ordem da questão na unidade |
| `status` | `ativa` ou `excluida` |
| `categoria` | `concorreu`, `dolo`, `tipicidade`, `ato_de_oficio` ou `outra` |
| `anotacao_tipicidade` | Na tipicidade, se a dúvida é a `existencia_fato` ou o `enquadramento` |
| `anotacoes` | `prova_colaboracao` (palavra de colaborador premiado) ou `prova_inquerito` (prova só do inquérito) |
| `principal` | Se é a pergunta principal da unidade |
| `resposta_tribunal` | `sim` ou `nao`; o "sim" significa que o elemento da acusação está presente |
| `sim_favorece` | A quem favorece o "sim": `acusacao` (todas as categorias fechadas) ou, em `outra`, `defesa` ou `neutra` |
| `padrao_dolo_exigido` | No dolo, o padrão que o voto exige: `generico`, `especifico` ou `nao_dito` |
| `modo_concurso` | Em `concorreu`: `autor`, `participe` ou `nao_dito` |
| `pergunta_outra` | Formulação da pergunta, quando a categoria é `outra` |

### `fase4_posicoes.psv` — uma linha por ministro em cada questão (1.704)

| Campo | Definição |
|---|---|
| `indice_questao`, `categoria` | Questão a que a posição se refere |
| `voto_resultado` | `Condena`, `Absolve`, `Extingue` (extinção da punibilidade) ou `Tranca` (trancamento da ação) |
| `voto_resultado_original` | Valor registrado pela leitura antes da consolidação |
| `enfrentou_a_questao` | `Sim` (fundamentação própria), `Adesao` (só acompanha) ou `Nao` (votou por outra razão) |
| `posicao` | `sim`, `nao` ou `nao_enfrentou` |
| `confianca_posicao` | `alta`, `media` ou `baixa` |
| `inferida_de` | Na adesão, de quem a posição foi inferida e onde |
| `fundamento_proprio` | Quando o ministro chega ao resultado por outra questão, qual |
| `regras_aplicadas` | Regras do *codebook* e itens de revisão aplicados à linha, pelo código de trabalho (correspondência em `docs/CODEBOOK.md`) |

### `fase4_precedentes.psv` — uma linha por referência a decisão anterior ou mudança de regra (585)

| Campo | Definição |
|---|---|
| `tipo` | `precedente_citado`, `distincao`, `mudanca_lei`, `mudanca_jurisprudencia` ou `superacao` |
| `sentido` | `para_seguir` ou `para_afastar` |
| `proprio_ministro` | Se o ministro cita voto seu anterior |
| `fonte`, `referencia` | Página do acórdão e a referência como aparece no texto |

`consolidado/casos/` traz a leitura consolidada de cada caso em JSON, com as evidências; `consolidado/conferencia/` traz as listas de conferência geradas na consolidação.

---

## 3. Fontes brutas (`dados/brutos/`) e corpus (`dados/corpus/`)

| Arquivo | Conteúdo |
|---|---|
| `censo_ap_plenario_1991_2024.psv` | Resultado da consulta ao índice do portal (classe AP, Tribunal Pleno, 1991–2024), sem os incidentes processuais: as 105 ações penais puras que formam o universo bruto. O cabeçalho comentado registra a consulta |
| `censo_complemento_ap_turmas_2026-10-18.psv` | Varredura das 85 APs catalogadas como julgamento de Turma |
| `resultados-de-acordaos.csv` | Export do portal (título, relator, datas, órgão julgador, ementa), separado por ponto e vírgula |
| `AP-307_ata_indice_sjur157761.txt` | Ata da AP 307 recuperada do índice |
| `corpus/texto/AP-*.txt` | Texto integral de cada acórdão, com as páginas marcadas (`===== [página N/M] =====`) |
| `corpus/manifesto_acordaos.psv` | Rota, identificador, formato, páginas e tamanho de cada PDF |
