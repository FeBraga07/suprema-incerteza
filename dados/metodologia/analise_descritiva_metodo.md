# Análise descritiva — o que é, o que rege

> Executada em 09/08/2026, logo após o L3. Cobre o escopo que `PLANO_EXTRACAO.md`
> §3 ("L3 · Consolidação e derivadas") previa: unanimidade ao longo do tempo,
> por composição da corte, por modalidade, por cargo do réu; distribuição do
> motivo da absolvição. Acrescenta dois recortes de comparabilidade não
> previstos no plano original, descobertos ao rodar o script (§7 e §7.1
> abaixo).

**Script:** `dados/metodologia/analise_descritiva.py`. Lê as 3 tabelas do
L3, não escreve nelas. Saídas em `dados/derivados/`:
- `analise_descritiva.md` — o relatório completo, com as 8 seções.
- `cargo_categoria_auditoria.psv` — tabela auditável `id_caso_reu | cargo_funcao (bruto) | cargo_categoria (heurística)`, uma linha por réu. Existe porque a categorização de cargo é a parte menos confiável deste build (ver pendência 1 abaixo) e não deve ser usada como agregado sem poder ser conferida linha a linha.

Como o `build_l3.py`, é determinístico e roda de novo se as tabelas do L3 mudarem — não editar os `.md`/`.psv` de saída à mão.

## Decisões de desenho tomadas aqui

1. **Categorização de `cargo_funcao` em `cargo_categoria` é heurística de palavra-chave sobre texto livre — CONFIRMADA em 22/08/2026 (D-025).** É o mesmo tipo de abordagem que já falhou uma vez neste projeto (regex de cargo, Onda 2 — `DICIONARIO.md` Seção 2.2: "cargo capturado por correspondência equivocada"). Revisão linha a linha dos 63 réus contra `cargo_categoria_auditoria.psv` encontrou e corrigiu 2 erros (AP-441-R02, correspondência incidental; AP-973-R01, negação — "Prefeito de fato" resolvido por override manual documentado). 0 réus não classificados após o fix. Ver `DECISOES.md` D-025.
2. **A categorização usa o cargo "à época dos fatos" — CONFIRMADO em 22/08/2026 (D-026).** Não o cargo no momento do julgamento, quando o texto distingue os dois (maioria dos réus foi Prefeito nos fatos e virou Deputado Federal depois, o que muda o foro mas não o cargo relevante para a conduta imputada). Efeito: muda a categoria de ~15 réus em relação à alternativa (cargo no julgamento). Ver `DECISOES.md` D-026.
3. **"Composição da corte" (seção 3) foi operacionalizada como `n_votantes`**, não como uma reconstrução da composição exata por data (que já existe em `4_referencia_ministros.psv`, mas cruzá-la data a data com os 24 julgamentos não foi feito). `n_votantes` mistura vacância formal com ausência/impedimento pontual — é proxy grosseiro, declarado como tal no relatório.
4. **Cluster DL 201/67 (seção 7)** foi escolhido como o recorte de comparabilidade mais limpo por ser a única "família" de casos que entra no universo por uma única regra normativa explícita (D-013) — não é o único recorte possível (dá para agrupar por modalidade Levcovitz, por relator, por cargo etc.), só o mais defensável para abrir a seção de resultados.

## Achado não previsto no plano — réus recorrentes (seção 7.1)

Ao construir o cluster DL 201/67, apareceu Cássio Taniguchi em dois casos daquela lista com resultados diferentes (AP-426 absolvição, AP-503 condenação parcial). Isso levantou a pergunta óbvia — quantos réus aparecem em mais de um dos 24 casos, no corpus inteiro, não só no cluster DL201? Resposta: 4 réus, 2 deles com resultado diferente entre julgamentos (Cássio Taniguchi; Fernando Collor de Mello). Ver seção 7.1 do relatório para os casos e a ressalva de que nenhum dos dois é "mesmo fato, resultado diferente" no sentido mais estrito — é o material mais próximo disso que o corpus tem, não a prova em si.

**Achado que quase se perdeu por acento:** a chave de agrupamento por nome inicial (sem normalização) reconhecia só 2 dos 3 casos de Taniguchi, porque a AP-430 o grafa sem acento ("Cassio") e a AP-426/AP-503 com acento ("Cássio") — extrações independentes, sessões diferentes, grafias diferentes da mesma fonte. Corrigido com `unicodedata.normalize` antes de agrupar. Vale como nota de método: qualquer join futuro por nome de réu ou ministro neste banco precisa da mesma normalização, ou perde casos silenciosamente.

## Pendências — status em 22/08/2026

As pendências 1 e 2 acima (categorização de cargo e "época dos fatos" vs. "época do julgamento") foram resolvidas nesta sessão (D-025, D-026). Ver `ESTADO.md`, seção "L3 CONCLUÍDA", para as demais pendências do build.
