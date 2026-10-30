#!/usr/bin/env python3
"""2026-10-30: 12 reels.
Rules (Kirill 10-30): Louboutin hooks only with quarter zips (never the red-lined zip hoodie, no "red inside" lines);
zip hoodie only on museum hooks. Red flash kept short (lead ~0.4 s) so the sole logo barely shows.
Museum hooks: only the ones that held >=44% past 3 s (24 colonnade 51%, 19 dome turn 46%, doors open 46%, 02 red wall/opera 45%).
H  - zip hoodie x museum hooks
LW - Louboutin x quarter zip black + white
LS - Louboutin x black quarter zip + new black knit sweater"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import clip, img, pages, fin_path, cat, COLLAR, HOOD, IX, ARA, ROME, SP, P

X = "/mnt/user-data/uploads/EX_MUSEO_hooks/"


def lb(key, flip, crop_x, lead, speed=0.95, zoom=1.035):
    return dict(type="clip", src=P[key], until="drop", align_red=True, speed=speed, zoom=zoom, crop_x=crop_x,
                flip=flip, lead=lead, grade=dict(c=1.04, s=0.92, b=-0.012))


def tx(text, y):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


KNIT = "BLACK KNIT"
ZH = [("ZF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))]
ZHW = [("XWF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))]
ZHB = [("ZB", cat(1, ARA, ROME)), ("ZPF", cat(2, HOOD))]
QW1 = [("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))]
QW2 = [("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR")), ("PF", cat(3, "BLACK  ·  WHITE"))]
QW3 = [("PF", cat(1, COLLAR)), ("KF", cat(2, IX))]
SW1 = [("KF", cat(1, COLLAR)), ("SWF", cat(2, KNIT)), ("SPF", cat(3, "QUARTER ZIP  ·  KNIT"))]
SW2 = [("SPF", cat(1, "QUARTER ZIP  ·  KNIT")), ("SWF", cat(2, KNIT))]
SW3 = [("SWF", cat(1, KNIT)), ("KF", cat(2, COLLAR)), ("SPF", cat(3, "ALL BLACK  ·  ONE RED"))]

# SOLES: the sole with the logo enters at ~4.3 s of the source; start 1.75 keeps it on screen only ~0.45 s before the drop
R = [  # key, hook, text, y, pages, finale
    ("H01_zip-hoodie-museum-date", clip("19_dome-turn", 0.2, flip=True, until="drop"), "best zip hoodie\nfor a museum date.", 0.62, ZH, ("ZPF", "ZPB")),
    ("H02_what-to-wear-museum", clip("24_colonnade", 0.2, until="drop"), "what to wear\nto the museum.", 0.58, ZHW, ("ZPF", "ZPB")),
    ("H03_what-to-wear-opera", clip("02_red-wall-white-doors", 0.2, flip=True, until="drop"), "what to wear\nto the opera.", 0.60, ZHB, ("ZPF", "ZPB")),
    ("H04_last-entry", clip("x", 0.0, src=X + "17_michaelthecanadian_CgoNt-POvh4.mp4", until="drop"), "last entry:\nmidnight.", 0.62, ZH, ("ZPF", "ZPB")),
    ("LW01_collar-says-it-all", lb("COUPLE", True, 0.45, 0.45), "the collar says it all.", 0.40, QW1, ("PF", "PB")),
    ("LW02_black-or-white", lb("COUPLE", False, 0.62, 0.4, speed=0.9), "black or white?", 0.40, QW2, ("PF", "PB")),
    ("LW03_what-to-wear-museum", dict(lb("SOLES", False, 0.55, 0.4), start=1.75, align_red=False), "what to wear\nto the museum.", 0.36, QW3, ("PF", "PB")),
    ("LW04_not-loud", lb("STREET", True, 0.5, 0.45), "not loud.\njust red.", 0.40, QW1, ("PF", "PB")),
    ("LS01_collar-says-it-all", lb("COUPLE", False, 0.5, 0.45, speed=0.92), "the collar says it all.", 0.40, SW1, ("SPF", "SPB")),
    ("LS02_what-to-wear-museum", dict(lb("SOLES", True, 0.45, 0.4), start=1.75, align_red=False), "what to wear\nto the museum.", 0.36, SW2, ("SPF", "SPB")),
    ("LS03_only-wears-black", lb("STREET", False, 0.45, 0.45), "for the one who\nonly wears black.", 0.40, SW3, ("SPF", "SPB")),
    ("LS04_not-loud", dict(lb("NAILS", False, 0.5, 0.4), start=3.6, align_red=False), "not loud.\njust red.", 0.40, SW2, ("SPF", "SPB")),
]
S = {}
for i, (k, hook, text, y, pg, fin) in enumerate(R):
    tag = f"o{i + 1:02d}"
    S[k] = dict(seed=11000 + i, segments=[hook] + pages(pg, None, tag, 2) +
                [img(fin_path(fin[0], fin[1], tag, "N° III" if len(pg) == 2 else "N° IV"), 4)], texts=[tx(text, y)])
for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"o1030_{k}.json"), "w"), indent=1)
print("\n".join(S))
