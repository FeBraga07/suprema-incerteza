# AP-565 — notas do mapa de votos (27/09/2026)

Mapa: `AP-565.psv` com 85 linhas. Há mais linhas que peças porque os votos longos (relatora, revisor, Joaquim Barbosa, Marco Aurélio na dosimetria) estão divididos em trechos por réu, como pedido. Réus: R01 Cassol, R02 Salomão, R03 Erodi, R04 Aníbal, R05 Neilton, R06 Izalino, R07 Ivalino, R08 Josué, R09 Ilva.

## (a) OCR
O PDF é `text_based` (manifesto), sem OCR. Conferi com `pdftotext` e o texto do corpus corresponde à camada de texto do PDF. Há apenas grafias do próprio documento: "Uva Mezzomo" por Ilva (p202), "lzalino/lvalino" com L minúsculo (p255), "MEZZONO" na relatora (p67 e seguintes) e "Salomão de Almeida" na fala de Barroso (p269). Nenhum desses casos exige abrir a imagem do PDF.

## (b) Peças anunciadas que não estão no acórdão
- p310: Joaquim Barbosa diz que transcreve na íntegra o seu voto da AP 470 sobre perda do mandato. O texto transcrito não está no acórdão: a peça termina na p311 com uma linha.
- Votos na 1ª e na 2ª questão de ordem e nas preliminares: Teori Zavascki, Joaquim Barbosa e outros ministros não têm peça própria. Só aparecem no placar da ata (p187 e p313: "por unanimidade"; Presidente "votou nas questões de ordem e nas preliminares").
- Luiz Fux estava impedido e não tem peça. Aparece só na ata (p188, p314 e p315).

## (c) DIVERGE
- Linha `ordem=63` (Joaquim Barbosa, p255): o dispositivo escrito condena os nove réus pelo art. 90 e pelo art. 288, **incluídos R07 e R09**. O banco registra `Absolve` para Joaquim Barbosa em R07 e R09, o que segue a ata (p314: "absolver, por unanimidade, os acusados Ivalino Mezzomo e Ilva Mezzomo Crisóstomo"). O texto do voto e a ata não batem entre si. Não corrigi nada.

## (d) Como li
- **Por navegação**, não li o acórdão inteiro. Mapeei as 315 páginas pelo rótulo de peça no cabeçalho de cada página, pelo número de autenticação do documento e pelos locutores. Com `grep`, localizei os subtítulos internos dos votos da relatora e do revisor, sem extrair resultado.
- **Li integralmente** p7 (início), p45-66, p184-191, p201-216 (revisor, art. 90), p229-268 (dispositivo do revisor, todos os votos de mérito dos demais, debates, confirmação e esclarecimentos), p269-279, p310-315 e as duas atas (p187-188 e p313-315).
- **Li por trechos** o voto da relatora nas fronteiras de seção (p111, p138, p148, p152-163, p178-183), o revisor p220-221 e o restante da dosimetria (p280-309), neste caso só os locutores e a menção a réus.

## Observações estruturais
- `3_votos.psv` só tem linhas do art. 90. Os trechos sobre o art. 288 levam `NA`, e a ata registra votos vencidos nesse crime (Marco Aurélio e Joaquim Barbosa, p314).
- Os 90 votos `sem_evidencia` estão localizados. O texto próprio por réu está nas linhas da relatora (138-159), do revisor (201-216), de Joaquim Barbosa (250-255) e de Marco Aurélio na dosimetria (305-307). Os demais votos de mérito (Barroso, Teori, Rosa, Gilmar, Marco Aurélio, Celso, Lewandowski, p234-249) tratam os réus em conjunto ou por grupo, na mesma página, sem trecho separado por réu.
- O dispositivo escrito do revisor (p230-231) já menciona o resultado do empate. A redação é, portanto, posterior à votação.
