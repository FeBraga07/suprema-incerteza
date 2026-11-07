# Congelamento dos dados da Fase 4, versão 2 — 24/10/2026

Sessão `72405cfe`, `claude-opus-5-5`. Substitui, como base da análise, a versão 1 (`CONGELAMENTO_2026-10-18.md`, 24 casos), que fica arquivada em `consolidado_v1_2026-10-18/`. Motivo: entrada da AP-307 (D-051) e gate das suas divergências A×B (D-052, decidido pelo Felipe em 24/10).

**Reprodutibilidade:** a execução de teste (pasta temporária da sessão) e a gravada em `consolidado/` deram saídas idênticas (`diff -r`). Fora da AP-307, as quatro tabelas são idênticas às da versão 1, linha por linha; as listas de conferência só ganham linhas da AP-307.

**Base:** 94 unidades ativas (74 no escopo Levcovitz), 174 questões ativas (64 concorreu, 63 tipicidade, 33 dolo, 11 ato de ofício, 3 outra), 1.704 posições (1.019 Absolve, 632 Condena, 45 Extingue, 8 Tranca). A AP-307 acrescenta 7 unidades, 14 questões, 112 posições e 42 precedentes.

**Daqui em diante, mudar qualquer arquivo abaixo exige decisão registrada em DECISOES.md e novo manifesto.**

Comando: `python3 fase4/consolidar_fase4.py fase4/extracao/lote/A fase4/extracao/lote/B fase4/extracao/lote/outra_polaridade_pareamento.psv ../derivados/2_casos_reus.psv ../derivados/1_casos.psv fase4/consolidado` (a partir de `dados/metodologia/`)

## Entradas
```
92389238a38c6643e0a25940dba3fa66 extracao/lote/A/AP-1025.json
52b5a3d9f6c4064f41e7834a4199faf9 extracao/lote/A/AP-1032.json
3a7d26652b84ff0a451faac5ea95b325 extracao/lote/A/AP-1036.json
b343cb83fb7794551f31220d962b57e3 extracao/lote/A/AP-307.json
ca1cb09e1c772379f6472e5b34f4e06f extracao/lote/A/AP-348.json
e63b435a65938c57e7f68c28f6cdfd1d extracao/lote/A/AP-365.json
02c909f0d17263c93d8b0cb3833e3d1c extracao/lote/A/AP-372.json
b4252662051a5994fa738034f9b4e709 extracao/lote/A/AP-375.json
f7e4d788456685c294afd8d3ff862a7f extracao/lote/A/AP-396.json
d5a6d9b976c6c96feffd0a92fd1d14de extracao/lote/A/AP-409.json
333deb7f7e0c6b4519e53bf4732fb19b extracao/lote/A/AP-416.json
1013e7cc4246501a3c2a3bdfea7c7da0 extracao/lote/A/AP-426.json
462c085e0550162101cd486a32fc727a extracao/lote/A/AP-430.json
1465a9b7c7190e462275e9db0aaa7917 extracao/lote/A/AP-432.json
e24f1e1fb3a5d8b3fe244482beaeb155 extracao/lote/A/AP-433.json
986f0d85f60d078b18dfc76211ec668e extracao/lote/A/AP-441.json
a69ce23265321b7ae80b7335c4266cfc extracao/lote/A/AP-447.json
81c45add34dec73d7f0149ae73cfc77d extracao/lote/A/AP-465.json
f0b007b68786043d4f899f9f98c73190 extracao/lote/A/AP-470.json
beeeceb2ad953a67199b9282ff18d351 extracao/lote/A/AP-503.json
902f78946b13d6c939007d47453c54f8 extracao/lote/A/AP-508.json
a854b04a5420a2f8acbf077c4a04f499 extracao/lote/A/AP-527.json
71dbd2b787c22851d6e37a1531558d27 extracao/lote/A/AP-565.json
efccf9035e0db41002a82958392f7934 extracao/lote/A/AP-940.json
c670abd43dfee44bfb851bb2ee791097 extracao/lote/A/AP-973.json
614866d64a5d3a7da1331eb109ffff13 extracao/lote/B/AP-1025.json
f76a3fa27677aa4a10f23469ec6d4cd5 extracao/lote/B/AP-307.json
592ff4384c4576292eef918e17c92be6 extracao/lote/B/AP-365.json
7f0843c88059a9233cc06c39bd4173b6 extracao/lote/B/AP-372.json
dc4d3ceec1dd8f655d5e4d411849e0f8 extracao/lote/B/AP-375.json
d72a78c69ad722140dc3b179f5c1ac07 extracao/lote/B/AP-409.json
a39156f9d85aa2e285376f22b7695f18 extracao/lote/B/AP-416.json
93a464b127582245f2ea3527c9825312 extracao/lote/B/AP-426.json
92cbbcfd090202ea60353a9ebcf2aabb extracao/lote/B/AP-430.json
2e5a531567a1c1affac0afbb08eed417 extracao/lote/B/AP-432.json
7cce2f35cb2d00dec0ceb3d48b13ee85 extracao/lote/B/AP-433.json
6b6cd8524484396f271fb30376d18da0 extracao/lote/B/AP-441.json
d4e18dc5d60a71e4c97f60ba3e904718 extracao/lote/B/AP-447.json
a1b62254ec4d3899bcc1a25c4781d2a7 extracao/lote/B/AP-465.json
d242f87e98f3aed4231350c4dce02b0b extracao/lote/B/AP-503.json
7df4b3ca59bf456abaa7f9302f05c557 extracao/lote/B/AP-565.json
0a735b66397650d4424c46d14c657b9d extracao/lote/B/AP-973.json
a358b214ebd5d1bcb1e037cb9183fddd extracao/lote/outra_polaridade_pareamento.psv
917dad538fb2afa68901cbef1077345f ../../derivados/2_casos_reus.psv
efb49d0982f048b863a9c6871fbe922c ../../derivados/1_casos.psv
d5fc46d807b96de8d636551b3f4199a6 ../../derivados/3_votos.psv
d3353d3334080e92c233d339108935b6 consolidar_fase4.py
c85eb98ecf8cda15600221f184309b3d CODEBOOK.md
5619e607539b9cf5f6f899e2570ee05a PROMPT_FASE4_v2.md
```

## Saídas
```
374571a03f970df0b33e8069852f8b06 consolidado/LOG_CONSOLIDACAO.md
e6a3967d242eee7eeb81ec99aa0afd50 consolidado/casos/AP-1025.json
e16902092a50117beebd942e314494d0 consolidado/casos/AP-1032.json
59e6cf05b1c0798159f87ec82da3945a consolidado/casos/AP-1036.json
8cb015339e0640326a2ef6932ff02fb7 consolidado/casos/AP-307.json
556faf30723342d4a4c52bf2956479a6 consolidado/casos/AP-348.json
da21f58fcb963cf48a5cb7223791121b consolidado/casos/AP-365.json
7cbcd53992828933bd42de9205c86e80 consolidado/casos/AP-372.json
b662d2d934acb86957c1ab2f352f1af6 consolidado/casos/AP-375.json
d5b422d81d341f1dcaea80b5113b14f6 consolidado/casos/AP-396.json
7f0149309fc9065aafda046d7d1d06f8 consolidado/casos/AP-409.json
3974cddc25b95d5f31fa118e483ae755 consolidado/casos/AP-416.json
8277ef2eee8e0bbdb1b0aa6b68fd6186 consolidado/casos/AP-426.json
34cd53b16b15200e93d744b63b671ba7 consolidado/casos/AP-430.json
3f48f4d14cad5df4c71e2ffc1a31d08f consolidado/casos/AP-432.json
abb36e601a5afd4ca80ddcd2bbbdd3ff consolidado/casos/AP-433.json
55dc6ed56291b1bfc1cddc0fff093987 consolidado/casos/AP-441.json
ef0ef8d4c56fd5cfd204c1b7b749550a consolidado/casos/AP-447.json
3d89fd641350dc6f23c37cda9704b6b1 consolidado/casos/AP-465.json
8dfc4c566335998a2b988c94292a23d7 consolidado/casos/AP-470.json
4217b264e4d3b37d680b80571963a44b consolidado/casos/AP-503.json
cc91abbd2d70c5c6845b03a7da422942 consolidado/casos/AP-508.json
b1f4c8bc8695c86dc074bd41b00978df consolidado/casos/AP-527.json
d0fbfb254f693d3a1080b0911cbb9622 consolidado/casos/AP-565.json
16d2a458256ee970ba0d4e21af003a53 consolidado/casos/AP-940.json
dad619d4993ee692deca3d89f360ed42 consolidado/casos/AP-973.json
5e16048e70f815b2c25474f4e0efa94c consolidado/conferencia/coerencia_marca_voto.psv
3284dca6d4654833175fa2f08ede26e1 consolidado/conferencia/cruzamento_motivo.psv
9e3efd074008dcb7569dc8fe54808d19 consolidado/conferencia/precedentes_filtro.psv
e8db4585f062e2a575b2cc509ef99721 consolidado/conferencia/r11_divergencias_enfrentou.psv
ce880b895e494e81c5ef9574f8d08c0d consolidado/conferencia/r12_todas_as_unidades.psv
97d148796e4908373f3f3ebb8b873d76 consolidado/conferencia/r8_aplicada.psv
0cff6daf7862ff2f14055497daf058c1 consolidado/conferencia/reclassificacao_outra.psv
24060b2d0f7dc3bbf7cbbe62e42549f2 consolidado/fase4_posicoes.psv
b7cb2caa8a6a13e1e7f3921ea026099f consolidado/fase4_precedentes.psv
e24577aa5b16f91b50261a5ea3c848c1 consolidado/fase4_questoes.psv
a7ed861c2da3bed629744ee8679d56f0 consolidado/fase4_unidades.psv
```
