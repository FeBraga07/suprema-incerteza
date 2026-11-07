# Prompt da extração L1 da AP-307 (D-051)

> **Caso:** AP-307 · **Data:** 18/10/2026, disparo ~19h20 (BRT) · **Sessão:** `a7d56ad4`
> **Modelo dos agentes:** `claude-opus-5-5`, passado explicitamente (`model: opus`). **Desvio declarado:** os 24 casos de agosto foram extraídos por `claude-sonnet-5` (REGISTRO_EXECUCAO §4), modelo que já não está disponível; a AP-307 é extraída pelo modelo da Fase 4.
> **Modo:** dupla extração (A e B), cega e independente; os dois prompts diferem só no caminho de saída.
> **Base:** prompt literal do lote 5, variante de leitura seletiva da AP-1025 (`PROMPT_LOTE_5.md`), com quatro ajustes: (1) fonte adicional, a ata do índice gravada em `brutos/` (o registro não tem inteiro teor indexado, e o OCR de 1994 é ruidoso); (2) aviso de OCR e de 756 páginas; (3) regra 8 explícita sobre os arts. 299, 305, 343 e 344 e sobre os réus fora do banco (D-020, D-022); (4) `reu` e `fato` em cada linha de `votos`, porque o placar do art. 317 pode variar por réu (D-021). A tabela de composição traz a saída de Carlos Velloso corrigida (G-A06, 2006-01-19) e só os ministros até 1997.
> **Entrega dos agentes:** `derivados/casos/_dupla/AP-307_A.json` e `_B.json`. Os agentes receberam o caminho deste texto, gravado antes do disparo em pasta temporária da sessão, com instrução de não abrir o do outro leitor.

## Prompt literal — extração A

````markdown
Você é um extrator jurídico independente, um entre dois (A e B) que vão ler o MESMO acórdão sem se comunicar. Isto é parte de um TCC de Economia (Insper) sobre insegurança jurídica no STF em casos de corrupção. Trabalhe em português brasileiro.

## Tarefa
Extrair dados estruturados do acórdão da **AP-307** (Ação Penal, STF, Plenário, julgamento em sessões de 07, 09, 12 e 13/12/1994), a partir de:
`dados/corpus/texto/AP-307.txt`

E, como fonte autoritativa de placar, da ata de julgamento gravada do índice do STF:
`dados/brutos/AP-307_ata_indice_sjur157761.txt`

**Aviso de tamanho e de OCR:** o acórdão tem 756 páginas, digitalizadas em 1994–1995 e convertidas por OCR (framework Vision do macOS). As páginas estão marcadas como `===== [página N/756] =====`; a página do PDF é esse N, e é ela que vai em `fonte` (`acordao p.N`). NÃO tente ler o arquivo inteiro de uma vez com a ferramenta Read. Estratégia recomendada:
1. Leia a ata do índice inteira (é curta). Ela narra as quatro sessões e é a fonte autoritativa de placar, vencidos, ausentes e suspeição.
2. Localize no acórdão a ementa e o relatório (início do arquivo), a(s) certidão(ões)/extrato(s) de ata (busque `EXTRATO DE ATA`, `DECISÃO`, `CERTIDÃO`, `Plenário,`) e os votos de mérito sobre o art. 317 (busque o nome de cada ministro, `VOTO`, `corrupção passiva`, `317`).
3. Para votos individuais, leia a vizinhança de cada ocorrência relevante com `offset`/`limit`. Não é obrigatório ler o documento inteiro; é obrigatório não inventar.
4. O OCR pode trocar letras e números. Na dúvida sobre nome, número ou artigo, confira no PDF (`dados/corpus/pdf/AP-307.pdf`, mesma numeração de página) ou marque `confianca: baixa` e explique em `avisos`.

Você NÃO tem acesso a nenhum outro caso, a nenhum gabarito, a nenhuma extração paralela. Não leia nada fora dos dois arquivos acima e do PDF do mesmo caso. Não use rede.

## Contexto já fechado (não reabrir)
A classificação deste caso foi decidida em 18/10/2026 e NÃO deve ser questionada:
- **Modalidade Levcovitz:** "8 (corrupção passiva, art. 317)"
- **Resumo da classificação:** "Imputação de corrupção passiva (art. 317, caput, do CP) ao ex-Presidente da República e a dois corréus, julgada no mérito pelo Plenário. As demais imputações do processo (arts. 299, 305, 343 e 344 do CP) não constam do Quadro 1.1 e ficam fora; os réus acusados só por elas ficam fora do banco."
- Fontes de classificação usadas: ementa+ata.

Sua tarefa NÃO é reclassificar — é extrair réus, resultado, placar, votos individuais e instituto jurídico, por LEITURA do texto.

## Regras que não se negociam (violação invalida a extração)

1. **Todo campo carrega evidência literal** — um trecho exato copiado da fonte que sustenta o valor. Campo sem citação é campo inválido.
2. **Regex/busca por palavra-chave localiza, nunca conclui.** Você pode (e deve, dado o tamanho) usar grep para achar onde algo está, mas a decisão sobre o que aquele trecho significa é sua leitura, não um match de padrão.
3. **Nunca preencher por conhecimento prévio.** Você não sabe nada sobre este caso que não esteja no texto que leu — inclusive sobre os réus, que são figuras públicas. Se a fonte não diz, o valor é `null` com o motivo declarado em avisos.
4. **Extração cega e independente.** Não existe "resposta certa" para comparar agora — isso vem depois, numa etapa de consolidação que você não vai fazer.
5. **Não reabrir a classificação** (ver acima). Se algo parecer mal classificado, registre em `avisos` e siga.
6. **`cargo_funcao` é o cargo/função do réu À ÉPOCA DOS FATOS**, não necessariamente à época do julgamento — registre ambos se houver mudança relevante para explicar o foro por prerrogativa de função no STF.
7. **Convenção sobre `motivo = atipicidade`:** quando a fundamentação do voto vencedor usa linguagem de "ausência de dolo" / "ausência do elemento subjetivo do tipo" como razão central da absolvição, classifique `motivo` como `atipicidade`, MESMO que o dispositivo formal cite outro inciso do art. 386 do CPP. Se houver tensão entre o inciso citado e a linguagem usada, registre em `avisos` — não esconda, mas siga a convenção de olhar o argumento substantivo, não só o inciso.
8. **Réu com crimes mistos, só parte no escopo Levcovitz (2014):** este caso TEM esse padrão. Só a corrupção passiva (art. 317 do CP) está no escopo. Os arts. 299 (falsidade ideológica), 305 (supressão de documento), 343 (corrupção ativa de testemunha) e 344 (coação no curso do processo) do CP estão FORA. O `resultado`/`motivo` de cada réu segue só o desfecho do art. 317. Os desfechos dos outros capítulos vão em `avisos`, por réu. **Réu sem nenhuma imputação do art. 317 NÃO entra no array `reus`** nem no painel `votos`: liste-o em `avisos` (nome, crimes, desfecho).
9. **D-018 — `resultado` segue o MÉRITO, não o desfecho processual posterior.** Se o réu é condenado no mérito e DEPOIS a punibilidade é extinta, `resultado` continua `Condenação` ou `Condenação parcial`; o desfecho posterior vai em `motivo` (`prescrição`) e `prescricao_pos_condenacao` (`true`). `Extinção da punibilidade` como `resultado` só se aplica quando a punibilidade se extingue ANTES de qualquer julgamento de mérito.

### Armadilhas já documentadas em casos anteriores deste projeto
- **Argumento do vencido não é o resultado.** Expressões de condenação aparecem nos votos da corrente vencida.
- **Contagem de votantes:** nunca assuma 11. Ausências, impedimentos, suspeições e cadeiras vagas reduzem o colegiado — a ata as registra nominalmente. Suspeição, impedimento e ausência são coisas distintas: registre qual foi, na palavra da ata.
- **Placar que varia por réu e por fato.** Neste caso o resultado do art. 317 pode não ser o mesmo para todos os réus, nem o fundamento para todos os episódios da denúncia. Por isso, **cada linha de `votos` nomeia `reu` e `fato`**: uma linha por ministro × réu do art. 317 × fato. Use um fato só ("corrupção passiva (art. 317, CP)") quando os votos não se separarem por episódio; se o placar ou o voto de algum ministro mudar de um episódio para outro, separe os fatos, nomeando o episódio, e explique em `avisos`. Diferença só de fundamento (inciso do art. 386) entre episódios, com o mesmo voto de cada ministro, não separa fato: registre-a em `avisos`.
- **Preliminares não são o mérito.** A ata registra votações sobre preliminares (por exemplo, sobre admissibilidade de prova). Elas não são o `voto_resultado`; mencione-as em `avisos` se relevantes.

## Composição do STF (nome padrão · posse · saída)
Moreira Alves 1975-06-25–2003-05-19 · Néri da Silveira 1985-04-10–2002-03-25 · Sydney Sanches 1985-04-17–2003-04-25 · Octavio Gallotti 1984-09-19–2001-10-31 · Sepúlveda Pertence 1989-04-17–2007-08-26 · Celso de Mello 1989-08-17–2020-10-13 · Carlos Velloso 1990-05-17–2006-01-19 · Marco Aurélio 1990-06-13–2021-07-05 · Ilmar Galvão 1991-04-26–2003-03-31 · Francisco Rezek 1992-04-15–2003-05-28 · Maurício Corrêa 1994-12-15–2004-07-30 · Nelson Jobim 1997-04-10–2006-03-30

Pela tabela, em 07–13/12/1994 estão em exercício: Moreira Alves, Néri da Silveira, Sydney Sanches, Octavio Gallotti, Sepúlveda Pertence, Celso de Mello, Carlos Velloso, Marco Aurélio, Ilmar Galvão e Francisco Rezek (10; Maurício Corrêa só toma posse em 15/12/1994). Use a ata para quem esteve presente, ausente, suspeito ou impedido; se a ata contradisser a tabela, a ata prevalece, e registre em `avisos`.

## Fontes, em ordem de autoridade
1. Acórdão integral (o .txt; PDF para tirar dúvida de OCR) — votos individuais, cargo, fundamentação.
2. Ata de julgamento — **autoritativa** para placar, unanimidade, vencidos, ausentes e suspeição. Use a ata do índice (arquivo acima) e o(s) extrato(s) de ata dentro do acórdão; se divergirem, registre em `avisos`.
3. Ementa — para instituto jurídico e resumo (início do documento).

## Contrato de saída
Grave o arquivo em:
`dados/derivados/casos/_dupla/AP-307_A.json`

Estrutura exata (todo campo é um objeto com `valor`, `evidencia`, `fonte`, `confianca` — exceto `crimes`, que é uma lista de objetos `{artigo, diploma, evidencia}`, e `avisos`, que é uma lista de strings):

```json
{
  "id_caso": "AP-307",
  "extraido_em": "2026-10-18",
  "fontes_lidas": ["dados/corpus/texto/AP-307.txt", "dados/brutos/AP-307_ata_indice_sjur157761.txt"],
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
    "reu": {"valor": ""}, "fato": {"valor": ""},
    "voto_resultado": {"valor": "", "evidencia": "", "fonte": "", "confianca": ""},
    "vencido": {"valor": false}, "ausente": {"valor": false}, "motivo_ausencia": {"valor": "n/a"}
  }],
  "avisos": []
}
```

`n_reus` conta só os réus do array `reus` (os do art. 317). `crimes` lista só o(s) crime(s) do escopo; os demais vão em `avisos`.
`fonte` ∈ `ementa` · `ata` · `acordao p.N` · `legislacao_citada` · `deducao D-004` (quando o voto não é observado diretamente e você o deduz pela regra: ministro em exercício, não ausente, não vencido → votou com a maioria — deixe isso explícito em `fonte`, nunca disfarçado de observado).
`confianca` ∈ `alta` · `media` · `baixa` — `baixa` sinaliza para revisão humana.
`resultado` ∈ `Condenação` · `Condenação parcial` · `Absolvição` · `Extinção da punibilidade`.
`motivo` ∈ `mérito` · `prescrição` · `processual` · `atipicidade` · `n/a`.
`voto_resultado` ∈ `condena` · `absolve` · `não votou`.
`motivo_ausencia`: a palavra da ata (`ausente`, `suspeição`, `impedimento`) ou `n/a`.

O painel de `votos` deve ser **denso**: para cada réu do art. 317 e cada fato, uma linha por ministro em exercício na data do julgamento, inclusive quem não votou (`não votou`, com `ausente`/`motivo_ausencia`), mesmo que o voto seja deduzido (regra D-004, com `fonte: "deducao D-004"`). Onde o acórdão ou a ata mostrar o voto individual, o valor observado tem precedência sobre a dedução; se observado e dedução divergirem, registre em `avisos`.

Em `avisos`, registre: qualquer ambiguidade, qualquer tensão entre regras e o texto, qualquer campo de baixa confiança e por quê, os desfechos dos capítulos fora do escopo por réu, os réus fora do banco, problemas de OCR relevantes, e qualquer achado estrutural (sessões, questões de ordem, preliminares).

Ao final, apenas confirme em texto curto que o arquivo foi gravado, incluindo quais páginas do acórdão você efetivamente examinou — não é preciso relatório longo.
````
