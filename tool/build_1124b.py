#!/usr/bin/env python3
"""2026-11-24 04:02, batch 1124b: 2 couple ("парные") reels P01-P02, 6.77 s, F05 sound.
Built on what works: both of them in the hook, red at the cut, short italic line on top, vitrine pages, pair finale
(K05 18K / L01 70K). Different from M01-M04: the pair mockups come first, and one of the two is the zip hoodie pair.
P01 matching for date night.   COUPLE full frame mirrored; pages: quarter zip pair front, pair back;
                                finale black qz (him) over white qz (her)
P02 one for him, one for her.  SOLES (K01 cut, 68.8 %): his red logo sole + her red soles; pages: HIS black zip hoodie,
                                HERS white zip hoodie; finale zip hoodie pair fronts / backs"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import cat, ARA, ROME
from build_1115 import lb, t
from build_1122 import build

R = [  # key, tone, hook, texts, layout, finale, opts, idea
    ("P01_matching-for-date-night", "vitrine", [lb("COUPLE", speed=1.08, zoom=1.0, crop_y=0.66, flip=True)],
     t("matching for\ndate night."),
     [("p", "PF", cat(1, "HIS  ·  HERS")), ("p", "PB", cat(2, ARA, ROME))], ("KF", "WF", 4), {},
     "couple: COUPLE full frame mirrored; quarter zip pair pages first; finale black over white"),
    ("P02_one-for-him-one-for-her", "vitrine", [lb("SOLES", start=1.55, speed=1.0, zoom=1.05, crop_y=0.6)],
     t("one for him,\none for her."),
     [("p", "ZF", cat(1, "HIS  ·  BLACK")), ("p", "XWF", cat(2, "HERS  ·  WHITE"))], ("ZPF", "ZPB", 4), {},
     "couple: SOLES (his logo sole + her soles); HIS black / HERS white zip hoodie; zip pair finale"),
]

if __name__ == "__main__":
    build("1124b", R, "p1124", 41000, tag="p")
