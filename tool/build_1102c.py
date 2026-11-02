#!/usr/bin/env python3
"""2026-11-02 (late): 4 test reels that combine a rose hook and a Louboutin hook in one (Kirill's idea).
The rose opens (stops the scroll with red), the red sole closes the hook right before the drop, then the quarter zip.
Louboutin is in the hook, so quarter zip only. One line of text for the whole hook, mid-frame so it sits well on both.
Two cut on the mr popular beat (2 beats before the drop), two calm on the aura grid (3 beats before the drop).
M04 is a hand-to-hand match: pale hand with the rose -> hand with nails -> red sole."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, pages, fin_path, cat, COLLAR, IX, ARA, ROME, SP, P

G = "/mnt/user-data/uploads/flowers hooks/"
GR = dict(c=1.04, s=0.92, b=-0.012)
CUT = {"mrpopular": 3.13 - 2 * 60 / 99.0, "aura": 3.13 - 3 * 60 / 123.05}


def rose(name, cut, start=0.0, speed=1.0, flip=False):
    return dict(type="clip", src=G + name + ".mp4", start=start, dur=cut, align_red=False, speed=speed,
                zoom=1.0, crop_x=0.5, flip=flip, grade={})


def lb(key, flip, crop_x, lead=0.42, speed=1.0, **kw):
    d = dict(type="clip", src=P[key], until="drop", align_red=True, speed=speed, zoom=1.035, crop_x=crop_x,
             flip=flip, lead=lead, grade=GR)
    d.update(kw)
    return d


def t(text, y=0.56):
    return [{"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.45, "font": "cg-italic"}]


QW1 = [("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))]
QW2 = [("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR")), ("PF", cat(3, "BLACK  ·  WHITE"))]
QK = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
QW3 = [("PF", cat(1, COLLAR)), ("KF", cat(2, IX))]
QF, QKF = ("PF", "PB"), ("KF", "KB")

R = [  # key, track, hook segments, text, pages, page beats, finale
    ("M01_three-reds", "mrpopular", lambda c: [rose("g3", c, speed=1.1), lb("COUPLE", False, 0.55, speed=1.1)],
     "red rose. red sole. red collar.", QW1, 1, QF),
    ("M02_date-night", "mrpopular", lambda c: [rose("g2", c, start=0.2, speed=1.1),
                                               lb("SOLES", True, 0.5, speed=1.1, start=3.42, align_red=False)],
     "date night.", QW2, 1, QF),
    ("M03_one-red-each", "aura", lambda c: [rose("g1", c, start=0.4), lb("COUPLE", True, 0.5, speed=0.95)],
     "one red thing each.", QK, 2, QKF),
    ("M04_she-prefers-red", "aura", lambda c: [rose("g1", c, start=0.3, flip=True),
                                               lb("NAILS", False, 0.5, speed=1.35, start=4.0, align_red=False)],
     "she prefers red.", QW3, 2, QF),
]
for i, (k, track, hook, text, pg, pb, fin) in enumerate(R):
    tag = f"m{i + 1:02d}"
    spec = dict(seed=18000 + i, track=track, segments=hook(CUT[track]) + pages(pg, None, tag, pb) +
                [img(fin_path(fin[0], fin[1], tag, "N° III" if len(pg) == 2 else "N° IV"), 4)], texts=t(text))
    json.dump(spec, open(os.path.join(SP, f"m1102_{k}.json"), "w"), indent=1)
    print(f"m1102_{k}")
