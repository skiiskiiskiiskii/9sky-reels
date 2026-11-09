#!/usr/bin/env python3
"""Turn a still (e.g. the all-red statue from the red graphic series) into a calm hook clip:
very slow push-in plus a soft band of light drifting across, so the frame is alive without any cut,
flash or punch-in. 1080x1920, 30 fps, h264.
usage: stillclip.py <image> <out.mp4> [dur=3.6] [z0=1.0] [z1=1.07] [cy=0.45]"""
import subprocess, sys
import numpy as np
from PIL import Image

W, H, FPS = 1080, 1920, 30


def make(src, out, dur=3.6, z0=1.0, z1=1.07, cy=0.45, light=0.10):
    im = Image.open(src).convert("RGB")
    s = max(W / im.width, H / im.height)
    base = im.resize((int(im.width * s * z1) + 2, int(im.height * s * z1) + 2), Image.LANCZOS)
    n = int(dur * FPS)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                          "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for i in range(n):
        t = i / max(1, n - 1)
        e = t * t * (3 - 2 * t)                                   # ease in-out
        z = z0 + (z1 - z0) * e
        w, h = int(W * z1 / z), int(H * z1 / z)                   # crop window in the z1-sized image
        cx0 = (base.width - w) // 2
        cy0 = int((base.height - h) * cy)
        fr = base.crop((cx0, cy0, cx0 + w, cy0 + h)).resize((W, H), Image.LANCZOS)
        a = np.asarray(fr).astype(np.float32)
        # soft diagonal light band drifting left -> right
        pos = -0.4 + 1.8 * t
        d = (xx / W * 0.8 + yy / H * 0.4) - pos
        band = np.exp(-(d / 0.18) ** 2) * light
        a = a * (1 + band[..., None])
        p.stdin.write(np.clip(a, 0, 255).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
    return out


if __name__ == "__main__":
    a = sys.argv
    make(a[1], a[2], *(float(x) for x in a[3:]))
