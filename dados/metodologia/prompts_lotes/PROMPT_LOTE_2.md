# Prompt do lote 2 — AP-447, AP-433, AP-372, AP-441, AP-565

> **Casos:** AP-447, AP-433, AP-372, AP-441, AP-565 · **Data:** 08/08/2026, 21:48–21:53 (BRT),
> com reexecução de AP-441 e AP-565 em 09/08/2026, 05:56–06:02.
> **Sessão:** `d51f6d0a` · **Modelo dos agentes:** `claude-sonnet-5`
> **Modo:** extração **única** ("cega"), por serem casos cobertos pelo `GABARITO_VALIDACAO.md`.
> **7 execuções de agente** (5 casos + 2 reexecuções).
>
> Este é o lote com **maior variação interna de prompt** — os casos não
> compartilham nem o mesmo número de regras. O orquestrador inseriu, em quatro
> dos cinco, um bloco `**ATENÇÃO ESPECÍFICA A ESTE CASO:**` ou uma regra extra
> desenhada para a dificuldade conhecida daquele acórdão:
>
> | Caso | Ajuste específico |
> |---|---|
> | AP-447 | regras 7 e 8: *"Cuidado com 'vencidos' capturados de uma QUESTÃO PRELIMINAR […] em vez do MÉRITO"* e *"Sessões com múltiplas votações podem ter placares diferentes"* |
> | AP-433 | bloco de atenção sobre **mais de uma sessão de julgamento** no mesmo acórdão ("uma primeira sessão que terminou empatada ou inconclusiva, e uma sessão posterior") |
> | AP-372 | tabela de composição da Corte enxugada (ministros antigos removidos) |
> | AP-441 | bloco de atenção sobre **réus sob sigilo/anonimizados**; regra 4 ganha *"se a ata não trouxer placar explícito […] registre `null` com o motivo, não invente um número"* |
> | AP-565 | regra 6 alerta para cargo de magistrado; regra 7 nova: *"Com 9 réus, é provável que nem todos tenham o mesmo resultado"* |
>
> AP-441 e AP-565 usam fonte `pdftotext` (corpus corrigido por D-017); os outros três, OCR.
>
> **Sobre as reexecuções de AP-441 e AP-565:** os prompts da segunda rodada são
> literalmente idênticos aos da primeira, com uma única diferença — o valor do
> campo `extraido_em` no molde de saída passa de `2026-08-08` para `2026-08-09`.
> Não houve mudança de instrução; foi reexecução após falha de infraestrutura.

---

## Prompt de referência — AP-447 (extração única)

> **Extraído de:** sessão `d51f6d0a`, agente `ae9ec06ab1` (`AP-447 extração cega`).
> **Tamanho:** 6330 caracteres.

O texto abaixo é o prompt literal, exatamente como o orquestrador o enviou ao agente.

````markdown
Você é um extrator de dados jurídicos para um TCC de Economia sobre estabilidade decisória do STF em casos de corrupção. Vai extrair UM único caso, por leitura cuidadosa do texto — nunca por regex, nunca por conhecimento prévio seu sobre o caso. Sua extração é cega: não consulte nenhum gabarito, planilha ou fonte externa. Você não tem acesso a nenhum outro material deste projeto além do listado abaixo.

## Arquivo a ler

Leia integralmente: `dados/corpus/texto/AP-447.txt`

É o acórdão integral (texto de OCR, com marcadores `===== [página N/M] =====`), incluindo a ementa e, ao final, a ata de julgamento ("Extrato de Ata"). Espere ruído de OCR — na dúvida, marque `confianca: baixa`. A ata é a fonte AUTORITATIVA para placar, unanimidade, vencidos e ausentes. Data do julgamento: 2009-02-18 (Plenário do STF).

NÃO acesse rede, NÃO procure este caso em nenhuma outra fonte, NÃO use conhecimento que você já tenha sobre este processo. Se o texto não disser algo, o campo é `null` com o motivo declarado — nunca preencha por suposição.

## Regras que não se negociam

1. **Todo campo carrega a evidência literal que o sustenta.** Campo sem citação textual da fonte é campo inválido.
2. **Regex/busca de palavra-chave localiza, nunca conclui.** A expressão "prescrição" pode aparecer no argumento da corrente VENCIDA — isso não faz da prescrição o resultado. Leia o contexto completo.
3. **Condenação seguida de prescrição ≠ absolvição por prescrição.** Quando um réu é condenado no mérito e depois a punibilidade é extinta, `resultado` registra o achado de MÉRITO (`Condenação` ou `Condenação parcial`) — nunca `Extinção da punibilidade`. `Extinção da punibilidade` só se aplica quando a punibilidade se extingue ANTES de qualquer julgamento de mérito. O evento de prescrição posterior vai em `motivo=prescrição` e `prescricao_pos_condenacao=true`. (Decisão D-018.)
4. **Nunca assuma 11 votantes.** Conte de verdade pela ata.
5. **Suspeição, impedimento e ausência são coisas distintas** — registre qual foi, na palavra exata da ata.
6. **Cargo/função do réu**: extraia do texto, nunca deduza pelo nome.
7. **Cuidado com "vencidos" capturados de uma QUESTÃO PRELIMINAR** (ex.: licitude de prova, competência) em vez do MÉRITO — são votações distintas com listas de vencidos possivelmente diferentes. Não misture.
8. **Sessões com múltiplas votações** podem ter placares diferentes — não misture.

## Composição do STF — tabela de referência

| Ministro | Posse | Saída |
|---|---|---|
| Moreira Alves | 1975-06-25 | 2003-05-19 |
| Néri da Silveira | 1985-04-10 | 2002-03-25 |
| Sydney Sanches | 1985-04-17 | 2003-04-25 |
| Octavio Gallotti | 1984-09-19 | 2001-10-31 |
| Sepúlveda Pertence | 1989-04-17 | 2007-08-26 |
| Celso de Mello | 1989-08-17 | 2020-10-13 |
| Carlos Velloso | 1990-05-17 | 2006-11-17 |
| Marco Aurélio | 1990-06-13 | 2021-07-05 |
| Ilmar Galvão | 1991-04-26 | 2003-03-31 |
| Francisco Rezek | 1992-04-15 | 2003-05-28 |
| Maurício Corrêa | 1994-12-15 | 2004-07-30 |
| Nelson Jobim | 1997-04-10 | 2006-03-30 |
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
| Luiz Fux | 2011-03-03 | em exercício |
| Rosa Weber | 2011-12-19 | 2023-10-02 |
| Teori Zavascki | 2012-11-29 | 2017-01-19 |
| Roberto Barroso | 2013-06-26 | em exercício |
| Edson Fachin | 2015-06-16 | em exercício |
| Alexandre de Moraes | 2017-03-22 | em exercício |
| Nunes Marques | 2020-11-05 | em exercício |
| André Mendonça | 2021-12-16 | em exercício |
| Cristiano Zanin | 2023-08-03 | em exercício |
| Flávio Dino | 2023-12-22 | em exercício |

`em exercício` = "sem data de saída registrada neste snapshot" — pode estar desatualizado. **A composição nomeada explicitamente na ata da sessão SEMPRE tem precedência sobre esta tabela** quando divergirem. Registre a divergência em `avisos`, mas siga a ata.

**Regra de dedução (D-004):** ministro em exercício na data + não ausente/impedido/suspeito + não vencido → deduz-se que votou com a maioria. Use `fonte: "deducao D-004"`. Se o acórdão mostrar o voto individual e ele DIVERGIR da dedução, registre em `avisos`.

## Vocabulários controlados

- `resultado`: `Condenação` · `Condenação parcial` · `Absolvição` · `Extinção da punibilidade`
- `motivo`: `mérito` · `prescrição` · `processual` · `atipicidade` · `n/a`
- `voto_resultado`: `condena` · `absolve` · `não votou`
- `fonte`: `ementa` · `ata` · `acordao p.N` · `legislacao_citada` · `deducao D-004`
- `confianca`: `alta` · `media` · `baixa`

## Formato de saída

Cada campo é um objeto: `{"valor": "...", "evidencia": "trecho literal", "fonte": "ata", "confianca": "alta"}`

```json
{
  "id_caso": "AP-447",
  "extraido_em": "2026-08-08",
  "fontes_lidas": ["dados/corpus/texto/AP-447.txt"],
  "caso": {"instituto_juridico": {}, "merito_finalizado": {}, "n_reus": {}, "multiplas_sessoes": {}},
  "reus": [{
    "nome": {}, "cargo_funcao": {}, "resultado": {}, "motivo": {}, "prescricao_pos_condenacao": {},
    "crimes": [{"artigo": "", "diploma": "", "evidencia": ""}],
    "n_votantes": {}, "votos_condenacao": {}, "votos_absolvicao": {}, "unanime": {}
  }],
  "votos": [{"ministro": {}, "eh_relator": {}, "voto_resultado": {}, "vencido": {}, "ausente": {}, "motivo_ausencia": {}}],
  "avisos": []
}
```

`reus`: um objeto por réu — este caso pode ter mais de um. `votos`: DENSO — uma linha por ministro em exercício na data, usando dedução D-004 quando a ata não nomear individualmente. `avisos`: lista livre. Não é sua função reclassificar o caso — se algo parecer mal enquadrado, registre em `avisos` e siga.

## Onde escrever

Escreva o JSON em: `dados/derivados/casos/AP-447.json`

Ao final, retorne um resumo curto (menos de 120 palavras): número de réus, resultado de cada um, unanimidade, avisos relevantes.
````

---

## Variante com bloco de atenção — AP-433

> **Extraído de:** sessão `d51f6d0a`, agente `ae092a2655` (`AP-433 extração cega`).
> **Tamanho:** 5751 caracteres.
> Reproduzido na íntegra por ser o caso em que o bloco `ATENÇÃO ESPECÍFICA` mais
> alterou o comportamento esperado (escolha da sessão que decidiu o mérito).

O texto abaixo é o prompt literal, exatamente como o orquestrador o enviou ao agente.

````markdown
Você é um extrator de dados jurídicos para um TCC de Economia sobre estabilidade decisória do STF em casos de corrupção. Vai extrair UM único caso, por leitura cuidadosa do texto — nunca por regex, nunca por conhecimento prévio seu sobre o caso. Sua extração é cega: não consulte nenhum gabarito, planilha ou fonte externa. Você não tem acesso a nenhum outro material deste projeto além do listado abaixo.

## Arquivo a ler

Leia integralmente: `dados/corpus/texto/AP-433.txt`

É o acórdão integral (texto de OCR, com marcadores `===== [página N/M] =====`), incluindo a ementa e, ao final, a ata de julgamento ("Extrato de Ata"). Espere ruído de OCR — na dúvida, marque `confianca: baixa`. A ata é a fonte AUTORITATIVA para placar, unanimidade, vencidos e ausentes.

**ATENÇÃO ESPECÍFICA A ESTE CASO:** este acórdão pode conter **mais de uma sessão de julgamento** (mais de um "Extrato de Ata", com datas diferentes) — por exemplo, uma primeira sessão que terminou empatada ou inconclusiva, e uma sessão posterior, com composição diferente (ex.: um ministro a mais), que efetivamente resolveu o mérito. Se isso ocorrer, identifique CLARAMENTE qual sessão é a que produziu o resultado final e definitivo do julgamento — normalmente a última, ou a que não terminou em empate — e use essa como fonte de `resultado`, placar e votos. Registre em `avisos` se houver mais de uma sessão, com as datas de cada uma e por que você escolheu a que escolheu. Não misture números de sessões diferentes num só campo.

NÃO acesse rede, NÃO procure este caso em nenhuma outra fonte, NÃO use conhecimento que você já tenha sobre este processo. Se o texto não disser algo, o campo é `null` com o motivo declarado — nunca preencha por suposição.

## Regras que não se negociam

1. **Todo campo carrega a evidência literal que o sustenta.** Campo sem citação textual da fonte é campo inválido.
2. **Regex/busca de palavra-chave localiza, nunca conclui.** A expressão "prescrição" pode aparecer no argumento da corrente VENCIDA — isso não faz da prescrição o resultado. Leia o contexto completo.
3. **Condenação seguida de prescrição ≠ absolvição por prescrição.** `resultado` registra o achado de MÉRITO — nunca `Extinção da punibilidade` quando há condenação prévia. O evento de prescrição posterior vai em `motivo=prescrição` e `prescricao_pos_condenacao=true`. (Decisão D-018.)
4. **Nunca assuma 11 votantes.** Conte de verdade pela ata da sessão que decidiu o mérito.
5. **Suspeição, impedimento e ausência são coisas distintas** — registre qual foi, na palavra exata da ata.
6. **Cargo/função do réu**: extraia do texto, nunca deduza pelo nome.

## Composição do STF — tabela de referência

| Ministro | Posse | Saída |
|---|---|---|
| Sepúlveda Pertence | 1989-04-17 | 2007-08-26 |
| Celso de Mello | 1989-08-17 | 2020-10-13 |
| Carlos Velloso | 1990-05-17 | 2006-11-17 |
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

`em exercício` = "sem data de saída registrada neste snapshot" — pode estar desatualizado. **A composição nomeada explicitamente na ata da sessão que decidiu o mérito SEMPRE tem precedência sobre esta tabela** quando divergirem. Registre a divergência em `avisos`, mas siga a ata.

**Regra de dedução (D-004):** ministro em exercício na data + não ausente/impedido/suspeito + não vencido → deduz-se que votou com a maioria. Use `fonte: "deducao D-004"`. Se o acórdão mostrar o voto individual e ele DIVERGIR da dedução, registre em `avisos`.

## Vocabulários controlados

- `resultado`: `Condenação` · `Condenação parcial` · `Absolvição` · `Extinção da punibilidade`
- `motivo`: `mérito` · `prescrição` · `processual` · `atipicidade` · `n/a`
- `voto_resultado`: `condena` · `absolve` · `não votou`
- `fonte`: `ementa` · `ata` · `acordao p.N` · `legislacao_citada` · `deducao D-004`
- `confianca`: `alta` · `media` · `baixa`

## Formato de saída

Cada campo é um objeto: `{"valor": "...", "evidencia": "trecho literal", "fonte": "ata", "confianca": "alta"}`

```json
{
  "id_caso": "AP-433",
  "extraido_em": "2026-08-08",
  "fontes_lidas": ["dados/corpus/texto/AP-433.txt"],
  "caso": {"instituto_juridico": {}, "merito_finalizado": {}, "n_reus": {}, "multiplas_sessoes": {}},
  "reus": [{
    "nome": {}, "cargo_funcao": {}, "resultado": {}, "motivo": {}, "prescricao_pos_condenacao": {},
    "crimes": [{"artigo": "", "diploma": "", "evidencia": ""}],
    "n_votantes": {}, "votos_condenacao": {}, "votos_absolvicao": {}, "unanime": {}
  }],
  "votos": [{"ministro": {}, "eh_relator": {}, "voto_resultado": {}, "vencido": {}, "ausente": {}, "motivo_ausencia": {}}],
  "avisos": []
}
```

`reus`: um objeto por réu — este caso pode ter mais de um. `votos`: DENSO — uma linha por ministro que participou da sessão que decidiu o mérito. `avisos`: lista livre. Não é sua função reclassificar o caso — se algo parecer mal enquadrado, registre em `avisos` e siga.

## Onde escrever

Escreva o JSON em: `dados/derivados/casos/AP-433.json`

Ao final, retorne um resumo curto (menos de 120 palavras): número de réus, resultado de cada um, unanimidade, quantas sessões encontrou, avisos relevantes.
````

---

## Variante com réus sob sigilo — AP-441 (1ª rodada)

> **Extraído de:** sessão `d51f6d0a`, agente `a87b097030` (`AP-441 extração cega`).
> **Tamanho:** 5329 caracteres.
> A 2ª rodada (09/08) difere apenas no campo `extraido_em` do molde de saída.

O texto abaixo é o prompt literal, exatamente como o orquestrador o enviou ao agente.

````markdown
Você é um extrator de dados jurídicos para um TCC de Economia sobre estabilidade decisória do STF em casos de corrupção. Vai extrair UM único caso, por leitura cuidadosa do texto — nunca por regex, nunca por conhecimento prévio seu sobre o caso. Sua extração é cega: não consulte nenhum gabarito, planilha ou fonte externa. Você não tem acesso a nenhum outro material deste projeto além do listado abaixo.

## Arquivo a ler

Leia integralmente: `dados/corpus/texto/AP-441.txt`

É o acórdão integral (texto extraído via pdftotext, com marcadores `===== [página N/M] =====`), incluindo a ementa e, ao final, a ata de julgamento ("Extrato de Ata"). A ata é a fonte AUTORITATIVA para placar, unanimidade, vencidos e ausentes. Data do julgamento: 2012-03-08 (Plenário do STF). Este caso tem 2 réus.

**ATENÇÃO ESPECÍFICA A ESTE CASO:** é possível que os nomes dos réus estejam sob sigilo/anonimizados no texto (ex.: substituídos por iniciais ou "acusado", sem nome completo). Se isso ocorrer, registre o que estiver disponível e marque `confianca: baixa` para o campo `nome`, com o motivo declarado — não invente nem complete um nome parcial.

NÃO acesse rede, NÃO procure este caso em nenhuma outra fonte, NÃO use conhecimento que você já tenha sobre este processo. Se o texto não disser algo, o campo é `null` com o motivo declarado — nunca preencha por suposição.

## Regras que não se negociam

1. **Todo campo carrega a evidência literal que o sustenta.** Campo sem citação textual da fonte é campo inválido.
2. **Regex/busca de palavra-chave localiza, nunca conclui.** A expressão "prescrição" pode aparecer no argumento da corrente VENCIDA — isso não faz da prescrição o resultado. Leia o contexto completo.
3. **Condenação seguida de prescrição ≠ absolvição por prescrição.** `resultado` registra o achado de MÉRITO — nunca `Extinção da punibilidade` quando há condenação prévia. O evento de prescrição posterior vai em `motivo=prescrição` e `prescricao_pos_condenacao=true`. (Decisão D-018.)
4. **Nunca assuma 11 votantes.** Conte de verdade pela ata — se a ata não trouxer placar explícito nem lista de vencidos em formato padronizado, registre `null` com o motivo, não invente um número.
5. **Suspeição, impedimento e ausência são coisas distintas** — registre qual foi, na palavra exata da ata.
6. **Cargo/função do réu**: extraia do texto, nunca deduza pelo nome.

## Composição do STF — tabela de referência

| Ministro | Posse | Saída |
|---|---|---|
| Celso de Mello | 1989-08-17 | 2020-10-13 |
| Marco Aurélio | 1990-06-13 | 2021-07-05 |
| Gilmar Mendes | 2002-06-20 | em exercício |
| Cezar Peluso | 2003-06-26 | 2012-08-17 |
| Ayres Britto (= Carlos Britto) | 2003-06-26 | 2012-11-17 |
| Joaquim Barbosa | 2003-06-25 | 2014-07-31 |
| Ricardo Lewandowski | 2006-03-16 | em exercício |
| Cármen Lúcia | 2006-06-21 | em exercício |
| Dias Toffoli | 2009-10-23 | em exercício |
| Luiz Fux | 2011-03-03 | em exercício |
| Rosa Weber | 2011-12-19 | 2023-10-02 |

`em exercício` = "sem data de saída registrada neste snapshot" — pode estar desatualizado. **A composição nomeada explicitamente na ata da sessão SEMPRE tem precedência sobre esta tabela** quando divergirem. Registre a divergência em `avisos`, mas siga a ata.

**Regra de dedução (D-004):** ministro em exercício na data + não ausente/impedido/suspeito + não vencido → deduz-se que votou com a maioria. Use `fonte: "deducao D-004"`. Se o acórdão mostrar o voto individual e ele DIVERGIR da dedução, registre em `avisos`.

## Vocabulários controlados

- `resultado`: `Condenação` · `Condenação parcial` · `Absolvição` · `Extinção da punibilidade`
- `motivo`: `mérito` · `prescrição` · `processual` · `atipicidade` · `n/a`
- `voto_resultado`: `condena` · `absolve` · `não votou`
- `fonte`: `ementa` · `ata` · `acordao p.N` · `legislacao_citada` · `deducao D-004`
- `confianca`: `alta` · `media` · `baixa`

## Formato de saída

Cada campo é um objeto: `{"valor": "...", "evidencia": "trecho literal", "fonte": "ata", "confianca": "alta"}`

```json
{
  "id_caso": "AP-441",
  "extraido_em": "2026-08-08",
  "fontes_lidas": ["dados/corpus/texto/AP-441.txt"],
  "caso": {"instituto_juridico": {}, "merito_finalizado": {}, "n_reus": {}, "multiplas_sessoes": {}},
  "reus": [{
    "nome": {}, "cargo_funcao": {}, "resultado": {}, "motivo": {}, "prescricao_pos_condenacao": {},
    "crimes": [{"artigo": "", "diploma": "", "evidencia": ""}],
    "n_votantes": {}, "votos_condenacao": {}, "votos_absolvicao": {}, "unanime": {}
  }],
  "votos": [{"ministro": {}, "eh_relator": {}, "voto_resultado": {}, "vencido": {}, "ausente": {}, "motivo_ausencia": {}}],
  "avisos": []
}
```

`reus`: um objeto por réu — este caso tem 2. `votos`: DENSO — uma linha por ministro em exercício na data, usando dedução D-004 quando a ata não nomear individualmente. `avisos`: lista livre. Não é sua função reclassificar o caso — se algo parecer mal enquadrado, registre em `avisos` e siga.

## Onde escrever

Escreva o JSON em: `dados/derivados/casos/AP-441.json`

Ao final, retorne um resumo curto (menos de 120 palavras): número de réus, resultado de cada um, unanimidade, avisos relevantes.
````
