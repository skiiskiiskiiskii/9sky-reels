#!/usr/bin/env python3
"""2026-11-19: variations of the vitrine mockup pages, so the second half of each reel is not the same picture
(Kirill: Instagram should not see the reels as the same; keep the aura, show it from a slightly different side).
Still clean: no grain, no zoom, no annotation lines, header + footer only.

New knobs: glow centre / size (light from above, off-centre), garment scale and height, two garments side by side,
three extra dark tones (ink, bronze, smoke)."""
import numpy as np
from PIL import Image
import vitrine as V

W, H = V.W, V.H
V.TONES.update({
    "ink":    ((26, 30, 42), (4, 4, 6)),       # cold blue-black
    "bronze": ((62, 47, 30), (6, 5, 3)),       # gilt-frame warmth
    "smoke":  ((44, 44, 44), (5, 5, 5)),       # neutral grey glow
})


def glow(tone, spots, seed=7):
    """several soft glows: spots = [(cx, cy, rx, ry), ...] in 0-1"""
    c0, c1 = (np.array(c, np.float32) for c in V.TONES[tone])
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    k = np.zeros((H, W), np.float32)
    for cx, cy, rx, ry in spots:
        d = np.sqrt(((x - W * cx) / (W * rx)) ** 2 + ((y - H * cy) / (H * ry)) ** 2)
        k = np.maximum(k, np.clip(1 - d, 0, 1) ** 1.8)
    img = c1 + (c0 - c1) * k[..., None]
    img += np.random.default_rng(seed).uniform(-0.5, 0.5, img.shape)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")


def vpage2(mockup, out, no, sub, tone="vitrine", scale=0.9, cy=0.47, spot=None, title=""):
    """one garment; spot = (cx, cy, rx, ry) of the glow, default centred on the garment"""
    import editorial as E
    c = glow(tone, [spot or (0.5, cy, 0.62, 0.36)])
    g = E._cut(mockup)
    g = g.resize((int(g.width * scale), int(g.height * scale)), Image.LANCZOS)
    k = min(1.0, 900 / g.width, 1150 / g.height)
    if k < 1.0:
        g = g.resize((int(g.width * k), int(g.height * k)), Image.LANCZOS)
    V._paste_soft(c, g, ((W - g.width) // 2, int(H * cy - g.height / 2)))
    c = E._footer(E._header(c, no), title, sub)
    c.save(out, quality=96)
    return out


def vside(left, right, out, no, sub="", tone="vitrine", title="", cy=0.47, box_h=900, footer_y=1548):
    """two garments side by side (his | hers, front | back), each with its own glow"""
    import editorial as E
    c = glow(tone, [(0.27, cy, 0.34, 0.27), (0.73, cy, 0.34, 0.27)])
    for i, mk in enumerate([left, right]):
        g, _ = E._fit(E._cut(mk), W // 2 - 70, box_h)
        cx = W * (0.27 if i == 0 else 0.73)
        V._paste_soft(c, g, (int(cx - g.width / 2), int(H * cy - g.height / 2)))
    c = E._footer(E._header(c, no), title, sub, y=footer_y)
    c.save(out, quality=96)
    return out


def vstacked2(front, back, out, no, tone="vitrine", title="EX MUSEO", sub="FIRST LOOK"):
    return V.vstacked(front, back, out, no, title=title, sub=sub, tone=tone)


def vgrid(items, out, no, sub="", tone="vitrine", title="EX MUSEO", cy=0.45, gap=0.25, cell_h=560, footer_y=1548):
    """four garments 2 x 2 (the whole first look on one page); items = 4 mockup paths, row by row"""
    import editorial as E
    xs, ys = (0.27, 0.73), (cy - gap / 2 + 0.0, cy + gap / 2)
    spots = [(x, y, 0.3, 0.17) for y in ys for x in xs]
    c = glow(tone, spots)
    for i, mk in enumerate(items):
        g, _ = E._fit(E._cut(mk), W // 2 - 90, cell_h)
        x, y = xs[i % 2], ys[i // 2]
        V._paste_soft(c, g, (int(W * x - g.width / 2), int(H * y - g.height / 2)))
    c = E._footer(E._header(c, no), title, sub, y=footer_y)
    c.save(out, quality=96)
    return out
