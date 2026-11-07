#!/usr/bin/env python3
"""Backgrounds for the mockup pages, 2026-11-07: still the black museum catalogue, but lit like a vitrine -
a soft glow behind the garment so black pieces separate from the page. No grain (only an invisible
sub-level dither against banding). Two tones:
  vitrine - warm charcoal glow
  oxblood - very dark red glow, picks up the collar
"""
import numpy as np
from PIL import Image

W, H = 1080, 1920
TONES = {
    "vitrine": ((56, 52, 48), (5, 5, 5)),
    "oxblood": ((60, 17, 20), (6, 3, 3)),
    "slate":   ((30, 33, 37), (4, 4, 5)),
}


def backdrop(tone="vitrine", cy=0.47, rx=0.62, ry=0.36, seed=7):
    c0, c1 = (np.array(c, np.float32) for c in TONES[tone])
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W / 2) / (W * rx)) ** 2 + ((y - H * cy) / (H * ry)) ** 2)
    k = np.clip(1 - d, 0, 1) ** 1.8                     # soft falloff, glow only in the middle
    img = c1 + (c0 - c1) * k[..., None]
    img += np.random.default_rng(seed).uniform(-0.5, 0.5, img.shape)   # sub-level dither, not visible
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")


def finale_backdrop(tone="vitrine"):
    """two glows for the stacked front/back finale"""
    a = np.asarray(backdrop(tone, cy=0.30, ry=0.22)).astype(np.float32)
    b = np.asarray(backdrop(tone, cy=0.63, ry=0.22, seed=8)).astype(np.float32)
    return Image.fromarray(np.maximum(a, b).astype(np.uint8), "RGB")


def _paste_soft(c, g, xy, halo=0.15):
    """editorial._paste with a lighter halo: on a glow a heavy dark halo kills the light"""
    from PIL import ImageFilter
    al = np.asarray(g.split()[-1]).astype(np.float32)
    pad = 90
    h = Image.new("L", (g.width + 2 * pad, g.height + 2 * pad), 0)
    h.paste(Image.fromarray(al.astype(np.uint8)), (pad, pad))
    h = h.filter(ImageFilter.GaussianBlur(75)).point(lambda v: int(v * halo))
    c.paste(Image.new("RGB", h.size, (0, 0, 0)), (xy[0] - pad, xy[1] - pad), h)
    c.paste(g, xy, g)


def vpage(mockup, out, no, sub, tone="vitrine", scale=0.9, title=""):
    import editorial as E
    c = backdrop(tone)
    g = E._cut(mockup)
    g = g.resize((int(g.width * scale), int(g.height * scale)), Image.LANCZOS)
    _paste_soft(c, g, ((W - g.width) // 2, int(H * 0.47 - g.height / 2)))
    c = E._footer(E._header(c, no), title, sub)
    c.save(out, quality=96)
    return out


def vstacked(front, back, out, no, title="EX MUSEO", sub="FIRST LOOK", tone="vitrine", footer_y=1580):
    import editorial as E
    c = finale_backdrop(tone)
    top, bottom, gap = 290, footer_y - 70, 40
    row_h = (bottom - top - gap) // 2
    for i, mk in enumerate([front, back]):
        g, _ = E._fit(E._cut(mk), W - 200, row_h)
        cy = top + row_h // 2 + i * (row_h + gap)
        _paste_soft(c, g, ((W - g.width) // 2, cy - g.height // 2))
    c = E._footer(E._header(c, no), title, sub, y=footer_y)
    c.save(out, quality=96)
    return out
