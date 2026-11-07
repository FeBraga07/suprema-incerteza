# Método, etapa por etapa

Este documento liga cada etapa do trabalho aos arquivos deste repositório: o que entrou, o que a produziu, o que saiu e como foi verificada. A justificativa das escolhas está na Metodologia do trabalho (capítulo 3).

## Visão geral

```
portal do STF ──► censo (105 AP) ──► classificação ──► 25 casos ──► corpus (texto dos acórdãos)
                                                                        │
                        ┌───────────────────────────────────────────────┤
                        ▼                                               ▼
              extração do banco                              leitura da fundamentação
         (resultado, placar, votos)                    (questão decisiva, posição, precedentes)
                        │                                               │
             dupla extração · gabarito                      piloto cego · dupla leitura
             · κ · reteste                                  · κ · revisão cega dos temas
                        ▼                                               ▼
        derivados/1_casos, 2_casos_reus, 3_votos          fase4/consolidado/ (congelado)
                        └──────────────────────┬────────────────────────┘
                                               ▼
                                 análise descritiva e comparação
```

## Etapas

| # | Etapa | Entrada | Como foi feita | Saída | Verificação |
|---|---|---|---|---|---|
| 1 | Censo | Índice de jurisprudência do portal | Consulta no navegador: acórdãos, classe AP, Tribunal Pleno, 1991–2024, sem incidentes (`metodologia/censo_2026-08-08.md`) | `brutos/censo_ap_plenario_1991_2024.psv` (105 ações penais) | Complemento: varredura das 85 APs catalogadas como Turma (`metodologia/censo_complemento_2026-10-18.md`), que trouxe a AP 307 |
| 2 | Classificação | Ementa, ata e legislação citada de cada AP | Protocolo escrito antes da classificação (`metodologia/PROTOCOLO_CLASSIFICACAO.md`), aplicado caso a caso pelas 19 modalidades de Levcovitz (2014) | `derivados/classificacao_105.psv` e complemento: 25 casos | Registro da decisão e da fonte de cada caso (`metodologia/CLASSIFICACAO_105.md`) |
| 3 | Corpus | Inteiro teor em PDF | Download no navegador (`corpus/baixar_acordaos.js`), extração com Poppler (`corpus/extrair_texto_pdftotext.py`) e reconhecimento óptico local nos digitalizados (`corpus/ocr_vision.py`) | `corpus/texto/` (25 acórdãos, 25,3 milhões de caracteres) e `corpus/manifesto_acordaos.psv` | Saída de cada conversor conferida contra uma segunda ferramenta |
| 4 | Extração do banco | Texto do acórdão, esquema de saída, composição da Corte e regras escritas | Um agente por caso, em contexto novo, sem rede e sem acesso a outros casos (`metodologia/prompts_lotes/`) | `derivados/casos/*.json`, com evidência literal para cada valor | Dupla extração em 15 casos (`derivados/casos/_dupla/`); gabarito humano em 9 (`metodologia/GABARITO_VALIDACAO.md`) |
| 5 | Construção das tabelas | `derivados/casos/*.json` | Passo determinístico (`metodologia/build_l3.py`, regras em `metodologia/build_l3.md`) | `derivados/1_casos.psv`, `2_casos_reus.psv`, `3_votos.psv` | Reconstruível a qualquer momento |
| 6 | Validação da extração | Extrações A e B; gabarito | `metodologia/concordancia_kappa.py`, `metodologia/validacao_gabarito.py`, `metodologia/medir_deducao_d004.py` | `concordancia_kappa_2026-09-20.md`, `validacao_gabarito_2026-09-19.md`, `medicao_deducao_d004_2026-10-24.md` | Teste-reteste cego de seis extrações (`metodologia/reteste/`) |
| 7 | Análise descritiva | Tabelas do banco | `metodologia/analise_descritiva.py` (método em `analise_descritiva_metodo.md`) | `derivados/analise_descritiva.md` | Reconstruível |
| 8 | *Codebook* | Leitura do autor de três acórdãos (AP 426, AP 416 e AP 409) | Folhas de leitura e entrevistas (`metodologia/fase4/anotacoes_codebook/`) | `docs/CODEBOOK.md` (versão aplicada); `metodologia/fase4/CODEBOOK.md` (arquivo de trabalho) | Revisto depois da primeira leitura do conjunto |
| 9 | Leitura da fundamentação | Texto do acórdão, mapa das peças de cada voto (`fase4/mapa_votos/`), unidades réu × imputação (`fase4/unidades_reu_fato.psv`) e *codebook* | Um agente por caso e por leitura, com contrato de saída (`fase4/CONTRATO_FASE4.md`) e prompt (`fase4/PROMPT_FASE4.md`; `PROMPT_FASE4_v2.md` para a AP 307); prompts de cada caso em `fase4/prompts_lote/` | `fase4/extracao/lote/A/` e `B/` | Piloto cego contra leitura humana (`fase4/extracao/piloto/`); concordância A × B (`fase4/extracao/lote/concordancia_fase4*.md`) |
| 10 | Consolidação | Leituras A e B e decisões da revisão | `fase4/consolidar_fase4.py` | `fase4/consolidado/`, congelado em 24/10/2026 (`fase4/CONGELAMENTO_2026-10-24.md`) | Listas de conferência em `fase4/consolidado/conferencia/` |
| 11 | Comparação | Base consolidada | `fase4/analise_fase4.py`; agrupamento das questões de direito por tema | `fase4/analise/resultados_preliminares_fase4_v2.md` | Reconstrução cega dos temas por um segundo modelo (`fase4/analise/revisao_cega_agrupamento_2026-10-24/`) |

Os caminhos da tabela são relativos a `dados/`.

## Modelos de linguagem por etapa

| Etapa | Modelo |
|---|---|
| Classificação, download e reconhecimento óptico | `claude-opus-5` |
| Extração do banco (44 agentes), comparação, arbitragem e consolidação | `claude-sonnet-5` |
| Construção das tabelas e análise descritiva | `claude-sonnet-5` |
| Auditoria das extrações e coeficientes de concordância | `claude-opus-5` |
| Extração da AP 307 | `claude-opus-5-5` |
| Leitura da fundamentação, consolidação e revisão cega dos temas | `claude-opus-5-5` |

Todas as etapas foram executadas pela ferramenta Claude Code (Anthropic). Os modelos mudaram ao longo do trabalho porque as versões disponíveis mudaram. Por isso cada etapa tem a própria verificação, em vez de se presumir o desempenho de uma para outra. Modelos proprietários são ajustados continuamente: repetir hoje uma leitura com os mesmos prompts não garante o mesmo resultado, e o desempenho precisa ser medido de novo. A análise não depende disso, porque as leituras estão congeladas em disco.

## Regras que valem para todas as etapas com modelo

- **Evidência literal obrigatória.** Todo valor tem o trecho da fonte que o sustenta e a página. Sem evidência, o campo fica nulo.
- **Correspondência de padrão localiza, não decide.** Expressões regulares foram abandonadas na extração de resultado e placar depois de produzirem erros em pelo menos doze casos.
- **Leitura cega.** Nenhum agente recebeu o gabarito, os resultados de outros casos ou as leituras do outro leitor.
- **Nada é editado à mão.** As tabelas são derivadas por script; quando uma regra muda, muda o script e ele roda de novo.

## Referências cruzadas nos documentos

Os documentos de método citam decisões pelo código `D-NNN` e itens de revisão por códigos como `G4-06`. São registros internos do projeto, não publicados; o conteúdo metodológico de cada decisão está descrito na Metodologia do trabalho.
