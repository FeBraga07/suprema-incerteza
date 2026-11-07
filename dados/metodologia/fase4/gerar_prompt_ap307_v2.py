#!/usr/bin/env python3
"""Gera os prompts A e B da Fase 4 para a AP-307 (D-051) a partir de PROMPT_FASE4_v2.md.

Mesma montagem de gerar_prompts_lote.py (unidades, votos do banco, mapa), com uma diferença:
as unidades chegam desdobradas por episódio (R14, codebook v2), uma por fato de 3_votos,
porque o banco já separa os três episódios do art. 317 para Collor e PC Farias.
Uso: python3 dados/metodologia/fase4/gerar_prompt_ap307_v2.py
"""
import csv, os, re
from collections import defaultdict, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
F4 = os.path.join(ROOT, "dados/metodologia/fase4")
CASO = "AP-307"

corpo = open(os.path.join(F4, "PROMPT_FASE4_v2.md"), encoding="utf-8").read()
corpo = corpo.split("=====INÍCIO=====\n", 1)[1].split("\n=====FIM=====", 1)[0]
us = [u for u in csv.DictReader(open(os.path.join(F4, "unidades_reu_fato.psv"), encoding="utf-8"), delimiter="|") if u["id_caso"] == CASO]
votos = defaultdict(lambda: defaultdict(list))
for v in csv.DictReader(open(os.path.join(ROOT, "dados/derivados/3_votos.psv"), encoding="utf-8"), delimiter="|"):
    if v["id_caso"] == CASO:
        votos[v["id_caso_reu"]][v["fato"]].append(v)
linhas_u, linhas_v = [], []
for u in us:
    fatos = list(votos[u["id_caso_reu"]])
    fatos.sort(key=lambda f: ("Mercedes" not in f, "VASP" not in f))   # ordem fixa: Mercedes, VASP, Marcelo Ribeiro
    for k, f in enumerate(fatos):
        uid = u["id_unidade"] + ("abc"[k] if len(fatos) > 1 else "")
        orig = f" (desdobrada de `{u['id_unidade']}`, R14)" if len(fatos) > 1 else ""
        linhas_u.append(f"  - `{uid}`{orig}: {u['nome_reu']}, imputação {u['n_imputacao']}: {u['artigo']} ({u['diploma']}); "
                        f"fato: **{f}**. Escopo Levcovitz: **Sim**")
        lst = [f"{v['ministro']}: {v['voto_resultado']}" for v in votos[u["id_caso_reu"]][f]]
        linhas_v.append(f"  - {uid} {u['nome_reu']} — {f}: {len(lst)} ministros. " + "; ".join(lst))
extra = (f"\n- **Mapa de páginas das peças (permitido, só estrutura):** `{os.path.join(F4, 'mapa_votos/AP-307.psv')}`. Diz onde começa e termina "
         "cada voto e quais réus ele abrange. Use para navegar; ele não contém categoria. Não abra o arquivo `_notas.md` ao lado.")
extra += ("\n- **AP-307 (756 pp., 1994, OCR):** acórdão digitalizado; o OCR fragmenta linhas pela diagramação em colunas. Na dúvida sobre uma "
          "palavra decisiva, confira no PDF (`dados/corpus/pdf/AP-307.pdf`, mesma página). A ata do julgamento também está, limpa, em "
          "`dados/brutos/AP-307_ata_indice_sjur157761.txt` (pode abrir). O processo julga outros crimes e outros réus (arts. 299, 305, 343 e 344): "
          "fora das unidades, não preencha. Use `unidade_origem` e `fato` como dados na lista de unidades; em `unidade_origem` da unidade de "
          "Cláudio Vieira repita o próprio id.")
txt = os.path.join(ROOT, f"dados/corpus/texto/{CASO}.txt")
arquivo = txt + "` (texto integral; as páginas estão marcadas como `===== [página N/M] =====`, e a página do PDF é esse N"
for leitor in ("A", "B"):
    saida = os.path.join(F4, f"extracao/lote/{leitor}/{CASO}.json")
    t = (corpo.replace("{CASO}", CASO).replace("{ARQUIVO_TEXTO}", arquivo).replace("{UNIDADES}", "\n".join(linhas_u))
         .replace("{VOTOS}", "\n".join(linhas_v) + extra).replace("{SAIDA}", saida))
    assert not re.search(r"\{[A-Z_]+\}", t)
    open(os.path.join(F4, "prompts_lote", leitor, f"{CASO}.md"), "w", encoding="utf-8").write(t + "\n")
print("\n".join(linhas_u)); print(len(linhas_v), "grupos de voto")
