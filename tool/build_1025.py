#!/usr/bin/env python3
"""2026-10-25: back to moving red-room location hooks (best likes + 40-45% past 3 s),
proven hook texts, pages alternate single mockup -> black+white pair, stacked pair finale."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import clip, img, pages, fin_path, ht, cat, VEIL, BACK, COLLAR, ARA, ROME, HOOD, FLEECE, IX, SP

S = {}
S["R1_collar-says-it-all"] = dict(seed=9501, segments=[clip("07_red-mirror-clock", 0.3, until="drop", flip=True)] +
    pages([("KF", cat(1, COLLAR)), ("PF", cat(2, "THE SAME RED COLLAR"))], None, "r1", 2) +
    [img(fin_path("PF", "PB", "r1", "N° III"), 4)], texts=[ht("the collar says it all.", 0.60)])
S["R2_his-and-hers"] = dict(seed=9502, segments=[clip("03_red-velvet-salon", 0.6, until="drop")] +
    pages([("KF", cat(1, "HIS")), ("WF", cat(2, "HERS"))], None, "r2", 2) +
    [img(fin_path("PF", "PB", "r2", "N° III"), 4)], texts=[ht("his & hers.", 0.60)])
S["R3_not-loud"] = dict(seed=9503, segments=[clip("06_red-gown", 0.2, until="drop")] +
    pages([("ZF", cat(1, HOOD)), ("ZPF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))], None, "r3", 2) +
    [img(fin_path("ZPF", "ZPB", "r3", "N° III"), 4)], texts=[ht("not loud. just red.", 0.40)])
S["R4_black-or-white"] = dict(seed=9504, segments=[clip("01_red-room-chandelier", 0.6, until="drop", flip=True)] +
    pages([("WF", cat(1, COLLAR)), ("KF", cat(2, COLLAR))], None, "r4", 2) +
    [img(fin_path("PF", "PB", "r4", "N° III"), 4)], texts=[ht("black or white?", 0.60)])
S["R5_do-not-touch"] = dict(seed=9505, segments=[clip("05_chandelier-pass", 0.4, until="drop")] +
    pages([("KB", cat(1, ARA, ROME)), ("PB", cat(2, ARA, ROME))], None, "r5", 2) +
    [img(fin_path("PF", "PB", "r5", "N° III"), 4)], texts=[ht("do not touch the exhibits.", 0.60)])
S["R6_white-outside"] = dict(seed=9506, segments=[clip("08_white-dress-red-room", 0.3, until="drop")] +
    pages([("XWF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))], None, "r6", 2) +
    [img(fin_path("ZPF", "ZPB", "r6", "N° III"), 4)], texts=[ht("white outside.\nred inside.", 0.62)])

for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"r1025_{k}.json"), "w"), indent=1)
print("\n".join(S))
