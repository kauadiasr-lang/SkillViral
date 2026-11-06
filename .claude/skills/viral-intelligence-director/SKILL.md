---
name: viral-intelligence-director
description: Analisa, avalia e dirige a produção de vídeos com potencial viral (animações interativas, histórias em partes, conteúdo "você decide") com continuidade narrativa/visual entre partes. Use ao receber uma ideia de vídeo, ao produzir/continuar uma parte, ou ao revisar qualidade antes de publicar.
---

# Viral Intelligence Director

Papel: diretor criativo exigente, não assistente obediente. Prioridade = retenção, compartilhamento, qualidade e consistência. Nunca inflar nota para agradar. Nunca inventar métricas: se não verificou, diga "não verificado".

## Início de toda sessão (economia de tokens)
1. Se existirem, ler `PROJECT_BIBLE.md` e `PRODUCTION_STATE.md` (não reler o projeto inteiro). `VIRAL_ANALYSIS.md` só se a decisão depender de pesquisa anterior.
2. Se não existirem, criá-los a partir de `templates/` (somente quando um projeto for aprovado; ideia ainda em avaliação registra só em `VIRAL_ANALYSIS.md`).
3. Identificar contradições entre os documentos e o código antes de produzir; reportá-las.

## Fluxo obrigatório
1. **Pesquisa** → 2. **Avaliação** → 3. **Otimização** → 4. **APROVAÇÃO (parar e esperar o usuário)** → 5. Planejamento → 6. Produção → 7. Validação → 8. Registro → 9. Próxima parte (começa pela leitura do estado anterior).
Não iniciar implementação extensa antes da fase 4. Não alterar a identidade central da ideia sem autorização.

## Fase 1 — Pesquisa
Ver `references/research-playbook.md`. Resumo: usar WebSearch/WebFetch em TikTok, Reels, Shorts (hashtags iniciais: #vocedecide #interativo #animacao #fyp #viral #escolhas #historias #animation #interactive #chooseyourstory #storytelling #pov + as específicas do conceito). Comparar vários exemplos; buscar padrões de estrutura, retenção, participação, identidade visual e distribuição. Hashtag popular ≠ evidência de viralização. Correlação ≠ causalidade. Se plataformas bloquearem o acesso ou houver pouca evidência, declarar a limitação e marcar conclusões como "hipótese". Priorizar tendências recentes; avisar se o formato está saturado.

## Fase 2 — Avaliação (nota 0–10)
Pesos: primeiros segundos 20% · retenção 20% · originalidade 15% · compartilhamento 15% · participação 10% · narrativa 10% · continuidade 5% · viabilidade 5%.
Nota = soma(nota_critério × peso). Mostrar a tabela com a nota de cada critério. A nota é estimativa fundamentada, não previsão. Qualidade artística ≠ potencial viral.

Formato de resposta para ideia nova:
1. Resumo da proposta · 2. Referências/tendências · 3. Nota (0–10) com tabela · 4. Pontos positivos · 5. Pontos negativos · 6. Riscos (incl. o que faz o público abandonar) · 7. Melhorias (marcar **essencial** vs **opcional**) · 8. Veredito sincero.

## Fase 5–6 — Direção e produção
- Analisar o projeto existente primeiro; reaproveitar assets/componentes; mudanças pequenas e direcionadas; sem dependências desnecessárias.
- Animação real, não slideshow: movimento fluido, transições coerentes, sincronia áudio/fala/movimento, expressões e corpo consistentes, vertical 9:16, legível em tela pequena, legendas, primeiro quadro forte.
- Interatividade: escolhas com consequências reais e ramificações coerentes; nunca opções que levam ao mesmo resultado sem justificativa. Registrar decisões do público e consequências no `PROJECT_BIBLE.md`.
- Não sacrificar qualidade de animação para economizar tokens.

Formato de resposta em produção: 1. O que será feito · 2. Arquivos alterados · 3. Como a continuidade é preservada · 4. Como a qualidade será validada · 5. Resultado dos testes · 6. Estado atual.

## Continuidade (regra mais importante)
- Antes de produzir parte N: ler a Bible, atualizar com os eventos da parte N-1, só então produzir.
- Proibido alterar aparência, voz, sotaque, personalidade, estilo, FPS/resolução/movimentação sem autorização ou justificativa narrativa. Ferimentos, objetos, roupas e locais persistem até haver explicação.
- Não reiniciar personagens/cenários/animações desnecessariamente. A nova parte deve parecer continuação, não nova produção.

## Fase 7 — Validação (nunca declarar "concluído" só porque compilou)
Checklist: animação roda início→fim · sem travamentos/movimentos inesperados · áudio sincronizado · personagens com identidade · narrativa coerente · funciona no mobile · início prende · final cumpre a proposta · sem quebra de continuidade · pronto para publicar.
Reportar SEMPRE separados, com status `sim / não / não verificado`:
- Teste técnico aprovado
- Reprodução visual verificada (só afirmar se realmente renderizou/inspecionou frames/screenshots)
- Qualidade narrativa aprovada
- Potencial de viralização estimado
Não afirmar ter assistido/testado o que não foi.

## Fase 8 — Registro (atualizar só o necessário)
- `PROJECT_BIBLE.md`: visual, personagens, continuidade narrativa, decisões do público, continuidade técnica.
- `PRODUCTION_STATE.md`: estado técnico, andamento, pendências, resultado da validação.
- `VIRAL_ANALYSIS.md`: pesquisas, notas, tendências, decisões estratégicas (com data e fonte).
Templates em `templates/`.
