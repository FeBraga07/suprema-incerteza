# Gabarito de Validação — Extração de Placar e Resultado por Leitura de Ata

## TCC — Insegurança Jurídica e o STF: Uma Análise Institucional

> Última atualização: 08/08/2026.
> Insumo direto para a seção de metodologia (defende a decisão D-003: regex proibido para placar/resultado).

---

## 1. Propósito e como usar

A Onda 2/3 da coleta extraiu resultado, placar e votos por **cascata de expressões regulares** sobre o texto da ata de julgamento (`acordao_ata`). O método errou em pelo menos 12 dos 26 casos do banco — Felipe detectou e corrigiu cada erro manualmente, lendo a ata. Essas correções hoje só existem como prosa em `_registro_metodologico_coleta.md` (seções 3.5 e 4.4), em `_metodologia_coleta_onda2.md` (seção 5) e em `_metodologia_coleta_onda3.md` (seção 5) — mais algumas células já corrigidas na planilha. Não havia, até este documento, um conjunto de teste explícito.

**A decisão D-003 manda refazer a extração por leitura (LLM lendo a ata), não por regex.** Este arquivo é o gabarito contra o qual essa nova extração deve ser validada, antes de aceitar seus resultados para o restante do banco.

**Como usar:**

1. Rodar a extração nova **"cega"** — sem mostrar ao extrator os valores deste gabarito, só o `acordao_ata` bruto de cada AP listada na Seção 3.
2. Para cada linha (caso/réu × campo) com valor correto **firme** (não marcado "a apurar"), comparar o valor produzido pela extração nova contra a coluna "Valor correto (apurado)".
3. Reportar acurácia por campo segundo as métricas da Seção 4 — nunca só um número agregado único, porque os campos têm naturezas diferentes (categórico, binário, contínuo).
4. Tratar qualquer discrepância entre este gabarito e a extração nova como candidata a **novo erro documentado** — investigar lendo a ata antes de decidir se o gabarito ou a extração nova está certa. Este gabarito também pode conter imprecisões herdadas do processo manual original; ele é a melhor referência disponível, não uma verdade absoluta e acima de verificação.
5. Ler a Seção 6 (limitações) antes de generalizar a acurácia medida aqui para o banco inteiro.

---

## 2. ⚠️ Divergências encontradas entre a metodologia (.md) e a planilha atual

Ao conferir os valores documentados contra `dados/brutos/snapshot_planilha_2026-05-17.xlsx` (aba `2_casos_reus`, com a coluna extra `modalidade_corrupção` na coluna D — `cargo_funcao` cai em E, `resultado_reu` em F, `resultado_binario` em G, `n_votantes` em H, `votos_condenacao` em I, `votos_absolvicao` em J, `margem_votos` em K, `perc_vencedor` em L, `unanime` em M, `categoria_placar` em N), duas inconsistências apareceram que precisam de resolução **antes** de tratar este gabarito como definitivo:

- **AP-432:** `_registro_metodologico_coleta.md` (3.5) e `_metodologia_coleta_onda2.md` (5.2) registram a correção como `Condenação parcial`; 11 votantes; 8×3 (vencidos: Teori Zavascki, Gilmar Mendes, Marco Aurélio); Apertado. A planilha atual (linha 17) mostra `resultado_reu = Condenação` (não "parcial"), `n_votantes = 8`, `votos_condenacao = 5`, `votos_absolvicao = 3`. Os números batem em parte (3 vencidos é consistente com votos_absolvicao=3), mas `n_votantes` e `resultado_reu` divergem do que o .md registra como correção aplicada.
- **AP-1036:** a aba `3_votos` (linha 535) tem `voto_resultado = Absolvição mérito` para o relator Dias Toffoli, unânime — consistente com a correção documentada em `_metodologia_coleta_onda3.md` (5.4, verbo "absolveu" adicionado ao parser). Mas a aba `2_casos_reus` (linha 83) tem `resultado_reu = Condenação`, `resultado_binario = 1`, unânime — o oposto binário do que `3_votos` registra para o mesmo caso.

### ✅ RESOLVIDO em 08/08/2026 — pela ata integral, não por arbitragem

A regra provisória adotada acima — *"na dúvida, vale o valor documentado nos .md"* — **estava errada, e de forma grave**: nos campos de placar da AP-432 o `.md` reproduz exatamente um dos erros que este gabarito existe para detectar. A régua continha uma instância do defeito que ela deveria medir. Se a validação tivesse rodado assim, teria **penalizado o extrator por acertar**.

As duas divergências foram resolvidas lendo a ata integral (recuperada do índice do STF em 08/08/2026). Felipe confirmou, na mesma data, que as correções foram feitas à mão diretamente na planilha — o que explica a divergência, mas não determina quem está certo. Quem determina é a ata.

**AP-1036** — ata integral: *"O Tribunal, por unanimidade, considerou não haver prova suficiente para a condenação do acusado pelo crime descrito na denúncia (art. 317, caput e § 1º, do Código Penal), motivo pelo qual **o absolveu** (art. 386, inciso VII, do CPP), nos termos do voto do Relator. Afirmou suspeição o Ministro Alexandre de Moraes."*

| Campo | Valor correto | Quem estava certo |
|---|---|---|
| `resultado_reu` | **Absolvição mérito** | a aba `3_votos` e o `.md` |
| `resultado_binario` | **0** | idem |
| `n_votantes` | **10** (11 menos a suspeição de Alexandre de Moraes) | nenhum dos dois registrava isso |
| `unanime` | sim | ambos |

> A célula `resultado_reu = Condenação` da aba `2_casos_reus` é **falsa** e inverte o resultado do caso. Corrigir na reconstrução.

**AP-432** — ata integral: *"por maioria, julgou **parcialmente procedente** a ação penal para condenar o réu pelo delito previsto no inciso II do art. 1º do Decreto-lei nº 201/1967, **vencidos os Ministros Teori Zavascki, Gilmar Mendes e Marco Aurélio**, que o absolviam. (…) **Ausentes, justificadamente, os Ministros Joaquim Barbosa (Presidente) (…) e Celso de Mello, e, ausente neste julgamento, a Ministra Cármen Lúcia.**"*

| Campo | Valor correto | Quem estava certo |
|---|---|---|
| `resultado_reu` | **Condenação parcial** | o `.md` |
| `n_votantes` | **8** (11 menos 3 ausentes) | **a planilha** |
| `votos_condenacao` | **5** | **a planilha** |
| `votos_absolvicao` | **3** | ambos |

> O `.md` registra 11 votantes e 8×3 — **contagem fixada em 11 ignorando as três ausências**, que é um dos padrões de erro catalogados na Seção 4 deste próprio documento. Cada fonte acertou uma metade: a metodologia acertou o resultado, a planilha acertou o placar.

**Observação para a taxonomia de resultado.** Na AP-432 houve condenação **seguida de extinção da punibilidade por prescrição retroativa**. Isso não é a mesma coisa que absolvição por prescrição, e a taxonomia de `motivo` precisa distinguir os dois — sob pena de um caso condenatório ser contado como absolvição.

**Lição de método, para o texto.** Divergência entre duas fontes derivadas não se resolve por hierarquia entre elas. Resolve-se voltando à fonte primária. Foi o que o item 4 da Seção 1 já mandava fazer, e o que a regra provisória acima contrariava.

---

## 3. Gabarito por caso

Convenção: **Valor errado** = o que a cascata de regex (Onda 2/3, documentada em `_metodologia_coleta_onda2.md` §4.1 e `_metodologia_coleta_onda3.md` §4) produziria ou produziu antes da correção manual. **Valor correto** = o valor apurado por Felipe lendo a ata, conforme registrado nos .md de metodologia. Onde o valor exato produzido pelo script não foi registrado por escrito (os .md descrevem a *natureza* do erro sem sempre citar o número/string exato que saiu), isso é declarado explicitamente — não foi inventado.

### AP-409 — José Gerardo Oliveira de Arruda Filho (AP-409-R01)

| Campo | Valor errado (script) | Valor correto (apurado) | Natureza do erro |
|---|---|---|---|
| `resultado_reu` | `Absolvição prescrição` | `Condenação` | (a) Falso positivo de prescrição — "prescrição da pretensão punitiva" aparecia só no argumento da corrente vencida (que pedia redução de pena até a faixa de prescrição em abstrato), não no resultado |
| `resultado_binario` | 0 | 1 | Consequência direta do erro acima |
| `n_votantes` | 11 (padrão) | 10 | (b) Contagem de votantes fixada em 11, ignorando que a ata registra "Ausente, neste julgamento, o Senhor Ministro" — Ellen Gracie ausente |
| `votos_condenacao` / `votos_absolvicao` | Não registrado nos .md com exatidão — decorrência em cascata do erro de resultado (o script provavelmente não teria contado voto de condenação algum, dado `resultado_binario=0`) | 7 / 3 | (c) Placar errado como consequência de (a)+(b) |
| `categoria_placar` | Não registrado nos .md | `Folgado` | Consequência em cascata |

Fonte: `_registro_metodologico_coleta.md` §3.5; `_metodologia_coleta_onda2.md` §5.1. Confirmado na planilha (`2_casos_reus` linha 15) — sem divergência.

### AP-432 — Jairo Ataíde Vieira (AP-432-R01)

| Campo | Valor errado (script) | Valor correto (apurado, conforme .md) | Natureza do erro |
|---|---|---|---|
| `resultado_reu` | Não registrado com exatidão nos .md — classificado como "mesmo padrão de falso positivo" da AP-409 | `Condenação parcial` | (a) Falso positivo de prescrição — ata diz "julgou parcialmente procedente", mas menciona prescrição como tese alternativa dos vencidos |
| `n_votantes` | Não registrado nos .md | 11 — ⚠️ **diverge da planilha atual, que mostra 8** (ver Seção 2) | A apurar / reconciliar |
| `votos_condenacao` / `votos_absolvicao` | Não registrado nos .md | 8 / 3 (vencidos: Teori Zavascki, Gilmar Mendes, Marco Aurélio) — ⚠️ **planilha mostra 5/3** (ver Seção 2) | A apurar / reconciliar |
| `categoria_placar` | Não registrado nos .md | `Apertado` | Consequência em cascata |

Fonte: `_registro_metodologico_coleta.md` §3.5; `_metodologia_coleta_onda2.md` §5.2. **Ver alerta de divergência na Seção 2 antes de usar `n_votantes` e os votos deste caso como gabarito firme.**

### AP-372 — Jackson Barreto de Lima e Roberto Sales Cardoso (AP-372-R01, AP-372-R02)

| Campo | Valor errado (script) | Valor correto (apurado) | Natureza do erro |
|---|---|---|---|
| `n_votantes` (ambos os réus) | 11 (padrão) | **9** | (b) Contagem fixada em 11 ignorando "Ausente, neste julgamento, o Senhor Ministro Gilmar Mendes" |

`resultado_reu` (Absolvição mérito, unânime) não foi afetado — único erro do caso foi a contagem de votantes.

Fonte: `_registro_metodologico_coleta.md` §3.5; `_metodologia_coleta_onda2.md` §5.3. Confirmado na planilha (`2_casos_reus` linhas 9–10) — sem divergência.

### ✅ CORRIGIDO em 09/08/2026 — o valor de 10 também estava errado (o gabarito reproduzia, de forma mais sutil, o mesmo padrão de erro (b) que ele mesmo cataloga)

A extração cega do L1 (09/08/2026) encontrou `n_votantes = 9`, divergindo deste gabarito (10). Investigado antes de decidir quem estava certo (Seção 1, item 4, regra do próprio gabarito): a AP-372 foi julgada em 16/12/2010. Eros Grau deixou a Corte em 18/08/2010 (quatro meses antes) e Luiz Fux só tomou posse em 03/03/2011 (quase três meses depois) — havia vacância real na cadeira de Eros Grau na data do julgamento. O Tribunal Pleno tinha, portanto, **10 ministros em exercício, não 11**. A própria ata é consistente com isso: nomeia exatamente 10 ministros ao todo (9 presentes + Gilmar Mendes ausente), nunca um 11º nome.

**O valor correto é 9** — o gabarito descontou corretamente a ausência nomeada de Gilmar Mendes, mas partiu de uma base de 11 (composição plena presumida) sem checar se a Corte tinha 11 membros na data do julgamento. É o mesmo erro (b) que este documento cataloga na Seção 4, só que numa camada mais sutil: o script errava fixando em 11 sem descontar ausência nenhuma; aqui o processo manual descontou a ausência certa, mas sobre uma base já errada. `n_votantes` corrigido para **9** na tabela acima. Ver `dados/derivados/casos/AP-372.json` (campo `n_votantes`, aviso de divergência).

### AP-565 — Todos os 9 réus (AP-565-R01 a R09)

| Campo | Valor errado (script) | Valor correto (apurado) | Natureza do erro |
|---|---|---|---|
| `cargo_funcao` | `Juiz` | (vazio — cargo não identificável com certeza) | (f) Cargo capturado por correspondência equivocada do regex com o contexto da ementa |
| `resultado_reu` | `Absolvição prescrição` | `Condenação parcial` | (a) Falso positivo de prescrição — ata diz "julgou parcialmente procedente, vencidos Marco Aurélio e Ricardo Lewandowski" |
| `votos_condenacao` / `votos_absolvicao` | Não registrado nos .md com exatidão | 9 / 2 | (c) Consequência em cascata do erro de resultado |
| `categoria_placar` | Não registrado nos .md | `Folgado` | Consequência em cascata |

Fonte: `_registro_metodologico_coleta.md` §3.5; `_metodologia_coleta_onda2.md` §5.4. Confirmado na planilha (`2_casos_reus` linhas 67–75) — sem divergência.

### ❌ CORREÇÃO ACIMA ANULADA em 09/08/2026 — o placar "9x2 uniforme" não existe na ata; é o mesmo padrão de erro da AP-470, só que não detectado antes

A extração cega do L1 (09/08/2026) divergiu fortemente deste gabarito: nenhum placar "9x2" aparece em lugar algum da ata (`corpus/texto/AP-565.txt`, linhas ~13479-13514). Investigado antes de decidir quem estava certo (Seção 1, item 4): o gabarito **colapsou nove resultados distintos numa única linha** — exatamente o padrão de erro que a Onda 2/3 cometia em casos multi-réu (documentado à parte para a AP-470, Seção "não aplicável ao formato erro→correção" abaixo), só que aqui ninguém tinha percebido que o mesmo colapso também aconteceu na correção manual.

**O quadro real, por grupo de réu, no art. 90 da Lei 8.666/93 (crime de escopo Levcovitz — o art. 288, quadrilha, é absolvido por maioria 8x2 para todos os 9 réus e fica fora do escopo):**

| Grupo de réus | `resultado_reu` | Placar (art. 90) | `unanime` |
|---|---|---|---|
| Ivo Narciso Cassol, Salomão da Silveira, Erodi Antonio Matt | `Condenação parcial` | 10×0 (condenação) | Sim |
| Aníbal de Jesus Rodrigues, Neilton Soares dos Santos, Izalino Mezzomo, Josué Crisóstomo | `Absolvição` | 5×5, empate desfeito a favor do réu | Não |
| Ivalino Mezzomo, Ilva Mezzomo Crisóstomo | `Absolvição` | 0×10 (absolvição) | Sim |

`votos_condenacao`/`votos_absolvicao`/`categoria_placar` da tabela acima ficam **anulados** — não existe um par único (9/2, `Folgado`) válido para o caso; cada grupo tem o seu. O achado sobre `cargo_funcao` (regex capturou "Juiz" por correspondência equivocada) permanece válido e não é afetado por esta correção.

Fonte: `dados/derivados/casos/AP-565.json` (`_validacao_gabarito` e campos por réu), lendo diretamente `corpus/texto/AP-565.txt` linhas ~13479-13514.

### AP-470 (Mensalão) — 40 réus — não aplicável ao formato erro→correção

O script **não tentou** extrair resultado individual para nenhum dos 40 réus — a ata tem ~114.000 caracteres com sub-julgamentos por réu e por crime, estrutura que o parser reconhecidamente não conseguia separar. Todos os 40 réus foram marcados `⚠️revisar` deliberadamente, sem processamento automático (`_registro_metodologico_coleta.md` §3.5; `_metodologia_coleta_onda2.md` §5.5).

Não há, portanto, um par (valor errado do script → valor correto) para catalogar aqui — é ausência de dado, não erro de extração. Fica fora do gabarito de acurácia por campo, mas continua sendo o teste mais exigente para a extração nova (ata longa, multi-réu, multi-crime).

**Achado à parte:** a planilha atual (`2_casos_reus` linha 49, `AP-470-R24`, réu Carlos Alberto Quaglia) tem `resultado_reu = Anulação` — um valor diferente de `⚠️revisar` e diferente de qualquer categoria do esquema documentado (`Condenação` / `Condenação parcial` / `Absolvição mérito` / `Absolvição proc.` / `Absolvição prescrição`). Não há registro em nenhum .md de quando ou como esse valor foi apurado. **A apurar:** confirmar com Felipe se essa célula reflete revisão manual real e, se sim, documentar a fonte; se não, tratar como resíduo a limpar.

### AP-441 — José Abelardo Guimarães Camarinha e Walter Miosi (AP-441-R01, R02) — sem valor correto documentado

`_registro_metodologico_coleta.md` §3.6 e `_metodologia_coleta_onda2.md` §5 (Limitações, item 2) registram que a contagem de votos ficou **em branco (0/0)** porque a ata não trouxe placar explícito nem lista de vencidos em formato padronizado, e recomendam verificação manual — que não está documentada como tendo sido concluída.

| Campo | Valor errado (script, documentado) | Valor correto (apurado) | Natureza do erro |
|---|---|---|---|
| `n_votantes`, `votos_condenacao`, `votos_absolvicao`, `categoria_placar` | 0 / 0 / 0 / (vazio) | **A apurar** — a planilha atual mostra `n_votantes=10, votos_condenacao=9, votos_absolvicao=1, categoria_placar=Folgado`, mas nenhum .md documenta o processo de verificação manual que teria produzido esses números. Não é seguro tratá-los como gabarito sem confirmação | Limitação de fonte — nomes sob possível sigilo do STF (iniciais), ata sem placar padronizado |

**Não incluir os campos de placar da AP-441 no cálculo de acurácia até que a origem dos valores atuais da planilha seja confirmada com Felipe.**

### AP-433 — Fernando Lúcio Giacobo e Alceni Angelo Guerra (AP-433-R01, R02)

| Campo | Valor errado (script) | Valor correto (apurado) | Natureza do erro |
|---|---|---|---|
| Sessão/relator capturados | 1ª sessão (05/03/2010): empate 5×5, inconclusiva; `eh_relator`/resultado marcados `⚠️verificar` | 2ª sessão (11/03/2010), com um ministro adicional: `Absolvição mérito` por maioria | (g) *[padrão adicional, não estava na lista mínima]* Ata multi-sessão — script capturou a sessão errada (inconclusiva) em vez da sessão que efetivamente resolveu o julgamento |
| `n_votantes` | Indeterminado (sessão de empate) | 11 | Consequência do erro de sessão |
| `votos_condenacao` / `votos_absolvicao` | Indeterminado | 5 / 6 | Consequência do erro de sessão |
| Vencidos | Não capturados corretamente | Ellen Gracie (relatora), Cezar Peluso (revisor), Cármen Lúcia, Joaquim Barbosa, Ayres Britto — todos vencidos, votaram Condenação | Consequência do erro de sessão |

Fonte: `_registro_metodologico_coleta.md` §4.4; `_metodologia_coleta_onda3.md` §5.1. Confirmado em `2_casos_reus` (linhas 18–19) e `3_votos` (linhas 22–31) — sem divergência.

### AP-447 — Sérgio Ivan Moraes e Maria Neli Groff da Silva (AP-447-R01, R02)

| Campo | Valor errado (script) | Valor correto (apurado) | Natureza do erro |
|---|---|---|---|
| Vencidos (tokens capturados) | "Menezes Direito e" e "Ministros" capturados como tokens de vencido | Removidos — não são vencidos no mérito | (e) Tokens espúrios capturados da frase "vencidos os Srs. Ministros Menezes Direito e Marco Aurélio" da **questão preliminar** (licitude da gravação), não do mérito |
| Vencidos (lista final) | Incompleta/incorreta pelos tokens espúrios | Joaquim Barbosa, Eros Grau, Cezar Peluso, Marco Aurélio (Marco Aurélio também vencido na preliminar, mas isso é observação à parte, não motivo de exclusão) | Consequência de (e) |
| `n_votantes` | 11 (padrão) | 10 | (b) Ellen Gracie ausente justificadamente, não capturada |
| `votos_condenacao` / `votos_absolvicao` | Não registrado nos .md com exatidão | 4 / 6 | (c) Consequência em cascata |

Fonte: `_registro_metodologico_coleta.md` §4.4; `_metodologia_coleta_onda3.md` §5.2. Confirmado em `2_casos_reus` (linhas 22–23) e `3_votos` (linhas 34–45) — sem divergência.

### AP-462 — Lindomar Barbosa Alves (AP-462-R01)

| Campo | Valor errado (script) | Valor correto (apurado) | Natureza do erro |
|---|---|---|---|
| Nome de ministro vencido | `Marco` | `Marco Aurélio` | (d) Nome truncado por quebra de linha (`\n`) no meio do nome, dentro do texto da ata |
| Ausentes | Celso de Mello e Menezes Direito não capturados | Celso de Mello (ausente — não assistiu ao relatório); Menezes Direito (ausente — licenciado) | (b) Ausência não capturada pelo regex de vencidos/ausentes |
| `n_votantes` | 11 (padrão) | 9 | Consequência de (b) |
| `votos_condenacao` / `votos_absolvicao` | Não registrado nos .md com exatidão | 1 / 8 | (c) Consequência em cascata |

Fonte: `_registro_metodologico_coleta.md` §4.4; `_metodologia_coleta_onda3.md` §5.3. Confirmado em `2_casos_reus` (linha 24) e `3_votos` (linhas 46–49) — sem divergência.

### AP-1036 — Ezequiel Ferreira de Souza (AP-1036-R01)

| Campo | Valor errado (script) | Valor correto (apurado) | Natureza do erro |
|---|---|---|---|
| `motivo_ausencia` (Alexandre de Moraes) | `Impedimento` | `Suspeição` | Motivo de ausência mal classificado — a ata registra "afirmou suspeição", não impedimento (categoria próxima de (b), mas sobre a *natureza* da ausência, não sua detecção) |
| `voto_resultado` / `resultado_reu` | `⚠️verificar` (verbo "absolveu" não reconhecido pelo parser) | `Absolvição mérito` (unânime) | (h) *[padrão adicional]* Verbo de resultado fora do vocabulário do regex — ⚠️ **atenção: a aba `2_casos_reus` da planilha atual mostra `Condenação`/binário 1 para este caso, contradizendo `3_votos` e a correção documentada** (ver Seção 2). Adotado o valor documentado como gabarito; a célula de `2_casos_reus` precisa ser corrigida ou explicada antes de qualquer uso |

Fonte: `_registro_metodologico_coleta.md` §4.4; `_metodologia_coleta_onda3.md` §5.4–5.5.

### AP-348 — Leonel Arcângelo Pavan (AP-348-R01)

| Campo | Valor errado (script) | Valor correto (apurado) | Natureza do erro |
|---|---|---|---|
| `voto_resultado` / `resultado_reu` | `⚠️verificar` | `Absolvição mérito` (unânime) | (h) Verbo "absolveu" não reconhecido pelo parser original (`getRes()` só reconhecia "julgou procedente/improcedente") |

Fonte: `_metodologia_coleta_onda3.md` §5. Confirmado em `2_casos_reus` (linha 6) e `3_votos` (linha 6) — sem divergência.

### AP-365 — Jackson Barreto de Lima e Sérgio Bezerra de Sant'Ana (AP-365-R01, R02)

| Campo | Valor errado (script) | Valor correto (apurado) | Natureza do erro |
|---|---|---|---|
| `voto_resultado` / `resultado_reu` (ambos os réus) | `⚠️verificar` | `Absolvição mérito` (unânime) | (h) Mesmo padrão de AP-348 — verbo "absolveu" fora do vocabulário do regex |

Fonte: `_metodologia_coleta_onda3.md` §5. Confirmado em `2_casos_reus` (linhas 7–8) e `3_votos` (linhas 7–8) — sem divergência.

---

## 4. Taxonomia de padrões de erro

| Código | Padrão | Casos no gabarito |
|---|---|---|
| (a) | **Falso positivo de prescrição** — "prescrição"/"prescri" aparecia no argumento da corrente vencida ou como tese alternativa, não no resultado efetivo do julgamento | AP-409, AP-432, AP-565 |
| (b) | **Número de votantes fixado em 11** (composição plena presumida), ignorando ministros ausentes, impedidos ou suspeitos que a ata registra explicitamente | AP-372, AP-409, AP-447, AP-462 |
| (c) | **Placar errado como consequência de (a) e/ou (b)** — votos_condenacao/votos_absolvicao/categoria_placar herdam o erro upstream | AP-409, AP-432 (parcial), AP-565, AP-447, AP-462 |
| (d) | **Nome de ministro truncado por quebra de linha** no texto bruto da ata | AP-462 |
| (e) | **Tokens espúrios capturados de questão preliminar** em vez do mérito | AP-447 |
| (f) | **Cargo do réu capturado por correspondência equivocada do regex** com o contexto da ementa | AP-565 |
| (g) *(adicional)* | **Ata multi-sessão** — script capturou a sessão errada (inconclusiva/empate) em vez da sessão que resolveu o julgamento | AP-433 |
| (h) *(adicional)* | **Verbo de resultado fora do vocabulário do regex** (ex.: "absolveu" em vez de "julgou improcedente") — produz placeholder de erro em vez de classificação | AP-348, AP-365, AP-1036 |
| *(sem código)* | **Ausência de processamento automático** por estrutura da ata incompatível com o parser (multi-réu, multi-crime, ata muito longa) | AP-470 |
| *(sem código)* | **Fonte com sigilo/anonimização** — nomes truncados a iniciais, ata sem placar em formato padronizado | AP-441 |

Os padrões (a)–(f) são os seis citados como piso obrigatório na tarefa que originou este gabarito; (g) e (h) foram descobertos ao ler as correções da Onda 3 e não estavam na lista original — vale a pena a nova extração ser testada contra eles também, já que são falhas de mecanismo de leitura (não de vocabulário de busca) e portanto continuam relevantes mesmo trocando regex por LLM.

---

## 5. Métricas propostas para reportar a acurácia da extração nova

Reportar **por campo**, nunca só um número agregado — os campos têm naturezas diferentes:

**Campos categóricos** (`resultado_reu`, `categoria_placar`, `cargo_funcao`, `motivo_ausencia`):
- Taxa de acerto exato = nº de linhas do gabarito com valor correto firme em que a extração nova bate exatamente ÷ total de linhas com valor firme para aquele campo.
- Matriz de confusão para `resultado_reu` (5 categorias) — permite ver se o erro concentrado é ainda o falso positivo de prescrição (padrão a) ou migrou para outra confusão.

**Campos binários** (`resultado_binario`, `unanime`, `voto_vencido`, `ausente_impedido`):
- Acurácia, mais precisão/recall/F1 tratando "Absolvição prescrição" como classe positiva especificamente nos casos-gabarito do padrão (a) — essa é a métrica mais diretamente ligada ao motivo do D-003.

**Campos numéricos** (`n_votantes`, `votos_condenacao`, `votos_absolvicao`, `margem_votos`):
- % de acerto exato.
- % dentro de ±1 do valor correto (tolerância a erro de contagem de 1 ministro).
- Erro médio absoluto (MAE).

**Campos de texto livre** (nome de ministro, tokens de vencido):
- % de acerto exato após normalização (case, acentuação).
- Verificação manual dirigida aos casos (d) e (e) — truncamento e tokens espúrios são erros de char-level que merecem checagem visual, não só string-match.

**Métrica por padrão da taxonomia:**
- Para cada código (a)–(h), taxa de reincidência = proporção dos casos daquele padrão em que a extração nova reproduz o mesmo tipo de erro. Reincidência zero no padrão (a), por exemplo, seria evidência direta de que a leitura por LLM resolve o problema que motivou D-003.

**Cobertura do gabarito em si:**
- Reportar também quantas linhas do gabarito ficaram de fora da comparação por terem valor correto marcado "a apurar" (AP-441, parte de AP-432, AP-470-R24) — essas não contam nem a favor nem contra a extração nova até serem resolvidas.

---

## 6. Limitações — leia antes de generalizar

1. **Este gabarito não é amostra aleatória.** Cobre exclusivamente os 12 casos em que um erro **foi detectado** durante a Onda 2/3 — nenhum processo sistemático de auditoria varreu os outros 14 casos do banco (26 total) em busca de erros não percebidos. Ele mede a acurácia da extração nova nos **casos difíceis já conhecidos**, não a taxa de erro do universo de 82 réus.

2. **Viés de detecção.** Os erros aqui são, por construção, os que Felipe percebeu ao revisar — provavelmente os mais grosseiros (resultado invertido, placar visivelmente errado) ou os que geraram um placeholder de erro explícito (`⚠️verificar`, `⚠️revisar`). Erros silenciosos — por exemplo, um cargo capturado incorretamente mas plausível, ou uma contagem de votantes errada por 1 sem gerar inconsistência visível — não têm chance de aparecer neste gabarito.

3. **Duas divergências não resolvidas** entre a metodologia documentada e a planilha atual (AP-432, AP-1036 — Seção 2) enfraquecem a confiabilidade desses dois casos como gabarito até serem reconciliados.

4. **AP-441 não contribui hoje** com nenhum valor correto firme para os campos de placar — só um valor errado documentado (0/0) e um valor de planilha sem processo de verificação registrado.

**Como complementar para uma estimativa não enviesada:** desenhar uma amostra aleatória estratificada (por década de julgamento e por tipo de resultado, para não sub-representar unanimidades) dentre os 82 réus do banco, independente de terem ou não sido sinalizados como problemáticos na coleta original. Para cada réu sorteado, ler a ata do zero (sem consultar a extração antiga nem a extração nova) e registrar o valor correto — só então comparar contra a saída da extração nova. Esse segundo conjunto, cego e aleatório, é o que permite estimar a taxa de erro geral do método; este gabarito mede especificamente a taxa de correção nos casos-armadilha já mapeados. Um tamanho de amostra na casa de 20–25 réus (~25–30% do banco) já dá margem para detectar taxas de erro moderadas com razoável confiança, dado o n pequeno do banco inteiro.

---

## 7. O que falta apurar

- **AP-432:** reconciliar `n_votantes` e `votos_condenacao`/`votos_absolvicao` entre o que `_registro_metodologico_coleta.md`/`_metodologia_coleta_onda2.md` registram (11 votantes, 8×3) e o que a planilha atual mostra (8 votantes, 5×3). Reler a ata para decidir qual está certo.
- **AP-1036:** reconciliar `resultado_reu`/`resultado_binario` entre `2_casos_reus` (Condenação, binário 1) e `3_votos` (Absolvição mérito, binário 0) — só um pode estar certo.
- **AP-441:** confirmar se os valores de placar hoje na planilha (`n_votantes=10, votos_condenacao=9, votos_absolvicao=1, categoria_placar=Folgado`) vieram de verificação manual por leitura da ata, ou são resíduo não documentado. Sem essa confirmação, nenhum valor de placar da AP-441 entra no gabarito.
- **AP-470-R24 (Carlos Alberto Quaglia):** a planilha tem `resultado_reu=Anulação`, valor fora do esquema documentado e sem registro de origem. Confirmar com Felipe.
- **AP-470 (demais 39 réus):** não há gabarito — é trabalho de leitura ainda não feito, não uma correção de erro. Fica para quando a extração nova processar a AP-470; nesse momento, os resultados por réu apurados manualmente (à medida que forem lidos) devem ser adicionados a este arquivo.
- **Valores exatos "errados"** que os .md não registraram por escrito (marcados "não registrado nos .md com exatidão" nas tabelas acima) — se o script antigo ainda estiver disponível para rodar isoladamente, rodá-lo sobre a ata de cada um desses casos preencheria a lacuna, mas não é essencial: o valor correto é o que importa para validar a extração nova.
