# AP-503 — notas do mapa de votos (27/09/2026)

**Paginação (procedimento).** `corpus/texto/AP-503.txt` é o único texto do corpus sem os marcadores `===== [página N/M] =====`, e as páginas não foram estimadas por ele. Gerei uma cópia paginada temporária, fora do projeto, com `pdftotext -layout -f N -l N corpus/pdf/AP-503.pdf` página a página (103 páginas), em `scratchpad/AP-503_paginado/`. Todas as páginas do mapa são do PDF. O corpus não foi alterado.

**(a) OCR que exige o PDF.** Nenhum problema que impeça a leitura: o PDF é texto nativo. Há artefatos menores de extração: letras espaçadas (p.81 "5 0 3"; p.91 "p r e t é r i t o s", "C o n s e q u ê n c i a s"), "seriara" e "o ito" (p.93) e "CARMEN" sem acento (p.93).

**(b) Peças anunciadas e ausentes.**
- Não há voto do Revisor (Marco Aurélio) sobre o mérito dos incisos V e XIV. No entanto, os votos do inciso V se referem a ele: Dias Toffoli "subscrevo os dois votos já proferidos" (p.84), Cármen Lúcia "com as achegas do Ministro Revisor" (p.85) e Lewandowski "acompanho [...] também o eminente Revisor" (p.86). Do Revisor, o acórdão só traz o voto do inciso IV (p.78), dois apartes (p.83 e 87) e o voto de dosimetria (p.88).
- Eros Grau não tem peça no acórdão. Só aparece entre os presentes (p.102-103).
- Sobre o inciso XIV, só há peças de Cármen Lúcia (p.76) e Ayres Britto (p.77), além da seção do Relator (pp.32-43). Sobre o inciso V, não há peça separada de Ayres Britto com título: a da p.87 foi identificada pela sequência.
- O debate da p.96 começa no meio. O Relator responde a uma intervenção de Dias Toffoli ("o efeito pretendido pelo eminente Ministro DIAS TOFFOLI") que não está no acórdão.
- Duas falas do Relator aparecem como "CANCELADO" (p.100).

**(c) DIVERGE.** Nenhum. Há uma ressalva estrutural, que não contradiz o banco. O `3_votos.psv` tem uma linha por ministro para o réu R01, com `fato` vazio, enquanto o texto separa o mérito por inciso. O `Absolve`/`vencido=Sim` de Marco Aurélio corresponde ao voto do inciso IV (p.78). No mesmo texto, ele fixa pena quanto ao inciso V (p.88). Os `Condena` dos demais convivem com a absolvição unânime no inciso XIV. O próprio JSON do caso registra essa redução. Não marquei DIVERGE, mas quem ler por inciso deve usar as colunas `obs`. Os votos de Ayres Britto, Cármen Lúcia, Dias Toffoli e Eros Grau estão como `sem_evidencia` no banco. Os três primeiros têm peças localizadas neste mapa. Eros Grau não tem nenhuma.

**(d) Como li.** Por navegação com leitura. Li integralmente as pp.4-6, 28-30 e 75-103 (todas as peças após o voto do Relator e a ata). Li as páginas de transição do voto do Relator (pp.32, 43, 52, 53, 67, 73-75) para delimitar os trechos por inciso. Não li integralmente as pp.1-3 (ementa), 7-27 (relatório, com a denúncia transcrita) e o corpo do voto do Relator entre as transições. Busquei títulos de peça e "inciso" página a página, só para navegar.
