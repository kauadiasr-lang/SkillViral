# VIDEO_PERFORMANCE — <título/conta>
_Resultados reais publicados. `origem` = real | sintetico. Dados sintéticos/de teste NÃO entram neste arquivo (ficam em tests/fixtures; o script exclui linhas com origem sintetica e recusa arquivo cujo título comece com '# DADOS SINTÉTICOS'). Só dados fornecidos pelo usuário ou lidos de fonte acessível. Campo vazio = n/d (nunca 0, nunca estimado)._

## Regras de análise
- Rodar `python3 scripts/vid.py perf VIDEO_PERFORMANCE.md --by <coluna>`: calcula taxas por view (likes, coment., shares, saves) e medianas; não somar de cabeça.
- O script compara apenas dentro de estratos (plataforma × faixa de duração). Comparação exige ≥2 grupos com ≥3 vídeos com views no estrato; liderança exige >10% de diferença. 3–4 por grupo = hipótese; ≥5 = indício; "recorrente" = mesmo líder em ≥2 estratos. Tudo correlacional; nunca "causou".
- Antes de atribuir diferença a um elemento (gancho, formato…), listar confusores disponíveis: duração, horário, seguidores_conta, distribuição, tema, nº de partes. Views <1000 = ruído alto.
- Dados parciais são válidos: analisar o que existe e dizer o que falta. Métricas ausentes não bloqueiam o registro.
- Ao ler: usar o script (tabela inteira) + a seção "Hipóteses". Não ler vídeo a vídeo.
- Recalibrar a rubrica: `--calibrate` (regras em references/scoring-rubric.md).
- Vincular ao planejado: `nota_prevista` = nota E# de VIRAL_ANALYSIS (para calibrar a rubrica).

## Vídeos
| id | origem | data | plataforma | formato | dur_s | tema | gancho | narrativa | partes | views | likes | comentarios | shares | saves | ret_media_pct | conclusao_pct | seguidores_novos | seguidores_conta | nota_prevista | criterios | contexto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
<!-- exemplo (apagar): | V1 | real | 2026-01-03 | tiktok | escolha-comentarios | 30 | porta | pergunta | misterio | 1 | | | | | | | | | 800 | 4.4 | fs=4,ret=4,orig=3,share=4,part=7,narr=4,cont=6,viab=7 | hora 20h; sem impulsionar | -->

## Hipóteses (atualizar só com evidência nova)
| H# | hipótese | status (aberta/apoiada/refutada) | vídeos (ids) | n por grupo | confusores não controlados | recomendação atual |
|---|---|---|---|---|---|---|
