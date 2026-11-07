# AP-465 — notas do mapa de votos (27/09/2026)

Modelo: claude-opus-5-5 (subagente). Fonte: `dados/corpus/texto/AP-465.txt` (171 pp., `text_based` segundo o manifesto, docTP=TP).

**(a) OCR.** Nenhum problema: texto nativo, sem caracteres corrompidos. Marcas do próprio original, não de OCR: três falas "CANCELADO" (Fux/Barbosa, p.166) e as sequências de encerramento `###` (p.64, p.153) e `xxxxxxxxxxxxxxx` (p.143). Não foi preciso abrir o PDF.

**(b) Peças anunciadas e ausentes.** Não há peça anunciada que falte. Dois registros estruturais:
- Dias Toffoli só tem no acórdão o voto escrito (p.65-142). Não há transcrição de fala oral dele, embora Fux (p.162) e Lewandowski (p.164) mencionem argumentos do Revisor.
- A "Explicação" da Relatora (p.62-64) aparece depois do voto dela no PDF, mas o próprio texto indica que foi dita antes da leitura do voto.
- Na p.170 a Relatora diz "Há um Ministro impedido". A ata (p.171) registra só três ausências justificadas (Celso de Mello, Marco Aurélio, Gilmar Mendes). O acórdão não identifica esse ministro.

**(c) DIVERGE.**
- Linha 6 (Dias Toffoli): o extrato de ata (p.171) não lista Toffoli entre os "vencidos, em parte". O banco registra `vencido=Sim` com base no voto escrito (p.113 e p.142). Essa divergência já estava documentada em `casos/AP-465.json`, e o banco não foi alterado.

**(d) Como li.** Por navegação. Mapeei os cabeçalhos de peça de todas as 171 páginas. Li na íntegra as p.14-15 (fim do relatório e início do voto da Relatora), 60-66 (fim do voto da Relatora, Explicação, início do Revisor), 113 e 142 (trechos do Revisor citados no banco, para conferir o DIVERGE) e 143-171 (todos os votos orais, apartes, esclarecimento, debates e ata). O corpo dos votos da Relatora (p.16-59) e do Revisor (p.66-112, 114-141) foi só percorrido por grep, para confirmar que não tem falas de outros ministros. Não tem.

Observação: o banco dá `fonte_voto=sem_evidencia` para Cármen Lúcia, e o voto escrito dela está nas p.15-61.
