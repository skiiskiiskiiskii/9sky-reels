#!/usr/bin/env python3
"""2026-10-23 v2: 10 reels, simple curiosity hooks, grey CAT lines, finale museum collection / FIRST LOOK."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from editorial import page, stacked, dark_bg

SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "specs")
P = json.load(open(os.path.join(SP, "_paths.json")))["paths"]
A = "/mnt/user-data/uploads/9sky-reels/aesthetics/"
L = "/mnt/user-data/outputs/hooks-locations/"
O = "/mnt/user-data/outputs/stills-1023b/"
os.makedirs(O, exist_ok=True)
COLL, FL = "museum collection", "FIRST LOOK"
VEIL = dark_bg(A + "statues_dark/9skyaes_statues_dark_28.jpg", "statue", 0.30)
BACK = dark_bg(A + "statues_dark/9skyaes_statues_dark_13.jpg", "statue", 0.30)
ORN = dark_bg(A + "ornament/9skyaes_ornament_11.jpg", "ornament", 0.10, centre=0.15)
B99, DROP = 60 / 99.0, 3.13
PRG, ROME = "PRAGUE, MMXXVI", "ROME, 9 BC"
cat = lambda n, what, place=PRG: f"CAT. {n:02d}  ·  {what}  ·  {place}"
FLEECE, COLLAR, HOOD, ARA, IX = "COTTON FLEECE", "RED RIBBED COLLAR", "RED-LINED HOOD", "AFTER THE ARA PACIS", "EMBOSSED IX"


def clip(name, start, **kw):
    d = dict(type="clip", src=L + name + ".mp4", start=start, align_red=False, speed=1.0, zoom=1.0,
             flip=False, crop_x=0.5, grade=dict(c=1.04, s=1.0, b=-0.03))
    d.update(kw)
    return d


def montage(shots):
    n = len(shots)
    first = DROP - (n - 1) * B99
    return [clip(nm, st, until="drop") if i == n - 1 else clip(nm, st, dur=first if i == 0 else B99)
            for i, (nm, st) in enumerate(shots)]


def img(p, b):
    return dict(type="image", src=p, fit="full", beats=b)


def ht(text, y=0.47):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


def pages(items, bg, tag, beats):
    nums = ["I", "II", "III", "IV"]
    return [img(page(P[k], O + f"{tag}{i}.jpg", "N° " + nums[i], "", line, bg=bg), beats) for i, (k, line) in enumerate(items)]


def fin(front, back, tag, no, bg=None):
    return img(stacked(P[front], P[back], O + f"{tag}c.jpg", no, COLL, FL, bg=bg), 4)


S = {}
# ---------------- drive (mr popular): montage hook, 4 x 1-beat pages, 4-beat finale
S["01_drive_wont-catch-it-all"] = dict(seed=8001, track="mrpopular", segments=
    montage([("09_orange-gallery", 0.4), ("13_palace-ceiling-walk", 1.4), ("05_chandelier-pass", 1.8), ("10_gold-chandelier", 1.6)]) +
    pages([("KF", cat(1, FLEECE)), ("WF", cat(2, COLLAR)), ("ZF", cat(3, HOOD)), ("XWF", cat(4, IX))], None, "a", 1) +
    [fin("PF", "PB", "a", "N° V")], texts=[ht("you won't catch it all.")])
S["02_drive_quiet-until"] = dict(seed=8002, track="mrpopular", segments=
    montage([("12_candles-montage", 0.0), ("16_armor-dark", 1.2), ("15_dark-baroque-gold", 0.6), ("01_red-room-chandelier", 2.4)]) +
    pages([("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME)), ("ZF", cat(3, HOOD)), ("ZB", cat(4, FLEECE))], None, "b", 1) +
    [fin("KKF", "KKB", "b", "N° V")], texts=[ht("quiet until it isn't.")])
S["03_drive_white-outside"] = dict(seed=8003, track="mrpopular", segments=
    montage([("08_white-dress-red-room", 0.4), ("02_red-wall-white-doors", 1.4), ("07_red-mirror-clock", 0.6), ("06_red-gown", 1.6)]) +
    pages([("XWF", cat(1, HOOD)), ("XWB", cat(2, ARA, ROME)), ("WF", cat(3, COLLAR)), ("WB", cat(4, FLEECE))], VEIL, "c", 1) +
    [fin("ZPF", "ZPB", "c", "N° V", VEIL)], texts=[ht("white outside.\nred inside.")])
S["04_drive_zip-or-quarter"] = dict(seed=8004, track="mrpopular", segments=
    montage([("14_gothic-vaults", 0.3), ("17_dome-ceiling", 0.4), ("03_red-velvet-salon", 0.6), ("05_chandelier-pass", 2.2)]) +
    pages([("ZF", cat(1, HOOD)), ("KF", cat(2, COLLAR)), ("ZB", cat(3, ARA, ROME)), ("KB", cat(4, ARA, ROME))], None, "d", 1) +
    [fin("KKF", "KKB", "d", "N° V")], texts=[ht("zip or quarter zip?")])
S["05_drive_louder-inside"] = dict(seed=8005, track="mrpopular", segments=
    montage([("15_dark-baroque-gold", 1.2), ("12_candles-montage", 1.6), ("16_armor-dark", 0.6), ("01_red-room-chandelier", 2.0)]) +
    pages([("ZF", cat(1, HOOD)), ("XWF", cat(2, HOOD)), ("ZB", cat(3, FLEECE)), ("XWB", cat(4, ARA, ROME))], BACK, "e", 1) +
    [fin("ZPF", "ZPB", "e", "N° V", BACK)], texts=[ht("louder on the inside.")])
# ---------------- calm (AURA): one hook, 2 x 2-beat pages, 4-beat finale
S["06_calm_his-and-hers"] = dict(seed=8006, segments=[clip("03_red-velvet-salon", 0.3, until="drop")] +
    pages([("KF", cat(1, "HIS")), ("WF", cat(2, "HERS"))], VEIL, "f", 2) + [fin("PF", "PB", "f", "N° III", VEIL)],
    texts=[ht("his & hers.", 0.60)])
S["07_calm_all-in-the-collar"] = dict(seed=8007, segments=[clip("01_red-room-chandelier", 0.35, until="drop")] +
    pages([("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR"))], ORN, "g", 2) + [fin("PF", "PB", "g", "N° III", ORN)],
    texts=[ht("it's all in the collar.", 0.60)])
S["08_calm_come-closer"] = dict(seed=8008, segments=[clip("04_golden-hall-windows", 0.2, until="drop")] +
    pages([("KF", cat(1, IX)), ("KB", cat(2, ARA, ROME))], BACK, "h", 2) + [fin("PF", "PB", "h", "N° III", BACK)],
    texts=[ht("you have to\ncome closer.", 0.62)])
S["09_calm_not-loud"] = dict(seed=8009, segments=[clip("07_red-mirror-clock", 0.4, until="drop")] +
    pages([("KF", cat(1, COLLAR)), ("ZF", cat(2, HOOD))], None, "i", 2) + [fin("KKF", "KKB", "i", "N° III")],
    texts=[ht("not loud. just red.", 0.42)])
S["10_calm_second-look"] = dict(seed=8010, segments=[clip("14_gothic-vaults", 0.3, until="drop")] +
    pages([("KF", cat(1, FLEECE)), ("KB", cat(2, ARA, ROME))], VEIL, "j", 2) + [fin("PF", "PB", "j", "N° III", VEIL)],
    texts=[ht("the second look\nis the point.", 0.56)])

for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"d1023b_{k}.json"), "w"), indent=1)
print("\n".join(S))
