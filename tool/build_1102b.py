#!/usr/bin/env python3
"""2026-11-02 (evening): 10 Louboutin-hook reels, quarter zip only (Kirill 11-02; Louboutin never with the zip
hoodie, no "red inside" lines, short red flash ~0.4 s). One line of text per hook.
Hook weights from the stats so far: COUPLE strongest (63-71%), SOLES (62-64%), NAILS (60-62%), STREET weakest (54-57%).
Half are dynamic for mr popular (99 BPM): either a 2-shot Louboutin montage cut on the beat 2 beats before the
drop (first shot is pre-red footage, the red flash stays on the second), or the hook at ~1.15x; pages switch
every beat. The other half are calm on the aura grid."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, pages, fin_path, cat, COLLAR, IX, ARA, ROME, SP, P

B = 60.0 / 99.0
CUT = 3.13 - 2 * B
GR = dict(c=1.04, s=0.92, b=-0.012)


def lb(key, flip, crop_x, lead, speed=0.95, zoom=1.035, **kw):
    d = dict(type="clip", src=P[key], until="drop", align_red=True, speed=speed, zoom=zoom, crop_x=crop_x,
             flip=flip, lead=lead, grade=GR)
    d.update(kw)
    return d


def soles(flip, crop_x, speed=0.95, start=1.75):
    return lb("SOLES", flip, crop_x, 0.4, speed=speed, start=start, align_red=False)


def nails(flip, crop_x, speed=0.95, start=3.6):
    return lb("NAILS", flip, crop_x, 0.4, speed=speed, start=start, align_red=False)


def pre(key, start, flip, crop_x, speed=1.1):
    """first shot of a montage: footage before any red shows"""
    d = lb(key, flip, crop_x, 0.4, speed=speed, start=start, align_red=False)
    d.pop("until"); d["dur"] = CUT
    return d


def t(text, y=0.40):
    return [{"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}]


QW1 = [("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))]
QW2 = [("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR")), ("PF", cat(3, "BLACK  ·  WHITE"))]
QW3 = [("PF", cat(1, COLLAR)), ("KF", cat(2, IX))]
QK = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
QWW = [("WF", cat(1, "THE SAME RED COLLAR")), ("WB", cat(2, ARA, ROME))]
QF, QKF, QWF = ("PF", "PB"), ("KF", "KB"), ("WF", "WB")

R = [  # key, track, hook segments, text, pages, page beats, finale
    ("Q01_collar-says-it-all", "mrpopular", [lb("COUPLE", False, 0.55, 0.42, speed=1.15)], "the collar says it all.", QW1, 1, QF),
    ("Q02_black-or-white", "mrpopular", [pre("STREET", 1.4, True, 0.5), lb("COUPLE", True, 0.45, 0.42, speed=1.1)], "black or white?", QW2, 1, QF),
    ("Q03_museum", "mrpopular", [soles(True, 0.5, speed=1.12, start=1.25)], "what to wear\nto the museum.", QW3, 1, QF),
    ("Q04_one-red-detail", "mrpopular", [pre("NAILS", 1.6, False, 0.5), lb("COUPLE", False, 0.62, 0.42, speed=1.1)], "one red detail.", QK, 1, QKF),
    ("Q05_not-loud", "mrpopular", [nails(True, 0.5, speed=1.15, start=2.56)], "not loud.\njust red.", QWW, 1, QWF),
    ("Q06_red-sole-red-collar", "aura", [lb("COUPLE", True, 0.5, 0.42, speed=0.92)], "red sole. red collar.", QW1, 2, QF),
    ("Q07_only-wears-black", "aura", [soles(False, 0.5, start=1.7)], "for the one who\nonly wears black.", QK, 2, QKF),
    ("Q08_museum-black-white", "aura", [lb("COUPLE", False, 0.5, 0.45, speed=0.9)], "what to wear\nto the museum.", QW2, 2, QF),
    ("Q09_details", "aura", [nails(False, 0.5, start=3.11)], "it's in the details.", QW3, 2, QF),
    ("Q10_quiet-luxury", "aura", [lb("STREET", False, 0.45, 0.42)], "quiet luxury.\none red collar.", QWW, 2, QWF),
]
for i, (k, track, hook, text, pg, pb, fin) in enumerate(R):
    tag = f"q{i + 1:02d}"
    spec = dict(seed=17000 + i, track=track, segments=hook + pages(pg, None, tag, pb) +
                [img(fin_path(fin[0], fin[1], tag, "N° III" if len(pg) == 2 else "N° IV"), 4)], texts=t(text))
    json.dump(spec, open(os.path.join(SP, f"q1102_{k}.json"), "w"), indent=1)
    print(f"q1102_{k}")
