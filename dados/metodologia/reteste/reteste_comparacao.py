#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste-reteste da extração L1: o mesmo modelo, com o mesmo prompt, lendo o mesmo texto
de novo e às cegas, dá o mesmo resultado?

Motivo (27/09/2026): lacuna apontada pelo levantamento bibliográfico de 20/09
(`02_bibliografia/_levantamento_llm_extracao_2026-09-20.md`) e declarada como limitação
na D-035. A dupla extração A×B de agosto mede concordância entre duas execuções
simultâneas; o reteste mede se a leitura se reproduz semanas depois, com o modelo em
outra sessão. É a propriedade que a literatura chama de estabilidade intra-codificador.

Entrada : derivados/casos/_reteste/AP-*_R.json   (reextração de 27/09, claude-sonnet-5)
          derivados/casos/_dupla/AP-*_{A,B}.json (extrações de 08–09/08, claude-sonnet-5)
Saída   : metodologia/reteste/reteste_2026-09-27.md

Comparações:
  R × A  — o reteste propriamente dito: mesmo prompt, byte a byte, salvo o caminho de saída
  R × B  — referência
  A × B  — linha de base: a concordância de agosto nesses mesmos casos
Alinhamento das unidades igual ao de `concordancia_kappa.py` (réu por nome normalizado,
ou por posição quando o número de réus coincide; voto por nome do ministro).
"""
import json, glob, os, sys, unicodedata, random
from collections import defaultdict, Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))           # dados
DUPLA = os.path.join(RAIZ, "derivados", "casos", "_dupla")
RETESTE = os.path.join(RAIZ, "derivados", "casos", "_reteste")
SAIDA = os.path.join(AQUI, "reteste_2026-09-27.md")

def norm(s):
    if s is None: return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.upper().split())

ALIAS_MINISTRO = {"CARLOS BRITTO": "AYRES BRITTO", "CARLOS AYRES BRITTO": "AYRES BRITTO"}

def nome_ministro(s):
    """Chave do ministro: tira o parêntese de nome alternativo e unifica aliases.
    Sem isso, 'AYRES BRITTO (CARLOS BRITTO)' e 'CARLOS BRITTO (AYRES BRITTO)' não casam."""
    n = norm(s).split(" (")[0].strip()
    return ALIAS_MINISTRO.get(n, n)

def val(o):
    if isinstance(o, dict) and "valor" in o: return o["valor"]
    return o

def cat(v):
    if v is None: return "__NULO__"
    if isinstance(v, bool): return "Sim" if v else "Nao"
    return norm(v)

def po(p):
    return sum(1 for a, b in p if a == b) / len(p) if p else None

def kappa(p):
    n = len(p)
    if n == 0: return None
    m1 = Counter(a for a, _ in p); m2 = Counter(b for _, b in p)
    Pe = sum((m1[c] / n) * (m2[c] / n) for c in set(m1) | set(m2))
    if abs(1 - Pe) < 1e-12: return None
    return (po(p) - Pe) / (1 - Pe)

def ic(p, B=5000, semente=20260927):
    if not p: return None, None
    rnd = random.Random(semente); n = len(p); vs = []
    for _ in range(B):
        v = kappa([p[rnd.randrange(n)] for _ in range(n)])
        if v is not None: vs.append(v)
    if len(vs) < B * 0.5: return None, None
    vs.sort()
    return vs[int(0.025 * len(vs))], vs[min(int(0.975 * len(vs)), len(vs) - 1)]

CAMPOS_REU = ("resultado", "motivo", "unanime", "prescricao_pos_condenacao",
              "n_votantes", "votos_condenacao", "votos_absolvicao")
CAMPOS_VOTO = ("voto_resultado", "vencido", "ausente", "eh_relator")
CONTAGENS = {"caso.n_reus", "reu.n_votantes", "reu.votos_condenacao", "reu.votos_absolvicao"}

def comparar(X, Y, cid, pares, diverg, falt):
    def add(campo, a, b, unidade):
        if a is None and b is None:
            falt[campo] += 1; return
        ca, cb = cat(a), cat(b)
        pares[campo].append((ca, cb))
        if ca != cb: diverg.append((cid, unidade, campo, ca, cb))
    for campo in ("merito_finalizado", "multiplas_sessoes", "n_reus"):
        add(f"caso.{campo}", val(X.get("caso", {}).get(campo)), val(Y.get("caso", {}).get(campo)), "caso")
    rx, ry = X.get("reus", []), Y.get("reus", [])
    idx = {norm(val(r.get("nome"))): r for r in ry}
    for i, r in enumerate(rx):
        nome = norm(val(r.get("nome")))
        par = idx.get(nome)
        if par is None and len(rx) == len(ry): par = ry[i]
        if par is None:
            falt["reu.__sem_par__"] += 1; diverg.append((cid, nome, "reu.__sem_par__", nome, "—")); continue
        for campo in CAMPOS_REU:
            add(f"reu.{campo}", val(r.get(campo)), val(par.get(campo)), nome)
    vx, vy = X.get("votos", []), Y.get("votos", [])
    idxv = {nome_ministro(val(v.get("ministro"))): v for v in vy}
    for v in vx:
        nome = nome_ministro(val(v.get("ministro")))
        par = idxv.get(nome)
        if par is None:
            falt["voto.__sem_par__"] += 1; diverg.append((cid, nome, "voto.__sem_par__", nome, "—")); continue
        for campo in CAMPOS_VOTO:
            add(f"voto.{campo}", val(v.get(campo)), val(par.get(campo)), nome)

def carregar(p):
    return json.load(open(p, encoding="utf-8"))

casos = sorted(os.path.basename(f).split("_")[0] for f in glob.glob(os.path.join(RETESTE, "AP-*_R.json")))
if not casos:
    sys.exit("Nenhum arquivo de reteste em " + RETESTE)

resultados = {}
for rotulo, (sx, sy) in {"R × A": ("R", "A"), "R × B": ("R", "B"), "A × B": ("A", "B")}.items():
    pares, diverg, falt = defaultdict(list), [], Counter()
    for cid in casos:
        cam = {"R": os.path.join(RETESTE, f"{cid}_R.json"),
               "A": os.path.join(DUPLA, f"{cid}_A.json"),
               "B": os.path.join(DUPLA, f"{cid}_B.json")}
        if not (os.path.exists(cam[sx]) and os.path.exists(cam[sy])): continue
        comparar(carregar(cam[sx]), carregar(cam[sy]), cid, pares, diverg, falt)
    resultados[rotulo] = (pares, diverg, falt)

def fmt(x, c=3):
    return "—" if x is None else f"{x:.{c}f}".replace(".", ",")

out = ["# Teste-reteste da extração L1\n",
       "> Gerado por `metodologia/reteste/reteste_comparacao.py`. Reextração cega em 27/09/2026 com "
       "`claude-sonnet-5` e o prompt original da extração A de cada caso (ver `README.md` desta pasta).\n",
       f"\n**Casos:** {', '.join(casos)}.\n"]

out.append("\n## Resumo\n")
out.append("| Comparação | Pares | Concordância bruta | Divergências |")
out.append("|---|---:|---:|---:|")
for rot, (pares, diverg, _) in resultados.items():
    n = sum(len(p) for p in pares.values())
    ok = sum(sum(1 for a, b in p if a == b) for p in pares.values())
    out.append(f"| {rot} | {n} | {ok/n*100:.1f}% | {len(diverg)} |" if n else f"| {rot} | 0 | — | — |")

pares, diverg, falt = resultados["R × A"]
out.append("\n## R × A por campo (o reteste)\n")
out.append("| Campo | Pares | Concordância bruta | κ de Cohen | IC95% de κ |")
out.append("|---|---:|---:|---:|:--:|")
for campo in sorted(pares, key=lambda c: (-len(pares[c]), c)):
    p = pares[campo]
    if campo in CONTAGENS:
        k, faixa = "n/a (contagem)", "—"
    else:
        kv = kappa(p); lo, hi = ic(p)
        k = fmt(kv) if kv is not None else "**indefinido**"
        faixa = "—" if lo is None else f"[{fmt(lo,2)}; {fmt(hi,2)}]"
    out.append(f"| `{campo}` | {len(p)} | {po(p)*100:.1f}% | {k} | {faixa} |")

for rot in ("R × A", "A × B"):
    _, dv, _ = resultados[rot]
    out.append(f"\n## Divergências {rot}, uma a uma\n")
    if not dv:
        out.append("Nenhuma.\n"); continue
    out.append(f"| Caso | Unidade | Campo | {rot.split(' × ')[0]} | {rot.split(' × ')[1]} |")
    out.append("|---|---|---|---|---|")
    for cid, un, campo, a, b in dv:
        out.append(f"| {cid} | {un} | `{campo}` | {a} | {b} |")

if falt:
    out.append("\n**Descartes em R × A:** " + "; ".join(f"`{k}`: {v}" for k, v in falt.most_common()) + ".\n")
out.append("\nIC95% por reamostragem das unidades (5.000 repetições, semente 20260927). Campos de contagem "
           "são comparados por coincidência exata.\n")
open(SAIDA, "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
