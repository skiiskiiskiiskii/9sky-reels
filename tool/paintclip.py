#!/usr/bin/env python3
"""Painting hook: the whole framed painting on the warm vitrine wall, then one slow, eased push-in onto a
detail (e.g. the red collar of Rogier van der Weyden's Francesco d'Este, Met, CC0). No cut, no flash.
1080x1920, 30 fps, h264.
usage: paintclip.py <image> <out.mp4> <fx> <fy> [dur=3.4] [w0=900] [z1=2.8] [y0=1060] [y1=1010]
fx, fy - the detail in source pixels; w0 - painting width on screen at the start; z1 - final zoom;
y0 - painting centre on screen at the start; y1 - where the detail sits on screen at the end."""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vitrine import backdrop

W, H, FPS = 1080, 1920, 30


def make(src, out, fx, fy, dur=3.4, w0=900, z1=2.8, y0=1060, y1=1010, tone="vitrine", ease="inout"):
    im = Image.open(src).convert("RGB")
    bg = backdrop(tone, cy=0.55, rx=0.75, ry=0.45)
    s0 = w0 / im.width                                   # screen px per source px at the start
    cx_src, cy_src = im.width / 2, im.height / 2
    n = int(dur * FPS)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                          "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / max(1, n - 1)
        e = t ** 1.6 if ease == "in" else t * t * (3 - 2 * t)   # "in": still moving into the cut
        z = 1 + (z1 - 1) * e
        s = s0 * z
        # the source point that sits at screen centre-x / target-y glides from the painting centre to the detail
        px = cx_src + (fx - cx_src) * e
        py = cy_src + (fy - cy_src) * e
        sy = y0 + (y1 - y0) * e
        ox, oy = W / 2 - px * s, sy - py * s             # screen position of the painting's top-left corner
        # crop only the visible part of the source, then scale it
        x0, yA = max(0, -ox / s), max(0, -oy / s)
        x1, yB = min(im.width, (W - ox) / s), min(im.height, (H - oy) / s)
        part = im.crop((int(x0), int(yA), int(np.ceil(x1)), int(np.ceil(yB))))
        pw, ph = int(round(part.width * s)), int(round(part.height * s))
        part = part.resize((max(1, pw), max(1, ph)), Image.LANCZOS)
        fr = bg.copy()
        if z < 1.6:                                      # soft shadow under the frame while it is still visible
            sh = Image.new("L", (W, H), 0)
            sx0, sy0 = int(ox + int(x0) * s), int(oy + int(yA) * s)
            sh.paste(110, (sx0 + 14, sy0 + 24, sx0 + pw + 14, sy0 + ph + 24))
            sh = sh.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * (1.6 - z) / 0.6))
            fr.paste((8, 7, 6), (0, 0), sh)
        fr.paste(part, (int(ox + int(x0) * s), int(oy + int(yA) * s)))
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()


if __name__ == "__main__":
    a = sys.argv
    kw = {}
    for k, v in zip(["dur", "w0", "z1", "y0", "y1"], a[5:]):
        kw[k] = float(v)
    make(a[1], a[2], float(a[3]), float(a[4]), **kw)
