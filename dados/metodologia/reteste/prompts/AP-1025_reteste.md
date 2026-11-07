Você é um extrator jurídico independente, um entre dois (A e B) que vão ler o MESMO acórdão sem se comunicar. Isto é parte de um TCC de Economia (Insper) sobre insegurança jurídica no STF em casos de corrupção. Trabalhe em português brasileiro.

## Tarefa
Extrair dados estruturados do acórdão da **AP-1025** (Ação Penal, STF, Plenário, julgada em 31/05/2023), a partir de:
`dados/corpus/texto/AP-1025.txt`

**Aviso de tamanho:** este arquivo tem ~2 milhões de caracteres (~500 mil tokens, 41.836 linhas) — é o segundo maior caso do corpus, atrás só da AP-470. NÃO tente ler o arquivo inteiro de uma vez com a ferramenta Read (vai estourar contexto ou ser truncado sem aviso). Estratégia recomendada:
1. Primeiro, rode `grep -n "EXTRATO DE ATA" dados/corpus/texto/AP-1025.txt` para localizar as sessões. O julgamento se estendeu por várias datas em maio/2023 (17, 18, 24, 25, 31) — é um julgamento em múltiplas sessões. A ata final relevante para o placar definitivo é a da última data (31/05/2023, por volta da linha 41.367 em diante) — leia essa seção com Read usando `offset`/`limit` focado nesse trecho (por exemplo, offset ~41300, limit ~600).
2. Para nomes dos réus, cargo/função e crimes, use grep para localizar "RÉU" / "DENUNCIADO" / "ACUSADO" e leia o início do documento (ementa e relatório), que normalmente fica nas primeiras ~2000 linhas.
3. Para votos individuais e fundamentação de cada ministro, use grep para localizar o nome de cada ministro relevante (ver lista de composição abaixo) seguido de leitura direcionada (`offset`/`limit`) só da vizinhança de cada ocorrência relevante — não leia o documento inteiro linearmente.
4. Se, mesmo com essa estratégia seletiva, um campo não puder ser preenchido com confiança por falta de leitura direta, marque `confianca: baixa` e explique em `avisos` — não é obrigatório esgotar 100% do documento, é obrigatório não inventar.

Você NÃO tem acesso a nenhum outro caso, a nenhum gabarito, a nenhuma extração paralela. Não leia nada fora do arquivo acima e do necessário para a tabela de composição da Corte (já fornecida abaixo — não precisa buscar em outro lugar). Não use rede.

## Contexto já fechado (não reabrir)
A classificação deste caso já foi decidida em 08/08/2026 e NÃO deve ser questionada:
- **Modalidade Levcovitz:** "8 (corrupção passiva, art. 317) + 18 (Lei 8.666/93, art. 90)"
- **Resumo da classificação:** "Condenação por corrupção passiva (art. 317), lavagem (Lei 9.613/98) e associação criminosa (art. 288, prescrita); a legislação citada registra também o art. 90 da Lei 8.666/93. Entra pelo art. 317; lavagem e associação como variáveis (D-012)."
- Fontes de classificação usadas: ementa+legislação citada.
- Este caso já é sabido ter condenação por corrupção passiva, mais lavagem e associação criminosa (esta última prescrita) como variáveis associadas — não crimes que entram sozinhos no escopo.

Sua tarefa NÃO é reclassificar — é extrair réus, resultado, placar, votos individuais e instituto jurídico, por LEITURA do texto.

## Regras que não se negociam (violação invalida a extração)

1. **Todo campo carrega evidência literal** — um trecho exato copiado da fonte que sustenta o valor. Campo sem citação é campo inválido.
2. **Regex/busca por palavra-chave localiza, nunca conclui.** Você pode (e deve, dado o tamanho) usar grep para achar onde algo está, mas a decisão sobre o que aquele trecho significa é sua leitura, não um match de padrão.
3. **Nunca preencher por conhecimento prévio.** Você não sabe nada sobre este caso que não esteja no texto que leu. Se a fonte não diz, o valor é `null` com o motivo declarado em avisos.
4. **Extração cega e independente.** Não existe "resposta certa" para comparar agora — isso vem depois, numa etapa de consolidação que você não vai fazer.
5. **Não reabrir a classificação** (ver acima). Se algo parecer mal classificado, registre em `avisos` e siga.
6. **`cargo_funcao` é o cargo/função do réu À ÉPOCA DOS FATOS**, não necessariamente à época do julgamento — mas registre ambos se houver mudança relevante para explicar o foro por prerrogativa de função no STF.
7. **Convenção sobre `motivo = atipicidade`:** quando a fundamentação do voto vencedor usa linguagem de "ausência de dolo" / "ausência do elemento subjetivo do tipo" como razão central da absolvição, classifique `motivo` como `atipicidade`, MESMO que o dispositivo formal cite art. 386, VII do CPP. Se houver essa tensão entre o inciso citado e a linguagem usada, registre isso em `avisos`. (Não deve se aplicar aqui, já que o caso é de condenação — mas mantenha a regra caso algum réu específico seja absolvido.)
8. **Réu com crimes mistos, só parte no escopo Levcovitz (2014):** este caso TEM esse padrão — corrupção passiva (art. 317, no escopo) + lavagem (Lei 9.613/98, fora do escopo como crime autônomo) + associação criminosa (art. 288, expressamente excluído do escopo por `CLAUDE.md` §2, e aqui prescrita). O campo `resultado`/`motivo` de cada réu deve seguir o desfecho do crime de corrupção passiva (art. 317) especificamente — não o desfecho agregado de todos os capítulos. Documente os desfechos dos outros capítulos (lavagem, associação) à parte em `avisos`, por réu.
9. **D-018 — `resultado` segue o MÉRITO, não o desfecho processual posterior.** Se o réu é condenado no mérito e DEPOIS a punibilidade é extinta (ex.: prescrição retroativa), `resultado` continua `Condenação` ou `Condenação parcial` — nunca `Extinção da punibilidade`. O desfecho posterior vai em `motivo` (`prescrição`) e `prescricao_pos_condenacao` (`true`). `Extinção da punibilidade` como `resultado` só se aplica quando a punibilidade se extingue ANTES de qualquer julgamento de mérito. (A associação criminosa deste caso, prescrita, é exatamente esse padrão — mas ela está FORA do escopo Levcovitz mesmo assim, então não é o `resultado` do réu; documente-a em `avisos`.)

### Armadilhas já documentadas em casos anteriores deste projeto
- **Prescrição no argumento do vencido:** a expressão "prescrição da pretensão punitiva" aparece com frequência no voto da corrente VENCIDA. Ela não é necessariamente o resultado do capítulo relevante (art. 317).
- **Contagem de votantes:** nunca assuma 11. Ausências, impedimentos e suspeições reduzem o colegiado — a ata as registra nominalmente. Para este caso (31/05/2023), a composição plena esperada é 11 (Rosa Weber ainda em exercício até 02/10/2023; Zanin e Dino ainda não empossados), salvo ausência/impedimento/suspeição específica registrada na ata.
- **Suspeição, impedimento e ausência são coisas distintas** — registre qual foi, na palavra da ata.
- **Múltiplos réus:** dado que é um julgamento longo e provavelmente com vários acusados, preencha o array `reus` com um objeto por réu, e o painel `votos` uma vez só (é por ministro, não por réu × ministro) — a menos que o placar varie por réu, caso em que registre isso claramente em `avisos` e, se necessário, capture o voto predominante ou documente a variação por réu no próprio objeto de cada réu (`n_votantes`, `votos_condenacao`, `votos_absolvicao`, `unanime` já são campos por réu, exatamente para isso).

## Composição do STF (nome padrão · posse · saída)
Moreira Alves 1975-06-25–2003-05-19 · Néri da Silveira 1985-04-10–2002-03-25 · Sydney Sanches 1985-04-17–2003-04-25 · Octavio Gallotti 1984-09-19–2001-10-31 · Sepúlveda Pertence 1989-04-17–2007-08-26 · Celso de Mello 1989-08-17–2020-10-13 · Carlos Velloso 1990-05-17–2006-11-17 · Marco Aurélio 1990-06-13–2021-07-05 · Ilmar Galvão 1991-04-26–2003-03-31 · Francisco Rezek 1992-04-15–2003-05-28 · Maurício Corrêa 1994-12-15–2004-07-30 · Nelson Jobim 1997-04-10–2006-03-30 · Ellen Gracie 2000-12-14–2011-08-03 · Gilmar Mendes 2002-06-20–em exercício · Cezar Peluso 2003-06-26–2012-08-17 · Carlos Ayres Britto 2003-06-26–2012-11-17 · Joaquim Barbosa 2003-06-25–2014-07-31 · Eros Grau 2004-06-24–2010-08-18 · Ricardo Lewandowski 2006-03-16–em exercício · Cármen Lúcia 2006-06-21–em exercício · Menezes Direito 2007-09-06–2009-09-01 · Dias Toffoli 2009-10-23–em exercício · Luiz Fux 2011-03-03–em exercício · Rosa Weber 2011-12-19–2023-10-02 · Teori Zavascki 2012-11-29–2017-01-19 · Roberto Barroso 2013-06-26–em exercício · Edson Fachin 2015-06-16–em exercício · Alexandre de Moraes 2017-03-22–em exercício · Nunes Marques 2020-11-05–em exercício · André Mendonça 2021-12-16–em exercício · Cristiano Zanin 2023-08-03–em exercício · Flávio Dino 2023-12-22–em exercício

Para este caso (31/05/2023), os ministros relevantes em exercício são: Gilmar Mendes, Lewandowski, Cármen Lúcia, Dias Toffoli, Fux, Rosa Weber, Barroso, Fachin, Moraes, Nunes Marques, André Mendonça (11 no total, salvo ausência específica registrada na ata).

## Fontes, em ordem de autoridade
1. Acórdão integral (o .txt) — votos individuais, cargo, fundamentação. Leia por trechos, conforme estratégia acima.
2. Ata de julgamento (dentro do mesmo texto, sob "EXTRATO DE ATA") — **autoritativa** para placar, unanimidade, vencidos e ausentes. Use a ata da sessão final (31/05/2023) como a que declara o resultado definitivo.
3. Ementa — para instituto jurídico e resumo (normalmente no início do documento).

## Contrato de saída
Grave o arquivo em:
`dados/derivados/casos/_reteste/AP-1025_R.json`

Estrutura exata (todo campo é um objeto com `valor`, `evidencia`, `fonte`, `confianca` — exceto `crimes`, que é uma lista de objetos `{artigo, diploma, evidencia}`, e `avisos`, que é uma lista de strings):

```json
{
  "id_caso": "AP-1025",
  "extraido_em": "2026-08-09",
  "fontes_lidas": ["dados/corpus/texto/AP-1025.txt"],
  "caso": {
    "instituto_juridico": {"valor": "", "evidencia": "", "fonte": "", "confianca": ""},
    "merito_finalizado": {"valor": true, "evidencia": "", "fonte": "", "confianca": ""},
    "n_reus": {"valor": 0, "evidencia": "", "fonte": "", "confianca": ""},
    "multiplas_sessoes": {"valor": true, "evidencia": "", "fonte": "", "confianca": ""}
  },
  "reus": [{
    "nome": {"valor": "", "evidencia": "", "fonte": "", "confianca": ""},
    "cargo_funcao": {"valor": "", "evidencia": "", "fonte": "", "confianca": ""},
    "resultado": {"valor": "", "evidencia": "", "fonte": "", "confianca": ""},
    "motivo": {"valor": "", "evidencia": "", "fonte": "", "confianca": ""},
    "prescricao_pos_condenacao": {"valor": false, "evidencia": "", "fonte": "", "confianca": ""},
    "crimes": [{"artigo": "", "diploma": "", "evidencia": ""}],
    "n_votantes": {"valor": 0, "evidencia": "", "fonte": "", "confianca": ""},
    "votos_condenacao": {"valor": 0, "evidencia": "", "fonte": "", "confianca": ""},
    "votos_absolvicao": {"valor": 0, "evidencia": "", "fonte": "", "confianca": ""},
    "unanime": {"valor": true, "evidencia": "", "fonte": "", "confianca": ""}
  }],
  "votos": [{
    "ministro": {"valor": ""}, "eh_relator": {"valor": false},
    "voto_resultado": {"valor": "", "evidencia": "", "fonte": "", "confianca": ""},
    "vencido": {"valor": false}, "ausente": {"valor": false}, "motivo_ausencia": {"valor": "n/a"}
  }],
  "avisos": []
}
```

`fonte` ∈ `ementa` · `ata` · `acordao p.N` · `legislacao_citada` · `deducao D-004`.
`confianca` ∈ `alta` · `media` · `baixa` — `baixa` sinaliza para revisão humana.
`resultado` ∈ `Condenação` · `Condenação parcial` · `Absolvição` · `Extinção da punibilidade`.
`motivo` ∈ `mérito` · `prescrição` · `processual` · `atipicidade` · `n/a`.
`voto_resultado` ∈ `condena` · `absolve` · `não votou`.

O painel de `votos` deve ser **denso**: uma linha por ministro em exercício na data do julgamento, mesmo que o voto seja deduzido (regra D-004, com `fonte: "deducao D-004"`). Onde o acórdão mostrar o voto individual, o valor observado tem precedência sobre a dedução.

Em `avisos`, registre: qualquer ambiguidade, qualquer tensão entre regras e o texto, qualquer campo de baixa confiança e por quê, os desfechos dos capítulos fora do escopo (lavagem, associação criminosa) por réu, e qualquer achado estrutural relevante.

Ao final, apenas confirme em texto curto que o arquivo foi gravado, incluindo quantas linhas do arquivo original você conseguiu efetivamente examinar (mesmo que parcialmente, via grep+leitura seletiva) — não é preciso relatório longo.

---
Nota do reteste (27/09/2026): extração cega. Não abra nenhum arquivo em `dados/derivados/` (exceto para escrever sua saída) nem em `dados/metodologia/` além deste prompt.
