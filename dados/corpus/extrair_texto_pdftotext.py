"""Extrai texto de PDF nativo via pdftotext (Poppler), com marcador de página.

Corrige o defeito do pdf-inspector, que produziu apenas os rótulos de navegação
(bookmarks) para 12 dos 13 acórdãos `text_based` — sem nenhum parágrafo de corpo.
Ver DECISOES.md D-017.

Uso: extrair_texto_pdftotext.py <arquivo.pdf> <saida.txt>
"""
import subprocess
import sys


def main():
    entrada, saida = sys.argv[1], sys.argv[2]

    bruto = subprocess.run(
        ["pdftotext", entrada, "-"], capture_output=True, check=True
    ).stdout.decode("utf-8", errors="replace")

    paginas = bruto.split("\f")
    if paginas and paginas[-1].strip() == "":
        paginas = paginas[:-1]
    n = len(paginas)

    partes = [f"\n\n===== [página {i}/{n}] =====\n{texto}" for i, texto in enumerate(paginas, 1)]
    conteudo = "".join(partes)

    with open(saida, "w") as fh:
        fh.write(conteudo)
    print(f"OK {entrada} -> {saida}: {n} páginas, {len(conteudo)} chars")


if __name__ == "__main__":
    main()
