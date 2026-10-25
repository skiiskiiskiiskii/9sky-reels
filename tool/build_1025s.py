#!/usr/bin/env python3
"""2026-10-25 sharp batch: hard cuts on the 99 BPM grid, punch-in + flash on every cut, bold upright caps that build on the beat."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, pages, fin_path, cat, COLLAR, ARA, ROME, HOOD, FLEECE, IX, SP
import sharp

S4 = "/mnt/user-data/uploads/hooks ids/snaptik_7566333336642129175_hd.mp4"
S5 = "/mnt/user-data/uploads/hooks ids/snaptik_7615821256385924366_hd.mp4"
S6 = "/mnt/user-data/uploads/hooks ids/snaptik_7629052842933849364_hd.mp4"
G = "/mnt/user-data/outputs/hooks-gen/"
B = 60 / 99.0
h, q = B / 2, B / 4
sh = lambda src, t, d=None, **k: dict(src=src, t=t, d=d, **k)

HOOKS = {
    "X1": dict(shots=[sh(S5, 15.1, 0.40), sh(S6, 10.0, h), sh(S5, 23.6, h), sh(S6, 5.5, h), sh(S5, 38.4, h),
                      sh(S6, 12.6, h), sh(S5, 29.8, h), sh(S6, 24.6, h), sh(S5, 16.0, h), sh(S6, 14.2)]),
    "X2": dict(shots=[sh(S4, 3.95, 0.45), sh(S4, 4.8, 0.45), sh(S4, 6.4, h), sh(S4, 14.9, h), sh(S4, 5.3, h),
                      sh(S4, 15.35, q), sh(S4, 6.8, q), sh(S4, 4.0, q), sh(S5, 15.1, None, drift=0.04)],
               punch=0.12, flash=0.30),
    "X3": dict(shots=[sh(S5, 9.2, B), sh(S6, 6.4, B), sh(S5, 42.0, h), sh(S5, 51.5, h), sh(S6, 33.6, h),
                      sh(S5, 6.0, q), sh(S6, 26.0, q), sh(S5, 19.5, q), sh(S6, 1.0, q), sh(S6, 11.0)]),
    "X4": dict(shots=[sh(S6, 3.8, None, speed=1.5, drift=0.05)], pulses=[B * k for k in range(1, 6)], punch=0.0, flash=0.0),
}


def tx(text, frm, to="drop", y=0.50, size=104):
    return {"text": text, "from": frm, "to": to, "y": y, "size": size, "scrim": 0.45, "font": "cg-600"}


def hook(name):
    return dict(type="clip", src=G + name + ".mp4", start=0, align_red=False, speed=1.0, zoom=1.0,
                flip=False, crop_x=0.5, grade=dict(c=1.0, s=1.0, b=0.0), until="drop")


if "--hooks" in sys.argv:
    only = [a for a in sys.argv[1:] if a in HOOKS]
    for k, v in HOOKS.items():
        if only and k not in only:
            continue
        v = dict(v); shots = v.pop("shots")
        sharp.build(shots, G + f"{k}_sharp.mp4", **v)
        print("hook", k)

S = {}
S["X1_rapid-red"] = dict(seed=9601, track="mrpopular", segments=[hook("X1_sharp")] +
    pages([("KF", cat(1, COLLAR)), ("PF", cat(2, "THE SAME RED COLLAR")), ("WF", cat(3, COLLAR)), ("PB", cat(4, ARA, ROME))], None, "x1", 1) +
    [img(fin_path("PF", "PB", "x1", "N° V"), 4)],
    texts=[tx("THE COLLAR", 0, 2 * B), tx("THE COLLAR\nSAYS IT ALL.", 2 * B)])
S["X2_dark-to-red-slam"] = dict(seed=9602, track="mrpopular", segments=[hook("X2_sharp")] +
    pages([("KF", cat(1, COLLAR)), ("ZPF", cat(2, HOOD)), ("ZF", cat(3, HOOD)), ("PF", cat(4, COLLAR))], None, "x2", 1) +
    [img(fin_path("PF", "PB", "x2", "N° V"), 4)],
    texts=[tx("NOT LOUD.", 0, 2.25), tx("JUST RED.", 2.25)])
S["X3_strobe"] = dict(seed=9603, track="mrpopular", segments=[hook("X3_sharp")] +
    pages([("WF", cat(1, COLLAR)), ("KF", cat(2, COLLAR)), ("PF", cat(3, "BLACK  ·  WHITE  ·  ONE RED")), ("ZPF", cat(4, HOOD))], None, "x3", 1) +
    [img(fin_path("PF", "PB", "x3", "N° V"), 4)],
    texts=[tx("BLACK", 0, 2 * B), tx("BLACK\nOR WHITE?", 2 * B)])
S["X4_push"] = dict(seed=9604, track="mrpopular", segments=[hook("X4_sharp")] +
    pages([("KB", cat(1, ARA, ROME)), ("PB", cat(2, ARA, ROME)), ("ZB", cat(3, FLEECE)), ("ZPB", cat(4, ARA, ROME))], None, "x4", 1) +
    [img(fin_path("ZPF", "ZPB", "x4", "N° V"), 4)],
    texts=[tx("DO NOT", 0, B), tx("DO NOT TOUCH", B, 2 * B), tx("DO NOT TOUCH\nTHE EXHIBITS.", 2 * B)])

for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"x1025_{k}.json"), "w"), indent=1)
print("\n".join(S))
