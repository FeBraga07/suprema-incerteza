# Agrupamento das 32 questões de direito: revisão cega

Revisor: subagente independente (claude-opus-5-5), 24/10/2026. Fonte única: `questoes_direito_cegas.md`, mais consultas pontuais ao inteiro teor (AP-441 p. 46-48; AP-432 p. 12-14; AP-375 p. 6-7; AP-365 p. 13; AP-470 p. 3685-3687; AP-503, que não tem marcadores de página no texto extraído e por isso foi lido por busca de termo, incluindo a ementa e a certidão de julgamento). Nenhum outro arquivo do projeto foi aberto.

**Nota sobre o campo "resposta".** Pelo conjunto, o campo parece codificar "a conduta se enquadra no tipo? (sim = enquadra / condena)", e não a resposta literal à frase registrada. Exemplo: Q02 pergunta "o tipo exige ato de ofício predeterminado?" e traz "nao", embora o Tribunal tenha absolvido justamente porque exigiu esse ato. Li as respostas nessa chave. Se a chave for outra, as comparações de resposta da seção 2 precisam ser relidas.

## 1. Tabela

| id | caso | grupo | confiança |
|---|---|---|---|
| Q01 | AP-503 | G6 | baixa |
| Q02 | AP-307 | G1 | alta |
| Q03 | AP-470 | G1 | média |
| Q04 | AP-375 | G3 | média |
| Q05 | AP-307 | G1 | alta |
| Q06 | AP-503 | U1 (unitário) | alta |
| Q07 | AP-441 | G6 | média |
| Q08 | AP-307 | G2 (só AP-307) | alta |
| Q09 | AP-441 | G6 | média |
| Q10 | AP-470 | G1 | média |
| Q11 | AP-365 | G3 | média |
| Q12 | AP-375 | G4 | alta |
| Q13 | AP-432 | G5 | média |
| Q14 | AP-470 | G1 | média |
| Q15 | AP-365 | G4 | alta |
| Q16 | AP-375 | G3 | alta |
| Q17 | AP-503 | U2 (unitário) | alta |
| Q18 | AP-441 | G5 | média |
| Q19 | AP-470 | G1 | média |
| Q20 | AP-372 | G3 | média |
| Q21 | AP-503 | G6 | média |
| Q22 | AP-433 | U3 (só AP-433) | alta |
| Q23 | AP-470 | G1 | média |
| Q24 | AP-307 | G2 (só AP-307) | alta |
| Q25 | AP-433 | U3 (só AP-433) | alta |
| Q26 | AP-348 | U4 (unitário) | alta |
| Q27 | AP-307 | G1 | alta |
| Q28 | AP-441 | G5 | média |
| Q29 | AP-365 | G4 | média |
| Q30 | AP-307 | G1 | alta |
| Q31 | AP-470 | G1 | média |
| Q32 | AP-372 | G3 | média |

A confiança refere-se à pertença da questão ao grupo. Dentro de um mesmo caso, as repetições para corréus ou para o mesmo fato (Q02/Q27, Q05/Q30, Q08/Q24, Q07/Q09, Q18/Q28, Q20/Q32, Q22/Q25, e as seis do AP-470) são idênticas na pergunta e no trecho, e ficam juntas com segurança.

**Grupos que reúnem casos diferentes: G1, G3, G4, G5 e G6 (cinco).** G2 e U1 a U4 ficam restritos a um caso.

## 2. Grupos com dois ou mais casos

### G1. Corrupção passiva (art. 317): qual vínculo entre a vantagem e um ato do cargo o tipo exige (ato de ofício como contrapartida)
- **Pergunta comum:** para configurar a corrupção passiva, basta que a vantagem seja solicitada ou recebida em razão da função, ou é preciso um ato de ofício determinado, apontado como contrapartida?
- **Casos:** AP-307 (1994): Q02/Q27 (episódio Mercedes-Benz) e Q05/Q30 (episódio VASP-Petrobras). AP-470 (2012): Q03, Q10, Q14, Q19, Q23, Q31 (seis réus parlamentares, itens VI.1 a VI.4).
- **Respostas:** AP-307, **não** se enquadra: absolvição porque "em nenhum momento houve sequer referência a ato de ofício [...] que pudesse ser apontado como contrapartida" (p. 152), e porque não foi apontado ato de ofício prometido ou praticado (p. 126). AP-470, **sim**, se enquadra: o dinheiro foi "solicitado e recebido em razão da função, em troca da prática de atos de ofício inseridos nas atribuições dos parlamentares, o que é suficiente" (p. 3686). Os réus foram condenados "por terem recebido dinheiro para votar, e não em decorrência do conteúdo de seus votos" (p. 3686-3687).
- **Por que é a mesma pergunta:** os dois casos discutem o mesmo elemento normativo, a contrapartida funcional da vantagem. AP-307 o formula como tese ("se o tipo exige [...] a predeterminação de ato de ofício"). AP-470 o resolve ao dizer que bastam atos de ofício genéricos dentro das atribuições (votos, apoio à base) e que o conteúdo e a licitude do ato são irrelevantes.
- **Ressalvas (caso-limite):** (a) a pergunta do AP-470, como foi registrada, tem moldura probatória ("se as provas permitem concluir que os recursos foram solicitados em razão da função e em troca de apoio"); o elemento jurídico só aparece no trecho do voto. Por isso a confiança é média. (b) AP-470 **não** abandona a referência ao ato de ofício: ele a mantém e a considera satisfeita por um conjunto indeterminado de votos. Há duas leituras possíveis, e com o que li não consigo escolher: (i) houve mudança de interpretação (de "ato determinado e predeterminado" para "ato genérico das atribuições"); (ii) os fatos são diferentes (em AP-307 nenhum ato foi sequer apontado; em AP-470 havia uma classe de atos identificada). A distinção entre (i) e (ii) é a questão central para a pesquisa e merece leitura própria dos votos. (c) Em AP-307 VASP, a absolvição tem "duplo motivo": falta de ato de ofício (Q05/Q30, que está em G1) e falta de vantagem (Q08/Q24, que está em G2). Só o primeiro motivo é comparável com o AP-470.

### G3. Peculato (art. 312): aplicar a verba numa finalidade pública diferente da contratada configura "desvio em proveito próprio ou alheio"?
- **Pergunta comum:** quando o recurso público continua revertido à própria Administração (outra obra, outro serviço de valor compatível), há desvio para fins do art. 312?
- **Casos:** AP-375 (2004): Q16, Q04. AP-365 (2006): Q11. AP-372 (2010): Q20/Q32.
- **Respostas:** **não** nos três casos. AP-375: o desvio "se verificou [em favor do] próprio ente público [...] Tal conduta não se amolda aos preceitos do art. 312" (p. 6). AP-365: pavimentação realizada, "impossível cogitar-se de crime de peculato" (p. 13). AP-372: serviços executados em compensação, "em valor compatível com o desembolso", e por isso não há apropriação nem desvio (p. 55).
- **Por que é a mesma pergunta:** o elemento discutido nos três é o mesmo, o desvio "em proveito próprio ou alheio" quando o dinheiro continua servindo à Administração.
- **Ressalvas:** (a) AP-375 e AP-365 têm o **mesmo réu** (Jackson Barreto de Lima), em fatos de obras municipais em Sergipe, e AP-365 remete expressamente a AP-375 ("Tal como na Ação Penal n° 375-2/SE", p. 13). São AP diferentes, mas não são julgamentos independentes: a coerência entre eles é quase mecânica. (b) AP-365 Q11 e AP-372 têm moldura de prova ("ausência de prova", "núcleo do tipo não demonstrado"), e por isso a confiança é média. (c) Q04 é o *habeas corpus* de ofício concedido ao corréu Arnaldo Arcanjo da Silva, por "atipicidade [...] tal como aduzido [...] quanto a Jackson Barreto" (p. 7). Pela imputação (312), foi para G3. Mas a atipicidade sustentada pelo Ministério Público abrange o 312 e o 315 (p. 6), de modo que Q04 também caberia em G4. Todas as respostas são iguais: o grupo não mostra instabilidade.

### G4. Emprego irregular de verbas (art. 315): o tipo exige que a destinação da verba esteja fixada em lei?
- **Pergunta comum:** dar à verba aplicação diferente da prevista em contrato ou programação, sem lei que fixe a destinação, configura o art. 315?
- **Casos:** AP-375 (2004): Q12. AP-365 (2006): Q15, Q29.
- **Respostas:** **não** nos dois. AP-375: o crime só se daria "se a destinação fosse prevista em LEI; o que não é o caso" (p. 6). AP-365: "O emprego de numerário em obra diversa configura, quando muito, em face do fato de não haver a destinação em lei, infração administrativa" (p. 13). Q29 estende ao corréu com base na "inexistência de lei a destinar aplicação de verba".
- **Por que é a mesma pergunta:** o elemento é o mesmo e está nomeado nos dois casos: a "aplicação diversa da estabelecida em lei".
- **Ressalvas:** a mesma de G3, item (a): mesmo réu, e o segundo caso segue o primeiro. Nos dois, o 315 aparece como tipificação alternativa, não como imputação da denúncia. Q29 tem confiança média porque a imputação registrada é o 312, embora a ementa citada seja a do 315.

### G5. Decreto-Lei 201/67, art. 1º, II: gastar dinheiro público de forma irregular é "utilizar-se indevidamente, em proveito próprio ou alheio, de bens, rendas ou serviços públicos"?
- **Pergunta comum:** o inciso II alcança o emprego irregular de recursos financeiros do município, ou exige o uso efetivo de um bem ou serviço público?
- **Casos:** AP-441 (2012): Q18/Q28. AP-432 (2013): Q13.
- **Respostas:** AP-441, **não**: "Os fatos narrados na denúncia [...] não se amoldam à efetiva utilização pelos réus de bens, serviços ou rendas públicas" (p. 46). O pagamento de aluguel numa locação vedada é "aplicação irregular de recursos públicos", e os fatos foram reclassificados para o inciso V (p. 47-48). O voto se apoia na doutrina do peculato de uso: com dinheiro, que é fungível, não há mera "utilização". AP-432, **sim**: o prefeito, com publicidade institucional de promoção pessoal paga pelos cofres municipais (cerca de R$ 90 mil, p. 12), "efetivamente utilizou, indevidamente, em proveito próprio, de bens, rendas ou serviços públicos" (p. 14).
- **Por que é a mesma pergunta:** os dois votos discutem o mesmo núcleo ("utilizar-se de [...] rendas ou serviços públicos") diante de um gasto de dinheiro municipal. AP-441 diz que gasto irregular não é "utilização". AP-432 enquadra um gasto irregular no inciso II.
- **Ressalvas (caso-limite forte):** (a) os fatos permitem distinguir: em AP-432 o proveito próprio é direto (promoção pessoal do prefeito) e o objeto usado pode ser lido como o **serviço** de publicidade contratado, não o dinheiro; em AP-441 o beneficiário é um terceiro (servidor ou cônjuge locador) e o objeto é o pagamento em si. (b) Pelo campo de imputação de Q13, o Min. Dias Toffoli, autor do voto citado em AP-441, ficou vencido em AP-432 quanto ao enquadramento (votou pelo inciso I). Isso sugere que a tensão foi percebida dentro do Plenário. Não verifiquei o voto dele em AP-432. (c) A divergência de resposta é real, mas não sei dizer, sem ler os votos, se é de interpretação ou de fato. É o grupo, entre os cinco, com maior potencial de mostrar instabilidade.

### G6. Decreto-Lei 201/67, art. 1º, V: o que é "ordenar ou efetuar despesas não autorizadas por lei, ou realizá-las em desacordo com as normas financeiras"
- **Pergunta comum:** um pagamento feito pelo prefeito sem amparo legal ou contra norma financeira (aluguel em locação legalmente vedada; precatório pago fora da ordem por transação) enquadra-se no inciso V?
- **Casos:** AP-441 (2012): Q07/Q09. AP-503 (2010): Q21, Q01.
- **Respostas:** AP-441, **sim** (reclassificação por *emendatio libelli* para o inciso V, p. 48). AP-503, registrado como **"nao"** em Q21 e Q01, **mas a certidão e a ementa do AP-503 dizem o contrário**: "por votação unânime, julgou procedente a ação penal concernente ao crime tipificado no inciso V do art. 1º do Decreto-lei nº 201/67", com pena de 3 meses de detenção e extinção da punibilidade por prescrição retroativa. O trecho de Q21 ("A materialidade dessa despesa [...] acha-se comprovada") vai na mesma direção. **Parece haver erro de codificação no banco** para Q21. A resposta de Q01 ("nao") pode estar certa na leitura literal (a transação **não** autoriza furar a ordem dos precatórios), o que mostra de novo a ambiguidade do campo. A prescrição não muda a resposta à questão de tipicidade.
- **Por que é a mesma pergunta:** os dois casos aplicam o mesmo elemento normativo, o da despesa sem autorização legal ou em desacordo com as normas financeiras, a pagamentos ordenados pelo prefeito. Corrigido o AP-503, as respostas coincidem (sim/sim).
- **Ressalvas:** (a) os fatos são bem diferentes (locação vedada × ordem cronológica de precatórios), e o grupo reúne casos pela norma mais do que por uma tese controvertida. Por isso a confiança é média. (b) Q01 trata de uma subquestão específica (se a transação vantajosa ao erário autoriza a quebra da ordem dos precatórios) que não tem par no AP-441. Pus Q01 em G6 por ser o mesmo fato e o mesmo inciso de Q21, com confiança baixa. Também se sustentaria como unitário. (c) Curiosidade sem efeito no agrupamento: o voto do AP-441 (p. 47) cita a "quitação de débito constante de precatório judiciário fora de sua ordem cronológica" como exemplo doutrinário do **inciso III**, não do V.

## 3. Questões sem par em outro caso

- **Q06** (AP-503, DL 201 art. 1º, IV): aplicar empréstimo do BID em desacordo com o plano a que se vinculava é típico. Resposta: sim (por maioria, vencido o Revisor, conforme a certidão).
- **Q17** (AP-503, DL 201 art. 1º, XIV): "descumprir ordem judicial" exige decisão de conteúdo jurisdicional, e o Presidente do Tribunal, ao processar precatórios, atua como autoridade administrativa. Resposta: não.
- **Q08/Q24** (AP-307, art. 317, VASP): falta qualquer referência a vantagem solicitada, recebida ou prometida. É um elemento diferente do de G1, e mais próximo da prova. Resposta: não.
- **Q22/Q25** (AP-433, Lei 8.666 art. 92, *caput* e parágrafo único): o fato imputado estava fora do âmbito de execução do contrato, e por isso não há o tipo. Resposta: não.
- **Q26** (AP-348, Lei 8.666 art. 89): o crime de dispensa indevida pressupõe o ilícito administrativo antecedente, que não existiu no caso. Resposta: não.

## 4. Dúvidas: agrupamentos considerados e rejeitados

1. **Q06 (AP-503, inciso IV) com G4 (art. 315).** As duas normas falam em aplicar recursos em destino diferente do previsto. Rejeitei porque o elemento normativo é outro: o inciso IV fala em "planos ou programas", e o art. 315 exige destinação "estabelecida em lei". As respostas opostas (sim × não) se explicam pelo texto das normas, não por instabilidade. Fica registrado como o par mais parecido entre os rejeitados.
2. **Fundir G3 e G4.** AP-375 e AP-365 tratam os dois tipos juntos, no mesmo raciocínio de atipicidade. Mantive separados porque os elementos diferem (desvio em proveito próprio ou alheio × destinação legal). Isso afeta só a contagem, não a conclusão: ambos são estáveis.
3. **Q26 (AP-348, art. 89: o crime pressupõe ilícito administrativo) com Q15 (AP-365: "quando muito, infração administrativa").** Os dois falam da relação entre ilícito administrativo e penal, mas em sentidos diferentes e sobre tipos diferentes. Rejeitei.
4. **Q08/Q24 (existência de vantagem) com G1.** O AP-470 discute o nexo da vantagem com a função, não a existência dela. Rejeitei.
5. **Separar, dentro de G1, AP-307 Mercedes (tese: o tipo exige ato predeterminado?) de AP-307 VASP (fato: nenhum ato foi apontado).** Mantive juntos porque o elemento é o mesmo. Quem quiser só a forma de tese pura pode restringir a comparação a Q02/Q27 × AP-470.
6. **G6 por inteiro.** Hesitei entre G6 e quatro unitários. Fiquei com G6 porque a norma e o elemento coincidem, mas o grupo não carrega uma tese controvertida, e sua utilidade para medir instabilidade é baixa.
7. **Possível erro no banco (fora do escopo do agrupamento, mas relevante):** Q21, e talvez Q01, do AP-503 trazem "nao", enquanto a certidão registra procedência unânime no inciso V. Convém conferir o campo antes de qualquer comparação de respostas.
