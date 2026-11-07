#!/usr/bin/env python3
"""
Taxa de acerto da extração por leitura (L1) contra o gabarito manual
(GABARITO_VALIDACAO.md, §2 e §3). Portão do PLANO_EXTRACAO.md §3-L2, medido em 19/09/2026.

Compara o VALOR EXTRAÍDO (antes de qualquer decisão do pesquisador — usa
`valor_extraido_original` quando existe) contra duas versões do gabarito:
  - "original" (08/08/2026): o que o gabarito dizia ANTES de a extração rodar;
  - "corrigido" (09/08/2026): depois de duas correções feitas lendo a ata, motivadas
    por divergência com a própria extração (AP-372 n_votantes; AP-565 quadro por réu).
As duas taxas são reportadas porque a segunda não é cega: o gabarito foi corrigido
à luz da extração. Onde as versões coincidem, o valor é o mesmo.

Saída: metodologia/validacao_gabarito_2026-09-19.md. Não escreve no banco.
"""
import csv, json, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
DER = os.path.join(os.path.dirname(HERE), "derivados")
def psv(p): return list(csv.DictReader(open(p, encoding="utf-8"), delimiter="|"))
reus = {r["id_caso_reu"]: r for r in psv(os.path.join(DER, "2_casos_reus.psv"))}
votos = psv(os.path.join(DER, "3_votos.psv"))

def extraido(id_reu, campo):
    """valor produzido pelo extrator, antes de decisões do pesquisador (D-029..D-031)."""
    ap, _ = id_reu.rsplit("-R", 1)
    d = json.load(open(os.path.join(DER, "casos", ap + ".json"), encoding="utf-8"))
    r = d["reus"][int(id_reu.rsplit("R", 1)[1]) - 1]
    f = r.get(campo)
    if isinstance(f, dict):
        v = f.get("valor_extraido_original", f.get("valor"))
    else:
        v = f
    if campo == "unanime": v = "Sim" if v else "Não"
    return v

def vencidos(id_reu):
    return frozenset(v["ministro"] for v in votos if v["id_caso_reu"] == id_reu and v["vencido"] == "Sim")

def motivo_ausencia(id_reu, ministro):
    for v in votos:
        if v["id_caso_reu"] == id_reu and v["ministro"] == ministro and (v["ausente"] == "Sim" or v["voto_resultado"] == "Não votou"):
            return v["motivo_ausencia"].strip().lower()
    return None

def categoria(vc, va, unanime):
    if unanime == "Sim": return "Unânime"
    return "Folgado" if max(vc, va) / (vc + va) >= 0.70 else "Apertado"

# ---- gabarito: {id_reu: {campo: (valor_original, valor_corrigido)}} ; None = "a apurar"
G = {}
def g(id_reu, **campos):
    G.setdefault(id_reu, {}).update({k: (v if isinstance(v, tuple) else (v, v)) for k, v in campos.items()})

g("AP-409-R01", resultado="Condenação", n_votantes=10, votos_condenacao=7, votos_absolvicao=3, categoria_placar="Folgado")
g("AP-432-R01", resultado="Condenação parcial", n_votantes=8, votos_condenacao=5, votos_absolvicao=3, categoria_placar="Apertado")
for r in ("AP-372-R01", "AP-372-R02"):
    g(r, resultado="Absolvição", unanime="Sim", n_votantes=(10, 9))   # corrigido em 09/08 após divergência com a extração
# AP-565: original = 'Condenação parcial' 9x2 uniforme para os 9 réus; corrigido em 09/08 = quadro por grupo (art. 90)
grp_cond = ("AP-565-R01", "AP-565-R02", "AP-565-R03")
grp_empate = ("AP-565-R04", "AP-565-R05", "AP-565-R06", "AP-565-R08")
grp_abs = ("AP-565-R07", "AP-565-R09")
for r in grp_cond:   g(r, resultado="Condenação parcial", votos_condenacao=(9, 10), votos_absolvicao=(2, 0), unanime=("Não", "Sim"))
for r in grp_empate: g(r, resultado=("Condenação parcial", "Absolvição"), votos_condenacao=(9, 5), votos_absolvicao=(2, 5), unanime=("Não", "Não"))
for r in grp_abs:    g(r, resultado=("Condenação parcial", "Absolvição"), votos_condenacao=(9, 0), votos_absolvicao=(2, 10), unanime=("Não", "Sim"))
V433 = frozenset(["Ellen Gracie", "Cezar Peluso", "Cármen Lúcia", "Joaquim Barbosa", "Ayres Britto"])
for r in ("AP-433-R01", "AP-433-R02"):
    g(r, resultado="Absolvição", n_votantes=11, votos_condenacao=5, votos_absolvicao=6, vencidos=V433)
V447 = frozenset(["Joaquim Barbosa", "Eros Grau", "Cezar Peluso", "Marco Aurélio"])
for r in ("AP-447-R01", "AP-447-R02"):
    g(r, n_votantes=10, votos_condenacao=4, votos_absolvicao=6, vencidos=V447)
g("AP-1036-R01", resultado="Absolvição", n_votantes=10, unanime="Sim", motivo_ausencia_alexandre="suspeição")
g("AP-348-R01", resultado="Absolvição", unanime="Sim")
for r in ("AP-365-R01", "AP-365-R02"):
    g(r, resultado="Absolvição", unanime="Sim")
# AP-441: sem valor firme (gabarito §7). AP-462: não está no corpus de 24. AP-470: sem gabarito.

# ---- comparação
linhas = []
acertos = {"original": collections.Counter(), "corrigido": collections.Counter()}
totais = collections.Counter()
for id_reu, campos in G.items():
    for campo, (vo, vcorr) in campos.items():
        if campo == "vencidos":
            ext = vencidos(id_reu)
        elif campo == "motivo_ausencia_alexandre":
            ext = motivo_ausencia(id_reu, "Alexandre de Moraes")
        elif campo == "categoria_placar":
            ext = categoria(extraido(id_reu, "votos_condenacao"), extraido(id_reu, "votos_absolvicao"), extraido(id_reu, "unanime"))
        else:
            ext = extraido(id_reu, campo)
        totais[campo] += 1
        ok_o, ok_c = (ext == vo), (ext == vcorr)
        acertos["original"][campo] += ok_o
        acertos["corrigido"][campo] += ok_c
        if not (ok_o and ok_c):
            fmt = lambda x: ", ".join(sorted(x)) if isinstance(x, frozenset) else str(x)
            linhas.append((id_reu, campo, fmt(ext), fmt(vo), fmt(vcorr), "✔" if ok_o else "✘", "✔" if ok_c else "✘"))

n_reus = len(G); n_casos = len({k.rsplit("-R", 1)[0] for k in G}); n_cmp = sum(totais.values())
out = []
out.append("# Taxa de acerto da extração por leitura contra o gabarito manual — 19/09/2026\n")
out.append(f"> Gerado por `metodologia/validacao_gabarito.py`. Portão do `PLANO_EXTRACAO.md` §3-L2, medido depois da análise descritiva (desvio declarado, D-028 §6.1). Modelo dos extratores: `claude-sonnet-5` (REGISTRO_EXECUCAO §2). Comparação e relatório: `claude-fable-5-1`.\n")
out.append(f"**Cobertura:** {n_casos} casos, {n_reus} réus, {n_cmp} comparações campo a campo com valor firme no gabarito. Fora: AP-441 (sem valor firme, gabarito §7), AP-462 (não está no universo de 24), AP-470 (sem gabarito).\n")
out.append("**O que se compara:** o valor produzido pelo extrator (antes de qualquer decisão do pesquisador — D-029 a D-031 não entram) contra o gabarito em duas versões. A versão **original** (08/08) é a única comparação cega. A versão **corrigida** (09/08) incorpora duas correções feitas lendo a ata *depois* de a extração divergir do gabarito — mede o acerto contra a fonte primária, mas não é cega.\n")
out.append("## Acerto por campo\n")
out.append("| Campo | Comparações | Acerto vs gabarito original (cego) | Acerto vs gabarito corrigido (fonte primária) |")
out.append("|---|---|---|---|")
for campo in ["resultado", "n_votantes", "votos_condenacao", "votos_absolvicao", "unanime", "categoria_placar", "vencidos", "motivo_ausencia_alexandre"]:
    if totais[campo]:
        t = totais[campo]; a = acertos["original"][campo]; c = acertos["corrigido"][campo]
        out.append(f"| `{campo}` | {t} | {a}/{t} ({a/t:.0%}) | {c}/{t} ({c/t:.0%}) |")
TA = sum(acertos["original"].values()); TC = sum(acertos["corrigido"].values())
out.append(f"| **Total** | **{n_cmp}** | **{TA}/{n_cmp} ({TA/n_cmp:.0%})** | **{TC}/{n_cmp} ({TC/n_cmp:.0%})** |\n")
out.append("## Divergências, uma a uma\n")
out.append("| Réu | Campo | Extraído | Gabarito original | Gabarito corrigido | = orig. | = corr. |")
out.append("|---|---|---|---|---|---|---|")
for l in linhas: out.append("| " + " | ".join(l) + " |")
out.append("""
## Leitura

1. **Contra a fonte primária (gabarito corrigido), a única divergência é `votos_condenacao` da AP-409** — e ela não é erro de leitura: a ata registra duas contagens (Cármen Lúcia: 5; Peluso, ao proclamar: 7). O extrator seguiu a primeira; o gabarito, a segunda. A escolha foi tomada pelo pesquisador em D-030 (7x3). `categoria_placar` da AP-409 herda a mesma divergência (0,50 → Apertado com 5; 0,70 → Folgado com 7).
2. **Todas as demais divergências contra o gabarito original são casos em que a extração estava certa e o gabarito errado**, conferido na ata: `n_votantes` da AP-372 (o gabarito presumia Corte de 11 numa data de vacância) e o quadro inteiro da AP-565 (o gabarito colapsava nove resultados num único 9x2). São os dois erros de gabarito que o `ESTADO.md` pedia para corrigir (G-M14, G-M15) — corrigidos aqui por registro, não por edição do arquivo original, que preserva o histórico.
3. **Padrões de erro do método antigo (gabarito §4):** nenhum reincidiu. (a) falso positivo de prescrição: 0 em AP-409, AP-432, AP-565; (b) votantes fixados em 11: 0 em AP-372, AP-409, AP-447 (e a extração detectou a vacância que o gabarito não detectou); (e) tokens de preliminar como vencidos: 0 na AP-447; (g) sessão errada em ata multissessão: 0 na AP-433; (h) verbo fora do vocabulário: 0 em AP-348, AP-365, AP-1036.
4. **O que esta medida não diz.** O gabarito cobre os casos-armadilha conhecidos, não uma amostra aleatória (gabarito §6); e os extratores, embora não vissem os valores, sabiam pelo prompt que existiam armadilhas (REGISTRO §4.2). A taxa mede a capacidade de não cair nas armadilhas catalogadas; não é estimativa da taxa de erro do banco inteiro. A complementação por amostra aleatória proposta no gabarito §6 não foi feita.
""")
open(os.path.join(HERE, "validacao_gabarito_2026-09-19.md"), "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
