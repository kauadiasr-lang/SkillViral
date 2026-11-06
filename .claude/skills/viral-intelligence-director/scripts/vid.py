#!/usr/bin/env python3
"""viral-intelligence-director helper (stdlib only).

  vid.py score fs=.. ret=.. orig=.. share=.. part=.. narr=.. cont=.. viab=.. evidence=low|medium|high
  vid.py continuity BIBLE.md MANIFEST.md [--scope prefix]
  vid.py perf VIDEO_PERFORMANCE.md [--by formato] [--include-synthetic] [--calibrate]
  vid.py evidence VIRAL_ANALYSIS.md          (nível de evidência a partir das referências R#)
  vid.py section FILE --toc | FILE "heading substring"
Exit codes: 0 ok, 1 violations found, 2 invalid/conflicting input, 3 nothing to verify against.
"""
import re, sys, statistics
from decimal import Decimal, ROUND_HALF_UP

WEIGHTS = [("fs", "Primeiros segundos", 20), ("ret", "Retenção", 20), ("orig", "Originalidade", 15),
           ("share", "Compartilhamento", 15), ("part", "Participação", 10), ("narr", "Qualidade narrativa", 10),
           ("cont", "Continuidade", 5), ("viab", "Viabilidade", 5)]
GATE_CAP, GATE_MIN = Decimal("6.0"), 4  # fs or ret below GATE_MIN caps the final score


def r2(x):
    return Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def cmd_score(args):
    kv = dict(a.split("=", 1) for a in args if "=" in a)
    missing = [k for k, _, _ in WEIGHTS if k not in kv] + (["evidence"] if "evidence" not in kv else [])
    if missing:
        print("ERRO: faltam", missing); return 2
    if kv["evidence"] not in ("low", "medium", "high"):
        print("ERRO: evidence deve ser low|medium|high"); return 2
    assert sum(w for _, _, w in WEIGHTS) == 100
    total, rows, gate = Decimal(0), [], False
    for k, name, w in WEIGHTS:
        try:
            v = Decimal(kv[k])
        except Exception:
            print(f"ERRO: {k}={kv[k]!r} não é número"); return 2
        if not (0 <= v <= 10):
            print(f"ERRO: {k}={v} fora de 0–10"); return 2
        c = v * w / 100
        total += c
        rows.append((name, v, w, c))
        if k in ("fs", "ret") and v < GATE_MIN:
            gate = True
    print(f"{'Critério':<22}{'Nota':>6}{'Peso':>7}{'Contrib.':>10}")
    for n, v, w, c in rows:
        print(f"{n:<22}{v:>6}{w:>6}%{r2(c):>10}")
    final = r2(total)
    print(f"{'SOMA PONDERADA':<35}{final:>10}")
    if gate and final > GATE_CAP:
        print(f"TETO: primeiros segundos ou retenção < {GATE_MIN} -> nota limitada a {GATE_CAP}")
        final = GATE_CAP
    print(f"NOTA FINAL: {final:.2f} / 10   (confiança da evidência: {kv['evidence']})")
    if kv["evidence"] == "low":
        print("AVISO: evidência baixa -> apresentar como estimativa preliminar, não como veredito.")
    return 0


# ---------- continuity ----------
def read_block(text, tag):
    m = re.search(r"```%s\s*\n(.*?)```" % tag, text, re.S)
    return m.group(1) if m else None


def parse_kv(block):
    out = []
    for ln in block.splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#") or "=" not in ln:
            continue
        key, rest = ln.split("=", 1)
        reason = None
        if "~" in rest:
            rest, reason = rest.split("~", 1)
            reason = reason.strip()
        out.append((key.strip().lower(), norm(rest), reason))
    return out


LOCKED = re.compile(r"\.(voice|accent|proportion|appearance|personality)$|^(style|tech)\.")  # só mudam com user-approved


def norm(s):
    return re.sub(r"\s+", " ", s.strip().lower())


def cmd_continuity(args):
    scope = None
    if "--scope" in args:
        i = args.index("--scope"); scope = args[i + 1].lower(); del args[i:i + 2]
    bible_t, man_t = open(args[0]).read(), open(args[1]).read()
    cb = read_block(bible_t, "canon")
    cb_items = [(k, v, r) for k, v, r in parse_kv(cb or "") if v and "<" not in k]  # ignora placeholders do template
    if not cb_items:
        print("SEM CANON: o PROJECT_BIBLE não tem bloco ```canon``` preenchido. Impossível verificar continuidade."
              " Não assumir nada: reconstruir o canon com o usuário antes de produzir."); return 3
    canon = {}
    for k, v, _ in cb_items:
        if k in canon and canon[k] != v:
            print(f"CONFLITO NO CANON: {k} = {canon[k]!r} e {v!r}. Resolver com o usuário antes de produzir."); return 2
        canon[k] = v
    man_blk = read_block(man_t, "manifest")
    man = parse_kv(man_blk if man_blk is not None else man_t)
    seen, bad, unch = set(), 0, []
    for k, v, reason in man:
        if scope and not k.startswith(scope):
            continue
        seen.add(k)
        if k not in canon and v == "@unchanged":
            print(f"MISMATCH  {k}: @unchanged para chave inexistente no canon"); bad += 1; continue
        if k not in canon:
            print(f"NEW       {k} = {v}  -> adicionar ao canon se for permanente"); continue
        if v == "@unchanged":
            if k in canon:
                unch.append(k); print(f"UNCHANGED {k}  (declarado sem mudança; NÃO confirmado no roteiro)")
            else:
                print(f"MISMATCH  {k}: @unchanged para chave inexistente no canon"); bad += 1
        elif v == "@removed":
            if reason:
                print(f"REMOVED   {k}  (justificado: {reason}) -> atualizar canon")
            else:
                print(f"MISMATCH  {k}: removido sem justificativa"); bad += 1
        elif v == canon[k]:
            print(f"OK        {k}")
        elif reason and reason.startswith("user-approved"):
            print(f"CHANGE-OK {k}: {canon[k]!r} -> {v!r}  ({reason}) -> atualizar canon")
        elif reason and reason.startswith("narrative:") and not LOCKED.search(k):
            print(f"CHANGE-OK {k}: {canon[k]!r} -> {v!r}  ({reason}) -> atualizar canon")
        elif reason and reason.startswith("narrative:"):
            print(f"MISMATCH  {k}: chave de identidade/técnica; justificativa narrativa NÃO basta, exige '~ user-approved'"); bad += 1
        else:
            print(f"MISMATCH  {k}: canon={canon[k]!r} parte={v!r}  (sem justificativa 'narrative:' ou 'user-approved')"); bad += 1
    for k in canon:
        if (not scope or k.startswith(scope)) and k not in seen:
            print(f"MISSING   {k}: canon={canon[k]!r} não declarado na parte (objeto/estado sumiu?)"); bad += 1
    if unch:
        print(f"ATENÇÃO: {len(unch)} item(ns) '@unchanged' só declarados, não verificados: conferir no roteiro/quadros ({', '.join(unch[:6])}{'…' if len(unch) > 6 else ''})")
    print(f"RESULTADO: {'REPROVADO' if bad else 'APROVADO'} ({bad} violação(ões)). "
          "Verifica apenas o que foi declarado; não prova o que aparece no vídeo renderizado.")
    return 1 if bad else 0


# ---------- performance ----------
NUM = ["views", "likes", "comentarios", "shares", "saves", "ret_media_pct", "conclusao_pct", "seguidores_novos",
       "seguidores_conta", "dur_s", "partes", "nota_prevista"]  # texto: origem, criterios, contexto


def tonum(x):
    x = x.strip().replace(".", "").replace(",", ".") if re.fullmatch(r"[\d.,]+", x.strip()) and x.count(",") else x.strip()
    try:
        return float(x)
    except ValueError:
        return None  # blank / n/d -> unknown, never 0


def parse_table(text):
    rows, hdr = [], None
    for ln in text.splitlines():
        if not ln.strip().startswith("|"):
            if ln.strip() and not ln.strip().startswith("<!--"):
                hdr = None  # fim de uma tabela
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if hdr is None:
            hdr = [c.lower() for c in cells]; continue
        if "views" not in hdr:
            continue  # outra tabela (ex.: Hipóteses)
        if set("".join(cells)) <= set("-: "):
            continue
        d = dict(zip(hdr, cells))
        if not d.get("id") or d["id"][0] in "<(_":
            continue
        for k in NUM:
            if k in d:
                d[k] = tonum(d[k])
        rows.append(d)
    return rows


SYN = re.compile(r"sint[eé]tic", re.I)
RATES = [("like", "likes"), ("coment", "comentarios"), ("share", "shares"), ("save", "saves")]


def band(d):
    return "dur?" if d is None else "<=20s" if d <= 20 else "21-40s" if d <= 40 else "41-60s" if d <= 60 else ">60s"


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i]); r = [0.0] * len(xs); i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = ranks(a), ranks(b); n = len(a); ma, mb = sum(ra) / n, sum(rb) / n
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** .5
    return sum((x - ma) * (y - mb) for x, y in zip(ra, rb)) / den if den else None


def cmd_perf(args):
    """perf FILE [--by campo=formato] [--include-synthetic] [--calibrate]
    Estratos = plataforma x faixa de duração. Compara valores de --by SÓ dentro de cada estrato."""
    by, syn, cal = "formato", "--include-synthetic" in args, "--calibrate" in args
    args = [a for a in args if a not in ("--include-synthetic", "--calibrate")]
    if "--by" in args:
        i = args.index("--by"); by = args[i + 1].lower(); del args[i:i + 2]
    text = open(args[0]).read()
    if not syn and any(re.match(r"#+\s*DADOS\s+SINT[EÉ]TIC", l, re.I) for l in text.splitlines()[:8]):
        print("ARQUIVO SINTÉTICO (título '# DADOS SINTÉTICOS'): dados de teste não entram em análise real. "
              "Use --include-synthetic só para testar a lógica."); return 3
    rows = parse_table(text)
    drop = [r for r in rows if SYN.search(r.get("origem") or "")]
    if drop and not syn:
        rows = [r for r in rows if r not in drop]
        print(f"{len(drop)} linha(s) com origem sintética EXCLUÍDA(s) da análise.")
    if syn:
        print("*** DADOS SINTÉTICOS INCLUÍDOS: resultados valem só como teste da lógica, nunca como evidência ***")
    if not rows:
        print("SEM DADOS: nenhuma linha de vídeo real preenchida. Nenhuma conclusão possível."); return 3
    noorig = sum(1 for r in rows if not r.get("origem"))
    if noorig:
        print(f"AVISO: {noorig} linha(s) sem coluna 'origem'; tratadas como reais (confirme).")
    print(f"{len(rows)} vídeo(s). Campos vazios = n/d (nunca tratados como 0).")
    f = lambda x: "n/d" if x is None else f"{x:.2f}%"
    for r in rows:
        v = r.get("views")
        r["_r"] = {n: (r.get(c) / v * 100 if v and r.get(c) is not None else None) for n, c in RATES}
        flag = "  [views<1000: ruído alto]" if v is not None and v < 1000 else ("  [sem views]" if not v else "")
        print(f"- {r['id']} [{r.get('plataforma') or '?'} {band(r.get('dur_s'))}]: views={'n/d' if v is None else int(v)} " +
              " ".join(f"{n}={f(r['_r'][n])}" for n, _ in RATES) + flag)
    strata = {}
    for r in rows:
        strata.setdefault((r.get("plataforma") or "?", band(r.get("dur_s"))), []).append(r)
    print(f"\nComparação de '{by}' DENTRO de cada estrato (plataforma x duração):")
    leaders = {n: {} for n, _ in RATES}  # métrica -> {estrato: valor líder}
    for st, rs in strata.items():
        groups = {}
        for r in rs:
            if r.get("views"):
                groups.setdefault(r.get(by) or "n/d", []).append(r)
        ok = {g: x for g, x in groups.items() if len(x) >= 3}
        if len(ok) < 2:
            print(f"  [{st[0]} {st[1]}] sem comparação: precisa de >=2 grupos com >=3 vídeos com views "
                  f"(tem {len(ok)}; grupos: {', '.join(f'{g}={len(x)}' for g, x in groups.items()) or 'nenhum'})")
            continue
        small = min(len(x) for x in ok.values())
        print(f"  [{st[0]} {st[1]}] {'HIPÓTESE (n<5)' if small < 5 else 'INDÍCIO (correlacional)'}")
        for g, x in ok.items():
            med = {n: statistics.median([y["_r"][n] for y in x if y["_r"][n] is not None] or [float('nan')]) for n, _ in RATES}
            print(f"    {g}: n={len(x)} " + " ".join(f"{n}={med[n]:.2f}%" for n, _ in RATES))
            ok[g] = (x, med)
        for n, _ in RATES:
            vals = {g: m[n] for g, (x, m) in ok.items() if m[n] == m[n]}
            top = sorted(vals.values(), reverse=True)
            if len(top) >= 2 and top[0] > top[1] * 1.10:  # empate/diferença <10% não é liderança
                leaders[n][st] = max(vals, key=vals.get)
        fol = [y.get("seguidores_conta") for x, m in ok.values() for y in x if y.get("seguidores_conta")]
        if fol and max(fol) / min(fol) > 3:
            print("    AVISO: tamanho da conta variou >3x neste estrato; confusor forte.")
    print("\nRecorrência (mesmo valor líder em >=2 estratos independentes):")
    any_rec = False
    for n, _ in RATES:
        cnt = {}
        for st, g in leaders[n].items():
            cnt.setdefault(g, []).append(st)
        for g, sts in cnt.items():
            if len(sts) >= 2:
                any_rec = True
                print(f"  {n}: '{g}' lidera em {len(sts)} estratos -> RECORRENTE (correlacional, não causal)")
    if not any_rec:
        print(f"  nenhuma (estratos com líder claro: {len({s for n in leaders for s in leaders[n]})})")
    print("AVISO: associação não é causa. Confusores não controlados: horário, distribuição, tema, sorte/algoritmo.")
    if cal:
        pr = [r for r in rows if r.get("nota_prevista") is not None and r["_r"]["share"] is not None]
        print(f"\nCalibração (resultado = taxa de share; views dependem da conta): {len(pr)} vídeo(s) com nota+share.")
        if len(pr) < 8:
            print("  INSUFICIENTE: precisa de >=8 vídeos reais (e >=15 antes de alterar pesos/âncoras).")
        else:
            rho = spearman([r["nota_prevista"] for r in pr], [r["_r"]["share"] for r in pr])
            print(f"  Spearman(nota_prevista, share) = {rho:.2f}" + ("  (n<15: instável, não recalibrar)" if len(pr) < 15 else ""))
            for k in ("fs", "ret", "orig", "share", "part", "narr", "cont", "viab"):
                xs = []
                for r in pr:
                    m = re.search(r"\b%s=(\d+(?:\.\d+)?)" % k, r.get("criterios") or "")
                    xs.append((float(m.group(1)), r["_r"]["share"]) if m else None)
                xs = [x for x in xs if x]
                if len(xs) >= 8:
                    rk = spearman([a for a, _ in xs], [b for _, b in xs])
                    print(f"    critério {k}: rho={'n/d' if rk is None else f'{rk:.2f}'} (n={len(xs)})")
    return 0


def cmd_evidence(args):
    """evidence VIRAL_ANALYSIS.md -> nível (low|medium|high) a partir das etiquetas da tabela de referências."""
    rows, hdr = [], None
    for ln in open(args[0]).read().splitlines():
        if not ln.strip().startswith("|"):
            hdr = None if ln.strip() and not ln.strip().startswith("<!--") else hdr; continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if hdr is None:
            hdr = [c.lower() for c in cells]; continue
        d = dict(zip(hdr, cells))
        if "etiqueta" in d and re.fullmatch(r"R\d+", d.get("r#", "")):
            rows.append(d)
    c = {t: 0 for t in ("OBS", "CONF", "USR", "REL")}
    for d in rows:
        t = re.sub(r"[\[\]\s]", "", d["etiqueta"]).upper()
        if t in c:
            c[t] += 1
    firm = c["OBS"] + c["CONF"]
    lvl = "high" if firm >= 5 else "medium" if (firm >= 2 or c["USR"] >= 5) else "low"
    print(f"{len(rows)} referência(s): OBS={c['OBS']} CONF={c['CONF']} USR={c['USR']} REL={c['REL']}")
    print(f"evidence={lvl}  (high: >=5 OBS/CONF; medium: 2-4 OBS/CONF ou >=5 USR; REL nunca conta)")
    return 0


# ---------- section ----------
def cmd_section(args):
    lines = open(args[0]).read().splitlines()
    heads, fenced = [], False
    for i, l in enumerate(lines):
        if l.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and (m := re.match(r"(#+)\s+(.*)", l)):
            heads.append((i, len(m.group(1)), m.group(2)))
    if len(args) > 1 and args[1] == "--toc":
        for i, lvl, t in heads:
            print(f"{i + 1:>5} {'  ' * (lvl - 1)}{t}")
        return 0
    q = args[1].lower()
    for n, (i, lvl, t) in enumerate(heads):
        if q in t.lower():
            end = next((j for j, l2, _ in heads[n + 1:] if l2 <= lvl), len(lines))
            print("\n".join(lines[i:end])); return 0
    print(f"SEÇÃO não encontrada: {args[1]!r}"); return 3


if __name__ == "__main__":
    cmds = {"score": cmd_score, "continuity": cmd_continuity, "perf": cmd_perf, "evidence": cmd_evidence, "section": cmd_section}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(__doc__); sys.exit(2)
    try:
        sys.exit(cmds[sys.argv[1]](sys.argv[2:]))
    except IndexError:
        print("ARGUMENTOS FALTANDO.\n" + __doc__); sys.exit(2)
    except FileNotFoundError as e:
        print(f"ARQUIVO AUSENTE: {e.filename}. Não presumir conteúdo; criar a partir de templates/ ou perguntar ao usuário."); sys.exit(3)
