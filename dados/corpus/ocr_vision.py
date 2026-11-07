"""OCR de PDFs digitalizados usando o framework Vision do macOS (local, sem custo de API).

Uso: ocr_vision.py <arquivo.pdf> <saida.txt> [escala]
"""
import sys
import Quartz
import Vision
from Foundation import NSURL


def ocr_pagina(page, escala=2.0):
    rect = Quartz.CGPDFPageGetBoxRect(page, Quartz.kCGPDFMediaBox)
    w, h = int(rect.size.width * escala), int(rect.size.height * escala)
    if w <= 0 or h <= 0:
        return ""

    cs = Quartz.CGColorSpaceCreateDeviceRGB()
    ctx = Quartz.CGBitmapContextCreate(
        None, w, h, 8, 0, cs, Quartz.kCGImageAlphaNoneSkipLast
    )
    Quartz.CGContextSetRGBFillColor(ctx, 1, 1, 1, 1)
    Quartz.CGContextFillRect(ctx, Quartz.CGRectMake(0, 0, w, h))
    Quartz.CGContextScaleCTM(ctx, escala, escala)
    Quartz.CGContextTranslateCTM(ctx, -rect.origin.x, -rect.origin.y)
    Quartz.CGContextDrawPDFPage(ctx, page)
    img = Quartz.CGBitmapContextCreateImage(ctx)
    if img is None:
        return ""

    linhas = []

    def handler(request, error):
        for obs in (request.results() or []):
            cand = obs.topCandidates_(1)
            if cand and len(cand):
                linhas.append(str(cand[0].string()))

    req = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(handler)
    req.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    req.setRecognitionLanguages_(["pt-BR", "en-US"])
    req.setUsesLanguageCorrection_(True)

    Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(img, None) \
        .performRequests_error_([req], None)
    return "\n".join(linhas)


def main():
    entrada, saida = sys.argv[1], sys.argv[2]
    escala = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0

    doc = Quartz.CGPDFDocumentCreateWithURL(
        NSURL.fileURLWithPath_(entrada)
    )
    n = Quartz.CGPDFDocumentGetNumberOfPages(doc)

    partes = []
    for i in range(1, n + 1):
        page = Quartz.CGPDFDocumentGetPage(doc, i)
        texto = ocr_pagina(page, escala)
        partes.append(f"\n\n===== [página {i}/{n}] =====\n{texto}")
        print(f"  pág {i}/{n} — {len(texto)} chars", file=sys.stderr)

    conteudo = "".join(partes)
    with open(saida, "w") as fh:
        fh.write(conteudo)
    print(f"OK {entrada} -> {saida}: {n} páginas, {len(conteudo)} chars")


if __name__ == "__main__":
    main()
