"""Mede o erro da dedução D-004 no painel de votos, contra os votos lidos na Fase 4.

D-004: ministro em exercício, não ausente e não vencido -> votou com a maioria. Os votos
assim registrados em `derivados/3_votos.psv` têm `fonte_voto = deduzido`; os sem trecho
de evidência, `sem_evidencia`. A Fase 4 registrou de novo o voto de cada ministro em cada
unidade (réu × fato), lido nas peças do acórdão.

Referência independente: só os votos da Fase 4 em que o ministro fundamenta com texto
próprio (`enfrentou_a_questao = Sim`). A adesão não serve: quando o ministro não tem peça
no acórdão (sessão virtual, voto não juntado), a leitura também a tira da ata, a mesma
fonte da dedução, e o campo `inferida_de` nem sempre o declara (conferido na AP-1032, em
que o acórdão só tem os votos do relator). Unidades ativas, no escopo Levcovitz.

Pareamento por réu e ministro: compara-se quando todos os votos de referência do ministro
naquele réu dão o mesmo resultado (Condena ou Absolve) e todas as linhas do painel do
mesmo ministro e réu também. Réu × ministro com resultados mistos (vários fatos com votos
diferentes) fica fora, contado à parte.

Uso: python3 dados/metodologia/medir_deducao_d004.py
Saída: dados/metodologia/medicao_deducao_d004_2026-10-24.md
"""
import csv
import os
from collections import Counter, defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOTOS = os.path.join(RAIZ, "derivados", "3_votos.psv")
F4 = os.path.join(RAIZ, "metodologia", "fase4", "consolidado")
SAIDA = os.path.join(RAIZ, "metodologia", "medicao_deducao_d004_2026-10-24.md")
EFETIVO = ("Condena", "Absolve")


def ler(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="|"))


def main():
    unid = {u["id_unidade"]: u for u in ler(os.path.join(F4, "fase4_unidades.psv"))}
    ativas = {k for k, u in unid.items() if u["status"] == "ativa" and u["escopo_levcovitz"] == "Sim"}

    ref = defaultdict(set)  # (id_caso_reu, ministro) -> votos lidos na Fase 4
    for p in ler(os.path.join(F4, "fase4_posicoes.psv")):
        if p["id_unidade"] not in ativas or p["voto_resultado"] not in EFETIVO:
            continue
        if p["enfrentou_a_questao"] != "Sim":
            continue
        reu = p["id_unidade"].split("-I")[0]
        ref[(reu, p["ministro"])].add(p["voto_resultado"])

    painel = defaultdict(list)
    for v in ler(VOTOS):
        if v["voto_resultado"] in EFETIVO:
            painel[(v["id_caso_reu"], v["ministro"])].append(v)

    res = {f: Counter() for f in ("deduzido", "sem_evidencia", "lido")}
    divergentes = []
    deduzidos_comparados = Counter()
    for chave, linhas in painel.items():
        fontes = Counter(l["fonte_voto"] for l in linhas)
        valores = {l["voto_resultado"] for l in linhas}
        r = ref.get(chave)
        for fonte, n in fontes.items():
            if not r:
                res[fonte]["sem referência na Fase 4"] += n
            elif len(r) > 1 or len(valores) > 1:
                res[fonte]["resultados mistos entre fatos (fora)"] += n
            elif r == valores:
                res[fonte]["coincide"] += n
                if fonte == "deduzido":
                    deduzidos_comparados[chave[0].rsplit("-R", 1)[0]] += n
            else:
                res[fonte]["diverge"] += n
                divergentes.append((chave, fonte, n, sorted(valores), sorted(r)))

    w = []
    w.append("# Medição do erro da dedução D-004 contra os votos lidos na Fase 4\n")
    w.append("> Gerado por `dados/metodologia/medir_deducao_d004.py` (sessão `b7d344d6`, 24/10/2026, `claude-opus-5-5`). Não editar à mão.\n")
    w.append("Referência: voto da Fase 4 em que o ministro fundamenta com texto próprio (adesões excluídas, porque sem peça própria também vêm da ata), unidades ativas no escopo; pareamento por réu e ministro. Contagens em linhas do painel `3_votos` com voto efetivo.\n")
    w.append("| Origem no painel | Linhas | Comparáveis | Coincidem | Divergem | Sem referência na Fase 4 | Mistos (fora) |")
    w.append("|---|---|---|---|---|---|---|")
    for fonte in ("deduzido", "sem_evidencia", "lido"):
        c = res[fonte]
        tot = sum(c.values())
        comp = c["coincide"] + c["diverge"]
        w.append(f"| {fonte} | {tot} | {comp} | {c['coincide']} | {c['diverge']} | {c['sem referência na Fase 4']} | {c['resultados mistos entre fatos (fora)']} |")
    w.append("")
    w.append("Votos deduzidos comparados, por caso: " + "; ".join(f"{k} {v}" for k, v in sorted(deduzidos_comparados.items())) + ".\n")
    if divergentes:
        w.append("## Divergências (conferir no acórdão)\n")
        w.append("| Réu | Ministro | Origem | Linhas | Painel | Fase 4 |")
        w.append("|---|---|---|---|---|---|")
        for (reu, m), fonte, n, pv, rv in sorted(divergentes):
            w.append(f"| {reu} | {m} | {fonte} | {n} | {', '.join(pv)} | {', '.join(rv)} |")
    else:
        w.append("Nenhuma divergência entre as linhas comparáveis.")
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write("\n".join(w) + "\n")
    print("\n".join(w))


if __name__ == "__main__":
    main()
