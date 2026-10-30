#!/usr/bin/env python3
"""2026-10-31: 6 reels on Kirill's ready rose POV hooks (~/Downloads/flowers hooks, already 9:16 and graded).
g1 - night, pale hand, rose on grass; g2 - top-down on asphalt; g3 - walk on paving tiles (2.87 s, eased to reach the drop).
Hooks are used as delivered: no zoom, no flip, no extra grade.
Rose = date, so date lines fit. No Louboutin link, so both garments are allowed (Kirill 10-30):
quarter zip x3, zip hoodie x2, black quarter zip + knit x1."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, pages, fin_path, cat, COLLAR, HOOD, ARA, ROME, SP

G = "/mnt/user-data/uploads/flowers hooks/"


def rose(name):
    return dict(type="clip", src=G + name + ".mp4", start=0.0, until="drop", align_red=False, speed=1.0,
                zoom=1.0, crop_x=0.5, flip=False, grade={})


def tx(text, y):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.4, "font": "cg-italic"}


KNIT = "BLACK KNIT"
QW1 = [("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))]
QW2 = [("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR")), ("PF", cat(3, "BLACK  ·  WHITE"))]
ZH = [("ZF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))]
ZHB = [("XWF", cat(1, HOOD)), ("ZB", cat(2, ARA, ROME)), ("ZPF", cat(3, "BLACK  ·  WHITE"))]
SW = [("KF", cat(1, COLLAR)), ("SWF", cat(2, KNIT)), ("SPF", cat(3, "ALL BLACK  ·  ONE RED"))]

R = [  # key, hook, text, y, pages, finale
    ("F01_date-night", rose("g1"), "date night.\none red collar.", 0.80, QW1, ("PF", "PB")),
    ("F02_only-wears-black", rose("g1"), "for the one who\nonly wears black.", 0.80, SW, ("SPF", "SPB")),
    ("F03_not-loud", rose("g2"), "not loud.\njust red.", 0.78, QW2, ("PF", "PB")),
    ("F04_first-date", rose("g2"), "what to wear\non a first date.", 0.78, ZH, ("ZPF", "ZPB")),
    ("F05_one-red-thing", rose("g3"), "one red thing\nis enough.", 0.76, QW1, ("PF", "PB")),
    ("F06_museum-date", rose("g3"), "what to wear\non a museum date.", 0.76, ZHB, ("ZPF", "ZPB")),
]
S = {}
for i, (k, hook, text, y, pg, fin) in enumerate(R):
    tag = f"f{i + 1:02d}"
    S[k] = dict(seed=13000 + i, segments=[hook] + pages(pg, None, tag, 2) +
                [img(fin_path(fin[0], fin[1], tag, "N° III" if len(pg) == 2 else "N° IV"), 4)], texts=[tx(text, y)])
for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"f1031_{k}.json"), "w"), indent=1)
print("\n".join(S))
