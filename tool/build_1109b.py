#!/usr/bin/env python3
"""2026-11-09, batch 1109b - rebuild of 1109a after Kirill's notes:
- keep the link to Louboutin / roses; the red statue is fine as an idea but has to be tied to them;
  from the own-shoot hooks only the red curtain stays.
- mockup cut-out fixed (editorial._cut): deep shadows at the hood seam and in the embossing are no longer
  treated as background, so the glow no longer shows through them.
G01-G03  F05 formula (tight crop on the shoes, line at the top, F05 timing for Cyn - North Pole)
G04      red curtain (own shoot), kept
H05      rose -> red sole, line "it starts with a rose." (F05 sibling with a rose)
H06      red statue -> red sole: "from the museum to the street." (EX MUSEO idea + Louboutin)
H07      rose -> red statue: "some reds belong in a museum." (calm)
H08      hand with nails -> red sole with a slow-down, knit + quarter zip, slate pages
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, IX, ARA, ROME, HOOD, SP, P, O
from vitrine import vpage, vstacked

BATCH = "1109b"
GR = dict(c=1.04, s=0.92, b=-0.012)
BMP, BAU, DROP = 60 / 99.0, 60 / 123.05, 3.13
C2 = DROP - 2 * BMP
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


def clip(src, start=0.0, dur=None, speed=1.0, zoom=1.0, crop_y=0.5, flip=False, grade=GR):
    d = dict(type="clip", src=src, start=start, align_red=False, speed=speed, zoom=zoom,
             crop_x=0.5, crop_y=crop_y, flip=flip, grade=grade)
    d.update(dict(dur=dur) if dur else dict(until="drop"))
    return d


def ramp(key, onset, total, slow=0.55, rate=0.5, pre=1.0, **kw):
    """normal speed, then a smooth slow-down for the last `slow` s; the red lands in the slow part"""
    s_end = onset + 0.13
    s_slow = s_end - slow * rate
    first = total - slow
    return [lb(key, start=s_slow - first * pre, dur=first, speed=pre, **kw),
            lb(key, start=s_slow, speed=rate, smooth=True, **kw)]


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
    ("H05_starts-with-a-rose", MP, "vitrine",
     [clip(ROSE + "g3.mp4", dur=C2, speed=1.1, grade={}), lb("COUPLE", crop_y=0.74, crop_x=0.5)],
     t("it starts\nwith a rose.", 0.42, 0.45), QBW, ("PF", "PB"), "F05 sibling: rose -> red sole"),
    ("H06_museum-to-street", MP, "oxblood",
     [clip(RED + "statue_low.mp4", start=0.4, dur=C2, grade={}), lb("COUPLE", crop_y=0.74, crop_x=0.55, flip=True)],
     t("from the museum\nto the street."), QBK, ("KF", "KB"), "red statue -> red sole"),
    ("H07_reds-in-a-museum", AU, "oxblood",
     [clip(ROSE + "g2.mp4", start=0.2, dur=DROP - 3 * BAU, grade={}), clip(RED + "statue_low.mp4", start=0.6, grade={})],
     t("some reds belong\nin a museum.", 0.80, 0.45), ZBW, ("ZPF", "ZPB"), "rose -> red statue, zip hoodie"),
    ("H08_red-goes-underneath", MP, "slate",
     [lb("NAILS", start=2.0, dur=C2 - 0.0, speed=1.1, zoom=1.1)] + ramp("COUPLE", 4.7, total=DROP - C2, slow=0.6, crop_y=0.72),
     t("red goes\nunderneath."), QKN, ("SPF", "SPB"), "nails -> sole slow-down, knit"),
]
ledger = []
for i, (k, track, tone, hook, texts, pg, fin, idea) in enumerate(R):
    tag = f"h{i + 1:02d}"
    pb = 1 if track == MP else 2
    segs = hook + vpages(pg, tone, tag, pb) + [vfin(fin[0], fin[1], tag, "N° " + NUMS[len(pg)], tone)]
    spec = dict(seed=25000 + i, track=track, segments=segs, texts=texts)
    json.dump(spec, open(os.path.join(SP, f"h1109_{k}.json"), "w"), indent=1)
    ledger.append([BATCH, k, track, tone, texts[0]["text"].replace("\n", " "), idea])
    print(f"h1109_{k}")
json.dump(ledger, open(os.path.join(SP, f"ledger_{BATCH}.json"), "w"), indent=1)
