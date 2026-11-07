#!/usr/bin/env python3
"""
Estatística descritiva sobre as tabelas do L3 (1_casos, 2_casos_reus, 3_votos).

Cobre o que PLANO_EXTRACAO.md §3 ("L3 · Consolidação e derivadas") previa:
unanimidade ao longo do tempo, por composição da corte (proxy: n_votantes),
por modalidade Levcovitz e por cargo do réu; distribuição do motivo da
absolvição. Acrescenta o recorte de comparabilidade por equivalência DL 201/67
(D-013), que é o cluster de "mesmo instituto jurídico" mais limpo do corpus.

Rege: dados/metodologia/analise_descritiva_metodo.md (mesma relação
script->documento->pendências do build_l3.py/build_l3.md).

A categorização de `cargo_funcao` em `cargo_categoria` é heurística de
palavra-chave sobre texto livre — o mesmo tipo de abordagem que já falhou
uma vez neste projeto (regex de cargo, Onda 2, ver DICIONARIO.md). Por isso
o script emite a tabela auditável completa (raw + categoria) em vez de só o
agregado. Revisada linha a linha e confirmada em 22/08/2026 (D-025/D-026)
depois de corrigir 2 erros encontrados na auditoria — ver `DECISOES.md`.

Uso: python3 dados/metodologia/analise_descritiva.py
"""
import csv
import os
import re
import unicodedata
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DER = os.path.join(ROOT, "dados/derivados")
OUT_MD = os.path.join(DER, "analise_descritiva.md")
OUT_CARGO_AUDIT = os.path.join(DER, "cargo_categoria_auditoria.psv")


def read_psv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="|"))


CARGO_REGRAS = [
    # "não determinado" precisa vir PRIMEIRO: o texto costuma citar um cargo
    # publicamente associado ao réu mesmo quando o próprio extrator marcou que
    # não achou evidência direta no trecho lido ("...associado a mandato de
    # Deputado Federal, mas não confirmado") — se as regras de cargo concreto
    # rodassem antes, a menção incidental venceria o próprio caveat do
    # extrator. É o mesmo tipo de falha que já queimou este projeto uma vez
    # (regex decidindo em vez de só localizar, D-003).
    (r"n[aã]o determinado", "Não determinado"),
    (r"presidente da rep[uú]blica", "Presidente da República"),
    (r"presidente da c[aâ]mara dos deputados", "Deputado Federal (Presidência da Câmara)"),
    (r"\bsenador", "Senador da República"),
    (r"\bgovernador", "Governador"),
    (r"deputado federal", "Deputado Federal"),
    (r"deputado estadual", "Deputado Estadual"),
    (r"\bprefeito", "Prefeito Municipal"),
    (r"secret[aá]ri[oa] (de estado|municipal|de sa[uú]de)", "Secretário (Estado/Município)"),
    (r"minist[r-]?[oa][\s-]?chefe|ministro de estado", "Ministro de Estado / Chefia de órgão federal"),
    (r"presidente d[oa] partido|tesoureiro d[oa] partido", "Dirigente partidário"),
    (r"particular|s[oó]cio|empres[aá]ri|publicit[aá]rio|representante legal|representante da empresa|contador de empresas|operador (particular|financeiro)", "Particular / setor privado"),
    (r"servidor|funcion[aá]ri[oa] p[uú]blic|cargo administrativo|gerente-executivo|diretor(a)? (financeiro|de marketing|da gazeta|da empresa municipal)|assessor|presidente da empresa municipal|comiss[aã]o de licita[cç][aã]o", "Servidor/agente público (outro cargo)"),
]


def extrai_clausula_fatos(cargo_texto):
    """Isola a cláusula referente 'à época dos fatos', quando marcada
    explicitamente; senão usa o texto inteiro. Escolha: a categorização usa o
    cargo NO MOMENTO DA CONDUTA IMPUTADA, não no momento do julgamento — é o
    cargo substantivamente ligado ao fato de corrupção. Ver pendência
    registrada no relatório: esta escolha não foi confirmada com o Felipe."""
    partes = [p.strip() for p in cargo_texto.split(";")]
    marcadas = [p for p in partes if re.search(r"[àa] [ée]poca dos fatos|aos fatos", p, re.I)]
    if len(marcadas) == 1:
        return marcadas[0]
    if len(marcadas) > 1:
        return " ".join(marcadas)
    return cargo_texto


def remove_mencoes_incidentais(texto):
    """Achado em 22/08/2026 (AP-441-R02): 'cargo de confiança do prefeito'
    referia-se ao cargo do CHEFE do réu (a esposa dele era servidora
    comissionada), não ao cargo do próprio réu — mas '\\bprefeito' batia do
    mesmo jeito e classificava um particular como Prefeito Municipal. Mesma
    classe de erro que já queimou o projeto uma vez (regex por correspondência
    incidental, não por leitura). Remove a menção antes de rodar CARGO_REGRAS."""
    return re.sub(r"confiança d[oa] \S+", "", texto, flags=re.I)


# Override manual para casos onde a heurística de palavra-chave é
# estruturalmente incapaz de decidir corretamente — não é preguiça de regex,
# é um limite reconhecido do método (texto livre com negação/nuance jurídica).
# Cada entrada tem que vir com a razão registrada aqui, não só no valor.
CARGO_OVERRIDE = {
    # AP-973-R01: o texto diz "nos fatos (2005-2007) não era prefeito
    # formal (...) descrito nos votos como 'Prefeito de fato'" — uma
    # heurística por palavra-chave não distingue "não era prefeito formal"
    # (negação) de "Prefeito de fato" (afirmação, poucas palavras depois) sem
    # risco real de inverter outros casos por engenharia excessiva do regex.
    # Decisão de leitura (22/08/2026, com o Felipe): "Prefeito de fato" é o
    # cargo substantivamente ligado à conduta imputada — mesma categoria de
    # um prefeito formal para efeito desta análise.
    "AP-973-R01": "Prefeito Municipal",
    # AP-307-R02 e R03 (D-051, 18/10/2026): o texto do cargo dos dois corréus
    # menciona o Presidente da República como referência ("coautor [...] do
    # Presidente da República"; "Chefe do Gabinete Pessoal do Presidente"), e
    # a regra de presidente bate antes da de particular/servidor — mesma classe
    # de erro da AP-441-R02 (menção incidental). R02 é particular pelo próprio
    # texto ("Particular (não funcionário público)"). R03: chefe do gabinete
    # pessoal, cargo de confiança da Presidência sem status de ministro;
    # categoria escolhida pela sessão, a conferir pelo Felipe.
    "AP-307-R02": "Particular / setor privado",
    "AP-307-R03": "Servidor/agente público (outro cargo)",
}


def categoriza_cargo(id_caso_reu, cargo_texto):
    if id_caso_reu in CARGO_OVERRIDE:
        return CARGO_OVERRIDE[id_caso_reu]
    if not cargo_texto:
        return "Não determinado"
    clausula = remove_mencoes_incidentais(extrai_clausula_fatos(cargo_texto))
    for padrao, categoria in CARGO_REGRAS:
        if re.search(padrao, clausula, re.I):
            return categoria
    return "NÃO CLASSIFICADO (revisar)"


def pct(n, total):
    return f"{100*n/total:.0f}%" if total else "—"


def nome_normalizado(s):
    """Chave de agrupamento robusta a acento (AP-430 grafa 'Cassio Taniguchi',
    sem acento; AP-426/AP-503 grafam 'Cássio Taniguchi' — sem isso o mesmo
    réu não é reconhecido como o mesmo em todos os casos)."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return s.strip().lower()


def main():
    casos = read_psv(os.path.join(DER, "1_casos.psv"))
    reus = read_psv(os.path.join(DER, "2_casos_reus.psv"))
    votos = read_psv(os.path.join(DER, "3_votos.psv"))
    casos_by_id = {c["id_caso"]: c for c in casos}

    for r in reus:
        r["cargo_categoria"] = categoriza_cargo(r["id_caso_reu"], r["cargo_funcao"])
        r["ano_julgamento"] = casos_by_id[r["id_caso"]]["ano_julgamento"]
        r["modalidade_levcovitz"] = casos_by_id[r["id_caso"]]["modalidade_levcovitz"]
        r["depende_dl201"] = casos_by_id[r["id_caso"]]["depende_dl201"]
        r["multiplas_sessoes"] = casos_by_id[r["id_caso"]]["multiplas_sessoes"]

    # auditoria de cargo — sempre a tabela crua junto da categoria, nunca só o agregado
    with open(OUT_CARGO_AUDIT, "w", encoding="utf-8") as f:
        f.write("id_caso_reu|cargo_funcao|cargo_categoria\n")
        for r in reus:
            raw = r["cargo_funcao"].replace("|", "/")
            f.write(f"{r['id_caso_reu']}|{raw}|{r['cargo_categoria']}\n")

    linhas = []
    linhas.append(f"# Estatística descritiva — banco de casos STF ({len(casos)} casos, {len(reus)} réus, {len(votos)} votos)\n")
    linhas.append(f"> Gerado por `dados/metodologia/analise_descritiva.py` a partir de `dados/derivados/{{1_casos,2_casos_reus,3_votos}}.psv`. Não editar à mão.\n")
    linhas.append("> Estatística descritiva pura (D-006 — sem econometria, sem teste de significância). Nenhum número aqui é causal.\n")

    # --- 1. Panorama geral ---
    linhas.append("\n## 1. Panorama geral\n")
    n = len(reus)
    res_c = Counter(r["resultado"] for r in reus)
    unan_c = Counter(r["unanime"] for r in reus)
    cat_c = Counter(r["categoria_placar"] for r in reus)
    linhas.append(f"- **{len(casos)} casos**, **{n} réus** no escopo Levcovitz (D-020), **{len(votos)} votos** individuais.")
    linhas.append(f"- `resultado`: " + ", ".join(f"{k} {v} ({pct(v,n)})" for k, v in res_c.most_common()))
    linhas.append(f"- `unanime`: " + ", ".join(f"{k} {v} ({pct(v,n)})" for k, v in unan_c.most_common()))
    linhas.append(f"- `categoria_placar`: " + ", ".join(f"{k} {v} ({pct(v,n)})" for k, v in cat_c.most_common()))
    linhas.append(f"- Janela temporal: {min(c['ano_julgamento'] for c in casos)}–{max(c['ano_julgamento'] for c in casos)}, com o vazio institucional 2014–2021 já documentado (D-011, Emenda Regimental 49/2014).")

    # --- 2. Unanimidade ao longo do tempo ---
    linhas.append("\n## 2. Unanimidade ao longo do tempo\n")
    linhas.append("Por ano de julgamento (nível réu, não caso — réus do mesmo caso têm o mesmo ano):\n")
    linhas.append("| Ano | N réus | Unânime | % unânime |")
    linhas.append("|---|---|---|---|")
    por_ano = defaultdict(list)
    for r in reus:
        por_ano[r["ano_julgamento"]].append(r)
    for ano in sorted(por_ano):
        rs = por_ano[ano]
        u = sum(1 for r in rs if r["unanime"] == "Sim")
        linhas.append(f"| {ano} | {len(rs)} | {u} | {pct(u, len(rs))} |")
    linhas.append("\nEm dois blocos (pré/pós vazio institucional 2014-2021, D-011):\n")
    linhas.append("| Bloco | N réus | Unânime | % unânime |")
    linhas.append("|---|---|---|---|")
    for label, cond in [("1994–2014 (pré-migração)", lambda a: a <= "2014"), ("2021–2023 (pós-retorno ao Plenário)", lambda a: a >= "2021")]:
        rs = [r for r in reus if cond(r["ano_julgamento"])]
        u = sum(1 for r in rs if r["unanime"] == "Sim")
        linhas.append(f"| {label} | {len(rs)} | {u} | {pct(u, len(rs))} |")

    # --- 3. Unanimidade por composição da corte (proxy: n_votantes) ---
    linhas.append("\n## 3. Unanimidade por composição da corte (proxy: `n_votantes`)\n")
    linhas.append("`n_votantes` varia por ausências/impedimentos pontuais, não só por vacância formal — é proxy grosseiro de composição, não uma reconstrução da Corte por data. Ver `4_referencia_ministros.psv` para a composição exata em qualquer data.\n")
    linhas.append("| n_votantes | N réus | Unânime | % unânime |")
    linhas.append("|---|---|---|---|")
    por_nv = defaultdict(list)
    for r in reus:
        por_nv[r["n_votantes"]].append(r)
    for nv in sorted(por_nv, key=int):
        rs = por_nv[nv]
        u = sum(1 for r in rs if r["unanime"] == "Sim")
        linhas.append(f"| {nv} | {len(rs)} | {u} | {pct(u, len(rs))} |")

    # --- 4. Unanimidade por modalidade Levcovitz ---
    linhas.append("\n## 4. Unanimidade por modalidade Levcovitz\n")
    linhas.append(f"Um réu pode estar em caso com mais de uma modalidade (`modalidade_levcovitz` é do caso, não do réu) — as contagens por código somam mais que {len(reus)}.\n")
    linhas.append("| Código | Rótulo | N réus | Unânime | % unânime |")
    linhas.append("|---|---|---|---|---|")
    rotulo_por_codigo = {}
    for c in casos:
        pass
    # recupera rótulos a partir de modalidade_corrupcao vs modalidade_levcovitz (mesma ordem de geração no build_l3.py)
    for c in casos:
        codigos = c["modalidade_levcovitz"].split(";")
        rotulos = c["modalidade_corrupcao"].split("; ")
        for cod, rot in zip(codigos, rotulos):
            rotulo_por_codigo.setdefault(cod, rot)
    por_modalidade = defaultdict(list)
    for r in reus:
        for cod in r["modalidade_levcovitz"].split(";"):
            por_modalidade[cod].append(r)
    for cod in sorted(por_modalidade, key=int):
        rs = por_modalidade[cod]
        u = sum(1 for r in rs if r["unanime"] == "Sim")
        rot = rotulo_por_codigo.get(cod, "?")
        linhas.append(f"| {cod} | {rot} | {len(rs)} | {u} | {pct(u, len(rs))} |")

    # --- 5. Unanimidade por cargo do réu ---
    linhas.append("\n## 5. Unanimidade por cargo do réu (categorização automática — confirmada em 22/08/2026, D-025/D-026; cargo à época dos fatos)\n")
    linhas.append("| Categoria | N réus | Unânime | % unânime | Condenação | Absolvição | Cond. parcial |")
    linhas.append("|---|---|---|---|---|---|---|")
    por_cargo = defaultdict(list)
    for r in reus:
        por_cargo[r["cargo_categoria"]].append(r)
    for cat, rs in sorted(por_cargo.items(), key=lambda kv: -len(kv[1])):
        u = sum(1 for r in rs if r["unanime"] == "Sim")
        rc = Counter(r["resultado"] for r in rs)
        linhas.append(f"| {cat} | {len(rs)} | {u} | {pct(u, len(rs))} | {rc.get('Condenação',0)} | {rc.get('Absolvição',0)} | {rc.get('Condenação parcial',0)} |")

    # --- 6. Distribuição do motivo, condicionada a resultado ---
    linhas.append("\n## 6. Distribuição do `motivo`\n")
    linhas.append(f"Geral (todos os {n} réus):\n")
    mot_c = Counter(r["motivo"] for r in reus)
    linhas.append("| Motivo | N | % |")
    linhas.append("|---|---|---|")
    for k, v in mot_c.most_common():
        linhas.append(f"| {k} | {v} | {pct(v, n)} |")
    abs_rs = [r for r in reus if r["resultado"] == "Absolvição"]
    linhas.append(f"\nSó entre os {len(abs_rs)} réus com `resultado = Absolvição` (\"motivo da absolvição\", D-008):\n")
    mot_abs = Counter(r["motivo"] for r in abs_rs)
    linhas.append("| Motivo | N | % das absolvições |")
    linhas.append("|---|---|---|")
    for k, v in mot_abs.most_common():
        linhas.append(f"| {k} | {v} | {pct(v, len(abs_rs))} |")

    # --- 7. Cluster de comparabilidade — equivalência DL 201/67 (D-013) ---
    linhas.append("\n## 7. Cluster de comparabilidade — réus por equivalência ao DL 201/67 (D-013)\n")
    linhas.append(
        "É o grupo de \"mesmo instituto jurídico\" mais limpo do corpus: 7 casos entraram só porque o STF processou "
        "o art. 1º do DL 201/67 (crime de prefeito) como equivalente ao peculato/emprego irregular de verbas do CP "
        "(D-013). Mesmo instituto de fundo, réus julgados em anos diferentes — o recorte que a definição de "
        "\"casos comparáveis\" do `CLAUDE.md` pede.\n"
    )
    dl201_casos = [c for c in casos if c["depende_dl201"] == "Sim"]
    linhas.append("| id_caso | Ano | Relator | Réu | Resultado | Unânime | Categoria placar |")
    linhas.append("|---|---|---|---|---|---|---|")
    for c in sorted(dl201_casos, key=lambda c: c["ano_julgamento"]):
        rs = [r for r in reus if r["id_caso"] == c["id_caso"]]
        for r in rs:
            linhas.append(f"| {c['id_caso']} | {c['ano_julgamento']} | {c['relator']} | {r['nome_reu']} | {r['resultado']} | {r['unanime']} | {r['categoria_placar']} |")
    n_dl = sum(1 for c in dl201_casos for r in reus if r["id_caso"] == c["id_caso"])
    n_dl_cond = sum(1 for c in dl201_casos for r in reus if r["id_caso"] == c["id_caso"] and r["resultado_binario"] == "1")
    linhas.append(f"\n**{len(dl201_casos)} casos, {n_dl} réus, {n_dl_cond} condenações ({pct(n_dl_cond, n_dl)}), {sum(1 for c in dl201_casos for r in reus if r['id_caso']==c['id_caso'] and r['unanime']=='Sim')} unânimes ({pct(sum(1 for c in dl201_casos for r in reus if r['id_caso']==c['id_caso'] and r['unanime']=='Sim'), n_dl)}).** Nenhum teste de significância (D-006) — é descrição do grupo, não prova de instabilidade. Ver a tabela linha a linha acima para inspeção qualitativa (é isso que a hipótese do trabalho precisa examinar: mesmo instituto, resultados e placares comparados caso a caso).")

    # --- 7.1 Réus recorrentes — o cluster de comparabilidade mais forte do corpus ---
    linhas.append("\n## 7.1 Réus recorrentes — o mesmo réu em mais de um caso do corpus\n")
    linhas.append(
        f"Achado do build, não previsto no plano original: alguns réus aparecem em mais de um dos {len(casos)} casos. "
        "É comparabilidade de tipo mais forte que \"mesmo instituto jurídico\" — é o **mesmo réu**, o que isola quase tudo "
        "que poderia explicar uma diferença de resultado que não seja o próprio padrão decisório do STF. Chave de "
        "agrupamento normalizada por acento (ver `nome_normalizado()` no script — sem isso, 'Cássio Taniguchi' e "
        "'Cassio Taniguchi', grafados de forma diferente em casos diferentes, não seriam reconhecidos como a mesma pessoa).\n"
    )
    por_reu_nome = defaultdict(list)
    for r in reus:
        por_reu_nome[nome_normalizado(r["nome_reu"])].append(r)
    recorrentes = {k: v for k, v in por_reu_nome.items() if len(v) > 1}
    linhas.append("| Réu | Casos (ano — resultado — unânime) |")
    linhas.append("|---|---|")
    for k, rs in sorted(recorrentes.items(), key=lambda kv: kv[1][0]["nome_reu"]):
        rs_sorted = sorted(rs, key=lambda r: casos_by_id[r["id_caso"]]["ano_julgamento"])
        detalhe = "; ".join(f"{r['id_caso']} ({casos_by_id[r['id_caso']]['ano_julgamento']} — {r['resultado']} — {r['unanime']})" for r in rs_sorted)
        linhas.append(f"| {rs_sorted[0]['nome_reu']} | {detalhe} |")
    linhas.append(
        "\n**Dois casos com resultado diferente entre julgamentos do mesmo réu:**\n"
        "- **Cássio Taniguchi** (ex-Prefeito de Curitiba): absolvido na AP-426 (2008) e na AP-430 (2008, mesmo ano, "
        "incisos diferentes do DL 201/67), depois **condenação parcial** na AP-503 (2010) — incisos IV e V do art. 1º "
        "condenados, inciso XIV absolvido. Não são os mesmos fatos exatos (incisos diferentes em cada ação), mas é o "
        "mesmo instituto (DL 201/67, equivalência D-013), o mesmo cargo, a mesma pessoa, em uma janela de 2 anos.\n"
        "- **Fernando Affonso Collor de Mello** (ex-Presidente da República, depois Senador): absolvido na AP-307 "
        "(1994) e na AP-465 (2014, fatos de 1991-1992, corrupção passiva/peculato) e **condenação parcial** na AP-1025 (2023, fatos "
        "de 2010-2014, corrupção passiva/lavagem) — 9 anos de intervalo, fatos e período distintos, mesma pessoa, "
        "mesmo tipo penal central (corrupção passiva).\n\n"
        "Nenhuma das duas comparações isola \"mudança de posição do STF sobre o mesmo fato\" no sentido mais estrito "
        "que `CLAUDE.md` define (fatos diferentes em cada ação, mesmo para o mesmo réu) — mas são o material bruto "
        "mais concreto do corpus para a seção de resultados examinar caso a caso. **Não incluído como prova de "
        "instabilidade aqui** — é só o achado de que o material existe e onde está."
    )

    # --- 8. Sessões múltiplas ---
    linhas.append("\n## 8. Julgamento em sessão única vs. múltiplas sessões\n")
    ms_c = Counter(c["multiplas_sessoes"] for c in casos)
    linhas.append(f"{ms_c.get('Sim',0)} dos {len(casos)} casos em múltiplas sessões, {ms_c.get('Não',0)} em sessão única.")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")

    print(f"Escrito: {OUT_MD}")
    print(f"Escrito: {OUT_CARGO_AUDIT}")
    nao_class = [r for r in reus if r["cargo_categoria"] == "NÃO CLASSIFICADO (revisar)"]
    print(f"\ncargo_categoria: {len(nao_class)} réu(s) não classificado(s) pela heurística:")
    for r in nao_class:
        print(f"  {r['id_caso_reu']}: {r['cargo_funcao'][:100]}")


if __name__ == "__main__":
    main()
