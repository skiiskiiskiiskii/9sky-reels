#!/usr/bin/env python3
"""2026-10-27 batch 3: the person comes back into the hook, without Louboutin.
Two ideas from hooks/inbox/vol2 (viral list A), two reels each, texts that won on 10-26:
N - red glass nails on a black glove (A2: one continuous shot, burned-in caption cropped away)
H - holding hands in black sleeves (A7, A9)
The first strong red the viewer sees after the hook is our collar."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import clip, img, pages, fin_path, cat, COLLAR, HOOD, SP

V = "/mnt/user-data/uploads/9sky-reels/hooks/inbox/vol2/"
QZ = ([("KF", cat(1, COLLAR)), ("PF", cat(2, "THE SAME RED COLLAR"))], ("PF", "PB"))
QZW = ([("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))], ("PF", "PB"))
ZH = ([("ZF", cat(1, HOOD)), ("ZPF", cat(2, "HIS  ·  HERS"))], ("ZPF", "ZPB"))
QZH = ([("PF", cat(1, "HIS  ·  HERS")), ("KF", cat(2, COLLAR))], ("PF", "PB"))


def tx(text, y):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


# A2 has a burned-in caption at 18-23 % of the height: a static 1.31x framing from the bottom keeps it out of frame
NAILS = dict(src=V + "A2_black-red-nails.mp4", zoom=1.31, crop_y=1.0)
R = [
    ("N01_nails-what-to-wear", clip("x", 0.2, **NAILS), "what to wear\nto the museum.", 0.70, QZ),
    ("N02_nails-museum-date", clip("x", 2.9, flip=True, **NAILS), "best quarter zip\nfor a museum date.", 0.70, QZW),
    ("H01_hands-zip-hoodie-date", clip("x", 0.0, src=V + "A7_holding-hands-black-sleeves.mp4"),
     "best zip hoodie\nfor a museum date.", 0.24, ZH),
    # A9 has a small handle watermark at the bottom: frame from the top
    ("H02_hands-what-to-wear-date", clip("x", 1.0, src=V + "A9_holding-hands-street.mp4", zoom=1.12, crop_y=0.0),
     "what to wear\non a museum date.", 0.22, QZH),
]
S = {}
for i, (k, hook, text, y, (pg, fin)) in enumerate(R):
    hook["until"] = "drop"
    tag = f"n{i + 1:02d}"
    S[k] = dict(seed=10300 + i, segments=[hook] + pages(pg, None, tag, 2) +
                [img(fin_path(fin[0], fin[1], tag, "N° III"), 4)], texts=[tx(text, y)])
for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"n1027_{k}.json"), "w"), indent=1)
print("\n".join(S))
