#!/usr/bin/env python3
"""Synthetic hooks built from stills (aesthetics + mockup pages). 3.13 s, 1080x1920, 30 fps, silent mp4.
Every hook moves from frame 0 and lands on red / the collar right before the drop.

flashlight(stills, page, out)    a torch beam wanders a dark gallery, last beat finds the collar
accelerate(stills, last, out)    cuts speed up 0.45 s -> 2 frames, ends on a red still
emerge(src, out)                 black -> image rises out of the dark in grey, red floods in last
redwave(src, out)                grey image, red sweeps down the frame at ~2.3 s
"""
import subprocess, numpy as np
from PIL import Image

W, H, FPS, DUR = 1080, 1920, 30, 3.13
N = round(DUR * FPS)


def load(p, w=W, h=H, over=1.12):
    im = Image.open(p).convert("RGB")
    s = max(w * over / im.width, h * over / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return np.asarray(im).astype(np.float32) / 255


def drift(a, t, dx=0.0, dy=-1.0):
    """slow camera drift across an oversized still (t 0..1); background only, never mockups"""
    h, w = a.shape[:2]
    x = int((w - W) * (0.5 + 0.5 * dx * (t - 0.5)))
    y = int((h - H) * (0.5 + 0.5 * dy * (t - 0.5)))
    return a[y:y + H, x:x + W]


def grey(a):
    g = a @ np.array([0.3, 0.59, 0.11], np.float32)
    return np.repeat(g[..., None], 3, 2)


def redness(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return np.clip((r - np.maximum(g, b)) * 4, 0, 1)[..., None]


YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)


def beam(cx, cy, r):
    d = np.sqrt((XX - cx) ** 2 + ((YY - cy) * 0.92) ** 2) / r
    return (np.exp(-d ** 4 * 1.6))[..., None]


class Out:
    def __init__(self, path):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                   "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "17", "-preset", "medium",
                                   "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)

    def put(self, f):
        self.p.stdin.write((np.clip(f, 0, 1) * 255).astype(np.uint8).tobytes())

    def close(self):
        self.p.stdin.close(); self.p.wait()


def collar_xy(page_path):
    a = np.asarray(Image.open(page_path).convert("RGB")).astype(np.float32) / 255
    m = redness(a)[..., 0] > 0.3
    ys, xs = np.nonzero(m)
    return (float(xs.mean()), float(ys.mean())) if len(xs) else (W / 2, H * 0.4)


def _hotspots(img, k=2):
    """k brightest blob centres (in output-crop coords at mid drift) so the beam finds the subject"""
    from PIL import ImageFilter
    a = drift(img, 0.5, 0.3, -0.6)
    g = Image.fromarray((a.mean(2) * 255).astype(np.uint8)).resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(6))
    g = np.asarray(g).astype(np.float32)
    pts = []
    for _ in range(k):
        y, x = np.unravel_index(np.argmax(g), g.shape)
        pts.append((x * 8.0, y * 8.0))
        g[max(0, y - 25):y + 25, max(0, x - 25):x + 25] = 0
    return pts


def flashlight(stills, page_path, out, land=2.35, seed=1, gain=1.0, amb=0.05):
    rng = np.random.default_rng(seed)
    imgs = [load(s) for s in stills]
    spots = [_hotspots(im) for im in imgs]
    pg = np.asarray(Image.open(page_path).convert("RGB").resize((W, H))).astype(np.float32) / 255
    cx1, cy1 = collar_xy(page_path)
    cy1 += 140  # centre on the chest so the collar sits in the top of the beam
    o = Out(out)
    seg = land / len(imgs)
    jit = rng.normal(0, 1, (N, 2)).cumsum(0) * 2.5
    prev = (W * 0.2, H * 0.3)
    for i in range(N):
        t = i / FPS
        if t < land:
            k = min(int(t / seg), len(imgs) - 1); u = (t - k * seg) / seg
            base = drift(imgs[k], u, 0.3, -0.6)
            (ax, ay), (bx, by) = spots[k]
            e = 0.5 - 0.5 * np.cos(np.pi * u)
            cx, cy = ax + (bx - ax) * e + jit[i, 0], ay + (by - ay) * e + jit[i, 1]
            m = beam(cx, cy, 360)
            f = base * (amb + 1.35 * m)
            prev = (cx, cy)
        else:
            u = min((t - land) / 0.3, 1.0); e = 1 - (1 - u) ** 3
            cx = prev[0] + (cx1 - prev[0]) * e + jit[i, 0] * 0.3
            cy = prev[1] + (cy1 - prev[1]) * e + jit[i, 1] * 0.3
            m = beam(cx, cy, 420)
            f = pg * (amb + gain * m)
        o.put(f)
    o.close()


def accelerate(stills, last, out, seed=2):
    imgs = [load(s) for s in stills]
    lastimg = load(last)
    durs, d = [], 0.45
    while sum(durs) + d < 2.45:
        durs.append(d); d = max(d * 0.72, 2 / FPS)
    o = Out(out); t0 = 0.0; edges = np.cumsum([0] + durs)
    for i in range(N):
        t = i / FPS
        if t < edges[-1]:
            k = int(np.searchsorted(edges, t, side="right") - 1)
            u = (t - edges[k]) / durs[k]
            f = drift(imgs[k % len(imgs)], u, 0.0, -1.0) * 0.92
        else:
            u = (t - edges[-1]) / (DUR - edges[-1])
            f = drift(lastimg, u, 0.0, -0.8)
        o.put(f)
    o.close()


def emerge(src, out, black=0.9):
    a = load(src); g = grey(a); rmask = redness(a)
    o = Out(out)
    for i in range(N):
        t = i / FPS; u = i / (N - 1)
        base = drift(a, u, 0.0, -1.0); gb = drift(g, u, 0.0, -1.0); rm = drift(rmask, u, 0.0, -1.0)
        lv = np.clip((t - black) / (DUR - black - 0.35), 0, 1) ** 1.6
        col = np.clip((t - 2.35) / 0.45, 0, 1)
        f = (gb * (1 - rm * col) + base * rm * col) * lv
        o.put(f)
    o.close()


def redwave(src, out, start=2.0, length=0.7):
    a = load(src); g = grey(a)
    o = Out(out)
    for i in range(N):
        t = i / FPS; u = i / (N - 1)
        base = drift(a, u, 0.25, -1.0); gb = drift(g, u, 0.25, -1.0)
        front = (t - start) / length * (H + 400) - 200
        m = np.clip((front - YY) / 200, 0, 1)[..., None]
        o.put(gb * (1 - m) + base * m)
    o.close()
