# Suprema Incerteza

**Dados, código e instrumentos de leitura do trabalho de conclusão de curso _Suprema Incerteza: uma análise da estabilidade decisória do STF em casos de corrupção sob a ótica da economia institucional_**

Felipe Braga Baldin · Ciências Econômicas, Insper, 2026 · Orientação: Profa. Dra. Luciana Yeung Luk Tai

---

## O trabalho

**Pergunta.** O padrão decisório do Supremo Tribunal Federal em casos de corrupção apresenta estabilidade suficiente para funcionar como instituição redutora de incerteza, no sentido da economia institucional?

**Hipótese.** O tribunal muda de posição em questões comparáveis julgadas em momentos diferentes sem que a regra jurídica tenha sido formalmente alterada.

**Universo.** Censo das ações penais julgadas no mérito pelo Plenário do STF entre 1991 e 2024 por crimes contra a administração pública, segundo as 19 modalidades de corrupção de Levcovitz (2014): **25 ações penais, 66 réus e 927 registros de voto**, com julgamentos entre 1994 e 2023.

**Método.** Cada acórdão foi lido com assistência de modelos de linguagem em dois níveis. No primeiro, o resultado, o placar e o voto de cada ministro. No segundo, a fundamentação: a questão que decidiu cada réu em cada fato e a posição de cada ministro sobre ela. Todo valor registrado tem o trecho literal e a página da fonte. A confiabilidade foi medida por dupla leitura independente, com κ de Cohen, por comparação com conferência humana e por teste-reteste.

**Resultado.** A maior parte dos julgamentos se decide pela prova, e não pela interpretação da norma. Nas questões de direito que o Plenário enfrentou em mais de um julgamento, nenhum ministro deu respostas opostas à mesma questão diante de fatos e acusações equivalentes. A hipótese não é corroborada; com poucas comparações possíveis, o resultado é ausência de evidência de instabilidade, e não prova de estabilidade.

---

## Comece por aqui

| Se você quer… | Abra |
|---|---|
| entender cada tabela e cada campo | [`docs/DICIONARIO.md`](docs/DICIONARIO.md) |
| ver como cada etapa foi feita e verificada | [`docs/METODO.md`](docs/METODO.md) |
| ver as categorias e regras de leitura da fundamentação | [`docs/CODEBOOK.md`](docs/CODEBOOK.md) |
| usar o banco de casos, réus e votos | [`dados/derivados/`](dados/derivados/) (`1_casos.psv`, `2_casos_reus.psv`, `3_votos.psv`) |
| usar a leitura da fundamentação | [`dados/metodologia/fase4/consolidado/`](dados/metodologia/fase4/consolidado/) |
| ler um acórdão | [`dados/corpus/texto/`](dados/corpus/texto/) |
| ver os prompts usados | [`dados/metodologia/prompts_lotes/`](dados/metodologia/prompts_lotes/) e [`dados/metodologia/fase4/prompts_lote/`](dados/metodologia/fase4/prompts_lote/) |

## Estrutura

```
docs/                      dicionário de dados, método e codebook
dados/
├── brutos/                capturas do portal do STF: censo, complemento, export de acórdãos
├── corpus/
│   ├── texto/             texto integral dos 25 acórdãos, com marcação de página
│   └── …                  manifesto de download e scripts de download, extração e OCR
├── derivados/             o banco (casos, réus, votos, referências) e a análise descritiva
│   └── casos/             um JSON por caso, com evidência; _dupla/ e _reteste/
└── metodologia/           protocolos, prompts, scripts de construção e validação, relatórios
    ├── prompts_lotes/     prompts da extração do banco
    ├── reteste/           teste-reteste cego da extração
    └── fase4/             leitura da fundamentação: codebook, contrato, prompts,
                           leituras A e B, base consolidada e congelada, análise
```

Os arquivos `.psv` são texto UTF-8 separado por barra vertical (`|`). Em Python: `csv.DictReader(open(caminho, encoding="utf-8"), delimiter="|")`, ignorando as linhas iniciadas por `#`.

## Como reproduzir

Requer Python 3.9 ou superior. Os scripts de construção e análise usam só a biblioteca padrão.

```bash
cd dados/metodologia
python3 build_l3.py              # casos/*.json → 1_casos, 2_casos_reus, 3_votos
python3 analise_descritiva.py    # → derivados/analise_descritiva.md
python3 concordancia_kappa.py    # concordância da dupla extração (κ de Cohen, α de Krippendorff)
python3 validacao_gabarito.py    # acerto contra a conferência humana
python3 fase4/consolidar_fase4.py fase4/extracao/lote/A fase4/extracao/lote/B \
    fase4/extracao/lote/outra_polaridade_pareamento.psv \
    ../derivados/2_casos_reus.psv ../derivados/1_casos.psv /tmp/consolidado
python3 fase4/analise_fase4.py fase4/consolidado ../derivados/1_casos.psv /tmp/analise_fase4.md
```

Os quatro primeiros regravam os arquivos do próprio repositório; se a reprodução for exata, `git status` continua limpo. Os dois últimos escrevem em `/tmp`, para comparação com a base congelada (`fase4/consolidado/`) e com `fase4/analise/resultados_preliminares_fase4_v2.md`. Todos foram testados a partir de uma cópia limpa deste repositório e reproduzem os arquivos publicados byte a byte.

Repetir a leitura com um modelo de linguagem não é necessário para reproduzir a análise, porque as leituras estão congeladas. Os prompts estão publicados para quem quiser repeti-la, sabendo que modelos proprietários mudam com o tempo e que o resultado precisa ser medido de novo.

## O que não está aqui

- **PDFs dos acórdãos.** São públicos no portal do STF, e o da AP 470 (114 MB) excede o limite do GitHub. O `dados/corpus/manifesto_acordaos.psv` traz a rota e o identificador de cada um: `https://redir.stf.jus.br/paginadorpub/paginador.jsp?docTP={doctp}&docID={docid}`. Use a rota indicada: a errada devolve uma página de 63 bytes sem sinalizar erro.
- **Transcrições das sessões de trabalho com o modelo**, que misturam o trabalho com outros assuntos. O que delas importa para a replicação, o prompt de cada etapa e o modelo usado, está publicado.
- **Registros internos de gestão do projeto**: decisões, planos e itens de revisão. Os documentos de método citam esses registros pelos códigos `D-NNN` e `G4-NN`; o conteúdo metodológico de cada decisão está na Metodologia do trabalho.

## Alterações em relação ao material de trabalho

- A pasta de dados do projeto aparece aqui como `dados/`, e os caminhos absolutos da máquina do autor foram convertidos em caminhos relativos.
- No texto do acórdão da AP 470, cinco endereços de e-mail de pessoas físicas, transcritos de provas dos autos, foram substituídos por `[e-mail omitido]`.
- Ficaram de fora as versões superadas: a primeira consolidação da leitura da fundamentação, anterior à inclusão da AP 307, e os rascunhos de contrato.

## Dados pessoais

Os nomes de réus e ministros constam de decisões públicas do STF e são necessários à análise, que compara votos de ministros e julgamentos do mesmo réu. Nenhum dado foi obtido fora dos acórdãos e do índice de jurisprudência do portal.

## Licença

Código sob licença MIT; dados, textos e documentação sob Creative Commons Atribuição 4.0 Internacional (CC BY 4.0). Os textos dos acórdãos são documentos públicos do STF. Ver [`LICENSE`](LICENSE).

## Como citar

> BRAGA BALDIN, F. **Suprema Incerteza**: uma análise da estabilidade decisória do STF em casos de corrupção sob a ótica da economia institucional. 2026. Trabalho de Conclusão de Curso (Graduação em Ciências Econômicas) – Insper, São Paulo, 2026. Dados e código disponíveis em: https://github.com/FeBraga07/suprema-incerteza.

Ver também [`CITATION.cff`](CITATION.cff).
