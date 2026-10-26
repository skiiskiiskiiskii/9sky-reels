#!/usr/bin/env python3
"""Editorial stills: mockups stay untouched on black; typography does the work.

  catalogue(mockup, out, no, title, sub)   - exhibition-catalogue page
  detail(src, out, crop, grade)            - full-bleed art / product detail for match cuts
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

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


# ====================================================================== v2: more catalogue layouts
GREY = (168, 162, 152)


def dark_bg(src, kind="statue", level=0.2, crop=None, centre=0.35):
    """Very dark backdrop: only silhouettes / pattern read, centre darker so the garment sits clean."""
    im = Image.open(src).convert("RGB")
    if crop:
        im = im.crop(tuple(crop))
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    x0, y0 = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((x0, y0, x0 + W, y0 + H))
    if kind == "ornament":
        g = ImageEnhance.Contrast(im.convert("L")).enhance(1.6)
        im = Image.merge("RGB", [g, g, g])
    else:
        im = ImageEnhance.Color(im).enhance(0.35)
    im = im.filter(ImageFilter.GaussianBlur(1.6))
    a = np.asarray(im).astype(np.float32) * level
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W / 2) / (W * 0.55)) ** 2 + ((y - H * 0.46) / (H * 0.36)) ** 2)
    a *= (centre + (1 - centre) * np.clip(d, 0, 1) ** 1.4)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


LOGO = "/mnt/user-data/outputs/9sky_logo_white.png"


def logo(height, color=INK):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((int(lg.width * height / lg.height), height), Image.LANCZOS)
    a = lg.split()[-1]
    out = Image.new("RGBA", lg.size, color + (0,))
    out.putalpha(a)
    return out


def put_logo(c, cx, cy, height):
    lg = logo(height)
    c.paste(lg, (int(cx - lg.width / 2), int(cy - lg.height / 2)), lg)
    return c


def _cut(mockup):
    """Garment cut-out (RGBA, cropped) from a pure-black mockup.

    - holes inside the garment are filled only if they are fabric (dark lining), never
      if they are enclosed background (pure 0,0,0 gaps between sleeve and body);
    - edge pixels are un-premultiplied from the black background, so no dark fringe.
    """
    from scipy import ndimage
    im = Image.open(mockup).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    mx = a.max(2)
    m = ndimage.binary_closing(mx > 4, iterations=2)
    holes = ndimage.binary_fill_holes(m) & ~m
    lab, n = ndimage.label(holes)
    zero = (mx == 0)
    for i in range(1, n + 1):
        comp = lab == i
        if zero[comp].mean() < 0.6:          # fabric shadow (e.g. inside the hood) -> keep opaque
            m |= comp
    core = ndimage.binary_erosion(m, iterations=2)
    lum = mx
    fg = ndimage.maximum_filter(np.where(core, lum, 0), size=9)
    fg = np.where(fg > 0, fg, 255)
    alpha = np.where(core, 1.0, np.clip(lum / np.maximum(fg, 1), 0, 1))
    alpha = np.where(ndimage.binary_dilation(m, iterations=1), alpha, 0.0)
    rgb = np.where(alpha[..., None] > 0.02, a / np.maximum(alpha[..., None], 0.02), 0)
    rgb = np.where(core[..., None], a, np.clip(rgb, 0, 255))
    out = np.dstack([rgb, alpha * 255]).astype(np.uint8)
    o = Image.fromarray(out, "RGBA")
    return o.crop(o.getbbox())


def _garment(mockup, bg=False):
    if bg:
        return _cut(mockup)
    im = Image.open(mockup).convert("RGB")
    a = np.asarray(im).max(2) > 4
    ys, xs = np.where(a)
    pad = 12
    return im.crop((max(0, xs.min() - pad), max(0, ys.min() - pad), min(im.width, xs.max() + pad), min(im.height, ys.max() + pad)))


def _paste(c, g, xy):
    """Paste garment; on a backdrop add a soft dark halo so black fabric separates from the pattern."""
    if g.mode == "RGBA":
        al = np.asarray(g.split()[-1]).astype(np.float32)
        pad = 90
        halo = Image.new("L", (g.width + 2 * pad, g.height + 2 * pad), 0)
        halo.paste(Image.fromarray(al.astype(np.uint8)), (pad, pad))
        halo = halo.filter(ImageFilter.GaussianBlur(75)).point(lambda v: int(v * 0.4))
        c.paste(Image.new("RGB", halo.size, (0, 0, 0)), (xy[0] - pad, xy[1] - pad), halo)
        c.paste(g, xy, g)
    else:
        c.paste(g, xy)


def _fit(im, bw, bh):
    s = min(bw / im.width, bh / im.height)
    return im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS), s


def _frame(no, year="MMXXVI", bg=None):
    c = bg.copy() if bg is not None else Image.new("RGB", (W, H), (0, 0, 0))
    return c


def _header(c, no, year="MMXXVI"):
    c = hairline(c, 214)
    d = ImageDraw.Draw(c)
    small = CG("500-normal", 30)
    tracked(d, (90, 190), no, small, INK)
    tracked(d, (W - 90, 190), year, small, INK, anchor="r")
    return c


def _footer(c, title, sub, y=1548, kicker=None):
    c = hairline(c, y)
    d = ImageDraw.Draw(c)
    k = 0
    if kicker:                                    # small inscription in caps above the title (e.g. EX MUSEO)
        tracked(d, (W / 2, y + 72), kicker, CG("500-normal", 34), INK, track=0.42, anchor="m")
        k = 62
    if title and title.isupper():                 # a name in caps (EX MUSEO) is set like an inscription
        tracked(d, (W / 2, y + 105 + k), title, CG("400-normal", 80), INK, track=0.24, anchor="m")
    elif title:
        d.text((W / 2, y + 107 + k), title, font=CG("300-italic", 92), fill=INK, anchor="ms")
    if sub:
        sy = (y + 187 + k) if title else y + 80   # no title: the grey catalogue line sits under the rule
        tracked(d, (W / 2, sy), sub, CG("500-normal", 26), (200, 194, 184), track=0.22, anchor="m")
    return c


def _line(c, p0, p1, alpha=0.7, w=2):
    d = ImageDraw.Draw(c, "RGBA")
    d.line([p0, p1], fill=INK + (int(255 * alpha),), width=w)
    r = 6
    d.ellipse((p1[0] - r, p1[1] - r, p1[0] + r, p1[1] + r), outline=INK + (230,), width=2)


def page(mockup, out, no, title, sub, bg=None, scale=0.9):
    """Variant A (catalogue page) with optional dark backdrop."""
    c = _frame(no, bg=bg)
    if bg is None:
        m = Image.open(mockup).convert("RGB").resize((int(W * scale), int(H * scale)), Image.LANCZOS)
        c.paste(m, ((W - m.width) // 2, int(H * 0.47 - m.height / 2)))
    else:
        g = _cut(mockup)
        g = g.resize((int(g.width * scale), int(g.height * scale)), Image.LANCZOS)
        _paste(c, g, ((W - g.width) // 2, int(H * 0.47 - g.height / 2)))
    c = _footer(_header(c, no), title, sub)
    c.save(out, quality=96)
    return out


def annotated(mockup, out, no, title, sub, notes, bg=None):
    """notes: [(px, py) point in mockup coords, label, (lx, ly) label baseline, anchor l|r]"""
    c = _frame(no, bg=bg)
    s = 0.84
    ox, oy = int((W - W * s) / 2), int(H * 0.47 - H * s / 2)
    if bg is None:
        m = Image.open(mockup).convert("RGB").resize((int(W * s), int(H * s)), Image.LANCZOS)
        c.paste(m, (ox, oy))
    else:
        im = Image.open(mockup).convert("RGB")
        g = _cut(mockup)
        bb = Image.fromarray((np.asarray(im).max(2) > 4).astype(np.uint8) * 255).getbbox()
        g = g.resize((int(g.width * s), int(g.height * s)), Image.LANCZOS)
        _paste(c, g, (int(ox + bb[0] * s), int(oy + bb[1] * s)))
    c = _header(c, no)
    d = ImageDraw.Draw(c)
    f = CG("500-normal", 25)
    for (px, py), label, (lx, ly), anc in notes:
        p = (ox + px * s, oy + py * s)
        tw = tracked(d, (lx, ly), label, f, INK, track=0.2, anchor=anc)
        end_x = lx + tw + 14 if anc == "l" else lx - tw - 14
        _line(c, (end_x, ly - 9), p)
    c = _footer(c, title, sub)
    c.save(out, quality=96)
    return out


def record(mockup, out, no, rows, foot, bg=None):
    """Museum collection record: object above, data table below."""
    c = _frame(no, bg=bg)
    g, _ = _fit(_garment(mockup, bg is not None), 760, 560)
    _paste(c, g, ((W - g.width) // 2, int(H * 0.33 - g.height / 2)))
    c = hairline(_header(c, no), 1000)
    d = ImageDraw.Draw(c)
    y = 1080
    for k, v in rows:
        tracked(d, (90, y), k, CG("500-normal", 24), GREY, track=0.22)
        d.text((430, y + 2), v, font=CG("400-italic", 44), fill=INK, anchor="ls")
        y += 84
    c = hairline(c, y - 30)
    put_logo(c, W / 2, y + 48, 66)
    d = ImageDraw.Draw(c)
    tracked(d, (W / 2, y + 140), foot, CG("500-normal", 24), (200, 194, 184), track=0.24, anchor="m")
    c.save(out, quality=96)
    return out


def spread(art, art_crop, art_cap, art_sub, mockup, cap, sub, out, no, bg=None):
    """Catalogue spread: antique plate on top, the garment below."""
    c = _frame(no, bg=bg)
    box = (90, 250, W - 90, 880)
    a = Image.open(art).convert("RGB")
    if art_crop:
        a = a.crop(tuple(art_crop))
    bw, bh = box[2] - box[0], box[3] - box[1]
    s = max(bw / a.width, bh / a.height)
    a = a.resize((int(a.width * s + 1), int(a.height * s + 1)), Image.LANCZOS)
    x0, y0 = (a.width - bw) // 2, (a.height - bh) // 2
    a = ImageEnhance.Color(a.crop((x0, y0, x0 + bw, y0 + bh))).enhance(0.8)
    c.paste(a, box[:2])
    c = _header(c, no)
    d = ImageDraw.Draw(c)
    d.text((W / 2, 950), art_cap, font=CG("400-italic", 50), fill=INK, anchor="ms")
    tracked(d, (W / 2, 1000), art_sub, CG("500-normal", 24), GREY, track=0.22, anchor="m")
    g, _ = _fit(_garment(mockup, bg is not None), 760, 500)
    _paste(c, g, ((W - g.width) // 2, int(1330 - g.height / 2)))
    d = ImageDraw.Draw(c)
    d.text((W / 2, 1680), cap, font=CG("400-italic", 50), fill=INK, anchor="ms")
    tracked(d, (W / 2, 1730), sub, CG("500-normal", 24), GREY, track=0.22, anchor="m")
    c.save(out, quality=96)
    return out


def plates(mockups, words, out, no, title, sub, bg=None):
    c = _frame(no, bg=bg)
    n = len(mockups)
    cw = (W - 180 - 40 * (n - 1)) // n
    pos = []
    for i, mk in enumerate(mockups):
        g, _ = _fit(_garment(mk, bg is not None), cw, 700)
        cx = 90 + i * (cw + 40) + cw // 2
        y0 = int(H * 0.45 - g.height / 2)
        _paste(c, g, (cx - g.width // 2, y0))
        pos.append((cx, y0 + g.height))
    c = _header(c, no)
    d = ImageDraw.Draw(c)
    for (cx, bottom), word in zip(pos, words):
        tracked(d, (cx, bottom + 70), word, CG("500-normal", 28), GREY, track=0.26, anchor="m")
    c = _footer(c, title, sub)
    c.save(out, quality=96)
    return out


def poster(mockup, out, big, under, line1, line2, bg=None):
    c = _frame("", bg=bg)
    g, _ = _fit(_garment(mockup, bg is not None), 900, 620)
    _paste(c, g, ((W - g.width) // 2, int(1040 - g.height / 2)))
    put_logo(c, W / 2, 205, 92)
    d = ImageDraw.Draw(c)
    d.text((W / 2, 545), big, font=CG("300-italic", 230), fill=INK, anchor="ms")
    tracked(d, (W / 2, 630), under, CG("500-normal", 30), (210, 204, 194), track=0.34, anchor="m")
    c = hairline(c, 1450, 300, W - 300)
    d = ImageDraw.Draw(c)
    d.text((W / 2, 1570), line1, font=CG("400-italic", 52), fill=INK, anchor="ms")
    tracked(d, (W / 2, 1660), line2, CG("500-normal", 28), GREY, track=0.3, anchor="m")
    c.save(out, quality=96)
    return out


def index(mockups, out, no, title, sub, bg=None):
    c = _frame(no, bg=bg)
    for i, mk in enumerate(mockups):
        col, row = i % 2, i // 2
        cx, cy = 90 + 225 + col * 450, 600 + row * 520
        g, _ = _fit(_garment(mk, bg is not None), 430, 410)
        _paste(c, g, (cx - g.width // 2, cy - g.height // 2))
    c = _header(c, no)
    c = _footer(c, title, sub)
    c.save(out, quality=96)
    return out


def stacked(front, back, out, no, title, sub, bg=None, footer_y=1580, kicker=None):
    """Pair fronts on top (white overlapping black), pair backs below - big and centred."""
    if kicker:
        footer_y -= 50                            # make room for the extra line
    c = _frame(no, bg=bg)
    top, bottom, gap = 290, footer_y - 70, 40
    row_h = (bottom - top - gap) // 2
    for i, mk in enumerate([front, back]):
        g, _ = _fit(_garment(mk, bg is not None), W - 200, row_h)
        cy = top + row_h // 2 + i * (row_h + gap)
        _paste(c, g, ((W - g.width) // 2, cy - g.height // 2))
    c = _header(c, no)
    c = _footer(c, title, sub, y=footer_y, kicker=kicker)
    c.save(out, quality=96)
    return out
