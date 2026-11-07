#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Esqueleto das unidades de análise da Fase 4: uma linha por réu × imputação.

Motivo (27/09/2026): a D-033 fixa a unidade da Fase 4 em réu × fato. Esta tabela é o
denominador, ou seja, o que o extrator da fundamentação terá de cobrir, montado só com o
que o banco já tem (`crimes` de cada réu nos JSONs). Não classifica nada. A coluna
`questao_decisiva` sai vazia, à espera do codebook do Felipe.

Imputação ≠ fato. Um mesmo artigo pode cobrir vários fatos (AP-1025: "fato UTC" e
"fatos DVBR..."), e a AP-470 organiza por item da denúncia. Por isso a tabela traz também
os rótulos de `fato` já usados em `3_votos.psv` para o réu. Desdobrar ou juntar
unidades é decisão da Fase 4, registrada caso a caso.

Entrada : derivados/casos/AP-*.json, derivados/2_casos_reus.psv, derivados/3_votos.psv
Saída   : metodologia/fase4/unidades_reu_fato.psv
"""
import json, glob, os, csv, unicodedata
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
DER = os.path.join(RAIZ, "derivados")
SAIDA = os.path.join(AQUI, "unidades_reu_fato.psv")

def norm(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    return " ".join("".join(c for c in s if not unicodedata.combining(c)).upper().split())

def val(o):
    return o["valor"] if isinstance(o, dict) and "valor" in o else o

def limpa(s):
    return " ".join(str(s or "").replace("|", "/").split())

reus_banco = defaultdict(dict)                       # id_caso -> nome_norm -> linha
for r in csv.DictReader(open(os.path.join(DER, "2_casos_reus.psv"), encoding="utf-8"), delimiter="|"):
    reus_banco[r["id_caso"]][norm(r["nome_reu"])] = r
fatos_votos = defaultdict(set)                       # id_caso_reu -> rótulos de fato
for v in csv.DictReader(open(os.path.join(DER, "3_votos.psv"), encoding="utf-8"), delimiter="|"):
    if v["fato"]: fatos_votos[v["id_caso_reu"]].add(v["fato"])

cols = ["id_unidade", "id_caso", "id_caso_reu", "nome_reu", "n_imputacao", "artigo", "diploma",
        "evidencia_imputacao", "resultado_inciso_banco", "fatos_em_3_votos", "resultado_reu_banco",
        "motivo_reu_banco", "unanime_reu_banco", "questao_decisiva", "obs"]
linhas, fora = [], []
for path in sorted(glob.glob(os.path.join(DER, "casos", "AP-*.json"))):
    d = json.load(open(path, encoding="utf-8"))
    cid = d["id_caso"]
    for reu in d["reus"]:
        nome = val(reu["nome"])
        b = reus_banco[cid].get(norm(nome))
        if b is None:
            fora.append((cid, nome)); continue      # réu fora de 2_casos_reus (D-020)
        for i, c in enumerate(reu.get("crimes") or [], 1):
            linhas.append({
                "id_unidade": f"{b['id_caso_reu']}-I{i:02d}", "id_caso": cid,
                "id_caso_reu": b["id_caso_reu"], "nome_reu": b["nome_reu"], "n_imputacao": i,
                "artigo": limpa(c.get("artigo")), "diploma": limpa(c.get("diploma")),
                "evidencia_imputacao": limpa(c.get("evidencia"))[:300],
                "resultado_inciso_banco": limpa(c.get("resultado_inciso")),
                "fatos_em_3_votos": " ; ".join(sorted(fatos_votos.get(b["id_caso_reu"], []))),
                "resultado_reu_banco": b["resultado"], "motivo_reu_banco": b["motivo"],
                "unanime_reu_banco": b["unanime"], "questao_decisiva": "", "obs": ""})

with open(SAIDA, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter="|", lineterminator="\n")
    w.writeheader(); w.writerows(linhas)

por_caso = defaultdict(int)
for l in linhas: por_caso[l["id_caso"]] += 1
print(f"{len(linhas)} unidades, {len({l['id_caso_reu'] for l in linhas})} réus, {len(por_caso)} casos")
print("por caso:", dict(sorted(por_caso.items(), key=lambda x: -x[1])))
print(f"réus do JSON fora de 2_casos_reus (D-020): {len(fora)} ->", fora)
