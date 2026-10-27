#!/usr/bin/env python3
"""2026-10-27 batch 8: the old Louboutin POV hooks back for variety (Kirill's call), with the current
catalogue (plain black, single -> pair) and the EX MUSEO finale. Red reveal lands ~0.6 s before the drop as before."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, pages, fin_path, cat, COLLAR, HOOD, SP, P

def lb(key, flip, crop_x, lead, speed=0.95, zoom=1.035):
    return dict(type="clip", src=P[key], until="drop", align_red=True, speed=speed, zoom=zoom, crop_x=crop_x,
                flip=flip, lead=lead, grade=dict(c=1.04, s=0.92, b=-0.012))


def tx(text, y):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


R = [  # key, hook, text, y, pages, finale
    ("L01_collar-says-it-all", lb("COUPLE", True, 0.40, 0.6), "the collar says it all.", 0.40,
     [("KF", cat(1, COLLAR)), ("PF", cat(2, "THE SAME RED COLLAR"))], ("PF", "PB")),
    ("L02_what-to-wear-museum", lb("SOLES", False, 0.50, 0.7), "what to wear\nto the museum.", 0.36,
     [("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))], ("PF", "PB")),
    ("L03_his-and-hers", lb("STREET", True, 0.55, 0.7), "his & hers.", 0.40,
     [("ZF", cat(1, HOOD)), ("ZPF", cat(2, "HIS  ·  HERS"))], ("ZPF", "ZPB")),
]
S = {}
for i, (k, hook, text, y, pg, fin) in enumerate(R):
    tag = f"l{i + 1:02d}"
    S[k] = dict(seed=10800 + i, segments=[hook] + pages(pg, None, tag, 2) +
                [img(fin_path(fin[0], fin[1], tag, "N° III"), 4)], texts=[tx(text, y)])
for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"l1027_{k}.json"), "w"), indent=1)
print("\n".join(S))
