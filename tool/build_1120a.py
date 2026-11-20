#!/usr/bin/env python3
"""made 2026-11-20, batch 1120a: 6 new reels for today.
Same rules as 1119a/b: Louboutin only, a new 3-shot mix at real speed in every hook, the red sole ~0.4 s before the
cut, new lines (none used before), quarter zips and zip hoodies, pages re-drawn with vitrine2, seamless loop 12 beats.
From the 11-18..11-19 numbers: the grey hook with only the red (D05) died at 25 % past 3 s -> no keep_red.
All on the F05 grid (99 BPM, drop on the 3.13 s cut); Kirill adds the sound in Instagram.

B01 what she wears to dinner.    SOLES rings -> COUPLE mirrored -> MARBLE           white zip + white QZ
B02 what he wears to meet her.   COUPLE wide mirrored -> NAILS -> SOLES logo        black QZ + black zip
B03 would you wear white?        NAILS mirrored -> SOLES watch -> COUPLE red sole    white QZ + white zip, 4 pages
B04 the walk after dinner.       COUPLE her nails -> SOLES pumps -> NAILS heel lift   zip hoodie pair
B05 which hood is hers?          SOLES hand mirrored -> COUPLE -> MARBLE             black zip | white zip
B06 dinner reservation at nine.  NAILS -> COUPLE shoes close -> SOLES logo           QZ black, white, 2 x 2 of all four"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, HOOD, ARA, ROME, P, O, SP
from vitrine2 import vpage2, vside, vstacked2, vgrid
from build_1119a import gr, sh, couple_red, soles_red, marble_red
import loopreel

OUT = "/mnt/user-data/outputs/ready-2026-11-20a/"


def o(n):
    return O + "b1120_" + n + ".jpg"


def pg(path, beats=1):
    return (beats, img(path, 1))


def nails_heel(n, grade, **kw):
    return sh("NAILS", round(6.0 - n / 30, 3), n, grade, zoom=1.05, crop_x=0.0, crop_y=0.5, **kw)


R = []
g = gr(b=-0.01, c=1.05, s=0.93); g.update(rm=0.03)
R.append(("B01_what-she-wears-to-dinner", "what she wears\nto dinner.",
          [sh("SOLES", 1.3, 34, g, zoom=1.2, crop_x=0.4), sh("COUPLE", 3.3, 40, g, zoom=1.15, flip=True), marble_red(20, g)],
          [pg(vpage2(P["XWF"], o("01a"), "N° I", cat(1, HOOD), "vitrine", scale=0.9, cy=0.47)),
           pg(vpage2(P["WF"], o("01b"), "N° II", cat(2, COLLAR), "vitrine", scale=0.9, cy=0.47)),
           pg(vside(P["XWF"], P["WF"], o("01c"), "N° III", "FIRST LOOK", "vitrine", title="EX MUSEO"), 4)],
          "SOLES rings -> COUPLE mirrored -> MARBLE; white zip hoodie + white QZ, side by side finale"))

g = gr(b=-0.016, c=1.06, s=0.9, g=0.97)
R.append(("B02_what-he-wears-to-meet-her", "what he wears\nto meet her.",
          [sh("COUPLE", 2.6, 36, g, zoom=1.0, crop_y=0.6, flip=True), sh("NAILS", 0.8, 30, g, zoom=1.2), soles_red(28, g, zoom=1.15, crop_y=0.62)],
          [pg(vpage2(P["KF"], o("02a"), "N° I", cat(1, COLLAR), "bronze", scale=0.88)),
           pg(vpage2(P["ZF"], o("02b"), "N° II", cat(2, HOOD), "bronze", scale=0.88)),
           pg(vstacked2(P["KF"], P["ZF"], o("02c"), "N° III", tone="bronze"), 4)],
          "COUPLE wide mirrored -> NAILS -> SOLES logo; black QZ + black zip hoodie, bronze"))

g = gr(b=-0.008, c=1.04, s=0.95, g=1.02); g.update(bs=0.02)
R.append(("B03_would-you-wear-white", "would you\nwear white?",
          [sh("NAILS", 2.4, 34, g, zoom=1.1, flip=True), sh("SOLES", 2.0, 32, g, zoom=1.25, crop_x=0.55), couple_red(g, zoom=1.2, crop_x=0.45, crop_y=0.75)],
          [pg(vpage2(P["WF"], o("03a"), "N° I", cat(1, COLLAR), "smoke", scale=0.9)),
           pg(vpage2(P["XWF"], o("03b"), "N° II", cat(2, HOOD), "smoke", scale=0.9)),
           pg(vpage2(P["WB"], o("03c"), "N° III", cat(3, ARA, ROME), "smoke", scale=0.9)),
           pg(vpage2(P["XWB"], o("03d"), "N° IV", cat(4, ARA, ROME), "smoke", scale=0.9)),
           pg(vside(P["WF"], P["XWF"], o("03e"), "N° V", "FIRST LOOK", "smoke", title="EX MUSEO"), 2)],
          "NAILS mirrored -> SOLES watch -> COUPLE red sole; white QZ + white zip, fronts, backs, side by side"))

g = gr(b=-0.012, c=1.05, s=0.9); g.update(bm=0.02)
R.append(("B04_the-walk-after-dinner", "the walk\nafter dinner.",
          [sh("COUPLE", 0.9, 34, g, zoom=1.25), sh("SOLES", 2.8, 30, g, zoom=1.15), nails_heel(30, g)],
          [pg(vpage2(P["ZPF"], o("04a"), "N° I", cat(1, HOOD), "ink", scale=0.86, spot=(0.5, 0.42, 0.6, 0.34))),
           pg(vpage2(P["ZPB"], o("04b"), "N° II", cat(2, ARA, ROME), "ink", scale=0.86, spot=(0.5, 0.42, 0.6, 0.34))),
           pg(vstacked2(P["ZPF"], P["ZPB"], o("04c"), "N° III", tone="ink"), 4)],
          "COUPLE her nails -> SOLES pumps -> NAILS heel lift; zip hoodie black + white, ink"))

g = gr(b=-0.014, c=1.06, s=0.92); g.update(rm=0.02, rh=0.02)
R.append(("B05_which-hood-is-hers", "which hood\nis hers?",
          [sh("SOLES", 0.7, 30, g, zoom=1.1, flip=True), sh("COUPLE", 1.9, 44, g, zoom=1.1, crop_y=0.62), marble_red(20, g, flip=True)],
          [pg(vside(P["ZF"], P["XWF"], o("05a"), "N° I", cat(1, "HIS  ·  HERS"), "oxblood")),
           pg(vside(P["ZB"], P["XWB"], o("05b"), "N° II", cat(2, ARA, ROME), "oxblood")),
           pg(vstacked2(P["XWF"], P["ZF"], o("05c"), "N° III", tone="oxblood"), 4)],
          "SOLES hand mirrored -> COUPLE -> MARBLE mirrored; black zip | white zip side by side, oxblood"))

g = gr(b=-0.012, c=1.05, s=0.9)
R.append(("B06_dinner-reservation-at-nine", "dinner reservation\nat nine.",
          [sh("NAILS", 1.3, 36, g, zoom=1.0), sh("COUPLE", 3.6, 30, g, zoom=1.3, crop_y=0.85), soles_red(28, g, zoom=1.2, crop_x=0.45)],
          [pg(vpage2(P["KF"], o("06a"), "N° I", cat(1, "BLACK"), "slate", scale=0.9)),
           pg(vpage2(P["WF"], o("06b"), "N° II", cat(2, "WHITE"), "slate", scale=0.9)),
           pg(vgrid([P["KF"], P["WF"], P["ZF"], P["XWF"]], o("06c"), "N° III", "FIRST LOOK", "slate"), 4)],
          "NAILS -> COUPLE shoes close -> SOLES logo; black / white QZ, then all four 2 x 2"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, hook, after, idea) in enumerate(R):
        ledger.append(["1120a", k, "F05 / mr popular", line.replace("\n", " "), idea])
        if only and k[:3] not in only:
            continue
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=45000 + i)
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"b1120_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1120a.json"), "w"), indent=1)
