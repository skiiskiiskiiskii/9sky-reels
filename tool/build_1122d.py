#!/usr/bin/env python3
"""2026-11-22 06:23, batch 1122d: v3 of the colour moodboards, Kirill's notes on v2:
- after the drop keep the mockup frames we already use (vitrine pages + stacked EX MUSEO finale, the F05 formula);
  we will work on them separately
- the references have no jumps, colour changes or camera moving in different directions - those effects look cheap.
So: still pictures, no push-in / pull-out, no strobe, no grey world, no grain, no vignette, no grading per shot.
Straight cuts on the beat grid that ends on the drop, then 2 pages (1 beat each) + finale (4 beats) = 6.77 s.

A01v3 my color.            dark red, 5 pictures on the beat; black quarter zip pages, oxblood
A02v3 if i was a color     black (statues, dark rooms, a little red), 10 pictures on the half beat in a square band
                           (the reference is letterboxed too); black zip hoodie pages, slate
A03v3 if aura had a color. burgundy, 5 pictures on the beat; white zip hoodie pages, zip pair finale, vitrine
A04v3 favourite color.     black + dark red, 3 pictures on the beat then 4 on the half beat into the drop;
                           black quarter zip + black zip hoodie pages, quarter zip pair finale, oxblood
Post with the F05 sound (drop on the cut at 3.1 s)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from build_1024 import img, cat, COLLAR, HOOD, ARA, ROME, SP, P, O
from build_1115 import MP
from build_1122b import aes, ff, met
from vitrine import vpage, vstacked

W, H = 1080, 1920
DROP, B = 3.13, 60 / 99.0
NUMS = ["I", "II", "III"]


def still(sh, out, band=None):
    """the picture as one static 1080x1920 frame: cover-crop around `focus`, or inside a letterbox band"""
    im = Image.open(sh["img"]).convert("RGB")
    bw, bh = (W, H) if not band else (W, int((band[1] - band[0]) * H))
    s = max(bw / im.width, bh / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    fx, fy = sh.get("focus", (0.5, 0.5))
    x0 = int(min(max(0, fx * im.width - bw / 2), im.width - bw))
    y0 = int(min(max(0, fy * im.height - bh / 2), im.height - bh))
    c = Image.new("RGB", (W, H), "black")
    c.paste(im.crop((x0, y0, x0 + bw, y0 + bh)), (0, 0 if not band else int(band[0] * H)))
    c.save(out, quality=95)
    return out


def grid(steps):
    """cut lengths that end exactly on the drop: steps in beats, listed from the first picture to the last;
    the first picture also takes whatever is left before the grid starts"""
    lens = [s * B for s in steps]
    lens[0] += DROP - sum(lens)
    return lens


R = [  # key, tone, text, text size, pictures, steps (beats), band, pages, finale
    ("A01v3_my-color", "oxblood", "my color.", 56,
     [met("m2_02", focus=(0.5, 0.42)), aes("candles_red", 14), aes("theatre_red", 24), aes("busts_red", 22),
      aes("theatre_red", 22)],
     [1] * 5, None, [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))], ("KF", "KB")),
    ("A02v3_if-i-was-a-color", "slate", "if i was a color", 46,
     [ff(55), ff(53), ff(65), ff(63), aes("candles_red", 28), ff(57), aes("theatre_red", 14), ff(44),
      aes("busts_red", 11), aes("theatre_red", 21)],
     [0.5] * 10, (0.22, 0.78), [("ZF", cat(1, HOOD)), ("ZB", cat(2, ARA, ROME))], ("ZF", "ZB")),
    ("A03v3_if-aura-had-a-color", "vitrine", "if aura had a color.", 54,
     [aes("palace_red", 3), aes("theatre_red", 2), aes("people_museum", 3), aes("gallery_red", 27),
      aes("busts_red", 26)],
     [1] * 5, None, [("XWF", cat(1, HOOD)), ("XWB", cat(2, ARA, ROME))], ("ZPF", "ZPB")),
    ("A04v3_favourite-color", "oxblood", "favourite color.", 54,
     [aes("palace_red", 8), ff(47), aes("candles_red", 11), aes("theatre_red", 20), aes("candles_red", 24),
      aes("busts_red", 4), aes("theatre_red", 7)],
     [1, 1, 1, 0.5, 0.5, 0.5, 0.5], None, [("KF", cat(1, COLLAR)), ("ZF", cat(2, HOOD))], ("PF", "PB")),
]


def build(batch="1122d", prefix="d1122", seed0=38000):
    ledger = []
    for i, (k, tone, text, size, pics, steps, band, pages, fin) in enumerate(R):
        tag = f"d{i + 1:02d}"
        segs = [img(still(sh, O + f"{tag}p{j}.jpg", band), dur=round(d, 4))
                for j, (sh, d) in enumerate(zip(pics, grid(steps)))]
        segs += [img(vpage(P[pk], O + f"{tag}y{j}.jpg", "N° " + NUMS[j], sub, tone), 1) for j, (pk, sub) in enumerate(pages)]
        segs += [img(vstacked(P[fin[0]], P[fin[1]], O + f"{tag}yc.jpg", "N° " + NUMS[len(pages)], tone=tone), 4)]
        texts = [{"text": text, "from": 0, "to": "drop", "y": 0.5 if band else 0.48, "size": size, "font": "cg-400"}]
        spec = dict(seed=seed0 + i, track=MP, segments=segs, texts=texts)
        json.dump(spec, open(os.path.join(SP, f"{prefix}_{k}.json"), "w"), indent=1, ensure_ascii=False)
        ledger.append([batch, k, MP, tone, text, f"{len(pics)} still pictures, steps {steps}, then F05 pages"])
        print(f"{prefix}_{k}", [round(sum(grid(steps)[:n + 1]), 3) for n in range(len(steps))])
    json.dump(ledger, open(os.path.join(SP, f"ledger_{batch}.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    build()
