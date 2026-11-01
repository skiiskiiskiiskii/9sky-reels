#!/usr/bin/env python3
"""2026-11-02: 10 rose-only reels (Kirill 11-02).
One line of text for the whole hook (no second line joining). Short single lines, the style of Kirill's own
(my color. / red / favourite color.) - those held 39-50% on 10-31, the two-step lines 25-37%.
Half are dynamic for mr popular (99 BPM, drop 3.13): either a 3-shot rose montage cut on the beat
(0.706 s and 1.918 s are beats before the drop) at 1.25x, or one hook at ~1.3x; mockup pages switch every beat.
No strobe, flashes or punch-ins - only beat cuts and speed.
The other half stay calm on the aura grid, one hook at normal speed."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, pages, fin_path, cat, COLLAR, HOOD, IX, ARA, ROME, SP

G = "/mnt/user-data/uploads/flowers hooks/"
B = 60.0 / 99.0                       # mr popular beat
CUT1, CUT2 = 3.13 - 4 * B, 3.13 - 2 * B
START = {"g1": 0.5, "g2": 0.3, "g3": 0.0}


def rose(name, flip=False, speed=1.0, start=None, **kw):
    d = dict(type="clip", src=G + name + ".mp4", start=START[name] if start is None else start, until="drop",
             align_red=False, speed=speed, zoom=1.0, crop_x=0.5, flip=flip, grade={})
    d.update(kw)
    return d


def montage(order, flips=(False, False, False), speed=1.25):
    a, b, c = order
    return [dict(rose(a, flips[0], speed), dur=CUT1, until=None),
            dict(rose(b, flips[1], speed), dur=CUT2 - CUT1, until=None),
            rose(c, flips[2], speed)]


def t(text, y=0.79):
    return [{"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.4, "font": "cg-italic"}]


KNIT = "BLACK KNIT"
QW1 = [("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))]
QW2 = [("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR")), ("PF", cat(3, "BLACK  ·  WHITE"))]
QW3 = [("PF", cat(1, COLLAR)), ("KF", cat(2, IX))]
QK = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
ZH = [("ZF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))]
ZHB = [("XWF", cat(1, HOOD)), ("ZB", cat(2, ARA, ROME)), ("ZPF", cat(3, "BLACK  ·  WHITE"))]
SW = [("KF", cat(1, COLLAR)), ("SWF", cat(2, KNIT)), ("SPF", cat(3, "ALL BLACK  ·  ONE RED"))]
QF, ZFIN, SFIN = ("PF", "PB"), ("ZPF", "ZPB"), ("SPF", "SPB")

R = [  # key, track, hook segments, text, pages, page beats, finale
    ("D01_red-always", "mrpopular", montage(("g2", "g3", "g1")), "red, always.", QW1, 1, QF),
    ("D02_love-language", "mrpopular", montage(("g3", "g1", "g2"), (False, True, False)), "love language: red.", ZHB, 1, ZFIN),
    ("D03_pov-your-color", "mrpopular", [rose("g2", speed=1.3, start=0.0)], "pov: your color is red.", QW2, 1, QF),
    ("D04_obsessed-with-red", "mrpopular", montage(("g1", "g2", "g3"), (True, True, True)), "obsessed with red.", SW, 1, SFIN),
    ("D05_red-flag", "mrpopular", [rose("g1", flip=True, speed=1.3, start=0.0)], "red flag? red collar.", QK, 1, QF),
    ("C01_the-only-color", "aura", [rose("g3")], "the only color.", QW1, 2, QF),
    ("C02_youre-my-red", "aura", [rose("g3", flip=True)], "you're my red.", QW2, 2, QF),
    ("C03_red-details", "aura", [rose("g2", flip=True)], "black outfit.\nred details.", QW3, 2, QF),
    ("C04_for-the-red-ones", "aura", [rose("g1", flip=True)], "for the red ones.", ZH, 2, ZFIN),
    ("C05_red-kind-of-person", "aura", [rose("g2")], "a red kind\nof person.", SW, 2, SFIN),
]
for i, (k, track, hook, text, pg, pb, fin) in enumerate(R):
    tag = f"n{i + 1:02d}"
    hook = [{kk: vv for kk, vv in s.items() if vv is not None} for s in hook]
    spec = dict(seed=16000 + i, track=track, segments=hook + pages(pg, None, tag, pb) +
                [img(fin_path(fin[0], fin[1], tag, "N° III" if len(pg) == 2 else "N° IV"), 4)], texts=t(text))
    json.dump(spec, open(os.path.join(SP, f"n1102_{k}.json"), "w"), indent=1)
    print(f"n1102_{k}")
