# AP-1025 — notas do mapa estrutural de votos

Produzido em 27/09/2026 por subagente `claude-opus-5-5`, conforme `PROMPT_MAPA.md`. Arquivo de dados: `AP-1025.psv` (59 linhas).

**(a) OCR.** O PDF é `text_based` (extraído com pdftotext, manifesto `TP`), então não há OCR. Não encontrei página que exija o PDF. O único defeito é de diagramação: em alguns cabeçalhos de fala, o texto justificado sai com uma palavra por linha (p677, 744-753, 822, 871), mas continua legível. As páginas curtas (menos de 900 caracteres) são todas fins de peça.

**(b) Peças anunciadas que não estão no acórdão, e outras lacunas estruturais**
- **Luiz Fux, mérito:** não há peça. O voto só aparece contado na ata de 18/05 (p685). Fux tem texto apenas na questão de ordem (p830) e na dosimetria (p864-865).
- **Roberto Barroso e Cármen Lúcia, mérito:** a única peça de cada um é a rotulada "Antecipação ao Voto" (p673-676 e p677-682). Nenhum dos dois juntou voto escrito. A peça de Cármen Lúcia traz "Publicado sem revisão".
- **Reajuste de voto do Revisor (25/05):** registrado na ata (p842) e mencionado pelo Relator (p758), mas sem peça própria.
- **Dosimetria do Revisor (31/05):** não há "Voto s/ Dosimetria" de Moraes. Ele fala sobre o tema no Debate (p848-853), e o voto escrito do Revisor traz uma seção de dosimetria (p504-518). Em 25/05, porém, o Relator diz que o Revisor ainda não votara essa matéria (p817), o que indica texto escrito completado depois da sessão.
- **Outros textos completados depois da sessão:** os votos escritos de Nunes Marques (p662-672) e Rosa Weber (p809-810) incluem dosimetria, matéria só votada em 31/05.
- **Juntadas anunciadas e não localizadas:** as razões escritas do Relator sobre a questão de ordem (anunciadas em p820) e a "adaptação" do escrito de Cármen Lúcia na dosimetria (anunciada em p869).
- **Anomalia na ata de 10/05 (p33):** consta "Não participou, justificadamente, deste julgamento, o Ministro Gilmar Mendes", mas ele está na lista de presentes da mesma sessão e votou em 24/05 (p710-743, ata p757). Registro sem interpretar.
- **Ausências:** Nunes Marques faltou em 10/05; Dias Toffoli faltou em 17/05 e 18/05 (votou em 24/05). Cármen Lúcia não votou na questão de ordem (p843).
- **Ricardo Lewandowski:** o banco registra "Não votou". O nome não consta de nenhuma lista de presentes das 7 atas. Incluí uma linha só para cobrir o banco.
- **p66-68 (dentro do voto do Relator):** transcrevem falas de outro julgado citado (Ayres Britto, Celso de Mello, Joaquim Barbosa). Não são falas deste julgamento.

**(c) Linhas `DIVERGE:`** Nenhuma. As atas de 17/05, 18/05, 24/05 e 25/05 (p522, 685, 757, 842) e o dispositivo final (p882-885) são compatíveis com `voto_resultado` e `vencido` do banco para os 10 votantes.

**(d) Como li: por navegação, não inteiro.**
1. Mapeei o rótulo de cada página, que fica na 2ª linha após o marcador `===== [página N/885] =====`.
2. Localizei o início de cada peça pelo cabeçalho "AÇÃO PENAL 1.025 DISTRITO FEDERAL" e pelas falas "O SENHOR MINISTRO / A SENHORA MINISTRA".
3. Li o início e o fim de cada peça para confirmar autor e limites.
4. Li integralmente os 7 extratos de ata (p33, 34, 520-522, 683-686, 754-757, 839-843, 878-885), a ementa e o acórdão (p1-9), as peças de 1 a 2 páginas (p32, 519, 523, 617-618, 758-760, 817-824, 836-838) e o início e o fim de cada página das peças de dosimetria e debate (p844-877).
5. Nos votos longos (p35-235, 236-518, 543-616, 619-672, 687-709, 710-743, 761-810), li só a abertura e o fecho, e usei busca textual apenas para achar os títulos de seção da dosimetria.

Não li a fundamentação de nenhum voto. Os resultados vêm do banco (`3_votos.psv`).

**Convenções de classificação usadas:**
- "Antecipação ao Voto" virou `voto` quando é a única peça de mérito do ministro (Barroso, Cármen Lúcia), e `outro` quando há voto escrito em seguida (Mendonça).
- Peças rotuladas "Esclarecimento" ou "Observação" com várias falas viraram `debate`; com um só autor, `outro`.
- Votos sobre a questão de ordem viraram `questao_ordem`, e "Voto s/ Dosimetria" virou `voto`, com a indicação em `obs`.
- `reus_abrangidos` = `todos` em todas as linhas, porque nenhuma peça se limita formalmente a um réu.
