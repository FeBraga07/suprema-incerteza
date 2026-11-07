#!/usr/bin/env python3
"""
Build determinístico L3 — gera 1_casos.psv, 2_casos_reus.psv e 3_votos.psv
a partir dos JSONs por caso (24 até 18/10/2026; 25 com a AP-307, D-051) em dados/derivados/casos/.

Rege: dados/metodologia/build_l3.md (mapeamento de campos e decisões de
esquema tomadas nesta versão). Não editar as PSVs de saída à mão — se uma
regra mudar, mudar este script e rodar de novo.

Uso: python3 dados/metodologia/build_l3.py
"""
import json
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CASOS_DIR = os.path.join(ROOT, "dados/derivados/casos")
CLASSIFICACAO_PSV = os.path.join(ROOT, "dados/derivados/classificacao_105.psv")
CENSO_PSV = os.path.join(ROOT, "dados/brutos/censo_ap_plenario_1991_2024.psv")
# D-051 (18/10/2026): complemento do censo — ações penais do Plenário que o índice cataloga
# como Turma. A classificação segue o mesmo protocolo, em arquivo próprio; o censo bruto do
# complemento não traz o relator, que vem do registro do índice (relator_processo_nome;
# relator_acordao_nome é nulo no registro) — ver brutos/AP-307_ata_indice_sjur157761.txt.
CLASSIFICACAO_COMPLEMENTO_PSV = os.path.join(ROOT, "dados/derivados/classificacao_complemento_2026-10-18.psv")
CENSO_COMPLEMENTO_PSV = os.path.join(ROOT, "dados/brutos/censo_complemento_ap_turmas_2026-10-18.psv")
RELATOR_COMPLEMENTO = {"307": "ILMAR GALVÃO"}
MINISTROS_PSV = os.path.join(ROOT, "dados/derivados/4_referencia_ministros.psv")
OUT_DIR = os.path.join(ROOT, "dados/derivados")

SIM_NAO = {True: "Sim", False: "Não"}

# Variantes de grafia do nome de ministro observadas nos JSONs de extração que
# não batem literalmente com 4_referencia_ministros.nome_padrao nem com
# nome_variantes — normalizadas aqui para permitir o cruzamento informal
# (ministro -> 4_referencia.nome_padrao). "Carlos Ayres Britto" e "Carlos
# Britto" são a mesma pessoa que "Ayres Britto" na tabela de referência
# (decisão registrada em 22/08/2026: a tabela tinha 2 linhas para 1 ministro,
# com datas de saída diferentes — 2012-11-17 é a correta, confirmada contra
# fonte externa: Ayres Britto completou 70 anos em 18/11/2012 e a
# aposentadoria compulsória foi decretada em 17/11/2012).
RENOMEIA_MINISTRO = {
    "Carlos Ayres Britto": "Ayres Britto",
    "Carlos Britto": "Ayres Britto",
}


def normaliza_ministro(nome):
    nome = re.sub(r"\s*\([^)]*\)\s*$", "", nome).strip()
    return RENOMEIA_MINISTRO.get(nome, nome)


def unwrap(v):
    """Campos do JSON L1 vêm como {'valor':..., 'evidencia':..., ...} ou,
    nos arrays 'votos' de casos multi-fato, como valor cru. Normaliza os dois."""
    if isinstance(v, dict) and "valor" in v:
        return v["valor"]
    return v


def clean(s):
    """Blinda contra '|' e quebras de linha vazando para o PSV (nenhuma
    ocorrência encontrada na auditoria pré-build, mas o build não deve
    quebrar silenciosamente se aparecer uma no futuro)."""
    if s is None:
        return ""
    s = str(s)
    if "|" in s or "\n" in s:
        s = s.replace("|", "/").replace("\n", " ")
    return s


def sim_nao(v):
    if v is None:
        return ""
    return SIM_NAO.get(bool(v), "")


def read_psv(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f if not l.startswith("#") and l.strip()]
    header = lines[0].split("|")
    for line in lines[1:]:
        parts = line.split("|")
        rows.append(dict(zip(header, parts)))
    return rows


def write_psv(path, header, rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write("|".join(header) + "\n")
        for r in rows:
            f.write("|".join(clean(r.get(c, "")) for c in header) + "\n")
    print(f"  {path.split('/')[-1]}: {len(rows)} linhas")


def load_casos():
    casos = {}
    for path in sorted(glob.glob(os.path.join(CASOS_DIR, "AP-*.json"))):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        casos[d["id_caso"]] = d
    return casos


def main():
    casos = load_casos()
    classificacao = {r["id_caso"]: r for r in read_psv(CLASSIFICACAO_PSV)}
    censo = {r["processo"]: r for r in read_psv(CENSO_PSV)}
    # D-051: só os casos classificados no complemento entram dele; o resto do complemento é Turma.
    complemento = {r["id_caso"]: r for r in read_psv(CLASSIFICACAO_COMPLEMENTO_PSV)}
    assert not set(complemento) & set(classificacao), "caso duplicado entre classificação e complemento"
    classificacao.update(complemento)
    for r in read_psv(CENSO_COMPLEMENTO_PSV):
        if f"AP-{r['processo']}" in complemento:
            assert r["processo"] not in censo
            censo[r["processo"]] = {**r, "relator": RELATOR_COMPLEMENTO[r["processo"]]}
    ministros_ref = read_psv(MINISTROS_PSV)
    nome_padrao_lookup = {m["nome_padrao"].upper(): m["nome_padrao"] for m in ministros_ref}

    incluidos = {k: v for k, v in classificacao.items() if v["decisao"] == "incluir"}
    assert set(incluidos) == set(casos), (
        "Descompasso entre classificacao_105.psv (decisao=incluir) e os JSONs em "
        f"dados/derivados/casos/: só na classificação={set(incluidos)-set(casos)}, "
        f"só nos JSONs={set(casos)-set(incluidos)}"
    )

    linhas_1_casos = []
    linhas_2_reus = []
    linhas_3_votos = []
    id_voto_seq = 1

    for id_caso in sorted(casos, key=lambda x: int(x.split("-")[1])):
        d = casos[id_caso]
        cls = classificacao[id_caso]
        numero_processo = id_caso.split("-")[1]
        cen = censo.get(numero_processo)
        if cen is None:
            raise SystemExit(f"{id_caso}: numero_processo {numero_processo} não encontrado no censo")

        caso = d["caso"]
        modalidade_ids = unwrap(caso["modalidade_levcovitz"]) or []
        modalidade_rotulos = caso["modalidade_levcovitz"].get("rotulos", []) if isinstance(caso["modalidade_levcovitz"], dict) else []

        nome_popular = "Mensalão" if id_caso == "AP-470" else ""

        # D-032: `relator` é o relator originário (eh_relator=Sim nos votos do JSON);
        # o campo do censo do portal é o REDATOR DO ACÓRDÃO. Os dois entram como colunas
        # distintas. D-057: a diferença entre eles não basta para dizer que o relator ficou
        # vencido (AP-508: saída do relator do Tribunal; AP-1025: relator na maioria);
        # `relator_vencido` é calculado depois, a partir do voto do relator em 3_votos.
        redator_acordao = nome_padrao_lookup.get(normaliza_ministro(cen["relator"].title()).upper(), cen["relator"].title())
        relatores_json = sorted({normaliza_ministro(unwrap(v["ministro"])) for v in d.get("votos", []) if unwrap(v["eh_relator"])})
        if len(relatores_json) != 1:
            raise SystemExit(f"{id_caso}: esperado exatamente 1 relator nos votos do JSON, encontrado {relatores_json}")
        relator_originario = relatores_json[0]

        linhas_1_casos.append({
            "id_caso": id_caso,
            "nome_popular": nome_popular,
            "numero_processo": numero_processo,
            "link_portal": f"https://jurisprudencia.stf.jus.br/pages/search/{cen['sjur_id']}/false",
            "data_julgamento": cen["julgamento"],
            "ano_julgamento": cen["julgamento"][:4],
            "multiplas_sessoes": sim_nao(unwrap(caso["multiplas_sessoes"])),
            "relator": relator_originario,
            "redator_acordao": redator_acordao,
            "relator_vencido": None,  # preenchido depois de 3_votos (D-057)
            "modalidade_corrupcao": "; ".join(modalidade_rotulos),
            "modalidade_levcovitz": ";".join(str(i) for i in modalidade_ids),
            "instituto_juridico_1": unwrap(caso["instituto_juridico"]) or "",
            "instituto_juridico_2": "",
            "n_reus": unwrap(caso["n_reus"]),
            "observacoes": "",
            "merito_finalizado": sim_nao(unwrap(caso["merito_finalizado"])),
            "lavagem_associada": sim_nao(cls["lavagem"] == "SIM"),
            "organizacao_criminosa_associada": sim_nao(cls["org_criminosa"] == "SIM"),
            "depende_dl201": sim_nao(cls["depende_dl201"] == "SIM"),
            "regra_aplicada": cls["regra_aplicada"],
            "justificativa_classificacao": cls["justificativa"],
        })

        # --- 2_casos_reus ---
        reu_id_by_nome = {}
        for i, r in enumerate(d.get("reus", []), start=1):
            reu_id_by_nome[unwrap(r["nome"])] = f"{id_caso}-R{i:02d}"

        # D-029 precisa dos placares por (réu, fato) ANTES de resumir o réu: pré-expande os votos.
        placar_por_reu = {}  # id_caso_reu -> {fato: (vc, va)}
        for v in d.get("votos", []):
            fato = unwrap(v.get("fato")) if "fato" in v else ""
            alvo_ids = [reu_id_by_nome[unwrap(v["reu"])]] if "reu" in v else list(reu_id_by_nome.values())
            vr = unwrap(v["voto_resultado"])
            for id_caso_reu in alvo_ids:
                vc_, va_ = placar_por_reu.setdefault(id_caso_reu, {}).setdefault(fato, (0, 0))
                if vr == "condena":
                    placar_por_reu[id_caso_reu][fato] = (vc_ + 1, va_)
                elif vr == "absolve":
                    placar_por_reu[id_caso_reu][fato] = (vc_, va_ + 1)

        for i, r in enumerate(d.get("reus", []), start=1):
            id_caso_reu = f"{id_caso}-R{i:02d}"
            nome_reu = unwrap(r["nome"])

            resultado = unwrap(r["resultado"])
            resultado_bin = 1 if resultado in ("Condenação", "Condenação parcial") else 0
            nv = unwrap(r["n_votantes"])
            vc = unwrap(r["votos_condenacao"])
            va = unwrap(r["votos_absolvicao"])
            unanime = unwrap(r["unanime"])
            placar_fato_ref = ""
            dissenso_fora_resultado = False
            observacoes = ""

            # D-029 (a): réu com mais de um fato com placares distintos -> placar do fato
            # mais apertado; unânime só se todos os fatos forem unânimes.
            fatos = {f: p for f, p in placar_por_reu.get(id_caso_reu, {}).items() if sum(p) > 0}
            if len(fatos) > 1:
                def perc(p):
                    return max(p) / sum(p)
                fato_ref, (vc_f, va_f) = min(fatos.items(), key=lambda kv: (perc(kv[1]), kv[0]))
                if (vc_f, va_f) != (vc, va):
                    observacoes += (f"D-029: placar do réu = fato mais apertado ('{fato_ref}': {vc_f}x{va_f}); "
                                    f"valor extraído no JSON era {vc}x{va}. ")
                vc, va = vc_f, va_f
                nv = vc + va
                unanime = all(min(p) == 0 for p in fatos.values())
                placar_fato_ref = fato_ref

            # D-029 (b): dissenso que não altera o resultado (crime fora do escopo ou
            # fundamento) não quebra a unanimidade — vira flag.
            if not unanime and (vc == 0 or va == 0):
                unanime = True
                dissenso_fora_resultado = True
                observacoes += ("D-029: extração registrou unanime=False com placar sem divergência de resultado; "
                                "dissenso restrito a capítulo fora do escopo ou a fundamento (ver avisos do JSON). ")

            margem = abs(vc - va)
            perc_vencedor = round(max(vc, va) / nv, 3) if nv else ""
            if unanime:
                categoria = "Unânime"
            elif isinstance(perc_vencedor, float) and perc_vencedor >= 0.70:
                categoria = "Folgado"
            else:
                categoria = "Apertado"
            crimes = "; ".join(
                f"{c.get('artigo','')} ({c.get('diploma','')})" for c in r.get("crimes", [])
            )

            linhas_2_reus.append({
                "id_caso_reu": id_caso_reu,
                "id_caso": id_caso,
                "nome_reu": nome_reu,
                "cargo_funcao": unwrap(r.get("cargo_funcao")) or "",
                "resultado": resultado,
                "resultado_binario": resultado_bin,
                "motivo": unwrap(r.get("motivo")) or "",
                "prescricao_pos_condenacao": sim_nao(unwrap(r.get("prescricao_pos_condenacao"))),
                "crimes": crimes,
                "n_votantes": nv,
                "votos_condenacao": vc,
                "votos_absolvicao": va,
                "margem_votos": margem,
                "perc_vencedor": perc_vencedor,
                "unanime": sim_nao(unanime),
                "categoria_placar": categoria,
                "placar_fato_ref": placar_fato_ref,
                "dissenso_fora_resultado": sim_nao(dissenso_fora_resultado),
                "observacoes": observacoes.strip(),
            })

        # --- 3_votos ---
        # Casos com placar homogêneo entre réus não carregam 'reu'/'fato' por
        # linha de voto (o L1 não diferenciou porque o placar é o mesmo) — o
        # build faz o fan-out para cada réu do caso. Casos com 'reu' explícito
        # (D-021: placar heterogêneo por réu/fato) usam o valor direto.
        reus_do_caso = list(reu_id_by_nome.values())
        grupos = {}  # (id_caso_reu, fato) -> list of row dicts (para acompanhou_relator)

        votos_expandidos = []
        for v in d.get("votos", []):
            fato = unwrap(v.get("fato")) if "fato" in v else ""
            if "reu" in v:
                nome_reu_voto = unwrap(v["reu"])
                if nome_reu_voto not in reu_id_by_nome:
                    raise SystemExit(
                        f"{id_caso}: voto referencia réu '{nome_reu_voto}' ausente de 2_casos_reus "
                        "(pode ser um dos réus fora do escopo Levcovitz, D-020 — não deveria ter voto próprio)"
                    )
                alvo_ids = [reu_id_by_nome[nome_reu_voto]]
            else:
                alvo_ids = reus_do_caso
            for id_caso_reu in alvo_ids:
                votos_expandidos.append((id_caso_reu, fato, v))

        for id_caso_reu, fato, v in votos_expandidos:
            grupos.setdefault((id_caso_reu, fato), []).append(v)

        for id_caso_reu, fato, v in votos_expandidos:
            voto_resultado = unwrap(v["voto_resultado"])
            eh_relator = unwrap(v["eh_relator"])
            vencido = unwrap(v["vencido"])
            ausente = unwrap(v["ausente"])
            motivo_ausencia = unwrap(v.get("motivo_ausencia"))
            if motivo_ausencia in ("n/a", "não se aplica", None):
                motivo_ausencia = ""

            voto_binario = {"condena": 1, "absolve": 0}.get(voto_resultado, "")

            # D-032: coesão do colegiado, distinta de deferência ao relator.
            if ausente or voto_resultado == "não votou":
                acompanhou_maioria = "NA"
            else:
                acompanhou_maioria = "Não" if vencido else "Sim"

            # D-034: proveniência do voto, rastreável na tabela.
            vr_raw = v.get("voto_resultado")
            if isinstance(vr_raw, dict) and vr_raw.get("evidencia"):
                fonte_voto = "deduzido" if "deducao" in str(vr_raw.get("fonte", "")).lower() else "lido"
            else:
                fonte_voto = "sem_evidencia"

            if eh_relator or voto_resultado == "não votou":
                acompanhou = "NA"
            else:
                relator_resultado = None
                for gv in grupos[(id_caso_reu, fato)]:
                    if unwrap(gv["eh_relator"]):
                        relator_resultado = unwrap(gv["voto_resultado"])
                        break
                if relator_resultado is None or relator_resultado == "não votou":
                    acompanhou = "NA"
                else:
                    acompanhou = "Sim" if voto_resultado == relator_resultado else "Não"

            linhas_3_votos.append({
                "id_voto": id_voto_seq,
                "id_caso": id_caso,
                "id_caso_reu": id_caso_reu,
                "fato": fato,
                "ministro": normaliza_ministro(unwrap(v["ministro"])),
                "eh_relator": sim_nao(eh_relator),
                "voto_resultado": {"condena": "Condena", "absolve": "Absolve", "não votou": "Não votou"}.get(voto_resultado, voto_resultado),
                "voto_binario": voto_binario,
                "acompanhou_relator": acompanhou,
                "acompanhou_maioria": acompanhou_maioria,
                "vencido": sim_nao(vencido),
                "ausente": sim_nao(ausente),
                "motivo_ausencia": motivo_ausencia,
                "fonte_voto": fonte_voto,
            })
            id_voto_seq += 1

    # D-057: relator vencido no resultado de ao menos um réu ou fato do escopo
    relator_vencido_em = {r["id_caso"] for r in linhas_3_votos if r["eh_relator"] == "Sim" and r["vencido"] == "Sim"}
    for r1 in linhas_1_casos:
        r1["relator_vencido"] = sim_nao(r1["id_caso"] in relator_vencido_em)

    header_1 = ["id_caso", "nome_popular", "numero_processo", "link_portal", "data_julgamento",
                "ano_julgamento", "multiplas_sessoes", "relator", "redator_acordao", "relator_vencido", "modalidade_corrupcao",
                "modalidade_levcovitz", "instituto_juridico_1", "instituto_juridico_2", "n_reus",
                "observacoes", "merito_finalizado", "lavagem_associada",
                "organizacao_criminosa_associada", "depende_dl201", "regra_aplicada",
                "justificativa_classificacao"]
    header_2 = ["id_caso_reu", "id_caso", "nome_reu", "cargo_funcao", "resultado",
                "resultado_binario", "motivo", "prescricao_pos_condenacao", "crimes",
                "n_votantes", "votos_condenacao", "votos_absolvicao", "margem_votos",
                "perc_vencedor", "unanime", "categoria_placar", "placar_fato_ref",
                "dissenso_fora_resultado", "observacoes"]
    header_3 = ["id_voto", "id_caso", "id_caso_reu", "fato", "ministro", "eh_relator",
                "voto_resultado", "voto_binario", "acompanhou_relator", "acompanhou_maioria", "vencido", "ausente",
                "motivo_ausencia", "fonte_voto"]

    print("Escrevendo tabelas:")
    write_psv(os.path.join(OUT_DIR, "1_casos.psv"), header_1, linhas_1_casos)
    write_psv(os.path.join(OUT_DIR, "2_casos_reus.psv"), header_2, linhas_2_reus)
    write_psv(os.path.join(OUT_DIR, "3_votos.psv"), header_3, linhas_3_votos)

    # --- checagens de integridade pós-build ---
    print("\nChecagens de integridade:")
    ids_casos = {r["id_caso"] for r in linhas_1_casos}
    # D-051: o número esperado de casos vem da classificação (24 até 18/10/2026; 25 com a AP-307)
    assert len(ids_casos) == len(linhas_1_casos) == len(incluidos), f"1_casos: PK duplicada ou != {len(incluidos)} linhas"
    print(f"  1_casos: {len(linhas_1_casos)} linhas, id_caso único — OK")

    ids_reus = [r["id_caso_reu"] for r in linhas_2_reus]
    assert len(ids_reus) == len(set(ids_reus)), "2_casos_reus: id_caso_reu duplicado"
    orfaos_2 = {r["id_caso"] for r in linhas_2_reus} - ids_casos
    assert not orfaos_2, f"2_casos_reus: id_caso órfão {orfaos_2}"
    print(f"  2_casos_reus: {len(linhas_2_reus)} linhas, PK única, 0 órfãs de id_caso — OK")

    orfaos_3_reu = {r["id_caso_reu"] for r in linhas_3_votos} - set(ids_reus)
    orfaos_3_caso = {r["id_caso"] for r in linhas_3_votos} - ids_casos
    assert not orfaos_3_reu, f"3_votos: id_caso_reu órfão {orfaos_3_reu}"
    assert not orfaos_3_caso, f"3_votos: id_caso órfão {orfaos_3_caso}"
    incons = [r for r in linhas_3_votos if r["id_caso"] != r["id_caso_reu"].rsplit("-R", 1)[0]]
    assert not incons, f"3_votos: id_caso inconsistente com id_caso_reu em {len(incons)} linhas"
    print(f"  3_votos: {len(linhas_3_votos)} linhas, 0 órfãs, id_caso consistente com id_caso_reu — OK")

    n_reus_mismatch = []
    for r1 in linhas_1_casos:
        n_reus_tabela = r1["n_reus"]
        n_reus_array = sum(1 for r2 in linhas_2_reus if r2["id_caso"] == r1["id_caso"])
        if n_reus_tabela != n_reus_array:
            n_reus_mismatch.append((r1["id_caso"], n_reus_tabela, n_reus_array))
    print(f"  n_reus (1_casos) vs contagem real em 2_casos_reus: {len(n_reus_mismatch)} descompasso(s) "
          "— esperado exatamente 1 (AP-470, D-020: réus sem crime de escopo ficam fora de 2_casos_reus)")
    for m in n_reus_mismatch:
        print(f"    {m[0]}: n_reus={m[1]}, réus em 2_casos_reus={m[2]}")

    relatores_fora = sorted({r["relator"] for r in linhas_1_casos} - set(nome_padrao_lookup.values()))
    ministros_fora = sorted({r["ministro"] for r in linhas_3_votos} - set(nome_padrao_lookup.values()))
    print(f"  relator (1_casos) fora de 4_referencia_ministros.nome_padrao: {relatores_fora or 'nenhum'}")
    print(f"  ministro (3_votos) fora de 4_referencia_ministros.nome_padrao: {ministros_fora or 'nenhum'}")

    soma_vc_va = [r for r in linhas_2_reus if r["votos_condenacao"] + r["votos_absolvicao"] != r["n_votantes"]]
    print(f"  2_casos_reus: votos_condenacao+votos_absolvicao != n_votantes em {len(soma_vc_va)} linha(s) "
          "(esperado 0 desde D-030, 19/09/2026)")
    fontes = {}
    for r in linhas_3_votos:
        fontes[r["fonte_voto"]] = fontes.get(r["fonte_voto"], 0) + 1
    print(f"  3_votos.fonte_voto (D-034): {fontes}")
    rv = [r["id_caso"] for r in linhas_1_casos if r["relator_vencido"] == "Sim"]
    print(f"  1_casos.relator_vencido = Sim (D-057): {len(rv)} caso(s) {rv}")
    rd = [r["id_caso"] for r in linhas_1_casos if r["relator"] != r["redator_acordao"]]
    print(f"  1_casos com redator diferente do relator: {len(rd)} caso(s) {rd}")
    d29 = [r["id_caso_reu"] for r in linhas_2_reus if r["observacoes"]]
    print(f"  2_casos_reus com observação D-029: {len(d29)} {d29}")
    for r in soma_vc_va:
        print(f"    {r['id_caso_reu']}: {r['votos_condenacao']}+{r['votos_absolvicao']} != {r['n_votantes']}")


if __name__ == "__main__":
    main()
