#!/usr/bin/env python3
"""Verificação visual auxiliar. Pillow é OPCIONAL (metrics, sheet); ffmpeg/ffprobe são OPCIONAIS (probe, frames).

  visual.py probe VIDEO [--fps 24] [--size 1080x1920]   mede fps/resolução/duração/áudio (ffprobe)
  visual.py frames VIDEO OUTDIR [--every 1.0]           extrai quadros-chave (ffmpeg), 1 a cada N segundos
  visual.py metrics REF FRAME [--palette #hex,#hex] [--min-frac 0.015]   deriva GROSSEIRA de cor, luz, contraste, resolução
  visual.py sheet OUT.png REF FRAME [FRAME ...] [--crop x0,y0,x1,y1]     folha lado a lado; --crop (frações 0-1) amplia um detalhe

LIMITES: as métricas pegam mudança global (cor dominante nova/ausente, luz, resolução). NÃO provam identidade de
personagem, pose, proporção nem objetos pequenos. Isso exige revisão visual da folha (sheet) contra o checklist
do canon, feita por pessoa ou pelo modelo olhando a imagem, e só pode ser afirmada se a imagem foi realmente vista.
Exit: 0 sem alertas, 1 alertas, 2 uso/erro, 3 dependência ausente.
"""
import json, math, os, shutil, subprocess, sys

DE_MAX, FR_MIN, DLUMA_MAX, DSTD_MAX = 30.0, 0.015, 0.12, 0.08  # limiares heurísticos (ver references/visual-verification.md)


def need_pil():
    try:
        from PIL import Image  # noqa
        return True
    except ImportError:
        print("DEPENDÊNCIA AUSENTE: Pillow (pip install pillow). Sem ela não há métricas nem folha; "
              "alternativa: comparar as imagens manualmente com o checklist do canon.")
        return False


def lab(rgb):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = map(f, rgb)
    x, y, z = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047, 0.2126 * r + 0.7152 * g + 0.0722 * b, \
              (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    h = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = h(x), h(y), h(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def de(a, b):
    return math.dist(lab(a), lab(b))


def hex2rgb(h):
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def dominant(img, k=16):
    from PIL import Image
    q = img.resize((96, 96), Image.BOX).quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal, tot = q.getpalette(), 96 * 96
    return sorted(((tuple(pal[i * 3:i * 3 + 3]), c / tot) for c, i in q.getcolors()), key=lambda t: -t[1])


def stats(img):
    from PIL import ImageStat
    s = ImageStat.Stat(img.convert("L"))
    return s.mean[0] / 255, s.stddev[0] / 255


def hx(c):
    return "#%02X%02X%02X" % c


def cmd_metrics(a):
    if not need_pil():
        return 3
    from PIL import Image
    pal = []
    if "--palette" in a:
        i = a.index("--palette"); pal = [hex2rgb(x) for x in a[i + 1].split(",")]; del a[i:i + 2]
    global FR_MIN
    if "--min-frac" in a:
        i = a.index("--min-frac"); FR_MIN = float(a[i + 1]); del a[i:i + 2]
    ref, fr = Image.open(a[0]).convert("RGB"), Image.open(a[1]).convert("RGB")
    alerts = []
    if ref.size != fr.size:
        alerts.append(f"RESOLUÇÃO: ref {ref.size} != quadro {fr.size}")
    (lr, sr), (lf, sf) = stats(ref), stats(fr)
    if abs(lr - lf) > DLUMA_MAX:
        alerts.append(f"ILUMINAÇÃO: luminância média {lr:.2f} -> {lf:.2f} (|Δ|>{DLUMA_MAX})")
    if abs(sr - sf) > DSTD_MAX:
        alerts.append(f"CONTRASTE: desvio {sr:.2f} -> {sf:.2f} (|Δ|>{DSTD_MAX})")
    dr, df = dominant(ref), dominant(fr)
    known = [c for c, p in dr if p >= 0.005] + pal
    for c, p in df:
        if p >= FR_MIN and min(de(c, k) for k in known) > DE_MAX:
            alerts.append(f"COR NOVA: {hx(c)} ocupa {p:.0%} do quadro e não existe na referência/paleta")
    for c, p in dr:
        if p >= FR_MIN and min(de(c, k) for k, q in df if q >= 0.005) > DE_MAX:
            alerts.append(f"COR AUSENTE: {hx(c)} ocupava {p:.0%} na referência e sumiu do quadro")
    print("ref dominantes:  " + " ".join(f"{hx(c)}:{p:.0%}" for c, p in dr[:6]))
    print("quadro dominantes:" + " ".join(f"{hx(c)}:{p:.0%}" for c, p in df[:6]))
    for al in alerts:
        print("ALERTA", al)
    print(f"RESULTADO: {'ALERTAS (' + str(len(alerts)) + ')' if alerts else 'sem alertas de deriva global'}. "
          "Ausência de alerta NÃO prova consistência de personagem/objetos: fazer revisão visual da folha.")
    return 1 if alerts else 0


def cmd_sheet(a):
    if not need_pil():
        return 3
    from PIL import Image, ImageDraw
    a = list(a); crop = None
    if "--crop" in a:
        i = a.index("--crop"); crop = [float(x) for x in a[i + 1].split(",")]; del a[i:i + 2]
    paths, H, cap = a[1:], 360, 16
    ims = []
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB")
        if crop:
            im = im.crop((int(crop[0] * im.width), int(crop[1] * im.height), int(crop[2] * im.width), int(crop[3] * im.height)))
        ims.append((("REF  " if i == 0 else f"F{i}   ") + os.path.basename(p), im.resize((max(1, round(im.width * H / im.height)), H))))
    W = sum(t.width for _, t in ims) + 8 * (len(ims) + 1)
    sheet = Image.new("RGB", (W, H + cap + 16), (30, 30, 30)); d = ImageDraw.Draw(sheet); x = 8
    for name, t in ims:
        sheet.paste(t, (x, cap + 8)); d.text((x, 4), name[:40], fill=(255, 255, 255)); x += t.width + 8
    sheet.save(a[0]); print(f"folha salva: {a[0]} ({sheet.width}x{sheet.height}); primeiro painel = referência")
    return 0


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def cmd_probe(a):
    if not shutil.which("ffprobe"):
        print("DEPENDÊNCIA AUSENTE: ffprobe (ffmpeg). Medir fps/resolução manualmente no software de edição."); return 3
    want_fps = float(a[a.index("--fps") + 1]) if "--fps" in a else None
    want_sz = a[a.index("--size") + 1] if "--size" in a else None
    p = run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,avg_frame_rate,duration",
             "-of", "json", a[0]])
    if p.returncode:
        print("ERRO ffprobe:", p.stderr.strip()[:200]); return 2
    st = json.loads(p.stdout)["streams"]
    v = next((s for s in st if s["codec_type"] == "video"), None)
    if not v:
        print("ERRO: sem stream de vídeo"); return 2
    n, dnm = v["avg_frame_rate"].split("/"); fps = float(n) / float(dnm or 1)
    audio = any(s["codec_type"] == "audio" for s in st)
    print(f"fps={fps:.3f} tamanho={v['width']}x{v['height']} duração={v.get('duration', 'n/d')}s áudio={'sim' if audio else 'NÃO'}")
    alerts = []
    if want_fps and abs(fps - want_fps) > 0.01:
        alerts.append(f"FPS: canon {want_fps} != medido {fps:.3f}")
    if want_sz and want_sz != f"{v['width']}x{v['height']}":
        alerts.append(f"TAMANHO: canon {want_sz} != medido {v['width']}x{v['height']}")
    for al in alerts:
        print("ALERTA", al)
    print("RESULTADO:", "ALERTAS" if alerts else "medidas coerentes com o informado (só fps/tamanho/áudio; não avalia movimento)")
    return 1 if alerts else 0


def cmd_frames(a):
    if not shutil.which("ffmpeg"):
        print("DEPENDÊNCIA AUSENTE: ffmpeg. Exporte quadros-chave pelo seu software de edição."); return 3
    every = float(a[a.index("--every") + 1]) if "--every" in a else 1.0
    os.makedirs(a[1], exist_ok=True)
    p = run(["ffmpeg", "-v", "error", "-y", "-i", a[0], "-vf", f"fps=1/{every}", os.path.join(a[1], "k_%03d.png")])
    if p.returncode:
        print("ERRO ffmpeg:", p.stderr.strip()[:200]); return 2
    print(f"{len(os.listdir(a[1]))} quadro(s) em {a[1]} (1 a cada {every}s)")
    return 0


if __name__ == "__main__":
    cmds = {"probe": cmd_probe, "frames": cmd_frames, "metrics": cmd_metrics, "sheet": cmd_sheet}
    if len(sys.argv) < 3 or sys.argv[1] not in cmds:
        print(__doc__); sys.exit(2)
    try:
        sys.exit(cmds[sys.argv[1]](sys.argv[2:]))
    except IndexError:
        print("ARGUMENTOS FALTANDO.\n" + __doc__); sys.exit(2)
    except FileNotFoundError as e:
        print(f"ARQUIVO AUSENTE: {e.filename}"); sys.exit(3)
