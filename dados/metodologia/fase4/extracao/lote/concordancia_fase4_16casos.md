# Concordância A × B — Fase 4

Unidades e questões em comum: 169 · sem par, nos casos com dupla leitura: só em A 8, só em B 5

| Campo | Pares | Concordância bruta | κ | IC95% |
|---|---:|---:|---:|:--:|
| `posicao.enfrentou_a_questao` | 1012 | 92.5% | 0,878 | [0,85; 0,90] |
| `posicao.posicao` | 1012 | 95.8% | 0,928 | [0,91; 0,95] |
| `posicao.voto_resultado` | 1012 | 98.8% | 0,975 | [0,96; 0,99] |
| `unidade.modo_concurso` | 106 | 97.2% | 0,942 | [0,87; 1,00] |
| `unidade.padrao_dolo_exigido` | 106 | 100.0% | 1,000 | [1,00; 1,00] |
| `unidade.principal` | 106 | 96.2% | 0,901 | [0,79; 0,98] |
| `unidade.resposta_tribunal` | 106 | 100.0% | 1,000 | [1,00; 1,00] |
| `unidade.escopo_levcovitz` | 63 | 100.0% | 1,000 | [1,00; 1,00] |
| `unidade.questoes_conjunto` | 63 | 88.9% | 0,866 | [0,76; 0,96] |
| `unidade.questoes_principais` | 63 | 90.5% | 0,880 | [0,78; 0,96] |
| `unidade.voto_condutor` | 63 | 90.5% | 0,882 | [0,79; 0,96] |

**Direção das perguntas `outra`.** A tabela acima usa a direção alinhada (D-046, item 2). Como lida, sem inverter:

| Campo | Concordância bruta | κ |
|---|---:|---:|
| `posicao.posicao` | 95.3% | 0,919 |
| `unidade.resposta_tribunal` | 99.1% | 0,976 |

**Precedentes:** Jaccard médio por unidade = 0,758 (169 unidades).


## Divergências (para o gate)

| Unidade | Ministro | Campo | A | B |
|---|---|---|---|---|
| AP-1025-R01-I01 |  | `questoes_principais` | CONCORREU+CONCORREU | CONCORREU |
| AP-1025-R01-I01 |  | `voto_condutor` | EDSON FACHIN | ALEXANDRE DE MORAES |
| AP-1025-R01-I01::concorreu#2 |  | `modo_concurso` | NAO_DITO | AUTOR |
| AP-1025-R01-I01::concorreu#2 |  | `principal` | SIM | NAO |
| AP-1025-R01-I02 |  | `questoes_conjunto` | OUTRA+OUTRA | OUTRA |
| AP-1025-R01-I02 |  | `voto_condutor` | EDSON FACHIN | ALEXANDRE DE MORAES |
| AP-1025-R01-I02::outra@A0 | DIAS TOFFOLI | `enfrentou_a_questao` | SIM | ADESAO |
| AP-1025-R01-I02::outra@A0 | ROBERTO BARROSO | `enfrentou_a_questao` | SIM | ADESAO |
| AP-1025-R01-I03::outra@A0 | CARMEN LUCIA | `enfrentou_a_questao` | SIM | ADESAO |
| AP-1025-R01-I03::outra@A0 | ROBERTO BARROSO | `enfrentou_a_questao` | SIM | ADESAO |
| AP-1025-R01-I03::outra@A1 | ROBERTO BARROSO | `enfrentou_a_questao` | SIM | ADESAO |
| AP-1025-R02-I01 |  | `questoes_principais` | CONCORREU+CONCORREU | CONCORREU |
| AP-1025-R02-I01 |  | `voto_condutor` | EDSON FACHIN | ALEXANDRE DE MORAES |
| AP-1025-R02-I01::concorreu#2 |  | `modo_concurso` | NAO_DITO | PARTICIPE |
| AP-1025-R02-I01::concorreu#2 |  | `principal` | SIM | NAO |
| AP-1025-R02-I02 |  | `voto_condutor` | EDSON FACHIN | ALEXANDRE DE MORAES |
| AP-1025-R02-I02::concorreu |  | `modo_concurso` | NAO_DITO | PARTICIPE |
| AP-1025-R02-I02::concorreu | ALEXANDRE DE MORAES | `enfrentou_a_questao` | NAO | ADESAO |
| AP-1025-R02-I02::concorreu | ALEXANDRE DE MORAES | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R02-I02::concorreu | ANDRE MENDONCA | `enfrentou_a_questao` | NAO | ADESAO |
| AP-1025-R02-I02::concorreu | ANDRE MENDONCA | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R02-I02::concorreu | CARMEN LUCIA | `enfrentou_a_questao` | NAO | ADESAO |
| AP-1025-R02-I02::concorreu | CARMEN LUCIA | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R02-I02::concorreu | DIAS TOFFOLI | `enfrentou_a_questao` | NAO | ADESAO |
| AP-1025-R02-I02::concorreu | DIAS TOFFOLI | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R02-I02::concorreu | EDSON FACHIN | `enfrentou_a_questao` | NAO | SIM |
| AP-1025-R02-I02::concorreu | EDSON FACHIN | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R02-I02::concorreu | LUIZ FUX | `enfrentou_a_questao` | NAO | ADESAO |
| AP-1025-R02-I02::concorreu | LUIZ FUX | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R02-I02::concorreu | ROBERTO BARROSO | `enfrentou_a_questao` | NAO | ADESAO |
| AP-1025-R02-I02::concorreu | ROBERTO BARROSO | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R02-I02::outra@A0 | ANDRE MENDONCA | `enfrentou_a_questao` | SIM | ADESAO |
| AP-1025-R02-I02::outra@A0 | ROSA WEBER | `enfrentou_a_questao` | NAO | SIM |
| AP-1025-R02-I02::outra@A0 | ROSA WEBER | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R02-I03::outra@A0 | CARMEN LUCIA | `enfrentou_a_questao` | SIM | ADESAO |
| AP-1025-R02-I03::outra@A0 | ROBERTO BARROSO | `enfrentou_a_questao` | SIM | ADESAO |
| AP-1025-R02-I03::outra@A1 | ROBERTO BARROSO | `enfrentou_a_questao` | SIM | ADESAO |
| AP-1025-R03-I01 |  | `questoes_conjunto` | CONCORREU+CONCORREU+DOLO | CONCORREU+DOLO |
| AP-1025-R03-I01 |  | `questoes_principais` | CONCORREU+CONCORREU+DOLO | CONCORREU+DOLO |
| AP-1025-R03-I01 |  | `voto_condutor` | EDSON FACHIN | ALEXANDRE DE MORAES |
| AP-1025-R03-I01::concorreu | CARMEN LUCIA | `enfrentou_a_questao` | NAO | ADESAO |
| AP-1025-R03-I01::concorreu | CARMEN LUCIA | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R03-I01::concorreu | DIAS TOFFOLI | `enfrentou_a_questao` | NAO | ADESAO |
| AP-1025-R03-I01::concorreu | DIAS TOFFOLI | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R03-I01::concorreu | EDSON FACHIN | `enfrentou_a_questao` | NAO | SIM |
| AP-1025-R03-I01::concorreu | EDSON FACHIN | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R03-I01::concorreu | LUIZ FUX | `enfrentou_a_questao` | NAO | ADESAO |
| AP-1025-R03-I01::concorreu | LUIZ FUX | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R03-I01::concorreu | NUNES MARQUES | `enfrentou_a_questao` | NAO | SIM |
| AP-1025-R03-I01::concorreu | NUNES MARQUES | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R03-I01::concorreu | ROBERTO BARROSO | `enfrentou_a_questao` | NAO | ADESAO |
| AP-1025-R03-I01::concorreu | ROBERTO BARROSO | `posicao` | NAO_ENFRENTOU | NAO |
| AP-1025-R03-I02 |  | `voto_condutor` | EDSON FACHIN | ALEXANDRE DE MORAES |
| AP-1025-R03-I02::outra@A0 | DIAS TOFFOLI | `enfrentou_a_questao` | SIM | ADESAO |
| AP-1025-R03-I02::outra@A0 | ROBERTO BARROSO | `enfrentou_a_questao` | SIM | ADESAO |
| AP-1025-R03-I03::outra@A0 | CARMEN LUCIA | `enfrentou_a_questao` | SIM | ADESAO |
| AP-1025-R03-I03::outra@A0 | ROBERTO BARROSO | `enfrentou_a_questao` | SIM | ADESAO |
| AP-1025-R03-I03::outra@A1 | ROBERTO BARROSO | `enfrentou_a_questao` | SIM | ADESAO |
| AP-375-R02-I01::outra@A0 | CARLOS VELLOSO | `voto_resultado` | HC DE OFICIO / TRANCAMENTO POR FALTA DE JUSTA CAUSA (NEM CONDENA NEM ABSOLVE) | CONCEDE HABEAS CORPUS DE OFICIO E TRANCA A ACAO PENAL (NAO ABSOLVE) |
| AP-375-R02-I01::outra@A0 | CEZAR PELUSO | `voto_resultado` | HC DE OFICIO / TRANCAMENTO POR FALTA DE JUSTA CAUSA (NEM CONDENA NEM ABSOLVE) | CONCEDE HABEAS CORPUS DE OFICIO E TRANCA A ACAO PENAL (NAO ABSOLVE) |
| AP-375-R02-I01::outra@A0 | ELLEN GRACIE | `voto_resultado` | HC DE OFICIO / TRANCAMENTO POR FALTA DE JUSTA CAUSA (NEM CONDENA NEM ABSOLVE) | CONCEDE HABEAS CORPUS DE OFICIO E TRANCA A ACAO PENAL (NAO ABSOLVE) |
| AP-375-R02-I01::outra@A0 | GILMAR MENDES | `voto_resultado` | HC DE OFICIO / TRANCAMENTO POR FALTA DE JUSTA CAUSA (NEM CONDENA NEM ABSOLVE) | CONCEDE HABEAS CORPUS DE OFICIO E TRANCA A ACAO PENAL (NAO ABSOLVE) |
| AP-375-R02-I01::outra@A0 | JOAQUIM BARBOSA | `voto_resultado` | HC DE OFICIO / TRANCAMENTO POR FALTA DE JUSTA CAUSA (NEM CONDENA NEM ABSOLVE) | CONCEDE HABEAS CORPUS DE OFICIO E TRANCA A ACAO PENAL (NAO ABSOLVE) |
| AP-375-R02-I01::outra@A0 | MARCO AURELIO | `voto_resultado` | HC DE OFICIO / TRANCAMENTO POR FALTA DE JUSTA CAUSA (NEM CONDENA NEM ABSOLVE) | CONCEDE HABEAS CORPUS DE OFICIO E TRANCA A ACAO PENAL (NAO ABSOLVE) |
| AP-375-R02-I01::outra@A0 | NELSON JOBIM | `voto_resultado` | HC DE OFICIO / TRANCAMENTO POR FALTA DE JUSTA CAUSA (NEM CONDENA NEM ABSOLVE) | CONCEDE HABEAS CORPUS DE OFICIO E TRANCA A ACAO PENAL (NAO ABSOLVE) |
| AP-375-R02-I01::outra@A0 | SEPULVEDA PERTENCE | `voto_resultado` | HC DE OFICIO / TRANCAMENTO POR FALTA DE JUSTA CAUSA (NEM CONDENA NEM ABSOLVE) | CONCEDE HABEAS CORPUS DE OFICIO E TRANCA A ACAO PENAL (NAO ABSOLVE) |
| AP-409-R01-I01::dolo | RICARDO LEWANDOWSKI | `enfrentou_a_questao` | SIM | ADESAO |
| AP-416-R01-I01::concorreu | CARMEN LUCIA | `enfrentou_a_questao` | NAO | ADESAO |
| AP-416-R01-I01::concorreu | CARMEN LUCIA | `posicao` | NAO_ENFRENTOU | NAO |
| AP-416-R01-I01::concorreu | ROSA WEBER | `enfrentou_a_questao` | NAO | ADESAO |
| AP-416-R01-I01::concorreu | ROSA WEBER | `posicao` | NAO_ENFRENTOU | NAO |
| AP-416-R01-I01::dolo | CARMEN LUCIA | `enfrentou_a_questao` | NAO | ADESAO |
| AP-416-R01-I01::dolo | CARMEN LUCIA | `posicao` | NAO_ENFRENTOU | NAO |
| AP-416-R01-I01::dolo | ROSA WEBER | `enfrentou_a_questao` | NAO | ADESAO |
| AP-416-R01-I01::dolo | ROSA WEBER | `posicao` | NAO_ENFRENTOU | NAO |
| AP-432-R01-I01::dolo | RICARDO LEWANDOWSKI | `enfrentou_a_questao` | ADESAO | NAO |
| AP-432-R01-I01::dolo | RICARDO LEWANDOWSKI | `posicao` | SIM | NAO_ENFRENTOU |
| AP-433-R02-I01::dolo | RICARDO LEWANDOWSKI | `enfrentou_a_questao` | SIM | NAO |
| AP-433-R02-I01::dolo | RICARDO LEWANDOWSKI | `posicao` | SIM | NAO_ENFRENTOU |
| AP-441-R01-I01 |  | `questoes_conjunto` | OUTRA | OUTRA+OUTRA |
| AP-441-R01-I02::dolo | CELSO DE MELLO | `enfrentou_a_questao` | __NULO__ | NAO |
| AP-441-R01-I02::dolo | CELSO DE MELLO | `posicao` | __NULO__ | NAO_ENFRENTOU |
| AP-441-R01-I02::dolo | LUIZ FUX | `enfrentou_a_questao` | SIM | ADESAO |
| AP-441-R02-I01 |  | `questoes_conjunto` | OUTRA | OUTRA+OUTRA |
| AP-441-R02-I02::dolo | CELSO DE MELLO | `enfrentou_a_questao` | __NULO__ | NAO |
| AP-441-R02-I02::dolo | CELSO DE MELLO | `posicao` | __NULO__ | NAO_ENFRENTOU |
| AP-441-R02-I02::dolo | LUIZ FUX | `enfrentou_a_questao` | SIM | ADESAO |
| AP-447-R01-I01 |  | `questoes_conjunto` | DOLO+OUTRA | DOLO |
| AP-447-R01-I01::dolo | CEZAR PELUSO | `enfrentou_a_questao` | SIM | ADESAO |
| AP-447-R01-I02::outra@A1 | CELSO DE MELLO | `enfrentou_a_questao` | NAO | ADESAO |
| AP-447-R01-I02::outra@A1 | CELSO DE MELLO | `posicao` | NAO_ENFRENTOU | NAO |
| AP-447-R02-I01 |  | `questoes_conjunto` | DOLO+OUTRA | DOLO |
| AP-447-R02-I01::dolo | CEZAR PELUSO | `enfrentou_a_questao` | SIM | ADESAO |
| AP-447-R02-I02::concorreu | CARMEN LUCIA | `enfrentou_a_questao` | SIM | ADESAO |
| AP-465-R01-I02 |  | `questoes_principais` | OUTRA | CONCORREU+OUTRA |
| AP-465-R01-I02::concorreu |  | `principal` | NAO | SIM |
| AP-465-R01-I03 |  | `questoes_principais` | OUTRA | CONCORREU+OUTRA |
| AP-465-R01-I03::concorreu |  | `principal` | NAO | SIM |
| AP-503-R01-I01::concorreu | EROS GRAU | `enfrentou_a_questao` | __NULO__ | ADESAO |
| AP-503-R01-I01::concorreu | EROS GRAU | `posicao` | __NULO__ | SIM |
| AP-503-R01-I01::outra@A0 | DIAS TOFFOLI | `enfrentou_a_questao` | ADESAO | SIM |
| AP-503-R01-I01::outra@A0 | EROS GRAU | `enfrentou_a_questao` | __NULO__ | ADESAO |
| AP-503-R01-I01::outra@A0 | EROS GRAU | `posicao` | __NULO__ | SIM |
| AP-503-R01-I02 |  | `questoes_conjunto` | OUTRA+OUTRA | OUTRA |
| AP-503-R01-I02 |  | `questoes_principais` | OUTRA+OUTRA | OUTRA |
| AP-503-R01-I02::outra@A0 | EROS GRAU | `enfrentou_a_questao` | __NULO__ | ADESAO |
| AP-503-R01-I02::outra@A0 | EROS GRAU | `posicao` | __NULO__ | SIM |
| AP-503-R01-I02::outra@A0 | MARCO AURELIO | `enfrentou_a_questao` | __NULO__ | SIM |
| AP-503-R01-I02::outra@A0 | MARCO AURELIO | `posicao` | __NULO__ | SIM |
| AP-503-R01-I02::outra@A0 | RICARDO LEWANDOWSKI | `enfrentou_a_questao` | ADESAO | SIM |
| AP-503-R01-I03::outra@A0 | DIAS TOFFOLI | `enfrentou_a_questao` | __NULO__ | ADESAO |
| AP-503-R01-I03::outra@A0 | DIAS TOFFOLI | `posicao` | __NULO__ | NAO |
| AP-503-R01-I03::outra@A0 | EROS GRAU | `enfrentou_a_questao` | __NULO__ | ADESAO |
| AP-503-R01-I03::outra@A0 | EROS GRAU | `posicao` | __NULO__ | NAO |
| AP-503-R01-I03::outra@A0 | MARCO AURELIO | `enfrentou_a_questao` | __NULO__ | ADESAO |
| AP-503-R01-I03::outra@A0 | MARCO AURELIO | `posicao` | __NULO__ | NAO |
| AP-503-R01-I03::outra@A0 | RICARDO LEWANDOWSKI | `enfrentou_a_questao` | __NULO__ | ADESAO |
| AP-503-R01-I03::outra@A0 | RICARDO LEWANDOWSKI | `posicao` | __NULO__ | NAO |
| AP-565-R01-I01::concorreu | RICARDO LEWANDOWSKI | `enfrentou_a_questao` | ADESAO | SIM |
| AP-565-R01-I02::outra@A1 | CELSO DE MELLO | `enfrentou_a_questao` | NAO | ADESAO |
| AP-565-R01-I02::outra@A1 | CELSO DE MELLO | `posicao` | NAO_ENFRENTOU | NAO |
| AP-565-R02-I01::concorreu | RICARDO LEWANDOWSKI | `enfrentou_a_questao` | ADESAO | SIM |
| AP-565-R02-I02::outra@A1 | CELSO DE MELLO | `enfrentou_a_questao` | NAO | ADESAO |
| AP-565-R02-I02::outra@A1 | CELSO DE MELLO | `posicao` | NAO_ENFRENTOU | NAO |
| AP-565-R03-I01::concorreu | RICARDO LEWANDOWSKI | `enfrentou_a_questao` | ADESAO | SIM |
| AP-565-R03-I02::outra@A1 | CELSO DE MELLO | `enfrentou_a_questao` | NAO | ADESAO |
| AP-565-R03-I02::outra@A1 | CELSO DE MELLO | `posicao` | NAO_ENFRENTOU | NAO |
| AP-565-R04-I01::dolo | GILMAR MENDES | `enfrentou_a_questao` | ADESAO | SIM |
| AP-565-R04-I02::outra@A1 | CELSO DE MELLO | `enfrentou_a_questao` | NAO | ADESAO |
| AP-565-R04-I02::outra@A1 | CELSO DE MELLO | `posicao` | NAO_ENFRENTOU | NAO |
| AP-565-R05-I01::dolo | GILMAR MENDES | `enfrentou_a_questao` | ADESAO | SIM |
| AP-565-R05-I02::outra@A1 | CELSO DE MELLO | `enfrentou_a_questao` | NAO | ADESAO |
| AP-565-R05-I02::outra@A1 | CELSO DE MELLO | `posicao` | NAO_ENFRENTOU | NAO |
| AP-565-R06-I01::dolo | GILMAR MENDES | `enfrentou_a_questao` | ADESAO | SIM |
| AP-565-R06-I02::outra@A1 | CELSO DE MELLO | `enfrentou_a_questao` | NAO | ADESAO |
| AP-565-R06-I02::outra@A1 | CELSO DE MELLO | `posicao` | NAO_ENFRENTOU | NAO |
| AP-565-R07-I01::concorreu | JOAQUIM BARBOSA | `voto_resultado` | CONDENA | ABSOLVE |
| AP-565-R07-I01::concorreu | MARCO AURELIO | `enfrentou_a_questao` | ADESAO | SIM |
| AP-565-R07-I01::dolo | GILMAR MENDES | `enfrentou_a_questao` | ADESAO | SIM |
| AP-565-R07-I01::dolo | JOAQUIM BARBOSA | `voto_resultado` | CONDENA | ABSOLVE |
| AP-565-R07-I02::concorreu | MARCO AURELIO | `enfrentou_a_questao` | NAO | SIM |
| AP-565-R07-I02::concorreu | MARCO AURELIO | `posicao` | NAO_ENFRENTOU | SIM |
| AP-565-R07-I02::outra@A1 | CELSO DE MELLO | `enfrentou_a_questao` | NAO | ADESAO |
| AP-565-R07-I02::outra@A1 | CELSO DE MELLO | `posicao` | NAO_ENFRENTOU | NAO |
| AP-565-R08-I01::dolo | GILMAR MENDES | `enfrentou_a_questao` | ADESAO | SIM |
| AP-565-R08-I02::outra@A1 | CELSO DE MELLO | `enfrentou_a_questao` | NAO | ADESAO |
| AP-565-R08-I02::outra@A1 | CELSO DE MELLO | `posicao` | NAO_ENFRENTOU | NAO |
| AP-565-R09-I01::concorreu | JOAQUIM BARBOSA | `voto_resultado` | CONDENA | ABSOLVE |
| AP-565-R09-I01::concorreu | MARCO AURELIO | `enfrentou_a_questao` | ADESAO | SIM |
| AP-565-R09-I01::dolo | GILMAR MENDES | `enfrentou_a_questao` | ADESAO | SIM |
| AP-565-R09-I01::dolo | JOAQUIM BARBOSA | `voto_resultado` | CONDENA | ABSOLVE |
| AP-565-R09-I02::concorreu | MARCO AURELIO | `enfrentou_a_questao` | NAO | SIM |
| AP-565-R09-I02::concorreu | MARCO AURELIO | `posicao` | NAO_ENFRENTOU | SIM |
| AP-565-R09-I02::outra@A1 | CELSO DE MELLO | `enfrentou_a_questao` | NAO | ADESAO |
| AP-565-R09-I02::outra@A1 | CELSO DE MELLO | `posicao` | NAO_ENFRENTOU | NAO |
| AP-973-R01-I01::concorreu | DIAS TOFFOLI | `enfrentou_a_questao` | ADESAO | __NULO__ |
| AP-973-R01-I01::concorreu | DIAS TOFFOLI | `posicao` | NAO | __NULO__ |

**Unidades sem par** (desdobramento ou junção divergente): só A ['AP-1025-R01-I02::outra@A1', 'AP-1025-R03-I01::concorreu#2', 'AP-447-R01-I01::outra@A1', 'AP-447-R02-I01::outra@A1', 'AP-447-R02-I02::outra@A1', 'AP-465-R01-I02::outra@A0', 'AP-465-R01-I03::outra@A0', 'AP-503-R01-I02::outra@A1']; só B ['AP-441-R01-I01::outra@B1', 'AP-441-R02-I01::outra@B1', 'AP-447-R02-I02::outra@B1', 'AP-465-R01-I02::outra@B1', 'AP-465-R01-I03::outra@B1']
