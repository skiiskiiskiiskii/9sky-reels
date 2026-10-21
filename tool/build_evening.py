#!/usr/bin/env python3
"""2026-10-21 evening batch: 4 calm (AURA) + 4 drive (mr popular, 99 BPM) catalogue reels."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from editorial import page, spread, stacked, dark_bg

SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "specs")
P = json.load(open(os.path.join(SP, "_paths.json")))["paths"]
A = "/mnt/user-data/uploads/9sky-reels/aesthetics/"
L = "/mnt/user-data/outputs/hooks-locations/"
O = "/mnt/user-data/outputs/evening-stills/"
os.makedirs(O, exist_ok=True)
COLL = "museum collection"
VEIL = dark_bg(A + "statues_dark/9skyaes_statues_dark_28.jpg", "statue", 0.30)
BACK = dark_bg(A + "statues_dark/9skyaes_statues_dark_13.jpg", "statue", 0.30)
ORN2 = dark_bg(A + "ornament/9skyaes_ornament_06.jpg", "ornament", 0.10, centre=0.15)
B99 = 60 / 99.0
DROP = 3.13


def clip(name, start, **kw):
    d = dict(type="clip", src=L + name + ".mp4", start=start, align_red=False, speed=1.0, zoom=1.0,
             flip=False, crop_x=0.5, grade=dict(c=1.04, s=1.0, b=-0.03))
    d.update(kw)
    return d


def hook(name, start, **kw):
    return clip(name, start, until="drop", **kw)


def montage(shots):
    """Hook cut on the 99 BPM grid so the last cut before the drop lands on a beat."""
    n = len(shots)
    first = DROP - (n - 1) * B99
    segs = []
    for i, (name, start) in enumerate(shots):
        if i == n - 1:
            segs.append(clip(name, start, until="drop"))
        else:
            segs.append(clip(name, start, dur=first if i == 0 else B99))
    return segs


def img(p, b):
    return dict(type="image", src=p, fit="full", beats=b)


def ht(text, y=0.47):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


S = {}
# ------------------------------------------------ calm, AURA (2 / 2 / 4 beats)
S["E1_calm_do-not-touch"] = dict(seed=4001, segments=[hook("05_chandelier-pass", 0.2),
    img(page(P["KF"], O + "e1a.jpg", "N° I", "IX quarter zip", "BLACK  ·  RED RIBBED COLLAR", bg=VEIL), 2),
    img(page(P["KB"], O + "e1b.jpg", "N° II", "the back", "AFTER THE ARA PACIS  ·  ROME, 9 BC", bg=VEIL), 2),
    img(stacked(P["PF"], P["PB"], O + "e1c.jpg", "N° III", COLL, "DROP II  ·  FIRST LOOK", bg=VEIL), 4)],
    texts=[ht("do not touch the exhibits.", 0.40)])
S["E2_calm_collar"] = dict(seed=4002, segments=[hook("07_red-mirror-clock", 0.1),
    img(page(P["WF"], O + "e2a.jpg", "N° I", "IX quarter zip", "WHITE  ·  RED RIBBED COLLAR", bg=BACK), 2),
    img(page(P["WB"], O + "e2b.jpg", "N° II", "the back", "AFTER THE ARA PACIS  ·  ROME, 9 BC", bg=BACK), 2),
    img(stacked(P["PF"], P["PB"], O + "e2c.jpg", "N° III", COLL, "NERO  ·  BIANCO", bg=BACK), 4)],
    texts=[ht("the collar says it all.", 0.42)])
S["E3_calm_private-viewing"] = dict(seed=4003, segments=[hook("10_gold-chandelier", 0.2),
    img(page(P["ZF"], O + "e3a.jpg", "N° I", "IX zip hoodie", "BLACK  ·  RED-LINED HOOD", bg=ORN2), 2),
    img(page(P["XWF"], O + "e3b.jpg", "N° II", "IX zip hoodie", "WHITE  ·  RED-LINED HOOD", bg=ORN2), 2),
    img(stacked(P["ZPF"], P["ZPB"], O + "e3c.jpg", "N° III", COLL, "DROP II  ·  FIRST LOOK", bg=ORN2), 4)],
    texts=[ht("private viewing.", 0.62)])
S["E4_calm_rome-prague"] = dict(seed=4004, segments=[hook("15_dark-baroque-gold", 0.4),
    img(page(P["KF"], O + "e4a.jpg", "N° I", "IX quarter zip", "BLACK  ·  RED RIBBED COLLAR", bg=VEIL), 2),
    img(spread(A + "ornament/9skyaes_ornament_05.jpg", None, "Ara Pacis", "ROME  ·  9 BC", P["KB"], "IX quarter zip", "PRAGUE  ·  2026", O + "e4b.jpg", "N° II", bg=VEIL), 2),
    img(stacked(P["PF"], P["PB"], O + "e4c.jpg", "N° III", COLL, "PRAGUE  ·  MMXXVI", bg=VEIL), 4)],
    texts=[ht("rome, 9 bc.\nprague, 2026.", 0.45)])

# ------------------------------------------------ drive, mr popular (montage hooks, 1-beat flips, 4-beat finale)
def flips(items, bg, tag):
    out = []
    for i, (k, title) in enumerate(items):
        out.append(img(page(P[k], O + f"{tag}{i}.jpg", "N° " + ["I", "II", "III", "IV"][i], title, "", bg=bg), 1))
    return out

S["D1_drive_museum-after-dark"] = dict(seed=5001, track="mrpopular", segments=
    montage([("09_orange-gallery", 0.4), ("13_palace-ceiling-walk", 1.2), ("06_red-gown", 1.0), ("01_red-room-chandelier", 2.4)]) +
    flips([("KF", "nero"), ("WF", "bianco"), ("KB", "the back"), ("WB", "the back")], None, "d1") +
    [img(stacked(P["PF"], P["PB"], O + "d1c.jpg", "N° V", COLL, "DROP II  ·  FIRST LOOK"), 4)],
    texts=[ht("the museum after dark.", 0.47)])
S["D2_drive_do-not-touch"] = dict(seed=5002, track="mrpopular", segments=
    montage([("12_candles-montage", 0.0), ("17_dome-ceiling", 0.4), ("16_armor-dark", 1.0), ("15_dark-baroque-gold", 1.0)]) +
    flips([("ZF", "nero"), ("XWF", "bianco"), ("ZB", "the back"), ("XWB", "the back")], VEIL, "d2") +
    [img(stacked(P["ZPF"], P["ZPB"], O + "d2c.jpg", "N° V", COLL, "DROP II  ·  FIRST LOOK", bg=VEIL), 4)],
    texts=[ht("do not touch the exhibits.", 0.47)])
S["D3_drive_collar"] = dict(seed=5003, track="mrpopular", segments=[hook("13_palace-ceiling-walk", 0.0, speed=1.15)] +
    flips([("KF", "nero"), ("WF", "bianco"), ("KF", "nero"), ("WF", "bianco")], None, "d3") +
    [img(stacked(P["PF"], P["PB"], O + "d3c.jpg", "N° V", COLL, "NERO  ·  BIANCO"), 4)],
    texts=[ht("the collar says it all.", 0.47)])
S["D4_drive_black-or-white"] = dict(seed=5004, track="mrpopular", segments=
    montage([("03_red-velvet-salon", 0.6), ("07_red-mirror-clock", 0.8), ("08_white-dress-red-room", 0.6), ("05_chandelier-pass", 2.0)]) +
    flips([("KF", "nero"), ("WF", "bianco"), ("ZF", "nero"), ("XWF", "bianco")], BACK, "d4") +
    [img(stacked(P["PF"], P["PB"], O + "d4c.jpg", "N° V", COLL, "PICK ONE", bg=BACK), 4)],
    texts=[ht("black or white?", 0.45)])

for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"eve_{k}.json"), "w"), indent=1)
print("\n".join(S))
