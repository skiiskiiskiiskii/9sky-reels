#!/usr/bin/env python3
"""2026-11-01: 8 reels with hooks cut from Kirill's own Oct 4 shoot (~/Downloads/исходники, 4K 60p, cut to
1080x1920 proxies in _разбор/hooks_src). Rule (Kirill 11-01): the IX hoodie must not appear in the hook, so every
cut ends before the hoodie shows (booth: on the closed red curtain; jacket: before she opens it; fur: on the
lens-cover blackout; walk: before she turns to camera)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, pages, fin_path, cat, COLLAR, HOOD, IX, ARA, ROME, SP

S_ = "/mnt/user-data/uploads/Downloads/исходники/_разбор/hooks_src/"
GR = dict(c=1.03, s=0.95, b=-0.01)


def shot(name, start, speed=1.0, zoom=1.0, crop_y=0.5):
    return dict(type="clip", src=S_ + name + ".mp4", start=start, until="drop", align_red=False, speed=speed,
                zoom=zoom, crop_x=0.5, crop_y=crop_y, flip=False, grade=GR)


def t(text, y=0.76):
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

R = [  # key, hook, texts, pages, finale
    ("S01_behind-the-curtain", shot("s12_0", 0.62), t("what's behind\nthe red curtain?", 0.80), QW2, QF),
    ("S02_only-where-its-red", shot("s11_5.5", 1.7), t("she only goes\nwhere it's red.", 0.80), ZH, ZFIN),
    ("S03_under-the-jacket", shot("s22_0", 0.0, speed=0.95), t("guess what's\nunder the jacket.", 0.80), QW1, QF),
    ("S04_she-turned-around", shot("s21_0", 0.0, speed=0.75), t("she turned around\nfor the collar.", 0.78), QW3, QF),
    ("S05_come-closer", shot("s13_5.5", 0.52), t("come closer.", 0.80), QK, QF),
    ("S06_under-the-fur", shot("s14_3.5", 2.45), t("what she wears\nunder the fur.", 0.80), SW, SFIN),
    ("S07_red-stairs", shot("s1_0", 0.3), t("dress code:\nblack, with red.", 0.62), QW2, QF),
    ("S08_hood-up", shot("s23_17", 1.25), t("hood up.\nprague after dark.", 0.80), ZHB, ZFIN),
]
for i, (k, hook, texts, pg, fin) in enumerate(R):
    tag = f"s{i + 1:02d}"
    spec = dict(seed=15000 + i, segments=[hook] + pages(pg, None, tag, 2) +
                [img(fin_path(fin[0], fin[1], tag, "N° III" if len(pg) == 2 else "N° IV"), 4)], texts=texts)
    json.dump(spec, open(os.path.join(SP, f"s1101_{k}.json"), "w"), indent=1)
    print(f"s1101_{k}")
