# Complemento do censo: ações penais do Plenário catalogadas como Turma (18/10/2026)

Sessão `a7d56ad4`, `claude-opus-5-5`, pelo navegador (o endpoint não aceita acesso programático; ver `CLAUDE.md` §4). Resultado bruto em `dados/brutos/censo_complemento_ap_turmas_2026-10-18.psv`.

## Por que foi feito

A consolidação da Fase 4 (D-050) encontrou a AP 307 citada nos votos da AP-1025 como "AP 307, Rel.: Min. ILMAR GALVÃO, Plenário, j. 13.12.1994", mas o censo de 08/08 não tem nenhuma ação penal pura do Plenário em 1994.

## O que se achou

1. **A AP 307 está no índice com o órgão julgador errado.** O registro do julgamento de mérito (`sjur157761`, 13/12/1994) traz `orgao_julgador = "Segunda Turma"`, mas a ata registra todas as sessões no Plenário ("Plenário, 07.12.94"; "O Tribunal acolheu a preliminar da defesa..."). O filtro do censo (`orgao_julgador.keyword = "Tribunal Pleno"`) a excluiu. Ementa: corrupção passiva (art. 317, caput), corrupção ativa de testemunha, coação no curso do processo, supressão de documento e falsidade ideológica; réus, entre outros, Fernando Affonso Collor de Mello e Paulo César Cavalcante Farias. **Está no recorte**: ação penal, Plenário, 1991–2024, crime do Quadro 1.1 de Levcovitz (art. 317), mérito julgado.
2. **Varredura do mesmo modo de falha.** Todas as 85 ações penais puras de 1991–2024 catalogadas como Turma (52 Primeira, 33 Segunda) foram triadas pela sequência de sessões que fecham a ata. Só duas têm **todas** as sessões no Plenário: a AP 307 e a **AP 351** (12/08/2004, Rel. Marco Aurélio, catalogada como Primeira Turma). A AP 351 é crime contra o sistema financeiro (Lei 7.492/1986) e falsidade ideológica, fora do Quadro 1.1: **fora do recorte**. As demais com "Plenário" na ata (AP 404, 497, 559, 595, 619, 678, todas de 2014) começaram no Plenário e foram concluídas na Turma, depois da Emenda Regimental nº 49/2014: estão corretamente fora.
3. **Outros modos de falha testados, sem achado:** ação penal sem data de julgamento (0); título "AP ..." no Plenário com classe diferente de AP (1, falso positivo: Ext 783).

## Consequência

O universo de 24 casos tem **uma omissão: a AP 307**. A decisão sobre incluí-la é do Felipe (ver `ESTADO.md`).
