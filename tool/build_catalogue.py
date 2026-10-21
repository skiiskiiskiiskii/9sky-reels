#!/usr/bin/env python3
"""Catalogue-style test reels C1..C6 (variant A family)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from editorial import page, annotated, record, spread, plates, poster, index, dark_bg

SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "specs")
P = json.load(open(os.path.join(SP, "_paths.json")))["paths"]
A = "/mnt/user-data/uploads/9sky-reels/aesthetics/"
L = "/mnt/user-data/outputs/hooks-locations/"
O = "/mnt/user-data/outputs/catalogue-stills/"
os.makedirs(O, exist_ok=True)

ORN = dark_bg(A + "ornament/9skyaes_ornament_11.jpg", "ornament", 0.10, centre=0.15)
ORN2 = dark_bg(A + "ornament/9skyaes_ornament_06.jpg", "ornament", 0.10, centre=0.15)
VEIL = dark_bg(A + "statues_dark/9skyaes_statues_dark_28.jpg", "statue", 0.30)
BACK = dark_bg(A + "statues_dark/9skyaes_statues_dark_13.jpg", "statue", 0.30)
QZ_KF_NOTES = [((535, 610), "RED RIBBED COLLAR", (90, 330), "l"), ((540, 790), "METAL ZIP", (990, 330), "r"),
               ((655, 935), "IX, EMBOSSED", (990, 1420), "r")]
QZ_KB_NOTES = [((540, 880), "AFTER THE ARA PACIS, 9 BC", (90, 330), "l"), ((540, 620), "HIGH COLLAR", (990, 1420), "r")]
REC = lambda col: [("OBJECT", "quarter zip"), ("COLOUR", col), ("DETAIL", "red ribbed collar"),
                   ("ORNAMENT", "after the Ara Pacis"), ("ORIGIN", "Prague"), ("DATE", "2026")]
FOUR = [P["KF"], P["WF"], P["ZF"], P["XWF"]]
FOUR_N = ["black quarter zip", "white quarter zip", "black zip hoodie", "white zip hoodie"]


def hook(name, start, b=-0.03):
    return dict(type="clip", src=L + name + ".mp4", start=start, until="drop", align_red=False, speed=1.0,
                zoom=1.0, flip=False, crop_x=0.5, grade=dict(c=1.04, s=1.0, b=b))


def img(p, b):
    return dict(type="image", src=p, fit="full", beats=b)


def ht(text, y=0.47):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


S = {}
S["C1_annotated"] = dict(seed=3001, grain=4, segments=[hook("06_red-gown", 0.2),
    img(annotated(P["KF"], O + "c1a.jpg", "N° I", "IX quarter zip", "BLACK  ·  PLATE I", QZ_KF_NOTES, bg=ORN), 2),
    img(annotated(P["KB"], O + "c1b.jpg", "N° II", "the back", "BLACK  ·  PLATE II", QZ_KB_NOTES, bg=ORN), 2),
    img(plates([P["KF"], P["WF"]], ["I", "II"], ["NERO", "BIANCO"], O + "c1c.jpg", "N° III", "one only. which?", "THE SAME RED COLLAR", bg=ORN), 4)],
    texts=[ht("the collar says it all.", 0.36)])
S["C2_record"] = dict(seed=3002, grain=4, segments=[hook("11_museum-flash-cuts", 0.0),
    img(record(P["KF"], O + "c2a.jpg", "INV. IX-001", REC("black"), "9SKY  ·  DROP II"), 2),
    img(record(P["WF"], O + "c2b.jpg", "INV. IX-002", REC("white"), "9SKY  ·  DROP II"), 2),
    img(index(FOUR, FOUR_N, O + "c2c.jpg", "INDEX", "the collection", "PICK ONE  ·  I, II, III OR IV"), 4)],
    texts=[ht("if museums had a dress code.")])
S["C3_spread"] = dict(seed=3003, grain=4, segments=[hook("14_gothic-vaults", 0.3),
    img(page(P["KF"], O + "c3a.jpg", "N° I", "IX quarter zip", "BLACK  ·  RED RIBBED COLLAR", bg=VEIL), 2),
    img(spread(A + "ornament/9skyaes_ornament_05.jpg", None, "Ara Pacis", "ROME  ·  9 BC", P["KB"], "IX quarter zip", "PRAGUE  ·  2026", O + "c3b.jpg", "N° II", bg=VEIL), 2),
    img(page(P["PF"], O + "c3c.jpg", "N° III", "black or white", "THE COLLECTION  ·  PRAGUE", bg=VEIL), 4)],
    texts=[ht("some things are built to last.", 0.56)])
S["C4_plates"] = dict(seed=3004, grain=4, segments=[hook("18_red-beat-montage", 0.0, b=-0.05),
    img(page(P["KF"], O + "c4a.jpg", "PLATE I", "nero", "BLACK  ·  RED RIBBED COLLAR", bg=BACK), 2),
    img(page(P["WF"], O + "c4b.jpg", "PLATE II", "bianco", "WHITE  ·  RED RIBBED COLLAR", bg=BACK), 2),
    img(plates([P["KF"], P["WF"]], ["I", "II"], ["NERO", "BIANCO"], O + "c4c.jpg", "PLATE III", "one only. which?", "THE SAME RED COLLAR", bg=BACK), 4)],
    texts=[ht("black or white?", 0.45)])
S["C5_poster"] = dict(seed=3005, grain=4, segments=[hook("08_white-dress-red-room", 0.2),
    img(page(P["XWF"], O + "c5a.jpg", "N° I", "IX zip hoodie", "WHITE  ·  RED-LINED HOOD", bg=VEIL), 2),
    img(page(P["XWB"], O + "c5b.jpg", "N° II", "the back", "AFTER THE ARA PACIS  ·  ROME, 9 BC", bg=VEIL), 2),
    img(poster(P["ZPF"], O + "c5c.jpg", "Drop II", "an exhibition in black, white and red", "PRAGUE  ·  MMXXVI", bg=VEIL), 4)],
    texts=[ht("white outside. red inside.", 0.45)])
S["C6_index"] = dict(seed=3006, grain=4, segments=[hook("03_red-velvet-salon", 0.3),
    img(page(P["KF"], O + "c6a.jpg", "N° I", "IX quarter zip", "BLACK  ·  RED RIBBED COLLAR", bg=ORN2), 2),
    img(page(P["ZF"], O + "c6b.jpg", "N° III", "IX zip hoodie", "BLACK  ·  RED-LINED HOOD", bg=ORN2), 2),
    img(index(FOUR, FOUR_N, O + "c6c.jpg", "INDEX", "the collection", "PICK ONE  ·  I, II, III OR IV", bg=ORN2), 4)],
    texts=[ht("dress code:\nblack. one red detail.", 0.62)])

for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"cat_{k}.json"), "w"), indent=1)
print("\n".join(S))
