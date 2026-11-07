#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Consolida os mapas estruturais de votos (mapa_votos/AP-*.psv) e confere contra o banco.

Para cada caso: (1) todo ministro que votou segundo 3_votos.psv aparece no mapa?
(2) dos votos `sem_evidencia` e `deducao D-004` do banco, quantos têm peça com texto
próprio localizada (tem_texto = Sim)? Isso dimensiona o subproduto da D-034;
(3) todas as linhas DIVERGE:.
A AP-470 tem só índice de peças e entra à parte.
Saída: mapa_votos/_consolidado.psv e mapa_votos/_consolidacao.md
"""
import csv, glob, os, unicodedata
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
MAPA = os.path.join(AQUI, "mapa_votos")
VOTOS = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "derivados", "3_votos.psv")

def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    n = " ".join("".join(c for c in s if not unicodedata.combining(c)).upper().split())
    return {"CARLOS BRITTO": "AYRES BRITTO", "CARLOS AYRES BRITTO": "AYRES BRITTO"}.get(n, n)

banco = defaultdict(lambda: defaultdict(set))          # caso -> ministro -> {fonte_voto}
for v in csv.DictReader(open(VOTOS, encoding="utf-8"), delimiter="|"):
    if v["voto_resultado"] in ("Condena", "Absolve"):
        banco[v["id_caso"]][norm(v["ministro"])].add(v["fonte_voto"])

todas, rel = [], ["# Consolidação do mapa de votos\n",
    "| Caso | Linhas | Votantes no banco | Sem linha no mapa | Votos sem_evidencia/deduzidos | …com texto próprio localizado | DIVERGE |",
    "|---|---:|---:|---|---:|---:|---:|"]
diverg = []
tot = defaultdict(int)
for f in sorted(glob.glob(os.path.join(MAPA, "AP-*.psv"))):
    caso = os.path.basename(f)[:-4]
    try:
        linhas = list(csv.DictReader(open(f, encoding="utf-8"), delimiter="|"))
    except Exception as e:
        rel.append(f"| {caso} | erro de leitura: {e} | | | | | |"); continue
    todas += linhas
    mapa_min = defaultdict(set)
    for l in linhas:
        for m in (l.get("ministro") or "").split(";"):
            if not m.strip(): continue
            t = (l.get("tem_texto") or "").strip()
            # só peça de voto conta como "texto próprio localizado"; debate e aparte não
            if l.get("peca") not in ("voto", "voto_aditamento", "confirmacao_voto") and t == "Sim": t = "Sim_fora_de_voto"
            mapa_min[norm(m)].add(t)
        if "DIVERGE:" in (l.get("obs") or ""):
            diverg.append(f"| {caso} | {l.get('ministro')} | {l.get('peca')} | pp. {l.get('pag_ini')}–{l.get('pag_fim')} | {l.get('obs')} |")
    votantes = banco.get(caso, {})
    faltam = sorted(m for m in votantes if m not in mapa_min)
    fracos = [m for m, fs in votantes.items() if fs & {"sem_evidencia", "deduzido", "deducao D-004"}]
    achados = [m for m in fracos if "Sim" in mapa_min.get(m, set())]
    nd = sum(1 for l in linhas if "DIVERGE:" in (l.get("obs") or ""))
    if caso == "AP-470":
        rel.append(f"| AP-470 | {len(linhas)} | {len(votantes)} | (índice de peças: não se aplica) | {len(fracos)} | — | {nd} |"); continue
    rel.append(f"| {caso} | {len(linhas)} | {len(votantes)} | {', '.join(faltam) or '—'} | {len(fracos)} | {len(achados)} | {nd} |")
    tot["fracos"] += len(fracos); tot["achados"] += len(achados); tot["faltam"] += len(faltam)
rel.append(f"\n**Totais, sem a AP-470:** ministros sem linha no mapa = {tot['faltam']}; ministros com voto fraco no banco (sem evidência ou deduzido) = {tot['fracos']}, dos quais {tot['achados']} têm peça com texto próprio localizada.\n")
rel.append("A contagem é por ministro × caso, e não por voto × réu: é o que o mapa localiza. “Texto próprio localizado” = ao menos uma peça do tipo voto com `tem_texto = Sim`; é um **limite superior**, porque um voto só sobre dosimetria ou questão de ordem também conta. As notas de cada caso detalham.\n")
rel += ["\n## Linhas DIVERGE\n", "| Caso | Ministro | Peça | Páginas | Observação |", "|---|---|---|---|---|"] + (diverg or ["| — | | | | |"])
if todas:
    with open(os.path.join(MAPA, "_consolidado.psv"), "w", encoding="utf-8", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(todas[0].keys()), delimiter="|", lineterminator="\n", extrasaction="ignore")
        w.writeheader(); w.writerows(todas)
open(os.path.join(MAPA, "_consolidacao.md"), "w", encoding="utf-8").write("\n".join(rel))
print("\n".join(rel))
