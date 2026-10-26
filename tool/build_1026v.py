#!/usr/bin/env python3
"""2026-10-26 vibe-text batch (Kirill's phrases): every reel gets a different, mostly never-used hook,
text in our Cormorant italic, pages single -> pair."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import clip, img, pages, fin_path, ht, cat, COLLAR, HOOD, ARA, ROME, IX, SP

QZ = ([("KF", cat(1, COLLAR)), ("PF", cat(2, "THE SAME RED COLLAR"))], ("PF", "PB"))
QZW = ([("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))], ("PF", "PB"))
QZB = ([("KB", cat(1, ARA, ROME)), ("PB", cat(2, ARA, ROME))], ("PF", "PB"))
ZH = ([("ZF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))], ("ZPF", "ZPB"))
ZHW = ([("XWF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))], ("ZPF", "ZPB"))
QIX = ([("KF", cat(1, IX)), ("PF", cat(2, COLLAR))], ("PF", "PB"))

R = [  # key, location hook, start, text, y, pages
    ("V01_whatever-this-is", "25_marble-floor-reveal", 0.2, "i love this vibe,\nwhatever this is.", 0.42, QZ),
    ("V02_best-for-a-museum", "21_gallery-statues-ceilings", 0.2, "best quarter zip\nfor visiting a museum.", 0.40, QZW),
    ("V03_from-the-museum", "22_red-niche-gold-ceiling", 0.1, "the quarter zip\nfrom the museum.", 0.40, QIX),
    ("V04_museum-date", "19_dome-turn", 0.2, "best zip hoodie\nfor a museum date.", 0.62, ZH),
    ("V05_what-to-wear", "24_colonnade", 0.2, "what to wear\nto the museum.", 0.58, QZ),
    ("V06_dressed-like-the-exhibit", "37_marble-relief", 0.2, "dressed like\nthe exhibit.", 0.58, QZB),
    ("V07_dont-know-what-this-is", "27_golden-dome", 0.2, "i don't know what this is\nbut i love it.", 0.60, ZHW),
    ("V08_fit-check", "29_fresco-to-gothic", 0.2, "museum date\nfit check.", 0.58, QZW),
    ("V09_gift-shop", "23_temple-clouds", 0.2, "the gift shop\nshould sell this.", 0.62, QZ),
    ("V10_only-thing-id-steal", "30_red-altar-chandelier", 0.2, "the only thing i'd steal\nfrom a museum.", 0.58, ZH),
]
S = {}
for i, (k, loc, t, txt, y, (pg, fin)) in enumerate(R):
    tag = f"v{i + 1:02d}"
    S[k] = dict(seed=9960 + i, segments=[clip(loc, t, until="drop")] + pages(pg, None, tag, 2) +
                [img(fin_path(fin[0], fin[1], tag, "N° III"), 4)], texts=[ht(txt, y)])
for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"v1026_{k}.json"), "w"), indent=1)
print("\n".join(S))
