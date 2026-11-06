# Research playbook (Fase 1)

Objetivo: padrões recorrentes, não anedotas. Meta: ≥5 vídeos comparáveis por ideia. Se não houver, dizer quantos foram de fato observados e rebaixar a confiança (ver scoring-rubric).

## Etiquetas de evidência (obrigatórias em cada afirmação registrada)
- `[OBS]` observado por mim na fonte primária: página/vídeo aberto, ou **imagem/print/quadro fornecido que eu vi** (o que aparece nele; métricas visíveis valem 'como exibidas no print', sem auditoria).
- `[CONF]` confirmado: fonte oficial da plataforma ou ≥2 fontes independentes.
- `[USR]` informado pelo usuário (link, descrição, métrica) sem que eu tenha visto a mídia. Vale como dado do usuário, não como observação minha.
- `[REL]` relato de terceiros ou resumo de busca/blog, sem acesso à fonte. Vale como pista, não como fato.
- `[INT]` minha interpretação de algo `[OBS]`/`[CONF]`.
- `[HIP]` hipótese não testada.
- `[N/D]` indisponível (bloqueado, login, sem dado). Nunca preencher com estimativa.

## Escada de acesso (tentar nesta ordem; parar ao falhar por rede/login)
1. Acesso direto à plataforma (hashtag/URL de vídeo). Se o host não resolve, exige login ou o proxy responde 403/bloqueio genérico → registrar `[N/D]` + motivo, **sem retentar nem usar rotas alternativas de acesso**; não repetir em outros endereços da mesma plataforma. Tentar uma plataforma bloqueada não obriga a tentar as demais: registrar as não tentadas como `[N/D]` (não tentada).
2. Busca web por exemplos citados em imprensa/blogs/páginas de criadores → `[REL]`.
3. Recursos oficiais da plataforma (ex.: enquetes em comentários, séries) → `[CONF]` só se a página oficial foi lida.
4. Referências do usuário (protocolo abaixo).
Se só chegar ao degrau 2–3: entregar avaliação com `evidence=low`, e dizer o que o usuário pode fornecer para subir a confiança. Se a ideia for original demais para ter comparáveis: comparar por **componentes** (gancho, mecânica de escolha, estilo) e declarar "sem comparável direto".

## Registro de cada referência (tabela em VIRAL_ANALYSIS)
`R# | plataforma | formato | link/fonte | data acesso | gancho | o que prende | participação | visual | semelhança/diferença | métricas (só se visíveis) | etiqueta`
Hashtag popular ≠ evidência de viralização. Viés de sobrevivência: só vemos o que o algoritmo mostrou. Correlação ≠ causa.

## Maturidade do formato
emergente / crescimento / saturado / evergreen — sempre com etiqueta; sem dados → `[HIP]`.

## Referências fornecidas pelo usuário (caminho legítimo quando não há acesso)
Nunca contornar bloqueio, login ou restrição de plataforma. O usuário pode fornecer:
- **Prints/quadros/GIF/vídeo do próprio arquivo** → eu vejo → registrar o que está visível como `[OBS]` (ex.: gancho em 0–2s, texto na tela, tipo de escolha, estilo visual, contadores visíveis "como exibidos").
- **Link sem mídia** → registrar link + o que o usuário descreveu como `[USR]`; não descrever o conteúdo do vídeo além disso. Se o host estiver acessível por fonte pública/oficial (ex.: página pública, oEmbed oficial, API oficial com chave do próprio usuário), usar e etiquetar `[OBS]`/`[CONF]` conforme o caso; senão `[N/D]`.
- **Exportações das métricas da própria conta** (analytics, CSV) → VIDEO_PERFORMANCE (origem=real).
Pedido mínimo útil: 5 vídeos, cada um com link + print do início + o que o usuário acha que funciona, e se possível métricas visíveis.
Fluxo: registrar R# com etiqueta → `python3 scripts/vid.py evidence VIRAL_ANALYSIS.md` → usar o `evidence=` resultante em `vid.py score`.
Fontes de metadados oficiais citadas em busca (TikTok oEmbed; YouTube Data API `videos.list`) **não foram verificadas nem testadas** (hosts bloqueados neste ambiente): confirmar na documentação oficial antes de depender delas.
