#!/usr/bin/env python3
"""2026-11-16, batch 1116a. Posted today (5): R01, R05, R02, R03, R06. R04 (painting) and N06 (rose/curtain) were
swapped out by Kirill for louboutin hooks and stay in reserve.
Scales the 11-15 winner K05 "his in black. hers in white." (16.7K, 66 shares, 67% past 3 s) in different wrappers.
New rule from 11-15: max 5 trials a day, and each hook clip at most once a day (COUPLE, MARBLE+SOLES, NAILS,
the painting, the curtain are all different here).

R01 she picked white. he kept black. - COUPLE wide (the K05 crop, unchanged), her white page first, pair finale
R02 matching, but not the same.     - MARBLE (his shoe + her red soles) -> SOLES logo sole; backs, pair finale
R03 her red is hidden. his isn't.   - NAILS alone: black nails -> red under the nails -> red sole; black quarter zip
R04 his and hers, around 1440.      - NEW painting: Fra Filippo Lippi, Portrait of a Woman with a Man at a Casement
                                      (Met, CC0, ca. 1440, probably an engagement portrait); push-in onto both faces;
                                      zip hoodie black for him / white for her (painting, not louboutin, so the zip is fine)
Same F05 timing (mrpopular), post with the F05 audio."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, HOOD, ARA, ROME, SP, P, O
from build_1115 import lb, clip, t, MARBLE_LEN, DROP, build as build1115
import paintclip

HERE = os.path.dirname(os.path.abspath(__file__))
LIPPI = os.path.join(HERE, "..", "out", "hooks", "paint_lippi_in.mp4")
if not os.path.exists(LIPPI):   # whole painting on the wall -> eased push-in that ends with both profiles in frame
    paintclip.make("/mnt/user-data/uploads/9sky-reels/hooks/art-met/9sky_art_m2_02.jpg", LIPPI, 400, 560,
                   dur=3.4, w0=900, z1=1.9, y0=1060, y1=1010, ease="in")

HIS, HERS = "HIS  ·  BLACK", "HERS  ·  WHITE"
R = [  # key, tone, hook, texts, pages, finale, idea
    ("R01_she-picked-white", "oxblood",
     [lb("COUPLE", speed=1.12, zoom=1.0, crop_y=0.6)],
     t("she picked white.\nhe kept black."),
     [("WF", cat(1, HERS)), ("KF", cat(2, HIS))], ("PF", "PB"),
     "K05 winner scaled: the same COUPLE wide hook, new line, her white page first, pair finale"),
    ("R02_matching-not-the-same", "slate",
     [clip(P["MARBLE"], start=0.0, dur=MARBLE_LEN),
      lb("SOLES", start=4.3 - (DROP - MARBLE_LEN - 0.42), speed=1.0, zoom=1.1, crop_y=0.6)],
     t("matching,\nbut not the same."),
     [("KB", cat(1, HIS)), ("WB", cat(2, HERS))], ("PF", "PB"),
     "K05 winner scaled: MARBLE (his black shoe + her red soles) -> SOLES logo sole; backs, pair finale"),
    ("R03_her-red-is-hidden", "vitrine",
     [lb("NAILS", start=6.1 - DROP, speed=1.0, zoom=1.15, crop_y=0.55)],
     t("her red is hidden.\nhis isn't."),
     [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))], ("KF", "KB"),
     "his/hers line on NAILS alone: black nails, red under the nails, red sole at the cut; black quarter zip"),
    ("R04_his-and-hers-1440", "vitrine",
     [clip(LIPPI, grade={})],
     t("his and hers,\naround 1440."),
     [("ZF", cat(1, "HIS  ·  BLACK  ·  RED-LINED HOOD")), ("XWF", cat(2, HERS))], ("ZPF", "ZPB"),
     "NEW painting hook (Lippi double portrait ca. 1440, engagement) -> zip hoodie black for him, white for her"),
    # 11-16 Kirill: swap the 2nd (painting) and 5th (rose/curtain) of today for louboutin hooks. All clean louboutin
    # clips are already in R01-R03, so these use the parts of COUPLE/SOLES nobody saw today (overlap <0.5 s).
    ("R05_when-she-walks-away", "vitrine",
     [lb("SOLES", start=4.30, speed=1.0, zoom=1.1, crop_y=0.6)],
     t("you only see her red\nwhen she walks away."),
     [("WF", cat(1, HERS)), ("WB", cat(2, ARA, ROME))], ("WF", "WB"),
     "red from the first frame: SOLES after the logo (4.3-7.4 s, unused today); her white quarter zip"),
    ("R06_her-nails-match-her-soles", "slate",
     [lb("COUPLE", start=0.0, dur=1.5, speed=1.0, zoom=1.0, crop_y=0.6),
      lb("COUPLE", start=4.75, speed=1.0, zoom=1.0, crop_y=0.6)],
     t("her nails match\nher soles."),
     [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))], ("KF", "KB"),
     "COUPLE parts unused today: her red-tipped nails (0-1.5 s) -> her red soles walking (4.75-6.4 s); black quarter zip"),
]

if __name__ == "__main__":
    build1115("1116a", R, "r1116", 33000, tag_letter="r")
