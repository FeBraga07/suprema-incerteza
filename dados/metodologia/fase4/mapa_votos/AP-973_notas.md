# AP-973 — notas do mapa de votos (27/09/2026)

Gerado por `claude-opus-5-5` (subagente), a partir de `dados/corpus/texto/AP-973.txt` (225 p.). O documento é o **julgamento conjunto das AP 969, 973 e 974** do mesmo réu; todas as peças tratam das três ações. O universo do TCC é só a AP-973, e a coluna `obs` do `.psv` indica, peça a peça, as páginas que se referem a cada AP.

**(a) OCR que exige o PDF.** Nenhum. O PDF é de texto nativo (`text_based` no manifesto), e o texto extraído é legível. Conferi três pontos no PDF (p.4, 90 e 132). As três anomalias abaixo **estão no original**, não vêm da extração:
- p.4: o cabeçalho do relatório indica "REVISORA: MIN. CÁRMEN LÚCIA". As demais peças e as atas indicam o Revisor Ricardo Lewandowski.
- p.90: a fala de Alexandre de Moraes está grafada "(RELATOR)".
- p.132: o voto de Fachin cita "Ação Penal 963"; pelo contexto, trata-se da AP 969.

**(b) Peças anunciadas e ausentes.**
- **Dias Toffoli:** não há nenhuma peça dele. O voto só aparece como "vencido" no dispositivo da ata (p.224) e do acórdão (p.3). O banco registra `lido`, e a fonte localizável é só a ata.
- **Extrato de ata de 30/09/2021:** o Presidente anuncia que vai consignar a retificação "na ata de hoje" (p.222), mas esse extrato não está no documento. Só existem as atas de 23/09 (p.13) e 29/09 (p.224-225).
- **Dosimetria:** Barroso reserva sua manifestação sobre a dosimetria (p.159), e Lewandowski pede uma sessão para que os vencidos a votem (p.212-221 e p.222-223). O documento não traz nenhuma peça posterior sobre isso.
- Os votos escritos anunciados nas antecipações **estão juntados**: o de Lewandowski (anúncio na p.67, voto nas p.69-89) e o de Cármen Lúcia (anúncio na p.177, voto nas p.179-205).
- Não há dosimetria isolada da AP 973. Nas p.127-128, Nunes Marques fixa uma pena única pelo art. 1º do DL 201/67 para as APs 973 e 974 (continuidade).

**(c) DIVERGE.** Nenhum. Os resultados e os vencidos do banco, para os 10 ministros, coincidem com os dispositivos dos votos e com a ata (p.3, p.224). Um ponto estrutural, não contraditório: o dispositivo de Fux diz "julgo procedente a Ação Penal", no singular e sem indicar a AP (p.211).

**(d) Como li.** Por navegação, sem leitura integral das 225 páginas.
- Li por inteiro, ou em trecho contínuo: p.1-5, 10-14, 62-73, 89-90, 97-99, 126-132, 148-161, 162-163 (parcial), 167-168, 175-179, 205, 208-212 e 222-225.
- Nas demais páginas, localizei início e fim de cada peça pelo cabeçalho de página ("Voto - MIN. X", "Debate" etc.), pelos títulos internos de seção (AP 969/973/974, preliminares, mérito, dosimetria) e pelos marcadores de fala ("O SENHOR MINISTRO..."), com `grep` usado só para navegar.
- No debate (p.212-221), identifiquei os falantes pelos marcadores de fala. Só falam Lewandowski, Fux, Barroso e Gilmar Mendes.
