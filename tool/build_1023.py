#!/usr/bin/env python3
"""2026-10-23: 5 drive (mr popular) + 5 calm (AURA) catalogue reels. Black and black+white pairs first."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from editorial import page, record, stacked, dark_bg

SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "specs")
P = json.load(open(os.path.join(SP, "_paths.json")))["paths"]
A = "/mnt/user-data/uploads/9sky-reels/aesthetics/"
L = "/mnt/user-data/outputs/hooks-locations/"
O = "/mnt/user-data/outputs/stills-1023/"
os.makedirs(O, exist_ok=True)
COLL = "museum collection"
VEIL = dark_bg(A + "statues_dark/9skyaes_statues_dark_28.jpg", "statue", 0.30)
BACK = dark_bg(A + "statues_dark/9skyaes_statues_dark_13.jpg", "statue", 0.30)
VEIL2 = dark_bg(A + "statues_dark/9skyaes_statues_dark_31.jpg", "statue", 0.30)
ORN = dark_bg(A + "ornament/9skyaes_ornament_11.jpg", "ornament", 0.10, centre=0.15)
ORN2 = dark_bg(A + "ornament/9skyaes_ornament_06.jpg", "ornament", 0.10, centre=0.15)
B99, DROP = 60 / 99.0, 3.13
QZ_SUB, QZB_SUB = "BLACK  ·  RED RIBBED COLLAR", "AFTER THE ARA PACIS  ·  ROME, 9 BC"
REC = lambda col: [("OBJECT", "quarter zip"), ("COLOUR", col), ("DETAIL", "red ribbed collar"),
                   ("ORNAMENT", "after the Ara Pacis"), ("ORIGIN", "Prague"), ("DATE", "2026")]


def clip(name, start, **kw):
    d = dict(type="clip", src=L + name + ".mp4", start=start, align_red=False, speed=1.0, zoom=1.0,
             flip=False, crop_x=0.5, grade=dict(c=1.04, s=1.0, b=-0.03))
    d.update(kw)
    return d


def hook(name, start, **kw):
    return clip(name, start, until="drop", **kw)


def montage(shots):
    n = len(shots)
    first = DROP - (n - 1) * B99
    return [clip(nm, st, until="drop") if i == n - 1 else clip(nm, st, dur=first if i == 0 else B99)
            for i, (nm, st) in enumerate(shots)]


def img(p, b):
    return dict(type="image", src=p, fit="full", beats=b)


def ht(text, y=0.47):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


def flips(items, bg, tag):
    return [img(page(P[k], O + f"{tag}{i}.jpg", "N° " + ["I", "II", "III", "IV"][i], t, "", bg=bg), 1)
            for i, (k, t) in enumerate(items)]


S = {}
# ---------------- drive: mr popular, 99 BPM
S["R01_drive_collar"] = dict(seed=6001, track="mrpopular", segments=
    montage([("06_red-gown", 1.0), ("01_red-room-chandelier", 1.6), ("07_red-mirror-clock", 0.8), ("05_chandelier-pass", 2.0)]) +
    flips([("KF", "nero"), ("WF", "bianco"), ("KB", "the back"), ("WB", "the back")], None, "r01") +
    [img(stacked(P["PF"], P["PB"], O + "r01c.jpg", "N° V", COLL, "NERO  ·  BIANCO"), 4)],
    texts=[ht("the collar says it all.")])
S["R02_drive_black-or-white"] = dict(seed=6002, track="mrpopular", segments=
    montage([("08_white-dress-red-room", 0.6), ("03_red-velvet-salon", 0.6), ("02_red-wall-white-doors", 1.4), ("10_gold-chandelier", 1.5)]) +
    flips([("KF", "nero"), ("WF", "bianco"), ("KF", "nero"), ("WF", "bianco")], BACK, "r02") +
    [img(stacked(P["PF"], P["PB"], O + "r02c.jpg", "N° V", COLL, "PICK ONE", bg=BACK), 4)],
    texts=[ht("black or white?", 0.45)])
S["R03_drive_do-not-touch"] = dict(seed=6003, track="mrpopular", segments=
    montage([("16_armor-dark", 1.0), ("12_candles-montage", 1.6), ("15_dark-baroque-gold", 1.0), ("17_dome-ceiling", 0.4)]) +
    flips([("ZF", "nero"), ("XWF", "bianco"), ("ZB", "the back"), ("XWB", "the back")], VEIL, "r03") +
    [img(stacked(P["ZPF"], P["ZPB"], O + "r03c.jpg", "N° V", COLL, "DROP II  ·  FIRST LOOK", bg=VEIL), 4)],
    texts=[ht("do not touch the exhibits.")])
S["R04_drive_museums-dress-code"] = dict(seed=6004, track="mrpopular", segments=
    montage([("14_gothic-vaults", 0.3), ("09_orange-gallery", 0.4), ("13_palace-ceiling-walk", 1.2), ("01_red-room-chandelier", 2.4)]) +
    flips([("KF", "nero"), ("ZF", "nero"), ("WF", "bianco"), ("XWF", "bianco")], None, "r04") +
    [img(stacked(P["PF"], P["PB"], O + "r04c.jpg", "N° V", COLL, "DROP II  ·  FIRST LOOK"), 4)],
    texts=[ht("if museums had a dress code.")])
S["R05_drive_only-wears-black"] = dict(seed=6005, track="mrpopular", segments=
    montage([("12_candles-montage", 0.0), ("16_armor-dark", 1.2), ("15_dark-baroque-gold", 0.6), ("06_red-gown", 1.6)]) +
    flips([("KF", "nero"), ("ZF", "nero"), ("KB", "the back"), ("ZB", "the back")], None, "r05") +
    [img(stacked(P["KKF"], P["KKB"], O + "r05c.jpg", "N° V", COLL, "ALL BLACK  ·  ONE RED DETAIL"), 4)],
    texts=[ht("for the one who\nonly wears black.")])

# ---------------- calm: AURA, 2 / 2 / 4
S["R06_calm_collar"] = dict(seed=6006, segments=[hook("02_red-wall-white-doors", 0.3),
    img(page(P["KF"], O + "r06a.jpg", "N° I", "IX quarter zip", QZ_SUB, bg=ORN), 2),
    img(page(P["KB"], O + "r06b.jpg", "N° II", "the back", QZB_SUB, bg=ORN), 2),
    img(stacked(P["PF"], P["PB"], O + "r06c.jpg", "N° III", COLL, "NERO  ·  BIANCO", bg=ORN), 4)],
    texts=[ht("the collar says it all.", 0.40)])
S["R07_calm_black-or-white"] = dict(seed=6007, segments=[hook("06_red-gown", 0.4),
    img(page(P["KF"], O + "r07a.jpg", "PLATE I", "nero", QZ_SUB, bg=VEIL), 2),
    img(page(P["WF"], O + "r07b.jpg", "PLATE II", "bianco", "WHITE  ·  RED RIBBED COLLAR", bg=VEIL), 2),
    img(stacked(P["PF"], P["PB"], O + "r07c.jpg", "PLATE III", COLL, "PICK ONE", bg=VEIL), 4)],
    texts=[ht("black or white?", 0.34)])
S["R08_calm_museums-dress-code"] = dict(seed=6008, segments=[hook("07_red-mirror-clock", 0.1),
    img(record(P["KF"], O + "r08a.jpg", "INV. IX-001", REC("black"), "DROP II  ·  FIRST LOOK"), 2),
    img(page(P["KB"], O + "r08b.jpg", "INV. IX-001", "the back", QZB_SUB), 2),
    img(stacked(P["PF"], P["PB"], O + "r08c.jpg", "INDEX", COLL, "PICK ONE"), 4)],
    texts=[ht("if museums had a dress code.", 0.42)])
S["R09_calm_do-not-touch"] = dict(seed=6009, segments=[hook("13_palace-ceiling-walk", 0.4),
    img(page(P["ZF"], O + "r09a.jpg", "N° I", "IX zip hoodie", "BLACK  ·  RED-LINED HOOD", bg=BACK), 2),
    img(page(P["ZB"], O + "r09b.jpg", "N° II", "the back", QZB_SUB, bg=BACK), 2),
    img(stacked(P["ZPF"], P["ZPB"], O + "r09c.jpg", "N° III", COLL, "DROP II  ·  FIRST LOOK", bg=BACK), 4)],
    texts=[ht("do not touch the exhibits.", 0.47)])
S["R10_calm_only-wears-black"] = dict(seed=6010, segments=[hook("15_dark-baroque-gold", 0.2),
    img(page(P["KF"], O + "r10a.jpg", "N° I", "IX quarter zip", QZ_SUB), 2),
    img(page(P["ZF"], O + "r10b.jpg", "N° II", "IX zip hoodie", "BLACK  ·  RED-LINED HOOD"), 2),
    img(stacked(P["KKF"], P["KKB"], O + "r10c.jpg", "N° III", COLL, "ALL BLACK  ·  ONE RED DETAIL"), 4)],
    texts=[ht("for the one who\nonly wears black.", 0.45)])

for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"d1023_{k}.json"), "w"), indent=1)
print("\n".join(S))
