# Rubrica de pontuação (usada na Fase 2)

Regra-mãe: pontuar **o que está descrito/planejado**, não o que a execução "poderia" ser. Gancho não definido → nota baixa em "primeiros segundos", com a melhoria listada à parte.
Calcular SEMPRE com o script (não somar de cabeça):
`python3 scripts/vid.py score fs=_ ret=_ orig=_ share=_ part=_ narr=_ cont=_ viab=_ evidence=low|medium|high`
Pesos: fs 20 · ret 20 · orig 15 · share 15 · part 10 · narr 10 · cont 5 · viab 5. **Teto**: fs<4 ou ret<4 → nota final ≤ 6,0 (gancho ou retenção quebrados invalidam o resto).

## Âncoras (use inteiros 0–10; justifique em 1 linha por critério)
| Nota | Significado geral |
|---|---|
| 0–2 | Ausente ou contraproducente (nada que prenda / nenhuma escolha real) |
| 3–4 | Genérico: igual a milhares de vídeos, sem diferencial identificável |
| 5–6 | Competente: cumpre o básico, 1 elemento de destaque |
| 7–8 | Forte: diferencial claro e específico, bem executável |
| 9–10 | Excepcional e raro. Exige evidência (referências verificadas); sem evidência, máx. 8 |

Específicos:
- **fs**: 0–3s têm imagem + pergunta/conflito concreto? "Personagem cumprimenta" = 2. Quadro 1 já mostra o conflito = 7+.
- **ret**: existe pergunta aberta que só fecha no fim? mudança visual/de informação a cada ~3s? Promessa cumprida?
- **orig** (âncora, não é teto): "porta misteriosa / fugir ou entrar" sem twist = 3. Original ≠ estranho: precisa ser compreensível em 2s.
- **share**: alguém marcaria/enviaria? Qual a frase de envio ("olha o final")?
- **part**: a escolha é clara, binária/curta, de baixo atrito (uma palavra no comentário) e muda algo visível depois? Escolha decorativa = ≤3.
- **narr**: causa→consequência, personagem quer algo, final cumpre a promessa.
- **cont**: ganchos e estados que sustentam as próximas partes (não precisa haver continuação para valer ≥5 se bem estruturado).
- **viab**: executável com a stack atual com qualidade de animação real (não slideshow). Ideia trivial de fazer NÃO ganha nota alta por isso se for vazia.

## Confiança (`evidence=`)
Obter com `python3 scripts/vid.py evidence VIRAL_ANALYSIS.md` (conta as etiquetas das referências R#):
- **high**: ≥5 referências `[OBS]`/`[CONF]` comparáveis.
- **medium**: 2–4 `[OBS]`/`[CONF]`, ou ≥5 `[USR]` (descrições do usuário não vistas por mim).
- **low**: o resto. `[REL]` (blog/busca) nunca conta. Nota = estimativa preliminar; dizer isso no veredito.
Nunca converter nota em previsão de views.

## Calibração e recalibração
1. Ao publicar, copiar a nota (E#) para `nota_prevista` e os 8 valores para `criterios` (`fs=7,ret=6,…`) em VIDEO_PERFORMANCE, com `origem=real`.
2. `python3 scripts/vid.py perf VIDEO_PERFORMANCE.md --calibrate`: Spearman nota×taxa de share e, por critério, correlação com o resultado. Views não entram (dependem do tamanho da conta).
3. Regras: <8 vídeos reais = não calibra. 8–14 = só observar (instável). ≥15 = pode propor ajuste de âncoras/pesos.
4. Proposta de ajuste = registrar em VIRAL_ANALYSIS (Decisões) com n, rho e confusores; aplicar só com aprovação do usuário. Nunca alterar pesos para "acertar" um vídeo. Correlação baixa de um critério pode ser mensuração ruim, não critério inútil.
