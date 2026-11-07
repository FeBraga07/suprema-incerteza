# Piloto da Fase 4: AP-426, agente × leitura do Felipe (12/10/2026)

> Agente `general-purpose`, modelo `claude-opus-5-5` (conferido na transcrição: 9 de 9 mensagens), prompt literal em `PROMPT_AP-426.md`, saída `AP-426.json`. Leitura cega: o agente leu só o acórdão (pp. 1–7). Leitura humana: `anotacoes_codebook/AP-426.md` e `entrevista_AP-426.md`. Comparação feita pela sessão `c81eab04`.

| Ponto | Felipe | Agente | Bate? |
|---|---|---|---|
| Perguntas, fato 1 (art. 89) | dolo + influência no ato (= concorreu) | concorreu + dolo | ✅ as mesmas duas |
| Perguntas, fato 2 (DL 201, III) | dolo + concorreu | dolo + concorreu | ✅ |
| Resposta do tribunal | não, não (nos dois fatos) | não, não (nos dois fatos) | ✅ |
| **Principal, fato 1** | dolo | **concorreu** (confiança média) | ❌ |
| Principal, fato 2 | dolo | dolo (confiança baixa) | ✅ |
| **Voto condutor** | relator (Marco Aurélio), que adota o parecer do PGR | **Ellen Gracie** (o acórdão diz "nos termos do voto da revisora") | ❌ |
| Precedente | nenhum | nenhum | ✅ |
| Votos (11 Absolve) | — | 11 Absolve, sem divergência com o banco | ✅ |

## Diagnóstico das duas divergências

1. **Principal no fato 1: lacuna do codebook.** O próprio agente avisa: o voto diz "concorrido dolosamente", os dois aparecem juntos, e a R5 não desempata em caso unânime (os votos não se separaram em lugar nenhum). A decisão é do Felipe: regra de desempate.
2. **Voto condutor: lacuna do prompt, não do codebook.** O rascunho do contrato já dizia "registrar o que o texto indica" (o relator), mas o prompt não definiu `voto_condutor`. Correção de forma no prompt.

## Outros avisos do agente (para o gate, não decidem agora)

- Gilmar Mendes presidiu a sessão e o texto não mostra se votou; o banco o conta entre os 11.
- Escopo Levcovitz marcado "Sim" com confiança baixa: a leitura cega não tem o Quadro 1.1. Correção de forma: o prompt passa a informar o escopo de cada unidade.
- Art. 386, IV num julgamento de 18/12/2008 com linguagem do inciso antigo: o agente aplicou a R2 corretamente.
