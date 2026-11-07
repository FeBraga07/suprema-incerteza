#!/usr/bin/env python3
"""Primeira análise da Fase 4 sobre os dados congelados (versão 2, 24/10/2026, com a AP-307; CONGELAMENTO_2026-10-24.md).
A versão 1 (18/10, 24 casos) está em consolidado_v1_2026-10-18/ e analise/resultados_preliminares_fase4.md.

As quatro descritivas do PLANO.md (Fase 4, passo 3): unanimidade por questão decisiva; a mesma questão
em anos diferentes; réus recorrentes lado a lado; relator vencido. Regras de leitura dos dados:
- análise principal só com unidades ativas e escopo Levcovitz = Sim (D-049 B); as de fora vão à parte;
- votos Extingue/Tranca ficam fora da comparação de posição no mérito (R16, G4-08);
- posição "própria" = enfrentou_a_questao = Sim; adesão conta à parte (R11);
- questão de direito = tipicidade/enquadramento e ato_de_oficio; questão de prova = dolo, concorreu,
  tipicidade/existencia_fato (distinção da G4-04).

Uso: python3 analise_fase4.py <consolidado> <1_casos.psv> <saida.md>
"""
import csv, sys
from collections import Counter, defaultdict

CONS, CASOS, SAIDA = sys.argv[1:4]
rd = lambda p: list(csv.DictReader(open(p, encoding='utf-8'), delimiter='|'))
U = {r['id_unidade']: r for r in rd(f'{CONS}/fase4_unidades.psv')}
Q = rd(f'{CONS}/fase4_questoes.psv')
P = rd(f'{CONS}/fase4_posicoes.psv')
C = {r['id_caso']: r for r in rd(CASOS)}
ano = lambda uid: int(C[U[uid]['id_caso']]['ano_julgamento'])

def natureza(q):
    if q['categoria'] == 'ato_de_oficio' or (q['categoria'] == 'tipicidade' and q['anotacao_tipicidade'] == 'enquadramento'):
        return 'direito'
    if q['categoria'] in ('dolo', 'concorreu') or q['categoria'] == 'tipicidade':
        return 'prova'
    return 'outra'

def rotulo(q):
    return q['categoria'] + (f"/{q['anotacao_tipicidade']}" if q['anotacao_tipicidade'] else '')

ativas = {k: u for k, u in U.items() if u['status'] == 'ativa'}
QA = [q for q in Q if q['id_unidade'] in ativas and q['status'] == 'ativa']
pos_por_q = defaultdict(list)
for p in P:
    pos_por_q[(p['id_unidade'], p['indice_questao'])].append(p)

def placar(q):
    c = Counter(p['voto_resultado'] for p in pos_por_q[(q['id_unidade'], q['indice'])] if p['voto_resultado'] in ('Condena', 'Absolve'))
    return c

out = []
w = out.append
w('# Resultados preliminares da Fase 4 (primeira passada)\n')
w('Gerado por `analise_fase4.py` sobre os dados congelados na versão 2 (24/10/2026, 25 casos, com a AP-307). **Primeira passada, para leitura do pesquisador: nada aqui é texto do TCC.**\n')
esc = Counter(ativas[k]['escopo_levcovitz'] for k in ativas)
w(f'Unidades ativas: {len(ativas)} ({esc["Sim"]} no escopo Levcovitz, {esc["Nao"]} fora). Questões ativas: {len(QA)}.\n')

# 1. unanimidade por questão decisiva (principal), escopo Sim
w('## 1. Unanimidade por questão decisiva (questão principal; escopo Levcovitz)\n')
w('| questão | natureza | unidades | casos | anos | unânimes | resposta do Tribunal sim/não |\n|---|---|---:|---:|---|---:|---|')
grp = defaultdict(list)
for q in QA:
    if q['principal'] == 'Sim' and ativas[q['id_unidade']]['escopo_levcovitz'] == 'Sim':
        grp[rotulo(q)].append(q)
for k, qs in sorted(grp.items(), key=lambda x: -len(x[1])):
    casos = {U[q['id_unidade']]['id_caso'] for q in qs}; anos = sorted({ano(q['id_unidade']) for q in qs})
    un = sum(1 for q in qs if len(placar(q)) == 1)
    resp = Counter(q['resposta_tribunal'] for q in qs)
    w(f"| {k} | {natureza(qs[0])} | {len(qs)} | {len(casos)} | {anos[0]}–{anos[-1]} | {un} ({un*100//len(qs)}%) | {resp.get('sim',0)}/{resp.get('nao',0)} |")
w('')

# 2. a mesma questão em anos diferentes: por ministro, posições próprias em casos diferentes
w('## 2. A mesma questão em anos diferentes: ministros que responderam de modo diferente\n')
w('Para cada ministro e cada questão (categoria e anotação), as posições **próprias** (`Sim` em enfrentou) em casos diferentes, no escopo Levcovitz e sem votos Extingue/Tranca. Posição na direção alinhada (R9): pró-acusação ou pró-defesa. "Muda" = o mesmo ministro fica do lado da acusação num caso e da defesa noutro. Nas questões de **prova** isso é esperado, porque os fatos diferem; nas de **direito**, é candidato a instabilidade e pede leitura.\n')
mp = defaultdict(lambda: defaultdict(list))
for q in QA:
    if ativas[q['id_unidade']]['escopo_levcovitz'] != 'Sim':
        continue
    for p in pos_por_q[(q['id_unidade'], q['indice'])]:
        if p['enfrentou_a_questao'] != 'Sim' or p['posicao'] not in ('sim', 'nao') or p['voto_resultado'] not in ('Condena', 'Absolve'):
            continue
        dirc = 'pró-acusação' if (p['posicao'] == 'sim') == (q['sim_favorece'] == 'acusacao') else 'pró-defesa'
        if q['sim_favorece'] not in ('acusacao', 'defesa'):
            continue
        mp[(p['ministro'], rotulo(q))][U[q['id_unidade']]['id_caso']].append((dirc, p['voto_resultado'], q['id_unidade']))
linhas = []
for (m, k), por_caso in mp.items():
    if len(por_caso) < 2:
        continue
    resp = {c: Counter(x[0] for x in v).most_common(1)[0][0] for c, v in por_caso.items()}
    muda = len(set(resp.values())) > 1
    nat = natureza({'categoria': k.split('/')[0], 'anotacao_tipicidade': k.split('/')[1] if '/' in k else ''})
    linhas.append((nat, k, m, len(por_caso), muda, '; '.join(f"{c} ({ano(por_caso[c][0][2])}): {resp[c]}" for c in sorted(por_caso, key=lambda c: ano(por_caso[c][0][2])))))
res = Counter((l[0], l[4]) for l in linhas)
w(f"Pares ministro × questão com posição própria em 2 ou mais casos: **{len(linhas)}**. Questões de direito: {res[('direito', True)]} mudam, {res[('direito', False)]} não mudam. Questões de prova: {res[('prova', True)]} mudam, {res[('prova', False)]} não mudam.\n")
w('### 2a. Questões de direito, na categoria (comparabilidade grossa)\n\n**Cuidado:** `tipicidade/enquadramento` junta tipos penais e elementares diferentes (peculato, art. 92, art. 89, incisos do DL 201/67). \"Mudar\" aqui quase sempre é responder a perguntas jurídicas diferentes. A comparação que conta está em 2c.\n\n| questão | ministro | casos | muda? | posições no tempo |\n|---|---|---:|---|---|')
for l in sorted(l for l in linhas if l[0] == 'direito'):
    w(f"| {l[1]} | {l[2]} | {l[3]} | {'**sim**' if l[4] else 'não'} | {l[5]} |")
w('\n### 2b. Questões de prova (só os que mudam)\n\n| questão | ministro | casos | posições no tempo |\n|---|---|---:|---|')
for l in sorted(l for l in linhas if l[0] == 'prova' and l[4]):
    w(f"| {l[1]} | {l[2]} | {l[3]} | {l[5]} |")
w('')

# 2c. grupos finos de questões de direito (mesma pergunta jurídica), proposta da sessão a conferir
GRUPOS = {
    'G1 · verba aplicada em finalidade diversa, revertida à Administração, é desvio "em proveito próprio ou alheio"? (peculato / DL 201, art. 1º, I)':
        ['AP-375-R01-I01', 'AP-375-R02-I01', 'AP-365-R01-I01', 'AP-365-R02-I01', 'AP-372-R01-I01', 'AP-372-R02-I01'],
    'G2 · sem lei que fixe a destinação da verba, há emprego irregular (art. 315 do CP)?':
        ['AP-375-R01-I02', 'AP-365-R01-I02'],
    'G3 · uso indevido de rendas públicas em proveito próprio (DL 201, art. 1º, II): mesmo inciso, fatos diferentes; comparabilidade a confirmar na leitura':
        ['AP-441-R01-I01', 'AP-441-R02-I01', 'AP-432-R01-I01a'],
    'G5 · pagamento sem autorização legal ou contra norma financeira é a despesa do DL 201, art. 1º, V? (achado pelo revisor cego, D-054; na AP-441 a questão inclui a emendatio, e quem fica "pró-defesa" condena pelo inciso II)':
        ['AP-503-R01-I02', 'AP-441-R01-I02', 'AP-441-R02-I02'],
    'G4 · a corrupção passiva exige ato de ofício determinado? (AP-307 e AP-470; AP-1025 pelos precedentes)':
        ['AP-307-R01-I01a', 'AP-307-R01-I01b', 'AP-307-R02-I01a', 'AP-307-R02-I01b', 'AP-470-R14-I01', 'AP-470-R15-I01', 'AP-470-R17-I01', 'AP-470-R19-I01', 'AP-470-R20-I01', 'AP-470-R21-I01', 'AP-470-R23-I01'],
}
w('### 2c. Questões de direito com a mesma pergunta jurídica (comparabilidade fina)\n')
w('Agrupamento proposto pela sessão a partir do texto das perguntas (G1–G4) e verificado por revisor cego, que reconstruiu os quatro e acrescentou o G5 (D-054; `analise/revisao_cega_agrupamento_2026-10-24/`). Fora destes grupos, cada pergunta de direito aparece num caso só, e não há comparação no tempo.\n')
for nome, uids in GRUPOS.items():
    w(f'**{nome}**\n\n| unidade | ano | resposta do Tribunal | placar (C×A) | pró-acusação | pró-defesa |\n|---|---|---|---|---|---|')
    porm = defaultdict(dict)
    for uid in uids:
        if uid not in ativas: continue
        for q in QA:
            if q['id_unidade'] != uid or not (q['categoria'] == 'ato_de_oficio' if nome.startswith('G4') else q['anotacao_tipicidade'] == 'enquadramento'): continue
            pl = placar(q); ac, de = [], []
            for p in pos_por_q[(uid, q['indice'])]:
                if p['posicao'] not in ('sim', 'nao') or p['voto_resultado'] not in ('Condena', 'Absolve'): continue
                d = 'A' if (p['posicao'] == 'sim') == (q['sim_favorece'] == 'acusacao') else 'D'
                (ac if d == 'A' else de).append(p['ministro'].split()[-1] + ('' if p['enfrentou_a_questao'] == 'Sim' else '*'))
                porm[p['ministro']][U[uid]['id_caso']] = d
            w(f"| {uid} | {ano(uid)} | {q['resposta_tribunal']} | {pl.get('Condena',0)}×{pl.get('Absolve',0)} | {', '.join(ac)} | {', '.join(de)} |")
    mud = [m for m, d in porm.items() if len(d) > 1 and len(set(d.values())) > 1]
    rep = [m for m, d in porm.items() if len(d) > 1]
    w(f"\nMinistros presentes em mais de um caso do grupo: {len(rep)}; que mudam de lado: {len(mud)}{' (' + ', '.join(mud) + ')' if mud else ''}. (* = posição por adesão)\n")

# 3. réus recorrentes
w('## 3. Réus recorrentes, lado a lado\n')
REC = {'Cássio Taniguchi': ['AP-426', 'AP-430', 'AP-503'], 'Fernando Collor de Mello': ['AP-307', 'AP-465', 'AP-1025'], 'Jackson Barreto de Lima': ['AP-375', 'AP-365', 'AP-372'], 'Sérgio Ivan Moraes': ['AP-447', 'AP-416']}
for reu, casos in REC.items():
    w(f'**{reu}**\n\n| caso | ano | unidade | escopo | questão principal | resposta | placar (C×A) |\n|---|---|---|---|---|---|---|')
    for c in casos:
        for uid, u in sorted(ativas.items()):
            if u['id_caso'] != c or not uid.startswith(c + '-R01'):
                continue
            for q in QA:
                if q['id_unidade'] == uid and q['principal'] == 'Sim':
                    pl = placar(q)
                    w(f"| {c} | {ano(uid)} | {uid} | {u['escopo_levcovitz']} | {rotulo(q)} | {q['resposta_tribunal']} | {pl.get('Condena',0)}×{pl.get('Absolve',0)} |")
    w('')
w('_Atenção: o réu R01 de cada caso foi tomado como o réu recorrente; conferir na leitura (Jackson Barreto é R01 nos três?)._\n')

# 4. relator vencido
w('## 4. Relator vencido (D-032)\n')
venc = [c for c, r in C.items() if r.get('relator_vencido') == 'Sim']
w('Casos com relator vencido: ' + ', '.join(f"{c} ({C[c]['ano_julgamento']}; relator {C[c]['relator']}, redator {C[c]['redator_acordao']})" for c in venc) + '.\n')

# fora do escopo, à parte
w('## 5. À parte: unidades fora do escopo Levcovitz (D-049 B)\n')
fora = Counter(rotulo(q) for q in QA if q['principal'] == 'Sim' and ativas[q['id_unidade']]['escopo_levcovitz'] == 'Nao')
w(', '.join(f'{k}: {v}' for k, v in fora.most_common()) + '.\n')
open(SAIDA, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
