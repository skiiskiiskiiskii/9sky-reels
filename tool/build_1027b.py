#!/usr/bin/env python3
"""2026-10-27 batch 2 (8 reels): the "what to wear to ..." line that won on 10-26
(V05 what to wear to the museum 51.7% past 3 s, V04 best zip hoodie for a museum date 46.3%),
now with 8 different, rarely used hooks and new occasions. Finale EX MUSEO."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import clip, img, pages, fin_path, cat, COLLAR, HOOD, ARA, ROME, IX, SP

S7 = "/mnt/user-data/uploads/hooks ids/snaptik_7656541418327903501_hd.mp4"
QZ = ([("KF", cat(1, COLLAR)), ("PF", cat(2, "THE SAME RED COLLAR"))], ("PF", "PB"))
QZW = ([("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))], ("PF", "PB"))
QIX = ([("KF", cat(1, IX)), ("PF", cat(2, COLLAR))], ("PF", "PB"))
ZH = ([("ZF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))], ("ZPF", "ZPB"))
ZHW = ([("XWF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))], ("ZPF", "ZPB"))
ZHB = ([("ZB", cat(1, ARA, ROME)), ("ZPF", cat(2, HOOD))], ("ZPF", "ZPB"))


def tx(text, y):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


R = [  # key, hook segment, text, y, pages
    ("E01_what-to-wear-museum", clip("x", 10.0, src=S7, until="drop"), "what to wear\nto the museum.", 0.60, QZ),
    ("E02_zip-hoodie-museum-date", clip("36_fresco-ceiling-gold", 0.2, until="drop"), "best zip hoodie\nfor a museum date.", 0.62, ZH),
    ("E03_what-to-wear-opera", clip("02_red-wall-white-doors", 0.2, until="drop"), "what to wear\nto the opera.", 0.60, QZW),
    ("E04_quarter-zip-museum-date", clip("09_orange-gallery", 0.2, until="drop"), "best quarter zip\nfor a museum date.", 0.62, QZ),
    ("E05_museum-this-winter", clip("26_church-nave", 0.2, until="drop"), "what to wear\nto the museum this winter.", 0.60, ZHW),
    ("E06_would-you-wear-this", clip("13_palace-ceiling-walk", 0.2, until="drop"), "would you wear this\nto the museum?", 0.62, QZ),
    ("E07_gallery-opening", clip("33_medallion-wall", 0.2, until="drop"), "what to wear\nto a gallery opening.", 0.60, QIX),
    ("E08_palace-tour", clip("10_gold-chandelier", 0.2, until="drop"), "what to wear\non a palace tour.", 0.62, ZHB),
]
S = {}
for i, (k, hook, text, y, (pg, fin)) in enumerate(R):
    tag = f"e{i + 1:02d}"
    S[k] = dict(seed=10200 + i, segments=[hook] + pages(pg, None, tag, 2) +
                [img(fin_path(fin[0], fin[1], tag, "N° III"), 4)], texts=[tx(text, y)])
for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"e1027_{k}.json"), "w"), indent=1)
print("\n".join(S))
