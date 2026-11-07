#!/usr/bin/env python3
"""Consolidação da Fase 4 (D-048, D-049).

Parte da leitura A dos 24 casos e aplica, sem nova leitura, as decisões do gate de 18/10/2026.
Cada alteração fica registrada no próprio elemento (campo `edicoes`) e em LOG_CONSOLIDACAO.md,
com o item do gate ou a regra que a autoriza. Nada é apagado: questão ou unidade que sai da
análise recebe `status` e `motivo_status`.

Uso: python3 consolidar_fase4.py <dir_A> <dir_B> <pareamento.psv> <2_casos_reus.psv> <1_casos.psv> <saida>
"""
import copy, csv, glob, json, os, random, sys
from collections import Counter, defaultdict

DIR_A, DIR_B, PAREAMENTO, CASOS_REUS, CASOS, SAIDA = sys.argv[1:7]
os.makedirs(SAIDA, exist_ok=True)

def V(x):
    return x.get('valor') if isinstance(x, dict) else x

def texto(x):
    x = V(x) if isinstance(x, dict) else x
    return x or ''

LOG = []
def edita(obj, campo, novo, regra, nota=''):
    antigo = obj.get(campo)
    obj[campo] = novo
    obj.setdefault('edicoes', []).append({'campo': campo, 'de': antigo, 'para': novo, 'regra': regra, 'nota': nota})
    return antigo

def log(caso, alvo, regra, texto):
    LOG.append((caso, alvo, regra, texto))

def carrega(d):
    return {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in sorted(glob.glob(os.path.join(d, '*.json')))}

A, B = carrega(DIR_A), carrega(DIR_B)
casos = {k: copy.deepcopy(v) for k, v in A.items()}
pol = {(r['leitura'], r['id_unidade'], r['indice']): r for r in csv.DictReader(open(PAREAMENTO, encoding='utf-8'), delimiter='|')}
relator = {r['id_caso']: r.get('relator', '') for r in csv.DictReader(open(CASOS, encoding='utf-8'), delimiter='|')}

def unid(caso, uid):
    for u in casos[caso]['unidades']:
        if u['id_unidade'] == uid:
            return u
    raise KeyError(uid)

def pos(q, ministro):
    for p in q['posicoes']:
        if p['ministro'] == ministro:
            return p
    raise KeyError(ministro)

def unid_b(caso, uid):
    for u in B[caso]['unidades']:
        if u['id_unidade'] == uid:
            return u
    raise KeyError(uid)

# ---------------------------------------------------------------- 0. campos novos e normalização
# D-051: a AP-307 foi lida com o prompt v2 (codebook v2): o leitor já marca tipicidade/ato_de_oficio,
# anotacao_tipicidade, anotacoes e sim_favorece (este só em `outra`). Esses campos são preservados.
LIDOS_V2 = {'AP-307'}
CATS_V2 = ('dolo', 'concorreu', 'tipicidade', 'ato_de_oficio')
for caso in LIDOS_V2 & set(casos):
    for u in casos[caso]['unidades']:
        u.setdefault('status', 'ativa'); u.setdefault('motivo_status', None)
        for qi, q in enumerate(u['questoes']):
            q.setdefault('status', 'ativa'); q.setdefault('motivo_status', None)
            q['categoria_v2'] = V(q['questao_decisiva'])
            q['anotacao_tipicidade'] = V(q.get('anotacao_tipicidade')) if q['categoria_v2'] == 'tipicidade' else None
            q['anotacoes'] = list(V(q.get('anotacoes')) or [])
            if isinstance(q.get('questao_outra_descricao'), dict):
                qd = q['questao_outra_descricao']
                q['questao_outra_evidencia'] = {k: qd.get(k) for k in ('evidencia', 'fonte', 'confianca')}
                q['questao_outra_descricao'] = qd.get('valor')
            q['sim_favorece'] = 'acusacao' if q['categoria_v2'] in CATS_V2 else V(q.get('sim_favorece'))
            for p in q['posicoes']:
                p['voto_resultado_original'] = V(p['voto_resultado'])
    log(caso, '*', 'D-051', 'lido com o prompt v2: categorias, anotações e sim_favorece do leitor preservados')
for caso, d in casos.items():
    if caso in LIDOS_V2:
        continue
    for u in d['unidades']:
        u.setdefault('status', 'ativa'); u.setdefault('motivo_status', None)
        for qi, q in enumerate(u['questoes']):
            q.setdefault('status', 'ativa'); q.setdefault('motivo_status', None)
            q['categoria_v2'] = V(q['questao_decisiva'])
            q['anotacao_tipicidade'] = None
            q['anotacoes'] = []
            # G4-28: questao_outra_descricao como texto
            qd = q.get('questao_outra_descricao')
            if isinstance(qd, dict):
                q['questao_outra_evidencia'] = {k: qd.get(k) for k in ('evidencia', 'fonte', 'confianca')}
                q['questao_outra_descricao'] = qd.get('valor')
                log(caso, u['id_unidade'] + f' q{qi}', 'G4-28', 'questao_outra_descricao normalizada de objeto para texto')
            # R9 / G4-09 a G4-11: direção do sim
            if q['categoria_v2'] in ('dolo', 'concorreu'):
                q['sim_favorece'] = 'acusacao'
            else:
                r = pol.get(('A', u['id_unidade'], str(qi)))
                q['sim_favorece'] = r['sim_favorece'] if r else None
            for p in q['posicoes']:
                p['voto_resultado_original'] = V(p['voto_resultado'])

# ---------------------------------------------------------------- 1. categorias do codebook v2 (G4-02, G4-03)
# Proposta da sessão, a conferir pelo Felipe (lista em reclassificacao_outra.psv).
ENQ, EXI = 'enquadramento', 'existencia_fato'
RECLASS = {
    ('AP-1025-R01-I02', 0): ('tipicidade', EXI), ('AP-1025-R01-I02', 1): ('tipicidade', ENQ),
    ('AP-1025-R01-I03', 0): ('tipicidade', EXI), ('AP-1025-R01-I03', 1): ('tipicidade', ENQ),
    ('AP-1025-R02-I02', 0): ('tipicidade', EXI),
    ('AP-1025-R02-I03', 0): ('tipicidade', EXI), ('AP-1025-R02-I03', 1): ('tipicidade', ENQ),
    ('AP-1025-R03-I02', 0): ('tipicidade', EXI),
    ('AP-1025-R03-I03', 0): ('tipicidade', EXI), ('AP-1025-R03-I03', 1): ('tipicidade', ENQ),
    ('AP-1032-R01-I02', 0): ('tipicidade', EXI), ('AP-1032-R02-I02', 0): ('tipicidade', EXI),
    ('AP-348-R01-I01', 0): ('tipicidade', ENQ),
    ('AP-365-R01-I01', 0): ('tipicidade', ENQ), ('AP-365-R01-I02', 0): ('tipicidade', ENQ),
    ('AP-365-R02-I01', 0): ('tipicidade', ENQ),
    ('AP-372-R01-I01', 0): ('tipicidade', ENQ), ('AP-372-R01-I02', 0): ('tipicidade', ENQ),
    ('AP-372-R02-I01', 0): ('tipicidade', ENQ), ('AP-372-R02-I02', 0): ('tipicidade', ENQ),
    ('AP-375-R01-I01', 0): ('tipicidade', ENQ), ('AP-375-R01-I02', 0): ('tipicidade', ENQ),
    ('AP-375-R02-I01', 0): ('tipicidade', ENQ),
    ('AP-396-R01-I02', 0): ('tipicidade', ENQ), ('AP-396-R01-I02', 1): ('tipicidade', EXI),
    ('AP-430-R01-I01', 0): ('tipicidade', EXI), ('AP-430-R01-I02', 0): ('tipicidade', EXI),
    ('AP-432-R01-I01', 0): ('tipicidade', ENQ),
    ('AP-433-R01-I01', 0): ('tipicidade', ENQ), ('AP-433-R02-I01', 0): ('tipicidade', ENQ),
    ('AP-441-R01-I01', 0): ('tipicidade', ENQ), ('AP-441-R01-I02', 0): ('tipicidade', ENQ),
    ('AP-441-R02-I01', 0): ('tipicidade', ENQ), ('AP-441-R02-I02', 0): ('tipicidade', ENQ),
    ('AP-447-R01-I01', 1): ('tipicidade', ENQ), ('AP-447-R01-I02', 1): ('tipicidade', ENQ),
    ('AP-447-R02-I01', 1): ('tipicidade', ENQ),
    ('AP-465-R01-I01', 1): ('tipicidade', EXI),
    ('AP-503-R01-I01', 0): ('tipicidade', ENQ), ('AP-503-R01-I02', 0): ('tipicidade', ENQ),
    ('AP-503-R01-I02', 1): ('tipicidade', ENQ), ('AP-503-R01-I03', 0): ('tipicidade', ENQ),
    ('AP-565-R01-I02', 0): ('tipicidade', ENQ), ('AP-565-R01-I02', 1): ('tipicidade', ENQ),
    ('AP-565-R02-I02', 0): ('tipicidade', ENQ), ('AP-565-R02-I02', 1): ('tipicidade', ENQ),
    ('AP-565-R03-I02', 0): ('tipicidade', ENQ), ('AP-565-R03-I02', 1): ('tipicidade', ENQ),
    ('AP-565-R04-I02', 1): ('tipicidade', ENQ), ('AP-565-R05-I02', 1): ('tipicidade', ENQ),
    ('AP-565-R06-I02', 1): ('tipicidade', ENQ), ('AP-565-R07-I02', 1): ('tipicidade', ENQ),
    ('AP-565-R08-I02', 1): ('tipicidade', ENQ), ('AP-565-R09-I02', 1): ('tipicidade', ENQ),
    ('AP-940-R01-I01', 1): ('tipicidade', EXI),
    # G4-03: ato de ofício (AP-470, item VI)
    ('AP-470-R14-I01', 0): ('ato_de_oficio', None), ('AP-470-R15-I01', 1): ('ato_de_oficio', None),
    ('AP-470-R17-I01', 0): ('ato_de_oficio', None), ('AP-470-R19-I01', 0): ('ato_de_oficio', None),
    ('AP-470-R20-I01', 0): ('ato_de_oficio', None), ('AP-470-R21-I01', 0): ('ato_de_oficio', None),
    ('AP-470-R23-I01', 1): ('ato_de_oficio', None),
}
# Ficam `outra`: AP-365-R01-I02 q1 (fato descrito na denúncia), prescrição da AP-465 (R6b) e da AP-508 (R6c),
# interceptação da AP-508 I02 (sai pela G4-22).
reclass_rows = []
for caso, d in casos.items():
    for u in d['unidades']:
        for qi, q in enumerate(u['questoes']):
            if V(q['questao_decisiva']) != 'outra':
                continue
            cat, anot = RECLASS.get((u['id_unidade'], qi), ('outra', None))
            if cat != 'outra':
                edita(q, 'categoria_v2', cat, 'G4-02' if cat == 'tipicidade' else 'G4-03')
                q['anotacao_tipicidade'] = anot
            reclass_rows.append([u['id_unidade'], qi, V(u['escopo_levcovitz']), V(q['principal']), q['sim_favorece'], cat, anot or '', q['questao_outra_descricao']])
assert all(any(u['id_unidade'] == k[0] for d in casos.values() for u in d['unidades']) for k in RECLASS), 'id inexistente em RECLASS'

# ---------------------------------------------------------------- 2. anotações de prova (G4-04, G4-17)
for caso, uids in (('AP-1032', ['AP-1032-R01-I01', 'AP-1032-R02-I01']), ('AP-1036', ['AP-1036-R01-I01']),
                   ('AP-1025', ['AP-1025-R01-I01', 'AP-1025-R02-I01'])):
    for uid in uids:
        u = unid(caso, uid)
        for qi, q in enumerate(u['questoes']):
            if q['categoria_v2'] != 'concorreu':
                continue
            txt = json.dumps(q, ensure_ascii=False).lower()
            if 'colabora' in txt:
                q['anotacoes'].append('prova_colaboracao'); log(caso, f'{uid} q{qi}', 'G4-04', 'anotação prova_colaboracao (o texto da questão menciona colaboração)')
            else:
                log(caso, f'{uid} q{qi}', 'G4-04', 'SEM menção a colaboração no texto transcrito; anotação não aplicada')
u = unid('AP-973', 'AP-973-R01-I01')
u['questoes'][0]['anotacoes'].append('prova_inquerito'); log('AP-973', 'AP-973-R01-I01 q0', 'G4-17', 'anotação prova_inquerito (art. 155 do CPP como modo de responder)')

# ---------------------------------------------------------------- 3. exclusões (G4-05, G4-21, G4-22, R6c)
for caso, uid, motivo in (('AP-940', 'AP-940-R01-I02', 'G4-21: não imputada; improbidade citada pelo relator só como obiter dictum (p. 22)'),
                          ('AP-1025', 'AP-1025-R02-I04', 'G4-21: denúncia rejeitada no recebimento pela 2ª Turma (22/08/2017), fora do recorte'),
                          ('AP-1025', 'AP-1025-R02-I05', 'G4-21: denúncia rejeitada no recebimento pela 2ª Turma (22/08/2017), fora do recorte')):
    u = unid(caso, uid); edita(u, 'status', 'excluida', 'G4-21'); u['motivo_status'] = motivo; log(caso, uid, 'G4-21', 'unidade excluída da Fase 4')

u = unid('AP-348', 'AP-348-R01-I01')
for qi, q in enumerate(u['questoes']):
    if q['categoria_v2'] == 'dolo':
        edita(q, 'status', 'excluida', 'G4-05/R10'); q['motivo_status'] = 'R10: o relator declara o dolo prejudicado pela atipicidade'
        log('AP-348', f'AP-348-R01-I01 q{qi}', 'R10', 'questão de dolo declarada prejudicada sai da unidade')

u = unid('AP-508', 'AP-508-R01-I02')
for qi, q in enumerate(u['questoes']):
    if 'intercepta' in (q.get('questao_outra_descricao') or '').lower():
        edita(q, 'status', 'excluida', 'G4-22/R6'); q['motivo_status'] = 'R6: o relator a chama de preliminar'
        log('AP-508', f'AP-508-R01-I02 q{qi}', 'R6', 'interceptação (preliminar) sai como questão')
    elif q['categoria_v2'] == 'concorreu':
        edita(q, 'principal', {'valor': 'Sim', 'evidencia': None, 'fonte': 'G4-22', 'confianca': 'alta'}, 'G4-22', 'principal única depois da saída da preliminar')

for uid in ('AP-508-R01-I01', 'AP-508-R01-I03', 'AP-508-R01-I04'):
    u = unid('AP-508', uid)
    for qi, q in enumerate(u['questoes']):
        edita(q, 'status', 'excluida', 'R6c'); q['motivo_status'] = 'R6c: unidade só com prescrição, sem questão decisiva'
    log('AP-508', uid, 'R6c', 'unidade fica sem questão decisiva (continua na descritiva)')

# ---------------------------------------------------------------- 4. voto sem mérito (G4-08, G4-24)
for p in unid('AP-375', 'AP-375-R02-I01')['questoes'][0]['posicoes']:
    edita(p, 'voto_resultado', {'valor': 'Tranca', 'evidencia': V(p['voto_resultado']) and p['voto_resultado'].get('evidencia'), 'fonte': p['voto_resultado'].get('fonte'), 'confianca': 'alta'}, 'G4-08')
log('AP-375', 'AP-375-R02-I01', 'G4-08', 'voto_resultado = Tranca (HC de ofício, falta de justa causa) nos 8 ministros')
for uid in ('AP-465-R01-I02', 'AP-465-R01-I03'):
    for q in unid('AP-465', uid)['questoes']:
        for m in ('Teori Zavascki', 'Rosa Weber', 'Joaquim Barbosa'):
            p = pos(q, m); edita(p, 'voto_resultado', {'valor': 'Extingue', 'evidencia': 'reconheciam a prescrição da pretensão punitiva em relação aos delitos de falsidade ideológica (art. 299 do Código Penal) e de corrupção passiva (art. 317 do Código Penal)', 'fonte': 'p. 3', 'confianca': 'alta'}, 'G4-08')
        p = pos(q, 'Dias Toffoli')
        edita(p, 'voto_resultado', {'valor': 'Absolve', 'evidencia': 'julgar improcedente a ação penal para absolver o réu com base no art. 386, inc. VII, do Código de Processo Penal, nos termos do voto da Relatora, vencidos [...] os Ministros Teori Zavascki, Rosa Weber e Joaquim Barbosa', 'fonte': 'p. 3', 'confianca': 'media'}, 'G4-24',
              'ata prevalece para o resultado; o voto escrito (p. 113) declara a prescrição dos arts. 299 e 317; Lewandowski, p. 164, cita os argumentos de Toffoli pela prescrição')
        pdx = p.get('posicao_detalhe'); pdx = V(pdx) if isinstance(pdx, dict) else pdx
        p['posicao_detalhe'] = ((pdx or '') + ' | G4-24: voto escrito declara extinta a punibilidade (p. 113: "julgo extinta a punibilidade do acusado"); a ata não o lista entre os vencidos (pp. 3, 171); Lewandowski, p. 164: "impressionado com os argumentos do eminente Ministro Dias Toffoli". Pela ata 5x3; pelo texto 4x4.').strip(' |')
    log('AP-465', uid, 'G4-08/G4-24', 'Teori, Rosa e Barbosa = Extingue; Toffoli = Absolve pela ata, com o voto escrito em posicao_detalhe')
for uid in ('AP-508-R01-I01', 'AP-508-R01-I03', 'AP-508-R01-I04'):
    for q in unid('AP-508', uid)['questoes']:
        for p in q['posicoes']:
            edita(p, 'voto_resultado', {'valor': 'Extingue', 'evidencia': None, 'fonte': 'R6c/G4-08', 'confianca': 'alta'}, 'G4-08')
    log('AP-508', uid, 'G4-08', 'voto_resultado = Extingue (prescrição declarada por todos)')

# ---------------------------------------------------------------- 5. pontos de ministro decididos no gate
# G4-13: Lewandowski, dolo, AP-409 — evidência do voto próprio (p. 77)
u = unid('AP-409', 'AP-409-R01-I01')
for q in u['questoes']:
    if q['categoria_v2'] == 'dolo':
        p = pos(q, 'Ricardo Lewandowski')
        ev = {'valor': 'Sim', 'evidencia': 'relembro que não saía um prego do almoxarifado sem que o prefeito tivesse conhecimento. Quem dirá uma enorme obra pública como um açude no principal rio que corta a cidade.', 'fonte': 'p. 77', 'confianca': 'media'}
        edita(p, 'enfrentou_a_questao', ev, 'G4-13')
        edita(p, 'posicao', {'valor': 'sim', 'evidencia': ev['evidencia'], 'fonte': 'p. 77', 'confianca': 'media', 'inferida_de': None}, 'G4-13',
              'p. 73 como evidência secundária: fala com rótulo de Lewandowski na transcrição dos debates de Cármen Lúcia')
        log('AP-409', 'AP-409-R01-I01 dolo', 'G4-13', 'Lewandowski Sim/sim com evidência principal na p. 77')

def copia_de_b(caso, uid, qi_a, qi_b, ministro, regra, nota):
    qa = unid(caso, uid)['questoes'][qi_a]; qb = unid_b(caso, uid)['questoes'][qi_b]
    assert V(qa['questao_decisiva']) == V(qb['questao_decisiva']), (uid, qi_a, qi_b)
    pa, pb = pos(qa, ministro), pos(qb, ministro)
    for campo in ('enfrentou_a_questao', 'posicao', 'fundamento_proprio'):
        edita(pa, campo, copy.deepcopy(pb.get(campo)), regra, nota)
    log(caso, f'{uid} q{qi_a} {ministro}', regra, nota)

def qidx(q_list, cat):
    return [i for i, q in enumerate(q_list) if V(q['questao_decisiva']) == cat]

# G4-14: Lewandowski, dolo, AP-432 — leitura B
copia_de_b('AP-432', 'AP-432-R01-I01', qidx(unid('AP-432', 'AP-432-R01-I01')['questoes'], 'dolo')[0],
           qidx(unid_b('AP-432', 'AP-432-R01-I01')['questoes'], 'dolo')[0], 'Ricardo Lewandowski', 'G4-14', 'G4-01 padrão (c): razão própria é a tipicidade')
# G4-20: Lewandowski, dolo, AP-433 R02 — leitura B
copia_de_b('AP-433', 'AP-433-R02-I01', qidx(unid('AP-433', 'AP-433-R02-I01')['questoes'], 'dolo')[0],
           qidx(unid_b('AP-433', 'AP-433-R02-I01')['questoes'], 'dolo')[0], 'Ricardo Lewandowski', 'G4-20', 'retificação de voto (p. 83): absolve pela unicidade do delito e isonomia')
p = pos(unid('AP-433', 'AP-433-R02-I01')['questoes'][qidx(unid('AP-433', 'AP-433-R02-I01')['questoes'], 'dolo')[0]], 'Ricardo Lewandowski')
if not p.get('fundamento_proprio'):
    edita(p, 'fundamento_proprio', 'unicidade do delito, pluralidade de agentes e isonomia (retificação de voto, p. 83)', 'G4-20')
# G4-26 (D-042): Joaquim Barbosa em R07 e R09 do art. 90 da AP-565 — leitura B, que seguiu a ata
for uid in ('AP-565-R07-I01', 'AP-565-R09-I01'):
    qa = unid('AP-565', uid)['questoes']; qb = unid_b('AP-565', uid)['questoes']
    for qi, q in enumerate(qa):
        jb = [j for j, x in enumerate(qb) if V(x['questao_decisiva']) == V(q['questao_decisiva'])][0]
        pa, pb = pos(q, 'Joaquim Barbosa'), pos(qb[jb], 'Joaquim Barbosa')
        for campo in ('voto_resultado', 'enfrentou_a_questao', 'posicao', 'fundamento_proprio'):
            edita(pa, campo, copy.deepcopy(pb.get(campo)), 'G4-26/D-042', 'a ata prevalece sobre o voto juntado')
    log('AP-565', uid, 'G4-26/D-042', 'Joaquim Barbosa pela ata (leitura B)')
# G4-19: Marco Aurélio no art. 288 de R07 e R09 — a leitura A já o registra condenando (texto próprio, p. 244: número
# mínimo de agentes, questão de tipicidade) e 'não enfrentou' na questão de concorreu, o que a R11 confirma. Sem patch.
log('AP-565', 'AP-565-R07-I02 / R09-I02 Marco Aurélio', 'G4-19/R11', 'mantida a leitura A: condena; Sim na tipicidade (p. 244), não enfrentou em concorreu')
# G4-16 (c): AP-447 R02-I02 — a secundária da leitura B (coautoria de não prefeito em crime de mão própria)
ua = unid('AP-447', 'AP-447-R02-I02'); ub = unid_b('AP-447', 'AP-447-R02-I02')
ia = [i for i, q in enumerate(ua['questoes']) if V(q['questao_decisiva']) == 'outra'][0]
ib = [i for i, q in enumerate(ub['questoes']) if 'mão própria' in json.dumps(q.get('questao_outra_descricao'), ensure_ascii=False)][0]
velha = ua['questoes'][ia]
nova = copy.deepcopy(ub['questoes'][ib])
qd = nova.get('questao_outra_descricao')
if isinstance(qd, dict):
    nova['questao_outra_evidencia'] = {k: qd.get(k) for k in ('evidencia', 'fonte', 'confianca')}; nova['questao_outra_descricao'] = qd.get('valor')
nova.update({'status': 'ativa', 'motivo_status': None, 'categoria_v2': 'tipicidade', 'anotacao_tipicidade': ENQ, 'anotacoes': [],
             'sim_favorece': pol[('B', 'AP-447-R02-I02', str(ib))]['sim_favorece'], 'origem': 'leitura B (G4-16 c)',
             'edicoes': [{'campo': 'questao', 'de': velha.get('questao_outra_descricao'), 'para': nova['questao_outra_descricao'], 'regra': 'G4-16', 'nota': 'secundária da leitura B; a da A repetia a do prefeito (R01-I02)'}]})
for p in nova['posicoes']:
    p['voto_resultado_original'] = V(p['voto_resultado'])
ua['questoes'][ia] = nova
log('AP-447', 'AP-447-R02-I02', 'G4-16', 'secundária substituída pela da leitura B (crime de mão própria), categoria tipicidade/enquadramento')
# G4-15: nota na AP-441 R01-I01
u = unid('AP-441', 'AP-441-R01-I01'); u['obs'] = (texto(u.get('obs'))) + ' | G4-15: a secundária "cabe a emendatio libelli?" da leitura B não entra aqui: é a mesma pergunta, com os mesmos votos (6x4), da principal de I02.'
# G4-12: AP-1025, redator em obs (o voto condutor da A já é o decidido)
for u in casos['AP-1025']['unidades']:
    if 'redator' not in (u.get('obs') or '').lower():
        u['obs'] = (texto(u.get('obs'))) + ' | G4-12: Alexandre de Moraes redigiu o acórdão; o voto condutor registrado é quem fundamenta (contrato §3).'

# ---------------------------------------------------------------- 5b. R11 (G4-01) aplicada às divergências A×B, caso a caso
# Lidas pela sessão em r11_divergencias_enfrentou.psv: nestas, o trecho próprio (padrão b) ou a R8 estão na leitura B.
R11_B = [
    ('AP-503', 'AP-503-R01-I01', 'outra', 'Dias Toffoli', 'R11 padrão (b): "ficou configurada a materialidade e também a autoria" (p. 79); limítrofe'),
    ('AP-565', 'AP-565-R01-I01', 'concorreu', 'Ricardo Lewandowski', 'R11 padrão (b): "houve um conluio, a meu ver" (p. 247)'),
    ('AP-565', 'AP-565-R02-I01', 'concorreu', 'Ricardo Lewandowski', 'R11 padrão (b): p. 247'),
    ('AP-565', 'AP-565-R03-I01', 'concorreu', 'Ricardo Lewandowski', 'R11 padrão (b): p. 247'),
    ('AP-565', 'AP-565-R07-I01', 'concorreu', 'Marco Aurélio', 'R11 padrão (b): "é sempre subjetiva" (p. 243)'),
    ('AP-565', 'AP-565-R09-I01', 'concorreu', 'Marco Aurélio', 'R11 padrão (b): p. 243'),
    ('AP-447', 'AP-447-R01-I02', 'outra', 'Celso de Mello', 'R8: voto só pela ata (p. 102)'),
] + [('AP-565', f'AP-565-R0{r}-I01', 'dolo', 'Gilmar Mendes', 'R11 padrão (b): "não está demonstrada [...] essa participação ou esse conluio, a não ser por presunção" (p. 240)') for r in (4, 5, 6, 7, 8, 9)]
for caso, uid, cat, mini, nota in R11_B:
    qa = unid(caso, uid)['questoes']; qb = unid_b(caso, uid)['questoes']
    ia = [i for i, q in enumerate(qa) if V(q['questao_decisiva']) == cat]; ib = [i for i, q in enumerate(qb) if V(q['questao_decisiva']) == cat]
    assert len(ia) == 1 and len(ib) == 1, (uid, cat, ia, ib)
    pa, pb = pos(qa[ia[0]], mini), pos(qb[ib[0]], mini)
    for campo in ('enfrentou_a_questao', 'posicao'):
        edita(pa, campo, copy.deepcopy(pb.get(campo)), 'R11' if nota.startswith('R11') else 'R8', nota)
    log(caso, f'{uid} {cat} {mini}', 'R11', 'leitura B: ' + nota)
log('*', '*', 'R11', 'nas demais divergências A×B de enfrentou, a R11 dá razão à A (lidas uma a uma; ver conferencia/r11_divergencias_enfrentou.psv); AP-1025-R02-I02 (lavagem, fora do escopo) tem estrutura divergente entre as leituras e fica como na A, sinalizada')

# ---------------------------------------------------------------- 5c. gate da AP-307 (D-052, 24/10/2026)
# Divergências A×B da leitura com o prompt v2, conferidas pela sessão no texto e decididas pelo Felipe.
if 'AP-307' in casos:
    for r in ('R01', 'R02'):
        # G5-01 (VASP): as duas principais, como na A (R5b: 8x0, resposta 'nao' nas duas; "duplo motivo", p. 126)
        log('AP-307', f'AP-307-{r}-I01b', 'G5-01/R5b', 'mantida a leitura A: tipicidade e ato_de_oficio principais')
        # G5-02 (Marcelo Ribeiro): acrescenta `concorreu` da B (p. 168 responde às duas perguntas); principal pela R5b
        ua, ub = unid('AP-307', f'AP-307-{r}-I01c'), unid_b('AP-307', f'AP-307-{r}-I01c')
        qb = copy.deepcopy(ub['questoes'][qidx(ub['questoes'], 'concorreu')[0]])
        qb.update(status='ativa', motivo_status=None, categoria_v2='concorreu', anotacao_tipicidade=None,
                  anotacoes=list(V(qb.get('anotacoes')) or []), sim_favorece='acusacao', origem='leitura B (G5-02)',
                  edicoes=[{'campo': 'questao', 'de': None, 'para': 'concorreu', 'regra': 'G5-02', 'nota': 'p. 168: "nem, tampouco, que de parte do ex-Presidente da República fora solicitada qualquer vantagem"'}])
        for p in qb['posicoes']:
            p['voto_resultado_original'] = V(p['voto_resultado'])
        ua['questoes'].append(qb)
        log('AP-307', f'AP-307-{r}-I01c', 'G5-02', 'questão concorreu acrescentada da leitura B; tipicidade e concorreu principais (R5b)')
        # G5-03: Néri da Silveira, Marcelo Ribeiro, tipicidade = Adesao (p. 663: "Limito-me [...] a acompanhar")
        copia_de_b('AP-307', f'AP-307-{r}-I01c', qidx(ua['questoes'], 'tipicidade')[0], qidx(ub['questoes'], 'tipicidade')[0],
                   'Néri da Silveira', 'G5-03/R11', 'só declara acompanhar; dispensa-se de reapreciar a prova (p. 663)')
        # G5-05 (Mercedes): anotação prova_inquerito em concorreu (depoimento de Scheuer só na polícia; pp. 599, 622)
        qa = unid('AP-307', f'AP-307-{r}-I01a')['questoes']
        q = qa[qidx(qa, 'concorreu')[0]]
        if 'prova_inquerito' not in q['anotacoes']:
            edita(q, 'anotacoes', q['anotacoes'] + ['prova_inquerito'], 'G5-05', 'Celso descarta o depoimento não produzido em juízo (p. 599); Pertence o aceita confirmado em juízo (p. 622)')
        log('AP-307', f'AP-307-{r}-I01a', 'G5-05', 'anotação prova_inquerito (leitura B)')
    # G5-04 (Cláudio Vieira): Sanches como na A (razão própria é a falta de ato de ofício, p. 639: R11 'Nao' nas duas);
    # Moreira Alves não enfrenta a tipicidade (absolve pela inverossimilhança do intermediário e pelo abandono da acusação, pp. 414-415)
    ua, ub = unid('AP-307', 'AP-307-R03-I01'), unid_b('AP-307', 'AP-307-R03-I01')
    copia_de_b('AP-307', 'AP-307-R03-I01', qidx(ua['questoes'], 'tipicidade')[0], qidx(ub['questoes'], 'tipicidade')[0],
               'Moreira Alves', 'G5-04/R11', 'a razão própria é a participação (p. 415), não a existência do crime')
    log('AP-307', 'AP-307-R03-I01 Sydney Sanches', 'G5-04/R11', 'mantida a leitura A: não enfrentou as duas; ato de ofício em fundamento_proprio')

# ---------------------------------------------------------------- 6. R8: ministro cujo voto só consta da ata (G4-15, G4-17, G4-23)
# Se a leitura já tirou a posição da ata, ela fica; a R8 só marca a adesão. Se não tirou, a posição é a de quem
# conduz o lado do ministro na unidade: o voto condutor, se estiver nesse lado; senão o relator; senão o primeiro
# ministro desse lado que fundamentou a questão principal.
r8_rows = []
for caso, d in casos.items():
    for u in d['unidades']:
        if u['status'] != 'ativa':
            continue
        cond = V(u['voto_condutor'])
        qp = next((q for q in u['questoes'] if q['status'] == 'ativa' and V(q['principal']) == 'Sim'), u['questoes'][0] if u['questoes'] else None)
        def lider_do_lado(lado, exceto):
            # o lado é o voto e, quando a leitura tirou da ata a posição do ministro na questão principal, também essa posição
            pm = next((V(x.get('posicao')) for x in qp['posicoes'] if x['ministro'] == exceto), None)
            mesmos = [x for x in qp['posicoes'] if V(x['voto_resultado']) == lado and x['ministro'] != exceto and (pm is None or V(x.get('posicao')) == pm)]
            for crit in (lambda x: x['ministro'] == cond, lambda x: x['ministro'] == relator.get(caso), lambda x: V(x.get('enfrentou_a_questao')) == 'Sim'):
                m = next((x['ministro'] for x in mesmos if crit(x)), None)
                if m: return m
            return None
        for qi, q in enumerate(u['questoes']):
            for p in q['posicoes']:
                if V(p.get('enfrentou_a_questao')) is not None:
                    continue
                lado = V(p['voto_resultado'])
                fonte = p['voto_resultado'].get('fonte') if isinstance(p['voto_resultado'], dict) else None
                edita(p, 'enfrentou_a_questao', {'valor': 'Adesao', 'evidencia': None, 'fonte': fonte, 'confianca': 'baixa'}, 'R8')
                if V(p.get('posicao')) is not None:
                    po = p['posicao']; po['confianca'] = 'baixa'
                    po['inferida_de'] = (po.get('inferida_de') or '') + ' | R8: posição tirada da ata pela leitura; mantida'
                    r8_rows.append([u['id_unidade'], qi, p['ministro'], lado, '(ata, pela leitura)', V(po), 'mantida da leitura']); continue
                lider = lider_do_lado(lado, p['ministro'])
                lp = next((x for x in q['posicoes'] if x['ministro'] == lider), None) if lider else None
                if lp is None or V(lp.get('posicao')) is None:
                    r8_rows.append([u['id_unidade'], qi, p['ministro'], lado, lider or '', '', 'SEM LÍDER COM POSIÇÃO: fica vazio']); continue
                edita(p, 'posicao', {'valor': V(lp['posicao']), 'evidencia': None, 'fonte': fonte, 'confianca': 'baixa',
                                     'inferida_de': f"R8: voto só pela ata ({fonte}); posição de {lider}, que conduz o lado"}, 'R8')
                r8_rows.append([u['id_unidade'], qi, p['ministro'], lado, lider, V(lp['posicao']), 'aplicada'])
log('*', '*', 'R8', f'{len(r8_rows)} posições marcadas pela R8: ' + str(Counter(r[-1] for r in r8_rows)))

# ---------------------------------------------------------------- 7. fusão (G4-07) e anotações de unidade
for r in ('R01', 'R02'):
    u1, u2 = unid('AP-372', f'AP-372-{r}-I01'), unid('AP-372', f'AP-372-{r}-I02')
    def assinatura(u):
        return sorted((qi, p['ministro'], V(p['voto_resultado']), V(p['posicao'])) for qi, q in enumerate(u['questoes']) for p in q['posicoes'])
    iguais = assinatura(u1) == assinatura(u2)
    log('AP-372', f'AP-372-{r}-I01/I02', 'G4-07', f'votos e posições idênticos nas duas classificações: {iguais}')
    if iguais:
        edita(u2, 'status', 'fundida', 'G4-07'); u2['motivo_status'] = f'G4-07: fundida em AP-372-{r}-I01 (mesmo fato; todos votam igual nas duas classificações)'
        u1['ajuste_unidade'] = {'valor': 'juntada', 'evidencia': f'G4-07: AP-372-{r}-I02 fundida nesta unidade', 'fonte': 'gate', 'confianca': 'alta'}
for caso, uid in (('AP-375', 'AP-375-R01-I02'), ('AP-365', 'AP-365-R01-I02')):
    u = unid(caso, uid); u['obs'] = (texto(u.get('obs'))) + ' | G4-07: art. 315 como tipificação alternativa não denunciada, decidida pelo Tribunal; mantida.'

# ---------------------------------------------------------------- 8. desdobramento por fato (G4-06)
def desdobra(caso, uid, grupos, regra='G4-06'):
    d = casos[caso]; i = [k for k, u in enumerate(d['unidades']) if u['id_unidade'] == uid][0]
    orig = d['unidades'][i]; novas = []
    for sufixo, idxs, fato, extra in grupos:
        n = copy.deepcopy(orig); n['id_unidade'] = uid + sufixo; n['unidade_origem'] = uid; n['fato'] = fato
        n['questoes'] = [copy.deepcopy(orig['questoes'][j]) for j in idxs]
        n['ajuste_unidade'] = {'valor': 'desdobrada', 'evidencia': f'{regra}: {fato}', 'fonte': 'gate', 'confianca': 'alta'}
        if extra: n.update(extra)
        ativas = [q for q in n['questoes'] if q['status'] == 'ativa']
        if len(ativas) == 1:
            edita(ativas[0], 'principal', {'valor': 'Sim', 'evidencia': None, 'fonte': regra, 'confianca': 'alta'}, regra, 'única questão da unidade desdobrada')
        novas.append(n)
    orig['status'] = 'desdobrada'; orig['motivo_status'] = f'{regra}: substituída por ' + ', '.join(x['id_unidade'] for x in novas)
    d['unidades'][i + 1:i + 1] = novas
    log(caso, uid, regra, 'desdobrada em ' + ', '.join(f"{x['id_unidade']} ({x['fato']})" for x in novas))

for uid in ('AP-1025-R01-I01', 'AP-1025-R02-I01', 'AP-1025-R03-I01'):
    u = unid('AP-1025', uid); fatos = []
    for qi, q in enumerate(u['questoes']):
        f = q.get('fato')
        if f not in [x[0] for x in fatos]:
            fatos.append((f, []))
        [x for x in fatos if x[0] == f][0][1].append(qi)
    desdobra('AP-1025', uid, [('ab'[k], idxs, f, None) for k, (f, idxs) in enumerate(fatos)])
desdobra('AP-940', 'AP-940-R01-I01', [('a', [0], '1º fato', None), ('b', [1], '2º e 3º fatos', None)])
desdobra('AP-432', 'AP-432-R01-I01', [('a', [0, 1], 'propaganda televisiva (abril de 2000)', None),
                                      ('b', [], "boletins 'Saúde Plena' (dois fatos)",
                                       {'status': 'pendente_leitura', 'motivo_status': 'G4-06: absolvição pelo voto da Revisora, contra o voto do relator (ementa, item 13, p. 3); as leituras não transcreveram as posições por ministro neste fato',
                                        'voto_condutor': {'valor': 'Rosa Weber', 'evidencia': 'nos termos do voto da Revisora, que absolveu o acusado quanto a esta imputação, por falta de provas da utilização indevida de rendas públicas em proveito próprio', 'fonte': 'p. 3', 'confianca': 'alta'}})])
casos['AP-432']['unidades'][[k for k, u in enumerate(casos['AP-432']['unidades']) if u['id_unidade'] == 'AP-432-R01-I01b'][0]]['status'] = 'pendente_leitura'

# ---------------------------------------------------------------- 9. R12 (G4-19, G4-20): calcula para todas, aplica e lista
def favorece(q, valor_pos):
    s = q.get('sim_favorece')
    if valor_pos not in ('sim', 'nao') or s not in ('acusacao', 'defesa'):
        return None
    pro_acus = (valor_pos == 'sim') == (s == 'acusacao')
    return 'Condena' if pro_acus else 'Absolve'

r12_rows = []
DECIDIDAS_R12 = {'AP-433-R01-I01', 'AP-433-R02-I01'}
# D-050: na AP-565 (art. 90, 5x5) a fórmula não dispara (concorreu tem os 5 votos absolutórios); as duas questões
# separam o placar no mesmo 5x5, e ficam principais pela R5 (empate na separação), como o Felipe decidiu no gate.
EMPATE_R5 = {'AP-565-R04-I01', 'AP-565-R05-I01', 'AP-565-R06-I01', 'AP-565-R08-I01'}
for caso, d in casos.items():
    for u in d['unidades']:
        if u['status'] != 'ativa':
            continue
        qs = [(qi, q) for qi, q in enumerate(u['questoes']) if q['status'] == 'ativa']
        if len(qs) < 2:
            continue
        votos = Counter(V(p['voto_resultado']) for p in qs[0][1]['posicoes'] if V(p['voto_resultado']) in ('Condena', 'Absolve'))
        if len(votos) < 2:
            continue  # unânime: R5b
        n = sum(votos.values()); res = 'Condena' if votos['Condena'] > votos['Absolve'] else 'Absolve'
        venc = votos[res]; necess = min(venc, n // 2 + 1)
        apoio = {}
        for qi, q in qs:
            apoio[qi] = {p['ministro'] for p in q['posicoes'] if V(p['voto_resultado']) == res and V(p.get('enfrentou_a_questao')) in ('Sim', 'Adesao') and favorece(q, V(p.get('posicao'))) == res}
        sozinha = [qi for qi in apoio if len(apoio[qi]) >= necess]
        uniao = set().union(*apoio.values())
        principais_antes = [qi for qi, q in qs if V(q['principal']) == 'Sim']
        dispara = not sozinha
        r12_rows.append([u['id_unidade'], res, f"{votos['Condena']}x{votos['Absolve']}", necess,
                         '; '.join(f"q{qi} {u['questoes'][qi]['categoria_v2']}={len(apoio[qi])}" for qi in apoio), len(uniao),
                         'SIM' if dispara else 'nao', ','.join(f'q{x}' for x in principais_antes), 'decidida no gate' if u['id_unidade'] in DECIDIDAS_R12 else ''])
        if u['id_unidade'] in EMPATE_R5:
            for qi, q in qs:
                if V(q['principal']) != 'Sim':
                    edita(q, 'principal', {'valor': 'Sim', 'evidencia': None, 'fonte': 'R5 (D-050)', 'confianca': 'media'}, 'R5/D-050', 'as duas questões separam o placar no mesmo 5x5')
            u['obs'] = texto(u.get('obs')) + f" | R5 (D-050): as duas questões são principais porque separam o placar no mesmo 5x5; a fórmula da R12 não dispara (apoio: {r12_rows[-1][4]})."
            r12_rows[-1][8] = 'R5, empate na separação (D-050)'
            continue
        if u['id_unidade'] in DECIDIDAS_R12 or dispara:
            for qi, q in qs:
                if V(q['principal']) != 'Sim':
                    edita(q, 'principal', {'valor': 'Sim', 'evidencia': None, 'fonte': 'R12', 'confianca': 'media'}, 'R12', 'maioria sem fundamento único')
            u['obs'] = (texto(u.get('obs'))) + f" | R12: as duas questões são principais (apoio do lado vencedor: {r12_rows[-1][4]}; necessários {necess})."

# ---------------------------------------------------------------- 10. precedentes (G4-27)
def paginas(s):
    out = set()
    for tok in str(s or '').replace('pp.', 'p.').replace('–', '-').replace(';', ',').split(','):
        tok = tok.strip().lstrip('p.').strip()
        if '-' in tok:
            a, _, b = tok.partition('-')
            if a.strip().isdigit() and b.strip().isdigit():
                out.update(range(int(a), int(b) + 1)); continue
        if tok.split(' ')[0].isdigit():
            out.add(int(tok.split(' ')[0]))
    return out

def filtra_precedentes(u):
    pags = defaultdict(set)
    for q in u['questoes']:
        if q.get('status', 'ativa') != 'ativa':
            continue
        for p in q['posicoes']:
            for campo in ('enfrentou_a_questao', 'posicao'):
                c = p.get(campo)
                if isinstance(c, dict):
                    pags[p['ministro']] |= paginas(c.get('fonte'))
    fica, sai = [], []
    for pr in u.get('precedentes') or []:
        ref = (pr.get('referencia') or '')
        if 'TCU' in ref or 'Tribunal de Contas' in ref:
            pr['tipo_g427'] = 'decisao_administrativa'; sai.append(pr); continue
        pp = paginas(pr.get('fonte')); alvo = pags.get(pr.get('ministro'), set())
        pr['na_pagina_da_evidencia'] = bool(pp and any(abs(a - b) <= 1 for a in pp for b in alvo))
        if not FILTRO_PAGINA or pr['na_pagina_da_evidencia']:
            fica.append(pr)
        else:
            sai.append(pr)
    return fica, sai

FILTRO_PAGINA = False  # G4-27: a regra por página tirava AP 307 e AP 470 do voto de Fachin; suspensa até nova decisão
prec_rows = []
for caso, d in casos.items():
    for u in d['unidades']:
        if u['status'] == 'desdobrada':
            u['precedentes_lidos'] = u.get('precedentes') or []; u['precedentes'] = []; continue
        fica, sai = filtra_precedentes(u)
        u['precedentes_lidos'] = u.get('precedentes') or []
        u['precedentes'] = fica
        for pr in fica: prec_rows.append([u['id_unidade'], pr.get('ministro'), pr.get('tipo'), pr.get('sentido'), pr.get('fonte'), 'fica' if pr['na_pagina_da_evidencia'] else 'fica (fora da página da evidência)', (pr.get('referencia') or '')[:120]])
        for pr in sai: prec_rows.append([u['id_unidade'], pr.get('ministro'), pr.get('tipo'), pr.get('sentido'), pr.get('fonte'), pr.get('tipo_g427', 'sai'), (pr.get('referencia') or '')[:120]])

def jaccard_filtrado():
    vals = []
    for caso in B:
        ua = {u['id_unidade']: u for u in A[caso]['unidades']}
        for ub in B[caso]['unidades']:
            if ub['id_unidade'] not in ua:
                continue
            ra = {(x.get('referencia') or '').strip().lower() for x in filtra_precedentes(copy.deepcopy(ua[ub['id_unidade']]))[0]}
            rb = {(x.get('referencia') or '').strip().lower() for x in filtra_precedentes(copy.deepcopy(ub))[0]}
            if ra or rb:
                vals.append(len(ra & rb) / len(ra | rb))
    return sum(vals) / len(vals) if vals else None, len(vals)

# ---------------------------------------------------------------- 11. conferências para o Felipe
coer_rows = []  # G4-11
for caso, d in casos.items():
    for u in d['unidades']:
        if u['status'] != 'ativa':
            continue
        princ = [q for q in u['questoes'] if q['status'] == 'ativa' and V(q['principal']) == 'Sim']
        if len(princ) != 1:
            continue
        q = princ[0]
        for p in q['posicoes']:
            vr = V(p['voto_resultado']); f = favorece(q, V(p.get('posicao')))
            if vr in ('Condena', 'Absolve') and f and f != vr and V(p.get('enfrentou_a_questao')) in ('Sim', 'Adesao'):
                coer_rows.append([u['id_unidade'], q['categoria_v2'], q['sim_favorece'], p['ministro'], V(p['enfrentou_a_questao']), V(p['posicao']), vr, (q.get('questao_outra_descricao') or '')[:150]])

motivo_rows = []  # G4-08
reus = {r['id_caso_reu']: r for r in csv.DictReader(open(CASOS_REUS, encoding='utf-8'), delimiter='|')}
por_reu = defaultdict(Counter)
for caso, d in casos.items():
    for u in d['unidades']:
        if u['status'] in ('excluida', 'desdobrada', 'fundida'):
            continue
        reu = '-'.join(u['id_unidade'].split('-')[:3])
        for q in u['questoes'][:1]:
            for p in q['posicoes']:
                por_reu[reu][V(p['voto_resultado'])] += 1
for reu, c in sorted(por_reu.items()):
    r = reus.get(reu); mot = r['motivo'] if r else '(réu fora de 2_casos_reus)'
    tem_sem_merito = c['Extingue'] + c['Tranca'] > 0
    if r and r.get('prescricao_pos_condenacao') == 'Sim':
        continue  # D-018: condenação seguida de prescrição; o voto de mérito é Condena
    if (mot in ('prescrição', 'processual')) != tem_sem_merito:
        motivo_rows.append([reu, mot, r['resultado'] if r else '', r.get('prescricao_pos_condenacao', '') if r else '', dict(c)])

r11_rows = []  # G4-01: divergências A×B em enfrentou_a_questao, resolvidas a favor da A salvo patch
for caso in B:
    ua = {u['id_unidade']: u for u in casos[caso]['unidades']}
    for ub in B[caso]['unidades']:
        u = ua.get(ub['id_unidade'])
        if not u:
            continue
        for qb in ub['questoes']:
            cands = [q for q in u['questoes'] if V(q['questao_decisiva']) == V(qb['questao_decisiva'])]
            if len(cands) != 1:
                continue
            for pb in qb['posicoes']:
                try:
                    pa = pos(cands[0], pb['ministro'])
                except KeyError:
                    continue
                ea, eb = V(pa.get('enfrentou_a_questao')), V(pb.get('enfrentou_a_questao'))
                if ea != eb and {ea, eb} <= {'Sim', 'Adesao', 'Nao'}:
                    regra = [e['regra'] for e in pa.get('edicoes', []) if e['campo'] == 'enfrentou_a_questao']
                    r11_rows.append([u['id_unidade'], V(qb['questao_decisiva']), pb['ministro'], ea, eb, regra[0] if regra else 'R11 (fica a A)',
                                     ((pa.get('enfrentou_a_questao') or {}).get('evidencia') or '')[:160], (pa.get('enfrentou_a_questao') or {}).get('fonte')])

# ---------------------------------------------------------------- 12. saída
def psv(nome, cab, linhas):
    with open(os.path.join(SAIDA, nome), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='|', lineterminator='\n'); w.writerow(cab); w.writerows(linhas)

os.makedirs(os.path.join(SAIDA, 'casos'), exist_ok=True)
for caso, d in casos.items():
    d['consolidado_em'] = '2026-10-18'; d['base'] = 'leitura A; decisões do gate (D-048, D-049) aplicadas por consolidar_fase4.py'
    json.dump(d, open(os.path.join(SAIDA, 'casos', caso + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

U, Q, P, PR = [], [], [], []
for caso, d in sorted(casos.items()):
    for u in d['unidades']:
        ativas = [q for q in u['questoes'] if q['status'] == 'ativa']
        U.append([caso, u['id_unidade'], u.get('unidade_origem', ''), u.get('fato', ''), V(u['escopo_levcovitz']), u['status'], u.get('motivo_status') or '',
                  V(u['voto_condutor']), len(ativas), sum(1 for q in ativas if V(q['principal']) == 'Sim')])
        for qi, q in enumerate(u['questoes']):
            Q.append([u['id_unidade'], qi, q['status'], q['categoria_v2'], q.get('anotacao_tipicidade') or '', ','.join(q['anotacoes']), V(q['principal']),
                      V(q['resposta_tribunal']), q.get('sim_favorece') or '', V(q.get('padrao_dolo_exigido')) or '', V(q.get('modo_concurso')) or '',
                      (q.get('questao_outra_descricao') or '').replace('\n', ' ')])
            for p in q['posicoes']:
                e, po = p.get('enfrentou_a_questao') or {}, p.get('posicao') or {}
                P.append([u['id_unidade'], qi, q['categoria_v2'], p['ministro'], V(p['voto_resultado']), p.get('voto_resultado_original'), V(e), V(po),
                          po.get('confianca') if isinstance(po, dict) else '', (po.get('inferida_de') or '') if isinstance(po, dict) else '',
                          (p.get('fundamento_proprio') or '').replace('\n', ' ') if isinstance(p.get('fundamento_proprio'), str) else json.dumps(p.get('fundamento_proprio'), ensure_ascii=False),
                          ';'.join(sorted({x['regra'] for x in p.get('edicoes', [])}))])
        for pr in u['precedentes']:
            PR.append([u['id_unidade'], pr.get('ministro'), pr.get('tipo'), pr.get('sentido'), pr.get('proprio_ministro'), pr.get('fonte'), (pr.get('referencia') or '').replace('\n', ' ')])
psv('fase4_unidades.psv', ['id_caso', 'id_unidade', 'unidade_origem', 'fato', 'escopo_levcovitz', 'status', 'motivo_status', 'voto_condutor', 'n_questoes_ativas', 'n_principais'], U)
psv('fase4_questoes.psv', ['id_unidade', 'indice', 'status', 'categoria', 'anotacao_tipicidade', 'anotacoes', 'principal', 'resposta_tribunal', 'sim_favorece', 'padrao_dolo_exigido', 'modo_concurso', 'pergunta_outra'], Q)
psv('fase4_posicoes.psv', ['id_unidade', 'indice_questao', 'categoria', 'ministro', 'voto_resultado', 'voto_resultado_original', 'enfrentou_a_questao', 'posicao', 'confianca_posicao', 'inferida_de', 'fundamento_proprio', 'regras_aplicadas'], P)
psv('fase4_precedentes.psv', ['id_unidade', 'ministro', 'tipo', 'sentido', 'proprio_ministro', 'fonte', 'referencia'], PR)
os.makedirs(os.path.join(SAIDA, 'conferencia'), exist_ok=True)
psv('conferencia/reclassificacao_outra.psv', ['id_unidade', 'indice', 'escopo', 'principal', 'sim_favorece', 'categoria_v2', 'anotacao', 'pergunta'], reclass_rows)
psv('conferencia/r8_aplicada.psv', ['id_unidade', 'indice', 'ministro', 'lado', 'lider', 'posicao_atribuida', 'status'], r8_rows)
psv('conferencia/r12_todas_as_unidades.psv', ['id_unidade', 'resultado', 'placar', 'necessarios', 'apoio_por_questao', 'apoio_uniao', 'r12_dispara', 'principais_antes', 'nota'], r12_rows)
psv('conferencia/coerencia_marca_voto.psv', ['id_unidade', 'categoria', 'sim_favorece', 'ministro', 'enfrentou', 'posicao', 'voto', 'pergunta'], coer_rows)
psv('conferencia/cruzamento_motivo.psv', ['id_caso_reu', 'motivo_banco', 'resultado_banco', 'prescricao_pos_condenacao', 'votos_fase4'], motivo_rows)
psv('conferencia/r11_divergencias_enfrentou.psv', ['id_unidade', 'categoria', 'ministro', 'A', 'B', 'regra', 'evidencia_A', 'fonte_A'], r11_rows)
psv('conferencia/precedentes_filtro.psv', ['id_unidade', 'ministro', 'tipo', 'sentido', 'fonte', 'destino', 'referencia'], prec_rows)
jac, nj = jaccard_filtrado()
with open(os.path.join(SAIDA, 'LOG_CONSOLIDACAO.md'), 'w', encoding='utf-8') as f:
    f.write('# Log da consolidação da Fase 4\n\nGerado por `consolidar_fase4.py` em 18/10/2026. Base: leitura A; decisões do gate (D-048) e D-049.\n\n')
    f.write(f'- Unidades: {Counter(x[5] for x in U)}\n- Questões: {Counter(x[2] for x in Q)}; categorias ativas: {Counter(x[3] for x in Q if x[2] == "ativa")}\n')
    f.write(f'- Posições: {len(P)}; voto_resultado: {Counter(x[4] for x in P)}\n- Precedentes: {dict(Counter(r[5] for r in prec_rows))}; filtro por página {"ligado" if FILTRO_PAGINA else "desligado"}; Jaccard: não recalculado aqui (sem filtro por página, vale o 0,73 de concordancia_fase4.md, que normaliza as referências)\n')
    f.write(f'- R12 dispara pela fórmula em {sum(1 for r in r12_rows if r[6] == "SIM")} de {len(r12_rows)} unidades divergentes com duas questões\n- Coerência marca × voto: {len(coer_rows)} descompassos\n- Cruzamento com motivo: {len(motivo_rows)} descompassos\n- R11: {len(r11_rows)} divergências A×B em enfrentou\n\n')
    f.write('| caso | alvo | regra | o que mudou |\n|---|---|---|---|\n')
    for c, a, r, t in LOG:
        f.write(f'| {c} | {a} | {r} | {t} |\n')
print(open(os.path.join(SAIDA, 'LOG_CONSOLIDACAO.md'), encoding='utf-8').read()[:2500])
