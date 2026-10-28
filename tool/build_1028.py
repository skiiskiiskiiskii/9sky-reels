#!/usr/bin/env python3
"""2026-10-28: 8 reels. 10-27 results: Louboutin hooks with the current catalogue held 72.5% (collar says it all)
and 69.5% (what to wear to the museum) past 3 s; museum/gothic hooks 21-44%.
LQ01-LQ04: Louboutin POV hooks, quarter zip only (Kirill). M01-M04: museum/opera hooks from EX_MUSEO_hooks, zip + quarter zip."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import clip, img, pages, fin_path, cat, COLLAR, HOOD, ARA, ROME, IX, FLEECE, SP, P

X = "/mnt/user-data/uploads/EX_MUSEO_hooks/"


def lb(key, flip, crop_x, lead, speed=0.95, zoom=1.035):
    return dict(type="clip", src=P[key], until="drop", align_red=True, speed=speed, zoom=zoom, crop_x=crop_x,
                flip=flip, lead=lead, grade=dict(c=1.04, s=0.92, b=-0.012))


def tx(text, y):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


QZ = [("KF", cat(1, COLLAR)), ("PF", cat(2, "THE SAME RED COLLAR"))]
QZW = [("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))]
QIX = [("KF", cat(1, IX)), ("PF", cat(2, COLLAR))]
QBK = [("PF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
ZH = [("ZF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))]
ZHW = [("XWF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))]

# LQ04: NAILS starts at the nail flip so the red sole lands at ~6 s, right before the drop
# M01: the red ballroom is one shot only from 2.5 to 5.4 s, so it runs at 0.92
R = [  # key, hook, text, y, pages, finale
    ("LQ01_collar-says-it-all", lb("COUPLE", False, 0.55, 0.65), "the collar says it all.", 0.40, QZW, ("PF", "PB")),
    ("LQ02_what-to-wear-museum", lb("SOLES", True, 0.45, 0.55), "what to wear\nto the museum.", 0.36, QZ, ("PF", "PB")),
    ("LQ03_black-or-white", lb("STREET", False, 0.45, 0.65), "black or white?", 0.40, QIX, ("PF", "PB")),
    ("LQ04_not-loud", dict(lb("NAILS", True, 0.50, 0.6), start=3.5, align_red=False), "not loud.\njust red.", 0.40, QBK, ("PF", "PB")),
    ("M01_red-ballroom", clip("x", 2.5, src=X + "09_baroqueblockbuster_DFfNGH9I1PK.mp4", speed=0.92, until="drop"),
     "the collar says it all.", 0.62, QZ, ("PF", "PB")),
    ("M02_dressed-for-the-opera", clip("x", 0.0, src=X + "10_roberto_celestri_DUDpdsQDZAd.mp4", until="drop"),
     "dressed\nfor the opera.", 0.62, ZH, ("ZPF", "ZPB")),
    ("M03_opera-night-fit", clip("x", 0.0, src=X + "12_roberto_celestri_DbQ7v2ENPlB.mp4", until="drop"),
     "opera night fit.", 0.24, QZW, ("PF", "PB")),
    ("M04_doors-open", clip("x", 0.0, src=X + "17_michaelthecanadian_CgoNt-POvh4.mp4", until="drop"),
     "doors open\nat nine.", 0.62, ZHW, ("ZPF", "ZPB")),
]
S = {}
for i, (k, hook, text, y, pg, fin) in enumerate(R):
    tag = f"w{i + 1:02d}"
    S[k] = dict(seed=10900 + i, segments=[hook] + pages(pg, None, tag, 2) +
                [img(fin_path(fin[0], fin[1], tag, "N° III"), 4)], texts=[tx(text, y)])
for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"w1028_{k}.json"), "w"), indent=1)
print("\n".join(S))
