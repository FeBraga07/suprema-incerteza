#!/usr/bin/env python3
"""Gera os prompts do lote da Fase 4 (D-040, D-044) a partir de PROMPT_FASE4.md.

Uso: python3 dados/metodologia/fase4/gerar_prompts_lote.py
Saída: fase4/prompts_lote/{A,B}/AP-XXX.md (prompt literal de cada agente).
Escopo Levcovitz por unidade: Nao quando a imputação é art. 288 do CP, art. 299 do CP,
Lei 9.613/1998 ou Lei 8.429/1992, ou quando a unidade já diz "fora do escopo"; Sim nos demais.
"""
import csv, os, re
from collections import defaultdict, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
F4 = os.path.join(ROOT, "dados/metodologia/fase4")
DUPLA = ["AP-426", "AP-409", "AP-503", "AP-416", "AP-441", "AP-432", "AP-973",   # DL 201/67
         "AP-430", "AP-465", "AP-1025", "AP-375", "AP-365", "AP-372", "AP-447",   # réus recorrentes
         "AP-565", "AP-433"]  # D-047 (14/10): placar apertado e confiança baixa na leitura A
AP470_REUS = {f"AP-470-R{i}" for i in range(14, 24)}

def fora(u):
    t = (u["artigo"] + " " + u["diploma"]).lower()
    return bool(re.search(r"288|9\.613|8\.429|\b299\b|fora do escopo", t))

def main():
    corpo = open(os.path.join(F4, "PROMPT_FASE4.md"), encoding="utf-8").read()
    corpo = corpo.split("=====INÍCIO=====\n", 1)[1].split("\n=====FIM=====", 1)[0]
    unidades = OrderedDict()
    for u in csv.DictReader(open(os.path.join(F4, "unidades_reu_fato.psv"), encoding="utf-8"), delimiter="|"):
        if u["id_caso"] == "AP-470":
            # D-040: só corrupção passiva do item VI (R14–R23, imputação 1)
            if u["id_caso_reu"] not in AP470_REUS or not u["id_unidade"].endswith("-I01"):
                continue
        unidades.setdefault(u["id_caso"], []).append(u)
    votos = defaultdict(lambda: defaultdict(list))
    for v in csv.DictReader(open(os.path.join(ROOT, "dados/derivados/3_votos.psv"), encoding="utf-8"), delimiter="|"):
        votos[v["id_caso"]][v["id_caso_reu"]].append(v)
    n_unid = {"A": 0, "B": 0}
    for leitor in ("A", "B"):
        os.makedirs(os.path.join(F4, "prompts_lote", leitor), exist_ok=True)
        os.makedirs(os.path.join(F4, "extracao/lote", leitor), exist_ok=True)
        for caso, us in unidades.items():
            if leitor == "B" and caso not in DUPLA:
                continue
            n_unid[leitor] += len(us)
            txt = os.path.join(ROOT, f"dados/corpus/texto/{caso}.txt")
            n_pag = open(txt, encoding="utf-8").read().count("===== [página")
            if n_pag == 0:
                arquivo = (f"{os.path.join(ROOT, f'dados/corpus/pdf/{caso}.pdf')}` (PDF; o texto extraído deste caso "
                           f"não tem marcadores de página, então leia o PDF, cuja página é a do leitor de PDF. "
                           f"O texto sem marcadores está em `{txt}`, se ajudar a buscar")
            else:
                arquivo = txt + "` (texto integral; as páginas estão marcadas como `===== [página N/M] =====`, e a página do PDF é esse N"
            linhas_u = []
            for u in us:
                esc = "Nao" if fora(u) else "Sim"
                linhas_u.append(f"  - `{u['id_unidade']}`: {u['nome_reu']}, imputação {u['n_imputacao']}: "
                                f"{u['artigo']} ({u['diploma']}). Escopo Levcovitz: **{esc}**")
            reus = OrderedDict((u["id_caso_reu"], u["nome_reu"]) for u in us)
            linhas_v = []
            for r, nome in reus.items():
                vs = votos[caso].get(r, [])
                por_fato = defaultdict(list)
                for v in vs:
                    por_fato[v["fato"] or "(sem separação por fato no banco)"].append(f"{v['ministro']}: {v['voto_resultado']}")
                for fato, lst in por_fato.items():
                    linhas_v.append(f"  - {r} {nome} — {fato}: {len(lst)} votantes. " + "; ".join(lst))
            extra = ""
            mapa = os.path.join(F4, f"mapa_votos/{caso}.psv")
            if os.path.exists(mapa):
                extra += (f"\n- **Mapa de páginas das peças (permitido, só estrutura):** `{mapa}`. Diz onde começa e termina "
                          f"cada voto e quais réus ele abrange. Use para navegar; ele não contém categoria. Não abra o arquivo `_notas.md` ao lado.")
            if caso == "AP-470":
                extra += ("\n- **AP-470 (8.405 pp.):** leia só o item VI, corrupção passiva. Votos de mérito: Joaquim Barbosa "
                          "(p. 3476-3703), Ricardo Lewandowski (p. 3728-3920 e aditamentos), Dias Toffoli (p. 4158-4355), Luiz Fux e "
                          "Gilmar Mendes (ver mapa), Rosa Weber C.6, Cármen Lúcia VII, Marco Aurélio, Celso de Mello e Ayres Britto "
                          "(p. 4499-4590); ata do item VI (p. 4996) e ata final (p. 8380-8383). Navegue pelos títulos de réu dentro de "
                          "cada voto ('RÉU:', nome do acusado, VI.1-VI.4). Cezar Peluso não votou no item VI (já aposentado): não crie "
                          "posição para ele.")
            saida = os.path.join(F4, f"extracao/lote/{leitor}/{caso}.json")
            t = (corpo.replace("{CASO}", caso).replace("{ARQUIVO_TEXTO}", arquivo)
                 .replace("{UNIDADES}", "\n".join(linhas_u)).replace("{VOTOS}", "\n".join(linhas_v) + extra)
                 .replace("{SAIDA}", saida))
            assert not re.search(r"\{[A-Z_]+\}", t), caso
            open(os.path.join(F4, "prompts_lote", leitor, f"{caso}.md"), "w", encoding="utf-8").write(t + "\n")
    print("unidades A:", n_unid["A"], "| unidades B:", n_unid["B"])
    print("casos A:", len(unidades), "| casos B:", len(DUPLA))

if __name__ == "__main__":
    main()
