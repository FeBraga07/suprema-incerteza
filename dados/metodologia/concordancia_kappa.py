#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Concordância entre as duas extrações independentes (A e B), corrigida por chance.

Motivo (20/09/2026): o projeto vinha reportando concordância como percentual bruto
(99,3%). A literatura de confiabilidade entre codificadores (COHEN, 1960; ARTSTEIN &
POESIO, 2008; KRIPPENDORFF, 2004) mostra que o percentual bruto superestima a
confiabilidade quando uma categoria domina — o chamado paradoxo do kappa. Este script
recalcula a mesma concordância com dois coeficientes corrigidos por chance, sobre
exatamente os mesmos arquivos, sem coleta nova.

Entrada : dados/derivados/casos/_dupla/AP-*_{A,B}.json  (15 casos, 30 arquivos)
Saída   : dados/metodologia/concordancia_kappa_2026-09-20.md

Alinhamento das unidades de observação:
  - caso  : o próprio id_caso
  - réu   : nome normalizado (sem acento, maiúsculas); se não casar, por posição
            quando A e B trazem o mesmo número de réus
  - voto  : nome do ministro normalizado
Pares em que um dos lados não tem o campo são descartados e contados à parte.
"""
import json, glob, os, unicodedata, random
from collections import defaultdict, Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUPLA = os.path.join(RAIZ, "derivados", "casos", "_dupla")
SAIDA = os.path.join(RAIZ, "metodologia", "concordancia_kappa_2026-09-20.md")

def norm(s):
    if s is None: return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.upper().split())

def val(o):
    """Campo do contrato de 4 partes: {valor, evidencia, fonte, confianca} -> valor."""
    if isinstance(o, dict) and "valor" in o: return o["valor"]
    return o

def cat(v):
    """Normaliza o valor para rótulo categórico comparável."""
    if v is None: return "__NULO__"
    if isinstance(v, bool): return "Sim" if v else "Nao"
    return norm(v)

# ---------- coeficientes ----------
def po(pares):
    return sum(1 for a, b in pares if a == b) / len(pares) if pares else None

def kappa_cohen(pares):
    n = len(pares)
    if n == 0: return None, None
    Po = po(pares)
    m1 = Counter(a for a, _ in pares); m2 = Counter(b for _, b in pares)
    Pe = sum((m1[c]/n) * (m2[c]/n) for c in set(m1) | set(m2))
    if abs(1 - Pe) < 1e-12: return None, Pe   # indefinido: uma só categoria
    return (Po - Pe) / (1 - Pe), Pe

def alpha_krippendorff(pares):
    """Alfa nominal, 2 codificadores, dados completos (matriz de coincidências)."""
    n_un = len(pares)
    if n_un == 0: return None
    o = defaultdict(float)
    for a, b in pares:          # cada unidade tem m=2 valores -> peso 1/(m-1)=1
        o[(a, b)] += 1.0
        o[(b, a)] += 1.0
    cats = sorted({c for par in o for c in par})
    nc = {c: sum(o[(c, k)] for k in cats) for c in cats}
    n = sum(nc.values())
    if n <= 1: return None
    Do = sum(o[(c, k)] for c in cats for k in cats if c != k) / n
    De = sum(nc[c] * nc[k] for c in cats for k in cats if c != k) / (n * (n - 1))
    if De == 0: return None
    return 1 - Do / De

def ic_bootstrap(pares, fn, B=5000, semente=20260920):
    """IC95% percentílico por reamostragem das unidades. Com n pequeno o kappa
    pontual diz pouco; o intervalo diz quanto."""
    if not pares: return None, None
    rnd = random.Random(semente); n = len(pares); vals = []
    for _ in range(B):
        am = [pares[rnd.randrange(n)] for _ in range(n)]
        v = fn(am)
        if isinstance(v, tuple): v = v[0]
        if v is not None: vals.append(v)
    if len(vals) < B * 0.5: return None, None   # indefinido com frequencia -> nao reporta
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[min(int(0.975 * len(vals)), len(vals) - 1)]

# ---------- coleta dos pares ----------
pares = defaultdict(list)     # campo -> [(a,b), ...]
faltantes = Counter()
casos = sorted({os.path.basename(f).split("_")[0] for f in glob.glob(os.path.join(DUPLA, "AP-*_A.json"))})
# O relatório é o de 20/09/2026 e cobre os 15 casos então com dupla extração. A AP 307,
# acrescentada em 18/10, tem votos por réu x fato, e o pareamento por ministro deste script
# não a trata (a concordância dela está em fase4/ e na seção 3.4 do texto). Sem este filtro,
# rodar o script de novo sobrescrevia o relatório datado com outro universo (D-061, 07/11/2026).
CASOS_2026_09_20 = {"AP-1025", "AP-1032", "AP-348", "AP-365", "AP-375", "AP-396", "AP-416", "AP-426",
                    "AP-430", "AP-465", "AP-503", "AP-508", "AP-527", "AP-940", "AP-973"}
casos = [c for c in casos if c in CASOS_2026_09_20]

def add(campo, a, b):
    if a is None and b is None:
        faltantes[campo] += 1; return
    pares[campo].append((cat(a), cat(b)))

for cid in casos:
    A = json.load(open(os.path.join(DUPLA, f"{cid}_A.json"), encoding="utf-8"))
    B = json.load(open(os.path.join(DUPLA, f"{cid}_B.json"), encoding="utf-8"))

    for campo in ("merito_finalizado", "multiplas_sessoes"):
        add(f"caso.{campo}", val(A.get("caso", {}).get(campo)), val(B.get("caso", {}).get(campo)))
    add("caso.n_reus", val(A.get("caso", {}).get("n_reus")), val(B.get("caso", {}).get("n_reus")))

    # --- réus ---
    ra, rb = A.get("reus", []), B.get("reus", [])
    idx = {norm(val(r.get("nome"))): r for r in rb}
    for i, r in enumerate(ra):
        nome = norm(val(r.get("nome")))
        par = idx.get(nome)
        if par is None and len(ra) == len(rb):
            par = rb[i]                      # mesmo número de réus: alinha por posição
        if par is None:
            faltantes["reu.__sem_par__"] += 1; continue
        for campo in ("resultado", "motivo", "unanime", "prescricao_pos_condenacao",
                      "n_votantes", "votos_condenacao", "votos_absolvicao"):
            add(f"reu.{campo}", val(r.get(campo)), val(par.get(campo)))

    # --- votos (no L1 a lista é por ministro, ainda sem o fan-out por réu x fato) ---
    va, vb = A.get("votos", []), B.get("votos", [])
    idxv = {norm(val(v.get("ministro"))): v for v in vb}
    for v in va:
        par = idxv.get(norm(val(v.get("ministro"))))
        if par is None:
            faltantes["voto.__sem_par__"] += 1; continue
        for campo in ("voto_resultado", "vencido", "ausente", "eh_relator"):
            add(f"voto.{campo}", val(v.get(campo)), val(par.get(campo)))

# ---------- relatório ----------
CONTAGENS = {"caso.n_reus", "reu.n_votantes", "reu.votos_condenacao", "reu.votos_absolvicao"}

linhas = []
for campo in sorted(pares):
    p = pares[campo]
    k, Pe = kappa_cohen(p)
    a = alpha_krippendorff(p)
    ncat = len({c for par in p for c in par})
    maior = Counter(c for par in p for c in par).most_common(1)[0]
    prev = maior[1] / (2 * len(p))
    lo, hi = (None, None) if campo in CONTAGENS else ic_bootstrap(p, kappa_cohen)
    linhas.append(dict(campo=campo, n=len(p), po=po(p), k=k, a=a, ncat=ncat,
                       prev=prev, maior=maior[0], conta=campo in CONTAGENS, lo=lo, hi=hi))

tot = sum(l["n"] for l in linhas)
conc = sum(l["n"] * l["po"] for l in linhas) / tot

def fmt(x, casas=3):
    return "—" if x is None else f"{x:.{casas}f}".replace(".", ",")

out = []
out.append("# Concordância entre extrações independentes, corrigida por chance\n")
out.append("> Gerado por `concordancia_kappa.py` em 20/09/2026, sessão `d7aca838`, modelo `claude-opus-5`.\n"
           "> Entrada: os 30 arquivos de dupla extração em `derivados/casos/_dupla/` (15 casos). **Nenhum dado novo foi coletado**: é recálculo sobre o material de 08–09/08/2026.\n")
out.append(f"\n**Unidades comparadas:** {tot} pares campo a campo, em {len(casos)} casos "
           f"({', '.join(casos)}).\n\n**Concordância bruta global: {conc*100:.1f}%**.\n")
out.append("\n## Por campo\n")
out.append("| Campo | Pares | Concordância bruta | κ de Cohen | IC95% de κ (bootstrap) | α de Krippendorff | Categorias | Prevalência da categoria modal |")
out.append("|---|---:|---:|---:|:--:|---:|---:|---:|")
for l in sorted(linhas, key=lambda x: (-x["n"], x["campo"])):
    k = "n/a (contagem)" if l["conta"] else (fmt(l["k"]) if l["k"] is not None else "**indefinido**")
    a = "n/a (contagem)" if l["conta"] else fmt(l["a"])
    ic = "—" if l["lo"] is None else f"[{fmt(l['lo'],2)}; {fmt(l['hi'],2)}]"
    out.append(f"| `{l['campo']}` | {l['n']} | {l['po']*100:.1f}% | {k} | {ic} | {a} | {l['ncat']} | {l['prev']*100:.0f}% (`{l['maior']}`) |")
out.append("\nIC95% por reamostragem das unidades (5.000 repetições, semente fixa 20260920). Onde o kappa "
           "é indefinido em boa parte das reamostras — o que ocorre quando a categoria modal domina —, o intervalo não é reportado.\n")
out.append("\nCampos de contagem (`n_reus`, `n_votantes`, `votos_condenacao`, `votos_absolvicao`) são numéricos: "
           "kappa e alfa nominais não se aplicam a eles, e o que se reporta é coincidência exata.\n")
if faltantes:
    out.append("\n**Descartes:** " + "; ".join(f"`{k}`: {v}" for k, v in faltantes.most_common()) + ".\n")
open(SAIDA, "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
