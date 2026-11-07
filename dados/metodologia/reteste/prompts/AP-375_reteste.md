Você é um extrator de dados jurídicos para um TCC de Economia sobre estabilidade decisória do STF em casos de corrupção. Vai extrair UM único caso, por leitura cuidadosa do texto — nunca por regex, nunca por conhecimento prévio seu sobre o caso. Não há gabarito para este caso; sua extração será comparada depois contra a de um segundo agente independente que também vai ler o mesmo texto sem ver o seu resultado. Você não tem acesso a nenhum outro material deste projeto além do listado abaixo.

## Arquivo a ler

Leia integralmente: `dados/corpus/texto/AP-375.txt`

É o acórdão integral (texto de OCR, com marcadores `===== [página N/M] =====`), incluindo a ementa e, ao final, a ata de julgamento ("Extrato de Ata"). Espere ruído de OCR: quebras de linha estranhas, artefatos de layout, possíveis erros de caractere em nomes e números — na dúvida, marque `confianca: baixa`. A ata é a fonte AUTORITATIVA para placar, unanimidade, vencidos e ausentes. Data do julgamento: 2004-10-27 (Plenário do STF).

NÃO acesse rede, NÃO procure este caso em nenhuma outra fonte, NÃO use conhecimento que você já tenha sobre este processo. Se o texto não disser algo, o campo é `null` com o motivo declarado — nunca preencha por suposição.

## Regras que não se negociam

1. **Todo campo carrega a evidência literal que o sustenta.** Campo sem citação textual da fonte é campo inválido.
2. **Regex/busca de palavra-chave localiza, nunca conclui.** A expressão "prescrição" pode aparecer no argumento da corrente VENCIDA — isso não faz da prescrição o resultado. Leia o contexto completo.
3. **Condenação seguida de prescrição ≠ absolvição por prescrição.** Quando um réu é condenado no mérito e depois a punibilidade é extinta (ex.: prescrição retroativa), `resultado` registra o achado de MÉRITO (`Condenação` ou `Condenação parcial`) — nunca `Extinção da punibilidade` nesse caso. `Extinção da punibilidade` como valor de `resultado` só se aplica quando a punibilidade se extingue ANTES de qualquer julgamento de mérito (sem condena/absolve a registrar). O evento de prescrição posterior à condenação vai em `motivo=prescrição` e `prescricao_pos_condenacao=true` — nunca sobrescrevendo o campo de mérito. (Decisão D-018 do projeto.)
4. **Nunca assuma 11 votantes.** Ausências, impedimentos e suspeições reduzem o colegiado — a ata os registra nominalmente. Conte de verdade.
5. **Suspeição, impedimento e ausência são coisas distintas** — registre qual foi, na palavra exata da ata.
6. **Cargo/função do réu**: extraia do texto, nunca deduza pelo nome.
7. **Sessões com múltiplas votações** (questão de ordem, mérito, dosimetria) podem ter placares diferentes — não misture.

## Composição do STF — tabela de referência (para deduzir quem estava em exercício)

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

`em exercício` significa "sem data de saída registrada neste snapshot de referência" — pode estar desatualizado. **A composição nomeada explicitamente na ata da sessão (lista de presentes/ausentes) SEMPRE tem precedência sobre esta tabela** quando as duas divergirem — já aconteceu antes (Lewandowski aparecia "em exercício" na tabela mas não constava na composição nomeada de uma sessão real). Registre a divergência em `avisos` se ocorrer, mas siga a ata.

**Regra de dedução (D-004):** ministro em exercício na data + não listado como ausente/impedido/suspeito + não listado como vencido → deduz-se que votou com a maioria. Use `fonte: "deducao D-004"` nesses casos — nunca apresente um voto deduzido como observado. Se o acórdão mostrar esse voto individualmente e ele DIVERGIR da dedução, registre em `avisos`.

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
  "id_caso": "AP-375",
  "extraido_em": "2026-08-08",
  "fontes_lidas": ["dados/corpus/texto/AP-375.txt"],
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

`reus`: um objeto por réu. `votos`: DENSO — uma linha por ministro em exercício na data (não só relator/vencidos/ausentes), usando dedução D-004 quando a ata não nomear individualmente. `avisos`: lista livre para achados que não cabem nos campos. Não é sua função reclassificar o caso — se algo parecer mal enquadrado, registre em `avisos` e siga.

## Onde escrever

Escreva o JSON em: `dados/derivados/casos/_reteste/AP-375_R.json`

Ao final, retorne um resumo curto (menos de 120 palavras): número de réus, resultado de cada um, unanimidade, avisos relevantes.

---
Nota do reteste (27/09/2026): extração cega. Não abra nenhum arquivo em `dados/derivados/` (exceto para escrever sua saída) nem em `dados/metodologia/` além deste prompt.
