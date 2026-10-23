#!/usr/bin/env python3
"""Trial: pages without the big word (grey CAT. line only), finale 'museum collection / FIRST LOOK', new hook texts."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from editorial import page, stacked, dark_bg

SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "specs")
P = json.load(open(os.path.join(SP, "_paths.json")))["paths"]
A = "/mnt/user-data/uploads/9sky-reels/aesthetics/"
L = "/mnt/user-data/outputs/hooks-locations/"
O = "/mnt/user-data/outputs/stills-trial-1023/"
os.makedirs(O, exist_ok=True)
COLL, FL = "museum collection", "FIRST LOOK"
VEIL = dark_bg(A + "statues_dark/9skyaes_statues_dark_28.jpg", "statue", 0.30)
BACK = dark_bg(A + "statues_dark/9skyaes_statues_dark_13.jpg", "statue", 0.30)
ORN = dark_bg(A + "ornament/9skyaes_ornament_11.jpg", "ornament", 0.10, centre=0.15)
B99, DROP = 60 / 99.0, 3.13
YR = "PRAGUE, MMXXVI"
cat = lambda n, what, place=YR: f"CAT. {n:02d}  ·  {what}  ·  {place}"


def clip(name, start, **kw):
    d = dict(type="clip", src=L + name + ".mp4", start=start, align_red=False, speed=1.0, zoom=1.0,
             flip=False, crop_x=0.5, grade=dict(c=1.04, s=1.0, b=-0.03))
    d.update(kw)
    return d


def montage(shots):
    n = len(shots)
    first = DROP - (n - 1) * B99
    return [clip(nm, st, until="drop") if i == n - 1 else clip(nm, st, dur=first if i == 0 else B99)
            for i, (nm, st) in enumerate(shots)]


def img(p, b):
    return dict(type="image", src=p, fit="full", beats=b)


def ht(text, y=0.47):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


def pages(items, bg, tag, beats):
    nums = ["I", "II", "III", "IV"]
    return [img(page(P[k], O + f"{tag}{i}.jpg", "N° " + nums[i], "", line, bg=bg), beats) for i, (k, line) in enumerate(items)]


S = {}
S["T1_drive_guard"] = dict(seed=7001, track="mrpopular", segments=
    montage([("02_red-wall-white-doors", 0.3), ("07_red-mirror-clock", 0.6), ("01_red-room-chandelier", 1.0), ("05_chandelier-pass", 2.2)]) +
    pages([("KF", cat(1, "COTTON FLEECE")), ("WF", cat(2, "RED RIBBED COLLAR")),
           ("KB", cat(3, "AFTER THE ARA PACIS", "ROME, 9 BC")), ("WB", cat(4, "EMBOSSED ORNAMENT"))], None, "t1", 1) +
    [img(stacked(P["PF"], P["PB"], O + "t1c.jpg", "N° V", COLL, FL), 4)],
    texts=[ht("the guard asked\nabout the collar.")])
S["T2_drive_paintings"] = dict(seed=7002, track="mrpopular", segments=
    montage([("11_museum-flash-cuts", 2.3), ("07_red-mirror-clock", 0.2), ("02_red-wall-white-doors", 1.4), ("01_red-room-chandelier", 2.4)]) +
    pages([("KF", cat(1, "COTTON FLEECE")), ("ZF", cat(2, "RED-LINED HOOD")),
           ("WF", cat(3, "RED RIBBED COLLAR")), ("XWF", cat(4, "EMBOSSED IX"))], VEIL, "t2", 1) +
    [img(stacked(P["PF"], P["PB"], O + "t2c.jpg", "N° V", COLL, FL, bg=VEIL), 4)],
    texts=[ht("nobody looked\nat the paintings.")])
S["T3_calm_no-flash"] = dict(seed=7003, segments=[clip("15_dark-baroque-gold", 0.3, until="drop")] +
    pages([("KF", cat(1, "COTTON FLEECE")), ("KB", cat(2, "AFTER THE ARA PACIS", "ROME, 9 BC"))], BACK, "t3", 2) +
    [img(stacked(P["PF"], P["PB"], O + "t3c.jpg", "N° III", COLL, FL, bg=BACK), 4)],
    texts=[ht("no flash photography.", 0.45)])
S["T4_calm_acquired"] = dict(seed=7004, segments=[clip("12_candles-montage", 0.0, until="drop")] +
    pages([("ZF", cat(1, "RED-LINED HOOD")), ("XWF", cat(2, "COTTON FLEECE"))], ORN, "t4", 2) +
    [img(stacked(P["ZPF"], P["ZPB"], O + "t4c.jpg", "N° III", COLL, FL, bg=ORN), 4)],
    texts=[ht("acquired after dark.", 0.47)])

for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"trial1023_{k}.json"), "w"), indent=1)
print("\n".join(S))
