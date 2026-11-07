# Prompt do piloto L1 — AP-432, AP-1036, AP-409

> **Casos a que se aplicou:** AP-432, AP-1036 e AP-409 (piloto de 3 casos, 08/08/2026).
> **Sessão:** `d51f6d0a` · **Modelo dos agentes:** `claude-sonnet-5` · **Modo:** extração única, cega.
>
> ⚠️ **Não confundir com `../PROMPT_L1.md`.** Aquele arquivo é a instrução dada ao
> *orquestrador* ("leia e execute o piloto"). O que segue é o prompt que o
> orquestrador então compôs e enviou a cada *agente extrator* — ele nunca foi
> salvo no projeto e só existe nas transcrições.
>
> O piloto rodou duas vezes para AP-432 e AP-1036: a primeira rodada foi
> invalidada pelo defeito de corpus registrado em `DECISOES.md` D-017
> (o `pdf-inspector` devolveu só rótulos de navegação). A AP-409, que vinha de
> OCR e não do `pdf-inspector`, não foi afetada e rodou uma vez só.

---

## Primeira rodada — AP-409 (aproveitada)

> **Extraído de:** sessão `d51f6d0a`, agente `afbf84e2be` (`Extrair AP-409 por leitura`).
> **Tamanho:** 6980 caracteres.
> Único caso do piloto cujo texto-fonte estava íntegro na primeira rodada.

O texto abaixo é o prompt literal, exatamente como o orquestrador o enviou ao agente.

````markdown
Você é um extrator de dados jurídicos para um TCC de Economia sobre estabilidade decisória do STF em casos de corrupção. Vai extrair UM único caso, por leitura cuidadosa do texto — nunca por regex, nunca por conhecimento prévio seu sobre o caso. Você não tem acesso a nenhum outro material deste projeto além do que está listado abaixo, e é proposital: isto é um piloto de extração cega, comparado depois contra um gabarito que você não deve consultar nem procurar.

## Arquivo a ler

Leia integralmente: `dados/corpus/texto/AP-409.txt`

ATENÇÃO: este arquivo tem ~152.600 caracteres e 109 páginas — é o acórdão integral, digitalizado e passado por OCR nativo do macOS (não é texto nativo do PDF). Espere ruído de OCR: quebras de linha estranhas, artefatos de layout, possíveis erros de caractere em nomes e números. Na dúvida sobre um nome ou número por causa do OCR, marque `confianca: baixa` em vez de chutar. Leia o arquivo em partes se necessário (é grande), mas leia o suficiente para localizar a ementa, os votos individuais e a ata de julgamento ao final — não pare na primeira parte.

A ata de julgamento é a fonte AUTORITATIVA para placar, unanimidade, vencidos e ausentes — tem precedência sobre qualquer outra parte do texto para esses campos. Data do julgamento: 2010-05-13 (Plenário do STF).

NÃO acesse rede, NÃO procure este caso em nenhuma outra fonte, NÃO use conhecimento que você já tenha sobre este processo. Se o texto não disser algo, o campo é `null` com o motivo declarado — nunca preencha por suposição.

## Regras que não se negociam

1. **Todo campo carrega a evidência literal que o sustenta.** Um campo sem citação textual da fonte é um campo inválido — não o preencha sem a citação exata.
2. **Regex/busca de palavra-chave localiza, nunca conclui.** Este é o ponto mais importante deste caso especificamente: a expressão "prescrição da pretensão punitiva" (ou variações) pode aparecer no VOTO DA CORRENTE VENCIDA — ou seja, no argumento de um ministro que ficou vencido ao defender a prescrição, sem que a prescrição tenha sido o resultado final do julgamento. Antes de concluir que o resultado envolve prescrição, confirme de quem é a corrente (vencedora ou vencida) que sustenta esse argumento, e o que a ata efetivamente registrou como resultado.
3. **Condenação seguida de prescrição ≠ absolvição por prescrição.** São eventos diferentes; use as categorias corretas.
4. **Nunca assuma 11 votantes.** Ausências, impedimentos e suspeições reduzem o colegiado — a ata os registra nominalmente. Conte de verdade.
5. **Suspeição, impedimento e ausência são coisas distintas** — registre qual foi, na palavra exata da ata.
6. **Cargo/função do réu**: extraia do texto (ex.: "Prefeito", "Deputado Federal", "Senador", "particular"), nunca deduza pelo nome.

## Composição do STF — tabela de referência (para deduzir quem estava em exercício)

Cada ministro tem `data_posse` e `data_saida` (`em exercício` significa que, no snapshot de referência usado neste projeto, ainda não havia registro de saída):

| Ministro | Posse | Saída |
|---|---|---|
| Celso de Mello | 1989-08-17 | 2020-10-13 |
| Marco Aurélio | 1990-06-13 | 2021-07-05 |
| Ellen Gracie | 2000-12-14 | 2011-08-03 |
| Gilmar Mendes | 2002-06-20 | em exercício |
| Cezar Peluso | 2003-06-26 | 2012-08-17 |
| Ayres Britto (= Carlos Britto) | 2003-06-26 | 2012-11-17 |
| Joaquim Barbosa | 2003-06-25 | 2014-07-31 |
| Eros Grau | 2004-06-24 | 2010-08-18 |
| Ricardo Lewandowski | 2006-03-16 | em exercício |
| Cármen Lúcia | 2006-06-21 | em exercício |
| Menezes Direito | 2007-09-06 | 2009-09-01 |
| Dias Toffoli | 2009-10-23 | em exercício |

Use esta tabela apenas para deduzir o voto de ministros em exercício que a ata NÃO nomeia individualmente (regra D-004 abaixo). Onde o acórdão mostrar o voto individual de um ministro, esse valor observado tem SEMPRE precedência sobre a dedução.

**Regra de dedução (D-004):** ministro em exercício na data do julgamento + não listado como ausente/impedido/suspeito + não listado como vencido → deduz-se que votou com a maioria. Quando usar esta dedução, o campo `fonte` do voto desse ministro deve ser literalmente `"deducao D-004"` — nunca apresente um voto deduzido como se fosse observado. Se o acórdão também mostrar esse voto individualmente e ele DIVERGIR da dedução, registre a divergência em `avisos`.

## Vocabulários controlados (use exatamente estes valores, nada fora deles)

- `resultado` (por réu): `Condenação` · `Condenação parcial` · `Absolvição` · `Extinção da punibilidade`
- `motivo`: `mérito` · `prescrição` · `processual` · `atipicidade` · `n/a`
- `voto_resultado` (por ministro): `condena` · `absolve` · `não votou`
- `fonte` (de cada campo): `ementa` · `ata` · `acordao p.N` · `legislacao_citada` · `deducao D-004` (só para votos deduzidos)
- `confianca`: `alta` · `media` · `baixa` — use `baixa` sempre que houver qualquer dúvida razoável, e especialmente para qualquer nome/número que pareça corrompido pelo OCR.

## Formato de saída

Cada campo individual é um objeto com 4 partes:
```json
{"valor": "...", "evidencia": "trecho literal da fonte", "fonte": "ata", "confianca": "alta"}
```

Estrutura completa do arquivo (preencha TODOS os campos como objetos desse formato, exceto os arrays de nível superior):

```json
{
  "id_caso": "AP-409",
  "extraido_em": "2026-08-08",
  "fontes_lidas": ["dados/corpus/texto/AP-409.txt"],
  "caso": {
    "instituto_juridico": {},
    "merito_finalizado": {},
    "n_reus": {},
    "multiplas_sessoes": {}
  },
  "reus": [{
    "nome": {},
    "cargo_funcao": {},
    "resultado": {},
    "motivo": {},
    "prescricao_pos_condenacao": {},
    "crimes": [{"artigo": "", "diploma": "", "evidencia": ""}],
    "n_votantes": {}, "votos_condenacao": {}, "votos_absolvicao": {}, "unanime": {}
  }],
  "votos": [{
    "ministro": {}, "eh_relator": {}, "voto_resultado": {},
    "vencido": {}, "ausente": {}, "motivo_ausencia": {}
  }],
  "avisos": []
}
```

`reus` tem um objeto por réu do caso. `votos` é DENSO: uma linha por ministro em exercício na data do julgamento (não só relator/vencidos/ausentes) — inclua todos, usando dedução D-004 quando a ata não os nomear individualmente. `avisos` é uma lista de strings livres para qualquer achado que não caiba nos campos — divergências entre voto observado e deduzido, ambiguidade na classificação, texto ilegível/corrompido por OCR, cargo não identificado, etc. Se algo parecer mal enquadrado ou estranho na classificação já feita do caso, registre em `avisos` e siga — não é sua função reclassificar o caso.

## Onde escrever

Escreva o JSON final em: `dados/derivados/casos/AP-409.json`

Ao final, retorne um resumo curto (menos de 150 palavras) do que extraiu: número de réus, resultado de cada um, unanimidade, e qualquer aviso relevante.
````

---

## Primeira rodada — AP-432 (descartada, D-017)

> **Extraído de:** sessão `d51f6d0a`, agente `a26ef25731` (`Extrair AP-432 por leitura`).
> **Tamanho:** 6564 caracteres.
> Produziu JSON com todos os campos `null`. Descartada.

O texto abaixo é o prompt literal, exatamente como o orquestrador o enviou ao agente.

````markdown
Você é um extrator de dados jurídicos para um TCC de Economia sobre estabilidade decisória do STF em casos de corrupção. Vai extrair UM único caso, por leitura cuidadosa do texto — nunca por regex, nunca por conhecimento prévio seu sobre o caso. Você não tem acesso a nenhum outro material deste projeto além do que está listado abaixo, e é proposital: isto é um piloto de extração cega, comparado depois contra um gabarito que você não deve consultar nem procurar.

## Arquivo a ler

Leia integralmente: `dados/corpus/texto/AP-432.txt`

É o acórdão integral (texto nativo, extraído de PDF), incluindo a ementa e, ao final, a ata de julgamento. A ata de julgamento é a fonte AUTORITATIVA para placar, unanimidade, vencidos e ausentes — tem precedência sobre qualquer outra parte do texto para esses campos. Data do julgamento: 2013-10-10 (Plenário do STF).

NÃO acesse rede, NÃO procure este caso em nenhuma outra fonte, NÃO use conhecimento que você já tenha sobre este processo. Se o texto não disser algo, o campo é `null` com o motivo declarado — nunca preencha por suposição.

## Regras que não se negociam

1. **Todo campo carrega a evidência literal que o sustenta.** Um campo sem citação textual da fonte é um campo inválido — não o preencha sem a citação exata.
2. **Regex/busca de palavra-chave localiza, nunca conclui.** Por exemplo: a expressão "prescrição" pode aparecer no argumento da corrente VENCIDA de um voto — isso não faz da prescrição o resultado do julgamento. Leia o contexto completo antes de concluir o resultado.
3. **Condenação seguida de prescrição ≠ absolvição por prescrição.** São eventos diferentes; use as categorias corretas. Se um réu foi condenado e, na sequência, a punibilidade foi extinta (ex.: por prescrição retroativa), registre ambos os eventos — o campo `resultado` reflete o desfecho final do processo, e `prescricao_pos_condenacao` marca que houve condenação anterior extinta.
4. **Nunca assuma 11 votantes.** Ausências, impedimentos e suspeições reduzem o colegiado — a ata os registra nominalmente. Conte de verdade.
5. **Suspeição, impedimento e ausência são coisas distintas** — registre qual foi, na palavra exata da ata.
6. **Cargo/função do réu**: extraia do texto (ex.: "Prefeito", "Deputado Federal", "Senador", "particular"), nunca deduza pelo nome.

## Composição do STF — tabela de referência (para deduzir quem estava em exercício)

Cada ministro tem `data_posse` e `data_saida` (`em exercício` significa que, no snapshot de referência usado neste projeto, ainda não havia registro de saída):

| Ministro | Posse | Saída |
|---|---|---|
| Celso de Mello | 1989-08-17 | 2020-10-13 |
| Marco Aurélio | 1990-06-13 | 2021-07-05 |
| Gilmar Mendes | 2002-06-20 | em exercício |
| Cezar Peluso | 2003-06-26 | 2012-08-17 |
| Ayres Britto (= Carlos Britto) | 2003-06-26 | 2012-11-17 |
| Joaquim Barbosa | 2003-06-25 | 2014-07-31 |
| Eros Grau | 2004-06-24 | 2010-08-18 |
| Ricardo Lewandowski | 2006-03-16 | em exercício |
| Cármen Lúcia | 2006-06-21 | em exercício |
| Dias Toffoli | 2009-10-23 | em exercício |
| Luiz Fux | 2011-03-03 | em exercício |
| Rosa Weber | 2011-12-19 | 2023-10-02 |
| Teori Zavascki | 2012-11-29 | 2017-01-19 |
| Roberto Barroso | 2013-06-26 | em exercício |
| Ellen Gracie | 2000-12-14 | 2011-08-03 |

Use esta tabela apenas para deduzir o voto de ministros em exercício que a ata NÃO nomeia individualmente (regra D-004 abaixo). Onde o acórdão mostrar o voto individual de um ministro, esse valor observado tem SEMPRE precedência sobre a dedução.

**Regra de dedução (D-004):** ministro em exercício na data do julgamento + não listado como ausente/impedido/suspeito + não listado como vencido → deduz-se que votou com a maioria. Quando usar esta dedução, o campo `fonte` do voto desse ministro deve ser literalmente `"deducao D-004"` — nunca apresente um voto deduzido como se fosse observado. Se o acórdão também mostrar esse voto individualmente e ele DIVERGIR da dedução, registre a divergência em `avisos`.

## Vocabulários controlados (use exatamente estes valores, nada fora deles)

- `resultado` (por réu): `Condenação` · `Condenação parcial` · `Absolvição` · `Extinção da punibilidade`
- `motivo`: `mérito` · `prescrição` · `processual` · `atipicidade` · `n/a`
- `voto_resultado` (por ministro): `condena` · `absolve` · `não votou`
- `fonte` (de cada campo): `ementa` · `ata` · `acordao p.N` · `legislacao_citada` · `deducao D-004` (só para votos deduzidos)
- `confianca`: `alta` · `media` · `baixa` — use `baixa` sempre que houver qualquer dúvida razoável; não force confiança alta.

## Formato de saída

Cada campo individual é um objeto com 4 partes:
```json
{"valor": "...", "evidencia": "trecho literal da fonte", "fonte": "ata", "confianca": "alta"}
```

Estrutura completa do arquivo (preencha TODOS os campos como objetos desse formato, exceto os arrays de nível superior):

```json
{
  "id_caso": "AP-432",
  "extraido_em": "2026-08-08",
  "fontes_lidas": ["dados/corpus/texto/AP-432.txt"],
  "caso": {
    "instituto_juridico": {},
    "merito_finalizado": {},
    "n_reus": {},
    "multiplas_sessoes": {}
  },
  "reus": [{
    "nome": {},
    "cargo_funcao": {},
    "resultado": {},
    "motivo": {},
    "prescricao_pos_condenacao": {},
    "crimes": [{"artigo": "", "diploma": "", "evidencia": ""}],
    "n_votantes": {}, "votos_condenacao": {}, "votos_absolvicao": {}, "unanime": {}
  }],
  "votos": [{
    "ministro": {}, "eh_relator": {}, "voto_resultado": {},
    "vencido": {}, "ausente": {}, "motivo_ausencia": {}
  }],
  "avisos": []
}
```

`reus` tem um objeto por réu do caso. `votos` é DENSO: uma linha por ministro em exercício na data do julgamento (não só relator/vencidos/ausentes) — inclua todos, usando dedução D-004 quando a ata não os nomear individualmente. `avisos` é uma lista de strings livres para qualquer achado que não caiba nos campos — divergências entre voto observado e deduzido, ambiguidade na classificação, texto ilegível, cargo não identificado, etc. Se algo parecer mal enquadrado ou estranho na classificação já feita do caso, registre em `avisos` e siga — não é sua função reclassificar o caso.

## Onde escrever

Escreva o JSON final em: `dados/derivados/casos/AP-432.json`

Ao final, retorne um resumo curto (menos de 150 palavras) do que extraiu: número de réus, resultado de cada um, unanimidade, e qualquer aviso relevante.
````

---

## Segunda rodada — AP-432 com corpus corrigido (aproveitada)

> **Extraído de:** sessão `d51f6d0a`, agente `a113a30d9a` (`Re-extrair AP-432 (corpus corrigido)`).
> **Tamanho:** 6943 caracteres.
> Diferenças em relação à primeira rodada: a descrição da fonte passa de
> `texto nativo, extraído de PDF` para `texto extraído de PDF via pdftotext`;
> acrescenta-se a regra 7 sobre questões de ordem intermediárias; e a instrução
> de escrita ganha a ressalva `(sobrescreva o arquivo existente, que está
> vazio/nulo por um problema de corpus já corrigido)`.

O texto abaixo é o prompt literal, exatamente como o orquestrador o enviou ao agente.

````markdown
Você é um extrator de dados jurídicos para um TCC de Economia sobre estabilidade decisória do STF em casos de corrupção. Vai extrair UM único caso, por leitura cuidadosa do texto — nunca por regex, nunca por conhecimento prévio seu sobre o caso. Você não tem acesso a nenhum outro material deste projeto além do que está listado abaixo, e é proposital: isto é um piloto de extração cega, comparado depois contra um gabarito que você não deve consultar nem procurar.

## Arquivo a ler

Leia integralmente: `dados/corpus/texto/AP-432.txt`

É o acórdão integral (texto extraído de PDF via pdftotext, com marcadores `===== [página N/M] =====`), incluindo a ementa e, ao final, a ata de julgamento ("Extrato de Ata"). A ata de julgamento é a fonte AUTORITATIVA para placar, unanimidade, vencidos e ausentes — tem precedência sobre qualquer outra parte do texto para esses campos. Data do julgamento: 2013-10-10 (Plenário do STF).

NÃO acesse rede, NÃO procure este caso em nenhuma outra fonte, NÃO use conhecimento que você já tenha sobre este processo. Se o texto não disser algo, o campo é `null` com o motivo declarado — nunca preencha por suposição.

## Regras que não se negociam

1. **Todo campo carrega a evidência literal que o sustenta.** Um campo sem citação textual da fonte é um campo inválido — não o preencha sem a citação exata.
2. **Regex/busca de palavra-chave localiza, nunca conclui.** Por exemplo: a expressão "prescrição" pode aparecer no argumento da corrente VENCIDA de um voto — isso não faz da prescrição o resultado do julgamento. Leia o contexto completo antes de concluir o resultado.
3. **Condenação seguida de prescrição ≠ absolvição por prescrição.** São eventos diferentes; use as categorias corretas. Se um réu foi condenado e, na sequência, a punibilidade foi extinta (ex.: por prescrição retroativa), registre ambos os eventos — o campo `resultado` reflete o desfecho final do processo, e `prescricao_pos_condenacao` marca que houve condenação anterior extinta.
4. **Nunca assuma 11 votantes.** Ausências, impedimentos e suspeições reduzem o colegiado — a ata os registra nominalmente. Conte de verdade.
5. **Suspeição, impedimento e ausência são coisas distintas** — registre qual foi, na palavra exata da ata.
6. **Cargo/função do réu**: extraia do texto (ex.: "Prefeito", "Deputado Federal", "Senador", "particular"), nunca deduza pelo nome.
7. **Cuidado com questões de ordem intermediárias.** A sessão pode ter resolvido mais de uma questão por votação separada (ex.: uma questão de ordem sobre participação de um ministro na dosimetria, depois o mérito, depois a dosimetria em si) — cada uma pode ter placar e vencidos próprios. Não misture os placares de questões diferentes.

## Composição do STF — tabela de referência (para deduzir quem estava em exercício)

Cada ministro tem `data_posse` e `data_saida` (`em exercício` significa que, no snapshot de referência usado neste projeto, ainda não havia registro de saída):

| Ministro | Posse | Saída |
|---|---|---|
| Celso de Mello | 1989-08-17 | 2020-10-13 |
| Marco Aurélio | 1990-06-13 | 2021-07-05 |
| Gilmar Mendes | 2002-06-20 | em exercício |
| Cezar Peluso | 2003-06-26 | 2012-08-17 |
| Ayres Britto (= Carlos Britto) | 2003-06-26 | 2012-11-17 |
| Joaquim Barbosa | 2003-06-25 | 2014-07-31 |
| Eros Grau | 2004-06-24 | 2010-08-18 |
| Ricardo Lewandowski | 2006-03-16 | em exercício |
| Cármen Lúcia | 2006-06-21 | em exercício |
| Dias Toffoli | 2009-10-23 | em exercício |
| Luiz Fux | 2011-03-03 | em exercício |
| Rosa Weber | 2011-12-19 | 2023-10-02 |
| Teori Zavascki | 2012-11-29 | 2017-01-19 |
| Roberto Barroso | 2013-06-26 | em exercício |
| Ellen Gracie | 2000-12-14 | 2011-08-03 |

Use esta tabela apenas para deduzir o voto de ministros em exercício que a ata NÃO nomeia individualmente (regra D-004 abaixo). Onde o acórdão mostrar o voto individual de um ministro, esse valor observado tem SEMPRE precedência sobre a dedução.

**Regra de dedução (D-004):** ministro em exercício na data do julgamento + não listado como ausente/impedido/suspeito + não listado como vencido → deduz-se que votou com a maioria. Quando usar esta dedução, o campo `fonte` do voto desse ministro deve ser literalmente `"deducao D-004"` — nunca apresente um voto deduzido como se fosse observado. Se o acórdão também mostrar esse voto individualmente e ele DIVERGIR da dedução, registre a divergência em `avisos`.

## Vocabulários controlados (use exatamente estes valores, nada fora deles)

- `resultado` (por réu): `Condenação` · `Condenação parcial` · `Absolvição` · `Extinção da punibilidade`
- `motivo`: `mérito` · `prescrição` · `processual` · `atipicidade` · `n/a`
- `voto_resultado` (por ministro): `condena` · `absolve` · `não votou`
- `fonte` (de cada campo): `ementa` · `ata` · `acordao p.N` · `legislacao_citada` · `deducao D-004` (só para votos deduzidos)
- `confianca`: `alta` · `media` · `baixa` — use `baixa` sempre que houver qualquer dúvida razoável; não force confiança alta.

## Formato de saída

Cada campo individual é um objeto com 4 partes:
```json
{"valor": "...", "evidencia": "trecho literal da fonte", "fonte": "ata", "confianca": "alta"}
```

Estrutura completa do arquivo (preencha TODOS os campos como objetos desse formato, exceto os arrays de nível superior):

```json
{
  "id_caso": "AP-432",
  "extraido_em": "2026-08-08",
  "fontes_lidas": ["dados/corpus/texto/AP-432.txt"],
  "caso": {
    "instituto_juridico": {},
    "merito_finalizado": {},
    "n_reus": {},
    "multiplas_sessoes": {}
  },
  "reus": [{
    "nome": {},
    "cargo_funcao": {},
    "resultado": {},
    "motivo": {},
    "prescricao_pos_condenacao": {},
    "crimes": [{"artigo": "", "diploma": "", "evidencia": ""}],
    "n_votantes": {}, "votos_condenacao": {}, "votos_absolvicao": {}, "unanime": {}
  }],
  "votos": [{
    "ministro": {}, "eh_relator": {}, "voto_resultado": {},
    "vencido": {}, "ausente": {}, "motivo_ausencia": {}
  }],
  "avisos": []
}
```

`reus` tem um objeto por réu do caso. `votos` é DENSO: uma linha por ministro em exercício na data do julgamento (não só relator/vencidos/ausentes) — inclua todos, usando dedução D-004 quando a ata não os nomear individualmente. `avisos` é uma lista de strings livres para qualquer achado que não caiba nos campos. Se algo parecer mal enquadrado ou estranho na classificação já feita do caso, registre em `avisos` e siga — não é sua função reclassificar o caso.

## Onde escrever

Escreva o JSON final em: `dados/derivados/casos/AP-432.json` (sobrescreva o arquivo existente, que está vazio/nulo por um problema de corpus já corrigido).

Ao final, retorne um resumo curto (menos de 150 palavras) do que extraiu: número de réus, resultado de cada um, unanimidade, e qualquer aviso relevante.
````
