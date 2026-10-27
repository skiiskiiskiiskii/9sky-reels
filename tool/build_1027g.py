#!/usr/bin/env python3
"""2026-10-27 batch 7: the G3 "keep up." format (10-23/24 reel, 4.9k views, 7.6 s average watch, RISK MONEY):
black-and-white statue stills, cuts speed up 0.45 s -> 2 frames, landing on a bust in a red niche;
then 4 pages at 1 beat on the dark statue backdrop, EX MUSEO finale. New still sets and landings per reel."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hookgen import accelerate
from build_1024 import img, pages, fin_path, cat, BACK, VEIL, COLLAR, ARA, ROME, HOOD, FLEECE, IX, SP

A = "/mnt/user-data/uploads/9sky-reels/aesthetics/"
G = "/mnt/user-data/outputs/hooks-gen/"
d = lambda n: A + f"statues_dark/9skyaes_statues_dark_{n}.jpg"
a = lambda n: A + f"statues_athletic/9skyaes_statues_athletic_{n:02d}.jpg"
r = lambda n: A + f"busts_red/9skyaes_busts_red_{n}.jpg"

R = [  # key, stills, landing, text, pages, finale, backdrop
    ("A01_dont-blink", [d(31), a(10), d(34), a(23), d(35), d(13)], r(21), "don't blink.",
     [("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR")), ("ZF", cat(3, HOOD)), ("KB", cat(4, ARA, ROME))], ("PF", "PB"), BACK),
    ("A02_wait-for-the-red", [a(4), d(21), d(20), a(24), d(33), a(16)], r(36), "wait for the red.",
     [("ZF", cat(1, HOOD)), ("XWF", cat(2, HOOD)), ("KF", cat(3, COLLAR)), ("ZB", cat(4, ARA, ROME))], ("ZPF", "ZPB"), VEIL),
    ("A03_keep-up", [d(28), a(18), d(31), a(1), d(21), a(23)], r(15), "keep up.",
     [("KF", cat(1, FLEECE)), ("WF", cat(2, COLLAR)), ("ZF", cat(3, HOOD)), ("KB", cat(4, ARA, ROME))], ("ZPF", "ZPB"), BACK),
]


def hook(name):
    return dict(type="clip", src=G + name + ".mp4", start=0, align_red=False, speed=1.0, zoom=1.0,
                flip=False, crop_x=0.5, grade=dict(c=1.0, s=1.0, b=0.0), until="drop")


S = {}
for i, (k, stills, last, text, pg, fin, bg) in enumerate(R):
    if not os.path.exists(G + k + ".mp4"):
        accelerate(stills, last, G + k + ".mp4")
    tag = f"a{i + 1:02d}"
    S[k] = dict(seed=10700 + i, track="mrpopular", segments=[hook(k)] + pages(pg, bg, tag, 1) +
                [img(fin_path(fin[0], fin[1], tag, "N° V", bg), 4)],
                texts=[{"text": text, "from": 0, "to": "drop", "y": 0.47, "size": 96, "scrim": 0.5, "font": "cg-italic"}])
for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"a1027_{k}.json"), "w"), indent=1)
print("\n".join(S))
