#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Concordância entre duas leituras independentes (A/B) da Fase 4, campo a campo.

Escrito em 27/09/2026, antes do codebook, e por isso não conhece os valores de
`questao_decisiva` nem de `posicao`: trata qualquer campo como categórico. Mesmos
coeficientes da D-035 (κ de Cohen com IC95% por reamostragem) e do reteste (D-037).

Uso: python3 concordancia_fase4.py DIR_A DIR_B [SAIDA.md] [--outra PSV]
     DIR_A/DIR_B contêm AP-XXX.json no formato de CONTRATO_FASE4 (§2–§4):
     {"id_caso": ..., "unidades": [{"id_unidade": ..., <campo>: {"valor": ...}, ...,
       "posicoes": [{"ministro": ..., <campo>: {"valor": ...}}],
       "precedentes": [{"ministro": ..., "tipo": ..., "referencia": ...}]}]}

Unidade: alinhada por `id_unidade`. Posição: por (id_unidade, ministro).
Precedentes: concordância de conjunto (Jaccard) por unidade sobre (ministro, tipo, referência).
Campos de texto livre (sufixos _formulacao, fundamento_proprio, obs) não são comparados.

Adaptado em 12/10/2026 ao CONTRATO_FASE4 v1 (D-044), que aninha questoes -> posicoes:
cada unidade gera (i) a unidade-base, com `questoes_conjunto` (quais questões) e
`questoes_principais` (quais marcadas principal) como campos categóricos, e (ii) uma
pseudo-unidade por questão, `id_unidade::questao`, com os campos da questão e as posições
dos ministros nela. Questão presente só em A ou só em B aparece como "sem par".

Corrigido em 13/10/2026 (sessão `fb1ad956`, autorizado pelo Felipe): questões repetidas
da mesma categoria na mesma unidade ganham sufixo (`::outra#2`), e a principal vem primeiro.

Ampliado em 13/10/2026 (sessão `2cd99bbf`, D-046 item 2, opção (ii) do Felipe): com
`--outra extracao/lote/outra_polaridade_pareamento.psv`, as perguntas `outra` (i) são
pareadas A↔B pelo conteúdo, conforme a coluna `par` do arquivo, e não pela ordem no JSON
(em AP-365-R01-I02 as duas leituras fizeram as mesmas perguntas em ordem trocada); e
(ii) têm a direção alinhada: onde o "sim" favorece a defesa, `resposta_tribunal` e
`posicao` são invertidos (sim↔nao) antes da comparação, para que "sim" signifique sempre
"o elemento da acusação está presente", como em `dolo` e `concorreu`. Os JSONs não mudam.
O relatório traz as duas medidas: direção alinhada (oficial) e como lida.
"""
import json, glob, os, sys, random, unicodedata
from collections import Counter, defaultdict

LIVRES = ("_formulacao", "formulacao", "fundamento_proprio", "obs", "ajuste_unidade", "questao_outra_descricao", "posicao_detalhe", "fato")  # `fato`: rótulo livre fora do contrato, só na A·AP-1025
CHAVES = {"id_unidade", "posicoes", "precedentes", "ministro", "questoes"}

def norm(s):
    s = unicodedata.normalize("NFKD", str(s if s is not None else "__NULO__"))
    return " ".join("".join(c for c in s if not unicodedata.combining(c)).upper().split())

def val(o):
    return o.get("valor") if isinstance(o, dict) else o

def kappa(p):
    n = len(p)
    if not n: return None
    po = sum(a == b for a, b in p) / n
    m1, m2 = Counter(a for a, _ in p), Counter(b for _, b in p)
    pe = sum(m1[c] / n * m2[c] / n for c in set(m1) | set(m2))
    return None if abs(1 - pe) < 1e-12 else (po - pe) / (1 - pe)

def ic(p, B=5000, semente=20260927):
    rnd = random.Random(semente); vs = []
    for _ in range(B):
        k = kappa([p[rnd.randrange(len(p))] for _ in p])
        if k is not None: vs.append(k)
    if len(vs) < B / 2: return None
    vs.sort(); return vs[int(.025 * len(vs))], vs[min(int(.975 * len(vs)), len(vs) - 1)]

def comparaveis(d):
    return {k: v for k, v in d.items() if k not in CHAVES and not k.endswith(LIVRES) and k not in LIVRES}

INV = {"sim": "nao", "nao": "sim"}

def ler_outra(caminho):
    """leitura|id_unidade|indice|sim_favorece|par|... -> {(leitura, id_unidade, indice): (sim_favorece, par)}"""
    out = {}
    for i, l in enumerate(open(caminho, encoding="utf-8")):
        c = l.rstrip("\n").split("|")
        if i and len(c) > 4: out[(c[0], c[1], int(c[2]))] = (c[3], c[4])
    return out

def inverter(q):
    """Cópia da questão com sim↔nao em resposta_tribunal e nas posições."""
    q = json.loads(json.dumps(q))
    for alvo in [q] + q.get("posicoes", []):
        campo = "resposta_tribunal" if alvo is q else "posicao"
        o = alvo.get(campo)
        if isinstance(o, dict) and o.get("valor") in INV: o["valor"] = INV[o["valor"]]
        elif isinstance(o, str) and o in INV: alvo[campo] = INV[o]
    return q

def achatar(u, leitura=None, outra=None, alinhar=False):
    """Contrato v1: unidade-base + uma pseudo-unidade por questão (D-044)."""
    qs = u.get("questoes")
    if qs is None:
        return {u["id_unidade"]: u}
    base = {k: v for k, v in u.items() if k != "questoes"}
    nomes = [norm(val(q.get("questao_decisiva"))) for q in qs]
    base["questoes_conjunto"] = {"valor": "+".join(sorted(nomes))}
    base["questoes_principais"] = {"valor": "+".join(sorted(n for n, q in zip(nomes, qs) if norm(val(q.get("principal"))) == "SIM"))}
    out = {u["id_unidade"]: base}
    # Duas questões da mesma categoria (p. ex., duas `outra`) tinham o mesmo id e a segunda
    # sobrescrevia a primeira (corrigido em 13/10/2026). Agora: dentro da categoria, a principal
    # vem antes e o resto segue a ordem do JSON; a segunda recebe o sufixo #2, e assim por diante.
    ordem = sorted(range(len(qs)), key=lambda i: (nomes[i], norm(val(qs[i].get("principal"))) != "SIM", i))
    vistos = Counter()
    for i in ordem:
        n, q = nomes[i], qs[i]
        vistos[n] += 1
        sufixo = f"#{vistos[n]}" if vistos[n] > 1 else ""
        marca = (outra or {}).get((leitura, u["id_unidade"], i)) if n == "OUTRA" else None
        if marca:
            pol, par = marca
            if par not in ("", "n/a"):   # pareada por conteúdo: chave comum = índice na leitura A
                sufixo = f"@A{i if leitura == 'A' else par}"
            elif par == "":               # sem par na outra leitura
                sufixo = f"@{leitura}{i}"
            if alinhar and pol == "defesa": q = inverter(q)
        pu = {k: v for k, v in q.items() if k != "questao_decisiva"}
        pu["id_unidade"] = f"{u['id_unidade']}::{n.lower()}" + sufixo
        pu.setdefault("precedentes", [])
        out[pu["id_unidade"]] = pu
    return out

def carregar(pasta, leitura=None, outra=None, alinhar=False):
    out = {}
    for f in glob.glob(os.path.join(pasta, "AP-*.json")):
        for u in json.load(open(f, encoding="utf-8")).get("unidades", []):
            out.update(achatar(u, leitura, outra, alinhar))
    return out

def comparar(A, B):
    pares, diverg, jacc = defaultdict(list), [], []
    # "Sem par" só nos casos lidos pelas duas leituras; os de leitura única não são divergência.
    caso = lambda uid: uid.split("-R")[0]
    comuns = {caso(u) for u in A} & {caso(u) for u in B}
    so_a = sorted(u for u in set(A) - set(B) if caso(u) in comuns)
    so_b = sorted(u for u in set(B) - set(A) if caso(u) in comuns)
    for uid in sorted(set(A) & set(B)):
        ua, ub = A[uid], B[uid]
        for campo in sorted(set(comparaveis(ua)) | set(comparaveis(ub))):
            a, b = norm(val(ua.get(campo))), norm(val(ub.get(campo)))
            pares["unidade." + campo].append((a, b))
            if a != b: diverg.append((uid, "", campo, a, b))
        pa = {norm(p["ministro"]): p for p in ua.get("posicoes", [])}
        pb = {norm(p["ministro"]): p for p in ub.get("posicoes", [])}
        for m in sorted(set(pa) | set(pb)):
            if m not in pa or m not in pb:
                diverg.append((uid, m, "posicao.__sem_par__", "A" if m in pa else "—", "B" if m in pb else "—")); continue
            for campo in sorted(set(comparaveis(pa[m])) | set(comparaveis(pb[m]))):
                a, b = norm(val(pa[m].get(campo))), norm(val(pb[m].get(campo)))
                pares["posicao." + campo].append((a, b))
                if a != b: diverg.append((uid, m, campo, a, b))
        ch = lambda u: {(norm(p.get("ministro")), norm(p.get("tipo")), norm(p.get("referencia"))) for p in u.get("precedentes", [])}
        sa, sb = ch(ua), ch(ub)
        jacc.append(1.0 if not (sa | sb) else len(sa & sb) / len(sa | sb))
    return pares, diverg, jacc, so_a, so_b

def main(dir_a, dir_b, saida, arq_outra=None):
    outra = ler_outra(arq_outra) if arq_outra else None
    A, B = carregar(dir_a, "A", outra, alinhar=bool(outra)), carregar(dir_b, "B", outra, alinhar=bool(outra))
    pares, diverg, jacc, so_a, so_b = comparar(A, B)
    f = lambda x, c=3: "—" if x is None else f"{x:.{c}f}".replace(".", ",")
    out = [f"# Concordância A × B — Fase 4\n", f"Unidades e questões em comum: {len(set(A) & set(B))} · sem par, nos casos com dupla leitura: só em A {len(so_a)}, só em B {len(so_b)}\n",
           "| Campo | Pares | Concordância bruta | κ | IC95% |", "|---|---:|---:|---:|:--:|"]
    for campo in sorted(pares, key=lambda c: (-len(pares[c]), c)):
        p = pares[campo]; k = kappa(p); faixa = ic(p) if k is not None else None
        out.append(f"| `{campo}` | {len(p)} | {sum(a == b for a, b in p) / len(p) * 100:.1f}% | "
                   f"{f(k) if k is not None else '**indefinido**'} | {'—' if not faixa else f'[{f(faixa[0],2)}; {f(faixa[1],2)}]'} |")
    if outra:
        pc, _, _, _, _ = comparar(carregar(dir_a, "A", outra), carregar(dir_b, "B", outra))
        out.append("\n**Direção das perguntas `outra`.** A tabela acima usa a direção alinhada (D-046, item 2). "
                   "Como lida, sem inverter:\n\n| Campo | Concordância bruta | κ |\n|---|---:|---:|")
        for campo in ("posicao.posicao", "unidade.resposta_tribunal"):
            if pc.get(campo):
                p = pc[campo]; k = kappa(p)
                out.append(f"| `{campo}` | {sum(a == b for a, b in p) / len(p) * 100:.1f}% | {f(k) if k is not None else '—'} |")
    if jacc:
        out.append(f"\n**Precedentes:** Jaccard médio por unidade = {f(sum(jacc) / len(jacc))} ({len(jacc)} unidades).\n")
    out.append("\n## Divergências (para o gate)\n\n| Unidade | Ministro | Campo | A | B |\n|---|---|---|---|---|")
    out += [f"| {u} | {m} | `{c}` | {a} | {b} |" for u, m, c, a, b in diverg] or ["| — | | | | |"]
    if so_a or so_b:
        out.append(f"\n**Unidades sem par** (desdobramento ou junção divergente): só A {so_a}; só B {so_b}\n")
    open(saida, "w", encoding="utf-8").write("\n".join(out)); print("\n".join(out))

if __name__ == "__main__":
    args = sys.argv[1:]
    arq_outra = None
    if "--outra" in args:
        j = args.index("--outra"); arq_outra = args[j + 1]; del args[j:j + 2]
    if len(args) < 2: sys.exit(__doc__)
    main(args[0], args[1], args[2] if len(args) > 2 else "concordancia_fase4.md", arq_outra)
