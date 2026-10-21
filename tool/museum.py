#!/usr/bin/env python3
"""Museum-style stills for the post-drop part of a reel (static, no zoom).

  exhibit  - garment hung as a painting in a gold frame on a museum wall + label
  palette  - colour chips (from the hook's last frame) + garment
  wall     - garment cut-out on a red damask wall under a spotlight + brass plaque

usage (python):  from museum import exhibit, palette_freeze, palette_card, wall
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
F = lambda n, s: ImageFont.truetype(os.path.join(HERE, "fonts", n), s)
W, H = 1080, 1920
BG = "/mnt/user-data/outputs/museum-bg/"


def cutout(path, thr=4):
    """RGBA cut-out of the garment(s) from a pure-black mockup, cropped to bbox."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    m = a.max(2) > thr
    m = ndimage.binary_closing(m, iterations=3)
    m = ndimage.binary_fill_holes(m)
    lab, n = ndimage.label(m)
    if n > 1:                                   # drop specks
        sizes = ndimage.sum(m, lab, range(1, n + 1))
        keep = [i + 1 for i, s in enumerate(sizes) if s > 0.02 * sizes.max()]
        m = np.isin(lab, keep)
    alpha = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    rgba = im.copy()
    rgba.putalpha(alpha)
    return rgba.crop(rgba.getbbox())


def fit(img, box_w, box_h):
    s = min(box_w / img.width, box_h / img.height)
    return img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)


def shadow(rgba, blur=28, alpha=0.75, off=(0, 18)):
    a = np.asarray(rgba.split()[-1]).astype(np.float32) * alpha
    pad = blur * 3
    sh = Image.new("L", (rgba.width + 2 * pad, rgba.height + 2 * pad), 0)
    sh.paste(Image.fromarray(a.astype(np.uint8)), (pad, pad))
    return sh.filter(ImageFilter.GaussianBlur(blur)), pad, off


def radial(w, h, cx, cy, rx, ry, power=1.6):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
    return np.clip(1 - d, 0, 1) ** power


def label_block(draw, x, y, lines, color=(236, 232, 224), scale=1.0):
    """lines: list of (text, style) with style in title|sub|italic|body"""
    styles = {"title": ("Inter-SemiBold.otf", 30), "sub": ("Inter-Regular.otf", 20),
              "italic": ("Inter-Italic.otf", 28), "body": ("Inter-Regular.otf", 21)}
    gap = {"title": 6, "sub": 18, "italic": 8, "body": 6}
    for text, st in lines:
        f = F(styles[st][0], int(styles[st][1] * scale))
        draw.text((x, y), text, font=f, fill=color)
        y += int(f.size * 1.25) + gap[st]
    return y


# ---------------------------------------------------------------- exhibit
FRAME_IN = (313, 587, 918, 1351)               # painting area inside the gold frame
LABEL_AT = (140, 1520)


def exhibit(mockup, out, label):
    bg = Image.open(BG + "frame_still.png").convert("RGB")
    a = np.asarray(bg).astype(np.float32)
    # erase the original wall label with the surrounding wall tone
    x0, y0, x1, y1 = 90, 1530, 760, 1790
    tone = np.median(a[y0 - 60:y0 - 10, x0:x1].reshape(-1, 3), axis=0)
    patch = np.ones((y1 - y0, x1 - x0, 3), np.float32) * tone
    patch += np.random.default_rng(1).normal(0, 1.2, patch.shape)
    a[y0:y1, x0:x1] = patch
    bg = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    # dark canvas inside the frame with a soft top light
    fx0, fy0, fx1, fy1 = FRAME_IN
    cw, ch = fx1 - fx0, fy1 - fy0
    glow = radial(cw, ch, cw / 2, ch * 0.35, cw * 0.9, ch * 0.8)
    canvas = np.zeros((ch, cw, 3), np.float32) + np.array([24, 23, 23])
    canvas += glow[..., None] * np.array([46, 42, 38])
    canvas = Image.fromarray(canvas.astype(np.uint8))
    g = fit(cutout(mockup), cw * 0.86, ch * 0.86)
    canvas.paste(g, ((cw - g.width) // 2, (ch - g.height) // 2 + int(ch * 0.02)), g)
    # inner shadow so the picture sits behind the frame lip
    c = np.asarray(canvas).astype(np.float32)
    yy, xx = np.mgrid[0:ch, 0:cw]
    edge = np.minimum.reduce([xx, cw - xx, yy, ch - yy]).astype(np.float32)
    c *= (0.55 + 0.45 * np.clip(edge / 40, 0, 1))[..., None]
    bg.paste(Image.fromarray(c.astype(np.uint8)), (fx0, fy0))
    d = ImageDraw.Draw(bg)
    label_block(d, LABEL_AT[0], LABEL_AT[1], label, scale=1.15)
    bg = bg.crop((100, 140, 1040, 1811)).resize((W, H), Image.LANCZOS)   # static framing, frame fills the screen
    bg.save(out, quality=95)
    return out


# ---------------------------------------------------------------- palette
def pick_palette(imgs, n=4):
    """red, gold/warm, dark, light picked from hook frames (fallbacks if absent)."""
    if not isinstance(imgs, (list, tuple)):
        imgs = [imgs]
    strip = np.concatenate([np.asarray(i.convert("RGB").resize((180, 320))) for i in imgs], axis=1)
    q = Image.fromarray(strip.astype(np.uint8)).quantize(16, method=Image.MEDIANCUT)
    pal = np.array(q.getpalette()[:48]).reshape(16, 3)
    counts = np.bincount(np.asarray(q).ravel(), minlength=16)
    cols = [(tuple(pal[i]), counts[i]) for i in range(16) if counts[i] > 0]
    def best(score):
        return max(cols, key=lambda c: score(np.array(c[0])) * (c[1] ** 0.3))[0]
    red = best(lambda c: (c[0] - max(c[1], c[2])) * (c[0] > 90))
    gold = best(lambda c: (min(c[0], c[1]) - c[2]) * (c[1] > 90) * (c[0] > 120))
    if red[0] - max(red[1], red[2]) < 50:
        red = (138, 20, 30)
    dark = (14, 12, 12)
    light = (236, 230, 220)
    return [red, gold, dark, light]


def chips(draw, colors, cy, size=128, gap=26, labels=True):
    n = len(colors)
    total = n * size + (n - 1) * gap
    x = (W - total) // 2
    f = F("Inter-Regular.otf", 22)
    for c in colors:
        draw.rectangle((x, cy - size // 2, x + size, cy + size // 2), fill=tuple(int(v) for v in c),
                       outline=(235, 230, 222), width=2)
        if labels:
            hx = "#%02X%02X%02X" % tuple(int(v) for v in c)
            draw.text((x + size / 2, cy + size // 2 + 26), hx, font=f, fill=(225, 220, 212), anchor="mm")
        x += size + gap


def palette_freeze(frame_img, out, colors, dim=0.5, cy=0.74):
    im = frame_img.convert("RGB").resize((W, H))
    im = Image.fromarray((np.asarray(im).astype(np.float32) * dim).astype(np.uint8))
    chips(ImageDraw.Draw(im), colors, int(H * cy))
    im.save(out, quality=95)
    return out


def palette_card(mockup, out, colors, cy=0.84):
    im = Image.new("RGB", (W, H), (0, 0, 0))
    g = fit(cutout(mockup), W * 0.86, H * 0.5)
    im.paste(g, ((W - g.width) // 2, int(H * 0.47 - g.height / 2)), g)
    chips(ImageDraw.Draw(im), colors, int(H * cy), size=110, gap=22)
    im.save(out, quality=95)
    return out


# ---------------------------------------------------------------- wall
def damask_bg():
    src = Image.open(BG + "red_wall.png").convert("RGB")
    crop = src.crop((20, 240, 600, 1270))                  # plain damask area
    bg = crop.resize((W, int(W * crop.height / crop.width)), Image.LANCZOS)
    bg = bg.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2.2))
    a = np.asarray(bg).astype(np.float32)
    spot = radial(W, H, W / 2, H * 0.40, W * 0.85, H * 0.55, power=1.3)
    a *= (0.22 + 0.78 * spot)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def wall(mockups, out, plaque=None):
    bg = damask_bg()
    gs = [cutout(m) for m in mockups]
    n = len(gs)
    box_w = W * (0.74 if n == 1 else 0.46)
    gs = [fit(g, box_w, H * 0.42) for g in gs]
    xs = [(W - gs[0].width) // 2] if n == 1 else [int(W * 0.27 - gs[0].width / 2), int(W * 0.73 - gs[1].width / 2)]
    cy = H * 0.43
    for g, x in zip(gs, xs):
        sh, pad, off = shadow(g)
        y = int(cy - g.height / 2)
        dark = Image.new("RGB", sh.size, (0, 0, 0))
        bg.paste(dark, (x - pad + off[0], y - pad + off[1]), sh)
        bg.paste(g, (x, y), g)
    if plaque:
        d = ImageDraw.Draw(bg)
        pw, ph = 470, 170
        px, py = (W - pw) // 2, int(H * 0.69)
        brass = Image.new("RGB", (pw, ph))
        grad = np.linspace(0, 1, pw)[None, :, None]
        base = np.array([150, 118, 62]) * (0.75 + 0.35 * np.sin(grad * 3.1))
        brass = Image.fromarray(np.broadcast_to(base, (ph, pw, 3)).astype(np.uint8))
        bg.paste(brass, (px, py))
        d.rectangle((px, py, px + pw - 1, py + ph - 1), outline=(92, 70, 36), width=3)
        f1, f2 = F("Inter-SemiBold.otf", 36), F("Inter-Regular.otf", 26)
        d.text((W / 2, py + 60), plaque[0], font=f1, fill=(40, 28, 14), anchor="mm")
        d.text((W / 2, py + 114), plaque[1], font=f2, fill=(48, 34, 18), anchor="mm")
    bg.save(out, quality=95)
    return out
