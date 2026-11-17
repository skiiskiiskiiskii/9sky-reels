#!/usr/bin/env python3
"""made 2026-11-17, batch 1117b: 8 new reels for today (Kirill: "8 new reels"; the daily limit of 5 trials is dropped,
he checked it and it does not hold). Hooks not named -> half Louboutin, half roses/red (no rose -> Louboutin, it failed twice).
Lines: 2-5 plain words that describe what is on screen (Kirill's 11-16 rule). New clip windows, no line repeated from 11-15..11-17.
Products: black/white IX quarter zip and IX zip hoodie only. F05 timing (mrpopular), post with the F05 audio.

U01 her nails. his shoes.            - COUPLE 0.2-1.5 (her black nails, red tips) -> his shoes -> her red sole; black quarter zip
U02 red nails, red soles.            - SOLES from the start (pumps, gold watch, red nails) -> the logo sole; white quarter zip
U03 red heel on marble.              - MARBLE (1.1 s) slowed to the full hook, red heel lifts; black quarter zip, pair finale
U04 he wears black. she wears red.   - the K05 hook (COUPLE wide, 16.7K) with a new line; his black / her white quarter zip, pair finale
U05 red rose. red hood.              - rose g1 (top of frame, line lowered); b+w zip hoodie pair
U06 he brought a rose.               - rose g2 (asphalt, black legs); white quarter zip
U07 bring the rose. wear the red.    - rose g3 (walk on tiles), 0.92x; white zip hoodie
U08 step behind the red curtain.     - red curtain fabric (own shoot, 3.95-5.35 at 0.45x, no person); black quarter zip, slate"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import cat, COLLAR, HOOD, ARA, ROME, P
from build_1115 import lb, clip, t, build, MARBLE_LEN, ROSE, SHOOT

HIS, HERS = "HIS  ·  BLACK", "HERS  ·  WHITE"
QB = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
QW = [("WF", cat(1, COLLAR)), ("WB", cat(2, ARA, ROME))]
MS = 0.352                                           # MARBLE slow-down: 1.10 s of footage fills 3.125 s

U = [  # key, tone, hook, texts, pages, finale, idea
    ("U01_her-nails-his-shoes", "vitrine",
     [lb("COUPLE", start=0.2, dur=1.3, speed=1.0, zoom=1.15, crop_y=0.6),
      lb("COUPLE", speed=1.12, zoom=1.15, crop_y=0.7)],
     t("her nails.\nhis shoes."), QB, ("KF", "KB"),
     "COUPLE first 1.5 s (never shown before: her nails) -> his shoes -> her red sole"),
    ("U02_red-nails-red-soles", "slate",
     [lb("SOLES", start=0.78, speed=1.3, zoom=1.1, crop_y=0.6)],
     t("red nails,\nred soles."), QW, ("WF", "WB"),
     "SOLES from the start (pumps, watch, red nails) -> logo sole; white quarter zip"),
    ("U03_red-heel-on-marble", "oxblood",
     [clip(P["MARBLE"], start=0.0, dur=round(MARBLE_LEN / MS, 3), speed=MS, smooth=True, grade=dict(c=1.04, s=0.92, b=-0.012))],
     t("red heel\non marble."), QB, ("PF", "PB"),
     "MARBLE slowed 0.35x to the whole hook (his black shoe, her red heel lifts); pair finale"),
    ("U04_he-wears-black-she-wears-red", "vitrine",
     [lb("COUPLE", speed=1.12, zoom=1.0, crop_y=0.6)],
     t("he wears black.\nshe wears red."),
     [("KF", cat(1, HIS)), ("WF", cat(2, HERS))], ("PF", "PB"),
     "K05 hook (16.7K) unchanged, new line; his black / her white quarter zip, pair finale"),
    ("U05_red-rose-red-hood", "slate",
     [clip(ROSE + "g1.mp4", start=0.3, zoom=1.15, crop_y=0.3, grade={})],
     t("red rose.\nred hood.", y=0.52), [("ZPF", cat(1, HOOD)), ("ZPB", cat(2, ARA, ROME))], ("ZPF", "ZPB"),
     "rose g1 alone, black + white zip hoodie pair (red-lined hood)"),
    ("U06_he-brought-a-rose", "vitrine",
     [clip(ROSE + "g2.mp4", start=0.3, zoom=1.1, crop_y=0.0, grade={})],
     t("he brought\na rose.", y=0.72), QW, ("WF", "WB"),
     "rose g2 alone (rose + black legs on asphalt); white quarter zip"),
    ("U07_bring-the-rose-wear-the-red", "oxblood",
     [clip(ROSE + "g3.mp4", start=0.0, speed=0.92, zoom=1.08, crop_y=0.3, grade={})],
     t("bring the rose.\nwear the red.", y=0.56), [("XWF", cat(1, HOOD)), ("XWB", cat(2, ARA, ROME))], ("XWF", "XWB"),
     "rose g3 (walk on tiles) alone; white zip hoodie"),
    ("U08_step-behind-the-red-curtain", "slate",
     [clip(SHOOT + "s12_0.mp4", start=3.95, speed=0.45, smooth=True, grade={})],
     t("step behind\nthe red curtain."), QB, ("KF", "KB"),
     "red curtain fabric only (no person), slowed 0.45x; black quarter zip"),
]

if __name__ == "__main__":
    build("1117b", U, "u1117", 35000, tag_letter="u")
