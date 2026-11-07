# Prompt do lote 3 — AP-426, AP-503, AP-396, AP-527

> **Casos:** AP-426, AP-503, AP-396, AP-527 · **Data:** 09/08/2026, 06:04–06:09 (BRT).
> **Sessão:** `d51f6d0a` · **Modelo dos agentes:** `claude-sonnet-5` · **Modo:** dupla extração (A e B).
> **8 execuções de agente.**
>
> Como no lote 1, A e B diferem **apenas** no caminho de saída (`_A.json` /
> `_B.json`) — verificado por diff literal nos 4 pares. Entre casos, além do
> arquivo de entrada e do `id_caso`, variam:
>
> | Caso | Ajuste específico |
> |---|---|
> | AP-426 | nenhum (é o caso-base do lote) |
> | AP-503 | fonte é **texto nativo do PDF, sem OCR**; bloco `ATENÇÃO ESPECÍFICA` avisando que o caso pode ter *"três resultados distintos no mesmo caso, por inciso do DL 201/67, com vencido nomeado por inciso"*; regra 7 nova sobre múltiplos incisos com resultados diferentes |
> | AP-396 | regra 6 alerta para cargo de magistrado |
> | AP-527 | nota de composição: *"em 16/12/2010, Eros Grau já saiu da Corte […] o Tribunal Pleno tinha só 10 ministros em exercício nesta data, não 11"* |
>
> A tabela de composição da Corte foi sendo **enxugada caso a caso**, mantendo só
> os ministros plausivelmente em exercício na data do julgamento.
>
> A regra 7 do prompt da AP-503 — *"escolha o resultado predominante ou mais
> grave para o campo `resultado` do réu"* — é a origem de um problema que a
> auditoria de 22/08/2026 registraria depois como item `G-A04` do dossiê do gate
> (placar heterogêneo por fato não expandido).

---

## Prompt de referência — AP-426, extração A

> **Extraído de:** sessão `d51f6d0a`, agente `a277067b6f` (`AP-426 extração A`).
> **Tamanho:** 5389 caracteres.

O texto abaixo é o prompt literal, exatamente como o orquestrador o enviou ao agente.

````markdown
Você é um extrator de dados jurídicos para um TCC de Economia sobre estabilidade decisória do STF em casos de corrupção. Vai extrair UM único caso, por leitura cuidadosa do texto — nunca por regex, nunca por conhecimento prévio seu sobre o caso. Não há gabarito para este caso; sua extração será comparada depois contra a de um segundo agente independente que também vai ler o mesmo texto sem ver o seu resultado. Você não tem acesso a nenhum outro material deste projeto além do listado abaixo.

## Arquivo a ler

Leia integralmente: `dados/corpus/texto/AP-426.txt`

É o acórdão integral (texto de OCR, com marcadores `===== [página N/M] =====`), incluindo a ementa e, ao final, a ata de julgamento ("Extrato de Ata"). Espere ruído de OCR — na dúvida, marque `confianca: baixa`. A ata é a fonte AUTORITATIVA para placar, unanimidade, vencidos e ausentes. Data do julgamento: 2008-12-18 (Plenário do STF). Este caso foi incluído no universo do TCC por equivalência ao DL 201/67 art. 1º, III/V — mas isso já está decidido, não questione a classificação.

NÃO acesse rede, NÃO procure este caso em nenhuma outra fonte, NÃO use conhecimento que você já tenha sobre este processo. Se o texto não disser algo, o campo é `null` com o motivo declarado — nunca preencha por suposição.

## Regras que não se negociam

1. **Todo campo carrega a evidência literal que o sustenta.** Campo sem citação textual da fonte é campo inválido.
2. **Regex/busca de palavra-chave localiza, nunca conclui.** A expressão "prescrição" pode aparecer no argumento da corrente VENCIDA — isso não faz da prescrição o resultado. Leia o contexto completo.
3. **Condenação seguida de prescrição ≠ absolvição por prescrição.** Quando um réu é condenado no mérito e depois a punibilidade é extinta, `resultado` registra o achado de MÉRITO (`Condenação` ou `Condenação parcial`) — nunca `Extinção da punibilidade`. `Extinção da punibilidade` só se aplica quando a punibilidade se extingue ANTES de qualquer julgamento de mérito. O evento de prescrição posterior vai em `motivo=prescrição` e `prescricao_pos_condenacao=true`. (Decisão D-018.)
4. **Nunca assuma 11 votantes.** Conte de verdade pela ata.
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
  "id_caso": "AP-426",
  "extraido_em": "2026-08-09",
  "fontes_lidas": ["dados/corpus/texto/AP-426.txt"],
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

`reus`: um objeto por réu. `votos`: DENSO — uma linha por ministro em exercício na data, usando dedução D-004 quando a ata não nomear individualmente. `avisos`: lista livre. Não é sua função reclassificar o caso — se algo parecer mal enquadrado, registre em `avisos` e siga.

## Onde escrever

Escreva o JSON em: `dados/derivados/casos/_dupla/AP-426_A.json`

Ao final, retorne um resumo curto (menos de 120 palavras): número de réus, resultado de cada um, unanimidade, avisos relevantes.
````

---

## Variante com múltiplos incisos — AP-503, extração A

> **Extraído de:** sessão `d51f6d0a`, agente `a82d8340dd` (`AP-503 extração A`).
> **Tamanho:** 5540 caracteres.
> Reproduzido na íntegra por conter a regra 7 que a auditoria posterior questionou.

O texto abaixo é o prompt literal, exatamente como o orquestrador o enviou ao agente.

````markdown
Você é um extrator de dados jurídicos para um TCC de Economia sobre estabilidade decisória do STF em casos de corrupção. Vai extrair UM único caso, por leitura cuidadosa do texto — nunca por regex, nunca por conhecimento prévio seu sobre o caso. Não há gabarito para este caso; sua extração será comparada depois contra a de um segundo agente independente que também vai ler o mesmo texto sem ver o seu resultado. Você não tem acesso a nenhum outro material deste projeto além do listado abaixo.

## Arquivo a ler

Leia integralmente: `dados/corpus/texto/AP-503.txt`

É o acórdão integral (texto nativo do PDF, sem OCR), incluindo a ementa e, ao final, a ata de julgamento ("Extrato de Ata"). A ata é a fonte AUTORITATIVA para placar, unanimidade, vencidos e ausentes. Data do julgamento: 2010-05-20 (Plenário do STF).

**ATENÇÃO ESPECÍFICA A ESTE CASO:** o gabarito de outro processo (não este) menciona que a AP-503 tem **três resultados distintos no mesmo caso, por inciso do DL 201/67, com vencido nomeado por inciso**. Leia com cuidado — pode haver mais de um crime/inciso imputado ao mesmo réu, cada um com seu próprio resultado e placar. Não misture os desfechos de incisos diferentes num só campo `resultado`.

NÃO acesse rede, NÃO procure este caso em nenhuma outra fonte, NÃO use conhecimento que você já tenha sobre este processo. Se o texto não disser algo, o campo é `null` com o motivo declarado — nunca preencha por suposição.

## Regras que não se negociam

1. **Todo campo carrega a evidência literal que o sustenta.** Campo sem citação textual da fonte é campo inválido.
2. **Regex/busca de palavra-chave localiza, nunca conclui.** A expressão "prescrição" pode aparecer no argumento da corrente VENCIDA — isso não faz da prescrição o resultado. Leia o contexto completo.
3. **Condenação seguida de prescrição ≠ absolvição por prescrição.** `resultado` registra o achado de MÉRITO — nunca `Extinção da punibilidade` quando há condenação prévia. O evento de prescrição posterior vai em `motivo=prescrição` e `prescricao_pos_condenacao=true`. (Decisão D-018.)
4. **Nunca assuma 11 votantes.** Conte de verdade pela ata.
5. **Suspeição, impedimento e ausência são coisas distintas** — registre qual foi, na palavra exata da ata.
6. **Cargo/função do réu**: extraia do texto, nunca deduza pelo nome.
7. **Se houver múltiplos incisos/crimes imputados ao mesmo réu com resultados diferentes**, registre isso claramente em `avisos` e escolha o resultado predominante ou mais grave para o campo `resultado` do réu, documentando a divisão por inciso no campo `crimes` e nos avisos.

## Composição do STF — tabela de referência

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
| Dias Toffoli | 2009-10-23 | em exercício |

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
  "id_caso": "AP-503",
  "extraido_em": "2026-08-09",
  "fontes_lidas": ["dados/corpus/texto/AP-503.txt"],
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

`reus`: um objeto por réu. `votos`: DENSO — uma linha por ministro em exercício na data, usando dedução D-004 quando a ata não nomear individualmente. `avisos`: lista livre. Não é sua função reclassificar o caso — se algo parecer mal enquadrado, registre em `avisos` e siga.

## Onde escrever

Escreva o JSON em: `dados/derivados/casos/_dupla/AP-503_A.json`

Ao final, retorne um resumo curto (menos de 150 palavras): número de réus, resultado de cada um, unanimidade, avisos relevantes.
````
