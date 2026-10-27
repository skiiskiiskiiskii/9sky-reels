#!/usr/bin/env python3
"""2026-10-27 batch 5: the "second look" aesthetic (10-23 reel: 4.9k views, 7.6 s average watch).
Cold dark gothic hook -> front on a dark statue backdrop -> back with the Ara Pacis ornament -> EX MUSEO on the backdrop."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
H = "/mnt/user-data/uploads/hooks ids/snaptik_"
S2, S3 = H + "7382217770819177761_hd.mp4", H + "7564486079613570360_hd.mp4"
from build_1024 import clip, img, pages, fin_path, cat, FLEECE, HOOD, ARA, ROME, COLLAR, VEIL, BACK, SP


def tx(text, y):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


# G03: source watermark at the bottom is framed out (zoom 1.07 from the top)
R = [  # key, hook, text, y, pages (front -> back), finale, backdrop
    ("G01_second-look", clip("x", 6.6, src=S2, flip=True, until="drop"), "the second look\nis the point.", 0.56,
     [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))], ("PF", "PB"), VEIL),
    ("G02_now-turn-around", clip("32_dark-sculpture-walls", 0.3, until="drop"), "now turn\naround.", 0.56,
     [("WF", cat(1, FLEECE)), ("WB", cat(2, ARA, ROME))], ("PF", "PB"), BACK),
    ("G03_the-back-is-the-point", clip("x", 0.3, src=S3, zoom=1.07, crop_y=0.0, until="drop"), "the back\nis the point.", 0.56,
     [("ZF", cat(1, HOOD)), ("ZB", cat(2, ARA, ROME))], ("ZPF", "ZPB"), VEIL),
]
S = {}
for i, (k, hook, text, y, pg, fin, bg) in enumerate(R):
    tag = f"g{i + 1:02d}"
    S[k] = dict(seed=10500 + i, segments=[hook] + pages(pg, bg, tag, 2) +
                [img(fin_path(fin[0], fin[1], tag, "N° III", bg), 4)], texts=[tx(text, y)])
for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"g1027_{k}.json"), "w"), indent=1)
print("\n".join(S))
