#!/usr/bin/env python3
"""made 2026-11-26 (morning), batch 1126c: 2 reels on the "bad together." format. Kirill: one with only the black zip
hoodie, one with the zip hoodie and the quarter zip; numbered BT25-BT26 because a parallel chat made BT23-BT24 (1126b, Roman Night hoodie) at the same time;
lines offered first - he picked "dark mode." and "same red. two zips.";
hooks: the couple hook on one, the bright-light hook on the other.

BT25 dark mode.            COUPLE in one take, 1.12x, framed on his side; only the black zip hoodie (front / back), on a
                           new brighter "lamp" glow so the black reads (4 black pages in a row on the usual tones look empty)
BT26 same red. two zips.   bright: his shoes in the flash <-> the marble, alternating; zip hoodie and quarter zip in turn
                           (FULL ZIP / QUARTER ZIP), finale 2 x 2 with the zips on the left and the quarter zips on the right"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, P, O, SP, HOOD, ARA, ROME
import vitrine as V
from vitrine2 import vpage2, vside, vstacked2, vgrid
from build_1119a import gr, sh, couple_red
import loopreel

V.TONES["lamp"] = ((92, 86, 78), (5, 5, 5))     # a warm museum lamp, brighter than vitrine: for all-black pages
OUT = "/mnt/user-data/outputs/ready-2026-11-26c/"
NUMS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]


def o(name):
    return O + "bt1126c_" + name + ".jpg"


def pages(tag, items, tone, cy=0.47):
    """items: (mockup key, catalogue label, place, scale, spot) -> one page per half beat"""
    return [(0.5, img(vpage2(P[k], o(f"{tag}{j}"), "N° " + NUMS[j], cat(j + 1, lab, place), tone, scale=sc, cy=cy,
                             spot=sp), 1)) for j, (k, lab, place, sc, sp) in enumerate(items)]


def fin(path, beats):
    return (beats, img(path, 1))


PRG = "PRAGUE, MMXXVI"
R = []

# BT25 dark mode. - COUPLE in one take (his side, 1.12x); black zip only: front / back / front up close / back up close,
# front | back side by side, front over back; lamp
g = gr(b=-0.02, c=1.08, s=0.88)
R.append(("BT25_dark-mode", "dark mode.",
          [couple_red(g, speed=1.12, zoom=1.2, crop_x=0.6, crop_y=0.58)],
          pages("25", [("ZF", HOOD, PRG, 0.9, None), ("ZB", ARA, ROME, 0.9, None),
                       ("ZF", HOOD, PRG, 1.05, (0.5, 0.36, 0.5, 0.3)), ("ZB", ARA, ROME, 1.05, (0.5, 0.44, 0.55, 0.32))],
                "lamp") +
          [fin(vside(P["ZF"], P["ZB"], o("25s"), "N° V", cat(5, HOOD), "lamp"), 1),
           fin(vstacked2(P["ZF"], P["ZB"], o("25f"), "N° VI", tone="lamp"), 3)],
          "COUPLE one take 1.12x on his side; black zip hoodie only (front / back / close-ups / side by side / stacked), lamp glow"))

# BT26 same red. two zips. - bright: shoes in the flash -> marble -> shoes close -> red heel wide; zip and QZ in turn
gb = gr(b=0.02, c=1.06, s=0.86, g=1.05)
R.append(("BT26_same-red-two-zips", "same red.\ntwo zips.",
          [sh("COUPLE", 1.35, 39, gb, zoom=1.15, crop_x=0.5, crop_y=0.6), sh("MARBLE", 0.0, 19, gb, zoom=1.2, crop_y=0.5, flip=True),
           sh("COUPLE", 2.0, 18, gb, zoom=1.4, crop_x=0.5, crop_y=0.62), sh("MARBLE", 0.49, 18, gb, zoom=1.1, crop_y=0.5)],
          pages("26", [("ZF", "FULL ZIP  ·  BLACK", PRG, 0.9, None), ("KF", "QUARTER ZIP  ·  BLACK", PRG, 0.9, None),
                       ("XWF", "FULL ZIP  ·  WHITE", PRG, 0.9, None), ("WF", "QUARTER ZIP  ·  WHITE", PRG, 0.9, None),
                       ("ZB", "FULL ZIP  ·  BLACK", PRG, 0.9, None), ("KB", "QUARTER ZIP  ·  BLACK", PRG, 0.9, None)],
                "lamp") +
          [fin(vgrid([P["ZF"], P["KF"], P["XWF"], P["WF"]], o("26f"), "N° VII", "FIRST LOOK", "lamp"), 3)],
          "bright: COUPLE shoes in the flash -> MARBLE mirrored -> shoes close -> red heel wide; zip / QZ in turn, lamp; 2 x 2 zips | QZ"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, hook, after, idea) in enumerate(R):
        ledger.append(["1126c", k, "bad together track (99 BPM grid)", line.replace("\n", " "), idea])
        if only and k.split("_")[0] not in only:
            continue
        assert abs(sum(b for b, _ in after) - 6) < 1e-6, k
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=52000 + i)
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"bt1126c_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1126c.json"), "w"), indent=1)
