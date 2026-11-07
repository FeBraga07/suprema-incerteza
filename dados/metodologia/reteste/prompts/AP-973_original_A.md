Você é um extrator de dados jurídicos para um TCC de Economia sobre estabilidade decisória do STF em casos de corrupção. Vai extrair UM único caso, por leitura cuidadosa do texto — nunca por regex, nunca por conhecimento prévio seu sobre o caso. Não há gabarito para este caso; sua extração será comparada depois contra a de um segundo agente independente que também vai ler o mesmo texto sem ver o seu resultado. Você não tem acesso a nenhum outro material deste projeto além do listado abaixo.

## Arquivo a ler

Leia integralmente: `dados/corpus/texto/AP-973.txt`

É o acórdão integral (texto extraído via pdftotext, com marcadores `===== [página N/M] =====`), incluindo a ementa e, ao final, a ata de julgamento ("Extrato de Ata"). É um arquivo relativamente longo (225 páginas). A ata é a fonte AUTORITATIVA para placar, unanimidade, vencidos e ausentes. Data do julgamento: 2021-09-29 (Plenário do STF).

NÃO acesse rede, NÃO procure este caso em nenhuma outra fonte, NÃO use conhecimento que você já tenha sobre este processo. Se o texto não disser algo, o campo é `null` com o motivo declarado — nunca preencha por suposição.

## Regras que não se negociam

1. **Todo campo carrega a evidência literal que o sustenta.** Campo sem citação textual da fonte é campo inválido.
2. **Regex/busca de palavra-chave localiza, nunca conclui.** A expressão "prescrição" pode aparecer no argumento da corrente VENCIDA — isso não faz da prescrição o resultado. Leia o contexto completo.
3. **Condenação seguida de prescrição ≠ absolvição por prescrição.** `resultado` registra o achado de MÉRITO (`Condenação` ou `Condenação parcial`) — nunca `Extinção da punibilidade` quando há condenação prévia. `Extinção da punibilidade` só se aplica quando a punibilidade se extingue ANTES de qualquer julgamento de mérito. O evento de prescrição posterior vai em `motivo=prescrição` e `prescricao_pos_condenacao=true`. Se houver condenação em alguns capítulos/réus e absolvição em outros, use `Condenação parcial` só quando for o MESMO réu com desfecho misto entre capítulos — se forem réus DIFERENTES com resultados diferentes, cada um tem seu próprio `resultado`. (Decisão D-018.)
4. **Nunca assuma 11 votantes.** Conte de verdade pela ata.
5. **Suspeição, impedimento e ausência são coisas distintas** — registre qual foi, na palavra exata da ata.
6. **Cargo/função do réu**: extraia do texto, nunca deduza pelo nome.
7. **"Ausência do elemento subjetivo do tipo" ou "ausência de dolo" como fundamento de absolvição conta como `motivo=atipicidade`**, EXCETO quando a fonte primária contiver uma declaração explícita de algum ministro distinguindo esse fundamento de atipicidade (nesse caso, siga a declaração explícita e registre `motivo=mérito`).
8. **Se um réu tiver crimes de naturezas muito diferentes na mesma ação penal (ex.: um deles fora do escopo de corrupção — associação criminosa, lavagem — e outro dentro), e os desfechos forem diferentes por crime, registre o `resultado`/`motivo` do réu com base no crime de corrupção propriamente dito (ex.: corrupção passiva/ativa, peculato, fraude a licitação), documentando os demais capítulos em `crimes[].resultado_inciso` e em `avisos`.**
9. **Este caso pode ter múltiplos réus.** Leia cada um individualmente, com seu próprio placar quando a ata os distinguir — não generalize o resultado de um para os demais.

## Composição do STF — tabela de referência

| Ministro | Posse | Saída |
|---|---|---|
| Marco Aurélio | 1990-06-13 | 2021-07-05 |
| Gilmar Mendes | 2002-06-20 | em exercício |
| Ricardo Lewandowski | 2006-03-16 | em exercício |
| Cármen Lúcia | 2006-06-21 | em exercício |
| Dias Toffoli | 2009-10-23 | em exercício |
| Luiz Fux | 2011-03-03 | em exercício |
| Rosa Weber | 2011-12-19 | 2023-10-02 |
| Roberto Barroso | 2013-06-26 | em exercício |
| Edson Fachin | 2015-06-16 | em exercício |
| Alexandre de Moraes | 2017-03-22 | em exercício |
| Nunes Marques | 2020-11-05 | em exercício |

Nota: em 29/09/2021, Marco Aurélio já havia se aposentado (saiu em 05/07/2021) e André Mendonça só tomaria posse em 16/12/2021 — a cadeira estava vaga. Confira se a ata confirma isso (10 ministros em exercício, não 11).

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
  "id_caso": "AP-973",
  "extraido_em": "2026-08-09",
  "fontes_lidas": ["dados/corpus/texto/AP-973.txt"],
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

`reus`: um objeto por réu — pode haver mais de um. `votos`: DENSO — uma linha por ministro em exercício na data, usando dedução D-004 quando a ata não nomear individualmente. `avisos`: lista livre. Não é sua função reclassificar o caso — se algo parecer mal enquadrado, registre em `avisos` e siga.

## Onde escrever

Escreva o JSON em: `dados/derivados/casos/_dupla/AP-973_A.json`

Ao final, retorne um resumo curto (menos de 150 palavras): número de réus, resultado de cada um, unanimidade, avisos relevantes.