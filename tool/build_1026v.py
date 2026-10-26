#!/usr/bin/env python3
"""2026-10-26 vibe-text test (Kirill's idea after a viral 'i love art and ...' reel): one fixed hook,
small plain lowercase text like a personal post, only the phrase changes. Same pages as the hook test."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import clip, img, pages, fin_path, cat, COLLAR, SP
from build_1026t import V

def vt(text):
    return {"text": text, "from": 0, "to": "drop", "y": 0.50, "size": 50, "scrim": 0.25, "font": "inter"}

TEXTS = [("V1_whatever-this-is", "i love this vibe whatever this is"),
         ("V2_best-for-a-museum", "best quarter zip for visiting a museum"),
         ("V3_from-the-museum", "the quarter zip from the museum"),
         ("V4_museum-date", "best zip hoodie for a museum date"),
         ("V5_what-to-wear", "what to wear to the museum"),
         ("V6_dressed-like-the-exhibit", "dressed like the exhibit")]
S = {}
for i, (k, txt) in enumerate(TEXTS):
    tag = f"v{i + 1}"
    zip_ = "zip hoodie" in txt
    p = [("ZF", cat(1, "RED-LINED HOOD")), ("ZPF", cat(2, "RED-LINED HOOD"))] if zip_ else \
        [("KF", cat(1, COLLAR)), ("PF", cat(2, "THE SAME RED COLLAR"))]
    fin = ("ZPF", "ZPB") if zip_ else ("PF", "PB")
    S[k] = dict(seed=9950 + i, segments=[clip("x", 3.8, src=V[6], until="drop")] + pages(p, None, tag, 2) +
                [img(fin_path(fin[0], fin[1], tag, "N° III"), 4)], texts=[vt(txt)])
for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"v1026_{k}.json"), "w"), indent=1)
print("\n".join(S))
