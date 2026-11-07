# Codebook da Fase 4: `questao_decisiva` e `posicao`

> **Autor:** Felipe Braga. **Status:** **versão 2, 18/10/2026** (gate da Fase 4, D-048; ajustes da consolidação, D-050). A versão 1 foi fechada em 12/10/2026 (D-043) e previa a revisão depois do lote pelas ocorrências de `outra` (§3.3 da v1). O que a v2 acrescenta está marcado com **(v2)** e o item do gate.
> **Origem:** leitura solitária de AP-426, AP-416 e AP-409 (D-033, condição 1), com entrevista depois de cada caso. Folhas e entrevistas em `anotacoes_codebook/`.
> **Divisão do trabalho:** o esqueleto (seções, regras já decididas com a fonte, quadro dos casos) foi montado pela sessão `c81eab04` (`claude-opus-5-5`). **O conteúdo (categorias, definições, critérios) é do Felipe**, escrito ou ditado por ele. A sessão não propôs categoria; onde fez recomendação de forma (nome "concorreu", forma de `posicao`, enquadramento do precedente) e o Felipe aceitou, isso está marcado.
> **Ditado:** a partir de 12/10 à noite, o Felipe respondeu pelo celular e a sessão transcreveu as respostas dele, marcadas com (ditado). Onde a sessão só deu forma a uma ideia dele, isso está dito.

---

## 1. Para que serve



A questão decisiva é a referência objetiva sobre qual a decisão principal a respeito da qual os ministros decidiram. Isso é essencial para comparação entre casos, pois, mesmo com diferentes contextos, pode-se reduzir o julgamento à essa informação, permitindo a comparação de acordo com a metodologia deste trabalho.


---

## 2. Regras de leitura (já decididas)

| # | Regra | Decidida em |
|---|---|---|
| R1 | A questão é escrita **como pergunta comparável**, não como conclusão. Ex.: "houve comprovação de dolo do réu?", e não "o réu agiu sem dolo". | AP-426, 11/10 |
| R2 | **Seguir a linguagem do voto, e não o número do inciso citado**, salvo quando a linguagem for vaga. | AP-426, 11/10 |
| R3 | Se a linguagem for vaga e for preciso recorrer ao inciso, usar a **redação vigente na data da peça que o cita** (parecer ou voto), e não a da data do julgamento. Sem data da peça: data do julgamento e confiança `baixa`. Motivo: a Lei 11.690/2008 renumerou o art. 386 do CPP (o antigo IV, "não existir prova de ter o réu concorrido", passou a ser o V; o novo IV é "estar provado que o réu não concorreu"). | AP-426 e AP-416, confirmada em 12/10 |
| R4 | **Quando duas perguntas decidem, registrar as duas** e marcar uma como principal. | AP-426, 11/10; aplicada a AP-416 e AP-409 em 12/10 |
| R5 | **Pergunta principal = a pergunta em que o resultado se decidiu; havendo divergência, a pergunta em que os votos se separaram.** O critério é onde o placar se separou, não quantos ministros escreveram sobre ela (vale mesmo para quem adere sem texto). | AP-409, 12/10 |
| R5b | **Desempate em caso unânime:** quando não houve divergência e as duas perguntas tiveram a mesma resposta, **as duas são principais** (empate declarado). | Piloto da AP-426, 12/10 (opção A, recomendação da sessão aceita pelo Felipe) |
| R6 | **Preliminares** (ex.: prescrição afastada no início do voto) não são questão decisiva. | AP-409, 12/10 |
| R6b | **Exceção à R6:** quando os votos se separam na própria preliminar (ex.: parte do Plenário declara a prescrição e extingue a punibilidade, parte examina o mérito e absolve), ela é a pergunta principal pela R5. A R6 continua valendo para a preliminar afastada por todos. | AP-465 e AP-508, depois do lote, 13/10 (recomendação da sessão aceita pelo Felipe; D-046) |
| R8 | **Ministro cujo voto só consta da ata** (sem texto no acórdão, ex.: falas canceladas): se a ata o põe de um lado, `enfrentou_a_questao = Adesao` e a posição é a de quem conduz aquele lado (o relator, ou quem abriu a divergência quando a ata os nomeia juntos), com `confianca = baixa` e a página da ata em `inferida_de`. Foi o que o Felipe fez com Celso de Mello na AP-409 ("Adesão sem texto", folha da AP-409). | Depois do lote, 13/10 (D-046) |
| R6c | **Unidade só com prescrição:** quando a única questão enfrentada é a prescrição, declarada por todos, a unidade fica **sem questão decisiva** (não há posição de mérito a comparar); continua no banco e na descritiva. | Depois do lote, 13/10 (AP-508; D-046, item 4b) |
| R9 | **Direção das perguntas `outra`:** a pergunta segue a linguagem do voto (R2), e cada uma leva a marca `sim_favorece` = `acusacao` / `defesa` / `neutra`. Contagem e concordância usam a marca, de modo que "sim" signifique sempre "o elemento da acusação está presente", como em `dolo` e `concorreu`. Pergunta dupla ("A ou B?") é lida pelo primeiro ramo. | Depois do lote, 13/10 (AP-503; D-046, item 2; opção (ii), recomendação da sessão aceita pelo Felipe) |
| R7 | A **competência do agente para o ato** é parte da pergunta de participação/autoria, não uma pergunta separada. | AP-416, 11/10 (revisa a leitura inicial da AP-426) |
| R10 **(v2)** | **Questão declarada prejudicada** pelo voto condutor não é questão decisiva: sai da unidade e não entra na R5b. | Gate, 18/10 (G4-05; AP-348) |
| R11 **(v2)** | **Fundamentou × aderiu**, pelo conteúdo do voto, não pela fórmula: `Sim` = há ao menos um trecho próprio, com página, que responde à questão, mesmo curto e mesmo com "acompanho"; `Adesao` = só declara acompanhar; `Nao` = a razão própria é outra questão (`posicao = nao_enfrentou`, razão em `fundamento_proprio`). | Gate, 18/10 (G4-01) |
| R12 **(v2)** | **Maioria sem fundamento único:** se nenhum fundamento, sozinho, reúne os votos necessários para formar o resultado, as duas questões que o formam são principais; `obs` registra o fundamento do voto condutor e o do desempate. | Gate, 18/10 (G4-19, G4-20); fórmula conferida na consolidação (D-050: dispara na AP-433) |
| R5c **(v2)** | **Empate na separação:** quando as duas questões separam o placar exatamente do mesmo modo, as duas são principais pela R5. | Consolidação, 18/10 (D-050; AP-565, art. 90, 5×5) |
| R13 **(v2)** | **Mesmo fato em duas classificações:** as duas unidades são fundidas quando todos os ministros votam igual nas duas; ficam separadas quando os votos se separam. | Gate, 18/10 (G4-07; funde AP-372, mantém AP-441) |
| R14 **(v2)** | **Unidade que junta fatos decididos de modo diferente** é desdobrada por fato (contrato §1). | Gate, 18/10 (G4-06; AP-432, AP-940, AP-1025) |
| R15 **(v2)** | **`modo_concurso` em réu absolvido:** quando a resposta a `concorreu` é "não", fica `nao_dito`; o modo imputado pela denúncia, se houver, vai em `obs`. | Gate, 18/10 (G4-18) |
| R16 **(v2)** | **Voto sem mérito:** `voto_resultado` admite `Extingue` (extinção da punibilidade) e `Tranca` (trancamento, HC de ofício), além de `Condena`/`Absolve`; esses votos ficam fora da comparação de posição no mérito. O banco (`3_votos`) continua binário. | Gate, 18/10 (G4-08) |
| R17 **(v2)** | **Ata e texto em conflito:** o resultado do voto vem da ata; a fundamentação vem do texto. | Gate, 18/10 (G4-24, coerente com a D-042) |

---

## 3. Categorias de `questao_decisiva`

Uma ficha por categoria. Os exemplos (caso e página) vêm das suas folhas; o resto é seu.

### 3.1 Categoria: Dolo

- **Pergunta-padrão:** "Há comprovação de dolo do réu?" (ditado; substitui "É possível provar o dolo do réu?", porque a pergunta é sobre o que ficou provado, não sobre o que seria possível)
- **Definição:** Se há provas de que o réu agiu com dolo em relação aos itens da denúncia. **O tipo de dolo exigido (genérico ou específico) não é fixado pelo codebook:** depende do tipo penal, e os próprios votos dizem qual exigem (ex.: AP-409, revisor, p. 55: "exige-se apenas o dolo simples ou genérico"). O extrator registra o padrão que o voto exige, quando o voto disser. (ditado)
- **Quando aplicar:** Quando os votos usam como base a questão do dolo, segundo a linguagem do voto (R2). O inciso citado só entra quando a linguagem for vaga (R3). (ditado; a versão anterior, "quando os incisos citados fazem referência a dolo", contrariava a R2)
- **Quando NÃO aplicar:** Quando a argumentação do voto vai para outra direção, ela se encaixa em outra categoria. Ex.: na AP-409 discute-se o dolo e a materialidade, mas a divergência dos ministros que julgam a ação improcedente é de autoria: eles discutem algo que não é dolo. (ditado)
- **Respostas possíveis:** Sim ou não. A suficiência de prova não é categoria: é o modo de responder (precisa haver prova que comprove o dolo). (ditado)
- **Exemplos das suas folhas:** AP-426, fato 1 (p. 4) e fato 2 (p. 5); AP-416 (pp. 24, 2 [ementa, item 7]); AP-409 (relator p. 29 e p. 36; revisor p. 55).

### 3.2 Categoria: Autoria/participação (`concorreu`)

- **Pergunta-padrão:** "Há comprovação de que o réu concorreu para o fato denunciado?" (ditado como "comprovação da autoria do réu sobre o fato denunciado"; a redação com "concorreu" segue o art. 29 do CP e o art. 386 do CPP, recomendação da sessão aceita pelo Felipe em 12/10)
- **Definição:** Se há provas de que o réu concorreu para o fato, como **autor** (praticou ou decidiu o ato) ou **partícipe** (ajudou, instigou ou concorreu de outro modo). Inclui a **competência do agente para o ato** (R7). Autoria e participação são **uma categoria só**: quando o voto disser se foi como autor ou como partícipe, isso vira anotação, não outra categoria; assim AP-426, AP-416 e AP-409 continuam comparáveis. A **anuência** (saber e concordar) fica no **dolo** (§3.1), como na folha da AP-409. (decidido em 12/10, recomendação da sessão aceita pelo Felipe)
- **Quando aplicar:** Quando os votos usam como base a questão de quem fez ou decidiu o ato (espelho do 3.1). (ditado)
- **Quando NÃO aplicar:** Quando a argumentação do voto vai para outra direção, como o dolo (se o réu sabia e quis). (ditado, espelho do 3.1)
- **Respostas possíveis:** Sim ou não. (ditado)
- **Anotações de prova (v2, G4-04 e G4-17):** a suficiência de uma prova específica não é categoria (§3.1), mas fica marcada para poder contar: `prova_colaboracao` (corroboração da palavra do colaborador premiado, art. 4º, §16, da Lei 12.850/2013; AP-1025, AP-1032, AP-1036) e `prova_inquerito` (art. 155 do CPP; AP-973).
- **Exemplos das suas folhas:** AP-426, fato 1 (p. 4, "agente público com competência para a prática do ato"); AP-416 (p. 28); AP-409 (relator pp. 32–33; Toffoli pp. 68 e 71; Gilmar pp. 81 e 88).

### 3.3 Categoria: Tipicidade (`tipicidade`) **(v2)**

> Gate de 18/10 (G4-02). Ficha redigida pela sessão no formato das fichas acima e aprovada pelo Felipe sem alteração. Na v1, esta seção dizia: "Nenhuma nos três casos lidos [...] Pode haver outras no resto do corpus; elas entram por `outra` e revisão do codebook depois do lote." Foi o que aconteceu: as duas leituras do lote sugeriram, sem combinar, esta categoria em pelo menos 12 casos.

- **Pergunta-padrão:** "O fato provado preenche os elementos do tipo imputado?"
- **Definição:** se a conduta, tal como provada, se enquadra no crime da denúncia, incluindo se o fato material existiu. A anotação diz qual das duas é a dúvida: `existencia_fato` (o fato existiu?) ou `enquadramento` (o fato provado é este crime?), na mesma lógica de autor e partícipe em `concorreu`.
- **Quando aplicar:** quando o voto discute uma elementar do tipo (ex.: "proveito próprio ou alheio" no peculato; "durante a execução do contrato" no art. 92 da Lei 8.666/1993; "ordem judicial" no art. 1º, XIV, do DL 201/67) ou a existência do fato.
- **Quando NÃO aplicar:** quando a dúvida é quem fez (`concorreu`), se o réu sabia e quis (`dolo`), prescrição ou questão processual.
- **Respostas possíveis:** sim ou não; o sim favorece a acusação (R9).

### 3.4 Categoria: Ato de ofício (`ato_de_oficio`) **(v2)**

> Gate de 18/10 (G4-03). Categoria própria, e não parte de `tipicidade`, porque é a pergunta formulada nos mesmos termos em AP 307 (1994), AP-470 (2012) e AP-1025 (2023).

- **Pergunta-padrão:** "A corrupção se configura sem ato de ofício determinado, bastando o nexo com a função?" (na direção da acusação, como as demais)
- **Quando aplicar:** quando o voto decide se a condenação por corrupção exige um ato de ofício identificado ou se basta o nexo da vantagem com as atribuições do cargo.
- **Respostas possíveis:** sim ou não; o sim favorece a acusação.
- **Ocorrências no lote:** AP-470, item VI (7 unidades). Na AP-1025 o debate aparece nos precedentes citados (AP 307 × Inq 4.506), não como pergunta própria (D-050).

### 3.x `outra`

Para o que o codebook não previr: o extrator escreve `outra` e descreve a questão em texto livre, com evidência. É por aí que o codebook é revisado depois do lote (contrato, §2).

---

## 4. Forma de `posicao`

Onde cada ministro se situa na questão decisiva (contrato, §3).

**Decidido em 12/10 (recomendação da sessão aceita pelo Felipe):** `posicao` é como cada ministro respondeu à **pergunta principal**, com três valores: `sim` / `nao` / `nao_enfrentou`. Um campo de texto curto e opcional, `posicao_detalhe`, guarda o desdobramento (qualidade da prova, ressalvas). Motivo: valores contáveis permitem ver quem se separou de quem e medir a concordância entre leitores; uma escala com graus exigiria definir cada grau e reduziria a concordância.

Com `enfrentou_a_questao` (contrato): `Sim` = fundamentou; `Adesao` = acompanhou sem fundamentar, e a posição é **inferida da adesão, não lida** (D-039, validada em 12/10); `Nao` = votou por outra razão.

---

## 5. Precedente

Tipos do contrato (§4): `precedente_citado`, `mudanca_lei`, `mudanca_jurisprudencia`, `distincao`, `superacao`; sentido `para_seguir` / `para_afastar`.

Exemplos das suas folhas:
- **AP-447** citada **para seguir** na AP-416 ("era um caso exatamente idêntico a este", p. 29) e **para distinguir** pelo relator da AP-409 (p. 25).
- **Inq 2.027**: Toffoli invoca o **próprio voto** para mostrar coerência (AP-409, pp. 68–69).

**Decidido (ditado, 12/10):** conta como precedente. Toffoli usa o próprio voto anterior para justificar a coerência dele: "já votei um caso que considero similar e agi dessa forma; por isso vou agir da mesma forma agora". Registro: `tipo = precedente_citado`, `sentido = para_seguir`, com a anotação "precedente do próprio ministro" (e, quando for o caso, "em inquérito"). O enquadramento nos tipos do contrato é forma dada pela sessão.

---

## 6. Pontos em aberto (decidir ao escrever)

1. ~~Precedente do próprio ministro, em inquérito~~ **Resolvido em 12/10:** conta (§5).
2. ~~Suficiência de prova~~ **Resolvido em 12/10:** é o modo de responder, não categoria (§3.1). Na AP-416 a primeira formulação foi "há provas que comprovam a denúncia?", e depois ficou "ausência de provas em relação ao dolo".
3. ~~Uma só definição de dolo~~ **Resolvido em 12/10:** o codebook não fixa o tipo de dolo; registra-se o padrão que o voto exige (§3.1). Na AP-409, o relator usa duas formulações: "empregar recursos… em desacordo com a destinação" (p. 29) e "lesar o interesse público" (p. 36). O revisor exige só o dolo genérico, "não se reclamando qualquer finalidade específica" (p. 55).
4. ~~Nome único para influência / participação / autoria~~ **Resolvido em 12/10:** uma categoria, "concorreu" (§3.2).

---

## 7. Os três casos de origem

| Caso | Ano | Placar | Pergunta principal | Segunda pergunta | Resposta (principal) |
|---|---|---|---|---|---|
| AP-426 (2 fatos) | 2008 | 11×0, absolvição | dolo e concorreu (empate, R5b; na leitura original, dolo) | — | não |
| AP-416 | 2012 | 9×0, absolvição | dolo e concorreu (empate, R5b; na leitura original, dolo) | — | não |
| AP-409 | 2010 | 7×3, condenação | concorreu (autoria; onde o placar se separou) | dolo (ciência e anuência do prefeito) | sim |
