#!/usr/bin/env python3
"""2026-10-31 (evening): 16 reels.
A  - 7 rose POV hooks with their own lines (not the Louboutin lines): two-step text, the second line lands
     ~1.5 s in, so the rose sets up the line and the collar/hood answers it.
L  - 3 Louboutin hooks, quarter zip only (Kirill 10-30), short red flash.
K  - 6 rose reels on Kirill's own lines: my color. / small "red" beside the rose / you're red to my black. /
     black and red >> / if love was a color. / favourite color.
Rose hooks: Kirill's ready 9:16 cuts in ~/Downloads/flowers hooks (g1 night grass, g2 top-down asphalt, g3 walk)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, pages, fin_path, cat, COLLAR, HOOD, IX, ARA, ROME, SP, P

G = "/mnt/user-data/uploads/flowers hooks/"


def rose(name, flip=False):
    return dict(type="clip", src=G + name + ".mp4", start=0.0, until="drop", align_red=False, speed=1.0,
                zoom=1.0, crop_x=0.5, flip=flip, grade={})


def lb(key, flip, crop_x, lead, speed=0.95, zoom=1.035):
    return dict(type="clip", src=P[key], until="drop", align_red=True, speed=speed, zoom=zoom, crop_x=crop_x,
                flip=flip, lead=lead, grade=dict(c=1.04, s=0.92, b=-0.012))


def t(text, y, frm=0, size=96, x=0.5, scrim=0.4):
    return {"text": text, "from": frm, "to": "drop", "y": y, "x": x, "size": size, "scrim": scrim, "font": "cg-italic"}


def two(a, b, y, at=1.5):
    """first line from the start, second joins at `at` seconds just below it"""
    return [t(a, y), t(b, y + 0.055, frm=at, scrim=0)]   # no second band: it would dim line one


KNIT = "BLACK KNIT"
QW1 = [("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))]
QW2 = [("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR")), ("PF", cat(3, "BLACK  ·  WHITE"))]
QW3 = [("PF", cat(1, COLLAR)), ("KF", cat(2, IX))]
QK = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
ZH = [("ZF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))]
ZHB = [("XWF", cat(1, HOOD)), ("ZB", cat(2, ARA, ROME)), ("ZPF", cat(3, "BLACK  ·  WHITE"))]
SW = [("KF", cat(1, COLLAR)), ("SWF", cat(2, KNIT)), ("SPF", cat(3, "ALL BLACK  ·  ONE RED"))]
BR = [("KF", cat(1, COLLAR)), ("ZF", cat(2, HOOD)), ("SPF", cat(3, "BLACK  ·  RED"))]
QF, ZFIN, SFIN = ("PF", "PB"), ("ZPF", "ZPB"), ("SPF", "SPB")

R = {  # batch -> [(key, hook, texts, pages, finale)]
    "a": [
        ("A01_roses-are-red", rose("g1"), two("roses are red.", "so is the collar.", 0.77), QW2, QF),
        ("A02_he-brought-a-rose", rose("g2"), two("he brought a rose.", "she noticed the collar.", 0.75), QW1, QF),
        ("A03_first-date-rule", rose("g3"), two("first date rule:", "one red thing.", 0.74, at=1.3), ZH, ZFIN),
        ("A04_flowers-die", rose("g1", flip=True), two("flowers die.", "the collar stays.", 0.77), QK, QF),
        ("A05_match-the-rose", rose("g2", flip=True), two("the rose is red.", "so is the hood.", 0.75), ZHB, ZFIN),
        ("A06_black-everything", rose("g3", flip=True), two("black everything.", "one rose.", 0.74, at=1.3), SW, SFIN),
        ("A07_dress-code", rose("g2"), two("date night dress code:", "black, one red detail.", 0.75), QW3, QF),
        ("L01_collar-says-it-all", lb("COUPLE", True, 0.5, 0.42), [t("the collar says it all.", 0.40, scrim=0.5)], QW1, QF),
        ("L02_black-or-white", lb("STREET", False, 0.5, 0.42), [t("black or white?", 0.40, scrim=0.5)], QW2, QF),
        ("L03_what-to-wear-museum", dict(lb("NAILS", True, 0.5, 0.4), start=3.5, align_red=False),
         [t("what to wear\nto the museum.", 0.40, scrim=0.5)], QW3, QF),
    ],
    "k": [
        ("K01_my-color", rose("g1"), [t("my color.", 0.80)], QW1, QF),
        ("K02_red", rose("g2"), [t("red", 0.235, size=60, x=0.585, scrim=0)], QW3, QF),
        ("K03_red-to-my-black", rose("g1", flip=True), [t("you're red\nto my black.", 0.79)], QW2, QF),
        ("K04_black-and-red", rose("g2", flip=True), [t("black and red >>", 0.77)], BR, SFIN),
        ("K05_if-love-was-a-color", rose("g3"), [t("if love was a color.", 0.76)], ZH, ZFIN),
        ("K06_favourite-color", rose("g3", flip=True), [t("favourite color.", 0.76)], SW, SFIN),
    ],
}
for batch, rows in R.items():
    for i, (k, hook, texts, pg, fin) in enumerate(rows):
        tag = f"{batch}{i + 1:02d}"
        spec = dict(seed=14000 + 100 * (batch == "k") + i, segments=[hook] + pages(pg, None, tag, 2) +
                    [img(fin_path(fin[0], fin[1], tag, "N° III" if len(pg) == 2 else "N° IV"), 4)], texts=texts)
        json.dump(spec, open(os.path.join(SP, f"{batch}1031_{k}.json"), "w"), indent=1)
        print(f"{batch}1031_{k}")
