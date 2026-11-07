// Baixa os 24 acórdãos do universo final do TCC. VERSÃO 2 — corrige a rota docTP.
//
// O QUE MUDOU DA v1: existem duas rotas no STF. A v1 usava docTP=AC para todos,
// e por isso os 12 acórdãos mais novos devolveram 63 bytes de erro. Agora cada
// caso usa a sua (AC = acervo antigo digitalizado, TP = acervo eletrônico).
//
// COMO USAR — no SEU Chrome, não no browser do Claude:
//   1. Abra EXATAMENTE esta URL:
//
//        https://redir.stf.jus.br/paginadorpub/paginador.jsp?docTP=TP&docID=1
//
//      Ela mostra "Não foi possível acessar a peça do processo". É ISSO MESMO —
//      a página existe só para carregar a origem redir.stf.jus.br, e assim os
//      fetch abaixo ficam same-origin.
//
//      ⚠️ NÃO use uma URL de acórdão de verdade aqui. Ela devolve um ARQUIVO, a aba
//         NÃO navega, a origem nunca carrega, e todos os fetch são bloqueados por
//         CORS — sem baixar nada e sem aviso de downloads múltiplos. (Foi o erro
//         da instrução anterior.)
//
//   2. Cmd+Option+J → console
//   3. Cole este arquivo inteiro e Enter
//
//   ⚠️ O CHROME VAI BLOQUEAR DOWNLOADS MÚLTIPLOS. Na primeira vez que o segundo
//      arquivo tentar baixar, aparece um ícone na barra de endereço perguntando
//      sobre "Downloads automáticos". Clique e escolha PERMITIR — senão só o
//      primeiro arquivo chega ao disco (foi o que aconteceu na v1: o console
//      reportou 12 baixados, mas só o AP-375 ficou).
//
//   4. Os PDFs caem em ~/Downloads como AP-XXX.pdf
//
// Demora ~3 minutos. A AP-470 é a maior e pode levar bem mais — não feche a aba.
// Se preferir ir em lotes, rode com FATIA abaixo (ex.: ACORDAOS.slice(0, 8)).

const ACORDAOS = [
  // [nome, docTP, docID]
  ['AP-375',  'AC', 324305],    ['AP-365',  'AC', 324304],
  ['AP-348',  'AC', 474586],    ['AP-430',  'AC', 550425],
  ['AP-426',  'AC', 575801],    ['AP-447',  'AC', 594599],
  ['AP-433',  'AC', 611494],    ['AP-409',  'AC', 612756],
  ['AP-503',  'AC', 629986],    ['AP-396',  'AC', 622288],
  ['AP-372',  'AC', 621403],    ['AP-527',  'AC', 621404],
  ['AP-441',  'TP', 2156185],   ['AP-416',  'TP', 2187217],
  ['AP-470',  'TP', 3678648],   ['AP-565',  'TP', 5931475],
  ['AP-432',  'TP', 7081118],   ['AP-465',  'TP', 7065801],
  ['AP-508',  'TP', 757691311], ['AP-973',  'TP', 759914006],
  ['AP-940',  'TP', 760134371], ['AP-1032', 'TP', 760902735],
  ['AP-1025', 'TP', 770952853], ['AP-1036', 'TP', 772196537]
];

(async () => {
  // TRAVA: sem a origem certa, todo fetch é bloqueado por CORS e nada acontece.
  if (location.origin !== 'https://redir.stf.jus.br') {
    console.error(
      '%c PARE — origem errada. ',
      'background:#b00;color:#fff;font-weight:bold;font-size:14px'
    );
    console.error('Você está em: ' + location.origin);
    console.error('Abra primeiro: https://redir.stf.jus.br/paginadorpub/paginador.jsp?docTP=TP&docID=1');
    console.error('Essa página mostra uma mensagem de erro do STF — é o esperado. Depois cole o script de novo.');
    return;
  }

  const alvo = ACORDAOS; // troque por ACORDAOS.slice(0, 8) para ir em lotes
  const ok = [], falhou = [];

  for (const [nome, doctp, docid] of alvo) {
    try {
      const r = await fetch(
        `https://redir.stf.jus.br/paginadorpub/paginador.jsp?docTP=${doctp}&docID=${docid}`,
        { credentials: 'include' }
      );
      const blob = await r.blob();

      // O STF devolve 200 com 63 bytes de HTML quando a rota está errada.
      if (blob.size < 2000) {
        const txt = await blob.text();
        falhou.push(`${nome} — ${blob.size} bytes :: ${txt.replace(/\s+/g, ' ').slice(0, 70)}`);
        console.warn(`✗ ${nome} — ${blob.size} bytes`);
        continue;
      }

      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${nome}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 15000);

      ok.push(`${nome} — ${(blob.size / 1024 / 1024).toFixed(2)} MB`);
      console.log(`✓ ${nome} — ${(blob.size / 1024 / 1024).toFixed(2)} MB`);
      await new Promise(res => setTimeout(res, 2000)); // dá tempo ao disco e não martela o servidor
    } catch (e) {
      falhou.push(`${nome} — ${e}`);
      console.warn(`✗ ${nome}`, e);
    }
  }

  console.log(`\n=== BAIXADOS (${ok.length}/${alvo.length}) ===\n` + ok.join('\n'));
  if (falhou.length) console.log(`\n=== FALHARAM (${falhou.length}) ===\n` + falhou.join('\n'));
  console.log('\n⚠️ Confira em ~/Downloads quantos arquivos REALMENTE chegaram.');
  console.log('   Se vieram menos que o reportado acima, o Chrome bloqueou downloads múltiplos.');
})();
