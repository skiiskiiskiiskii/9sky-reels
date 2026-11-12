#!/usr/bin/env python3
"""2026-11-12, batch 1112a: 5 reels. Every top reel so far (F05 63K, H08 12.6K, E03 4.8K, G01 4.5K) has
the COUPLE clip, a short style-rule line at the top and black quarter zip (or knit) pages, so 3 reels
stay on that, with new angles; 2 try something new while keeping the red link.

K01 match her red        - COUPLE from his shoes to her sole; a line for him (send this to him)
K02 never show all red   - H08 recipe (nails -> sole slow-down, knit) with a new rule
K03 red collar, 1460     - NEW: Rogier van der Weyden's Francesco d'Este (Met, CC0): black with a red
                           collar; slow push-in onto the collar, cut to our collar = "ex museo"
K04 one rose             - rose -> sole, rule line about one red detail
K05 his black hers white - COUPLE wide (both of them), pages his black / her white quarter zip
All on the F05 timing (pages 1 beat at 99 BPM, finale 4 beats) - post with the F05 audio."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, ARA, ROME, SP, P, O
from vitrine import vpage, vstacked
import paintclip

GR = dict(c=1.04, s=0.92, b=-0.012)
DROP, BMP = 3.13, 60 / 99.0
C2 = DROP - 2 * BMP
MP = "mrpopular"
NUMS = ["I", "II", "III", "IV"]
ROSE = "/mnt/user-data/uploads/flowers hooks/"
HERE = os.path.dirname(os.path.abspath(__file__))
PAINT = os.path.join(HERE, "..", "out", "hooks", "paint_deste_in.mp4")
if not os.path.exists(PAINT):              # push-in that keeps moving into the cut (ease-in), ends on the collar
    paintclip.make("/mnt/user-data/uploads/9sky-reels/hooks/art-met/9sky_art_m1_05.jpg", PAINT, 885, 1045,
                   dur=3.2, ease="in", y1=1250)       # collar low enough that the face clears the line


def lb(key, start=None, dur=None, speed=1.12, flip=False, crop_x=0.5, crop_y=0.5, zoom=1.2, lead=0.42, **kw):
    d = dict(type="clip", src=P[key], speed=speed, zoom=zoom, crop_x=crop_x, crop_y=crop_y, flip=flip, grade=GR)
    d.update(dict(align_red=True, lead=lead) if start is None else dict(start=start, align_red=False))
    d.update(dict(dur=dur) if dur else dict(until="drop"))
    d.update(kw)
    return d


def clip(src, start=0.0, dur=None, speed=1.0, zoom=1.0, crop_y=0.5, flip=False, grade=GR, **kw):
    d = dict(type="clip", src=src, start=start, align_red=False, speed=speed, zoom=zoom,
             crop_x=0.5, crop_y=crop_y, flip=flip, grade=grade)
    d.update(dict(dur=dur) if dur else dict(until="drop"))
    d.update(kw)
    return d


def ramp(key, onset, total, slow=0.55, rate=0.5, pre=1.0, **kw):
    s_end = onset + 0.13
    s_slow = s_end - slow * rate
    first = total - slow
    return [lb(key, start=s_slow - first * pre, dur=first, speed=pre, **kw),
            lb(key, start=s_slow, speed=rate, smooth=True, **kw)]


def t(text, y=0.22, scrim=0.5):
    return [{"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": scrim, "font": "cg-italic"}]


QBK = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
K = [  # key, tone, hook, texts, pages, finale, idea
    ("K01_match-her-red", "vitrine",
     [lb("SOLES", start=4.3 - (DROP - 0.42), speed=1.0, zoom=1.1, crop_y=0.6)],
     t("match her red."), QBK, ("KF", "KB"), "SOLES: her red nails, his black shoes, her logo sole; a line for him"),
    ("K02_never-show-all-the-red", "slate",
     [lb("NAILS", start=1.6, dur=C2, speed=1.1, zoom=1.0)]
     + ramp("COUPLE", 4.7, DROP - C2, slow=0.6, crop_y=0.76, crop_x=0.42, zoom=1.3, flip=True),
     t("never show\nall the red."), [("SWF", cat(1, "BLACK KNIT")), ("KF", cat(2, COLLAR))], ("SPF", "SPB"),
     "H08 recipe (nails -> sole slow-down, knit), new rule line"),
    ("K03_red-collar-1460", "vitrine",
     [clip(PAINT, grade={})],
     t("black with a red collar,\naround 1460.", y=0.16), QBK, ("KF", "KB"),
     "painting push-in onto a 1460 red collar -> our collar"),
    ("K04_one-rose", "vitrine",
     [clip(ROSE + "g1.mp4", start=0.3, dur=C2, zoom=1.15, crop_y=0.3, grade={}),
      lb("NAILS", start=5.935 - (DROP - C2) * 0.7, speed=0.7, zoom=1.2, crop_y=0.55, smooth=True)],
     t("one rose,\nnever a bouquet."), [("PF", cat(1, "BLACK  ·  WHITE  ·  ONE RED")), ("PB", cat(2, ARA, ROME))],
     ("PF", "PB"), "rose -> her heel lifts (slowed), rule line about one red detail"),
    ("K05_his-black-hers-white", "vitrine",
     [lb("COUPLE", speed=1.12, zoom=1.0, crop_y=0.6)],
     t("his in black.\nhers in white."), [("KF", cat(1, "HIS  ·  BLACK")), ("WF", cat(2, "HERS  ·  WHITE"))],
     ("PF", "PB"), "COUPLE wide (both of them), his black / her white quarter zip"),
]


def build(batch, rows, out_prefix, seed0):
    ledger = []
    for i, (k, tone, hook, texts, pg, fin, idea) in enumerate(rows):
        tag = f"k{i + 1:02d}z"
        pages = [img(vpage(P[pk], O + f"{tag}{j}.jpg", "N° " + NUMS[j], sub, tone), 1) for j, (pk, sub) in enumerate(pg)]
        fimg = vstacked(P[fin[0]], P[fin[1]], O + f"{tag}c.jpg", "N° " + NUMS[len(pg)], tone=tone)
        spec = dict(seed=seed0 + i, track=MP, segments=hook + pages + [img(fimg, 4)], texts=texts)
        json.dump(spec, open(os.path.join(SP, f"{out_prefix}_{k}.json"), "w"), indent=1)
        ledger.append([batch, k, MP, tone, texts[0]["text"].replace("\n", " "), idea])
        print(f"{out_prefix}_{k}")
    json.dump(ledger, open(os.path.join(SP, f"ledger_{batch}.json"), "w"), indent=1)


build("1112a", K, "k1112", 30000)
