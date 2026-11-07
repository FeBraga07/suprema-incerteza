# AP-470: notas do índice de peças (27/09/2026, modelo claude-opus-5-5)

**Escopo:** índice de peças, não mapa por réu e voto (adaptação do PROMPT_MAPA para a AP-470). O arquivo `AP-470.psv` tem **866 linhas**: 843 peças do acórdão, mais 1 linha porque ementa e acórdão foram separados, mais 20 linhas porque os votos únicos de Rosa Weber (p.1060-1478) e de Cármen Lúcia (p.1784-2147) foram divididos em 13 e 9 segmentos de capítulo, mais 2 linhas de ata criadas por regra. Por tipo de peça: voto 369, aparte 173, debate 94, outro 79, extrato_ata 54, questao_ordem 45, voto_aditamento 45, confirmacao_voto 4, e uma linha cada para ementa, acórdão e relatório.

**Como foi lido (d):** por navegação, sem leitura linear.
1. **Limites das peças.** Cada peça tem um número próprio de autenticação no rodapé ("sob o número N"), e a troca desse número marca o limite de peça em 100% das páginas. Com isso saíram 843 blocos, e o cabeçalho corrente de cada página deu o tipo.
2. **Cabeçalhos usados:** Voto s/ item II…VIII, Voto s/ Preliminar, Voto s/ Questão de Ordem, Voto s/ Proposta, Voto s/ Dosimetria, Voto s/ Continuidade Delitiva, Voto s/ Perda de Mandato, Voto - MIN. X, Aditamento ao Voto, Antecipação ao Voto, Retificação de Voto, Confirmação de Voto, Notas/Incidências ao Voto, Debate, Esclarecimento, Explicação, Comunicação, Questão de Ordem, Proposta e Decisão de Julgamento (= extrato de ata).
3. **Autor.** É o primeiro "O SENHOR MINISTRO / A SENHORA MINISTRA X" da peça. Em debates, apartes e questões de ordem vêm todos os que falam, em ordem.
4. **Conferência.** Li as primeiras e as últimas linhas das peças de voto. Nos votos grandes de mérito, localizei os títulos internos (III.1/III.2/III.3; VI.1-VI.4; capítulos C.x e I-XII dos votos únicos).
5. **Leitura direta, só para presença.** Li as listas de presentes das atas de 29.08, 03.09, 19.09 e 09.10.2012, e na ata final (p.8380-8383) os parágrafos das sessões de 01.10 a 10.10.2012.

Placar e resultado não foram extraídos. As colunas do banco foram copiadas de `3_votos.psv`.

**Convenções.**
- `reus_abrangidos` usa o item da denúncia. No item VI, a divisão entre passiva e ativa segue a sessão:
  - 1ª rodada (17/09 a 01/10): corrupção passiva, réus R14 a R23.
  - 2ª rodada (03/10 a 10/10): corrupção ativa, réus R04 a R13.
  - Item III: réus R01 a R06.
- `ctx:` indica o item julgado na sessão ou nas peças vizinhas. É inferência de posição.
- `(?)` indica alcance herdado do voto adjacente.
- Nas peças de mérito dos itens III e VI, as três colunas do banco valem `varia`, e `obs` traz a contagem do banco. Todas as 418 linhas do banco têm `fonte_voto=lido`.
- Itens II, IV, V, VII e VIII, preliminares, questão de ordem e toda a fase pós-mérito (a partir de 23/10) ficam `NA`: não há linha no banco.
- `tem_texto=Adesao` (192 linhas) é **heurística**: peça com menos de 1.500 caracteres que contém "acompanh". Precisa ser confirmada na leitura.

**(a) OCR.**
- **p.342-346** é imagem sem camada de texto (tanto o .txt quanto o `pdftotext` saem vazios). Pelo PDF, é um Esclarecimento de Cezar Peluso de 10/08/2012.
- O cabeçalho de página "Tipo Texto 298" (p.8361-8364) é anômalo.
- Nenhuma outra página vazia fora das capas de autuação.

**(b) Peças anunciadas ou esperadas que não aparecem.**
- **Luiz Fux, item VI (corrupção ativa):** não há peça própria de mérito. A única peça dele no bloco é o aditamento da p.4974-4976, com a fala marcada CANCELADO. O voto consta só na ata (p.4996; ata final p.8382). Foi criada linha `extrato_ata` com `tem_texto=Nao`.
- **Falas canceladas:** 68 linhas têm fala do autor marcada "CANCELADO" (Celso de Mello 35, Fux 33). Em várias delas, o que resta são falas de outros ministros.

**(c) DIVERGE.**
- **Cezar Peluso × item VI:** o banco registra 20 votos dele (Condena 18, Absolve 2). No acórdão, não há peça de autoria dele depois da p.2291. Ele não está na lista de presentes a partir da ata de 03.09.2012 (p.2675) nem nas sessões do item VI (p.3715, p.4996), e a ata final do item VI (p.8380-8383) não o nomeia.
- Foi criada linha `extrato_ata` com `DIVERGE:` na p.2675. O banco não foi corrigido. O próprio JSON do caso já marcava confiança só MEDIA na composição (`n_votantes=11`).

**O que ficou de fora.**
- A localização, dentro de cada voto, das páginas de cada réu × fato. Só os votos de Barbosa (item III), Rosa, Cármen e Fux (item II) receberam subdivisão.
- A confirmação de `Adesao`.
- As falas de cada ministro dentro dos debates. A lista de quem fala é a ordem de entrada.
- A fase pós-mérito (2.114 pp.): foi indexada, mas não conferida réu a réu.

**Proposta para o mapa completo (réu × fato × ministro).** O banco só cobre os itens III e VI, que somam ~5,1 M de caracteres em 35 peças de mérito mais aditamentos. Passo 0, barato e automático: usar os títulos internos de cada voto ("RÉU: X", "Nº acusado", VI.1-VI.4), que já aparecem na maioria dos votos, para pré-localizar as páginas de cada réu. Depois, **12 passadas** de ~300 a 450 mil caracteres, cada uma sobre um conjunto fechado de peças:
- **Item III, 4 passadas:**
  - Barbosa + Lewandowski
  - Fux + Toffoli
  - Peluso (antecipação + voto) + Gilmar
  - Rosa C.2 + Cármen II-IV + Marco Aurélio + Celso + Ayres (com incidências)
- **Item VI passiva, 5 passadas:**
  - Barbosa (p.3476-3703)
  - Lewandowski (p.3728-3920) + aditamentos
  - Toffoli (p.4158-4355)
  - Fux + Gilmar
  - Rosa C.6 + Cármen VII + Marco Aurélio + Celso + Ayres (p.4499-4590)
- **Item VI ativa, 3 passadas:**
  - Barbosa + Lewandowski (2 peças)
  - Toffoli + Gilmar + Marco Aurélio
  - Celso + Ayres (aditamento) + Rosa C.7 + Cármen VIII e aditamento
- **Passada de fechamento:** debates, apartes e retificações em `ctx: item III/VI`, mais os `DIVERGE`.

Os itens II, IV, V, VII e VIII e a dosimetria só entram se o escopo do banco for ampliado, por decisão registrada.
