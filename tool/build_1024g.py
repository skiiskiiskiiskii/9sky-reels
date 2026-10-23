#!/usr/bin/env python3
"""2026-10-24 own hooks: synthetic hooks from hookgen.py (flashlight, accelerate, emerge, redwave)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_1024 as b
from build_1024 import img, pages, fin_path, cat, VEIL, BACK, COLLAR, ARA, ROME, HOOD, FLEECE, IX, SP

G = "/mnt/user-data/outputs/hooks-gen/"


def hook(name):
    return dict(type="clip", src=G + name + ".mp4", start=0, align_red=False, speed=1.0, zoom=1.0,
                flip=False, crop_x=0.5, grade=dict(c=1.0, s=1.0, b=0.0), until="drop")


def ht(text, y=0.47, to="drop"):
    return {"text": text, "from": 0, "to": to, "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


S = {}
S["G1_flashlight-white"] = dict(seed=9201, track="mrpopular", segments=[hook("G1_flashlight-white")] +
    pages([("WF", cat(1, COLLAR)), ("WB", cat(2, ARA, ROME)), ("XWF", cat(3, HOOD)), ("XWB", cat(4, FLEECE))], None, "g1", 1) +
    [img(fin_path("PF", "PB", "g1", "N° V"), 4)], texts=[ht("the museum is closed.", 0.80, 2.35)])
S["G2_flashlight-black"] = dict(seed=9202, segments=[hook("G2_flashlight-black")] +
    pages([("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))], None, "g2", 2) +
    [img(fin_path("KKF", "KKB", "g2", "N° III"), 4)], texts=[ht("someone left a light on.", 0.80, 2.35)])
S["G3_accelerate"] = dict(seed=9203, track="mrpopular", segments=[hook("G3_accelerate")] +
    pages([("KF", cat(1, FLEECE)), ("WF", cat(2, COLLAR)), ("ZF", cat(3, HOOD)), ("KB", cat(4, ARA, ROME))], BACK, "g3", 1) +
    [img(fin_path("ZPF", "ZPB", "g3", "N° V", BACK), 4)], texts=[ht("keep up.")])
S["G4_emerge"] = dict(seed=9204, segments=[hook("G4_emerge")] +
    pages([("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR"))], VEIL, "g4", 2) +
    [img(fin_path("PF", "PB", "g4", "N° III", VEIL), 4)], texts=[ht("turn your brightness up.", 0.30)])
S["G5_redwave"] = dict(seed=9205, segments=[hook("G5_redwave")] +
    pages([("KF", cat(1, COLLAR)), ("ZF", cat(2, HOOD))], None, "g5", 2) +
    [img(fin_path("KKF", "KKB", "g5", "N° III"), 4)], texts=[ht("only one colour stayed.", 0.47)])

for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"g1024_{k}.json"), "w"), indent=1)
print("\n".join(S))
