# Taxa de acerto da extração por leitura contra o gabarito manual — 19/09/2026

> Gerado por `metodologia/validacao_gabarito.py`. Portão do `PLANO_EXTRACAO.md` §3-L2, medido depois da análise descritiva (desvio declarado, D-028 §6.1). Modelo dos extratores: `claude-sonnet-5` (REGISTRO_EXECUCAO §2). Comparação e relatório: `claude-fable-5-1`.

**Cobertura:** 9 casos, 21 réus, 80 comparações campo a campo com valor firme no gabarito. Fora: AP-441 (sem valor firme, gabarito §7), AP-462 (não está no universo de 24), AP-470 (sem gabarito).

**O que se compara:** o valor produzido pelo extrator (antes de qualquer decisão do pesquisador — D-029 a D-031 não entram) contra o gabarito em duas versões. A versão **original** (08/08) é a única comparação cega. A versão **corrigida** (09/08) incorpora duas correções feitas lendo a ata *depois* de a extração divergir do gabarito — mede o acerto contra a fonte primária, mas não é cega.

## Acerto por campo

| Campo | Comparações | Acerto vs gabarito original (cego) | Acerto vs gabarito corrigido (fonte primária) |
|---|---|---|---|
| `resultado` | 19 | 13/19 (68%) | 19/19 (100%) |
| `n_votantes` | 9 | 7/9 (78%) | 9/9 (100%) |
| `votos_condenacao` | 15 | 5/15 (33%) | 14/15 (93%) |
| `votos_absolvicao` | 15 | 6/15 (40%) | 15/15 (100%) |
| `unanime` | 15 | 10/15 (67%) | 15/15 (100%) |
| `categoria_placar` | 2 | 1/2 (50%) | 1/2 (50%) |
| `vencidos` | 4 | 4/4 (100%) | 4/4 (100%) |
| `motivo_ausencia_alexandre` | 1 | 1/1 (100%) | 1/1 (100%) |
| **Total** | **80** | **47/80 (59%)** | **78/80 (98%)** |

## Divergências, uma a uma

| Réu | Campo | Extraído | Gabarito original | Gabarito corrigido | = orig. | = corr. |
|---|---|---|---|---|---|---|
| AP-409-R01 | votos_condenacao | 5 | 7 | 7 | ✘ | ✘ |
| AP-409-R01 | categoria_placar | Apertado | Folgado | Folgado | ✘ | ✘ |
| AP-372-R01 | n_votantes | 9 | 10 | 9 | ✘ | ✔ |
| AP-372-R02 | n_votantes | 9 | 10 | 9 | ✘ | ✔ |
| AP-565-R01 | votos_condenacao | 10 | 9 | 10 | ✘ | ✔ |
| AP-565-R01 | votos_absolvicao | 0 | 2 | 0 | ✘ | ✔ |
| AP-565-R01 | unanime | Sim | Não | Sim | ✘ | ✔ |
| AP-565-R02 | votos_condenacao | 10 | 9 | 10 | ✘ | ✔ |
| AP-565-R02 | votos_absolvicao | 0 | 2 | 0 | ✘ | ✔ |
| AP-565-R02 | unanime | Sim | Não | Sim | ✘ | ✔ |
| AP-565-R03 | votos_condenacao | 10 | 9 | 10 | ✘ | ✔ |
| AP-565-R03 | votos_absolvicao | 0 | 2 | 0 | ✘ | ✔ |
| AP-565-R03 | unanime | Sim | Não | Sim | ✘ | ✔ |
| AP-565-R04 | resultado | Absolvição | Condenação parcial | Absolvição | ✘ | ✔ |
| AP-565-R04 | votos_condenacao | 5 | 9 | 5 | ✘ | ✔ |
| AP-565-R04 | votos_absolvicao | 5 | 2 | 5 | ✘ | ✔ |
| AP-565-R05 | resultado | Absolvição | Condenação parcial | Absolvição | ✘ | ✔ |
| AP-565-R05 | votos_condenacao | 5 | 9 | 5 | ✘ | ✔ |
| AP-565-R05 | votos_absolvicao | 5 | 2 | 5 | ✘ | ✔ |
| AP-565-R06 | resultado | Absolvição | Condenação parcial | Absolvição | ✘ | ✔ |
| AP-565-R06 | votos_condenacao | 5 | 9 | 5 | ✘ | ✔ |
| AP-565-R06 | votos_absolvicao | 5 | 2 | 5 | ✘ | ✔ |
| AP-565-R08 | resultado | Absolvição | Condenação parcial | Absolvição | ✘ | ✔ |
| AP-565-R08 | votos_condenacao | 5 | 9 | 5 | ✘ | ✔ |
| AP-565-R08 | votos_absolvicao | 5 | 2 | 5 | ✘ | ✔ |
| AP-565-R07 | resultado | Absolvição | Condenação parcial | Absolvição | ✘ | ✔ |
| AP-565-R07 | votos_condenacao | 0 | 9 | 0 | ✘ | ✔ |
| AP-565-R07 | votos_absolvicao | 10 | 2 | 10 | ✘ | ✔ |
| AP-565-R07 | unanime | Sim | Não | Sim | ✘ | ✔ |
| AP-565-R09 | resultado | Absolvição | Condenação parcial | Absolvição | ✘ | ✔ |
| AP-565-R09 | votos_condenacao | 0 | 9 | 0 | ✘ | ✔ |
| AP-565-R09 | votos_absolvicao | 10 | 2 | 10 | ✘ | ✔ |
| AP-565-R09 | unanime | Sim | Não | Sim | ✘ | ✔ |

## Leitura

1. **Contra a fonte primária (gabarito corrigido), a única divergência é `votos_condenacao` da AP-409** — e ela não é erro de leitura: a ata registra duas contagens (Cármen Lúcia: 5; Peluso, ao proclamar: 7). O extrator seguiu a primeira; o gabarito, a segunda. A escolha foi tomada pelo pesquisador em D-030 (7x3). `categoria_placar` da AP-409 herda a mesma divergência (0,50 → Apertado com 5; 0,70 → Folgado com 7).
2. **Todas as demais divergências contra o gabarito original são casos em que a extração estava certa e o gabarito errado**, conferido na ata: `n_votantes` da AP-372 (o gabarito presumia Corte de 11 numa data de vacância) e o quadro inteiro da AP-565 (o gabarito colapsava nove resultados num único 9x2). São os dois erros de gabarito que o `ESTADO.md` pedia para corrigir (G-M14, G-M15) — corrigidos aqui por registro, não por edição do arquivo original, que preserva o histórico.
3. **Padrões de erro do método antigo (gabarito §4):** nenhum reincidiu. (a) falso positivo de prescrição: 0 em AP-409, AP-432, AP-565; (b) votantes fixados em 11: 0 em AP-372, AP-409, AP-447 (e a extração detectou a vacância que o gabarito não detectou); (e) tokens de preliminar como vencidos: 0 na AP-447; (g) sessão errada em ata multissessão: 0 na AP-433; (h) verbo fora do vocabulário: 0 em AP-348, AP-365, AP-1036.
4. **O que esta medida não diz.** O gabarito cobre os casos-armadilha conhecidos, não uma amostra aleatória (gabarito §6); e os extratores, embora não vissem os valores, sabiam pelo prompt que existiam armadilhas (REGISTRO §4.2). A taxa mede a capacidade de não cair nas armadilhas catalogadas; não é estimativa da taxa de erro do banco inteiro. A complementação por amostra aleatória proposta no gabarito §6 não foi feita.
