# Classificação das 105 ações penais do Plenário pelo Quadro 1.1 de Levcovitz

> Executada em **08/08/2026**, sob o `PROTOCOLO_CLASSIFICACAO.md`, escrito antes de qualquer caso ter sido olhado.
> Registro linha a linha em `dados/derivados/classificacao_105.psv`.
> Este documento é matéria-prima direta da seção **Seleção dos Casos**.

---

## 1. Resultado

| | Casos |
|---|---|
| Universo do censo (AP puras, Plenário, 1991-2024) | **105** |
| Incluídos como casos de corrupção | **24** |
| Excluídos | **81** |
| Não classificáveis pelas fontes disponíveis | **0** |

**Relatório de sensibilidade** (conforme decidido junto com D-013):

| Cenário | n | Casos que mudam |
|---|---|---|
| Com DL 201/67 (D-013 vigente) | **24** | — |
| Sem DL 201/67 (leitura estritamente literal do Quadro 1.1) | **17** | saem AP-426, AP-409, AP-503, AP-441, AP-416, AP-432, AP-973 |

O universo final é, portanto, **24 casos**, com **17** como piso defensável sob a leitura mais restritiva possível. A estimativa prévia do censo — "~24" — acertou o número, mas por um caminho errado: a composição não é a que ela supunha (ver §3).

### Os 24 casos incluídos

| AP | Julgamento | Modalidade(s) do Quadro 1.1 |
|---|---|---|
| AP-375 | 2004-10-27 | 1 — peculato (art. 312) · 5 — emprego irregular de verbas (art. 315) |
| AP-365 | 2006-03-30 | 1 — peculato (art. 312) |
| AP-348 | 2006-12-15 | 18 — Lei de Licitações (art. 89) |
| AP-430 | 2008-08-07 | 18 — Lei de Licitações (art. 90) |
| AP-426 | 2008-12-18 | 5 — equivalente (DL 201/67, art. 1º III) |
| AP-447 | 2009-02-18 | 10 — prevaricação (art. 319) · 19 — improbidade (Lei 8.429/92) |
| AP-433 | 2010-03-11 | 18 — Lei de Licitações (arts. 91 e 92) |
| AP-409 | 2010-05-13 | 5 — equivalente (DL 201/67, art. 1º IV) |
| AP-503 | 2010-05-20 | 5 — equivalente (DL 201/67, art. 1º IV e V) |
| AP-396 | 2010-10-28 | 1 — peculato (art. 312) |
| AP-372 | 2010-12-16 | 1 — peculato (art. 312) |
| AP-527 | 2010-12-16 | 18 — Lei de Licitações (art. 89) |
| AP-441 | 2012-03-08 | 5 — equivalente (DL 201/67, art. 1º V) |
| AP-416 | 2012-03-08 | 1 — equivalente (DL 201/67, art. 1º I e II) |
| AP-470 | 2012-12-17 | 1 · 8 — corrupção passiva (art. 317) · 15 — corrupção ativa (art. 333) |
| AP-565 | 2013-08-08 | 18 — Lei de Licitações |
| AP-432 | 2013-10-10 | 1/5 — equivalente (DL 201/67, art. 1º II) |
| AP-465 | 2014-04-24 | 1 · 8 — corrupção passiva (art. 317) |
| AP-508 | 2021-08-03 | 8 · 10 · 18 |
| AP-973 | 2021-09-29 | 1 — equivalente (DL 201/67, art. 1º I e II) |
| AP-940 | 2022-04-04 | 1 — peculato-desvio (art. 312) · 19 — improbidade (Lei 8.429/92) |
| AP-1032 | 2022-04-22 | 8 — corrupção passiva (art. 317) |
| AP-1025 | 2023-05-31 | 8 — corrupção passiva (art. 317) · 18 — Lei de Licitações (art. 90) |
| AP-1036 | 2023-09-25 | 8 — corrupção passiva (art. 317) · 15 — corrupção ativa (art. 333) |

---

## 2. Método efetivamente aplicado

**Insumo.** O campo `ementa_trecho` do PSV do censo está truncado em **118 caracteres no máximo** — é rótulo de triagem, não ementa. Nove dos 105 casos não nomeavam tipo penal algum nesse campo. A classificação foi feita sobre o **`ementa_texto` integral** (458.249 caracteres no total) e, para todos os 53 casos fora do bloco antidemocrático, também sobre o **`acordao_ata`**. Ambos recuperados pela consulta documentada em `censo_2026-08-08.md` §3, em três chamadas ao endpoint.

**Regra de leitura.** Nenhuma decisão de inclusão ou exclusão foi tomada por correspondência de padrão sobre o texto. Padrões foram usados apenas para *localizar* e para *agrupar*, nunca para decidir — a mesma disciplina que `DECISOES.md` D-003 impõe ao placar, aqui estendida à classificação.

**Bloco antidemocrático.** 52 dos 105 casos são ações penais dos atos antidemocráticos. Verificou-se que se reduzem a **três redações-template** mais **cinco casos singulares**:

| Template | Casos | Conteúdo |
|---|---|---|
| 1 — "propagação de ideias contrárias à ordem constitucional" | 36 | art. 359-L do CP e correlatos |
| 2 — "acampamento ilegal em frente a quartel-general" | 11 | art. 288 (associação criminosa) e art. 286 par. ún. (incitação) |
| singulares | 5 | AP-1044, AP-1147, AP-1423, AP-1373, AP-2493 |

A identidade dos templates foi verificada por comparação literal dos 300 primeiros caracteres, o que torna a amostra de auditoria do §7 do protocolo **principiada, não arbitrária**: um exemplar de cada template mais os cinco singulares foram lidos individualmente; os demais recebem justificativa padronizada com identidade de redação demonstrável.

Todos os 52 foram excluídos pela regra de desempate do §4: o bem jurídico lesado é a ordem constitucional, e os réus não são agentes públicos agindo em razão da função.

---

## 3. Quatro achados que o censo não previu

O censo projetava `26 coletados − 4 contaminados + 2 ausentes = ~24`. A classificação cega chegou ao mesmo número por um caminho diferente: **26 − 6 + 4 = 24**. O total coincide; a composição, não. Dois dos casos que o censo dava por bons saem, e dois que ele não viu entram.

### 3.1 AP-296 é falso positivo — crime eleitoral, não calúnia comum

A ementa fala em *"intenção de caluniar evidenciada"*, o que sugere calúnia do art. 138 do CP. **A ata revela condenação pelo art. 324 c/c art. 327, II, do Código Eleitoral.** Crime eleitoral é exclusão explícita de Levcovitz (p. 21). O caso estava no banco desde a primeira coleta.

### 3.2 AP-462 é falso positivo — bem jurídico previdenciário

Art. 297 §4º do CP, omissão de informações na GFIP do INSS por prefeito municipal. Não consta do Quadro 1.1, e o bem jurídico é a arrecadação previdenciária — exatamente a categoria que Levcovitz exclui (p. 21). Estava no banco.

### 3.3 AP-503 é uma terceira ausência, não detectada pelo censo

O censo identificou duas ausências (AP-430 e AP-527). Há uma terceira: **AP-503**, julgada em 20/05/2010, relator Celso de Mello, com **condenação** pelo DL 201/67 art. 1º, incisos IV e V — emprego de recursos em desacordo com o programa a que se destinavam e realização de despesas não autorizadas. Entra por D-013.

### 3.4 AP-426 é uma quarta ausência — e só foi decidida pela legislação citada

**AP-426**, julgada em 18/12/2008, relator Marco Aurélio, revisora Ellen Gracie. Réu: ex-prefeito de Curitiba. Foi o único caso que a ementa e a ata não permitiram classificar (ver §4), e por isso ficou pendente na primeira versão deste documento. Resolvida em 08/08/2026 pelo campo `documental_legislacao_citada_texto`: **DL 201/67, art. 1º, inciso III**, com absolvição por ausência de dolo (art. 18, par. ún. do CP; art. 386, IV do CPP). Entra por D-013.

**Consequência.** O banco perde 6 dos 26 casos (os 4 do 8 de janeiro mais AP-296 e AP-462) e ganha 4 (AP-430, AP-527, AP-503 e AP-426).

---

## 4. A ementa não é fonte suficiente para classificar — a ata é

O achado metodológico mais consequente da etapa.

**AP-508** tem ementa de **164 caracteres**: *"Ação penal originária. Extinção da punibilidade do agente em razão da prescrição. Absolvição por insuficiência de provas. Presunção de inocência e in dubio pro reo."* Nenhum crime é nomeado. A ata registra que o julgamento versou sobre os **arts. 288, 319 e 317 do Código Penal e o art. 92 da Lei 8.666/93** — três modalidades do Quadro 1.1 num único caso.

Classificar AP-508 pela ementa produziria um **falso negativo**: a perda de um caso de corrupção por insuficiência do texto indexado. É o mesmo modo de falha que `DECISOES.md` D-001 diagnosticou na busca por palavra-chave — o critério sendo terceirizado a quem redigiu a ementa — reproduzido em escala menor dentro do próprio censo.

O mesmo mecanismo, em sentido inverso, produziu os dois falsos positivos do §3: em AP-296 e AP-481 a ementa induz a uma tipificação que a ata desmente.

**Regra que decorre disso, a incorporar ao protocolo:** sempre que a ementa não nomear expressamente o tipo penal *e o diploma*, a ata é consultada antes de qualquer decisão. Nesta etapa a ata foi consultada para os 53 casos relevantes, o que tem o efeito colateral útil de já pré-carregar o insumo da Fase 2.

---

## 5. Correções a documentos anteriores

### 5.1 "55 do 8 de janeiro" está errado — são 51 (ou 52)

O censo (§5.2) e o protocolo (§3) afirmam que 55 dos 105 casos são do 8 de janeiro. A contagem sobre o texto das ementas dá **51** casos de atos antidemocráticos de 8/1, mais **AP-1044** — que é de **20/04/2022**, anterior ao 8 de janeiro, e trata de deputado federal condenado por propagação de ideias contrárias à ordem constitucional. Total de 52 no sentido amplo, 51 no sentido estrito.

A exclusão de AP-1044 se dá pelo mesmo fundamento, mas ela **não pode ser descrita como caso do 8 de janeiro** em nenhum texto do TCC.

### 5.2 A causa alegada em D-010 não se confirma nas ementas

`DECISOES.md` D-010 e o §3 do protocolo afirmam que os quatro falsos positivos entraram na coleta original *"pela busca 17"* — `(subtração ou inutilização) e (livro ou documento) e 337`. **Nenhuma das quatro ementas menciona o art. 337.**

- **AP-1147** — art. 163, par. ún., I-IV do CP (dano qualificado) e art. 62, I, da Lei 9.605/98 (patrimônio tombado);
- **AP-2493** — art. 23, IV c/c art. 18 da Lei 7.170/83 (abolição violenta) e art. 138 do CP (calúnia);
- **AP-1075** e **AP-1179** — template 1, propagação de ideias contrárias à ordem constitucional.

**A decisão de excluir os quatro continua correta e reforçada.** O que não se sustenta é a *causa* atribuída à entrada deles. A hipótese remanescente é que o casamento tenha ocorrido pelo campo de indexação, não pela ementa — o campo `indexacao` veio vazio no índice para os casos testados, o que não permite nem confirmar nem descartar. **Recomendação: reescrever a justificativa de D-010 sem afirmar o mecanismo, ou verificá-lo antes de afirmá-lo.** É um ponto pequeno, mas está escrito num documento que vai à banca.

---

## 6. Aplicação do D-012 (lavagem e organização criminosa)

Nenhum caso do universo entrou ou saiu por conta do D-012 — confirmando a previsão feita antes da decisão. **Não existe, entre os 105, nenhum caso de lavagem ou organização criminosa isolada, sem crime do Quadro 1.1 acoplado**, que é a única hipótese em que o cenário escolhido morderia. A questão do §6 do protocolo fica, portanto, resolvida sem custo analítico.

Casos com as variáveis marcadas: lavagem em AP-470, AP-1032 e AP-1025; organização/associação criminosa em AP-396, AP-470, AP-565, AP-508 e AP-1025.

---

## 6-bis. A terceira fonte: `documental_legislacao_citada_texto`

Descoberto ao investigar a AP-426, é o campo do índice que lista a legislação citada no acórdão em formato normalizado (`LEG-FED DEL-000201 ANO-1967 ART-00001 INC-00003`). Não substitui a leitura — inclui dispositivos processuais (art. 386 do CPP), de parte geral (art. 18 do CP) e legislação apenas contextual —, mas é **uma quarta via de verificação, independente da ementa e da ata**, e em formato estruturado.

Aplicado aos 29 casos relevantes, **confirmou integralmente a classificação já feita** e acrescentou:

- **AP-447** e **AP-940** — arts. 9º e 11 da Lei 8.429/1992, que é a **modalidade 19** do Quadro 1.1 (a única das 19 que nenhum caso havia acionado até então);
- **AP-1025** — art. 90 da Lei 8.666/93 (modalidade 18), além da corrupção passiva;
- **AP-1036** — art. 333 do CP (modalidade 15, corrupção ativa);
- **AP-426** — a decisão do caso (§3.4).

**Um resultado colateral importante.** A AP-296 cita o **art. 312 do CP** entre a legislação, o que à primeira vista contradiria sua exclusão como crime eleitoral. Não contradiz: a calúnia eleitoral pela qual o réu foi condenado consistiu em **imputar peculato a terceiro**. O art. 312 aparece como *conteúdo da imputação caluniosa*, não como acusação contra o réu — o que explica a exceção da verdade e o *"presume-se a falsidade desta"* da ementa.

Isso é, com alta probabilidade, o mecanismo pelo qual a AP-296 entrou na coleta original: a busca pelo termo "peculato" casou com um caso em que a palavra designa o conteúdo de uma mentira. **É a demonstração concreta e verificável do modo de falha que o D-001 descreve em abstrato**, e vale ser citada nominalmente na seção de metodologia.

---

## 7. Pendências abertas

1. **Reescrever a justificativa de D-010** conforme §5.2.
2. **Corrigir "55" para 51/52** no censo e no protocolo.
3. **Incorporar ao protocolo** a regra do §4 (ata obrigatória quando a ementa não nomeia tipo e diploma) e o campo de legislação citada como quarta fonte (§6-bis).
4. Levar à orientadora, como confirmação e não como pergunta aberta: D-012, D-013 (incluída a extensão ao inciso III) e o relatório de sensibilidade.

**Nenhum caso do universo permanece sem classificação.**
