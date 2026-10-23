#!/usr/bin/env python3
"""2026-10-24 hook-mechanics test: 6 reels, each tests one retention mechanic on existing assets.
P1 flash-forward  - 0.33 s of the finale before the hook (product in the first second)
P2 dark-to-red    - 8 half-beat cuts from frame 0, dark shots, last one red
P3 red flicker    - slow dark hook with 2-frame red inserts (the old nail-flip micro-reveal)
P4 collar flicker - same, but the inserts are the collar page itself
P5 match cut      - red room until the drop, hard cut to the collar
P6 rush + flicker - P2 on AURA tempo with one collar insert
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from editorial import page, stacked, dark_bg

SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "specs")
P = json.load(open(os.path.join(SP, "_paths.json")))["paths"]
A = "/mnt/user-data/uploads/9sky-reels/aesthetics/"
L = "/mnt/user-data/outputs/hooks-locations/"
O = "/mnt/user-data/outputs/stills-1024/"
os.makedirs(O, exist_ok=True)
COLL, FL = "museum collection", "FIRST LOOK"
VEIL = dark_bg(A + "statues_dark/9skyaes_statues_dark_28.jpg", "statue", 0.30)
BACK = dark_bg(A + "statues_dark/9skyaes_statues_dark_13.jpg", "statue", 0.30)
DROP = 3.13
PRG, ROME = "PRAGUE, MMXXVI", "ROME, 9 BC"
cat = lambda n, what, place=PRG: f"CAT. {n:02d}  ·  {what}  ·  {place}"
FLEECE, COLLAR, HOOD, ARA, IX = "COTTON FLEECE", "RED RIBBED COLLAR", "RED-LINED HOOD", "AFTER THE ARA PACIS", "EMBOSSED IX"
F = 1 / 30.0


def clip(name, start, **kw):
    d = dict(type="clip", src=L + name + ".mp4", start=start, align_red=False, speed=1.0, zoom=1.0,
             flip=False, crop_x=0.5, grade=dict(c=1.04, s=1.0, b=-0.03))
    d.update(kw)
    return d


def img(p, b=None, dur=None):
    d = dict(type="image", src=p, fit="full")
    d.update(dict(dur=dur) if dur else dict(beats=b))
    return d


def ht(text, y=0.47, frm=0):
    return {"text": text, "from": frm, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


def pages(items, bg, tag, beats):
    nums = ["I", "II", "III", "IV"]
    return [img(page(P[k], O + f"{tag}{i}.jpg", "N° " + nums[i], "", line, bg=bg), beats) for i, (k, line) in enumerate(items)]


def fin_path(front, back, tag, no, bg=None):
    return stacked(P[front], P[back], O + f"{tag}c.jpg", no, COLL, FL, bg=bg)


def rush(shots, step):
    """cuts every `step` s from frame 0; last shot runs to the drop"""
    out, t = [], 0.0
    for i, (nm, st) in enumerate(shots):
        if i == len(shots) - 1:
            out.append(clip(nm, st, until="drop"))
        else:
            out.append(clip(nm, st, dur=step)); t += step
    return out


def flicker(base, base_start, inserts, end_with=None):
    """one continuous base shot interrupted by 2-frame inserts at given times (s).
    inserts: list of (time, segment-factory)"""
    out, t, pos = [], 0.0, base_start
    for at, seg in inserts:
        out.append(clip(base, pos, dur=at - t)); pos += at - t
        out.append(seg); t = at + 2 * F; pos += 2 * F
    out.append(clip(base, pos, until="drop") if end_with is None else clip(base, pos, dur=end_with - t))
    return out


B99 = 60 / 99.0
S = {}
# P1 flash-forward (mr popular)
fa = fin_path("KKF", "KKB", "p1", "N° V")
S["P1_flash-forward"] = dict(seed=9101, track="mrpopular", segments=
    [img(fa, dur=10 * F), clip("30_red-altar-chandelier", 0.3, until="drop")] +
    pages([("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME)), ("ZF", cat(3, HOOD)), ("ZB", cat(4, FLEECE))], None, "p1", 1) +
    [img(fa, 4)], texts=[ht("remember this one.", 0.47, 10 * F)])
# P2 dark-to-red rush (mr popular): 7 half-beat cuts then red to the drop
S["P2_dark-to-red"] = dict(seed=9102, track="mrpopular", segments=
    rush([("16_armor-dark", 0.6), ("32_dark-sculpture-walls", 0.4), ("34_dark-dome", 0.5), ("15_dark-baroque-gold", 1.0),
          ("35_dark-dome-b", 0.6), ("26_church-nave", 0.5), ("12_candles-montage", 0.4), ("02_red-wall-white-doors", 1.2)], B99 / 2 * 1.0 + 0.0) +
    pages([("KF", cat(1, FLEECE)), ("WF", cat(2, COLLAR)), ("ZF", cat(3, HOOD)), ("XWF", cat(4, IX))], None, "p2", 1) +
    [img(fin_path("PF", "PB", "p2", "N° V"), 4)], texts=[ht("it starts dark.")])
# P3 red flicker (AURA): dark dome, 2-frame red inserts
S["P3_red-flicker"] = dict(seed=9103, segments=
    flicker("34_dark-dome", 0.3, [(1.0, clip("02_red-wall-white-doors", 1.5, dur=2 * F)),
                                  (1.9, clip("07_red-mirror-clock", 1.0, dur=2 * F)),
                                  (2.6, clip("06_red-gown", 1.5, dur=2 * F))]) +
    pages([("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR"))], VEIL, "p3", 2) +
    [img(fin_path("PF", "PB", "p3", "N° III", VEIL), 4)], texts=[ht("did you see it?", 0.42)])
# P4 collar flicker (AURA): dark sculpture walls, inserts are the collar page
kp = page(P["WF"], O + "p4x.jpg", "", "", "", bg=None)
S["P4_collar-flicker"] = dict(seed=9104, segments=
    flicker("32_dark-sculpture-walls", 0.2, [(1.2, img(kp, dur=2 * F)), (2.4, img(kp, dur=2 * F))]) +
    pages([("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))], None, "p4", 2) +
    [img(fin_path("KKF", "KKB", "p4", "N° III"), 4)], texts=[ht("you blinked.", 0.42)])
# P5 match cut (AURA): red room straight into the red collar
S["P5_match-cut"] = dict(seed=9105, segments=
    [clip("07_red-mirror-clock", 0.2, until="drop")] +
    pages([("KF", cat(1, COLLAR)), ("WF", cat(2, COLLAR))], None, "p5", 2) +
    [img(fin_path("PF", "PB", "p5", "N° III", BACK), 4)], texts=[ht("same red.", 0.60)])
# P6 rush with one collar insert (mr popular)
S["P6_rush-collar"] = dict(seed=9106, track="mrpopular", segments=
    rush([("26_church-nave", 0.4), ("33_medallion-wall", 0.5), ("16_armor-dark", 1.2), ("36_fresco-ceiling-gold", 0.6),
          ("35_dark-dome-b", 1.0)], B99 / 2)[:-1] +
    [img(kp, dur=2 * F), clip("06_red-gown", 1.2, until="drop")] +
    pages([("ZF", cat(1, HOOD)), ("KF", cat(2, COLLAR)), ("ZB", cat(3, ARA, ROME)), ("KB", cat(4, FLEECE))], BACK, "p6", 1) +
    [img(fin_path("ZPF", "ZPB", "p6", "N° V", BACK), 4)], texts=[ht("one red thing.")])

for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"m1024_{k}.json"), "w"), indent=1)
print("\n".join(S))
