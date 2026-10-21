#!/usr/bin/env python3
"""Editorial stills: mockups stay untouched on black; typography does the work.

  catalogue(mockup, out, no, title, sub)   - exhibition-catalogue page
  detail(src, out, crop, grade)            - full-bleed art / product detail for match cuts
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
CG = lambda w, s: ImageFont.truetype(os.path.join(HERE, "fonts", f"cormorant-garamond-latin-{w}.woff"), s)
INK = (232, 226, 214)


def tracked(d, xy, text, font, fill, track=0.18, anchor="l"):
    """Draw letter-spaced text. anchor: l (left), m (centre), r (right) on x."""
    widths = [d.textlength(ch, font=font) for ch in text]
    sp = font.size * track
    total = sum(widths) + sp * (len(text) - 1)
    x, y = xy
    x = x - total / 2 if anchor == "m" else x - total if anchor == "r" else x
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill, anchor="ls")
        x += w + sp
    return total


def hairline(img, y, x0=90, x1=W - 90, alpha=0.32):
    a = np.asarray(img).astype(np.float32)
    a[y:y + 2, x0:x1] = a[y:y + 2, x0:x1] * (1 - alpha) + np.array(INK) * alpha
    return Image.fromarray(a.astype(np.uint8))


def catalogue(mockup, out, no, title, sub, year="MMXXVI", scale=0.9):
    c = Image.new("RGB", (W, H), (0, 0, 0))
    m = Image.open(mockup).convert("RGB")
    m = m.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
    c.paste(m, ((W - m.width) // 2, int(H * 0.47 - m.height / 2)))
    c = hairline(c, 214)
    c = hairline(c, 1548)
    d = ImageDraw.Draw(c)
    small = CG("500-normal", 30)
    tracked(d, (90, 190), no, small, INK)
    tracked(d, (W - 90, 190), year, small, INK, anchor="r")
    d.text((W / 2, 1655), title, font=CG("300-italic", 92), fill=INK, anchor="ms")
    tracked(d, (W / 2, 1735), sub, CG("500-normal", 26), (200, 194, 184), track=0.22, anchor="m")
    c.save(out, quality=96)
    return out


def detail(src, out, crop=None, warm=0.0, sat=1.0, bright=1.0, contrast=1.0, caption=None):
    im = Image.open(src).convert("RGB")
    if crop:
        im = im.crop(tuple(crop))
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    x0, y0 = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((x0, y0, x0 + W, y0 + H))
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Brightness(im).enhance(bright)
    if warm:
        a = np.asarray(im).astype(np.float32)
        a *= np.array([1 + warm, 1 + warm * 0.35, 1 - warm * 0.6])
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if caption:
        d = ImageDraw.Draw(im)
        tracked(d, (W / 2, 1735), caption, CG("500-normal", 28), INK, track=0.22, anchor="m")
    im.save(out, quality=96)
    return out
