#!/usr/bin/env python3
"""Gera imagens SINTÉTICAS (formas planas) e um vídeo de teste em OUTDIR. Uso: make_images.py OUTDIR"""
import os, subprocess, sys, shutil
from PIL import Image, ImageDraw

W, H = 360, 640
BG, LAMP, BODY, SCARF, KEY = (27, 42, 65), (232, 163, 61), (107, 143, 78), (42, 92, 170), (224, 176, 64)


def scene(bg=BG, scarf=SCARF, dx=0, scale=1.0, key=True, extra=False, size=(W, H)):
    im = Image.new("RGB", size, bg); d = ImageDraw.Draw(im)
    d.ellipse((250, 60, 330, 140), fill=LAMP)                      # lampião
    cx, cy, r = 150 + dx, 400, int(90 * scale)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=BODY)         # corpo
    d.rectangle((cx - r + 10, cy - 15, cx + r - 10, cy + 25), fill=scarf)  # cachecol
    d.polygon([(cx - 50, cy - r + 5), (cx - 70, cy - r - 70), (cx - 30, cy - r - 10)], fill=BODY)  # orelha
    if key:
        d.rectangle((cx + r - 5, cy + 60, cx + r + 7, cy + 90), fill=KEY)  # chave pequena (~0,2% do quadro)
    if extra:
        d.ellipse((20, 40, 140, 200), fill=(190, 40, 40))           # criatura vermelha nova
    return im


def main(out):
    os.makedirs(out, exist_ok=True)
    ref = scene(); ref.save(f"{out}/ref.png")
    scene(dx=40, scale=0.9).save(f"{out}/ok_moved.png")                       # pose/posição diferente: deve passar
    ref.save(f"{out}/ok_jpeg.jpg", quality=60)                                # recompressão: deve passar
    scene(scarf=(192, 48, 42)).save(f"{out}/bad_red_scarf.png")               # roupa mudou
    scene(bg=(143, 176, 216)).save(f"{out}/bad_bright.png")                   # iluminação mudou
    scene(key=False).save(f"{out}/bad_no_key.png")                            # objeto pequeno sumiu
    scene(extra=True).save(f"{out}/bad_extra_creature.png")                   # elemento novo
    scene(size=(360, 360)).save(f"{out}/bad_size.png")                        # resolução/aspecto
    if shutil.which("ffmpeg"):
        for fps in (24, 30):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"testsrc=size=360x640:rate={fps}:duration=3",
                            "-f", "lavfi", "-i", "sine=frequency=440:duration=3", "-shortest", "-pix_fmt", "yuv420p", f"{out}/video_{fps}fps.mp4"])


if __name__ == "__main__":
    main(sys.argv[1])
