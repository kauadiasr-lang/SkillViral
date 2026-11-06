#!/usr/bin/env bash
# Testes reproduzíveis do scripts/vid.py com fixtures FICTÍCIAS. Uso: bash tests/run_tests.sh
cd "$(dirname "$0")/.." || exit 2
S="python3 scripts/vid.py"; F=tests/fixtures; T=templates; pass=0; fail=0
t() { # nome esperado_exit "comando" [padrão_grep]
  out=$(eval "$3" 2>&1); code=$?
  if [ "$code" = "$2" ] && { [ -z "$4" ] || echo "$out" | grep -q -- "$4"; }; then pass=$((pass+1)); echo "PASS $1"; else fail=$((fail+1)); echo "FAIL $1 (exit=$code, esperado $2)"; echo "$out" | head -5; fi
}
cnt() { eval "$1" 2>&1 | grep -c "$2"; }
t "continuidade: manifesto com erros reprova" 1 "$S continuity $F/bible_part1.md $F/manifest_part2_bad.md" "REPROVADO (7"
t "continuidade: 6 MISMATCH + 1 MISSING detectados" 0 "[ \$(cnt '$S continuity $F/bible_part1.md $F/manifest_part2_bad.md' '^MISMATCH') = 6 ] && [ \$(cnt '$S continuity $F/bible_part1.md $F/manifest_part2_bad.md' '^MISSING') = 1 ]"
t "continuidade: manifesto corrigido aprova" 0 "$S continuity $F/bible_part1.md $F/manifest_part2_good.md" "APROVADO"
t "continuidade: voz com justificativa narrativa NÃO basta" 1 "$S continuity $F/bible_part1.md $F/manifest_voice_narrative.md" "exige '~ user-approved'"
t "continuidade: voz com user-approved passa" 0 "$S continuity $F/bible_part1.md $F/manifest_voice_approved.md" "APROVADO"
t "continuidade: remoção justificada de objeto passa" 0 "$S continuity $F/bible_part1.md $F/manifest_key_removed.md" "REMOVED"
t "continuidade: escopo limita a verificação" 1 "$S continuity $F/bible_part1.md $F/manifest_part2_bad.md --scope char.pip" "REPROVADO (3"
t "continuidade: canon vazio -> não verifica" 3 "$S continuity $F/bible_empty.md $F/manifest_part2_good.md" "SEM CANON"
t "continuidade: template cru do Bible -> não verifica" 3 "$S continuity $T/PROJECT_BIBLE.md $F/manifest_part2_good.md" "SEM CANON"
t "continuidade: canon contraditório aborta" 2 "$S continuity $F/bible_conflict.md $F/manifest_part2_good.md" "CONFLITO NO CANON"
t "continuidade: arquivo ausente" 3 "$S continuity $F/nao_existe.md $F/manifest_part2_good.md" "ARQUIVO AUSENTE"
t "continuidade: @unchanged explícito é aceito, mas sinalizado como não verificado" 0 "$S continuity $F/bible_part1.md $F/manifest_unchanged.md" "ATENÇÃO: 2 item"
t "continuidade: @unchanged em chave inexistente reprova" 1 "$S continuity $F/bible_part1.md $F/manifest_unchanged_bad.md" "chave inexistente"
t "evidence sem argumento: erro limpo, sem traceback" 2 "$S evidence | grep -q Traceback && exit 9 || $S evidence" "ARGUMENTOS FALTANDO"
t "score: ideia fraca 2.10" 0 "$S score fs=2 ret=2 orig=1 share=2 part=2 narr=1 cont=2 viab=9 evidence=low" "NOTA FINAL: 2.10"
t "score: porta 4.40" 0 "$S score fs=4 ret=4 orig=3 share=4 part=7 narr=4 cont=6 viab=7 evidence=low" "NOTA FINAL: 4.40"
t "score: elaborada 6.55" 0 "$S score fs=7 ret=6 orig=6 share=6 part=8 narr=7 cont=8 viab=5 evidence=low" "NOTA FINAL: 6.55"
t "score: teto 6.00 com gancho fraco" 0 "$S score fs=3 ret=9 orig=9 share=9 part=9 narr=9 cont=9 viab=9 evidence=high" "NOTA FINAL: 6.00"
t "score: nota fora de faixa rejeitada" 2 "$S score fs=11 ret=4 orig=3 share=4 part=7 narr=4 cont=6 viab=7 evidence=low" "fora de 0"
t "score: exige evidence" 2 "$S score fs=4 ret=4 orig=3 share=4 part=7 narr=4 cont=6 viab=7" "evidence"
SY="--include-synthetic"
t "perf: arquivo marcado SINTÉTICO é recusado sem flag" 3 "$S perf $F/performance_strata.md" "ARQUIVO SINTÉTICO"
t "perf: arquivo misto exclui só linhas sintéticas" 0 "$S perf $F/performance_mixed.md" "1 linha(s) com origem sintética EXCLUÍDA"
t "perf: flag deixa claro que são dados sintéticos" 0 "$S perf $F/performance_strata.md $SY" "DADOS SINTÉTICOS INCLUÍDOS"
t "perf: sem grupos suficientes -> sem comparação" 0 "$S perf $F/performance_synthetic.md $SY" "sem comparação"
t "perf: vazio != zero (S5 sem views)" 0 "$S perf $F/performance_synthetic.md $SY" "S5 .*views=n/d"
t "perf: vazio não conclui" 3 "$S perf $F/perf_empty.md" "SEM DADOS"
t "perf: template cru não conclui" 3 "$S perf $T/VIDEO_PERFORMANCE.md" "SEM DADOS"
t "perf: estratos comparáveis -> hipótese" 0 "$S perf $F/performance_strata.md $SY" "HIPÓTESE"
t "perf: recorrência em 2 estratos" 0 "$S perf $F/performance_strata.md $SY" "share: 'escolha' lidera em 2 estratos"
t "perf: empate não vira liderança (like)" 1 "$S perf $F/performance_strata.md $SY | grep -q 'like: .*lidera'" ""
t "perf: confusor de conta é avisado" 0 "$S perf $F/performance_confound.md $SY" "tamanho da conta variou"
t "perf: não afirma causa" 0 "$S perf $F/performance_strata.md $SY" "associação não é causa"
t "perf: calibração <8 vídeos recusa" 0 "$S perf $F/performance_calib_small.md $SY --calibrate" "INSUFICIENTE"
t "perf: calibração com 10 vídeos calcula rho e avisa instável" 0 "$S perf $F/performance_calib.md $SY --calibrate" "n<15: instável"
t "perf: calibração por critério" 0 "$S perf $F/performance_calib.md $SY --calibrate" "critério part: rho=-1.00"
t "evidence: REL/USR/1 OBS -> low" 0 "$S evidence $F/va_refs_low.md" "evidence=low"
t "evidence: 4 OBS/CONF -> medium" 0 "$S evidence $F/va_refs_high.md" "evidence=medium"
t "evidence: template cru -> low" 0 "$S evidence $T/VIRAL_ANALYSIS.md" "evidence=low"
t "section: TOC" 0 "$S section $T/PROJECT_BIBLE.md --toc" "Canon"
t "section: extrai só a seção" 0 "$S section $F/bible_part1.md Canon | grep -c 'char.pip.outfit'" "1"

# ---- visual (Pillow/ffmpeg opcionais) ----
V="python3 scripts/visual.py"; IMG=$(mktemp -d)
if python3 -c "import PIL" 2>/dev/null; then
  python3 tests/make_images.py "$IMG"
  t "visual: pose/posição diferente NÃO gera alerta" 0 "$V metrics $IMG/ref.png $IMG/ok_moved.png" "sem alertas"
  t "visual: recompressão JPEG NÃO gera alerta" 0 "$V metrics $IMG/ref.png $IMG/ok_jpeg.jpg" "sem alertas"
  t "visual: cachecol de cor errada detectado" 1 "$V metrics $IMG/ref.png $IMG/bad_red_scarf.png" "COR NOVA"
  t "visual: iluminação alterada detectada" 1 "$V metrics $IMG/ref.png $IMG/bad_bright.png" "ILUMINAÇÃO"
  t "visual: elemento novo detectado" 1 "$V metrics $IMG/ref.png $IMG/bad_extra_creature.png" "COR NOVA"
  t "visual: resolução diferente detectada" 1 "$V metrics $IMG/ref.png $IMG/bad_size.png" "RESOLUÇÃO"
  t "visual: LIMITE CONHECIDO objeto pequeno NÃO é detectado por métricas" 0 "$V metrics $IMG/ref.png $IMG/bad_no_key.png" "NÃO prova"
  t "visual: folha gerada" 0 "$V sheet $IMG/s.png $IMG/ref.png $IMG/bad_no_key.png --crop 0.45,0.6,0.85,0.9" "folha salva"
  t "visual: arquivo ausente" 3 "$V metrics $IMG/nada.png $IMG/ref.png" "AUSENTE"
else echo "SKIP visual (Pillow ausente)"; fi
if command -v ffprobe >/dev/null && [ -f "$IMG/video_24fps.mp4" ]; then
  t "probe: fps/tamanho conforme canon" 0 "$V probe $IMG/video_24fps.mp4 --fps 24 --size 360x640" "coerentes"
  t "probe: fps divergente detectado" 1 "$V probe $IMG/video_30fps.mp4 --fps 24" "FPS"
  t "frames: extrai quadros-chave" 0 "$V frames $IMG/video_24fps.mp4 $IMG/kf --every 1" "3 quadro"
else echo "SKIP probe/frames (ffmpeg ou Pillow ausente)"; fi
rm -rf "$IMG"
echo "RESULTADO: $pass passaram, $fail falharam"; [ "$fail" = 0 ]
