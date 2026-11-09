#!/usr/bin/env python3
"""2026-11-09 evening: two batches of 6, each with its own change (Kirill: every batch new).

1109c - new hook treatments, F05 page set (pages switch every beat, stacked finale):
  freeze  : the hook stops on the red sole for the last 0.4 s (a held frame, no flash, no zoom)
  short   : 1 page + finale, ~5.6 s, for loops
  slow    : the whole hook smoothly slowed (motion-interpolated)
  rose    : rose straight into the oxblood pages, no shoes
1109d - new ending and pacing: slower pages (2 beats each) and a single big back plate with the
        EX MUSEO inscription as the finale; hooks are new pairings (curtain -> sole, statue -> sole,
        3 shots on the beat)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, IX, ARA, ROME, HOOD, SP, P, O
from vitrine import vpage, vstacked

GR = dict(c=1.04, s=0.92, b=-0.012)
BMP, BAU, DROP = 60 / 99.0, 60 / 123.05, 3.13
C2, C3, C4 = DROP - 2 * BMP, DROP - 3 * BMP, DROP - 4 * BMP
MP, AU = "mrpopular", "aura"
NUMS = ["I", "II", "III", "IV"]
SHOOT = "/mnt/user-data/uploads/Downloads/исходники/_разбор/hooks_src/"
RED = "/mnt/user-data/uploads/9sky-reels/hooks/red-graphic/"
ROSE = "/mnt/user-data/uploads/flowers hooks/"


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


def freeze(key, hold_src, total=DROP, hold=0.4, speed=1.12, **kw):
    """play to the red sole, then hold that frame (very slow creep) for `hold` s up to the drop"""
    first = total - hold
    return [lb(key, start=hold_src - first * speed, dur=first, speed=speed, **kw),
            lb(key, start=hold_src, speed=0.03, **kw)]


def soles_tail(tail, speed=1.1, **kw):
    """SOLES as the last shot of `tail` s; the logo sole enters ~4.3 s of the source, ~0.4 s before the drop"""
    return lb("SOLES", start=4.3 - (tail - 0.42) * speed, speed=speed, zoom=1.1, **kw)


def t(text, y=0.22, scrim=0.5):
    return [{"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": scrim, "font": "cg-italic"}]


def vpages(items, tone, tag, beats):
    return [img(vpage(P[k], O + f"{tag}{i}.jpg", "N° " + NUMS[i], sub, tone), beats) for i, (k, sub) in enumerate(items)]


def fin_stacked(front, back, tag, no, tone):
    return img(vstacked(P[front], P[back], O + f"{tag}c.jpg", no, tone=tone), 4)


def fin_plate(back, tag, no, tone):
    """single big back with the EX MUSEO inscription"""
    return img(vpage(P[back], O + f"{tag}c.jpg", no, "FIRST LOOK", tone, scale=0.92, title="EX MUSEO"), 4)


KNIT = "BLACK KNIT"
QBK = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
QK1 = [("KF", cat(1, COLLAR))]
QWH = [("WF", cat(1, COLLAR)), ("WB", cat(2, ARA, ROME))]
QKN = [("KF", cat(1, COLLAR)), ("SWF", cat(2, KNIT))]
QBW = [("PF", cat(1, "BLACK  ·  WHITE  ·  ONE RED")), ("PB", cat(2, ARA, ROME))]
ZBW = [("ZPF", cat(1, HOOD)), ("ZPB", cat(2, ARA, ROME))]
ZW = [("XWF", cat(1, HOOD)), ("ZF", cat(2, "BLACK  ·  WHITE"))]

C = [  # key, track, tone, hook, texts, pages, finale(kind, a, b), idea
    ("C01_watch-her-shoes", MP, "vitrine", freeze("COUPLE", 4.95, crop_y=0.74, crop_x=0.45),
     t("watch her shoes."), QBK, ("stack", "KF", "KB"), "freeze on the red sole"),
    ("C02_a-rose-then-this", MP, "oxblood",
     [clip(ROSE + "g2.mp4", start=0.2, dur=C2, speed=1.1, grade={})] + freeze("COUPLE", 4.95, total=DROP - C2, hold=0.35, flip=True, crop_y=0.74),
     t("a rose.\nthen this.", 0.45, 0.45), QBW, ("stack", "PF", "PB"), "rose -> sole, freeze"),
    ("C03_one-detail", MP, "vitrine", [lb("COUPLE", flip=True, crop_y=0.76, crop_x=0.5)],
     t("it only takes\none detail."), QK1, ("stack", "KF", "KB"), "short: 1 page + finale"),
    ("C04_slow-down", AU, "slate", [lb("COUPLE", start=4.7 + 0.45 * 0.75 - DROP * 0.75, speed=0.75, smooth=True, crop_y=0.72)],
     t("slow down.\nlook at the shoes."), QWH, ("stack", "WF", "WB"), "whole hook smoothly slowed"),
    ("C05_same-red", AU, "oxblood", [clip(ROSE + "g3.mp4", start=0.0, grade={})],
     t("same red.", 0.45, 0.45), ZBW, ("stack", "ZPF", "ZPB"), "rose straight into oxblood pages, zip hoodie"),
    ("C06_red-underneath", MP, "slate",
     [lb("STREET", start=1.4, dur=C2, speed=1.1, flip=True, zoom=1.1), lb("COUPLE", speed=1.1, crop_y=0.74)],
     t("black on black.\nred underneath."), QKN, ("stack", "SPF", "SPB"), "street -> couple, knit"),
]
D = [
    ("D01_which-red-first", MP, "vitrine",
     [clip(ROSE + "g3.mp4", dur=C4, speed=1.15, grade={}), lb("NAILS", start=2.0, dur=C2 - C4, speed=1.1),
      lb("COUPLE", speed=1.1, crop_y=0.74)],
     t("which red did\nyou see first?", 0.45, 0.45), QBW, ("plate", "PB"), "3 shots on the beat"),
    ("D02_museum-or-street", MP, "oxblood",
     [clip(RED + "statue_low.mp4", start=0.4, dur=C2, grade={}), soles_tail(DROP - C2)],
     t("museum\nor street?"), QBK, ("plate", "KB"), "red statue -> soles"),
    ("D03_behind-the-curtain", MP, "oxblood",
     [clip(SHOOT + "s12_0.mp4", start=1.6, dur=C2), lb("COUPLE", speed=1.1, crop_y=0.74, flip=True)],
     t("what she wore\nbehind the curtain.", 0.18), QWH, ("plate", "WB"), "red curtain -> sole"),
    ("D04_match-the-rose", AU, "vitrine",
     [clip(ROSE + "g1.mp4", start=0.3, dur=DROP - 3 * BAU, zoom=1.3, crop_y=0.12, grade={})]
     + freeze("COUPLE", 4.95, total=3 * BAU, hold=0.35, speed=1.0, crop_y=0.74),
     t("dressed to match\nthe rose.", 0.62, 0.45), QKN, ("plate", "KB"), "tight rose -> sole freeze"),
    ("D05_nails-soles-collar", MP, "slate",
     [lb("NAILS", start=2.2, dur=C2, speed=1.0, zoom=1.35, crop_y=0.55), lb("COUPLE", speed=1.1, crop_y=0.74)],
     t("her nails. her soles.\nhis collar."), QBK, ("plate", "KB"), "tight nails -> sole"),
    ("D06_everyone-looked", MP, "vitrine",
     [lb("STREET", start=1.0, dur=C3, speed=1.05, zoom=1.1), soles_tail(DROP - C3, flip=True)],
     t("everyone looked\nat her shoes."), ZW, ("plate", "ZB"), "street -> soles, zip hoodie"),
]


def build(batch, rows, out_prefix, seed0, page_beats):
    ledger = []
    for i, (k, track, tone, hook, texts, pg, fin, idea) in enumerate(rows):
        tag = f"{batch[-1]}{i + 1:02d}x"
        pb = page_beats if track == MP else 2
        no = "N° " + NUMS[len(pg)]
        f = fin_stacked(fin[1], fin[2], tag, no, tone) if fin[0] == "stack" else fin_plate(fin[1], tag, no, tone)
        segs = hook + vpages(pg, tone, tag, pb) + [f]
        spec = dict(seed=seed0 + i, track=track, segments=segs, texts=texts)
        json.dump(spec, open(os.path.join(SP, f"{out_prefix}_{k}.json"), "w"), indent=1)
        ledger.append([batch, k, track, tone, texts[0]["text"].replace("\n", " "), idea])
        print(f"{out_prefix}_{k}")
    json.dump(ledger, open(os.path.join(SP, f"ledger_{batch}.json"), "w"), indent=1)


build("1109c", C, "c1109", 26000, 1)
build("1109d", D, "d1109", 27000, 2)
