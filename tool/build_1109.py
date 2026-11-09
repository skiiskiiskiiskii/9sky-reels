#!/usr/bin/env python3
"""2026-11-09, batch 1109a (8 reels). Kirill: work in batches of 7-8, keep each batch new; 2-3 close to F05
(the 60K one) to see if the formula repeats; don't lean only on Louboutin.
F05 formula: tight crop on the shoes, short line at the TOP promising something about the shoes, F05's exact
timing (cut at 3.13 s, pages every 0.606 s, 2 pages + finale ~6.8 s) so the same fragment of Cyn - North Pole
fits, warm vitrine pages, single product, caption that asks to send it.
G01-G03  F05 family (new lines, small variations, one with the white quarter zip)
G04-G06  hooks from Kirill's own shoot (red booth, the closed jacket, fur coat to the lens) - never posted
G07-G08  red graphic series: the all-red statue and the red fragment, slow push + drifting light
All mockups are the v5 set (new backs)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, IX, ARA, ROME, HOOD, SP, P, O
from vitrine import vpage, vstacked

BATCH = "1109a"
GR = dict(c=1.04, s=0.92, b=-0.012)
DROP = 3.13
MP, AU = "mrpopular", "aura"
NUMS = ["I", "II", "III", "IV"]
SHOOT = "/mnt/user-data/uploads/Downloads/исходники/_разбор/hooks_src/"
RED = "/mnt/user-data/uploads/9sky-reels/hooks/red-graphic/"


def lb(key, start=None, speed=1.12, flip=False, crop_x=0.5, crop_y=0.5, zoom=1.2, lead=0.42, **kw):
    d = dict(type="clip", src=P[key], until="drop", speed=speed, zoom=zoom, crop_x=crop_x, crop_y=crop_y,
             flip=flip, grade=GR)
    d.update(dict(align_red=True, lead=lead) if start is None else dict(start=start, align_red=False))
    d.update(kw)
    return d


def clip(src, start=0.0, speed=1.0, zoom=1.0, crop_y=0.5, grade=GR):
    return dict(type="clip", src=src, start=start, until="drop", align_red=False, speed=speed, zoom=zoom,
                crop_x=0.5, crop_y=crop_y, flip=False, grade=grade)


def t(text, y=0.22, scrim=0.5):
    return [{"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": scrim, "font": "cg-italic"}]


def vpages(items, tone, tag, beats):
    return [img(vpage(P[k], O + f"{tag}{i}.jpg", "N° " + NUMS[i], sub, tone), beats) for i, (k, sub) in enumerate(items)]


def vfin(front, back, tag, no, tone):
    return img(vstacked(P[front], P[back], O + f"{tag}c.jpg", no, tone=tone), 4)


KNIT = "BLACK KNIT"
QBK = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
QWH = [("WF", cat(1, COLLAR)), ("WB", cat(2, ARA, ROME))]
QKN = [("KF", cat(1, COLLAR)), ("SWF", cat(2, KNIT))]
QBW = [("PF", cat(1, "BLACK  ·  WHITE  ·  ONE RED")), ("PB", cat(2, ARA, ROME))]
ZBW = [("ZPF", cat(1, HOOD)), ("ZPB", cat(2, ARA, ROME))]

R = [  # key, track, tone, hook, texts, pages, finale, idea
    ("G01_look-down-first", MP, "vitrine", [lb("COUPLE", crop_y=0.74, crop_x=0.45)],
     t("look down first."), QBK, ("KF", "KB"), "F05 formula: new line"),
    ("G02_always-the-shoes", MP, "vitrine", [lb("SOLES", start=4.3 - 2.8 * 1.12, zoom=1.15, crop_y=0.62)],
     t("it's always\nthe shoes."), QBK, ("KF", "KB"), "F05 formula: SOLES hook"),
    ("G03_follow-the-shoes", MP, "vitrine", [lb("COUPLE", flip=True, crop_y=0.76, crop_x=0.55, lead=0.45)],
     t("follow the shoes."), QWH, ("WF", "WB"), "F05 formula: white quarter zip"),
    ("G04_behind-the-curtain", MP, "oxblood", [clip(SHOOT + "s12_0.mp4", start=0.62)],
     t("what's behind\nthe red curtain?", 0.18), QBK, ("KF", "KB"), "own shoot: red booth"),
    ("G05_under-the-jacket", MP, "vitrine", [clip(SHOOT + "s22_0.mp4", start=0.0, speed=0.95)],
     t("guess what's\nunder the jacket.", 0.80), QBW, ("PF", "PB"), "own shoot: closed jacket"),
    ("G06_come-closer", AU, "vitrine", [clip(SHOOT + "s13_5.5.mp4", start=0.52)],
     t("come closer.", 0.80), QKN, ("SPF", "SPB"), "own shoot: fur coat to the lens"),
    ("G07_one-color", AU, "oxblood", [clip(RED + "statue_red.mp4", grade={})],
     t("the museum kept\nonly one color.", 0.80, 0.0), QBK, ("KF", "KB"), "red graphic: statue"),
    ("G08_found-in-the-archive", MP, "oxblood", [clip(RED + "fragment_red.mp4", grade={})],
     t("found in the archive.\nN° IX.", 0.74, 0.0), ZBW, ("ZPF", "ZPB"), "red graphic: fragment, zip hoodie"),
]
ledger = []
for i, (k, track, tone, hook, texts, pg, fin, idea) in enumerate(R):
    tag = f"g{i + 1:02d}"
    pb = 1 if track == MP else 2
    segs = hook + vpages(pg, tone, tag, pb) + [vfin(fin[0], fin[1], tag, "N° " + NUMS[len(pg)], tone)]
    spec = dict(seed=24000 + i, track=track, segments=segs, texts=texts)
    json.dump(spec, open(os.path.join(SP, f"g1109_{k}.json"), "w"), indent=1)
    ledger.append([BATCH, k, track, tone, texts[0]["text"].replace("\n", " "), idea])
    print(f"g1109_{k}")
json.dump(ledger, open(os.path.join(SP, f"ledger_{BATCH}.json"), "w"), indent=1)
