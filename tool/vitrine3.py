#!/usr/bin/env python3
"""2026-11-20: pages where the garment stands in a real room - a frame of the palace / salon footage, blurred and
darkened, behind a clean mockup (no grain, no zoom, no lines on the garment; header + footer as on every page).
Used by 1120b (three new ideas: red thread, palace walk, red salon)."""
import subprocess
import numpy as np
from PIL import Image, ImageFilter
import vitrine as V

W, H = V.W, V.H


def frame_bg(src, t, blur=10, dark=0.36, cx=0.5, cy=0.5, zoom=1.0, warm=None):
    """one frame of a clip, cover-fitted to 1080x1920, blurred, darkened, with a soft vignette"""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    import io
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    k = max(W / im.width, H / im.height) * zoom
    im = im.resize((int(im.width * k + 1), int(im.height * k + 1)), Image.LANCZOS)
    x0 = int((im.width - W) * cx)
    y0 = int((im.height - H) * cy)
    im = im.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im).astype(np.float32) * dark
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H * 0.47) / (H * 0.5)) ** 2)
    a *= np.clip(1.15 - 0.55 * d, 0.35, 1.0)[..., None]
    if warm:
        a *= np.array(warm, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def page_single(bg, mockup, out, no, sub, scale=0.9, cy=0.47, title=""):
    import editorial as E
    c = bg.copy()
    g = E._cut(mockup)
    g = g.resize((int(g.width * scale), int(g.height * scale)), Image.LANCZOS)
    k = min(1.0, 900 / g.width, 1150 / g.height)
    if k < 1.0:
        g = g.resize((int(g.width * k), int(g.height * k)), Image.LANCZOS)
    V._paste_soft(c, g, ((W - g.width) // 2, int(H * cy - g.height / 2)), halo=0.35)
    c = E._footer(E._header(c, no), title, sub)
    c.save(out, quality=96)
    return out


def page_stacked(bg, top_mk, bottom_mk, out, no, title="EX MUSEO", sub="FIRST LOOK", footer_y=1580):
    import editorial as E
    c = bg.copy()
    top, bottom, gap = 290, footer_y - 70, 40
    row_h = (bottom - top - gap) // 2
    for i, mk in enumerate([top_mk, bottom_mk]):
        g, _ = E._fit(E._cut(mk), W - 200, row_h)
        y = top + row_h // 2 + i * (row_h + gap)
        V._paste_soft(c, g, ((W - g.width) // 2, y - g.height // 2), halo=0.35)
    c = E._footer(E._header(c, no), title, sub, y=footer_y)
    c.save(out, quality=96)
    return out


def page_grid(bg, items, out, no, title="EX MUSEO", sub="FIRST LOOK", cy=0.45, gap=0.25, cell_h=560, footer_y=1548):
    import editorial as E
    c = bg.copy()
    xs, ys = (0.27, 0.73), (cy - gap / 2, cy + gap / 2)
    for i, mk in enumerate(items):
        g, _ = E._fit(E._cut(mk), W // 2 - 90, cell_h)
        x, y = xs[i % 2], ys[i // 2]
        V._paste_soft(c, g, (int(W * x - g.width / 2), int(H * y - g.height / 2)), halo=0.35)
    c = E._footer(E._header(c, no), title, sub, y=footer_y)
    c.save(out, quality=96)
    return out
