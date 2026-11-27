#!/usr/bin/env python3
"""2026-11-27: other kinds of on-screen text for the hook (Kirill: change the approach to the lines completely).
Each function returns (rgb float HxWx3, alpha HxWx1 0..1) like compose.text_layer, for loopreel.make(layer=...).

label(...)  - a museum wall label (off-white card, black type): the scene described as an exhibit
quote(...)  - "OVERHEARD IN PRAGUE" + a stranger's line in quotes
chat(...)   - a short text-message exchange (her on the left, him on the right)"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
F = {"cg-i": "cormorant-garamond-latin-400-italic.woff", "cg-600": "cormorant-garamond-latin-600-normal.woff",
     "cg-500": "cormorant-garamond-latin-500-normal.woff", "inter": "Inter-Regular.otf", "inter-m": "Inter-Medium.otf",
     "inter-sb": "Inter-SemiBold.otf", "inter-i": "Inter-Italic.otf"}


def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", F[name]), size)


def tracked(d, xy, text, f, fill, track, anchor="l"):
    """text with letter-spacing; anchor l = xy is the left end, m = xy is the middle (baseline-ish via 'ls')"""
    widths = [d.textlength(ch, font=f) for ch in text]
    total = sum(widths) + track * (len(text) - 1)
    x, y = xy
    if anchor == "m":
        x -= total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=f, fill=fill, anchor="ls")
        x += w + track
    return total


def _out(img):
    a = np.asarray(img).astype(np.float32)
    return a[..., :3], a[..., 3:4] / 255.0


def _shadow(img, r=10, alpha=110):
    """a soft dark shadow under everything drawn in img (for cards / bubbles on busy footage)"""
    a = img.split()[3]
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh.putalpha(a.point(lambda v: min(alpha, v)))
    sh = sh.filter(ImageFilter.GaussianBlur(r))
    return Image.alpha_composite(sh, img)


def label(title, lines, sub, x=80, y=230, w=720):
    """museum wall label: title in spaced capitals, an italic line or two, small sans lines under a rule"""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    ft, fi, fs = font("inter-sb", 33), font("cg-i", 64), font("inter", 30)
    pad = 44
    h = pad + 32 + 26 + len(lines) * 70 + 40 + len(sub) * 44 + pad - 6
    d.rectangle((x, y, x + w, y + h), fill=(238, 233, 224, 240))
    cy = y + pad + 30
    tracked(d, (x + pad, cy), title, ft, (18, 16, 14, 255), 6)
    cy += 26
    for ln in lines:
        cy += 70
        d.text((x + pad, cy), ln, font=fi, fill=(18, 16, 14, 255), anchor="ls")
    cy += 34
    d.line((x + pad, cy, x + pad + 120, cy), fill=(18, 16, 14, 200), width=2)
    cy += 6
    for ln in sub:
        cy += 44
        d.text((x + pad, cy), ln, font=fs, fill=(40, 37, 33, 255), anchor="ls")
    img = Image.alpha_composite(img, _shadow(card, 14, 120))
    return _out(img)


def quote(kicker, text_lines, y=330, size=84):
    """small spaced capitals above a large italic quote, centred, on a soft dark band"""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fk, fq = font("inter-m", 28), font("cg-i", size)
    lh = int(size * 1.12)
    top = y - 90
    bottom = y + lh * len(text_lines) + 10
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(band).rectangle((-100, top - 40, W + 100, bottom + 30), fill=(0, 0, 0, 120))
    img = Image.alpha_composite(img, band.filter(ImageFilter.GaussianBlur(40)))
    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)
    tracked(d, (W / 2, y - 40), kicker, fk, (255, 255, 255, 215), 7, anchor="m")
    for i, ln in enumerate(text_lines):
        d.text((W / 2, y + lh * (i + 1) - 22), ln, font=fq, fill=(255, 255, 255, 250), anchor="ms")
    img = Image.alpha_composite(img, _shadow(txt, 8, 150))
    return _out(img)


def chat(msgs, stamp="today 21:47", y=200, size=42):
    """text bubbles: msgs = [("her" | "him", text), ...]; her = dark bubble on the left, him = light bubble on the right"""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f, fs = font("inter", size), font("inter-m", 24)
    tracked(d, (W / 2, y), stamp.upper(), fs, (255, 255, 255, 190), 4, anchor="m")
    cy = y + 34
    for who, text in msgs:
        tw = d.textlength(text, font=f)
        bw, bh = tw + 2 * 34, size + 2 * 24
        if who == "her":
            x0, fill, ink = 70, (38, 36, 34, 235), (255, 255, 255, 255)
        else:
            x0, fill, ink = W - 70 - bw, (236, 231, 222, 245), (18, 16, 14, 255)
        d.rounded_rectangle((x0, cy, x0 + bw, cy + bh), radius=bh // 2, fill=fill)
        d.text((x0 + 34, cy + bh / 2), text, font=f, fill=ink, anchor="lm")
        cy += bh + 16
    img = Image.alpha_composite(img, _shadow(lay, 12, 120))
    return _out(img)


if __name__ == "__main__":       # previews on a grey frame
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/textcards.jpg"
    bg = np.full((H, W, 3), 70, np.float32)
    tiles = []
    for rgb, a in [label("EXHIBIT N° IX", ["red soles, red collar."], ["found together. prague, 2026.", "on loan from the museum - never returned."]),
                   quote("OVERHEARD IN PRAGUE", ["“wait, is his collar", "red too?”"]),
                   chat([("her", "wear the black one tonight"), ("him", "the one with the red inside?"), ("her", "obviously")])]:
        tiles.append(Image.fromarray((bg * (1 - a) + rgb * a).astype(np.uint8)).resize((360, 640)))
    c = Image.new("RGB", (1100, 640))
    for i, t in enumerate(tiles):
        c.paste(t, (i * 370, 0))
    c.save(out)
