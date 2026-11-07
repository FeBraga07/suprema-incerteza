# Prompt comum: mapa estrutural de votos (Fase 4, preparação) — 27/09/2026

Você está apoiando o TCC de Economia do Felipe Braga (Insper) sobre estabilidade decisória do STF em Ações Penais de corrupção julgadas pelo Plenário. Trabalhe em português brasileiro.

Raiz do projeto: ``

## Para que serve

A Fase 4 do trabalho (D-033) vai ler a fundamentação de todos os acórdãos para extrair, por réu × fato, a questão jurídica que decidiu o resultado e a posição de cada ministro. O vocabulário dessa questão será escrito pelo Felipe **depois**, e até lá nenhum agente pode categorizar fundamentação. Seu trabalho é só o **mapa de navegação**: onde está cada peça e cada voto de cada ministro, para que a leitura posterior não precise procurar. O mapa também vai localizar o texto dos votos que o banco registra como `sem_evidencia` ou `deducao D-004` (D-034).

## Fontes

- Texto: `dados/corpus/texto/AP-XXX.txt`. Os marcadores `===== [página N/M] =====` dão a página do PDF, que é a convenção de página do banco.
- PDF original, para tirar dúvida de OCR: `dados/corpus/pdf/`.
- Banco, **só para conferir e para preencher as colunas marcadas "do banco"**: `dados/derivados/3_votos.psv` (colunas `voto_resultado`, `vencido`, `fonte_voto`) e `dados/derivados/casos/AP-XXX.json` (réus e crimes).

## O que entregar, por caso

**1. `dados/metodologia/fase4/mapa_votos/AP-XXX.psv`**, separado por `|`, com cabeçalho e uma linha por peça:

```
id_caso|ordem|peca|ministro|pag_ini|pag_fim|tem_texto|reus_abrangidos|voto_banco|vencido_banco|fonte_voto_banco|obs
```

- `peca`: um de `ementa`, `acordao`, `relatorio`, `voto`, `voto_aditamento`, `confirmacao_voto`, `debate`, `aparte`, `questao_ordem`, `extrato_ata`, `outro`. Use `outro` com explicação em `obs`.
- `ministro`: nome como o banco grafa (confira em `3_votos.psv`); vazio para peças sem autor (ementa, ata). Em debates, liste os ministros que falam, separados por `;`.
- `tem_texto`: `Sim` se há fundamentação escrita própria (mais que poucas linhas); `Adesao` se é só "acompanho o relator/a divergência" ou equivalente; `Nao` se o ministro só aparece na ata.
- **Todo ministro que votou segundo o banco precisa aparecer em ao menos uma linha.** Se ele não tem peça nenhuma no acórdão, crie uma linha `peca=extrato_ata`, `tem_texto=Nao`, com a página da ata onde ele é contado.
- `reus_abrangidos`: ids `AP-XXX-Rnn` do banco a que a peça se refere, separados por `;`. Use `todos` quando for o caso.
- `voto_banco`, `vencido_banco`, `fonte_voto_banco`: **copiados** de `3_votos.psv` para aquele ministro e réu (quando varia por réu, use `varia` e detalhe em `obs`). Não corrija o banco. Se o texto contradisser o banco, registre em `obs` com a página, começando por `DIVERGE:`.
- `obs`: só informação estrutural (ex.: "cancelado", "voto juntado depois", "trata só do réu R02", "peça fora da ordem cronológica").

**2. `dados/metodologia/fase4/mapa_votos/AP-XXX_notas.md`**: no máximo 1 página, com (a) problemas de OCR que exijam o PDF, com página; (b) peças anunciadas que não estão no acórdão; (c) todas as linhas `DIVERGE:`; (d) como você leu (inteiro, ou por navegação — diga quais páginas).

## Proibido — é o ponto mais importante

- **Não** nomeie, resuma nem categorize a questão jurídica, a tese ou o argumento de nenhum voto. Nada de "discute o dolo", "trata da prova", "questão da prescrição". Só estrutura: quem, onde, quanto, com que resultado segundo o banco.
- **Não** proponha vocabulário nem categorias.
- **Não** use regex ou busca textual para extrair resultado, placar ou vencidos: esses vêm do banco. Busca textual (`grep`) é permitida **só para navegar** (achar onde começa uma peça).
- **Não** edite nenhum arquivo existente. Escreva só os dois arquivos do seu caso.
- Não invente página. Se não tiver certeza, marque `?` e explique em `obs`.

## Ao terminar

Responda em no máximo 5 linhas por caso: arquivos escritos; nº de peças; nº de ministros sem texto próprio; nº de `DIVERGE:`; problemas de OCR.
