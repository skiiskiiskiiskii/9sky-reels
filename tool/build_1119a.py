#!/usr/bin/env python3
"""made 2026-11-19, batch 1119a: 9 reels. Kirill: Instagram should not see them as the same - mix the pieces, new text,
slightly changed mockup frames; same aura and aesthetic, from a slightly different side.

What changes reel to reel (so no two share a fingerprint with each other or with the ~80 reels before):
- hook: a new 3-shot Louboutin mix each time (COUPLE / SOLES / NAILS / MARBLE), real speed, new windows, crops,
  mirroring; three different endings for the red (COUPLE sole, SOLES logo sole, NAILS heel lift, MARBLE heel);
  a small grade shift per reel; D05 keeps only the red (rest grey);
- line: 5 about the place / the evening, 4 questions, line height varies a little;
- pages (tool/vitrine2.py): new tones (ink, bronze, smoke) next to vitrine / oxblood / slate, garment scale and
  height, glow from above or off-centre, side-by-side pages (his | hers, front | back), different finales;
- sound: 6 reels on the F05 grid (Cyn - North Pole / mr popular, 99 BPM), 3 on LV Sandals (95 BPM, from 0:09.5).
All loop seamlessly (12 beats)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, HOOD, ARA, ROME, P, O, SP
import vitrine2 as V2
from vitrine2 import vpage2, vside, vstacked2
import loopreel

OUT = "/mnt/user-data/outputs/ready-2026-11-19a/"
F05, LV = 60 / 99.0, 0.632
BOTH = "RED COLLAR, RED-LINED HOOD"


def gr(b=-0.012, c=1.04, s=0.92, g=1.0):
    return dict(b=b, c=c, s=s, g=g)


def sh(key, start, n, grade, **kw):
    d = dict(type="clip", src=P[key], start=start, align_red=False, speed=1.0, zoom=1.15, crop_x=0.5,
             crop_y=0.6, flip=False, grade=grade, n=n)
    d.update(kw)
    return d


def couple_red(grade, **kw):                      # COUPLE: her red sole lands 0.42 s before the cut
    d = dict(type="clip", src=P["COUPLE"], speed=1.0, zoom=1.2, crop_x=0.45, crop_y=0.75, flip=False, grade=grade,
             align_red=True, lead=0.42)
    d.update(kw)
    return d


def soles_red(n, grade, **kw):                    # SOLES logo sole at ~4.3 s
    return sh("SOLES", round(4.72 - n / 30, 3), n, grade, **kw)


def nails_red(n, grade, **kw):                    # NAILS: her heel lifts, red at ~5.7 s
    return sh("NAILS", round(5.95 - n / 30, 3), n, grade, **kw)


def marble_red(n, grade, **kw):                   # MARBLE is red all through, keep it short and last
    return sh("MARBLE", round(1.09 - n / 30, 3), n, grade, zoom=1.1, crop_y=0.5, **kw)


def pg(path, beats=1):
    return (beats, img(path, 1))


def o(name):
    return O + "d1119_" + name + ".jpg"


R = []   # key, line, y, beat, hook, after, idea, track

# D01 tonight, in prague. - black QZ + black zip together, bronze, garment a bit smaller and higher
g1 = gr(b=-0.016, c=1.06, s=0.9, g=0.97)
R.append(("D01_tonight-in-prague", "tonight,\nin prague.", 0.22, F05,
          [sh("COUPLE", 1.8, 34, g1, zoom=1.0, flip=True), sh("NAILS", 2.0, 32, g1, zoom=1.05), soles_red(28, g1, zoom=1.2, crop_y=0.62)],
          [pg(vpage2(P["KKF"], o("01a"), "N° I", cat(1, BOTH), "bronze", scale=0.82, cy=0.45)),
           pg(vpage2(P["KKB"], o("01b"), "N° II", cat(2, ARA, ROME), "bronze", scale=0.82, cy=0.45)),
           pg(vstacked2(P["KF"], P["ZF"], o("01c"), "N° III", tone="bronze"), 4)],
          "COUPLE wide mirrored -> NAILS -> SOLES logo sole; black QZ + black zip hoodie; bronze, smaller garment", "F05"))

# D02 a late table for two. - his | hers side by side, ink
g2 = gr(b=-0.01, c=1.03, s=0.86)
R.append(("D02_a-late-table-for-two", "a late table\nfor two.", 0.24, LV,
          [sh("SOLES", 0.8, 34, g2, zoom=1.25, crop_x=0.4), sh("COUPLE", 3.2, 40, g2, zoom=1.2, crop_y=0.8), marble_red(20, g2)],
          [pg(vside(P["KF"], P["WF"], o("02a"), "N° I", cat(1, "HIS  ·  HERS"), "ink")),
           pg(vside(P["KB"], P["WB"], o("02b"), "N° II", cat(2, ARA, ROME), "ink")),
           pg(vstacked2(P["PF"], P["PB"], o("02c"), "N° III", tone="ink"), 4)],
          "SOLES rings -> COUPLE his shoes -> MARBLE heel; his | hers side by side, ink; LV Sandals", "LV"))

# D03 after the gallery opening. - white zip hoodie, bigger, light from above, smoke
g3 = gr(b=-0.008, c=1.05, s=0.95, g=1.02)
R.append(("D03_after-the-gallery-opening", "after the\ngallery opening.", 0.2, F05,
          [sh("NAILS", 0.9, 36, g3, zoom=1.0), sh("SOLES", 2.6, 30, g3, zoom=1.15), couple_red(g3, zoom=1.15, crop_x=0.4)],
          [pg(vpage2(P["XWF"], o("03a"), "N° I", cat(1, HOOD), "smoke", scale=1.0, cy=0.48, spot=(0.5, 0.36, 0.55, 0.32))),
           pg(vpage2(P["XWB"], o("03b"), "N° II", cat(2, ARA, ROME), "smoke", scale=1.0, cy=0.48, spot=(0.5, 0.36, 0.55, 0.32))),
           pg(vstacked2(P["XWF"], P["XWB"], o("03c"), "N° III", tone="smoke"), 4)],
          "NAILS -> SOLES pumps -> COUPLE red sole; white zip hoodie, light from above, smoke", "F05"))

# D04 the long way home. - black zip hoodie, oxblood glow off-centre, front | back finale
g4 = gr(b=-0.02, c=1.07, s=0.9, g=0.96)
R.append(("D04_the-long-way-home", "the long\nway home.", 0.22, F05,
          [sh("COUPLE", 0.7, 36, g4, zoom=1.2), sh("SOLES", 1.9, 30, g4, zoom=1.1, flip=True), sh("NAILS", round(6.0 - 28 / 30, 3), 28, g4, zoom=1.05, crop_x=0.0, crop_y=0.5)],
          [pg(vpage2(P["ZF"], o("04a"), "N° I", cat(1, HOOD), "oxblood", scale=0.88, spot=(0.42, 0.44, 0.6, 0.34))),
           pg(vpage2(P["ZB"], o("04b"), "N° II", cat(2, ARA, ROME), "oxblood", scale=0.88, spot=(0.58, 0.44, 0.6, 0.34))),
           pg(vside(P["ZF"], P["ZB"], o("04c"), "N° III", "FIRST LOOK", "oxblood", title="EX MUSEO"), 4)],
          "COUPLE her nails -> SOLES watch mirrored -> NAILS heel lift (new ending); black zip hoodie, glow off-centre", "F05"))

# D05 which one is his? - only the red keeps its colour; black / white QZ, slate
g5 = gr(b=-0.01, c=1.08, s=1.0)
R.append(("D05_which-one-is-his", "which one\nis his?", 0.22, LV,
          [sh("SOLES", 2.4, 34, g5, zoom=1.15, keep_red=True), sh("NAILS", 1.4, 30, g5, zoom=1.0, keep_red=True),
           couple_red(g5, zoom=1.0, crop_y=0.6, keep_red=True)],
          [pg(vpage2(P["KF"], o("05a"), "N° I", cat(1, "BLACK"), "slate", scale=0.86)),
           pg(vpage2(P["WF"], o("05b"), "N° II", cat(2, "WHITE"), "slate", scale=0.86)),
           pg(vstacked2(P["PF"], P["PB"], o("05c"), "N° III", tone="slate"), 4)],
          "grey hook, only the red keeps its colour: SOLES pumps -> NAILS -> COUPLE wide red sole; black / white QZ; LV Sandals", "LV"))

# D06 dinner or the opera? - white QZ + white zip side by side, vitrine, garment lower
g6 = gr(b=-0.012, c=1.04, s=0.95, g=1.03)
R.append(("D06_dinner-or-the-opera", "dinner\nor the opera?", 0.24, F05,
          [sh("COUPLE", 2.2, 40, g6, zoom=1.0, crop_y=0.6), sh("SOLES", 0.6, 34, g6, zoom=1.2, crop_x=0.55), marble_red(20, g6, flip=True)],
          [pg(vpage2(P["WF"], o("06a"), "N° I", cat(1, COLLAR), "vitrine", scale=0.95, cy=0.5)),
           pg(vpage2(P["WB"], o("06b"), "N° II", cat(2, ARA, ROME), "vitrine", scale=0.95, cy=0.5)),
           pg(vside(P["WF"], P["XWF"], o("06c"), "N° III", "FIRST LOOK", "vitrine", title="EX MUSEO"), 4)],
          "COUPLE wide -> SOLES rings -> MARBLE mirrored; white QZ, white QZ | white zip finale", "F05"))

# D07 first date in prague. - zip hoodie pair, ink, smaller
g7 = gr(b=-0.014, c=1.05, s=0.88, g=0.98)
R.append(("D07_first-date-in-prague", "first date\nin prague.", 0.22, F05,
          [sh("SOLES", 0.5, 30, g7, zoom=1.1, flip=True), sh("NAILS", 2.6, 36, g7, zoom=1.1, crop_x=0.45), couple_red(g7, zoom=1.0, crop_y=0.6)],
          [pg(vpage2(P["ZPF"], o("07a"), "N° I", cat(1, HOOD), "ink", scale=0.84)),
           pg(vpage2(P["ZPB"], o("07b"), "N° II", cat(2, ARA, ROME), "ink", scale=0.84)),
           pg(vstacked2(P["ZPF"], P["ZPB"], o("07c"), "N° III", tone="ink"), 4)],
          "SOLES hand mirrored -> NAILS -> COUPLE wide red sole; zip hoodie black + white, ink", "F05"))

# D08 would you match with him? - his black QZ | her white zip, bronze
g8 = gr(b=-0.01, c=1.05, s=0.93)
R.append(("D08_would-you-match-with-him", "would you\nmatch with him?", 0.22, LV,
          [sh("COUPLE", 3.0, 36, g8, zoom=1.15, crop_y=0.7), sh("NAILS", 0.7, 30, g8, zoom=1.0, flip=True), soles_red(28, g8, zoom=1.1)],
          [pg(vpage2(P["KF"], o("08a"), "N° I", cat(1, "HIS  ·  BLACK"), "bronze", scale=0.9, spot=(0.5, 0.42, 0.58, 0.34))),
           pg(vpage2(P["XWF"], o("08b"), "N° II", cat(2, "HERS  ·  WHITE"), "bronze", scale=0.9, spot=(0.5, 0.42, 0.58, 0.34))),
           pg(vside(P["KF"], P["XWF"], o("08c"), "N° III", "FIRST LOOK", "bronze", title="EX MUSEO"), 4)],
          "COUPLE his shoes -> NAILS mirrored -> SOLES logo sole; his black QZ | her white zip hoodie; LV Sandals", "LV"))

# D09 the shoes or the collar? - black QZ, smoke, front | back side by side as the second page
g9 = gr(b=-0.016, c=1.06, s=0.9)
R.append(("D09_the-shoes-or-the-collar", "the shoes\nor the collar?", 0.2, F05,
          [sh("NAILS", 1.6, 30, g9, zoom=1.0), sh("COUPLE", 1.0, 44, g9, zoom=1.15, crop_y=0.62), marble_red(20, g9)],
          [pg(vpage2(P["KF"], o("09a"), "N° I", cat(1, COLLAR), "smoke", scale=0.92, cy=0.46)),
           pg(vside(P["KF"], P["KB"], o("09b"), "N° II", cat(2, ARA, ROME), "smoke")),
           pg(vstacked2(P["KF"], P["KB"], o("09c"), "N° III", tone="smoke"), 4)],
          "NAILS -> COUPLE her nails -> MARBLE heel; black QZ, front | back side by side, smoke", "F05"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, y, beat, hook, after, idea, track) in enumerate(R):
        ledger.append(["1119a", k, track, line.replace("\n", " "), idea])
        if only and k[:3] not in only:
            continue
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, y=y, seed=42000 + i, beat=beat, total_beats=12)
        json.dump(dict(hook=hook, line=line, after=after, beat=beat, track=track),
                  open(os.path.join(SP, f"d1119_{k}.json"), "w"), indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1119a.json"), "w"), indent=1)
