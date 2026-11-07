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

Escreva o JSON em: `dados/derivados/casos/_reteste/AP-503_R.json`

Ao final, retorne um resumo curto (menos de 150 palavras): número de réus, resultado de cada um, unanimidade, avisos relevantes.

---
Nota do reteste (27/09/2026): extração cega. Não abra nenhum arquivo em `dados/derivados/` (exceto para escrever sua saída) nem em `dados/metodologia/` além deste prompt.
