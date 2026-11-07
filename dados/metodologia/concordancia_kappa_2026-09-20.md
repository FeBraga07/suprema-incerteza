# Concordância entre extrações independentes, corrigida por chance

> Gerado por `concordancia_kappa.py` em 20/09/2026, sessão `d7aca838`, modelo `claude-opus-5`.
> Entrada: os 30 arquivos de dupla extração em `derivados/casos/_dupla/` (15 casos). **Nenhum dado novo foi coletado**: é recálculo sobre o material de 08–09/08/2026.


**Unidades comparadas:** 801 pares campo a campo, em 15 casos (AP-1025, AP-1032, AP-348, AP-365, AP-375, AP-396, AP-416, AP-426, AP-430, AP-465, AP-503, AP-508, AP-527, AP-940, AP-973).

**Concordância bruta global: 99.3%**.


## Por campo

| Campo | Pares | Concordância bruta | κ de Cohen | IC95% de κ (bootstrap) | α de Krippendorff | Categorias | Prevalência da categoria modal |
|---|---:|---:|---:|:--:|---:|---:|---:|
| `voto.ausente` | 154 | 99.4% | 0,974 | [0,91; 1,00] | 0,974 | 2 | 85% (`Nao`) |
| `voto.eh_relator` | 154 | 100.0% | 1,000 | [1,00; 1,00] | 1,000 | 2 | 91% (`Nao`) |
| `voto.vencido` | 154 | 100.0% | 1,000 | [1,00; 1,00] | 1,000 | 2 | 93% (`Nao`) |
| `voto.voto_resultado` | 154 | 100.0% | 1,000 | [1,00; 1,00] | 1,000 | 3 | 66% (`ABSOLVE`) |
| `reu.motivo` | 20 | 80.0% | 0,690 | [0,39; 0,92] | 0,690 | 4 | 50% (`MERITO`) |
| `reu.n_votantes` | 20 | 100.0% | n/a (contagem) | — | n/a (contagem) | 5 | 25% (`11`) |
| `reu.prescricao_pos_condenacao` | 20 | 100.0% | 1,000 | [1,00; 1,00] | 1,000 | 2 | 95% (`Nao`) |
| `reu.resultado` | 20 | 95.0% | 0,895 | [0,65; 1,00] | 0,898 | 4 | 70% (`ABSOLVICAO`) |
| `reu.unanime` | 20 | 100.0% | 1,000 | [1,00; 1,00] | 1,000 | 2 | 70% (`Sim`) |
| `reu.votos_absolvicao` | 20 | 100.0% | n/a (contagem) | — | n/a (contagem) | 9 | 25% (`11`) |
| `reu.votos_condenacao` | 20 | 100.0% | n/a (contagem) | — | n/a (contagem) | 3 | 75% (`0`) |
| `caso.merito_finalizado` | 15 | 100.0% | **indefinido** | — | — | 1 | 100% (`Sim`) |
| `caso.multiplas_sessoes` | 15 | 100.0% | 1,000 | [1,00; 1,00] | 1,000 | 2 | 87% (`Nao`) |
| `caso.n_reus` | 15 | 100.0% | n/a (contagem) | — | n/a (contagem) | 3 | 73% (`1`) |

IC95% por reamostragem das unidades (5.000 repetições, semente fixa 20260920). Onde o kappa é indefinido em boa parte das reamostras — o que ocorre quando a categoria modal domina —, o intervalo não é reportado.


Campos de contagem (`n_reus`, `n_votantes`, `votos_condenacao`, `votos_absolvicao`) são numéricos: kappa e alfa nominais não se aplicam a eles, e o que se reporta é coincidência exata.


**Descartes:** `voto.__sem_par__`: 9.
