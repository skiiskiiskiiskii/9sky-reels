#!/usr/bin/env python3
"""2026-10-24 flashlight series: G2 'someone left a light on.' hit 56.4% past 3 s.
Every hook opens on a close, already-lit statue (frame 0 = subject in the beam), the beam wanders, last shot is a red bust."""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hookgen import flashlight
from build_1024 import img, pages, fin_path, cat, VEIL, BACK, COLLAR, ARA, ROME, HOOD, FLEECE, IX, SP, P

A = "/mnt/user-data/uploads/9sky-reels/aesthetics/"
G = "/mnt/user-data/outputs/hooks-gen/"
g = lambda c, i: sorted(glob.glob(A + c + "/*.jpg"))[i]
dummy = "/mnt/user-data/outputs/stills-1024/gen_kf.jpg"

HOOKS = {
    "F1": [g("statues_dark", 4), g("statues_dark", 6), g("busts_red", 6)],
    "F2": [g("statues_dark", 6), g("statues_athletic", 5), g("busts_red", 0)],
    "F3": [g("statues_dark", 7), g("statues_athletic", 6), g("busts_red", 6)],
    "F4": [g("statues_athletic", 3), g("statues_athletic", 6), g("busts_red", 6)],
    "F5": [g("statues_dark", 0), g("statues_dark", 4), g("busts_red", 0)],
    "F6": [g("statues_athletic", 5), g("statues_dark", 4), g("busts_red", 0)],
}


def hook(name):
    return dict(type="clip", src=G + name + ".mp4", start=0, align_red=False, speed=1.0, zoom=1.0,
                flip=False, crop_x=0.5, grade=dict(c=1.0, s=1.0, b=0.0), until="drop")


def ht(text):
    return {"text": text, "from": 0, "to": "drop", "y": 0.80, "size": 96, "scrim": 0.5, "font": "cg-italic"}


if "--hooks" in sys.argv:
    for i, (k, st) in enumerate(HOOKS.items()):
        if len(sys.argv) > 2 and k not in sys.argv[2:]: continue
        flashlight(st, dummy, G + f"{k}_flash.mp4", land=3.5, seed=20 + i)

S = {}
# black + white pairs everywhere: PF/PB = quarter zip pair, ZPF/ZPB = zip hoodie pair
S["F1_light-on"] = dict(seed=9301, track="mrpopular", segments=[hook("F1_flash")] +
    pages([("PF", cat(1, COLLAR)), ("PB", cat(2, ARA, ROME)), ("ZPF", cat(3, HOOD)), ("ZPB", cat(4, FLEECE))], None, "f1", 1) +
    [img(fin_path("ZPF", "ZPB", "f1", "N° V"), 4)], texts=[ht("someone left a light on.")])
S["F2_guard-went-home"] = dict(seed=9302, segments=[hook("F2_flash")] +
    pages([("PF", cat(1, "HIS / HERS")), ("ZPF", cat(2, HOOD))], None, "f2", 2) +
    [img(fin_path("PF", "PB", "f2", "N° III"), 4)], texts=[ht("the guard went home.")])
S["F3_not-supposed-to-see"] = dict(seed=9303, track="mrpopular", segments=[hook("F3_flash")] +
    pages([("ZPF", cat(1, HOOD)), ("ZPB", cat(2, ARA, ROME)), ("PF", cat(3, COLLAR)), ("PB", cat(4, FLEECE))], None, "f3", 1) +
    [img(fin_path("PF", "PB", "f3", "N° V"), 4)], texts=[ht("you weren't supposed to see this.")])
S["F4_after-closing"] = dict(seed=9304, segments=[hook("F4_flash")] +
    pages([("PF", cat(1, "THE SAME RED COLLAR")), ("PB", cat(2, ARA, ROME))], None, "f4", 2) +
    [img(fin_path("ZPF", "ZPB", "f4", "N° III"), 4)], texts=[ht("after closing.")])
S["F5_last-one-out"] = dict(seed=9305, track="mrpopular", segments=[hook("F5_flash")] +
    pages([("PF", cat(1, COLLAR)), ("ZPF", cat(2, HOOD)), ("PB", cat(3, ARA, ROME)), ("ZPB", cat(4, FLEECE))], None, "f5", 1) +
    [img(fin_path("PF", "PB", "f5", "N° V"), 4)], texts=[ht("last one out.")])
S["F6_no-flash"] = dict(seed=9306, segments=[hook("F6_flash")] +
    pages([("ZPF", cat(1, "HIS / HERS")), ("ZPB", cat(2, ARA, ROME))], None, "f6", 2) +
    [img(fin_path("PF", "PB", "f6", "N° III"), 4)], texts=[ht("no flash photography.")])

for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"f1024_{k}.json"), "w"), indent=1)
print("\n".join(S))
