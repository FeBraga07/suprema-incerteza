# Prompt de extração da Fase 4 (versão 2, 18/10/2026)

> **Uso:** só a AP-307 (D-051). O orquestrador substitui os campos `{…}` do bloco "Caso" e envia o texto entre `=====INÍCIO=====` e `=====FIM=====`.
> **Modelo:** passado explicitamente em cada chamada (`claude-opus-5-5`) e registrado no `REGISTRO_EXECUCAO.md`.
> **Por que uma v2:** decisão do Felipe (D-051, adendo): a AP 307, retomada depois do recorte inicial, é lida já com o codebook corrigido pelo gate (`CODEBOOK.md` v2, D-048 a D-050). Nos outros 24 casos, as categorias e regras da v2 foram aplicadas na consolidação, sobre leituras feitas com a v1.1.
> **O que muda em relação à v1.1 (`PROMPT_FASE4.md`), e nada mais:** (1) categorias `tipicidade` (com `anotacao_tipicidade`) e `ato_de_oficio`, com as fichas §3.3 e §3.4 do codebook v2, e o campo `anotacoes` (prova de colaboração e de inquérito); (2) `sim_favorece` marcado pelo leitor nas `outra` (R9, que na v1 era marcada depois); (3) regras R5c, R6b, R6c, R8, R10, R11, R12, R15 e R17, com o texto do codebook v2; (4) `voto_resultado` com `Extingue` e `Tranca` (R16); (5) campos `unidade_origem` e `fato`, porque as unidades chegam desdobradas por episódio (R14). As regras R13 e R14, que são estruturais, ficam com o orquestrador. Exemplos por caso e o quadro dos casos de origem continuam fora, como na v1.
> **Redação:** sessão `a7d56ad4`, `claude-opus-5-5`, a partir do texto da v1.1 e do codebook v2. **Duas notas de aplicação são da sessão, e não do codebook:** (a) na ficha de `ato_de_oficio`, a instrução de separar "exige ato de ofício?" de "houve o ato? o réu o praticou?" (aplicação da R4); (b) em `tipicidade`, "quando não aplicar", a exclusão do ato de ofício da corrupção (consequência da G4-03, que fez dele categoria própria). A conferir pelo Felipe no mini-gate da AP-307.

=====INÍCIO=====
Você é um leitor de acórdãos para um TCC de Economia sobre estabilidade decisória do STF em ações penais de corrupção. Sua tarefa é ler UM acórdão e preencher, para cada unidade réu × fato, qual foi a questão jurídica decisiva e como cada ministro se posicionou nela. Trabalhe só por leitura cuidadosa do texto, nunca por regex e nunca por conhecimento prévio seu sobre o caso.

## Leitura cega: o que você NÃO pode abrir

Você só pode ler o arquivo do acórdão indicado abaixo. Não abra nenhum outro arquivo do projeto: nada em `anotacoes_codebook/`, `CODEBOOK.md`, `DECISOES.md`, `ESTADO.md`, `PLANO.md`, `derivados/`, `mapa_votos/` (exceto o `.psv` do seu caso, quando indicado abaixo), `extracao/` nem transcrições. O arquivo com estas instruções, em `prompts_lote/`, você já está lendo; não abra os de outros casos. Isto é proposital: sua leitura será comparada com a de um leitor humano e com a de outro leitor independente.

## Caso

- **Caso:** {CASO}
- **Arquivo a ler:** `{ARQUIVO_TEXTO}` (texto integral; as páginas estão marcadas como `===== [página N/M] =====`, e a página do PDF é esse N)
- **Unidades réu × fato a preencher** (com o escopo Levcovitz já decidido; copie-o em `escopo_levcovitz` com `fonte = "banco"`, sem procurar evidência):
{UNIDADES}
- **Votos registrados no banco (para conferência, não para copiar):**
{VOTOS}
- **Arquivo de saída:** `{SAIDA}`

## O que é a questão decisiva

É a pergunta jurídica cuja resposta decidiu o réu naquele fato. Ela é escrita como pergunta comparável, que poderia ser feita em outro caso, e não como conclusão.

### Regras de leitura

- **R1.** Escreva a questão como pergunta comparável, não como conclusão. Ex.: "houve comprovação de dolo do réu?", e não "o réu agiu sem dolo".
- **R2.** Siga a linguagem do voto, e não o número do inciso citado, salvo quando a linguagem for vaga.
- **R3.** Se a linguagem for vaga e for preciso recorrer ao inciso, use a redação vigente na data da peça que o cita (parecer ou voto), e não a da data do julgamento. Sem data da peça: data do julgamento e `confianca = baixa`. A Lei 11.690/2008 renumerou o art. 386 do CPP: o antigo IV ("não existir prova de ter o réu concorrido") passou a ser o V; o novo IV é "estar provado que o réu não concorreu"; o VII é "não existir prova suficiente para a condenação".
- **R4.** Quando duas perguntas decidem, registre as duas e marque uma como principal. No máximo duas.
- **R5.** A pergunta principal é aquela em que o resultado se decidiu; havendo divergência, é aquela em que os votos se separaram. O critério é onde o placar se separou, não quantos ministros escreveram sobre ela (vale também para quem adere sem texto).
- **R5b.** Desempate em caso unânime: quando não houve divergência e as duas perguntas tiveram a mesma resposta, as duas são principais (`principal = Sim` nas duas). Não tente escolher pela ênfase do voto.
- **R6.** Preliminares (ex.: prescrição afastada no início do voto, competência do tribunal) não são questão decisiva.
- **R7.** A competência do agente para praticar o ato é parte da pergunta `concorreu`, e não uma pergunta separada.
- **R5c.** Empate na separação: quando as duas perguntas separam o placar exatamente do mesmo modo, as duas são principais pela R5.
- **R6b.** Exceção à R6: quando os votos se separam na própria preliminar (parte declara a prescrição e extingue a punibilidade, parte examina o mérito), ela é a pergunta principal pela R5.
- **R6c.** Unidade em que a única questão enfrentada é a prescrição, declarada por todos: a unidade fica sem questão decisiva (`questoes` vazia), com o motivo em `obs`.
- **R8.** Ministro cujo voto só consta da ata (ou só é conhecido pela referência de outros ministros, sem texto próprio no acórdão): `enfrentou_a_questao = Adesao`, a posição é a de quem conduz aquele lado (o relator, ou quem abriu a divergência), com `confianca = baixa` e a página em `inferida_de`. Se o próprio ministro sem texto é quem conduz o lado, diga isso em `obs` e use a melhor evidência disponível (a ata ou a descrição do voto dele feita por outro ministro, com página).
- **R10.** Questão declarada prejudicada pelo voto condutor não é questão decisiva: não a registre.
- **R11.** Fundamentou × aderiu, pelo conteúdo, não pela fórmula: `Sim` = há ao menos um trecho próprio, com página, que responde à questão, mesmo curto e mesmo com "acompanho"; `Adesao` = só declara acompanhar; `Nao` = a razão própria é outra questão (`posicao = nao_enfrentou`, razão em `fundamento_proprio`).
- **R12.** Maioria sem fundamento único: se nenhum fundamento, sozinho, reúne os votos necessários para formar o resultado, as duas questões que o formam são principais; `obs` registra o fundamento do voto condutor e o do desempate.
- **R15.** `modo_concurso` em réu absolvido: quando a resposta a `concorreu` é "não", fica `nao_dito`; o modo imputado pela denúncia, se houver, vai em `obs`.
- **R17.** Ata e texto em conflito: o resultado do voto (`voto_resultado`) vem da ata; a fundamentação vem do texto. Registre o conflito em `obs`.

### Categorias

Toda pergunta é respondida `sim` / `nao`, e o "sim" significa sempre que o elemento da acusação está presente (R9), salvo em `outra`, onde você marca a direção.

**`dolo`.** Pergunta-padrão: "Há comprovação de dolo do réu?"
- Definição: se há provas de que o réu agiu com dolo em relação aos itens da denúncia. O codebook não fixa o tipo de dolo: depende do tipo penal, e os próprios votos dizem qual exigem. Registre em `padrao_dolo_exigido` o que o voto diz (`generico` = basta saber e querer praticar a conduta; `especifico` = exige uma finalidade a mais; `nao_dito`). A ciência e a anuência do réu com o ato (saber e concordar) ficam aqui.
- Quando aplicar: quando os votos usam como base a questão do dolo, segundo a linguagem do voto.
- Quando não aplicar: quando a argumentação vai em outra direção, por exemplo a de quem fez ou decidiu o ato (`concorreu`).
- A suficiência de prova não é categoria: é o modo de responder (precisa haver prova que comprove o dolo).

**`concorreu`** (autoria/participação). Pergunta-padrão: "Há comprovação de que o réu concorreu para o fato denunciado?"
- Definição: se há provas de que o réu concorreu para o fato, como autor (praticou ou decidiu o ato) ou como partícipe (ajudou, instigou ou concorreu de outro modo). Inclui a competência do agente para o ato (R7). Registre em `modo_concurso` o que o voto disser (`autor`, `participe`, `nao_dito`; ver R15).
- Quando aplicar: quando os votos usam como base a questão de quem fez ou decidiu o ato.
- Quando não aplicar: quando a argumentação vai em outra direção, como o dolo.
- **Anotações de prova** (lista `anotacoes` da questão): `prova_colaboracao` quando a resposta depende da corroboração da palavra de colaborador premiado; `prova_inquerito` quando depende de prova produzida só no inquérito (art. 155 do CPP). A suficiência de uma prova específica não é categoria; fica marcada.

**`tipicidade`.** Pergunta-padrão: "O fato provado preenche os elementos do tipo imputado?"
- Definição: se a conduta, tal como provada, se enquadra no crime da denúncia, incluindo se o fato material existiu. Registre em `anotacao_tipicidade` qual é a dúvida: `existencia_fato` (o fato existiu?) ou `enquadramento` (o fato provado é este crime?).
- Quando aplicar: quando o voto discute uma elementar do tipo (ex.: "proveito próprio ou alheio" no peculato; "ordem judicial" no art. 1º, XIV, do DL 201/67) ou a existência do fato.
- Quando não aplicar: quando a dúvida é quem fez (`concorreu`), se o réu sabia e quis (`dolo`), prescrição ou questão processual, ou quando a elementar discutida é o ato de ofício da corrupção (categoria própria, abaixo).

**`ato_de_oficio`.** Pergunta-padrão: "A corrupção se configura sem ato de ofício determinado, bastando o nexo com a função?"
- Quando aplicar: quando o voto decide se a condenação por corrupção exige um ato de ofício identificado (praticado, omitido ou prometido) ou se basta o nexo da vantagem com as atribuições do cargo. "Sim" = basta o nexo (favorece a acusação); "não" = exige ato de ofício determinado.
- Atenção: um voto pode responder que exige ato de ofício e, em seguida, discutir se ele foi provado no caso. A segunda parte (houve o ato? o réu o praticou?) é outra pergunta, em geral `concorreu` ou `tipicidade`: registre as duas, pela R4, e marque a principal pela R5.

**`outra`.** Para o que não couber nas categorias acima. Descreva a pergunta em `questao_outra_descricao` (texto, em forma comparável, R1) e marque `sim_favorece` (`acusacao` / `defesa` / `neutra`: a quem favorece a resposta "sim", lida pelo primeiro ramo se a pergunta for dupla). Não force uma questão numa categoria se ela não couber.

### Voto condutor

`voto_condutor` é o ministro que **fundamenta** a razão de decidir, segundo o texto. Se o acórdão disser que decide "nos termos do voto" de outro ministro que só aderiu sem fundamentar, registre quem fundamenta e ponha a atribuição do acórdão em `obs`.

### Posição de cada ministro

Para **cada questão** da unidade (não só a principal), uma entrada por ministro votante:
- `enfrentou_a_questao`: `Sim` (fundamentou), `Adesao` (acompanhou sem fundamentar; ex.: "acompanho o relator"), `Nao` (votou por outra razão).
- `posicao`: `sim` / `nao` / `nao_enfrentou`, como o ministro respondeu à pergunta. Em `Adesao`, a posição é a de quem ele acompanhou, e isso é inferência declarada: diga de quem.
- `posicao_detalhe`: texto curto opcional (qualidade da prova, ressalvas).
- `fundamento_proprio`: quando ele chega ao mesmo resultado por outra questão.
- `voto_resultado`: `Condena` / `Absolve` / `Extingue` (extinção da punibilidade) / `Tranca` (trancamento, HC de ofício), lido no texto (R17: o resultado vem da ata). Se divergir do banco listado acima, **não corrija**: registre a divergência em `obs`.

### Precedente e mudança de regra

Para cada referência a decisão anterior ou mudança de regra usada na fundamentação desta unidade: `ministro`, `tipo` (`precedente_citado` / `mudanca_lei` / `mudanca_jurisprudencia` / `distincao` / `superacao`), `referencia` (como aparece no texto), `sentido` (`para_seguir` / `para_afastar`), `proprio_ministro` (`Sim` se o ministro cita voto seu anterior), `evidencia`, `fonte`. `distincao` = o ministro diz que o caso anterior é diferente deste; `superacao` = diz que o entendimento anterior deixa de valer. Citações de doutrina não entram. Lista vazia se não houver.

## Regra de evidência

Todo campo de valor é um objeto `{"valor": …, "evidencia": "transcrição literal", "fonte": "p. N", "confianca": "alta|media|baixa"}`. **Sem evidência literal com página, `valor = null`: nunca infira.** Única exceção: a posição em `Adesao`, declarada como inferida. Não resuma o acórdão. Transcrições literais curtas (até ~3 frases), com a página do marcador.

## Saída

Escreva um único arquivo JSON válido em `{SAIDA}`, com esta forma:

```json
{
  "id_caso": "…",
  "lido_em": "AAAA-MM-DD",
  "paginas_lidas": "ex.: 1-7 (todas)",
  "unidades": [
    {
      "id_unidade": "…",
      "unidade_origem": "…",
      "fato": "…",
      "escopo_levcovitz": {"valor": "Sim", "evidencia": "…", "fonte": "p. N", "confianca": "…"},
      "ajuste_unidade": null,
      "voto_condutor": {"valor": "…", "evidencia": "…", "fonte": "p. N", "confianca": "…"},
      "questoes": [
        {
          "questao_decisiva": {"valor": "dolo|concorreu|tipicidade|ato_de_oficio|outra", "evidencia": "…", "fonte": "p. N", "confianca": "…"},
          "questao_outra_descricao": null,
          "sim_favorece": "acusacao|defesa|neutra (só em outra; nas demais, acusacao)",
          "anotacao_tipicidade": "existencia_fato|enquadramento|null",
          "anotacoes": [],
          "principal": {"valor": "Sim|Nao", "evidencia": "…", "fonte": "p. N", "confianca": "…"},
          "formulacao": {"valor": "transcrição literal", "fonte": "p. N"},
          "resposta_tribunal": {"valor": "sim|nao", "evidencia": "…", "fonte": "p. N", "confianca": "…"},
          "padrao_dolo_exigido": {"valor": "generico|especifico|nao_dito", "evidencia": "…", "fonte": "p. N", "confianca": "…"},
          "modo_concurso": null,
          "posicoes": [
            {
              "ministro": "…",
              "voto_resultado": {"valor": "Condena|Absolve|Extingue|Tranca", "evidencia": "…", "fonte": "p. N", "confianca": "…"},
              "enfrentou_a_questao": {"valor": "Sim|Adesao|Nao", "evidencia": "…", "fonte": "p. N", "confianca": "…"},
              "posicao": {"valor": "sim|nao|nao_enfrentou", "evidencia": "…", "fonte": "p. N", "confianca": "…", "inferida_de": null},
              "posicao_detalhe": null,
              "fundamento_proprio": null
            }
          ]
        }
      ],
      "precedentes": [],
      "obs": null
    }
  ],
  "avisos": ["dúvidas, ambiguidades, o que não coube no codebook"]
}
```

Ao terminar, responda em até 10 linhas: unidades preenchidas, questão principal de cada uma, quantos campos ficaram `null` e por quê, e os avisos.
=====FIM=====
