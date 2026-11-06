# Verificação visual de continuidade

Independente da ferramenta de produção (código, editor de vídeo, gerador de imagem, motion). Entrada = qualquer export: MP4/GIF, sequência PNG, render de Lottie/SVG. Texto no canon não basta: o que está no vídeo precisa ser visto.

## 1. Materiais de referência (criados na Parte 1, citados no canon)
- Folha do personagem: 1 imagem neutra de frente (+ perfil se houver) com fundo liso. Canon: `ref.<nome> = assets/ref/<nome>.png`.
- Folha de cenário: 1 quadro-chave por cenário/iluminação. Canon: `ref.scene.<nome> = …`.
- Objetos importantes: 1 recorte limpo. Canon: `ref.obj.<nome> = …`.
Ausente → dizer que a verificação visual é impossível para aquele item; não aprovar por texto.

## 2. Extrair quadros-chave da parte
`python3 scripts/visual.py frames PARTE.mp4 out/kf --every 1` (ffmpeg), ou exportar quadros no próprio software. Escolher também 1 quadro por cena e 1 por mudança de estado (ferimento, objeto novo). Se só há código sem render, renderizar antes: sem render = "reprodução visual não verificada".

## 3. Métricas objetivas (deriva global)
- `python3 scripts/visual.py metrics REF.png QUADRO.png [--palette #hex,...]` → alerta de **cor nova/ausente, iluminação, contraste, resolução**.
- `python3 scripts/visual.py probe PARTE.mp4 --fps <tech.fps> --size <tech.resolution>` → fps, tamanho, duração, áudio medidos.
Limiares são heurísticos, testados só com imagens sintéticas planas. Em animação real (gradiente, sombra, anti-aliasing) podem gerar falso positivo/negativo: ajustar `--min-frac`, registrar o ajuste no PRODUCTION_STATE.
**Não detectam**: proporção, rosto/expressão, pose errada, objeto pequeno, personagem trocado por outro de mesmas cores, estilo de traço.

## 4. Revisão visual guiada (obrigatória; é aqui que se verifica identidade)
1. `python3 scripts/visual.py sheet out/sheet.png REF.png Q1.png Q2.png … [--crop x0,y0,x1,y1]` (primeiro painel = referência; `--crop` em frações amplia um detalhe).
   **Objetos pequenos (chaves, curativos, acessórios) exigem SEMPRE uma folha com `--crop` sobre a região onde deveriam estar**; na folha inteira passam despercebidos (testado).
2. **Ver a imagem** (modelo com visão ou pessoa) e preencher, por chave do canon aplicável, `ok / divergente / não visível / não verificável`: aparência, roupa, proporção, cor, objeto presente e na posição certa, ferimento, iluminação, cenário, posição relativa dos personagens, estilo do traço.
3. Uma chave só é `ok` se o item está **visível** no quadro examinado. `não visível` não é aprovação.
4. Registrar no PRODUCTION_STATE: quadros examinados, o que foi `divergente`, o que ficou `não verificável`. Se a imagem não foi realmente vista, escrever "reprodução visual NÃO verificada".

## 5. Características de animação (o que um quadro parado não mostra)
- Medível: fps, duração, resolução, áudio presente (`probe`).
- Não medido por estas ferramentas: easing, timing, transições, comportamento da câmera, sincronia fala/boca. Exigem assistir/reproduzir; comparar com os valores `tech.motion` e `tech.camera`. Sem reprodução, declarar "movimento não verificado".

## 6. Decisão
Qualquer `divergente` sem justificativa no manifesto (`~ narrative:` / `~ user-approved`) bloqueia a publicação. Diferença visual real que o texto não previa → corrigir o asset ou, se for mudança desejada, atualizar o canon com autorização.

## 7. Resultados dos testes desta metodologia (imagens sintéticas planas; não há asset real)
- Métricas: sem alerta em pose/posição diferente e JPEG; alerta em roupa de cor errada, iluminação, elemento novo e resolução. Não detectam objeto pequeno nem mudança de tamanho do personagem.
- Revisão visual cega por agente independente: identificou roupa, iluminação, objeto ausente (com `--crop`) e apontou diferença de escala/posição no quadro que o autor tratou como variação aceitável: a revisão visual é mais estrita e subjetiva; **definir no canon a tolerância** (distância de câmera permitida, escala mínima/máxima) para evitar discordâncias.
