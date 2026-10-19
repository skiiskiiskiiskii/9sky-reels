#!/usr/bin/env python3
"""Rebuild a 9sky collage template with three new aesthetic panels in the bottom row."""
import sys
from PIL import Image, ImageFilter
BOXES = [(50, 968, 374, 1612), (377, 968, 702, 1612), (705, 968, 1029, 1612)]

def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
    x0, y0 = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x0, y0, x0 + w, y0 + h))

def build(template, panels, out):
    base = Image.open(template).convert("RGB").resize((1080, 1920))
    for (x0, y0, x1, y1), p in zip(BOXES, panels):
        base.paste((0, 0, 0), (x0 - 2, y0 - 2, x1 + 2, y1 + 2))
        tile = cover(Image.open(p).convert("RGB"), x1 - x0, y1 - y0)
        tile = tile.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=2))
        base.paste(tile, (x0, y0))
    base.save(out, quality=95)

if __name__ == "__main__":
    build(sys.argv[1], sys.argv[3:6], sys.argv[2])
