#!/usr/bin/env python3
"""made 2026-11-17, batch 1117c: 4 Louboutin reels replacing U05-U08 (Kirill: drop rose and curtain for now, he has a new idea
for them; use Louboutin, mix the shots, vary the mockup pages a little). Louboutin only with the quarter zip.
Clips mixed in new orders (SOLES->COUPLE, NAILS->SOLES, MARBLE->COUPLE, COUPLE nails->NAILS heel); mockups: back first,
white/black mixes, other tones, other finale pairs. F05 timing, post with the F05 audio. Lines: plain, 2-5 words.
V01 her heels. his shoes.  V02 nails, then soles.  V03 his shoes. her soles.  V04 her nails. her heels."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import cat, COLLAR, ARA, ROME, P
from build_1115 import lb, clip, t, build, MARBLE_LEN

V = [
    ("V01_her-heels-his-shoes", "vitrine",
     [lb("SOLES", start=0.0, dur=1.4, speed=1.0, zoom=1.1, crop_y=0.6),
      lb("COUPLE", speed=1.12, zoom=1.2, crop_x=0.45, crop_y=0.7)],
     t("her heels.\nhis shoes."), [("KB", cat(1, ARA, ROME)), ("KF", cat(2, COLLAR))], ("PF", "PB"),
     "SOLES (pumps, watch) -> COUPLE his shoes -> her red sole; pages back first, black quarter zip, pair finale"),
    ("V02_nails-then-soles", "oxblood",
     [lb("NAILS", start=1.6, dur=1.3, speed=1.1, zoom=1.0),
      lb("SOLES", start=2.31, speed=1.3, zoom=1.15, crop_y=0.6)],
     t("nails,\nthen soles."), [("WF", cat(1, COLLAR)), ("WB", cat(2, ARA, ROME))], ("PF", "PB"),
     "NAILS red nails -> SOLES logo sole; white quarter zip pages, pair finale, oxblood"),
    ("V03_his-shoes-her-soles", "slate",
     [clip(P["MARBLE"], start=0.0, dur=round(MARBLE_LEN / 0.7, 3), speed=0.7, flip=True, smooth=True),
      lb("COUPLE", speed=1.12, zoom=1.2, crop_x=0.4, crop_y=0.75, flip=True)],
     t("his shoes.\nher soles."), [("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR"))], ("PF", "PB"),
     "MARBLE mirrored 0.7x -> COUPLE mirrored; black front then white front, pair finale, slate"),
    ("V04_her-nails-her-heels", "vitrine",
     [lb("COUPLE", start=0.2, dur=1.2, speed=1.0, zoom=1.15, crop_y=0.6),
      lb("NAILS", start=round(5.935 - 1.93 * 0.7, 3), speed=0.7, smooth=True, zoom=1.15, crop_y=0.55)],
     t("her nails.\nher heels."), [("WB", cat(1, ARA, ROME)), ("KF", cat(2, COLLAR))], ("KF", "KB"),
     "COUPLE nails -> NAILS red heel lifts; white back then black front, black finale"),
]

if __name__ == "__main__":
    build("1117c", V, "v1117", 36000, tag_letter="v")
