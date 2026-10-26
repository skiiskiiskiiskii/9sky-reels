#!/usr/bin/env python3
"""2026-10-26 hook test: 10 reels, 10 different, never-used scenes from all 7 source videos.
Everything else is fixed (same hook text, same pages, same finale, AURA grid), so the hook picture is the only variable."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import clip, img, pages, fin_path, ht, cat, COLLAR, SP

H = "/mnt/user-data/uploads/hooks ids/snaptik_"
V = {k: H + v + "_hd.mp4" for k, v in {1: "7232604837769334042", 2: "7382217770819177761", 3: "7564486079613570360",
                                       5: "7615821256385924366", 6: "7629052842933849364", 7: "7656541418327903501"}.items()}
TEXT = "the collar says it all."
HOOKS = [  # key, source, start, speed
    ("T01_dark-museum-walk", 1, 1.0, 0.78),
    ("T02_carved-ceiling", 2, 0.0, 0.80),
    ("T03_clock-cabinet-room", 2, 9.80, 0.72),
    ("T04_gold-ceiling-gallery", 2, 12.5, 1.0),
    ("T05_gothic-statues-dark", 3, 0.3, 1.0),
    ("T06_fresco-chandelier", 6, 0.1, 1.0),
    ("T07_dark-portraits", 7, 5.6, 1.0),
    ("T08_coat-of-arms", 7, 18.2, 1.0),
    ("T09_globe-and-shield", 5, 34.98, 1.0),
    ("T10_green-panel-room", 5, 27.35, 0.70),
]
S = {}
for i, (k, s, t, sp) in enumerate(HOOKS):
    tag = f"t{i + 1:02d}"
    S[k] = dict(seed=9800 + i, segments=[clip("x", t, src=V[s], speed=sp, until="drop")] +
                pages([("KF", cat(1, COLLAR)), ("PF", cat(2, "THE SAME RED COLLAR"))], None, tag, 2) +
                [img(fin_path("PF", "PB", tag, "N° III"), 4)], texts=[ht(TEXT, 0.60)])
for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"t1026_{k}.json"), "w"), indent=1)
print("\n".join(S))
