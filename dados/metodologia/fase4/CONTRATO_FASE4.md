# Contrato de extração da Fase 4 (versão 1, aprovada)

> **Status:** **aprovado pelo Felipe em 12/10/2026** (D-044). Substitui `CONTRATO_FASE4_rascunho.md` (27/09), que fica como histórico. Os valores de `questao_decisiva` e `posicao` vêm do `CODEBOOK.md` versão 1 (D-043).
> **Redação:** sessão `c81eab04`, `claude-opus-5-5`, a partir do rascunho e do codebook.

## 1. Unidade

Uma unidade é **réu × fato**. O ponto de partida é `unidades_reu_fato.psv` (130 unidades = réu × imputação). Escopo da Fase 4 pela D-040: os 23 casos sem a AP-470 e, da AP-470, só R14–R23 (corrupção passiva, item VI). O extrator pode:
- **desdobrar** uma imputação em vários fatos quando o acórdão os decide separadamente: novos ids `…-I01a`, `…-I01b`;
- **juntar** imputações que o acórdão decide como um só ponto.

Nos dois casos, o motivo vai com evidência literal em `ajuste_unidade`. Unidade fora do escopo Levcovitz continua na tabela, com `escopo_levcovitz = Nao` (D-022, D-029 b).

## 2. Regra de evidência

Todo campo segue `{valor, evidencia, fonte, confianca}`. `evidencia` é transcrição literal; `fonte` é a página do PDF, na convenção dos marcadores `===== [página N/M] =====` do `.txt`; `confianca` é `alta | media | baixa`.

**Sem evidência literal com página, o campo fica vazio (`valor = null`), nunca inferido.** Única exceção: `enfrentou_a_questao = Adesao`, cuja `posicao` é inferida da adesão e declarada como tal (D-039). Origem da regra: os 20 votos de Peluso inferidos sem evidência na AP-470 (D-041).

## 3. Campos por unidade

| Campo | Valor | Observação |
|---|---|---|
| `id_unidade` | de `unidades_reu_fato.psv` | |
| `escopo_levcovitz` | `Sim` / `Nao` | |
| `ajuste_unidade` | vazio / `desdobrada` / `juntada` + justificativa | |
| `voto_condutor` | ministro | quem **fundamenta** a razão de decidir, segundo o texto; se o acórdão atribuir a outro (ex.: AP-426, "nos termos do voto da revisora", que só adere), registra-se quem fundamenta, e a atribuição do acórdão vai em `obs` (correção do piloto, 12/10) |
| `questoes` | lista de 1 ou 2 | ver §4 |
| `obs` | texto curto | |

## 4. Questões decisivas, por unidade (codebook §2–§3)

Até duas (R4). Para cada uma:

| Campo | Valor | Observação |
|---|---|---|
| `questao_decisiva` | `dolo` / `concorreu` / `outra` | codebook §3 |
| `questao_outra_descricao` | texto curto | só quando `outra`: a pergunta em forma comparável (R1) |
| `principal` | `Sim` / `Nao` | R5: a pergunta em que o resultado se decidiu; havendo divergência, aquela em que os votos se separaram. Uma `Sim` por unidade, **salvo o empate da R5b** (caso unânime, duas perguntas com a mesma resposta: as duas `Sim`) |
| `formulacao` | transcrição literal | a questão como o voto condutor a formula |
| `resposta_tribunal` | `sim` / `nao` | a resposta da maioria à pergunta |
| `padrao_dolo_exigido` | `generico` / `especifico` / `nao_dito` | só quando `dolo`: o que o voto diz que o tipo penal exige |
| `modo_concurso` | `autor` / `participe` / `nao_dito` | só quando `concorreu`, quando o voto disser |
| `posicoes` | lista por ministro | ver §5 |

## 5. Posição de cada ministro, por questão

Uma entrada por ministro votante, **para cada questão da unidade** (não só a principal):

| Campo | Valor | Observação |
|---|---|---|
| `ministro` | nome como grafado em `3_votos.psv` | |
| `voto_resultado` | `Condena` / `Absolve` | **conferência**: tem de bater com `3_votos.psv`; divergência é sinalizada, não corrigida |
| `enfrentou_a_questao` | `Sim` / `Adesao` / `Nao` | `Adesao` = acompanhou sem fundamentar; `Nao` = votou por outra razão |
| `posicao` | `sim` / `nao` / `nao_enfrentou` | como o ministro respondeu à pergunta (codebook §4) |
| `posicao_detalhe` | texto curto, opcional | qualidade da prova, ressalvas |
| `fundamento_proprio` | texto curto ou vazio | quando chega ao mesmo resultado por outra questão |

## 6. Precedente e mudança de regra, por unidade

Lista, possivelmente vazia:

| Campo | Valor |
|---|---|
| `ministro` | quem invocou |
| `tipo` | `precedente_citado` / `mudanca_lei` / `mudanca_jurisprudencia` / `distincao` / `superacao` |
| `referencia` | processo ou diploma, como aparece no texto |
| `sentido` | `para_seguir` / `para_afastar` |
| `proprio_ministro` | `Sim` / `Nao`: o ministro cita voto seu anterior (codebook §5) |
| `evidencia`, `fonte` | como sempre |

`distincao` e `superacao` ficam separados: o STF costuma mudar de posição distinguindo o caso anterior, e não declarando a superação.

## 7. Disciplina (D-033, condição 2)

- Piloto na AP-426, comparado com a leitura do Felipe, antes do lote.
- Dupla leitura independente (A/B) nos 7 casos do DL 201/67 e nos réus recorrentes (14 casos, 43 unidades); passada única no resto.
- Concordância com κ por campo (`concordancia_fase4.py`), com gate humano sobre as divergências.
- Modelo fixado explicitamente em cada agente e registrado no `REGISTRO_EXECUCAO.md`.
- Proibido: regex para resultado ou posição; preencher campo sem evidência literal; resumir o acórdão.

## 8. Ainda aberto (não afeta a extração)

- Superação declarada e fundamentada conta como insegurança jurídica? Muda a análise, não a extração. Até ~19/10.
